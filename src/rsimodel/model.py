"""Multisector capacity dynamics with maximin LP allocation.

Self-expansion criterion (per the paper): feasible positive net growth in
EVERY indispensable sector, not aggregate growth. The per-step LP implements
exactly that: maximize the worst-case sector growth rate.

v1 extensions over the v0 scaffold:
- 10 sectors (repair, recycling as explicit service sectors)
- delta decomposed per environment (wear + catastrophic + obsolescence +
  logistics) from params/environments.yaml, anchored where anchors exist
- repair offsets the wear component only; recycling turns retiring capacity
  into secondary mining/refining feed
- vitamin-part stockpiles with shelf life; imports of stockable goods land in
  the stockpile (pulsed for Mars synodic resupply)
- correlated common-cause shocks (Poisson events hitting sector groups)
- per-sector import cutoffs (electronics-class cutoff scenarios)
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, TypedDict

import numpy as np

from .array_types import BoolArray, FloatArray, IntArray, validate_shape
from .delta import (
    DELTA_COMPONENTS,
    Provenance,
    Shock,
    assemble_delta,
    draw_anchors,
    load_anchors,
    load_environment,
    load_shocks,
    resolve_entry,
)
from .solver_adapter import (
    PersistentLinearProgram,
    SparseMatrix,
    minimize_diagonal_quadratic,
    persistent_highs_available,
    solve_identity_quadratic_program,
    solve_linear_program,
    sparse_csc,
    sparse_diagonal,
    sparse_identity,
    sparse_vstack,
)
from .yaml_adapter import (
    load_yaml,
    require_mapping,
    require_number,
    require_sequence,
    require_string,
)

PARAMS_DIR = Path(__file__).resolve().parents[2] / "params"

# Fast path: a persistent warm-started HiGHS model behind the typed solver
# boundary. The public SciPy LP remains the fallback and reference path.
_USE_FAST_LP = persistent_highs_available() and os.environ.get("RSI_SLOW_LP") != "1"


class ShockRng(Protocol):
    """Random operations required by the stochastic shock path."""

    def poisson(self, lam: float, /) -> int: ...

    def uniform(self, low: float, high: float, /) -> float: ...


class AllocationAction(TypedDict):
    """One model step's physical dispatch variables."""

    x: FloatArray
    u: FloatArray
    w: float
    d: FloatArray


class AllocationResult(AllocationAction):
    """Fully diagnosed lexicographic allocation result."""

    g: float
    binding: int
    binding_mask: BoolArray
    binding_responses: FloatArray
    bal_duals: FloatArray


@dataclass
class Params:
    sectors: list[str]
    q: FloatArray  # (n,) output units per capacity unit per year (env-scaled)
    delta_comps: dict[str, FloatArray]  # component -> (n,) fractional loss / yr
    A: FloatArray  # (n, n) A[i, j]: units of i's output to build 1 unit of j capacity
    import_profile: FloatArray  # (n,) shares of import budget
    import_budget0: float
    import_decay_years: float
    # repair / recycling (service sectors)
    repair_eff: float  # capacity-units of wear offset per unit repair output
    repair_spares_fraction: float  # repairing 1 unit draws this fraction of A[:, j]
    scrap_recovery: float  # fraction of retiring capacity recoverable as feed
    salvage_factors: dict[str, FloatArray]  # loss component -> recoverable share (n,)
    recycle_profile: FloatArray  # (n,) where secondary feed lands (sums to 1)
    recycle_opex: FloatArray  # (n,) operating inputs per unit feed produced
    # vitamin-part stockpiles
    stockable: BoolArray  # (n,) bool
    stock_initial_years: float  # years of replacement demand pre-positioned
    stock_capacity_years: float  # max holding, years of replacement demand
    shelf_life: FloatArray  # (n,) years (inf = indefinite)
    # environment
    shocks: list[Shock]
    pulse_years: float | None  # synodic batch period (None = continuous delivery)
    environment: str = "lunar"
    label: str = "central"
    provenance: list[Provenance] = field(
        default_factory=lambda: list[Provenance](),
        repr=False,
    )
    lp_template: tuple[SparseMatrix, slice, SparseMatrix, slice, FloatArray] | None = field(
        default=None,
        init=False,
        repr=False,
    )
    fast_lp_cache: _FastLP | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        n = self.n
        vectors = {
            "q": self.q,
            "import_profile": self.import_profile,
            "recycle_profile": self.recycle_profile,
            "recycle_opex": self.recycle_opex,
            "shelf_life": self.shelf_life,
        }
        for name, vector in vectors.items():
            validate_shape(vector, (n,), name=f"Params.{name}")
        validate_shape(self.stockable, (n,), name="Params.stockable")
        validate_shape(self.A, (n, n), name="Params.A")
        for component, vector in self.delta_comps.items():
            validate_shape(vector, (n,), name=f"Params.delta_comps[{component!r}]")
        for component, vector in self.salvage_factors.items():
            validate_shape(vector, (n,), name=f"Params.salvage_factors[{component!r}]")
        for shock in self.shocks:
            validate_shape(shock.sector_idx, (None,), name=f"Shock[{shock.name!r}].sector_idx")
            if np.any((shock.sector_idx < 0) | (shock.sector_idx >= n)):
                raise ValueError(f"Shock[{shock.name!r}].sector_idx is outside [0, {n})")

    @property
    def n(self) -> int:
        return len(self.sectors)

    @property
    def delta(self) -> FloatArray:
        return sum(self.delta_comps.values(), start=np.zeros(self.n, dtype=float))

    @property
    def wear(self) -> FloatArray:
        return self.delta_comps["wear"]

    def idx(self, name: str) -> int:
        return self.sectors.index(name)


