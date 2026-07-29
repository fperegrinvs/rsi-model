"""Explicit sensitivity models added by the post-r4.0 manuscript review.

The functions in this module are deliberately small and auditable.  They
implement the equations introduced in Part I without turning them into
empirical laws.  Unless a caller supplies calibrated inputs, every coefficient
is an assumption-class scenario value.
"""

from __future__ import annotations

import math
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from itertools import combinations, pairwise

import numpy as np

from .array_types import FloatArray
from .extension_config import (
    AuthorizedCapacityControlConfig,
    ChronologicalReleaseBacktestConfig,
    CognitivePhysicalLaborConfig,
    ComputeAllocationConfig,
    ComputeCohortConfig,
    DataEvaluatorCoevolutionConfig,
    DigitalImprovementConfig,
    ElectronicsSupplyChainConfig,
    IndustrialReliabilityConfig,
    MilestoneOrderConfig,
    ReleaseBacktestObservation,
    ReplicationGovernanceConfig,
    VerificationHierarchyConfig,
)

LIFECYCLE_STATES = (
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


def validate_unit_interval(value: float, label: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{label} must be in [0, 1]")
    return number


def effective_training_compute(
    training_flop: float,
    *,
    hardware_efficiency: float,
    utilization: float,
    algorithmic_efficiency: float,
    architecture_efficiency: float,
) -> float:
    """Return baseline-equivalent useful training FLOP.

    Efficiency factors are ratios at a named held-out target.  They must be
    positive but need not be bounded by one: an algorithm or architecture can
    outperform the baseline.
    """
    terms = (
        float(training_flop),
        float(hardware_efficiency),
        float(utilization),
        float(algorithmic_efficiency),
        float(architecture_efficiency),
    )
    if any(value < 0.0 for value in terms):
        raise ValueError("training compute and efficiency terms must be nonnegative")
    return float(np.prod(terms))


def verified_loop_throughput(stage_rates: Mapping[str, float]) -> float:
    """Return the bottleneck verified-loop rate in completed loops per year."""
    return verified_loop_bottleneck(stage_rates).rate_per_year


@dataclass(frozen=True)
class VerifiedLoopBottleneck:
    binding_stages: tuple[str, ...]
    rate_per_year: float


def verified_loop_bottleneck(
    stage_rates: Mapping[str, float],
) -> VerifiedLoopBottleneck:
    """Return both the verified-loop rate and every tied binding stage."""
    required = {
        "train",
        "data",
        "experiment",
        "evaluate",
        "safety",
        "deploy",
        "observe",
    }
    missing = required - set(stage_rates)
    if missing:
        raise ValueError(f"missing verified-loop stages: {sorted(missing)}")
    values = [float(stage_rates[name]) for name in sorted(required)]
    if any(value < 0.0 for value in values):
        raise ValueError("verified-loop stage rates must be nonnegative")
    rate = min(values)
    binding = tuple(
        name for name in sorted(required) if math.isclose(float(stage_rates[name]), rate)
    )
    return VerifiedLoopBottleneck(binding, rate)


@dataclass(frozen=True)
class DigitalChannelAblation:
    channel: str
    full_annual_multiplier: float
    frozen_annual_multiplier: float
    removed_log_progress_share: float


def digital_channel_ablations(
    annual_progress_rates: Mapping[str, float],
) -> tuple[DigitalChannelAblation, ...]:
    """Freeze one declared progress channel at a time.

    Rates are fractional annual improvements at a fixed held-out target.
    They combine in log space so the decomposition is unit-consistent and a
    frozen channel removes exactly its declared log contribution. This is an
    assumption-class accounting sensitivity, not a causal estimate.
    """
    required = {
        "compute",
        "data",
        "hardware",
        "algorithm",
        "architecture",
    }
    missing = required - set(annual_progress_rates)
    if missing:
        raise ValueError(f"missing digital progress channels: {sorted(missing)}")
    if any(float(rate) < 0.0 for rate in annual_progress_rates.values()):
        raise ValueError("annual digital progress rates must be nonnegative")
    contributions = {name: math.log1p(float(rate)) for name, rate in annual_progress_rates.items()}
    total = sum(contributions.values())
    full = math.exp(total)
    return tuple(
        DigitalChannelAblation(
            channel=name,
            full_annual_multiplier=full,
            frozen_annual_multiplier=math.exp(total - contributions[name]),
            removed_log_progress_share=(contributions[name] / total if total > 0.0 else 0.0),
        )
        for name in annual_progress_rates
    )


@dataclass(frozen=True)
class ReleaseBacktestRow:
    relation: str
    model: str
    release_date: str
    release_year: int
    split: str
    parameters_billion: float
    training_tokens_billion: float
    token_count_is_lower_bound: bool
    compute_proxy_flop: float
    data_balance_fraction: float
    observed_mmlu_percent: float
    predicted_mmlu_percent: float
    residual_percentage_points: float
    absolute_error_percentage_points: float
    source_id: str
    source_locator: str


@dataclass(frozen=True)
class ReleaseBacktestSummary:
    relation: str
    split: str
    observations: int
    mean_absolute_error_percentage_points: float
    root_mean_square_error_percentage_points: float
    mean_signed_error_percentage_points: float
    intercept: float
    log_compute_coefficient: float
    log_balance_coefficient: float | None
    fit_model_names: tuple[str, ...]
    fit_release_year_max: int


def chronological_release_backtest(
    config: ChronologicalReleaseBacktestConfig,
) -> tuple[tuple[ReleaseBacktestRow, ...], tuple[ReleaseBacktestSummary, ...]]:
    """Fit declared relations on early releases and score later releases.

    The target is chance-adjusted five-shot MMLU accuracy. Training compute is
    represented by the dense-Transformer proxy ``6 * parameters * tokens``;
    it is not a claim about measured end-to-end development compute. Split
    labels are supplied before fitting and validated chronologically so later
    benchmark observations cannot leak into the fitted coefficients.
    """
    if not bool(config.get("split_declared_before_fit", False)):
        raise ValueError("chronological split must be declared before fitting")
    releases = tuple(config["releases"])
    if not releases:
        raise ValueError("release backtest requires observations")
    allowed_splits = ("train", "validation", "holdout")
    split_rank = {name: index for index, name in enumerate(allowed_splits)}
    names = [str(row["model"]) for row in releases]
    if len(set(names)) != len(names):
        raise ValueError("release backtest model names must be unique")

    years_by_split: dict[str, list[int]] = {split: [] for split in allowed_splits}
    for row in releases:
        split = str(row["split"])
        if split not in split_rank:
            raise ValueError(f"unknown release split {split!r}")
        years_by_split[split].append(int(row["release_year"]))
    if any(not years_by_split[split] for split in allowed_splits):
        raise ValueError("train, validation, and holdout splits are required")
    if not (
        max(years_by_split["train"])
        < min(years_by_split["validation"])
        <= max(years_by_split["validation"])
        < min(years_by_split["holdout"])
    ):
        raise ValueError("release splits must be strictly chronological")

    chance = float(config["chance_accuracy_percent"])
    ceiling = float(config.get("score_ceiling_percent", 100.0))
    if not 0.0 <= chance < ceiling <= 100.0:
        raise ValueError("invalid chance/ceiling accuracy boundary")
    compute_reference = float(config["compute_reference_flop"])
    balance_target = float(config["target_tokens_per_parameter"])
    if compute_reference <= 0.0 or balance_target <= 0.0:
        raise ValueError("compute reference and balance target must be positive")

    def release_features(
        row: ReleaseBacktestObservation,
        relation: str,
    ) -> tuple[list[float], float, float]:
        parameters = float(row["parameters_billion"])
        tokens = float(row["training_tokens_billion"])
        if parameters <= 0.0 or tokens <= 0.0:
            raise ValueError("release parameters and tokens must be positive")
        compute = 6.0 * parameters * 1e9 * tokens * 1e9
        tokens_per_parameter = tokens / parameters
        balance = min(
            tokens_per_parameter / balance_target,
            balance_target / tokens_per_parameter,
        )
        features = [1.0, math.log10(compute / compute_reference)]
        if relation == "compute_plus_balance":
            features.append(math.log10(balance))
        elif relation != "compute_only":
            raise ValueError(f"unknown release-backtest relation {relation!r}")
        return features, compute, balance

    relations = tuple(str(value) for value in config["relations"])
    if set(relations) != {"compute_only", "compute_plus_balance"}:
        raise ValueError("release backtest must compare compute_only and compute_plus_balance")

    output_rows: list[ReleaseBacktestRow] = []
    summaries: list[ReleaseBacktestSummary] = []
    fit_releases = tuple(row for row in releases if str(row["split"]) == "train")
    for relation in relations:
        design: list[list[float]] = []
        targets: list[float] = []
        for row in fit_releases:
            observed = float(row["mmlu_five_shot_percent"])
            if not chance < observed < ceiling:
                raise ValueError("MMLU scores must lie between chance and ceiling")
            features, _, _ = release_features(row, relation)
            normalized = (observed - chance) / (ceiling - chance)
            targets.append(math.log(normalized / (1.0 - normalized)))
            design.append(features)
        if len(design) <= len(design[0]):
            raise ValueError(f"{relation} needs more training observations than coefficients")
        coefficients, _, _, _ = np.linalg.lstsq(
            np.asarray(design, dtype=float),
            np.asarray(targets, dtype=float),
            rcond=None,
        )

        relation_rows: list[ReleaseBacktestRow] = []
        for row in releases:
            observed = float(row["mmlu_five_shot_percent"])
            if not chance < observed < ceiling:
                raise ValueError("MMLU scores must lie between chance and ceiling")
            features, compute, balance = release_features(row, relation)
            logit = float(np.dot(np.asarray(features), coefficients))
            normalized_prediction = 1.0 / (1.0 + math.exp(-logit))
            prediction = chance + (ceiling - chance) * normalized_prediction
            residual = prediction - observed
            result = ReleaseBacktestRow(
                relation=relation,
                model=str(row["model"]),
                release_date=str(row["release_date"]),
                release_year=int(row["release_year"]),
                split=str(row["split"]),
                parameters_billion=float(row["parameters_billion"]),
                training_tokens_billion=float(row["training_tokens_billion"]),
                token_count_is_lower_bound=bool(row.get("token_count_is_lower_bound", False)),
                compute_proxy_flop=compute,
                data_balance_fraction=balance,
                observed_mmlu_percent=observed,
                predicted_mmlu_percent=prediction,
                residual_percentage_points=residual,
                absolute_error_percentage_points=abs(residual),
                source_id=str(row["source_id"]),
                source_locator=str(row["source_locator"]).strip(),
            )
            relation_rows.append(result)
            output_rows.append(result)

        for split in allowed_splits:
            selected = [row for row in relation_rows if row.split == split]
            errors = np.asarray(
                [row.residual_percentage_points for row in selected],
                dtype=float,
            )
            summaries.append(
                ReleaseBacktestSummary(
                    relation=relation,
                    split=split,
                    observations=len(selected),
                    mean_absolute_error_percentage_points=float(np.mean(np.abs(errors))),
                    root_mean_square_error_percentage_points=float(np.sqrt(np.mean(errors**2))),
                    mean_signed_error_percentage_points=float(np.mean(errors)),
                    intercept=float(coefficients[0]),
                    log_compute_coefficient=float(coefficients[1]),
                    log_balance_coefficient=(
                        float(coefficients[2]) if relation == "compute_plus_balance" else None
                    ),
                    fit_model_names=tuple(str(row["model"]) for row in fit_releases),
                    fit_release_year_max=max(int(row["release_year"]) for row in fit_releases),
                )
            )
    return tuple(output_rows), tuple(summaries)


@dataclass(frozen=True)
class MilestoneOrderResult:
    branch: str
    digital_speed: str
    physical_speed: str
    ai_rd_closure_year: float
    embodiment_closure_year: float
    earth_capital_closure_year: float
    space_capital_closure_year: float
    control_readiness_year: float
    intelligence_overhang_years: float
    first_capital_closure: str
    space_path_timing: str
    control_ready_for_ai_rd: bool
    control_ready_for_earth_closure: bool
    control_ready_for_space_closure: bool
    safety_conditions_pass: bool
    earth_bridge_cost_multiplier: float


def evaluate_milestone_order(
    config: MilestoneOrderConfig,
) -> tuple[MilestoneOrderResult, ...]:
    """Classify declared milestone order without collapsing it to takeoff."""
    results: list[MilestoneOrderResult] = []
    required_regimes = {
        ("fast", "slow"),
        ("slow", "fast"),
        ("fast", "fast"),
        ("slow", "slow"),
    }
    observed_regimes: set[tuple[str, str]] = set()
    for branch in config["branches"]:
        digital_speed = str(branch["digital_speed"])
        physical_speed = str(branch["physical_speed"])
        if digital_speed not in {"fast", "slow"}:
            raise ValueError("digital_speed must be fast or slow")
        if physical_speed not in {"fast", "slow"}:
            raise ValueError("physical_speed must be fast or slow")
        observed_regimes.add((digital_speed, physical_speed))
        ai_rd = float(branch["ai_rd_closure_year"])
        embodiment = float(branch["embodiment_closure_year"])
        earth = float(branch["earth_capital_closure_year"])
        space = float(branch["space_capital_closure_year"])
        control = float(branch["control_readiness_year"])
        if min(ai_rd, embodiment, earth, space, control) < 0.0:
            raise ValueError("milestone years must be nonnegative")
        if earth < embodiment or space < embodiment:
            raise ValueError("capital closure cannot precede embodied-production closure")
        bridge_multiplier = float(branch.get("earth_bridge_cost_multiplier", 1.0))
        if bridge_multiplier <= 0.0:
            raise ValueError("Earth bridge-cost multiplier must be positive")
        ready_ai = control <= ai_rd
        ready_earth = control <= earth
        ready_space = control <= space
        results.append(
            MilestoneOrderResult(
                branch=str(branch["name"]),
                digital_speed=digital_speed,
                physical_speed=physical_speed,
                ai_rd_closure_year=ai_rd,
                embodiment_closure_year=embodiment,
                earth_capital_closure_year=earth,
                space_capital_closure_year=space,
                control_readiness_year=control,
                intelligence_overhang_years=max(embodiment - ai_rd, 0.0),
                first_capital_closure=("Earth" if earth <= space else "space"),
                space_path_timing=(
                    "pre_ai_rd_closure_path" if space < ai_rd else "post_ai_rd_construction_path"
                ),
                control_ready_for_ai_rd=ready_ai,
                control_ready_for_earth_closure=ready_earth,
                control_ready_for_space_closure=ready_space,
                safety_conditions_pass=ready_ai and ready_earth and ready_space,
                earth_bridge_cost_multiplier=bridge_multiplier,
            )
        )
    if not required_regimes.issubset(observed_regimes):
        raise ValueError("milestone matrix must include all four speed regimes")
    return tuple(results)


@dataclass(frozen=True)
class AuthorizedCapacityControlResult:
    scenario: str
    task_capability: float
    coordination_capability: float
    evaluator_capability: float
    controllability_confidence: float
    evaluator_independence_score: float
    correlated_monitor_failure_probability: float
    t: FloatArray
    gross_operating_capacity: FloatArray
    authorized_operating_capacity: FloatArray
    unauthorized_operating_capacity: FloatArray
    proposed_high_impact_actions_per_year: FloatArray
    authorized_high_impact_actions_per_year: FloatArray
    reliability_verification_capacity_per_year: FloatArray
    adversarial_verification_capacity_per_year: FloatArray
    secure_command_capacity_per_year: FloatArray
    environmental_capacity_per_year: FloatArray
    treaty_capacity_per_year: FloatArray
    human_comprehension_capacity_per_year: FloatArray
    binding_authorization_limit: tuple[str, ...]
    first_independent_verification_lag_year: float | None
    first_human_oversight_lag_year: float | None
    human_approval_ceremonial_at_horizon: bool
    governance_endpoint_passes: bool


def simulate_authorized_capacity_control(
    config: AuthorizedCapacityControlConfig,
) -> tuple[AuthorizedCapacityControlResult, ...]:
    """Simulate gross and authorized capacity under independent rate gates."""
    years = float(config["years"])
    dt = float(config["dt"])
    evaluator_reference = float(config["evaluator_capability_reference"])
    max_unauthorized_share = validate_unit_interval(
        config["maximum_unauthorized_capacity_fraction"],
        "maximum_unauthorized_capacity_fraction",
    )
    if years <= 0.0 or dt <= 0.0 or evaluator_reference <= 0.0:
        raise ValueError("control horizon, step, and evaluator reference positive")
    independence_dimensions = tuple(config["independence_dimensions"])
    if not independence_dimensions:
        raise ValueError("evaluator independence dimensions are required")

    results: list[AuthorizedCapacityControlResult] = []
    for name, scenario in config["scenarios"].items():
        capability = scenario["capability_state"]
        task_capability = float(capability["task"])
        coordination_capability = float(capability["coordination"])
        evaluator_capability = float(capability["evaluator"])
        controllability = validate_unit_interval(
            capability["controllability_confidence"],
            "controllability_confidence",
        )
        if (
            min(
                task_capability,
                coordination_capability,
                evaluator_capability,
            )
            < 0.0
        ):
            raise ValueError("capability coordinates must be nonnegative")
        independence_values = [
            validate_unit_interval(
                scenario["evaluator_independence"][dimension],
                f"evaluator_independence.{dimension}",
            )
            for dimension in independence_dimensions
        ]
        independence = float(math.prod(independence_values) ** (1.0 / len(independence_values)))
        producer_failure = validate_unit_interval(
            scenario["producer_monitor_failure_probability"],
            "producer_monitor_failure_probability",
        )
        evaluator_failure = validate_unit_interval(
            scenario["evaluator_monitor_failure_probability"],
            "evaluator_monitor_failure_probability",
        )
        correlation = validate_unit_interval(
            scenario["monitor_failure_correlation"],
            "monitor_failure_correlation",
        )
        covariance = correlation * math.sqrt(
            producer_failure
            * (1.0 - producer_failure)
            * evaluator_failure
            * (1.0 - evaluator_failure)
        )
        joint_failure = min(
            producer_failure * evaluator_failure + covariance,
            producer_failure,
            evaluator_failure,
        )

        initial_gross = float(scenario["initial_gross_capacity"])
        initial_authorized = float(scenario["initial_authorized_capacity"])
        replication_rate = float(scenario["gross_replication_rate_per_year"])
        actions_per_capacity = float(scenario["high_impact_actions_per_added_capacity"])
        control_growth = float(scenario["annual_control_capacity_growth_fraction"])
        if (
            initial_gross < 0.0
            or not 0.0 <= initial_authorized <= initial_gross
            or replication_rate < 0.0
            or actions_per_capacity <= 0.0
            or control_growth < 0.0
        ):
            raise ValueError("invalid authorized-capacity scenario values")

        steps = round(years / dt)
        t = np.arange(steps + 1, dtype=float) * dt
        gross = np.zeros(steps + 1)
        authorized = np.zeros(steps + 1)
        unauthorized = np.zeros(steps + 1)
        proposed = np.zeros(steps + 1)
        authorized_actions = np.zeros(steps + 1)
        reliability_capacity = np.zeros(steps + 1)
        adversarial_capacity = np.zeros(steps + 1)
        command_capacity = np.zeros(steps + 1)
        environmental_capacity = np.zeros(steps + 1)
        treaty_capacity = np.zeros(steps + 1)
        human_capacity = np.zeros(steps + 1)
        binding: list[str] = []
        gross[0] = initial_gross
        authorized[0] = initial_authorized
        unauthorized[0] = initial_gross - initial_authorized
        verification_lag: float | None = None
        human_lag: float | None = None
        evaluator_effectiveness = min(
            evaluator_capability / evaluator_reference,
            1.0,
        )
        human_required = bool(scenario["human_approval_required"])

        for k, year in enumerate(t):
            scale = (1.0 + control_growth) ** year
            gross_addition_rate = replication_rate * gross[k]
            proposed[k] = gross_addition_rate * actions_per_capacity
            raw_verification = float(scenario["independent_verification_actions_per_year"]) * scale
            reliability_capacity[k] = (
                raw_verification
                * validate_unit_interval(
                    scenario["reliability_test_coverage_fraction"],
                    "reliability_test_coverage_fraction",
                )
                * evaluator_effectiveness
            )
            adversarial_capacity[k] = (
                raw_verification
                * validate_unit_interval(
                    scenario["adversarial_test_coverage_fraction"],
                    "adversarial_test_coverage_fraction",
                )
                * evaluator_effectiveness
                * independence
                * (1.0 - joint_failure)
            )
            command_capacity[k] = (
                float(scenario["secure_command_actions_per_year"]) * scale * controllability
            )
            environmental_capacity[k] = float(scenario["environmental_limit_actions_per_year"])
            treaty_capacity[k] = float(scenario["treaty_limit_actions_per_year"])
            human_capacity[k] = float(scenario["human_comprehension_actions_per_year"]) * scale
            limits = {
                "gross_production": proposed[k],
                "reliability_verification": reliability_capacity[k],
                "adversarial_verification": adversarial_capacity[k],
                "secure_command": command_capacity[k],
                "environmental_limit": environmental_capacity[k],
                "treaty_limit": treaty_capacity[k],
            }
            if human_required:
                limits["human_comprehension"] = human_capacity[k]
            limiter = min(limits, key=lambda name: limits[name])
            binding.append(limiter)
            authorized_actions[k] = max(float(limits[limiter]), 0.0)

            if (
                verification_lag is None
                and proposed[k] > min(reliability_capacity[k], adversarial_capacity[k]) + 1e-12
            ):
                verification_lag = float(year)
            if human_lag is None and human_required and proposed[k] > human_capacity[k] + 1e-12:
                human_lag = float(year)
            if k == steps:
                break
            gross[k + 1] = gross[k] + gross_addition_rate * dt
            authorized_addition_rate = authorized_actions[k] / actions_per_capacity
            authorized[k + 1] = min(
                gross[k + 1],
                authorized[k] + authorized_addition_rate * dt,
            )
            unauthorized[k + 1] = max(
                gross[k + 1] - authorized[k + 1],
                0.0,
            )

        final_unauthorized_share = unauthorized[-1] / gross[-1] if gross[-1] > 0.0 else 0.0
        results.append(
            AuthorizedCapacityControlResult(
                scenario=str(name),
                task_capability=task_capability,
                coordination_capability=coordination_capability,
                evaluator_capability=evaluator_capability,
                controllability_confidence=controllability,
                evaluator_independence_score=independence,
                correlated_monitor_failure_probability=joint_failure,
                t=t,
                gross_operating_capacity=gross,
                authorized_operating_capacity=authorized,
                unauthorized_operating_capacity=unauthorized,
                proposed_high_impact_actions_per_year=proposed,
                authorized_high_impact_actions_per_year=authorized_actions,
                reliability_verification_capacity_per_year=(reliability_capacity),
                adversarial_verification_capacity_per_year=(adversarial_capacity),
                secure_command_capacity_per_year=command_capacity,
                environmental_capacity_per_year=environmental_capacity,
                treaty_capacity_per_year=treaty_capacity,
                human_comprehension_capacity_per_year=human_capacity,
                binding_authorization_limit=tuple(binding),
                first_independent_verification_lag_year=verification_lag,
                first_human_oversight_lag_year=human_lag,
                human_approval_ceremonial_at_horizon=(
                    human_required and proposed[-1] > human_capacity[-1] + 1e-12
                ),
                governance_endpoint_passes=(
                    final_unauthorized_share <= max_unauthorized_share + 1e-12
                    and not (human_required and proposed[-1] > human_capacity[-1] + 1e-12)
                ),
            )
        )
    return tuple(results)


@dataclass(frozen=True)
class ComputeAllocationResult:
    objective: str
    algorithmic_efficiency: float
    total_physical_accelerator_hours: float
    training_hours: float
    research_inference_hours: float
    experiment_hours: float
    data_generation_filtering_hours: float
    verification_safety_hours: float
    external_productive_service_hours: float
    effective_training_hours: float
    automated_researcher_instances: float
    useful_research_task_limit: float
    researcher_candidate_rate: float
    experiment_candidate_rate: float
    accepted_data_candidate_rate: float
    verification_candidate_rate: float
    serial_depth_candidate_limit: float
    raw_capability_progress_rate: float
    verified_progress_rate: float
    external_productive_service_units: float
    industrial_control_service_units: float
    foregone_external_revenue: float
    objective_score: float


def _integer_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    """Yield nonnegative integer tuples of ``parts`` summing to ``total``."""
    for bars in combinations(range(total + parts - 1), parts - 1):
        points = (-1, *bars, total + parts - 1)
        yield tuple(points[index + 1] - points[index] - 1 for index in range(parts))


def optimize_compute_allocation(
    config: ComputeAllocationConfig,
) -> tuple[ComputeAllocationResult, ...]:
    """Allocate one physical accelerator-hour budget across six uses.

    A stars-and-bars grid makes the opportunity cost exact on the declared
    resolution: every candidate allocation sums to the same physical budget.
    Algorithmic efficiency changes useful-work conversion and never the
    accelerator-hour stock.
    """
    total_hours = float(config["total_physical_accelerator_hours_per_year"])
    grid_units = int(config["allocation_grid_units"])
    if total_hours <= 0.0 or grid_units <= 0:
        raise ValueError("compute budget and allocation grid must be positive")
    categories = (
        "training",
        "research_inference",
        "experiments",
        "data_generation_filtering",
        "verification_safety",
        "external_productive_service",
    )
    if tuple(config["categories"]) != categories:
        raise ValueError("compute allocation must use the canonical six uses")
    objectives = tuple(config["objectives"])
    if set(objectives) != {
        "raw_capability",
        "verified_progress",
        "physical_growth",
    }:
        raise ValueError("three compute-allocation objectives are required")

    useful_tasks = float(config["useful_research_tasks"])
    inference_per_instance = float(config["inference_hours_per_researcher_instance"])
    candidates_per_instance = float(config["candidate_rate_per_researcher_instance"])
    experiment_hours_per_candidate = float(config["experiment_hours_per_candidate"])
    data_hours_per_candidate = float(config["data_hours_per_candidate"])
    training_hours_per_candidate = float(config["effective_training_hours_per_candidate"])
    verification_hours_per_candidate = float(config["verification_hours_per_candidate"])
    serial_limit = 1.0 / float(config["serial_experiment_cycle_years"])
    data_yield = validate_unit_interval(
        config["accepted_data_yield"],
        "accepted_data_yield",
    )
    evaluator_independence = validate_unit_interval(
        config["evaluator_independence"],
        "evaluator_independence",
    )
    service_hours_per_unit = float(config["external_service_hours_per_unit"])
    control_fraction = validate_unit_interval(
        config["industrial_control_share_of_external_service"],
        "industrial_control_share_of_external_service",
    )
    revenue_per_hour = float(config["external_revenue_per_accelerator_hour"])
    verified_to_physical = float(config["physical_growth_units_per_verified_progress"])
    positive = (
        useful_tasks,
        inference_per_instance,
        candidates_per_instance,
        experiment_hours_per_candidate,
        data_hours_per_candidate,
        training_hours_per_candidate,
        verification_hours_per_candidate,
        serial_limit,
        service_hours_per_unit,
    )
    if any(value <= 0.0 for value in positive):
        raise ValueError("compute conversion rates must be positive")
    if revenue_per_hour < 0.0 or verified_to_physical < 0.0:
        raise ValueError("compute opportunity values must be nonnegative")

    step_hours = total_hours / grid_units
    results: list[ComputeAllocationResult] = []
    for algorithmic_efficiency in config["algorithmic_efficiency_sensitivity"]:
        efficiency = float(algorithmic_efficiency)
        if efficiency <= 0.0:
            raise ValueError("algorithmic efficiency must be positive")
        best: dict[str, tuple[tuple[float, ...], ComputeAllocationResult]] = {}
        for integer_allocation in _integer_compositions(
            grid_units,
            len(categories),
        ):
            allocation = tuple(value * step_hours for value in integer_allocation)
            (
                training,
                research_inference,
                experiments,
                data_generation,
                verification,
                external_service,
            ) = allocation
            effective_training = training * efficiency
            researcher_instances = min(
                research_inference / inference_per_instance,
                useful_tasks,
            )
            researcher_candidates = researcher_instances * candidates_per_instance
            experiment_candidates = experiments * efficiency / experiment_hours_per_candidate
            data_candidates = data_generation * data_yield / data_hours_per_candidate
            training_candidates = effective_training / training_hours_per_candidate
            raw_progress = min(
                researcher_candidates,
                experiment_candidates,
                data_candidates,
                training_candidates,
            )
            verification_candidates = (
                verification * evaluator_independence / verification_hours_per_candidate
            )
            verified_progress = min(
                raw_progress,
                verification_candidates,
                serial_limit,
            )
            external_units = external_service / service_hours_per_unit
            control_units = external_units * control_fraction
            foregone_revenue = (total_hours - external_service) * revenue_per_hour
            scores = {
                "raw_capability": raw_progress,
                "verified_progress": verified_progress,
                "physical_growth": (external_units + verified_to_physical * verified_progress),
            }
            for objective in objectives:
                result = ComputeAllocationResult(
                    objective=str(objective),
                    algorithmic_efficiency=efficiency,
                    total_physical_accelerator_hours=total_hours,
                    training_hours=training,
                    research_inference_hours=research_inference,
                    experiment_hours=experiments,
                    data_generation_filtering_hours=data_generation,
                    verification_safety_hours=verification,
                    external_productive_service_hours=external_service,
                    effective_training_hours=effective_training,
                    automated_researcher_instances=researcher_instances,
                    useful_research_task_limit=useful_tasks,
                    researcher_candidate_rate=researcher_candidates,
                    experiment_candidate_rate=experiment_candidates,
                    accepted_data_candidate_rate=data_candidates,
                    verification_candidate_rate=verification_candidates,
                    serial_depth_candidate_limit=serial_limit,
                    raw_capability_progress_rate=raw_progress,
                    verified_progress_rate=verified_progress,
                    external_productive_service_units=external_units,
                    industrial_control_service_units=control_units,
                    foregone_external_revenue=foregone_revenue,
                    objective_score=scores[objective],
                )
                # Deterministic tie-break: preserve verified progress and then
                # external service instead of wasting a score-equivalent hour.
                if objective == "raw_capability":
                    key = (
                        scores[objective],
                        -verification,
                        external_service,
                        -experiments,
                    )
                elif objective == "verified_progress":
                    key = (
                        scores[objective],
                        external_service,
                        raw_progress,
                        -experiments,
                    )
                else:
                    key = (
                        scores[objective],
                        verified_progress,
                        external_service,
                        -experiments,
                    )
                if objective not in best or key > best[objective][0]:
                    best[objective] = (key, result)
        results.extend(best[objective][1] for objective in objectives)
    return tuple(results)


@dataclass(frozen=True)
class CognitivePhysicalLaborResult:
    model_instances: int
    inference_capacity_instances: int
    active_cognitive_instances: int
    physical_robots_machines: int
    experimental_stations: int
    independently_verifiable_work_cells: int
    effective_physical_agents: float
    simulation_planning_monitoring_instances: float
    waiting_or_contention_instances: float
    physical_output_units_per_year: float
    parallel_experiment_capacity: int
    serial_depth_steps: int
    serial_wall_clock_floor_years: float
    independent_experiment_batch_years: float
    combined_experiment_program_years: float
    coordination_graph_edges: float
    duplicate_work_fraction: float
    verification_demand_units_per_year: float
    onboarding_hours_per_active_instance: float
    total_onboarding_hours: float


def cognitive_physical_labor_sweep(
    config: CognitivePhysicalLaborConfig,
) -> tuple[CognitivePhysicalLaborResult, ...]:
    """Bound cognitive copies by inference and physical work channels."""
    inference_capacity = int(config["inference_capacity_instances"])
    robots = int(config["physical_robots_machines"])
    stations = int(config["experimental_stations"])
    work_cells = int(config["independently_verifiable_work_cells"])
    physical_limits = {
        "robots_machines": robots,
        "sensor_channels": int(config["sensor_channels"]),
        "safe_simultaneous_work_envelopes": int(config["safe_simultaneous_work_envelopes"]),
        "task_parallelism": int(config["physical_task_parallelism"]),
        "tool_material_slots": int(config["tool_material_slots"]),
        "verifiable_work_cells": work_cells,
    }
    if min(inference_capacity, stations, *physical_limits.values()) <= 0:
        raise ValueError("cognitive and physical labor capacities must be positive")
    output_per_agent = float(config["physical_output_per_effective_agent_year"])
    useful_nonphysical = sum(
        int(config[name])
        for name in (
            "useful_simulation_tasks",
            "useful_planning_tasks",
            "useful_monitoring_channels",
        )
    )
    independent_experiments = int(config["independent_experiments"])
    serial_depth = int(config["serial_experiment_depth_steps"])
    cycle = float(config["physical_experiment_cycle_years"])
    edges_per_active = float(config["coordination_edges_per_active_instance"])
    verification_per_physical = float(config["verification_units_per_physical_output"])
    verification_per_nonphysical = float(config["verification_units_per_nonphysical_candidate"])
    onboarding_base = float(config["onboarding_hours_first_instance"])
    if (
        min(
            output_per_agent,
            independent_experiments,
            serial_depth,
            cycle,
            edges_per_active,
            onboarding_base,
        )
        <= 0.0
    ):
        raise ValueError("labor conversion settings must be positive")
    if min(verification_per_physical, verification_per_nonphysical) < 0.0:
        raise ValueError("verification demands must be nonnegative")

    rows: list[CognitivePhysicalLaborResult] = []
    for raw_instances in config["model_instance_sweep"]:
        instances = int(raw_instances)
        if instances <= 0:
            raise ValueError("model instances must be positive")
        active = min(instances, inference_capacity)
        effective_physical = float(min(active, *physical_limits.values()))
        remaining_active = max(active - int(effective_physical), 0)
        nonphysical = float(min(remaining_active, useful_nonphysical))
        waiting = float(max(instances - effective_physical - nonphysical, 0.0))
        parallel_capacity = min(
            active,
            stations,
            int(config["safe_simultaneous_work_envelopes"]),
            int(config["physical_task_parallelism"]),
        )
        serial_floor = serial_depth * cycle
        independent_batch = math.ceil(independent_experiments / parallel_capacity) * cycle
        total_program = serial_floor + independent_batch
        total_useful_tasks = effective_physical + useful_nonphysical
        duplicate_fraction = max(
            1.0 - total_useful_tasks / max(active, 1),
            0.0,
        )
        graph_edges = (
            active * edges_per_active
            + effective_physical * max(effective_physical - 1.0, 0.0) / 2.0
        )
        physical_output = effective_physical * output_per_agent
        verification_demand = (
            physical_output * verification_per_physical + nonphysical * verification_per_nonphysical
        )
        onboarding_per_instance = onboarding_base / (1.0 + math.log1p(active))
        rows.append(
            CognitivePhysicalLaborResult(
                model_instances=instances,
                inference_capacity_instances=inference_capacity,
                active_cognitive_instances=active,
                physical_robots_machines=robots,
                experimental_stations=stations,
                independently_verifiable_work_cells=work_cells,
                effective_physical_agents=effective_physical,
                simulation_planning_monitoring_instances=nonphysical,
                waiting_or_contention_instances=waiting,
                physical_output_units_per_year=physical_output,
                parallel_experiment_capacity=parallel_capacity,
                serial_depth_steps=serial_depth,
                serial_wall_clock_floor_years=serial_floor,
                independent_experiment_batch_years=independent_batch,
                combined_experiment_program_years=total_program,
                coordination_graph_edges=graph_edges,
                duplicate_work_fraction=duplicate_fraction,
                verification_demand_units_per_year=verification_demand,
                onboarding_hours_per_active_instance=onboarding_per_instance,
                total_onboarding_hours=onboarding_per_instance * active,
            )
        )
    return tuple(rows)


@dataclass(frozen=True)
class ElectronicsSupplyChainResult:
    tier: str
    parent_sector: str
    closure_strategy: str
    closure_sequence_rank: int
    continuing_earth_umbilical: bool
    shelf_life_years: int
    physical_failure_fraction_per_year: float
    economic_obsolescence_fraction_per_year: float
    cumulative_demand_units: float
    cumulative_local_supply_units: float
    cumulative_import_supply_units: float
    cumulative_reused_downbinned_units: float
    cumulative_expired_failed_units: float
    cumulative_unmet_units: float
    terminal_frontier_inventory_units: float
    terminal_downbinned_inventory_units: float
    first_shortfall_year: int | None
    demand_fulfillment_fraction: float
    early_resilience_per_localization_effort: float


def _consume_frontier_inventory(
    inventory: FloatArray,
    shelf_life: int,
    amount: float,
) -> float:
    """Consume newest-capable stock oldest-first while mutating its inventory."""
    supplied = 0.0
    for age in range(shelf_life - 1, -1, -1):
        take = min(float(inventory[age]), amount)
        inventory[age] -= take
        amount -= take
        supplied += take
        if amount <= 1e-12:
            break
    return supplied


def electronics_supply_chain_sensitivity(
    config: ElectronicsSupplyChainConfig,
) -> tuple[ElectronicsSupplyChainResult, ...]:
    """Simulate heterogeneous electronics inventories and reassignment."""
    years = int(config["years"])
    if years <= 0:
        raise ValueError("electronics horizon must be positive")
    required_tiers = {
        "front_end_logic_fabrication",
        "memory_fabrication",
        "advanced_packaging",
        "substrates_interposers",
        "high_speed_interconnect",
        "power_electronics",
        "test_metrology",
        "radiation_qualified_system_integration",
    }
    if set(config["tiers"]) != required_tiers:
        raise ValueError("electronics sensitivity requires all eight tiers")
    rows: list[ElectronicsSupplyChainResult] = []
    for name, tier in config["tiers"].items():
        shelf_life = int(tier["shelf_life_years"])
        if shelf_life <= 0:
            raise ValueError("electronics shelf life must be positive")
        physical_failure = validate_unit_interval(
            tier["physical_failure_fraction_per_year"],
            "physical_failure_fraction_per_year",
        )
        obsolescence = validate_unit_interval(
            tier["economic_obsolescence_fraction_per_year"],
            "economic_obsolescence_fraction_per_year",
        )
        downbin_yield = validate_unit_interval(
            tier["downbin_reassignment_yield"],
            "downbin_reassignment_yield",
        )
        frontier_share = validate_unit_interval(
            tier["frontier_workload_demand_share"],
            "frontier_workload_demand_share",
        )
        initial_inventory = float(tier["initial_stockpile_units"])
        initial_demand = float(tier["initial_annual_demand_units"])
        demand_growth = float(tier["annual_demand_growth_fraction"])
        local_supply = float(tier["local_supply_units_per_year"])
        local_start = int(tier["local_supply_start_year"])
        imports = float(tier["earth_import_units_per_year"])
        effort = float(tier["localization_effort_capacity_years"])
        if (
            min(
                initial_inventory,
                initial_demand,
                demand_growth,
                local_supply,
                local_start,
                imports,
                effort,
            )
            < 0.0
        ):
            raise ValueError("electronics supply values must be nonnegative")
        frontier_inventory = np.zeros(shelf_life, dtype=float)
        frontier_inventory[0] = initial_inventory
        downbinned_inventory = 0.0
        cumulative_demand = 0.0
        cumulative_local = 0.0
        cumulative_import = 0.0
        cumulative_reused = 0.0
        cumulative_expired = 0.0
        cumulative_unmet = 0.0
        early_fulfilled = 0.0
        first_shortfall = None

        for year in range(years):
            failed = frontier_inventory * physical_failure
            frontier_inventory -= failed
            cumulative_expired += float(failed.sum())
            obsolete = frontier_inventory * obsolescence
            frontier_inventory -= obsolete
            downbinned_inventory += float(obsolete.sum()) * downbin_yield

            expired = float(frontier_inventory[-1])
            cumulative_expired += expired
            frontier_inventory[1:] = frontier_inventory[:-1]
            frontier_inventory[0] = 0.0
            downbinned_inventory *= 1.0 - physical_failure

            local = local_supply if year >= local_start else 0.0
            frontier_inventory[0] += local + imports
            cumulative_local += local
            cumulative_import += imports

            demand = initial_demand * (1.0 + demand_growth) ** year
            frontier_demand = demand * frontier_share
            general_demand = demand - frontier_demand
            cumulative_demand += demand

            reused = min(downbinned_inventory, general_demand)
            downbinned_inventory -= reused
            general_remaining = general_demand - reused
            cumulative_reused += reused

            general_new = _consume_frontier_inventory(
                frontier_inventory,
                shelf_life,
                general_remaining,
            )
            frontier_new = _consume_frontier_inventory(
                frontier_inventory,
                shelf_life,
                frontier_demand,
            )
            fulfilled = reused + general_new + frontier_new
            unmet = max(demand - fulfilled, 0.0)
            cumulative_unmet += unmet
            if year < int(config["early_resilience_horizon_years"]):
                early_fulfilled += fulfilled
            if first_shortfall is None and unmet > 1e-9:
                first_shortfall = year

        fulfillment = 1.0 - cumulative_unmet / cumulative_demand if cumulative_demand > 0.0 else 1.0
        rows.append(
            ElectronicsSupplyChainResult(
                tier=str(name),
                parent_sector=str(tier["parent_sector"]),
                closure_strategy=str(tier["closure_strategy"]),
                closure_sequence_rank=int(tier["closure_sequence_rank"]),
                continuing_earth_umbilical=bool(tier["continuing_earth_umbilical"]),
                shelf_life_years=shelf_life,
                physical_failure_fraction_per_year=physical_failure,
                economic_obsolescence_fraction_per_year=obsolescence,
                cumulative_demand_units=cumulative_demand,
                cumulative_local_supply_units=cumulative_local,
                cumulative_import_supply_units=cumulative_import,
                cumulative_reused_downbinned_units=cumulative_reused,
                cumulative_expired_failed_units=cumulative_expired,
                cumulative_unmet_units=cumulative_unmet,
                terminal_frontier_inventory_units=float(frontier_inventory.sum()),
                terminal_downbinned_inventory_units=downbinned_inventory,
                first_shortfall_year=first_shortfall,
                demand_fulfillment_fraction=fulfillment,
                early_resilience_per_localization_effort=(
                    early_fulfilled / effort if effort > 0.0 else math.inf
                ),
            )
        )
    return tuple(sorted(rows, key=lambda row: row.closure_sequence_rank))


@dataclass(frozen=True)
class ComputeCohortRow:
    scenario: str
    year: int
    cohort_generation: int
    cohort_launch_year: int
    cohort_age_years: int
    installed_physical_units: float
    cumulative_physical_failure_units: float
    radiation_performance_factor: float
    intrinsic_performance_per_watt: float
    effective_performance_capacity: float
    relative_performance_to_frontier: float
    assigned_workload: str
    frontier_training_eligible: bool
    economically_obsolete_for_frontier: bool


@dataclass(frozen=True)
class ComputeCohortSummary:
    scenario: str
    architecture_convergence_year: int | None
    terminal_physical_units: float
    terminal_effective_performance_capacity: float
    terminal_frontier_training_units: float
    terminal_reassigned_units: float
    terminal_economically_obsolete_but_functional_units: float
    cumulative_physical_failure_units: float
    reassigned_share_of_functional_stock: float


def simulate_compute_cohorts(
    config: ComputeCohortConfig,
) -> tuple[tuple[ComputeCohortRow, ...], tuple[ComputeCohortSummary, ...]]:
    """Track physical failure, radiation loss, obsolescence, and reassignment."""
    years = int(config["years"])
    interval = int(config["generation_interval_years"])
    new_units = float(config["new_capacity_units_per_generation"])
    physical_failure = validate_unit_interval(
        config["physical_failure_fraction_per_year"],
        "physical_failure_fraction_per_year",
    )
    radiation_loss = validate_unit_interval(
        config["radiation_performance_loss_fraction_per_year"],
        "radiation_performance_loss_fraction_per_year",
    )
    thresholds = {
        name: float(value)
        for name, value in config["workload_relative_performance_thresholds"].items()
    }
    ordered_workloads = (
        "frontier_training",
        "inference",
        "verification",
        "control",
        "simulation_nonfrontier",
    )
    if tuple(thresholds) != ordered_workloads:
        raise ValueError("compute workload ladder order is invalid")
    if (
        years <= 0
        or interval <= 0
        or new_units <= 0.0
        or any(value < 0.0 for value in thresholds.values())
    ):
        raise ValueError("invalid compute-cohort settings")
    if any(thresholds[a] < thresholds[b] for a, b in pairwise(ordered_workloads)):
        raise ValueError("workload thresholds must be nonincreasing")

    all_rows: list[ComputeCohortRow] = []
    summaries: list[ComputeCohortSummary] = []
    for scenario_name, scenario in config["scenarios"].items():
        convergence = scenario.get("architecture_convergence_year")
        convergence_year = None if convergence is None else int(convergence)
        before_multiplier = float(scenario["generation_performance_multiplier_before_convergence"])
        after_multiplier = float(scenario["generation_performance_multiplier_after_convergence"])
        workload_mismatch = validate_unit_interval(
            scenario["persistent_workload_mismatch_fraction_per_year"],
            "persistent_workload_mismatch_fraction_per_year",
        )
        if before_multiplier < 1.0 or after_multiplier < 1.0:
            raise ValueError("generation performance multipliers must be >= 1")
        cohorts: list[dict[str, float | int]] = []
        intrinsic = 1.0
        generation = 0
        cumulative_failure = 0.0
        final_rows: list[ComputeCohortRow] = []
        for year in range(years + 1):
            if year % interval == 0:
                if generation > 0:
                    multiplier = (
                        after_multiplier
                        if (convergence_year is not None and year >= convergence_year)
                        else before_multiplier
                    )
                    intrinsic *= multiplier
                cohorts.append(
                    {
                        "generation": generation,
                        "launch_year": year,
                        "units": new_units,
                        "initial_units": new_units,
                        "radiation_factor": 1.0,
                        "intrinsic": intrinsic,
                    }
                )
                generation += 1
            if year > 0:
                for cohort in cohorts:
                    failed = float(cohort["units"]) * physical_failure
                    cohort["units"] = float(cohort["units"]) - failed
                    cohort["radiation_factor"] = float(cohort["radiation_factor"]) * (
                        1.0 - radiation_loss
                    )
                    cumulative_failure += failed
            frontier_intrinsic = float(cohorts[-1]["intrinsic"])
            year_rows: list[ComputeCohortRow] = []
            for cohort in cohorts:
                age = year - int(cohort["launch_year"])
                adjusted_relative = (
                    float(cohort["intrinsic"])
                    * float(cohort["radiation_factor"])
                    * (1.0 - workload_mismatch) ** age
                    / frontier_intrinsic
                )
                assignment = ordered_workloads[-1]
                for workload in ordered_workloads:
                    if adjusted_relative >= thresholds[workload] - 1e-12:
                        assignment = workload
                        break
                units = float(cohort["units"])
                row = ComputeCohortRow(
                    scenario=str(scenario_name),
                    year=year,
                    cohort_generation=int(cohort["generation"]),
                    cohort_launch_year=int(cohort["launch_year"]),
                    cohort_age_years=age,
                    installed_physical_units=units,
                    cumulative_physical_failure_units=(float(cohort["initial_units"]) - units),
                    radiation_performance_factor=float(cohort["radiation_factor"]),
                    intrinsic_performance_per_watt=float(cohort["intrinsic"]),
                    effective_performance_capacity=(
                        units * float(cohort["intrinsic"]) * float(cohort["radiation_factor"])
                    ),
                    relative_performance_to_frontier=adjusted_relative,
                    assigned_workload=assignment,
                    frontier_training_eligible=(assignment == "frontier_training"),
                    economically_obsolete_for_frontier=(assignment != "frontier_training"),
                )
                all_rows.append(row)
                year_rows.append(row)
            final_rows = year_rows
        terminal_physical = sum(row.installed_physical_units for row in final_rows)
        terminal_reassigned = sum(
            row.installed_physical_units
            for row in final_rows
            if row.assigned_workload != "frontier_training"
        )
        summaries.append(
            ComputeCohortSummary(
                scenario=str(scenario_name),
                architecture_convergence_year=convergence_year,
                terminal_physical_units=terminal_physical,
                terminal_effective_performance_capacity=sum(
                    row.effective_performance_capacity for row in final_rows
                ),
                terminal_frontier_training_units=sum(
                    row.installed_physical_units
                    for row in final_rows
                    if row.assigned_workload == "frontier_training"
                ),
                terminal_reassigned_units=terminal_reassigned,
                terminal_economically_obsolete_but_functional_units=(terminal_reassigned),
                cumulative_physical_failure_units=cumulative_failure,
                reassigned_share_of_functional_stock=(
                    terminal_reassigned / terminal_physical if terminal_physical > 0.0 else 0.0
                ),
            )
        )
    return tuple(all_rows), tuple(summaries)


@dataclass(frozen=True)
class VerificationHierarchyResult:
    stress_scenario: str
    verifier_class: str
    evidence_strength_rank: int
    claim_scope: str
    candidate_iterations_per_year: float
    verifier_capacity_per_year: float
    reviewed_iterations_per_year: float
    accepted_iterations_per_year: float
    false_accepted_iterations_per_year: float
    independently_supported_iterations_per_year: float
    evaluator_independence_score: float
    evaluator_false_positive_fraction: float
    model_lineage_independence: float
    training_data_independence: float
    tool_independence: float
    authority_separation: float
    audit_access: float
    execution_against_fixed_target_per_year: float
    research_direction_setting_per_year: float
    direction_limited_licensed_loops_per_year: float
    positive_records_preserved: float
    negative_records_preserved: float
    null_records_preserved: float
    observed_positive_share_after_filtering: float


def verification_hierarchy_sensitivity(
    config: VerificationHierarchyConfig,
) -> tuple[VerificationHierarchyResult, ...]:
    """Keep verifier classes, independence, and selection bias explicit."""
    expected_order = (
        "formal_invariant",
        "destructive_physical_acceptance",
        "independent_heldout_experiment",
        "causal_operational_outcome",
        "human_ai_rubric",
        "model_self_assessment",
    )
    if tuple(config["verifier_classes"]) != expected_order:
        raise ValueError("verification hierarchy order is invalid")
    records = config["industrial_memory_records"]
    positives = float(records["positive"])
    negatives = float(records["negative"])
    nulls = float(records["null"])
    if min(positives, negatives, nulls) < 0.0:
        raise ValueError("industrial-memory record counts must be nonnegative")
    dimensions = (
        "model_lineage",
        "training_data",
        "tools",
        "authority",
        "audit_access",
    )
    rows: list[VerificationHierarchyResult] = []
    for stress_name, stress in config["stress_scenarios"].items():
        false_positive_addition = validate_unit_interval(
            stress["false_positive_addition"],
            "false_positive_addition",
        )
        independence_multiplier = validate_unit_interval(
            stress["independence_multiplier"],
            "independence_multiplier",
        )
        positive_preservation = validate_unit_interval(
            stress["positive_record_preservation"],
            "positive_record_preservation",
        )
        negative_preservation = validate_unit_interval(
            stress["negative_record_preservation"],
            "negative_record_preservation",
        )
        null_preservation = validate_unit_interval(
            stress["null_record_preservation"],
            "null_record_preservation",
        )
        direction_capacity = float(stress["research_direction_setting_tasks_per_year"])
        execution_capacity = float(stress["fixed_target_execution_tasks_per_year"])
        if min(direction_capacity, execution_capacity) < 0.0:
            raise ValueError("research task capacities must be nonnegative")
        preserved_positive = positives * positive_preservation
        preserved_negative = negatives * negative_preservation
        preserved_null = nulls * null_preservation
        preserved_total = preserved_positive + preserved_negative + preserved_null
        observed_positive_share = (
            preserved_positive / preserved_total if preserved_total > 0.0 else 0.0
        )
        for rank, verifier_name in enumerate(expected_order, start=1):
            verifier = config["verifier_classes"][verifier_name]
            values = [
                validate_unit_interval(
                    verifier["evaluator_independence"][dimension],
                    f"{verifier_name}.{dimension}",
                )
                * independence_multiplier
                for dimension in dimensions
            ]
            independence = float(math.prod(values) ** (1.0 / len(values)))
            false_positive = min(
                validate_unit_interval(
                    verifier["base_false_positive_fraction"],
                    "base_false_positive_fraction",
                )
                + false_positive_addition,
                1.0,
            )
            candidates = float(verifier["candidate_iterations_per_year"])
            capacity = float(verifier["verifier_capacity_per_year"])
            acceptance = validate_unit_interval(
                verifier["acceptance_fraction"],
                "acceptance_fraction",
            )
            if min(candidates, capacity) < 0.0:
                raise ValueError("verification throughputs must be nonnegative")
            reviewed = min(candidates, capacity)
            accepted = reviewed * acceptance
            false_accepted = accepted * false_positive
            independently_supported = (accepted - false_accepted) * independence
            licensed = min(
                independently_supported,
                direction_capacity,
                execution_capacity,
            )
            rows.append(
                VerificationHierarchyResult(
                    stress_scenario=str(stress_name),
                    verifier_class=verifier_name,
                    evidence_strength_rank=rank,
                    claim_scope=str(verifier["claim_scope"]),
                    candidate_iterations_per_year=candidates,
                    verifier_capacity_per_year=capacity,
                    reviewed_iterations_per_year=reviewed,
                    accepted_iterations_per_year=accepted,
                    false_accepted_iterations_per_year=false_accepted,
                    independently_supported_iterations_per_year=(independently_supported),
                    evaluator_independence_score=independence,
                    evaluator_false_positive_fraction=false_positive,
                    model_lineage_independence=values[0],
                    training_data_independence=values[1],
                    tool_independence=values[2],
                    authority_separation=values[3],
                    audit_access=values[4],
                    execution_against_fixed_target_per_year=execution_capacity,
                    research_direction_setting_per_year=direction_capacity,
                    direction_limited_licensed_loops_per_year=licensed,
                    positive_records_preserved=preserved_positive,
                    negative_records_preserved=preserved_negative,
                    null_records_preserved=preserved_null,
                    observed_positive_share_after_filtering=(observed_positive_share),
                )
            )
    return tuple(rows)


@dataclass(frozen=True)
class IndustrialReliabilityLadderResult:
    task: str
    task_domain: str
    consequence_class: str
    required_reliability_fraction: float
    measured_success_fraction: float
    trials: int
    task_duration_hours: float
    verifier_class: str
    intervention_events_per_100_tasks: float
    prompt_check_hours_per_task: float
    expected_recovery_cleanup_hours_per_task: float
    expected_total_human_hours_per_task: float
    rollback_success_fraction: float
    out_of_distribution_recovery_fraction: float
    achieved_rung: str
    achieved_rung_rank: int
    required_rung: str
    required_rung_rank: int
    reliability_requirement_passes: bool
    rung_requirement_passes: bool
    economic_substitution_passes: bool


def industrial_reliability_ladder(
    config: IndustrialReliabilityConfig,
) -> tuple[IndustrialReliabilityLadderResult, ...]:
    """Map benchmark-like success to consequence-specific substitution gates."""
    rungs = tuple(config["rungs"])
    expected = (
        "single_attempt",
        "repeated_success",
        "low_context_long_task",
        "high_context_production_task",
        "safety_critical_field_task",
        "unscripted_recovery",
        "sustained_bounded_intervention",
    )
    if rungs != expected:
        raise ValueError("industrial reliability ladder order is invalid")
    rank = {name: index for index, name in enumerate(rungs, start=1)}
    reliability = {
        name: validate_unit_interval(value, f"reliability.{name}")
        for name, value in config["required_reliability_by_consequence"].items()
    }
    rows: list[IndustrialReliabilityLadderResult] = []
    for name, task in config["tasks"].items():
        consequence = str(task["consequence_class"])
        if consequence not in reliability:
            raise ValueError(f"unknown consequence class {consequence!r}")
        success = validate_unit_interval(
            task["measured_success_fraction"],
            "measured_success_fraction",
        )
        rollback = validate_unit_interval(
            task["rollback_success_fraction"],
            "rollback_success_fraction",
        )
        ood_recovery = validate_unit_interval(
            task["out_of_distribution_recovery_fraction"],
            "out_of_distribution_recovery_fraction",
        )
        trials = int(task["trials"])
        duration = float(task["task_duration_hours"])
        interventions = float(task["intervention_events_per_100_tasks"])
        prompt_check = float(task["prompt_check_hours_per_task"])
        recovery_hours = float(task["recovery_hours_per_failed_task"])
        cleanup_hours = float(task["cleanup_hours_per_failed_task"])
        sustained_hours = float(task["sustained_operation_hours"])
        if (
            min(
                trials,
                duration,
                interventions,
                prompt_check,
                recovery_hours,
                cleanup_hours,
                sustained_hours,
            )
            < 0.0
        ):
            raise ValueError("reliability task values must be nonnegative")
        gates = {
            "single_attempt": (
                trials >= 1 and success >= float(config["single_attempt_threshold"])
            ),
            "repeated_success": (
                trials >= int(config["minimum_repeated_trials"])
                and success >= float(config["repeated_success_threshold"])
            ),
            "low_context_long_task": (
                bool(task["low_context_long_task_observed"])
                and duration >= float(config["long_task_hours_threshold"])
            ),
            "high_context_production_task": bool(task["high_context_production_observed"]),
            "safety_critical_field_task": (
                bool(task["safety_critical_field_observed"]) and success >= reliability[consequence]
            ),
            "unscripted_recovery": (
                bool(task["unscripted_recovery_observed"])
                and ood_recovery >= float(config["minimum_ood_recovery_fraction"])
                and rollback >= float(config["minimum_rollback_success_fraction"])
            ),
            "sustained_bounded_intervention": (
                sustained_hours >= float(config["minimum_sustained_operation_hours"])
                and interventions <= float(config["maximum_interventions_per_100_tasks"])
            ),
        }
        achieved_rank = 0
        achieved = "none"
        for rung in rungs:
            if gates[rung] and achieved_rank == rank[rung] - 1:
                achieved_rank = rank[rung]
                achieved = rung
            else:
                break
        required_rung = str(task["required_rung"])
        if required_rung not in rank:
            raise ValueError(f"unknown required rung {required_rung!r}")
        expected_failure_human = (1.0 - success) * (recovery_hours + cleanup_hours)
        reliability_pass = success >= reliability[consequence]
        rung_pass = achieved_rank >= rank[required_rung]
        rows.append(
            IndustrialReliabilityLadderResult(
                task=str(name),
                task_domain=str(task["task_domain"]),
                consequence_class=consequence,
                required_reliability_fraction=reliability[consequence],
                measured_success_fraction=success,
                trials=trials,
                task_duration_hours=duration,
                verifier_class=str(task["verifier_class"]),
                intervention_events_per_100_tasks=interventions,
                prompt_check_hours_per_task=prompt_check,
                expected_recovery_cleanup_hours_per_task=(expected_failure_human),
                expected_total_human_hours_per_task=(prompt_check + expected_failure_human),
                rollback_success_fraction=rollback,
                out_of_distribution_recovery_fraction=ood_recovery,
                achieved_rung=achieved,
                achieved_rung_rank=achieved_rank,
                required_rung=required_rung,
                required_rung_rank=rank[required_rung],
                reliability_requirement_passes=reliability_pass,
                rung_requirement_passes=rung_pass,
                economic_substitution_passes=(reliability_pass and rung_pass),
            )
        )
    return tuple(rows)


@dataclass(frozen=True)
class DataEvaluatorCoevolutionRow:
    scenario: str
    generation: int
    synthetic_records_generated: float
    synthetic_records_after_deduplication: float
    accepted_synthetic_training_signal: float
    physical_causal_episodes: float
    total_accepted_training_signal: float
    apparent_progress_index: float
    heldout_transfer_index: float
    evaluator_error_fraction: float
    evaluator_bias_fraction: float
    data_diversity_index: float
    provenance_valid_fraction: float
    causal_linkage_fraction: float
    physical_experiment_time_hours: float
    equipment_wear_units: float
    destructive_samples: float
    verification_capacity_used: float
    proprietary_data_advantage_index: float


def data_evaluator_coevolution(
    config: DataEvaluatorCoevolutionConfig,
) -> tuple[DataEvaluatorCoevolutionRow, ...]:
    """Co-evolve accepted signal, evaluator error, diversity, and leakage."""
    generations = int(config["generations"])
    if generations <= 0:
        raise ValueError("data coevolution generations must be positive")
    rows: list[DataEvaluatorCoevolutionRow] = []
    for scenario_name, scenario in config["scenarios"].items():
        synthetic_volume = float(scenario["initial_synthetic_records"])
        synthetic_growth = float(scenario["synthetic_volume_multiplier"])
        dedup = validate_unit_interval(
            scenario["deduplication_fraction"],
            "deduplication_fraction",
        )
        filter_yield = validate_unit_interval(
            scenario["filter_acceptance_fraction"],
            "filter_acceptance_fraction",
        )
        provenance = validate_unit_interval(
            scenario["provenance_valid_fraction"],
            "provenance_valid_fraction",
        )
        synthetic_share = validate_unit_interval(
            scenario["synthetic_share_of_training_mix"],
            "synthetic_share_of_training_mix",
        )
        evaluator_error = validate_unit_interval(
            scenario["initial_evaluator_error_fraction"],
            "initial_evaluator_error_fraction",
        )
        evaluator_bias = validate_unit_interval(
            scenario["initial_evaluator_bias_fraction"],
            "initial_evaluator_bias_fraction",
        )
        diversity = validate_unit_interval(
            scenario["initial_data_diversity_index"],
            "initial_data_diversity_index",
        )
        advantage = validate_unit_interval(
            scenario["initial_proprietary_data_advantage"],
            "initial_proprietary_data_advantage",
        )
        causal_linkage = validate_unit_interval(
            scenario["physical_causal_linkage_fraction"],
            "physical_causal_linkage_fraction",
        )
        if synthetic_volume < 0.0 or synthetic_growth <= 0.0:
            raise ValueError("synthetic volume settings are invalid")

        episode_limits = (
            float(scenario["physical_experiment_time_budget_hours"])
            / float(scenario["hours_per_physical_episode"]),
            float(scenario["equipment_wear_budget_units"])
            / float(scenario["wear_units_per_physical_episode"]),
            float(scenario["destructive_sample_budget"])
            / float(scenario["samples_per_physical_episode"]),
            float(scenario["physical_verification_capacity_episodes"]),
        )
        if any(value < 0.0 for value in episode_limits):
            raise ValueError("physical data budgets must be nonnegative")
        physical_episodes = min(episode_limits)
        time_used = physical_episodes * float(scenario["hours_per_physical_episode"])
        wear_used = physical_episodes * float(scenario["wear_units_per_physical_episode"])
        samples_used = physical_episodes * float(scenario["samples_per_physical_episode"])
        verification_used = physical_episodes

        leakage_survival = math.prod(
            1.0
            - validate_unit_interval(
                scenario[field],
                field,
            )
            for field in (
                "open_publication_capture_fraction",
                "espionage_leakage_fraction",
                "employee_mobility_leakage_fraction",
                "distillation_catchup_fraction",
                "independent_replication_fraction",
            )
        )
        for generation in range(generations):
            post_dedup = synthetic_volume * (1.0 - dedup)
            accepted_synthetic = (
                post_dedup * filter_yield * provenance * (1.0 - evaluator_error) * diversity
            )
            accepted_physical = physical_episodes * causal_linkage * (1.0 - evaluator_error)
            total_signal = accepted_synthetic + accepted_physical
            apparent_progress = math.log1p(synthetic_volume) * (1.0 - 0.25 * evaluator_error)
            heldout_transfer = (
                math.log1p(total_signal)
                * diversity
                * (1.0 - evaluator_bias)
                * (1.0 - evaluator_error)
            )
            rows.append(
                DataEvaluatorCoevolutionRow(
                    scenario=str(scenario_name),
                    generation=generation,
                    synthetic_records_generated=synthetic_volume,
                    synthetic_records_after_deduplication=post_dedup,
                    accepted_synthetic_training_signal=accepted_synthetic,
                    physical_causal_episodes=physical_episodes,
                    total_accepted_training_signal=total_signal,
                    apparent_progress_index=apparent_progress,
                    heldout_transfer_index=heldout_transfer,
                    evaluator_error_fraction=evaluator_error,
                    evaluator_bias_fraction=evaluator_bias,
                    data_diversity_index=diversity,
                    provenance_valid_fraction=provenance,
                    causal_linkage_fraction=causal_linkage,
                    physical_experiment_time_hours=time_used,
                    equipment_wear_units=wear_used,
                    destructive_samples=samples_used,
                    verification_capacity_used=verification_used,
                    proprietary_data_advantage_index=advantage,
                )
            )
            evaluator_error = min(
                max(
                    evaluator_error
                    + float(scenario["evaluator_drift_per_generation"]) * synthetic_share
                    - float(scenario["independent_evaluator_correction_per_generation"]),
                    0.0,
                ),
                1.0,
            )
            evaluator_bias = min(
                evaluator_bias
                + float(scenario["bias_amplification_per_generation"]) * synthetic_share,
                1.0,
            )
            diversity = max(
                diversity
                * (1.0 - float(scenario["diversity_narrowing_per_generation"]) * synthetic_share),
                0.0,
            )
            advantage *= leakage_survival
            synthetic_volume *= synthetic_growth
    return tuple(rows)


@dataclass(frozen=True)
class ReplicationGovernanceExternalityResult:
    scenario: str
    t: FloatArray
    productive_capacity: FloatArray
    legitimately_authorized_capacity: FloatArray
    unauthorized_capacity: FloatArray
    contested_resource_preempting_capacity: FloatArray
    debris_externality_stock: FloatArray
    remaining_contested_resource: FloatArray
    material_governance_leverage: FloatArray
    cumulative_output: FloatArray
    cumulative_owner_claim: FloatArray
    cumulative_public_claim: FloatArray
    cumulative_future_affected_party_claim: FloatArray
    cumulative_externality_cost: FloatArray
    engineering_endpoint_succeeds: bool
    governance_endpoint_succeeds: bool
    private_objective_succeeds: bool
    negative_sum_race: bool
    private_net_value: float
    social_net_value: float
    resource_claim_legitimacy: float
    externality_cost_internalization_fraction: float
    update_authority_gate: bool
    liability_gate: bool
    audit_rights_gate: bool
    succession_of_control_gate: bool
    future_affected_party_representation_gate: bool


def replication_governance_externalities(
    config: ReplicationGovernanceConfig,
) -> tuple[ReplicationGovernanceExternalityResult, ...]:
    """Compare private replication incentives with legitimate capacity."""
    years = float(config["years"])
    dt = float(config["dt"])
    max_unauthorized = validate_unit_interval(
        config["maximum_unauthorized_capacity_fraction"],
        "maximum_unauthorized_capacity_fraction",
    )
    max_preemptive = validate_unit_interval(
        config["maximum_preemptive_capacity_fraction"],
        "maximum_preemptive_capacity_fraction",
    )
    min_legitimacy = validate_unit_interval(
        config["minimum_resource_claim_legitimacy"],
        "minimum_resource_claim_legitimacy",
    )
    min_internalization = validate_unit_interval(
        config["minimum_externality_internalization_fraction"],
        "minimum_externality_internalization_fraction",
    )
    if years <= 0.0 or dt <= 0.0:
        raise ValueError("governance externality horizon and step positive")
    steps = round(years / dt)
    t = np.arange(steps + 1, dtype=float) * dt
    results: list[ReplicationGovernanceExternalityResult] = []
    for name, scenario in config["scenarios"].items():
        growth_rate = float(scenario["private_replication_rate_per_year"])
        auth_rate = float(scenario["authorization_capacity_per_year"])
        preempt_fraction = validate_unit_interval(
            scenario["contested_resource_preemption_fraction"],
            "contested_resource_preemption_fraction",
        )
        mitigation = validate_unit_interval(
            scenario["debris_mitigation_fraction"],
            "debris_mitigation_fraction",
        )
        legitimacy = validate_unit_interval(
            scenario["resource_claim_legitimacy"],
            "resource_claim_legitimacy",
        )
        internalization = validate_unit_interval(
            scenario["externality_cost_internalization_fraction"],
            "externality_cost_internalization_fraction",
        )
        claim_shares = {
            key: validate_unit_interval(value, f"claim_share.{key}")
            for key, value in scenario["future_output_claim_shares"].items()
        }
        if not math.isclose(sum(claim_shares.values()), 1.0, abs_tol=1e-9):
            raise ValueError("future output claim shares must sum to one")
        gates = {
            key: bool(scenario[key])
            for key in (
                "update_authority_gate",
                "liability_gate",
                "audit_rights_gate",
                "succession_of_control_gate",
                "future_affected_party_representation_gate",
            )
        }
        initial_capacity = float(scenario["initial_productive_capacity"])
        resource_initial = float(scenario["contested_resource_capacity"])
        output_rate = float(scenario["output_per_capacity_year"])
        debris_per_addition = float(scenario["debris_externality_per_capacity_added"])
        debris_cost = float(scenario["cost_per_debris_externality_unit"])
        preemption_cost = float(scenario["cost_per_preempted_resource_unit"])
        unauthorized_cost = float(scenario["cost_per_unauthorized_capacity_unit_year"])
        closure_rate = float(scenario["material_leverage_decline_rate_per_year"])
        private_build_cost = float(scenario["private_build_cost_per_capacity"])
        if (
            min(
                growth_rate,
                auth_rate,
                initial_capacity,
                resource_initial,
                output_rate,
                debris_per_addition,
                debris_cost,
                preemption_cost,
                unauthorized_cost,
                closure_rate,
                private_build_cost,
            )
            < 0.0
        ):
            raise ValueError("governance scenario values must be nonnegative")

        productive = np.zeros(steps + 1)
        authorized = np.zeros(steps + 1)
        unauthorized = np.zeros(steps + 1)
        preemptive = np.zeros(steps + 1)
        debris = np.zeros(steps + 1)
        remaining_resource = np.zeros(steps + 1)
        leverage = np.exp(-closure_rate * t)
        cumulative_output = np.zeros(steps + 1)
        owner_claim = np.zeros(steps + 1)
        public_claim = np.zeros(steps + 1)
        future_claim = np.zeros(steps + 1)
        externality_cost = np.zeros(steps + 1)
        productive[0] = initial_capacity
        authorized[0] = initial_capacity
        remaining_resource[0] = resource_initial
        cumulative_private_build_cost = 0.0

        for k in range(steps):
            proposed_addition = growth_rate * productive[k] * dt
            authorized_addition = min(
                proposed_addition,
                auth_rate * dt,
            )
            unauthorized_addition = max(
                proposed_addition - authorized_addition,
                0.0,
            )
            preempted = min(
                proposed_addition * preempt_fraction,
                remaining_resource[k],
            )
            productive[k + 1] = productive[k] + proposed_addition
            authorized[k + 1] = authorized[k] + authorized_addition
            unauthorized[k + 1] = unauthorized[k] + unauthorized_addition
            preemptive[k + 1] = preemptive[k] + preempted
            remaining_resource[k + 1] = max(
                remaining_resource[k] - preempted,
                0.0,
            )
            debris[k + 1] = debris[k] + proposed_addition * debris_per_addition * (1.0 - mitigation)
            output = productive[k] * output_rate * dt
            cumulative_output[k + 1] = cumulative_output[k] + output
            owner_claim[k + 1] = owner_claim[k] + output * claim_shares["owner_operator"]
            public_claim[k + 1] = public_claim[k] + output * claim_shares["current_public"]
            future_claim[k + 1] = future_claim[k] + output * claim_shares["future_affected_parties"]
            step_externality = (
                debris[k + 1] * debris_cost * dt
                + preempted * preemption_cost
                + unauthorized[k + 1] * unauthorized_cost * dt
            )
            externality_cost[k + 1] = externality_cost[k] + step_externality
            cumulative_private_build_cost += (
                proposed_addition * private_build_cost + step_externality * internalization
            )
        unauthorized_share = unauthorized[-1] / productive[-1] if productive[-1] > 0.0 else 0.0
        preemptive_share = preemptive[-1] / productive[-1] if productive[-1] > 0.0 else 0.0
        engineering_success = productive[-1] >= 2.0 * initial_capacity
        governance_success = (
            unauthorized_share <= max_unauthorized + 1e-12
            and preemptive_share <= max_preemptive + 1e-12
            and legitimacy >= min_legitimacy
            and internalization >= min_internalization
            and all(gates.values())
        )
        private_net = owner_claim[-1] - cumulative_private_build_cost
        social_net = cumulative_output[-1] - externality_cost[-1]
        private_success = private_net > 0.0
        results.append(
            ReplicationGovernanceExternalityResult(
                scenario=str(name),
                t=t,
                productive_capacity=productive,
                legitimately_authorized_capacity=authorized,
                unauthorized_capacity=unauthorized,
                contested_resource_preempting_capacity=preemptive,
                debris_externality_stock=debris,
                remaining_contested_resource=remaining_resource,
                material_governance_leverage=leverage,
                cumulative_output=cumulative_output,
                cumulative_owner_claim=owner_claim,
                cumulative_public_claim=public_claim,
                cumulative_future_affected_party_claim=future_claim,
                cumulative_externality_cost=externality_cost,
                engineering_endpoint_succeeds=engineering_success,
                governance_endpoint_succeeds=governance_success,
                private_objective_succeeds=private_success,
                negative_sum_race=private_success and social_net < 0.0,
                private_net_value=private_net,
                social_net_value=social_net,
                resource_claim_legitimacy=legitimacy,
                externality_cost_internalization_fraction=internalization,
                update_authority_gate=gates["update_authority_gate"],
                liability_gate=gates["liability_gate"],
                audit_rights_gate=gates["audit_rights_gate"],
                succession_of_control_gate=gates["succession_of_control_gate"],
                future_affected_party_representation_gate=gates[
                    "future_affected_party_representation_gate"
                ],
            )
        )
    return tuple(results)


@dataclass(frozen=True)
class DigitalProgressResult:
    regime: str
    gate_case: str
    t: FloatArray
    internal_capability: FloatArray
    public_capability: FloatArray
    effective_compute: FloatArray
    frontier: FloatArray
    experiment_loops_per_year: FloatArray
    technically_validated_loops_per_year: FloatArray
    internally_authorized_loops_per_year: FloatArray
    marginal_gain_per_loop: FloatArray
    completed_experiments: FloatArray
    completed_technical_validations: FloatArray
    completed_internal_adoptions: FloatArray
    public_release_events: FloatArray
    capability_overhang: FloatArray

    @property
    def capability(self) -> FloatArray:
        """Compatibility view of capability available to the internal loop."""
        return self.internal_capability

    @property
    def verified_loops_per_year(self) -> FloatArray:
        """Compatibility view of technically validated and authorized loops."""
        return self.internally_authorized_loops_per_year

    @property
    def completed_loops(self) -> FloatArray:
        """Compatibility view of completed internally authorized adoptions."""
        return self.completed_internal_adoptions


def simulate_digital_progress(
    config: DigitalImprovementConfig,
    *,
    regime: str,
    gate_case: str = "zero_lag",
    years: float = 20.0,
    dt: float = 0.25,
) -> DigitalProgressResult:
    """Simulate one declared digital-progress sensitivity regime.

    ``smooth_diminishing`` declines with cumulative effective effort,
    ``saturating_frontier`` declines with the remaining frontier gap, and
    ``innovation_interrupted`` uses the same frontier dynamics but applies
    declared, discrete frontier shifts at their event years.
    """
    allowed = {
        "smooth_diminishing",
        "saturating_frontier",
        "innovation_interrupted",
    }
    if regime not in allowed:
        raise ValueError(f"unknown digital progress regime {regime!r}")
    if years <= 0.0 or dt <= 0.0:
        raise ValueError("years and dt must be positive")

    stage_rates = config["stage_rates_per_year"]
    experiment_loop_rate = verified_loop_throughput(stage_rates)
    training_flop = float(config["training_flop_per_loop"])
    useful_flop = effective_training_compute(
        training_flop,
        hardware_efficiency=float(config["hardware_efficiency"]),
        utilization=float(config["utilization"]),
        algorithmic_efficiency=float(config["algorithmic_efficiency"]),
        architecture_efficiency=float(config["architecture_efficiency"]),
    )
    initial = float(config["initial_capability"])
    base_frontier = float(config["frontier_capability"])
    if base_frontier <= initial:
        raise ValueError("frontier_capability must exceed initial_capability")
    gain_scale = float(config["gain_scale_per_verified_loop"])
    curvature = float(config["diminishing_exponent"])
    compute_scale = float(config["effective_compute_scale_flop"])
    technical_validation_fraction = validate_unit_interval(
        config["technical_validation_fraction"],
        "technical_validation_fraction",
    )
    gate_cases = config["capability_gate_cases"]
    if gate_case not in gate_cases:
        raise ValueError(f"unknown capability gate case {gate_case!r}")
    gate_config = gate_cases[gate_case]
    internal_authorization_fraction = validate_unit_interval(
        gate_config["internal_authorization_fraction"],
        "internal_authorization_fraction",
    )
    public_authorization_fraction = validate_unit_interval(
        gate_config["public_authorization_fraction"],
        "public_authorization_fraction",
    )
    public_capability_slice_fraction = validate_unit_interval(
        gate_config["public_capability_slice_fraction"],
        "public_capability_slice_fraction",
    )
    public_release_interval_years = float(gate_config["public_release_interval_years"])
    if public_release_interval_years < 0.0:
        raise ValueError("public_release_interval_years must be nonnegative")
    if gain_scale < 0.0 or curvature <= 0.0 or compute_scale <= 0.0:
        raise ValueError("gain scale must be nonnegative; exponent and scale positive")

    events = sorted(
        (
            float(event["year"]),
            float(event["frontier_increment"]),
        )
        for event in config.get("innovation_events", ())
    )
    if any(year < 0.0 or increment < 0.0 for year, increment in events):
        raise ValueError("innovation event years and increments must be nonnegative")

    steps = round(years / dt)
    t = np.arange(steps + 1, dtype=float) * dt
    internal_capability = np.zeros(steps + 1)
    public_capability = np.zeros(steps + 1)
    effective_compute = np.zeros(steps + 1)
    frontier = np.full(steps + 1, base_frontier)
    experiment_rates = np.full(steps + 1, experiment_loop_rate)
    technical_rates = np.full(
        steps + 1,
        experiment_loop_rate * technical_validation_fraction,
    )
    internal_rates = np.full(
        steps + 1,
        experiment_loop_rate * technical_validation_fraction * internal_authorization_fraction,
    )
    marginal = np.zeros(steps + 1)
    experiments = np.zeros(steps + 1)
    technical_validations = np.zeros(steps + 1)
    internal_adoptions = np.zeros(steps + 1)
    public_release_events = np.zeros(steps + 1)
    capability_overhang = np.zeros(steps + 1)
    internal_capability[0] = initial
    public_capability[0] = initial
    event_cursor = 0
    current_frontier = base_frontier
    initial_gap = base_frontier - initial
    next_public_release = public_release_interval_years

    for k in range(steps):
        if regime == "innovation_interrupted":
            while event_cursor < len(events) and events[event_cursor][0] <= t[k]:
                current_frontier += events[event_cursor][1]
                event_cursor += 1
        frontier[k] = current_frontier
        completed_experiments = experiment_rates[k] * dt
        completed_validations = technical_rates[k] * dt
        authorized_adoptions = internal_rates[k] * dt
        experiments[k + 1] = experiments[k] + completed_experiments
        technical_validations[k + 1] = technical_validations[k] + completed_validations
        internal_adoptions[k + 1] = internal_adoptions[k] + authorized_adoptions
        effective_compute[k + 1] = effective_compute[k] + completed_experiments * useful_flop

        if regime == "smooth_diminishing":
            attenuation = (1.0 + effective_compute[k] / compute_scale) ** (-curvature)
        else:
            gap = max(current_frontier - internal_capability[k], 0.0)
            reference_gap = max(current_frontier - initial, initial_gap, 1e-12)
            attenuation = (gap / reference_gap) ** curvature
        marginal[k] = gain_scale * attenuation
        internal_capability[k + 1] = internal_capability[k] + marginal[k] * authorized_adoptions
        if regime != "smooth_diminishing":
            internal_capability[k + 1] = min(
                internal_capability[k + 1],
                current_frontier,
            )

        public_capability[k + 1] = public_capability[k]
        public_release_events[k + 1] = public_release_events[k]
        release_due = public_release_interval_years == 0.0 or (
            t[k + 1] + 1e-12 >= next_public_release
        )
        if release_due:
            public_share = public_authorization_fraction * public_capability_slice_fraction
            public_capability[k + 1] = initial + public_share * (
                internal_capability[k + 1] - initial
            )
            public_release_events[k + 1] += 1.0
            if public_release_interval_years > 0.0:
                while next_public_release <= t[k + 1] + 1e-12:
                    next_public_release += public_release_interval_years
        capability_overhang[k + 1] = internal_capability[k + 1] - public_capability[k + 1]
        frontier[k + 1] = current_frontier
    marginal[-1] = marginal[-2] if steps else 0.0
    return DigitalProgressResult(
        regime=regime,
        gate_case=gate_case,
        t=t,
        internal_capability=internal_capability,
        public_capability=public_capability,
        effective_compute=effective_compute,
        frontier=frontier,
        experiment_loops_per_year=experiment_rates,
        technically_validated_loops_per_year=technical_rates,
        internally_authorized_loops_per_year=internal_rates,
        marginal_gain_per_loop=marginal,
        completed_experiments=experiments,
        completed_technical_validations=technical_validations,
        completed_internal_adoptions=internal_adoptions,
        public_release_events=public_release_events,
        capability_overhang=capability_overhang,
    )


@dataclass(frozen=True)
class DataAdvantageResult:
    profile: dict[str, float]
    scalar_assumption: float
    gates_passed: bool


def data_advantage(
    components: Mapping[str, float],
    *,
    weights: Mapping[str, float],
    gates: Mapping[str, float],
) -> DataAdvantageResult:
    """Report a component profile and an explicitly assumption-class scalar."""
    required = {
        "unique",
        "causal",
        "coverage",
        "quality",
        "access",
        "integration",
        "verification",
    }
    if set(components) != required or set(weights) != required:
        raise ValueError("data-advantage components and weights must use exact schema")
    profile = {
        name: validate_unit_interval(value, f"data component {name}")
        for name, value in components.items()
    }
    total_weight = sum(float(value) for value in weights.values())
    if total_weight <= 0.0 or any(float(value) < 0.0 for value in weights.values()):
        raise ValueError("data-advantage weights must be nonnegative and nonzero")
    normalized = {name: float(weights[name]) / total_weight for name in required}
    gates_passed = all(
        profile[name] >= validate_unit_interval(threshold, f"gate {name}")
        for name, threshold in gates.items()
    )
    if set(gates) - required:
        raise ValueError("unknown data-advantage gate")
    if not gates_passed or any(value == 0.0 for value in profile.values()):
        scalar = 0.0
    else:
        scalar = math.exp(sum(normalized[name] * math.log(profile[name]) for name in required))
    return DataAdvantageResult(profile, scalar, gates_passed)
