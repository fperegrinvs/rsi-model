"""r4.1 additive analysis layer over the Fourth Edition bootstrap model.

Implements the computable subset of the ROADMAP's external-review
follow-ups without inventing any new structural coefficient:

* durable reproduction endpoints (retention at horizon, final-five-year
  net reproduction, vitamin-pool exhaustion timing);
* vitamin-stock resolution (composition, initial-rate coverage, pooled
  residuals at first passage and horizon);
* intelligence/autonomy ablations restricted to zero/freeze operations on
  already-declared coefficients;
* the installed-mass versus reproduction-time oversize frontier (the
  oversize factor is a sweep axis, not a new assumption);
* ensemble diagnostics over the exact named crc32 draws of
  ``seed_ensemble`` (failure reasons, binding-constraint frequencies,
  Spearman sensitivity); and
* an elastic-relaxation infeasibility certificate for structurally
  infeasible scenarios, interrogating the identical LP matrix via
  ``build_seed_lp``.

Everything here is derived from coefficients already declared in
``params/fourth_edition.yaml``; outputs remain scenario implications, not
measurements or probabilities. Items that require new ASSUMPTION-class
coefficients (sector-resolved reproduction, a delivered-seed deployment
stage, shock-recovery endpoints, shell-resolved debris) stay in ROADMAP
pending authorial sign-off.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

import numpy as np
from scipy.optimize import linprog
from scipy.stats import spearmanr

from .fourth import (FourthParams, ReproductionResult, SeedResult,
                     _named_loguniform, build_seed_lp, process_profile,
                     sample_fourth_params, simulate_reproduction, size_seed)

EXHAUSTION_FRACTION = 0.01  # pool counted exhausted below 1% of initial stock


# --- durable endpoints -------------------------------------------------------

@dataclass(frozen=True)
class DurableEndpoints:
    scenario: str
    first_passage_year: float | None
    operating_at_horizon: float
    retained_at_horizon: bool
    net_reproduction_final5: float
    durable_final5: bool
    vitamin_pools_exhausted_year: float | None
    post_exhaustion_net_reproduction: float | None


def _pool_exhaustion_years(
    params: FourthParams,
    seed: SeedResult,
    run: ReproductionResult,
) -> dict[str, float | None]:
    """First year each vitamin-bearing category's pooled inventory falls
    below EXHAUSTION_FRACTION of its initial Earth stock (None if never).

    The pool mixes the initial Earth stock with recycled returns and any
    local production, so exhaustion here means the combined buffer is
    empty, not that specifically Earth-origin atoms are gone.
    """
    out: dict[str, float | None] = {}
    for e, element in enumerate(params.elements):
        v0 = float(seed.vitamin_stock_t[e])
        if v0 <= 1e-12:
            continue
        below = np.flatnonzero(run.inventory_t[:, e] < EXHAUSTION_FRACTION * v0)
        out[element] = float(run.t[below[0]]) if len(below) else None
    return out


def durable_endpoints(
    params: FourthParams,
    seed: SeedResult,
    run: ReproductionResult,
    *,
    window_years: float = 5.0,
) -> DurableEndpoints:
    dt = float(run.t[1] - run.t[0])
    w = max(1, int(round(window_years / dt)))
    final5 = float(run.operating_cells[-1] - run.operating_cells[-1 - w])
    exhaustion = _pool_exhaustion_years(params, seed, run)
    if exhaustion and all(v is not None for v in exhaustion.values()):
        ex_year: float | None = max(v for v in exhaustion.values() if v is not None)
    else:
        ex_year = None
    post = None
    if ex_year is not None and ex_year < float(run.t[-1]):
        k = int(np.searchsorted(run.t, ex_year))
        post = float(run.operating_cells[-1] - run.operating_cells[k])
    return DurableEndpoints(
        scenario=run.scenario,
        first_passage_year=run.second_cell_year,
        operating_at_horizon=float(run.operating_cells[-1]),
        retained_at_horizon=bool(run.operating_cells[-1] >= 2.0),
        net_reproduction_final5=final5,
        durable_final5=bool(final5 > 0.0),
        vitamin_pools_exhausted_year=ex_year,
        post_exhaustion_net_reproduction=post,
    )


# --- vitamin-stock resolution ------------------------------------------------

@dataclass(frozen=True)
class VitaminRow:
    element: str
    initial_stock_t: float
    share_of_vitamin_stock: float
    initial_rate_coverage_years: float | None
    pool_min_t: float
    pool_at_first_passage_t: float | None
    pool_at_horizon_t: float
    pool_exhaustion_year: float | None


def _base_cell_order_rate(params: FourthParams, seed: SeedResult) -> float:
    """The initial gross cell-order rate, as computed in
    ``simulate_reproduction`` before any intelligence gain."""
    z = seed.capacities
    service_need = params.A @ z
    ratio = np.divide(
        seed.process.q_effective * z,
        service_need,
        out=np.full(params.n, np.inf),
        where=service_need > 1e-12,
    )
    return min(
        float(np.min(ratio)),
        float(params.seed["maximum_gross_cell_orders_per_operating_cell_year"]),
    )


def vitamin_composition(
    params: FourthParams,
    seed: SeedResult,
    run: ReproductionResult,
) -> tuple[VitaminRow, ...]:
    total = float(seed.vitamin_stock_t.sum())
    if total <= 1e-12:
        return ()
    cell_bom = seed.process.B_effective @ seed.capacities
    rate = _base_cell_order_rate(params, seed)
    exhaustion = _pool_exhaustion_years(params, seed, run)
    fp = run.second_cell_year
    k_fp = int(np.searchsorted(run.t, fp)) if fp is not None else None
    rows = []
    for e, element in enumerate(params.elements):
        v0 = float(seed.vitamin_stock_t[e])
        if v0 <= 1e-12:
            continue
        draw = float(cell_bom[e]) * rate
        rows.append(VitaminRow(
            element=element,
            initial_stock_t=v0,
            share_of_vitamin_stock=v0 / total,
            initial_rate_coverage_years=(v0 / draw) if draw > 1e-12 else None,
            pool_min_t=float(run.inventory_t[:, e].min()),
            pool_at_first_passage_t=(
                float(run.inventory_t[k_fp, e]) if k_fp is not None else None
            ),
            pool_at_horizon_t=float(run.inventory_t[-1, e]),
            pool_exhaustion_year=exhaustion.get(element),
        ))
    rows.sort(key=lambda r: -r.initial_stock_t)
    return tuple(rows)


def material_limited_steps(
    params: FourthParams,
    seed: SeedResult,
    run: ReproductionResult,
) -> tuple[int, int]:
    """(material-limited steps, total steps): steps at which available
    material capped built cell orders below the desired order rate, i.e.
    where the intelligence-coupling multipliers on desired orders had no
    effect on realized construction."""
    cfg = params.scenarios[seed.scenario]
    intel = params.intelligence
    base = _base_cell_order_rate(params, seed)
    dt = float(run.t[1] - run.t[0])
    limited = 0
    steps = len(run.t) - 1
    for k in range(steps):
        gain = max(float(run.intelligence[k]) - float(cfg["ai_level"]), 0.0)
        desired = (
            base * max(float(run.operating_cells[k]), 0.0)
            * (1.0 + float(intel["productivity_elasticity"]) * gain)
            * (1.0 + float(intel["autonomy_learning_multiplier"]) * gain)
            * dt
        )
        if float(run.ordered_cells[k + 1]) + 1e-10 < desired:
            limited += 1
    return limited, steps


# --- intelligence/autonomy ablations ----------------------------------------

ABLATIONS: tuple[tuple[str, str], ...] = (
    ("baseline", "declared coefficients"),
    ("no_intelligence_growth", "learning_rate_per_year = 0"),
    ("productivity_channel_only", "autonomy_learning_multiplier = 0"),
    ("autonomy_channel_only", "productivity_elasticity = 0"),
    ("fully_uncoupled",
     "productivity_elasticity = autonomy_learning_multiplier = 0"),
)


@dataclass(frozen=True)
class AblationRow:
    variant: str
    definition: str
    feasible: bool
    first_passage_year: float | None
    operating_at_horizon: float | None
    growth_share_of_baseline: float | None


def _ablated_params(params: FourthParams, variant: str) -> FourthParams:
    intel = dict(params.intelligence)
    if variant in ("no_intelligence_growth",):
        intel["learning_rate_per_year"] = 0.0
    if variant in ("productivity_channel_only", "fully_uncoupled"):
        intel["autonomy_learning_multiplier"] = 0.0
    if variant in ("autonomy_channel_only", "fully_uncoupled"):
        intel["productivity_elasticity"] = 0.0
    return replace(params, intelligence=intel)


def ablation_suite(
    params: FourthParams,
    scenario: str,
    *,
    years: float = 40.0,
    dt: float = 0.25,
) -> tuple[AblationRow, ...]:
    """Zero/freeze ablations of the declared intelligence coupling.

    The seed LP does not read the intelligence block, so every dynamics
    variant reuses the identical central seed; only the reproduction pass
    changes. The final row re-sizes the seed at AI level 1.0 (coverage
    frozen at its base values) — a seed-level ablation that can be
    infeasible when a scenario's autonomy threshold exceeds base coverage.
    """
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    base_run = simulate_reproduction(params, seed, years=years, dt=dt)
    base_growth = float(base_run.operating_cells[-1]) - 1.0
    rows: list[AblationRow] = []
    for variant, definition in ABLATIONS:
        run = (base_run if variant == "baseline" else simulate_reproduction(
            _ablated_params(params, variant), seed, years=years, dt=dt))
        growth = float(run.operating_cells[-1]) - 1.0
        rows.append(AblationRow(
            variant=variant,
            definition=definition,
            feasible=True,
            first_passage_year=run.second_cell_year,
            operating_at_horizon=float(run.operating_cells[-1]),
            growth_share_of_baseline=(
                growth / base_growth if abs(base_growth) > 1e-9 else None
            ),
        ))
    frozen_seed = size_seed(params, scenario, ai_level=1.0)
    if frozen_seed.feasible:
        run = simulate_reproduction(params, frozen_seed, years=years, dt=dt)
        growth = float(run.operating_cells[-1]) - 1.0
        rows.append(AblationRow(
            "seed_sized_at_base_autonomy", "seed re-sized at AI level 1.0",
            True, run.second_cell_year, float(run.operating_cells[-1]),
            growth / base_growth if abs(base_growth) > 1e-9 else None,
        ))
    else:
        rows.append(AblationRow(
            "seed_sized_at_base_autonomy", "seed re-sized at AI level 1.0",
            False, None, None, None,
        ))
    return tuple(rows)


# --- oversize frontier -------------------------------------------------------

@dataclass(frozen=True)
class FrontierRow:
    oversize_factor: float
    installed_mass_t: float
    time_to_one_additional_cell: float | None
    additional_cells_at_horizon: float
    retained_plus_one_at_horizon: bool


def oversize_frontier(
    params: FourthParams,
    scenario: str,
    *,
    factors: tuple[float, ...] = (1.0, 1.25, 1.5, 2.0),
    years: float = 40.0,
    dt: float = 0.25,
) -> tuple[FrontierRow, ...]:
    """Installed mass versus reproduction time along the oversize axis.

    A factor-f seed installs f cell-equivalents of the minimum-mass
    design (capacities, feeds, and vitamin stock all scale with f; the
    one digital package is shared). The recorded time is first passage to
    one *additional* operating cell-equivalent, so f = 1 coincides with
    the canonical first-passage-to-two metric.
    """
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    scalable = float(seed.physical_seed_mass_t + seed.vitamin_stock_mass_t)
    rows = []
    for f in factors:
        run = simulate_reproduction(params, seed, years=years, dt=dt,
                                    initial_cells=f)
        reached = np.flatnonzero(run.operating_cells >= f + 1.0)
        rows.append(FrontierRow(
            oversize_factor=float(f),
            installed_mass_t=f * scalable + seed.digital_seed_mass_t,
            time_to_one_additional_cell=(
                float(run.t[reached[0]]) if len(reached) else None
            ),
            additional_cells_at_horizon=float(run.operating_cells[-1] - f),
            retained_plus_one_at_horizon=bool(
                run.operating_cells[-1] >= f + 1.0
            ),
        ))
    return tuple(rows)


# --- ensemble diagnostics ----------------------------------------------------

@dataclass(frozen=True)
class DrawRecord:
    run_index: int
    draws: dict[str, float]
    feasible: bool
    failure_reason: str | None
    seed_mass_t: float | None
    first_passage_year: float | None
    operating_at_horizon: float | None
    retained_at_horizon: bool | None
    durable_final5: bool | None
    top_binding_constraint: str | None


@dataclass(frozen=True)
class DiagnosticsSummary:
    scenario: str
    n_runs: int
    records: tuple[DrawRecord, ...]
    failure_histogram: dict[str, int]
    binding_histogram: dict[str, int]
    n_retained: int
    n_durable_final5: int
    sensitivity: dict[str, dict[str, float]]

    @property
    def n_feasible(self) -> int:
        return sum(r.feasible for r in self.records)


def ensemble_diagnostics(
    params: FourthParams,
    scenario: str,
    *,
    n_runs: int = 200,
    seed: int = 404,
    years: float = 40.0,
    dt: float = 0.5,
) -> DiagnosticsSummary:
    """Re-run the exact named draws of ``seed_ensemble`` and keep the
    per-draw detail it discards: failure reasons, binding constraints,
    durable endpoints, and Spearman sensitivity of every named multiplier
    against seed mass, first passage, and horizon cell-equivalents."""
    records: list[DrawRecord] = []
    for i in range(n_runs):
        draws = {
            name: _named_loguniform(seed, i, name, bounds)
            for name, bounds in params.uncertainty.items()
        }
        sampled = sample_fourth_params(params, seed=seed, run_index=i)
        sized = size_seed(sampled, scenario)
        if not sized.feasible:
            reason = ("autonomy_threshold"
                      if sized.status.startswith("autonomy threshold")
                      else "lp_infeasible")
            records.append(DrawRecord(i, draws, False, reason, None, None,
                                      None, None, None, None))
            continue
        run = simulate_reproduction(sampled, sized, years=years, dt=dt)
        ends = durable_endpoints(sampled, sized, run)
        records.append(DrawRecord(
            run_index=i,
            draws=draws,
            feasible=True,
            failure_reason=None,
            seed_mass_t=float(sized.total_seed_mass_t),
            first_passage_year=run.second_cell_year,
            operating_at_horizon=ends.operating_at_horizon,
            retained_at_horizon=ends.retained_at_horizon,
            durable_final5=ends.durable_final5,
            top_binding_constraint=(
                sized.binding_constraints[0][0]
                if sized.binding_constraints else None
            ),
        ))

    failure_hist: dict[str, int] = {}
    binding_hist: dict[str, int] = {}
    for r in records:
        if not r.feasible:
            failure_hist[r.failure_reason] = failure_hist.get(r.failure_reason, 0) + 1
        elif r.top_binding_constraint:
            binding_hist[r.top_binding_constraint] = (
                binding_hist.get(r.top_binding_constraint, 0) + 1
            )

    feasible = [r for r in records if r.feasible]
    outputs: dict[str, list[float]] = {"seed_mass_t": [], "first_passage_year": [],
                                       "operating_at_horizon": []}
    kept: dict[str, list[dict[str, float]]] = {k: [] for k in outputs}
    for r in feasible:
        for key, value in (("seed_mass_t", r.seed_mass_t),
                           ("first_passage_year", r.first_passage_year),
                           ("operating_at_horizon", r.operating_at_horizon)):
            if value is not None:
                outputs[key].append(float(value))
                kept[key].append(r.draws)
    sensitivity: dict[str, dict[str, float]] = {}
    for name in params.uncertainty:
        sensitivity[name] = {}
        for key, values in outputs.items():
            if len(values) >= 8:
                xs = [d[name] for d in kept[key]]
                rho = spearmanr(xs, values).statistic
                sensitivity[name][key] = float(rho) if np.isfinite(rho) else 0.0
            else:
                sensitivity[name][key] = float("nan")

    return DiagnosticsSummary(
        scenario=scenario,
        n_runs=n_runs,
        records=tuple(records),
        failure_histogram=failure_hist,
        binding_histogram=binding_hist,
        n_retained=sum(bool(r.retained_at_horizon) for r in feasible),
        n_durable_final5=sum(bool(r.durable_final5) for r in feasible),
        sensitivity=sensitivity,
    )


# --- elastic infeasibility certificate --------------------------------------

@dataclass(frozen=True)
class CertificateRow:
    constraint: str
    minimum_violation: float
    units: str


_ROW_UNITS = {
    "service": "sector service capacity-units over the horizon",
    "element": "tonnes over the horizon",
    "throughput": "tonnes of feed per year (energy row: MWh)",
    "autonomy": "intervention hours per year",
}


def infeasibility_certificate(
    params: FourthParams,
    scenario: str,
    *,
    tolerance: float = 1e-6,
) -> tuple[CertificateRow, ...]:
    """Minimum-total-violation elastic relaxation of the exact seed LP.

    Every constraint row receives a nonnegative slack; minimizing the
    slack sum (row-native units) names the requirement rows that cannot
    be satisfied simultaneously and by how much they fall short. This is
    a minimum *total-violation* certificate, not a strict irreducible
    infeasible subsystem; rows with zero slack in the optimum are
    jointly satisfiable with the violated set held at its minimum.
    Returns () when the scenario is feasible or blocked by the autonomy
    threshold before the LP is reached.
    """
    cfg = params.scenarios[scenario]
    profile = process_profile(params, scenario)
    if profile.minimum_coverage + 1e-12 < float(cfg["minimum_task_coverage"]):
        return ()
    lp = build_seed_lp(params, scenario, profile)
    A_ub, b_ub, labels = lp["A_ub"], lp["b_ub"], lp["labels"]
    n_rows, nv = A_ub.shape[0], lp["nv"]
    A_e = np.hstack([A_ub, -np.eye(n_rows)])
    c_e = np.concatenate([np.zeros(nv), np.ones(n_rows)])
    bounds = list(lp["bounds"]) + [(0.0, None)] * n_rows
    solved = linprog(c_e, A_ub=A_e, b_ub=b_ub, bounds=bounds, method="highs")
    if not solved.success:
        raise RuntimeError(f"elastic relaxation failed: {solved.message}")
    slack = solved.x[nv:]
    rows = [
        CertificateRow(
            constraint=labels[i],
            minimum_violation=float(slack[i]),
            units=_ROW_UNITS.get(labels[i].split(":", 1)[0], "row-native"),
        )
        for i in np.argsort(-slack) if slack[i] > tolerance
    ]
    return tuple(rows)
