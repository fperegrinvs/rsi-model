"""Generated-artifact component for the integrated pipeline."""

from __future__ import annotations

import csv
import itertools

import numpy as np

from rsimodel.extensions import (
    ClusterLayoutResult,
    MitigationPortfolioResult,
    common_cause_loss_budget,
    debris_control_actions,
    evaluate_cluster_layout,
    evaluate_degraded_conjunction_control,
    evaluate_mitigation_portfolio,
    evaluate_multi_operator_capacity,
    evaluate_orbital_service_decision,
    evaluate_transport_service,
    simulate_breakup_cloud,
    simulate_orbital_lifecycle,
)

from .integrated_artifacts import (
    ArtifactWorkspace,
)
from .integrated_types import DebrisRuns, IntegratedParams, ShellDebrisResult
from .orbital_config import (
    TransportServiceCase,
    lifecycle_inputs,
    replace_transport_service_case,
)


def _transport_sensitivity_case(
    base: TransportServiceCase,
    axis: str,
    value: float | None,
) -> TransportServiceCase:
    if axis == "central" or value is None:
        return replace_transport_service_case(base)
    if axis == "client_value_musd":
        return replace_transport_service_case(base, client_value_musd=value)
    if axis == "failure_rate_per_year":
        return replace_transport_service_case(base, failure_rate_per_year=value)
    if axis == "serviceability_fraction":
        return replace_transport_service_case(base, serviceability_fraction=value)
    if axis == "clients":
        return replace_transport_service_case(base, clients=value)
    if axis == "recovered_mass_t_per_mission":
        return replace_transport_service_case(base, recovered_mass_t_per_mission=value)
    if axis == "reuse_cycles":
        return replace_transport_service_case(base, reuse_cycles=value)
    if axis == "lunar_industrial_maturity":
        return replace_transport_service_case(base, lunar_industrial_maturity=value)
    raise ValueError(f"unknown transport sensitivity axis {axis!r}")


