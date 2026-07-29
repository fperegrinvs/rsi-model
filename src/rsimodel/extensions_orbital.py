"""Domain models split from the public :mod:`rsimodel.extensions` facade."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np

from .array_types import FloatArray
from .extensions_digital import LIFECYCLE_STATES, validate_unit_interval
from .orbital_config import (
    BreakupEvent,
    ClusterLayout,
    ConstellationNode,
    DegradedControlScenario,
    MitigationPortfolioConfig,
    MultiOperatorShell,
    OrbitalLifecycleInputs,
    OrbitalOperator,
    ServiceAction,
    ServiceAsset,
    ServiceFleet,
    ServiceGovernance,
    ServiceOrbit,
    TransportServiceCase,
)


@dataclass(frozen=True)
class LifecycleResult:
    t: FloatArray
    stocks: FloatArray
    flows: dict[str, FloatArray]
    effective_irreversible_loss_per_year: float

    def state(self, name: str) -> FloatArray:
        return self.stocks[:, LIFECYCLE_STATES.index(name)]


@dataclass(frozen=True)
class TransportServiceResult:
    architecture: str
    available: bool
    annual_missions: float
    propellant_t_per_mission: float
    annual_cost_musd: float
    annual_preserved_value_musd: float
    net_value_musd: float
    breakeven_client_value_musd: float | None


@dataclass(frozen=True)
class OrbitalServiceDecisionResult:
    orbit: str
    asset_class: str
    fleet: str
    action: str
    technically_feasible: bool
    technical_blockers: tuple[str, ...]
    governance_ready: bool
    governance_dependencies: tuple[str, ...]
    annual_fleet_capacity: float
    fixed_cost_per_client_musd: float
    routing_cost_per_client_musd: float
    expected_lifetime_output_value_musd: float
    avoided_replacement_launch_musd: float
    recovered_value_musd: float
    expected_benefit_musd: float
    service_cost_musd: float
    downtime_cost_musd: float
    risk_and_liability_cost_musd: float
    depreciation_cost_musd: float
    residual_value_musd: float
    net_value_musd: float
    economic_viable: bool
    deployable: bool
    break_even_service_cost_musd: float


def evaluate_orbital_service_decision(
    *,
    orbit_name: str,
    orbit: ServiceOrbit,
    asset_name: str,
    asset: ServiceAsset,
    fleet_name: str,
    fleet: ServiceFleet,
    action_name: str,
    action: ServiceAction,
    governance: ServiceGovernance,
) -> OrbitalServiceDecisionResult:
    """Evaluate one orbital disposition on a common value-and-risk boundary.

    Technical feasibility, economic viability, and authorization readiness are
    intentionally independent. All monetary quantities are real 2025 MUSD per
    client event. The result is an assumption-class decision surface, not a
    legal opinion or demonstrated service capability.
    """
    unit_fields = (
        "output_restoration_fraction",
        "replacement_avoidance_fraction",
        "asset_value_preservation_fraction",
        "component_recovery_fraction",
        "material_recovery_fraction",
        "service_failure_probability",
        "debris_incident_probability",
        "depreciation_fraction",
        "residual_value_fraction",
    )
    for name in unit_fields:
        validate_unit_interval(action[name], f"{action_name}.{name}")
    for name in (
        "serviceability_fraction",
        "modularity_fraction",
        "refuel_access_fraction",
    ):
        validate_unit_interval(asset[name], f"{asset_name}.{name}")
    if float(asset["remaining_life_years"]) < 0.0:
        raise ValueError("remaining life must be nonnegative")
    if float(fleet["servicers"]) <= 0.0 or float(fleet["design_life_years"]) <= 0.0:
        raise ValueError("fleet size and design life must be positive")
    if float(fleet["missions_per_servicer_year"]) < 0.0:
        raise ValueError("fleet mission rate must be nonnegative")

    blockers: list[str] = []
    if float(asset["serviceability_fraction"]) < float(action["minimum_serviceability_fraction"]):
        blockers.append("serviceability")
    if float(asset["modularity_fraction"]) < float(action["minimum_modularity_fraction"]):
        blockers.append("modularity")
    if float(asset["refuel_access_fraction"]) < float(action["minimum_refuel_access_fraction"]):
        blockers.append("refuel_access")
    if bool(action.get("requires_depot", False)) and not bool(fleet["has_depot"]):
        blockers.append("depot")
    if bool(action.get("requires_recycling_plant", False)) and not bool(
        fleet["has_recycling_plant"]
    ):
        blockers.append("recycling_plant")
    if bool(action.get("requires_cooperative_target", False)) and not bool(
        asset["cooperative_target"]
    ):
        blockers.append("cooperative_target")
    if action_name == "relocate" and not bool(orbit["relocation_supported"]):
        blockers.append("relocation_route")
    technically_feasible = not blockers

    dependencies = tuple(action.get("governance_dependencies", ()))
    evidence = governance["evidence_status"]
    governance_ready = all(evidence.get(name) == "validated" for name in dependencies)

    annual_capacity = (
        float(fleet["servicers"])
        * float(fleet["missions_per_servicer_year"])
        / max(
            float(orbit["routing_multiplier"])
            * float(orbit["inclination_change_multiplier"])
            * float(fleet["scheduling_multiplier"])
            * float(fleet["congestion_multiplier"]),
            1e-12,
        )
    )
    fixed_total = (
        float(fleet["development_cost_musd"])
        + float(fleet["depot_cost_musd"])
        + float(fleet["recycling_plant_cost_musd"])
    )
    lifetime_clients = annual_capacity * float(fleet["design_life_years"])
    fixed_per_client = fixed_total / lifetime_clients if lifetime_clients > 0.0 else math.inf
    routing_cost = float(orbit["rendezvous_delta_v_km_s"]) * float(
        orbit["inclination_change_multiplier"]
    ) * float(fleet["routing_cost_musd_per_km_s"]) + float(
        orbit["stationkeeping_m_s_per_year"]
    ) / 1000.0 * float(asset["remaining_life_years"]) * float(
        fleet["propellant_replenishment_cost_musd_per_km_s"]
    )
    service_cost = (
        float(action["variable_service_cost_musd"]) * float(orbit["service_cost_multiplier"])
        + fixed_per_client
        + routing_cost
    )

    useful_life = float(asset["remaining_life_years"])
    downtime = min(float(action["downtime_years"]), useful_life)
    output_value = (
        float(asset["annual_output_value_musd"])
        * max(useful_life - downtime, 0.0)
        * float(action["output_restoration_fraction"])
    )
    avoided_launch = float(asset["replacement_launch_cost_musd"]) * float(
        action["replacement_avoidance_fraction"]
    )
    remaining_asset_value = (
        float(asset["asset_value_musd"])
        * (useful_life / max(float(asset["design_life_years"]), 1e-12))
        * float(action["asset_value_preservation_fraction"])
    )
    recovered_value = float(asset["component_value_musd"]) * float(
        action["component_recovery_fraction"]
    ) + float(asset["material_value_musd"]) * float(action["material_recovery_fraction"])
    residual_value = float(asset["residual_value_musd"]) * float(action["residual_value_fraction"])
    success = 1.0 - float(action["service_failure_probability"])
    expected_benefit = success * (
        output_value
        + avoided_launch
        + remaining_asset_value
        + recovered_value
        + float(action["upgrade_incremental_value_musd"])
        + residual_value
    )
    downtime_cost = (
        float(asset["annual_output_value_musd"])
        * downtime
        * float(action["downtime_loss_fraction"])
    )
    risk_and_liability = float(action["service_failure_probability"]) * float(
        asset["asset_value_musd"]
    ) + float(action["debris_incident_probability"]) * float(
        governance["debris_liability_exposure_musd"]
    ) * float(orbit["debris_liability_multiplier"])
    depreciation = float(asset["asset_value_musd"]) * float(action["depreciation_fraction"])
    net = expected_benefit - service_cost - downtime_cost - risk_and_liability - depreciation
    break_even_service_cost = expected_benefit - downtime_cost - risk_and_liability - depreciation
    economic_viable = net >= 0.0
    return OrbitalServiceDecisionResult(
        orbit=orbit_name,
        asset_class=asset_name,
        fleet=fleet_name,
        action=action_name,
        technically_feasible=technically_feasible,
        technical_blockers=tuple(blockers),
        governance_ready=governance_ready,
        governance_dependencies=dependencies,
        annual_fleet_capacity=annual_capacity,
        fixed_cost_per_client_musd=fixed_per_client,
        routing_cost_per_client_musd=routing_cost,
        expected_lifetime_output_value_musd=output_value,
        avoided_replacement_launch_musd=avoided_launch,
        recovered_value_musd=recovered_value,
        expected_benefit_musd=expected_benefit,
        service_cost_musd=service_cost,
        downtime_cost_musd=downtime_cost,
        risk_and_liability_cost_musd=risk_and_liability,
        depreciation_cost_musd=depreciation,
        residual_value_musd=residual_value,
        net_value_musd=net,
        economic_viable=economic_viable,
        deployable=technically_feasible and economic_viable and governance_ready,
        break_even_service_cost_musd=break_even_service_cost,
    )


def rocket_propellant_required(
    final_mass_kg: float,
    *,
    delta_v_km_s: float,
    specific_impulse_s: float,
) -> float:
    """Return ideal propellant mass from Tsiolkovsky's rocket equation."""
    if final_mass_kg < 0.0 or delta_v_km_s < 0.0:
        raise ValueError("mass and delta-v must be nonnegative")
    if specific_impulse_s <= 0.0:
        raise ValueError("specific impulse must be positive")
    mass_ratio = math.exp(delta_v_km_s * 1000.0 / (9.80665 * specific_impulse_s))
    return float(final_mass_kg * (mass_ratio - 1.0))


