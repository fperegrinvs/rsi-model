"""Domain models split from the public :mod:`rsimodel.extensions` facade."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .array_types import FloatArray
from .extension_config import (
    IntergenerationalLearningConfig,
    PartialClosureSupportConfig,
)
from .extensions_digital import (
    validate_unit_interval,
)


def active_graph_edge_weight(adjacency: FloatArray) -> float:
    """Return weighted directed edge count after validating a task graph."""
    graph = np.asarray(adjacency, dtype=float)
    if graph.ndim != 2 or graph.shape[0] != graph.shape[1]:
        raise ValueError("coordination adjacency must be square")
    if np.any(graph < 0.0) or np.any(np.diag(graph) != 0.0):
        raise ValueError("coordination edges must be nonnegative with zero diagonal")
    return float(graph.sum())


def coordination_burden(
    *,
    irreducible_hours: float,
    reference_hours: float,
    active_edge_weight: float,
    edge_reference: float,
    complexity: float,
    complexity_reference: float,
    uncertainty: float,
    uncertainty_reference: float,
    effective_intelligence: float,
    intelligence_reference: float,
    alpha: float,
    beta: float,
    gamma: float,
    delta: float,
    intelligence_response: float,
) -> float:
    """Coordination agent-hours per unit of verified production."""
    positive = (
        reference_hours,
        edge_reference,
        complexity_reference,
        uncertainty_reference,
        intelligence_reference,
        alpha,
        beta,
        gamma,
        delta,
        intelligence_response,
    )
    if irreducible_hours < 0.0 or any(value <= 0.0 for value in positive):
        raise ValueError("coordination references/exponents must be positive")
    if min(active_edge_weight, complexity, uncertainty, effective_intelligence) < 0:
        raise ValueError("coordination inputs must be nonnegative")
    numerator = (
        reference_hours
        * (active_edge_weight / edge_reference) ** alpha
        * (complexity / complexity_reference) ** beta
        * (uncertainty / uncertainty_reference) ** gamma
    )
    denominator = (
        1.0 + intelligence_response * (effective_intelligence / intelligence_reference) ** delta
    )
    return float(irreducible_hours + numerator / denominator)


def coordination_burden_form(
    form: str,
    *,
    edge_saturation_ratio: float = 3.0,
    **kwargs: float,
) -> float:
    """Evaluate alternative edge-response forms on the same burden boundary."""
    if form == "power":
        return coordination_burden(**kwargs)
    # Reuse the canonical validator and limiting-case checks.
    coordination_burden(**kwargs)
    edges = float(kwargs["active_edge_weight"])
    edge_reference = float(kwargs["edge_reference"])
    alpha = float(kwargs["alpha"])
    ratio = edges / edge_reference
    if form == "logarithmic":
        edge_factor = math.log1p(ratio) / math.log(2.0)
    elif form == "saturating":
        if edge_saturation_ratio <= 0.0:
            raise ValueError("edge_saturation_ratio must be positive")
        raw = ratio**alpha / (1.0 + (ratio / edge_saturation_ratio) ** alpha)
        reference = 1.0 / (1.0 + (1.0 / edge_saturation_ratio) ** alpha)
        edge_factor = raw / reference
    else:
        raise ValueError(f"unknown coordination burden form {form!r}")
    numerator = (
        float(kwargs["reference_hours"])
        * edge_factor
        * (float(kwargs["complexity"]) / float(kwargs["complexity_reference"]))
        ** float(kwargs["beta"])
        * (float(kwargs["uncertainty"]) / float(kwargs["uncertainty_reference"]))
        ** float(kwargs["gamma"])
    )
    denominator = 1.0 + float(kwargs["intelligence_response"]) * (
        float(kwargs["effective_intelligence"]) / float(kwargs["intelligence_reference"])
    ) ** float(kwargs["delta"])
    return float(float(kwargs["irreducible_hours"]) + numerator / denominator)


@dataclass(frozen=True)
class EmbodimentEvaluation:
    task: str
    portfolio: str
    physically_adequate: bool
    failed_dimensions: tuple[str, ...]
    hardware_ceiling: float
    intelligence_threshold: float | None
    first_passage_year: float | None
    score_trajectory: FloatArray
    failure_attribution: str


@dataclass(frozen=True)
class IntergenerationalLearningResult:
    generation: int
    fault_family: str
    training_case: str
    hidden_transfer_case: str
    holdout_exposed_to_training: bool
    learning_latency_days: float
    lesson_retention_fraction: float
    transfer_success_fraction: float
    recurrence_fraction: float
    recovery_time_days: float
    verification_compute_hours: float
    prior_task_regression_fraction: float
    transfer_gate_passes: bool
    retention_gate_passes: bool
    regression_gate_passes: bool


def simulate_intergenerational_learning(
    config: IntergenerationalLearningConfig,
) -> tuple[IntergenerationalLearningResult, ...]:
    """Run a deterministic hidden-transfer fault campaign across generations."""
    generations = int(config["generations"])
    if generations < 2:
        raise ValueError("at least two generations are required")
    transfer_gate = validate_unit_interval(
        config["minimum_transfer_success_fraction"],
        "minimum transfer success",
    )
    retention_gate = validate_unit_interval(
        config["minimum_lesson_retention_fraction"],
        "minimum lesson retention",
    )
    regression_gate = validate_unit_interval(
        config["maximum_prior_task_regression_fraction"],
        "maximum prior-task regression",
    )
    results: list[IntergenerationalLearningResult] = []
    for family_name, family in config["fault_families"].items():
        baseline_recurrence = validate_unit_interval(
            family["baseline_recurrence_fraction"],
            f"{family_name}.baseline recurrence",
        )
        learning_effectiveness = validate_unit_interval(
            family["learning_effectiveness_fraction"],
            f"{family_name}.learning effectiveness",
        )
        transfer_similarity = validate_unit_interval(
            family["hidden_case_structural_similarity"],
            f"{family_name}.hidden-case similarity",
        )
        retention_per_generation = validate_unit_interval(
            family["retention_per_generation"],
            f"{family_name}.retention",
        )
        replay_protection = validate_unit_interval(
            family["replay_protection_fraction"],
            f"{family_name}.replay protection",
        )
        for generation in range(generations):
            if generation == 0:
                retention = 0.0
                transfer = float(family["baseline_transfer_success_fraction"])
            else:
                retention = learning_effectiveness * retention_per_generation ** (generation - 1)
                transfer = min(
                    float(family["baseline_transfer_success_fraction"])
                    + retention * transfer_similarity,
                    1.0,
                )
            recurrence = baseline_recurrence * (1.0 - transfer)
            recovery = float(family["baseline_recovery_time_days"]) * (
                1.0 - float(family["maximum_recovery_reduction_fraction"]) * transfer
            )
            latency = (
                float(config["pipeline_base_latency_days"])
                + float(family["curation_days"])
                + float(family["training_days"])
                + float(family["verification_days"])
                + float(family["deployment_days"])
            )
            verification_compute = float(family["verification_compute_hours"]) * (
                1.0 + float(config["holdout_compute_overhead_fraction"])
            )
            regression = (
                float(family["update_interference_fraction"])
                * (1.0 - replay_protection)
                * (1.0 - retention)
                if generation > 0
                else 0.0
            )
            results.append(
                IntergenerationalLearningResult(
                    generation=generation,
                    fault_family=family_name,
                    training_case=str(family["training_case"]),
                    hidden_transfer_case=str(family["hidden_transfer_case"]),
                    holdout_exposed_to_training=False,
                    learning_latency_days=latency,
                    lesson_retention_fraction=retention,
                    transfer_success_fraction=transfer,
                    recurrence_fraction=recurrence,
                    recovery_time_days=recovery,
                    verification_compute_hours=verification_compute,
                    prior_task_regression_fraction=regression,
                    transfer_gate_passes=(generation == 0 or transfer >= transfer_gate),
                    retention_gate_passes=(generation == 0 or retention >= retention_gate),
                    regression_gate_passes=regression <= regression_gate,
                )
            )
    return tuple(results)


def learning_feedback_to_digital_loop(
    base_stage_rates: Mapping[str, float],
    learning_results: Sequence[IntergenerationalLearningResult],
    *,
    annual_verification_compute_budget_hours: float,
) -> tuple[dict[str, float], float]:
    """Convert observed campaign metrics into loop rates and verified yield."""
    if not learning_results:
        raise ValueError("learning_results cannot be empty")
    if annual_verification_compute_budget_hours <= 0.0:
        raise ValueError("verification budget must be positive")
    rates = {name: float(value) for name, value in base_stage_rates.items()}
    verified = [row for row in learning_results if row.generation > 0]
    if not verified:
        raise ValueError("learning_results need a post-update generation")
    latency = float(np.median([row.learning_latency_days for row in verified]))
    verification_cost = float(np.mean([row.verification_compute_hours for row in verified]))
    retention = float(np.mean([row.lesson_retention_fraction for row in verified]))
    transfer = float(np.mean([row.transfer_success_fraction for row in verified]))
    recurrence = float(np.mean([row.recurrence_fraction for row in verified]))
    rates["observe"] = min(rates["observe"], 365.0 / latency)
    rates["deploy"] = min(rates["deploy"], 365.0 / latency)
    verification_rate = annual_verification_compute_budget_hours / (
        verification_cost * len({row.fault_family for row in verified})
    )
    rates["evaluate"] = min(rates["evaluate"], verification_rate)
    rates["safety"] = min(rates["safety"], verification_rate)
    verified_yield = validate_unit_interval(
        retention * transfer * (1.0 - recurrence),
        "campaign-derived verification yield",
    )
    return rates, verified_yield


def evaluate_embodiment(
    *,
    task: str,
    portfolio: str,
    requirements: Mapping[str, float],
    embodiment: Mapping[str, float],
    intelligence: ArrayLike,
    years: ArrayLike,
    verification: ArrayLike | None = None,
    intelligence_onset: float,
    intelligence_scale: float,
    required_score: float,
) -> EmbodimentEvaluation:
    """Evaluate hard physical gates and intelligence first passage."""
    if set(requirements) != set(embodiment):
        raise ValueError("task and embodiment dimensions must match exactly")
    if intelligence_scale <= 0.0:
        raise ValueError("intelligence_scale must be positive")
    required_score = validate_unit_interval(required_score, "required_score")
    trajectory = np.asarray(intelligence, dtype=float)
    time = np.asarray(years, dtype=float)
    if trajectory.shape != time.shape or trajectory.ndim != 1:
        raise ValueError("intelligence and years must be equal one-dimensional arrays")
    if len(time) == 0 or np.any(np.diff(time) < 0.0):
        raise ValueError("years must be nonempty and nondecreasing")
    verify = (
        np.ones(len(time), dtype=bool)
        if verification is None
        else np.asarray(verification, dtype=bool)
    )
    if verify.shape != time.shape:
        raise ValueError("verification must match trajectory")

    failed = tuple(
        name for name in sorted(requirements) if float(embodiment[name]) < float(requirements[name])
    )
    ratios = [
        float(embodiment[name]) / max(float(requirements[name]), 1e-12) for name in requirements
    ]
    ceiling = min(max(min(ratios), 0.0), 1.0)
    adequate = not failed
    if not adequate:
        scores = np.zeros_like(trajectory)
        return EmbodimentEvaluation(
            task,
            portfolio,
            False,
            failed,
            ceiling,
            None,
            None,
            scores,
            "embodiment_limited",
        )

    positive = np.maximum((trajectory - intelligence_onset) / intelligence_scale, 0.0)
    scores = ceiling * (1.0 - np.exp(-positive))
    if required_score >= ceiling:
        threshold = None
    else:
        threshold = float(
            intelligence_onset - intelligence_scale * math.log(1.0 - required_score / ceiling)
        )
    reached = np.flatnonzero((scores >= required_score) & verify)
    first_passage = float(time[reached[0]]) if len(reached) else None
    attribution = (
        "verified"
        if first_passage is not None
        else (
            "verification_limited" if np.any(scores >= required_score) else "intelligence_limited"
        )
    )
    return EmbodimentEvaluation(
        task,
        portfolio,
        True,
        (),
        ceiling,
        threshold,
        first_passage,
        scores,
        attribution,
    )


@dataclass(frozen=True)
class ClosureMetrics:
    strict_autonomy: bool
    mass_closure_fraction: float
    external_support_intensity: float
    import_leverage: float | None
    critical_external_inputs: tuple[str, ...]


def partial_closure_metrics(
    *,
    local_mass_flow: Mapping[str, float],
    external_mass_flow: Mapping[str, float],
    verified_capacity_added_per_year: float,
    critical_inputs: Sequence[str],
) -> ClosureMetrics:
    """Separate mass closure from strict autonomy and import leverage."""
    if set(local_mass_flow) != set(external_mass_flow):
        raise ValueError("local and external flows must have identical inputs")
    if verified_capacity_added_per_year < 0.0:
        raise ValueError("verified capacity flow must be nonnegative")
    if any(value < 0.0 for value in (*local_mass_flow.values(), *external_mass_flow.values())):
        raise ValueError("mass flows must be nonnegative")
    total_local = float(sum(local_mass_flow.values()))
    total_external = float(sum(external_mass_flow.values()))
    total = total_local + total_external
    closure = total_local / total if total > 0.0 else 1.0
    critical_external = tuple(
        name for name in critical_inputs if float(external_mass_flow.get(name, 0.0)) > 1e-12
    )
    strict = not critical_external
    intensity = (
        total_external / verified_capacity_added_per_year
        if verified_capacity_added_per_year > 0.0
        else math.inf
        if total_external > 0.0
        else 0.0
    )
    leverage = verified_capacity_added_per_year / total_external if total_external > 0.0 else None
    return ClosureMetrics(
        strict,
        closure,
        intensity,
        leverage,
        critical_external,
    )


@dataclass(frozen=True)
class SupportedGrowthResult:
    policy: str
    t: FloatArray
    capacity: FloatArray
    inventory: FloatArray
    external_delivery: FloatArray
    replacement_demand: FloatArray
    commissioning_demand: FloatArray
    capacity_loss: FloatArray
    binding_input: tuple[str, ...]
    first_stockout_year: float | None
    substitution_effort: FloatArray
    substitution_validated: FloatArray
    substitution_failed: FloatArray
    supplier_capacity_t_per_year: FloatArray
    supplier_utilization: FloatArray
    supplier_binding_resource: tuple[str, ...]


def simulate_supported_growth(
    config: PartialClosureSupportConfig,
    *,
    policy: str,
) -> SupportedGrowthResult:
    """Simulate local growth constrained by a vector of residual imports.

    The model is intentionally probability-free. Failed deliveries are a
    declared derating, synchronized replacement waves are deterministic, and
    a disrupted policy follows its named outage interval. Replacement demand
    is served before expansion; unmet indispensable replacement demand removes
    the affected capacity. All residual-input masses are tonnes.
    """
    inputs = tuple(config["residual_inputs"])
    if not inputs:
        raise ValueError("supported growth requires residual inputs")
    policies = {
        **config["policies"],
        **config.get("allocation_policies", {}),
    }
    if policy not in policies:
        raise ValueError(f"unknown support policy {policy!r}")
    policy_cfg = policies[policy]
    years = int(config["horizon_years"])
    if years <= 0:
        raise ValueError("horizon_years must be a positive integer")
    growth_rate = float(config["local_growth_per_year"])
    if growth_rate < 0.0:
        raise ValueError("local_growth_per_year must be nonnegative")

    n_inputs = len(inputs)
    t = np.arange(years + 1, dtype=float)
    capacity = np.zeros(years + 1)
    inventory = np.zeros((years + 1, n_inputs))
    delivery = np.zeros((years + 1, n_inputs))
    replacement = np.zeros((years + 1, n_inputs))
    commissioning = np.zeros((years + 1, n_inputs))
    capacity_loss = np.zeros(years + 1)
    substitution_effort = np.zeros((years + 1, n_inputs))
    substitution_validated = np.zeros((years + 1, n_inputs), dtype=bool)
    substitution_failed = np.zeros((years + 1, n_inputs), dtype=bool)
    supplier_capacity = np.zeros(years + 1)
    supplier_utilization = np.zeros(years + 1)
    supplier_binding: list[str] = [""] * (years + 1)
    binding: list[str] = [""] * (years + 1)
    capacity[0] = float(config["initial_capacity"])
    if capacity[0] < 0.0:
        raise ValueError("initial_capacity must be nonnegative")
    for index, name in enumerate(inputs):
        spec = config["residual_inputs"][name]
        inventory[0, index] = float(spec["initial_stockpile_t"])
        nonnegative = (
            "commissioning_t_per_capacity",
            "replacement_t_per_capacity_year",
            "initial_stockpile_t",
            "shelf_life_years",
            "obsolescence_per_year",
            "radiation_storage_loss_per_year",
            "delivery_failure_fraction",
            "minimum_lot_t",
            "replacement_wave_interval_years",
            "replacement_wave_fraction",
            "external_supplier_capacity_t_per_year",
        )
        if any(float(spec[key]) < 0.0 for key in nonnegative):
            raise ValueError(f"negative residual-input parameter for {name}")
        validate_unit_interval(
            spec["delivery_failure_fraction"],
            f"{name} delivery_failure_fraction",
        )
    supplier_cfg = config["external_supplier"]
    supplier_reliability = validate_unit_interval(
        supplier_cfg["reliability_fraction"],
        "external supplier reliability_fraction",
    )
    if not supplier_cfg["resources"]:
        raise ValueError("external supplier needs resource capacities")
    for name, resource in supplier_cfg["resources"].items():
        if (
            float(resource["initial_capacity_per_year"]) < 0.0
            or float(resource["growth_per_year"]) < 0.0
            or float(resource["requirement_per_import_t"]) <= 0.0
        ):
            raise ValueError(f"invalid external supplier resource {name}")

    first_stockout: float | None = None
    for year in range(years):
        substitution_effort[year + 1] = substitution_effort[year]
        substitution_validated[year + 1] = substitution_validated[year]
        substitution_failed[year + 1] = substitution_failed[year]
        programs = config.get("substitution_programs", {})
        allocation_fraction = float(policy_cfg.get("substitution_allocation_fraction", 0.0))
        validate_unit_interval(
            allocation_fraction,
            f"{policy} substitution_allocation_fraction",
        )
        active_programs = [
            (index, name, programs[name])
            for index, name in enumerate(inputs)
            if name in programs
            and not substitution_validated[year, index]
            and not substitution_failed[year, index]
        ]
        intelligence = (
            float(config.get("initial_intelligence", 1.0))
            + float(config.get("intelligence_gain_per_year", 0.0)) * year
        )
        eligible_programs = [
            (index, name, program)
            for index, name, program in active_programs
            if intelligence >= float(program["required_intelligence"])
            and bool(program["embodiment_adequate"])
            and bool(program["materials_available"])
            and bool(program["tools_available"])
            and bool(program["test_facility_available"])
        ]
        program_effort_budget = (
            capacity[year] * growth_rate * allocation_fraction if eligible_programs else 0.0
        )
        if eligible_programs:
            effort_per_program = program_effort_budget / len(eligible_programs)
            for index, _name, program in eligible_programs:
                substitution_effort[year + 1, index] += effort_per_program
                threshold = float(program["effort_capacity_years"])
                minimum_completion_year = float(program["minimum_completion_year"])
                if (
                    substitution_effort[year + 1, index] >= threshold
                    and year + 1 >= minimum_completion_year
                ):
                    if program["outcome"] == "validated":
                        substitution_validated[year + 1, index] = True
                    elif program["outcome"] == "failed":
                        substitution_failed[year + 1, index] = True
                    else:
                        raise ValueError("substitution outcome must be validated or failed")

        planned_imports = np.zeros(n_inputs)
        for index, name in enumerate(inputs):
            spec = config["residual_inputs"][name]
            if policy_cfg["kind"] == "fixed":
                annual_imports = policy_cfg.get("annual_import_t")
                if annual_imports is None:
                    raise ValueError(f"{policy}: fixed policy requires annual_import_t")
                planned = float(annual_imports[name])
            elif policy_cfg["kind"] == "proportional":
                capacity_imports = policy_cfg.get("t_per_capacity_year")
                if capacity_imports is None:
                    raise ValueError(f"{policy}: proportional policy requires t_per_capacity_year")
                planned = float(capacity_imports[name]) * capacity[year]
            elif policy_cfg["kind"] == "finite_stockpile":
                planned = 0.0
            elif policy_cfg["kind"] == "declining_disrupted":
                initial_imports = policy_cfg.get("initial_annual_import_t")
                decline_per_year = policy_cfg.get("decline_per_year")
                outage_years = policy_cfg.get("outage_years")
                recovery_fraction = policy_cfg.get("recovery_fraction")
                if (
                    initial_imports is None
                    or decline_per_year is None
                    or outage_years is None
                    or recovery_fraction is None
                ):
                    raise ValueError(
                        f"{policy}: declining-disrupted policy requires its full schedule"
                    )
                planned = float(initial_imports[name]) * math.exp(-float(decline_per_year) * year)
                outage_start, outage_end = outage_years
                if float(outage_start) <= year < float(outage_end):
                    planned = 0.0
                elif year >= float(outage_end):
                    planned *= float(recovery_fraction)
            else:
                raise ValueError(f"unknown support policy kind {policy_cfg['kind']!r}")
            if 0.0 < planned < float(spec["minimum_lot_t"]):
                planned = float(spec["minimum_lot_t"])
            planned_imports[index] = min(
                planned,
                float(spec["external_supplier_capacity_t_per_year"]),
            )

        resource_capacities = {
            name: (
                float(resource["initial_capacity_per_year"])
                * (1.0 + float(resource["growth_per_year"])) ** year
                / float(resource["requirement_per_import_t"])
            )
            for name, resource in supplier_cfg["resources"].items()
        }
        supplier_binding[year + 1] = min(
            resource_capacities,
            key=lambda name: resource_capacities[name],
        )
        supplier_capacity[year + 1] = (
            resource_capacities[supplier_binding[year + 1]] * supplier_reliability
        )
        total_planned = float(planned_imports.sum())
        if total_planned > supplier_capacity[year + 1] > 0.0:
            planned_imports *= supplier_capacity[year + 1] / total_planned
        elif supplier_capacity[year + 1] == 0.0:
            planned_imports[:] = 0.0
        supplier_utilization[year + 1] = (
            float(planned_imports.sum()) / supplier_capacity[year + 1]
            if supplier_capacity[year + 1] > 0.0
            else 0.0
        )

        usable_inventory = inventory[year].copy()
        for index, name in enumerate(inputs):
            spec = config["residual_inputs"][name]
            requirement_multiplier = (
                float(programs[name]["remaining_requirement_multiplier"])
                if name in programs and substitution_validated[year + 1, index]
                else 1.0
            )
            shelf_life = float(spec["shelf_life_years"])
            shelf_hazard = 1.0 / shelf_life if shelf_life > 0.0 else 1.0
            loss_fraction = min(
                shelf_hazard
                + float(spec["obsolescence_per_year"])
                + float(spec["radiation_storage_loss_per_year"]),
                1.0,
            )
            usable_inventory[index] *= 1.0 - loss_fraction

            delivery[year + 1, index] = planned_imports[index] * (
                1.0 - float(spec["delivery_failure_fraction"])
            )
            usable_inventory[index] += delivery[year + 1, index]

            wave_interval = int(spec["replacement_wave_interval_years"])
            wave = (
                float(spec["replacement_wave_fraction"])
                if wave_interval > 0 and (year + 1) % wave_interval == 0
                else 0.0
            )
            replacement[year + 1, index] = (
                capacity[year]
                * float(spec["replacement_t_per_capacity_year"])
                * requirement_multiplier
                * (1.0 + wave)
            )

        replacement_served = np.minimum(
            usable_inventory,
            replacement[year + 1],
        )
        replacement_shortfall = replacement[year + 1] - replacement_served
        usable_inventory -= replacement_served
        losses: list[float] = []
        for index, name in enumerate(inputs):
            per_capacity = float(config["residual_inputs"][name]["replacement_t_per_capacity_year"])
            losses.append(
                replacement_shortfall[index] / per_capacity if per_capacity > 0.0 else 0.0
            )
        lost = min(max(losses, default=0.0), capacity[year])
        capacity_loss[year + 1] = lost
        surviving_capacity = capacity[year] - lost
        desired_addition = (
            surviving_capacity
            * growth_rate
            * (1.0 - allocation_fraction if eligible_programs else 1.0)
        )
        reserve_years = float(policy_cfg.get("stockpile_reserve_years", 0.0))
        if reserve_years < 0.0:
            raise ValueError("stockpile_reserve_years must be nonnegative")
        expansion_limits: list[float] = []
        for index, name in enumerate(inputs):
            mass_per_capacity = float(
                config["residual_inputs"][name]["commissioning_t_per_capacity"]
            )
            if name in programs and substitution_validated[year + 1, index]:
                mass_per_capacity *= float(programs[name]["remaining_requirement_multiplier"])
            inventory_available_for_expansion = max(
                usable_inventory[index] - reserve_years * replacement[year + 1, index],
                0.0,
            )
            expansion_limits.append(
                inventory_available_for_expansion / mass_per_capacity
                if mass_per_capacity > 0.0
                else math.inf
            )
        supported_addition = min(desired_addition, *expansion_limits)
        supported_addition = max(supported_addition, 0.0)
        if expansion_limits:
            binding_index = int(np.argmin(expansion_limits))
            if expansion_limits[binding_index] < desired_addition - 1e-12:
                binding[year + 1] = inputs[binding_index]
        for index, name in enumerate(inputs):
            commissioning[year + 1, index] = (
                supported_addition
                * float(config["residual_inputs"][name]["commissioning_t_per_capacity"])
                * (
                    float(programs[name]["remaining_requirement_multiplier"])
                    if name in programs and substitution_validated[year + 1, index]
                    else 1.0
                )
            )
        usable_inventory -= commissioning[year + 1]
        usable_inventory = np.maximum(usable_inventory, 0.0)
        inventory[year + 1] = usable_inventory
        capacity[year + 1] = surviving_capacity + supported_addition
        if first_stockout is None and (
            np.any(replacement_shortfall > 1e-12)
            or any(limit < desired_addition - 1e-12 for limit in expansion_limits)
        ):
            first_stockout = float(year + 1)

    return SupportedGrowthResult(
        policy=policy,
        t=t,
        capacity=capacity,
        inventory=inventory,
        external_delivery=delivery,
        replacement_demand=replacement,
        commissioning_demand=commissioning,
        capacity_loss=capacity_loss,
        binding_input=tuple(binding),
        first_stockout_year=first_stockout,
        substitution_effort=substitution_effort,
        substitution_validated=substitution_validated,
        substitution_failed=substitution_failed,
        supplier_capacity_t_per_year=supplier_capacity,
        supplier_utilization=supplier_utilization,
        supplier_binding_resource=tuple(supplier_binding),
    )
