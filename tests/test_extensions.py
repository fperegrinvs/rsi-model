"""Contracts for the explicit post-r4.0 sensitivity models."""

from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np
import pytest
import yaml

from rsimodel.extensions import (
    LIFECYCLE_STATES,
    active_graph_edge_weight,
    chronological_release_backtest,
    cognitive_physical_labor_sweep,
    common_cause_loss_budget,
    coordination_burden,
    coordination_burden_form,
    data_advantage,
    data_evaluator_coevolution,
    debris_control_actions,
    digital_channel_ablations,
    effective_training_compute,
    electronics_supply_chain_sensitivity,
    evaluate_cluster_layout,
    evaluate_degraded_conjunction_control,
    evaluate_embodiment,
    evaluate_milestone_order,
    evaluate_mitigation_portfolio,
    evaluate_multi_operator_capacity,
    evaluate_orbital_service_decision,
    evaluate_transport_service,
    industrial_reliability_ladder,
    learning_feedback_to_digital_loop,
    optimize_compute_allocation,
    partial_closure_metrics,
    replication_governance_externalities,
    rocket_propellant_required,
    simulate_authorized_capacity_control,
    simulate_breakup_cloud,
    simulate_compute_cohorts,
    simulate_digital_progress,
    simulate_intergenerational_learning,
    simulate_orbital_lifecycle,
    simulate_supported_growth,
    verification_hierarchy_sensitivity,
    verified_loop_bottleneck,
    verified_loop_throughput,
)
from rsimodel.orbital_config import replace_transport_service_case

