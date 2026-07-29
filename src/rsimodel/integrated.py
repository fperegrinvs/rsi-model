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
from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from typing import NotRequired, TypedDict

import numpy as np

from .array_types import BoolArray, FloatArray, validate_shape
from .extension_config import (
    AuthorizedCapacityControlConfig,
    BottleneckUpgradeConfig,
    ChronologicalReleaseBacktestConfig,
    CognitivePhysicalLaborConfig,
    ComputeAllocationConfig,
    ComputeCohortConfig,
    ComputeDemandConfig,
    CoordinationConfig,
    DataAdvantageConfig,
    DataEvaluatorCoevolutionConfig,
    DigitalImprovementConfig,
    ElectronicsSupplyChainConfig,
    EmbodimentBOMConfig,
    IndustrialReliabilityConfig,
    IntelligenceMarginalResponseConfig,
    IntergenerationalLearningConfig,
    MilestoneOrderConfig,
    PartialClosureSupportConfig,
    ReplicationGovernanceConfig,
    VerificationHierarchyConfig,
)
from .extensions import verified_loop_throughput
from .orbital_config import (
    OrbitalControlConfig,
    OrbitalLifecycleConfig,
    OrbitalResilienceConfig,
    OrbitalServiceStrategyConfig,
    OrbitalTransportConfig,
)
from .solver_adapter import solve_linear_program
from .typed_config import parse_typed_config
from .yaml_adapter import (
    load_yaml_mapping,
    require_mapping,
    require_number,
    require_sequence,
    require_string,
)

PARAMS_PATH = Path(__file__).resolve().parents[2] / "params" / "integrated_model.yaml"


class EnvironmentSettings(TypedDict):
    lunar_gravity_g: float
    centrifuge_structural_mass_fraction_at_full_g: float
    centrifuge_parasitic_power_fraction_at_full_g: float
    centrifuge_overhead_composition: Mapping[str, float]


class SectorSettings(TypedDict):
    name: str
    q_per_capacity_year: float
    depreciation_per_year: float
    min_seed_capacity: float
    commissioning_lag_years: float
    yield_ramp_years: float
    gravity_required_g: float
    centrifuge_radius_m: float
    base_task_coverage: float
    autonomy_ceiling: float
    autonomy_response: float
    intervention_hours_per_capacity_year: float
    bom_t: Mapping[str, float]
    recipe_additions: Mapping[str, float]


class ScenarioSettings(TypedDict):
    description: str
    horizon_years: float
    asteroid_enabled: bool
    asteroid_commission_year: float
    ai_level: float
    minimum_task_coverage: float
    remote_intervention_budget_hours_per_year: float
    viable_floor_multiplier: float
    environment_profile: str
    earth_import_cutoff_year: float
    earth_import_caps_t: Mapping[str, float]


class SeedSettings(TypedDict):
    fixed_digital_seed_mass_t: float
    maximum_gross_cell_orders_per_operating_cell_year: float
    minimum_viable_cell_equivalents: float
    recycling_recovery_fraction: float
    repairable_failure_fraction: float
    repair_parts_fraction_of_bom: float
    repair_service_per_capacity: float
    repair_intervention_hours_per_capacity: float
    repair_lag_years: float


class IntelligenceSettings(TypedDict):
    initial_level: float
    verification_factor: float
    gain_scale_per_verified_loop: float
    frontier_gap_exponent: float
    productivity_elasticity: float
    autonomy_learning_multiplier: float
    maximum_level: float
    compute_units_per_compute_capacity: float
    effective_compute_factors: Mapping[str, float]
    verified_loop_stage_rates_per_year: Mapping[str, float]


class TransferArcSettings(TypedDict):
    cargo_class: str
    lag_years: float
    share_of_new_endogenous_compute: NotRequired[float]
    normalized_compute_units_per_transport_capacity_year: NotRequired[float]


class TransferArcsSettings(TypedDict):
    earth_to_moon_strategic_materials: TransferArcSettings
    asteroid_to_moon_feed: TransferArcSettings
    moon_to_orbit_compute: TransferArcSettings


@dataclass(frozen=True, slots=True)
class EarthComputeCase:
    terrestrial_build_units_per_year: float
    earth_to_orbit_build_units_per_year: float
    launch_units_per_year: float
    terrestrial_site_ceiling_units: float


@dataclass(frozen=True, slots=True)
class EarthComputeSettings:
    cases: Mapping[str, EarthComputeCase]
    depreciation_per_year: float


class DebrisMitigationSettings(TypedDict):
    controlled_disposal_fraction: float
    active_removal_fragment_index_per_year: float
    retrieval_fraction_per_year: float
    collision_kernel_multiplier: NotRequired[float]


class DebrisSettings(TypedDict):
    initial_active_units: float
    initial_derelict_units: float
    initial_fragment_index: float
    asset_failure_per_year: float
    collision_kernel: float
    fragment_hazard_multiplier: float
    fragments_per_collision_index: float
    natural_fragment_clearance_per_year: float
    derelict_collision_clearance_fraction: float
    scenarios: Mapping[str, DebrisMitigationSettings]


class KnowledgeAutonomySettings(TypedDict):
    source_class: str
    bounding_argument: str
    knowledge_package_t: Mapping[str, float]
    fault_diagnosis_scale: float
    verification_throughput_per_service_unit: float
    verification_units_per_new_capacity: float
    engineering_cycle_base_years: float
    engineering_cycle_response: float
    process_yield_floor: float
    repair_success_scale: float
    mttr_days_at_zero_coverage: float
    mttr_days_floor: float
    stop_line_threshold_below_declared_coverage: float
    compute_units_per_cell_order_year: float


class ProcessEnvironmentEffect(TypedDict):
    mechanism: str
    throughput_multiplier: float
    yield_multiplier: float
    depreciation_multiplier: float
    power_demand_multiplier: float


class ProcessEnvironmentProfileSettings(TypedDict):
    source_class: str
    note: str
    effects: Mapping[str, ProcessEnvironmentEffect]


class EmbodimentTaskSettings(TypedDict):
    sector: str
    requirements: Mapping[str, float]
    intelligence_onset: float
    intelligence_scale: float
    required_score: float


class EmbodimentValidationSweeps(TypedDict):
    fixed_embodiment_portfolio: str
    intelligence_levels: tuple[float, ...]
    fixed_intelligence_level: float
    embodiment_quality_multipliers: tuple[float, ...]


class EmbodimentCompatibilitySettings(TypedDict):
    source_class: str
    bounding_argument: str
    dimensions: tuple[str, ...]
    portfolios: Mapping[str, Mapping[str, float]]
    tasks: Mapping[str, EmbodimentTaskSettings]
    default_portfolio_by_scenario: Mapping[str, str]
    validation_sweeps: EmbodimentValidationSweeps
    terrestrial_rehearsal_faults: Mapping[str, Mapping[str, float]]


class DeploymentSettings(TypedDict):
    source_class: str
    bounding_argument: str
    transport_packaging_fraction: float
    initial_spares_fraction: float
    unloading_equipment_mass_t: float
    site_work_equipment_mass_t: float
    calibration_standards_mass_t: float
    startup_energy_mwh_per_seed_t: float
    startup_storage_t_per_mwh: float
    unloading_rate_t_per_year: float
    site_ready_year: float
    initial_power_ready_year: float
    installation_rate_t_per_year: float
    commissioning_rate_t_per_year: float
    startup_failure_fraction: float
    recovery_rate_t_per_year: float
    recovery_spares_t_per_failed_t: float


class OrbitalShellSettings(TypedDict):
    name: str
    deployment_share: float
    volume_index: float
    collision_kernel: float
    natural_trackable_clearance_per_year: float
    natural_untrackable_clearance_per_year: float
    active_removal_trackable_per_year: float


class OrbitalMassSettings(TypedDict):
    source_class: str
    bounding_argument: str
    initial_uncaptured_reservoir_t: float
    initial_feed_inventory_t: float
    earth_import_t_per_year: float
    earth_import_cutoff_year: float
    capture_fraction_of_reservoir_per_year: float
    mass_t_per_capacity_unit: float
    recovery_fraction_of_controlled_retirement: float
    replacement_delivery_cost_per_kg: float
    asset_failure_per_year: float
    controlled_disposal_fraction: float
    retrieval_fraction_per_year: float
    trackable_fragments_per_collision: float
    untrackable_fragments_per_collision: float
    fragment_hazard_weight_trackable: float
    fragment_hazard_weight_untrackable: float
    avoidance_saturation_threshold: float
    avoidance_saturation_slope: float
    shells: tuple[OrbitalShellSettings, ...]
    cross_shell_transfer: FloatArray


class ElectronicsTierSettings(TypedDict):
    local_producibility_fraction: float
    shelf_life_years: float
    obsolescence_per_year: float
    substitution_route: str
    measurement_priority: str


class ElectronicsArchitectureSettings(TypedDict):
    annual_import_fraction_of_initial_capacity: float
    initial_import_inventory_fraction: float
    local_producibility_multiplier: float
    cannibalization_fraction: float
    mature_substitution_credit_fraction: float


class ElectronicsClosureSettings(TypedDict):
    source_class: str
    bounding_argument: str
    tiers: Mapping[str, ElectronicsTierSettings]
    architectures: Mapping[str, ElectronicsArchitectureSettings]


class EconomicMarketSettings(TypedDict):
    revenue_musd_per_compute_unit_year: float
    demand_growth_per_year: float
    demand_ceiling_units: float
    space_price_multiplier: float


class DynamicEconomicsSettings(TypedDict):
    source_class: str
    bounding_argument: str
    markets: Mapping[str, EconomicMarketSettings]
    space: Mapping[str, float]
    earth: Mapping[str, float]


class RedundancySettings(TypedDict):
    all_sector_multiplier: NotRequired[float]
    sectors: NotRequired[Mapping[str, float]]


class SourcePortfolioSettings(TypedDict):
    lunar_feed_multiplier: float
    asteroid_feed_multiplier: float
    capacity_sectors: Mapping[str, float]


class RobustSeedDesignSettings(TypedDict):
    source_class: str
    bounding_argument: str
    routes: Mapping[str, Mapping[str, float]]
    redundancy: Mapping[str, RedundancySettings]
    source_portfolios: Mapping[str, SourcePortfolioSettings]


class SeedLinearProgram(TypedDict):
    c: FloatArray
    objective_vectors: Mapping[str, FloatArray]
    A_ub: FloatArray
    b_ub: FloatArray
    bounds: list[tuple[float | None, float | None]]
    labels: list[str]
    iz: slice
    ip_l: int
    ip_a: int
    iv: slice
    nv: int
    mass_per_capacity: FloatArray


