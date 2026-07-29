"""Empirical evidence ingestion must fail closed."""

import hashlib
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from rsimodel.economic_calibration import (
    economic_calibration_bundle_template,
    evaluate_economic_calibration_bundle,
)
from rsimodel.process_closure import (
    evaluate_process_closure_bundle,
    process_closure_bundle_template,
)
from rsimodel.rehearsal import (
    evaluate_rehearsal_evidence_bundle,
    rehearsal_evidence_bundle_template,
)

EvidenceBundle = dict[str, Any]
TemplateBuilder = Callable[[], EvidenceBundle]
BundleEvaluator = Callable[..., dict[str, Any]]


def _backed_template(template: EvidenceBundle, tmp_path: Path) -> EvidenceBundle:
    artifact = tmp_path / "evidence.bin"
    artifact.write_bytes(b"independent evidence fixture")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()

    numeric_fields = {
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
        "estimate",
        "denominator",
        "failed_trials",
        "censored_trials",
        "failed_and_censored_count",
        "amount",
    }
    structured_fields = {
        "stoichiometry_or_bom",
        "quantity_and_units",
        "yield_distribution",
        "energy_distribution",
        "contamination_and_rework",
        "consumables_and_tool_wear",
        "capacity_and_cycle_time",
    }

    def fill(value: Any, key: str = "") -> Any:
        if isinstance(value, dict):
            return {child_key: fill(child, child_key) for child_key, child in value.items()}
        if isinstance(value, list):
            return [fill(child, key) for child in value]
        if value is not None:
            if isinstance(value, str) and "REPLACE_WITH_64" in value:
                return digest
            return value
        if key.endswith("sha256") or key.endswith("_hash"):
            return digest
        if key in numeric_fields:
            return 1.0
        if key in structured_fields:
            return {"value": 1.0, "units": "declared"}
        if key == "timestamp_utc":
            return "2026-07-28T00:00:00Z"
        if key == "cell_id":
            return "cell_0"
        return "evidence"

    completed = fill(template)
    completed["artifact_files"] = {"fixture": {"path": artifact.name, "sha256": digest}}
    return completed


def test_absent_bundles_remain_explicitly_pending() -> None:
    assert evaluate_rehearsal_evidence_bundle(None)["overall_status"] == ("execution_pending")
    assert evaluate_process_closure_bundle(None)["overall_status"] == ("graph_and_evidence_pending")
    assert evaluate_economic_calibration_bundle(None)["overall_status"] == (
        "empirical_calibration_pending"
    )


def test_rehearsal_rejects_claimed_results_without_raw_evidence() -> None:
    with pytest.raises(ValueError, match="raw_archive_sha256"):
        evaluate_rehearsal_evidence_bundle(
            {
                "protocol_id": "stage0-terrestrial-autonomous-closure",
                "gate_results": {},
                "fault_results": {},
                "parameter_replacements": {},
                "events": [],
            }
        )


def test_process_closure_rejects_empty_graph_claim() -> None:
    with pytest.raises(ValueError, match="archive_sha256"):
        evaluate_process_closure_bundle(
            {
                "contract_id": "process-feasible-industrial-closure",
                "graph_version": "claimed-v1",
                "nodes": [],
                "edges": [],
                "evidence_records": [],
                "gate_results": {},
            }
        )


def test_economics_rejects_calibration_without_records_and_holdout_fits() -> None:
    with pytest.raises(ValueError, match="archive_sha256"):
        evaluate_economic_calibration_bundle(
            {
                "protocol_id": "symmetric-compute-economics-calibration",
                "evidence_packages": {},
                "correlation_fits": {},
                "cash_flow_events": [],
                "promotion_decisions": {},
            }
        )


@pytest.mark.parametrize(
    ("builder", "evaluator"),
    (
        (
            process_closure_bundle_template,
            evaluate_process_closure_bundle,
        ),
        (
            rehearsal_evidence_bundle_template,
            evaluate_rehearsal_evidence_bundle,
        ),
        (
            economic_calibration_bundle_template,
            evaluate_economic_calibration_bundle,
        ),
    ),
)
def test_generated_templates_are_deterministic_and_cannot_fake_evidence(
    builder: TemplateBuilder,
    evaluator: BundleEvaluator,
) -> None:
    template = builder()
    assert template == builder()
    assert template["template_status"] == "incomplete_do_not_submit"
    with pytest.raises(ValueError, match="sha256"):
        evaluator(template)


def test_rehearsal_rejects_gate_pass_when_fault_cases_fail(tmp_path: Path) -> None:
    bundle = _backed_template(rehearsal_evidence_bundle_template(), tmp_path)
    for result in bundle["gate_results"].values():
        result["status"] = "pass"
    for result in bundle["fault_results"].values():
        result["status"] = "fail"
    for replacement in bundle["parameter_replacements"].values():
        replacement["decision"] = "retain_assumption"
    with pytest.raises(ValueError, match="G07_fault_campaign"):
        evaluate_rehearsal_evidence_bundle(
            bundle,
            archive_root=tmp_path,
        )


def test_economics_rejects_promotions_without_holdout_and_review(tmp_path: Path) -> None:
    bundle = _backed_template(
        economic_calibration_bundle_template(),
        tmp_path,
    )
    for fit in bundle["correlation_fits"].values():
        fit["holdout_status"] = "pass"
    for decision in bundle["promotion_decisions"].values():
        decision.update(
            {
                "decision": "promote_empirical",
                "holdout_result": "fail",
                "independent_review_status": "rejected",
            }
        )
    with pytest.raises(ValueError, match="empirical promotion requires"):
        evaluate_economic_calibration_bundle(
            bundle,
            archive_root=tmp_path,
        )


def test_process_graph_rejects_disconnected_declared_success(tmp_path: Path) -> None:
    bundle = _backed_template(process_closure_bundle_template(), tmp_path)
    bundle["graph_version"] = "fixture-v1"
    for result in bundle["gate_results"].values():
        result["status"] = "pass"
    with pytest.raises(ValueError, match="not reachable from a source lot"):
        evaluate_process_closure_bundle(
            bundle,
            archive_root=tmp_path,
        )


def test_evidence_evaluators_reject_malformed_containers() -> None:
    with pytest.raises(ValueError, match="must be an array"):
        evaluate_rehearsal_evidence_bundle(
            {
                **rehearsal_evidence_bundle_template(),
                "events": "not-an-array",
            }
        )