def evaluate_transport_service(
    config: TransportServiceCase,
) -> TransportServiceResult:
    """Evaluate one explicitly origin–destination orbital-service case.

    Delta-v is converted into propellant by the rocket equation, never
    directly into dollars. The remaining vehicle, infrastructure, cadence,
    reliability, serviceability, and maturity terms are declared separately.
    """
    nonnegative = (
        "clients",
        "failure_rate_per_year",
        "serviceability_fraction",
        "clients_per_mission",
        "servicer_dry_mass_t",
        "parts_t_per_mission",
        "recovered_mass_t_per_mission",
        "delta_v_km_s",
        "propellant_cost_per_kg",
        "parts_cost_per_kg",
        "recovered_material_credit_per_kg",
        "operations_musd_per_mission",
        "servicer_capex_musd",
        "reuse_cycles",
        "fixed_infrastructure_musd",
        "infrastructure_life_years",
        "client_value_musd",
        "preserved_value_fraction",
        "lunar_industrial_maturity",
        "required_lunar_maturity",
    )
    if any(float(config[name]) < 0.0 for name in nonnegative):
        raise ValueError("transport-service inputs must be nonnegative")
    for name in (
        "failure_rate_per_year",
        "serviceability_fraction",
        "preserved_value_fraction",
        "lunar_industrial_maturity",
        "required_lunar_maturity",
    ):
        validate_unit_interval(config[name], name)
    if (
        float(config["clients_per_mission"]) <= 0.0
        or float(config["reuse_cycles"]) <= 0.0
        or float(config["infrastructure_life_years"]) <= 0.0
    ):
        raise ValueError("mission, reuse, and infrastructure denominators must be positive")

    serviceable_clients = (
        float(config["clients"])
        * float(config["failure_rate_per_year"])
        * float(config["serviceability_fraction"])
    )
    missions = serviceable_clients / float(config["clients_per_mission"])
    final_mass_kg = (
        float(config["servicer_dry_mass_t"]) + float(config["parts_t_per_mission"])
    ) * 1000.0
    propellant_kg = rocket_propellant_required(
        final_mass_kg,
        delta_v_km_s=float(config["delta_v_km_s"]),
        specific_impulse_s=float(config["specific_impulse_s"]),
    )
    mission_cost = (
        propellant_kg * float(config["propellant_cost_per_kg"]) / 1e6
        + float(config["parts_t_per_mission"]) * 1000.0 * float(config["parts_cost_per_kg"]) / 1e6
        + float(config["operations_musd_per_mission"])
        + float(config["servicer_capex_musd"]) / float(config["reuse_cycles"])
        - float(config["recovered_mass_t_per_mission"])
        * 1000.0
        * float(config["recovered_material_credit_per_kg"])
        / 1e6
    )
    mission_cost = max(mission_cost, 0.0)
    annual_cost = missions * mission_cost + float(config["fixed_infrastructure_musd"]) / float(
        config["infrastructure_life_years"]
    )
    preserved = (
        serviceable_clients
        * float(config["client_value_musd"])
        * float(config["preserved_value_fraction"])
    )
    available = not bool(config.get("requires_lunar_industry", False)) or float(
        config["lunar_industrial_maturity"]
    ) >= float(config["required_lunar_maturity"])
    denominator = serviceable_clients * float(config["preserved_value_fraction"])
    breakeven = annual_cost / denominator if denominator > 0.0 else None
    return TransportServiceResult(
        architecture=str(config["architecture"]),
        available=available,
        annual_missions=missions,
        propellant_t_per_mission=propellant_kg / 1000.0,
        annual_cost_musd=annual_cost,
        annual_preserved_value_musd=preserved,
        net_value_musd=preserved - annual_cost,
        breakeven_client_value_musd=breakeven,
    )