@dataclass(frozen=True)
class IntegratedParams:
    version: str
    elements: tuple[str, ...]
    sectors: tuple[str, ...]
    q: FloatArray
    delta: FloatArray
    min_seed: FloatArray
    lag: FloatArray
    ramp: FloatArray
    gravity_required: FloatArray
    centrifuge_radius: FloatArray
    base_coverage: FloatArray
    coverage_ceiling: FloatArray
    coverage_response: FloatArray
    intervention_hours: FloatArray
    B: FloatArray
    A: FloatArray
    lunar_yield: FloatArray
    asteroid_yield: FloatArray
    processing: Mapping[str, float]
    environment: EnvironmentSettings
    scenarios: Mapping[str, ScenarioSettings]
    seed: SeedSettings
    intelligence: IntelligenceSettings
    transfer_arcs: TransferArcsSettings
    earth_compute: EarthComputeSettings
    debris: DebrisSettings
    knowledge_autonomy: KnowledgeAutonomySettings
    process_environment_profiles: Mapping[str, ProcessEnvironmentProfileSettings]
    embodiment_compatibility: EmbodimentCompatibilitySettings
    embodiment_bom: EmbodimentBOMConfig
    deployment: DeploymentSettings
    orbital_mass_and_shell_debris: OrbitalMassSettings
    electronics_closure: ElectronicsClosureSettings
    dynamic_economics: DynamicEconomicsSettings
    robust_seed_design_space: RobustSeedDesignSettings
    intelligence_marginal_response: IntelligenceMarginalResponseConfig
    bottleneck_upgrade_projects: BottleneckUpgradeConfig
    compute_demand_allocation: ComputeDemandConfig
    digital_improvement: DigitalImprovementConfig
    chronological_release_backtest: ChronologicalReleaseBacktestConfig
    milestone_order_branches: MilestoneOrderConfig
    authorized_capacity_control: AuthorizedCapacityControlConfig
    ai_rd_compute_allocation: ComputeAllocationConfig
    cognitive_physical_labor: CognitivePhysicalLaborConfig
    ai_electronics_supply_chain: ElectronicsSupplyChainConfig
    compute_cohort_obsolescence: ComputeCohortConfig
    verification_hierarchy: VerificationHierarchyConfig
    industrial_reliability_ladder: IndustrialReliabilityConfig
    data_evaluator_coevolution: DataEvaluatorCoevolutionConfig
    replication_governance_externalities: ReplicationGovernanceConfig
    data_advantage: DataAdvantageConfig
    intergenerational_learning_rehearsal: IntergenerationalLearningConfig
    coordination_model: CoordinationConfig
    partial_closure_support: PartialClosureSupportConfig
    orbital_lifecycle: OrbitalLifecycleConfig
    orbital_transport_service: OrbitalTransportConfig
    orbital_service_strategy: OrbitalServiceStrategyConfig
    orbital_control: OrbitalControlConfig
    orbital_resilience_strategy: OrbitalResilienceConfig
    uncertainty: Mapping[str, tuple[float, float]]

    def __post_init__(self) -> None:
        n, m = self.n, self.m
        sector_vectors = {
            "q": self.q,
            "delta": self.delta,
            "min_seed": self.min_seed,
            "lag": self.lag,
            "ramp": self.ramp,
            "gravity_required": self.gravity_required,
            "centrifuge_radius": self.centrifuge_radius,
            "base_coverage": self.base_coverage,
            "coverage_ceiling": self.coverage_ceiling,
            "coverage_response": self.coverage_response,
            "intervention_hours": self.intervention_hours,
        }
        for name, vector in sector_vectors.items():
            validate_shape(vector, (n,), name=f"IntegratedParams.{name}")
        validate_shape(self.B, (m, n), name="IntegratedParams.B")
        validate_shape(self.A, (n, n), name="IntegratedParams.A")
        validate_shape(self.lunar_yield, (m,), name="IntegratedParams.lunar_yield")
        validate_shape(self.asteroid_yield, (m,), name="IntegratedParams.asteroid_yield")

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
    embodiment_portfolio: str
    embodiment_task_pass: tuple[tuple[str, bool, tuple[str, ...]], ...]
    coverage: FloatArray
    q_effective: FloatArray
    B_effective: FloatArray
    centrifuge_rpm: FloatArray
    centrifuge_mass_t: FloatArray
    intervention_hours_per_year: FloatArray
    named_task_completion_rate: FloatArray
    fault_diagnosis_fraction: FloatArray
    verification_throughput_per_year: FloatArray
    engineering_cycle_years: FloatArray
    process_yield: FloatArray
    repair_success_fraction: FloatArray
    mean_time_to_recovery_days: FloatArray
    stop_line_task_pass: BoolArray
    environment_throughput_multiplier: FloatArray
    environment_yield_multiplier: FloatArray
    environment_depreciation_multiplier: FloatArray
    environment_power_demand_multiplier: FloatArray

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
    capacities: FloatArray
    import_stock_t: FloatArray
    lunar_feed_t_per_year: float
    asteroid_feed_t_per_year: float
    minimum_task_coverage: float
    intervention_hours_per_year: float
    binding_constraints: tuple[tuple[str, float], ...]
    process: ProcessProfile

    def capacity(self, params: IntegratedParams, sector: str) -> float:
        return float(self.capacities[params.sector_idx(sector)])

    def required_masses(self) -> tuple[float, float, float]:
        """Return feasible total, physical, and import masses.

        Infeasible solver results intentionally carry missing mass fields. A
        feasible result without all three fields is an internal model
        invariant violation rather than a zero-mass case.
        """
        if (
            not self.feasible
            or self.total_seed_mass_t is None
            or self.physical_seed_mass_t is None
            or self.import_stock_mass_t is None
        ):
            raise RuntimeError("seed mass fields require a feasible seed result")
        return (
            self.total_seed_mass_t,
            self.physical_seed_mass_t,
            self.import_stock_mass_t,
        )


@dataclass(frozen=True)
class CapacityGrowthResult:
    scenario: str
    t: FloatArray
    installed_sector_capacity: FloatArray
    operating_sector_capacity: FloatArray
    ordered_sector_capacity: FloatArray
    installed_cells: FloatArray
    operating_cells: FloatArray
    intelligence: FloatArray
    verified_loop_throughput: FloatArray
    intelligence_marginal_gain_per_loop: FloatArray
    local_compute: FloatArray
    inventory_t: FloatArray
    ordered_cells: FloatArray
    aggregate_doubling_year: float | None
    survived: bool
    limiting_elements: tuple[tuple[str, int], ...]
    lunar_material_t: float
    asteroid_material_t: float
    recycled_material_t: float
    failed_sector_capacity: FloatArray
    repaired_sector_capacity: FloatArray
    commissioned_sector_capacity: FloatArray
    activated_sector_capacity: FloatArray
    shock_loss_sector_capacity: FloatArray
    allocation_policy: str
    repair_enabled: bool
    primary_constraint: tuple[str, ...]
    intervention_demand_hours: FloatArray
    verification_demand_units: FloatArray


@dataclass(frozen=True)
class ComputeComparison:
    t: FloatArray
    endogenous: FloatArray
    endogenous_orbit: FloatArray
    terrestrial: dict[str, FloatArray]
    earth_fed_orbit: dict[str, FloatArray]


@dataclass(frozen=True)
class DebrisResult:
    label: str
    t: FloatArray
    active: FloatArray
    derelict: FloatArray
    fragments: FloatArray
    fragments_created: FloatArray
    fragments_cleared: FloatArray
    creation_clearance_ratio: float
    subcritical: bool


@dataclass(frozen=True)
class ShellDebrisResult:
    t: FloatArray
    shells: tuple[str, ...]
    active_capacity: FloatArray
    intact_derelicts: FloatArray
    trackable_fragments: FloatArray
    untrackable_fragments: FloatArray
    uncaptured_reservoir_t: FloatArray
    feed_inventory_t: FloatArray
    accessible_orbital_mass_t: FloatArray
    earth_imported_t: FloatArray
    captured_t: FloatArray
    recovered_t: FloatArray
    unrecoverable_loss_t: FloatArray
    requested_deployment_units: FloatArray
    served_deployment_units: FloatArray
    deployment_shortfall_units: FloatArray
    branching_ratio_by_shell: FloatArray
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
        low, median, high = np.percentile(np.asarray(values), [10, 50, 90])
        return float(low), float(median), float(high)


@dataclass(frozen=True)
class SeedDeploymentResult:
    scenario: str
    t: FloatArray
    delivered_core_t: FloatArray
    staged_core_t: FloatArray
    installed_core_t: FloatArray
    commissioned_core_t: FloatArray
    operating_core_t: FloatArray
    recovery_backlog_t: FloatArray
    spares_remaining_t: FloatArray
    installed_seed_mass_t: float
    delivered_seed_mass_t: float
    logistics_mass_t: float
    startup_energy_mwh: float
    first_operating_year: float | None
    full_operating_seed_year: float | None
    recovered_startup_failure_t: float
    success: bool


def _vector(
    names: tuple[str, ...],
    values: Mapping[str, float],
    label: str,
) -> FloatArray:
    unknown = set(values) - set(names)
    if unknown:
        raise ValueError(f"{label}: unknown names: {sorted(unknown)}")
    return np.array([float(values.get(name, 0.0)) for name in names], dtype=float)


def _field_mapping(
    mapping: Mapping[str, object],
    key: str,
    *,
    label: str,
) -> dict[str, object]:
    return require_mapping(mapping.get(key), label=f"{label}.{key}")


def _field_number(
    mapping: Mapping[str, object],
    key: str,
    *,
    label: str,
) -> float:
    return require_number(mapping.get(key), label=f"{label}.{key}")


def _field_string(
    mapping: Mapping[str, object],
    key: str,
    *,
    label: str,
) -> str:
    return require_string(mapping.get(key), label=f"{label}.{key}")


def _field_bool(
    mapping: Mapping[str, object],
    key: str,
    *,
    label: str,
) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise ValueError(f"{label}.{key}: expected a boolean")
    return value


def _number_mapping(value: object, *, label: str) -> dict[str, float]:
    mapping = require_mapping(value, label=label)
    return {
        key: require_number(raw_value, label=f"{label}.{key}") for key, raw_value in mapping.items()
    }


def _scenario_settings(value: object, *, label: str) -> ScenarioSettings:
    mapping = require_mapping(value, label=label)
    return ScenarioSettings(
        description=_field_string(mapping, "description", label=label),
        horizon_years=_field_number(mapping, "horizon_years", label=label),
        asteroid_enabled=_field_bool(mapping, "asteroid_enabled", label=label),
        asteroid_commission_year=_field_number(
            mapping,
            "asteroid_commission_year",
            label=label,
        ),
        ai_level=_field_number(mapping, "ai_level", label=label),
        minimum_task_coverage=_field_number(
            mapping,
            "minimum_task_coverage",
            label=label,
        ),
        remote_intervention_budget_hours_per_year=_field_number(
            mapping,
            "remote_intervention_budget_hours_per_year",
            label=label,
        ),
        viable_floor_multiplier=_field_number(
            mapping,
            "viable_floor_multiplier",
            label=label,
        ),
        environment_profile=_field_string(
            mapping,
            "environment_profile",
            label=label,
        ),
        earth_import_cutoff_year=_field_number(
            mapping,
            "earth_import_cutoff_year",
            label=label,
        ),
        earth_import_caps_t=_number_mapping(
            mapping.get("earth_import_caps_t"),
            label=f"{label}.earth_import_caps_t",
        ),
    )


