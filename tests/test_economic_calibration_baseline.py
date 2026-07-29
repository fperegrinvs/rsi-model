"""The public economic calibration must retain every unsupported assumption."""

import json
from collections.abc import Mapping
from pathlib import Path

from rsimodel.economic_calibration import evaluate_economic_calibration_bundle
from rsimodel.economic_calibration_baseline import (
    economic_calibration_public_baseline_bundle,
    write_economic_calibration_public_baseline,
)

ROOT = Path(__file__).resolve().parents[1]


def test_public_economic_baseline_fails_holdouts_and_promotes_nothing() -> None:
    bundle = economic_calibration_public_baseline_bundle()
    assert bundle == economic_calibration_public_baseline_bundle()
    result = evaluate_economic_calibration_bundle(bundle, archive_root=ROOT)
    assert result["overall_status"] == "holdout_failed"
    fit_status = result["correlation_fit_status"]
    assert isinstance(fit_status, Mapping)
    assert set(fit_status.values()) == {"fail"}
    assert result["promoted_parameter_count"] == 0
    assert result["retained_assumption_count"] == 40


def test_gap_ledger_never_presents_missing_amounts_as_observed_zero() -> None:
    bundle = economic_calibration_public_baseline_bundle()
    events = bundle["cash_flow_events"]
    assert isinstance(events, list)
    assert events
    assert all(event["record_status"] == "evidence_missing" for event in events)
    assert all("not an observed zero" in event["quantity_and_units"] for event in events)
    assert {event["amount"] for event in events} == {0.0}


def test_public_economic_baseline_writer_matches_generator(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle.json"
    evaluation_path = tmp_path / "evaluation.json"
    assert write_economic_calibration_public_baseline(
        bundle_path=bundle_path,
        evaluation_path=evaluation_path,
    ) == (bundle_path, evaluation_path)
    assert json.loads(bundle_path.read_text(encoding="utf-8")) == (
        economic_calibration_public_baseline_bundle()
    )
    result = json.loads(evaluation_path.read_text(encoding="utf-8"))
    assert result["overall_status"] == "holdout_failed"
