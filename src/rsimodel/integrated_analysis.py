"""r4.0 analysis layer over the Current bootstrap model.

Implements the computable subset of the ROADMAP's external-review
follow-ups without inventing any new structural coefficient:

* terminal-window capacity endpoints (retention at horizon, final-five-year
  net capacity change, import-pool exhaustion timing);
* strategic-import-stock resolution (composition, initial-rate coverage, pooled
  residuals at first passage and horizon);
* intelligence/autonomy ablations restricted to zero/freeze operations on
  already-declared coefficients;
* the installed-mass versus aggregate-capacity-doubling oversize frontier (the
  oversize factor is a sweep axis, not a new assumption);
* ensemble diagnostics over the exact named crc32 draws of
  ``seed_ensemble`` (failure reasons, binding-constraint frequencies,
  Spearman sensitivity); and
* an elastic-relaxation infeasibility certificate for structurally
  infeasible scenarios, interrogating the identical LP matrix via
  ``build_seed_lp``.

Everything here is derived from coefficients declared in
``params/integrated_model.yaml``; outputs remain scenario implications, not
measurements or probabilities. Independent allocation, repair queues,
delivered-seed deployment, shock recovery, shell-resolved debris, and the
post-review equation extensions are now explicit assumption-class diagnostics.
They remain uncalibrated pending the evidence programs in ROADMAP.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import TypedDict

import numpy as np

from .array_types import FloatArray
from .extension_config import (
    BottleneckUpgradeConfig,
    ComputeDemandConfig,
    IntelligenceMarginalResponseConfig,
)
from .integrated import (
    CapacityGrowthResult,
    IntegratedParams,
    SeedResult,
    _named_loguniform,
    build_seed_lp,
    process_profile,
    sample_integrated_params,
    simulate_capacity_growth,
    simulate_seed_deployment,
    size_seed,
)
from .solver_adapter import solve_linear_program, spearman_correlation

EXHAUSTION_FRACTION = 0.01  # pool counted exhausted below 1% of initial stock


# --- terminal-window endpoints ----------------------------------------------


@dataclass(frozen=True)
class TerminalEndpoints:
    scenario: str
    aggregate_doubling_year: float | None
    operating_at_horizon: float
    retained_at_horizon: bool
    net_capacity_change_final5: float
    terminal_window_expanding: bool
    import_pools_exhausted_year: float | None
    post_exhaustion_capacity_change: float | None


def _pool_exhaustion_years(
    params: IntegratedParams,
    seed: SeedResult,
    run: CapacityGrowthResult,
) -> dict[str, float | None]:
    """First year each imported category's pooled inventory falls
    below EXHAUSTION_FRACTION of its initial Earth stock (None if never).

    The pool mixes the initial Earth stock with recycled returns and any
    local production, so exhaustion here means the combined buffer is
    empty, not that specifically Earth-origin atoms are gone.
    """
    out: dict[str, float | None] = {}
    for e, element in enumerate(params.elements):
        v0 = float(seed.import_stock_t[e])
        if v0 <= 1e-12:
            continue
        below = np.flatnonzero(run.inventory_t[:, e] < EXHAUSTION_FRACTION * v0)
        out[element] = float(run.t[below[0]]) if len(below) else None
    return out


def terminal_endpoints(
    params: IntegratedParams,
    seed: SeedResult,
    run: CapacityGrowthResult,
    *,
    window_years: float = 5.0,
) -> TerminalEndpoints:
    dt = float(run.t[1] - run.t[0])
    w = max(1, round(window_years / dt))
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
    return TerminalEndpoints(
        scenario=run.scenario,
        aggregate_doubling_year=run.aggregate_doubling_year,
        operating_at_horizon=float(run.operating_cells[-1]),
        retained_at_horizon=bool(run.operating_cells[-1] >= 2.0),
        net_capacity_change_final5=final5,
        terminal_window_expanding=bool(final5 > 0.0),
        import_pools_exhausted_year=ex_year,
        post_exhaustion_capacity_change=post,
    )


# --- strategic-import-stock resolution --------------------------------------


@dataclass(frozen=True)
class ImportStockRow:
    element: str
    initial_stock_t: float
    share_of_import_stock: float
    initial_rate_coverage_years: float | None
    pool_min_t: float
    pool_at_aggregate_doubling_t: float | None
    pool_at_horizon_t: float
    pool_exhaustion_year: float | None


def _base_cell_order_rate(params: IntegratedParams, seed: SeedResult) -> float:
    """The initial gross cell-order rate, as computed in
    ``simulate_capacity_growth`` before any intelligence gain."""
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


def import_stock_composition(
    params: IntegratedParams,
    seed: SeedResult,
    run: CapacityGrowthResult,
) -> tuple[ImportStockRow, ...]:
    total = float(seed.import_stock_t.sum())
    if total <= 1e-12:
        return ()
    cell_bom = seed.process.B_effective @ seed.capacities
    rate = _base_cell_order_rate(params, seed)
    exhaustion = _pool_exhaustion_years(params, seed, run)
    fp = run.aggregate_doubling_year
    k_fp = int(np.searchsorted(run.t, fp)) if fp is not None else None
    rows = []
    for e, element in enumerate(params.elements):
        v0 = float(seed.import_stock_t[e])
        if v0 <= 1e-12:
            continue
        draw = float(cell_bom[e]) * rate
        rows.append(
            ImportStockRow(
                element=element,
                initial_stock_t=v0,
                share_of_import_stock=v0 / total,
                initial_rate_coverage_years=(v0 / draw) if draw > 1e-12 else None,
                pool_min_t=float(run.inventory_t[:, e].min()),
                pool_at_aggregate_doubling_t=(
                    float(run.inventory_t[k_fp, e]) if k_fp is not None else None
                ),
                pool_at_horizon_t=float(run.inventory_t[-1, e]),
                pool_exhaustion_year=exhaustion.get(element),
            )
        )
    rows.sort(key=lambda r: -r.initial_stock_t)
    return tuple(rows)


def material_limited_steps(
    params: IntegratedParams,
    seed: SeedResult,
    run: CapacityGrowthResult,
) -> tuple[int, int]:
    summary = capacity_regime_summary(params, seed, run)
    return summary.material_limited, summary.total_steps


@dataclass(frozen=True)
class CapacityRegimeSummary:
    scenario: str
    total_steps: int
    material_limited: int
    service_limited: int
    order_rate_limited: int
    autonomy_limited: int = 0
    verification_limited: int = 0
    repair_limited: int = 0
    compute_limited: int = 0


def capacity_regime_summary(
    params: IntegratedParams,
    seed: SeedResult,
    run: CapacityGrowthResult,
) -> CapacityRegimeSummary:
    """Classify each dynamic step by its realized primary order constraint.

    Material-limited means available material reduced realized balanced
    orders below the service/order-cap target. Otherwise the lower of live
    sector service capacity and the declared gross-order cap names the
    regime. Counts are exhaustive and mutually exclusive.
    """
    if len(run.primary_constraint) == len(run.t) - 1:
        counts = {
            name: run.primary_constraint.count(name)
            for name in (
                "material",
                "service",
                "order_rate",
                "autonomy",
                "verification",
                "repair",
                "compute",
            )
        }
        return CapacityRegimeSummary(
            scenario=seed.scenario,
            total_steps=len(run.primary_constraint),
            material_limited=counts["material"],
            service_limited=counts["service"],
            order_rate_limited=counts["order_rate"],
            autonomy_limited=counts["autonomy"],
            verification_limited=counts["verification"],
            repair_limited=counts["repair"],
            compute_limited=counts["compute"],
        )
    cfg = params.scenarios[seed.scenario]
    intel = params.intelligence
    z = seed.capacities
    service_need = params.A @ z
    dt = float(run.t[1] - run.t[0])
    material = service = order_rate = 0
    steps = len(run.t) - 1
    for k in range(steps):
        op_sector = run.operating_sector_capacity[k]
        normalized = np.divide(
            op_sector,
            z,
            out=np.zeros(params.n),
            where=z > 1e-12,
        )
        aggregate_op = max(float(np.min(normalized)), 0.0)
        gain = max(float(run.intelligence[k]) - float(cfg["ai_level"]), 0.0)
        service_limit = float(
            np.min(
                np.divide(
                    seed.process.q_effective * op_sector,
                    service_need,
                    out=np.full(params.n, np.inf),
                    where=service_need > 1e-12,
                )
            )
        )
        rate_cap = (
            float(params.seed["maximum_gross_cell_orders_per_operating_cell_year"]) * aggregate_op
        )
        desired = (
            min(service_limit, rate_cap)
            * (1.0 + float(intel["productivity_elasticity"]) * gain)
            * (1.0 + float(intel["autonomy_learning_multiplier"]) * gain)
            * dt
        )
        if float(run.ordered_cells[k + 1]) + 1e-10 < desired:
            material += 1
        elif service_limit <= rate_cap:
            service += 1
        else:
            order_rate += 1
    return CapacityRegimeSummary(
        scenario=seed.scenario,
        total_steps=steps,
        material_limited=material,
        service_limited=service,
        order_rate_limited=order_rate,
    )


# --- build-allocation, repair, and shock-policy diagnostics -----------------


@dataclass(frozen=True)
class AllocationRepairRow:
    scenario: str
    policy: str
    repair_enabled: bool
    shock: str
    aggregate_doubling_year: float | None
    operating_at_horizon: float
    minimum_sector_margin_at_horizon: float
    survived: bool
    shock_recovery_year: float | None
    cumulative_repaired_capacity: float


def allocation_repair_suite(
    params: IntegratedParams,
    scenario: str,
    *,
    years: float = 40.0,
    dt: float = 0.25,
    shock_year: float = 20.0,
    shock_sector: str = "advanced_logic_memory",
    shock_fraction: float = 0.50,
) -> tuple[AllocationRepairRow, ...]:
    """Compare balanced and independent allocation, repair, and one shock.

    The shock is a deterministic structural diagnostic, not a frequency
    claim. Recovery means the shocked sector regains its immediately
    pre-shock operating capacity; survival remains the scenario-specific
    viable-floor test performed by ``simulate_capacity_growth``.
    """
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    variants = (
        ("balanced", False, ()),
        ("maximin_sector", False, ()),
        ("maximin_sector", True, ()),
        (
            "maximin_sector",
            True,
            ((shock_year, shock_sector, shock_fraction),),
        ),
    )
    rows = []
    for policy, repair, shocks in variants:
        run = simulate_capacity_growth(
            params,
            seed,
            years=years,
            dt=dt,
            allocation_policy=policy,
            repair_enabled=repair,
            shock_events=shocks,
        )
        normalized = np.divide(
            run.operating_sector_capacity[-1],
            seed.capacities,
            out=np.zeros(params.n),
            where=seed.capacities > 1e-12,
        )
        recovery_year = None
        shock_label = "none"
        if shocks:
            shock_label = f"{shock_sector}:{shock_fraction:.0%}@year{shock_year:g}"
            j = params.sector_idx(shock_sector)
            event_k = int(np.searchsorted(run.t, shock_year))
            reference_k = max(event_k - 1, 0)
            reference = float(run.operating_sector_capacity[reference_k, j])
            recovered = np.flatnonzero(
                run.operating_sector_capacity[event_k:, j] >= reference - 1e-9
            )
            if len(recovered):
                recovery_year = float(run.t[event_k + recovered[0]])
        rows.append(
            AllocationRepairRow(
                scenario=scenario,
                policy=policy,
                repair_enabled=repair,
                shock=shock_label,
                aggregate_doubling_year=run.aggregate_doubling_year,
                operating_at_horizon=float(run.operating_cells[-1]),
                minimum_sector_margin_at_horizon=float(np.min(normalized)),
                survived=run.survived,
                shock_recovery_year=recovery_year,
                cumulative_repaired_capacity=float(run.repaired_sector_capacity.sum()),
            )
        )
    return tuple(rows)


@dataclass(frozen=True)
class KnowledgeRegimeRow:
    scenario: str
    variant: str
    operating_at_horizon: float
    aggregate_doubling_year: float | None
    material_steps: int
    autonomy_steps: int
    verification_steps: int
    repair_steps: int
    compute_steps: int
    service_steps: int
    order_rate_steps: int


class KnowledgeRegimeOverrides(TypedDict, total=False):
    operational_constraints_enabled: bool
    communication_outage_windows: tuple[tuple[float, float, float], ...]
    verification_outage_windows: tuple[tuple[float, float, float], ...]
    compute_outage_windows: tuple[tuple[float, float, float], ...]
    allocation_policy: str
    repair_enabled: bool
    shock_events: tuple[tuple[float, str, float], ...]


def knowledge_regime_suite(
    params: IntegratedParams,
    scenario: str,
    *,
    years: float = 40.0,
    dt: float = 0.25,
) -> tuple[KnowledgeRegimeRow, ...]:
    """Exercise each named non-material operating gate.

    Two-year zero-capacity windows are adversarial diagnostics, not outage
    frequency claims. The repair case removes 90% of advanced-logic/memory at
    year 5 under independent allocation and the declared repair process.
    """
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    variants: tuple[tuple[str, KnowledgeRegimeOverrides], ...] = (
        ("declared", {"operational_constraints_enabled": True}),
        (
            "communication_outage_years10_12",
            {
                "operational_constraints_enabled": True,
                "communication_outage_windows": ((10.0, 12.0, 0.0),),
            },
        ),
        (
            "verification_outage_years10_12",
            {
                "operational_constraints_enabled": True,
                "verification_outage_windows": ((10.0, 12.0, 0.0),),
            },
        ),
        (
            "compute_outage_years10_12",
            {
                "operational_constraints_enabled": True,
                "compute_outage_windows": ((10.0, 12.0, 0.0),),
            },
        ),
        (
            "repair_after_advanced_logic_90pct_loss_year5",
            {
                "operational_constraints_enabled": True,
                "allocation_policy": "maximin_sector",
                "repair_enabled": True,
                "shock_events": ((5.0, "advanced_logic_memory", 0.90),),
            },
        ),
    )
    rows = []
    for label, kwargs in variants:
        run = simulate_capacity_growth(
            params,
            seed,
            years=years,
            dt=dt,
            **kwargs,
        )
        regime = capacity_regime_summary(params, seed, run)
        rows.append(
            KnowledgeRegimeRow(
                scenario=scenario,
                variant=label,
                operating_at_horizon=float(run.operating_cells[-1]),
                aggregate_doubling_year=run.aggregate_doubling_year,
                material_steps=regime.material_limited,
                autonomy_steps=regime.autonomy_limited,
                verification_steps=regime.verification_limited,
                repair_steps=regime.repair_limited,
                compute_steps=regime.compute_limited,
                service_steps=regime.service_limited,
                order_rate_steps=regime.order_rate_limited,
            )
        )
    return tuple(rows)


# --- environment/process coupling -------------------------------------------


@dataclass(frozen=True)
class EnvironmentEffectRow:
    scenario: str
    environment_profile: str
    feasible: bool
    seed_mass_t: float | None
    top_binding_constraint: str | None
    operating_at_horizon: float | None
    aggregate_doubling_year: float | None
    survived: bool | None


def environment_effect_suite(
    params: IntegratedParams,
    scenario: str,
    *,
    years: float = 40.0,
    dt: float = 0.25,
) -> tuple[EnvironmentEffectRow, ...]:
    """Compare identity, nominal-lunar, and adverse-lunar process effects."""
    rows = []
    for environment_profile in (
        "centrifuge_only",
        "lunar_nominal",
        "lunar_adverse",
    ):
        seed = size_seed(
            params,
            scenario,
            environment_profile=environment_profile,
        )
        if not seed.feasible:
            rows.append(
                EnvironmentEffectRow(
                    scenario,
                    environment_profile,
                    False,
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            )
            continue
        run = simulate_capacity_growth(
            params,
            seed,
            years=years,
            dt=dt,
        )
        total_mass, _, _ = seed.required_masses()
        rows.append(
            EnvironmentEffectRow(
                scenario=scenario,
                environment_profile=environment_profile,
                feasible=True,
                seed_mass_t=total_mass,
                top_binding_constraint=(
                    seed.binding_constraints[0][0] if seed.binding_constraints else None
                ),
                operating_at_horizon=float(run.operating_cells[-1]),
                aggregate_doubling_year=run.aggregate_doubling_year,
                survived=run.survived,
            )
        )
    return tuple(rows)


# --- policy and structural-uncertainty sweep --------------------------------


@dataclass(frozen=True)
class PolicyRobustnessRow:
    scenario: str
    sweep_dimension: str
    sweep_value: float
    policy: str
    horizon_years: float
    survived: bool
    terminal_window_expanding: bool
    operating_at_horizon: float
    minimum_sector_margin_at_horizon: float
    aggregate_doubling_year: float | None


def policy_robustness_sweep(
    params: IntegratedParams,
    scenario: str,
    *,
    dt: float = 0.5,
) -> tuple[PolicyRobustnessRow, ...]:
    """One-factor structural sweep across five build policies.

    Dimensions cover shock knockout, event time, horizon, retained initial
    import stock, initial surplus, and obsolescence/depreciation. The sweep is
    deterministic scenario discovery; it is not a probability distribution.
    """
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    policies = (
        "balanced",
        "maximin_sector",
        "surplus_preserving",
        "shock_aware",
        "perfect_foresight",
    )
    sweeps = {
        "knockout_fraction": (0.25, 0.50, 0.75, 0.90),
        "event_time_year": (10.0, 20.0, 30.0),
        "horizon_years": (20.0, 40.0, 60.0),
        "retained_import_stock_fraction": (0.0, 0.5, 1.0),
        "initial_surplus_cells": (1.0, 1.25, 1.5),
        "obsolescence_multiplier": (0.75, 1.0, 1.5),
    }
    rows = []
    for dimension, values in sweeps.items():
        for value in values:
            horizon = value if dimension == "horizon_years" else 40.0
            knockout = value if dimension == "knockout_fraction" else 0.50
            event_year = value if dimension == "event_time_year" else 15.0
            import_multiplier = value if dimension == "retained_import_stock_fraction" else 1.0
            initial_cells = value if dimension == "initial_surplus_cells" else 1.0
            depreciation = value if dimension == "obsolescence_multiplier" else 1.0
            for policy in policies:
                run = simulate_capacity_growth(
                    params,
                    seed,
                    years=horizon,
                    dt=dt,
                    initial_cells=initial_cells,
                    allocation_policy=policy,
                    repair_enabled=True,
                    shock_events=(
                        (
                            min(event_year, max(horizon - dt, 0.0)),
                            "advanced_logic_memory",
                            knockout,
                        ),
                    ),
                    import_stock_multiplier=import_multiplier,
                    depreciation_multiplier=depreciation,
                )
                window = max(1, round(5.0 / dt))
                final_change = float(
                    run.operating_cells[-1] - run.operating_cells[max(len(run.t) - 1 - window, 0)]
                )
                normalized = np.divide(
                    run.operating_sector_capacity[-1],
                    seed.capacities,
                    out=np.zeros(params.n),
                    where=seed.capacities > 1e-12,
                )
                rows.append(
                    PolicyRobustnessRow(
                        scenario=scenario,
                        sweep_dimension=dimension,
                        sweep_value=float(value),
                        policy=policy,
                        horizon_years=float(horizon),
                        survived=run.survived,
                        terminal_window_expanding=bool(final_change > 0.0),
                        operating_at_horizon=float(run.operating_cells[-1]),
                        minimum_sector_margin_at_horizon=float(np.min(normalized)),
                        aggregate_doubling_year=run.aggregate_doubling_year,
                    )
                )
    return tuple(rows)


# --- electronics architecture and shelf-life closure ------------------------


@dataclass(frozen=True)
class ElectronicsArchitectureRow:
    scenario: str
    architecture: str
    tier: str
    replacement_demand_capacity: float
    local_supply_capacity: float
    imported_supply_capacity: float
    cannibalized_supply_capacity: float
    substitution_credit_capacity: float
    expired_inventory_capacity: float
    terminal_import_inventory_capacity: float
    shortfall_capacity: float
    first_shortfall_year: float | None
    viable: bool
    imported_mass_t: float
    measurement_priority: str


def electronics_architecture_suite(
    params: IntegratedParams,
    scenario: str,
    *,
    years: float = 40.0,
    dt: float = 0.25,
) -> tuple[ElectronicsArchitectureRow, ...]:
    """Resolve tier replacement supply, shelf decay, and substitutions."""
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    run = simulate_capacity_growth(
        params,
        seed,
        years=years,
        dt=dt,
    )
    cfg = params.electronics_closure
    tiers = tuple(cfg["tiers"])
    indices = [params.sector_idx(tier) for tier in tiers]
    rows = []
    for architecture, arch in cfg["architectures"].items():
        inventory = np.array(
            [seed.capacities[j] * float(arch["initial_import_inventory_fraction"]) for j in indices]
        )
        totals = {
            name: np.zeros(len(tiers))
            for name in (
                "demand",
                "local",
                "imports",
                "cannibal",
                "substitution",
                "expired",
                "shortfall",
                "imported_mass",
            )
        }
        first_shortfall: list[float | None] = [None] * len(tiers)
        for k in range(len(run.t) - 1):
            for x, (tier, j) in enumerate(zip(tiers, indices, strict=True)):
                tier_cfg = cfg["tiers"][tier]
                growth = max(
                    float(
                        run.installed_sector_capacity[k + 1, j]
                        - run.installed_sector_capacity[k, j]
                    ),
                    0.0,
                )
                retirement = (
                    float(run.installed_sector_capacity[k, j])
                    * (float(params.delta[j]) + float(tier_cfg["obsolescence_per_year"]))
                    * dt
                )
                demand = growth + retirement
                local = min(
                    demand,
                    float(seed.process.q_effective[j])
                    * float(run.operating_sector_capacity[k, j])
                    * float(tier_cfg["local_producibility_fraction"])
                    * float(arch["local_producibility_multiplier"])
                    * dt,
                )
                cannibal = min(
                    max(demand - local, 0.0),
                    retirement * float(arch["cannibalization_fraction"]),
                )
                substitution = 0.0
                if tier == "advanced_logic_memory":
                    substitution = min(
                        max(demand - local - cannibal, 0.0),
                        demand * float(arch["mature_substitution_credit_fraction"]),
                    )
                imported = (
                    seed.capacities[j]
                    * float(arch["annual_import_fraction_of_initial_capacity"])
                    * dt
                )
                inventory[x] += imported
                retained = inventory[x] * math.exp(
                    -dt / max(float(tier_cfg["shelf_life_years"]), 1e-12)
                )
                expired = inventory[x] - retained
                inventory[x] = retained
                draw = min(
                    inventory[x],
                    max(demand - local - cannibal - substitution, 0.0),
                )
                inventory[x] -= draw
                shortfall = max(
                    demand - local - cannibal - substitution - draw,
                    0.0,
                )
                if shortfall > 1e-9 and first_shortfall[x] is None:
                    first_shortfall[x] = float(run.t[k + 1])
                totals["demand"][x] += demand
                totals["local"][x] += local
                totals["imports"][x] += draw
                totals["cannibal"][x] += cannibal
                totals["substitution"][x] += substitution
                totals["expired"][x] += expired
                totals["shortfall"][x] += shortfall
                mass_per_capacity = float(seed.process.B_effective[:, j].sum())
                totals["imported_mass"][x] += imported * mass_per_capacity
        for x, tier in enumerate(tiers):
            rows.append(
                ElectronicsArchitectureRow(
                    scenario=scenario,
                    architecture=architecture,
                    tier=tier,
                    replacement_demand_capacity=float(totals["demand"][x]),
                    local_supply_capacity=float(totals["local"][x]),
                    imported_supply_capacity=float(totals["imports"][x]),
                    cannibalized_supply_capacity=float(totals["cannibal"][x]),
                    substitution_credit_capacity=float(totals["substitution"][x]),
                    expired_inventory_capacity=float(totals["expired"][x]),
                    terminal_import_inventory_capacity=float(inventory[x]),
                    shortfall_capacity=float(totals["shortfall"][x]),
                    first_shortfall_year=first_shortfall[x],
                    viable=bool(totals["shortfall"][x] <= 1e-9),
                    imported_mass_t=float(totals["imported_mass"][x]),
                    measurement_priority=str(cfg["tiers"][tier]["measurement_priority"]),
                )
            )
    return tuple(rows)


# --- symmetric dynamic economics --------------------------------------------


@dataclass(frozen=True)
class EconomicTrajectory:
    scenario: str
    market: str
    t: FloatArray
    technical_space_capacity: FloatArray
    funded_space_capacity: FloatArray
    earth_capacity: FloatArray
    market_demand: FloatArray
    space_cash_musd: FloatArray
    earth_cash_musd: FloatArray
    space_debt_musd: FloatArray
    earth_debt_musd: FloatArray
    space_investment_musd: FloatArray
    earth_investment_musd: FloatArray
    space_finance_constrained_steps: int
    earth_finance_constrained_steps: int
    space_self_financing_year: float | None
    earth_self_financing_year: float | None


def _learning_cost(
    initial_cost: float,
    cumulative_capacity: float,
    learning_rate: float,
) -> float:
    exponent = math.log2(max(1.0 - learning_rate, 1e-9))
    return initial_cost * max(cumulative_capacity, 1.0) ** exponent


def simulate_symmetric_economics(
    params: IntegratedParams,
    seed: SeedResult,
    run: CapacityGrowthResult,
    market: str,
) -> EconomicTrajectory:
    """Fund Earth and space with the same reinvestment/debt mechanics.

    Space build is capped by the physical model's compute trajectory and pays
    for ordered industrial mass plus intervention demand. Earth expands an
    endogenous resource ceiling. Both sides have learning, depreciation,
    regulatory delay, bridge finance, interest, and debt-to-revenue limits.
    """
    cfg = params.dynamic_economics
    if market not in cfg["markets"]:
        raise ValueError(f"unknown economic market {market!r}")
    mkt = cfg["markets"][market]
    space_cfg = cfg["space"]
    earth_cfg = cfg["earth"]
    t = run.t
    dt = float(t[1] - t[0])
    n = len(t)
    technical_space = run.local_compute / max(float(run.local_compute[0]), 1e-12)
    funded_space = np.zeros(n)
    earth_capacity = np.zeros(n)
    demand = np.zeros(n)
    space_cash = np.zeros(n)
    earth_cash = np.zeros(n)
    space_debt = np.zeros(n)
    earth_debt = np.zeros(n)
    space_investment = np.zeros(n)
    earth_investment = np.zeros(n)
    funded_space[0] = min(1.0, technical_space[0])
    earth_capacity[0] = 1.0
    demand[0] = 1.5
    space_cash[0] = float(space_cfg["initial_equity_musd"]) + float(
        space_cfg["bridge_financing_musd"]
    )
    earth_cash[0] = float(earth_cfg["initial_equity_musd"]) + float(
        earth_cfg["bridge_financing_musd"]
    )
    space_lag = max(1, round(float(space_cfg["regulatory_delay_years"]) / dt))
    earth_lag = max(1, round(float(earth_cfg["regulatory_delay_years"]) / dt))
    space_queue = np.zeros(space_lag)
    earth_queue = np.zeros(earth_lag)
    cumulative_space_capacity = 1.0
    cumulative_earth_capacity = 1.0
    cumulative_space_revenue = 0.0
    cumulative_earth_revenue = 0.0
    cumulative_space_cost = float(space_cfg["initial_equity_musd"]) + float(
        space_cfg["bridge_financing_musd"]
    )
    cumulative_earth_cost = float(earth_cfg["initial_equity_musd"]) + float(
        earth_cfg["bridge_financing_musd"]
    )
    space_self_financing = None
    earth_self_financing = None
    space_constrained = earth_constrained = 0
    physical_mass_per_step = np.sum(
        seed.process.B_effective @ run.ordered_sector_capacity.T,
        axis=0,
    )

    for k in range(n - 1):
        demand[k + 1] = min(
            demand[k] * math.exp(float(mkt["demand_growth_per_year"]) * dt),
            float(mkt["demand_ceiling_units"]),
        )
        space_revenue = (
            min(funded_space[k], demand[k])
            * float(mkt["revenue_musd_per_compute_unit_year"])
            * float(mkt["space_price_multiplier"])
            * dt
        )
        earth_revenue = (
            min(earth_capacity[k], demand[k])
            * float(mkt["revenue_musd_per_compute_unit_year"])
            * dt
        )
        funded_share = funded_space[k] / max(float(technical_space[k]), 1e-12)
        space_opex = (
            funded_space[k] * float(space_cfg["operating_cost_musd_per_compute_unit_year"]) * dt
            + physical_mass_per_step[k]
            * funded_share
            * float(space_cfg["material_transfer_cost_musd_per_t"])
            + float(run.intervention_demand_hours[k])
            * funded_share
            * float(space_cfg["intervention_cost_musd_per_hour"])
            * dt
        )
        earth_opex = (
            earth_capacity[k] * float(earth_cfg["operating_cost_musd_per_compute_unit_year"]) * dt
        )
        space_interest = space_debt[k] * float(space_cfg["wacc"]) * dt
        earth_interest = earth_debt[k] * float(earth_cfg["wacc"]) * dt
        preinvestment_space_cash = space_cash[k] + space_revenue - space_opex - space_interest
        preinvestment_earth_cash = earth_cash[k] + earth_revenue - earth_opex - earth_interest

        due_space = space_queue[0]
        space_queue[:-1] = space_queue[1:]
        space_queue[-1] = 0.0
        due_earth = earth_queue[0]
        earth_queue[:-1] = earth_queue[1:]
        earth_queue[-1] = 0.0
        after_depreciation_space = max(
            funded_space[k] * (1.0 - float(space_cfg["depreciation_per_year"]) * dt) + due_space,
            0.0,
        )
        after_depreciation_earth = max(
            earth_capacity[k] * (1.0 - float(earth_cfg["depreciation_per_year"]) * dt) + due_earth,
            0.0,
        )
        desired_space = max(
            technical_space[k + 1] - after_depreciation_space - float(space_queue.sum()),
            0.0,
        )
        resource_ceiling = (
            float(earth_cfg["initial_resource_ceiling_units"])
            + float(earth_cfg["induced_resource_ceiling_units_per_year"]) * t[k]
        )
        desired_earth = max(
            min(demand[k + 1], resource_ceiling)
            - after_depreciation_earth
            - float(earth_queue.sum()),
            0.0,
        )
        space_unit_cost = _learning_cost(
            float(space_cfg["capex_musd_per_compute_unit"]),
            cumulative_space_capacity,
            float(space_cfg["learning_rate"]),
        )
        earth_unit_cost = _learning_cost(
            float(earth_cfg["capex_musd_per_compute_unit"]),
            cumulative_earth_capacity,
            float(earth_cfg["learning_rate"]),
        )
        max_space_debt = (
            float(space_cfg["max_debt_to_annual_revenue"]) * space_revenue / max(dt, 1e-12)
        )
        max_earth_debt = (
            float(earth_cfg["max_debt_to_annual_revenue"]) * earth_revenue / max(dt, 1e-12)
        )
        space_borrowing = max(max_space_debt - space_debt[k], 0.0)
        earth_borrowing = max(max_earth_debt - earth_debt[k], 0.0)
        affordable_space = max(
            preinvestment_space_cash + space_borrowing,
            0.0,
        ) / max(space_unit_cost, 1e-12)
        affordable_earth = max(
            preinvestment_earth_cash + earth_borrowing,
            0.0,
        ) / max(earth_unit_cost, 1e-12)
        build_space = min(desired_space, affordable_space)
        build_earth = min(desired_earth, affordable_earth)
        if build_space + 1e-9 < desired_space:
            space_constrained += 1
        if build_earth + 1e-9 < desired_earth:
            earth_constrained += 1
        spend_space = build_space * space_unit_cost
        spend_earth = build_earth * earth_unit_cost
        new_space_debt = min(
            max(spend_space - max(preinvestment_space_cash, 0.0), 0.0),
            space_borrowing,
        )
        new_earth_debt = min(
            max(spend_earth - max(preinvestment_earth_cash, 0.0), 0.0),
            earth_borrowing,
        )
        space_queue[-1] += build_space
        earth_queue[-1] += build_earth
        space_investment[k + 1] = spend_space
        earth_investment[k + 1] = spend_earth
        space_cash[k + 1] = max(
            preinvestment_space_cash + new_space_debt - spend_space,
            0.0,
        )
        earth_cash[k + 1] = max(
            preinvestment_earth_cash + new_earth_debt - spend_earth,
            0.0,
        )
        space_repayment = min(
            max(space_revenue - space_opex, 0.0) * 0.25,
            space_debt[k] + new_space_debt,
        )
        earth_repayment = min(
            max(earth_revenue - earth_opex, 0.0) * 0.25,
            earth_debt[k] + new_earth_debt,
        )
        space_debt[k + 1] = max(
            space_debt[k] + new_space_debt - space_repayment,
            0.0,
        )
        earth_debt[k + 1] = max(
            earth_debt[k] + new_earth_debt - earth_repayment,
            0.0,
        )
        funded_space[k + 1] = min(
            after_depreciation_space,
            technical_space[k + 1],
        )
        earth_capacity[k + 1] = after_depreciation_earth
        cumulative_space_capacity += build_space
        cumulative_earth_capacity += build_earth
        cumulative_space_revenue += space_revenue
        cumulative_earth_revenue += earth_revenue
        cumulative_space_cost += space_opex + space_interest + spend_space
        cumulative_earth_cost += earth_opex + earth_interest + spend_earth
        if space_self_financing is None and cumulative_space_revenue >= cumulative_space_cost:
            space_self_financing = float(t[k + 1])
        if earth_self_financing is None and cumulative_earth_revenue >= cumulative_earth_cost:
            earth_self_financing = float(t[k + 1])

    return EconomicTrajectory(
        scenario=seed.scenario,
        market=market,
        t=t,
        technical_space_capacity=technical_space,
        funded_space_capacity=funded_space,
        earth_capacity=earth_capacity,
        market_demand=demand,
        space_cash_musd=space_cash,
        earth_cash_musd=earth_cash,
        space_debt_musd=space_debt,
        earth_debt_musd=earth_debt,
        space_investment_musd=space_investment,
        earth_investment_musd=earth_investment,
        space_finance_constrained_steps=space_constrained,
        earth_finance_constrained_steps=earth_constrained,
        space_self_financing_year=space_self_financing,
        earth_self_financing_year=earth_self_financing,
    )


# --- composition-changing robust-seed Pareto search -------------------------


@dataclass(frozen=True)
class ParetoSeedDesign:
    scenario: str
    route: str
    redundancy: str
    source_portfolio: str
    delivered_mass_t: float
    import_mass_t: float
    intervention_hours_per_year: float
    aggregate_doubling_year: float | None
    operating_at_horizon: float
    terminal_window_expanding: bool
    source_outage_operating_at_horizon: float
    source_outage_survived: bool
    non_dominated: bool
    robust_candidate: bool


class ParetoCandidate(TypedDict):
    scenario: str
    route: str
    redundancy: str
    source_portfolio: str
    delivered_mass_t: float
    import_mass_t: float
    intervention_hours_per_year: float
    aggregate_doubling_year: float | None
    operating_at_horizon: float
    terminal_window_expanding: bool
    source_outage_operating_at_horizon: float
    source_outage_survived: bool


def _route_params(
    params: IntegratedParams,
    route: str,
    cfg: Mapping[str, float],
) -> IntegratedParams:
    if route == "baseline":
        return params
    B = params.B.copy()
    q = params.q.copy()
    delta = params.delta.copy()
    if route == "mature_node":
        j = params.sector_idx("advanced_logic_memory")
        B[:, j] *= float(cfg["advanced_logic_memory_bom_multiplier"])
        B[params.element_idx("dopants"), j] = params.B[params.element_idx("dopants"), j] * float(
            cfg["advanced_logic_memory_dopants_multiplier"]
        )
        q[j] *= float(cfg["advanced_logic_memory_q_multiplier"])
        delta[j] *= float(cfg["advanced_logic_memory_depreciation_multiplier"])
    elif route == "modular_tools":
        j = params.sector_idx("process_equipment_metrology")
        B[:, j] *= float(cfg["process_equipment_bom_multiplier"])
        q[j] *= float(cfg["process_equipment_q_multiplier"])
        delta[j] *= float(cfg["process_equipment_depreciation_multiplier"])
        q[params.sector_idx("repair")] *= float(cfg["repair_q_multiplier"])
    else:
        raise ValueError(f"unknown design route {route!r}")
    return replace(params, B=B, q=q, delta=delta)


def pareto_seed_designs(
    params: IntegratedParams,
    scenario: str = "moon_asteroid_network",
    *,
    years: float = 40.0,
    dt: float = 0.5,
) -> tuple[ParetoSeedDesign, ...]:
    """Enumerate route/redundancy/source designs and mark the Pareto set."""
    design_cfg = params.robust_seed_design_space
    candidates: list[ParetoCandidate] = []
    for route, route_cfg in design_cfg["routes"].items():
        routed = _route_params(params, route, route_cfg)
        base_seed = size_seed(routed, scenario)
        if not base_seed.feasible:
            continue
        _, _, base_import_mass = base_seed.required_masses()
        for redundancy, redundancy_cfg in design_cfg["redundancy"].items():
            for source, source_cfg in design_cfg["source_portfolios"].items():
                capacities = base_seed.capacities.copy()
                capacities *= float(redundancy_cfg.get("all_sector_multiplier", 1.0))
                for sector, multiplier in redundancy_cfg.get("sectors", {}).items():
                    capacities[routed.sector_idx(sector)] *= float(multiplier)
                for sector, multiplier in source_cfg.get("capacity_sectors", {}).items():
                    capacities[routed.sector_idx(sector)] *= float(multiplier)
                physical = float(base_seed.process.B_effective.sum(axis=0) @ capacities)
                intervention = float(base_seed.process.intervention_hours_per_year @ capacities)
                seed = replace(
                    base_seed,
                    capacities=capacities,
                    physical_seed_mass_t=physical,
                    total_seed_mass_t=(physical + base_import_mass + base_seed.digital_seed_mass_t),
                    intervention_hours_per_year=intervention,
                    lunar_feed_t_per_year=(
                        base_seed.lunar_feed_t_per_year * float(source_cfg["lunar_feed_multiplier"])
                    ),
                    asteroid_feed_t_per_year=(
                        base_seed.asteroid_feed_t_per_year
                        * float(source_cfg["asteroid_feed_multiplier"])
                    ),
                )
                deployment = simulate_seed_deployment(routed, seed)
                run = simulate_capacity_growth(
                    routed,
                    seed,
                    years=years,
                    dt=dt,
                    allocation_policy="maximin_sector",
                    repair_enabled=True,
                )
                endpoints = terminal_endpoints(routed, seed, run)
                outage = simulate_capacity_growth(
                    routed,
                    seed,
                    years=years,
                    dt=dt,
                    allocation_policy="maximin_sector",
                    repair_enabled=True,
                    asteroid_source_outage_windows=((15.0, 20.0, 0.0),),
                )
                candidates.append(
                    {
                        "scenario": scenario,
                        "route": route,
                        "redundancy": redundancy,
                        "source_portfolio": source,
                        "delivered_mass_t": deployment.delivered_seed_mass_t,
                        "import_mass_t": seed.required_masses()[2],
                        "intervention_hours_per_year": intervention,
                        "aggregate_doubling_year": run.aggregate_doubling_year,
                        "operating_at_horizon": float(run.operating_cells[-1]),
                        "terminal_window_expanding": endpoints.terminal_window_expanding,
                        "source_outage_operating_at_horizon": float(outage.operating_cells[-1]),
                        "source_outage_survived": outage.survived,
                    }
                )

    def objective_tuple(candidate: ParetoCandidate) -> tuple[float, ...]:
        doubling = (
            float(candidate["aggregate_doubling_year"])
            if candidate["aggregate_doubling_year"] is not None
            else math.inf
        )
        return (
            float(candidate["delivered_mass_t"]),
            float(candidate["import_mass_t"]),
            float(candidate["intervention_hours_per_year"]),
            doubling,
            -float(candidate["operating_at_horizon"]),
            -float(candidate["source_outage_operating_at_horizon"]),
        )

    points = [objective_tuple(candidate) for candidate in candidates]
    non_dominated = []
    for i, point in enumerate(points):
        dominated = False
        for j, other in enumerate(points):
            if i == j:
                continue
            if all(a <= b + 1e-9 for a, b in zip(other, point, strict=True)) and any(
                a < b - 1e-9 for a, b in zip(other, point, strict=True)
            ):
                dominated = True
                break
        non_dominated.append(not dominated)
    rows = []
    for candidate, is_frontier in zip(candidates, non_dominated, strict=True):
        robust = bool(
            is_frontier
            and candidate["terminal_window_expanding"]
            and candidate["source_outage_survived"]
            and candidate["source_outage_operating_at_horizon"] >= 1.0
        )
        rows.append(
            ParetoSeedDesign(
                **candidate,
                non_dominated=is_frontier,
                robust_candidate=robust,
            )
        )
    return tuple(rows)


# --- intelligence/autonomy ablations ----------------------------------------

ABLATIONS: tuple[tuple[str, str], ...] = (
    ("baseline", "declared coefficients"),
    ("research_automation_frozen", "gain_scale_per_verified_loop = 0"),
    (
        "task_autonomy_improvement_frozen",
        "autonomy_learning_multiplier = 0",
    ),
    (
        "industrial_productivity_improvement_frozen",
        "productivity_elasticity = 0",
    ),
    ("both_couplings_frozen", "productivity_elasticity = autonomy_learning_multiplier = 0"),
    ("capital_reproduction_frozen", "all new-capacity orders = 0"),
)


@dataclass(frozen=True)
class AblationRow:
    variant: str
    definition: str
    feasible: bool
    aggregate_doubling_year: float | None
    operating_at_horizon: float | None
    growth_share_of_baseline: float | None


def _ablated_params(params: IntegratedParams, variant: str) -> IntegratedParams:
    intel = params.intelligence.copy()
    if variant == "research_automation_frozen":
        intel["gain_scale_per_verified_loop"] = 0.0
    if variant in (
        "task_autonomy_improvement_frozen",
        "both_couplings_frozen",
    ):
        intel["autonomy_learning_multiplier"] = 0.0
    if variant in (
        "industrial_productivity_improvement_frozen",
        "both_couplings_frozen",
    ):
        intel["productivity_elasticity"] = 0.0
    return replace(params, intelligence=intel)


def ablation_suite(
    params: IntegratedParams,
    scenario: str,
    *,
    years: float = 40.0,
    dt: float = 0.25,
) -> tuple[AblationRow, ...]:
    """Zero/freeze ablations of the declared intelligence coupling.

    The seed LP does not read the intelligence block, so every dynamics
    variant reuses the identical central seed; only the capacity-growth pass
    changes. The final row re-sizes the seed at AI level 1.0 (coverage
    frozen at its base values) — a seed-level ablation that can be
    infeasible when a scenario's autonomy threshold exceeds base coverage.
    """
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    base_run = simulate_capacity_growth(params, seed, years=years, dt=dt)
    base_growth = float(base_run.operating_cells[-1]) - 1.0
    rows: list[AblationRow] = []
    for variant, definition in ABLATIONS:
        run = (
            base_run
            if variant == "baseline"
            else simulate_capacity_growth(
                _ablated_params(params, variant),
                seed,
                years=years,
                dt=dt,
                capacity_reproduction_enabled=(variant != "capital_reproduction_frozen"),
            )
        )
        growth = float(run.operating_cells[-1]) - 1.0
        rows.append(
            AblationRow(
                variant=variant,
                definition=definition,
                feasible=True,
                aggregate_doubling_year=run.aggregate_doubling_year,
                operating_at_horizon=float(run.operating_cells[-1]),
                growth_share_of_baseline=(
                    growth / base_growth if abs(base_growth) > 1e-9 else None
                ),
            )
        )
    frozen_seed = size_seed(params, scenario, ai_level=1.0)
    if frozen_seed.feasible:
        run = simulate_capacity_growth(params, frozen_seed, years=years, dt=dt)
        growth = float(run.operating_cells[-1]) - 1.0
        rows.append(
            AblationRow(
                "seed_sized_at_base_autonomy",
                "seed re-sized at AI level 1.0",
                True,
                run.aggregate_doubling_year,
                float(run.operating_cells[-1]),
                growth / base_growth if abs(base_growth) > 1e-9 else None,
            )
        )
    else:
        rows.append(
            AblationRow(
                "seed_sized_at_base_autonomy",
                "seed re-sized at AI level 1.0",
                False,
                None,
                None,
                None,
            )
        )
    return tuple(rows)


@dataclass(frozen=True)
class ClosureAblationRow:
    verified_ai_rd_loop: bool
    reproductive_capital_loop: bool
    conceptual_regime: str
    aggregate_doubling_year: float | None
    operating_at_horizon: float
    intelligence_at_horizon: float
    physical_doubling_occurs: bool


def closure_ablation_suite(
    params: IntegratedParams,
    scenario: str,
    *,
    years: float = 40.0,
    dt: float = 0.25,
) -> tuple[ClosureAblationRow, ...]:
    """Cross an active verified AI-R&D proxy with capital reproduction.

    The digital dimension is the implemented verified-loop capability-growth
    channel, not evidence that full AI-R&D closure exists. The physical
    dimension permits or blocks all new-capacity orders while retaining
    depreciation and other state updates.
    """
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    labels = {
        (False, False): ("externally supplied capital; bounded technical progress"),
        (False, True): ("endogenous physical growth with bounded controller"),
        (True, False): ("digital improvement bottlenecked by externally supplied capital"),
        (True, True): "coupled recursive industrial intelligence",
    }
    rows: list[ClosureAblationRow] = []
    for ai_loop in (False, True):
        run_params = params if ai_loop else _ablated_params(params, "research_automation_frozen")
        for capital_loop in (False, True):
            run = simulate_capacity_growth(
                run_params,
                seed,
                years=years,
                dt=dt,
                capacity_reproduction_enabled=capital_loop,
            )
            rows.append(
                ClosureAblationRow(
                    verified_ai_rd_loop=ai_loop,
                    reproductive_capital_loop=capital_loop,
                    conceptual_regime=labels[(ai_loop, capital_loop)],
                    aggregate_doubling_year=run.aggregate_doubling_year,
                    operating_at_horizon=float(run.operating_cells[-1]),
                    intelligence_at_horizon=float(run.intelligence[-1]),
                    physical_doubling_occurs=(run.aggregate_doubling_year is not None),
                )
            )
    return tuple(rows)


# --- finite marginal return to intelligence and bottleneck upgrades --------


@dataclass(frozen=True)
class IntelligenceMarginalResponseRow:
    regime: str
    scenario: str
    intelligence_uplift: float
    baseline_operating_capacity: float
    uplifted_operating_capacity: float
    marginal_operating_capacity_per_intelligence_unit: float
    baseline_doubling_year: float | None
    uplifted_doubling_year: float | None
    doubling_year_acceleration_per_intelligence_unit: float | None
    dominant_constraint: str
    material_constraint_share: float
    leading_limiting_material: str | None
    response_class: str
    complementary_stock_boundary: str


def intelligence_marginal_response_suite(
    params: IntegratedParams,
    config: IntelligenceMarginalResponseConfig,
) -> tuple[IntelligenceMarginalResponseRow, ...]:
    """Finite-response value of capability under declared complements.

    The perturbation changes only the initial capability state while reusing
    the exact seed, material stocks, process graph, and policy for a regime.
    It therefore reports a local scenario derivative, not a general marginal
    product of intelligence.
    """
    uplift = float(config["intelligence_uplift"])
    near_zero = float(config["near_zero_response_threshold"])
    years = float(config["years"])
    dt = float(config["dt"])
    if uplift <= 0.0 or near_zero < 0.0 or years <= 0.0 or dt <= 0.0:
        raise ValueError("invalid intelligence finite-response settings")

    rows: list[IntelligenceMarginalResponseRow] = []
    for regime, cfg in config["regimes"].items():
        scenario = str(cfg["scenario"])
        seed = size_seed(params, scenario)
        if not seed.feasible:
            raise ValueError(f"marginal-response regime {regime!r} has infeasible seed")
        import_stock_multiplier = cfg["import_stock_multiplier"]
        kwargs = {
            "years": years,
            "dt": dt,
            "operational_constraints_enabled": bool(cfg["operational_constraints_enabled"]),
            "import_stock_multiplier": (
                None if import_stock_multiplier is None else float(import_stock_multiplier)
            ),
        }
        baseline = simulate_capacity_growth(params, seed, **kwargs)
        uplifted = simulate_capacity_growth(
            params,
            seed,
            intelligence_level_offset=uplift,
            **kwargs,
        )
        response = (
            float(uplifted.operating_cells[-1]) - float(baseline.operating_cells[-1])
        ) / uplift
        counts = {
            constraint: baseline.primary_constraint.count(constraint)
            for constraint in set(baseline.primary_constraint)
        }
        dominant = max(counts, key=lambda name: counts[name])
        total_steps = max(len(baseline.primary_constraint), 1)
        material_share = counts.get("material", 0) / total_steps
        leading_material = baseline.limiting_elements[0][0] if baseline.limiting_elements else None
        if abs(response) <= near_zero:
            response_class = "near_zero"
        elif response > 0.0:
            response_class = "positive"
        else:
            response_class = "adverse"
        acceleration = None
        if (
            baseline.aggregate_doubling_year is not None
            and uplifted.aggregate_doubling_year is not None
        ):
            acceleration = (
                baseline.aggregate_doubling_year - uplifted.aggregate_doubling_year
            ) / uplift
        rows.append(
            IntelligenceMarginalResponseRow(
                regime=str(regime),
                scenario=scenario,
                intelligence_uplift=uplift,
                baseline_operating_capacity=float(baseline.operating_cells[-1]),
                uplifted_operating_capacity=float(uplifted.operating_cells[-1]),
                marginal_operating_capacity_per_intelligence_unit=response,
                baseline_doubling_year=baseline.aggregate_doubling_year,
                uplifted_doubling_year=uplifted.aggregate_doubling_year,
                doubling_year_acceleration_per_intelligence_unit=acceleration,
                dominant_constraint=dominant,
                material_constraint_share=material_share,
                leading_limiting_material=leading_material,
                response_class=response_class,
                complementary_stock_boundary=str(cfg["complementary_stock_boundary"]).strip(),
            )
        )
    return tuple(rows)


@dataclass(frozen=True)
class BottleneckUpgradeResult:
    project: str
    constraint: str
    constraint_class: str
    intelligence_can_reduce: bool
    cost_capacity_years: float
    available_budget_capacity_years: float
    design_lag_years: float
    construction_lag_years: float
    verification_lag_years: float
    commission_year: float | None
    initial_capacity: float
    capacity_increment: float
    capacity_at_horizon: float
    productive_capacity_available: bool
    verified_causal_path: bool
    productive_sector: str
    causal_path: str
    t: FloatArray
    capacity: FloatArray


def bottleneck_upgrade_suite(
    config: BottleneckUpgradeConfig,
) -> tuple[BottleneckUpgradeResult, ...]:
    """Gate proposed bottleneck relief by cost, lag, production, and evidence."""
    years = float(config["years"])
    dt = float(config["dt"])
    if years <= 0.0 or dt <= 0.0:
        raise ValueError("upgrade horizon and step must be positive")
    steps = round(years / dt)
    t = np.arange(steps + 1, dtype=float) * dt
    allowed_classes = {
        "intelligence_reducible",
        "physical_floor",
        "observation_time",
        "external_authority",
    }
    rows: list[BottleneckUpgradeResult] = []
    for name, cfg in config["projects"].items():
        constraint_class = str(cfg["constraint_class"])
        if constraint_class not in allowed_classes:
            raise ValueError(f"unknown constraint class {constraint_class!r}")
        reducible = bool(cfg["intelligence_can_reduce"])
        initial = float(cfg["initial_capacity"])
        increment = float(cfg["capacity_increment"])
        cost = float(cfg["cost_capacity_years"])
        budget = float(cfg["available_budget_capacity_years"])
        design_lag = float(cfg["design_lag_years"])
        construction_lag = float(cfg["construction_lag_years"])
        verification_lag = float(cfg["verification_lag_years"])
        productive = bool(cfg["productive_capacity_available"])
        verified = bool(cfg["verified_causal_path"])
        productive_sector = str(cfg["productive_sector"]).strip()
        causal_path = str(cfg["causal_path"]).strip()
        if (
            min(
                initial,
                increment,
                cost,
                budget,
                design_lag,
                construction_lag,
                verification_lag,
            )
            < 0.0
        ):
            raise ValueError("upgrade values must be nonnegative")
        if reducible and (
            increment <= 0.0 or cost <= 0.0 or not productive_sector or not causal_path
        ):
            raise ValueError(
                "reducible upgrades require positive increment/cost and a "
                "productive-sector causal path"
            )
        if not reducible and increment > 0.0:
            raise ValueError(
                "irreducible or externally imposed constraints cannot receive "
                "an automatic capacity increment"
            )
        commission = None
        if reducible and productive and verified and budget + 1e-12 >= cost:
            commission = design_lag + construction_lag + verification_lag
        capacity = np.full(steps + 1, initial, dtype=float)
        if commission is not None and commission <= years + 1e-12:
            capacity[t + 1e-12 >= commission] += increment
        rows.append(
            BottleneckUpgradeResult(
                project=str(name),
                constraint=str(cfg["constraint"]),
                constraint_class=constraint_class,
                intelligence_can_reduce=reducible,
                cost_capacity_years=cost,
                available_budget_capacity_years=budget,
                design_lag_years=design_lag,
                construction_lag_years=construction_lag,
                verification_lag_years=verification_lag,
                commission_year=commission,
                initial_capacity=initial,
                capacity_increment=increment,
                capacity_at_horizon=float(capacity[-1]),
                productive_capacity_available=productive,
                verified_causal_path=verified,
                productive_sector=productive_sector,
                causal_path=causal_path,
                t=t,
                capacity=capacity,
            )
        )
    return tuple(rows)


@dataclass(frozen=True)
class ComputeDemandAllocationResult:
    branch: str
    demand_type: str
    t: FloatArray
    available_compute: FloatArray
    valuable_demand: FloatArray
    used_compute: FloatArray
    unmet_demand: FloatArray
    humanitarian_compute: FloatArray
    science_public_goods_compute: FloatArray
    industrial_expansion_compute: FloatArray
    relocated_harmful_activity: FloatArray
    expanded_activity_above_initial: FloatArray


def compute_demand_allocation_suite(
    config: ComputeDemandConfig,
) -> tuple[ComputeDemandAllocationResult, ...]:
    """Separate demand saturation, allocation, relocation, and expansion."""

    def _fraction(value: float, name: str) -> float:
        result = float(value)
        if not 0.0 <= result <= 1.0:
            raise ValueError(f"{name} must be in [0, 1]")
        return result

    years = float(config["years"])
    dt = float(config["dt"])
    initial_supply = float(config["initial_compute_capacity"])
    supply_growth = float(config["annual_compute_capacity_growth_fraction"])
    initial_activity = float(config["initial_activity_reference"])
    if (
        years <= 0.0
        or dt <= 0.0
        or initial_supply < 0.0
        or supply_growth < 0.0
        or initial_activity < 0.0
    ):
        raise ValueError("invalid demand-allocation settings")
    steps = round(years / dt)
    t = np.arange(steps + 1, dtype=float) * dt
    available = initial_supply * (1.0 + supply_growth) ** t
    rows: list[ComputeDemandAllocationResult] = []
    for name, branch in config["branches"].items():
        demand_type = str(branch["demand_type"])
        initial_demand = float(branch["initial_valuable_demand"])
        demand_growth = float(branch["demand_growth_rate"])
        if initial_demand < 0.0 or demand_growth < 0.0:
            raise ValueError("demand values must be nonnegative")
        if demand_type == "non_saturating":
            demand = initial_demand * (1.0 + demand_growth) ** t
        elif demand_type == "bounded":
            ceiling_value = branch.get("valuable_demand_ceiling")
            if ceiling_value is None:
                raise ValueError("bounded demand requires a valuable-demand ceiling")
            ceiling = float(ceiling_value)
            if ceiling < initial_demand:
                raise ValueError("bounded demand ceiling below initial demand")
            demand = ceiling - (ceiling - initial_demand) * np.exp(-demand_growth * t)
        else:
            raise ValueError(f"unknown demand type {demand_type!r}")
        used = np.minimum(available, demand)
        switch_year = float(branch["priority_switch_year"])
        early_humanitarian = _fraction(
            branch["early_humanitarian_share"],
            "early_humanitarian_share",
        )
        late_humanitarian = _fraction(
            branch["late_humanitarian_share"],
            "late_humanitarian_share",
        )
        science_share = _fraction(
            branch["science_public_goods_share"],
            "science_public_goods_share",
        )
        relocation_share = _fraction(
            branch["relocated_harmful_activity_share"],
            "relocated_harmful_activity_share",
        )
        humanitarian_share = np.where(
            t < switch_year,
            early_humanitarian,
            late_humanitarian,
        )
        if np.any(humanitarian_share + science_share > 1.0 + 1e-12):
            raise ValueError("allocation shares exceed one")
        humanitarian = used * humanitarian_share
        science = used * science_share
        industrial = np.maximum(used - humanitarian - science, 0.0)
        rows.append(
            ComputeDemandAllocationResult(
                branch=str(name),
                demand_type=demand_type,
                t=t,
                available_compute=available.copy(),
                valuable_demand=demand,
                used_compute=used,
                unmet_demand=np.maximum(demand - available, 0.0),
                humanitarian_compute=humanitarian,
                science_public_goods_compute=science,
                industrial_expansion_compute=industrial,
                relocated_harmful_activity=used * relocation_share,
                expanded_activity_above_initial=np.maximum(
                    used - initial_activity,
                    0.0,
                ),
            )
        )
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
    params: IntegratedParams,
    scenario: str,
    *,
    factors: tuple[float, ...] = (1.0, 1.25, 1.5, 2.0),
    years: float = 40.0,
    dt: float = 0.25,
) -> tuple[FrontierRow, ...]:
    """Installed mass versus aggregate-capacity-doubling time.

    A factor-f seed installs f cell-equivalents of the minimum-mass
    design (capacities, feeds, and strategic import stock all scale with f; the
    one digital package is shared). The recorded time is first passage to
    one *additional* operating cell-equivalent, so f = 1 coincides with
    the canonical first-passage-to-two metric.
    """
    seed = size_seed(params, scenario)
    if not seed.feasible:
        return ()
    _, physical_mass, import_mass = seed.required_masses()
    scalable = physical_mass + import_mass
    rows = []
    for f in factors:
        run = simulate_capacity_growth(params, seed, years=years, dt=dt, initial_cells=f)
        reached = np.flatnonzero(run.operating_cells >= f + 1.0)
        rows.append(
            FrontierRow(
                oversize_factor=float(f),
                installed_mass_t=f * scalable + seed.digital_seed_mass_t,
                time_to_one_additional_cell=(float(run.t[reached[0]]) if len(reached) else None),
                additional_cells_at_horizon=float(run.operating_cells[-1] - f),
                retained_plus_one_at_horizon=bool(run.operating_cells[-1] >= f + 1.0),
            )
        )
    return tuple(rows)


# --- ensemble diagnostics ----------------------------------------------------


@dataclass(frozen=True)
class DrawRecord:
    run_index: int
    draws: dict[str, float]
    feasible: bool
    failure_reason: str | None
    seed_mass_t: float | None
    aggregate_doubling_year: float | None
    operating_at_horizon: float | None
    retained_at_horizon: bool | None
    terminal_window_expanding: bool | None
    top_binding_constraint: str | None


@dataclass(frozen=True)
class DiagnosticsSummary:
    scenario: str
    n_runs: int
    records: tuple[DrawRecord, ...]
    failure_histogram: dict[str, int]
    binding_histogram: dict[str, int]
    n_retained: int
    n_terminal_window_expanding: int
    sensitivity: dict[str, dict[str, float]]

    @property
    def n_feasible(self) -> int:
        return sum(r.feasible for r in self.records)


def ensemble_diagnostics(
    params: IntegratedParams,
    scenario: str,
    *,
    n_runs: int = 200,
    seed: int = 404,
    years: float = 40.0,
    dt: float = 0.5,
) -> DiagnosticsSummary:
    """Re-run the exact named draws of ``seed_ensemble`` and keep the
    per-draw detail it discards: failure reasons, binding constraints,
    terminal-window endpoints, and Spearman sensitivity of every named
    multiplier against seed mass, aggregate doubling, and horizon
    cell-equivalents."""
    records: list[DrawRecord] = []
    for i in range(n_runs):
        draws = {
            name: _named_loguniform(seed, i, name, bounds)
            for name, bounds in params.uncertainty.items()
        }
        sampled = sample_integrated_params(params, seed=seed, run_index=i)
        sized = size_seed(sampled, scenario)
        if not sized.feasible:
            reason = (
                "autonomy_threshold"
                if sized.status.startswith("autonomy threshold")
                else "lp_infeasible"
            )
            records.append(DrawRecord(i, draws, False, reason, None, None, None, None, None, None))
            continue
        run = simulate_capacity_growth(sampled, sized, years=years, dt=dt)
        ends = terminal_endpoints(sampled, sized, run)
        total_mass, _, _ = sized.required_masses()
        records.append(
            DrawRecord(
                run_index=i,
                draws=draws,
                feasible=True,
                failure_reason=None,
                seed_mass_t=total_mass,
                aggregate_doubling_year=run.aggregate_doubling_year,
                operating_at_horizon=ends.operating_at_horizon,
                retained_at_horizon=ends.retained_at_horizon,
                terminal_window_expanding=ends.terminal_window_expanding,
                top_binding_constraint=(
                    sized.binding_constraints[0][0] if sized.binding_constraints else None
                ),
            )
        )

    failure_hist: dict[str, int] = {}
    binding_hist: dict[str, int] = {}
    for r in records:
        if not r.feasible:
            reason = r.failure_reason or "unspecified"
            failure_hist[reason] = failure_hist.get(reason, 0) + 1
        elif r.top_binding_constraint:
            binding_hist[r.top_binding_constraint] = (
                binding_hist.get(r.top_binding_constraint, 0) + 1
            )

    feasible = [r for r in records if r.feasible]
    outputs: dict[str, list[float]] = {
        "seed_mass_t": [],
        "aggregate_doubling_year": [],
        "operating_at_horizon": [],
    }
    kept: dict[str, list[dict[str, float]]] = {k: [] for k in outputs}
    for r in feasible:
        for key, value in (
            ("seed_mass_t", r.seed_mass_t),
            ("aggregate_doubling_year", r.aggregate_doubling_year),
            ("operating_at_horizon", r.operating_at_horizon),
        ):
            if value is not None:
                outputs[key].append(float(value))
                kept[key].append(r.draws)
    sensitivity: dict[str, dict[str, float]] = {}
    for name in params.uncertainty:
        sensitivity[name] = {}
        for key, values in outputs.items():
            if len(values) >= 8:
                xs = [d[name] for d in kept[key]]
                rho = spearman_correlation(
                    np.asarray(xs, dtype=float),
                    np.asarray(values, dtype=float),
                )
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
        n_terminal_window_expanding=sum(bool(r.terminal_window_expanding) for r in feasible),
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
    params: IntegratedParams,
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
    solved = solve_linear_program(
        c_e,
        a_ub=A_e,
        b_ub=b_ub,
        bounds=bounds,
    )
    if not solved.success:
        raise RuntimeError(f"elastic relaxation failed: {solved.message}")
    slack = solved.x[nv:]
    rows = [
        CertificateRow(
            constraint=labels[i],
            minimum_violation=float(slack[i]),
            units=_ROW_UNITS.get(labels[i].split(":", 1)[0], "row-native"),
        )
        for i in np.argsort(-slack)
        if slack[i] > tolerance
    ]
    return tuple(rows)