def _sector_settings(value: object, *, label: str) -> SectorSettings:
    mapping = require_mapping(value, label=label)
    numeric_keys = (
        "q_per_capacity_year",
        "depreciation_per_year",
        "min_seed_capacity",
        "commissioning_lag_years",
        "yield_ramp_years",
        "gravity_required_g",
        "centrifuge_radius_m",
        "base_task_coverage",
        "autonomy_ceiling",
        "autonomy_response",
        "intervention_hours_per_capacity_year",
    )
    numbers = {key: _field_number(mapping, key, label=label) for key in numeric_keys}
    return SectorSettings(
        name=_field_string(mapping, "name", label=label),
        q_per_capacity_year=numbers["q_per_capacity_year"],
        depreciation_per_year=numbers["depreciation_per_year"],
        min_seed_capacity=numbers["min_seed_capacity"],
        commissioning_lag_years=numbers["commissioning_lag_years"],
        yield_ramp_years=numbers["yield_ramp_years"],
        gravity_required_g=numbers["gravity_required_g"],
        centrifuge_radius_m=numbers["centrifuge_radius_m"],
        base_task_coverage=numbers["base_task_coverage"],
        autonomy_ceiling=numbers["autonomy_ceiling"],
        autonomy_response=numbers["autonomy_response"],
        intervention_hours_per_capacity_year=numbers["intervention_hours_per_capacity_year"],
        bom_t=_number_mapping(mapping.get("bom_t", {}), label=f"{label}.bom_t"),
        recipe_additions=_number_mapping(
            mapping.get("recipe_additions", {}),
            label=f"{label}.recipe_additions",
        ),
    )


def _seed_settings(value: object, *, label: str) -> SeedSettings:
    mapping = require_mapping(value, label=label)
    return SeedSettings(
        fixed_digital_seed_mass_t=_field_number(
            mapping,
            "fixed_digital_seed_mass_t",
            label=label,
        ),
        maximum_gross_cell_orders_per_operating_cell_year=_field_number(
            mapping,
            "maximum_gross_cell_orders_per_operating_cell_year",
            label=label,
        ),
        minimum_viable_cell_equivalents=_field_number(
            mapping,
            "minimum_viable_cell_equivalents",
            label=label,
        ),
        recycling_recovery_fraction=_field_number(
            mapping,
            "recycling_recovery_fraction",
            label=label,
        ),
        repairable_failure_fraction=_field_number(
            mapping,
            "repairable_failure_fraction",
            label=label,
        ),
        repair_parts_fraction_of_bom=_field_number(
            mapping,
            "repair_parts_fraction_of_bom",
            label=label,
        ),
        repair_service_per_capacity=_field_number(
            mapping,
            "repair_service_per_capacity",
            label=label,
        ),
        repair_intervention_hours_per_capacity=_field_number(
            mapping,
            "repair_intervention_hours_per_capacity",
            label=label,
        ),
        repair_lag_years=_field_number(mapping, "repair_lag_years", label=label),
    )


def _intelligence_settings(value: object, *, label: str) -> IntelligenceSettings:
    mapping = require_mapping(value, label=label)
    return IntelligenceSettings(
        initial_level=_field_number(mapping, "initial_level", label=label),
        verification_factor=_field_number(
            mapping,
            "verification_factor",
            label=label,
        ),
        gain_scale_per_verified_loop=_field_number(
            mapping,
            "gain_scale_per_verified_loop",
            label=label,
        ),
        frontier_gap_exponent=_field_number(
            mapping,
            "frontier_gap_exponent",
            label=label,
        ),
        productivity_elasticity=_field_number(
            mapping,
            "productivity_elasticity",
            label=label,
        ),
        autonomy_learning_multiplier=_field_number(
            mapping,
            "autonomy_learning_multiplier",
            label=label,
        ),
        maximum_level=_field_number(mapping, "maximum_level", label=label),
        compute_units_per_compute_capacity=_field_number(
            mapping,
            "compute_units_per_compute_capacity",
            label=label,
        ),
        effective_compute_factors=_number_mapping(
            mapping.get("effective_compute_factors"),
            label=f"{label}.effective_compute_factors",
        ),
        verified_loop_stage_rates_per_year=_number_mapping(
            mapping.get("verified_loop_stage_rates_per_year"),
            label=f"{label}.verified_loop_stage_rates_per_year",
        ),
    )


def _transfer_arc_settings(value: object, *, label: str) -> TransferArcSettings:
    mapping = require_mapping(value, label=label)
    result = TransferArcSettings(
        cargo_class=_field_string(mapping, "cargo_class", label=label),
        lag_years=_field_number(mapping, "lag_years", label=label),
    )
    for key in (
        "share_of_new_endogenous_compute",
        "normalized_compute_units_per_transport_capacity_year",
    ):
        if key in mapping:
            result[key] = require_number(mapping[key], label=f"{label}.{key}")
    return result


def _earth_compute_settings(value: object, *, label: str) -> EarthComputeSettings:
    mapping = require_mapping(value, label=label)
    cases: dict[str, EarthComputeCase] = {}
    for name, raw_case in mapping.items():
        if name == "depreciation_per_year":
            continue
        case = require_mapping(raw_case, label=f"{label}.{name}")
        cases[name] = EarthComputeCase(
            terrestrial_build_units_per_year=_field_number(
                case,
                "terrestrial_build_units_per_year",
                label=f"{label}.{name}",
            ),
            earth_to_orbit_build_units_per_year=_field_number(
                case,
                "earth_to_orbit_build_units_per_year",
                label=f"{label}.{name}",
            ),
            launch_units_per_year=_field_number(
                case,
                "launch_units_per_year",
                label=f"{label}.{name}",
            ),
            terrestrial_site_ceiling_units=_field_number(
                case,
                "terrestrial_site_ceiling_units",
                label=f"{label}.{name}",
            ),
        )
    if not cases:
        raise ValueError(f"{label}: at least one counterfactual case is required")
    return EarthComputeSettings(
        cases=cases,
        depreciation_per_year=_field_number(
            mapping,
            "depreciation_per_year",
            label=label,
        ),
    )


def _debris_settings(value: object, *, label: str) -> DebrisSettings:
    mapping = require_mapping(value, label=label)
    raw_scenarios = _field_mapping(mapping, "scenarios", label=label)
    scenarios: dict[str, DebrisMitigationSettings] = {}
    for name, raw_scenario in raw_scenarios.items():
        scenario = require_mapping(raw_scenario, label=f"{label}.scenarios.{name}")
        parsed = DebrisMitigationSettings(
            controlled_disposal_fraction=_field_number(
                scenario,
                "controlled_disposal_fraction",
                label=f"{label}.scenarios.{name}",
            ),
            active_removal_fragment_index_per_year=_field_number(
                scenario,
                "active_removal_fragment_index_per_year",
                label=f"{label}.scenarios.{name}",
            ),
            retrieval_fraction_per_year=_field_number(
                scenario,
                "retrieval_fraction_per_year",
                label=f"{label}.scenarios.{name}",
            ),
        )
        if "collision_kernel_multiplier" in scenario:
            parsed["collision_kernel_multiplier"] = require_number(
                scenario["collision_kernel_multiplier"],
                label=f"{label}.scenarios.{name}.collision_kernel_multiplier",
            )
        scenarios[name] = parsed
    numeric_keys = (
        "initial_active_units",
        "initial_derelict_units",
        "initial_fragment_index",
        "asset_failure_per_year",
        "collision_kernel",
        "fragment_hazard_multiplier",
        "fragments_per_collision_index",
        "natural_fragment_clearance_per_year",
        "derelict_collision_clearance_fraction",
    )
    numbers = {key: _field_number(mapping, key, label=label) for key in numeric_keys}
    return DebrisSettings(**numbers, scenarios=scenarios)


def _knowledge_settings(value: object, *, label: str) -> KnowledgeAutonomySettings:
    mapping = require_mapping(value, label=label)
    numeric_keys = (
        "fault_diagnosis_scale",
        "verification_throughput_per_service_unit",
        "verification_units_per_new_capacity",
        "engineering_cycle_base_years",
        "engineering_cycle_response",
        "process_yield_floor",
        "repair_success_scale",
        "mttr_days_at_zero_coverage",
        "mttr_days_floor",
        "stop_line_threshold_below_declared_coverage",
        "compute_units_per_cell_order_year",
    )
    numbers = {key: _field_number(mapping, key, label=label) for key in numeric_keys}
    return KnowledgeAutonomySettings(
        source_class=_field_string(mapping, "source_class", label=label),
        bounding_argument=_field_string(mapping, "bounding_argument", label=label),
        knowledge_package_t=_number_mapping(
            mapping.get("knowledge_package_t"),
            label=f"{label}.knowledge_package_t",
        ),
        **numbers,
    )


def _process_environment_profiles(
    value: object,
    *,
    label: str,
) -> dict[str, ProcessEnvironmentProfileSettings]:
    mapping = require_mapping(value, label=label)
    profiles: dict[str, ProcessEnvironmentProfileSettings] = {}
    for profile_name, raw_profile in mapping.items():
        profile_label = f"{label}.{profile_name}"
        profile = require_mapping(raw_profile, label=profile_label)
        raw_effects = _field_mapping(profile, "effects", label=profile_label)
        effects: dict[str, ProcessEnvironmentEffect] = {}
        for sector, raw_effect in raw_effects.items():
            effect_label = f"{profile_label}.effects.{sector}"
            effect = require_mapping(raw_effect, label=effect_label)
            effects[sector] = ProcessEnvironmentEffect(
                mechanism=_field_string(effect, "mechanism", label=effect_label),
                throughput_multiplier=_field_number(
                    effect,
                    "throughput_multiplier",
                    label=effect_label,
                ),
                yield_multiplier=_field_number(
                    effect,
                    "yield_multiplier",
                    label=effect_label,
                ),
                depreciation_multiplier=_field_number(
                    effect,
                    "depreciation_multiplier",
                    label=effect_label,
                ),
                power_demand_multiplier=_field_number(
                    effect,
                    "power_demand_multiplier",
                    label=effect_label,
                ),
            )
        profiles[profile_name] = ProcessEnvironmentProfileSettings(
            source_class=_field_string(
                profile,
                "source_class",
                label=profile_label,
            ),
            note=_field_string(profile, "note", label=profile_label),
            effects=effects,
        )
    return profiles