def _transfer_lifecycle_stock(
    stocks: FloatArray,
    indices: Mapping[str, int],
    flows: Mapping[str, FloatArray],
    step: int,
    source: str,
    target: str,
    amount: float,
    flow: str,
) -> float:
    """Move a bounded lifecycle quantity and record the associated flow."""
    moved = min(max(float(amount), 0.0), stocks[indices[source]])
    stocks[indices[source]] -= moved
    stocks[indices[target]] += moved
    flows[flow][step + 1] += moved
    return moved


def simulate_orbital_lifecycle(
    config: OrbitalLifecycleInputs,
    *,
    years: float = 20.0,
    dt: float = 0.1,
) -> LifecycleResult:
    """Simulate explicit repair, reuse, recycling, and debris state flows.

    All stocks use capacity-equivalent mass units, which makes the conservation
    check meaningful while keeping physical output and frontier-equivalent
    obsolescence conceptually separate.
    """
    if years <= 0.0 or dt <= 0.0:
        raise ValueError("years and dt must be positive")
    rates = (
        "degradation_per_year",
        "failure_per_year",
        "collision_loss_per_year",
        "degraded_to_service_per_year",
        "service_start_capacity_per_year",
        "repair_completion_per_year",
        "controlled_retirement_per_year",
        "obsolescence_per_year",
        "cannibalization_per_year",
        "recycling_per_year",
        "disposal_per_year",
        "debris_retrieval_per_year",
        "manufacturing_from_feedstock_per_year",
        "external_deployment_per_year",
    )
    if any(float(config[name]) < 0.0 for name in rates):
        raise ValueError("lifecycle rates and capacities must be nonnegative")
    repair_success = validate_unit_interval(config["repair_success_fraction"], "repair success")
    recycle_yield = validate_unit_interval(config["recycling_yield"], "recycling yield")
    retrieval_success = validate_unit_interval(
        config["retrieval_success_fraction"], "retrieval success"
    )
    initial = float(config["initial_operating"])
    if initial < 0.0:
        raise ValueError("initial operating stock must be nonnegative")

    steps = round(years / dt)
    t = np.arange(steps + 1, dtype=float) * dt
    stocks = np.zeros((steps + 1, len(LIFECYCLE_STATES)))
    stocks[0, 0] = initial
    flow_names = (
        "degraded",
        "failed",
        "collision_loss",
        "repair_started",
        "repair_return",
        "repair_failed",
        "retired",
        "obsoleted",
        "salvaged",
        "recycled",
        "recycling_waste",
        "disposed",
        "debris_retrieved",
        "manufactured",
        "external_deployment",
    )
    flows = {name: np.zeros(steps + 1) for name in flow_names}
    ix = {name: index for index, name in enumerate(LIFECYCLE_STATES)}
    irreversible_flow = 0.0
    operating_exposure = 0.0

    for k in range(steps):
        x = stocks[k].copy()
        operating_exposure += x[ix["operating"]] * dt

        _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "operating",
            "degraded",
            config["degradation_per_year"] * x[ix["operating"]] * dt,
            "degraded",
        )
        _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "operating",
            "awaiting_service",
            config["failure_per_year"] * x[ix["operating"]] * dt,
            "failed",
        )
        collision = _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "operating",
            "uncontrolled_debris",
            config["collision_loss_per_year"] * x[ix["operating"]] * dt,
            "collision_loss",
        )
        irreversible_flow += collision
        _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "degraded",
            "awaiting_service",
            config["degraded_to_service_per_year"] * x[ix["degraded"]] * dt,
            "failed",
        )
        _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "operating",
            "cannibalized",
            config["controlled_retirement_per_year"] * x[ix["operating"]] * dt,
            "retired",
        )
        _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "operating",
            "cannibalized",
            config["obsolescence_per_year"] * x[ix["operating"]] * dt,
            "obsoleted",
        )
        _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "awaiting_service",
            "under_repair",
            float(config["service_start_capacity_per_year"]) * dt,
            "repair_started",
        )
        completion = min(
            x[ix["under_repair"]],
            config["repair_completion_per_year"] * x[ix["under_repair"]] * dt,
        )
        x[ix["under_repair"]] -= completion
        returned = completion * repair_success
        failed_repair = completion - returned
        x[ix["operating"]] += returned
        x[ix["cannibalized"]] += failed_repair
        flows["repair_return"][k + 1] = returned
        flows["repair_failed"][k + 1] = failed_repair

        retrieved = (
            min(
                x[ix["uncontrolled_debris"]],
                config["debris_retrieval_per_year"] * x[ix["uncontrolled_debris"]] * dt,
            )
            * retrieval_success
        )
        x[ix["uncontrolled_debris"]] -= retrieved
        x[ix["salvaged"]] += retrieved
        flows["debris_retrieved"][k + 1] = retrieved
        irreversible_flow -= retrieved

        _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "cannibalized",
            "salvaged",
            config["cannibalization_per_year"] * x[ix["cannibalized"]] * dt,
            "salvaged",
        )
        disposed = _transfer_lifecycle_stock(
            x,
            ix,
            flows,
            k,
            "cannibalized",
            "disposed_waste",
            config["disposal_per_year"] * x[ix["cannibalized"]] * dt,
            "disposed",
        )
        irreversible_flow += disposed

        processed = min(
            x[ix["salvaged"]],
            config["recycling_per_year"] * x[ix["salvaged"]] * dt,
        )
        x[ix["salvaged"]] -= processed
        recycled = processed * recycle_yield
        waste = processed - recycled
        x[ix["recycled_feedstock"]] += recycled
        x[ix["disposed_waste"]] += waste
        flows["recycled"][k + 1] = recycled
        flows["recycling_waste"][k + 1] = waste
        irreversible_flow += waste

        manufactured = min(
            x[ix["recycled_feedstock"]],
            float(config["manufacturing_from_feedstock_per_year"]) * dt,
        )
        x[ix["recycled_feedstock"]] -= manufactured
        x[ix["operating"]] += manufactured
        flows["manufactured"][k + 1] = manufactured
        external = float(config["external_deployment_per_year"]) * dt
        x[ix["operating"]] += external
        flows["external_deployment"][k + 1] = external
        stocks[k + 1] = np.maximum(x, 0.0)

    diagnostic = (
        max(irreversible_flow, 0.0) / operating_exposure if operating_exposure > 0.0 else math.inf
    )
    return LifecycleResult(t, stocks, flows, diagnostic)


