from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import pytest

from rsimodel.precursor_telemetry import (
    load_precursor_telemetry,
    write_precursor_telemetry_csv,
)


def test_precursor_register_has_distinct_objects_and_evidence_boundaries() -> None:
    as_of, records = load_precursor_telemetry()
    assert as_of == "2026-07-28"
    assert [record["systemId"] for record in records] == [
        "karpathy_autoresearch",
        "darwin_godel_machine",
        "ai_scientist_v2",
        "sakana_rsi_lab_strategy",
    ]
    assert len({record["objectModified"] for record in records}) == len(records)
    assert all(record["doesNotDemonstrate"] for record in records)
    assert records[0]["attempts"] == ""
    assert records[-1]["sourceClass"] == "company_declared_strategy"


def test_precursor_csv_is_generated_from_source(tmp_path: Path) -> None:
    output = write_precursor_telemetry_csv(tmp_path / "telemetry.csv")
    rows = list(csv.DictReader(io.StringIO(output.read_text(encoding="utf-8"))))
    assert len(rows) == 4
    assert rows[1]["observedResult"].startswith("SWE-bench 20.0% to 50.0%")


def test_precursor_register_rejects_unknown_fields(tmp_path: Path) -> None:
    source = Path("params/observed_precursor_telemetry.json")
    value = json.loads(source.read_text(encoding="utf-8"))
    value["records"][0]["unsupported"] = True
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="field mismatch"):
        load_precursor_telemetry(invalid)