def load_params(
    set_name: str = "central",
    env: str = "lunar",
    path: Path | None = None,
    anchor_draws: Mapping[str, float] | None = None,
    rng: np.random.Generator | None = None,
) -> Params:
    """Build Params from an assumption set x environment.

    anchor_draws/rng are the Monte Carlo hooks: pass draws from
    delta.draw_anchors(anchors, rng) to sample anchored ranges; rng also
    jitters shock rates. Deterministic (geometric-mid anchors) when omitted.
    """
    source = path or PARAMS_DIR / "assumptions.yaml"
    raw = require_mapping(load_yaml(source), label=str(source))
    sectors = [
        require_string(item, label=f"{source}.sectors[{index}]")
        for index, item in enumerate(
            require_sequence(raw.get("sectors"), label=f"{source}.sectors")
        )
    ]
    raw_sets = require_mapping(raw.get("sets"), label=f"{source}.sets")
    selected = require_mapping(raw_sets.get(set_name), label=f"{source}.sets.{set_name}")
    inherited = selected.get("inherit")
    if inherited is None:
        base = selected
        base_label = f"{source}.sets.{set_name}"
    else:
        inherited_name = require_string(
            inherited,
            label=f"{source}.sets.{set_name}.inherit",
        )
        base = require_mapping(
            raw_sets.get(inherited_name),
            label=f"{source}.sets.{inherited_name}",
        )
        base_label = f"{source}.sets.{inherited_name}"
    selected_label = f"{source}.sets.{set_name}"

    def number(
        mapping: Mapping[str, object],
        key: str,
        *,
        label: str,
        default: float | None = None,
    ) -> float:
        value = mapping.get(key)
        if value is None:
            if default is None:
                raise ValueError(f"{label}.{key}: missing required number")
            return default
        return require_number(value, label=f"{label}.{key}")

    def number_sequence(value: object, *, label: str) -> list[float]:
        return [
            require_number(item, label=f"{label}[{index}]")
            for index, item in enumerate(require_sequence(value, label=label))
        ]

    base_q = number_sequence(base.get("q"), label=f"{base_label}.q")
    base_matrix = [
        number_sequence(row, label=f"{base_label}.A[{index}]")
        for index, row in enumerate(require_sequence(base.get("A"), label=f"{base_label}.A"))
    ]
    if len(base_q) != len(sectors):
        raise ValueError(f"{base_label}.q: expected {len(sectors)} entries")
    if len(base_matrix) != len(sectors) or any(len(row) != len(sectors) for row in base_matrix):
        raise ValueError(f"{base_label}.A: expected a {len(sectors)}×{len(sectors)} matrix")

    env_cfg = load_environment(env)
    anchors = load_anchors()
    draws = anchor_draws if anchor_draws is not None else draw_anchors(anchors)
    comps, prov = assemble_delta(env_cfg, sectors, anchors, draws)
    scale_delta = number(selected, "scale_delta", label=selected_label, default=1.0)
    comps = {k: v * scale_delta for k, v in comps.items()}

    q_scale = np.empty(len(sectors))
    for i, entry in enumerate(env_cfg.q_scale):
        q_scale[i], pr = resolve_entry(entry, draws, anchors, f"q_scale[{sectors[i]}]")
        prov.append(pr)
    q = np.array(base_q, dtype=float) * q_scale
    A = np.array(base_matrix, dtype=float) * number(
        selected,
        "scale_A",
        label=selected_label,
        default=1.0,
    )

    imp = env_cfg.import_config
    base_import_profile = number_sequence(
        base.get("import_profile"),
        label=f"{base_label}.import_profile",
    )
    profile = np.array(imp.profile or base_import_profile, dtype=float)
    budget0 = (
        number(
            selected,
            "import_budget0",
            label=selected_label,
            default=number(base, "import_budget0", label=base_label),
        )
        * imp.budget_scale
    )
    decay = (
        number(
            selected,
            "import_decay_years",
            label=selected_label,
            default=number(base, "import_decay_years", label=base_label),
        )
        * imp.decay_scale
    )

    repair = require_mapping(base.get("repair"), label=f"{base_label}.repair")
    recycling = require_mapping(base.get("recycling"), label=f"{base_label}.recycling")
    stockpile = require_mapping(base.get("stockpile"), label=f"{base_label}.stockpile")
    recovery_profile = number_sequence(
        recycling.get("output_profile"),
        label=f"{base_label}.recycling.output_profile",
    )
    recycling_opex = number_sequence(
        recycling.get("opex"),
        label=f"{base_label}.recycling.opex",
    )
    stockable_values = number_sequence(
        stockpile.get("stockable"),
        label=f"{base_label}.stockpile.stockable",
    )
    if any(value not in (0.0, 1.0) for value in stockable_values):
        raise ValueError(f"{base_label}.stockpile.stockable: expected only 0 or 1")
    shelf_life = number_sequence(
        stockpile.get("shelf_life_years"),
        label=f"{base_label}.stockpile.shelf_life_years",
    )
    salvage_cfg = env_cfg.salvage_factors
    salvage: dict[str, FloatArray] = {}
    salvage_defaults = {
        "wear": 1.0,
        "catastrophic": 0.0,
        "obsolescence": 1.0,
        "logistics": 0.0,
    }
    for comp in DELTA_COMPONENTS:
        raw_factor = salvage_cfg.get(comp, salvage_defaults[comp])
        entries = raw_factor if isinstance(raw_factor, tuple) else (raw_factor,) * len(sectors)
        if len(entries) != len(sectors):
            raise ValueError(
                f"salvage_factors.{comp}: expected {len(sectors)} entries, got {len(entries)}"
            )
        salvage[comp] = np.empty(len(sectors))
        for i, entry in enumerate(entries):
            salvage[comp][i], pr = resolve_entry(
                entry, draws, anchors, f"salvage.{comp}[{sectors[i]}]"
            )
            if not 0.0 <= salvage[comp][i] <= 1.0:
                raise ValueError(f"salvage_factors.{comp}[{sectors[i]}] must be in [0,1]")
            prov.append(pr)
    stock_scale = number(selected, "scale_stock", label=selected_label, default=1.0)
    return Params(
        sectors=sectors,
        q=q,
        delta_comps=comps,
        A=A,
        import_profile=profile,
        import_budget0=budget0,
        import_decay_years=decay,
        repair_eff=number(repair, "efficiency", label=f"{base_label}.repair")
        * number(
            selected,
            "scale_repair_efficiency",
            label=selected_label,
            default=1.0,
        ),
        repair_spares_fraction=number(
            repair,
            "spares_fraction",
            label=f"{base_label}.repair",
        ),
        scrap_recovery=min(
            1.0,
            number(
                recycling,
                "scrap_recovery",
                label=f"{base_label}.recycling",
            )
            * number(
                selected,
                "scale_scrap_recovery",
                label=selected_label,
                default=1.0,
            ),
        ),
        salvage_factors=salvage,
        recycle_profile=np.array(recovery_profile, dtype=float),
        recycle_opex=np.array(recycling_opex, dtype=float),
        stockable=np.array(stockable_values, dtype=bool),
        stock_initial_years=number(
            stockpile,
            "initial_years",
            label=f"{base_label}.stockpile",
        )
        * stock_scale,
        stock_capacity_years=number(
            stockpile,
            "capacity_years",
            label=f"{base_label}.stockpile",
        )
        * stock_scale,
        shelf_life=np.array(shelf_life, dtype=float),
        shocks=load_shocks(env_cfg, sectors, rng),
        pulse_years=imp.pulse_years,
        environment=env,
        label=set_name,
        provenance=prov,
    )