@dataclass(frozen=True)
class CommonCauseResult:
    maximum_loss: float
    maximum_loss_fraction: float
    budget_fraction: float
    passes: bool
    binding_hazard: str | None
    reserve_required: float


@dataclass(frozen=True)
class ClusterLayoutResult:
    layout: str
    total_nodes: int
    nodes_per_cluster: int
    clusters: int
    maximum_common_cause_fraction: float
    correlated_fragment_exposure: float
    shared_service_failure_fraction: float
    communications_burden_index: float
    concentration_benefit_index: float
    expected_loss_index: float
    passes_loss_budget: bool


def evaluate_cluster_layout(
    layout_name: str,
    layout: ClusterLayout,
    *,
    collision_exposure_index: float,
    common_cause_budget_fraction: float,
) -> ClusterLayoutResult:
    """Evaluate an explicit physical and logical failure-domain layout."""
    total_nodes = int(layout["total_nodes"])
    nodes_per_cluster = int(layout["nodes_per_cluster"])
    planes = int(layout["orbital_planes"])
    gateways = int(layout["independent_gateways"])
    control_domains = int(layout["independent_control_domains"])
    shells = int(layout["independent_shells"])
    if (
        min(
            total_nodes,
            nodes_per_cluster,
            planes,
            gateways,
            control_domains,
            shells,
        )
        <= 0
    ):
        raise ValueError("layout counts must be positive")
    if nodes_per_cluster > total_nodes:
        raise ValueError("nodes_per_cluster cannot exceed total_nodes")
    for name in (
        "altitude_dispersion_km",
        "inclination_dispersion_deg",
        "along_track_spacing_deg",
        "shared_power_fraction",
        "shared_navigation_fraction",
        "shared_software_fraction",
        "crosslink_latency_index",
    ):
        if float(layout[name]) < 0.0:
            raise ValueError(f"{name} must be nonnegative")
    budget = validate_unit_interval(
        common_cause_budget_fraction,
        "common_cause_budget_fraction",
    )
    clusters = math.ceil(total_nodes / nodes_per_cluster)
    physical_domain_fraction = nodes_per_cluster / total_nodes
    gateway_fraction = 1.0 / gateways
    control_fraction = 1.0 / control_domains
    shared_service_fraction = max(
        float(layout["shared_power_fraction"]),
        float(layout["shared_navigation_fraction"]),
        float(layout["shared_software_fraction"]),
        gateway_fraction,
        control_fraction,
    )
    maximum_common_cause = max(physical_domain_fraction, shared_service_fraction)
    fragment_correlation = (
        float(collision_exposure_index)
        * math.exp(-float(layout["altitude_dispersion_km"]) / 120.0)
        * math.exp(-float(layout["inclination_dispersion_deg"]) / 18.0)
        / math.sqrt(planes * shells)
        * min(
            1.0,
            12.0 / max(float(layout["along_track_spacing_deg"]), 1e-12),
        )
    )
    communications = (
        float(layout["crosslink_latency_index"])
        * math.log2(max(clusters, 2))
        * (1.0 + 0.10 * (shells - 1))
    )
    concentration_benefit = math.log1p(nodes_per_cluster) / (
        1.0 + 0.15 * (planes - 1) + 0.20 * (shells - 1) + 0.05 * communications
    )
    expected_loss = fragment_correlation * physical_domain_fraction + 0.50 * shared_service_fraction
    return ClusterLayoutResult(
        layout=layout_name,
        total_nodes=total_nodes,
        nodes_per_cluster=nodes_per_cluster,
        clusters=clusters,
        maximum_common_cause_fraction=maximum_common_cause,
        correlated_fragment_exposure=fragment_correlation,
        shared_service_failure_fraction=shared_service_fraction,
        communications_burden_index=communications,
        concentration_benefit_index=concentration_benefit,
        expected_loss_index=expected_loss,
        passes_loss_budget=maximum_common_cause <= budget + 1e-12,
    )