def _embodiment_settings(
    value: object,
    *,
    label: str,
) -> EmbodimentCompatibilitySettings:
    mapping = require_mapping(value, label=label)
    dimensions = tuple(
        require_string(raw, label=f"{label}.dimensions[{index}]")
        for index, raw in enumerate(
            require_sequence(mapping.get("dimensions"), label=f"{label}.dimensions")
        )
    )
    raw_portfolios = _field_mapping(mapping, "portfolios", label=label)
    portfolios = {
        name: _number_mapping(raw, label=f"{label}.portfolios.{name}")
        for name, raw in raw_portfolios.items()
    }
    raw_tasks = _field_mapping(mapping, "tasks", label=label)
    tasks: dict[str, EmbodimentTaskSettings] = {}
    for name, raw_task in raw_tasks.items():
        task_label = f"{label}.tasks.{name}"
        task = require_mapping(raw_task, label=task_label)
        tasks[name] = EmbodimentTaskSettings(
            sector=_field_string(task, "sector", label=task_label),
            requirements=_number_mapping(
                task.get("requirements"),
                label=f"{task_label}.requirements",
            ),
            intelligence_onset=_field_number(
                task,
                "intelligence_onset",
                label=task_label,
            ),
            intelligence_scale=_field_number(
                task,
                "intelligence_scale",
                label=task_label,
            ),
            required_score=_field_number(
                task,
                "required_score",
                label=task_label,
            ),
        )
    defaults_raw = _field_mapping(
        mapping,
        "default_portfolio_by_scenario",
        label=label,
    )
    defaults = {
        name: require_string(raw, label=f"{label}.default_portfolio_by_scenario.{name}")
        for name, raw in defaults_raw.items()
    }
    sweeps_raw = _field_mapping(mapping, "validation_sweeps", label=label)
    intelligence_levels = tuple(
        require_number(raw, label=f"{label}.validation_sweeps.intelligence_levels[{index}]")
        for index, raw in enumerate(
            require_sequence(
                sweeps_raw.get("intelligence_levels"),
                label=f"{label}.validation_sweeps.intelligence_levels",
            )
        )
    )
    quality_multipliers = tuple(
        require_number(
            raw,
            label=f"{label}.validation_sweeps.embodiment_quality_multipliers[{index}]",
        )
        for index, raw in enumerate(
            require_sequence(
                sweeps_raw.get("embodiment_quality_multipliers"),
                label=f"{label}.validation_sweeps.embodiment_quality_multipliers",
            )
        )
    )
    validation_sweeps = EmbodimentValidationSweeps(
        fixed_embodiment_portfolio=_field_string(
            sweeps_raw,
            "fixed_embodiment_portfolio",
            label=f"{label}.validation_sweeps",
        ),
        intelligence_levels=intelligence_levels,
        fixed_intelligence_level=_field_number(
            sweeps_raw,
            "fixed_intelligence_level",
            label=f"{label}.validation_sweeps",
        ),
        embodiment_quality_multipliers=quality_multipliers,
    )
    fault_rows = _field_mapping(
        mapping,
        "terrestrial_rehearsal_faults",
        label=label,
    )
    faults = {
        name: _number_mapping(raw, label=f"{label}.terrestrial_rehearsal_faults.{name}")
        for name, raw in fault_rows.items()
    }
    return EmbodimentCompatibilitySettings(
        source_class=_field_string(mapping, "source_class", label=label),
        bounding_argument=_field_string(mapping, "bounding_argument", label=label),
        dimensions=dimensions,
        portfolios=portfolios,
        tasks=tasks,
        default_portfolio_by_scenario=defaults,
        validation_sweeps=validation_sweeps,
        terrestrial_rehearsal_faults=faults,
    )


def _deployment_settings(value: object, *, label: str) -> DeploymentSettings:
    mapping = require_mapping(value, label=label)
    return DeploymentSettings(
        source_class=_field_string(mapping, "source_class", label=label),
        bounding_argument=_field_string(mapping, "bounding_argument", label=label),
        transport_packaging_fraction=_field_number(
            mapping,
            "transport_packaging_fraction",
            label=label,
        ),
        initial_spares_fraction=_field_number(
            mapping,
            "initial_spares_fraction",
            label=label,
        ),
        unloading_equipment_mass_t=_field_number(
            mapping,
            "unloading_equipment_mass_t",
            label=label,
        ),
        site_work_equipment_mass_t=_field_number(
            mapping,
            "site_work_equipment_mass_t",
            label=label,
        ),
        calibration_standards_mass_t=_field_number(
            mapping,
            "calibration_standards_mass_t",
            label=label,
        ),
        startup_energy_mwh_per_seed_t=_field_number(
            mapping,
            "startup_energy_mwh_per_seed_t",
            label=label,
        ),
        startup_storage_t_per_mwh=_field_number(
            mapping,
            "startup_storage_t_per_mwh",
            label=label,
        ),
        unloading_rate_t_per_year=_field_number(
            mapping,
            "unloading_rate_t_per_year",
            label=label,
        ),
        site_ready_year=_field_number(mapping, "site_ready_year", label=label),
        initial_power_ready_year=_field_number(
            mapping,
            "initial_power_ready_year",
            label=label,
        ),
        installation_rate_t_per_year=_field_number(
            mapping,
            "installation_rate_t_per_year",
            label=label,
        ),
        commissioning_rate_t_per_year=_field_number(
            mapping,
            "commissioning_rate_t_per_year",
            label=label,
        ),
        startup_failure_fraction=_field_number(
            mapping,
            "startup_failure_fraction",
            label=label,
        ),
        recovery_rate_t_per_year=_field_number(
            mapping,
            "recovery_rate_t_per_year",
            label=label,
        ),
        recovery_spares_t_per_failed_t=_field_number(
            mapping,
            "recovery_spares_t_per_failed_t",
            label=label,
        ),
    )


def _orbital_mass_settings(value: object, *, label: str) -> OrbitalMassSettings:
    mapping = require_mapping(value, label=label)
    raw_shells = require_sequence(mapping.get("shells"), label=f"{label}.shells")
    shells: list[OrbitalShellSettings] = []
    for index, raw_shell in enumerate(raw_shells):
        shell_label = f"{label}.shells[{index}]"
        shell = require_mapping(raw_shell, label=shell_label)
        shells.append(
            OrbitalShellSettings(
                name=_field_string(shell, "name", label=shell_label),
                deployment_share=_field_number(
                    shell,
                    "deployment_share",
                    label=shell_label,
                ),
                volume_index=_field_number(shell, "volume_index", label=shell_label),
                collision_kernel=_field_number(
                    shell,
                    "collision_kernel",
                    label=shell_label,
                ),
                natural_trackable_clearance_per_year=_field_number(
                    shell,
                    "natural_trackable_clearance_per_year",
                    label=shell_label,
                ),
                natural_untrackable_clearance_per_year=_field_number(
                    shell,
                    "natural_untrackable_clearance_per_year",
                    label=shell_label,
                ),
                active_removal_trackable_per_year=_field_number(
                    shell,
                    "active_removal_trackable_per_year",
                    label=shell_label,
                ),
            )
        )
    raw_transfer = require_sequence(
        mapping.get("cross_shell_transfer"),
        label=f"{label}.cross_shell_transfer",
    )
    transfer_rows: list[list[float]] = []
    for row_index, raw_row in enumerate(raw_transfer):
        row = require_sequence(
            raw_row,
            label=f"{label}.cross_shell_transfer[{row_index}]",
        )
        transfer_rows.append(
            [
                require_number(
                    cell,
                    label=f"{label}.cross_shell_transfer[{row_index}][{column_index}]",
                )
                for column_index, cell in enumerate(row)
            ]
        )
    numeric_keys = (
        "initial_uncaptured_reservoir_t",
        "initial_feed_inventory_t",
        "earth_import_t_per_year",
        "earth_import_cutoff_year",
        "capture_fraction_of_reservoir_per_year",
        "mass_t_per_capacity_unit",
        "recovery_fraction_of_controlled_retirement",
        "replacement_delivery_cost_per_kg",
        "asset_failure_per_year",
        "controlled_disposal_fraction",
        "retrieval_fraction_per_year",
        "trackable_fragments_per_collision",
        "untrackable_fragments_per_collision",
        "fragment_hazard_weight_trackable",
        "fragment_hazard_weight_untrackable",
        "avoidance_saturation_threshold",
        "avoidance_saturation_slope",
    )
    numbers = {key: _field_number(mapping, key, label=label) for key in numeric_keys}
    return OrbitalMassSettings(
        source_class=_field_string(mapping, "source_class", label=label),
        bounding_argument=_field_string(mapping, "bounding_argument", label=label),
        initial_uncaptured_reservoir_t=numbers["initial_uncaptured_reservoir_t"],
        initial_feed_inventory_t=numbers["initial_feed_inventory_t"],
        earth_import_t_per_year=numbers["earth_import_t_per_year"],
        earth_import_cutoff_year=numbers["earth_import_cutoff_year"],
        capture_fraction_of_reservoir_per_year=numbers["capture_fraction_of_reservoir_per_year"],
        mass_t_per_capacity_unit=numbers["mass_t_per_capacity_unit"],
        recovery_fraction_of_controlled_retirement=numbers[
            "recovery_fraction_of_controlled_retirement"
        ],
        replacement_delivery_cost_per_kg=numbers["replacement_delivery_cost_per_kg"],
        asset_failure_per_year=numbers["asset_failure_per_year"],
        controlled_disposal_fraction=numbers["controlled_disposal_fraction"],
        retrieval_fraction_per_year=numbers["retrieval_fraction_per_year"],
        trackable_fragments_per_collision=numbers["trackable_fragments_per_collision"],
        untrackable_fragments_per_collision=numbers["untrackable_fragments_per_collision"],
        fragment_hazard_weight_trackable=numbers["fragment_hazard_weight_trackable"],
        fragment_hazard_weight_untrackable=numbers["fragment_hazard_weight_untrackable"],
        avoidance_saturation_threshold=numbers["avoidance_saturation_threshold"],
        avoidance_saturation_slope=numbers["avoidance_saturation_slope"],
        shells=tuple(shells),
        cross_shell_transfer=np.asarray(transfer_rows, dtype=float),
    )


