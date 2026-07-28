"""Validate and render the r4.0 economic-calibration data contract."""
from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

import yaml

from rsimodel.evidence import (
    SHA256_PLACEHOLDER,
    artifact_files_template,
    require_exact_ids,
    require_fields,
    require_list,
    require_mapping,
    require_nonnegative_number,
    require_sha256,
    required_field_template,
    verify_artifact_files,
)

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = ROOT / "params" / "economic_calibration.yaml"
ANCHORS_PATH = ROOT / "params" / "anchors.yaml"
INTEGRATED_PATH = ROOT / "params" / "integrated_model.yaml"


def load_economic_calibration(path: Path | None = None) -> dict[str, Any]:
    return yaml.safe_load((path or PROTOCOL_PATH).read_text(encoding="utf-8"))


def _path_exists(tree: dict[str, Any], dotted: str) -> bool:
    node: Any = tree
    for component in dotted.split("."):
        if not isinstance(node, dict) or component not in node:
            return False
        node = node[component]
    return True


def validate_economic_calibration(
    protocol: dict[str, Any] | None = None,
) -> None:
    """Reject coverage gaps, invented readiness, and stale model bindings."""
    protocol = protocol or load_economic_calibration()
    errors: list[str] = []

    if protocol.get("status") != (
        "data_contract_ready_empirical_calibration_pending"
    ):
        errors.append("status must keep empirical calibration pending")
    if protocol.get("source_class") != "ASSUMPTION":
        errors.append("protocol must remain ASSUMPTION-class")

    architectures = protocol.get("architecture_cases", {})
    required_architectures = {
        "earth_reference",
        "serviceable_space_platform",
        "integrated_disposable_ai1",
    }
    if set(architectures) != required_architectures:
        errors.append("architecture cases must cover the three declared boundaries")

    packages = protocol.get("evidence_packages", {})
    for package_id, package in packages.items():
        for field in ("purpose", "required_fields", "model_bindings"):
            if not package.get(field):
                errors.append(f"{package_id}: missing {field}")
        if package.get("readiness") != "data_pending":
            errors.append(f"{package_id}: readiness must be data_pending")
    for architecture, config in architectures.items():
        unknown = set(config.get("required_evidence", [])) - set(packages)
        if unknown:
            errors.append(
                f"{architecture}: unknown evidence packages {sorted(unknown)}"
            )
        if not config.get("model_cases"):
            errors.append(f"{architecture}: model_cases is empty")

    anchors = yaml.safe_load(ANCHORS_PATH.read_text(encoding="utf-8"))
    integrated = yaml.safe_load(INTEGRATED_PATH.read_text(encoding="utf-8"))
    all_bindings = {
        binding
        for package in packages.values()
        for binding in package.get("model_bindings", [])
    }
    all_bindings |= {
        binding
        for group in protocol.get("correlation_groups", {}).values()
        for binding in group.get("members", [])
    }
    for binding in all_bindings:
        tree = integrated if binding.startswith("dynamic_economics.") else anchors
        if not _path_exists(tree, binding):
            errors.append(f"stale or unknown model binding {binding}")

    groups = protocol.get("correlation_groups", {})
    if len(groups) < 5:
        errors.append("at least five correlation groups are required")
    for group_id, group in groups.items():
        if not group.get("rationale"):
            errors.append(f"{group_id}: missing rationale")
        if len(group.get("members", [])) < 2:
            errors.append(f"{group_id}: fewer than two correlated members")

    event_schema = protocol.get("cash_flow_event_schema", {})
    common = set(event_schema.get("common_required_fields", []))
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
    if set(event_schema.get("event_types", {})) != required_events:
        errors.append("cash-flow event types are incomplete or unexpected")

    plan = protocol.get("calibration_plan", {})
    for field in (
        "calibration_split",
        "validation_split",
        "external_validation",
        "missingness",
        "censoring",
        "estimation",
        "sensitivity",
    ):
        if not plan.get(field):
            errors.append(f"calibration plan missing {field}")

    promotion = protocol.get("promotion_rule", {})
    if len(promotion.get("required", [])) < 8 or not promotion.get("decision"):
        errors.append("assumption-promotion rule is incomplete")

    if errors:
        raise ValueError(
            "invalid economic calibration protocol:\n- " + "\n- ".join(errors)
        )


