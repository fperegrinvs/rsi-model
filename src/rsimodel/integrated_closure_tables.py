"""Generated-artifact component for the integrated pipeline."""

from __future__ import annotations

import csv
import math

import numpy as np

from rsimodel.extensions import (
    partial_closure_metrics,
    simulate_supported_growth,
)

from .integrated_artifacts import (
    ArtifactWorkspace,
)
from .integrated_types import CapacityRuns, IntegratedParams, SeedResults


def _write_partial_closure_tables(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    seeds: SeedResults,
    runs: CapacityRuns,
) -> None:
    with open(
        workspace.table_directory / "partial_closure_metrics.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "horizon_years",
                "strict_autonomy",
                "horizon_mass_closure_fraction",
                "external_support_t_per_net_cell_equivalent",
                "net_cell_equivalents_per_external_t",
                "critical_external_inputs",
                "initial_installed_seed_mass_t",
                "initial_seed_excluded_from_autonomy",
                "interpretation",
            ]
        )
        horizon = 40.0
        for name, run in runs.items():
            external = float(seeds[name].import_stock_t.sum())
            local = run.lunar_material_t + run.asteroid_material_t + run.recycled_material_t
            added = max(float(run.operating_cells[-1] - 1.0), 0.0)
            metrics = partial_closure_metrics(
                local_mass_flow={
                    "local_material": local / horizon,
                    "strategic_import": 0.0,
                },
                external_mass_flow={
                    "local_material": 0.0,
                    "strategic_import": external / horizon,
                },
                verified_capacity_added_per_year=added / horizon,
                critical_inputs=("strategic_import",),
            )
            w.writerow(
                [
                    name,
                    f"{horizon:.1f}",
                    int(metrics.strict_autonomy),
                    f"{metrics.mass_closure_fraction:.9f}",
                    (
                        "inf"
                        if np.isinf(metrics.external_support_intensity)
                        else f"{metrics.external_support_intensity:.9f}"
                    ),
                    ("" if metrics.import_leverage is None else f"{metrics.import_leverage:.9f}"),
                    ";".join(metrics.critical_external_inputs),
                    f"{seeds[name].total_seed_mass_t:.9f}",
                    1,
                    (
                        "horizon-equivalent ongoing-support diagnostic; "
                        "the separately reported initial installed seed remains "
                        "external entry capital; not a steady-state flow estimate"
                    ),
                ]
            )

    support_cfg = params.partial_closure_support
    support_inputs = tuple(support_cfg["residual_inputs"])
    support_results = {
        policy: simulate_supported_growth(support_cfg, policy=policy)
        for policy in support_cfg["policies"]
    }
    allocation_results = {
        policy: simulate_supported_growth(support_cfg, policy=policy)
        for policy in support_cfg["allocation_policies"]
    }
    with open(
        workspace.table_directory / "partial_closure_support_policies.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "policy",
                "year",
                "capacity",
                "capacity_added",
                "external_delivery_t",
                "external_delivery_volume_m3",
                "external_delivery_value_musd",
                "usable_inventory_t",
                "replacement_demand_t",
                "commissioning_demand_t",
                "binding_residual_input",
                "capacity_loss",
                "substitution_effort_capacity_years",
                "validated_substitutions",
                "failed_substitutions",
                "strict_autonomy",
                "source_class",
            ]
        )
        for policy, result in support_results.items():
            for k, year in enumerate(result.t):
                delivered_mass = float(result.external_delivery[k].sum())
                delivered_volume = sum(
                    result.external_delivery[k, index]
                    * float(support_cfg["residual_inputs"][name]["delivered_volume_m3_per_t"])
                    for index, name in enumerate(support_inputs)
                )
                delivered_value = sum(
                    result.external_delivery[k, index]
                    * float(support_cfg["residual_inputs"][name]["delivered_value_musd_per_t"])
                    for index, name in enumerate(support_inputs)
                )
                w.writerow(
                    [
                        policy,
                        f"{year:.1f}",
                        f"{result.capacity[k]:.9f}",
                        (
                            "0.000000000"
                            if k == 0
                            else f"{max(result.capacity[k] - result.capacity[k - 1], 0.0):.9f}"
                        ),
                        f"{delivered_mass:.9f}",
                        f"{delivered_volume:.9f}",
                        f"{delivered_value:.9f}",
                        f"{result.inventory[k].sum():.9f}",
                        f"{result.replacement_demand[k].sum():.9f}",
                        f"{result.commissioning_demand[k].sum():.9f}",
                        result.binding_input[k],
                        f"{result.capacity_loss[k]:.9f}",
                        f"{result.substitution_effort[k].sum():.9f}",
                        ";".join(
                            name
                            for index, name in enumerate(support_inputs)
                            if result.substitution_validated[k, index]
                        ),
                        ";".join(
                            name
                            for index, name in enumerate(support_inputs)
                            if result.substitution_failed[k, index]
                        ),
                        0,
                        support_cfg["source_class"],
                    ]
                )

    with open(
        workspace.table_directory / "partial_closure_supplier_boundary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "policy",
                "year",
                "resource",
                "resource_capacity_per_year",
                "requirement_per_import_t",
                "resource_implied_import_capacity_t_per_year",
                "system_supplier_capacity_t_per_year",
                "supplier_utilization",
                "binding_resource",
                "delivered_residual_t",
                "supplier_reliability_fraction",
                "source_class",
            ]
        )
        supplier_cfg = support_cfg["external_supplier"]
        for policy, result in support_results.items():
            for k, year in enumerate(result.t):
                exponent = max(k - 1, 0)
                for resource_name, resource in supplier_cfg["resources"].items():
                    capacity_value = (
                        float(resource["initial_capacity_per_year"])
                        * (1.0 + float(resource["growth_per_year"])) ** exponent
                    )
                    requirement = float(resource["requirement_per_import_t"])
                    w.writerow(
                        [
                            policy,
                            f"{year:.1f}",
                            resource_name,
                            f"{capacity_value:.9f}",
                            f"{requirement:.9f}",
                            f"{capacity_value / requirement:.9f}",
                            f"{result.supplier_capacity_t_per_year[k]:.9f}",
                            f"{result.supplier_utilization[k]:.9f}",
                            result.supplier_binding_resource[k],
                            f"{result.external_delivery[k].sum():.9f}",
                            f"{supplier_cfg['reliability_fraction']:.6f}",
                            support_cfg["source_class"],
                        ]
                    )

    residual_commissioning_mass = sum(
        float(spec["commissioning_t_per_capacity"])
        for spec in support_cfg["residual_inputs"].values()
    )
    local_mass = float(support_cfg["local_bulk_t_per_capacity"])
    mass_closure = local_mass / (local_mass + residual_commissioning_mass)
    local_value = local_mass * float(support_cfg["local_bulk_value_musd_per_t"])
    residual_value = sum(
        float(spec["commissioning_t_per_capacity"]) * float(spec["delivered_value_musd_per_t"])
        for spec in support_cfg["residual_inputs"].values()
    )
    value_closure = local_value / (local_value + residual_value)
    part_family_closure = float(support_cfg["local_part_families"]) / float(
        support_cfg["total_part_families"]
    )
    with open(
        workspace.table_directory / "partial_closure_dashboard.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "policy",
                "strict_autonomy",
                "mass_closure_fraction",
                "part_family_closure_fraction",
                "value_closure_fraction",
                "embodied_energy_closure_fraction",
                "process_work_closure_fraction",
                "initial_external_seed_t",
                "wholly_earth_seed_t",
                "seed_delivery_mass_reduction_fraction",
                "initial_delivery_cost_musd",
                "wholly_earth_delivery_cost_musd",
                "initial_external_inventory_value_musd",
                "external_support_t_per_net_capacity",
                "net_capacity_per_external_t",
                "external_support_t_per_capacity_doubling",
                "maximum_supportable_scale",
                "first_stockout_year",
                "ending_stockpile_runway_years",
                "binding_residual_input",
                "capacity_loss_over_horizon",
                "capacity_loss_during_declared_outage",
                "external_human_intervention_hours_per_capacity_year",
                "external_verification_hours_per_capacity_year",
                "maximum_supplier_utilization",
                "criticality_weighted_residual_t_per_capacity",
                "minimum_cut_status",
                "critical_residual_inputs",
                "validated_substitutions",
                "failed_substitutions",
                "substitution_effort_capacity_years",
                "source_class",
            ]
        )
        for policy, result in support_results.items():
            delivered = float(result.external_delivery.sum()) + sum(
                float(spec["initial_stockpile_t"])
                for spec in support_cfg["residual_inputs"].values()
            )
            net_added = max(
                float(result.capacity[-1] - result.capacity[0]),
                0.0,
            )
            intensity = delivered / net_added if net_added > 0.0 else math.inf
            leverage = net_added / delivered if delivered > 0.0 else None
            maximum_scale = float(np.max(result.capacity))
            completed_doublings = (
                math.log2(maximum_scale / result.capacity[0])
                if maximum_scale > result.capacity[0] > 0.0
                else 0.0
            )
            support_per_doubling = (
                delivered / completed_doublings if completed_doublings > 0.0 else math.inf
            )
            runway_by_input = []
            for index, _name in enumerate(support_inputs):
                ending_demand = (
                    result.replacement_demand[-1, index] + result.commissioning_demand[-1, index]
                )
                if ending_demand > 0.0:
                    runway_by_input.append(result.inventory[-1, index] / ending_demand)
            binding_counts = {name: result.binding_input.count(name) for name in support_inputs}
            binding_input = max(
                binding_counts,
                key=lambda name: binding_counts[name],
            )
            initial_external = float(support_cfg["bridge_initial_external_seed_t"])
            earth_seed = float(support_cfg["wholly_earth_manufactured_t_per_capacity"])
            delivery_cost = float(support_cfg["earth_delivery_musd_per_t"])
            initial_inventory_value = sum(
                float(spec["initial_stockpile_t"]) * float(spec["delivered_value_musd_per_t"])
                for spec in support_cfg["residual_inputs"].values()
            )
            criticality_weighted_residual = sum(
                float(spec["criticality_weight"]) * float(spec["commissioning_t_per_capacity"])
                for spec in support_cfg["residual_inputs"].values()
            )
            outage_mask = (result.t >= 12.0) & (result.t <= 17.0)
            w.writerow(
                [
                    policy,
                    0,
                    f"{mass_closure:.9f}",
                    f"{part_family_closure:.9f}",
                    f"{value_closure:.9f}",
                    f"{support_cfg['local_embodied_energy_fraction']:.9f}",
                    f"{support_cfg['local_process_work_fraction']:.9f}",
                    f"{initial_external:.9f}",
                    f"{earth_seed:.9f}",
                    f"{1.0 - initial_external / earth_seed:.9f}",
                    f"{initial_external * delivery_cost:.9f}",
                    f"{earth_seed * delivery_cost:.9f}",
                    f"{initial_inventory_value:.9f}",
                    "inf" if np.isinf(intensity) else f"{intensity:.9f}",
                    "" if leverage is None else f"{leverage:.9f}",
                    ("inf" if np.isinf(support_per_doubling) else f"{support_per_doubling:.9f}"),
                    f"{maximum_scale:.9f}",
                    (
                        ""
                        if result.first_stockout_year is None
                        else f"{result.first_stockout_year:.1f}"
                    ),
                    (
                        "0.000000000"
                        if result.capacity[-1] <= 1e-12
                        else "inf"
                        if not runway_by_input
                        else f"{min(runway_by_input):.9f}"
                    ),
                    binding_input,
                    f"{result.capacity_loss.sum():.9f}",
                    f"{result.capacity_loss[outage_mask].sum():.9f}",
                    f"{support_cfg['external_human_intervention_hours_per_capacity_year']:.9f}",
                    f"{support_cfg['external_verification_hours_per_capacity_year']:.9f}",
                    f"{float(np.max(result.supplier_utilization)):.9f}",
                    f"{criticality_weighted_residual:.9f}",
                    "each listed residual is a single-input stop-line cut",
                    ";".join(support_inputs),
                    ";".join(
                        name
                        for index, name in enumerate(support_inputs)
                        if result.substitution_validated[-1, index]
                    ),
                    ";".join(
                        name
                        for index, name in enumerate(support_inputs)
                        if result.substitution_failed[-1, index]
                    ),
                    f"{result.substitution_effort[-1].sum():.9f}",
                    support_cfg["source_class"],
                ]
            )

    with open(
        workspace.table_directory / "partial_closure_substitution_programs.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "policy",
                "residual_input",
                "capability_threshold",
                "parent_tool_ancestry",
                "initial_evidence_state",
                "minimum_completion_year",
                "effort_threshold_capacity_years",
                "required_intelligence",
                "embodiment_adequate",
                "materials_available",
                "tools_available",
                "test_facility_available",
                "declared_outcome",
                "final_state",
                "remaining_requirement_multiplier",
                "resource",
                "resource_share",
                "charged_effort_capacity_years",
                "source_class",
            ]
        )
        for policy, result in support_results.items():
            for index, name in enumerate(support_inputs):
                program = support_cfg["substitution_programs"].get(name)
                if program is None:
                    continue
                final_state = (
                    "validated"
                    if result.substitution_validated[-1, index]
                    else "failed"
                    if result.substitution_failed[-1, index]
                    else "incomplete"
                )
                total_effort = float(result.substitution_effort[-1, index])
                for resource, share in program["effort_resource_shares"].items():
                    w.writerow(
                        [
                            policy,
                            name,
                            program["capability_threshold"],
                            program["parent_tool_ancestry"],
                            program["evidence_state"],
                            f"{program['minimum_completion_year']:.6f}",
                            f"{program['effort_capacity_years']:.9f}",
                            f"{program['required_intelligence']:.6f}",
                            int(program["embodiment_adequate"]),
                            int(program["materials_available"]),
                            int(program["tools_available"]),
                            int(program["test_facility_available"]),
                            program["outcome"],
                            final_state,
                            f"{program['remaining_requirement_multiplier']:.6f}",
                            resource,
                            f"{share:.6f}",
                            f"{total_effort * float(share):.9f}",
                            support_cfg["source_class"],
                        ]
                    )

    with open(
        workspace.table_directory / "partial_closure_allocation_policies.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "allocation_policy",
                "substitution_allocation_fraction",
                "stockpile_reserve_years",
                "maximum_scale",
                "final_scale",
                "first_stockout_year",
                "total_external_support_t",
                "ending_inventory_t",
                "capacity_loss_over_horizon",
                "substitution_effort_capacity_years",
                "validated_substitutions",
                "failed_substitutions",
                "interpretation",
                "source_class",
            ]
        )
        initial_stockpile = sum(
            float(spec["initial_stockpile_t"]) for spec in support_cfg["residual_inputs"].values()
        )
        for policy, result in allocation_results.items():
            policy_cfg = support_cfg["allocation_policies"][policy]
            w.writerow(
                [
                    policy,
                    f"{policy_cfg['substitution_allocation_fraction']:.6f}",
                    f"{policy_cfg.get('stockpile_reserve_years', 0.0):.6f}",
                    f"{float(np.max(result.capacity)):.9f}",
                    f"{float(result.capacity[-1]):.9f}",
                    (
                        ""
                        if result.first_stockout_year is None
                        else f"{result.first_stockout_year:.1f}"
                    ),
                    f"{initial_stockpile + result.external_delivery.sum():.9f}",
                    f"{result.inventory[-1].sum():.9f}",
                    f"{result.capacity_loss.sum():.9f}",
                    f"{result.substitution_effort[-1].sum():.9f}",
                    ";".join(
                        name
                        for index, name in enumerate(support_inputs)
                        if result.substitution_validated[-1, index]
                    ),
                    ";".join(
                        name
                        for index, name in enumerate(support_inputs)
                        if result.substitution_failed[-1, index]
                    ),
                    (
                        "same capacity-proportional external supply; policy "
                        "changes only immediate expansion, replacement reserve, "
                        "and substitution effort"
                    ),
                    support_cfg["source_class"],
                ]
            )