@dataclass(frozen=True)
class BreakupCloudResult:
    event: str
    t_days: FloatArray
    active_capacity: FloatArray
    fragment_cloud: FloatArray
    direct_loss_capacity: float
    expected_secondary_collisions: float
    expected_avoidance_maneuvers: float
    service_interruption_capacity_days: float
    repair_load_capacity: float
    time_to_restore_days: float | None


def simulate_breakup_cloud(
    nodes: Sequence[ConstellationNode],
    event: BreakupEvent,
    *,
    days: int = 365,
    dt_days: float = 1.0,
) -> BreakupCloudResult:
    """Propagate a stylized breakup cloud through explicit node geometry.

    Outputs are deterministic expected counts/capacity, not a conjunction
    forecast. Altitude, inclination, plane, and along-track phase all enter
    exposure. Secondary collisions grow the cloud; clearance removes it;
    repair begins after a declared delay and restores capacity at a bounded
    rate.
    """
    if days <= 0 or dt_days <= 0.0:
        raise ValueError("days and dt_days must be positive")
    if not nodes:
        raise ValueError("at least one constellation node is required")
    environment = event.get("environment")
    if environment is not None:
        nodes = tuple(node for node in nodes if node.get("environment") == environment)
    if not nodes:
        raise ValueError("event environment has no constellation nodes")
    capacities = np.asarray([float(node["capacity"]) for node in nodes])
    if np.any(capacities <= 0.0):
        raise ValueError("node capacities must be positive")
    if "origin_node_name" in event:
        matches = [
            index
            for index, node in enumerate(nodes)
            if node.get("name") == event["origin_node_name"]
        ]
        if len(matches) != 1:
            raise ValueError("origin_node_name must identify exactly one node")
        origin = matches[0]
    else:
        origin_value = event.get("origin_node")
        if origin_value is None:
            raise ValueError("breakup event requires origin_node_name or origin_node")
        origin = int(origin_value)
        if origin < 0 or origin >= len(nodes):
            raise ValueError("origin_node is out of range")
    for name in (
        "initial_fragments",
        "fragment_clearance_per_day",
        "secondary_fragments_per_collision",
        "collision_kernel_per_fragment_day",
        "altitude_scale_km",
        "inclination_scale_deg",
        "cloud_spread_deg_per_day",
        "tracking_fraction",
        "maneuver_success_fraction",
        "repair_delay_days",
        "repair_capacity_per_day",
    ):
        if float(event[name]) < 0.0:
            raise ValueError(f"{name} must be nonnegative")
    tracking = validate_unit_interval(event["tracking_fraction"], "tracking_fraction")
    maneuver = validate_unit_interval(
        event["maneuver_success_fraction"],
        "maneuver_success_fraction",
    )
    clearance = validate_unit_interval(
        event["fragment_clearance_per_day"],
        "fragment_clearance_per_day",
    )

    steps = round(days / dt_days)
    t = np.arange(steps + 1, dtype=float) * dt_days
    active_by_node = capacities.copy()
    lost_inventory = np.zeros_like(capacities)
    origin_loss = active_by_node[origin]
    active_by_node[origin] = 0.0
    lost_inventory[origin] = origin_loss
    active_capacity = np.zeros(steps + 1)
    active_capacity[0] = active_by_node.sum()
    cloud = np.zeros(steps + 1)
    cloud[0] = float(event["initial_fragments"])
    secondary_total = 0.0
    maneuvers_total = 0.0
    interruption = 0.0
    repair_load = origin_loss
    initial_total = float(capacities.sum())
    restore_threshold = float(event.get("restore_fraction", 0.95)) * initial_total
    restore_time: float | None = None
    origin_node = nodes[origin]

    for k in range(steps):
        day = t[k]
        spread = max(
            float(event["initial_cloud_width_deg"])
            + float(event["cloud_spread_deg_per_day"]) * day,
            1e-9,
        )
        secondary_step = 0.0
        for index, node in enumerate(nodes):
            if active_by_node[index] <= 0.0:
                continue
            altitude = math.exp(
                -abs(float(node["altitude_km"]) - float(origin_node["altitude_km"]))
                / max(float(event["altitude_scale_km"]), 1e-12)
            )
            inclination = math.exp(
                -abs(float(node["inclination_deg"]) - float(origin_node["inclination_deg"]))
                / max(float(event["inclination_scale_deg"]), 1e-12)
            )
            plane = (
                1.0
                if int(node["plane"]) == int(origin_node["plane"])
                else float(event["cross_plane_exposure_fraction"])
            )
            phase = abs(
                (float(node["along_track_deg"]) - float(origin_node["along_track_deg"]) + 180.0)
                % 360.0
                - 180.0
            )
            along_track = math.exp(-0.5 * (phase / spread) ** 2)
            exposure = altitude * inclination * plane * along_track
            conjunctions = (
                cloud[k] * float(event["collision_kernel_per_fragment_day"]) * exposure * dt_days
            )
            avoided = conjunctions * tracking * maneuver
            maneuvers_total += avoided
            residual = max(conjunctions - avoided, 0.0)
            loss = min(active_by_node[index], residual * capacities[index])
            active_by_node[index] -= loss
            lost_inventory[index] += loss
            secondary_step += loss / capacities[index]
            repair_load += loss
        secondary_total += secondary_step
        cloud[k + 1] = max(
            cloud[k] * (1.0 - clearance * dt_days)
            + secondary_step * float(event["secondary_fragments_per_collision"]),
            0.0,
        )
        if day >= float(event["repair_delay_days"]):
            available_repair = float(event["repair_capacity_per_day"]) * dt_days
            for index in np.argsort(-lost_inventory):
                repaired = min(lost_inventory[index], available_repair)
                lost_inventory[index] -= repaired
                active_by_node[index] += repaired
                available_repair -= repaired
                if available_repair <= 1e-15:
                    break
        active_capacity[k + 1] = active_by_node.sum()
        interruption += (initial_total - active_capacity[k + 1]) * dt_days
        if (
            restore_time is None
            and active_capacity[k + 1] >= restore_threshold
            and day >= float(event["repair_delay_days"])
        ):
            restore_time = t[k + 1]
    return BreakupCloudResult(
        event=str(event["name"]),
        t_days=t,
        active_capacity=active_capacity,
        fragment_cloud=cloud,
        direct_loss_capacity=origin_loss,
        expected_secondary_collisions=secondary_total,
        expected_avoidance_maneuvers=maneuvers_total,
        service_interruption_capacity_days=interruption,
        repair_load_capacity=repair_load,
        time_to_restore_days=restore_time,
    )


