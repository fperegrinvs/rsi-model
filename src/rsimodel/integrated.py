"""Current integrated bootstrap model.

This module is deliberately separate from the current ten-sector model.  It
adds the structures that the Current manuscript names as missing:

* seven non-substitutable electronics tiers;
* element-by-sector bills of material and source-specific recoverable yields;
* an explicit lunar-surface / asteroid / Earth-import material graph;
* process-specific gravity overhead;
* task-resolved embodied autonomy and residual intervention demand;
* commissioning lags, yield ramps, minimum viable scale, and aggregate
  operating-capacity doubling;
* a coupled, intentionally stylized intelligence/compute/productivity loop;
* rate-limited terrestrial and Earth-fed orbital compute counterfactuals; and
* endogenous debris stocks with a reported five-year fragment
  creation-to-clearance ratio.

The numerical coefficients in ``params/integrated_model.yaml`` are scenario
assumptions unless a source reference is named.  A cited composition datum
does not turn a recovery yield, plant recipe, or seed mass into a
measurement.  Results are mechanical implications of the named scenarios,
not forecasts or empirical probabilities.
"""
from __future__ import annotations

import math
import zlib
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from scipy.optimize import linprog

PARAMS_PATH = Path(__file__).resolve().parents[2] / "params" / "integrated_model.yaml"


@dataclass(frozen=True)
class IntegratedParams:
    version: str
    elements: tuple[str, ...]
    sectors: tuple[str, ...]
    q: np.ndarray
    delta: np.ndarray
    min_seed: np.ndarray
    lag: np.ndarray
    ramp: np.ndarray
    gravity_required: np.ndarray
    centrifuge_radius: np.ndarray
    base_coverage: np.ndarray
    coverage_ceiling: np.ndarray
    coverage_response: np.ndarray
    intervention_hours: np.ndarray
    B: np.ndarray
    A: np.ndarray
    lunar_yield: np.ndarray
    asteroid_yield: np.ndarray
    processing: dict[str, float]
    environment: dict[str, Any]
    scenarios: dict[str, dict[str, Any]]
    seed: dict[str, float]
    intelligence: dict[str, float]
    transfer_arcs: dict[str, Any]
    earth_compute: dict[str, Any]
    debris: dict[str, Any]
    uncertainty: dict[str, tuple[float, float]]
    raw: dict[str, Any]

    @property
    def n(self) -> int:
        return len(self.sectors)

    @property
    def m(self) -> int:
        return len(self.elements)

    def sector_idx(self, name: str) -> int:
        return self.sectors.index(name)

    def element_idx(self, name: str) -> int:
        return self.elements.index(name)


@dataclass(frozen=True)
class ProcessProfile:
    scenario: str
    environment_profile: str
    ai_level: float
    coverage: np.ndarray
    q_effective: np.ndarray
    B_effective: np.ndarray
    centrifuge_rpm: np.ndarray
    centrifuge_mass_t: np.ndarray
    intervention_hours_per_year: np.ndarray
    named_task_completion_rate: np.ndarray
    fault_diagnosis_fraction: np.ndarray
    verification_throughput_per_year: np.ndarray
    engineering_cycle_years: np.ndarray
    process_yield: np.ndarray
    repair_success_fraction: np.ndarray
    mean_time_to_recovery_days: np.ndarray
    stop_line_task_pass: np.ndarray
    environment_throughput_multiplier: np.ndarray
    environment_yield_multiplier: np.ndarray
    environment_depreciation_multiplier: np.ndarray
    environment_power_demand_multiplier: np.ndarray

    @property
    def minimum_coverage(self) -> float:
        return float(np.min(self.coverage))


@dataclass(frozen=True)
class SeedResult:
    scenario: str
    feasible: bool
    status: str
    total_seed_mass_t: float | None
    physical_seed_mass_t: float | None
    import_stock_mass_t: float | None
    digital_seed_mass_t: float
    capacities: np.ndarray
    import_stock_t: np.ndarray
    lunar_feed_t_per_year: float
    asteroid_feed_t_per_year: float
    minimum_task_coverage: float
    intervention_hours_per_year: float
    binding_constraints: tuple[tuple[str, float], ...]
    process: ProcessProfile

    def capacity(self, params: IntegratedParams, sector: str) -> float:
        return float(self.capacities[params.sector_idx(sector)])


@dataclass(frozen=True)
class CapacityGrowthResult:
    scenario: str
    t: np.ndarray
    installed_sector_capacity: np.ndarray
    operating_sector_capacity: np.ndarray
    ordered_sector_capacity: np.ndarray
    installed_cells: np.ndarray
    operating_cells: np.ndarray
    intelligence: np.ndarray
    local_compute: np.ndarray
    inventory_t: np.ndarray
    ordered_cells: np.ndarray
    aggregate_doubling_year: float | None
    survived: bool
    limiting_elements: tuple[tuple[str, int], ...]
    lunar_material_t: float
    asteroid_material_t: float
    recycled_material_t: float
    failed_sector_capacity: np.ndarray
    repaired_sector_capacity: np.ndarray
    commissioned_sector_capacity: np.ndarray
    activated_sector_capacity: np.ndarray
    shock_loss_sector_capacity: np.ndarray
    allocation_policy: str
    repair_enabled: bool
    primary_constraint: tuple[str, ...]
    intervention_demand_hours: np.ndarray
    verification_demand_units: np.ndarray


@dataclass(frozen=True)
class ComputeComparison:
    t: np.ndarray
    endogenous: np.ndarray
    endogenous_orbit: np.ndarray
    terrestrial: dict[str, np.ndarray]
    earth_fed_orbit: dict[str, np.ndarray]


@dataclass(frozen=True)
class DebrisResult:
    label: str
    t: np.ndarray
    active: np.ndarray
    derelict: np.ndarray
    fragments: np.ndarray
    fragments_created: np.ndarray
    fragments_cleared: np.ndarray
    creation_clearance_ratio: float
    subcritical: bool


@dataclass(frozen=True)
class ShellDebrisResult:
    t: np.ndarray
    shells: tuple[str, ...]
    active_capacity: np.ndarray
    intact_derelicts: np.ndarray
    trackable_fragments: np.ndarray
    untrackable_fragments: np.ndarray
    uncaptured_reservoir_t: np.ndarray
    feed_inventory_t: np.ndarray
    accessible_orbital_mass_t: np.ndarray
    earth_imported_t: np.ndarray
    captured_t: np.ndarray
    recovered_t: np.ndarray
    unrecoverable_loss_t: np.ndarray
    requested_deployment_units: np.ndarray
    served_deployment_units: np.ndarray
    deployment_shortfall_units: np.ndarray
    branching_ratio_by_shell: np.ndarray
    replacement_and_import_cost_usd: float


@dataclass(frozen=True)
class EnsembleSummary:
    scenario: str
    n_runs: int
    n_feasible: int
    seed_masses_t: tuple[float, ...]
    aggregate_doubling_years: tuple[float, ...]
    n_survived: int

    @property
    def feasible_share(self) -> float:
        return self.n_feasible / self.n_runs

    @property
    def survived_share(self) -> float:
        return self.n_survived / self.n_runs

    def percentiles(self, values: tuple[float, ...]) -> tuple[float, float, float] | None:
        if not values:
            return None
        return tuple(float(x) for x in np.percentile(np.asarray(values), [10, 50, 90]))


@dataclass(frozen=True)
class SeedDeploymentResult:
    scenario: str
    t: np.ndarray
    delivered_core_t: np.ndarray
    staged_core_t: np.ndarray
    installed_core_t: np.ndarray
    commissioned_core_t: np.ndarray
    operating_core_t: np.ndarray
    recovery_backlog_t: np.ndarray
    spares_remaining_t: np.ndarray
    installed_seed_mass_t: float
    delivered_seed_mass_t: float
    logistics_mass_t: float
    startup_energy_mwh: float
    first_operating_year: float | None
    full_operating_seed_year: float | None
    recovered_startup_failure_t: float
    success: bool


def _vector(names: tuple[str, ...], values: dict[str, float], label: str) -> np.ndarray:
    unknown = set(values) - set(names)
    if unknown:
        raise ValueError(f"{label}: unknown names: {sorted(unknown)}")
    return np.array([float(values.get(name, 0.0)) for name in names], dtype=float)


