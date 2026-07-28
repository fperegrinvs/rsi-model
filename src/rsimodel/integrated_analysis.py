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

Everything here is derived from coefficients already declared in
``params/integrated_model.yaml``; outputs remain scenario implications, not
measurements or probabilities. Items that require new ASSUMPTION-class
coefficients (independent sector build allocation and repair, a delivered-
seed deployment stage, shock-recovery endpoints, and shell-resolved debris)
stay in ROADMAP pending authorial sign-off.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Any

import numpy as np
from scipy.optimize import linprog
from scipy.stats import spearmanr

from .integrated import (CapacityGrowthResult, IntegratedParams, SeedResult,
                     _named_loguniform, build_seed_lp, process_profile,
                     sample_integrated_params, simulate_capacity_growth,
                     simulate_seed_deployment, size_seed)

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
        rows.append(ImportStockRow(
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
        ))
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
        service_limit = float(np.min(np.divide(
            seed.process.q_effective * op_sector,
            service_need,
            out=np.full(params.n, np.inf),
            where=service_need > 1e-12,
        )))
        rate_cap = (
            float(params.seed[
                "maximum_gross_cell_orders_per_operating_cell_year"
            ])
            * aggregate_op
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
            shock_label = (
                f"{shock_sector}:{shock_fraction:.0%}@year{shock_year:g}"
            )
            j = params.sector_idx(shock_sector)
            event_k = int(np.searchsorted(run.t, shock_year))
            reference_k = max(event_k - 1, 0)
            reference = float(run.operating_sector_capacity[reference_k, j])
            recovered = np.flatnonzero(
                run.operating_sector_capacity[event_k:, j]
                >= reference - 1e-9
            )
            if len(recovered):
                recovery_year = float(run.t[event_k + recovered[0]])
        rows.append(AllocationRepairRow(
            scenario=scenario,
            policy=policy,
            repair_enabled=repair,
            shock=shock_label,
            aggregate_doubling_year=run.aggregate_doubling_year,
            operating_at_horizon=float(run.operating_cells[-1]),
            minimum_sector_margin_at_horizon=float(np.min(normalized)),
            survived=run.survived,
            shock_recovery_year=recovery_year,
            cumulative_repaired_capacity=float(
                run.repaired_sector_capacity.sum()
            ),
        ))
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
    variants: tuple[tuple[str, dict[str, Any]], ...] = (
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
        rows.append(KnowledgeRegimeRow(
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
        ))
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
            rows.append(EnvironmentEffectRow(
                scenario, environment_profile, False, None, None,
                None, None, None,
            ))
            continue
        run = simulate_capacity_growth(
            params,
            seed,
            years=years,
            dt=dt,
        )
        rows.append(EnvironmentEffectRow(
            scenario=scenario,
            environment_profile=environment_profile,
            feasible=True,
            seed_mass_t=float(seed.total_seed_mass_t),
            top_binding_constraint=(
                seed.binding_constraints[0][0]
                if seed.binding_constraints else None
            ),
            operating_at_horizon=float(run.operating_cells[-1]),
            aggregate_doubling_year=run.aggregate_doubling_year,
            survived=run.survived,
        ))
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
            import_multiplier = (
                value
                if dimension == "retained_import_stock_fraction"
                else 1.0
            )
            initial_cells = (
                value if dimension == "initial_surplus_cells" else 1.0
            )
            depreciation = (
                value if dimension == "obsolescence_multiplier" else 1.0
            )
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
                window = max(1, int(round(5.0 / dt)))
                final_change = float(
                    run.operating_cells[-1]
                    - run.operating_cells[max(len(run.t) - 1 - window, 0)]
                )
                normalized = np.divide(
                    run.operating_sector_capacity[-1],
                    seed.capacities,
                    out=np.zeros(params.n),
                    where=seed.capacities > 1e-12,
                )
                rows.append(PolicyRobustnessRow(
                    scenario=scenario,
                    sweep_dimension=dimension,
                    sweep_value=float(value),
                    policy=policy,
                    horizon_years=float(horizon),
                    survived=run.survived,
                    terminal_window_expanding=bool(final_change > 0.0),
                    operating_at_horizon=float(run.operating_cells[-1]),
                    minimum_sector_margin_at_horizon=float(
                        np.min(normalized)
                    ),
                    aggregate_doubling_year=run.aggregate_doubling_year,
                ))
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
    cfg = params.raw["electronics_closure"]
    tiers = tuple(cfg["tiers"])
    indices = [params.sector_idx(tier) for tier in tiers]
    rows = []
    for architecture, arch in cfg["architectures"].items():
        inventory = np.array([
            seed.capacities[j]
            * float(arch["initial_import_inventory_fraction"])
            for j in indices
        ])
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
            for x, (tier, j) in enumerate(zip(tiers, indices)):
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
                    * (
                        float(params.delta[j])
                        + float(tier_cfg["obsolescence_per_year"])
                    )
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
                        demand * float(
                            arch["mature_substitution_credit_fraction"]
                        ),
                    )
                imported = (
                    seed.capacities[j]
                    * float(
                        arch[
                            "annual_import_fraction_of_initial_capacity"
                        ]
                    )
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
                mass_per_capacity = float(
                    seed.process.B_effective[:, j].sum()
                )
                totals["imported_mass"][x] += imported * mass_per_capacity
        for x, (tier, j) in enumerate(zip(tiers, indices)):
            rows.append(ElectronicsArchitectureRow(
                scenario=scenario,
                architecture=architecture,
                tier=tier,
                replacement_demand_capacity=float(totals["demand"][x]),
                local_supply_capacity=float(totals["local"][x]),
                imported_supply_capacity=float(totals["imports"][x]),
                cannibalized_supply_capacity=float(
                    totals["cannibal"][x]
                ),
                substitution_credit_capacity=float(
                    totals["substitution"][x]
                ),
                expired_inventory_capacity=float(totals["expired"][x]),
                terminal_import_inventory_capacity=float(inventory[x]),
                shortfall_capacity=float(totals["shortfall"][x]),
                first_shortfall_year=first_shortfall[x],
                viable=bool(totals["shortfall"][x] <= 1e-9),
                imported_mass_t=float(totals["imported_mass"][x]),
                measurement_priority=str(
                    cfg["tiers"][tier]["measurement_priority"]
                ),
            ))
    return tuple(rows)


# --- symmetric dynamic economics --------------------------------------------

@dataclass(frozen=True)
class EconomicTrajectory:
    scenario: str
    market: str
    t: np.ndarray
    technical_space_capacity: np.ndarray
    funded_space_capacity: np.ndarray
    earth_capacity: np.ndarray
    market_demand: np.ndarray
    space_cash_musd: np.ndarray
    earth_cash_musd: np.ndarray
    space_debt_musd: np.ndarray
    earth_debt_musd: np.ndarray
    space_investment_musd: np.ndarray
    earth_investment_musd: np.ndarray
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
    cfg = params.raw["dynamic_economics"]
    if market not in cfg["markets"]:
        raise ValueError(f"unknown economic market {market!r}")
    mkt = cfg["markets"][market]
    space_cfg = cfg["space"]
    earth_cfg = cfg["earth"]
    t = run.t
    dt = float(t[1] - t[0])
    n = len(t)
    technical_space = (
        run.local_compute / max(float(run.local_compute[0]), 1e-12)
    )
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
    space_cash[0] = (
        float(space_cfg["initial_equity_musd"])
        + float(space_cfg["bridge_financing_musd"])
    )
    earth_cash[0] = (
        float(earth_cfg["initial_equity_musd"])
        + float(earth_cfg["bridge_financing_musd"])
    )
    space_lag = max(
        1, int(round(float(space_cfg["regulatory_delay_years"]) / dt))
    )
    earth_lag = max(
        1, int(round(float(earth_cfg["regulatory_delay_years"]) / dt))
    )
    space_queue = np.zeros(space_lag)
    earth_queue = np.zeros(earth_lag)
    cumulative_space_capacity = 1.0
    cumulative_earth_capacity = 1.0
    cumulative_space_revenue = 0.0
    cumulative_earth_revenue = 0.0
    cumulative_space_cost = float(
        space_cfg["initial_equity_musd"]
    ) + float(space_cfg["bridge_financing_musd"])
    cumulative_earth_cost = float(
        earth_cfg["initial_equity_musd"]
    ) + float(earth_cfg["bridge_financing_musd"])
    space_self_financing = None
    earth_self_financing = None
    space_constrained = earth_constrained = 0
    physical_mass_per_step = np.sum(
        seed.process.B_effective @ run.ordered_sector_capacity.T,
        axis=0,
    )

    for k in range(n - 1):
        demand[k + 1] = min(
            demand[k]
            * math.exp(float(mkt["demand_growth_per_year"]) * dt),
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
        funded_share = funded_space[k] / max(
            float(technical_space[k]), 1e-12
        )
        space_opex = (
            funded_space[k]
            * float(space_cfg[
                "operating_cost_musd_per_compute_unit_year"
            ])
            * dt
            + physical_mass_per_step[k] * funded_share
            * float(space_cfg["material_transfer_cost_musd_per_t"])
            + float(run.intervention_demand_hours[k]) * funded_share
            * float(space_cfg["intervention_cost_musd_per_hour"])
            * dt
        )
        earth_opex = (
            earth_capacity[k]
            * float(earth_cfg[
                "operating_cost_musd_per_compute_unit_year"
            ])
            * dt
        )
        space_interest = (
            space_debt[k] * float(space_cfg["wacc"]) * dt
        )
        earth_interest = (
            earth_debt[k] * float(earth_cfg["wacc"]) * dt
        )
        preinvestment_space_cash = (
            space_cash[k] + space_revenue - space_opex - space_interest
        )
        preinvestment_earth_cash = (
            earth_cash[k] + earth_revenue - earth_opex - earth_interest
        )

        due_space = space_queue[0]
        space_queue[:-1] = space_queue[1:]
        space_queue[-1] = 0.0
        due_earth = earth_queue[0]
        earth_queue[:-1] = earth_queue[1:]
        earth_queue[-1] = 0.0
        after_depreciation_space = max(
            funded_space[k]
            * (1.0 - float(space_cfg["depreciation_per_year"]) * dt)
            + due_space,
            0.0,
        )
        after_depreciation_earth = max(
            earth_capacity[k]
            * (1.0 - float(earth_cfg["depreciation_per_year"]) * dt)
            + due_earth,
            0.0,
        )
        desired_space = max(
            technical_space[k + 1]
            - after_depreciation_space
            - float(space_queue.sum()),
            0.0,
        )
        resource_ceiling = (
            float(earth_cfg["initial_resource_ceiling_units"])
            + float(earth_cfg[
                "induced_resource_ceiling_units_per_year"
            ])
            * t[k]
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
            float(space_cfg["max_debt_to_annual_revenue"])
            * space_revenue / max(dt, 1e-12)
        )
        max_earth_debt = (
            float(earth_cfg["max_debt_to_annual_revenue"])
            * earth_revenue / max(dt, 1e-12)
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
        if (
            space_self_financing is None
            and cumulative_space_revenue >= cumulative_space_cost
        ):
            space_self_financing = float(t[k + 1])
        if (
            earth_self_financing is None
            and cumulative_earth_revenue >= cumulative_earth_cost
        ):
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


def _route_params(
    params: IntegratedParams,
    route: str,
    cfg: dict[str, Any],
) -> IntegratedParams:
    if route == "baseline":
        return params
    B = params.B.copy()
    q = params.q.copy()
    delta = params.delta.copy()
    if route == "mature_node":
        j = params.sector_idx("advanced_logic_memory")
        B[:, j] *= float(cfg["advanced_logic_memory_bom_multiplier"])
        B[params.element_idx("dopants"), j] = (
            params.B[params.element_idx("dopants"), j]
            * float(cfg["advanced_logic_memory_dopants_multiplier"])
        )
        q[j] *= float(cfg["advanced_logic_memory_q_multiplier"])
        delta[j] *= float(
            cfg["advanced_logic_memory_depreciation_multiplier"]
        )
    elif route == "modular_tools":
        j = params.sector_idx("process_equipment_metrology")
        B[:, j] *= float(cfg["process_equipment_bom_multiplier"])
        q[j] *= float(cfg["process_equipment_q_multiplier"])
        delta[j] *= float(
            cfg["process_equipment_depreciation_multiplier"]
        )
        q[params.sector_idx("repair")] *= float(
            cfg["repair_q_multiplier"]
        )
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
    design_cfg = params.raw["robust_seed_design_space"]
    candidates: list[dict[str, Any]] = []
    for route, route_cfg in design_cfg["routes"].items():
        routed = _route_params(params, route, route_cfg)
        base_seed = size_seed(routed, scenario)
        if not base_seed.feasible:
            continue
        for redundancy, redundancy_cfg in design_cfg["redundancy"].items():
            for source, source_cfg in design_cfg[
                "source_portfolios"
            ].items():
                capacities = base_seed.capacities.copy()
                capacities *= float(
                    redundancy_cfg.get("all_sector_multiplier", 1.0)
                )
                for sector, multiplier in redundancy_cfg.get(
                    "sectors", {}
                ).items():
                    capacities[routed.sector_idx(sector)] *= float(
                        multiplier
                    )
                for sector, multiplier in source_cfg.get(
                    "capacity_sectors", {}
                ).items():
                    capacities[routed.sector_idx(sector)] *= float(
                        multiplier
                    )
                physical = float(
                    base_seed.process.B_effective.sum(axis=0)
                    @ capacities
                )
                intervention = float(
                    base_seed.process.intervention_hours_per_year
                    @ capacities
                )
                seed = replace(
                    base_seed,
                    capacities=capacities,
                    physical_seed_mass_t=physical,
                    total_seed_mass_t=(
                        physical
                        + float(base_seed.import_stock_mass_t)
                        + base_seed.digital_seed_mass_t
                    ),
                    intervention_hours_per_year=intervention,
                    lunar_feed_t_per_year=(
                        base_seed.lunar_feed_t_per_year
                        * float(source_cfg["lunar_feed_multiplier"])
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
                    asteroid_source_outage_windows=(
                        (15.0, 20.0, 0.0),
                    ),
                )
                candidates.append({
                    "scenario": scenario,
                    "route": route,
                    "redundancy": redundancy,
                    "source_portfolio": source,
                    "delivered_mass_t": deployment.delivered_seed_mass_t,
                    "import_mass_t": float(seed.import_stock_mass_t),
                    "intervention_hours_per_year": intervention,
                    "aggregate_doubling_year": run.aggregate_doubling_year,
                    "operating_at_horizon": float(run.operating_cells[-1]),
                    "terminal_window_expanding":
                        endpoints.terminal_window_expanding,
                    "source_outage_operating_at_horizon":
                        float(outage.operating_cells[-1]),
                    "source_outage_survived": outage.survived,
                })

    def objective_tuple(candidate: dict[str, Any]) -> tuple[float, ...]:
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
            if all(a <= b + 1e-9 for a, b in zip(other, point)) and any(
                a < b - 1e-9 for a, b in zip(other, point)
            ):
                dominated = True
                break
        non_dominated.append(not dominated)
    rows = []
    for candidate, is_frontier in zip(candidates, non_dominated):
        robust = bool(
            is_frontier
            and candidate["terminal_window_expanding"]
            and candidate["source_outage_survived"]
            and candidate["source_outage_operating_at_horizon"] >= 1.0
        )
        rows.append(ParetoSeedDesign(
            **candidate,
            non_dominated=is_frontier,
            robust_candidate=robust,
        ))
    return tuple(rows)


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
    aggregate_doubling_year: float | None
    operating_at_horizon: float | None
    growth_share_of_baseline: float | None


def _ablated_params(params: IntegratedParams, variant: str) -> IntegratedParams:
    intel = dict(params.intelligence)
    if variant in ("no_intelligence_growth",):
        intel["learning_rate_per_year"] = 0.0
    if variant in ("productivity_channel_only", "fully_uncoupled"):
        intel["autonomy_learning_multiplier"] = 0.0
    if variant in ("autonomy_channel_only", "fully_uncoupled"):
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
        run = (base_run if variant == "baseline" else simulate_capacity_growth(
            _ablated_params(params, variant), seed, years=years, dt=dt))
        growth = float(run.operating_cells[-1]) - 1.0
        rows.append(AblationRow(
            variant=variant,
            definition=definition,
            feasible=True,
            aggregate_doubling_year=run.aggregate_doubling_year,
            operating_at_horizon=float(run.operating_cells[-1]),
            growth_share_of_baseline=(
                growth / base_growth if abs(base_growth) > 1e-9 else None
            ),
        ))
    frozen_seed = size_seed(params, scenario, ai_level=1.0)
    if frozen_seed.feasible:
        run = simulate_capacity_growth(params, frozen_seed, years=years, dt=dt)
        growth = float(run.operating_cells[-1]) - 1.0
        rows.append(AblationRow(
            "seed_sized_at_base_autonomy", "seed re-sized at AI level 1.0",
            True, run.aggregate_doubling_year, float(run.operating_cells[-1]),
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
    scalable = float(seed.physical_seed_mass_t + seed.import_stock_mass_t)
    rows = []
    for f in factors:
        run = simulate_capacity_growth(
            params, seed, years=years, dt=dt, initial_cells=f
        )
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
            reason = ("autonomy_threshold"
                      if sized.status.startswith("autonomy threshold")
                      else "lp_infeasible")
            records.append(DrawRecord(i, draws, False, reason, None, None,
                                      None, None, None, None))
            continue
        run = simulate_capacity_growth(sampled, sized, years=years, dt=dt)
        ends = terminal_endpoints(sampled, sized, run)
        records.append(DrawRecord(
            run_index=i,
            draws=draws,
            feasible=True,
            failure_reason=None,
            seed_mass_t=float(sized.total_seed_mass_t),
            aggregate_doubling_year=run.aggregate_doubling_year,
            operating_at_horizon=ends.operating_at_horizon,
            retained_at_horizon=ends.retained_at_horizon,
            terminal_window_expanding=ends.terminal_window_expanding,
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
    outputs: dict[str, list[float]] = {
        "seed_mass_t": [],
        "aggregate_doubling_year": [],
        "operating_at_horizon": [],
    }
    kept: dict[str, list[dict[str, float]]] = {k: [] for k in outputs}
    for r in feasible:
        for key, value in (("seed_mass_t", r.seed_mass_t),
                           ("aggregate_doubling_year", r.aggregate_doubling_year),
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
        n_terminal_window_expanding=sum(
            bool(r.terminal_window_expanding) for r in feasible
        ),
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
