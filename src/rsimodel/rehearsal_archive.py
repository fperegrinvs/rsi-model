"""Hash-chained event capture and deterministic queries for the Stage-0 rehearsal."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import cast

from rsimodel.evidence import SHA256_RE
from rsimodel.rehearsal import RehearsalProtocol, load_rehearsal_protocol

GENESIS_SHA256 = "0" * 64
NUMERIC_EVENT_FIELDS = {
    "monotonic_time_s",
    "measured_mass_kg",
    "gross_mass_kg",
    "waste_mass_kg",
    "uncertainty_kg",
    "duration_s",
    "verification_backlog_s",
    "energy_kwh",
    "yield",
    "duration_person_hours",
    "detection_latency_s",
    "containment_latency_s",
    "recovery_latency_s",
    "physical_order_rate_before",
    "physical_order_rate_after",
    "electricity_kwh",
    "thermal_input_kwh",
    "storage_charge_kwh",
    "storage_discharge_kwh",
    "unserved_energy_kwh",
}


def _canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode()


def _record_payload(
    sequence: int,
    previous_record_sha256: str,
    event: Mapping[str, object],
) -> dict[str, object]:
    return {
        "event": dict(event),
        "previous_record_sha256": previous_record_sha256,
        "sequence": sequence,
    }


def _record_sha256(
    sequence: int,
    previous_record_sha256: str,
    event: Mapping[str, object],
) -> str:
    return hashlib.sha256(
        _canonical_bytes(_record_payload(sequence, previous_record_sha256, event))
    ).hexdigest()


def validate_rehearsal_event(
    event: Mapping[str, object],
    protocol: RehearsalProtocol | None = None,
) -> None:
    """Validate one event before it enters the append-only campaign archive."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    errors: list[str] = []
    event_type = event.get("event_type")
    event_types = protocol["event_schema"]["event_types"]
    if not isinstance(event_type, str) or event_type not in event_types:
        errors.append(f"event_type must be one of {sorted(event_types)}")
    required = set(protocol["event_schema"]["common_required_fields"])
    if isinstance(event_type, str) and event_type in event_types:
        required.update(event_types[event_type]["required_fields"])
    missing = sorted(field for field in required if event.get(field) in (None, "", []))
    if missing:
        errors.append(f"missing required fields {missing}")

    event_id = event.get("event_id")
    if not isinstance(event_id, str) or not event_id:
        errors.append("event_id must be a nonempty string")
    timestamp = event.get("timestamp_utc")
    try:
        parsed_timestamp = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
        if parsed_timestamp.tzinfo is None:
            raise ValueError
    except ValueError:
        errors.append("timestamp_utc must be an ISO-8601 timestamp with a timezone")
    monotonic = event.get("monotonic_time_s")
    if not isinstance(monotonic, (int, float)) or isinstance(monotonic, bool) or monotonic < 0:
        errors.append("monotonic_time_s must be a nonnegative number")
    if event.get("cell_id") not in {"cell_0", "cell_1", "site"}:
        errors.append("cell_id must be cell_0, cell_1, or site")
    witness_hash = event.get("external_witness_hash")
    if not isinstance(witness_hash, str) or not SHA256_RE.fullmatch(witness_hash):
        errors.append("external_witness_hash must be a lowercase sha256")

    for field in sorted(NUMERIC_EVENT_FIELDS & set(event)):
        value = event[field]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            errors.append(f"{field} must be a nonnegative number")

    if event_type == "build_state":
        allowed = set(event_types["build_state"].get("allowed_states", ()))
        if event.get("prior_state") not in allowed:
            errors.append("prior_state is not an allowed build state")
        if event.get("new_state") not in allowed:
            errors.append("new_state is not an allowed build state")

    if errors:
        raise ValueError("invalid rehearsal event:\n- " + "\n- ".join(errors))


def initialize_rehearsal_archive(path: Path) -> Path:
    """Create a new empty archive without overwriting an existing campaign."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8"):
        pass
    return path


def _load_record(line: str, line_number: int) -> dict[str, object]:
    try:
        value: object = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ValueError(f"archive line {line_number}: invalid JSON: {exc.msg}") from exc
    if not isinstance(value, Mapping):
        raise ValueError(f"archive line {line_number}: record must be an object")
    raw = cast(Mapping[object, object], value)
    if not all(isinstance(key, str) for key in raw):
        raise ValueError(f"archive line {line_number}: record keys must be strings")
    return {str(key): child for key, child in raw.items()}


def load_rehearsal_archive(
    path: Path,
    protocol: RehearsalProtocol | None = None,
) -> list[dict[str, object]]:
    """Verify the complete hash chain and return the validated event records."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    if not path.is_file():
        raise ValueError(f"rehearsal archive does not exist: {path}")

    events: list[dict[str, object]] = []
    expected_previous = GENESIS_SHA256
    previous_monotonic: float | None = None
    seen_event_ids: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError(f"archive line {line_number}: blank records are prohibited")
        record = _load_record(line, line_number)
        expected_sequence = line_number
        if record.get("sequence") != expected_sequence:
            raise ValueError(f"archive line {line_number}: sequence must be {expected_sequence}")
        if record.get("previous_record_sha256") != expected_previous:
            raise ValueError(f"archive line {line_number}: broken previous-record hash")
        raw_event = record.get("event")
        if not isinstance(raw_event, Mapping):
            raise ValueError(f"archive line {line_number}: event must be an object")
        event_raw = cast(Mapping[object, object], raw_event)
        if not all(isinstance(key, str) for key in event_raw):
            raise ValueError(f"archive line {line_number}: event keys must be strings")
        event = {str(key): child for key, child in event_raw.items()}
        validate_rehearsal_event(event, protocol)

        actual_digest = _record_sha256(expected_sequence, expected_previous, event)
        if record.get("record_sha256") != actual_digest:
            raise ValueError(f"archive line {line_number}: record hash does not match content")
        event_id = cast(str, event["event_id"])
        if event_id in seen_event_ids:
            raise ValueError(f"archive line {line_number}: duplicate event_id {event_id}")
        seen_event_ids.add(event_id)
        monotonic = float(cast(float, event["monotonic_time_s"]))
        if previous_monotonic is not None and monotonic < previous_monotonic:
            raise ValueError(f"archive line {line_number}: monotonic_time_s moved backwards")
        previous_monotonic = monotonic
        events.append(event)
        expected_previous = actual_digest
    return events