type Config = dict[str, Any]

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def config() -> Config:
    with open(ROOT / "params" / "integrated_model.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_effective_compute_and_verified_loop_bottleneck_are_separate() -> None:
    useful = effective_training_compute(
        100.0,
        hardware_efficiency=0.8,
        utilization=0.5,
        algorithmic_efficiency=1.25,
        architecture_efficiency=1.1,
    )
    assert useful == pytest.approx(55.0)
    rates = {
        "train": 5.0,
        "data": 4.0,
        "experiment": 3.0,
        "evaluate": 7.0,
        "safety": 2.0,
        "deploy": 6.0,
        "observe": 1.5,
    }
    assert verified_loop_throughput(rates) == 1.5
    bottleneck = verified_loop_bottleneck(rates)
    assert bottleneck.binding_stages == ("observe",)
    assert bottleneck.rate_per_year == 1.5


def test_digital_channel_freezes_remove_only_declared_log_contribution(config: Config) -> None:
    rates = config["digital_improvement"]["annual_progress_channels"]
    rows = digital_channel_ablations(rates)
    assert {row.channel for row in rows} >= {
        "compute",
        "data",
        "hardware",
        "algorithm",
        "architecture",
    }
    assert sum(row.removed_log_progress_share for row in rows) == pytest.approx(1.0)
    assert all(row.frozen_annual_multiplier < row.full_annual_multiplier for row in rows)


def test_release_backtest_is_chronological_and_has_no_later_year_leakage(config: Config) -> None:
    cfg = config["chronological_release_backtest"]
    rows, summaries = chronological_release_backtest(cfg)
    assert {row.split for row in rows} == {"train", "validation", "holdout"}
    train_years = {row.release_year for row in rows if row.split == "train"}
    validation_years = {row.release_year for row in rows if row.split == "validation"}
    holdout_years = {row.release_year for row in rows if row.split == "holdout"}
    assert max(train_years) < min(validation_years)
    assert max(validation_years) < min(holdout_years)
    assert all(summary.fit_release_year_max == 2022 for summary in summaries)
    assert all(
        set(summary.fit_model_names) == {"GPT-3 175B", "Gopher 280B", "Chinchilla 70B", "PaLM 540B"}
        for summary in summaries
    )

    mutated = yaml.safe_load(yaml.safe_dump(cfg))
    for release in mutated["releases"]:
        if release["split"] != "train":
            release["mmlu_five_shot_percent"] -= 10.0
    _, mutated_summaries = chronological_release_backtest(mutated)
    coefficients = {
        summary.relation: (
            summary.intercept,
            summary.log_compute_coefficient,
            summary.log_balance_coefficient,
        )
        for summary in summaries
        if summary.split == "train"
    }
    mutated_coefficients = {
        summary.relation: (
            summary.intercept,
            summary.log_compute_coefficient,
            summary.log_balance_coefficient,
        )
        for summary in mutated_summaries
        if summary.split == "train"
    }
    assert mutated_coefficients == coefficients


def test_release_backtest_reports_out_of_time_error_and_lower_bound(config: Config) -> None:
    rows, summaries = chronological_release_backtest(config["chronological_release_backtest"])
    holdout = [
        row for row in rows if row.split == "holdout" and row.relation == "compute_plus_balance"
    ]
    assert len(holdout) == 1
    assert holdout[0].token_count_is_lower_bound
    assert 25.0 < holdout[0].predicted_mmlu_percent < 100.0
    summary_index = {(summary.relation, summary.split): summary for summary in summaries}
    assert (
        summary_index[("compute_plus_balance", "validation")].mean_absolute_error_percentage_points
        < summary_index[("compute_only", "validation")].mean_absolute_error_percentage_points
    )


def test_milestone_order_keeps_closures_and_control_separate(config: Config) -> None:
    rows = evaluate_milestone_order(config["milestone_order_branches"])
    assert {(row.digital_speed, row.physical_speed) for row in rows} >= {
        ("fast", "slow"),
        ("slow", "fast"),
        ("fast", "fast"),
        ("slow", "slow"),
    }
    overhang = next(row for row in rows if row.branch == "fast_digital_slow_physical")
    assert overhang.intelligence_overhang_years == pytest.approx(8.0)
    assert overhang.space_path_timing == "post_ai_rd_construction_path"
    terrestrial = next(
        row for row in rows if row.branch == "terrestrial_acceleration_counterfactual"
    )
    assert terrestrial.first_capital_closure == "Earth"
    assert terrestrial.earth_bridge_cost_multiplier < 1.0
    assert all(row.safety_conditions_pass for row in rows)


def test_authorized_capacity_is_bounded_by_independent_control_rates(config: Config) -> None:
    rows = {
        row.scenario: row
        for row in simulate_authorized_capacity_control(config["authorized_capacity_control"])
    }
    balanced = rows["balanced_independent_control"]
    verification_lag = rows["verification_lag"]
    independent = rows["independent_monitors"]
    correlated = rows["correlated_monitors"]
    authorization = rows["authorization_bottleneck"]

    assert balanced.governance_endpoint_passes
    assert balanced.authorized_operating_capacity[-1] == pytest.approx(
        balanced.gross_operating_capacity[-1]
    )
    assert balanced.first_independent_verification_lag_year is None

    assert not verification_lag.governance_endpoint_passes
    assert verification_lag.human_approval_ceremonial_at_horizon
    assert verification_lag.first_independent_verification_lag_year == 0.0
    assert (
        verification_lag.authorized_operating_capacity[-1]
        < (verification_lag.gross_operating_capacity[-1])
    )

    assert independent.governance_endpoint_passes
    assert not correlated.governance_endpoint_passes
    assert correlated.gross_operating_capacity[-1] == pytest.approx(
        independent.gross_operating_capacity[-1]
    )
    assert (
        correlated.authorized_operating_capacity[-1]
        < (independent.authorized_operating_capacity[-1])
    )
    assert correlated.correlated_monitor_failure_probability > (
        independent.correlated_monitor_failure_probability
    )

    assert not authorization.governance_endpoint_passes
    assert authorization.binding_authorization_limit[-1] == "treaty_limit"
    assert np.all(
        authorization.authorized_high_impact_actions_per_year
        <= authorization.proposed_high_impact_actions_per_year + 1e-12
    )
    assert np.all(
        authorization.authorized_high_impact_actions_per_year
        <= authorization.reliability_verification_capacity_per_year + 1e-12
    )
    assert np.all(
        authorization.authorized_high_impact_actions_per_year
        <= authorization.adversarial_verification_capacity_per_year + 1e-12
    )


def test_compute_allocation_conserves_hours_and_exposes_opportunity_cost(config: Config) -> None:
    rows = optimize_compute_allocation(config["ai_rd_compute_allocation"])
    assert len(rows) == 9
    for row in rows:
        allocated = sum(
            (
                row.training_hours,
                row.research_inference_hours,
                row.experiment_hours,
                row.data_generation_filtering_hours,
                row.verification_safety_hours,
                row.external_productive_service_hours,
            )
        )
        assert allocated == pytest.approx(row.total_physical_accelerator_hours)
        assert row.automated_researcher_instances <= (row.useful_research_task_limit + 1e-12)
        assert row.verified_progress_rate <= (row.raw_capability_progress_rate + 1e-12)
        assert row.effective_training_hours == pytest.approx(
            row.training_hours * row.algorithmic_efficiency
        )

    central = {row.objective: row for row in rows if row.algorithmic_efficiency == 1.0}
    assert central["raw_capability"].verification_safety_hours == 0.0
    assert central["raw_capability"].verified_progress_rate == 0.0
    assert central["verified_progress"].verified_progress_rate > 0.0
    assert central["physical_growth"].external_productive_service_hours == (
        central["physical_growth"].total_physical_accelerator_hours
    )
    assert central["verified_progress"].foregone_external_revenue > (
        central["physical_growth"].foregone_external_revenue
    )

    verified = sorted(
        (
            row.algorithmic_efficiency,
            row.verified_progress_rate,
        )
        for row in rows
        if row.objective == "verified_progress"
    )
    assert verified[0][1] < verified[-1][1]


def test_cognitive_copies_do_not_create_physical_agents(config: Config) -> None:
    rows = cognitive_physical_labor_sweep(config["cognitive_physical_labor"])
    million = next(row for row in rows if row.model_instances == 1_000_000)
    assert million.active_cognitive_instances == 200_000
    assert million.effective_physical_agents == 20.0
    assert million.physical_output_units_per_year == 20.0
    assert million.waiting_or_contention_instances > 990_000
    assert million.serial_wall_clock_floor_years == pytest.approx(1.2)
    assert million.combined_experiment_program_years >= (million.serial_wall_clock_floor_years)
    assert million.duplicate_work_fraction > 0.9

    one = next(row for row in rows if row.model_instances == 1)
    ten = next(row for row in rows if row.model_instances == 10)
    assert one.effective_physical_agents == 1.0
    assert ten.effective_physical_agents == 10.0
    assert million.onboarding_hours_per_active_instance < (ten.onboarding_hours_per_active_instance)
    assert million.total_onboarding_hours > ten.total_onboarding_hours
    assert million.coordination_graph_edges > ten.coordination_graph_edges
    assert million.verification_demand_units_per_year > (ten.verification_demand_units_per_year)


def test_ai_electronics_tiers_are_heterogeneous_and_sequence_resilience(config: Config) -> None:
    rows = electronics_supply_chain_sensitivity(config["ai_electronics_supply_chain"])
    assert len(rows) == 8
    assert [row.closure_sequence_rank for row in rows] == list(range(1, 9))
    assert len({row.shelf_life_years for row in rows}) > 1
    assert len({row.economic_obsolescence_fraction_per_year for row in rows}) > 1
    assert all(row.cumulative_reused_downbinned_units > 0.0 for row in rows)

    early = rows[:3]
    frontier = rows[-2:]
    assert all(not row.continuing_earth_umbilical for row in early)
    assert all(row.continuing_earth_umbilical for row in frontier)
    assert min(row.early_resilience_per_localization_effort for row in early) > max(
        row.early_resilience_per_localization_effort for row in frontier
    )
    assert {row.tier for row in rows} == {
        "front_end_logic_fabrication",
        "memory_fabrication",
        "advanced_packaging",
        "substrates_interposers",
        "high_speed_interconnect",
        "power_electronics",
        "test_metrology",
        "radiation_qualified_system_integration",
    }


def test_compute_cohorts_reassign_obsolete_but_functional_hardware(config: Config) -> None:
    rows, summaries = simulate_compute_cohorts(config["compute_cohort_obsolescence"])
    assert rows
    assert len(summaries) == 2
    for summary in summaries:
        assert summary.terminal_physical_units > 0.0
        assert summary.cumulative_physical_failure_units > 0.0
        assert summary.terminal_reassigned_units > 0.0
        assert summary.terminal_frontier_training_units > 0.0
        assert summary.terminal_economically_obsolete_but_functional_units == (
            summary.terminal_reassigned_units
        )
        assert 0.0 < summary.reassigned_share_of_functional_stock < 1.0

    assignments = {
        row.assigned_workload
        for row in rows
        if row.year == config["compute_cohort_obsolescence"]["years"]
    }
    assert assignments >= {
        "frontier_training",
        "inference",
        "verification",
        "simulation_nonfrontier",
    }
    convergence = next(
        summary
        for summary in summaries
        if summary.scenario == "architectural_convergence_with_persistent_turnover"
    )
    assert convergence.terminal_economically_obsolete_but_functional_units > (
        0.5 * convergence.terminal_physical_units
    )


def test_verifier_classes_are_not_collapsed_into_iteration_count(config: Config) -> None:
    rows = verification_hierarchy_sensitivity(config["verification_hierarchy"])
    baseline = {row.verifier_class: row for row in rows if row.stress_scenario == "baseline"}
    assert list(baseline) == [
        "formal_invariant",
        "destructive_physical_acceptance",
        "independent_heldout_experiment",
        "causal_operational_outcome",
        "human_ai_rubric",
        "model_self_assessment",
    ]
    self_scored = baseline["model_self_assessment"]
    physical = baseline["destructive_physical_acceptance"]
    assert self_scored.candidate_iterations_per_year == 1000.0
    assert self_scored.independently_supported_iterations_per_year == 0.0
    assert physical.candidate_iterations_per_year == 1.0
    assert physical.independently_supported_iterations_per_year > 0.0

    self_confirming = {
        row.verifier_class: row for row in rows if row.stress_scenario == "self_confirming_loop"
    }
    assert (
        self_confirming["independent_heldout_experiment"].evaluator_false_positive_fraction
        > baseline["independent_heldout_experiment"].evaluator_false_positive_fraction
    )
    assert (
        self_confirming["independent_heldout_experiment"].evaluator_independence_score
        < baseline["independent_heldout_experiment"].evaluator_independence_score
    )
    assert (
        self_confirming["formal_invariant"].observed_positive_share_after_filtering
        > baseline["formal_invariant"].observed_positive_share_after_filtering
    )
    assert all(
        row.direction_limited_licensed_loops_per_year
        <= row.research_direction_setting_per_year + 1e-12
        for row in rows
    )


def test_industrial_reliability_is_consequence_and_rung_specific(config: Config) -> None:
    rows = {
        row.task: row
        for row in industrial_reliability_ladder(config["industrial_reliability_ladder"])
    }
    cheap = rows["cheap_reversible_search"]
    assert cheap.measured_success_fraction == 0.50
    assert cheap.economic_substitution_passes

    destructive = rows["destructive_fabrication_batch"]
    launch = rows["launch_commit"]
    power = rows["critical_power_switching"]
    replication = rows["replication_authorization"]
    assert not destructive.economic_substitution_passes
    assert not launch.economic_substitution_passes
    assert not power.economic_substitution_passes
    assert not replication.economic_substitution_passes

    commissioning = rows["autonomous_commissioning"]
    assert commissioning.economic_substitution_passes
    assert commissioning.achieved_rung == "sustained_bounded_intervention"

    # Rare failures can dominate human cleanup even when interventions are
    # infrequent.
    assert launch.intervention_events_per_100_tasks < (
        rows["high_context_production_code"].intervention_events_per_100_tasks
    )
    assert launch.expected_total_human_hours_per_task > (
        rows["high_context_production_code"].expected_total_human_hours_per_task
    )


def test_synthetic_volume_can_diverge_from_heldout_signal(config: Config) -> None:
    rows = data_evaluator_coevolution(config["data_evaluator_coevolution"])
    by_scenario = {
        scenario: sorted(
            (row for row in rows if row.scenario == scenario),
            key=lambda row: row.generation,
        )
        for scenario in {row.scenario for row in rows}
    }
    governed = by_scenario["governed_balanced"][-1]
    volume = by_scenario["synthetic_volume_maximization"][-1]
    open_pressure = by_scenario["open_replication_pressure"][-1]

    assert volume.synthetic_records_generated > (governed.synthetic_records_generated)
    assert volume.apparent_progress_index > governed.apparent_progress_index
    assert volume.heldout_transfer_index < governed.heldout_transfer_index
    assert volume.evaluator_error_fraction > governed.evaluator_error_fraction
    assert volume.evaluator_bias_fraction > governed.evaluator_bias_fraction
    assert volume.data_diversity_index < governed.data_diversity_index
    assert volume.physical_causal_episodes == 25.0
    assert governed.physical_causal_episodes == 100.0
    assert open_pressure.proprietary_data_advantage_index < (
        governed.proprietary_data_advantage_index
    )
    assert all(
        row.synthetic_records_after_deduplication <= row.synthetic_records_generated for row in rows
    )


def test_engineering_success_can_be_governance_failure(config: Config) -> None:
    rows = {
        row.scenario: row
        for row in replication_governance_externalities(
            config["replication_governance_externalities"]
        )
    }
    cooperative = rows["cooperative_authorized"]
    race = rows["private_replication_race"]
    treaty = rows["treaty_limited_shared_claims"]
    assert cooperative.engineering_endpoint_succeeds
    assert cooperative.governance_endpoint_succeeds
    assert treaty.engineering_endpoint_succeeds
    assert treaty.governance_endpoint_succeeds

    assert race.engineering_endpoint_succeeds
    assert race.private_objective_succeeds
    assert not race.governance_endpoint_succeeds
    assert race.negative_sum_race
    assert race.social_net_value < 0.0 < race.private_net_value
    assert race.unauthorized_capacity[-1] > (race.legitimately_authorized_capacity[-1])
    assert race.contested_resource_preempting_capacity[-1] > 0.0
    assert race.cumulative_owner_claim[-1] > (race.cumulative_future_affected_party_claim[-1])
    assert race.material_governance_leverage[-1] < (cooperative.material_governance_leverage[-1])


def test_hidden_fault_transfer_metrics_feed_digital_loop(config: Config) -> None:
    cfg = config["intergenerational_learning_rehearsal"]
    rows = simulate_intergenerational_learning(cfg)
    assert len(rows) == cfg["generations"] * len(cfg["fault_families"])
    assert all(not row.holdout_exposed_to_training for row in rows)
    assert all(row.regression_gate_passes for row in rows)
    assert all(
        row.transfer_gate_passes and row.retention_gate_passes and row.regression_gate_passes
        for row in rows
        if row.generation > 0
    )
    for family in cfg["fault_families"]:
        family_rows = [row for row in rows if row.fault_family == family]
        assert family_rows[1].recurrence_fraction < (family_rows[0].recurrence_fraction)
        assert family_rows[1].recovery_time_days < (family_rows[0].recovery_time_days)

    base = config["digital_improvement"]["stage_rates_per_year"]
    adjusted, verified_yield = learning_feedback_to_digital_loop(
        base,
        rows,
        annual_verification_compute_budget_hours=cfg["annual_verification_compute_budget_hours"],
    )
    assert 0.0 < verified_yield < 1.0
    assert adjusted["evaluate"] < base["evaluate"]
    assert adjusted["safety"] < base["safety"]
    assert adjusted["observe"] < base["observe"]
    assert verified_loop_throughput(adjusted) < verified_loop_throughput(base)


def test_elasticity_correlation_assumption_is_valid(config: Config) -> None:
    cfg = config["digital_improvement"]
    names = cfg["elasticity_correlation_order"]
    correlation = np.asarray(cfg["elasticity_correlation_matrix"], dtype=float)
    assert correlation.shape == (len(names), len(names))
    assert np.allclose(correlation, correlation.T)
    assert np.allclose(np.diag(correlation), 1.0)
    assert np.linalg.eigvalsh(correlation).min() >= -1e-12
    assert set(names) == set(cfg["elasticity_bounds"])
    for lower, central, upper in cfg["elasticity_bounds"].values():
        assert 0.0 <= lower <= central <= upper


def test_coordination_forms_share_reference_and_irreducible_limit(config: Config) -> None:
    cfg = config["coordination_model"]
    base = {
        "irreducible_hours": cfg["irreducible_hours"],
        "reference_hours": cfg["reference_hours"],
        "active_edge_weight": cfg["edge_reference"],
        "edge_reference": cfg["edge_reference"],
        "complexity": cfg["complexity_reference"],
        "complexity_reference": cfg["complexity_reference"],
        "uncertainty": cfg["uncertainty_reference"],
        "uncertainty_reference": cfg["uncertainty_reference"],
        "effective_intelligence": cfg["intelligence_reference"],
        "intelligence_reference": cfg["intelligence_reference"],
        "alpha": cfg["alpha"],
        "beta": cfg["beta"],
        "gamma": cfg["gamma"],
        "delta": cfg["delta"],
        "intelligence_response": cfg["intelligence_response"],
    }
    values = {
        form: coordination_burden_form(form, **base)
        for form in ("power", "logarithmic", "saturating")
    }
    assert values["power"] == pytest.approx(values["logarithmic"])
    assert values["power"] == pytest.approx(values["saturating"])
    for form in values:
        zero = coordination_burden_form(
            form,
            **{**base, "active_edge_weight": 0.0},
        )
        assert zero == pytest.approx(cfg["irreducible_hours"])
    with pytest.raises(ValueError):
        coordination_burden_form("unknown", **base)


def test_three_digital_regimes_have_diminishing_gain_and_innovation(config: Config) -> None:
    cfg = config["digital_improvement"]
    smooth = simulate_digital_progress(
        cfg,
        regime="smooth_diminishing",
        years=20.0,
    )
    saturating = simulate_digital_progress(
        cfg,
        regime="saturating_frontier",
        years=20.0,
    )
    interrupted = simulate_digital_progress(
        cfg,
        regime="innovation_interrupted",
        years=20.0,
    )
    for result in (smooth, saturating, interrupted):
        assert np.all(np.diff(result.capability) >= -1e-12)
        assert np.all(result.verified_loops_per_year >= 0.0)
        assert result.capability[-1] > result.capability[0]
    assert smooth.marginal_gain_per_loop[-1] < smooth.marginal_gain_per_loop[0]
    assert saturating.capability[-1] <= saturating.frontier[-1] + 1e-12
    assert interrupted.frontier[-1] > saturating.frontier[-1]
    assert interrupted.capability[-1] > saturating.capability[-1]


def test_digital_capability_gates_separate_internal_and_public_clocks(config: Config) -> None:
    cfg = config["digital_improvement"]
    zero_lag = simulate_digital_progress(
        cfg,
        regime="saturating_frontier",
        gate_case="zero_lag",
        years=8.0,
    )
    slower = simulate_digital_progress(
        cfg,
        regime="saturating_frontier",
        gate_case="slower_publication",
        years=8.0,
    )
    overhang = simulate_digital_progress(
        cfg,
        regime="saturating_frontier",
        gate_case="internal_capability_overhang",
        years=8.0,
    )

    assert np.allclose(zero_lag.internal_capability, zero_lag.public_capability)
    assert np.all(slower.experiment_loops_per_year >= slower.technically_validated_loops_per_year)
    assert np.all(
        slower.technically_validated_loops_per_year >= slower.internally_authorized_loops_per_year
    )
    assert np.all(slower.capability_overhang >= -1e-12)
    assert np.max(slower.capability_overhang) > 0.0
    assert np.max(overhang.capability_overhang) > np.max(slower.capability_overhang)
    assert np.allclose(slower.internal_capability, overhang.internal_capability)
    assert slower.public_release_events[-1] > overhang.public_release_events[-1]


def test_public_release_assumptions_do_not_change_internal_capability(config: Config) -> None:
    cfg = deepcopy(config["digital_improvement"])
    baseline = simulate_digital_progress(
        cfg,
        regime="saturating_frontier",
        gate_case="slower_publication",
        years=8.0,
    )
    cfg["capability_gate_cases"]["slower_publication"].update(
        {
            "public_authorization_fraction": 0.0,
            "public_capability_slice_fraction": 0.0,
            "public_release_interval_years": 8.0,
        }
    )
    no_public_release = simulate_digital_progress(
        cfg,
        regime="saturating_frontier",
        gate_case="slower_publication",
        years=8.0,
    )
    assert np.allclose(
        baseline.internal_capability,
        no_public_release.internal_capability,
    )
    assert no_public_release.public_capability[-1] == pytest.approx(cfg["initial_capability"])


def test_technical_validation_is_required_for_capability_compounding(config: Config) -> None:
    cfg = deepcopy(config["digital_improvement"])
    cfg["technical_validation_fraction"] = 0.0
    result = simulate_digital_progress(
        cfg,
        regime="saturating_frontier",
        gate_case="zero_lag",
        years=4.0,
    )
    assert np.allclose(result.internal_capability, cfg["initial_capability"])
    assert np.allclose(result.public_capability, cfg["initial_capability"])
    assert np.allclose(result.completed_technical_validations, 0.0)
    assert result.completed_experiments[-1] > 0.0


def test_data_advantage_uses_hard_gates_and_geometric_scalar(config: Config) -> None:
    cfg = config["data_advantage"]
    passing = data_advantage(
        cfg["components"],
        weights=cfg["weights"],
        gates=cfg["gates"],
    )
    assert passing.gates_passed
    assert 0.0 < passing.scalar_assumption < 1.0
    blocked_components = dict(cfg["components"])
    blocked_components["verification"] = 0.1
    blocked = data_advantage(
        blocked_components,
        weights=cfg["weights"],
        gates=cfg["gates"],
    )
    assert not blocked.gates_passed
    assert blocked.scalar_assumption == 0.0


def test_coordination_preserves_floor_and_uses_graph_edges(config: Config) -> None:
    cfg = config["coordination_model"]
    modular = active_graph_edge_weight(np.asarray(cfg["topology_examples"]["modular"]))
    all_to_all = active_graph_edge_weight(np.asarray(cfg["topology_examples"]["all_to_all"]))

    def burden(edges: float, intelligence: float) -> float:
        return coordination_burden(
            irreducible_hours=cfg["irreducible_hours"],
            reference_hours=cfg["reference_hours"],
            active_edge_weight=edges,
            edge_reference=cfg["edge_reference"],
            complexity=1.0,
            complexity_reference=cfg["complexity_reference"],
            uncertainty=1.0,
            uncertainty_reference=cfg["uncertainty_reference"],
            effective_intelligence=intelligence,
            intelligence_reference=cfg["intelligence_reference"],
            alpha=cfg["alpha"],
            beta=cfg["beta"],
            gamma=cfg["gamma"],
            delta=cfg["delta"],
            intelligence_response=cfg["intelligence_response"],
        )

    assert burden(all_to_all, 1.0) > burden(modular, 1.0)
    assert burden(modular, 4.0) < burden(modular, 1.0)
    assert burden(modular, 1e9) >= cfg["irreducible_hours"]


def test_embodiment_separates_physical_gate_intelligence_and_verification(config: Config) -> None:
    cfg = config["embodiment_compatibility"]
    task = cfg["tasks"]["maintenance"]
    years = np.arange(0.0, 11.0)
    intelligence = np.linspace(0.8, 4.0, len(years))
    verified = np.ones(len(years), dtype=bool)
    verified[:7] = False
    adequate = evaluate_embodiment(
        task="maintenance",
        portfolio="hybrid",
        requirements=task["requirements"],
        embodiment=cfg["portfolios"]["hybrid"],
        intelligence=intelligence,
        years=years,
        verification=verified,
        intelligence_onset=task["intelligence_onset"],
        intelligence_scale=task["intelligence_scale"],
        required_score=task["required_score"],
    )
    assert adequate.physically_adequate
    assert adequate.intelligence_threshold is not None
    assert adequate.first_passage_year is not None
    assert adequate.first_passage_year >= 7.0

    inadequate = evaluate_embodiment(
        task="maintenance",
        portfolio="general_purpose",
        requirements=task["requirements"],
        embodiment=cfg["portfolios"]["general_purpose"],
        intelligence=intelligence,
        years=years,
        intelligence_onset=task["intelligence_onset"],
        intelligence_scale=task["intelligence_scale"],
        required_score=task["required_score"],
    )
    assert not inadequate.physically_adequate
    assert inadequate.first_passage_year is None
    assert inadequate.failure_attribution == "embodiment_limited"


def test_embodiment_two_direction_and_degraded_fault_sensitivities(config: Config) -> None:
    cfg = config["embodiment_compatibility"]
    task = cfg["tasks"]["maintenance"]
    base = cfg["portfolios"]["hybrid"]
    low_i = evaluate_embodiment(
        task="maintenance",
        portfolio="hybrid",
        requirements=task["requirements"],
        embodiment=base,
        intelligence=[1.0],
        years=[0.0],
        intelligence_onset=task["intelligence_onset"],
        intelligence_scale=task["intelligence_scale"],
        required_score=task["required_score"],
    )
    high_i = evaluate_embodiment(
        task="maintenance",
        portfolio="hybrid",
        requirements=task["requirements"],
        embodiment=base,
        intelligence=[4.0],
        years=[0.0],
        intelligence_onset=task["intelligence_onset"],
        intelligence_scale=task["intelligence_scale"],
        required_score=task["required_score"],
    )
    assert high_i.score_trajectory[0] > low_i.score_trajectory[0]

    degraded = dict(base)
    degraded["sensor_observability"] *= 0.60
    degraded_result = evaluate_embodiment(
        task="maintenance",
        portfolio="hybrid_degraded_sensors",
        requirements=task["requirements"],
        embodiment=degraded,
        intelligence=[4.0],
        years=[0.0],
        intelligence_onset=task["intelligence_onset"],
        intelligence_scale=task["intelligence_scale"],
        required_score=task["required_score"],
    )
    assert not degraded_result.physically_adequate
    assert "sensor_observability" in degraded_result.failed_dimensions
    assert degraded_result.failure_attribution == "embodiment_limited"


def test_partial_closure_reports_import_leverage_without_claiming_autonomy() -> None:
    metrics = partial_closure_metrics(
        local_mass_flow={"structure": 999.0, "electronics": 0.0},
        external_mass_flow={"structure": 0.0, "electronics": 1.0},
        verified_capacity_added_per_year=100.0,
        critical_inputs=("electronics",),
    )
    assert metrics.mass_closure_fraction == pytest.approx(0.999)
    assert not metrics.strict_autonomy
    assert metrics.import_leverage == pytest.approx(100.0)
    assert metrics.critical_external_inputs == ("electronics",)


def test_four_partial_closure_support_policies_expose_supply_constraint(config: Config) -> None:
    cfg = config["partial_closure_support"]
    results = {name: simulate_supported_growth(cfg, policy=name) for name in cfg["policies"]}
    assert set(results) == {
        "fixed_annual_imports",
        "capacity_proportional_imports",
        "finite_initial_stockpile",
        "declining_disrupted_imports",
    }
    for result in results.values():
        assert np.all(result.capacity >= 0.0)
        assert np.all(result.inventory >= -1e-12)
        assert len(result.binding_input) == len(result.t)
        assert np.all(result.supplier_utilization >= 0.0)
        assert np.all(result.supplier_utilization <= 1.0 + 1e-12)
        assert len(result.supplier_binding_resource) == len(result.t)
    finite = results["finite_initial_stockpile"]
    assert finite.first_stockout_year is not None
    assert finite.capacity[-1] < results["capacity_proportional_imports"].capacity[-1]
    disrupted = results["declining_disrupted_imports"]
    assert disrupted.capacity_loss[12:18].sum() > 0.0
    names = tuple(cfg["residual_inputs"])
    electronics = names.index("advanced_electronics")
    metrology = names.index("calibration_metrology")
    assert disrupted.substitution_validated[:, electronics].any()
    assert disrupted.substitution_failed[:, metrology].any()
    assert disrupted.substitution_effort[-1].sum() > 0.0
    for program in cfg["substitution_programs"].values():
        assert sum(program["effort_resource_shares"].values()) == pytest.approx(1.0)
    allocation = {
        name: simulate_supported_growth(cfg, policy=name) for name in cfg["allocation_policies"]
    }
    assert allocation["substitution_first"].substitution_effort[-1].sum() > (
        allocation["immediate_expansion"].substitution_effort[-1].sum()
    )
    assert allocation["stockpile_first"].inventory[-1].sum() >= (
        allocation["immediate_expansion"].inventory[-1].sum()
    )


def test_orbital_lifecycle_conserves_stock_and_exposes_returns(config: Config) -> None:
    cfg = config["orbital_lifecycle"]
    result = simulate_orbital_lifecycle(cfg, years=20.0, dt=0.1)
    external = float(result.flows["external_deployment"].sum())
    assert result.stocks[-1].sum() == pytest.approx(
        cfg["initial_operating"] + external,
        rel=1e-10,
        abs=1e-10,
    )
    assert set(LIFECYCLE_STATES) == {
        "operating",
        "degraded",
        "awaiting_service",
        "under_repair",
        "cannibalized",
        "salvaged",
        "recycled_feedstock",
        "disposed_waste",
        "uncontrolled_debris",
    }
    assert result.flows["repair_return"].sum() > 0.0
    assert result.flows["recycled"].sum() > 0.0
    assert result.flows["debris_retrieved"].sum() > 0.0
    assert result.effective_irreversible_loss_per_year > 0.0


def test_transport_service_uses_rocket_equation_and_maturity_gate(config: Config) -> None:
    low = rocket_propellant_required(
        1000.0,
        delta_v_km_s=1.9,
        specific_impulse_s=450.0,
    )
    high = rocket_propellant_required(
        1000.0,
        delta_v_km_s=9.0,
        specific_impulse_s=450.0,
    )
    assert high > low > 0.0
    cases = config["orbital_transport_service"]["cases"]
    lunar = evaluate_transport_service(cases["lunar_supplied_lunar_orbit"])
    assert lunar.available
    assert lunar.annual_missions > 0.0
    immature = replace_transport_service_case(
        cases["lunar_supplied_lunar_orbit"],
        lunar_industrial_maturity=0.2,
    )
    assert not evaluate_transport_service(immature).available


def test_orbital_service_decisions_separate_three_feasibility_gates(config: Config) -> None:
    cfg = config["orbital_service_strategy"]
    results = [
        evaluate_orbital_service_decision(
            orbit_name=orbit_name,
            orbit=orbit,
            asset_name=asset_name,
            asset=asset,
            fleet_name=fleet_name,
            fleet=fleet,
            action_name=action_name,
            action=action,
            governance=cfg["governance"],
        )
        for orbit_name, orbit in cfg["orbits"].items()
        for asset_name, asset in cfg["asset_classes"].items()
        for fleet_name, fleet in cfg["fleets"].items()
        for action_name, action in cfg["actions"].items()
    ]
    assert len(results) == 6 * 2 * 3 * 9
    assert {row.action for row in results} == {
        "replace",
        "refuel_life_extend",
        "repair",
        "upgrade",
        "cannibalize",
        "repurpose",
        "recycle",
        "relocate",
        "dispose",
    }
    assert any(row.technically_feasible for row in results)
    assert any(not row.technically_feasible for row in results)
    assert any(row.economic_viable for row in results)
    assert all(not row.governance_ready for row in results)
    assert all(
        row.deployable
        == (row.technically_feasible and row.economic_viable and row.governance_ready)
        for row in results
    )

    high_repair = next(
        row
        for row in results
        if row.orbit == "leo_400"
        and row.asset_class == "high_value_serviceable"
        and row.fleet == "regional_service_fleet"
        and row.action == "repair"
    )
    cheap_repair = next(
        row
        for row in results
        if row.orbit == "leo_400"
        and row.asset_class == "cheap_short_lived_unprepared"
        and row.fleet == "regional_service_fleet"
        and row.action == "repair"
    )
    assert high_repair.technically_feasible
    assert high_repair.economic_viable
    assert not cheap_repair.technically_feasible

    single = next(
        row
        for row in results
        if row.orbit == "leo_400"
        and row.asset_class == "high_value_serviceable"
        and row.fleet == "single_demonstrator"
        and row.action == "replace"
    )
    network = next(
        row
        for row in results
        if row.orbit == "leo_400"
        and row.asset_class == "high_value_serviceable"
        and row.fleet == "circular_network"
        and row.action == "replace"
    )
    assert network.annual_fleet_capacity > single.annual_fleet_capacity
    assert network.fixed_cost_per_client_musd < single.fixed_cost_per_client_musd


def test_common_cause_budget_and_control_triggers(config: Config) -> None:
    cfg = config["orbital_control"]
    result = common_cause_loss_budget(
        cfg["node_capacities"],
        cfg["hazard_sets"],
        epsilon=cfg["common_cause_budget_fraction"],
    )
    assert result.maximum_loss_fraction <= 0.10
    assert result.passes
    actions = debris_control_actions(
        {
            "creation_clearance_ratio": 1.2,
            "tracking_uncertainty": 0.4,
            "disposal_failure_fraction": 0.2,
        },
        cfg["trigger_thresholds"],
    )
    assert "pause_deployment" in actions
    assert "reduce_cluster_cap" in actions
    assert "retire_shell" in actions


def test_geometry_breakup_and_degraded_control_are_explicit(config: Config) -> None:
    cfg = config["orbital_resilience_strategy"]
    layouts = {
        name: evaluate_cluster_layout(
            name,
            values,
            collision_exposure_index=cfg["collision_exposure_index"],
            common_cause_budget_fraction=cfg["common_cause_budget_fraction"],
        )
        for name, values in cfg["cluster_layouts"].items()
    }
    assert layouts["multi_shell_resilient"].passes_loss_budget
    assert not layouts["concentrated_single_plane"].passes_loss_budget
    assert not layouts["physically_distributed_gateway_fragile"].passes_loss_budget
    assert (
        layouts["multi_shell_resilient"].correlated_fragment_exposure
        < layouts["concentrated_single_plane"].correlated_fragment_exposure
    )

    breakup = {
        name: simulate_breakup_cloud(
            cfg["constellation_nodes"],
            event,
            days=365,
        )
        for name, event in cfg["breakup_events"].items()
    }
    for result in breakup.values():
        assert result.direct_loss_capacity == pytest.approx(1.0)
        assert result.expected_secondary_collisions > 0.0
        assert result.expected_avoidance_maneuvers > 0.0
        assert result.service_interruption_capacity_days > 0.0
        assert result.repair_load_capacity >= result.direct_loss_capacity
        assert np.all(result.active_capacity >= 0.0)
        assert np.all(result.fragment_cloud >= 0.0)
    assert (
        breakup["low_lunar_orbit_breakup"].fragment_cloud[-1]
        > breakup["leo_650_breakup"].fragment_cloud[-1]
    )

    stress = cfg["conjunction_stress"]
    controls = [
        evaluate_degraded_conjunction_control(
            name,
            scenario,
            conjunctions=stress["conjunctions"],
            collision_probability_per_unsafe_conjunction=stress[
                "collision_probability_per_unsafe_conjunction"
            ],
            risk_limit=stress["risk_limit"],
        )
        for name, scenario in stress["scenarios"].items()
    ]
    assert any(not result.safe_before_fallback for result in controls)
    assert all(result.safe_after_fallback for result in controls)
    assert any("independent_tracking" in result.fallback_actions for result in controls)


def test_mitigation_pareto_inputs_and_multi_operator_capacity(config: Config) -> None:
    cfg = config["orbital_resilience_strategy"]
    mitigation = cfg["mitigation_portfolio"]
    low = {name: values[0] for name, values in mitigation["levels"].items()}
    high = {name: values[-1] for name, values in mitigation["levels"].items()}
    high["deployment_cadence"] = low["deployment_cadence"]
    low_result = evaluate_mitigation_portfolio(low, mitigation)
    high_result = evaluate_mitigation_portfolio(high, mitigation)
    assert high_result.residual_risk_index < low_result.residual_risk_index
    assert high_result.lifecycle_cost_index > low_result.lifecycle_cost_index

    multi = cfg["multi_operator"]
    coordinated = evaluate_multi_operator_capacity(
        "leo_650",
        multi["shells"]["leo_650"],
        multi["scenarios"]["coordinated_authorized"],
    )
    uncoordinated = evaluate_multi_operator_capacity(
        "leo_650",
        multi["shells"]["leo_650"],
        multi["scenarios"]["uncoordinated_growth"],
    )
    assert coordinated.admissible
    assert not uncoordinated.capacity_compliant
    assert not uncoordinated.governance_compliant
    assert uncoordinated.uncoordinated_workload > (coordinated.uncoordinated_workload)