def _electronics_closure_settings(
    value: object,
    *,
    label: str,
) -> ElectronicsClosureSettings:
    mapping = require_mapping(value, label=label)
    raw_tiers = _field_mapping(mapping, "tiers", label=label)
    tiers: dict[str, ElectronicsTierSettings] = {}
    for name, raw_tier in raw_tiers.items():
        tier_label = f"{label}.tiers.{name}"
        tier = require_mapping(raw_tier, label=tier_label)
        tiers[name] = ElectronicsTierSettings(
            local_producibility_fraction=_field_number(
                tier,
                "local_producibility_fraction",
                label=tier_label,
            ),
            shelf_life_years=_field_number(
                tier,
                "shelf_life_years",
                label=tier_label,
            ),
            obsolescence_per_year=_field_number(
                tier,
                "obsolescence_per_year",
                label=tier_label,
            ),
            substitution_route=_field_string(
                tier,
                "substitution_route",
                label=tier_label,
            ),
            measurement_priority=_field_string(
                tier,
                "measurement_priority",
                label=tier_label,
            ),
        )
    raw_architectures = _field_mapping(mapping, "architectures", label=label)
    architectures: dict[str, ElectronicsArchitectureSettings] = {}
    for name, raw_architecture in raw_architectures.items():
        architecture_label = f"{label}.architectures.{name}"
        architecture = require_mapping(raw_architecture, label=architecture_label)
        architectures[name] = ElectronicsArchitectureSettings(
            annual_import_fraction_of_initial_capacity=_field_number(
                architecture,
                "annual_import_fraction_of_initial_capacity",
                label=architecture_label,
            ),
            initial_import_inventory_fraction=_field_number(
                architecture,
                "initial_import_inventory_fraction",
                label=architecture_label,
            ),
            local_producibility_multiplier=_field_number(
                architecture,
                "local_producibility_multiplier",
                label=architecture_label,
            ),
            cannibalization_fraction=_field_number(
                architecture,
                "cannibalization_fraction",
                label=architecture_label,
            ),
            mature_substitution_credit_fraction=_field_number(
                architecture,
                "mature_substitution_credit_fraction",
                label=architecture_label,
            ),
        )
    return ElectronicsClosureSettings(
        source_class=_field_string(mapping, "source_class", label=label),
        bounding_argument=_field_string(mapping, "bounding_argument", label=label),
        tiers=tiers,
        architectures=architectures,
    )


def _dynamic_economics_settings(
    value: object,
    *,
    label: str,
) -> DynamicEconomicsSettings:
    mapping = require_mapping(value, label=label)
    raw_markets = _field_mapping(mapping, "markets", label=label)
    markets: dict[str, EconomicMarketSettings] = {}
    for name, raw_market in raw_markets.items():
        market_label = f"{label}.markets.{name}"
        market = require_mapping(raw_market, label=market_label)
        markets[name] = EconomicMarketSettings(
            revenue_musd_per_compute_unit_year=_field_number(
                market,
                "revenue_musd_per_compute_unit_year",
                label=market_label,
            ),
            demand_growth_per_year=_field_number(
                market,
                "demand_growth_per_year",
                label=market_label,
            ),
            demand_ceiling_units=_field_number(
                market,
                "demand_ceiling_units",
                label=market_label,
            ),
            space_price_multiplier=_field_number(
                market,
                "space_price_multiplier",
                label=market_label,
            ),
        )
    return DynamicEconomicsSettings(
        source_class=_field_string(mapping, "source_class", label=label),
        bounding_argument=_field_string(mapping, "bounding_argument", label=label),
        markets=markets,
        space=_number_mapping(mapping.get("space"), label=f"{label}.space"),
        earth=_number_mapping(mapping.get("earth"), label=f"{label}.earth"),
    )


def _robust_seed_design_settings(
    value: object,
    *,
    label: str,
) -> RobustSeedDesignSettings:
    mapping = require_mapping(value, label=label)
    raw_routes = _field_mapping(mapping, "routes", label=label)
    routes = {
        name: _number_mapping(raw_route, label=f"{label}.routes.{name}")
        for name, raw_route in raw_routes.items()
    }
    raw_redundancy = _field_mapping(mapping, "redundancy", label=label)
    redundancy: dict[str, RedundancySettings] = {}
    for name, raw_entry in raw_redundancy.items():
        entry_label = f"{label}.redundancy.{name}"
        entry = require_mapping(raw_entry, label=entry_label)
        parsed = RedundancySettings()
        if "all_sector_multiplier" in entry:
            parsed["all_sector_multiplier"] = require_number(
                entry["all_sector_multiplier"],
                label=f"{entry_label}.all_sector_multiplier",
            )
        if "sectors" in entry:
            parsed["sectors"] = _number_mapping(
                entry["sectors"],
                label=f"{entry_label}.sectors",
            )
        redundancy[name] = parsed
    raw_sources = _field_mapping(mapping, "source_portfolios", label=label)
    sources: dict[str, SourcePortfolioSettings] = {}
    for name, raw_source in raw_sources.items():
        source_label = f"{label}.source_portfolios.{name}"
        source = require_mapping(raw_source, label=source_label)
        sources[name] = SourcePortfolioSettings(
            lunar_feed_multiplier=_field_number(
                source,
                "lunar_feed_multiplier",
                label=source_label,
            ),
            asteroid_feed_multiplier=_field_number(
                source,
                "asteroid_feed_multiplier",
                label=source_label,
            ),
            capacity_sectors=_number_mapping(
                source.get("capacity_sectors"),
                label=f"{source_label}.capacity_sectors",
            ),
        )
    return RobustSeedDesignSettings(
        source_class=_field_string(mapping, "source_class", label=label),
        bounding_argument=_field_string(mapping, "bounding_argument", label=label),
        routes=routes,
        redundancy=redundancy,
        source_portfolios=sources,
    )


