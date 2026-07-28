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
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml
from scipy.optimize import linprog

from .delta import (DELTA_COMPONENTS, Provenance, Shock, assemble_delta, draw_anchors,
                    load_anchors, load_environment, load_shocks, resolve_entry)

PARAMS_DIR = Path(__file__).resolve().parents[2] / "params"

# Fast path: a persistent warm-started HiGHS model via the highspy
# bindings that scipy bundles (pinned scipy==1.16.0 in requirements.lock;
# the module is private to scipy, so guard the import and keep the
# scipy.linprog path as fallback + reference implementation).
try:
    from scipy.optimize._highspy import _core as _hcore
except Exception:  # pragma: no cover — older/newer scipy layout
    _hcore = None
_USE_FAST_LP = _hcore is not None and os.environ.get("RSI_SLOW_LP") != "1"


@dataclass
class Params:
    sectors: list[str]
    q: np.ndarray                 # (n,) output units per capacity unit per year (env-scaled)
    delta_comps: dict[str, np.ndarray]  # component -> (n,) fractional loss / yr
    A: np.ndarray                 # (n, n) A[i, j]: units of i's output to build 1 unit of j capacity
    import_profile: np.ndarray    # (n,) shares of import budget
    import_budget0: float
    import_decay_years: float
    # repair / recycling (service sectors)
    repair_eff: float             # capacity-units of wear offset per unit repair output
    repair_spares_fraction: float # repairing 1 unit draws this fraction of A[:, j]
    scrap_recovery: float         # fraction of retiring capacity recoverable as feed
    salvage_factors: dict[str, np.ndarray]  # loss component -> recoverable share (n,)
    recycle_profile: np.ndarray   # (n,) where secondary feed lands (sums to 1)
    recycle_opex: np.ndarray      # (n,) operating inputs per unit feed produced
    # vitamin-part stockpiles
    stockable: np.ndarray         # (n,) bool
    stock_initial_years: float    # years of replacement demand pre-positioned
    stock_capacity_years: float   # max holding, years of replacement demand
    shelf_life: np.ndarray        # (n,) years (inf = indefinite)
    # environment
    shocks: list[Shock]
    pulse_years: float | None     # synodic batch period (None = continuous delivery)
    environment: str = "lunar"
    label: str = "central"
    provenance: list[Provenance] = field(default_factory=list, repr=False)

    @property
    def n(self) -> int:
        return len(self.sectors)

    @property
    def delta(self) -> np.ndarray:
        return sum(self.delta_comps.values())

    @property
    def wear(self) -> np.ndarray:
        return self.delta_comps["wear"]

    def idx(self, name: str) -> int:
        return self.sectors.index(name)


