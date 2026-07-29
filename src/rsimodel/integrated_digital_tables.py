"""Generated-artifact component for the integrated pipeline."""

from __future__ import annotations

import csv

import numpy as np

from rsimodel.extensions import (
    chronological_release_backtest,
    cognitive_physical_labor_sweep,
    data_advantage,
    data_evaluator_coevolution,
    digital_channel_ablations,
    electronics_supply_chain_sensitivity,
    evaluate_milestone_order,
    industrial_reliability_ladder,
    learning_feedback_to_digital_loop,
    optimize_compute_allocation,
    replication_governance_externalities,
    simulate_authorized_capacity_control,
    simulate_compute_cohorts,
    simulate_digital_progress,
    simulate_intergenerational_learning,
    verification_hierarchy_sensitivity,
    verified_loop_bottleneck,
)
from rsimodel.lco import (
    MATCHED_COST_CATEGORIES,
    AnchorSet,
    earth_lco_contributions,
    lco_earth,
    lco_space,
    space_lco_contributions,
)

from .integrated_artifacts import (
    ArtifactWorkspace,
)
from .integrated_types import IntegratedParams


def _write_digital_extension_tables(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
) -> None:
    """Write the explicit equation-review sensitivity outputs."""
    earth_central = lco_earth("base")
    space_central = lco_space(
        "leo_inference",
        architecture="serviceable_platform",
    )
    central_costs = {
        "earth": earth_lco_contributions(earth_central),
        "space": space_lco_contributions(space_central),
    }
    paired_cost_draws = {
        environment: {category: [] for category in MATCHED_COST_CATEGORIES}
        for environment in ("earth", "space")
    }
    rng = np.random.default_rng(20260728)
    for _ in range(workspace.ensemble_size):
        anchors = AnchorSet(rng)
        sampled = {
            "earth": earth_lco_contributions(lco_earth("base", a=anchors)),
            "space": space_lco_contributions(
                lco_space(
                    "leo_inference",
                    a=anchors,
                    architecture="serviceable_platform",
                )
            ),
        }
        for environment in ("earth", "space"):
            for category in MATCHED_COST_CATEGORIES:
                paired_cost_draws[environment][category].append(sampled[environment][category])

    central_delta = {
        category: (central_costs["space"][category] - central_costs["earth"][category])
        for category in MATCHED_COST_CATEGORIES
    }
    difference_rank = {
        category: rank
        for rank, category in enumerate(
            sorted(
                MATCHED_COST_CATEGORIES,
                key=lambda name: abs(central_delta[name]),
                reverse=True,
            ),
            start=1,
        )
    }
    with open(
        workspace.table_directory / "matched_lifecycle_cost_contributions.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "environment",
                "category_order",
                "category",
                "central_usd_per_frontier_kw_year",
                "p10",
                "p50",
                "p90",
                "share_of_environment_lco",
                "space_minus_earth_central",
                "absolute_difference_rank",
                "treatment",
                "source_class",
            ]
        )
        for environment, result in (
            ("earth", earth_central),
            ("space", space_central),
        ):
            for order, category in enumerate(MATCHED_COST_CATEGORIES, start=1):
                values = np.asarray(
                    paired_cost_draws[environment][category],
                    dtype=float,
                )
                p10, p50, p90 = np.percentile(values, (10, 50, 90))
                central = central_costs[environment][category]
                if category == "residual_value_credit" and central != 0.0:
                    treatment = "explicit_credit"
                elif np.allclose(values, 0.0):
                    treatment = "omitted_from_implemented_boundary"
                else:
                    treatment = "explicitly_priced"
                w.writerow(
                    [
                        environment,
                        order,
                        category,
                        f"{central:.9f}",
                        f"{p10:.9f}",
                        f"{p50:.9f}",
                        f"{p90:.9f}",
                        f"{central / result.lco:.9f}",
                        f"{central_delta[category]:.9f}",
                        difference_rank[category],
                        treatment,
                        "ASSUMPTION",
                    ]
                )

    digital = {
        regime: simulate_digital_progress(
            params.digital_improvement,
            regime=regime,
            gate_case="zero_lag",
            years=20.0,
            dt=0.25,
        )
        for regime in (
            "smooth_diminishing",
            "saturating_frontier",
            "innovation_interrupted",
        )
    }
    with open(
        workspace.table_directory / "digital_progress_regimes.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "regime",
                "year",
                "internally_available_capability_index",
                "publicly_visible_capability_index",
                "frontier_index",
                "cumulative_effective_compute_flop",
                "experiment_loops_per_year",
                "technically_validated_loops_per_year",
                "internally_authorized_loops_per_year",
                "cumulative_experiments",
                "cumulative_technical_validations",
                "cumulative_internal_adoptions",
                "marginal_gain_per_internal_adoption",
                "source_class",
            ]
        )
        for regime, result in digital.items():
            for k, year in enumerate(result.t):
                w.writerow(
                    [
                        regime,
                        f"{year:.6f}",
                        f"{result.internal_capability[k]:.9f}",
                        f"{result.public_capability[k]:.9f}",
                        f"{result.frontier[k]:.9f}",
                        f"{result.effective_compute[k]:.9e}",
                        f"{result.experiment_loops_per_year[k]:.9f}",
                        f"{result.technically_validated_loops_per_year[k]:.9f}",
                        f"{result.internally_authorized_loops_per_year[k]:.9f}",
                        f"{result.completed_experiments[k]:.9f}",
                        f"{result.completed_technical_validations[k]:.9f}",
                        f"{result.completed_internal_adoptions[k]:.9f}",
                        f"{result.marginal_gain_per_loop[k]:.9f}",
                        params.digital_improvement["source_class"],
                    ]
                )

    gate_cases = {
        gate_case: simulate_digital_progress(
            params.digital_improvement,
            regime="saturating_frontier",
            gate_case=gate_case,
            years=20.0,
            dt=0.25,
        )
        for gate_case in params.digital_improvement["capability_gate_cases"]
    }
    with open(
        workspace.table_directory / "internal_public_capability_trajectories.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "gate_case",
                "year",
                "internally_available_capability_index",
                "publicly_visible_capability_index",
                "assumption_dependent_capability_overhang",
                "experiment_loops_per_year",
                "technically_validated_loops_per_year",
                "internally_authorized_loops_per_year",
                "cumulative_experiments",
                "cumulative_technical_validations",
                "cumulative_internal_adoptions",
                "cumulative_public_release_events",
                "public_release_interval_years",
                "internal_authorization_fraction",
                "public_authorization_fraction",
                "public_capability_slice_fraction",
                "interpretation",
                "source_class",
            ]
        )
        for gate_case, result in gate_cases.items():
            case_config = params.digital_improvement["capability_gate_cases"][gate_case]
            for k, year in enumerate(result.t):
                w.writerow(
                    [
                        gate_case,
                        f"{year:.6f}",
                        f"{result.internal_capability[k]:.9f}",
                        f"{result.public_capability[k]:.9f}",
                        f"{result.capability_overhang[k]:.9f}",
                        f"{result.experiment_loops_per_year[k]:.9f}",
                        f"{result.technically_validated_loops_per_year[k]:.9f}",
                        f"{result.internally_authorized_loops_per_year[k]:.9f}",
                        f"{result.completed_experiments[k]:.9f}",
                        f"{result.completed_technical_validations[k]:.9f}",
                        f"{result.completed_internal_adoptions[k]:.9f}",
                        f"{result.public_release_events[k]:.0f}",
                        f"{case_config['public_release_interval_years']:.6f}",
                        f"{case_config['internal_authorization_fraction']:.6f}",
                        f"{case_config['public_authorization_fraction']:.6f}",
                        f"{case_config['public_capability_slice_fraction']:.6f}",
                        case_config["interpretation"].strip(),
                        params.digital_improvement["source_class"],
                    ]
                )

    compute_allocation_cfg = params.ai_rd_compute_allocation
    compute_allocation_rows = optimize_compute_allocation(compute_allocation_cfg)
    with open(
        workspace.table_directory / "ai_rd_compute_allocation.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "objective",
                "algorithmic_efficiency",
                "total_physical_accelerator_hours",
                "training_hours",
                "research_inference_hours",
                "experiment_hours",
                "data_generation_filtering_hours",
                "verification_safety_hours",
                "external_productive_service_hours",
                "effective_training_hours",
                "automated_researcher_instances",
                "useful_research_task_limit",
                "researcher_candidate_rate",
                "experiment_candidate_rate",
                "accepted_data_candidate_rate",
                "verification_candidate_rate",
                "serial_depth_candidate_limit",
                "raw_capability_progress_rate",
                "verified_progress_rate",
                "external_productive_service_units",
                "industrial_control_service_units",
                "foregone_external_revenue",
                "objective_score",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in compute_allocation_rows:
            w.writerow(
                [
                    row.objective,
                    f"{row.algorithmic_efficiency:.6f}",
                    f"{row.total_physical_accelerator_hours:.6f}",
                    f"{row.training_hours:.6f}",
                    f"{row.research_inference_hours:.6f}",
                    f"{row.experiment_hours:.6f}",
                    f"{row.data_generation_filtering_hours:.6f}",
                    f"{row.verification_safety_hours:.6f}",
                    f"{row.external_productive_service_hours:.6f}",
                    f"{row.effective_training_hours:.6f}",
                    f"{row.automated_researcher_instances:.6f}",
                    f"{row.useful_research_task_limit:.6f}",
                    f"{row.researcher_candidate_rate:.6f}",
                    f"{row.experiment_candidate_rate:.6f}",
                    f"{row.accepted_data_candidate_rate:.6f}",
                    f"{row.verification_candidate_rate:.6f}",
                    f"{row.serial_depth_candidate_limit:.6f}",
                    f"{row.raw_capability_progress_rate:.6f}",
                    f"{row.verified_progress_rate:.6f}",
                    f"{row.external_productive_service_units:.6f}",
                    f"{row.industrial_control_service_units:.6f}",
                    f"{row.foregone_external_revenue:.6f}",
                    f"{row.objective_score:.6f}",
                    compute_allocation_cfg["evidence_status"],
                    compute_allocation_cfg["source_class"],
                    compute_allocation_cfg["boundary"].strip(),
                ]
            )

    labor_cfg = params.cognitive_physical_labor
    labor_rows = cognitive_physical_labor_sweep(labor_cfg)
    with open(
        workspace.table_directory / "cognitive_physical_labor.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "model_instances",
                "inference_capacity_instances",
                "active_cognitive_instances",
                "physical_robots_machines",
                "experimental_stations",
                "independently_verifiable_work_cells",
                "effective_physical_agents",
                "simulation_planning_monitoring_instances",
                "waiting_or_contention_instances",
                "physical_output_units_per_year",
                "parallel_experiment_capacity",
                "serial_depth_steps",
                "serial_wall_clock_floor_years",
                "independent_experiment_batch_years",
                "combined_experiment_program_years",
                "coordination_graph_edges",
                "duplicate_work_fraction",
                "verification_demand_units_per_year",
                "onboarding_hours_per_active_instance",
                "total_onboarding_hours",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in labor_rows:
            w.writerow(
                [
                    row.model_instances,
                    row.inference_capacity_instances,
                    row.active_cognitive_instances,
                    row.physical_robots_machines,
                    row.experimental_stations,
                    row.independently_verifiable_work_cells,
                    f"{row.effective_physical_agents:.6f}",
                    f"{row.simulation_planning_monitoring_instances:.6f}",
                    f"{row.waiting_or_contention_instances:.6f}",
                    f"{row.physical_output_units_per_year:.6f}",
                    row.parallel_experiment_capacity,
                    row.serial_depth_steps,
                    f"{row.serial_wall_clock_floor_years:.6f}",
                    f"{row.independent_experiment_batch_years:.6f}",
                    f"{row.combined_experiment_program_years:.6f}",
                    f"{row.coordination_graph_edges:.6f}",
                    f"{row.duplicate_work_fraction:.9f}",
                    f"{row.verification_demand_units_per_year:.6f}",
                    f"{row.onboarding_hours_per_active_instance:.6f}",
                    f"{row.total_onboarding_hours:.6f}",
                    labor_cfg["evidence_status"],
                    labor_cfg["source_class"],
                    labor_cfg["boundary"].strip(),
                ]
            )

    supply_chain_cfg = params.ai_electronics_supply_chain
    supply_chain_rows = electronics_supply_chain_sensitivity(supply_chain_cfg)
    with open(
        workspace.table_directory / "ai_electronics_supply_chain.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "tier",
                "parent_sector",
                "closure_strategy",
                "closure_sequence_rank",
                "continuing_earth_umbilical",
                "shelf_life_years",
                "physical_failure_fraction_per_year",
                "economic_obsolescence_fraction_per_year",
                "cumulative_demand_units",
                "cumulative_local_supply_units",
                "cumulative_import_supply_units",
                "cumulative_reused_downbinned_units",
                "cumulative_expired_failed_units",
                "cumulative_unmet_units",
                "terminal_frontier_inventory_units",
                "terminal_downbinned_inventory_units",
                "first_shortfall_year",
                "demand_fulfillment_fraction",
                "early_resilience_per_localization_effort",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in supply_chain_rows:
            w.writerow(
                [
                    row.tier,
                    row.parent_sector,
                    row.closure_strategy,
                    row.closure_sequence_rank,
                    int(row.continuing_earth_umbilical),
                    row.shelf_life_years,
                    f"{row.physical_failure_fraction_per_year:.9f}",
                    f"{row.economic_obsolescence_fraction_per_year:.9f}",
                    f"{row.cumulative_demand_units:.9f}",
                    f"{row.cumulative_local_supply_units:.9f}",
                    f"{row.cumulative_import_supply_units:.9f}",
                    f"{row.cumulative_reused_downbinned_units:.9f}",
                    f"{row.cumulative_expired_failed_units:.9f}",
                    f"{row.cumulative_unmet_units:.9f}",
                    f"{row.terminal_frontier_inventory_units:.9f}",
                    f"{row.terminal_downbinned_inventory_units:.9f}",
                    ("" if row.first_shortfall_year is None else row.first_shortfall_year),
                    f"{row.demand_fulfillment_fraction:.9f}",
                    f"{row.early_resilience_per_localization_effort:.9f}",
                    supply_chain_cfg["evidence_status"],
                    supply_chain_cfg["source_class"],
                    supply_chain_cfg["boundary"].strip(),
                ]
            )

    cohort_cfg = params.compute_cohort_obsolescence
    cohort_rows, cohort_summaries = simulate_compute_cohorts(cohort_cfg)
    with open(
        workspace.table_directory / "compute_cohort_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "year",
                "cohort_generation",
                "cohort_launch_year",
                "cohort_age_years",
                "installed_physical_units",
                "cumulative_physical_failure_units",
                "radiation_performance_factor",
                "intrinsic_performance_per_watt",
                "effective_performance_capacity",
                "relative_performance_to_frontier",
                "assigned_workload",
                "frontier_training_eligible",
                "economically_obsolete_for_frontier",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in cohort_rows:
            w.writerow(
                [
                    row.scenario,
                    row.year,
                    row.cohort_generation,
                    row.cohort_launch_year,
                    row.cohort_age_years,
                    f"{row.installed_physical_units:.9f}",
                    f"{row.cumulative_physical_failure_units:.9f}",
                    f"{row.radiation_performance_factor:.9f}",
                    f"{row.intrinsic_performance_per_watt:.9f}",
                    f"{row.effective_performance_capacity:.9f}",
                    f"{row.relative_performance_to_frontier:.9f}",
                    row.assigned_workload,
                    int(row.frontier_training_eligible),
                    int(row.economically_obsolete_for_frontier),
                    cohort_cfg["evidence_status"],
                    cohort_cfg["source_class"],
                    cohort_cfg["boundary"].strip(),
                ]
            )
    with open(
        workspace.table_directory / "compute_cohort_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "architecture_convergence_year",
                "terminal_physical_units",
                "terminal_effective_performance_capacity",
                "terminal_frontier_training_units",
                "terminal_reassigned_units",
                "terminal_economically_obsolete_but_functional_units",
                "cumulative_physical_failure_units",
                "reassigned_share_of_functional_stock",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in cohort_summaries:
            w.writerow(
                [
                    row.scenario,
                    (
                        ""
                        if row.architecture_convergence_year is None
                        else row.architecture_convergence_year
                    ),
                    f"{row.terminal_physical_units:.9f}",
                    f"{row.terminal_effective_performance_capacity:.9f}",
                    f"{row.terminal_frontier_training_units:.9f}",
                    f"{row.terminal_reassigned_units:.9f}",
                    (f"{row.terminal_economically_obsolete_but_functional_units:.9f}"),
                    f"{row.cumulative_physical_failure_units:.9f}",
                    f"{row.reassigned_share_of_functional_stock:.9f}",
                    cohort_cfg["evidence_status"],
                    cohort_cfg["source_class"],
                    cohort_cfg["boundary"].strip(),
                ]
            )

    verifier_cfg = params.verification_hierarchy
    verifier_rows = verification_hierarchy_sensitivity(verifier_cfg)
    with open(
        workspace.table_directory / "verification_hierarchy.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "stress_scenario",
                "verifier_class",
                "evidence_strength_rank",
                "claim_scope",
                "candidate_iterations_per_year",
                "verifier_capacity_per_year",
                "reviewed_iterations_per_year",
                "accepted_iterations_per_year",
                "false_accepted_iterations_per_year",
                "independently_supported_iterations_per_year",
                "evaluator_independence_score",
                "evaluator_false_positive_fraction",
                "model_lineage_independence",
                "training_data_independence",
                "tool_independence",
                "authority_separation",
                "audit_access",
                "execution_against_fixed_target_per_year",
                "research_direction_setting_per_year",
                "direction_limited_licensed_loops_per_year",
                "positive_records_preserved",
                "negative_records_preserved",
                "null_records_preserved",
                "observed_positive_share_after_filtering",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in verifier_rows:
            w.writerow(
                [
                    row.stress_scenario,
                    row.verifier_class,
                    row.evidence_strength_rank,
                    row.claim_scope,
                    f"{row.candidate_iterations_per_year:.9f}",
                    f"{row.verifier_capacity_per_year:.9f}",
                    f"{row.reviewed_iterations_per_year:.9f}",
                    f"{row.accepted_iterations_per_year:.9f}",
                    f"{row.false_accepted_iterations_per_year:.9f}",
                    f"{row.independently_supported_iterations_per_year:.9f}",
                    f"{row.evaluator_independence_score:.9f}",
                    f"{row.evaluator_false_positive_fraction:.9f}",
                    f"{row.model_lineage_independence:.9f}",
                    f"{row.training_data_independence:.9f}",
                    f"{row.tool_independence:.9f}",
                    f"{row.authority_separation:.9f}",
                    f"{row.audit_access:.9f}",
                    f"{row.execution_against_fixed_target_per_year:.9f}",
                    f"{row.research_direction_setting_per_year:.9f}",
                    f"{row.direction_limited_licensed_loops_per_year:.9f}",
                    f"{row.positive_records_preserved:.9f}",
                    f"{row.negative_records_preserved:.9f}",
                    f"{row.null_records_preserved:.9f}",
                    f"{row.observed_positive_share_after_filtering:.9f}",
                    verifier_cfg["evidence_status"],
                    verifier_cfg["source_class"],
                    verifier_cfg["boundary"].strip(),
                ]
            )

    reliability_cfg = params.industrial_reliability_ladder
    reliability_rows = industrial_reliability_ladder(reliability_cfg)
    with open(
        workspace.table_directory / "industrial_reliability_ladder.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "task",
                "task_domain",
                "consequence_class",
                "required_reliability_fraction",
                "measured_success_fraction",
                "trials",
                "task_duration_hours",
                "verifier_class",
                "intervention_events_per_100_tasks",
                "prompt_check_hours_per_task",
                "expected_recovery_cleanup_hours_per_task",
                "expected_total_human_hours_per_task",
                "rollback_success_fraction",
                "out_of_distribution_recovery_fraction",
                "achieved_rung",
                "achieved_rung_rank",
                "required_rung",
                "required_rung_rank",
                "reliability_requirement_passes",
                "rung_requirement_passes",
                "economic_substitution_passes",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in reliability_rows:
            w.writerow(
                [
                    row.task,
                    row.task_domain,
                    row.consequence_class,
                    f"{row.required_reliability_fraction:.9f}",
                    f"{row.measured_success_fraction:.9f}",
                    row.trials,
                    f"{row.task_duration_hours:.9f}",
                    row.verifier_class,
                    f"{row.intervention_events_per_100_tasks:.9f}",
                    f"{row.prompt_check_hours_per_task:.9f}",
                    f"{row.expected_recovery_cleanup_hours_per_task:.9f}",
                    f"{row.expected_total_human_hours_per_task:.9f}",
                    f"{row.rollback_success_fraction:.9f}",
                    f"{row.out_of_distribution_recovery_fraction:.9f}",
                    row.achieved_rung,
                    row.achieved_rung_rank,
                    row.required_rung,
                    row.required_rung_rank,
                    int(row.reliability_requirement_passes),
                    int(row.rung_requirement_passes),
                    int(row.economic_substitution_passes),
                    reliability_cfg["evidence_status"],
                    reliability_cfg["source_class"],
                    reliability_cfg["boundary"].strip(),
                ]
            )

    data_coevolution_cfg = params.data_evaluator_coevolution
    data_coevolution_rows = data_evaluator_coevolution(data_coevolution_cfg)
    with open(
        workspace.table_directory / "data_evaluator_coevolution.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "generation",
                "synthetic_records_generated",
                "synthetic_records_after_deduplication",
                "accepted_synthetic_training_signal",
                "physical_causal_episodes",
                "total_accepted_training_signal",
                "apparent_progress_index",
                "heldout_transfer_index",
                "evaluator_error_fraction",
                "evaluator_bias_fraction",
                "data_diversity_index",
                "provenance_valid_fraction",
                "causal_linkage_fraction",
                "physical_experiment_time_hours",
                "equipment_wear_units",
                "destructive_samples",
                "verification_capacity_used",
                "proprietary_data_advantage_index",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in data_coevolution_rows:
            w.writerow(
                [
                    row.scenario,
                    row.generation,
                    f"{row.synthetic_records_generated:.9f}",
                    f"{row.synthetic_records_after_deduplication:.9f}",
                    f"{row.accepted_synthetic_training_signal:.9f}",
                    f"{row.physical_causal_episodes:.9f}",
                    f"{row.total_accepted_training_signal:.9f}",
                    f"{row.apparent_progress_index:.9f}",
                    f"{row.heldout_transfer_index:.9f}",
                    f"{row.evaluator_error_fraction:.9f}",
                    f"{row.evaluator_bias_fraction:.9f}",
                    f"{row.data_diversity_index:.9f}",
                    f"{row.provenance_valid_fraction:.9f}",
                    f"{row.causal_linkage_fraction:.9f}",
                    f"{row.physical_experiment_time_hours:.9f}",
                    f"{row.equipment_wear_units:.9f}",
                    f"{row.destructive_samples:.9f}",
                    f"{row.verification_capacity_used:.9f}",
                    f"{row.proprietary_data_advantage_index:.9f}",
                    data_coevolution_cfg["evidence_status"],
                    data_coevolution_cfg["source_class"],
                    data_coevolution_cfg["boundary"].strip(),
                ]
            )

    governance_externality_cfg = params.replication_governance_externalities
    governance_externality_rows = replication_governance_externalities(governance_externality_cfg)
    with open(
        workspace.table_directory / "replication_governance_externalities_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "productive_capacity_at_horizon",
                "legitimately_authorized_capacity_at_horizon",
                "unauthorized_capacity_at_horizon",
                "contested_resource_preempting_capacity_at_horizon",
                "debris_externality_stock_at_horizon",
                "remaining_contested_resource_at_horizon",
                "material_governance_leverage_at_horizon",
                "cumulative_output",
                "cumulative_owner_claim",
                "cumulative_public_claim",
                "cumulative_future_affected_party_claim",
                "cumulative_externality_cost",
                "engineering_endpoint_succeeds",
                "governance_endpoint_succeeds",
                "private_objective_succeeds",
                "negative_sum_race",
                "private_net_value",
                "social_net_value",
                "resource_claim_legitimacy",
                "externality_cost_internalization_fraction",
                "update_authority_gate",
                "liability_gate",
                "audit_rights_gate",
                "succession_of_control_gate",
                "future_affected_party_representation_gate",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in governance_externality_rows:
            w.writerow(
                [
                    row.scenario,
                    f"{row.productive_capacity[-1]:.9f}",
                    f"{row.legitimately_authorized_capacity[-1]:.9f}",
                    f"{row.unauthorized_capacity[-1]:.9f}",
                    (f"{row.contested_resource_preempting_capacity[-1]:.9f}"),
                    f"{row.debris_externality_stock[-1]:.9f}",
                    f"{row.remaining_contested_resource[-1]:.9f}",
                    f"{row.material_governance_leverage[-1]:.9f}",
                    f"{row.cumulative_output[-1]:.9f}",
                    f"{row.cumulative_owner_claim[-1]:.9f}",
                    f"{row.cumulative_public_claim[-1]:.9f}",
                    (f"{row.cumulative_future_affected_party_claim[-1]:.9f}"),
                    f"{row.cumulative_externality_cost[-1]:.9f}",
                    int(row.engineering_endpoint_succeeds),
                    int(row.governance_endpoint_succeeds),
                    int(row.private_objective_succeeds),
                    int(row.negative_sum_race),
                    f"{row.private_net_value:.9f}",
                    f"{row.social_net_value:.9f}",
                    f"{row.resource_claim_legitimacy:.9f}",
                    f"{row.externality_cost_internalization_fraction:.9f}",
                    int(row.update_authority_gate),
                    int(row.liability_gate),
                    int(row.audit_rights_gate),
                    int(row.succession_of_control_gate),
                    int(row.future_affected_party_representation_gate),
                    governance_externality_cfg["evidence_status"],
                    governance_externality_cfg["source_class"],
                    governance_externality_cfg["boundary"].strip(),
                ]
            )
    with open(
        workspace.table_directory / "replication_governance_externalities_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "year",
                "productive_capacity",
                "legitimately_authorized_capacity",
                "unauthorized_capacity",
                "contested_resource_preempting_capacity",
                "debris_externality_stock",
                "remaining_contested_resource",
                "material_governance_leverage",
                "cumulative_output",
                "cumulative_owner_claim",
                "cumulative_public_claim",
                "cumulative_future_affected_party_claim",
                "cumulative_externality_cost",
                "source_class",
            ]
        )
        for row in governance_externality_rows:
            for k, year in enumerate(row.t):
                w.writerow(
                    [
                        row.scenario,
                        f"{year:.6f}",
                        f"{row.productive_capacity[k]:.9f}",
                        f"{row.legitimately_authorized_capacity[k]:.9f}",
                        f"{row.unauthorized_capacity[k]:.9f}",
                        (f"{row.contested_resource_preempting_capacity[k]:.9f}"),
                        f"{row.debris_externality_stock[k]:.9f}",
                        f"{row.remaining_contested_resource[k]:.9f}",
                        f"{row.material_governance_leverage[k]:.9f}",
                        f"{row.cumulative_output[k]:.9f}",
                        f"{row.cumulative_owner_claim[k]:.9f}",
                        f"{row.cumulative_public_claim[k]:.9f}",
                        (f"{row.cumulative_future_affected_party_claim[k]:.9f}"),
                        f"{row.cumulative_externality_cost[k]:.9f}",
                        governance_externality_cfg["source_class"],
                    ]
                )

    digital_cfg = params.digital_improvement
    with open(
        workspace.table_directory / "digital_channel_ablations.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "frozen_channel",
                "assumed_annual_channel_rate",
                "full_annual_multiplier",
                "frozen_annual_multiplier",
                "removed_log_progress_share",
                "interpretation",
                "source_class",
            ]
        )
        for row in digital_channel_ablations(digital_cfg["annual_progress_channels"]):
            w.writerow(
                [
                    row.channel,
                    f"{digital_cfg['annual_progress_channels'][row.channel]:.9f}",
                    f"{row.full_annual_multiplier:.9f}",
                    f"{row.frozen_annual_multiplier:.9f}",
                    f"{row.removed_log_progress_share:.9f}",
                    "one-channel freeze; accounting sensitivity, not causal estimate",
                    digital_cfg["source_class"],
                ]
            )

    backtest_cfg = params.chronological_release_backtest
    backtest_rows, backtest_summaries = chronological_release_backtest(backtest_cfg)
    with open(
        workspace.table_directory / "digital_release_backtest.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "relation",
                "model",
                "release_date",
                "release_year",
                "split",
                "parameters_billion",
                "training_tokens_billion",
                "token_count_is_lower_bound",
                "compute_proxy_flop",
                "data_balance_fraction",
                "observed_mmlu_five_shot_percent",
                "predicted_mmlu_five_shot_percent",
                "residual_percentage_points",
                "absolute_error_percentage_points",
                "source_id",
                "source_locator",
                "evidence_status",
                "source_class",
            ]
        )
        for row in backtest_rows:
            w.writerow(
                [
                    row.relation,
                    row.model,
                    row.release_date,
                    row.release_year,
                    row.split,
                    f"{row.parameters_billion:.9f}",
                    f"{row.training_tokens_billion:.9f}",
                    int(row.token_count_is_lower_bound),
                    f"{row.compute_proxy_flop:.9e}",
                    f"{row.data_balance_fraction:.9f}",
                    f"{row.observed_mmlu_percent:.9f}",
                    f"{row.predicted_mmlu_percent:.9f}",
                    f"{row.residual_percentage_points:.9f}",
                    f"{row.absolute_error_percentage_points:.9f}",
                    row.source_id,
                    row.source_locator,
                    backtest_cfg["evidence_status"],
                    backtest_cfg["source_class"],
                ]
            )
    with open(
        workspace.table_directory / "digital_release_backtest_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "relation",
                "split",
                "observations",
                "mean_absolute_error_percentage_points",
                "root_mean_square_error_percentage_points",
                "mean_signed_error_percentage_points",
                "intercept",
                "log_compute_coefficient",
                "log_balance_coefficient",
                "fit_model_names",
                "fit_release_year_max",
                "split_rule",
                "target_definition",
                "compute_proxy_definition",
                "evidence_status",
                "source_class",
            ]
        )
        for row in backtest_summaries:
            w.writerow(
                [
                    row.relation,
                    row.split,
                    row.observations,
                    f"{row.mean_absolute_error_percentage_points:.9f}",
                    f"{row.root_mean_square_error_percentage_points:.9f}",
                    f"{row.mean_signed_error_percentage_points:.9f}",
                    f"{row.intercept:.12f}",
                    f"{row.log_compute_coefficient:.12f}",
                    (
                        f"{row.log_balance_coefficient:.12f}"
                        if row.log_balance_coefficient is not None
                        else ""
                    ),
                    ";".join(row.fit_model_names),
                    row.fit_release_year_max,
                    backtest_cfg["split_rule"].strip(),
                    backtest_cfg["target_definition"].strip(),
                    backtest_cfg["compute_proxy_definition"].strip(),
                    backtest_cfg["evidence_status"],
                    backtest_cfg["source_class"],
                ]
            )

    milestone_cfg = params.milestone_order_branches
    milestone_rows = evaluate_milestone_order(milestone_cfg)
    with open(
        workspace.table_directory / "milestone_order_branches.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "branch",
                "digital_speed",
                "physical_speed",
                "ai_rd_closure_year",
                "embodiment_closure_year",
                "earth_capital_closure_year",
                "space_capital_closure_year",
                "control_readiness_year",
                "intelligence_overhang_years",
                "first_capital_closure",
                "space_path_timing",
                "control_ready_for_ai_rd",
                "control_ready_for_earth_closure",
                "control_ready_for_space_closure",
                "safety_conditions_pass",
                "earth_bridge_cost_multiplier",
                "boundary",
                "evidence_status",
                "source_class",
            ]
        )
        for row in milestone_rows:
            w.writerow(
                [
                    row.branch,
                    row.digital_speed,
                    row.physical_speed,
                    f"{row.ai_rd_closure_year:.6f}",
                    f"{row.embodiment_closure_year:.6f}",
                    f"{row.earth_capital_closure_year:.6f}",
                    f"{row.space_capital_closure_year:.6f}",
                    f"{row.control_readiness_year:.6f}",
                    f"{row.intelligence_overhang_years:.6f}",
                    row.first_capital_closure,
                    row.space_path_timing,
                    int(row.control_ready_for_ai_rd),
                    int(row.control_ready_for_earth_closure),
                    int(row.control_ready_for_space_closure),
                    int(row.safety_conditions_pass),
                    f"{row.earth_bridge_cost_multiplier:.6f}",
                    milestone_cfg["boundary"].strip(),
                    milestone_cfg["evidence_status"],
                    milestone_cfg["source_class"],
                ]
            )

    control_cfg = params.authorized_capacity_control
    control_rows = simulate_authorized_capacity_control(control_cfg)
    with open(
        workspace.table_directory / "authorized_capacity_control_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "task_capability",
                "coordination_capability",
                "evaluator_capability",
                "controllability_confidence",
                "evaluator_independence_score",
                "correlated_monitor_failure_probability",
                "gross_capacity_at_horizon",
                "authorized_capacity_at_horizon",
                "unauthorized_capacity_at_horizon",
                "proposed_high_impact_actions_at_horizon_per_year",
                "authorized_high_impact_actions_at_horizon_per_year",
                "binding_authorization_limit_at_horizon",
                "first_independent_verification_lag_year",
                "first_human_oversight_lag_year",
                "human_approval_ceremonial_at_horizon",
                "governance_endpoint_passes",
                "boundary",
                "evidence_status",
                "source_class",
            ]
        )
        for row in control_rows:
            w.writerow(
                [
                    row.scenario,
                    f"{row.task_capability:.9f}",
                    f"{row.coordination_capability:.9f}",
                    f"{row.evaluator_capability:.9f}",
                    f"{row.controllability_confidence:.9f}",
                    f"{row.evaluator_independence_score:.9f}",
                    f"{row.correlated_monitor_failure_probability:.9f}",
                    f"{row.gross_operating_capacity[-1]:.9f}",
                    f"{row.authorized_operating_capacity[-1]:.9f}",
                    f"{row.unauthorized_operating_capacity[-1]:.9f}",
                    f"{row.proposed_high_impact_actions_per_year[-1]:.9f}",
                    f"{row.authorized_high_impact_actions_per_year[-1]:.9f}",
                    row.binding_authorization_limit[-1],
                    (
                        ""
                        if row.first_independent_verification_lag_year is None
                        else f"{row.first_independent_verification_lag_year:.6f}"
                    ),
                    (
                        ""
                        if row.first_human_oversight_lag_year is None
                        else f"{row.first_human_oversight_lag_year:.6f}"
                    ),
                    int(row.human_approval_ceremonial_at_horizon),
                    int(row.governance_endpoint_passes),
                    control_cfg["boundary"].strip(),
                    control_cfg["evidence_status"],
                    control_cfg["source_class"],
                ]
            )
    with open(
        workspace.table_directory / "authorized_capacity_control_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "year",
                "gross_operating_capacity",
                "authorized_operating_capacity",
                "unauthorized_operating_capacity",
                "proposed_high_impact_actions_per_year",
                "authorized_high_impact_actions_per_year",
                "reliability_verification_capacity_per_year",
                "adversarial_verification_capacity_per_year",
                "secure_command_capacity_per_year",
                "environmental_limit_capacity_per_year",
                "treaty_limit_capacity_per_year",
                "human_comprehension_capacity_per_year",
                "binding_authorization_limit",
                "source_class",
            ]
        )
        for row in control_rows:
            for index, year in enumerate(row.t):
                w.writerow(
                    [
                        row.scenario,
                        f"{year:.6f}",
                        f"{row.gross_operating_capacity[index]:.9f}",
                        f"{row.authorized_operating_capacity[index]:.9f}",
                        f"{row.unauthorized_operating_capacity[index]:.9f}",
                        f"{row.proposed_high_impact_actions_per_year[index]:.9f}",
                        f"{row.authorized_high_impact_actions_per_year[index]:.9f}",
                        (f"{row.reliability_verification_capacity_per_year[index]:.9f}"),
                        (f"{row.adversarial_verification_capacity_per_year[index]:.9f}"),
                        f"{row.secure_command_capacity_per_year[index]:.9f}",
                        f"{row.environmental_capacity_per_year[index]:.9f}",
                        f"{row.treaty_capacity_per_year[index]:.9f}",
                        (f"{row.human_comprehension_capacity_per_year[index]:.9f}"),
                        row.binding_authorization_limit[index],
                        control_cfg["source_class"],
                    ]
                )

    with open(
        workspace.table_directory / "digital_loop_bottlenecks.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "period",
                "start_year",
                "end_year",
                "binding_stage",
                "verified_loops_per_year",
                "progress_mechanism",
                "stage_rates_per_year",
                "source_class",
            ]
        )
        for period in digital_cfg["loop_capacity_periods"]:
            result = verified_loop_bottleneck(period["stage_rates_per_year"])
            w.writerow(
                [
                    period["name"],
                    f"{period['start_year']:.6f}",
                    f"{period['end_year']:.6f}",
                    ";".join(result.binding_stages),
                    f"{result.rate_per_year:.9f}",
                    period["progress_mechanism"],
                    ";".join(
                        f"{name}={value:g}"
                        for name, value in period["stage_rates_per_year"].items()
                    ),
                    digital_cfg["source_class"],
                ]
            )

    elasticity_names = digital_cfg["elasticity_correlation_order"]
    elasticity_correlation = np.asarray(
        digital_cfg["elasticity_correlation_matrix"],
        dtype=float,
    )
    with open(
        workspace.table_directory / "digital_elasticity_bounds.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "record_type",
                "quantity",
                "paired_quantity",
                "lower",
                "central",
                "upper",
                "correlation",
                "source_class",
            ]
        )
        for name in elasticity_names:
            lower, central, upper = digital_cfg["elasticity_bounds"][name]
            w.writerow(
                [
                    "elasticity_bound",
                    name,
                    "",
                    f"{lower:.6f}",
                    f"{central:.6f}",
                    f"{upper:.6f}",
                    "",
                    digital_cfg["source_class"],
                ]
            )
        for row_index, first in enumerate(elasticity_names):
            for column_index in range(row_index + 1, len(elasticity_names)):
                second = elasticity_names[column_index]
                w.writerow(
                    [
                        "correlation",
                        first,
                        second,
                        "",
                        "",
                        "",
                        f"{elasticity_correlation[row_index, column_index]:.6f}",
                        digital_cfg["source_class"],
                    ]
                )

    learning_cfg = params.intergenerational_learning_rehearsal
    learning_rows = simulate_intergenerational_learning(learning_cfg)
    with open(
        workspace.table_directory / "intergenerational_learning_faults.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "generation",
                "fault_family",
                "training_case",
                "hidden_transfer_case",
                "holdout_exposed_to_training",
                "learning_latency_days",
                "lesson_retention_fraction",
                "transfer_success_fraction",
                "recurrence_fraction",
                "recovery_time_days",
                "verification_compute_hours",
                "prior_task_regression_fraction",
                "transfer_gate_passes",
                "retention_gate_passes",
                "regression_gate_passes",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in learning_rows:
            w.writerow(
                [
                    row.generation,
                    row.fault_family,
                    row.training_case,
                    row.hidden_transfer_case,
                    int(row.holdout_exposed_to_training),
                    f"{row.learning_latency_days:.9f}",
                    f"{row.lesson_retention_fraction:.9f}",
                    f"{row.transfer_success_fraction:.9f}",
                    f"{row.recurrence_fraction:.9f}",
                    f"{row.recovery_time_days:.9f}",
                    f"{row.verification_compute_hours:.9f}",
                    f"{row.prior_task_regression_fraction:.9f}",
                    int(row.transfer_gate_passes),
                    int(row.retention_gate_passes),
                    int(row.regression_gate_passes),
                    learning_cfg["evidence_status"],
                    learning_cfg["source_class"],
                    learning_cfg["boundary"].strip(),
                ]
            )

    adjusted_stage_rates, campaign_technical_validation_fraction = (
        learning_feedback_to_digital_loop(
            digital_cfg["stage_rates_per_year"],
            learning_rows,
            annual_verification_compute_budget_hours=learning_cfg[
                "annual_verification_compute_budget_hours"
            ],
        )
    )
    campaign_metrics = {
        "median_learning_latency_days": float(
            np.median([row.learning_latency_days for row in learning_rows if row.generation > 0])
        ),
        "mean_lesson_retention_fraction": float(
            np.mean([row.lesson_retention_fraction for row in learning_rows if row.generation > 0])
        ),
        "mean_transfer_success_fraction": float(
            np.mean([row.transfer_success_fraction for row in learning_rows if row.generation > 0])
        ),
        "mean_recurrence_fraction": float(
            np.mean([row.recurrence_fraction for row in learning_rows if row.generation > 0])
        ),
        "mean_verification_compute_hours": float(
            np.mean([row.verification_compute_hours for row in learning_rows if row.generation > 0])
        ),
    }
    feedback_scenarios = {
        "unadjusted_assumption": digital_cfg,
        "synthetic_rehearsal_feedback": {
            **digital_cfg,
            "stage_rates_per_year": adjusted_stage_rates,
            "technical_validation_fraction": (campaign_technical_validation_fraction),
        },
    }
    with open(
        workspace.table_directory / "digital_learning_feedback.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "stage_rates_per_year",
                "experiment_pipeline_throughput_per_year",
                "technical_validation_fraction",
                *campaign_metrics,
                "capability_year20",
                "completed_verified_loops_year20",
                "mean_marginal_gain_per_loop",
                "evidence_status",
                "source_class",
            ]
        )
        for scenario_name, scenario in feedback_scenarios.items():
            result = simulate_digital_progress(
                scenario,
                regime="saturating_frontier",
                years=20.0,
                dt=0.25,
            )
            w.writerow(
                [
                    scenario_name,
                    ";".join(
                        f"{name}={value:g}"
                        for name, value in scenario["stage_rates_per_year"].items()
                    ),
                    f"{verified_loop_bottleneck(scenario['stage_rates_per_year']).rate_per_year:.9f}",
                    f"{scenario['technical_validation_fraction']:.9f}",
                    *(f"{value:.9f}" for value in campaign_metrics.values()),
                    f"{result.capability[-1]:.9f}",
                    f"{result.completed_loops[-1]:.9f}",
                    f"{np.mean(result.marginal_gain_per_loop):.9f}",
                    (
                        "baseline_assumption"
                        if scenario_name == "unadjusted_assumption"
                        else learning_cfg["evidence_status"]
                    ),
                    digital_cfg["source_class"],
                ]
            )

    data_cfg = params.data_advantage
    data_result = data_advantage(
        data_cfg["components"],
        weights=data_cfg["weights"],
        gates=data_cfg["gates"],
    )
    with open(
        workspace.table_directory / "data_advantage_profile.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "component",
                "normalized_value",
                "uncertainty_half_width",
                "assumption_weight",
                "hard_gate",
                "gate_threshold",
                "all_gates_passed",
                "scalar_assumption",
                "source_class",
            ]
        )
        for component, value in data_result.profile.items():
            w.writerow(
                [
                    component,
                    f"{value:.6f}",
                    f"{data_cfg['component_uncertainty_half_width'][component]:.6f}",
                    f"{data_cfg['weights'][component]:.6f}",
                    int(component in data_cfg["gates"]),
                    (
                        f"{data_cfg['gates'][component]:.6f}"
                        if component in data_cfg["gates"]
                        else ""
                    ),
                    int(data_result.gates_passed),
                    f"{data_result.scalar_assumption:.6f}",
                    data_cfg["source_class"],
                ]
            )
