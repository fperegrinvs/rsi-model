"""Validate and render the r4.0 economic-calibration data contract."""

from __future__ import annotations

import csv
import io
from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, TypedDict

from rsimodel.evidence import (
    SHA256_PLACEHOLDER,
    artifact_files_template,
    require_exact_ids,
    require_fields,
    require_list,
    require_mapping,
    require_nonnegative_number,
    require_sha256,
    require_string,
    required_field_template,
    verify_artifact_files,
)
from rsimodel.yaml_adapter import (
    load_yaml_mapping,
    require_string_sequence,
)
from rsimodel.yaml_adapter import (
    require_mapping as require_yaml_mapping,
)
from rsimodel.yaml_adapter import (
    require_string as require_yaml_string,
)

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = ROOT / "params" / "economic_calibration.yaml"
ANCHORS_PATH = ROOT / "params" / "anchors.yaml"
INTEGRATED_PATH = ROOT / "params" / "integrated_model.yaml"


class ArchitectureCaseSettings(TypedDict):
    description: str
    model_cases: tuple[str, ...]
    required_evidence: tuple[str, ...]


class EvidencePackageSettings(TypedDict):
    purpose: str
    required_fields: tuple[str, ...]
    model_bindings: tuple[str, ...]
    readiness: str


class CorrelationGroupSettings(TypedDict):
    rationale: str
    members: tuple[str, ...]


class CashFlowEventSchemaSettings(TypedDict):
    common_required_fields: tuple[str, ...]
    event_types: Mapping[str, tuple[str, ...]]


class CalibrationPlanSettings(TypedDict):
    unit_of_observation: str
    calibration_split: str
    validation_split: str
    external_validation: str
    missingness: str
    censoring: str
    estimation: str
    sensitivity: str


class PromotionRuleSettings(TypedDict):
    required: tuple[str, ...]
    decision: str


class EconomicCalibrationProtocol(TypedDict):
    version: str
    protocol_id: str
    status: str
    source_class: str
    epistemic_status: str
    objective: str
    architecture_cases: Mapping[str, ArchitectureCaseSettings]
    evidence_packages: Mapping[str, EvidencePackageSettings]
    correlation_groups: Mapping[str, CorrelationGroupSettings]
    cash_flow_event_schema: CashFlowEventSchemaSettings
    calibration_plan: CalibrationPlanSettings
    promotion_rule: PromotionRuleSettings
    execution_outputs_required: tuple[str, ...]


class RecordParser[Record](Protocol):
    def __call__(self, value: object, *, label: str) -> Record: ...


def _named_records[Record](
    value: object,
    *,
    label: str,
    parser: RecordParser[Record],
) -> dict[str, Record]:
    source = require_yaml_mapping(value, label=label)
    return {name: parser(record, label=f"{label}.{name}") for name, record in source.items()}


def _architecture_case(value: object, *, label: str) -> ArchitectureCaseSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "description": require_yaml_string(
            record.get("description"),
            label=f"{label}.description",
        ),
        "model_cases": require_string_sequence(
            record.get("model_cases"),
            label=f"{label}.model_cases",
        ),
        "required_evidence": require_string_sequence(
            record.get("required_evidence"),
            label=f"{label}.required_evidence",
        ),
    }


def _evidence_package(value: object, *, label: str) -> EvidencePackageSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "purpose": require_yaml_string(record.get("purpose"), label=f"{label}.purpose"),
        "required_fields": require_string_sequence(
            record.get("required_fields"),
            label=f"{label}.required_fields",
        ),
        "model_bindings": require_string_sequence(
            record.get("model_bindings"),
            label=f"{label}.model_bindings",
        ),
        "readiness": require_yaml_string(
            record.get("readiness"),
            label=f"{label}.readiness",
        ),
    }


def _correlation_group(value: object, *, label: str) -> CorrelationGroupSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "rationale": require_yaml_string(
            record.get("rationale"),
            label=f"{label}.rationale",
        ),
        "members": require_string_sequence(
            record.get("members"),
            label=f"{label}.members",
        ),
    }


