"""Append-only capture tests for a future physical Stage-0 campaign."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rsimodel.rehearsal_archive import (
    append_rehearsal_event,
    initialize_rehearsal_archive,
    load_rehearsal_archive,
    rehearsal_archive_report,
    validate_rehearsal_event,
)
from rsimodel.rehearsal_archive_cli import main

WITNESS_HASH = "a" * 64


def _utility_event(event_id: str, monotonic: float) -> dict[str, object]:
    return {
        "event_id": event_id,
        "event_type": "utility_meter",
        "timestamp_utc": f"2026-07-29T00:00:{int(monotonic):02d}Z",
        "monotonic_time_s": monotonic,
        "cell_id": "site",
        "actor_or_controller": "meter-01",
        "signed_build_or_fault_campaign_id": "campaign-01",
        "software_and_recipe_version": "capture-v1",
        "sensor_source": "revenue-meter-01",
        "external_witness_hash": WITNESS_HASH,
        "electricity_kwh": 1.0,
        "thermal_input_kwh": 2.0,
        "storage_charge_kwh": 0.5,
        "storage_discharge_kwh": 0.25,
        "unserved_energy_kwh": 0.0,
    }


def test_archive_is_hash_chained_and_reported_without_claiming_a_gate(tmp_path: Path) -> None:
    archive = initialize_rehearsal_archive(tmp_path / "events.jsonl")
    first = append_rehearsal_event(archive, _utility_event("event-1", 1))
    second = append_rehearsal_event(archive, _utility_event("event-2", 2))

    assert first != second
    assert len(first) == 64
    assert [event["event_id"] for event in load_rehearsal_archive(archive)] == [
        "event-1",
        "event-2",
    ]
    report = rehearsal_archive_report(archive)
    assert report["event_count"] == 2
    assert report["query_status"] == "acquisition_incomplete"
    assert report["numeric_totals"] == {
        "electricity_kwh": 2.0,
        "storage_charge_kwh": 1.0,
        "storage_discharge_kwh": 0.5,
        "thermal_input_kwh": 4.0,
        "unserved_energy_kwh": 0.0,
    }
    assert "does not pass" in str(report["warning"])


def test_archive_rejects_tampering_duplicates_and_time_reversal(tmp_path: Path) -> None:
    archive = initialize_rehearsal_archive(tmp_path / "events.jsonl")
    append_rehearsal_event(archive, _utility_event("event-1", 2))
    original = archive.read_text(encoding="utf-8")
    archive.write_text(original.replace('"electricity_kwh":1.0', '"electricity_kwh":9.0'))
    with pytest.raises(ValueError, match="record hash"):
        load_rehearsal_archive(archive)

    archive.write_text(original, encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate event_id"):
        append_rehearsal_event(archive, _utility_event("event-1", 3))
    with pytest.raises(ValueError, match="moved backwards"):
        append_rehearsal_event(archive, _utility_event("event-2", 1))


def test_event_validation_rejects_missing_witness_and_bad_numeric_value() -> None:
    event = _utility_event("event-1", 1)
    event["external_witness_hash"] = "not-a-hash"
    event["electricity_kwh"] = -1
    with pytest.raises(ValueError, match="external_witness_hash"):
        validate_rehearsal_event(event)


def test_cli_initializes_appends_and_writes_report(tmp_path: Path) -> None:
    archive = tmp_path / "events.jsonl"
    event_path = tmp_path / "event.json"
    report_path = tmp_path / "report.json"
    event_path.write_text(json.dumps(_utility_event("event-1", 1)), encoding="utf-8")

    assert main(["init", str(archive)]) == 0
    assert main(["append", str(archive), str(event_path)]) == 0
    assert main(["verify", str(archive), "--output", str(report_path)]) == 0
    assert json.loads(report_path.read_text(encoding="utf-8"))["event_count"] == 1


def test_cli_fails_closed_for_invalid_event(tmp_path: Path) -> None:
    archive = tmp_path / "events.jsonl"
    event_path = tmp_path / "event.json"
    assert main(["init", str(archive)]) == 0
    event_path.write_text("[]", encoding="utf-8")
    assert main(["append", str(archive), str(event_path)]) == 2