@dataclass(frozen=True)
class DegradedControlResult:
    scenario: str
    detected_conjunctions: float
    executed_avoidance_maneuvers: float
    conflicting_maneuvers: float
    residual_unsafe_conjunctions: float
    collision_risk_index: float
    safe_before_fallback: bool
    fallback_actions: tuple[str, ...]
    residual_risk_after_fallback: float
    safe_after_fallback: bool


def evaluate_degraded_conjunction_control(
    scenario_name: str,
    scenario: DegradedControlScenario,
    *,
    conjunctions: float,
    collision_probability_per_unsafe_conjunction: float,
    risk_limit: float,
) -> DegradedControlResult:
    """Stress tracking, communication, navigation, and coordination together."""
    if min(conjunctions, collision_probability_per_unsafe_conjunction, risk_limit) < 0:
        raise ValueError("conjunction and risk quantities must be nonnegative")
    tracking = validate_unit_interval(scenario["tracking_fraction"], "tracking_fraction")
    communications = validate_unit_interval(
        scenario["communications_fraction"],
        "communications_fraction",
    )
    navigation = validate_unit_interval(
        scenario["navigation_fraction"],
        "navigation_fraction",
    )
    coordination = validate_unit_interval(
        scenario["coordination_fraction"],
        "coordination_fraction",
    )
    independent = validate_unit_interval(
        scenario["independent_fallback_fraction"],
        "independent_fallback_fraction",
    )
    detected = conjunctions * tracking * navigation
    executable = detected * communications * navigation
    conflicts = executable * (1.0 - coordination)
    executed = executable - conflicts
    unsafe = max(conjunctions - executed, 0.0)
    risk = unsafe * collision_probability_per_unsafe_conjunction
    actions: list[str] = []
    fallback_factor = 1.0
    if risk > risk_limit:
        actions.extend(("pause_deployment", "increase_spacing"))
        fallback_factor *= float(scenario["cadence_risk_multiplier"])
        fallback_factor *= float(scenario["spacing_risk_multiplier"])
    if min(tracking, communications, navigation) < 0.8:
        actions.extend(("independent_tracking", "local_safe_mode"))
        fallback_factor *= 1.0 - 0.65 * independent
    if coordination < 0.8:
        actions.extend(("isolate_control_domains", "deterministic_right_of_way"))
        fallback_factor *= float(scenario["coordination_fallback_multiplier"])
    after = risk * fallback_factor
    return DegradedControlResult(
        scenario=scenario_name,
        detected_conjunctions=detected,
        executed_avoidance_maneuvers=executed,
        conflicting_maneuvers=conflicts,
        residual_unsafe_conjunctions=unsafe,
        collision_risk_index=risk,
        safe_before_fallback=risk <= risk_limit,
        fallback_actions=tuple(dict.fromkeys(actions)),
        residual_risk_after_fallback=after,
        safe_after_fallback=after <= risk_limit,
    )