def load_params(set_name: str = "central", env: str = "lunar",
                path: Path | None = None,
                anchor_draws: dict[str, float] | None = None,
                rng: np.random.Generator | None = None) -> Params:
    """Build Params from an assumption set x environment.

    anchor_draws/rng are the Monte Carlo hooks: pass draws from
    delta.draw_anchors(anchors, rng) to sample anchored ranges; rng also
    jitters shock rates. Deterministic (geometric-mid anchors) when omitted.
    """
    from .delta import _load_yaml
    raw = _load_yaml(str(path or PARAMS_DIR / "assumptions.yaml"))
    sectors = raw["sectors"]
    s = raw["sets"][set_name]
    base = raw["sets"][s["inherit"]] if "inherit" in s else s

    env_cfg = load_environment(env)
    anchors = load_anchors()
    draws = anchor_draws if anchor_draws is not None else draw_anchors(anchors)
    comps, prov = assemble_delta(env_cfg, sectors, anchors, draws)
    scale_delta = s.get("scale_delta", 1.0)
    comps = {k: v * scale_delta for k, v in comps.items()}

    q_scale = np.empty(len(sectors))
    for i, entry in enumerate(env_cfg["q_scale"]):
        q_scale[i], pr = resolve_entry(entry, draws, anchors,
                                       f"q_scale[{sectors[i]}]")
        prov.append(pr)
    q = np.array(base["q"], float) * q_scale
    A = np.array(base["A"], float) * s.get("scale_A", 1.0)

    imp = env_cfg.get("import", {})
    profile = np.array(imp.get("profile", base["import_profile"]), float)
    budget0 = float(s.get("import_budget0", base["import_budget0"])) * float(imp.get("budget_scale", 1.0))
    decay = float(s.get("import_decay_years", base["import_decay_years"])) * float(imp.get("decay_scale", 1.0))

    rep, rec, stk = base["repair"], base["recycling"], base["stockpile"]
    salvage_cfg = env_cfg.get("salvage_factors", {})
    salvage: dict[str, np.ndarray] = {}
    salvage_defaults = {
        "wear": 1.0,
        "catastrophic": 0.0,
        "obsolescence": 1.0,
        "logistics": 0.0,
    }
    for comp in DELTA_COMPONENTS:
        raw_factor = salvage_cfg.get(comp, salvage_defaults[comp])
        entries = raw_factor if isinstance(raw_factor, list) else [raw_factor] * len(sectors)
        if len(entries) != len(sectors):
            raise ValueError(
                f"salvage_factors.{comp}: expected {len(sectors)} entries, "
                f"got {len(entries)}"
            )
        salvage[comp] = np.empty(len(sectors))
        for i, entry in enumerate(entries):
            salvage[comp][i], pr = resolve_entry(
                entry, draws, anchors, f"salvage.{comp}[{sectors[i]}]"
            )
            if not 0.0 <= salvage[comp][i] <= 1.0:
                raise ValueError(
                    f"salvage_factors.{comp}[{sectors[i]}] must be in [0,1]"
                )
            prov.append(pr)
    stock_scale = float(s.get("scale_stock", 1.0))
    return Params(
        sectors=sectors,
        q=q,
        delta_comps=comps,
        A=A,
        import_profile=profile,
        import_budget0=budget0,
        import_decay_years=decay,
        repair_eff=float(rep["efficiency"]) * float(s.get("scale_repair_efficiency", 1.0)),
        repair_spares_fraction=float(rep["spares_fraction"]),
        scrap_recovery=min(1.0, float(rec["scrap_recovery"]) * float(s.get("scale_scrap_recovery", 1.0))),
        salvage_factors=salvage,
        recycle_profile=np.array(rec["output_profile"], float),
        recycle_opex=np.array(rec["opex"], float),
        stockable=np.array(stk["stockable"], bool),
        stock_initial_years=float(stk["initial_years"]) * stock_scale,
        stock_capacity_years=float(stk["capacity_years"]) * stock_scale,
        shelf_life=np.array(stk["shelf_life_years"], float),
        shocks=load_shocks(env_cfg, sectors, rng),
        pulse_years=(float(imp["pulse_years"]) if "pulse_years" in imp else None),
        environment=env,
        label=set_name,
        provenance=prov,
    )


def imports_at(p: Params, t: float, cutoff_year: float | None = None,
               cutoff_idx: np.ndarray | None = None) -> np.ndarray:
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


def replacement_demand(p: Params, K: np.ndarray) -> np.ndarray:
    """Output units of each sector needed per year just to replace retiring capacity."""
    return p.A @ (p.delta * K)


def recoverable_retirement(p: Params, K: np.ndarray,
                           wear_repair: np.ndarray | None = None) -> float:
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