def _cash_flow_schema(value: object, *, label: str) -> CashFlowEventSchemaSettings:
    record = require_yaml_mapping(value, label=label)
    event_source = require_yaml_mapping(
        record.get("event_types"),
        label=f"{label}.event_types",
    )
    return {
        "common_required_fields": require_string_sequence(
            record.get("common_required_fields"),
            label=f"{label}.common_required_fields",
        ),
        "event_types": {
            event_type: require_string_sequence(
                fields,
                label=f"{label}.event_types.{event_type}",
            )
            for event_type, fields in event_source.items()
        },
    }


def _calibration_plan(value: object, *, label: str) -> CalibrationPlanSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "unit_of_observation": require_yaml_string(
            record.get("unit_of_observation"),
            label=f"{label}.unit_of_observation",
        ),
        "calibration_split": require_yaml_string(
            record.get("calibration_split"),
            label=f"{label}.calibration_split",
        ),
        "validation_split": require_yaml_string(
            record.get("validation_split"),
            label=f"{label}.validation_split",
        ),
        "external_validation": require_yaml_string(
            record.get("external_validation"),
            label=f"{label}.external_validation",
        ),
        "missingness": require_yaml_string(
            record.get("missingness"),
            label=f"{label}.missingness",
        ),
        "censoring": require_yaml_string(
            record.get("censoring"),
            label=f"{label}.censoring",
        ),
        "estimation": require_yaml_string(
            record.get("estimation"),
            label=f"{label}.estimation",
        ),
        "sensitivity": require_yaml_string(
            record.get("sensitivity"),
            label=f"{label}.sensitivity",
        ),
    }


def _promotion_rule(value: object, *, label: str) -> PromotionRuleSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "required": require_string_sequence(
            record.get("required"),
            label=f"{label}.required",
        ),
        "decision": require_yaml_string(
            record.get("decision"),
            label=f"{label}.decision",
        ),
    }


def load_economic_calibration(
    path: Path | None = None,
) -> EconomicCalibrationProtocol:
    """Load and structurally validate the economic calibration protocol."""
    raw = load_yaml_mapping(path or PROTOCOL_PATH)
    return {
        "version": require_yaml_string(
            raw.get("version"),
            label="economic_calibration.version",
        ),
        "protocol_id": require_yaml_string(
            raw.get("protocol_id"),
            label="economic_calibration.protocol_id",
        ),
        "status": require_yaml_string(
            raw.get("status"),
            label="economic_calibration.status",
        ),
        "source_class": require_yaml_string(
            raw.get("source_class"),
            label="economic_calibration.source_class",
        ),
        "epistemic_status": require_yaml_string(
            raw.get("epistemic_status"),
            label="economic_calibration.epistemic_status",
        ),
        "objective": require_yaml_string(
            raw.get("objective"),
            label="economic_calibration.objective",
        ),
        "architecture_cases": _named_records(
            raw.get("architecture_cases"),
            label="economic_calibration.architecture_cases",
            parser=_architecture_case,
        ),
        "evidence_packages": _named_records(
            raw.get("evidence_packages"),
            label="economic_calibration.evidence_packages",
            parser=_evidence_package,
        ),
        "correlation_groups": _named_records(
            raw.get("correlation_groups"),
            label="economic_calibration.correlation_groups",
            parser=_correlation_group,
        ),
        "cash_flow_event_schema": _cash_flow_schema(
            raw.get("cash_flow_event_schema"),
            label="economic_calibration.cash_flow_event_schema",
        ),
        "calibration_plan": _calibration_plan(
            raw.get("calibration_plan"),
            label="economic_calibration.calibration_plan",
        ),
        "promotion_rule": _promotion_rule(
            raw.get("promotion_rule"),
            label="economic_calibration.promotion_rule",
        ),
        "execution_outputs_required": require_string_sequence(
            raw.get("execution_outputs_required"),
            label="economic_calibration.execution_outputs_required",
        ),
    }


