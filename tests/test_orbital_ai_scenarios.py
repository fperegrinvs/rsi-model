"""Contracts for the dated orbital-AI scenario and closure registries."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pytest

from rsimodel import draw_anchors, load_anchors
from rsimodel.lco import lco_earth, lco_space
from rsimodel.orbital_ai_scenarios import (
    CLOSURE_LAYER_ORDER,
    LCO_COMPONENT_HATCHES,
    LCO_SCENARIO_DISPLAY_LABELS,
    PROGRAM_ORDER,
    RATIO_CASE_LABELS,
    RATIO_LINE_STYLES,
    SCENARIO_ORDER,
    SIMULATION_ORDER,
    expanded_closure_rows,
    load_orbital_ai_registry,
    scenario_anchor_tree,
    write_orbital_ai_scenario_csvs,
)

ROOT = Path(__file__).resolve().parents[1]


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_registry_has_exact_tracks_inputs_snapshots_and_boundaries() -> None:
    registry = load_orbital_ai_registry()
    assert tuple(record["scenarioId"] for record in registry.scenarios) == SCENARIO_ORDER
    assert tuple(record["simulationId"] for record in registry.simulations) == SIMULATION_ORDER
    assert tuple(record["programId"] for record in registry.programs) == PROGRAM_ORDER
    assert tuple(record["layerId"] for record in registry.layers) == CLOSURE_LAYER_ORDER
    assert len(registry.inputs) == 18
    assert all(record["maturityState"] != "observed_operation" for record in registry.inputs)
    assert all(
        record["evidenceClass"] == "ASSUMPTION"
        for record in registry.inputs
        if record["maturityState"] == "hybrid_completion"
    )
    assert all((ROOT / record["sourceSnapshot"]).is_file() for record in registry.inputs)
    assert "not controlled" in registry.programs[0]["boundary"]


def test_named_scenario_anchor_tree_preserves_published_values() -> None:
    tree = scenario_anchor_tree()
    assert set(tree) == {"starmind", "aspirations"}
    assert tree["starmind"]["compute_payload_kw_peak"]["value"] == 150.0
    assert tree["starmind"]["vehicle_mass_kg_per_average_kw"]["low"] == 14.285714
    assert tree["starmind"]["vehicle_mass_kg_per_average_kw"]["high"] == 17.857143
    assert tree["aspirations"]["starship_leo_cost_per_kg"]["value"] == 185.0
    assert tree["aspirations"]["starmind_life_years"]["source_class"] == "ASSUMPTION"


def test_named_scenarios_do_not_change_generic_draws_or_central_lco(
    tmp_path: Path,
) -> None:
    # The generic YAML has no named SpaceXAI groups.  Adding the registry is
    # draw-stable because every draw is keyed by anchor name rather than list order.
    generic_yaml = tmp_path / "generic-anchors.yaml"
    generic_yaml.write_bytes((ROOT / "params" / "anchors.yaml").read_bytes())
    generic = load_anchors(generic_yaml)
    combined = load_anchors()
    assert set(generic) < set(combined)
    generic_draws = draw_anchors(generic, np.random.default_rng(20260728))
    combined_draws = draw_anchors(combined, np.random.default_rng(20260728))
    assert all(generic_draws[name] == combined_draws[name] for name in generic)
    assert lco_space("leo_inference").lco == pytest.approx(77559.294109303)
    assert lco_earth("base").lco == pytest.approx(14669.404064368)


def test_coverage_declares_every_relevant_output_and_none_are_missing() -> None:
    registry = load_orbital_ai_registry()
    output_paths = [
        output_path
        for simulation in registry.simulations
        for output_path in simulation["outputPaths"]
    ]
    assert len(set(output_paths)) <= len(output_paths)
    assert all((ROOT / output_path).is_file() for output_path in output_paths)
    for simulation in registry.simulations:
        for prefix in (
            "generic",
            "independent",
            "disclosed",
            "aspiration",
            "hybrid",
        ):
            assert simulation[f"{prefix}Status"]  # type: ignore[literal-required]
            assert simulation[f"{prefix}Boundary"]  # type: ignore[literal-required]


def test_closure_matrix_expands_negative_evidence_without_conflating_tesla() -> None:
    registry = load_orbital_ai_registry()
    rows = expanded_closure_rows(registry)
    assert len(rows) == len(PROGRAM_ORDER) * len(CLOSURE_LAYER_ORDER) == 72
    assert all(
        not capability["underCommonControl"]
        for _, _, capability in rows
        if capability is not None and "Tesla" in capability["responsibleLegalEntity"]
    )
    assert not any(
        capability is not None and capability["offWorldReproductivelyClosed"]
        for _, _, capability in rows
    )
    spacexai = [
        capability
        for program, _, capability in rows
        if program["programId"] == "spacexai_bounded_ecosystem"
    ]
    assert sum(capability is not None for capability in spacexai) == 17
    assert spacexai[-1] is None


def test_generated_views_preserve_order_metadata_and_zero_closure(
    tmp_path: Path,
) -> None:
    outputs = tuple(
        tmp_path / name
        for name in ("inputs.csv", "coverage.csv", "stack.csv", "summary.csv", "results.csv")
    )
    write_orbital_ai_scenario_csvs(*outputs)
    input_rows = _rows(outputs[0])
    coverage_rows = _rows(outputs[1])
    stack_rows = _rows(outputs[2])
    summary_rows = _rows(outputs[3])
    result_rows = _rows(outputs[4])

    assert len(input_rows) == 18
    assert len(stack_rows) == 72
    assert [row["program_id"] for row in summary_rows] == list(PROGRAM_ORDER)
    assert summary_rows[0]["breadth_rank"] == "1"
    assert summary_rows[0]["evidenced_layers"] == "17"
    assert summary_rows[0]["minimum_cut_gaps"] == "capital_equipment_reproduction"
    assert all(row["dependency_aware_off_world_closure"] == "false" for row in summary_rows)
    assert [row["scenario_id"] for row in result_rows] == sorted(
        (row["scenario_id"] for row in result_rows),
        key=SCENARIO_ORDER.index,
    )
    assert all(
        row["evidence_class"]
        and row["source_snapshot"]
        and row["parameter_completeness"]
        and row["boundary"]
        for row in result_rows
    )
    assert {row["simulation_id"] for row in coverage_rows} == set(SIMULATION_ORDER)
    assert all(row["output_path"].startswith("outputs/") for row in coverage_rows)


def test_named_plot_labels_and_non_color_encodings_are_stable() -> None:
    assert LCO_SCENARIO_DISPLAY_LABELS["starmind_ai1"] == ("AI1 disclosed\n(company statement)")
    assert LCO_SCENARIO_DISPLAY_LABELS["starmind_ai1_aspirational"] == (
        "AI1 targets +\nmodel assumptions"
    )
    assert RATIO_CASE_LABELS["starmind_ai1"] == "SpaceXAI AI1 disclosed design"
    assert len(set(LCO_COMPONENT_HATCHES)) == len(LCO_COMPONENT_HATCHES) == 5
    assert len(set(RATIO_LINE_STYLES)) == len(RATIO_LINE_STYLES) == 4