def _lp_templates(p: Params):
    """Constant sparse constraint templates for allocate_step, cached on the
    Params instance. The matrix is constant except the growth rows' g-column
    entries (K_j) and the stage-3 normalized-draw row."""
    tpl = getattr(p, "_lp_tpl", None)
    if tpl is not None:
        return tpl
    from scipy.sparse import csc_matrix

    n = p.n
    iw, ir = p.idx("recycling"), p.idx("repair")
    nv = 3 * n + 2
    sx, su, swv, sd, sg = 0, n, 2 * n, 2 * n + 1, 3 * n + 1
    M = np.zeros((3 * n + 1, nv))
    for j in range(n):
        M[j, sx + j] = -1.0            # growth rows
        M[j, su + j] = -1.0
        M[j, sg] = 1.0                 # placeholder: set to K_j each step
        M[n + j, su + j] = 1.0         # wear caps
    for i in range(n):                 # material balance
        r = M[2 * n + i]
        r[sx:sx + n] = p.A[i]
        r[su:su + n] = p.repair_spares_fraction * p.A[i]
        if i == ir:
            r[su:su + n] += 1.0 / p.repair_eff
        if i == iw:
            r[swv] += 1.0
        r[swv] += p.recycle_opex[i] - p.recycle_profile[i]
        r[sd + i] = -1.0
    M[3 * n, swv] = 1.0                # scrap cap
    M[3 * n, su:su + n] = (
        p.scrap_recovery * p.salvage_factors["wear"]
    )
    A1 = csc_matrix(M)
    pin = np.zeros((1, nv))
    pin[0, sg] = -1.0                  # stages 2/3: hold g at its optimum
    draw = np.zeros((1, nv))
    draw[0, sd:sd + n] = 1.0           # stage 3: hold normalized draw optimum
    A3 = csc_matrix(np.vstack([M, pin, draw]))
    s1 = slice(A1.indptr[sg], A1.indptr[sg] + n)
    s3 = slice(A3.indptr[sg], A3.indptr[sg] + n)
    # csc stores each column's rows sorted, so the growth rows 0..n-1 are the
    # first n entries of column sg in both templates.
    assert (A1.indices[s1] == np.arange(n)).all()
    assert (A3.indices[s3] == np.arange(n)).all()
    bal = M[2 * n:3 * n].copy()        # dense balance block (slack fallback)
    tpl = (A1, s1, A3, s3, bal)
    p._lp_tpl = tpl
    return tpl


def _draw_weights(p: Params, supply: np.ndarray,
                  stock_avail: np.ndarray) -> np.ndarray:
    """Dimensionless stock-draw objective weights.

    Raw ``sum(d)`` compares unlike sector output units. Dividing each draw rate
    by a same-unit state scale makes stage 2 invariant to row-unit changes.
    """
    scale = np.maximum(np.maximum(np.abs(supply), np.abs(stock_avail)), 1e-12)
    weights = np.where(p.stockable, 1.0 / scale, 0.0)
    peak = float(np.max(weights))
    return weights / peak if peak > 0.0 else weights


def _qp_diagonal(p: Params, K: np.ndarray, supply: np.ndarray,
                 stock_avail: np.ndarray) -> np.ndarray:
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
    diag[n:2 * n] = 2.0 / build_scale**2
    scrap_scale = max(recoverable_retirement(p, K), build_floor)
    diag[2 * n] = 2.0 / scrap_scale**2
    draw_floor = max(
        float(np.max(np.maximum(np.abs(supply), np.abs(stock_avail)))) * 1e-3,
        1e-12,
    )
    draw_scale = np.maximum(
        np.maximum(np.abs(supply), np.abs(stock_avail)), draw_floor
    )
    diag[sd:sd + n] = 2.0
    active_draw = p.stockable & (stock_avail > 1e-10)
    diag[sd:sd + n][active_draw] = 2.0 / draw_scale[active_draw]**2
    diag[sg] = 2.0  # fixed by equality; positive keeps the Hessian strict
    return diag