def imports_at(
    p: Params, t: float, cutoff_year: float | None = None, cutoff_idx: IntArray | None = None
) -> FloatArray:
    """Earth supply rate by sector at time t (output units / yr).

    cutoff_idx selects WHICH sectors are cut at cutoff_year (None = all):
    the electronics-class cutoff scenario is cutoff_idx=[electronics].
    """
    m = p.import_budget0 * np.exp(-t / p.import_decay_years) * p.import_profile
    if cutoff_year is not None and t >= cutoff_year:
        if cutoff_idx is None:
            m[:] = 0.0
        else:
            m[cutoff_idx] = 0.0
    return m


def replacement_demand(p: Params, K: FloatArray) -> FloatArray:
    """Output units of each sector needed per year just to replace retiring capacity."""
    return p.A @ (p.delta * K)


def recoverable_retirement(
    p: Params, K: FloatArray, wear_repair: FloatArray | None = None
) -> float:
    """Gross retiring capacity physically available to the recycling process.

    Depreciation is not synonymous with scrap. Wear retirement and planned
    obsolescence are usually recoverable; catastrophic and logistics losses
    use environment-specific availability factors. Repair offsets wear before
    retirement, so repaired capacity cannot simultaneously enter the scrap
    stream. ``scrap_recovery`` is applied separately as the processing yield.
    """
    total = 0.0
    for comp, delta in p.delta_comps.items():
        retired = delta * K
        if comp == "wear" and wear_repair is not None:
            retired = np.maximum(retired - wear_repair, 0.0)
        total += float(np.sum(p.salvage_factors[comp] * retired))
    return total