def render_economic_calibration_csv(
    protocol: dict[str, Any] | None = None,
) -> str:
    """Render the evidence queue without implying that data were collected."""
    protocol = protocol or load_economic_calibration()
    validate_economic_calibration(protocol)
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow([
        "record_type",
        "id",
        "scope_or_purpose",
        "required_fields_or_members",
        "model_bindings_or_cases",
        "readiness",
    ])
    for case_id, case in protocol["architecture_cases"].items():
        writer.writerow([
            "architecture_case",
            case_id,
            case["description"],
            "; ".join(case["required_evidence"]),
            "; ".join(case["model_cases"]),
            "data_pending",
        ])
    for package_id, package in protocol["evidence_packages"].items():
        writer.writerow([
            "evidence_package",
            package_id,
            package["purpose"],
            "; ".join(package["required_fields"]),
            "; ".join(package["model_bindings"]),
            package["readiness"],
        ])
    for group_id, group in protocol["correlation_groups"].items():
        writer.writerow([
            "correlation_group",
            group_id,
            group["rationale"],
            "; ".join(group["members"]),
            "joint or hierarchical fit with held-out validation",
            "data_pending",
        ])
    for event_id, required_fields in protocol[
        "cash_flow_event_schema"
    ]["event_types"].items():
        writer.writerow([
            "cash_flow_event",
            event_id,
            "audited dated project event",
            "; ".join(required_fields),
            "; ".join(
                protocol["cash_flow_event_schema"]["common_required_fields"]
            ),
            "data_pending",
        ])
    return stream.getvalue()


def write_economic_calibration_csv(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_economic_calibration_csv(), encoding="utf-8")
    return path