def _unique_stage3(
    p: Params,
    K: np.ndarray,
    supply: np.ndarray,
    stock_avail: np.ndarray,
    b_ub: np.ndarray,
    g_star: float,
    draw_weights: np.ndarray,
    draw_star: float,
    z_start: np.ndarray,
) -> np.ndarray:
    """Select one unique point on the stage-1/stage-2 optimal face.

    OSQP is used here rather than SciPy's private HiGHS QP binding. The latter
    can misclassify the narrow face as infeasible when a capacity is nearly
    zero, even when initialized with the feasible stage-2 LP solution.
    """
    import osqp
    from scipy.sparse import csc_matrix, diags, eye, vstack

    n = p.n
    nv = 3 * n + 2
    sd, sg = 2 * n + 1, 3 * n + 1
    A1, s1, _, _, _ = _lp_templates(p)
    A1.data[s1] = K

    draw_row = np.zeros(nv)
    draw_row[sd:sd + n] = draw_weights
    qdiag = _qp_diagonal(p, K, supply, stock_avail)
    # Solve in normalized variables y with z = scale*y. This turns the
    # normalized quadratic into an identity Hessian and prevents large/small
    # sector units from degrading the ADMM feasibility test.
    variable_scale = 1.0 / np.sqrt(qdiag)
    core_z = vstack(
        [A1, csc_matrix(draw_row.reshape(1, -1))], format="csc"
    )
    core_y = core_z @ diags(variable_scale, format="csc")
    A_osqp = vstack(
        [core_y, eye(nv, format="csc")],
        format="csc",
    )
    g_tol = 1e-5 * max(1.0, abs(g_star))
    draw_tol = 1e-5 * max(1.0, abs(draw_star))
    lower_var = np.zeros(nv)
    upper_var = np.full(nv, np.inf)
    lower_var[sg], upper_var[sg] = g_star - g_tol, g_star
    for i in range(n):
        upper_var[sd + i] = (
            float(stock_avail[i]) if p.stockable[i] else 0.0
        )
    lower_var_y = lower_var / variable_scale
    upper_var_y = upper_var / variable_scale
    lower = np.concatenate([
        np.full(len(b_ub), -np.inf),
        [draw_star - draw_tol],
        lower_var_y,
    ])
    upper = np.concatenate([
        b_ub,
        [draw_star + draw_tol],
        upper_var_y,
    ])
    solver = osqp.OSQP()
    solver.setup(
        P=eye(nv, format="csc"),
        q=np.zeros(nv),
        A=A_osqp,
        l=lower,
        u=upper,
        verbose=False,
        polishing=True,
        eps_abs=1e-5,
        eps_rel=1e-5,
        max_iter=4_000,
    )
    solver.warm_start(x=np.asarray(z_start, float) / variable_scale)
    result = solver.solve(raise_error=False)
    primal_violation = max(
        float(np.max(A_osqp @ result.x - upper)),
        float(np.max(lower - A_osqp @ result.x)),
    )
    if result.info.status_val not in (1, 2) and primal_violation > 1e-3:
        # OSQP's infeasibility certificates can be unreliable on an
        # exceptionally narrow, badly scaled optimal face. SLSQP is slower but
        # starts from the feasible stage-2 LP vertex and supplies an independent
        # public-solver fallback for these rare states.
        from scipy.optimize import Bounds, LinearConstraint, minimize

        core = core_z.tocsr()
        core_lower = np.concatenate([
            np.full(len(b_ub), -np.inf), [draw_star - draw_tol]
        ])
        core_upper = np.concatenate([
            b_ub, [draw_star + draw_tol]
        ])
        qdiag = qdiag / float(np.max(qdiag))

        def objective(candidate):
            return 0.5 * float(np.dot(qdiag, candidate * candidate))

        def gradient(candidate):
            return qdiag * candidate

        fallback = minimize(
            objective,
            np.clip(np.asarray(z_start, float), lower_var, upper_var),
            jac=gradient,
            method="SLSQP",
            bounds=Bounds(lower_var, upper_var),
            constraints=[
                LinearConstraint(core, core_lower, core_upper)
            ],
            options={"ftol": 1e-9, "maxiter": 200},
        )
        fallback_violation = max(
            float(np.max(core @ fallback.x - core_upper)),
            float(np.max(core_lower - core @ fallback.x)),
        )
        if not fallback.success and fallback_violation > 1e-3:
            raise RuntimeError(
                f"stage-3 QP failed in OSQP ({result.info.status}) and "
                f"SLSQP ({fallback.message}); "
                f"primal violation={fallback_violation:.3g}"
            )
        z = np.asarray(fallback.x, float)
    else:
        z = np.asarray(result.x, float) * variable_scale
    # Remove solver-tolerance dust at explicit variable bounds.
    z[:3 * n + 1] = np.maximum(z[:3 * n + 1], 0.0)
    z[n:2 * n] = np.minimum(z[n:2 * n], p.wear * K)
    for i in range(n):
        cap = upper_var[sd + i]
        z[sd + i] = np.clip(z[sd + i], 0.0, cap)
    return z