@dataclass(frozen=True)
class MitigationPortfolioResult:
    deployment_cadence: float
    disposal_reliability: float
    removal_rate: float
    shielding_mass_fraction: float
    cluster_cap_fraction: float
    shell_diversity: int
    servicer_fleet_size: int
    repair_recycling_capacity: float
    residual_risk_index: float
    lifecycle_cost_index: float
    delivered_capacity_index: float


def evaluate_mitigation_portfolio(
    values: Mapping[str, float],
    config: MitigationPortfolioConfig,
) -> MitigationPortfolioResult:
    """Evaluate one mitigation portfolio without collapsing its objectives."""
    cadence = float(values["deployment_cadence"])
    disposal = validate_unit_interval(values["disposal_reliability"], "disposal")
    removal = float(values["removal_rate"])
    shielding = float(values["shielding_mass_fraction"])
    cluster_cap = validate_unit_interval(values["cluster_cap_fraction"], "cluster cap")
    shell_diversity = int(values["shell_diversity"])
    servicers = int(values["servicer_fleet_size"])
    repair = float(values["repair_recycling_capacity"])
    if min(cadence, removal, shielding, shell_diversity, servicers, repair) < 0:
        raise ValueError("mitigation inputs must be nonnegative")
    if shell_diversity < 1:
        raise ValueError("shell_diversity must be at least one")
    risk = (
        float(config["base_risk_index"])
        * cadence ** float(config["cadence_exponent"])
        * (1.0 - disposal + float(config["disposal_floor"]))
        / (
            1.0
            + float(config["removal_effectiveness"]) * removal
            + float(config["small_debris_shielding_effectiveness"]) * shielding
            + float(config["servicer_effectiveness"]) * servicers
            + float(config["repair_effectiveness"]) * repair
        )
        * cluster_cap
        / math.sqrt(shell_diversity)
    )
    cost = (
        float(config["cadence_cost"]) * cadence
        + float(config["disposal_cost"]) * disposal
        + float(config["removal_cost"]) * removal
        + float(config["shielding_cost"]) * shielding
        + float(config["shell_diversity_cost"]) * shell_diversity
        + float(config["servicer_cost"]) * servicers
        + float(config["repair_cost"]) * repair
    )
    delivered = (
        cadence
        * (1.0 - shielding)
        * (1.0 - float(config["shell_distribution_capacity_penalty"]) * (shell_diversity - 1))
        - risk
        + float(config["repair_capacity_return"]) * repair
    )
    return MitigationPortfolioResult(
        deployment_cadence=cadence,
        disposal_reliability=disposal,
        removal_rate=removal,
        shielding_mass_fraction=shielding,
        cluster_cap_fraction=cluster_cap,
        shell_diversity=shell_diversity,
        servicer_fleet_size=servicers,
        repair_recycling_capacity=repair,
        residual_risk_index=max(risk, 0.0),
        lifecycle_cost_index=max(cost, 0.0),
        delivered_capacity_index=max(delivered, 0.0),
    )