def _write_orbital_extension_tables(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    debris_runs: DebrisRuns,
    shell_debris: ShellDebrisResult,
) -> None:
    lifecycle = simulate_orbital_lifecycle(
        params.orbital_lifecycle,
        years=20.0,
        dt=0.1,
    )
    with open(
        workspace.table_directory / "orbital_lifecycle_states.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "year",
                *(
                    f"{name}_capacity_equivalent"
                    for name in (
                        "operating",
                        "degraded",
                        "awaiting_service",
                        "under_repair",
                        "cannibalized",
                        "salvaged",
                        "recycled_feedstock",
                        "disposed_waste",
                        "uncontrolled_debris",
                    )
                ),
                "gross_failures",
                "repair_return",
                "recycled_return",
                "debris_retrieved",
                "effective_irreversible_loss_per_year",
                "source_class",
            ]
        )
        for k, year in enumerate(lifecycle.t):
            w.writerow(
                [
                    f"{year:.6f}",
                    *(f"{value:.9f}" for value in lifecycle.stocks[k]),
                    f"{lifecycle.flows['failed'][k]:.9f}",
                    f"{lifecycle.flows['repair_return'][k]:.9f}",
                    f"{lifecycle.flows['recycled'][k]:.9f}",
                    f"{lifecycle.flows['debris_retrieved'][k]:.9f}",
                    f"{lifecycle.effective_irreversible_loss_per_year:.9f}",
                    params.orbital_lifecycle["source_class"],
                ]
            )

    lifecycle_cfg = params.orbital_lifecycle
    with open(
        workspace.table_directory / "orbital_lifecycle_strategy_comparison.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "portfolio",
                "docking_refueling_interfaces",
                "modular_replaceable_units",
                "accessible_fasteners_ports_grapples",
                "material_passports_separability",
                "passivation_and_safe_state",
                "machine_readable_service_manuals",
                "mass_penalty_fraction",
                "repair_success_fraction",
                "recycling_yield",
                "capture_rate_multiplier",
                "operating_capacity_year20",
                "repair_return_cumulative",
                "recycled_return_cumulative",
                "uncontrolled_debris_year20",
                "effective_irreversible_loss_per_year",
                "source_class",
            ]
        )
        for portfolio, design in lifecycle_cfg["serviceability_portfolios"].items():
            mass_multiplier = 1.0 + float(design["mass_penalty_fraction"])
            scenario = lifecycle_inputs(
                lifecycle_cfg,
                repair_success_fraction=min(
                    float(lifecycle_cfg["repair_success_fraction"])
                    * float(design["repair_success_multiplier"]),
                    1.0,
                ),
                recycling_yield=min(
                    float(lifecycle_cfg["recycling_yield"])
                    * float(design["recycling_yield_multiplier"]),
                    1.0,
                ),
                service_start_capacity_per_year=(
                    float(lifecycle_cfg["service_start_capacity_per_year"])
                    * float(design["capture_rate_multiplier"])
                ),
                debris_retrieval_per_year=(
                    float(lifecycle_cfg["debris_retrieval_per_year"])
                    * float(design["capture_rate_multiplier"])
                ),
                external_deployment_per_year=(
                    float(lifecycle_cfg["external_deployment_per_year"]) / mass_multiplier
                ),
                manufacturing_from_feedstock_per_year=(
                    float(lifecycle_cfg["manufacturing_from_feedstock_per_year"]) / mass_multiplier
                ),
            )
            result = simulate_orbital_lifecycle(
                scenario,
                years=20.0,
                dt=0.1,
            )
            w.writerow(
                [
                    portfolio,
                    f"{design['docking_refueling_interfaces']:.6f}",
                    f"{design['modular_replaceable_units']:.6f}",
                    f"{design['accessible_fasteners_ports_grapples']:.6f}",
                    f"{design['material_passports_separability']:.6f}",
                    f"{design['passivation_and_safe_state']:.6f}",
                    f"{design['machine_readable_service_manuals']:.6f}",
                    f"{design['mass_penalty_fraction']:.6f}",
                    f"{scenario['repair_success_fraction']:.6f}",
                    f"{scenario['recycling_yield']:.6f}",
                    f"{design['capture_rate_multiplier']:.6f}",
                    f"{result.state('operating')[-1]:.9f}",
                    f"{result.flows['repair_return'].sum():.9f}",
                    f"{result.flows['recycled'].sum():.9f}",
                    f"{result.state('uncontrolled_debris')[-1]:.9f}",
                    f"{result.effective_irreversible_loss_per_year:.9f}",
                    lifecycle_cfg["source_class"],
                ]
            )

    transport_cfg = params.orbital_transport_service
    with open(
        workspace.table_directory / "orbital_transport_service_network.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "case",
                "sensitivity_axis",
                "sensitivity_value",
                "architecture",
                "origin",
                "destination",
                "delta_v_km_s",
                "delta_v_source",
                "specific_impulse_s",
                "propellant_source",
                "clients",
                "failure_rate_per_year",
                "serviceability_fraction",
                "reuse_cycles",
                "recovered_mass_t_per_mission",
                "lunar_industrial_maturity",
                "available",
                "annual_missions",
                "propellant_t_per_mission",
                "annual_cost_musd",
                "annual_preserved_value_musd",
                "net_value_musd",
                "breakeven_client_value_musd",
                "orbit_plane_distribution",
                "source_class",
            ]
        )
        sensitivity_axes = {
            "central": (None,),
            "client_value_musd": (40.0, 80.0, 160.0),
            "failure_rate_per_year": (0.02, 0.05, 0.10),
            "serviceability_fraction": (0.40, 0.70, 0.90),
            "clients": (50.0, 200.0, 1000.0),
            "recovered_mass_t_per_mission": (0.0, 0.10, 0.40),
            "reuse_cycles": (2.0, 8.0, 20.0),
            "lunar_industrial_maturity": (0.30, 0.70, 1.00),
        }
        for case_name, base_case in transport_cfg["cases"].items():
            for axis, values in sensitivity_axes.items():
                for value in values:
                    scenario = _transport_sensitivity_case(base_case, axis, value)
                    result = evaluate_transport_service(scenario)
                    w.writerow(
                        [
                            case_name,
                            axis,
                            "" if value is None else f"{value:g}",
                            scenario["architecture"],
                            scenario["origin"],
                            scenario["destination"],
                            f"{scenario['delta_v_km_s']:.6f}",
                            scenario["delta_v_source"],
                            f"{scenario['specific_impulse_s']:.6f}",
                            scenario["propellant_source"],
                            f"{scenario['clients']:.6f}",
                            f"{scenario['failure_rate_per_year']:.6f}",
                            f"{scenario['serviceability_fraction']:.6f}",
                            f"{scenario['reuse_cycles']:.6f}",
                            f"{scenario['recovered_mass_t_per_mission']:.6f}",
                            f"{scenario['lunar_industrial_maturity']:.6f}",
                            int(result.available),
                            f"{result.annual_missions:.9f}",
                            f"{result.propellant_t_per_mission:.9f}",
                            f"{result.annual_cost_musd:.9f}",
                            f"{result.annual_preserved_value_musd:.9f}",
                            f"{result.net_value_musd:.9f}",
                            (
                                ""
                                if result.breakeven_client_value_musd is None
                                else f"{result.breakeven_client_value_musd:.9f}"
                            ),
                            scenario["orbit_plane_distribution"],
                            transport_cfg["source_class"],
                        ]
                    )

    with open(
        workspace.table_directory / "orbital_transport_break_even_surface.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "case",
                "architecture",
                "origin",
                "destination",
                "orbit_plane_distribution",
                "propellant_source",
                "client_value_musd",
                "failure_rate_per_year",
                "serviceability_fraction",
                "clients",
                "recovered_mass_t_per_mission",
                "reuse_cycles",
                "lunar_industrial_maturity",
                "available",
                "annual_cost_musd",
                "annual_preserved_value_musd",
                "net_value_musd",
                "breakeven_client_value_musd",
                "economically_positive",
                "source_class",
            ]
        )
        for case_name, base_case in transport_cfg["cases"].items():
            for client_value in (40.0, 120.0, 240.0):
                for failure_rate in (0.02, 0.07):
                    for serviceability in (0.40, 0.80):
                        for clients in (50.0, 500.0):
                            for recovered_mass in (0.0, 0.30):
                                for reuse_cycles in (3.0, 15.0):
                                    for maturity in (0.30, 0.80):
                                        scenario = replace_transport_service_case(
                                            base_case,
                                            client_value_musd=client_value,
                                            failure_rate_per_year=failure_rate,
                                            serviceability_fraction=serviceability,
                                            clients=clients,
                                            recovered_mass_t_per_mission=recovered_mass,
                                            reuse_cycles=reuse_cycles,
                                            lunar_industrial_maturity=maturity,
                                        )
                                        result = evaluate_transport_service(scenario)
                                        w.writerow(
                                            [
                                                case_name,
                                                scenario["architecture"],
                                                scenario["origin"],
                                                scenario["destination"],
                                                scenario["orbit_plane_distribution"],
                                                scenario["propellant_source"],
                                                f"{client_value:.6f}",
                                                f"{failure_rate:.6f}",
                                                f"{serviceability:.6f}",
                                                f"{clients:.6f}",
                                                f"{recovered_mass:.6f}",
                                                f"{reuse_cycles:.6f}",
                                                f"{maturity:.6f}",
                                                int(result.available),
                                                f"{result.annual_cost_musd:.9f}",
                                                (f"{result.annual_preserved_value_musd:.9f}"),
                                                f"{result.net_value_musd:.9f}",
                                                (
                                                    ""
                                                    if result.breakeven_client_value_musd is None
                                                    else (
                                                        f"{result.breakeven_client_value_musd:.9f}"
                                                    )
                                                ),
                                                int(
                                                    result.available and result.net_value_musd > 0.0
                                                ),
                                                transport_cfg["source_class"],
                                            ]
                                        )

    strategy_cfg = params.orbital_service_strategy
    decision_rows = []
    for orbit_name, orbit in strategy_cfg["orbits"].items():
        for asset_name, asset in strategy_cfg["asset_classes"].items():
            for fleet_name, fleet in strategy_cfg["fleets"].items():
                for action_name, action in strategy_cfg["actions"].items():
                    decision_rows.append(
                        evaluate_orbital_service_decision(
                            orbit_name=orbit_name,
                            orbit=orbit,
                            asset_name=asset_name,
                            asset=asset,
                            fleet_name=fleet_name,
                            fleet=fleet,
                            action_name=action_name,
                            action=action,
                            governance=strategy_cfg["governance"],
                        )
                    )

    with open(
        workspace.table_directory / "orbital_service_decision_comparison.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "orbit",
                "asset_class",
                "fleet",
                "action",
                "technically_feasible",
                "technical_blockers",
                "economic_viable",
                "governance_ready",
                "deployable",
                "governance_dependencies",
                "annual_fleet_capacity",
                "fixed_cost_per_client_musd",
                "routing_cost_per_client_musd",
                "expected_lifetime_output_value_musd",
                "avoided_replacement_launch_musd",
                "recovered_value_musd",
                "expected_benefit_musd",
                "service_cost_musd",
                "downtime_cost_musd",
                "risk_and_liability_cost_musd",
                "depreciation_cost_musd",
                "residual_value_musd",
                "net_value_musd",
                "break_even_service_cost_musd",
                "currency_year",
                "source_class",
                "evidence_boundary",
            ]
        )
        for row in decision_rows:
            w.writerow(
                [
                    row.orbit,
                    row.asset_class,
                    row.fleet,
                    row.action,
                    int(row.technically_feasible),
                    ";".join(row.technical_blockers),
                    int(row.economic_viable),
                    int(row.governance_ready),
                    int(row.deployable),
                    ";".join(row.governance_dependencies),
                    f"{row.annual_fleet_capacity:.9f}",
                    f"{row.fixed_cost_per_client_musd:.9f}",
                    f"{row.routing_cost_per_client_musd:.9f}",
                    f"{row.expected_lifetime_output_value_musd:.9f}",
                    f"{row.avoided_replacement_launch_musd:.9f}",
                    f"{row.recovered_value_musd:.9f}",
                    f"{row.expected_benefit_musd:.9f}",
                    f"{row.service_cost_musd:.9f}",
                    f"{row.downtime_cost_musd:.9f}",
                    f"{row.risk_and_liability_cost_musd:.9f}",
                    f"{row.depreciation_cost_musd:.9f}",
                    f"{row.residual_value_musd:.9f}",
                    f"{row.net_value_musd:.9f}",
                    f"{row.break_even_service_cost_musd:.9f}",
                    strategy_cfg["currency_year"],
                    strategy_cfg["source_class"],
                    strategy_cfg["evidence_boundary"].strip(),
                ]
            )

    with open(
        workspace.table_directory / "orbital_regime_assumptions.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "orbit",
                "family",
                "rendezvous_delta_v_km_s",
                "inclination_change_multiplier",
                "routing_multiplier",
                "service_cost_multiplier",
                "stationkeeping_m_s_per_year",
                "residence_time_years",
                "atmospheric_clearance",
                "radiation_index",
                "debris_exposure_index",
                "tracking_coverage_fraction",
                "disposal_route",
                "disposal_delta_v_km_s",
                "debris_liability_multiplier",
                "relocation_supported",
                "source_class",
            ]
        )
        for orbit_name, orbit in strategy_cfg["orbits"].items():
            w.writerow(
                [
                    orbit_name,
                    orbit["family"],
                    f"{orbit['rendezvous_delta_v_km_s']:.6f}",
                    f"{orbit['inclination_change_multiplier']:.6f}",
                    f"{orbit['routing_multiplier']:.6f}",
                    f"{orbit['service_cost_multiplier']:.6f}",
                    f"{orbit['stationkeeping_m_s_per_year']:.6f}",
                    f"{orbit['residence_time_years']:.6f}",
                    orbit["atmospheric_clearance"],
                    f"{orbit['radiation_index']:.6f}",
                    f"{orbit['debris_exposure_index']:.6f}",
                    f"{orbit['tracking_coverage_fraction']:.6f}",
                    orbit["disposal_route"],
                    f"{orbit['disposal_delta_v_km_s']:.6f}",
                    f"{orbit['debris_liability_multiplier']:.6f}",
                    int(orbit["relocation_supported"]),
                    strategy_cfg["source_class"],
                ]
            )

    with open(
        workspace.table_directory / "orbital_fleet_amortization.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "orbit",
                "fleet",
                "servicers",
                "has_depot",
                "has_recycling_plant",
                "annual_fleet_capacity",
                "fixed_cost_per_client_musd",
                "routing_cost_per_client_musd",
                "scheduling_multiplier",
                "congestion_multiplier",
                "source_class",
            ]
        )
        for orbit_name in strategy_cfg["orbits"]:
            for fleet_name, fleet in strategy_cfg["fleets"].items():
                row = next(
                    item
                    for item in decision_rows
                    if item.orbit == orbit_name
                    and item.asset_class == "high_value_serviceable"
                    and item.fleet == fleet_name
                    and item.action == "replace"
                )
                w.writerow(
                    [
                        orbit_name,
                        fleet_name,
                        f"{fleet['servicers']:.6f}",
                        int(fleet["has_depot"]),
                        int(fleet["has_recycling_plant"]),
                        f"{row.annual_fleet_capacity:.9f}",
                        f"{row.fixed_cost_per_client_musd:.9f}",
                        f"{row.routing_cost_per_client_musd:.9f}",
                        f"{fleet['scheduling_multiplier']:.6f}",
                        f"{fleet['congestion_multiplier']:.6f}",
                        strategy_cfg["source_class"],
                    ]
                )

    with open(
        workspace.table_directory / "orbital_governance_constraints.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "constraint",
                "evidence_status",
                "authoritative_basis",
                "affected_actions",
                "blocks_deployable_claim",
                "source_class",
            ]
        )
        evidence = strategy_cfg["governance"]["evidence_status"]
        basis = strategy_cfg["governance"]["authoritative_basis"]
        for constraint, status in evidence.items():
            affected = [
                action_name
                for action_name, action in strategy_cfg["actions"].items()
                if constraint in action["governance_dependencies"]
            ]
            w.writerow(
                [
                    constraint,
                    status,
                    basis[constraint],
                    ";".join(affected),
                    int(status != "validated"),
                    (
                        "LEGAL_REQUIREMENT"
                        if basis[constraint] != "ASSUMPTION"
                        else strategy_cfg["source_class"]
                    ),
                ]
            )

    control_cfg = params.orbital_control
    budget = common_cause_loss_budget(
        control_cfg["node_capacities"],
        control_cfg["hazard_sets"],
        epsilon=control_cfg["common_cause_budget_fraction"],
    )
    control_metrics = {
        "creation_clearance_ratio": max(result.creation_clearance_ratio for result in debris_runs),
        "expected_hazardous_descendants": float(np.max(shell_debris.branching_ratio_by_shell)),
        "derelict_mass": float(shell_debris.intact_derelicts[-1].sum()),
        "conjunction_probability": 0.0,
        "maneuver_workload": 0.0,
        "avoidance_propellant_fraction_used": 0.0,
        "tracking_uncertainty": 0.0,
        "communications_outage_fraction": 0.0,
        "disposal_failure_fraction": (
            1.0 - params.orbital_mass_and_shell_debris["controlled_disposal_fraction"]
        ),
    }
    with open(
        workspace.table_directory / "orbital_control_policy.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            ["kind", "name", "value", "threshold_or_budget", "crossed", "actions", "source_class"]
        )
        w.writerow(
            [
                "common_cause",
                budget.binding_hazard or "",
                f"{budget.maximum_loss_fraction:.9f}",
                f"{budget.budget_fraction:.9f}",
                int(not budget.passes),
                (
                    "reduce_cluster_cap;isolate_failure_domains;add_independent_reserve"
                    if not budget.passes
                    else ""
                ),
                control_cfg["source_class"],
            ]
        )
        for name, value in control_metrics.items():
            threshold = float(control_cfg["trigger_thresholds"][name])
            metric_actions = debris_control_actions(
                {name: value},
                {name: threshold},
            )
            w.writerow(
                [
                    "shell_trigger",
                    name,
                    f"{value:.9f}",
                    f"{threshold:.9f}",
                    int(value > threshold),
                    ";".join(metric_actions),
                    control_cfg["source_class"],
                ]
            )

    resilience_cfg = params.orbital_resilience_strategy
    layout_rows = [
        evaluate_cluster_layout(
            name,
            layout,
            collision_exposure_index=resilience_cfg["collision_exposure_index"],
            common_cause_budget_fraction=resilience_cfg["common_cause_budget_fraction"],
        )
        for name, layout in resilience_cfg["cluster_layouts"].items()
    ]

    def layout_dominated(candidate: ClusterLayoutResult) -> bool:
        return any(
            other.layout != candidate.layout
            and other.expected_loss_index <= candidate.expected_loss_index
            and other.communications_burden_index <= candidate.communications_burden_index
            and other.concentration_benefit_index >= candidate.concentration_benefit_index
            and (
                other.expected_loss_index < candidate.expected_loss_index
                or other.communications_burden_index < candidate.communications_burden_index
                or other.concentration_benefit_index > candidate.concentration_benefit_index
            )
            for other in layout_rows
        )

    with open(
        workspace.table_directory / "orbital_cluster_layout_optimization.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "layout",
                "total_nodes",
                "nodes_per_cluster",
                "clusters",
                "maximum_common_cause_fraction",
                "correlated_fragment_exposure",
                "shared_service_failure_fraction",
                "communications_burden_index",
                "concentration_benefit_index",
                "expected_loss_index",
                "passes_loss_budget",
                "pareto_nondominated",
                "source_class",
                "bounding_argument",
            ]
        )
        for row in layout_rows:
            w.writerow(
                [
                    row.layout,
                    row.total_nodes,
                    row.nodes_per_cluster,
                    row.clusters,
                    f"{row.maximum_common_cause_fraction:.9f}",
                    f"{row.correlated_fragment_exposure:.9f}",
                    f"{row.shared_service_failure_fraction:.9f}",
                    f"{row.communications_burden_index:.9f}",
                    f"{row.concentration_benefit_index:.9f}",
                    f"{row.expected_loss_index:.9f}",
                    int(row.passes_loss_budget),
                    int(not layout_dominated(row)),
                    resilience_cfg["source_class"],
                    resilience_cfg["bounding_argument"].strip(),
                ]
            )

    breakup_rows = [
        simulate_breakup_cloud(
            resilience_cfg["constellation_nodes"],
            event,
            days=365,
            dt_days=1.0,
        )
        for event in resilience_cfg["breakup_events"].values()
    ]
    with open(
        workspace.table_directory / "orbital_breakup_cloud_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "event",
                "environment",
                "direct_loss_capacity",
                "expected_secondary_collisions",
                "expected_avoidance_maneuvers",
                "service_interruption_capacity_days",
                "repair_load_capacity",
                "time_to_restore_days",
                "ending_active_capacity",
                "ending_fragment_cloud",
                "source_class",
                "interpretation",
            ]
        )
        for row in breakup_rows:
            event = resilience_cfg["breakup_events"][row.event]
            environment = event.get("environment")
            if environment is None:
                raise ValueError(f"{row.event}: table output requires an environment")
            w.writerow(
                [
                    row.event,
                    environment,
                    f"{row.direct_loss_capacity:.9f}",
                    f"{row.expected_secondary_collisions:.9f}",
                    f"{row.expected_avoidance_maneuvers:.9f}",
                    f"{row.service_interruption_capacity_days:.9f}",
                    f"{row.repair_load_capacity:.9f}",
                    ("" if row.time_to_restore_days is None else f"{row.time_to_restore_days:.6f}"),
                    f"{row.active_capacity[-1]:.9f}",
                    f"{row.fragment_cloud[-1]:.9f}",
                    resilience_cfg["source_class"],
                    (
                        "deterministic expected-count geometry stress; "
                        "not a catalog-calibrated conjunction forecast"
                    ),
                ]
            )
    with open(
        workspace.table_directory / "orbital_breakup_cloud_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "event",
                "day",
                "active_capacity",
                "fragment_cloud",
                "source_class",
            ]
        )
        for row in breakup_rows:
            for day, active, fragments in zip(
                row.t_days,
                row.active_capacity,
                row.fragment_cloud,
                strict=True,
            ):
                w.writerow(
                    [
                        row.event,
                        f"{day:.6f}",
                        f"{active:.9f}",
                        f"{fragments:.9f}",
                        resilience_cfg["source_class"],
                    ]
                )

    stress_cfg = resilience_cfg["conjunction_stress"]
    degraded_rows = [
        evaluate_degraded_conjunction_control(
            name,
            scenario,
            conjunctions=stress_cfg["conjunctions"],
            collision_probability_per_unsafe_conjunction=stress_cfg[
                "collision_probability_per_unsafe_conjunction"
            ],
            risk_limit=stress_cfg["risk_limit"],
        )
        for name, scenario in stress_cfg["scenarios"].items()
    ]
    with open(
        workspace.table_directory / "orbital_degraded_control_stress.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "detected_conjunctions",
                "executed_avoidance_maneuvers",
                "conflicting_maneuvers",
                "residual_unsafe_conjunctions",
                "collision_risk_index",
                "risk_limit",
                "safe_before_fallback",
                "fallback_actions",
                "residual_risk_after_fallback",
                "safe_after_fallback",
                "source_class",
            ]
        )
        for row in degraded_rows:
            w.writerow(
                [
                    row.scenario,
                    f"{row.detected_conjunctions:.9f}",
                    f"{row.executed_avoidance_maneuvers:.9f}",
                    f"{row.conflicting_maneuvers:.9f}",
                    f"{row.residual_unsafe_conjunctions:.9f}",
                    f"{row.collision_risk_index:.9f}",
                    f"{stress_cfg['risk_limit']:.9f}",
                    int(row.safe_before_fallback),
                    ";".join(row.fallback_actions),
                    f"{row.residual_risk_after_fallback:.9f}",
                    int(row.safe_after_fallback),
                    resilience_cfg["source_class"],
                ]
            )

    mitigation_cfg = resilience_cfg["mitigation_portfolio"]
    level_names = tuple(mitigation_cfg["levels"])
    mitigation_rows = [
        evaluate_mitigation_portfolio(
            dict(zip(level_names, combination, strict=True)),
            mitigation_cfg,
        )
        for combination in itertools.product(
            *(mitigation_cfg["levels"][name] for name in level_names)
        )
    ]

    def mitigation_dominated(candidate: MitigationPortfolioResult) -> bool:
        return any(
            other.residual_risk_index <= candidate.residual_risk_index
            and other.lifecycle_cost_index <= candidate.lifecycle_cost_index
            and other.delivered_capacity_index >= candidate.delivered_capacity_index
            and (
                other.residual_risk_index < candidate.residual_risk_index
                or other.lifecycle_cost_index < candidate.lifecycle_cost_index
                or other.delivered_capacity_index > candidate.delivered_capacity_index
            )
            for other in mitigation_rows
        )

    with open(
        workspace.table_directory / "orbital_mitigation_portfolio_pareto.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                *level_names,
                "residual_risk_index",
                "lifecycle_cost_index",
                "delivered_capacity_index",
                "pareto_nondominated",
                "source_class",
            ]
        )
        for row in mitigation_rows:
            w.writerow(
                [
                    f"{row.deployment_cadence:.6f}",
                    f"{row.disposal_reliability:.6f}",
                    f"{row.removal_rate:.6f}",
                    f"{row.shielding_mass_fraction:.6f}",
                    f"{row.cluster_cap_fraction:.6f}",
                    row.shell_diversity,
                    row.servicer_fleet_size,
                    f"{row.repair_recycling_capacity:.6f}",
                    f"{row.residual_risk_index:.9f}",
                    f"{row.lifecycle_cost_index:.9f}",
                    f"{row.delivered_capacity_index:.9f}",
                    int(not mitigation_dominated(row)),
                    resilience_cfg["source_class"],
                ]
            )

    multi_cfg = resilience_cfg["multi_operator"]
    with open(
        workspace.table_directory / "orbital_multi_operator_capacity.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "shell",
                "operator_scenario",
                "planned_nodes",
                "carrying_capacity_nodes",
                "coordinated_fraction",
                "predicted_conjunction_workload",
                "uncoordinated_workload",
                "capacity_compliant",
                "governance_compliant",
                "admissible",
                "source_class",
            ]
        )
        for shell_name, shell in multi_cfg["shells"].items():
            for scenario_name, operators in multi_cfg["scenarios"].items():
                row = evaluate_multi_operator_capacity(
                    shell_name,
                    shell,
                    operators,
                )
                w.writerow(
                    [
                        shell_name,
                        scenario_name,
                        row.planned_nodes,
                        row.carrying_capacity_nodes,
                        f"{row.coordinated_fraction:.9f}",
                        f"{row.predicted_conjunction_workload:.9f}",
                        f"{row.uncoordinated_workload:.9f}",
                        int(row.capacity_compliant),
                        int(row.governance_compliant),
                        int(row.admissible),
                        resilience_cfg["source_class"],
                    ]
                )

    with open(
        workspace.table_directory / "orbital_environment_strategy_comparison.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "environment",
                "breakup_event",
                "atmospheric_clearance",
                "tracking_fraction",
                "fragment_clearance_per_day",
                "stationkeeping_m_s_per_year",
                "residence_time_years",
                "disposal_route",
                "direct_loss_capacity",
                "expected_secondary_collisions",
                "service_interruption_capacity_days",
                "time_to_restore_days",
                "source_class",
            ]
        )
        environment_orbit = {
            "Earth orbit": "leo_650",
            "lunar orbit": "llo",
        }
        for row in breakup_rows:
            event = resilience_cfg["breakup_events"][row.event]
            environment = event.get("environment")
            if environment is None:
                raise ValueError(f"{row.event}: environment comparison requires an environment")
            orbit = strategy_cfg["orbits"][environment_orbit[environment]]
            w.writerow(
                [
                    environment,
                    row.event,
                    orbit["atmospheric_clearance"],
                    f"{event['tracking_fraction']:.6f}",
                    f"{event['fragment_clearance_per_day']:.9f}",
                    f"{orbit['stationkeeping_m_s_per_year']:.6f}",
                    f"{orbit['residence_time_years']:.6f}",
                    orbit["disposal_route"],
                    f"{row.direct_loss_capacity:.9f}",
                    f"{row.expected_secondary_collisions:.9f}",
                    f"{row.service_interruption_capacity_days:.9f}",
                    ("" if row.time_to_restore_days is None else f"{row.time_to_restore_days:.6f}"),
                    resilience_cfg["source_class"],
                ]
            )