def _binding_from_responses(responses: np.ndarray, bal: np.ndarray,
                            z: np.ndarray, supply: np.ndarray,
                            ) -> tuple[int, np.ndarray]:
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

    def __init__(self, p: Params):
        _, _, A3, _, bal = _lp_templates(p)
        n = p.n
        self.p, self.n = p, n
        nv, nr = 3 * n + 2, 3 * n + 3
        self.nv, self.nr = nv, nr
        self.sd, self.sg = 2 * n + 1, 3 * n + 1
        self.pin_row, self.draw_row = 3 * n + 1, 3 * n + 2
        self.bal = bal
        self.INF = _hcore.kHighsInf
        self.c = np.zeros(nv)
        self.c[self.sg] = -1.0
        self._all_cols = np.arange(nv, dtype=np.int32)
        lp = _hcore.HighsLp()
        lp.num_col_, lp.num_row_ = nv, nr
        lp.sense_ = _hcore.ObjSense.kMinimize
        lp.col_cost_ = self.c
        cl, cu = np.zeros(nv), np.full(nv, self.INF)
        cl[self.sg], cu[self.sg] = -self.INF, self.INF
        lp.col_lower_, lp.col_upper_ = cl, cu
        lp.row_lower_ = np.full(nr, -self.INF)
        ru = np.zeros(nr)
        ru[-2:] = self.INF                  # pin/draw rows inactive
        lp.row_upper_ = ru
        m = _hcore.HighsSparseMatrix()
        m.format_ = _hcore.MatrixFormat.kColwise
        m.num_col_, m.num_row_ = nv, nr
        m.start_ = A3.indptr.astype(np.int32)
        m.index_ = A3.indices.astype(np.int32)
        m.value_ = A3.data.copy()
        lp.a_matrix_ = m
        self.h = _hcore._Highs()
        self.h.setOptionValue("output_flag", False)
        if self.h.passModel(lp) != _hcore.HighsStatus.kOk:  # pragma: no cover
            raise RuntimeError("HiGHS passModel failed")

    def _set_state(self, model, K: np.ndarray, b_ub: np.ndarray,
                   stock_avail: np.ndarray) -> None:
        n, sd, sg, INF = self.n, self.sd, self.sg, self.INF
        for j in range(n):
            model.changeCoeff(j, sg, float(K[j]))
        for i in range(3 * n + 1):
            model.changeRowBounds(i, -INF, float(b_ub[i]))
        for i in range(n):
            cap = float(stock_avail[i]) if self.p.stockable[i] else 0.0
            model.changeColBounds(sd + i, 0.0, cap)

    def step(self, K: np.ndarray, m_direct: np.ndarray,
             stock_avail: np.ndarray) -> dict:
        p, n, h, INF = self.p, self.n, self.h, self.INF
        sd, sg = self.sd, self.sg
        supply = p.q * K + m_direct
        b_ub = np.concatenate([
            -p.delta * K, p.wear * K, supply,
            [p.scrap_recovery * recoverable_retirement(p, K)]])
        self._set_state(h, K, b_ub, stock_avail)
        h.changeColsCost(self.nv, self._all_cols, self.c)
        h.changeRowBounds(self.pin_row, -INF, INF)
        h.changeRowBounds(self.draw_row, -INF, INF)
        h.run()
        if h.getModelStatus() != _hcore.HighsModelStatus.kOptimal:  # pragma: no cover
            raise RuntimeError(f"HiGHS: {h.modelStatusToString(h.getModelStatus())}")
        z1 = np.array(h.getSolution().col_value)
        g_star = float(z1[sg])

        # Unit-invariant binding response: relax each material supply by 1%.
        responses = np.zeros(n)
        for i in range(n):
            row = 2 * n + i
            relaxed = float(supply[i] + 0.01 * max(abs(supply[i]), 1e-12))
            h.changeRowBounds(row, -INF, relaxed)
            h.run()
            if h.getModelStatus() == _hcore.HighsModelStatus.kOptimal:
                responses[i] = max(
                    0.0, float(h.getSolution().col_value[sg]) - g_star
                )
            h.changeRowBounds(row, -INF, float(supply[i]))
        h.run()  # restore the unperturbed optimum before stage 2
        z1 = np.array(h.getSolution().col_value)
        bal_duals = -np.array(h.getSolution().row_dual)[2 * n:3 * n]

        # Stage 2: exact g pin + dimensionless stock-draw objective.
        draw_weights = _draw_weights(p, supply, stock_avail)
        c2 = np.zeros(self.nv)
        c2[sd:sd + n] = draw_weights
        h.changeColsCost(self.nv, self._all_cols, c2)
        g_tol = 1e-5 * max(1.0, abs(g_star))
        # HiGHS' stage-1 optimum can sit a few ulps above the feasible face.
        # Keep stage 2 within solver tolerance below g*, never above it.
        h.changeRowBounds(self.pin_row, -INF, -g_star + g_tol)
        h.run()
        if h.getModelStatus() != _hcore.HighsModelStatus.kOptimal:
            raise RuntimeError("HiGHS stage-2 normalized-draw LP failed")
        z2 = np.array(h.getSolution().col_value)
        draw_star = float(np.dot(draw_weights, z2[sd:sd + n]))

        try:
            z = _unique_stage3(
                p, K, supply, stock_avail, b_ub, g_star,
                draw_weights, draw_star, z2,
            )
        except RuntimeError:
            # Long warm-start sequences with repeated RHS perturbations can
            # occasionally leave the private persistent HiGHS interface on a
            # numerically degraded basis. Re-solve once through the public,
            # cold SciPy reference path and replace the persistent model.
            result = _allocate_scipy(p, K, m_direct, stock_avail)
            p._fast_lp = _FastLP(p)
            return result
        z[sg] = g_star
        x, u, w, d, g = z[0:n], z[n:2 * n], z[2 * n], z[sd:sd + n], z[sg]
        binding, binding_mask = _binding_from_responses(
            responses, self.bal, z, supply
        )
        return {"x": x, "u": u, "w": w, "d": d, "g": g, "binding": binding,
                "binding_mask": binding_mask,
                "binding_responses": responses, "bal_duals": bal_duals}


