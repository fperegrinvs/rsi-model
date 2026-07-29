"""Closed schemas for orbital extension configuration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import NotRequired, TypedDict


class OrbitalLifecycleInputs(TypedDict):
    initial_operating: float
    degradation_per_year: float
    failure_per_year: float
    collision_loss_per_year: float
    degraded_to_service_per_year: float
    service_start_capacity_per_year: float
    repair_completion_per_year: float
    repair_success_fraction: float
    controlled_retirement_per_year: float
    obsolescence_per_year: float
    cannibalization_per_year: float
    recycling_per_year: float
    recycling_yield: float
    disposal_per_year: float
    debris_retrieval_per_year: float
    retrieval_success_fraction: float
    manufacturing_from_feedstock_per_year: float
    external_deployment_per_year: float


class ServiceabilityPortfolio(TypedDict):
    docking_refueling_interfaces: float
    modular_replaceable_units: float
    accessible_fasteners_ports_grapples: float
    material_passports_separability: float
    passivation_and_safe_state: float
    machine_readable_service_manuals: float
    repair_success_multiplier: float
    recycling_yield_multiplier: float
    capture_rate_multiplier: float
    mass_penalty_fraction: float


class OrbitalLifecycleConfig(OrbitalLifecycleInputs):
    source_class: str
    serviceability_portfolios: Mapping[str, ServiceabilityPortfolio]


class TransportServiceCase(TypedDict):
    architecture: str
    origin: str
    destination: str
    delta_v_km_s: float
    delta_v_source: str
    specific_impulse_s: float
    clients: float
    failure_rate_per_year: float
    serviceability_fraction: float
    clients_per_mission: float
    servicer_dry_mass_t: float
    parts_t_per_mission: float
    recovered_mass_t_per_mission: float
    propellant_cost_per_kg: float
    propellant_source: str
    parts_cost_per_kg: float
    recovered_material_credit_per_kg: float
    orbit_plane_distribution: str
    operations_musd_per_mission: float
    servicer_capex_musd: float
    reuse_cycles: float
    fixed_infrastructure_musd: float
    infrastructure_life_years: float
    client_value_musd: float
    preserved_value_fraction: float
    requires_lunar_industry: bool
    lunar_industrial_maturity: float
    required_lunar_maturity: float


class OrbitalTransportConfig(TypedDict):
    source_class: str
    evidence_boundary: str
    cases: Mapping[str, TransportServiceCase]


class ServiceOrbit(TypedDict):
    family: str
    rendezvous_delta_v_km_s: float
    inclination_change_multiplier: float
    routing_multiplier: float
    service_cost_multiplier: float
    stationkeeping_m_s_per_year: float
    residence_time_years: float
    atmospheric_clearance: str
    radiation_index: float
    debris_exposure_index: float
    tracking_coverage_fraction: float
    disposal_route: str
    disposal_delta_v_km_s: float
    debris_liability_multiplier: float
    relocation_supported: bool


class ServiceAsset(TypedDict):
    asset_value_musd: float
    replacement_launch_cost_musd: float
    annual_output_value_musd: float
    design_life_years: float
    remaining_life_years: float
    component_value_musd: float
    material_value_musd: float
    residual_value_musd: float
    serviceability_fraction: float
    modularity_fraction: float
    refuel_access_fraction: float
    cooperative_target: bool


class ServiceFleet(TypedDict):
    servicers: float
    missions_per_servicer_year: float
    development_cost_musd: float
    depot_cost_musd: float
    recycling_plant_cost_musd: float
    design_life_years: float
    routing_cost_musd_per_km_s: float
    propellant_replenishment_cost_musd_per_km_s: float
    scheduling_multiplier: float
    congestion_multiplier: float
    has_depot: bool
    has_recycling_plant: bool


class ServiceAction(TypedDict):
    minimum_serviceability_fraction: float
    minimum_modularity_fraction: float
    minimum_refuel_access_fraction: float
    requires_depot: NotRequired[bool]
    requires_recycling_plant: NotRequired[bool]
    requires_cooperative_target: NotRequired[bool]
    output_restoration_fraction: float
    replacement_avoidance_fraction: float
    asset_value_preservation_fraction: float
    component_recovery_fraction: float
    material_recovery_fraction: float
    service_failure_probability: float
    debris_incident_probability: float
    depreciation_fraction: float
    residual_value_fraction: float
    upgrade_incremental_value_musd: float
    variable_service_cost_musd: float
    downtime_years: float
    downtime_loss_fraction: float
    governance_dependencies: tuple[str, ...]


class ServiceGovernance(TypedDict):
    debris_liability_exposure_musd: float
    evidence_status: Mapping[str, str]
    authoritative_basis: Mapping[str, str]


class OrbitalServiceStrategyConfig(TypedDict):
    source_class: str
    currency_year: str
    evidence_boundary: str
    orbits: Mapping[str, ServiceOrbit]
    asset_classes: Mapping[str, ServiceAsset]
    fleets: Mapping[str, ServiceFleet]
    actions: Mapping[str, ServiceAction]
    governance: ServiceGovernance


class OrbitalControlConfig(TypedDict):
    source_class: str
    common_cause_budget_fraction: float
    node_capacities: tuple[float, ...]
    hazard_sets: Mapping[str, tuple[int, ...]]
    trigger_thresholds: Mapping[str, float]


class ClusterLayout(TypedDict):
    total_nodes: int
    nodes_per_cluster: int
    orbital_planes: int
    independent_shells: int
    altitude_dispersion_km: float
    inclination_dispersion_deg: float
    along_track_spacing_deg: float
    independent_gateways: int
    independent_control_domains: int
    shared_power_fraction: float
    shared_navigation_fraction: float
    shared_software_fraction: float
    crosslink_latency_index: float


class ConstellationNode(TypedDict):
    name: str
    environment: str
    altitude_km: float
    inclination_deg: float
    plane: int
    along_track_deg: float
    capacity: float
    gateway: str
    control_domain: str


class BreakupEvent(TypedDict):
    name: str
    environment: NotRequired[str]
    origin_node_name: NotRequired[str]
    origin_node: NotRequired[int]
    initial_fragments: float
    fragment_clearance_per_day: float
    secondary_fragments_per_collision: float
    collision_kernel_per_fragment_day: float
    altitude_scale_km: float
    inclination_scale_deg: float
    initial_cloud_width_deg: float
    cloud_spread_deg_per_day: float
    cross_plane_exposure_fraction: float
    tracking_fraction: float
    maneuver_success_fraction: float
    repair_delay_days: float
    repair_capacity_per_day: float
    restore_fraction: NotRequired[float]


class DegradedControlScenario(TypedDict):
    tracking_fraction: float
    communications_fraction: float
    navigation_fraction: float
    coordination_fraction: float
    independent_fallback_fraction: float
    cadence_risk_multiplier: float
    spacing_risk_multiplier: float
    coordination_fallback_multiplier: float


class ConjunctionStressConfig(TypedDict):
    conjunctions: float
    collision_probability_per_unsafe_conjunction: float
    risk_limit: float
    scenarios: Mapping[str, DegradedControlScenario]


class MitigationPortfolioConfig(TypedDict):
    levels: Mapping[str, tuple[float, ...]]
    base_risk_index: float
    cadence_exponent: float
    disposal_floor: float
    removal_effectiveness: float
    small_debris_shielding_effectiveness: float
    servicer_effectiveness: float
    repair_effectiveness: float
    cadence_cost: float
    disposal_cost: float
    removal_cost: float
    shielding_cost: float
    shell_diversity_cost: float
    servicer_cost: float
    repair_cost: float
    shell_distribution_capacity_penalty: float
    repair_capacity_return: float


class MultiOperatorShell(TypedDict):
    conjunctions_per_node_pair_year: float
    maximum_coordinated_conjunctions_per_year: float
    minimum_operator_compliance_fraction: float


class OrbitalOperator(TypedDict):
    name: str
    planned_nodes: int
    tracking_data_share_fraction: float
    maneuver_coordination_fraction: float
    disposal_compliance_fraction: float
    authorization_valid: bool


class MultiOperatorConfig(TypedDict):
    shells: Mapping[str, MultiOperatorShell]
    scenarios: Mapping[str, tuple[OrbitalOperator, ...]]


class OrbitalResilienceConfig(TypedDict):
    source_class: str
    bounding_argument: str
    common_cause_budget_fraction: float
    collision_exposure_index: float
    cluster_layouts: Mapping[str, ClusterLayout]
    constellation_nodes: tuple[ConstellationNode, ...]
    breakup_events: Mapping[str, BreakupEvent]
    conjunction_stress: ConjunctionStressConfig
    mitigation_portfolio: MitigationPortfolioConfig
    multi_operator: MultiOperatorConfig


def lifecycle_inputs(
    config: OrbitalLifecycleInputs,
    *,
    repair_success_fraction: float | None = None,
    recycling_yield: float | None = None,
    service_start_capacity_per_year: float | None = None,
    debris_retrieval_per_year: float | None = None,
    manufacturing_from_feedstock_per_year: float | None = None,
    external_deployment_per_year: float | None = None,
) -> OrbitalLifecycleInputs:
    """Copy the lifecycle calculation boundary with named overrides."""
    result = OrbitalLifecycleInputs(
        initial_operating=config["initial_operating"],
        degradation_per_year=config["degradation_per_year"],
        failure_per_year=config["failure_per_year"],
        collision_loss_per_year=config["collision_loss_per_year"],
        degraded_to_service_per_year=config["degraded_to_service_per_year"],
        service_start_capacity_per_year=config["service_start_capacity_per_year"],
        repair_completion_per_year=config["repair_completion_per_year"],
        repair_success_fraction=config["repair_success_fraction"],
        controlled_retirement_per_year=config["controlled_retirement_per_year"],
        obsolescence_per_year=config["obsolescence_per_year"],
        cannibalization_per_year=config["cannibalization_per_year"],
        recycling_per_year=config["recycling_per_year"],
        recycling_yield=config["recycling_yield"],
        disposal_per_year=config["disposal_per_year"],
        debris_retrieval_per_year=config["debris_retrieval_per_year"],
        retrieval_success_fraction=config["retrieval_success_fraction"],
        manufacturing_from_feedstock_per_year=(config["manufacturing_from_feedstock_per_year"]),
        external_deployment_per_year=config["external_deployment_per_year"],
    )
    overrides = (
        ("repair_success_fraction", repair_success_fraction),
        ("recycling_yield", recycling_yield),
        ("service_start_capacity_per_year", service_start_capacity_per_year),
        ("debris_retrieval_per_year", debris_retrieval_per_year),
        (
            "manufacturing_from_feedstock_per_year",
            manufacturing_from_feedstock_per_year,
        ),
        ("external_deployment_per_year", external_deployment_per_year),
    )
    for key, value in overrides:
        if value is not None:
            result[key] = value
    return result


def replace_transport_service_case(
    case: TransportServiceCase,
    *,
    client_value_musd: float | None = None,
    failure_rate_per_year: float | None = None,
    serviceability_fraction: float | None = None,
    clients: float | None = None,
    recovered_mass_t_per_mission: float | None = None,
    reuse_cycles: float | None = None,
    lunar_industrial_maturity: float | None = None,
) -> TransportServiceCase:
    """Copy a transport case while restricting sensitivity overrides."""
    result = case.copy()
    if client_value_musd is not None:
        result["client_value_musd"] = client_value_musd
    if failure_rate_per_year is not None:
        result["failure_rate_per_year"] = failure_rate_per_year
    if serviceability_fraction is not None:
        result["serviceability_fraction"] = serviceability_fraction
    if clients is not None:
        result["clients"] = clients
    if recovered_mass_t_per_mission is not None:
        result["recovered_mass_t_per_mission"] = recovered_mass_t_per_mission
    if reuse_cycles is not None:
        result["reuse_cycles"] = reuse_cycles
    if lunar_industrial_maturity is not None:
        result["lunar_industrial_maturity"] = lunar_industrial_maturity
    return result


__all__ = [
    "BreakupEvent",
    "ClusterLayout",
    "ConjunctionStressConfig",
    "ConstellationNode",
    "DegradedControlScenario",
    "MitigationPortfolioConfig",
    "MultiOperatorConfig",
    "MultiOperatorShell",
    "OrbitalControlConfig",
    "OrbitalLifecycleConfig",
    "OrbitalLifecycleInputs",
    "OrbitalOperator",
    "OrbitalResilienceConfig",
    "OrbitalServiceStrategyConfig",
    "OrbitalTransportConfig",
    "ServiceAction",
    "ServiceAsset",
    "ServiceFleet",
    "ServiceGovernance",
    "ServiceOrbit",
    "ServiceabilityPortfolio",
    "TransportServiceCase",
    "lifecycle_inputs",
    "replace_transport_service_case",
]
