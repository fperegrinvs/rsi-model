"""Coverage policy distinguishes model-critical code from presentation glue."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rsimodel.coverage_gate import (
    AGGREGATE_FLOOR,
    CRITICAL_MODULE_FLOORS,
    coverage_failures,
    coverage_main,
)


def _report(percent: float = 100.0) -> dict[str, object]:
    return {
        "totals": {"percent_covered": percent},
        "files": {
            module: {"summary": {"percent_covered": percent}} for module in CRITICAL_MODULE_FLOORS
        },
    }


def test_coverage_policy_accepts_complete_report(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps(_report()), encoding="utf-8")
    assert coverage_main([str(report)]) == 0
    assert "PASS coverage policy" in capsys.readouterr().out


def test_coverage_policy_reports_all_floor_failures() -> None:
    document = _report(AGGREGATE_FLOOR - 1.0)
    files = document["files"]
    assert isinstance(files, dict)
    missing = next(iter(CRITICAL_MODULE_FLOORS))
    files.pop(missing)
    failures = coverage_failures(document)
    assert any("aggregate coverage" in failure for failure in failures)
    assert any(missing in failure for failure in failures)


def test_coverage_cli_rejects_malformed_or_incomplete_report(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    malformed = tmp_path / "malformed.json"
    malformed.write_text("[]", encoding="utf-8")
    assert coverage_main([str(malformed)]) == 2
    assert "root must be an object" in capsys.readouterr().err

    incomplete = tmp_path / "incomplete.json"
    incomplete.write_text(json.dumps({"totals": {}}), encoding="utf-8")
    assert coverage_main([str(incomplete)]) == 2
    assert "totals and files" in capsys.readouterr().err