def _lp_templates(
    p: Params,
) -> tuple[SparseMatrix, slice, SparseMatrix, slice, FloatArray]:
    """Constant sparse constraint templates for allocate_step, cached on the
    Params instance. The matrix is constant except the growth rows' g-column
    entries (K_j) and the stage-3 normalized-draw row."""
    tpl = p.lp_template
    if tpl is not None:
        return tpl
    n = p.n
    iw, ir = p.idx("recycling"), p.idx("repair")
    nv = 3 * n + 2
    sx, su, swv, sd, sg = 0, n, 2 * n, 2 * n + 1, 3 * n + 1
    M = np.zeros((3 * n + 1, nv))
    for j in range(n):
        M[j, sx + j] = -1.0  # growth rows
        M[j, su + j] = -1.0
        M[j, sg] = 1.0  # placeholder: set to K_j each step
        M[n + j, su + j] = 1.0  # wear caps
    for i in range(n):  # material balance
        r = M[2 * n + i]
        r[sx : sx + n] = p.A[i]
        r[su : su + n] = p.repair_spares_fraction * p.A[i]
        if i == ir:
            r[su : su + n] += 1.0 / p.repair_eff
        if i == iw:
            r[swv] += 1.0
        r[swv] += p.recycle_opex[i] - p.recycle_profile[i]
        r[sd + i] = -1.0
    M[3 * n, swv] = 1.0  # scrap cap
    M[3 * n, su : su + n] = p.scrap_recovery * p.salvage_factors["wear"]
    A1 = sparse_csc(M)
    pin = np.zeros((1, nv))
    pin[0, sg] = -1.0  # stages 2/3: hold g at its optimum
    draw = np.zeros((1, nv))
    draw[0, sd : sd + n] = 1.0  # stage 3: hold normalized draw optimum
    A3 = sparse_csc(np.vstack([M, pin, draw]))
    s1 = slice(A1.indptr[sg], A1.indptr[sg] + n)
    s3 = slice(A3.indptr[sg], A3.indptr[sg] + n)
    # csc stores each column's rows sorted, so the growth rows 0..n-1 are the
    # first n entries of column sg in both templates.
    if not (A1.indices[s1] == np.arange(n)).all():
        raise RuntimeError("stage-1 LP template has an invalid growth-column layout")
    if not (A3.indices[s3] == np.arange(n)).all():
        raise RuntimeError("stage-3 LP template has an invalid growth-column layout")
    bal = M[2 * n : 3 * n].copy()  # dense balance block (slack fallback)
    tpl = (A1, s1, A3, s3, bal)
    p.lp_template = tpl
    return tpl


def _draw_weights(p: Params, supply: FloatArray, stock_avail: FloatArray) -> FloatArray:
    """Dimensionless stock-draw objective weights.

    Raw ``sum(d)`` compares unlike sector output units. Dividing each draw rate
    by a same-unit state scale makes stage 2 invariant to row-unit changes.
    """
    scale = np.maximum(np.maximum(np.abs(supply), np.abs(stock_avail)), 1e-12)
    weights = np.where(p.stockable, 1.0 / scale, 0.0)
    peak = float(np.max(weights))
    return weights / peak if peak > 0.0 else weights


def _qp_diagonal(
    p: Params, K: FloatArray, supply: FloatArray, stock_avail: FloatArray
) -> FloatArray:
    """Positive diagonal for the strictly convex stage-3 tie-break.

    Every action is normalized by a same-unit state quantity. The growth
    equalities and fixed stage-1/stage-2 optima define the economic policy; this
    quadratic only selects one unique action on that optimal face.
    """
    n = p.n
    nv = 3 * n + 2
    sd, sg = 2 * n + 1, 3 * n + 1
    diag = np.ones(nv)
    # A nearly destroyed sector can have K many orders below the rest. A
    # relative floor prevents the otherwise equivalent QP from becoming
    # numerically ill-conditioned while preserving a strictly positive weight.
    build_floor = max(float(np.max(np.abs(K))) * 1e-3, 1e-12)
    build_scale = np.maximum(np.abs(K), build_floor)
    diag[:n] = 2.0 / build_scale**2
    diag[n : 2 * n] = 2.0 / build_scale**2
    scrap_scale = max(recoverable_retirement(p, K), build_floor)
    diag[2 * n] = 2.0 / scrap_scale**2
    draw_floor = max(
        float(np.max(np.maximum(np.abs(supply), np.abs(stock_avail)))) * 1e-3,
        1e-12,
    )
    draw_scale = np.maximum(np.maximum(np.abs(supply), np.abs(stock_avail)), draw_floor)
    diag[sd : sd + n] = 2.0
    active_draw = p.stockable & (stock_avail > 1e-10)
    diag[sd : sd + n][active_draw] = 2.0 / draw_scale[active_draw] ** 2
    diag[sg] = 2.0  # fixed by equality; positive keeps the Hessian strict
    return diag


