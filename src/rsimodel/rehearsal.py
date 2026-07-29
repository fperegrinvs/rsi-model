"""Validation and public checklist rendering for the Stage-0 rehearsal."""

from __future__ import annotations

import csv
import io
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import NotRequired, Protocol, TypedDict

from rsimodel.evidence import (
    SHA256_PLACEHOLDER,
    artifact_files_template,
    binary_results_template,
    binary_statuses,
    require_exact_ids,
    require_fields,
    require_list,
    require_mapping,
    require_nonnegative_number,
    require_sha256,
    require_string,
    required_field_template,
    validate_binary_results,
    verify_artifact_files,
)
from rsimodel.governance import (
    GovernanceConfig,
    load_governance_controls,
)
from rsimodel.yaml_adapter import (
    load_yaml_mapping,
    require_boolean,
    require_sequence,
    require_string_sequence,
)
from rsimodel.yaml_adapter import (
    require_mapping as require_yaml_mapping,
)
from rsimodel.yaml_adapter import (
    require_string as require_yaml_string,
)

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = ROOT / "params" / "rehearsal_protocol.yaml"


class EmergencyEntrySettings(TypedDict):
    allowed: bool
    consequence: str
    required_record: str


class MaterialPaletteSettings(TypedDict):
    rule: str
    provenance_required: bool


class EnergyPaletteSettings(TypedDict):
    rule: str


class SiteBoundarySettings(TypedDict):
    routine_human_entry: str
    emergency_entry: EmergencyEntrySettings
    allowed_external_flows: tuple[str, ...]
    prohibited_external_flows: tuple[str, ...]
    material_palette: MaterialPaletteSettings
    energy_palette: EnergyPaletteSettings


class ExperimentalUnitSettings(TypedDict):
    identity: str
    role: str


class ReproducedCellSettings(ExperimentalUnitSettings):
    independence_rule: str


class ExperimentalUnitsSettings(TypedDict):
    seed_cell: ExperimentalUnitSettings
    reproduced_cell: ReproducedCellSettings


class EventTypeSettings(TypedDict):
    required_fields: tuple[str, ...]
    allowed_states: NotRequired[tuple[str, ...]]


class EventSchemaSettings(TypedDict):
    common_required_fields: tuple[str, ...]
    event_types: Mapping[str, EventTypeSettings]


class AcceptanceGateSettings(TypedDict):
    test: str
    evidence: tuple[str, ...]
    acceptance: str


class FaultCaseSettings(TypedDict):
    id: str
    injection: str
    expected_controls: tuple[str, ...]


class ParameterReplacementSettings(TypedDict):
    measurement: str
    model_paths: tuple[str, ...]
    events: tuple[str, ...]


class RehearsalProtocol(TypedDict):
    version: str
    protocol_id: str
    status: str
    source_class: str
    epistemic_status: str
    objective: str
    site_boundary: SiteBoundarySettings
    experimental_units: ExperimentalUnitsSettings
    event_schema: EventSchemaSettings
    acceptance_gates: Mapping[str, AcceptanceGateSettings]
    fault_campaign: tuple[FaultCaseSettings, ...]
    parameter_replacement_map: tuple[ParameterReplacementSettings, ...]
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


def _emergency_entry(value: object, *, label: str) -> EmergencyEntrySettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "allowed": require_boolean(record.get("allowed"), label=f"{label}.allowed"),
        "consequence": require_yaml_string(
            record.get("consequence"),
            label=f"{label}.consequence",
        ),
        "required_record": require_yaml_string(
            record.get("required_record"),
            label=f"{label}.required_record",
        ),
    }


def _material_palette(value: object, *, label: str) -> MaterialPaletteSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "rule": require_yaml_string(record.get("rule"), label=f"{label}.rule"),
        "provenance_required": require_boolean(
            record.get("provenance_required"),
            label=f"{label}.provenance_required",
        ),
    }


def _energy_palette(value: object, *, label: str) -> EnergyPaletteSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "rule": require_yaml_string(record.get("rule"), label=f"{label}.rule"),
    }


