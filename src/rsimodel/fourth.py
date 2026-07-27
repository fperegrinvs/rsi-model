"""Fourth Edition integrated bootstrap model.

This module is deliberately separate from the r3.5 ten-sector model.  It
adds the structures that the Fourth Edition manuscript names as missing:

* seven non-substitutable electronics tiers;
* element-by-sector bills of material and source-specific recoverable yields;
* an explicit lunar-surface / asteroid / Earth-vitamin material graph;
* process-specific gravity overhead;
* task-resolved embodied autonomy and residual intervention demand;
* commissioning lags, yield ramps, minimum viable scale, and an explicit
  commissioned second production cell;
* a coupled, intentionally stylized intelligence/compute/productivity loop;
* rate-limited terrestrial and Earth-fed orbital compute counterfactuals; and
* endogenous debris stocks with a reported five-year fragment
  creation-to-clearance ratio.

The numerical coefficients in ``params/fourth_edition.yaml`` are scenario
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

PARAMS_PATH = Path(__file__).resolve().parents[2] / "params" / "fourth_edition.yaml"


@dataclass(frozen=True)
class FourthParams:
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
    ai_level: float
    coverage: np.ndarray
    q_effective: np.ndarray
    B_effective: np.ndarray
    centrifuge_rpm: np.ndarray
    centrifuge_mass_t: np.ndarray
    intervention_hours_per_year: np.ndarray

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
    vitamin_stock_mass_t: float | None
    digital_seed_mass_t: float
    capacities: np.ndarray
    vitamin_stock_t: np.ndarray
    lunar_feed_t_per_year: float
    asteroid_feed_t_per_year: float
    minimum_task_coverage: float
    intervention_hours_per_year: float
    binding_constraints: tuple[tuple[str, float], ...]
    process: ProcessProfile

    def capacity(self, params: FourthParams, sector: str) -> float:
        return float(self.capacities[params.sector_idx(sector)])


@dataclass(frozen=True)
class ReproductionResult:
    scenario: str
    t: np.ndarray
    installed_cells: np.ndarray
    operating_cells: np.ndarray
    intelligence: np.ndarray
    local_compute: np.ndarray
    inventory_t: np.ndarray
    ordered_cells: np.ndarray
    second_cell_year: float | None
    survived: bool
    limiting_elements: tuple[tuple[str, int], ...]
    lunar_material_t: float
    asteroid_material_t: float
    recycled_material_t: float


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
    reproduction_ratio: float
    subcritical: bool


@dataclass(frozen=True)
class EnsembleSummary:
    scenario: str
    n_runs: int
    n_feasible: int
    seed_masses_t: tuple[float, ...]
    second_cell_years: tuple[float, ...]
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


def _vector(names: tuple[str, ...], values: dict[str, float], label: str) -> np.ndarray:
    unknown = set(values) - set(names)
    if unknown:
        raise ValueError(f"{label}: unknown names: {sorted(unknown)}")
    return np.array([float(values.get(name, 0.0)) for name in names], dtype=float)


def load_fourth_params(path: Path | None = None) -> FourthParams:
    with open(path or PARAMS_PATH, encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    elements = tuple(raw["elements"])
    sector_rows = raw["sectors"]
    sectors = tuple(row["name"] for row in sector_rows)
    if len(set(elements)) != len(elements) or len(set(sectors)) != len(sectors):
        raise ValueError("Fourth Edition elements and sectors must be unique")

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

    uncertainty = {
        name: (float(bounds[0]), float(bounds[1]))
        for name, bounds in raw["uncertainty"].items()
    }
    return FourthParams(
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
    params: FourthParams,
    scenario: str,
    *,
    ai_level: float | None = None,
) -> ProcessProfile:
    cfg = params.scenarios[scenario]
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
    q_eff = params.q * autonomy_productivity / (1.0 + parasitic)
    accel_m_s2 = acceleration_gap_g * 9.80665
    omega = np.sqrt(np.divide(
        accel_m_s2,
        params.centrifuge_radius,
        out=np.zeros_like(accel_m_s2),
        where=params.centrifuge_radius > 0,
    ))
    rpm = omega * 60.0 / (2.0 * math.pi)
    intervention = params.intervention_hours * np.maximum(1.0 - coverage, 0.0)
    return ProcessProfile(
        scenario=scenario,
        ai_level=level,
        coverage=coverage,
        q_effective=q_eff,
        B_effective=B_eff,
        centrifuge_rpm=rpm,
        centrifuge_mass_t=centrifuge_mass,
        intervention_hours_per_year=intervention,
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


def size_seed(params: FourthParams, scenario: str) -> SeedResult:
    cfg = params.scenarios[scenario]
    profile = process_profile(params, scenario)
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

    # Variables: sector capacities z[n], lunar feed p_l, asteroid feed p_a,
    # and initial Earth-vitamin stocks v[m].
    n, m = params.n, params.m
    iz = slice(0, n)
    ip_l, ip_a = n, n + 1
    iv = slice(n + 2, n + 2 + m)
    nv = n + 2 + m
    mass_per_capacity = profile.B_effective.sum(axis=0)
    c = np.zeros(nv)
    c[iz] = mass_per_capacity
    c[iv] = 1.0

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
    replacement_multiplier = 1.0 + params.delta * T
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
    # complete service recipe of a commissioned second cell.
    for i, sector in enumerate(params.sectors):
        row = np.zeros(nv)
        row[iz] = params.A[i] * replacement_multiplier
        row[i] -= profile.q_effective[i] * productive_years[i]
        rows.append(row)
        rhs.append(0.0)
        labels.append(f"service:{sector}")

    # Element balances: initial vitamin stock is the only Earth term.
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

    A_ub = np.vstack(rows)
    b_ub = np.array(rhs)
    solved = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not solved.success:
        return SeedResult(
            scenario, False, solved.message, None, None, None, digital_mass,
            np.zeros(n), np.zeros(m), 0.0, 0.0,
            profile.minimum_coverage, 0.0, (), profile,
        )

    x = solved.x
    capacities = x[iz].copy()
    vitamins = x[iv].copy()
    physical = float(mass_per_capacity @ capacities)
    vitamin_mass = float(vitamins.sum())
    total = physical + vitamin_mass + digital_mass
    interventions = float(profile.intervention_hours_per_year @ capacities)
    return SeedResult(
        scenario=scenario,
        feasible=True,
        status="optimal within the declared linear seed architecture",
        total_seed_mass_t=total,
        physical_seed_mass_t=physical,
        vitamin_stock_mass_t=vitamin_mass,
        digital_seed_mass_t=digital_mass,
        capacities=capacities,
        vitamin_stock_t=vitamins,
        lunar_feed_t_per_year=float(x[ip_l]),
        asteroid_feed_t_per_year=float(x[ip_a]),
        minimum_task_coverage=profile.minimum_coverage,
        intervention_hours_per_year=interventions,
        binding_constraints=_constraint_slacks(labels, A_ub, b_ub, x),
        process=profile,
    )


def simulate_reproduction(
    params: FourthParams,
    seed_result: SeedResult,
    *,
    years: float = 40.0,
    dt: float = 0.25,
) -> ReproductionResult:
    if not seed_result.feasible:
        raise ValueError(f"Cannot simulate infeasible seed: {seed_result.status}")
    cfg = params.scenarios[seed_result.scenario]
    profile = seed_result.process
    z = seed_result.capacities
    cell_bom = profile.B_effective @ z
    service_need = params.A @ z
    service_ratio = np.divide(
        profile.q_effective * z,
        service_need,
        out=np.full(params.n, np.inf),
        where=service_need > 1e-12,
    )
    base_cell_rate = min(
        float(np.min(service_ratio)),
        float(params.seed["maximum_gross_cell_orders_per_operating_cell_year"]),
    )

    steps = int(round(years / dt))
    t = np.arange(steps + 1, dtype=float) * dt
    installed = np.zeros(steps + 1)
    operating = np.zeros(steps + 1)
    intelligence = np.zeros(steps + 1)
    compute = np.zeros(steps + 1)
    inventory = np.zeros((steps + 1, params.m))
    ordered = np.zeros(steps + 1)
    installed[0] = operating[0] = 1.0
    intelligence[0] = float(cfg["ai_level"])
    i_compute = params.sector_idx("compute")
    compute_scale = float(params.intelligence["compute_units_per_compute_capacity"])
    compute[0] = operating[0] * z[i_compute] * compute_scale
    inventory[0] = seed_result.vitamin_stock_t

    lag_steps = max(1, int(round(float(params.seed["construction_lag_years"]) / dt)))
    queue = np.zeros(lag_steps + 1)
    cell_delta = float(params.seed["cell_depreciation_per_year"])
    ramp = float(params.seed["cell_yield_ramp_years"])
    recovery = float(params.seed["recycling_recovery_fraction"])
    min_cells = float(params.seed["minimum_viable_cell_equivalents"])
    asteroid_start = float(cfg["asteroid_commission_year"])
    limiting_counts = np.zeros(params.m, dtype=int)
    lunar_total = asteroid_total = recycled_total = 0.0

    for k in range(steps):
        op = max(operating[k], 0.0)
        retired = installed[k] * cell_delta * dt
        recovered = recovery * retired * cell_bom
        recycled_total += float(recovered.sum())

        lunar_prod = (
            params.lunar_yield * seed_result.lunar_feed_t_per_year * op * dt
        )
        asteroid_prod = np.zeros(params.m)
        if cfg["asteroid_enabled"] and t[k] >= asteroid_start:
            asteroid_prod = (
                params.asteroid_yield
                * seed_result.asteroid_feed_t_per_year
                * op * dt
            )
        lunar_total += float(lunar_prod.sum())
        asteroid_total += float(asteroid_prod.sum())
        available = inventory[k] + recovered + lunar_prod + asteroid_prod

        level_gain = max(intelligence[k] - float(cfg["ai_level"]), 0.0)
        productivity = 1.0 + float(
            params.intelligence["productivity_elasticity"]
        ) * level_gain
        autonomy_gain = 1.0 + float(
            params.intelligence["autonomy_learning_multiplier"]
        ) * level_gain
        desired = base_cell_rate * op * productivity * autonomy_gain * dt
        if desired > 0.0:
            material_limit_by_element = np.divide(
                available,
                cell_bom,
                out=np.full(params.m, np.inf),
                where=cell_bom > 1e-12,
            )
            material_limit = float(np.min(material_limit_by_element))
            built = min(desired, max(material_limit, 0.0))
            if built + 1e-10 < desired:
                binding = np.flatnonzero(
                    material_limit_by_element <= material_limit + 1e-8
                )
                limiting_counts[binding] += 1
        else:
            built = 0.0
        inventory[k + 1] = np.maximum(available - built * cell_bom, 0.0)
        ordered[k + 1] = built
        due = queue[0]
        queue[:-1] = queue[1:]
        queue[-1] = built

        installed_next = max(installed[k] * (1.0 - cell_delta * dt) + due, 0.0)
        op_after_loss = max(operating[k] * (1.0 - cell_delta * dt), 0.0)
        if ramp > 0:
            operating_next = op_after_loss + (
                installed_next - op_after_loss
            ) * min(dt / ramp, 1.0)
        else:
            operating_next = installed_next
        installed[k + 1] = installed_next
        operating[k + 1] = min(max(operating_next, 0.0), installed_next)

        compute[k + 1] = operating[k + 1] * z[i_compute] * compute_scale
        verification = float(params.intelligence["verification_factor"])
        learning = float(params.intelligence["learning_rate_per_year"])
        normalized_compute = compute[k + 1] / max(compute[0], 1e-12)
        d_intelligence = learning * math.log1p(normalized_compute) * verification * dt
        intelligence[k + 1] = min(
            intelligence[k] + d_intelligence,
            float(params.intelligence["maximum_level"]),
        )

    reached = np.flatnonzero(operating >= 2.0)
    second = float(t[reached[0]]) if len(reached) else None
    survived = bool(np.min(installed) >= min_cells and installed[-1] >= min_cells)
    limiting = tuple(
        (params.elements[i], int(limiting_counts[i]))
        for i in np.argsort(-limiting_counts)
        if limiting_counts[i] > 0
    )
    return ReproductionResult(
        scenario=seed_result.scenario,
        t=t,
        installed_cells=installed,
        operating_cells=operating,
        intelligence=intelligence,
        local_compute=compute,
        inventory_t=inventory,
        ordered_cells=ordered,
        second_cell_year=second,
        survived=survived,
        limiting_elements=limiting,
        lunar_material_t=lunar_total,
        asteroid_material_t=asteroid_total,
        recycled_material_t=recycled_total,
    )


def compare_compute_regimes(
    params: FourthParams,
    reproduction: ReproductionResult,
) -> ComputeComparison:
    t = reproduction.t
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
    endogenous = reproduction.local_compute / max(reproduction.local_compute[0], 1e-12)
    arc = params.transfer_arcs["moon_to_orbit_compute"]
    export_share = float(arc["share_of_new_endogenous_compute"])
    export_lag_steps = max(1, int(round(float(arc["lag_years"]) / dt)))
    i_transport = params.sector_idx("transport")
    # The canonical cell's transport capacity scales with operating cells.
    # Capacity values are normalized to the initial off-world compute stock.
    base_seed = size_seed(params, reproduction.scenario)
    transport_per_cell = (
        base_seed.capacities[i_transport] if base_seed.feasible else params.min_seed[i_transport]
    )
    transport_rate = (
        float(arc["normalized_compute_units_per_transport_capacity_year"])
        * transport_per_cell
        * reproduction.operating_cells
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
    params: FourthParams,
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
        reproduction_ratio=ratio,
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


def sample_fourth_params(
    params: FourthParams,
    *,
    seed: int,
    run_index: int,
) -> FourthParams:
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
    params: FourthParams,
    scenario: str,
    *,
    n_runs: int = 200,
    seed: int = 404,
    years: float = 40.0,
    dt: float = 0.5,
) -> EnsembleSummary:
    masses: list[float] = []
    second: list[float] = []
    survived = 0
    feasible = 0
    for i in range(n_runs):
        sampled = sample_fourth_params(params, seed=seed, run_index=i)
        sized = size_seed(sampled, scenario)
        if not sized.feasible:
            continue
        feasible += 1
        masses.append(float(sized.total_seed_mass_t))
        run = simulate_reproduction(sampled, sized, years=years, dt=dt)
        survived += int(run.survived)
        if run.second_cell_year is not None:
            second.append(run.second_cell_year)
    return EnsembleSummary(
        scenario=scenario,
        n_runs=n_runs,
        n_feasible=feasible,
        seed_masses_t=tuple(masses),
        second_cell_years=tuple(second),
        n_survived=survived,
    )