def _unique_stage3(
    p: Params,
    K: FloatArray,
    supply: FloatArray,
    stock_avail: FloatArray,
    b_ub: FloatArray,
    g_star: float,
    draw_weights: FloatArray,
    draw_star: float,
    z_start: FloatArray,
) -> FloatArray:
    """Select one unique point on the stage-1/stage-2 optimal face.

    OSQP is used here rather than SciPy's private HiGHS QP binding. The latter
    can misclassify the narrow face as infeasible when a capacity is nearly
    zero, even when initialized with the feasible stage-2 LP solution.
    """
    n = p.n
    nv = 3 * n + 2
    sd, sg = 2 * n + 1, 3 * n + 1
    A1, s1, _, _, _ = _lp_templates(p)
    A1.data[s1] = K

    draw_row = np.zeros(nv)
    draw_row[sd : sd + n] = draw_weights
    qdiag = _qp_diagonal(p, K, supply, stock_avail)
    # Solve in normalized variables y with z = scale*y. This turns the
    # normalized quadratic into an identity Hessian and prevents large/small
    # sector units from degrading the ADMM feasibility test.
    variable_scale = 1.0 / np.sqrt(qdiag)
    core_z = sparse_vstack([A1, sparse_csc(draw_row.reshape(1, -1))])
    core_y = core_z @ sparse_diagonal(variable_scale)
    A_osqp = sparse_vstack([core_y, sparse_identity(nv)])
    g_tol = 1e-5 * max(1.0, abs(g_star))
    draw_tol = 1e-5 * max(1.0, abs(draw_star))
    lower_var = np.zeros(nv)
    upper_var = np.full(nv, np.inf)
    lower_var[sg], upper_var[sg] = g_star - g_tol, g_star
    for i in range(n):
        upper_var[sd + i] = float(stock_avail[i]) if p.stockable[i] else 0.0
    lower_var_y = lower_var / variable_scale
    upper_var_y = upper_var / variable_scale
    lower = np.concatenate(
        [
            np.full(len(b_ub), -np.inf),
            [draw_star - draw_tol],
            lower_var_y,
        ]
    )
    upper = np.concatenate(
        [
            b_ub,
            [draw_star + draw_tol],
            upper_var_y,
        ]
    )
    result = solve_identity_quadratic_program(
        A_osqp,
        lower,
        upper,
        np.asarray(z_start, float) / variable_scale,
    )
    primal_violation = max(
        float(np.max(A_osqp @ result.x - upper)),
        float(np.max(lower - A_osqp @ result.x)),
    )
    if result.status_value not in (1, 2) and primal_violation > 1e-3:
        # OSQP's infeasibility certificates can be unreliable on an
        # exceptionally narrow, badly scaled optimal face. SLSQP is slower but
        # starts from the feasible stage-2 LP vertex and supplies an independent
        # public-solver fallback for these rare states.
        core = core_z.tocsr()
        core_lower = np.concatenate([np.full(len(b_ub), -np.inf), [draw_star - draw_tol]])
        core_upper = np.concatenate([b_ub, [draw_star + draw_tol]])
        qdiag = qdiag / float(np.max(qdiag))
        fallback = minimize_diagonal_quadratic(
            qdiag,
            np.clip(np.asarray(z_start, float), lower_var, upper_var),
            lower_var,
            upper_var,
            core,
            core_lower,
            core_upper,
        )
        fallback_violation = max(
            float(np.max(core @ fallback.x - core_upper)),
            float(np.max(core_lower - core @ fallback.x)),
        )
        if not fallback.success and fallback_violation > 1e-3:
            raise RuntimeError(
                f"stage-3 QP failed in OSQP ({result.status}) and "
                f"SLSQP ({fallback.message}); "
                f"primal violation={fallback_violation:.3g}"
            )
        z = np.asarray(fallback.x, float)
    else:
        z = np.asarray(result.x, float) * variable_scale
    # Remove solver-tolerance dust at explicit variable bounds.
    z[: 3 * n + 1] = np.maximum(z[: 3 * n + 1], 0.0)
    z[n : 2 * n] = np.minimum(z[n : 2 * n], p.wear * K)
    for i in range(n):
        cap = upper_var[sd + i]
        z[sd + i] = np.clip(z[sd + i], 0.0, cap)
    return z


def _binding_from_responses(
    responses: FloatArray,
    bal: FloatArray,
    z: FloatArray,
    supply: FloatArray,
) -> tuple[int, BoolArray]:
    """Primary binding index plus a co-binding mask.

    ``responses[i]`` is the finite change in stage-1 g when balance-row supply
    i is relaxed by one percent. Rows within 5% of the largest positive
    response co-bind. If no material row has a positive response, normalized
    slack supplies a unit-invariant fallback diagnostic.
    """
    peak = float(np.max(responses))
    if peak > 1e-12:
        tol = max(1e-10, 0.05 * peak)
        mask = responses >= peak - tol
        return int(np.argmax(responses)), mask
    slack = supply - bal @ z
    rel = slack / np.maximum(np.abs(supply), 1e-12)
    floor = float(np.min(rel))
    tol = max(1e-10, 0.01 * max(abs(floor), 1e-12))
    mask = rel <= floor + tol
    return int(np.flatnonzero(mask)[0]), mask


