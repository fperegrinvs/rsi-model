"""Dated, denominator-matched test of the SpaceXAI orbital-compute thesis.

The company-only case is intentionally allowed to remain non-computable.
The separately named hybrid completes its missing quantities with visible
ASSUMPTION-class values and never enters a probability distribution.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Final, cast

from .lco import AnchorSet, EarthLCO, SpaceLCO, lco_earth, lco_space
from .plotting_adapter import close_figure, single_axes, use_style

ROOT: Final = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE: Final = ROOT / "params" / "spacexai_economic_case.json"
TABLE_NAMES: Final[tuple[str, ...]] = (
    "spacexai_proponent_claim_crosswalk.csv",
    "spacexai_proponent_case.csv",
    "spacexai_proponent_hybrid.csv",
    "spacexai_economic_comparison.csv",
    "spacexai_time_to_useful_compute.csv",
    "spacexai_threshold_tornado.csv",
)
FIGURE_NAME: Final = "spacexai_threshold_tornado.png"
CASE_ORDER: Final[tuple[str, ...]] = (
    "earth_reference",
    "generic_model",
    "independent_reference",
    "spacexai_proponent_case",
    "spacexai_proponent_hybrid",
)


@dataclass(frozen=True, slots=True)
class WorkloadBoundary:
    """Frozen inference workload used to translate power-normalized cost."""

    workload_id: str
    model_boundary: str
    precision: str
    batch_size: int
    input_tokens_per_request: int
    output_tokens_per_request: int
    raw_requests_per_delivered_kwh: float
    quality_acceptance_fraction: float
    acceptance_rule: str
    earth_goodput: float
    generic_space_goodput: float
    independent_space_goodput: float
    hybrid_space_goodput: float

    @property
    def raw_output_tokens_per_delivered_kwh(self) -> float:
        return self.raw_requests_per_delivered_kwh * self.output_tokens_per_request


@dataclass(frozen=True, slots=True)
class ScheduleBoundary:
    """Capacity timing for one matched one-kW deployment."""

    delay_years: float
    ramp_years: float | None
    source_class: str
    note: str


@dataclass(frozen=True, slots=True)
class EconomicRegistry:
    """Validated projection of the JSON registry."""

    as_of: str
    currency_year: int
    forecast: Mapping[str, object]
    workload: WorkloadBoundary
    discount_rate: float
    schedules: Mapping[str, ScheduleBoundary]
    independent_mass_kg_per_kw: float
    independent_mass_range: tuple[float, float]
    independent_boundary: str
    company_quantities: tuple[Mapping[str, object], ...]
    hybrid_completions: tuple[Mapping[str, object], ...]


@dataclass(frozen=True, slots=True)
class EconomicCaseResult:
    """One commensurable economic result or an explicit missing-data result."""

    scenario_id: str
    label: str
    evidence_boundary: str
    result_status: str
    lco: float | None
    accepted_cost: float | None
    service_goodput: float | None
    first_useful_date: str | None
    schedule_key: str


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label}: expected object")
    return cast(Mapping[str, object], value)


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected non-empty string")
    return value


def _number(value: object, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label}: expected number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label}: expected finite number")
    return result


def _integer(value: object, label: str) -> int:
    result = _number(value, label)
    if not result.is_integer():
        raise ValueError(f"{label}: expected integer")
    return int(result)


def _fraction(value: object, label: str) -> float:
    result = _number(value, label)
    if not 0.0 < result <= 1.0:
        raise ValueError(f"{label}: expected value in (0, 1]")
    return result


def _schedule(value: object, label: str) -> ScheduleBoundary:
    raw = _mapping(value, label)
    delay = _number(raw.get("delayYears"), f"{label}.delayYears")
    ramp_raw = raw.get("rampYears")
    ramp = None if ramp_raw is None else _number(ramp_raw, f"{label}.rampYears")
    if delay < 0.0 or (ramp is not None and ramp <= 0.0):
        raise ValueError(f"{label}: delay must be nonnegative and ramp positive")
    return ScheduleBoundary(
        delay,
        ramp,
        _string(raw.get("sourceClass"), f"{label}.sourceClass"),
        _string(raw.get("note"), f"{label}.note"),
    )


def load_spacexai_economic_registry(source: Path = DEFAULT_SOURCE) -> EconomicRegistry:
    """Load the dated case registry and fail on stale source provenance."""
    raw = _mapping(json.loads(source.read_text(encoding="utf-8")), "registry")
    if _integer(raw.get("schemaVersion"), "schemaVersion") != 1:
        raise ValueError("schemaVersion must be 1")
    snapshot = ROOT / _string(raw.get("sourceSnapshot"), "sourceSnapshot")
    expected_hash = _string(raw.get("snapshotSha256"), "snapshotSha256")
    actual_hash = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        raise ValueError("SpaceXAI economic source snapshot hash mismatch")

    workload_raw = _mapping(raw.get("workload"), "workload")
    workload = WorkloadBoundary(
        workload_id=_string(workload_raw.get("workloadId"), "workload.workloadId"),
        model_boundary=_string(workload_raw.get("modelBoundary"), "workload.modelBoundary"),
        precision=_string(workload_raw.get("precision"), "workload.precision"),
        batch_size=_integer(workload_raw.get("batchSize"), "workload.batchSize"),
        input_tokens_per_request=_integer(
            workload_raw.get("inputTokensPerRequest"),
            "workload.inputTokensPerRequest",
        ),
        output_tokens_per_request=_integer(
            workload_raw.get("outputTokensPerRequest"),
            "workload.outputTokensPerRequest",
        ),
        raw_requests_per_delivered_kwh=_number(
            workload_raw.get("rawRequestsPerDeliveredKwh"),
            "workload.rawRequestsPerDeliveredKwh",
        ),
        quality_acceptance_fraction=_fraction(
            workload_raw.get("qualityAcceptanceFraction"),
            "workload.qualityAcceptanceFraction",
        ),
        acceptance_rule=_string(
            workload_raw.get("acceptanceRule"),
            "workload.acceptanceRule",
        ),
        earth_goodput=_fraction(
            workload_raw.get("earthServiceGoodputFraction"),
            "workload.earthServiceGoodputFraction",
        ),
        generic_space_goodput=_fraction(
            workload_raw.get("genericSpaceServiceGoodputFraction"),
            "workload.genericSpaceServiceGoodputFraction",
        ),
        independent_space_goodput=_fraction(
            workload_raw.get("independentSpaceServiceGoodputFraction"),
            "workload.independentSpaceServiceGoodputFraction",
        ),
        hybrid_space_goodput=_fraction(
            workload_raw.get("hybridSpaceServiceGoodputFraction"),
            "workload.hybridSpaceServiceGoodputFraction",
        ),
    )
    if (
        workload.batch_size <= 0
        or min(
            workload.input_tokens_per_request,
            workload.output_tokens_per_request,
            workload.raw_requests_per_delivered_kwh,
        )
        <= 0
    ):
        raise ValueError("workload counts and throughput must be positive")

    schedule_raw = _mapping(raw.get("schedule"), "schedule")
    schedules = {
        key: _schedule(schedule_raw.get(json_key), f"schedule.{json_key}")
        for key, json_key in (
            ("earth", "earth"),
            ("generic_space", "genericSpace"),
            ("independent_space", "independentSpace"),
            ("company_only", "companyOnly"),
            ("proponent_hybrid", "proponentHybrid"),
        )
    }
    independent = _mapping(raw.get("independentReference"), "independentReference")
    mass_range_raw = independent.get("massRangeKgPerKw")
    if not isinstance(mass_range_raw, list) or len(mass_range_raw) != 2:
        raise ValueError("independentReference.massRangeKgPerKw must have two values")
    mass_range_values = cast(list[object], mass_range_raw)
    mass_range = (
        _number(mass_range_values[0], "independentReference.massRangeKgPerKw[0]"),
        _number(mass_range_values[1], "independentReference.massRangeKgPerKw[1]"),
    )
    mass = _number(independent.get("massKgPerKw"), "independentReference.massKgPerKw")
    if not 0.0 < mass_range[0] <= mass <= mass_range[1]:
        raise ValueError("independent reference mass must lie inside its range")

    company_raw = raw.get("companyQuantities")
    hybrid_raw = raw.get("hybridCompletions")
    if not isinstance(company_raw, list) or not isinstance(hybrid_raw, list):
        raise ValueError("companyQuantities and hybridCompletions must be arrays")
    company_values = cast(list[object], company_raw)
    hybrid_values = cast(list[object], hybrid_raw)
    company = tuple(_mapping(item, "companyQuantities[]") for item in company_values)
    hybrid = tuple(_mapping(item, "hybridCompletions[]") for item in hybrid_values)
    company_ids = tuple(_string(item.get("quantityId"), "company quantityId") for item in company)
    hybrid_ids = tuple(_string(item.get("quantityId"), "hybrid quantityId") for item in hybrid)
    if len(set(company_ids)) != len(company_ids) or len(set(hybrid_ids)) != len(hybrid_ids):
        raise ValueError("economic quantity IDs must be unique within each case")
    missing = {
        "cost_per_token",
        "compute_hardware_capex",
        "useful_life",
        "compute_availability",
        "communications_goodput",
        "replacement_cost",
        "useful_capacity_ramp",
    }
    statuses = {
        _string(item.get("quantityId"), "company quantityId"): _string(
            item.get("status"),
            "company status",
        )
        for item in company
    }
    if any(statuses.get(quantity) != "not_disclosed" for quantity in missing):
        raise ValueError("company-only case must preserve every required undisclosed quantity")

    return EconomicRegistry(
        as_of=_string(raw.get("asOf"), "asOf"),
        currency_year=_integer(raw.get("currencyYear"), "currencyYear"),
        forecast=_mapping(raw.get("forecast"), "forecast"),
        workload=workload,
        discount_rate=_fraction(schedule_raw.get("discountRate"), "schedule.discountRate"),
        schedules=schedules,
        independent_mass_kg_per_kw=mass,
        independent_mass_range=mass_range,
        independent_boundary=_string(independent.get("boundary"), "independent.boundary"),
        company_quantities=company,
        hybrid_completions=hybrid,
    )


def accepted_tokens_per_kw_year(
    workload: WorkloadBoundary,
    service_goodput: float,
) -> float:
    """Accepted output tokens from one delivered kW-year of fixed inference."""
    if not 0.0 < service_goodput <= 1.0:
        raise ValueError("service_goodput must lie in (0, 1]")
    return (
        workload.raw_output_tokens_per_delivered_kwh
        * 8760.0
        * workload.quality_acceptance_fraction
        * service_goodput
    )


def accepted_cost_per_million(
    lco_per_kw_year: float,
    workload: WorkloadBoundary,
    service_goodput: float,
) -> float:
    """Convert LCO into dollars per million accepted inference output tokens."""
    return lco_per_kw_year / accepted_tokens_per_kw_year(workload, service_goodput) * 1_000_000.0


def _date_after_years(start: date, years: float) -> date:
    return start + timedelta(days=round(years * 365.2425))


def _years_between(start: date, end: date) -> float:
    return (end - start).days / 365.2425


def discounted_capacity_years(
    deadline_years: float,
    schedule: ScheduleBoundary,
    discount_rate: float,
) -> float | None:
    """Discounted available kW-years through a deadline for one-kW nameplate.

    A daily midpoint integration makes the schedule boundary transparent and
    stable while avoiding a hidden assumption that all ramped capacity appears
    at the end of a year.
    """
    if schedule.ramp_years is None:
        return None
    if deadline_years <= schedule.delay_years:
        return 0.0
    days = max(1, math.ceil(deadline_years * 365.2425))
    step = deadline_years / days
    total = 0.0
    for index in range(days):
        elapsed = (index + 0.5) * step
        if elapsed <= schedule.delay_years:
            capacity = 0.0
        else:
            capacity = min(1.0, (elapsed - schedule.delay_years) / schedule.ramp_years)
        total += capacity * (1.0 + discount_rate) ** -elapsed * step
    return total


def _case_results(registry: EconomicRegistry) -> tuple[EconomicCaseResult, ...]:
    workload = registry.workload
    earth = lco_earth("base")
    generic = lco_space("leo_inference")
    independent = lco_space(
        "leo_inference",
        total_mass_kg_per_kw=registry.independent_mass_kg_per_kw,
    )
    hybrid = lco_space("starmind_ai1_aspirational")
    statement_date = date.fromisoformat(
        _string(registry.forecast["statementDate"], "statementDate")
    )

    def result(
        scenario_id: str,
        label: str,
        boundary: str,
        model: EarthLCO | SpaceLCO,
        goodput: float,
        schedule_key: str,
    ) -> EconomicCaseResult:
        schedule = registry.schedules[schedule_key]
        return EconomicCaseResult(
            scenario_id,
            label,
            boundary,
            "computable_model_projection",
            model.lco,
            accepted_cost_per_million(model.lco, workload, goodput),
            goodput,
            _date_after_years(statement_date, schedule.delay_years).isoformat(),
            schedule_key,
        )

    return (
        result(
            "earth_reference",
            "Terrestrial reference",
            "Generic Earth base, held to the same 2026-USD lifecycle and fixed-inference boundary.",
            earth,
            workload.earth_goodput,
            "earth",
        ),
        result(
            "generic_model",
            "Generic orbital model",
            "Generic serviceable LEO model; all inputs retain their registered model classes.",
            generic,
            workload.generic_space_goodput,
            "generic_space",
        ),
        result(
            "independent_reference",
            "Independent conventional-mass reference",
            registry.independent_boundary,
            independent,
            workload.independent_space_goodput,
            "independent_space",
        ),
        EconomicCaseResult(
            "spacexai_proponent_case",
            "SpaceXAI company-only case",
            "Only dated company quantities; lifecycle cost and accepted-token "
            "cost remain non-computable.",
            "not_computable_missing_company_inputs",
            None,
            None,
            None,
            None,
            "company_only",
        ),
        result(
            "spacexai_proponent_hybrid",
            "SpaceXAI proponent hybrid",
            "Company targets plus separately registered independent/model "
            "ASSUMPTION completions; not a company estimate.",
            hybrid,
            workload.hybrid_space_goodput,
            "proponent_hybrid",
        ),
    )


def economic_comparison_rows(
    registry: EconomicRegistry,
) -> tuple[dict[str, object], ...]:
    """Return the denominator-matched, schedule-aware case comparison."""
    cases = _case_results(registry)
    earth = cases[0]
    if earth.lco is None or earth.accepted_cost is None:
        raise RuntimeError("the terrestrial reference must be computable")
    statement = date.fromisoformat(_string(registry.forecast["statementDate"], "statementDate"))
    earliest = date.fromisoformat(
        _string(registry.forecast["earliestBoundary"], "earliestBoundary")
    )
    latest = date.fromisoformat(_string(registry.forecast["latestBoundary"], "latestBoundary"))
    deadlines = (_years_between(statement, earliest), _years_between(statement, latest))
    rows: list[dict[str, object]] = []
    for index, case in enumerate(cases, 1):
        schedule = registry.schedules[case.schedule_key]
        discounted_years = tuple(
            discounted_capacity_years(deadline, schedule, registry.discount_rate)
            for deadline in deadlines
        )
        accepted_rate = (
            None
            if case.service_goodput is None
            else accepted_tokens_per_kw_year(registry.workload, case.service_goodput)
        )
        discounted_tokens = tuple(
            None if value is None or accepted_rate is None else value * accepted_rate
            for value in discounted_years
        )
        rows.append(
            {
                "scenario_order": index,
                "scenario_id": case.scenario_id,
                "label": case.label,
                "as_of": registry.as_of,
                "currency_year": registry.currency_year,
                "workload_id": registry.workload.workload_id,
                "result_status": case.result_status,
                "evidence_boundary": case.evidence_boundary,
                "lco_usd_per_frontier_equivalent_kw_year": case.lco,
                "lco_ratio_to_earth": None if case.lco is None else case.lco / earth.lco,
                "accepted_output_cost_usd_per_million_tokens": case.accepted_cost,
                "accepted_output_cost_ratio_to_earth": (
                    None if case.accepted_cost is None else case.accepted_cost / earth.accepted_cost
                ),
                "service_goodput_fraction": case.service_goodput,
                "first_useful_compute_date": case.first_useful_date,
                "ramp_years": schedule.ramp_years,
                "discounted_accepted_tokens_through_2028_01_22": discounted_tokens[0],
                "discounted_accepted_tokens_through_2029_01_22": discounted_tokens[1],
                "forecast_window_status": (
                    "not_computable_missing_commissioning_and_ramp"
                    if discounted_tokens[1] is None
                    else (
                        "cost_parity_not_reached"
                        if case.scenario_id == "spacexai_proponent_hybrid"
                        and case.accepted_cost is not None
                        and case.accepted_cost > earth.accepted_cost
                        else "comparison_value"
                    )
                ),
            }
        )
    return tuple(rows)


def schedule_rows(registry: EconomicRegistry) -> tuple[dict[str, object], ...]:
    """Expose construction/launch/commissioning/ramp timing without hiding gaps."""
    comparison = {str(row["scenario_id"]): row for row in economic_comparison_rows(registry)}
    rows: list[dict[str, object]] = []
    for index, scenario_id in enumerate(CASE_ORDER, 1):
        row = comparison[scenario_id]
        case = _case_results(registry)[index - 1]
        schedule = registry.schedules[case.schedule_key]
        rows.append(
            {
                "scenario_order": index,
                "scenario_id": scenario_id,
                "schedule_source_class": schedule.source_class,
                "delay_from_2026_01_22_years": schedule.delay_years,
                "first_useful_compute_date": row["first_useful_compute_date"],
                "useful_capacity_ramp_years": schedule.ramp_years,
                "discount_rate": registry.discount_rate,
                "discounted_accepted_tokens_through_2028_01_22": row[
                    "discounted_accepted_tokens_through_2028_01_22"
                ],
                "discounted_accepted_tokens_through_2029_01_22": row[
                    "discounted_accepted_tokens_through_2029_01_22"
                ],
                "schedule_note": schedule.note,
            }
        )
    return tuple(rows)


def _hybrid_metrics(
    registry: EconomicRegistry,
    *,
    launch_price: float = 185.0,
    mass_kg_per_kw: float = 10.0,
    qualification: float = 1.2,
    life_years: float = 7.0,
    utilization: float = 0.95,
    communications_capex: float | None = None,
    hardware_capex: float | None = None,
    space_wacc: float | None = None,
    service_goodput: float | None = None,
    delay_years: float = 2.0,
    ramp_years: float = 0.75,
) -> tuple[float, float, float]:
    overrides = {
        "aspirations.starship_leo_cost_per_kg": launch_price,
        "aspirations.starmind_vehicle_mass_kg_per_average_kw": mass_kg_per_kw,
        "aspirations.starmind_qualification_multiplier": qualification,
        "aspirations.starmind_life_years": life_years,
        "aspirations.starmind_utilization": utilization,
    }
    if communications_capex is not None:
        overrides["space_cost_completion.communications_capex_per_kw"] = communications_capex
    if hardware_capex is not None:
        overrides["compute.hw_per_kw_it"] = hardware_capex
    if space_wacc is not None:
        overrides["space_cost_completion.wacc"] = space_wacc
    space = lco_space("starmind_ai1_aspirational", a=AnchorSet(overrides=overrides))
    earth = lco_earth("base")
    goodput = registry.workload.hybrid_space_goodput if service_goodput is None else service_goodput
    earth_token_cost = accepted_cost_per_million(
        earth.lco,
        registry.workload,
        registry.workload.earth_goodput,
    )
    space_token_cost = accepted_cost_per_million(space.lco, registry.workload, goodput)
    statement = date.fromisoformat(_string(registry.forecast["statementDate"], "statementDate"))
    latest = date.fromisoformat(_string(registry.forecast["latestBoundary"], "latestBoundary"))
    deadline = _years_between(statement, latest)
    capacity_years = discounted_capacity_years(
        deadline,
        ScheduleBoundary(delay_years, ramp_years, "ASSUMPTION", "sensitivity"),
        registry.discount_rate,
    )
    earth_capacity_years = discounted_capacity_years(
        deadline,
        registry.schedules["earth"],
        registry.discount_rate,
    )
    if capacity_years is None or earth_capacity_years is None:
        raise RuntimeError("hybrid and terrestrial schedules must be computable")
    output_ratio = (
        capacity_years
        * accepted_tokens_per_kw_year(registry.workload, goodput)
        / (
            earth_capacity_years
            * accepted_tokens_per_kw_year(registry.workload, registry.workload.earth_goodput)
        )
    )
    return space.lco / earth.lco, space_token_cost / earth_token_cost, output_ratio


@dataclass(frozen=True, slots=True)
class SensitivityAxis:
    parameter: str
    unit: str
    low: float
    base: float
    high: float
    favorable: str
    controls_forecast_window: bool


SENSITIVITY_AXES: Final[tuple[SensitivityAxis, ...]] = (
    SensitivityAxis("launch_price", "2026 USD/kg", 0.0, 185.0, 3000.0, "low", False),
    SensitivityAxis("mass_kg_per_kw", "kg/kW", 5.0, 10.0, 20.0, "low", False),
    SensitivityAxis("qualification", "multiple", 1.0, 1.2, 3.0, "low", False),
    SensitivityAxis("life_years", "years", 3.0, 7.0, 10.0, "high", False),
    SensitivityAxis("utilization", "fraction", 0.65, 0.95, 0.99, "high", False),
    SensitivityAxis(
        "communications_capex",
        "2026 USD/kW",
        0.0,
        1581.1388300841897,
        5000.0,
        "low",
        False,
    ),
    SensitivityAxis(
        "hardware_capex",
        "2026 USD/kW",
        20000.0,
        33541.019662496845,
        45000.0,
        "low",
        False,
    ),
    SensitivityAxis("space_wacc", "fraction", 0.08, 0.14832396974191325, 0.22, "low", False),
    SensitivityAxis("service_goodput", "fraction", 0.5, 0.85, 1.0, "high", False),
    SensitivityAxis("delay_years", "years", 1.75, 2.0, 3.5, "low", True),
    SensitivityAxis("ramp_years", "years", 0.25, 0.75, 2.0, "low", True),
)


def _axis_metrics(
    registry: EconomicRegistry,
    axis: SensitivityAxis,
    value: float,
) -> tuple[float, float, float]:
    return _hybrid_metrics(registry, **{axis.parameter: value})


def _threshold(
    registry: EconomicRegistry,
    axis: SensitivityAxis,
    metric_index: int,
    target: float,
) -> float | None:
    left, right = axis.low, axis.high
    f_left = _axis_metrics(registry, axis, left)[metric_index] - target
    f_right = _axis_metrics(registry, axis, right)[metric_index] - target
    if f_left == 0.0:
        return left
    if f_right == 0.0:
        return right
    if f_left * f_right > 0.0:
        return None
    for _ in range(60):
        midpoint = (left + right) / 2.0
        f_mid = _axis_metrics(registry, axis, midpoint)[metric_index] - target
        if abs(f_mid) < 1e-10:
            return midpoint
        if f_left * f_mid <= 0.0:
            right = midpoint
        else:
            left = midpoint
            f_left = f_mid
    return (left + right) / 2.0


def threshold_tornado_rows(
    registry: EconomicRegistry,
) -> tuple[dict[str, object], ...]:
    """Return one-at-a-time ranges plus one explicitly joint favorable corner."""
    rows: list[dict[str, object]] = []
    for order, axis in enumerate(SENSITIVITY_AXES, 1):
        low = _axis_metrics(registry, axis, axis.low)
        base = _axis_metrics(registry, axis, axis.base)
        high = _axis_metrics(registry, axis, axis.high)
        rows.append(
            {
                "sensitivity_order": order,
                "parameter": axis.parameter,
                "unit": axis.unit,
                "scope": "one_at_a_time",
                "favorable_direction": axis.favorable,
                "low_value": axis.low,
                "base_value": axis.base,
                "high_value": axis.high,
                "lco_ratio_at_low": low[0],
                "lco_ratio_at_base": base[0],
                "lco_ratio_at_high": high[0],
                "accepted_token_ratio_at_low": low[1],
                "accepted_token_ratio_at_base": base[1],
                "accepted_token_ratio_at_high": high[1],
                "discounted_output_ratio_at_low": low[2],
                "discounted_output_ratio_at_base": base[2],
                "discounted_output_ratio_at_high": high[2],
                "lco_parity_threshold": _threshold(registry, axis, 0, 1.0),
                "accepted_token_parity_threshold": _threshold(registry, axis, 1, 1.0),
                "forecast_output_parity_threshold": _threshold(registry, axis, 2, 1.0),
                "controls_2028_2029_window": axis.controls_forecast_window,
                "interpretation": (
                    "Schedule controls useful output inside the forecast window "
                    "but does not change steady-state LCO."
                    if axis.controls_forecast_window
                    else "Steady-state economic sensitivity; all unvaried terms "
                    "remain at the proponent-hybrid boundary."
                ),
            }
        )
    joint = _hybrid_metrics(
        registry,
        launch_price=0.0,
        mass_kg_per_kw=5.0,
        qualification=1.0,
        life_years=10.0,
        utilization=0.99,
        communications_capex=0.0,
        hardware_capex=20000.0,
        space_wacc=0.08,
        service_goodput=1.0,
        delay_years=1.75,
        ramp_years=0.25,
    )
    rows.append(
        {
            "sensitivity_order": len(rows) + 1,
            "parameter": "simultaneous_favorable_boundary",
            "unit": "registered joint corner",
            "scope": "joint_not_probability",
            "favorable_direction": "all",
            "low_value": None,
            "base_value": None,
            "high_value": None,
            "lco_ratio_at_low": None,
            "lco_ratio_at_base": joint[0],
            "lco_ratio_at_high": None,
            "accepted_token_ratio_at_low": None,
            "accepted_token_ratio_at_base": joint[1],
            "accepted_token_ratio_at_high": None,
            "discounted_output_ratio_at_low": None,
            "discounted_output_ratio_at_base": joint[2],
            "discounted_output_ratio_at_high": None,
            "lco_parity_threshold": None,
            "accepted_token_parity_threshold": None,
            "forecast_output_parity_threshold": None,
            "controls_2028_2029_window": True,
            "interpretation": "All favorable endpoints applied simultaneously; "
            "deterministic boundary, not a likelihood or company estimate.",
        }
    )
    return tuple(rows)


def claim_crosswalk_rows() -> tuple[dict[str, str], ...]:
    """Map the strongest proponent claims to observables and current evidence."""
    return (
        {
            "claim_order": "1",
            "proponent_claim": "Near-continuous orbital solar lowers the energy term.",
            "source_ref": "S37;S38;S102",
            "model_term": "energy; utilization; power overhead",
            "required_observable": (
                "Delivered annual IT kWh, solar degradation, conversion losses, "
                "eclipse duty, and achieved compute availability."
            ),
            "current_result": (
                "Direction accepted; AI1 nameplate values are disclosed, but "
                "achieved availability and full energy cost are not."
            ),
        },
        {
            "claim_order": "2",
            "proponent_claim": "Radiative rejection can reduce cooling-power overhead.",
            "source_ref": "S38",
            "model_term": "radiator mass/capex; pumping load; thermal margin",
            "required_observable": (
                "Sustained heat rejection, coolant and junction temperatures, "
                "full-loop mass, parasitic power, degradation, and failures."
            ),
            "current_result": (
                "110 m² is disclosed; full thermal performance, mass, power, "
                "cost, and life are not."
            ),
        },
        {
            "claim_order": "3",
            "proponent_claim": "Reusable launch lowers deployment cost.",
            "source_ref": "S37;S102",
            "model_term": "launch USD/kg; cadence; vehicle depreciation",
            "required_observable": (
                "Achieved reusable payload, fully allocated cost/kg, turnaround, "
                "fleet size, reliability, and licensed cadence."
            ),
            "current_result": (
                "$185/kg is a target-derived ceiling; the SEC response says "
                "launch asset depreciation remains part of satellite cost."
            ),
        },
        {
            "claim_order": "4",
            "proponent_claim": "Scaled satellite manufacturing lowers spacecraft cost.",
            "source_ref": "S37;S38",
            "model_term": "manufacturing and spacecraft-bus capex",
            "required_observable": (
                "Recurring factory cost per delivered kW, yield, throughput, "
                "NRE allocation, and acceptance-test cost."
            ),
            "current_result": (
                "Factory scale is stated; no comparable manufacturing cost or yield is disclosed."
            ),
        },
        {
            "claim_order": "5",
            "proponent_claim": "High kW/t reduces launch mass.",
            "source_ref": "S37;S38;S39",
            "model_term": "kg per delivered kW",
            "required_observable": (
                "As-flown mass divided by sustained average delivered IT kW at "
                "equal service quality."
            ),
            "current_result": (
                "AI1 states 70 kW/t and the long-run filing uses 100 kW/t; an "
                "independent conventional study gives 34–59 kg/kW."
            ),
        },
        {
            "claim_order": "6",
            "proponent_claim": "Proprietary chips reduce hardware cost and depreciation.",
            "source_ref": "S37;S102",
            "model_term": "qualified hardware capex; refresh life; efficiency",
            "required_observable": (
                "Qualified accelerator cost, useful FLOP/s or accepted tokens "
                "per watt, yield, failure rate, and economic refresh life."
            ),
            "current_result": (
                "Compute depreciation is identified as the largest component; "
                "no comparable value or achieved chip trajectory is disclosed."
            ),
        },
        {
            "claim_order": "7",
            "proponent_claim": "Orbital hardware remains useful long enough to amortize.",
            "source_ref": "S38",
            "model_term": "hardware and infrastructure life",
            "required_observable": (
                "Cohort survival, radiation faults, degradation, repair, and "
                "economic retirement under the fixed workload."
            ),
            "current_result": (
                "AI1 life is not disclosed; seven years in the hybrid is an ASSUMPTION."
            ),
        },
        {
            "claim_order": "8",
            "proponent_claim": "Laser and Starlink links deliver useful output globally.",
            "source_ref": "S38",
            "model_term": "service goodput; communications capex; latency",
            "required_observable": (
                "Sustained application goodput, latency distribution, contention, "
                "outages, gateway capacity, and cost."
            ),
            "current_result": (
                "Link architecture is described; delivered application goodput and cost are not."
            ),
        },
        {
            "claim_order": "9",
            "proponent_claim": "Replacement and modular upgrades preserve value.",
            "source_ref": "S38",
            "model_term": "replacement launch; serviceability; residual value",
            "required_observable": (
                "Demonstrated payload exchange or repair, replacement "
                "mass/cadence, downtime, and recovered value."
            ),
            "current_result": (
                "Modularity is stated; no orbital repair, exchange, or AI1 "
                "replacement record is disclosed."
            ),
        },
        {
            "claim_order": "10",
            "proponent_claim": "Orbit reaches useful power faster than terrestrial projects.",
            "source_ref": "S37;S38;S103",
            "model_term": "production, launch, commissioning, and constellation ramp",
            "required_observable": (
                "Contract-to-service dates and accepted-output ramp for matched "
                "orbital and terrestrial deployments."
            ),
            "current_result": (
                "Possible initial deployment is stated for 2028; commissioning "
                "and useful-output ramp are missing."
            ),
        },
        {
            "claim_order": "11",
            "proponent_claim": "Terrestrial power scarcity widens the orbital advantage.",
            "source_ref": "S37",
            "model_term": "Earth power price, PUE, interconnection and construction schedule",
            "required_observable": (
                "Matched forward power, cooling, site, interconnection, "
                "construction, and financing trajectories."
            ),
            "current_result": (
                "The generic model tests tight/base/responsive Earth cases; "
                "SpaceX supplies no matched escalation path."
            ),
        },
        {
            "claim_order": "12",
            "proponent_claim": (
                "Space becomes the lowest-cost place for AI by January 2028–January 2029."
            ),
            "source_ref": "S103",
            "model_term": "full LCO and accepted-output cost ratios plus schedule",
            "required_observable": (
                "A frozen comparator, workload, quality boundary, full lifecycle "
                "bill, and commissioned accepted output by each deadline."
            ),
            "current_result": (
                "Company-only comparison is not computable; the registered hybrid "
                "remains above Earth on both steady-state denominators."
            ),
        },
    )


def _company_case_rows(registry: EconomicRegistry) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for order, item in enumerate(registry.company_quantities, 1):
        rows.append(
            {
                "quantity_order": order,
                "scenario_id": "spacexai_proponent_case",
                "as_of": registry.as_of,
                "quantity_id": item["quantityId"],
                "value": item.get("value"),
                "unit": item["unit"],
                "status": item["status"],
                "evidence_class": item["evidenceClass"],
                "source_ref": item["sourceRef"],
                "note": item["note"],
            }
        )
    return tuple(rows)


def _hybrid_case_rows(registry: EconomicRegistry) -> tuple[dict[str, object], ...]:
    company = {str(item["quantityId"]): item for item in registry.company_quantities}
    completions = {str(item["quantityId"]): item for item in registry.hybrid_completions}
    quantity_ids = tuple(company) + tuple(key for key in completions if key not in company)
    rows: list[dict[str, object]] = []
    for order, quantity_id in enumerate(quantity_ids, 1):
        company_item = company.get(quantity_id)
        completion = completions.get(quantity_id)
        if company_item is not None and company_item.get("value") is not None:
            selected = company_item
            value = selected["value"]
            evidence = selected["evidenceClass"]
            source = selected["sourceRef"]
            status = selected["status"]
            note = selected["note"]
            unit = selected["unit"]
        elif completion is not None:
            value = completion["value"]
            evidence = completion["evidenceClass"]
            source = completion["source"]
            status = "explicit_gap_completion"
            note = "Not disclosed by SpaceX; selected only for the named hybrid."
            unit = completion["unit"]
        else:
            if company_item is None:
                raise RuntimeError(f"missing company quantity {quantity_id}")
            value = None
            evidence = company_item["evidenceClass"]
            source = company_item["sourceRef"]
            status = company_item["status"]
            note = company_item["note"]
            unit = company_item["unit"]
        rows.append(
            {
                "quantity_order": order,
                "scenario_id": "spacexai_proponent_hybrid",
                "as_of": registry.as_of,
                "quantity_id": quantity_id,
                "selected_value": value,
                "unit": unit,
                "selection_status": status,
                "evidence_class": evidence,
                "source_or_model_anchor": source,
                "note": note,
            }
        )
    return tuple(rows)


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError(f"{path.name}: cannot write empty table")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = tuple(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            if tuple(row) != fields:
                raise ValueError(f"{path.name}: inconsistent row schema")
            writer.writerow({key: "" if value is None else value for key, value in row.items()})


def _write_tornado_figure(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    data = [row for row in rows if row["scope"] == "one_at_a_time"]
    ordered = sorted(
        data,
        key=lambda row: abs(
            _number(row["accepted_token_ratio_at_high"], "accepted ratio high")
            - _number(row["accepted_token_ratio_at_low"], "accepted ratio low")
        ),
    )
    labels = [str(row["parameter"]).replace("_", " ") for row in ordered]
    lows = [
        min(
            _number(row["accepted_token_ratio_at_low"], "accepted ratio low"),
            _number(row["accepted_token_ratio_at_high"], "accepted ratio high"),
        )
        for row in ordered
    ]
    highs = [
        max(
            _number(row["accepted_token_ratio_at_low"], "accepted ratio low"),
            _number(row["accepted_token_ratio_at_high"], "accepted ratio high"),
        )
        for row in ordered
    ]
    bases = [_number(row["accepted_token_ratio_at_base"], "accepted ratio base") for row in ordered]
    use_style("seaborn-v0_8-whitegrid")
    fig, ax = single_axes(figsize=(9.2, 6.4))
    positions = list(range(len(ordered)))
    for position, low, high, base in zip(positions, lows, highs, bases, strict=True):
        ax.hlines(position, low, high, color="#28536b", linewidth=7)
        ax.plot(base, position, marker="D", color="#b23a48", markersize=5)
    ax.axvline(1.0, color="#111111", linestyle="--", linewidth=1.2, label="Earth parity")
    ax.set_yticks(positions, labels=labels)
    ax.set_xlabel("Space / Earth cost per accepted output token")
    ax.set_title("SpaceXAI proponent-hybrid one-at-a-time sensitivity")
    ax.legend(loc="lower right")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    close_figure(fig)


def write_spacexai_economic_artifacts(
    table_directory: Path,
    figure_directory: Path,
    source: Path = DEFAULT_SOURCE,
) -> tuple[Path, ...]:
    """Validate and write every dated SpaceXAI economic artifact."""
    registry = load_spacexai_economic_registry(source)
    outputs = tuple(table_directory / name for name in TABLE_NAMES)
    rows_by_name: tuple[Sequence[Mapping[str, object]], ...] = (
        claim_crosswalk_rows(),
        _company_case_rows(registry),
        _hybrid_case_rows(registry),
        economic_comparison_rows(registry),
        schedule_rows(registry),
        threshold_tornado_rows(registry),
    )
    for path, rows in zip(outputs, rows_by_name, strict=True):
        _write_csv(path, rows)
    figure = figure_directory / FIGURE_NAME
    _write_tornado_figure(figure, rows_by_name[-1])
    return (*outputs, figure)


__all__ = [
    "CASE_ORDER",
    "DEFAULT_SOURCE",
    "FIGURE_NAME",
    "TABLE_NAMES",
    "EconomicRegistry",
    "ScheduleBoundary",
    "WorkloadBoundary",
    "accepted_cost_per_million",
    "accepted_tokens_per_kw_year",
    "claim_crosswalk_rows",
    "discounted_capacity_years",
    "economic_comparison_rows",
    "load_spacexai_economic_registry",
    "schedule_rows",
    "threshold_tornado_rows",
    "write_spacexai_economic_artifacts",
]