def _site_boundary(value: object, *, label: str) -> SiteBoundarySettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "routine_human_entry": require_yaml_string(
            record.get("routine_human_entry"),
            label=f"{label}.routine_human_entry",
        ),
        "emergency_entry": _emergency_entry(
            record.get("emergency_entry"),
            label=f"{label}.emergency_entry",
        ),
        "allowed_external_flows": require_string_sequence(
            record.get("allowed_external_flows"),
            label=f"{label}.allowed_external_flows",
        ),
        "prohibited_external_flows": require_string_sequence(
            record.get("prohibited_external_flows"),
            label=f"{label}.prohibited_external_flows",
        ),
        "material_palette": _material_palette(
            record.get("material_palette"),
            label=f"{label}.material_palette",
        ),
        "energy_palette": _energy_palette(
            record.get("energy_palette"),
            label=f"{label}.energy_palette",
        ),
    }


def _experimental_unit(value: object, *, label: str) -> ExperimentalUnitSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "identity": require_yaml_string(
            record.get("identity"),
            label=f"{label}.identity",
        ),
        "role": require_yaml_string(record.get("role"), label=f"{label}.role"),
    }


def _reproduced_cell(value: object, *, label: str) -> ReproducedCellSettings:
    record = require_yaml_mapping(value, label=label)
    base = _experimental_unit(value, label=label)
    return {
        **base,
        "independence_rule": require_yaml_string(
            record.get("independence_rule"),
            label=f"{label}.independence_rule",
        ),
    }


def _experimental_units(value: object, *, label: str) -> ExperimentalUnitsSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "seed_cell": _experimental_unit(
            record.get("seed_cell"),
            label=f"{label}.seed_cell",
        ),
        "reproduced_cell": _reproduced_cell(
            record.get("reproduced_cell"),
            label=f"{label}.reproduced_cell",
        ),
    }


def _event_type(value: object, *, label: str) -> EventTypeSettings:
    record = require_yaml_mapping(value, label=label)
    result: EventTypeSettings = {
        "required_fields": require_string_sequence(
            record.get("required_fields"),
            label=f"{label}.required_fields",
        )
    }
    if "allowed_states" in record:
        result["allowed_states"] = require_string_sequence(
            record["allowed_states"],
            label=f"{label}.allowed_states",
        )
    return result


def _event_schema(value: object, *, label: str) -> EventSchemaSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "common_required_fields": require_string_sequence(
            record.get("common_required_fields"),
            label=f"{label}.common_required_fields",
        ),
        "event_types": _named_records(
            record.get("event_types"),
            label=f"{label}.event_types",
            parser=_event_type,
        ),
    }


def _acceptance_gate(value: object, *, label: str) -> AcceptanceGateSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "test": require_yaml_string(record.get("test"), label=f"{label}.test"),
        "evidence": require_string_sequence(
            record.get("evidence"),
            label=f"{label}.evidence",
        ),
        "acceptance": require_yaml_string(
            record.get("acceptance"),
            label=f"{label}.acceptance",
        ),
    }


def _fault_case(value: object, *, label: str) -> FaultCaseSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "id": require_yaml_string(record.get("id"), label=f"{label}.id"),
        "injection": require_yaml_string(
            record.get("injection"),
            label=f"{label}.injection",
        ),
        "expected_controls": require_string_sequence(
            record.get("expected_controls"),
            label=f"{label}.expected_controls",
        ),
    }


def _parameter_replacement(
    value: object,
    *,
    label: str,
) -> ParameterReplacementSettings:
    record = require_yaml_mapping(value, label=label)
    return {
        "measurement": require_yaml_string(
            record.get("measurement"),
            label=f"{label}.measurement",
        ),
        "model_paths": require_string_sequence(
            record.get("model_paths"),
            label=f"{label}.model_paths",
        ),
        "events": require_string_sequence(
            record.get("events"),
            label=f"{label}.events",
        ),
    }


def _record_sequence[Record](
    value: object,
    *,
    label: str,
    parser: RecordParser[Record],
) -> tuple[Record, ...]:
    return tuple(
        parser(item, label=f"{label}[{index}]")
        for index, item in enumerate(require_sequence(value, label=label))
    )