class _FastLP:
    """Persistent HiGHS LP/QP pair for the three-stage allocation policy.

    Stage 1 maximizes g. Stage 2 fixes g and minimizes normalized stock draw.
    Stage 3 fixes both optima and solves a strictly convex normalized QP. This
    makes the complete action and therefore the state transition unique even
    when some growth-floor inequalities are necessarily slack. One-percent
    finite balance-row perturbations provide a unit-invariant co-binding
    diagnostic.
    """

    def __init__(self, p: Params) -> None:
        _, _, A3, _, bal = _lp_templates(p)
        n = p.n
        self.p, self.n = p, n
        nv, nr = 3 * n + 2, 3 * n + 3
        self.nv, self.nr = nv, nr
        self.sd, self.sg = 2 * n + 1, 3 * n + 1
        self.pin_row, self.draw_row = 3 * n + 1, 3 * n + 2
        self.bal = bal
        self.c = np.zeros(nv)
        self.c[self.sg] = -1.0
        self._all_cols = np.arange(nv, dtype=np.int32)
        column_lower = np.zeros(nv)
        column_upper = np.full(nv, np.inf)
        column_lower[self.sg], column_upper[self.sg] = -np.inf, np.inf
        row_lower = np.full(nr, -np.inf)
        row_upper = np.zeros(nr)
        row_upper[-2:] = np.inf
        self.h = PersistentLinearProgram(
            objective=self.c,
            column_lower=column_lower,
            column_upper=column_upper,
            row_lower=row_lower,
            row_upper=row_upper,
            matrix=A3,
        )
        self.INF = self.h.infinity

    def _set_state(
        self,
        model: PersistentLinearProgram,
        K: FloatArray,
        b_ub: FloatArray,
        stock_avail: FloatArray,
    ) -> None:
        n, sd, sg, INF = self.n, self.sd, self.sg, self.INF
        for j in range(n):
            model.change_coefficient(j, sg, float(K[j]))
        for i in range(3 * n + 1):
            model.change_row_bounds(i, -INF, float(b_ub[i]))
        for i in range(n):
            cap = float(stock_avail[i]) if self.p.stockable[i] else 0.0
            model.change_column_bounds(sd + i, 0.0, cap)

    def step(
        self,
        K: FloatArray,
        m_direct: FloatArray,
        stock_avail: FloatArray,
    ) -> AllocationResult:
        p, n, h, INF = self.p, self.n, self.h, self.INF
        sd, sg = self.sd, self.sg
        supply = p.q * K + m_direct
        b_ub = np.concatenate(
            [-p.delta * K, p.wear * K, supply, [p.scrap_recovery * recoverable_retirement(p, K)]]
        )
        self._set_state(h, K, b_ub, stock_avail)
        h.change_costs(self._all_cols, self.c)
        h.change_row_bounds(self.pin_row, -INF, INF)
        h.change_row_bounds(self.draw_row, -INF, INF)
        h.run()
        if not h.is_optimal():  # pragma: no cover
            raise RuntimeError(f"HiGHS: {h.status()}")
        z1 = h.solution().columns
        g_star = float(z1[sg])

        # Unit-invariant binding response: relax each material supply by 1%.
        responses = np.zeros(n)
        for i in range(n):
            row = 2 * n + i
            relaxed = float(supply[i] + 0.01 * max(abs(supply[i]), 1e-12))
            h.change_row_bounds(row, -INF, relaxed)
            h.run()
            if h.is_optimal():
                responses[i] = max(0.0, float(h.solution().columns[sg]) - g_star)
            h.change_row_bounds(row, -INF, float(supply[i]))
        h.run()  # restore the unperturbed optimum before stage 2
        restored = h.solution()
        z1 = restored.columns
        bal_duals = -restored.row_duals[2 * n : 3 * n]

        # Stage 2: exact g pin + dimensionless stock-draw objective.
        draw_weights = _draw_weights(p, supply, stock_avail)
        c2 = np.zeros(self.nv)
        c2[sd : sd + n] = draw_weights
        h.change_costs(self._all_cols, c2)
        g_tol = 1e-5 * max(1.0, abs(g_star))
        # HiGHS' stage-1 optimum can sit a few ulps above the feasible face.
        # Keep stage 2 within solver tolerance below g*, never above it.
        h.change_row_bounds(self.pin_row, -INF, -g_star + g_tol)
        h.run()
        if not h.is_optimal():
            raise RuntimeError("HiGHS stage-2 normalized-draw LP failed")
        z2 = h.solution().columns
        draw_star = float(np.dot(draw_weights, z2[sd : sd + n]))

        try:
            z = _unique_stage3(
                p,
                K,
                supply,
                stock_avail,
                b_ub,
                g_star,
                draw_weights,
                draw_star,
                z2,
            )
        except RuntimeError:
            # Long warm-start sequences with repeated RHS perturbations can
            # occasionally leave the private persistent HiGHS interface on a
            # numerically degraded basis. Re-solve once through the public,
            # cold SciPy reference path and replace the persistent model.
            result = _allocate_scipy(p, K, m_direct, stock_avail)
            p.fast_lp_cache = _FastLP(p)
            return result
        z[sg] = g_star
        x, u, w, d, g = z[0:n], z[n : 2 * n], z[2 * n], z[sd : sd + n], z[sg]
        binding, binding_mask = _binding_from_responses(responses, self.bal, z, supply)
        return {
            "x": x,
            "u": u,
            "w": w,
            "d": d,
            "g": g,
            "binding": binding,
            "binding_mask": binding_mask,
            "binding_responses": responses,
            "bal_duals": bal_duals,
        }


def allocate_step(
    p: Params,
    K: FloatArray,
    m_direct: FloatArray,
    stock_avail: FloatArray,
) -> AllocationResult:
    """Maximin LP over one step — dispatches to the persistent-HiGHS fast
    path (default) or the scipy.linprog reference path (RSI_SLOW_LP=1, or
    when scipy's bundled highspy is unavailable). Both solve the identical
    LP; see _allocate_scipy for the constraint documentation."""
    if _USE_FAST_LP:
        fast = p.fast_lp_cache
        if fast is None:
            fast = _FastLP(p)
            p.fast_lp_cache = fast
        return fast.step(K, m_direct, stock_avail)
    return _allocate_scipy(p, K, m_direct, stock_avail)


