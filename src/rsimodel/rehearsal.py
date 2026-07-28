"""Validation and public checklist rendering for the Stage-0 rehearsal."""
from __future__ import annotations

import csv
from datetime import datetime
import io
from pathlib import Path
from typing import Any

import yaml

from rsimodel.evidence import (
    SHA256_PLACEHOLDER,
    artifact_files_template,
    binary_results_template,
    require_exact_ids,
    require_fields,
    require_list,
    require_mapping,
    require_nonnegative_number,
    require_sha256,
    required_field_template,
    validate_binary_results,
    verify_artifact_files,
)

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = ROOT / "params" / "rehearsal_protocol.yaml"
GOVERNANCE_PATH = ROOT / "params" / "governance_controls.yaml"


def load_rehearsal_protocol(path: Path | None = None) -> dict[str, Any]:
    return yaml.safe_load((path or PROTOCOL_PATH).read_text(encoding="utf-8"))


def load_governance_controls(path: Path | None = None) -> dict[str, Any]:
    return yaml.safe_load((path or GOVERNANCE_PATH).read_text(encoding="utf-8"))


def validate_rehearsal_protocol(
    protocol: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
) -> None:
    """Reject incomplete gates, event contracts, or threat/control drift."""
    protocol = protocol or load_rehearsal_protocol()
    governance = governance or load_governance_controls()
    errors: list[str] = []

    if protocol.get("status") != "protocol_ready_physical_execution_pending":
        errors.append("protocol status must keep physical execution pending")
    if protocol.get("source_class") != "ASSUMPTION":
        errors.append("protocol must remain ASSUMPTION-class before execution")

    event_types = set(protocol["event_schema"]["event_types"])
    common_fields = set(protocol["event_schema"]["common_required_fields"])
    gates = protocol.get("acceptance_gates", {})
    if set(gates) != {f"G{i:02d}_{suffix}" for i, suffix in (
        (1, "closed_boundary"),
        (2, "provenance_complete"),
        (3, "mass_energy_reconciled"),
        (4, "second_cell_discrete"),
        (5, "second_cell_retained_operation"),
        (6, "observable_autonomy"),
        (7, "fault_campaign"),
        (8, "lost_link_safe_hold"),
        (9, "independent_audit"),
        (10, "assumption_replacement"),
    )}:
        errors.append("acceptance gates must be the complete G01-G10 set")
    for gate, cfg in gates.items():
        for field in ("test", "evidence", "acceptance"):
            if not cfg.get(field):
                errors.append(f"{gate}: missing {field}")
        for evidence in cfg.get("evidence", []):
            if (
                evidence not in event_types
                and evidence not in common_fields
                and evidence != "all_event_types"
            ):
                errors.append(f"{gate}: unknown evidence type/field {evidence}")

    controls = set(governance["controls"])
    threats = set(governance["threats"])
    cases = {case["id"]: case for case in protocol.get("fault_campaign", [])}
    if not threats <= set(cases):
        errors.append(
            f"fault campaign misses governance threats {sorted(threats - set(cases))}"
        )
    for case_id, case in cases.items():
        if not case.get("injection"):
            errors.append(f"{case_id}: missing injection")
        unknown = set(case.get("expected_controls", [])) - controls
        if unknown:
            errors.append(f"{case_id}: unknown controls {sorted(unknown)}")
    if "communication_loss" not in cases:
        errors.append("fault campaign must include progressive communication loss")

    mappings = protocol.get("parameter_replacement_map", [])
    if not mappings:
        errors.append("parameter_replacement_map is empty")
    for index, mapping in enumerate(mappings):
        for field in ("measurement", "model_paths", "events"):
            if not mapping.get(field):
                errors.append(f"parameter_replacement_map[{index}] missing {field}")
        unknown = set(mapping.get("events", [])) - event_types
        if unknown:
            errors.append(
                f"parameter_replacement_map[{index}] unknown events {sorted(unknown)}"
            )

    if errors:
        raise ValueError("invalid rehearsal protocol:\n- " + "\n- ".join(errors))