def economic_calibration_bundle_template(
    protocol: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an invalid-until-calibrated evidence release template."""
    protocol = protocol or load_economic_calibration()
    validate_economic_calibration(protocol)

    packages = {}
    for package_id, package in protocol["evidence_packages"].items():
        packages[package_id] = {
            "normalized_records_sha256": SHA256_PLACEHOLDER,
            "records": [
                required_field_template(package["required_fields"])
            ],
        }
    fits = {}
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
    events = []
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
    decisions = {
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
    bundle: dict[str, Any] | None,
    protocol: dict[str, Any] | None = None,
    *,
    archive_root: Path | None = None,
) -> dict[str, Any]:
    """Validate normalized records, correlation fits, and promotion decisions."""
    protocol = protocol or load_economic_calibration()
    validate_economic_calibration(protocol)
    if not bundle:
        return {
            "overall_status": "empirical_calibration_pending",
            "evidence_package_status": {
                package: "data_pending"
                for package in protocol["evidence_packages"]
            },
        }

    errors: list[str] = []
    if bundle.get("protocol_id") != protocol["protocol_id"]:
        errors.append("protocol_id does not match the r4.0 protocol")
    require_sha256(bundle, "archive_sha256", "bundle", errors)
    verify_artifact_files(bundle, archive_root, errors)

    packages = require_mapping(
        bundle.get("evidence_packages"), "evidence_packages", errors
    )
    require_exact_ids(
        packages,
        set(protocol["evidence_packages"]),
        "evidence_packages",
        errors,
    )
    for package_id, raw_submission in packages.items():
        submission = require_mapping(
            raw_submission, f"evidence_packages.{package_id}", errors
        )
        records = require_list(
            submission.get("records"),
            f"evidence_packages.{package_id}.records",
            errors,
        )
        if not records:
            errors.append(f"evidence_packages.{package_id}: records are empty")
            continue
        required = protocol["evidence_packages"].get(
            package_id, {}
        ).get("required_fields", [])
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

    fits = require_mapping(
        bundle.get("correlation_fits"), "correlation_fits", errors
    )
    require_exact_ids(
        fits,
        set(protocol["correlation_groups"]),
        "correlation_fits",
        errors,
    )
    fit_statuses: dict[str, str] = {}
    for group_id, raw_fit in fits.items():
        fit = require_mapping(
            raw_fit, f"correlation_fits.{group_id}", errors
        )
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
        expected_members = set(
            protocol["correlation_groups"].get(group_id, {}).get("members", [])
        )
        if set(fit.get("members", [])) != expected_members:
            errors.append(
                f"correlation_fits.{group_id}: members do not match contract"
            )
        if fit.get("holdout_status") not in {"pass", "fail"}:
            errors.append(
                f"correlation_fits.{group_id}: holdout_status must be pass or fail"
            )
        fit_statuses[group_id] = fit.get("holdout_status")

    schema = protocol["cash_flow_event_schema"]
    cash_events = require_list(
        bundle.get("cash_flow_events"), "cash_flow_events", errors
    )
    if not cash_events:
        errors.append("cash_flow_events: no events supplied")
    seen_events: set[str] = set()
    observed_event_types: set[str] = set()
    for index, raw_event in enumerate(cash_events):
        label = f"cash_flow_events[{index}]"
        event = require_mapping(raw_event, label, errors)
        event_type = event.get("event_type")
        if event_type not in schema["event_types"]:
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
        event_id = event.get("event_id")
        if event_id in seen_events:
            errors.append(f"{label}: duplicate event_id {event_id}")
        seen_events.add(event_id)
        observed_event_types.add(event_type)
        require_sha256(event, "source_document_hash", label, errors)
        require_nonnegative_number(event, "amount", label, errors)
    missing_events = set(schema["event_types"]) - observed_event_types
    if missing_events:
        errors.append(
            f"cash_flow_events: missing event types {sorted(missing_events)}"
        )

    all_bindings = {
        binding
        for package in protocol["evidence_packages"].values()
        for binding in package["model_bindings"]
    }
    decisions = require_mapping(
        bundle.get("promotion_decisions"), "promotion_decisions", errors
    )
    require_exact_ids(
        decisions,
        all_bindings,
        "promotion_decisions",
        errors,
    )
    promotion_statuses: dict[str, str] = {}
    for binding, raw_decision in decisions.items():
        decision = require_mapping(
            raw_decision, f"promotion_decisions.{binding}", errors
        )
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
            errors.append(
                f"promotion_decisions.{binding}: invalid decision"
            )
        unknown_packages = set(
            decision.get("evidence_package_ids", [])
        ) - set(protocol["evidence_packages"])
        if unknown_packages:
            errors.append(
                f"promotion_decisions.{binding}: unknown evidence packages "
                f"{sorted(unknown_packages)}"
            )
        if decision.get("independent_review_status") not in {
            "accepted",
            "rejected",
        }:
            errors.append(
                f"promotion_decisions.{binding}: invalid independent review"
            )
        if decision.get("holdout_result") not in {"pass", "fail"}:
            errors.append(
                f"promotion_decisions.{binding}: holdout_result must be "
                "pass or fail"
            )
        promotion_valid = (
            decision.get("decision") == "promote_empirical"
            and decision.get("holdout_result") == "pass"
            and decision.get("independent_review_status") == "accepted"
        )
        if (
            decision.get("decision") == "promote_empirical"
            and not promotion_valid
        ):
            errors.append(
                f"promotion_decisions.{binding}: empirical promotion "
                "requires a passing holdout and accepted independent review"
            )
        promotion_statuses[binding] = (
            "promoted"
            if promotion_valid
            else "retained_assumption"
        )

    if errors:
        raise ValueError(
            "invalid economic-calibration evidence bundle:\n- "
            + "\n- ".join(errors)
        )
    promoted = sum(
        status == "promoted" for status in promotion_statuses.values()
    )
    all_fits_pass = all(
        status == "pass" for status in fit_statuses.values()
    )
    all_promotions_reviewed = all(
        decision.get("decision") != "promote_empirical"
        or (
            decision.get("holdout_result") == "pass"
            and decision.get("independent_review_status") == "accepted"
        )
        for decision in decisions.values()
        if isinstance(decision, dict)
    )
    return {
        "overall_status": (
            "validated"
            if all_fits_pass and all_promotions_reviewed
            else "holdout_failed"
        ),
        "evidence_package_count": len(packages),
        "correlation_fit_status": fit_statuses,
        "cash_flow_event_count": len(cash_events),
        "promoted_parameter_count": promoted,
        "retained_assumption_count": len(decisions) - promoted,
        "promotion_status": promotion_statuses,
    }