def _path_exists(tree: Mapping[str, object], dotted: str) -> bool:
    node: object = tree
    for component in dotted.split("."):
        try:
            mapping = require_yaml_mapping(node, label=dotted)
        except ValueError:
            return False
        if component not in mapping:
            return False
        node = mapping[component]
    return True


def validate_economic_calibration(
    protocol: EconomicCalibrationProtocol | None = None,
) -> None:
    """Reject coverage gaps, invented readiness, and stale model bindings."""
    if protocol is None:
        protocol = load_economic_calibration()
    errors: list[str] = []

    if protocol.get("status") != ("data_contract_ready_empirical_calibration_pending"):
        errors.append("status must keep empirical calibration pending")
    if protocol.get("source_class") != "ASSUMPTION":
        errors.append("protocol must remain ASSUMPTION-class")

    architectures = protocol["architecture_cases"]
    required_architectures = {
        "earth_reference",
        "serviceable_space_platform",
        "integrated_disposable_ai1",
    }
    if set(architectures) != required_architectures:
        errors.append("architecture cases must cover the three declared boundaries")

    packages = protocol["evidence_packages"]
    for package_id, package in packages.items():
        errors.extend(
            f"{package_id}: missing {field}"
            for field in ("purpose", "required_fields", "model_bindings")
            if not package.get(field)
        )
        if package.get("readiness") != "data_pending":
            errors.append(f"{package_id}: readiness must be data_pending")
    for architecture, config in architectures.items():
        unknown = set(config["required_evidence"]) - set(packages)
        if unknown:
            errors.append(f"{architecture}: unknown evidence packages {sorted(unknown)}")
        if not config["model_cases"]:
            errors.append(f"{architecture}: model_cases is empty")

    anchors = load_yaml_mapping(ANCHORS_PATH)
    integrated = load_yaml_mapping(INTEGRATED_PATH)
    all_bindings = {
        binding for package in packages.values() for binding in package["model_bindings"]
    }
    all_bindings |= {
        binding for group in protocol["correlation_groups"].values() for binding in group["members"]
    }
    for binding in all_bindings:
        tree = integrated if binding.startswith("dynamic_economics.") else anchors
        if not _path_exists(tree, binding):
            errors.append(f"stale or unknown model binding {binding}")

    groups = protocol["correlation_groups"]
    if len(groups) < 5:
        errors.append("at least five correlation groups are required")
    for group_id, group in groups.items():
        if not group.get("rationale"):
            errors.append(f"{group_id}: missing rationale")
        if len(group["members"]) < 2:
            errors.append(f"{group_id}: fewer than two correlated members")

    event_schema = protocol["cash_flow_event_schema"]
    common = set(event_schema["common_required_fields"])
    required_common = {
        "event_id",
        "project_id",
        "architecture_case",
        "event_time",
        "source_document_hash",
        "nominal_currency",
        "price_base_date",
        "amount",
        "quantity_and_units",
    }
    if common != required_common:
        errors.append("cash-flow common fields are incomplete or unexpected")
    required_events = {
        "capex_commitment",
        "construction_payment",
        "launch_or_transfer",
        "commissioning",
        "operation",
        "failure_and_repair",
        "insurance",
        "financing",
        "regulatory",
        "retirement_disposal",
        "earth_resource",
    }
    if set(event_schema["event_types"]) != required_events:
        errors.append("cash-flow event types are incomplete or unexpected")

    plan = protocol["calibration_plan"]
    errors.extend(
        f"calibration plan missing {field}"
        for field in (
            "calibration_split",
            "validation_split",
            "external_validation",
            "missingness",
            "censoring",
            "estimation",
            "sensitivity",
        )
        if not plan.get(field)
    )

    promotion = protocol["promotion_rule"]
    if len(promotion["required"]) < 8 or not promotion["decision"]:
        errors.append("assumption-promotion rule is incomplete")

    if errors:
        raise ValueError("invalid economic calibration protocol:\n- " + "\n- ".join(errors))


