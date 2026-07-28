"""Tests for the process-feasible closure acceptance contract."""
import csv
import io
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.process_closure import (
    load_process_closure_contract,
    render_process_closure_gap_csv,
    validate_process_closure_contract,
)


def test_contract_tracks_current_categories_and_required_detail():
    contract = load_process_closure_contract()
    validate_process_closure_contract(contract)
    assert len(contract["current_aggregate_categories"]) == 17
    assert len(contract["critical_part_families"]) == 14
    assert len(contract["acceptance_gates"]) == 8


def test_gap_register_does_not_claim_process_closure():
    rows = list(csv.DictReader(io.StringIO(render_process_closure_gap_csv())))
    assert rows
    assert {row["readiness"] for row in rows} == {"evidence_pending"}
    assert {row["record_type"] for row in rows} == {
        "graph_node_type",
        "material_grade",
        "critical_part_family",
        "source_register",
        "fleet_register",
        "acceptance_gate",
    }


def test_required_part_ancestry_and_source_fleet_are_explicit():
    contract = load_process_closure_contract()
    assert "parent_tools" in contract["critical_part_families"]
    assert "calibration_artifacts" in contract["critical_part_families"]
    assert "delta_v_and_transfer_windows" in (
        contract["source_and_fleet_requirements"]["fleet_fields"]
    )
    assert "depletion_and_failed_source_rule" in (
        contract["source_and_fleet_requirements"]["source_fields"]
    )
    assert "source_record_id" in (
        contract["graph_schema"]["node_types"]["source_lot"][
            "required_fields"
        ]
    )
    assert "fleet_record_id" in (
        contract["graph_schema"]["node_types"]["transport_leg"][
            "required_fields"
        ]
    )


def test_committed_process_closure_gap_register_is_current():
    target = ROOT / "outputs" / "integrated" / "tables" / (
        "process_closure_gap_register.csv"
    )
    assert target.read_text(encoding="utf-8") == (
        render_process_closure_gap_csv()
    )