def render_rehearsal_acceptance_csv(
    protocol: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
) -> str:
    """Render gates, injections, and parameter mappings without fake results."""
    protocol = protocol or load_rehearsal_protocol()
    governance = governance or load_governance_controls()
    validate_rehearsal_protocol(protocol, governance)

    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow([
        "record_type",
        "id",
        "test_or_measurement",
        "required_evidence_or_controls",
        "acceptance_or_model_paths",
        "execution_status",
    ])
    for gate, cfg in protocol["acceptance_gates"].items():
        writer.writerow([
            "acceptance_gate",
            gate,
            cfg["test"],
            "; ".join(cfg["evidence"]),
            cfg["acceptance"],
            "execution_pending",
        ])
    for case in protocol["fault_campaign"]:
        writer.writerow([
            "fault_injection",
            case["id"],
            case["injection"],
            "; ".join(case["expected_controls"]),
            "execute and preserve measured containment/recovery or failure",
            "execution_pending",
        ])
    for index, mapping in enumerate(protocol["parameter_replacement_map"], 1):
        writer.writerow([
            "parameter_replacement",
            f"P{index:02d}",
            mapping["measurement"],
            "; ".join(mapping["events"]),
            "; ".join(mapping["model_paths"]),
            "data_pending",
        ])
    return stream.getvalue()


def write_rehearsal_acceptance_csv(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_rehearsal_acceptance_csv(), encoding="utf-8")
    return path