def _allocate_scipy(
    p: Params, K: FloatArray, m_direct: FloatArray, stock_avail: FloatArray
) -> AllocationResult:
    """Maximin LP over one step. Variables z = [x (n), u (n), w, d (n), g]:
      x_j  gross builds of sector j capacity
      u_j  wear offset via repair (u_j <= wear_j K_j)
      w    recycling activity (secondary feed produced / yr)
      d_i  stockpile drawdown rate (stockable i only)
      g    growth floor (maximized)

    maximize g s.t.
      x_j + u_j - delta_j K_j >= g K_j                                (growth, all j)
      A@x + sf*(A@u) + [repair row: sum(u)/eff] + [recycle row: w]
          + opex*w - recycle_profile*w - d  <=  q*K + m_direct        (material balance)
      w <= scrap_recovery * recoverable_retirement(K, u)              (scrap cap)
      d_i <= stock_avail_i                                            (drawdown cap)

    Stage 2 fixes g exactly and minimizes dimensionless stock draw. Stage 3
    fixes both prior optima and minimizes a strictly convex normalized
    quadratic over all actions, producing a unique state transition.

    Binding responses are one-percent finite supply relaxations, with co-binding
    rows reported within five percent of the largest positive response.
    """
    n = p.n
    nv = 3 * n + 2
    sd, sg = 2 * n + 1, 3 * n + 1
    A1, s1, _, _, bal = _lp_templates(p)

    c = np.zeros(nv)
    c[sg] = -1.0

    # constraint order (template rows): growth (n) | wear caps (n) |
    # material balance (n) | scrap cap (1) — only the g-column K_j entries
    # and this RHS vary with the state
    A1.data[s1] = K
    supply = p.q * K + m_direct
    b_ub = np.concatenate(
        [
            -p.delta * K,  # growth rows
            p.wear * K,  # wear caps
            supply,  # material balance
            [p.scrap_recovery * recoverable_retirement(p, K)],  # scrap cap
        ]
    )

    bounds: list[tuple[float | None, float | None]] = [(0.0, None) for _ in range(3 * n + 1)]
    bounds.append((None, None))
    for i in range(n):
        cap = float(stock_avail[i]) if p.stockable[i] else 0.0
        bounds[sd + i] = (0, cap)

    res = solve_linear_program(c, a_ub=A1, b_ub=b_ub, bounds=bounds)
    if not res.success:  # pragma: no cover — feasible with x=u=w=d=0, g <= -max(delta)
        raise RuntimeError(f"LP failed: {res.message}")
    z1 = res.x
    g_star = float(z1[sg])
    if res.inequality_marginals is None:
        raise RuntimeError("LP did not return inequality marginals")
    bal_duals = -res.inequality_marginals[2 * n : 3 * n]

    responses = np.zeros(n)
    for i in range(n):
        perturbed = b_ub.copy()
        perturbed[2 * n + i] += 0.01 * max(abs(supply[i]), 1e-12)
        rp = solve_linear_program(c, a_ub=A1, b_ub=perturbed, bounds=bounds)
        if rp.success:
            responses[i] = max(0.0, float(rp.x[sg]) - g_star)

    draw_weights = _draw_weights(p, supply, stock_avail)
    c2 = np.zeros(nv)
    c2[sd : sd + n] = draw_weights
    g_tol = 1e-5 * max(1.0, abs(g_star))
    bounds2 = list(bounds)
    bounds2[sg] = (g_star - g_tol, g_star)
    res2 = solve_linear_program(
        c2,
        a_ub=A1,
        b_ub=b_ub,
        bounds=bounds2,
        options={"presolve": False},
    )
    if not res2.success:
        raise RuntimeError(f"stage-2 LP failed: {res2.message}")
    z2 = res2.x
    draw_star = float(np.dot(draw_weights, z2[sd : sd + n]))

    z = _unique_stage3(
        p,
        K,
        supply,
        stock_avail,
        b_ub,
        g_star,
        draw_weights,
        draw_star,
        z2,
    )
    z[sg] = g_star
    sx, su, swv = 0, n, 2 * n
    x, u, w, d, g = z[sx : sx + n], z[su : su + n], z[swv], z[sd : sd + n], z[sg]
    binding, binding_mask = _binding_from_responses(responses, bal, z, supply)
    return {
        "x": x,
        "u": u,
        "w": w,
        "d": d,
        "g": g,
        "binding": binding,
        "binding_mask": binding_mask,
        "binding_responses": responses,
        "bal_duals": bal_duals,
    }


