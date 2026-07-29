"""Contracts for the dated SpaceXAI economic comparison."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import cast

import pytest

from rsimodel.lco import lco_earth, lco_space
from rsimodel.spacexai_economics import (
    CASE_ORDER,
    TABLE_NAMES,
    accepted_cost_per_million,
    claim_crosswalk_rows,
    discounted_capacity_years,
    economic_comparison_rows,
    load_spacexai_economic_registry,
    threshold_tornado_rows,
    write_spacexai_economic_artifacts,
)

ROOT = Path(__file__).resolve().parents[1]


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_registry_preserves_forecast_workload_and_company_gaps() -> None:
    registry = load_spacexai_economic_registry()
    assert registry.forecast["statementDate"] == "2026-01-22"
    assert registry.forecast["earliestBoundary"] == "2028-01-22"
    assert registry.forecast["latestBoundary"] == "2029-01-22"
    assert registry.workload.precision == "FP8"
    assert registry.workload.output_tokens_per_request == 256
    assert registry.independent_mass_range == (34.0, 59.0)
    company = {str(row["quantityId"]): row for row in registry.company_quantities}
    for quantity in (
        "cost_per_token",
        "compute_hardware_capex",
        "useful_life",
        "compute_availability",
        "communications_goodput",
        "replacement_cost",
        "useful_capacity_ramp",
    ):
        assert company[quantity]["status"] == "not_disclosed"
        assert company[quantity]["value"] is None


def test_registry_rejects_stale_source_snapshot(tmp_path: Path) -> None:
    raw = json.loads((ROOT / "params" / "spacexai_economic_case.json").read_text(encoding="utf-8"))
    raw["snapshotSha256"] = "0" * 64
    source = tmp_path / "case.json"
    source.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        load_spacexai_economic_registry(source)


def test_mass_override_exposes_independent_system_constraint() -> None:
    low = lco_space("leo_inference", total_mass_kg_per_kw=34.0)
    high = lco_space("leo_inference", total_mass_kg_per_kw=59.0)
    assert low.mass_kg_per_kw == pytest.approx(34.0)
    assert high.mass_kg_per_kw == pytest.approx(59.0)
    assert low.lco < high.lco
    with pytest.raises(ValueError, match="must be positive"):
        lco_space("leo_inference", total_mass_kg_per_kw=0.0)


def test_accepted_token_metric_is_inference_only_and_penalizes_goodput() -> None:
    registry = load_spacexai_economic_registry()
    lco = lco_earth("base").lco
    high_goodput = accepted_cost_per_million(lco, registry.workload, 0.95)
    low_goodput = accepted_cost_per_million(lco, registry.workload, 0.50)
    assert high_goodput < low_goodput
    with pytest.raises(ValueError, match="service_goodput"):
        accepted_cost_per_million(lco, registry.workload, 0.0)


def test_company_only_remains_noncomputable_and_hybrid_is_named() -> None:
    registry = load_spacexai_economic_registry()
    rows = economic_comparison_rows(registry)
    assert tuple(str(row["scenario_id"]) for row in rows) == CASE_ORDER
    company = rows[3]
    hybrid = rows[4]
    assert company["result_status"] == "not_computable_missing_company_inputs"
    assert company["lco_ratio_to_earth"] is None
    assert company["accepted_output_cost_ratio_to_earth"] is None
    assert company["forecast_window_status"] == ("not_computable_missing_commissioning_and_ramp")
    assert cast(float, hybrid["lco_ratio_to_earth"]) == pytest.approx(1.0877739293)
    assert cast(float, hybrid["accepted_output_cost_ratio_to_earth"]) > cast(
        float, hybrid["lco_ratio_to_earth"]
    )
    assert hybrid["forecast_window_status"] == "cost_parity_not_reached"


def test_schedule_values_time_explicitly_and_does_not_impute_company_ramp() -> None:
    registry = load_spacexai_economic_registry()
    company_schedule = registry.schedules["company_only"]
    assert discounted_capacity_years(3.0, company_schedule, registry.discount_rate) is None
    earth = discounted_capacity_years(
        3.0,
        registry.schedules["earth"],
        registry.discount_rate,
    )
    hybrid = discounted_capacity_years(
        3.0,
        registry.schedules["proponent_hybrid"],
        registry.discount_rate,
    )
    assert earth is not None and hybrid is not None
    assert earth > hybrid > 0.0


def test_tornado_separates_one_axis_from_joint_boundary() -> None:
    registry = load_spacexai_economic_registry()
    rows = threshold_tornado_rows(registry)
    assert len(rows) == 12
    assert all(row["scope"] == "one_at_a_time" for row in rows[:-1])
    assert rows[-1]["scope"] == "joint_not_probability"
    assert cast(float, rows[-1]["lco_ratio_at_base"]) < 1.0
    assert cast(float, rows[-1]["accepted_token_ratio_at_base"]) < 1.0
    by_parameter = {str(row["parameter"]): row for row in rows}
    assert by_parameter["launch_price"]["lco_parity_threshold"] is None
    assert by_parameter["delay_years"]["controls_2028_2029_window"] is True
    assert cast(float, by_parameter["delay_years"]["forecast_output_parity_threshold"]) < 2.0


def test_claim_crosswalk_covers_every_discriminating_observable() -> None:
    rows = claim_crosswalk_rows()
    assert len(rows) == 12
    joined = " ".join(str(value) for row in rows for value in row.values()).lower()
    for term in (
        "solar",
        "cooling",
        "launch",
        "manufacturing",
        "kg per delivered kw",
        "depreciation",
        "life",
        "goodput",
        "replacement",
        "commissioning",
        "terrestrial",
        "2028–january 2029",
    ):
        assert term in joined


def test_artifact_writer_emits_complete_tables_and_figure(tmp_path: Path) -> None:
    outputs = write_spacexai_economic_artifacts(tmp_path / "tables", tmp_path / "figures")
    assert len(outputs) == len(TABLE_NAMES) + 1
    assert all(path.is_file() and path.stat().st_size > 0 for path in outputs)
    company_rows = _rows(tmp_path / "tables" / "spacexai_proponent_case.csv")
    comparison_rows = _rows(tmp_path / "tables" / "spacexai_economic_comparison.csv")
    assert any(row["status"] == "not_disclosed" for row in company_rows)
    assert comparison_rows[3]["lco_ratio_to_earth"] == ""
    assert comparison_rows[4]["scenario_id"] == "spacexai_proponent_hybrid"
