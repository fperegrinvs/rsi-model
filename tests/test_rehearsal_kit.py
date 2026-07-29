"""The facility handoff kit must be complete, deterministic, and non-evidentiary."""

import hashlib
import json
from pathlib import Path

from rsimodel.rehearsal import load_rehearsal_protocol
from rsimodel.rehearsal_kit import (
    rehearsal_event_json_schema,
    write_rehearsal_execution_kit,
)


def test_event_schema_covers_every_protocol_event_type() -> None:
    protocol = load_rehearsal_protocol()
    schema = rehearsal_event_json_schema(protocol)
    branches = schema["oneOf"]
    assert isinstance(branches, list)
    assert {branch["properties"]["event_type"]["const"] for branch in branches} == set(
        protocol["event_schema"]["event_types"]
    )


def test_execution_kit_is_content_addressed_and_stays_pending(tmp_path: Path) -> None:
    output = tmp_path / "kit"
    manifest_path = write_rehearsal_execution_kit(output)
    first = manifest_path.read_bytes()
    manifest = json.loads(first)
    assert manifest["kit_status"] == "facility_handoff_ready_physical_execution_pending"
    assert "not measurements" in manifest["warning"]
    assert len(manifest["files"]) == (
        6 + len(load_rehearsal_protocol()["event_schema"]["event_types"])
    )
    for relative, digest in manifest["files"].items():
        assert hashlib.sha256((output / relative).read_bytes()).hexdigest() == digest

    assert write_rehearsal_execution_kit(output) == manifest_path
    assert manifest_path.read_bytes() == first


def test_templates_contain_no_unearned_result(tmp_path: Path) -> None:
    output = tmp_path / "kit"
    write_rehearsal_execution_kit(output)
    serialized = "\n".join(
        path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file()
    )
    assert "template_not_evidence" in serialized
    assert '"result": null' in serialized
    assert "pending_physical_campaign" in serialized
    assert '"status": "pass"' not in serialized