def render_economic_calibration_csv(
    protocol: EconomicCalibrationProtocol | None = None,
) -> str:
    """Render the evidence queue without implying that data were collected."""
    if protocol is None:
        protocol = load_economic_calibration()
    validate_economic_calibration(protocol)
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(
        [
            "record_type",
            "id",
            "scope_or_purpose",
            "required_fields_or_members",
            "model_bindings_or_cases",
            "readiness",
        ]
    )
    for case_id, case in protocol["architecture_cases"].items():
        writer.writerow(
            [
                "architecture_case",
                case_id,
                case["description"],
                "; ".join(case["required_evidence"]),
                "; ".join(case["model_cases"]),
                "data_pending",
            ]
        )
    for package_id, package in protocol["evidence_packages"].items():
        writer.writerow(
            [
                "evidence_package",
                package_id,
                package["purpose"],
                "; ".join(package["required_fields"]),
                "; ".join(package["model_bindings"]),
                package["readiness"],
            ]
        )
    for group_id, group in protocol["correlation_groups"].items():
        writer.writerow(
            [
                "correlation_group",
                group_id,
                group["rationale"],
                "; ".join(group["members"]),
                "joint or hierarchical fit with held-out validation",
                "data_pending",
            ]
        )
    for event_id, required_fields in protocol["cash_flow_event_schema"]["event_types"].items():
        writer.writerow(
            [
                "cash_flow_event",
                event_id,
                "audited dated project event",
                "; ".join(required_fields),
                "; ".join(protocol["cash_flow_event_schema"]["common_required_fields"]),
                "data_pending",
            ]
        )
    return stream.getvalue()


def write_economic_calibration_csv(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_economic_calibration_csv(), encoding="utf-8")
    return path


def economic_calibration_bundle_template(
    protocol: EconomicCalibrationProtocol | None = None,
) -> dict[str, object]:
    """Return an invalid-until-calibrated evidence release template."""
    if protocol is None:
        protocol = load_economic_calibration()
    validate_economic_calibration(protocol)

    packages: dict[str, object] = {}
    for package_id, package in protocol["evidence_packages"].items():
        packages[package_id] = {
            "normalized_records_sha256": SHA256_PLACEHOLDER,
            "records": [required_field_template(package["required_fields"])],
        }
    fits: dict[str, object] = {}
    for group_id, group in protocol["correlation_groups"].items():
        fits[group_id] = {
            "members": group["members"],
            "model": None,
            "calibration_period": None,
            "validation_period": None,
            "diagnostics": None,
            "holdout_status": None,
            "fit_query_sha256": SHA256_PLACEHOLDER,
        }
    events: list[dict[str, object]] = []
    common = protocol["cash_flow_event_schema"]["common_required_fields"]
    for index, (event_type, fields) in enumerate(
        protocol["cash_flow_event_schema"]["event_types"].items(),
        1,
    ):
        events.append(
            required_field_template(
                [*common, *fields],
                {
                    "event_id": f"CASH_EVENT_REPLACE_{index:03d}",
                    "event_type": event_type,
                },
            )
        )
    package_ids_by_binding: dict[str, list[str]] = {}
    for package_id, package in protocol["evidence_packages"].items():
        for binding in package["model_bindings"]:
            package_ids_by_binding.setdefault(binding, []).append(package_id)
    decisions: dict[str, object] = {
        binding: {
            "decision": None,
            "evidence_package_ids": package_ids,
            "estimate": None,
            "units": None,
            "uncertainty": None,
            "failed_and_censored_count": None,
            "holdout_result": None,
            "calibration_query_sha256": SHA256_PLACEHOLDER,
            "independent_review_status": None,
        }
        for binding, package_ids in sorted(package_ids_by_binding.items())
    }
    return {
        "template_status": "incomplete_do_not_submit",
        "protocol_id": protocol["protocol_id"],
        "archive_sha256": SHA256_PLACEHOLDER,
        "artifact_files": artifact_files_template(),
        "evidence_packages": packages,
        "correlation_fits": fits,
        "cash_flow_events": events,
        "promotion_decisions": decisions,
    }