def load_rehearsal_protocol(path: Path | None = None) -> RehearsalProtocol:
    """Load and structurally validate the complete Stage-0 protocol."""
    raw = load_yaml_mapping(path or PROTOCOL_PATH)
    return {
        "version": require_yaml_string(raw.get("version"), label="rehearsal.version"),
        "protocol_id": require_yaml_string(
            raw.get("protocol_id"),
            label="rehearsal.protocol_id",
        ),
        "status": require_yaml_string(raw.get("status"), label="rehearsal.status"),
        "source_class": require_yaml_string(
            raw.get("source_class"),
            label="rehearsal.source_class",
        ),
        "epistemic_status": require_yaml_string(
            raw.get("epistemic_status"),
            label="rehearsal.epistemic_status",
        ),
        "objective": require_yaml_string(
            raw.get("objective"),
            label="rehearsal.objective",
        ),
        "site_boundary": _site_boundary(
            raw.get("site_boundary"),
            label="rehearsal.site_boundary",
        ),
        "experimental_units": _experimental_units(
            raw.get("experimental_units"),
            label="rehearsal.experimental_units",
        ),
        "event_schema": _event_schema(
            raw.get("event_schema"),
            label="rehearsal.event_schema",
        ),
        "acceptance_gates": _named_records(
            raw.get("acceptance_gates"),
            label="rehearsal.acceptance_gates",
            parser=_acceptance_gate,
        ),
        "fault_campaign": _record_sequence(
            raw.get("fault_campaign"),
            label="rehearsal.fault_campaign",
            parser=_fault_case,
        ),
        "parameter_replacement_map": _record_sequence(
            raw.get("parameter_replacement_map"),
            label="rehearsal.parameter_replacement_map",
            parser=_parameter_replacement,
        ),
        "execution_outputs_required": require_string_sequence(
            raw.get("execution_outputs_required"),
            label="rehearsal.execution_outputs_required",
        ),
    }