def load_integrated_params(path: Path | None = None) -> IntegratedParams:
    with open(path or PARAMS_PATH, encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    elements = tuple(raw["elements"])
    sector_rows = raw["sectors"]
    sectors = tuple(row["name"] for row in sector_rows)
    if len(set(elements)) != len(elements) or len(set(sectors)) != len(sectors):
        raise ValueError("Current elements and sectors must be unique")

    def arr(key: str) -> np.ndarray:
        return np.array([float(row[key]) for row in sector_rows], dtype=float)

    B = np.column_stack([
        _vector(elements, row.get("bom_t", {}), f"bom_t[{row['name']}]")
        for row in sector_rows
    ])
    base = _vector(sectors, raw["base_service_recipe"], "base_service_recipe")
    A = np.empty((len(sectors), len(sectors)), dtype=float)
    for j, row in enumerate(sector_rows):
        A[:, j] = base + _vector(
            sectors, row.get("recipe_additions", {}),
            f"recipe_additions[{row['name']}]",
        )

    lunar = _vector(
        elements,
        raw["source_yields"]["lunar_regolith"]["yield_t_per_t_feed"],
        "lunar_regolith yield",
    )
    asteroid = _vector(
        elements,
        raw["source_yields"]["diverse_asteroid_portfolio"]["yield_t_per_t_feed"],
        "asteroid yield",
    )
    if lunar.sum() > 1.0 + 1e-12 or asteroid.sum() > 1.0 + 1e-12:
        raise ValueError("Recoverable source yields cannot exceed feed mass")
    if np.any(B < 0) or np.any(A < 0):
        raise ValueError("Bills of material and service recipes must be nonnegative")
    if np.any(B.sum(axis=0) <= 0):
        raise ValueError("Every sector needs a nonzero physical bill of material")
    knowledge_mass = sum(
        float(value)
        for value in raw["knowledge_autonomy"]["knowledge_package_t"].values()
    )
    if not math.isclose(
        knowledge_mass,
        float(raw["seed"]["fixed_digital_seed_mass_t"]),
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        raise ValueError(
            "knowledge package decomposition must sum to fixed digital seed mass"
        )

    uncertainty = {
        name: (float(bounds[0]), float(bounds[1]))
        for name, bounds in raw["uncertainty"].items()
    }
    return IntegratedParams(
        version=str(raw["version"]),
        elements=elements,
        sectors=sectors,
        q=arr("q_per_capacity_year"),
        delta=arr("depreciation_per_year"),
        min_seed=arr("min_seed_capacity"),
        lag=arr("commissioning_lag_years"),
        ramp=arr("yield_ramp_years"),
        gravity_required=arr("gravity_required_g"),
        centrifuge_radius=arr("centrifuge_radius_m"),
        base_coverage=arr("base_task_coverage"),
        coverage_ceiling=arr("autonomy_ceiling"),
        coverage_response=arr("autonomy_response"),
        intervention_hours=arr("intervention_hours_per_capacity_year"),
        B=B,
        A=A,
        lunar_yield=lunar,
        asteroid_yield=asteroid,
        processing={k: float(v) for k, v in raw["processing"].items()},
        environment=raw["environment"],
        scenarios=raw["scenarios"],
        seed={k: float(v) for k, v in raw["seed"].items()},
        intelligence={k: float(v) for k, v in raw["intelligence"].items()},
        transfer_arcs=raw["transfer_arcs"],
        earth_compute=raw["earth_compute_counterfactuals"],
        debris=raw["debris"],
        uncertainty=uncertainty,
        raw=raw,
    )


def process_profile(
    params: IntegratedParams,
    scenario: str,
    *,
    ai_level: float | None = None,
    environment_profile: str | None = None,
) -> ProcessProfile:
    cfg = params.scenarios[scenario]
    environment_name = str(
        cfg["environment_profile"]
        if environment_profile is None else environment_profile
    )
    profiles = params.raw["process_environment_profiles"]
    if environment_name not in profiles:
        raise ValueError(
            f"unknown process environment profile {environment_name!r}"
        )
    effects = profiles[environment_name].get("effects", {})
    environment_throughput = np.ones(params.n)
    environment_yield = np.ones(params.n)
    environment_depreciation = np.ones(params.n)
    environment_power = np.ones(params.n)
    for sector, values in effects.items():
        j = params.sector_idx(sector)
        environment_throughput[j] = float(
            values.get("throughput_multiplier", 1.0)
        )
        environment_yield[j] = float(
            values.get("yield_multiplier", 1.0)
        )
        environment_depreciation[j] = float(
            values.get("depreciation_multiplier", 1.0)
        )
        environment_power[j] = float(
            values.get("power_demand_multiplier", 1.0)
        )
    level = float(cfg["ai_level"] if ai_level is None else ai_level)
    coverage = np.minimum(
        params.coverage_ceiling,
        params.base_coverage + params.coverage_response * max(level - 1.0, 0.0),
    )
    autonomy_productivity = 0.50 + 0.50 * coverage

    lunar_g = float(params.environment["lunar_gravity_g"])
    acceleration_gap_g = np.maximum(params.gravity_required - lunar_g, 0.0)
    structural_fraction = float(
        params.environment["centrifuge_structural_mass_fraction_at_full_g"]
    )
    power_fraction = float(
        params.environment["centrifuge_parasitic_power_fraction_at_full_g"]
    )
    base_mass = params.B.sum(axis=0)
    centrifuge_mass = base_mass * structural_fraction * acceleration_gap_g
    B_eff = params.B.copy()
    overhead_comp = params.environment["centrifuge_overhead_composition"]
    for element, share in overhead_comp.items():
        B_eff[params.element_idx(element)] += centrifuge_mass * float(share)

    parasitic = power_fraction * acceleration_gap_g
    q_eff = (
        params.q
        * autonomy_productivity
        * environment_throughput
        * environment_yield
        / ((1.0 + parasitic) * environment_power)
    )
    accel_m_s2 = acceleration_gap_g * 9.80665
    omega = np.sqrt(np.divide(
        accel_m_s2,
        params.centrifuge_radius,
        out=np.zeros_like(accel_m_s2),
        where=params.centrifuge_radius > 0,
    ))
    rpm = omega * 60.0 / (2.0 * math.pi)
    intervention = params.intervention_hours * np.maximum(1.0 - coverage, 0.0)
    knowledge = params.raw["knowledge_autonomy"]
    diagnosis = np.minimum(
        coverage * float(knowledge["fault_diagnosis_scale"]),
        1.0,
    )
    verification = (
        q_eff
        * coverage
        * float(knowledge["verification_throughput_per_service_unit"])
    )
    engineering_cycle = (
        float(knowledge["engineering_cycle_base_years"])
        / (
            1.0
            + float(knowledge["engineering_cycle_response"])
            * max(level - 1.0, 0.0)
        )
    ) * np.ones_like(coverage)
    yield_floor = float(knowledge["process_yield_floor"])
    process_yield = yield_floor + (1.0 - yield_floor) * coverage
    repair_success = np.minimum(
        coverage * float(knowledge["repair_success_scale"]),
        1.0,
    )
    mttr = (
        float(knowledge["mttr_days_floor"])
        + (
            float(knowledge["mttr_days_at_zero_coverage"])
            - float(knowledge["mttr_days_floor"])
        )
        * (1.0 - coverage)
    )
    stop_line_threshold = np.maximum(
        params.base_coverage
        - float(knowledge["stop_line_threshold_below_declared_coverage"]),
        0.0,
    )
    return ProcessProfile(
        scenario=scenario,
        environment_profile=environment_name,
        ai_level=level,
        coverage=coverage,
        q_effective=q_eff,
        B_effective=B_eff,
        centrifuge_rpm=rpm,
        centrifuge_mass_t=centrifuge_mass,
        intervention_hours_per_year=intervention,
        named_task_completion_rate=coverage.copy(),
        fault_diagnosis_fraction=diagnosis,
        verification_throughput_per_year=verification,
        engineering_cycle_years=engineering_cycle,
        process_yield=process_yield,
        repair_success_fraction=repair_success,
        mean_time_to_recovery_days=mttr,
        stop_line_task_pass=coverage >= stop_line_threshold,
        environment_throughput_multiplier=environment_throughput,
        environment_yield_multiplier=environment_yield,
        environment_depreciation_multiplier=environment_depreciation,
        environment_power_demand_multiplier=environment_power,
    )


def _constraint_slacks(
    labels: list[str],
    A_ub: np.ndarray,
    b_ub: np.ndarray,
    x: np.ndarray,
) -> tuple[tuple[str, float], ...]:
    slack = b_ub - A_ub @ x
    scale = np.maximum(np.abs(b_ub), 1.0)
    normalized = slack / scale
    order = np.argsort(normalized)[:8]
    return tuple((labels[i], float(normalized[i])) for i in order)


def build_seed_lp(
    params: IntegratedParams,
    scenario: str,
    profile: ProcessProfile,
) -> dict[str, Any]:
    """Assemble the seed-sizing LP exactly as ``size_seed`` solves it.

    Shared with the r4.0 analysis layer (elastic infeasibility
    certificates) so the certificate interrogates the identical matrix.
    """
    cfg = params.scenarios[scenario]
    # Variables: sector capacities z[n], lunar feed p_l, asteroid feed p_a,
    # and initial Earth strategic-material import stocks v[m].
    n, m = params.n, params.m
    iz = slice(0, n)
    ip_l, ip_a = n, n + 1
    iv = slice(n + 2, n + 2 + m)
    nv = n + 2 + m
    mass_per_capacity = profile.B_effective.sum(axis=0)
    c = np.zeros(nv)
    c[iz] = mass_per_capacity
    c[iv] = 1.0
    c_import = np.zeros(nv)
    c_import[iv] = 1.0
    c_intervention = np.zeros(nv)
    c_intervention[iz] = profile.intervention_hours_per_year

    bounds: list[tuple[float | None, float | None]] = [
        (float(params.min_seed[i]), None) for i in range(n)
    ]
    bounds += [(0.0, None)]
    bounds += [(0.0, None if cfg["asteroid_enabled"] else 0.0)]
    import_caps = cfg.get("earth_import_caps_t", {})
    bounds += [
        (0.0, float(import_caps.get(element, 0.0)))
        for element in params.elements
    ]

    T = float(cfg["horizon_years"])
    replacement_multiplier = (
        1.0
        + params.delta
        * profile.environment_depreciation_multiplier
        * T
    )
    productive_years = np.maximum(T - params.lag - 0.5 * params.ramp, 0.0)
    lunar_years = max(
        T
        - max(
            params.lag[params.sector_idx("mining")],
            params.lag[params.sector_idx("refining")],
        )
        - 0.5 * params.ramp[params.sector_idx("refining")],
        0.0,
    )
    asteroid_years = (
        max(T - float(cfg["asteroid_commission_year"]), 0.0)
        if cfg["asteroid_enabled"] else 0.0
    )

    rows: list[np.ndarray] = []
    rhs: list[float] = []
    labels: list[str] = []

    # Service capacity must cover replacement during the horizon and the
    # complete service recipe of one additional operating-capacity equivalent.
    for i, sector in enumerate(params.sectors):
        row = np.zeros(nv)
        row[iz] = params.A[i] * replacement_multiplier
        row[i] -= profile.q_effective[i] * productive_years[i]
        rows.append(row)
        rhs.append(0.0)
        labels.append(f"service:{sector}")

    # Element balances: the initial strategic-material stock is the only Earth term.
    for e, element in enumerate(params.elements):
        row = np.zeros(nv)
        row[iz] = profile.B_effective[e] * replacement_multiplier
        row[ip_l] = -params.lunar_yield[e] * lunar_years
        row[ip_a] = -params.asteroid_yield[e] * asteroid_years
        row[n + 2 + e] = -1.0
        rows.append(row)
        rhs.append(0.0)
        labels.append(f"element:{element}")

    i_mining = params.sector_idx("mining")
    i_refining = params.sector_idx("refining")
    i_transport = params.sector_idx("transport")
    i_power = params.sector_idx("power")
    proc = params.processing

    row = np.zeros(nv)
    row[ip_l] = 1.0
    row[ip_a] = 1.0
    row[i_mining] = -proc["lunar_feed_t_per_mining_capacity_year"]
    rows.append(row)
    rhs.append(0.0)
    labels.append("throughput:mining")

    row = np.zeros(nv)
    row[ip_l] = 1.0
    row[ip_a] = 1.0
    row[i_refining] = -proc["lunar_feed_t_per_refining_capacity_year"]
    rows.append(row)
    rhs.append(0.0)
    labels.append("throughput:refining")

    row = np.zeros(nv)
    row[ip_a] = 1.0
    row[i_mining] = -proc["asteroid_feed_t_per_mining_capacity_year"]
    rows.append(row)
    rhs.append(0.0)
    labels.append("throughput:asteroid_mining")

    row = np.zeros(nv)
    row[ip_a] = 1.0
    row[i_transport] = -proc["asteroid_feed_t_per_transport_capacity_year"]
    rows.append(row)
    rhs.append(0.0)
    labels.append("throughput:asteroid_transport")

    row = np.zeros(nv)
    row[ip_l] = proc["lunar_energy_mwh_per_t_feed"]
    row[ip_a] = proc["asteroid_energy_mwh_per_t_feed"]
    row[i_power] = -proc["process_energy_mwh_per_power_capacity_year"]
    rows.append(row)
    rhs.append(0.0)
    labels.append("throughput:process_energy")

    row = np.zeros(nv)
    row[iz] = profile.intervention_hours_per_year
    rows.append(row)
    rhs.append(float(cfg["remote_intervention_budget_hours_per_year"]))
    labels.append("autonomy:intervention_budget")

    return {
        "c": c,
        "objective_vectors": {
            "installed_mass": c,
            "earth_import_mass": c_import,
            "intervention_hours": c_intervention,
        },
        "A_ub": np.vstack(rows),
        "b_ub": np.array(rhs),
        "bounds": bounds,
        "labels": labels,
        "iz": iz,
        "ip_l": ip_l,
        "ip_a": ip_a,
        "iv": iv,
        "nv": nv,
        "mass_per_capacity": mass_per_capacity,
    }


def size_seed(
    params: IntegratedParams,
    scenario: str,
    *,
    ai_level: float | None = None,
    objective: str = "installed_mass",
    environment_profile: str | None = None,
) -> SeedResult:
    cfg = params.scenarios[scenario]
    profile = process_profile(
        params,
        scenario,
        ai_level=ai_level,
        environment_profile=environment_profile,
    )
    digital_mass = float(params.seed["fixed_digital_seed_mass_t"])
    min_required = float(cfg["minimum_task_coverage"])
    if profile.minimum_coverage + 1e-12 < min_required:
        return SeedResult(
            scenario, False,
            f"autonomy threshold {profile.minimum_coverage:.3f} < {min_required:.3f}",
            None, None, None, digital_mass,
            np.zeros(params.n), np.zeros(params.m), 0.0, 0.0,
            profile.minimum_coverage, 0.0, (), profile,
        )

    lp = build_seed_lp(params, scenario, profile)
    n, m = params.n, params.m
    iz, ip_l, ip_a, iv = lp["iz"], lp["ip_l"], lp["ip_a"], lp["iv"]
    mass_per_capacity = lp["mass_per_capacity"]
    A_ub, b_ub, labels = lp["A_ub"], lp["b_ub"], lp["labels"]
    if objective not in lp["objective_vectors"]:
        raise ValueError(
            f"Unknown seed objective {objective!r}; expected one of "
            f"{sorted(lp['objective_vectors'])}"
        )
    primary = lp["objective_vectors"][objective]
    solved = linprog(
        primary,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=lp["bounds"],
        method="highs",
    )
    if solved.success and objective != "installed_mass":
        primary_optimum = float(primary @ solved.x)
        tolerance = 1e-8 * max(abs(primary_optimum), 1.0)
        A_lex = np.vstack([A_ub, primary])
        b_lex = np.append(b_ub, primary_optimum + tolerance)
        solved = linprog(
            lp["c"],
            A_ub=A_lex,
            b_ub=b_lex,
            bounds=lp["bounds"],
            method="highs",
        )
    if not solved.success:
        return SeedResult(
            scenario, False, solved.message, None, None, None, digital_mass,
            np.zeros(n), np.zeros(m), 0.0, 0.0,
            profile.minimum_coverage, 0.0, (), profile,
        )

    x = solved.x
    capacities = x[iz].copy()
    import_stock = x[iv].copy()
    physical = float(mass_per_capacity @ capacities)
    import_stock_mass = float(import_stock.sum())
    total = physical + import_stock_mass + digital_mass
    interventions = float(profile.intervention_hours_per_year @ capacities)
    return SeedResult(
        scenario=scenario,
        feasible=True,
        status=(
            f"lexicographic {objective} optimum within the declared "
            "linear seed architecture"
        ),
        total_seed_mass_t=total,
        physical_seed_mass_t=physical,
        import_stock_mass_t=import_stock_mass,
        digital_seed_mass_t=digital_mass,
        capacities=capacities,
        import_stock_t=import_stock,
        lunar_feed_t_per_year=float(x[ip_l]),
        asteroid_feed_t_per_year=float(x[ip_a]),
        minimum_task_coverage=profile.minimum_coverage,
        intervention_hours_per_year=interventions,
        binding_constraints=_constraint_slacks(labels, A_ub, b_ub, x),
        process=profile,
    )


def simulate_seed_deployment(
    params: IntegratedParams,
    seed_result: SeedResult,
    *,
    years: float = 12.0,
    dt: float = 0.25,
) -> SeedDeploymentResult:
    """Move a delivered core seed through staging and commissioning.

    Logistics equipment, transport packaging, calibration references,
    startup-energy storage, and initial spares are included in delivered
    mass. The model applies a declared startup failure fraction to newly
    commissioned core mass; failed mass becomes operational only through the
    bounded recovery rate and by consuming the delivered spares stock.
    """
    if not seed_result.feasible:
        raise ValueError(f"Cannot deploy infeasible seed: {seed_result.status}")
    cfg = params.raw["deployment"]
    core = float(seed_result.total_seed_mass_t)
    packaging = core * float(cfg["transport_packaging_fraction"])
    spares_initial = core * float(cfg["initial_spares_fraction"])
    startup_energy = core * float(cfg["startup_energy_mwh_per_seed_t"])
    startup_storage = (
        startup_energy * float(cfg["startup_storage_t_per_mwh"])
    )
    fixed_logistics = (
        float(cfg["unloading_equipment_mass_t"])
        + float(cfg["site_work_equipment_mass_t"])
        + float(cfg["calibration_standards_mass_t"])
    )
    logistics = packaging + spares_initial + startup_storage + fixed_logistics
    delivered_mass = core + logistics

    steps = int(round(years / dt))
    t = np.arange(steps + 1, dtype=float) * dt
    delivered = np.zeros(steps + 1)
    staged = np.zeros(steps + 1)
    installed = np.zeros(steps + 1)
    commissioned = np.zeros(steps + 1)
    operating = np.zeros(steps + 1)
    backlog = np.zeros(steps + 1)
    spares = np.zeros(steps + 1)
    delivered[0] = core
    spares[0] = spares_initial
    recovered_total = 0.0

    for k in range(steps):
        unload = min(
            delivered[k],
            float(cfg["unloading_rate_t_per_year"]) * dt,
        )
        delivered[k + 1] = delivered[k] - unload
        staged_available = staged[k] + unload

        install = 0.0
        if t[k] >= float(cfg["site_ready_year"]):
            install = min(
                staged_available,
                float(cfg["installation_rate_t_per_year"]) * dt,
            )
        staged[k + 1] = staged_available - install
        installed_available = installed[k] + install

        commission = 0.0
        if t[k] >= float(cfg["initial_power_ready_year"]):
            commission = min(
                installed_available,
                float(cfg["commissioning_rate_t_per_year"]) * dt,
            )
        installed[k + 1] = installed_available - commission
        commissioned[k + 1] = commissioned[k] + commission

        startup_failed = commission * float(cfg["startup_failure_fraction"])
        operating_gain = commission - startup_failed
        backlog_available = backlog[k] + startup_failed
        spares_per_failed = float(cfg["recovery_spares_t_per_failed_t"])
        repair = min(
            backlog_available,
            float(cfg["recovery_rate_t_per_year"]) * dt,
            spares[k] / max(spares_per_failed, 1e-12),
        )
        backlog[k + 1] = backlog_available - repair
        spares[k + 1] = max(
            spares[k] - repair * spares_per_failed,
            0.0,
        )
        operating[k + 1] = operating[k] + operating_gain + repair
        recovered_total += repair

    first = np.flatnonzero(operating > 1e-9)
    full = np.flatnonzero(operating >= core - 1e-8)
    return SeedDeploymentResult(
        scenario=seed_result.scenario,
        t=t,
        delivered_core_t=delivered,
        staged_core_t=staged,
        installed_core_t=installed,
        commissioned_core_t=commissioned,
        operating_core_t=operating,
        recovery_backlog_t=backlog,
        spares_remaining_t=spares,
        installed_seed_mass_t=core,
        delivered_seed_mass_t=delivered_mass,
        logistics_mass_t=logistics,
        startup_energy_mwh=startup_energy,
        first_operating_year=float(t[first[0]]) if len(first) else None,
        full_operating_seed_year=float(t[full[0]]) if len(full) else None,
        recovered_startup_failure_t=recovered_total,
        success=bool(len(full)),
    )


def _independent_sector_order(
    params: IntegratedParams,
    seed_result: SeedResult,
    installed_sector: np.ndarray,
    operating_sector: np.ndarray,
    available_material: np.ndarray,
    *,
    gross_cell_order_budget: float,
    productivity_multiplier: float,
    dt: float,
) -> np.ndarray:
    """Max-min sector build allocation with an installed-mass tie-break.

    The decision variables are additions in each sector's native capacity
    units. Material, live service output, and a normalized gross-order budget
    constrain the allocation. The primary solve maximizes the weakest
    projected normalized sector; the secondary solve installs the least mass
    that attains that max-min target. Unlike balanced packet construction,
    this can repair a sector margin without ordering every other sector.
    """
    n = params.n
    z = seed_result.capacities
    if gross_cell_order_budget <= 1e-12 or np.all(available_material <= 1e-12):
        return np.zeros(n)

    service_budget = (
        seed_result.process.q_effective
        * np.maximum(operating_sector, 0.0)
        * productivity_multiplier
        * dt
    )
    normalized_weight = np.divide(
        1.0,
        z,
        out=np.zeros(n),
        where=z > 1e-12,
    )
    current_ratio = np.divide(
        installed_sector,
        z,
        out=np.zeros(n),
        where=z > 1e-12,
    )

    # Variables are x[n] sector additions and lambda, the minimum projected
    # normalized installed-sector margin.
    rows = []
    rhs = []
    for e in range(params.m):
        row = np.zeros(n + 1)
        row[:n] = seed_result.process.B_effective[e]
        rows.append(row)
        rhs.append(max(float(available_material[e]), 0.0))
    for i in range(n):
        row = np.zeros(n + 1)
        row[:n] = params.A[i]
        rows.append(row)
        rhs.append(max(float(service_budget[i]), 0.0))
    row = np.zeros(n + 1)
    row[:n] = normalized_weight / n
    rows.append(row)
    rhs.append(max(float(gross_cell_order_budget), 0.0))
    for j in range(n):
        row = np.zeros(n + 1)
        row[j] = -normalized_weight[j]
        row[-1] = 1.0
        rows.append(row)
        rhs.append(float(current_ratio[j]))

    c = np.zeros(n + 1)
    c[-1] = -1.0
    primary = linprog(
        c,
        A_ub=np.asarray(rows),
        b_ub=np.asarray(rhs),
        bounds=[(0.0, None)] * (n + 1),
        method="highs",
    )
    if not primary.success:
        return np.zeros(n)
    target = float(primary.x[-1])

    # Fix the max-min target and minimize embodied mass. This removes the
    # arbitrary excess-sector choices that a single-stage max-min LP permits.
    rows2 = [np.asarray(row[:n]) for row in rows[:-n]]
    rhs2 = list(rhs[:-n])
    for j in range(n):
        row2 = np.zeros(n)
        row2[j] = -normalized_weight[j]
        rows2.append(row2)
        rhs2.append(float(current_ratio[j] - target + 1e-9))
    mass = seed_result.process.B_effective.sum(axis=0)
    secondary = linprog(
        mass,
        A_ub=np.asarray(rows2),
        b_ub=np.asarray(rhs2),
        bounds=[(0.0, None)] * n,
        method="highs",
    )
    if not secondary.success:
        return primary.x[:n]
    return np.maximum(secondary.x, 0.0)


def simulate_capacity_growth(
    params: IntegratedParams,
    seed_result: SeedResult,
    *,
    years: float = 40.0,
    dt: float = 0.25,
    initial_cells: float = 1.0,
    allocation_policy: str = "balanced",
    repair_enabled: bool = False,
    shock_events: tuple[tuple[float, str, float], ...] = (),
    operational_constraints_enabled: bool = False,
    communication_outage_windows: tuple[tuple[float, float, float], ...] = (),
    verification_outage_windows: tuple[tuple[float, float, float], ...] = (),
    compute_outage_windows: tuple[tuple[float, float, float], ...] = (),
    lunar_source_outage_windows: tuple[tuple[float, float, float], ...] = (),
    asteroid_source_outage_windows: tuple[tuple[float, float, float], ...] = (),
    import_stock_multiplier: float | None = None,
    depreciation_multiplier: float = 1.0,
) -> CapacityGrowthResult:
    """Advance sector-resolved operating-capacity dynamics.

    ``initial_cells`` scales the installed seed to that many
    cell-equivalents of the given design (capacities, feeds, and strategic
    import stock all scale with it). Aggregate cell-equivalents are a
    derived minimum across the 18 normalized sector capacities; they are
    not the dynamic state. New capacity is ordered as a balanced packet,
    but each sector follows its own commissioning lag, ramp, and
    depreciation, so an incomplete packet contributes only the services of
    sectors already operating. ``allocation_policy="maximin_sector"`` instead
    chooses native sector additions against the live material/service graph.
    ``repair_enabled=True`` makes a declared share of depreciation repairable,
    consumes repair service, parts, intervention hours, and a repair queue,
    and returns completed repairs to operation.

    ``shock_events`` contains ``(year, sector, fraction_lost)`` records.
    Shocks act on the named installed sector at the start of the matching
    step; their repairable share enters the same repair queue as ordinary
    failures, so post-shock recovery is tested against live sector margins.

    When ``operational_constraints_enabled`` is true, named intervention,
    verification, compute, and non-divisible stop-line gates constrain new
    orders. Outage windows are ``(start_year, end_year, multiplier)`` records
    applied to remote-intervention or verification capacity.
    """
    if not seed_result.feasible:
        raise ValueError(f"Cannot simulate infeasible seed: {seed_result.status}")
    if allocation_policy not in {
        "balanced",
        "maximin_sector",
        "surplus_preserving",
        "shock_aware",
        "perfect_foresight",
    }:
        raise ValueError(
            "unknown allocation_policy"
        )
    if (
        import_stock_multiplier is not None
        and import_stock_multiplier < 0.0
    ):
        raise ValueError("import_stock_multiplier must be nonnegative")
    if depreciation_multiplier <= 0.0:
        raise ValueError("depreciation_multiplier must be positive")
    for year, sector, fraction in shock_events:
        if sector not in params.sectors:
            raise ValueError(f"unknown shock sector {sector!r}")
        if year < 0.0 or not 0.0 <= fraction <= 1.0:
            raise ValueError("shock year must be nonnegative and fraction in [0, 1]")
    for start, end, multiplier in (
        *communication_outage_windows,
        *verification_outage_windows,
        *compute_outage_windows,
        *lunar_source_outage_windows,
        *asteroid_source_outage_windows,
    ):
        if start < 0.0 or end <= start or not 0.0 <= multiplier <= 1.0:
            raise ValueError(
                "outage windows require 0 <= start < end and multiplier in [0, 1]"
            )
    cfg = params.scenarios[seed_result.scenario]
    profile = seed_result.process
    z = seed_result.capacities
    cell_bom = profile.B_effective @ z
    service_need = params.A @ z

    steps = int(round(years / dt))
    t = np.arange(steps + 1, dtype=float) * dt
    installed_sector = np.zeros((steps + 1, params.n))
    operating_sector = np.zeros((steps + 1, params.n))
    ordered_sector = np.zeros((steps + 1, params.n))
    installed = np.zeros(steps + 1)
    operating = np.zeros(steps + 1)
    intelligence = np.zeros(steps + 1)
    compute = np.zeros(steps + 1)
    inventory = np.zeros((steps + 1, params.m))
    ordered = np.zeros(steps + 1)
    failed_sector = np.zeros((steps + 1, params.n))
    repaired_sector = np.zeros((steps + 1, params.n))
    commissioned_sector = np.zeros((steps + 1, params.n))
    activated_sector = np.zeros((steps + 1, params.n))
    shock_loss_sector = np.zeros((steps + 1, params.n))
    intervention_demand = np.zeros(steps + 1)
    verification_demand = np.zeros(steps + 1)
    primary_constraints: list[str] = []
    installed_sector[0] = z * float(initial_cells)
    operating_sector[0] = z * float(initial_cells)
    installed[0] = operating[0] = float(initial_cells)
    intelligence[0] = float(cfg["ai_level"])
    i_compute = params.sector_idx("compute")
    compute_scale = float(params.intelligence["compute_units_per_compute_capacity"])
    compute[0] = operating_sector[0, i_compute] * compute_scale
    inventory[0] = seed_result.import_stock_t * float(
        initial_cells
        if import_stock_multiplier is None
        else import_stock_multiplier
    )

    lag_steps = np.maximum(1, np.rint(params.lag / dt).astype(int))
    queue = np.zeros((params.n, int(np.max(lag_steps))))
    ramp_steps = np.maximum(1, np.rint(params.ramp / dt).astype(int))
    activation_queue = np.zeros((params.n, int(np.max(ramp_steps))))
    repair_lag_steps = max(
        1,
        int(round(float(params.seed["repair_lag_years"]) / dt)),
    )
    repair_queue = np.zeros((params.n, repair_lag_steps))
    recovery = float(params.seed["recycling_recovery_fraction"])
    min_cells = float(params.seed["minimum_viable_cell_equivalents"])
    asteroid_start = float(cfg["asteroid_commission_year"])
    limiting_counts = np.zeros(params.m, dtype=int)
    lunar_total = asteroid_total = recycled_total = 0.0
    i_mining = params.sector_idx("mining")
    i_refining = params.sector_idx("refining")
    i_transport = params.sector_idx("transport")
    i_power = params.sector_idx("power")
    viable_floor = (
        params.min_seed * float(cfg["viable_floor_multiplier"])
    )
    effective_delta = (
        params.delta
        * profile.environment_depreciation_multiplier
        * depreciation_multiplier
    )

    for k in range(steps):
        installed_state = np.maximum(installed_sector[k], 0.0).copy()
        op_sector = np.maximum(operating_sector[k], 0.0).copy()
        shock_loss = np.zeros(params.n)
        for event_year, event_sector, event_fraction in shock_events:
            if abs(float(t[k]) - float(event_year)) <= 0.5 * dt + 1e-12:
                j = params.sector_idx(event_sector)
                loss = installed_state[j] * float(event_fraction)
                shock_loss[j] += loss
                installed_state[j] -= loss
                op_sector[j] = max(op_sector[j] - loss, 0.0)
        shock_loss_sector[k + 1] = shock_loss
        capacity_ratio = np.divide(
            op_sector,
            z,
            out=np.zeros(params.n),
            where=z > 1e-12,
        )
        op = max(float(np.min(capacity_ratio)), 0.0)
        retired_sector = installed_state * effective_delta * dt
        repairable_fraction = (
            float(params.seed["repairable_failure_fraction"])
            if repair_enabled else 0.0
        )
        newly_failed = (
            retired_sector + shock_loss
        ) * repairable_fraction
        unrecoverable_retirement = (
            retired_sector + shock_loss - newly_failed
        )
        failed_available = failed_sector[k] + newly_failed
        recovered = recovery * (
            profile.B_effective @ unrecoverable_retirement
        )
        recycled_total += float(recovered.sum())

        lunar_scale = max(float(np.min(
            capacity_ratio[[i_mining, i_refining, i_power]]
        )), 0.0)
        lunar_prod = (
            params.lunar_yield
            * seed_result.lunar_feed_t_per_year
            * lunar_scale
            * dt
        )
        for start, end, multiplier in lunar_source_outage_windows:
            if start <= t[k] < end:
                lunar_prod *= multiplier
        asteroid_prod = np.zeros(params.m)
        if cfg["asteroid_enabled"] and t[k] >= asteroid_start:
            asteroid_scale = max(float(np.min(
                capacity_ratio[[i_mining, i_refining, i_transport, i_power]]
            )), 0.0)
            asteroid_prod = (
                params.asteroid_yield
                * seed_result.asteroid_feed_t_per_year
                * asteroid_scale
                * dt
            )
            for start, end, multiplier in asteroid_source_outage_windows:
                if start <= t[k] < end:
                    asteroid_prod *= multiplier
        lunar_total += float(lunar_prod.sum())
        asteroid_total += float(asteroid_prod.sum())
        available = inventory[k] + recovered + lunar_prod + asteroid_prod

        repair_started = np.zeros(params.n)
        repaired_due = repair_queue[:, 0].copy()
        repair_queue[:, :-1] = repair_queue[:, 1:]
        repair_queue[:, -1] = 0.0
        if repair_enabled and np.any(failed_available > 1e-12):
            repair_index = params.sector_idx("repair")
            service_limit_repair = (
                profile.q_effective[repair_index]
                * op_sector[repair_index]
                * dt
                / max(float(params.seed["repair_service_per_capacity"]), 1e-12)
            )
            routine_intervention = float(
                profile.intervention_hours_per_year @ op_sector
            )
            intervention_budget = max(
                (
                    float(cfg["remote_intervention_budget_hours_per_year"])
                    - routine_intervention
                )
                * dt,
                0.0,
            )
            intervention_limit = intervention_budget / max(
                float(params.seed["repair_intervention_hours_per_capacity"]),
                1e-12,
            )
            desired_repair = min(
                float(failed_available.sum()),
                max(service_limit_repair, 0.0),
                max(intervention_limit, 0.0),
            )
            if desired_repair > 1e-12:
                shares = failed_available / float(failed_available.sum())
                candidate = desired_repair * shares
                parts_fraction = float(
                    params.seed["repair_parts_fraction_of_bom"]
                )
                parts = parts_fraction * (
                    profile.B_effective @ candidate
                )
                material_scale = float(np.min(np.divide(
                    available,
                    parts,
                    out=np.full(params.m, np.inf),
                    where=parts > 1e-12,
                )))
                repair_started = candidate * min(
                    max(material_scale, 0.0),
                    1.0,
                )
                available = np.maximum(
                    available
                    - parts_fraction * (
                        profile.B_effective @ repair_started
                    ),
                    0.0,
                )
                repair_queue[:, -1] += repair_started
        failed_sector[k + 1] = np.maximum(
            failed_available - repair_started,
            0.0,
        )
        repaired_sector[k + 1] = repaired_due

        level_gain = max(intelligence[k] - float(cfg["ai_level"]), 0.0)
        productivity = 1.0 + float(
            params.intelligence["productivity_elasticity"]
        ) * level_gain
        autonomy_gain = 1.0 + float(
            params.intelligence["autonomy_learning_multiplier"]
        ) * level_gain
        service_limit = float(np.min(np.divide(
            profile.q_effective * op_sector,
            service_need,
            out=np.full(params.n, np.inf),
            where=service_need > 1e-12,
        )))
        rate_cap = (
            float(params.seed[
                "maximum_gross_cell_orders_per_operating_cell_year"
            ])
            * op
        )
        intervention_demand[k] = float(
            profile.intervention_hours_per_year @ op_sector
        )
        verification_per_cell = (
            float(params.raw["knowledge_autonomy"][
                "verification_units_per_new_capacity"
            ])
            * float(z.sum())
        )
        verification_demand[k] = rate_cap * verification_per_cell
        candidate_limits = {
            "service": service_limit,
            "order_rate": rate_cap,
        }
        if operational_constraints_enabled:
            communication_multiplier = 1.0
            for start, end, multiplier in communication_outage_windows:
                if start <= t[k] < end:
                    communication_multiplier *= multiplier
            verification_multiplier = 1.0
            for start, end, multiplier in verification_outage_windows:
                if start <= t[k] < end:
                    verification_multiplier *= multiplier
            compute_multiplier = 1.0
            for start, end, multiplier in compute_outage_windows:
                if start <= t[k] < end:
                    compute_multiplier *= multiplier
            remote_budget = (
                float(cfg["remote_intervention_budget_hours_per_year"])
                * communication_multiplier
            )
            intervention_per_cell = max(
                float(profile.intervention_hours_per_year @ z),
                1e-12,
            )
            candidate_limits["autonomy"] = max(
                (remote_budget - intervention_demand[k])
                / intervention_per_cell,
                0.0,
            )
            verification_available = (
                float(profile.verification_throughput_per_year @ op_sector)
                * verification_multiplier
            )
            candidate_limits["verification"] = (
                verification_available
                / max(verification_per_cell, 1e-12)
            )
            candidate_limits["compute"] = (
                compute[k] * compute_multiplier
                / max(
                    float(params.raw["knowledge_autonomy"][
                        "compute_units_per_cell_order_year"
                    ]),
                    1e-12,
                )
            )
            if not bool(np.all(profile.stop_line_task_pass)):
                candidate_limits["autonomy"] = 0.0
        primary = min(candidate_limits, key=candidate_limits.get)
        desired = (
            max(float(candidate_limits[primary]), 0.0)
            * productivity
            * autonomy_gain
            * dt
        )
        sector_order = np.zeros(params.n)
        if desired > 0.0 and allocation_policy == "balanced":
            material_limit_by_element = np.divide(
                available,
                cell_bom,
                out=np.full(params.m, np.inf),
                where=cell_bom > 1e-12,
            )
            material_limit = float(np.min(material_limit_by_element))
            built = min(desired, max(material_limit, 0.0))
            if built + 1e-10 < desired:
                primary = "material"
                binding = np.flatnonzero(
                    material_limit_by_element <= material_limit + 1e-8
                )
                limiting_counts[binding] += 1
        else:
            built = 0.0
        if allocation_policy == "balanced":
            sector_order = built * z
            material_use = built * cell_bom
            ordered[k + 1] = built
        else:
            gross_budget = (
                float(params.seed[
                    "maximum_gross_cell_orders_per_operating_cell_year"
                ])
                * op
                * productivity
                * autonomy_gain
                * dt
            )
            allocation_material = available
            if allocation_policy == "surplus_preserving":
                allocation_material = 0.80 * available
            objective_installed = installed_state.copy()
            future_shocks = [
                event
                for event in shock_events
                if float(event[0]) >= float(t[k])
            ]
            if allocation_policy in {"shock_aware", "perfect_foresight"}:
                for event_year, event_sector, event_fraction in future_shocks:
                    j = params.sector_idx(event_sector)
                    discount = (
                        float(event_fraction)
                        if allocation_policy == "perfect_foresight"
                        else min(float(event_fraction), 0.25)
                    )
                    objective_installed[j] *= 1.0 - discount
            sector_order = _independent_sector_order(
                params,
                seed_result,
                objective_installed,
                op_sector,
                allocation_material,
                gross_cell_order_budget=gross_budget,
                productivity_multiplier=productivity * autonomy_gain,
                dt=dt,
            )
            material_use = profile.B_effective @ sector_order
            normalized_order = np.divide(
                sector_order,
                z,
                out=np.zeros(params.n),
                where=z > 1e-12,
            )
            ordered[k + 1] = float(np.min(normalized_order))
            binding = np.flatnonzero(
                available - material_use <= 1e-8
            )
            if len(binding):
                primary = "material"
                limiting_counts[binding] += 1
        if (
            repair_enabled
            and (
                np.any(failed_available - repair_started > 1e-9)
                or np.any(repair_queue > 1e-9)
            )
            and (
                np.any(op_sector < viable_floor)
                or np.any(shock_loss > 1e-9)
            )
        ):
            primary = "repair"
        primary_constraints.append(primary)
        inventory[k + 1] = np.maximum(available - material_use, 0.0)
        ordered_sector[k + 1] = sector_order

        due = queue[:, 0].copy()
        queue[:, :-1] = queue[:, 1:]
        queue[:, -1] = 0.0
        for j in range(params.n):
            queue[j, lag_steps[j] - 1] += sector_order[j]
            activation_queue[j, :ramp_steps[j]] += (
                due[j] / ramp_steps[j]
            )
        commissioned_sector[k + 1] = due

        activated_due = activation_queue[:, 0].copy()
        activation_queue[:, :-1] = activation_queue[:, 1:]
        activation_queue[:, -1] = 0.0
        activation_queue *= np.maximum(
            1.0 - effective_delta[:, None] * dt,
            0.0,
        )
        activated_sector[k + 1] = activated_due

        installed_before_repair = np.maximum(
            installed_state * (1.0 - effective_delta * dt)
            + due,
            0.0,
        )
        installed_next = installed_before_repair + repaired_due
        op_after_loss = np.maximum(
            operating_sector[k] * (1.0 - effective_delta * dt),
            0.0,
        )
        operating_next = op_after_loss + activated_due + repaired_due
        installed_sector[k + 1] = installed_next
        operating_sector[k + 1] = np.minimum(
            np.maximum(operating_next, 0.0),
            installed_next,
        )
        installed[k + 1] = float(np.min(np.divide(
            installed_sector[k + 1],
            z,
            out=np.full(params.n, np.inf),
            where=z > 1e-12,
        )))
        operating[k + 1] = float(np.min(np.divide(
            operating_sector[k + 1],
            z,
            out=np.full(params.n, np.inf),
            where=z > 1e-12,
        )))

        compute[k + 1] = operating_sector[k + 1, i_compute] * compute_scale
        verification = float(params.intelligence["verification_factor"])
        learning = float(params.intelligence["learning_rate_per_year"])
        normalized_compute = compute[k + 1] / max(compute[0], 1e-12)
        d_intelligence = (
            learning * math.log1p(normalized_compute) * verification * dt
        )
        intelligence[k + 1] = min(
            intelligence[k] + d_intelligence,
            float(params.intelligence["maximum_level"]),
        )

    reached = np.flatnonzero(operating >= 2.0)
    doubling = float(t[reached[0]]) if len(reached) else None
    intervention_demand[-1] = float(
        profile.intervention_hours_per_year
        @ np.maximum(operating_sector[-1], 0.0)
    )
    verification_demand[-1] = verification_demand[-2] if steps else 0.0
    survived = bool(
        np.min(installed) >= min_cells
        and installed[-1] >= min_cells
        and np.all(operating_sector[-1] >= viable_floor)
    )
    limiting = tuple(
        (params.elements[i], int(limiting_counts[i]))
        for i in np.argsort(-limiting_counts)
        if limiting_counts[i] > 0
    )
    return CapacityGrowthResult(
        scenario=seed_result.scenario,
        t=t,
        installed_sector_capacity=installed_sector,
        operating_sector_capacity=operating_sector,
        ordered_sector_capacity=ordered_sector,
        installed_cells=installed,
        operating_cells=operating,
        intelligence=intelligence,
        local_compute=compute,
        inventory_t=inventory,
        ordered_cells=ordered,
        aggregate_doubling_year=doubling,
        survived=survived,
        limiting_elements=limiting,
        lunar_material_t=lunar_total,
        asteroid_material_t=asteroid_total,
        recycled_material_t=recycled_total,
        failed_sector_capacity=failed_sector,
        repaired_sector_capacity=repaired_sector,
        commissioned_sector_capacity=commissioned_sector,
        activated_sector_capacity=activated_sector,
        shock_loss_sector_capacity=shock_loss_sector,
        allocation_policy=allocation_policy,
        repair_enabled=repair_enabled,
        primary_constraint=tuple(primary_constraints),
        intervention_demand_hours=intervention_demand,
        verification_demand_units=verification_demand,
    )


def compare_compute_regimes(
    params: IntegratedParams,
    capacity_growth: CapacityGrowthResult,
) -> ComputeComparison:
    t = capacity_growth.t
    dt = float(t[1] - t[0])
    dep = float(params.earth_compute["depreciation_per_year"])
    terrestrial: dict[str, np.ndarray] = {}
    orbital: dict[str, np.ndarray] = {}
    for label, cfg in params.earth_compute.items():
        if label == "depreciation_per_year":
            continue
        earth = np.zeros_like(t)
        orbit = np.zeros_like(t)
        earth[0] = orbit[0] = 1.0
        for k in range(len(t) - 1):
            build = float(cfg["terrestrial_build_units_per_year"])
            ceiling = float(cfg["terrestrial_site_ceiling_units"])
            if earth[k] >= ceiling:
                build = 0.0
            else:
                build = min(build, (ceiling - earth[k]) / dt)
            earth[k + 1] = max(earth[k] + (build - dep * earth[k]) * dt, 0.0)

            delivery = min(
                float(cfg["earth_to_orbit_build_units_per_year"]),
                float(cfg["launch_units_per_year"]),
            )
            orbit[k + 1] = max(
                orbit[k] + (delivery - dep * orbit[k]) * dt,
                0.0,
            )
        terrestrial[label] = earth
        orbital[label] = orbit
    endogenous = (
        capacity_growth.local_compute
        / max(capacity_growth.local_compute[0], 1e-12)
    )
    arc = params.transfer_arcs["moon_to_orbit_compute"]
    export_share = float(arc["share_of_new_endogenous_compute"])
    export_lag_steps = max(1, int(round(float(arc["lag_years"]) / dt)))
    i_transport = params.sector_idx("transport")
    # The canonical cell's transport capacity scales with operating cells.
    # Capacity values are normalized to the initial off-world compute stock.
    base_seed = size_seed(params, capacity_growth.scenario)
    transport_per_cell = (
        base_seed.capacities[i_transport] if base_seed.feasible else params.min_seed[i_transport]
    )
    transport_rate = (
        float(arc["normalized_compute_units_per_transport_capacity_year"])
        * transport_per_cell
        * capacity_growth.operating_cells
    )
    endogenous_orbit = np.ones_like(t)
    export_queue = np.zeros(export_lag_steps + 1)
    for k in range(len(t) - 1):
        new_capacity = max(endogenous[k + 1] - endogenous[k], 0.0)
        export = min(export_share * new_capacity, transport_rate[k] * dt)
        due = export_queue[0]
        export_queue[:-1] = export_queue[1:]
        export_queue[-1] = export
        endogenous_orbit[k + 1] = max(
            endogenous_orbit[k] * (1.0 - dep * dt) + due,
            0.0,
        )
    return ComputeComparison(t, endogenous, endogenous_orbit, terrestrial, orbital)


def simulate_debris(
    params: IntegratedParams,
    deployment_capacity: np.ndarray,
    t: np.ndarray,
    mitigation: str,
    *,
    label: str | None = None,
) -> DebrisResult:
    cfg = params.debris
    mit = cfg["scenarios"][mitigation]
    dt = float(t[1] - t[0])
    active = np.zeros_like(t)
    derelict = np.zeros_like(t)
    fragments = np.zeros_like(t)
    created = np.zeros_like(t)
    cleared = np.zeros_like(t)
    active[0] = float(cfg["initial_active_units"])
    derelict[0] = float(cfg["initial_derelict_units"])
    fragments[0] = float(cfg["initial_fragment_index"])
    deployments = np.maximum(np.diff(deployment_capacity, prepend=deployment_capacity[0]), 0.0)

    for k in range(len(t) - 1):
        failures = float(cfg["asset_failure_per_year"]) * active[k] * dt
        hazard_population = (
            active[k]
            + derelict[k]
            + float(cfg["fragment_hazard_multiplier"]) * fragments[k]
        )
        kernel = float(cfg["collision_kernel"]) * float(
            mit.get("collision_kernel_multiplier", 1.0)
        )
        collisions = kernel * active[k] * hazard_population * dt
        collisions = min(collisions, 0.25 * active[k])
        disposed = float(mit["controlled_disposal_fraction"]) * failures
        retrieval = min(
            float(mit["retrieval_fraction_per_year"]) * derelict[k] * dt,
            derelict[k],
        )
        frag_created = float(cfg["fragments_per_collision_index"]) * collisions
        frag_cleared = min(
            (
                float(cfg["natural_fragment_clearance_per_year"]) * fragments[k]
                + float(mit["active_removal_fragment_index_per_year"])
            ) * dt,
            fragments[k] + frag_created,
        )
        derelict_collision_clear = min(
            float(cfg["derelict_collision_clearance_fraction"]) * collisions,
            derelict[k] + failures - disposed,
        )
        active[k + 1] = max(
            active[k] + deployments[k + 1] - failures - collisions,
            0.0,
        )
        derelict[k + 1] = max(
            derelict[k] + failures - disposed - retrieval - derelict_collision_clear,
            0.0,
        )
        fragments[k + 1] = max(fragments[k] + frag_created - frag_cleared, 0.0)
        created[k + 1] = frag_created
        cleared[k + 1] = frag_cleared

    window = max(1, int(round(5.0 / dt)))
    c_new = float(created[-window:].sum())
    c_clear = float(cleared[-window:].sum())
    ratio = c_new / c_clear if c_clear > 0 else math.inf
    return DebrisResult(
        label=label or mitigation,
        t=t,
        active=active,
        derelict=derelict,
        fragments=fragments,
        fragments_created=created,
        fragments_cleared=cleared,
        creation_clearance_ratio=ratio,
        # At an effectively empty fragment stock, actual clearance is capped
        # by available fragments, so creation/actual-clearance approaches
        # exactly one even when removal capacity exceeds creation.  Treat
        # that zero-stock boundary as non-supercritical when the stock is not
        # rising over the reporting window.
        subcritical=bool(
            ratio <= 1.0 + 1e-9
            and fragments[-1] <= fragments[-window] + 1e-9
        ),
    )


def simulate_shell_debris(
    params: IntegratedParams,
    deployment_capacity: np.ndarray,
    t: np.ndarray,
) -> ShellDebrisResult:
    """Finite-mass, shell- and fragment-class-resolved orbital stress model.

    Requested positive deployment increments consume feed inventory. Feed is
    supplied only by finite-reservoir capture, time-limited Earth imports, and
    recovered controlled retirements. Collision and failure losses reduce
    active capacity, so the returned trajectory—not the requested input—is
    the industrially available orbital stock.
    """
    cfg = params.raw["orbital_mass_and_shell_debris"]
    shell_cfg = cfg["shells"]
    shells = tuple(row["name"] for row in shell_cfg)
    ns = len(shells)
    if len(t) != len(deployment_capacity) or len(t) < 2:
        raise ValueError("deployment_capacity and t must have equal length >= 2")
    transfer = np.asarray(cfg["cross_shell_transfer"], dtype=float)
    if transfer.shape != (ns, ns) or not np.allclose(
        transfer.sum(axis=1), 1.0
    ):
        raise ValueError("cross-shell transfer matrix must be row-stochastic")
    shares = np.array(
        [float(row["deployment_share"]) for row in shell_cfg],
        dtype=float,
    )
    if not math.isclose(float(shares.sum()), 1.0, abs_tol=1e-12):
        raise ValueError("shell deployment shares must sum to one")

    dt = float(t[1] - t[0])
    shape = (len(t), ns)
    active = np.zeros(shape)
    derelict = np.zeros(shape)
    trackable = np.zeros(shape)
    untrackable = np.zeros(shape)
    active[0] = float(deployment_capacity[0]) * shares
    derelict[0] = 0.08 * active[0]
    trackable[0] = 0.10 * shares
    untrackable[0] = 0.30 * shares

    reservoir = np.zeros(len(t))
    feed = np.zeros(len(t))
    imported = np.zeros(len(t))
    captured = np.zeros(len(t))
    recovered = np.zeros(len(t))
    lost = np.zeros(len(t))
    requested = np.zeros(len(t))
    served = np.zeros(len(t))
    shortfall = np.zeros(len(t))
    reservoir[0] = float(cfg["initial_uncaptured_reservoir_t"])
    feed[0] = float(cfg["initial_feed_inventory_t"])
    mass_per_unit = float(cfg["mass_t_per_capacity_unit"])

    requested_increments = np.maximum(
        np.diff(deployment_capacity, prepend=deployment_capacity[0]),
        0.0,
    )
    for k in range(len(t) - 1):
        capture = min(
            reservoir[k],
            reservoir[k]
            * float(cfg["capture_fraction_of_reservoir_per_year"])
            * dt,
        )
        earth_import = (
            float(cfg["earth_import_t_per_year"]) * dt
            if t[k] < float(cfg["earth_import_cutoff_year"])
            else 0.0
        )
        available_feed = feed[k] + capture + earth_import
        demand_units = float(requested_increments[k + 1])
        served_units = min(
            demand_units,
            available_feed / max(mass_per_unit, 1e-12),
        )
        requested[k + 1] = demand_units
        served[k + 1] = served_units
        shortfall[k + 1] = demand_units - served_units
        available_feed -= served_units * mass_per_unit

        failures = (
            float(cfg["asset_failure_per_year"]) * active[k] * dt
        )
        collisions = np.zeros(ns)
        for s, row in enumerate(shell_cfg):
            hazard = (
                active[k, s]
                + derelict[k, s]
                + float(cfg["fragment_hazard_weight_trackable"])
                * trackable[k, s]
                + float(cfg["fragment_hazard_weight_untrackable"])
                * untrackable[k, s]
            )
            saturation = 1.0 + float(
                cfg["avoidance_saturation_slope"]
            ) * max(
                trackable[k, s]
                - float(cfg["avoidance_saturation_threshold"]),
                0.0,
            )
            collisions[s] = min(
                float(row["collision_kernel"])
                * saturation
                * active[k, s]
                * hazard
                / max(float(row["volume_index"]), 1e-12)
                * dt,
                0.25 * active[k, s],
            )
        disposed = (
            float(cfg["controlled_disposal_fraction"]) * failures
        )
        retrieval = np.minimum(
            float(cfg["retrieval_fraction_per_year"]) * derelict[k] * dt,
            derelict[k],
        )
        recovered_mass = (
            float(cfg["recovery_fraction_of_controlled_retirement"])
            * float((disposed + retrieval).sum())
            * mass_per_unit
        )
        unrecoverable_mass = float(
            collisions.sum() * mass_per_unit
            + (
                1.0
                - float(cfg[
                    "recovery_fraction_of_controlled_retirement"
                ])
            )
            * float((disposed + retrieval).sum())
            * mass_per_unit
        )

        new_trackable_origin = (
            float(cfg["trackable_fragments_per_collision"]) * collisions
        )
        new_untrackable_origin = (
            float(cfg["untrackable_fragments_per_collision"]) * collisions
        )
        new_trackable = new_trackable_origin @ transfer
        new_untrackable = new_untrackable_origin @ transfer
        trackable_clear = np.array([
            float(row["natural_trackable_clearance_per_year"])
            * trackable[k, s] * dt
            + float(row["active_removal_trackable_per_year"]) * dt
            for s, row in enumerate(shell_cfg)
        ])
        untrackable_clear = np.array([
            float(row["natural_untrackable_clearance_per_year"])
            * untrackable[k, s] * dt
            for s, row in enumerate(shell_cfg)
        ])
        trackable_clear = np.minimum(
            trackable_clear,
            trackable[k] + new_trackable,
        )
        untrackable_clear = np.minimum(
            untrackable_clear,
            untrackable[k] + new_untrackable,
        )

        deployments = served_units * shares
        active[k + 1] = np.maximum(
            active[k] + deployments - failures - collisions,
            0.0,
        )
        derelict[k + 1] = np.maximum(
            derelict[k] + failures - disposed - retrieval,
            0.0,
        )
        trackable[k + 1] = np.maximum(
            trackable[k] + new_trackable - trackable_clear,
            0.0,
        )
        untrackable[k + 1] = np.maximum(
            untrackable[k] + new_untrackable - untrackable_clear,
            0.0,
        )
        reservoir[k + 1] = reservoir[k] - capture
        feed[k + 1] = available_feed + recovered_mass
        imported[k + 1] = earth_import
        captured[k + 1] = capture
        recovered[k + 1] = recovered_mass
        lost[k + 1] = unrecoverable_mass

    branching = np.zeros(ns)
    for s, row in enumerate(shell_cfg):
        hazard = (
            active[-1, s]
            + derelict[-1, s]
            + float(cfg["fragment_hazard_weight_trackable"])
            * trackable[-1, s]
            + float(cfg["fragment_hazard_weight_untrackable"])
            * untrackable[-1, s]
        )
        collision_probability = (
            float(row["collision_kernel"])
            * hazard
            / max(float(row["volume_index"]), 1e-12)
        )
        weighted_descendants = (
            float(cfg["trackable_fragments_per_collision"])
            * float(cfg["fragment_hazard_weight_trackable"])
            / max(
                float(row["natural_trackable_clearance_per_year"]),
                1e-12,
            )
            + float(cfg["untrackable_fragments_per_collision"])
            * float(cfg["fragment_hazard_weight_untrackable"])
            / max(
                float(row["natural_untrackable_clearance_per_year"]),
                1e-12,
            )
        )
        branching[s] = collision_probability * weighted_descendants

    accessible = (
        feed
        + mass_per_unit * (active.sum(axis=1) + derelict.sum(axis=1))
    )
    cost = (
        float(imported.sum() + lost.sum())
        * 1000.0
        * float(cfg["replacement_delivery_cost_per_kg"])
    )
    return ShellDebrisResult(
        t=t,
        shells=shells,
        active_capacity=active,
        intact_derelicts=derelict,
        trackable_fragments=trackable,
        untrackable_fragments=untrackable,
        uncaptured_reservoir_t=reservoir,
        feed_inventory_t=feed,
        accessible_orbital_mass_t=accessible,
        earth_imported_t=imported,
        captured_t=captured,
        recovered_t=recovered,
        unrecoverable_loss_t=lost,
        requested_deployment_units=requested,
        served_deployment_units=served,
        deployment_shortfall_units=shortfall,
        branching_ratio_by_shell=branching,
        replacement_and_import_cost_usd=cost,
    )


def _named_loguniform(
    seed: int,
    run_index: int,
    name: str,
    bounds: tuple[float, float],
) -> float:
    entropy = zlib.crc32(f"{seed}/{run_index}/{name}".encode("utf-8"))
    rng = np.random.default_rng(entropy)
    lo, hi = bounds
    return float(np.exp(rng.uniform(np.log(lo), np.log(hi))))


def sample_integrated_params(
    params: IntegratedParams,
    *,
    seed: int,
    run_index: int,
) -> IntegratedParams:
    draw = {
        name: _named_loguniform(seed, run_index, name, bounds)
        for name, bounds in params.uncertainty.items()
    }
    gap = 1.0 - params.base_coverage
    base_coverage = np.clip(
        1.0 - gap * draw["autonomy_gap_multiplier"],
        0.0,
        params.coverage_ceiling,
    )
    return replace(
        params,
        q=params.q * draw["service_productivity_multiplier"],
        B=params.B * draw["bom_multiplier"],
        lunar_yield=params.lunar_yield * draw["lunar_yield_multiplier"],
        asteroid_yield=params.asteroid_yield * draw["asteroid_yield_multiplier"],
        delta=params.delta * draw["depreciation_multiplier"],
        lag=params.lag * draw["lag_multiplier"],
        ramp=params.ramp * draw["lag_multiplier"],
        base_coverage=base_coverage,
    )


def seed_ensemble(
    params: IntegratedParams,
    scenario: str,
    *,
    n_runs: int = 200,
    seed: int = 404,
    years: float = 40.0,
    dt: float = 0.5,
) -> EnsembleSummary:
    masses: list[float] = []
    doubling: list[float] = []
    survived = 0
    feasible = 0
    for i in range(n_runs):
        sampled = sample_integrated_params(params, seed=seed, run_index=i)
        sized = size_seed(sampled, scenario)
        if not sized.feasible:
            continue
        feasible += 1
        masses.append(float(sized.total_seed_mass_t))
        run = simulate_capacity_growth(sampled, sized, years=years, dt=dt)
        survived += int(run.survived)
        if run.aggregate_doubling_year is not None:
            doubling.append(run.aggregate_doubling_year)
    return EnsembleSummary(
        scenario=scenario,
        n_runs=n_runs,
        n_feasible=feasible,
        seed_masses_t=tuple(masses),
        aggregate_doubling_years=tuple(doubling),
        n_survived=survived,
    )