def evaluate_economic_calibration_bundle(
    bundle: Mapping[str, object] | None,
    protocol: EconomicCalibrationProtocol | None = None,
    *,
    archive_root: Path | None = None,
) -> dict[str, object]:
    """Validate normalized records, correlation fits, and promotion decisions."""
    if protocol is None:
        protocol = load_economic_calibration()
    validate_economic_calibration(protocol)
    if not bundle:
        return {
            "overall_status": "empirical_calibration_pending",
            "evidence_package_status": dict.fromkeys(protocol["evidence_packages"], "data_pending"),
        }

    errors: list[str] = []
    if bundle.get("protocol_id") != protocol["protocol_id"]:
        errors.append("protocol_id does not match the r4.0 protocol")
    require_sha256(bundle, "archive_sha256", "bundle", errors)
    verify_artifact_files(bundle, archive_root, errors)

    packages = require_mapping(bundle.get("evidence_packages"), "evidence_packages", errors)
    require_exact_ids(
        packages,
        set(protocol["evidence_packages"]),
        "evidence_packages",
        errors,
    )
    for package_id, raw_submission in packages.items():
        submission = require_mapping(raw_submission, f"evidence_packages.{package_id}", errors)
        records = require_list(
            submission.get("records"),
            f"evidence_packages.{package_id}.records",
            errors,
        )
        if not records:
            errors.append(f"evidence_packages.{package_id}: records are empty")
            continue
        package_config = protocol["evidence_packages"].get(package_id)
        required = () if package_config is None else package_config["required_fields"]
        for index, raw_record in enumerate(records):
            record = require_mapping(
                raw_record,
                f"evidence_packages.{package_id}.records[{index}]",
                errors,
            )
            require_fields(
                record,
                required,
                f"evidence_packages.{package_id}.records[{index}]",
                errors,
            )
        require_sha256(
            submission,
            "normalized_records_sha256",
            f"evidence_packages.{package_id}",
            errors,
        )

    fits = require_mapping(bundle.get("correlation_fits"), "correlation_fits", errors)
    require_exact_ids(
        fits,
        set(protocol["correlation_groups"]),
        "correlation_fits",
        errors,
    )
    fit_statuses: dict[str, str] = {}
    for group_id, raw_fit in fits.items():
        fit = require_mapping(raw_fit, f"correlation_fits.{group_id}", errors)
        require_fields(
            fit,
            {
                "members",
                "model",
                "calibration_period",
                "validation_period",
                "diagnostics",
                "holdout_status",
                "fit_query_sha256",
            },
            f"correlation_fits.{group_id}",
            errors,
        )
        require_sha256(
            fit,
            "fit_query_sha256",
            f"correlation_fits.{group_id}",
            errors,
        )
        group_config = protocol["correlation_groups"].get(group_id)
        expected_members = set(() if group_config is None else group_config["members"])
        submitted_members = require_list(
            fit.get("members"),
            f"correlation_fits.{group_id}.members",
            errors,
        )
        if {str(member) for member in submitted_members} != expected_members:
            errors.append(f"correlation_fits.{group_id}: members do not match contract")
        holdout_status = require_string(
            fit,
            "holdout_status",
            f"correlation_fits.{group_id}",
            errors,
        )
        if holdout_status not in {"pass", "fail"}:
            errors.append(f"correlation_fits.{group_id}: holdout_status must be pass or fail")
        else:
            fit_statuses[group_id] = holdout_status

    schema = protocol["cash_flow_event_schema"]
    cash_events = require_list(bundle.get("cash_flow_events"), "cash_flow_events", errors)
    if not cash_events:
        errors.append("cash_flow_events: no events supplied")
    seen_events: set[str] = set()
    observed_event_types: set[str] = set()
    for index, raw_event in enumerate(cash_events):
        label = f"cash_flow_events[{index}]"
        event = require_mapping(raw_event, label, errors)
        event_type = require_string(event, "event_type", label, errors)
        if event_type is None or event_type not in schema["event_types"]:
            errors.append(f"{label}: unknown event_type {event_type}")
            continue
        require_fields(
            event,
            schema["common_required_fields"],
            label,
            errors,
        )
        require_fields(
            event,
            schema["event_types"][event_type],
            label,
            errors,
        )
        event_id = require_string(event, "event_id", label, errors)
        if event_id is None:
            continue
        if event_id in seen_events:
            errors.append(f"{label}: duplicate event_id {event_id}")
        seen_events.add(event_id)
        observed_event_types.add(event_type)
        require_sha256(event, "source_document_hash", label, errors)
        require_nonnegative_number(event, "amount", label, errors)
    missing_events = set(schema["event_types"]) - observed_event_types
    if missing_events:
        errors.append(f"cash_flow_events: missing event types {sorted(missing_events)}")

    all_bindings = {
        binding
        for package in protocol["evidence_packages"].values()
        for binding in package["model_bindings"]
    }
    decisions = require_mapping(bundle.get("promotion_decisions"), "promotion_decisions", errors)
    require_exact_ids(
        decisions,
        all_bindings,
        "promotion_decisions",
        errors,
    )
    promotion_statuses: dict[str, str] = {}
    all_promotions_reviewed = True
    for binding, raw_decision in decisions.items():
        decision = require_mapping(raw_decision, f"promotion_decisions.{binding}", errors)
        require_fields(
            decision,
            {
                "decision",
                "evidence_package_ids",
                "estimate",
                "units",
                "uncertainty",
                "failed_and_censored_count",
                "holdout_result",
                "calibration_query_sha256",
                "independent_review_status",
            },
            f"promotion_decisions.{binding}",
            errors,
        )
        require_sha256(
            decision,
            "calibration_query_sha256",
            f"promotion_decisions.{binding}",
            errors,
        )
        if decision.get("decision") not in {
            "retain_assumption",
            "promote_empirical",
        }:
            errors.append(f"promotion_decisions.{binding}: invalid decision")
        evidence_package_ids = require_list(
            decision.get("evidence_package_ids"),
            f"promotion_decisions.{binding}.evidence_package_ids",
            errors,
        )
        unknown_packages = {str(package_id) for package_id in evidence_package_ids} - set(
            protocol["evidence_packages"]
        )
        if unknown_packages:
            errors.append(
                f"promotion_decisions.{binding}: unknown evidence packages "
                f"{sorted(unknown_packages)}"
            )
        if decision.get("independent_review_status") not in {
            "accepted",
            "rejected",
        }:
            errors.append(f"promotion_decisions.{binding}: invalid independent review")
        if decision.get("holdout_result") not in {"pass", "fail"}:
            errors.append(f"promotion_decisions.{binding}: holdout_result must be pass or fail")
        promotion_valid = (
            decision.get("decision") == "promote_empirical"
            and decision.get("holdout_result") == "pass"
            and decision.get("independent_review_status") == "accepted"
        )
        if decision.get("decision") == "promote_empirical" and not promotion_valid:
            all_promotions_reviewed = False
            errors.append(
                f"promotion_decisions.{binding}: empirical promotion "
                "requires a passing holdout and accepted independent review"
            )
        promotion_statuses[binding] = "promoted" if promotion_valid else "retained_assumption"

    if errors:
        raise ValueError("invalid economic-calibration evidence bundle:\n- " + "\n- ".join(errors))
    promoted = sum(status == "promoted" for status in promotion_statuses.values())
    all_fits_pass = all(status == "pass" for status in fit_statuses.values())
    return {
        "overall_status": (
            "validated" if all_fits_pass and all_promotions_reviewed else "holdout_failed"
        ),
        "evidence_package_count": len(packages),
        "correlation_fit_status": fit_statuses,
        "cash_flow_event_count": len(cash_events),
        "promoted_parameter_count": promoted,
        "retained_assumption_count": len(decisions) - promoted,
        "promotion_status": promotion_statuses,
    }