def validate_rehearsal_protocol(
    protocol: RehearsalProtocol | None = None,
    governance: GovernanceConfig | None = None,
) -> None:
    """Reject incomplete gates, event contracts, or threat/control drift."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    if governance is None:
        governance = load_governance_controls()
    errors: list[str] = []

    if protocol.get("status") != "protocol_ready_physical_execution_pending":
        errors.append("protocol status must keep physical execution pending")
    if protocol.get("source_class") != "ASSUMPTION":
        errors.append("protocol must remain ASSUMPTION-class before execution")

    event_types = set(protocol["event_schema"]["event_types"])
    common_fields = set(protocol["event_schema"]["common_required_fields"])
    build_event_type = protocol["event_schema"]["event_types"].get("build_state")
    build_states = None if build_event_type is None else build_event_type.get("allowed_states")
    if not build_states:
        errors.append("event_schema.event_types.build_state must declare allowed_states")
    gates = protocol["acceptance_gates"]
    if set(gates) != {
        f"G{i:02d}_{suffix}"
        for i, suffix in (
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
        )
    }:
        errors.append("acceptance gates must be the complete G01-G10 set")
    for gate, cfg in gates.items():
        errors.extend(
            f"{gate}: missing {field}"
            for field in ("test", "evidence", "acceptance")
            if not cfg.get(field)
        )
        errors.extend(
            f"{gate}: unknown evidence type/field {evidence}"
            for evidence in cfg.get("evidence", [])
            if evidence not in event_types
            and evidence not in common_fields
            and evidence != "all_event_types"
        )

    controls = set(governance["controls"])
    threats = set(governance["threats"])
    cases = {case["id"]: case for case in protocol["fault_campaign"]}
    if not threats <= set(cases):
        errors.append(f"fault campaign misses governance threats {sorted(threats - set(cases))}")
    for case_id, case in cases.items():
        if not case.get("injection"):
            errors.append(f"{case_id}: missing injection")
        unknown = set(case.get("expected_controls", [])) - controls
        if unknown:
            errors.append(f"{case_id}: unknown controls {sorted(unknown)}")
    if "communication_loss" not in cases:
        errors.append("fault campaign must include progressive communication loss")

    mappings = protocol["parameter_replacement_map"]
    if not mappings:
        errors.append("parameter_replacement_map is empty")
    for index, mapping in enumerate(mappings):
        errors.extend(
            f"parameter_replacement_map[{index}] missing {field}"
            for field in ("measurement", "model_paths", "events")
            if not mapping.get(field)
        )
        unknown = set(mapping.get("events", [])) - event_types
        if unknown:
            errors.append(f"parameter_replacement_map[{index}] unknown events {sorted(unknown)}")

    if errors:
        raise ValueError("invalid rehearsal protocol:\n- " + "\n- ".join(errors))


def render_rehearsal_acceptance_csv(
    protocol: RehearsalProtocol | None = None,
    governance: GovernanceConfig | None = None,
) -> str:
    """Render gates, injections, and parameter mappings without fake results."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    if governance is None:
        governance = load_governance_controls()
    validate_rehearsal_protocol(protocol, governance)

    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(
        [
            "record_type",
            "id",
            "test_or_measurement",
            "required_evidence_or_controls",
            "acceptance_or_model_paths",
            "execution_status",
        ]
    )
    for gate, cfg in protocol["acceptance_gates"].items():
        writer.writerow(
            [
                "acceptance_gate",
                gate,
                cfg["test"],
                "; ".join(cfg["evidence"]),
                cfg["acceptance"],
                "execution_pending",
            ]
        )
    for case in protocol["fault_campaign"]:
        writer.writerow(
            [
                "fault_injection",
                case["id"],
                case["injection"],
                "; ".join(case["expected_controls"]),
                "execute and preserve measured containment/recovery or failure",
                "execution_pending",
            ]
        )
    for index, mapping in enumerate(protocol["parameter_replacement_map"], 1):
        writer.writerow(
            [
                "parameter_replacement",
                f"P{index:02d}",
                mapping["measurement"],
                "; ".join(mapping["events"]),
                "; ".join(mapping["model_paths"]),
                "data_pending",
            ]
        )
    return stream.getvalue()


def write_rehearsal_acceptance_csv(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_rehearsal_acceptance_csv(), encoding="utf-8")
    return path