@dataclass(frozen=True)
class MultiOperatorCapacityResult:
    shell: str
    planned_nodes: int
    carrying_capacity_nodes: int
    coordinated_fraction: float
    predicted_conjunction_workload: float
    uncoordinated_workload: float
    capacity_compliant: bool
    governance_compliant: bool
    admissible: bool


def evaluate_multi_operator_capacity(
    shell_name: str,
    shell: MultiOperatorShell,
    operators: Sequence[OrbitalOperator],
) -> MultiOperatorCapacityResult:
    """Evaluate shared-shell carrying capacity and coordination compliance."""
    planned = sum(int(operator["planned_nodes"]) for operator in operators)
    if planned < 0:
        raise ValueError("planned node counts must be nonnegative")
    for operator in operators:
        for field in (
            "tracking_data_share_fraction",
            "maneuver_coordination_fraction",
            "disposal_compliance_fraction",
        ):
            validate_unit_interval(operator[field], field)
    pair_coefficient = float(shell["conjunctions_per_node_pair_year"])
    workload_limit = float(shell["maximum_coordinated_conjunctions_per_year"])
    if pair_coefficient <= 0.0 or workload_limit < 0.0:
        raise ValueError("shell workload coefficients must be positive")
    weights = np.asarray([int(operator["planned_nodes"]) for operator in operators])
    total_weight = float(weights.sum())
    if total_weight > 0.0:
        coordinated = float(
            np.average(
                [
                    min(
                        float(operator["tracking_data_share_fraction"]),
                        float(operator["maneuver_coordination_fraction"]),
                        float(operator["disposal_compliance_fraction"]),
                    )
                    for operator in operators
                ],
                weights=weights,
            )
        )
    else:
        coordinated = 1.0
    workload = pair_coefficient * planned * max(planned - 1, 0) / 2.0
    uncoordinated = workload * (1.0 - coordinated)
    discriminant = 1.0 + 8.0 * workload_limit / pair_coefficient
    carrying = math.floor((1.0 + math.sqrt(discriminant)) / 2.0)
    capacity_compliant = planned <= carrying
    governance_compliant = all(
        bool(operator["authorization_valid"])
        and min(
            float(operator["tracking_data_share_fraction"]),
            float(operator["maneuver_coordination_fraction"]),
            float(operator["disposal_compliance_fraction"]),
        )
        >= float(shell["minimum_operator_compliance_fraction"])
        for operator in operators
    )
    return MultiOperatorCapacityResult(
        shell=shell_name,
        planned_nodes=planned,
        carrying_capacity_nodes=carrying,
        coordinated_fraction=coordinated,
        predicted_conjunction_workload=workload,
        uncoordinated_workload=uncoordinated,
        capacity_compliant=capacity_compliant,
        governance_compliant=governance_compliant,
        admissible=capacity_compliant and governance_compliant,
    )


def common_cause_loss_budget(
    capacities: Sequence[float],
    hazard_sets: Mapping[str, Sequence[int]],
    *,
    epsilon: float,
) -> CommonCauseResult:
    """Evaluate the largest capacity loss from one credible hazard set."""
    cap = np.asarray(capacities, dtype=float)
    if cap.ndim != 1 or np.any(cap < 0.0):
        raise ValueError("capacities must be a nonnegative vector")
    epsilon = validate_unit_interval(epsilon, "epsilon")
    total = float(cap.sum())
    losses: dict[str, float] = {}
    for name, indices in hazard_sets.items():
        unique = tuple({int(index) for index in indices})
        if any(index < 0 or index >= len(cap) for index in unique):
            raise ValueError(f"hazard set {name!r} contains an invalid node")
        losses[name] = float(cap[list(unique)].sum()) if unique else 0.0
    binding = max(losses, key=lambda name: losses[name]) if losses else None
    maximum = losses[binding] if binding is not None else 0.0
    fraction = maximum / total if total > 0.0 else 0.0
    return CommonCauseResult(
        maximum,
        fraction,
        epsilon,
        fraction <= epsilon + 1e-12,
        binding,
        max(maximum - epsilon * total, 0.0),
    )


def debris_control_actions(
    metrics: Mapping[str, float],
    thresholds: Mapping[str, float],
) -> tuple[str, ...]:
    """Return deterministic control actions for crossed shell-state triggers."""
    unknown = set(metrics) - set(thresholds)
    if unknown:
        raise ValueError(f"missing debris thresholds for {sorted(unknown)}")
    crossed = {name for name, value in metrics.items() if float(value) > float(thresholds[name])}
    actions: list[str] = []
    if crossed & {
        "creation_clearance_ratio",
        "expected_hazardous_descendants",
        "derelict_mass",
    }:
        actions.extend(("pause_deployment", "dispatch_active_removal"))
    if crossed & {
        "conjunction_probability",
        "maneuver_workload",
        "avoidance_propellant_fraction_used",
    }:
        actions.extend(("increase_spacing", "reserve_maneuver_propellant"))
    if crossed & {"tracking_uncertainty", "communications_outage_fraction"}:
        actions.extend(("reduce_cluster_cap", "isolate_failure_domains"))
    if "disposal_failure_fraction" in crossed:
        actions.extend(("tighten_disposal_reliability", "retire_shell"))
    return tuple(dict.fromkeys(actions))