@dataclass
class RunResult:
    t: FloatArray  # (T,)
    K: FloatArray  # (T, n)
    g: FloatArray  # (T,) realized worst-sector net growth, incl. shocks
    binding: IntArray  # (T,) index of binding sector
    S: FloatArray  # (T, n) stockpile levels (output units)
    shock_log: list[tuple[float, str, float]]  # (t, shock name, fraction lost)
    params: Params = field(repr=False)
    K0: FloatArray = field(repr=False)  # supplied initial K (pre-step)
    g_alloc: FloatArray | None = field(repr=False, default=None)
    co_binding: BoolArray | None = field(repr=False, default=None)  # (T,n) bool

    def self_expanding_at(self, year: float) -> bool:
        """Positive realized worst-sector net growth in the step ending at year."""
        i = min(int(np.searchsorted(self.t, year)), len(self.g) - 1)
        return bool(self.g[i] > 0)

    def allocatively_expanding_at(self, year: float) -> bool:
        """Positive pre-shock LP growth capacity at the step ending at year."""
        series = self.g if self.g_alloc is None else self.g_alloc
        i = min(int(np.searchsorted(self.t, year)), len(series) - 1)
        return bool(series[i] > 0)

    def sustained_expanding(self, start: float, end: float) -> bool:
        """Realized g(t) > 0 in every complete step whose end is in (start,end]."""
        mask = (self.t > start + 1e-9) & (self.t <= end + 1e-9)
        return bool(mask.any() and np.all(self.g[mask] > 0))

    def _K0(self) -> FloatArray:
        return self.K0

    def lambda_series(self) -> FloatArray:
        """Balanced system scale λ(t) = min_j K_j(t)/K_j(0).

        Invariant to each sector's arbitrary capacity unit (a unit rescaling
        cancels in the ratio), unlike sum(K). λ ≥ 2 means every sector has at
        least doubled in the abstract continuous-capacity model."""
        return (self.K / np.maximum(self._K0(), 1e-30)).min(axis=1)

    def balanced_doubling_time(self) -> float | None:
        """Unit-invariant replication time: first t with λ(t) ≥ 2 (every
        sector doubled), if reached. This is a balanced-capacity event, not a
        commissioned second physical seed."""
        lam = self.lambda_series()
        idx = np.argmax(lam >= 2.0)
        return float(self.t[idx]) if lam[idx] >= 2.0 else None

    def doubling_time(self) -> float | None:
        """AGGREGATE ABSTRACT-CAPACITY doubling: years for sum_j K_j to double.

        NOT unit-invariant — sector capacities are in arbitrary units, so this
        sum depends on unit conventions and can be reached by overbuilding easy
        sectors while a hard sector lags (review correction). Kept for continuity;
        balanced_doubling_time() is the defensible replication metric.
        Compares against the SUPPLIED K0, not the first post-step record."""
        tot = self.K.sum(axis=1)
        tot0 = float(self._K0().sum())
        idx = np.argmax(tot >= 2 * tot0)
        return float(self.t[idx]) if tot[idx] >= 2 * tot0 else None


def run(
    p: Params,
    K0: FloatArray | None = None,
    years: float = 40.0,
    dt: float = 0.25,
    cutoff_year: float | None = None,
    cutoff_sectors: list[str] | None = None,
    rng: np.random.Generator | ShockRng | None = None,
) -> RunResult:
    """Integrate the system. rng=None disables stochastic shocks (deterministic
    baseline); pass a Generator to sample common-cause events.
    cutoff_sectors names which sectors' imports stop at cutoff_year (None = all).
    """
    n = p.n
    if K0 is not None:
        validate_shape(K0, (n,), name="run.K0")
    capacity = np.full(n, 1.0) if K0 is None else K0.astype(float).copy()
    initial_capacity = capacity.copy()
    cutoff_idx = (
        None if cutoff_sectors is None else np.array([p.idx(s) for s in cutoff_sectors], int)
    )

    rep0 = replacement_demand(p, capacity)
    stock = np.where(p.stockable, p.stock_initial_years * rep0, 0.0)

    steps = round(years / dt)
    times: list[float] = []
    capacities: list[FloatArray] = []
    realized_growth: list[float] = []
    allocated_growth: list[float] = []
    binding_sectors: list[int] = []
    co_binding_masks: list[BoolArray] = []
    stock_history: list[FloatArray] = []
    shock_log: list[tuple[float, str, float]] = []
    next_pulse = 0.0
    for s_i in range(steps):
        t = s_i * dt
        m = imports_at(p, t, cutoff_year, cutoff_idx)
        m_stock = np.where(p.stockable, m, 0.0)
        m_direct = m - m_stock
        # deliveries: continuous trickle into the stockpile, or synodic batches
        if p.pulse_years is None:
            inflow = m_stock * dt
        else:
            inflow = np.zeros(n)
            if t + dt > next_pulse - 1e-9:
                inflow = m_stock * p.pulse_years  # one synodic batch
                next_pulse += p.pulse_years

        a = allocate_step(p, capacity, m_direct, stock / dt)
        previous_capacity = capacity.copy()
        capacity = np.maximum(
            capacity + dt * (a["x"] + a["u"] - p.delta * capacity),
            1e-9,
        )
        # Stock flow is computed during the step. Its capacity clip is applied
        # after shocks so a damaged system cannot retain a pre-shock warehouse.
        stock = stock + inflow - a["d"] * dt - stock * dt / p.shelf_life

        if rng is not None:
            for sh in p.shocks:
                for _ in range(rng.poisson(sh.rate_per_year * dt)):
                    frac = rng.uniform(*sh.fraction_lost)
                    capacity[sh.sector_idx] *= 1.0 - frac
                    shock_log.append((t + dt, sh.name, frac))

        cap = p.stock_capacity_years * replacement_demand(p, capacity)
        stock = np.clip(
            stock,
            0.0,
            np.where(p.stockable, np.maximum(cap, 1e-9), 0.0),
        )
        g_real = float(
            np.min((capacity - previous_capacity) / (dt * np.maximum(previous_capacity, 1e-30)))
        )

        times.append(t + dt)
        capacities.append(capacity.copy())
        realized_growth.append(g_real)
        allocated_growth.append(a["g"])
        binding_sectors.append(a["binding"])
        co_binding_masks.append(a["binding_mask"].copy())
        stock_history.append(stock.copy())
    return RunResult(
        np.asarray(times, dtype=float),
        np.asarray(capacities, dtype=float),
        np.asarray(realized_growth, dtype=float),
        np.asarray(binding_sectors, dtype=np.int64),
        np.asarray(stock_history, dtype=float),
        shock_log,
        g_alloc=np.asarray(allocated_growth, dtype=float),
        co_binding=np.asarray(co_binding_masks, dtype=bool),
        params=p,
        K0=initial_capacity,
    )
