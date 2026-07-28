"""Tests for the r4.0 empirical economic-calibration contract."""
import csv
import io
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.economic_calibration import (
    load_economic_calibration,
    render_economic_calibration_csv,
    validate_economic_calibration,
)


def test_contract_covers_architectures_evidence_and_correlations():
    protocol = load_economic_calibration()
    validate_economic_calibration(protocol)
    assert len(protocol["architecture_cases"]) == 3
    assert len(protocol["evidence_packages"]) == 6
    assert len(protocol["correlation_groups"]) >= 5


def test_workload_and_cash_flow_contracts_preserve_required_boundaries():
    protocol = load_economic_calibration()
    workload_fields = set(
        protocol["evidence_packages"]["E01_workload_benchmark"][
            "required_fields"
        ]
    )
    assert {
        "model_and_version",
        "precision_and_quantization",
        "latency_distribution",
        "accuracy_or_quality_gate",
        "topology_and_synchronization",
        "fault_and_checkpoint_policy",
    } <= workload_fields
    assert {
        "failure_and_repair",
        "insurance",
        "financing",
        "retirement_disposal",
        "earth_resource",
    } <= set(protocol["cash_flow_event_schema"]["event_types"])


def test_readiness_table_contains_no_empirical_or_calibrated_claim():
    rows = list(
        csv.DictReader(io.StringIO(render_economic_calibration_csv()))
    )
    assert rows
    assert {row["readiness"] for row in rows} == {"data_pending"}
    assert {row["record_type"] for row in rows} == {
        "architecture_case",
        "evidence_package",
        "correlation_group",
        "cash_flow_event",
    }


def test_committed_economic_calibration_table_is_current():
    target = ROOT / "outputs" / "integrated" / "tables" / (
        "economic_calibration_readiness.csv"
    )
    assert target.read_text(encoding="utf-8") == (
        render_economic_calibration_csv()
    )