def allocate_step(p: Params, K: np.ndarray, m_direct: np.ndarray,
                  stock_avail: np.ndarray) -> dict:
    """Maximin LP over one step — dispatches to the persistent-HiGHS fast
    path (default) or the scipy.linprog reference path (RSI_SLOW_LP=1, or
    when scipy's bundled highspy is unavailable). Both solve the identical
    LP; see _allocate_scipy for the constraint documentation."""
    if _USE_FAST_LP:
        fast = getattr(p, "_fast_lp", None)
        if fast is None:
            fast = _FastLP(p)
            p._fast_lp = fast
        return fast.step(K, m_direct, stock_avail)
    return _allocate_scipy(p, K, m_direct, stock_avail)


def _allocate_scipy(p: Params, K: np.ndarray, m_direct: np.ndarray,
                    stock_avail: np.ndarray) -> dict:
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
    b_ub = np.concatenate([
        -p.delta * K,                                   # growth rows
        p.wear * K,                                     # wear caps
        supply,                                         # material balance
        [p.scrap_recovery * recoverable_retirement(p, K)],  # scrap cap
    ])

    bounds = [(0, None)] * (3 * n + 1) + [(None, None)]
    for i in range(n):
        cap = float(stock_avail[i]) if p.stockable[i] else 0.0
        bounds[sd + i] = (0, cap)

    res = linprog(c, A_ub=A1, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success:  # pragma: no cover — feasible with x=u=w=d=0, g <= -max(delta)
        raise RuntimeError(f"LP failed: {res.message}")
    z1 = res.x
    g_star = float(z1[sg])
    bal_duals = -np.asarray(res.ineqlin.marginals)[2 * n:3 * n]

    responses = np.zeros(n)
    for i in range(n):
        perturbed = b_ub.copy()
        perturbed[2 * n + i] += 0.01 * max(abs(supply[i]), 1e-12)
        rp = linprog(c, A_ub=A1, b_ub=perturbed, bounds=bounds, method="highs")
        if rp.success:
            responses[i] = max(0.0, float(rp.x[sg]) - g_star)

    draw_weights = _draw_weights(p, supply, stock_avail)
    c2 = np.zeros(nv)
    c2[sd:sd + n] = draw_weights
    g_tol = 1e-5 * max(1.0, abs(g_star))
    bounds2 = list(bounds)
    bounds2[sg] = (g_star - g_tol, g_star)
    res2 = linprog(
        c2, A_ub=A1, b_ub=b_ub, bounds=bounds2, method="highs",
        options={"presolve": False},
    )
    if not res2.success:
        raise RuntimeError(f"stage-2 LP failed: {res2.message}")
    z2 = res2.x
    draw_star = float(np.dot(draw_weights, z2[sd:sd + n]))

    z = _unique_stage3(
        p, K, supply, stock_avail, b_ub, g_star,
        draw_weights, draw_star, z2,
    )
    z[sg] = g_star
    sx, su, swv = 0, n, 2 * n
    x, u, w, d, g = z[sx:sx + n], z[su:su + n], z[swv], z[sd:sd + n], z[sg]
    binding, binding_mask = _binding_from_responses(responses, bal, z, supply)
    return {"x": x, "u": u, "w": w, "d": d, "g": g, "binding": binding,
            "binding_mask": binding_mask,
            "binding_responses": responses, "bal_duals": bal_duals}


@dataclass
class RunResult:
    t: np.ndarray            # (T,)
    K: np.ndarray            # (T, n)
    g: np.ndarray            # (T,) realized worst-sector net growth, incl. shocks
    binding: np.ndarray      # (T,) index of binding sector
    S: np.ndarray            # (T, n) stockpile levels (output units)
    shock_log: list[tuple[float, str, float]]  # (t, shock name, fraction lost)
    g_alloc: np.ndarray | None = field(repr=False, default=None)
    co_binding: np.ndarray | None = field(repr=False, default=None)  # (T,n) bool
    params: Params = field(repr=False, default=None)
    K0: np.ndarray = field(repr=False, default=None)  # supplied initial K (pre-step)

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

    def _K0(self) -> np.ndarray:
        return self.K0 if self.K0 is not None else self.K[0]

    def lambda_series(self) -> np.ndarray:
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
    K0: np.ndarray | None = None,
    years: float = 40.0,
    dt: float = 0.25,
    cutoff_year: float | None = None,
    cutoff_sectors: list[str] | None = None,
    rng: np.random.Generator | None = None,
) -> RunResult:
    """Integrate the system. rng=None disables stochastic shocks (deterministic
    baseline); pass a Generator to sample common-cause events.
    cutoff_sectors names which sectors' imports stop at cutoff_year (None = all).
    """
    n = p.n
    K = np.full(n, 1.0) if K0 is None else K0.astype(float).copy()
    K_init = K.copy()
    cutoff_idx = (None if cutoff_sectors is None
                  else np.array([p.idx(s) for s in cutoff_sectors], int))

    rep0 = replacement_demand(p, K)
    S = np.where(p.stockable, p.stock_initial_years * rep0, 0.0)

    steps = int(round(years / dt))
    T, KK, GG, GA, BB, CB, SS = [], [], [], [], [], [], []
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
                inflow = m_stock * p.pulse_years   # one synodic batch
                next_pulse += p.pulse_years

        a = allocate_step(p, K, m_direct, S / dt)
        K_prev = K.copy()
        K = np.maximum(K + dt * (a["x"] + a["u"] - p.delta * K), 1e-9)
        # Stock flow is computed during the step. Its capacity clip is applied
        # after shocks so a damaged system cannot retain a pre-shock warehouse.
        S = S + inflow - a["d"] * dt - S * dt / p.shelf_life

        if rng is not None:
            for sh in p.shocks:
                for _ in range(rng.poisson(sh.rate_per_year * dt)):
                    frac = rng.uniform(*sh.fraction_lost)
                    K[sh.sector_idx] *= 1.0 - frac
                    shock_log.append((t + dt, sh.name, frac))

        cap = p.stock_capacity_years * replacement_demand(p, K)
        S = np.clip(S, 0.0, np.where(p.stockable, np.maximum(cap, 1e-9), 0.0))
        g_real = float(np.min((K - K_prev) / (dt * np.maximum(K_prev, 1e-30))))

        T.append(t + dt)
        KK.append(K.copy())
        GG.append(g_real)
        GA.append(a["g"])
        BB.append(a["binding"])
        CB.append(a["binding_mask"].copy())
        SS.append(S.copy())
    return RunResult(
        np.array(T), np.array(KK), np.array(GG), np.array(BB),
        np.array(SS), shock_log,
        g_alloc=np.array(GA), co_binding=np.array(CB),
        params=p, K0=K_init,
    )
