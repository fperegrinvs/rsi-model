"""Executable contract tests for the Stage-0 physical rehearsal protocol."""

import csv
import io
from pathlib import Path

from rsimodel.rehearsal import (
    load_governance_controls,
    load_rehearsal_protocol,
    render_rehearsal_acceptance_csv,
    validate_rehearsal_protocol,
)

ROOT = Path(__file__).resolve().parents[1]


def test_rehearsal_protocol_is_complete_and_explicitly_unexecuted() -> None:
    protocol = load_rehearsal_protocol()
    validate_rehearsal_protocol(protocol)
    assert protocol["status"] == "protocol_ready_physical_execution_pending"
    assert protocol["source_class"] == "ASSUMPTION"
    assert len(protocol["acceptance_gates"]) == 10


def test_fault_campaign_covers_governance_register_and_lost_link() -> None:
    protocol = load_rehearsal_protocol()
    governance = load_governance_controls()
    case_ids = {case["id"] for case in protocol["fault_campaign"]}
    assert set(governance["threats"]) <= case_ids
    assert "communication_loss" in case_ids


def test_generated_matrix_contains_no_unearned_success_state() -> None:
    rows = list(csv.DictReader(io.StringIO(render_rehearsal_acceptance_csv())))
    assert rows
    assert {row["record_type"] for row in rows} == {
        "acceptance_gate",
        "fault_injection",
        "parameter_replacement",
    }
    assert {row["execution_status"] for row in rows} == {"execution_pending", "data_pending"}
    serialized = "\n".join(value for row in rows for value in row.values())
    assert "passed" not in serialized.lower()
    assert "validated" not in serialized.lower()


def test_committed_rehearsal_matrix_is_current() -> None:
    target = ROOT / "outputs" / "integrated" / "tables" / ("rehearsal_acceptance_matrix.csv")
    assert target.read_text(encoding="utf-8") == (render_rehearsal_acceptance_csv())