def rehearsal_evidence_bundle_template(
    protocol: RehearsalProtocol | None = None,
    governance: GovernanceConfig | None = None,
) -> dict[str, object]:
    """Return an invalid-until-measured campaign bundle template."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    if governance is None:
        governance = load_governance_controls()
    validate_rehearsal_protocol(protocol, governance)
    schema = protocol["event_schema"]
    events: list[dict[str, object]] = []
    event_index = 0
    for event_type, cfg in schema["event_types"].items():
        cases: list[str | None] = (
            [case["id"] for case in protocol["fault_campaign"]]
            if event_type == "fault_event"
            else [None]
        )
        for case_id in cases:
            event_index += 1
            overrides: dict[str, object] = {
                "event_id": f"EVENT_REPLACE_{event_index:03d}",
                "event_type": event_type,
            }
            if event_type == "build_state":
                overrides.update(
                    {
                        "prior_state": "delivered",
                        "new_state": "staged",
                    }
                )
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

    replacements: dict[str, object] = {}
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
        "gate_results": binary_results_template(protocol["acceptance_gates"]),
        "fault_results": binary_results_template(case["id"] for case in protocol["fault_campaign"]),
        "parameter_replacements": replacements,
    }


def evaluate_rehearsal_evidence_bundle(
    bundle: Mapping[str, object] | None,
    protocol: RehearsalProtocol | None = None,
    governance: GovernanceConfig | None = None,
    *,
    archive_root: Path | None = None,
) -> dict[str, object]:
    """Validate a completed campaign bundle or return an honest pending state."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    if governance is None:
        governance = load_governance_controls()
    validate_rehearsal_protocol(protocol, governance)
    if not bundle:
        return {
            "overall_status": "execution_pending",
            "gate_status": dict.fromkeys(protocol["acceptance_gates"], "execution_pending"),
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
    event_records: list[dict[str, object]] = []
    previous_monotonic: float | None = None
    for index, raw_event in enumerate(events):
        label = f"events[{index}]"
        event = require_mapping(raw_event, label, errors)
        event_records.append(event)
        event_type = require_string(event, "event_type", label, errors)
        if event_type is None or event_type not in schema["event_types"]:
            errors.append(f"{label}: unknown event_type {event_type}")
            continue
        require_fields(event, common, label, errors)
        require_fields(
            event,
            schema["event_types"][event_type]["required_fields"],
            label,
            errors,
        )
        event_id = require_string(event, "event_id", label, errors)
        if event_id is None:
            continue
        if event_id in seen_events:
            errors.append(f"{label}: duplicate event_id {event_id}")
        seen_events.add(event_id)
        observed_types.add(event_type)
        timestamp = event.get("timestamp_utc")
        try:
            parsed_timestamp = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
            if parsed_timestamp.tzinfo is None:
                raise ValueError
        except ValueError:
            errors.append(f"{label}: timestamp_utc must include a timezone")
        require_nonnegative_number(event, "monotonic_time_s", label, errors)
        monotonic = event.get("monotonic_time_s")
        if isinstance(monotonic, (int, float)) and not isinstance(monotonic, bool):
            if previous_monotonic is not None and monotonic < previous_monotonic:
                errors.append(f"{label}: monotonic_time_s moved backwards")
            previous_monotonic = float(monotonic)
        if event.get("cell_id") not in {"cell_0", "cell_1", "site"}:
            errors.append(f"{label}: cell_id must be cell_0, cell_1, or site")
        if event_type == "build_state":
            allowed = set(schema["event_types"]["build_state"].get("allowed_states", ()))
            if event.get("prior_state") not in allowed:
                errors.append(f"{label}: invalid prior_state")
            if event.get("new_state") not in allowed:
                errors.append(f"{label}: invalid new_state")

    gate_results = require_mapping(bundle.get("gate_results"), "gate_results", errors)
    validate_binary_results(
        gate_results,
        set(protocol["acceptance_gates"]),
        "gate_results",
        errors,
    )
    fault_results = require_mapping(bundle.get("fault_results"), "fault_results", errors)
    expected_faults = {case["id"] for case in protocol["fault_campaign"]}
    validate_binary_results(
        fault_results,
        expected_faults,
        "fault_results",
        errors,
    )
    errors.extend(
        f"fault_results.{case_id}: no matching fault_event"
        for case_id in expected_faults
        if not any(
            event.get("event_type") == "fault_event" and event.get("campaign_case") == case_id
            for event in event_records
        )
    )

    replacements = require_mapping(
        bundle.get("parameter_replacements"),
        "parameter_replacements",
        errors,
    )
    expected_replacements = {
        f"P{index:02d}" for index, _ in enumerate(protocol["parameter_replacement_map"], 1)
    }
    require_exact_ids(
        replacements,
        expected_replacements,
        "parameter_replacements",
        errors,
    )
    for replacement_id, raw_record in replacements.items():
        record = require_mapping(raw_record, f"parameter_replacements.{replacement_id}", errors)
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
            errors.append(f"parameter_replacements.{replacement_id}: invalid decision")
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
        raise ValueError("invalid rehearsal evidence bundle:\n- " + "\n- ".join(errors))
    statuses = binary_statuses(gate_results)
    fault_statuses = binary_statuses(fault_results)
    all_faults_pass = all(status == "pass" for status in fault_statuses.values())
    if statuses.get("G07_fault_campaign") == "pass" and not all_faults_pass:
        raise ValueError(
            "invalid rehearsal evidence bundle:\n- "
            "G07_fault_campaign cannot pass while a fault case fails"
        )
    return {
        "overall_status": (
            "passed"
            if all(status == "pass" for status in statuses.values()) and all_faults_pass
            else "failed"
        ),
        "gate_status": statuses,
        "fault_status": fault_statuses,
        "event_count": len(events),
        "fault_case_count": len(fault_results),
        "parameter_replacement_count": len(replacements),
    }