def load_integrated_params(path: Path | None = None) -> IntegratedParams:
    source = path or PARAMS_PATH
    root = load_yaml_mapping(source)
    elements = tuple(
        require_string(value, label=f"elements[{index}]")
        for index, value in enumerate(require_sequence(root.get("elements"), label="elements"))
    )
    sector_rows = [
        _sector_settings(value, label=f"sectors[{index}]")
        for index, value in enumerate(require_sequence(root.get("sectors"), label="sectors"))
    ]
    sectors = tuple(row["name"] for row in sector_rows)
    if len(set(elements)) != len(elements) or len(set(sectors)) != len(sectors):
        raise ValueError("Current elements and sectors must be unique")

    def arr(key: str) -> FloatArray:
        return np.asarray([row[key] for row in sector_rows], dtype=float)

    B = np.column_stack(
        [_vector(elements, row.get("bom_t", {}), f"bom_t[{row['name']}]") for row in sector_rows]
    )
    base = _vector(
        sectors,
        _number_mapping(root.get("base_service_recipe"), label="base_service_recipe"),
        "base_service_recipe",
    )
    A = np.empty((len(sectors), len(sectors)), dtype=float)
    for j, row in enumerate(sector_rows):
        A[:, j] = base + _vector(
            sectors,
            row.get("recipe_additions", {}),
            f"recipe_additions[{row['name']}]",
        )
    sector_index = {name: index for index, name in enumerate(sectors)}
    q = arr("q_per_capacity_year")
    embodiment_bom = parse_typed_config(
        root.get("embodiment_bom"),
        EmbodimentBOMConfig,
        label="embodiment_bom",
    )
    for item_name, item in embodiment_bom["items"].items():
        producer = item["producer_sector"]
        if producer not in sector_index:
            raise ValueError(f"embodiment_bom[{item_name}]: unknown producer {producer}")
        material_addition = _vector(
            elements,
            item["material_bom_t_per_target_capacity"],
            f"embodiment_bom[{item_name}] material",
        )
        replacement_service = item["replacement_service_units_per_target_capacity_year"]
        if replacement_service < 0.0 or np.any(material_addition < 0.0):
            raise ValueError(f"embodiment_bom[{item_name}] additions must be nonnegative")
        for target in item["target_sectors"]:
            if target not in sector_index:
                raise ValueError(f"embodiment_bom[{item_name}]: unknown target {target}")
            target_index = sector_index[target]
            B[:, target_index] += material_addition
            A[sector_index[producer], target_index] += replacement_service / q[target_index]

    source_yields = _field_mapping(root, "source_yields", label="integrated_model")
    lunar_source = _field_mapping(
        source_yields,
        "lunar_regolith",
        label="source_yields",
    )
    asteroid_source = _field_mapping(
        source_yields,
        "diverse_asteroid_portfolio",
        label="source_yields",
    )
    lunar = _vector(
        elements,
        _number_mapping(
            lunar_source.get("yield_t_per_t_feed"),
            label="source_yields.lunar_regolith.yield_t_per_t_feed",
        ),
        "lunar_regolith yield",
    )
    asteroid = _vector(
        elements,
        _number_mapping(
            asteroid_source.get("yield_t_per_t_feed"),
            label="source_yields.diverse_asteroid_portfolio.yield_t_per_t_feed",
        ),
        "asteroid yield",
    )
    if lunar.sum() > 1.0 + 1e-12 or asteroid.sum() > 1.0 + 1e-12:
        raise ValueError("Recoverable source yields cannot exceed feed mass")
    if np.any(B < 0) or np.any(A < 0):
        raise ValueError("Bills of material and service recipes must be nonnegative")
    if np.any(B.sum(axis=0) <= 0):
        raise ValueError("Every sector needs a nonzero physical bill of material")
    knowledge = _knowledge_settings(
        root.get("knowledge_autonomy"),
        label="knowledge_autonomy",
    )
    seed = _seed_settings(root.get("seed"), label="seed")
    knowledge_mass = sum(knowledge["knowledge_package_t"].values())
    if not math.isclose(
        knowledge_mass,
        seed["fixed_digital_seed_mass_t"],
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        raise ValueError("knowledge package decomposition must sum to fixed digital seed mass")

    uncertainty: dict[str, tuple[float, float]] = {}
    raw_uncertainty = _field_mapping(root, "uncertainty", label="integrated_model")
    for name, raw_bounds in raw_uncertainty.items():
        bounds = require_sequence(raw_bounds, label=f"uncertainty.{name}")
        if len(bounds) != 2:
            raise ValueError(f"uncertainty.{name}: expected [low, high]")
        low = require_number(bounds[0], label=f"uncertainty.{name}[0]")
        high = require_number(bounds[1], label=f"uncertainty.{name}[1]")
        if low > high:
            raise ValueError(f"uncertainty.{name}: low must not exceed high")
        uncertainty[name] = (low, high)
    environment_raw = _field_mapping(root, "environment", label="integrated_model")
    environment = EnvironmentSettings(
        lunar_gravity_g=_field_number(
            environment_raw,
            "lunar_gravity_g",
            label="environment",
        ),
        centrifuge_structural_mass_fraction_at_full_g=_field_number(
            environment_raw,
            "centrifuge_structural_mass_fraction_at_full_g",
            label="environment",
        ),
        centrifuge_parasitic_power_fraction_at_full_g=_field_number(
            environment_raw,
            "centrifuge_parasitic_power_fraction_at_full_g",
            label="environment",
        ),
        centrifuge_overhead_composition=_number_mapping(
            environment_raw.get("centrifuge_overhead_composition"),
            label="environment.centrifuge_overhead_composition",
        ),
    )
    raw_scenarios = _field_mapping(root, "scenarios", label="integrated_model")
    scenarios = {
        name: _scenario_settings(value, label=f"scenarios.{name}")
        for name, value in raw_scenarios.items()
    }
    transfer_raw = _field_mapping(root, "transfer_arcs", label="integrated_model")
    transfer_arcs = TransferArcsSettings(
        earth_to_moon_strategic_materials=_transfer_arc_settings(
            transfer_raw.get("earth_to_moon_strategic_materials"),
            label="transfer_arcs.earth_to_moon_strategic_materials",
        ),
        asteroid_to_moon_feed=_transfer_arc_settings(
            transfer_raw.get("asteroid_to_moon_feed"),
            label="transfer_arcs.asteroid_to_moon_feed",
        ),
        moon_to_orbit_compute=_transfer_arc_settings(
            transfer_raw.get("moon_to_orbit_compute"),
            label="transfer_arcs.moon_to_orbit_compute",
        ),
    )
    return IntegratedParams(
        version=_field_string(root, "version", label="integrated_model"),
        elements=elements,
        sectors=sectors,
        q=q,
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
        processing=_number_mapping(root.get("processing"), label="processing"),
        environment=environment,
        scenarios=scenarios,
        seed=seed,
        intelligence=_intelligence_settings(
            root.get("intelligence"),
            label="intelligence",
        ),
        transfer_arcs=transfer_arcs,
        earth_compute=_earth_compute_settings(
            root.get("earth_compute_counterfactuals"),
            label="earth_compute_counterfactuals",
        ),
        debris=_debris_settings(root.get("debris"), label="debris"),
        knowledge_autonomy=knowledge,
        process_environment_profiles=_process_environment_profiles(
            root.get("process_environment_profiles"),
            label="process_environment_profiles",
        ),
        embodiment_compatibility=_embodiment_settings(
            root.get("embodiment_compatibility"),
            label="embodiment_compatibility",
        ),
        embodiment_bom=embodiment_bom,
        deployment=_deployment_settings(root.get("deployment"), label="deployment"),
        orbital_mass_and_shell_debris=_orbital_mass_settings(
            root.get("orbital_mass_and_shell_debris"),
            label="orbital_mass_and_shell_debris",
        ),
        electronics_closure=_electronics_closure_settings(
            root.get("electronics_closure"),
            label="electronics_closure",
        ),
        dynamic_economics=_dynamic_economics_settings(
            root.get("dynamic_economics"),
            label="dynamic_economics",
        ),
        robust_seed_design_space=_robust_seed_design_settings(
            root.get("robust_seed_design_space"),
            label="robust_seed_design_space",
        ),
        intelligence_marginal_response=parse_typed_config(
            root.get("intelligence_marginal_response"),
            IntelligenceMarginalResponseConfig,
            label="intelligence_marginal_response",
        ),
        bottleneck_upgrade_projects=parse_typed_config(
            root.get("bottleneck_upgrade_projects"),
            BottleneckUpgradeConfig,
            label="bottleneck_upgrade_projects",
        ),
        compute_demand_allocation=parse_typed_config(
            root.get("compute_demand_allocation"),
            ComputeDemandConfig,
            label="compute_demand_allocation",
        ),
        digital_improvement=parse_typed_config(
            root.get("digital_improvement"),
            DigitalImprovementConfig,
            label="digital_improvement",
        ),
        chronological_release_backtest=parse_typed_config(
            root.get("chronological_release_backtest"),
            ChronologicalReleaseBacktestConfig,
            label="chronological_release_backtest",
        ),
        milestone_order_branches=parse_typed_config(
            root.get("milestone_order_branches"),
            MilestoneOrderConfig,
            label="milestone_order_branches",
        ),
        authorized_capacity_control=parse_typed_config(
            root.get("authorized_capacity_control"),
            AuthorizedCapacityControlConfig,
            label="authorized_capacity_control",
        ),
        ai_rd_compute_allocation=parse_typed_config(
            root.get("ai_rd_compute_allocation"),
            ComputeAllocationConfig,
            label="ai_rd_compute_allocation",
        ),
        cognitive_physical_labor=parse_typed_config(
            root.get("cognitive_physical_labor"),
            CognitivePhysicalLaborConfig,
            label="cognitive_physical_labor",
        ),
        ai_electronics_supply_chain=parse_typed_config(
            root.get("ai_electronics_supply_chain"),
            ElectronicsSupplyChainConfig,
            label="ai_electronics_supply_chain",
        ),
        compute_cohort_obsolescence=parse_typed_config(
            root.get("compute_cohort_obsolescence"),
            ComputeCohortConfig,
            label="compute_cohort_obsolescence",
        ),
        verification_hierarchy=parse_typed_config(
            root.get("verification_hierarchy"),
            VerificationHierarchyConfig,
            label="verification_hierarchy",
        ),
        industrial_reliability_ladder=parse_typed_config(
            root.get("industrial_reliability_ladder"),
            IndustrialReliabilityConfig,
            label="industrial_reliability_ladder",
        ),
        data_evaluator_coevolution=parse_typed_config(
            root.get("data_evaluator_coevolution"),
            DataEvaluatorCoevolutionConfig,
            label="data_evaluator_coevolution",
        ),
        replication_governance_externalities=parse_typed_config(
            root.get("replication_governance_externalities"),
            ReplicationGovernanceConfig,
            label="replication_governance_externalities",
        ),
        data_advantage=parse_typed_config(
            root.get("data_advantage"),
            DataAdvantageConfig,
            label="data_advantage",
        ),
        intergenerational_learning_rehearsal=parse_typed_config(
            root.get("intergenerational_learning_rehearsal"),
            IntergenerationalLearningConfig,
            label="intergenerational_learning_rehearsal",
        ),
        coordination_model=parse_typed_config(
            root.get("coordination_model"),
            CoordinationConfig,
            label="coordination_model",
        ),
        partial_closure_support=parse_typed_config(
            root.get("partial_closure_support"),
            PartialClosureSupportConfig,
            label="partial_closure_support",
        ),
        orbital_lifecycle=parse_typed_config(
            root.get("orbital_lifecycle"),
            OrbitalLifecycleConfig,
            label="orbital_lifecycle",
        ),
        orbital_transport_service=parse_typed_config(
            root.get("orbital_transport_service"),
            OrbitalTransportConfig,
            label="orbital_transport_service",
        ),
        orbital_service_strategy=parse_typed_config(
            root.get("orbital_service_strategy"),
            OrbitalServiceStrategyConfig,
            label="orbital_service_strategy",
        ),
        orbital_control=parse_typed_config(
            root.get("orbital_control"),
            OrbitalControlConfig,
            label="orbital_control",
        ),
        orbital_resilience_strategy=parse_typed_config(
            root.get("orbital_resilience_strategy"),
            OrbitalResilienceConfig,
            label="orbital_resilience_strategy",
        ),
        uncertainty=uncertainty,
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
        cfg["environment_profile"] if environment_profile is None else environment_profile
    )
    profiles = params.process_environment_profiles
    if environment_name not in profiles:
        raise ValueError(f"unknown process environment profile {environment_name!r}")
    effects = profiles[environment_name]["effects"]
    environment_throughput = np.ones(params.n)
    environment_yield = np.ones(params.n)
    environment_depreciation = np.ones(params.n)
    environment_power = np.ones(params.n)
    for sector, values in effects.items():
        j = params.sector_idx(sector)
        environment_throughput[j] = float(values.get("throughput_multiplier", 1.0))
        environment_yield[j] = float(values.get("yield_multiplier", 1.0))
        environment_depreciation[j] = float(values.get("depreciation_multiplier", 1.0))
        environment_power[j] = float(values.get("power_demand_multiplier", 1.0))
    level = float(cfg["ai_level"] if ai_level is None else ai_level)
    embodiment_cfg = params.embodiment_compatibility
    portfolio_name = embodiment_cfg["default_portfolio_by_scenario"][scenario]
    embodiment = embodiment_cfg["portfolios"][portfolio_name]
    physical_sector_pass = np.ones(params.n, dtype=bool)
    embodiment_task_pass: list[tuple[str, bool, tuple[str, ...]]] = []
    for task_name, task in embodiment_cfg["tasks"].items():
        requirements = task["requirements"]
        failed = tuple(
            dimension
            for dimension in embodiment_cfg["dimensions"]
            if float(embodiment[dimension]) < float(requirements[dimension])
        )
        task_pass = not failed
        physical_sector_pass[params.sector_idx(task["sector"])] &= task_pass
        embodiment_task_pass.append((task_name, task_pass, failed))
    coverage = np.minimum(
        params.coverage_ceiling,
        params.base_coverage + params.coverage_response * max(level - 1.0, 0.0),
    )
    autonomy_productivity = 0.50 + 0.50 * coverage

    lunar_g = float(params.environment["lunar_gravity_g"])
    acceleration_gap_g = np.maximum(params.gravity_required - lunar_g, 0.0)
    structural_fraction = float(params.environment["centrifuge_structural_mass_fraction_at_full_g"])
    power_fraction = float(params.environment["centrifuge_parasitic_power_fraction_at_full_g"])
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
    omega = np.sqrt(
        np.divide(
            accel_m_s2,
            params.centrifuge_radius,
            out=np.zeros_like(accel_m_s2),
            where=params.centrifuge_radius > 0,
        )
    )
    rpm = omega * 60.0 / (2.0 * math.pi)
    intervention = params.intervention_hours * np.maximum(1.0 - coverage, 0.0)
    knowledge = params.knowledge_autonomy
    diagnosis = np.minimum(
        coverage * float(knowledge["fault_diagnosis_scale"]),
        1.0,
    )
    verification = q_eff * coverage * float(knowledge["verification_throughput_per_service_unit"])
    engineering_cycle = (
        float(knowledge["engineering_cycle_base_years"])
        / (1.0 + float(knowledge["engineering_cycle_response"]) * max(level - 1.0, 0.0))
    ) * np.ones_like(coverage)
    yield_floor = float(knowledge["process_yield_floor"])
    process_yield = yield_floor + (1.0 - yield_floor) * coverage
    repair_success = np.minimum(
        coverage * float(knowledge["repair_success_scale"]),
        1.0,
    )
    mttr = float(knowledge["mttr_days_floor"]) + (
        float(knowledge["mttr_days_at_zero_coverage"]) - float(knowledge["mttr_days_floor"])
    ) * (1.0 - coverage)
    stop_line_threshold = np.maximum(
        params.base_coverage - float(knowledge["stop_line_threshold_below_declared_coverage"]),
        0.0,
    )
    return ProcessProfile(
        scenario=scenario,
        environment_profile=environment_name,
        ai_level=level,
        embodiment_portfolio=portfolio_name,
        embodiment_task_pass=tuple(embodiment_task_pass),
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
        stop_line_task_pass=((coverage >= stop_line_threshold) & physical_sector_pass),
        environment_throughput_multiplier=environment_throughput,
        environment_yield_multiplier=environment_yield,
        environment_depreciation_multiplier=environment_depreciation,
        environment_power_demand_multiplier=environment_power,
    )


def _constraint_slacks(
    labels: list[str],
    A_ub: FloatArray,
    b_ub: FloatArray,
    x: FloatArray,
) -> tuple[tuple[str, float], ...]:
    slack = b_ub - A_ub @ x
    scale = np.maximum(np.abs(b_ub), 1.0)
    normalized = slack / scale
    order = np.argsort(normalized)[:8]
    return tuple(
        (labels[index], float(normalized[index]))
        for raw_index in order
        for index in (int(raw_index),)
    )


def build_seed_lp(
    params: IntegratedParams,
    scenario: str,
    profile: ProcessProfile,
) -> SeedLinearProgram:
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
    bounds += [(0.0, float(import_caps.get(element, 0.0))) for element in params.elements]

    T = float(cfg["horizon_years"])
    replacement_multiplier = 1.0 + params.delta * profile.environment_depreciation_multiplier * T
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
        max(T - float(cfg["asteroid_commission_year"]), 0.0) if cfg["asteroid_enabled"] else 0.0
    )

    rows: list[FloatArray] = []
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
            scenario,
            False,
            f"autonomy threshold {profile.minimum_coverage:.3f} < {min_required:.3f}",
            None,
            None,
            None,
            digital_mass,
            np.zeros(params.n),
            np.zeros(params.m),
            0.0,
            0.0,
            profile.minimum_coverage,
            0.0,
            (),
            profile,
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
    solved = solve_linear_program(
        primary,
        a_ub=A_ub,
        b_ub=b_ub,
        bounds=lp["bounds"],
    )
    if solved.success and objective != "installed_mass":
        primary_optimum = float(primary @ solved.x)
        tolerance = 1e-8 * max(abs(primary_optimum), 1.0)
        A_lex = np.vstack([A_ub, primary])
        b_lex = np.append(b_ub, primary_optimum + tolerance)
        solved = solve_linear_program(
            lp["c"],
            a_ub=A_lex,
            b_ub=b_lex,
            bounds=lp["bounds"],
        )
    if not solved.success:
        return SeedResult(
            scenario,
            False,
            solved.message,
            None,
            None,
            None,
            digital_mass,
            np.zeros(n),
            np.zeros(m),
            0.0,
            0.0,
            profile.minimum_coverage,
            0.0,
            (),
            profile,
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
        status=(f"lexicographic {objective} optimum within the declared linear seed architecture"),
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
    cfg = params.deployment
    core, _, _ = seed_result.required_masses()
    packaging = core * float(cfg["transport_packaging_fraction"])
    spares_initial = core * float(cfg["initial_spares_fraction"])
    startup_energy = core * float(cfg["startup_energy_mwh_per_seed_t"])
    startup_storage = startup_energy * float(cfg["startup_storage_t_per_mwh"])
    fixed_logistics = (
        float(cfg["unloading_equipment_mass_t"])
        + float(cfg["site_work_equipment_mass_t"])
        + float(cfg["calibration_standards_mass_t"])
    )
    logistics = packaging + spares_initial + startup_storage + fixed_logistics
    delivered_mass = core + logistics

    steps = round(years / dt)
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
    installed_sector: FloatArray,
    operating_sector: FloatArray,
    available_material: FloatArray,
    *,
    gross_cell_order_budget: float,
    productivity_multiplier: float,
    dt: float,
) -> FloatArray:
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
    rows: list[FloatArray] = []
    rhs: list[float] = []
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
    primary = solve_linear_program(
        c,
        a_ub=np.asarray(rows),
        b_ub=np.asarray(rhs),
        bounds=[(0.0, None)] * (n + 1),
    )
    if not primary.success:
        return np.zeros(n)
    target = float(primary.x[-1])

    # Fix the max-min target and minimize embodied mass. This removes the
    # arbitrary excess-sector choices that a single-stage max-min LP permits.
    rows2: list[FloatArray] = [np.asarray(row[:n], dtype=float) for row in rows[:-n]]
    rhs2: list[float] = list(rhs[:-n])
    for j in range(n):
        row2 = np.zeros(n)
        row2[j] = -normalized_weight[j]
        rows2.append(row2)
        rhs2.append(float(current_ratio[j] - target + 1e-9))
    mass = seed_result.process.B_effective.sum(axis=0)
    secondary = solve_linear_program(
        mass,
        a_ub=np.asarray(rows2),
        b_ub=np.asarray(rhs2),
        bounds=[(0.0, None)] * n,
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
    capacity_reproduction_enabled: bool = True,
    intelligence_level_offset: float = 0.0,
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

    ``capacity_reproduction_enabled=False`` blocks all new-capacity orders
    while leaving depreciation, repair, compute, and verified digital-loop
    accounting active. It is a causal ablation, not a feasible operating
    policy.

    ``intelligence_level_offset`` adds a declared exogenous capability
    perturbation above the scenario baseline without moving the reference
    from which productivity and autonomy gains are calculated. It exists for
    finite-response diagnostics and is not an endogenous forecast.
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
        raise ValueError("unknown allocation_policy")
    if import_stock_multiplier is not None and import_stock_multiplier < 0.0:
        raise ValueError("import_stock_multiplier must be nonnegative")
    if depreciation_multiplier <= 0.0:
        raise ValueError("depreciation_multiplier must be positive")
    if intelligence_level_offset < 0.0:
        raise ValueError("intelligence_level_offset must be nonnegative")
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
            raise ValueError("outage windows require 0 <= start < end and multiplier in [0, 1]")
    cfg = params.scenarios[seed_result.scenario]
    profile = seed_result.process
    knowledge = params.knowledge_autonomy
    z = seed_result.capacities
    cell_bom = profile.B_effective @ z
    service_need = params.A @ z

    steps = round(years / dt)
    t = np.arange(steps + 1, dtype=float) * dt
    installed_sector = np.zeros((steps + 1, params.n))
    operating_sector = np.zeros((steps + 1, params.n))
    ordered_sector = np.zeros((steps + 1, params.n))
    installed = np.zeros(steps + 1)
    operating = np.zeros(steps + 1)
    intelligence = np.zeros(steps + 1)
    loop_throughput = np.zeros(steps + 1)
    marginal_gain_per_loop = np.zeros(steps + 1)
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
    intelligence[0] = float(cfg["ai_level"]) + float(intelligence_level_offset)
    i_compute = params.sector_idx("compute")
    compute_scale = float(params.intelligence["compute_units_per_compute_capacity"])
    compute[0] = operating_sector[0, i_compute] * compute_scale
    inventory[0] = seed_result.import_stock_t * float(
        initial_cells if import_stock_multiplier is None else import_stock_multiplier
    )

    lag_steps = np.maximum(1, np.rint(params.lag / dt).astype(int))
    queue = np.zeros((params.n, int(np.max(lag_steps))))
    ramp_steps = np.maximum(1, np.rint(params.ramp / dt).astype(int))
    activation_queue = np.zeros((params.n, int(np.max(ramp_steps))))
    repair_lag_steps = max(
        1,
        round(float(params.seed["repair_lag_years"]) / dt),
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
    viable_floor = params.min_seed * float(cfg["viable_floor_multiplier"])
    effective_delta = (
        params.delta * profile.environment_depreciation_multiplier * depreciation_multiplier
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
            float(params.seed["repairable_failure_fraction"]) if repair_enabled else 0.0
        )
        newly_failed = (retired_sector + shock_loss) * repairable_fraction
        unrecoverable_retirement = retired_sector + shock_loss - newly_failed
        failed_available = failed_sector[k] + newly_failed
        recovered = recovery * (profile.B_effective @ unrecoverable_retirement)
        recycled_total += float(recovered.sum())

        lunar_scale = max(float(np.min(capacity_ratio[[i_mining, i_refining, i_power]])), 0.0)
        lunar_prod = params.lunar_yield * seed_result.lunar_feed_t_per_year * lunar_scale * dt
        for start, end, multiplier in lunar_source_outage_windows:
            if start <= t[k] < end:
                lunar_prod *= multiplier
        asteroid_prod = np.zeros(params.m)
        if cfg["asteroid_enabled"] and t[k] >= asteroid_start:
            asteroid_scale = max(
                float(np.min(capacity_ratio[[i_mining, i_refining, i_transport, i_power]])), 0.0
            )
            asteroid_prod = (
                params.asteroid_yield * seed_result.asteroid_feed_t_per_year * asteroid_scale * dt
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
            routine_intervention = float(profile.intervention_hours_per_year @ op_sector)
            intervention_budget = max(
                (float(cfg["remote_intervention_budget_hours_per_year"]) - routine_intervention)
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
                parts_fraction = float(params.seed["repair_parts_fraction_of_bom"])
                parts = parts_fraction * (profile.B_effective @ candidate)
                material_scale = float(
                    np.min(
                        np.divide(
                            available,
                            parts,
                            out=np.full(params.m, np.inf),
                            where=parts > 1e-12,
                        )
                    )
                )
                repair_started = candidate * min(
                    max(material_scale, 0.0),
                    1.0,
                )
                available = np.maximum(
                    available - parts_fraction * (profile.B_effective @ repair_started),
                    0.0,
                )
                repair_queue[:, -1] += repair_started
        failed_sector[k + 1] = np.maximum(
            failed_available - repair_started,
            0.0,
        )
        repaired_sector[k + 1] = repaired_due

        level_gain = max(intelligence[k] - float(cfg["ai_level"]), 0.0)
        productivity = 1.0 + float(params.intelligence["productivity_elasticity"]) * level_gain
        autonomy_gain = (
            1.0 + float(params.intelligence["autonomy_learning_multiplier"]) * level_gain
        )
        service_limit = float(
            np.min(
                np.divide(
                    profile.q_effective * op_sector,
                    service_need,
                    out=np.full(params.n, np.inf),
                    where=service_need > 1e-12,
                )
            )
        )
        rate_cap = float(params.seed["maximum_gross_cell_orders_per_operating_cell_year"]) * op
        intervention_demand[k] = float(profile.intervention_hours_per_year @ op_sector)
        verification_per_cell = knowledge["verification_units_per_new_capacity"] * float(z.sum())
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
                float(cfg["remote_intervention_budget_hours_per_year"]) * communication_multiplier
            )
            intervention_per_cell = max(
                float(profile.intervention_hours_per_year @ z),
                1e-12,
            )
            candidate_limits["autonomy"] = max(
                (remote_budget - intervention_demand[k]) / intervention_per_cell,
                0.0,
            )
            verification_available = (
                float(profile.verification_throughput_per_year @ op_sector)
                * verification_multiplier
            )
            candidate_limits["verification"] = verification_available / max(
                verification_per_cell, 1e-12
            )
            candidate_limits["compute"] = (
                compute[k]
                * compute_multiplier
                / max(
                    knowledge["compute_units_per_cell_order_year"],
                    1e-12,
                )
            )
            if not bool(np.all(profile.stop_line_task_pass)):
                candidate_limits["autonomy"] = 0.0
        primary = min(candidate_limits, key=lambda name: candidate_limits[name])
        if capacity_reproduction_enabled:
            desired = max(float(candidate_limits[primary]), 0.0) * productivity * autonomy_gain * dt
        else:
            desired = 0.0
            primary = "capital_reproduction_frozen"
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
                binding = np.flatnonzero(material_limit_by_element <= material_limit + 1e-8)
                limiting_counts[binding] += 1
        else:
            built = 0.0
        if allocation_policy == "balanced":
            sector_order = built * z
            material_use = built * cell_bom
            ordered[k + 1] = built
        else:
            gross_budget = (
                float(params.seed["maximum_gross_cell_orders_per_operating_cell_year"])
                * op
                * productivity
                * autonomy_gain
                * dt
                if capacity_reproduction_enabled
                else 0.0
            )
            allocation_material = available
            if allocation_policy == "surplus_preserving":
                allocation_material = 0.80 * available
            objective_installed = installed_state.copy()
            future_shocks = [event for event in shock_events if float(event[0]) >= float(t[k])]
            if allocation_policy in {"shock_aware", "perfect_foresight"}:
                for _event_year, event_sector, event_fraction in future_shocks:
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
            binding = np.flatnonzero(available - material_use <= 1e-8)
            if len(binding):
                primary = "material"
                limiting_counts[binding] += 1
        if (
            repair_enabled
            and (np.any(failed_available - repair_started > 1e-9) or np.any(repair_queue > 1e-9))
            and (np.any(op_sector < viable_floor) or np.any(shock_loss > 1e-9))
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
            activation_queue[j, : ramp_steps[j]] += due[j] / ramp_steps[j]
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
            installed_state * (1.0 - effective_delta * dt) + due,
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
        installed[k + 1] = float(
            np.min(
                np.divide(
                    installed_sector[k + 1],
                    z,
                    out=np.full(params.n, np.inf),
                    where=z > 1e-12,
                )
            )
        )
        operating[k + 1] = float(
            np.min(
                np.divide(
                    operating_sector[k + 1],
                    z,
                    out=np.full(params.n, np.inf),
                    where=z > 1e-12,
                )
            )
        )

        compute[k + 1] = operating_sector[k + 1, i_compute] * compute_scale
        verification = float(params.intelligence["verification_factor"])
        gain_scale = float(params.intelligence["gain_scale_per_verified_loop"])
        normalized_compute = compute[k + 1] / max(compute[0], 1e-12)
        stage_rates = {
            name: float(value)
            for name, value in params.intelligence["verified_loop_stage_rates_per_year"].items()
        }
        stage_rates["train"] *= min(
            max(normalized_compute, 0.0) ** 0.5,
            2.0,
        )
        loop_throughput[k] = verified_loop_throughput(stage_rates) * verification
        factors = params.intelligence["effective_compute_factors"]
        effectiveness = float(
            np.prod(
                [
                    float(factors["hardware_efficiency"]),
                    float(factors["utilization"]),
                    float(factors["algorithmic_efficiency"]),
                    float(factors["architecture_efficiency"]),
                ]
            )
        )
        maximum_level = float(params.intelligence["maximum_level"])
        initial_level = float(params.intelligence["initial_level"])
        frontier_gap = max(maximum_level - intelligence[k], 0.0)
        reference_gap = max(maximum_level - initial_level, 1e-12)
        diminishing = (frontier_gap / reference_gap) ** float(
            params.intelligence["frontier_gap_exponent"]
        )
        compute_signal = math.log1p(max(normalized_compute, 0.0)) / math.log(2.0)
        d_intelligence = (
            gain_scale * loop_throughput[k] * effectiveness * compute_signal * diminishing * dt
        )
        marginal_gain_per_loop[k] = d_intelligence / max(loop_throughput[k] * dt, 1e-12)
        intelligence[k + 1] = min(
            intelligence[k] + d_intelligence,
            maximum_level,
        )

    reached = np.flatnonzero(operating >= 2.0)
    doubling = float(t[reached[0]]) if len(reached) else None
    intervention_demand[-1] = float(
        profile.intervention_hours_per_year @ np.maximum(operating_sector[-1], 0.0)
    )
    verification_demand[-1] = verification_demand[-2] if steps else 0.0
    loop_throughput[-1] = loop_throughput[-2] if steps else 0.0
    marginal_gain_per_loop[-1] = marginal_gain_per_loop[-2] if steps else 0.0
    survived = bool(
        np.min(installed) >= min_cells
        and installed[-1] >= min_cells
        and np.all(operating_sector[-1] >= viable_floor)
    )
    limiting = tuple(
        (params.elements[index], int(limiting_counts[index]))
        for raw_index in np.argsort(-limiting_counts)
        for index in (int(raw_index),)
        if limiting_counts[index] > 0
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
        verified_loop_throughput=loop_throughput,
        intelligence_marginal_gain_per_loop=marginal_gain_per_loop,
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
    dep = params.earth_compute.depreciation_per_year
    terrestrial: dict[str, FloatArray] = {}
    orbital: dict[str, FloatArray] = {}
    for label, cfg in params.earth_compute.cases.items():
        earth = np.zeros_like(t)
        orbit = np.zeros_like(t)
        earth[0] = orbit[0] = 1.0
        for k in range(len(t) - 1):
            build = cfg.terrestrial_build_units_per_year
            ceiling = cfg.terrestrial_site_ceiling_units
            build = 0.0 if earth[k] >= ceiling else min(build, (ceiling - earth[k]) / dt)
            earth[k + 1] = max(earth[k] + (build - dep * earth[k]) * dt, 0.0)

            delivery = min(
                cfg.earth_to_orbit_build_units_per_year,
                cfg.launch_units_per_year,
            )
            orbit[k + 1] = max(
                orbit[k] + (delivery - dep * orbit[k]) * dt,
                0.0,
            )
        terrestrial[label] = earth
        orbital[label] = orbit
    endogenous = capacity_growth.local_compute / max(capacity_growth.local_compute[0], 1e-12)
    arc = params.transfer_arcs["moon_to_orbit_compute"]
    export_share = arc.get("share_of_new_endogenous_compute")
    transport_units = arc.get("normalized_compute_units_per_transport_capacity_year")
    if export_share is None or transport_units is None:
        raise ValueError("moon_to_orbit_compute requires share and transport-unit fields")
    export_lag_steps = max(1, round(arc["lag_years"] / dt))
    i_transport = params.sector_idx("transport")
    # The canonical cell's transport capacity scales with operating cells.
    # Capacity values are normalized to the initial off-world compute stock.
    base_seed = size_seed(params, capacity_growth.scenario)
    transport_per_cell = (
        base_seed.capacities[i_transport] if base_seed.feasible else params.min_seed[i_transport]
    )
    transport_rate = transport_units * transport_per_cell * capacity_growth.operating_cells
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
    deployment_capacity: FloatArray,
    t: FloatArray,
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
            active[k] + derelict[k] + float(cfg["fragment_hazard_multiplier"]) * fragments[k]
        )
        kernel = float(cfg["collision_kernel"]) * float(mit.get("collision_kernel_multiplier", 1.0))
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
            )
            * dt,
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

    window = max(1, round(5.0 / dt))
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
        subcritical=bool(ratio <= 1.0 + 1e-9 and fragments[-1] <= fragments[-window] + 1e-9),
    )


def simulate_shell_debris(
    params: IntegratedParams,
    deployment_capacity: FloatArray,
    t: FloatArray,
) -> ShellDebrisResult:
    """Finite-mass, shell- and fragment-class-resolved orbital stress model.

    Requested positive deployment increments consume feed inventory. Feed is
    supplied only by finite-reservoir capture, time-limited Earth imports, and
    recovered controlled retirements. Collision and failure losses reduce
    active capacity, so the returned trajectory—not the requested input—is
    the industrially available orbital stock.
    """
    cfg = params.orbital_mass_and_shell_debris
    shell_cfg = cfg["shells"]
    shells = tuple(row["name"] for row in shell_cfg)
    ns = len(shells)
    if len(t) != len(deployment_capacity) or len(t) < 2:
        raise ValueError("deployment_capacity and t must have equal length >= 2")
    transfer = np.asarray(cfg["cross_shell_transfer"], dtype=float)
    if transfer.shape != (ns, ns) or not np.allclose(transfer.sum(axis=1), 1.0):
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
            reservoir[k] * float(cfg["capture_fraction_of_reservoir_per_year"]) * dt,
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

        failures = float(cfg["asset_failure_per_year"]) * active[k] * dt
        collisions = np.zeros(ns)
        for s, row in enumerate(shell_cfg):
            hazard = (
                active[k, s]
                + derelict[k, s]
                + float(cfg["fragment_hazard_weight_trackable"]) * trackable[k, s]
                + float(cfg["fragment_hazard_weight_untrackable"]) * untrackable[k, s]
            )
            saturation = 1.0 + float(cfg["avoidance_saturation_slope"]) * max(
                trackable[k, s] - float(cfg["avoidance_saturation_threshold"]),
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
        disposed = float(cfg["controlled_disposal_fraction"]) * failures
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
            + (1.0 - float(cfg["recovery_fraction_of_controlled_retirement"]))
            * float((disposed + retrieval).sum())
            * mass_per_unit
        )

        new_trackable_origin = float(cfg["trackable_fragments_per_collision"]) * collisions
        new_untrackable_origin = float(cfg["untrackable_fragments_per_collision"]) * collisions
        new_trackable = new_trackable_origin @ transfer
        new_untrackable = new_untrackable_origin @ transfer
        trackable_clear = np.array(
            [
                float(row["natural_trackable_clearance_per_year"]) * trackable[k, s] * dt
                + float(row["active_removal_trackable_per_year"]) * dt
                for s, row in enumerate(shell_cfg)
            ]
        )
        untrackable_clear = np.array(
            [
                float(row["natural_untrackable_clearance_per_year"]) * untrackable[k, s] * dt
                for s, row in enumerate(shell_cfg)
            ]
        )
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
            + float(cfg["fragment_hazard_weight_trackable"]) * trackable[-1, s]
            + float(cfg["fragment_hazard_weight_untrackable"]) * untrackable[-1, s]
        )
        collision_probability = (
            float(row["collision_kernel"]) * hazard / max(float(row["volume_index"]), 1e-12)
        )
        weighted_descendants = float(cfg["trackable_fragments_per_collision"]) * float(
            cfg["fragment_hazard_weight_trackable"]
        ) / max(
            float(row["natural_trackable_clearance_per_year"]),
            1e-12,
        ) + float(cfg["untrackable_fragments_per_collision"]) * float(
            cfg["fragment_hazard_weight_untrackable"]
        ) / max(
            float(row["natural_untrackable_clearance_per_year"]),
            1e-12,
        )
        branching[s] = collision_probability * weighted_descendants

    accessible = feed + mass_per_unit * (active.sum(axis=1) + derelict.sum(axis=1))
    cost = (
        float(imported.sum() + lost.sum()) * 1000.0 * float(cfg["replacement_delivery_cost_per_kg"])
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
    entropy = zlib.crc32(f"{seed}/{run_index}/{name}".encode())
    rng = np.random.default_rng(entropy)
    lo, hi = bounds
    log_draw = float(rng.uniform(math.log(lo), math.log(hi)))
    return math.exp(log_draw)


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
        total_mass, _, _ = sized.required_masses()
        masses.append(total_mass)
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