def append_rehearsal_event(
    path: Path,
    event: Mapping[str, object],
    protocol: RehearsalProtocol | None = None,
) -> str:
    """Validate and append one event, returning its content-chain digest."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    validate_rehearsal_event(event, protocol)
    existing = load_rehearsal_archive(path, protocol)
    event_id = cast(str, event["event_id"])
    if any(existing_event["event_id"] == event_id for existing_event in existing):
        raise ValueError(f"duplicate event_id {event_id}")
    monotonic = float(cast(float, event["monotonic_time_s"]))
    if existing and monotonic < float(cast(float, existing[-1]["monotonic_time_s"])):
        raise ValueError("monotonic_time_s moved backwards")

    sequence = len(existing) + 1
    previous_digest = GENESIS_SHA256
    if existing:
        last_line = path.read_text(encoding="utf-8").splitlines()[-1]
        previous_digest = cast(str, _load_record(last_line, sequence - 1)["record_sha256"])
    digest = _record_sha256(sequence, previous_digest, event)
    record = {
        **_record_payload(sequence, previous_digest, event),
        "record_sha256": digest,
    }
    with path.open("a", encoding="utf-8", newline="") as stream:
        stream.write(_canonical_bytes(record).decode())
    return digest


def rehearsal_archive_report(
    path: Path,
    protocol: RehearsalProtocol | None = None,
) -> dict[str, object]:
    """Return deterministic acquisition coverage without evaluating physical gates."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    events = load_rehearsal_archive(path, protocol)
    event_type_counts = Counter(str(event["event_type"]) for event in events)
    cell_counts = Counter(str(event["cell_id"]) for event in events)
    observed_faults = {
        str(event["campaign_case"])
        for event in events
        if event["event_type"] == "fault_event" and event.get("campaign_case")
    }
    expected_faults = {case["id"] for case in protocol["fault_campaign"]}
    missing_event_types = sorted(
        set(protocol["event_schema"]["event_types"]) - set(event_type_counts)
    )
    missing_fault_cases = sorted(expected_faults - observed_faults)

    totals = {
        field: sum(
            float(cast(float, event[field]))
            for event in events
            if isinstance(event.get(field), (int, float)) and not isinstance(event.get(field), bool)
        )
        for field in sorted(NUMERIC_EVENT_FIELDS - {"monotonic_time_s"})
        if any(field in event for event in events)
    }
    archive_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "archive_path": path.name,
        "archive_sha256": archive_digest,
        "cell_counts": dict(sorted(cell_counts.items())),
        "event_count": len(events),
        "event_type_counts": dict(sorted(event_type_counts.items())),
        "first_timestamp_utc": events[0]["timestamp_utc"] if events else None,
        "last_record_sha256": (
            _load_record(path.read_text(encoding="utf-8").splitlines()[-1], len(events))[
                "record_sha256"
            ]
            if events
            else GENESIS_SHA256
        ),
        "last_timestamp_utc": events[-1]["timestamp_utc"] if events else None,
        "missing_event_types": missing_event_types,
        "missing_fault_cases": missing_fault_cases,
        "numeric_totals": totals,
        "protocol_id": protocol["protocol_id"],
        "query_status": (
            "acquisition_shape_complete"
            if not missing_event_types and not missing_fault_cases
            else "acquisition_incomplete"
        ),
        "warning": (
            "Coverage and integrity only. This report does not pass an acceptance gate "
            "or replace an independent audit."
        ),
    }


def write_rehearsal_archive_report(
    archive_path: Path,
    output_path: Path,
    protocol: RehearsalProtocol | None = None,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            rehearsal_archive_report(archive_path, protocol),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return output_path


def append_events(
    path: Path,
    events: Sequence[Mapping[str, object]],
    protocol: RehearsalProtocol | None = None,
) -> tuple[str, ...]:
    """Append a sequence in order; intended for instrument batch export."""
    return tuple(append_rehearsal_event(path, event, protocol) for event in events)