def rehearsal_evidence_bundle_template(
    protocol: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an invalid-until-measured campaign bundle template."""
    protocol = protocol or load_rehearsal_protocol()
    governance = governance or load_governance_controls()
    validate_rehearsal_protocol(protocol, governance)
    schema = protocol["event_schema"]
    events: list[dict[str, Any]] = []
    event_index = 0
    for event_type, cfg in schema["event_types"].items():
        cases: list[str | None] = (
            [case["id"] for case in protocol["fault_campaign"]]
            if event_type == "fault_event"
            else [None]
        )
        for case_id in cases:
            event_index += 1
            overrides: dict[str, Any] = {
                "event_id": f"EVENT_REPLACE_{event_index:03d}",
                "event_type": event_type,
            }
            if event_type == "build_state":
                overrides.update({
                    "prior_state": "delivered",
                    "new_state": "staged",
                })
            if case_id is not None:
                overrides["campaign_case"] = case_id
            events.append(
                required_field_template(
                    [
                        *schema["common_required_fields"],
                        *cfg["required_fields"],
                    ],
                    overrides,
                )
            )

    replacements = {}
    for index, mapping in enumerate(
        protocol["parameter_replacement_map"],
        1,
    ):
        replacements[f"P{index:02d}"] = {
            "model_paths": mapping["model_paths"],
            "estimate": None,
            "units": None,
            "uncertainty": None,
            "denominator": None,
            "failed_trials": None,
            "censored_trials": None,
            "evidence_query_sha256": SHA256_PLACEHOLDER,
            "decision": None,
        }
    return {
        "template_status": "incomplete_do_not_submit",
        "protocol_id": protocol["protocol_id"],
        "raw_archive_sha256": SHA256_PLACEHOLDER,
        "auditor_report_sha256": SHA256_PLACEHOLDER,
        "artifact_files": artifact_files_template(),
        "events": events,
        "gate_results": binary_results_template(
            protocol["acceptance_gates"]
        ),
        "fault_results": binary_results_template(
            case["id"] for case in protocol["fault_campaign"]
        ),
        "parameter_replacements": replacements,
    }


def evaluate_rehearsal_evidence_bundle(
    bundle: dict[str, Any] | None,
    protocol: dict[str, Any] | None = None,
    governance: dict[str, Any] | None = None,
    *,
    archive_root: Path | None = None,
) -> dict[str, Any]:
    """Validate a completed campaign bundle or return an honest pending state."""
    protocol = protocol or load_rehearsal_protocol()
    governance = governance or load_governance_controls()
    validate_rehearsal_protocol(protocol, governance)
    if not bundle:
        return {
            "overall_status": "execution_pending",
            "gate_status": {
                gate: "execution_pending"
                for gate in protocol["acceptance_gates"]
            },
        }

    errors: list[str] = []
    if bundle.get("protocol_id") != protocol["protocol_id"]:
        errors.append("protocol_id does not match the r4.0 protocol")
    require_sha256(bundle, "raw_archive_sha256", "bundle", errors)
    require_sha256(bundle, "auditor_report_sha256", "bundle", errors)
    verify_artifact_files(bundle, archive_root, errors)

    schema = protocol["event_schema"]
    common = schema["common_required_fields"]
    events = require_list(bundle.get("events"), "events", errors)
    if not events:
        errors.append("events: no raw events supplied")
    seen_events: set[str] = set()
    observed_types: set[str] = set()
    previous_monotonic: float | None = None
    for index, raw_event in enumerate(events):
        label = f"events[{index}]"
        event = require_mapping(raw_event, label, errors)
        event_type = event.get("event_type")
        if event_type not in schema["event_types"]:
            errors.append(f"{label}: unknown event_type {event_type}")
            continue
        require_fields(event, common, label, errors)
        require_fields(
            event,
            schema["event_types"][event_type]["required_fields"],
            label,
            errors,
        )
        event_id = event.get("event_id")
        if event_id in seen_events:
            errors.append(f"{label}: duplicate event_id {event_id}")
        seen_events.add(event_id)
        observed_types.add(event_type)
        timestamp = event.get("timestamp_utc")
        try:
            parsed_timestamp = datetime.fromisoformat(
                str(timestamp).replace("Z", "+00:00")
            )
            if parsed_timestamp.tzinfo is None:
                raise ValueError
        except ValueError:
            errors.append(f"{label}: timestamp_utc must include a timezone")
        require_nonnegative_number(
            event, "monotonic_time_s", label, errors
        )
        monotonic = event.get("monotonic_time_s")
        if isinstance(monotonic, (int, float)) and not isinstance(
            monotonic, bool
        ):
            if (
                previous_monotonic is not None
                and monotonic < previous_monotonic
            ):
                errors.append(
                    f"{label}: monotonic_time_s moved backwards"
                )
            previous_monotonic = float(monotonic)
        if event.get("cell_id") not in {"cell_0", "cell_1", "site"}:
            errors.append(f"{label}: cell_id must be cell_0, cell_1, or site")
        if event_type == "build_state":
            allowed = set(schema["event_types"]["build_state"]["allowed_states"])
            if event.get("prior_state") not in allowed:
                errors.append(f"{label}: invalid prior_state")
            if event.get("new_state") not in allowed:
                errors.append(f"{label}: invalid new_state")

    gate_results = require_mapping(
        bundle.get("gate_results"), "gate_results", errors
    )
    validate_binary_results(
        gate_results,
        set(protocol["acceptance_gates"]),
        "gate_results",
        errors,
    )
    fault_results = require_mapping(
        bundle.get("fault_results"), "fault_results", errors
    )
    expected_faults = {case["id"] for case in protocol["fault_campaign"]}
    validate_binary_results(
        fault_results,
        expected_faults,
        "fault_results",
        errors,
    )
    for case_id in expected_faults:
        if not any(
            event.get("event_type") == "fault_event"
            and event.get("campaign_case") == case_id
            for event in events
        ):
            errors.append(f"fault_results.{case_id}: no matching fault_event")

    replacements = require_mapping(
        bundle.get("parameter_replacements"),
        "parameter_replacements",
        errors,
    )
    expected_replacements = {
        f"P{index:02d}"
        for index, _ in enumerate(protocol["parameter_replacement_map"], 1)
    }
    require_exact_ids(
        replacements,
        expected_replacements,
        "parameter_replacements",
        errors,
    )
    for replacement_id, raw_record in replacements.items():
        record = require_mapping(
            raw_record, f"parameter_replacements.{replacement_id}", errors
        )
        require_fields(
            record,
            {
                "model_paths",
                "estimate",
                "units",
                "uncertainty",
                "denominator",
                "failed_trials",
                "censored_trials",
                "evidence_query_sha256",
                "decision",
            },
            f"parameter_replacements.{replacement_id}",
            errors,
        )
        require_sha256(
            record,
            "evidence_query_sha256",
            f"parameter_replacements.{replacement_id}",
            errors,
        )
        if record.get("decision") not in {
            "retain_assumption",
            "replace_assumption",
        }:
            errors.append(
                f"parameter_replacements.{replacement_id}: invalid decision"
            )
        require_nonnegative_number(
            record,
            "failed_trials",
            f"parameter_replacements.{replacement_id}",
            errors,
        )
        require_nonnegative_number(
            record,
            "censored_trials",
            f"parameter_replacements.{replacement_id}",
            errors,
        )

    if observed_types != set(schema["event_types"]):
        errors.append(
            "events: complete campaign must exercise every event type; "
            f"missing {sorted(set(schema['event_types']) - observed_types)}"
        )
    if errors:
        raise ValueError(
            "invalid rehearsal evidence bundle:\n- " + "\n- ".join(errors)
        )
    statuses = {
        gate: record["status"] for gate, record in gate_results.items()
    }
    fault_statuses = {
        case: record["status"] for case, record in fault_results.items()
    }
    all_faults_pass = all(
        status == "pass" for status in fault_statuses.values()
    )
    if statuses.get("G07_fault_campaign") == "pass" and not all_faults_pass:
        raise ValueError(
            "invalid rehearsal evidence bundle:\n- "
            "G07_fault_campaign cannot pass while a fault case fails"
        )
    return {
        "overall_status": (
            "passed"
            if all(status == "pass" for status in statuses.values())
            and all_faults_pass
            else "failed"
        ),
        "gate_status": statuses,
        "fault_status": fault_statuses,
        "event_count": len(events),
        "fault_case_count": len(fault_results),
        "parameter_replacement_count": len(replacements),
    }
