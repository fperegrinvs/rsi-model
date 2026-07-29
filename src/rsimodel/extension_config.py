"""Closed schemas for integrated-model extension configuration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal, NotRequired, TypedDict


class EvidenceMetadata(TypedDict):
    source_class: str
    evidence_status: str
    boundary: str


class IntelligenceResponseRegime(TypedDict):
    scenario: str
    operational_constraints_enabled: bool
    import_stock_multiplier: float | None
    complementary_stock_boundary: str


class IntelligenceMarginalResponseConfig(EvidenceMetadata):
    years: float
    dt: float
    intelligence_uplift: float
    near_zero_response_threshold: float
    regimes: Mapping[str, IntelligenceResponseRegime]


class BottleneckUpgradeProject(TypedDict):
    constraint: str
    constraint_class: Literal[
        "intelligence_reducible",
        "physical_floor",
        "observation_time",
        "external_authority",
    ]
    intelligence_can_reduce: bool
    initial_capacity: float
    capacity_increment: float
    cost_capacity_years: float
    available_budget_capacity_years: float
    design_lag_years: float
    construction_lag_years: float
    verification_lag_years: float
    productive_capacity_available: bool
    verified_causal_path: bool
    productive_sector: str
    causal_path: str


class BottleneckUpgradeConfig(EvidenceMetadata):
    years: float
    dt: float
    projects: Mapping[str, BottleneckUpgradeProject]


class ComputeDemandBranch(TypedDict):
    demand_type: Literal["non_saturating", "bounded"]
    initial_valuable_demand: float
    valuable_demand_ceiling: NotRequired[float]
    demand_growth_rate: float
    priority_switch_year: float
    early_humanitarian_share: float
    late_humanitarian_share: float
    science_public_goods_share: float
    relocated_harmful_activity_share: float


class ComputeDemandConfig(EvidenceMetadata):
    years: float
    dt: float
    initial_compute_capacity: float
    annual_compute_capacity_growth_fraction: float
    initial_activity_reference: float
    branches: Mapping[str, ComputeDemandBranch]


class ReleaseBacktestObservation(TypedDict):
    model: str
    release_date: str
    release_year: int
    split: Literal["train", "validation", "holdout"]
    parameters_billion: float
    training_tokens_billion: float
    token_count_is_lower_bound: bool
    mmlu_five_shot_percent: float
    source_id: str
    source_locator: str


class ChronologicalReleaseBacktestConfig(TypedDict):
    evidence_status: str
    source_class: str
    split_declared_before_fit: bool
    split_rule: str
    target_definition: str
    compute_proxy_definition: str
    chance_accuracy_percent: float
    score_ceiling_percent: float
    compute_reference_flop: float
    target_tokens_per_parameter: float
    relations: tuple[Literal["compute_only", "compute_plus_balance"], ...]
    releases: tuple[ReleaseBacktestObservation, ...]


class MilestoneBranch(TypedDict):
    name: str
    digital_speed: Literal["fast", "slow"]
    physical_speed: Literal["fast", "slow"]
    ai_rd_closure_year: float
    embodiment_closure_year: float
    earth_capital_closure_year: float
    space_capital_closure_year: float
    control_readiness_year: float
    earth_bridge_cost_multiplier: float


class MilestoneOrderConfig(EvidenceMetadata):
    branches: tuple[MilestoneBranch, ...]


class CapabilityState(TypedDict):
    task: float
    coordination: float
    evaluator: float
    controllability_confidence: float


class AuthorizedCapacityScenario(TypedDict):
    capability_state: CapabilityState
    initial_gross_capacity: float
    initial_authorized_capacity: float
    gross_replication_rate_per_year: float
    high_impact_actions_per_added_capacity: float
    annual_control_capacity_growth_fraction: float
    independent_verification_actions_per_year: float
    reliability_test_coverage_fraction: float
    adversarial_test_coverage_fraction: float
    secure_command_actions_per_year: float
    environmental_limit_actions_per_year: float
    treaty_limit_actions_per_year: float
    human_approval_required: bool
    human_comprehension_actions_per_year: float
    producer_monitor_failure_probability: float
    evaluator_monitor_failure_probability: float
    monitor_failure_correlation: float
    evaluator_independence: Mapping[str, float]


class AuthorizedCapacityControlConfig(EvidenceMetadata):
    years: float
    dt: float
    evaluator_capability_reference: float
    maximum_unauthorized_capacity_fraction: float
    independence_dimensions: tuple[str, ...]
    scenarios: Mapping[str, AuthorizedCapacityScenario]


class ComputeAllocationConfig(EvidenceMetadata):
    categories: tuple[str, ...]
    objectives: tuple[
        Literal["raw_capability", "verified_progress", "physical_growth"],
        ...,
    ]
    total_physical_accelerator_hours_per_year: float
    allocation_grid_units: int
    algorithmic_efficiency_sensitivity: tuple[float, ...]
    useful_research_tasks: float
    inference_hours_per_researcher_instance: float
    candidate_rate_per_researcher_instance: float
    experiment_hours_per_candidate: float
    data_hours_per_candidate: float
    effective_training_hours_per_candidate: float
    verification_hours_per_candidate: float
    serial_experiment_cycle_years: float
    accepted_data_yield: float
    evaluator_independence: float
    external_service_hours_per_unit: float
    industrial_control_share_of_external_service: float
    external_revenue_per_accelerator_hour: float
    physical_growth_units_per_verified_progress: float


class CognitivePhysicalLaborConfig(EvidenceMetadata):
    model_instance_sweep: tuple[int, ...]
    inference_capacity_instances: int
    physical_robots_machines: int
    experimental_stations: int
    independently_verifiable_work_cells: int
    sensor_channels: int
    safe_simultaneous_work_envelopes: int
    physical_task_parallelism: int
    tool_material_slots: int
    physical_output_per_effective_agent_year: float
    useful_simulation_tasks: int
    useful_planning_tasks: int
    useful_monitoring_channels: int
    independent_experiments: int
    serial_experiment_depth_steps: int
    physical_experiment_cycle_years: float
    coordination_edges_per_active_instance: float
    verification_units_per_physical_output: float
    verification_units_per_nonphysical_candidate: float
    onboarding_hours_first_instance: float


class ElectronicsTier(TypedDict):
    parent_sector: str
    closure_strategy: str
    closure_sequence_rank: int
    continuing_earth_umbilical: bool
    shelf_life_years: int
    physical_failure_fraction_per_year: float
    economic_obsolescence_fraction_per_year: float
    downbin_reassignment_yield: float
    frontier_workload_demand_share: float
    initial_stockpile_units: float
    initial_annual_demand_units: float
    annual_demand_growth_fraction: float
    local_supply_units_per_year: float
    local_supply_start_year: int
    earth_import_units_per_year: float
    localization_effort_capacity_years: float


class ElectronicsSupplyChainConfig(EvidenceMetadata):
    years: int
    early_resilience_horizon_years: int
    tiers: Mapping[str, ElectronicsTier]


class ComputeCohortScenario(TypedDict):
    architecture_convergence_year: int | None
    generation_performance_multiplier_before_convergence: float
    generation_performance_multiplier_after_convergence: float
    persistent_workload_mismatch_fraction_per_year: float


class ComputeCohortConfig(EvidenceMetadata):
    years: int
    generation_interval_years: int
    new_capacity_units_per_generation: float
    physical_failure_fraction_per_year: float
    radiation_performance_loss_fraction_per_year: float
    workload_relative_performance_thresholds: Mapping[str, float]
    scenarios: Mapping[str, ComputeCohortScenario]


class EvaluatorIndependence(TypedDict):
    model_lineage: float
    training_data: float
    tools: float
    authority: float
    audit_access: float


class VerifierClass(TypedDict):
    claim_scope: str
    candidate_iterations_per_year: float
    verifier_capacity_per_year: float
    acceptance_fraction: float
    base_false_positive_fraction: float
    evaluator_independence: EvaluatorIndependence


class VerificationStressScenario(TypedDict):
    false_positive_addition: float
    independence_multiplier: float
    positive_record_preservation: float
    negative_record_preservation: float
    null_record_preservation: float
    fixed_target_execution_tasks_per_year: float
    research_direction_setting_tasks_per_year: float


class VerificationHierarchyConfig(EvidenceMetadata):
    verifier_classes: Mapping[str, VerifierClass]
    industrial_memory_records: Mapping[str, float]
    stress_scenarios: Mapping[str, VerificationStressScenario]


class ReliabilityTask(TypedDict):
    task_domain: str
    consequence_class: str
    required_rung: str
    measured_success_fraction: float
    trials: int
    task_duration_hours: float
    verifier_class: str
    low_context_long_task_observed: bool
    high_context_production_observed: bool
    safety_critical_field_observed: bool
    unscripted_recovery_observed: bool
    sustained_operation_hours: float
    intervention_events_per_100_tasks: float
    prompt_check_hours_per_task: float
    recovery_hours_per_failed_task: float
    cleanup_hours_per_failed_task: float
    rollback_success_fraction: float
    out_of_distribution_recovery_fraction: float


class IndustrialReliabilityConfig(EvidenceMetadata):
    rungs: tuple[str, ...]
    required_reliability_by_consequence: Mapping[str, float]
    single_attempt_threshold: float
    minimum_repeated_trials: int
    repeated_success_threshold: float
    long_task_hours_threshold: float
    minimum_ood_recovery_fraction: float
    minimum_rollback_success_fraction: float
    minimum_sustained_operation_hours: float
    maximum_interventions_per_100_tasks: float
    tasks: Mapping[str, ReliabilityTask]


class DataCoevolutionScenario(TypedDict):
    initial_synthetic_records: float
    synthetic_volume_multiplier: float
    deduplication_fraction: float
    filter_acceptance_fraction: float
    provenance_valid_fraction: float
    synthetic_share_of_training_mix: float
    initial_evaluator_error_fraction: float
    evaluator_drift_per_generation: float
    independent_evaluator_correction_per_generation: float
    initial_evaluator_bias_fraction: float
    bias_amplification_per_generation: float
    initial_data_diversity_index: float
    diversity_narrowing_per_generation: float
    physical_experiment_time_budget_hours: float
    hours_per_physical_episode: float
    equipment_wear_budget_units: float
    wear_units_per_physical_episode: float
    destructive_sample_budget: float
    samples_per_physical_episode: float
    physical_verification_capacity_episodes: float
    physical_causal_linkage_fraction: float
    initial_proprietary_data_advantage: float
    open_publication_capture_fraction: float
    espionage_leakage_fraction: float
    employee_mobility_leakage_fraction: float
    distillation_catchup_fraction: float
    independent_replication_fraction: float


class DataEvaluatorCoevolutionConfig(EvidenceMetadata):
    generations: int
    scenarios: Mapping[str, DataCoevolutionScenario]


class ReplicationGovernanceScenario(TypedDict):
    initial_productive_capacity: float
    private_replication_rate_per_year: float
    authorization_capacity_per_year: float
    contested_resource_capacity: float
    contested_resource_preemption_fraction: float
    debris_externality_per_capacity_added: float
    debris_mitigation_fraction: float
    output_per_capacity_year: float
    cost_per_debris_externality_unit: float
    cost_per_preempted_resource_unit: float
    cost_per_unauthorized_capacity_unit_year: float
    private_build_cost_per_capacity: float
    externality_cost_internalization_fraction: float
    resource_claim_legitimacy: float
    material_leverage_decline_rate_per_year: float
    future_output_claim_shares: Mapping[str, float]
    update_authority_gate: bool
    liability_gate: bool
    audit_rights_gate: bool
    succession_of_control_gate: bool
    future_affected_party_representation_gate: bool


class ReplicationGovernanceConfig(EvidenceMetadata):
    years: float
    dt: float
    maximum_unauthorized_capacity_fraction: float
    maximum_preemptive_capacity_fraction: float
    minimum_resource_claim_legitimacy: float
    minimum_externality_internalization_fraction: float
    scenarios: Mapping[str, ReplicationGovernanceScenario]


class CapabilityGateCase(TypedDict):
    interpretation: str
    internal_authorization_fraction: float
    public_authorization_fraction: float
    public_capability_slice_fraction: float
    public_release_interval_years: float


class InnovationEvent(TypedDict):
    year: float
    frontier_increment: float


class LoopCapacityPeriod(TypedDict):
    name: str
    start_year: float
    end_year: float
    progress_mechanism: str
    stage_rates_per_year: Mapping[str, float]


class DigitalImprovementConfig(TypedDict):
    source_class: str
    initial_capability: float
    frontier_capability: float
    gain_scale_per_verified_loop: float
    diminishing_exponent: float
    effective_compute_scale_flop: float
    training_flop_per_loop: float
    hardware_efficiency: float
    utilization: float
    algorithmic_efficiency: float
    architecture_efficiency: float
    technical_validation_fraction: float
    capability_gate_cases: Mapping[str, CapabilityGateCase]
    stage_rates_per_year: Mapping[str, float]
    innovation_events: tuple[InnovationEvent, ...]
    annual_progress_channels: Mapping[str, float]
    elasticity_bounds: Mapping[str, tuple[float, float, float]]
    elasticity_correlation_order: tuple[str, ...]
    elasticity_correlation_matrix: tuple[tuple[float, ...], ...]
    loop_capacity_periods: tuple[LoopCapacityPeriod, ...]


class DataAdvantageConfig(TypedDict):
    source_class: str
    components: Mapping[str, float]
    component_uncertainty_half_width: Mapping[str, float]
    weights: Mapping[str, float]
    gates: Mapping[str, float]


class IntergenerationalFaultFamily(TypedDict):
    training_case: str
    hidden_transfer_case: str
    baseline_recurrence_fraction: float
    baseline_transfer_success_fraction: float
    learning_effectiveness_fraction: float
    hidden_case_structural_similarity: float
    retention_per_generation: float
    baseline_recovery_time_days: float
    maximum_recovery_reduction_fraction: float
    curation_days: float
    training_days: float
    verification_days: float
    deployment_days: float
    verification_compute_hours: float
    update_interference_fraction: float
    replay_protection_fraction: float


class IntergenerationalLearningConfig(EvidenceMetadata):
    generations: int
    pipeline_base_latency_days: float
    holdout_compute_overhead_fraction: float
    annual_verification_compute_budget_hours: float
    minimum_transfer_success_fraction: float
    minimum_lesson_retention_fraction: float
    maximum_prior_task_regression_fraction: float
    fault_families: Mapping[str, IntergenerationalFaultFamily]


class CoordinationEvaluationCase(TypedDict):
    topology: str
    complexity: float
    uncertainty: float
    effective_intelligence: float


class CoordinationDownstreamAccount(TypedDict):
    staffing_agent_hours_per_day: float
    verified_output_units_per_day: float
    labor_cost_real_2025_usd_per_agent_hour: float
    base_failure_probability: float
    failure_probability_per_100_coordination_hours: float
    accounting_rule: str


class CoordinationUncertaintyConfig(TypedDict):
    telemetry_status: str
    bound_basis: str
    draws: int
    seed: int
    forms: tuple[Literal["power", "logarithmic", "saturating"], ...]
    edge_saturation_ratio_bounds: tuple[float, float]
    parameter_bounds: Mapping[str, tuple[float, float]]
    evaluation_case: CoordinationEvaluationCase
    downstream_account: CoordinationDownstreamAccount


class CoordinationConfig(TypedDict):
    source_class: str
    output_unit: str
    irreducible_hours: float
    reference_hours: float
    edge_reference: float
    complexity_reference: float
    uncertainty_reference: float
    intelligence_reference: float
    alpha: float
    beta: float
    gamma: float
    delta: float
    intelligence_response: float
    topology_examples: Mapping[str, tuple[tuple[float, ...], ...]]
    uncertainty_comparison: CoordinationUncertaintyConfig


class SupplierResource(TypedDict):
    initial_capacity_per_year: float
    growth_per_year: float
    requirement_per_import_t: float


class ExternalSupplierConfig(TypedDict):
    reliability_fraction: float
    resources: Mapping[str, SupplierResource]


class ResidualInputConfig(TypedDict):
    commissioning_t_per_capacity: float
    replacement_t_per_capacity_year: float
    initial_stockpile_t: float
    shelf_life_years: float
    obsolescence_per_year: float
    radiation_storage_loss_per_year: float
    delivery_failure_fraction: float
    minimum_lot_t: float
    replacement_wave_interval_years: int
    replacement_wave_fraction: float
    external_supplier_capacity_t_per_year: float
    delivered_value_musd_per_t: float
    delivered_volume_m3_per_t: float
    criticality_weight: float


class SupportPolicy(TypedDict):
    kind: Literal["fixed", "proportional", "finite_stockpile", "declining_disrupted"]
    substitution_allocation_fraction: float
    stockpile_reserve_years: NotRequired[float]
    annual_import_t: NotRequired[Mapping[str, float]]
    t_per_capacity_year: NotRequired[Mapping[str, float]]
    initial_annual_import_t: NotRequired[Mapping[str, float]]
    decline_per_year: NotRequired[float]
    outage_years: NotRequired[tuple[float, float]]
    recovery_fraction: NotRequired[float]


class SubstitutionProgram(TypedDict):
    capability_threshold: str
    parent_tool_ancestry: str
    evidence_state: str
    minimum_completion_year: float
    effort_capacity_years: float
    required_intelligence: float
    embodiment_adequate: bool
    materials_available: bool
    tools_available: bool
    test_facility_available: bool
    outcome: Literal["validated", "failed"]
    remaining_requirement_multiplier: float
    charged_work: str
    effort_resource_shares: Mapping[str, float]


class PartialClosureSupportConfig(TypedDict):
    source_class: str
    horizon_years: int
    initial_capacity: float
    local_growth_per_year: float
    local_bulk_t_per_capacity: float
    wholly_earth_manufactured_t_per_capacity: float
    bridge_initial_external_seed_t: float
    earth_delivery_musd_per_t: float
    local_bulk_value_musd_per_t: float
    local_part_families: int
    total_part_families: int
    local_embodied_energy_fraction: float
    local_process_work_fraction: float
    external_human_intervention_hours_per_capacity_year: float
    external_verification_hours_per_capacity_year: float
    initial_intelligence: float
    intelligence_gain_per_year: float
    external_supplier: ExternalSupplierConfig
    residual_inputs: Mapping[str, ResidualInputConfig]
    policies: Mapping[str, SupportPolicy]
    allocation_policies: Mapping[str, SupportPolicy]
    substitution_programs: Mapping[str, SubstitutionProgram]


class EmbodimentBOMItem(TypedDict):
    producer_sector: str
    target_sectors: tuple[str, ...]
    material_bom_t_per_target_capacity: Mapping[str, float]
    replacement_service_units_per_target_capacity_year: float


class EmbodimentBOMConfig(TypedDict):
    source_class: str
    bounding_argument: str
    items: Mapping[str, EmbodimentBOMItem]


__all__ = [
    "AuthorizedCapacityControlConfig",
    "AuthorizedCapacityScenario",
    "BottleneckUpgradeConfig",
    "BottleneckUpgradeProject",
    "CapabilityGateCase",
    "CapabilityState",
    "ChronologicalReleaseBacktestConfig",
    "CognitivePhysicalLaborConfig",
    "ComputeAllocationConfig",
    "ComputeCohortConfig",
    "ComputeCohortScenario",
    "ComputeDemandBranch",
    "ComputeDemandConfig",
    "CoordinationConfig",
    "CoordinationDownstreamAccount",
    "CoordinationEvaluationCase",
    "CoordinationUncertaintyConfig",
    "DataAdvantageConfig",
    "DataCoevolutionScenario",
    "DataEvaluatorCoevolutionConfig",
    "DigitalImprovementConfig",
    "ElectronicsSupplyChainConfig",
    "ElectronicsTier",
    "EmbodimentBOMConfig",
    "EmbodimentBOMItem",
    "EvaluatorIndependence",
    "EvidenceMetadata",
    "ExternalSupplierConfig",
    "IndustrialReliabilityConfig",
    "InnovationEvent",
    "IntelligenceMarginalResponseConfig",
    "IntelligenceResponseRegime",
    "IntergenerationalFaultFamily",
    "IntergenerationalLearningConfig",
    "LoopCapacityPeriod",
    "MilestoneBranch",
    "MilestoneOrderConfig",
    "PartialClosureSupportConfig",
    "ReleaseBacktestObservation",
    "ReliabilityTask",
    "ReplicationGovernanceConfig",
    "ReplicationGovernanceScenario",
    "ResidualInputConfig",
    "SubstitutionProgram",
    "SupplierResource",
    "SupportPolicy",
    "VerificationHierarchyConfig",
    "VerificationStressScenario",
    "VerifierClass",
]
