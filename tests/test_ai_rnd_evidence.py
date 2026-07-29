from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import pytest

from rsimodel.ai_rnd_evidence import (
    REQUIRED_GATES,
    REQUIRED_STAGES,
    load_ai_rnd_evidence,
    write_ai_rnd_evidence_csvs,
)


def test_registry_has_complete_stage_and_gate_boundaries() -> None:
    registry = load_ai_rnd_evidence()
    assert set(registry["stages"]) == REQUIRED_STAGES
    assert set(registry["analyticGates"]) == REQUIRED_GATES
    entries = {entry["evidenceId"]: entry for entry in registry["entries"]}
    assert {
        "openai_preparedness_high_ai_self_improvement",
        "openai_preparedness_critical_ai_self_improvement",
        "openai_paperbench_v1",
        "openai_gpt56_internal_research_debugging",
        "openai_gpt56_kernelgen_1p",
        "openai_gpt56_nanogpt",
        "openai_gpt56_posttrainbench_lite",
        "openai_gpt56_mlebench_revised",
        "metr_time_horizon_1_1_gpt56_sol",
        "openai_gpt56_below_high_assessment",
        "deepmind_technical_agi_safety_feedback",
        "deepmind_fsf31_rnd_acceleration_level_1",
        "deepmind_fsf31_rnd_automation_level_1",
        "deepmind_fsf31_internal_public_boundary",
    } <= set(entries)
    assert entries["openai_paperbench_v1"]["stages"] == [
        "hypothesis_generation",
        "implementation",
        "experiment_execution",
        "debugging",
        "evaluation",
    ]
    assert entries["deepmind_fsf31_rnd_acceleration_level_1"]["analyticGates"] == [
        "realized_rnd_acceleration"
    ]
    assert all(entry["coefficientUse"] == "none_observational_only" for entry in entries.values())
    assert all(entry["crossLabComparison"] == "not_permitted" for entry in entries.values())


def test_registry_requires_full_evaluation_context(tmp_path: Path) -> None:
    source = Path("params/ai_rnd_evidence_registry.json")
    value = json.loads(source.read_text(encoding="utf-8"))
    value["entries"][4]["harness"] = ""
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="string fields must all be non-empty"):
        load_ai_rnd_evidence(invalid)


def test_component_measurement_rejects_unqualified_rsi_claim(tmp_path: Path) -> None:
    source = Path("params/ai_rnd_evidence_registry.json")
    value = json.loads(source.read_text(encoding="utf-8"))
    value["entries"][4]["publishedStatus"] = "This is an RSI benchmark."
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="unqualified phrase"):
        load_ai_rnd_evidence(invalid)


def test_generated_tables_preserve_evidence_classes_and_normalize_crosswalk(
    tmp_path: Path,
) -> None:
    benchmark, crosswalk = write_ai_rnd_evidence_csvs(
        tmp_path / "benchmark.csv",
        tmp_path / "crosswalk.csv",
    )
    benchmark_rows = list(csv.DictReader(io.StringIO(benchmark.read_text(encoding="utf-8"))))
    crosswalk_rows = list(csv.DictReader(io.StringIO(crosswalk.read_text(encoding="utf-8"))))
    assert len(benchmark_rows) == len(load_ai_rnd_evidence()["entries"])
    assert {row["evidenceClass"] for row in benchmark_rows} >= {
        "company_framework",
        "company_self_evaluation_nonpublic_tasks",
        "external_evaluation",
        "scenario_assumption",
    }
    assert {row["mappingType"] for row in crosswalk_rows} == {
        "loop_stage",
        "analytic_gate",
    }
    assert all(row["coefficientUse"] == "none_observational_only" for row in crosswalk_rows)
