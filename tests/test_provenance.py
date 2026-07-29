"""Publication-level source-provenance contract for r4.0."""

from pathlib import Path

import yaml

from rsimodel import load_anchors
from rsimodel.provenance import (
    PROVENANCE_OUTPUT,
    load_claim_provenance,
    render_claim_provenance_csv,
    validate_claim_provenance,
)

ROOT = Path(__file__).resolve().parents[1]


def test_every_non_assumption_anchor_has_verified_claim_level_provenance() -> None:
    register = load_claim_provenance()
    validate_claim_provenance(register, load_anchors())


def test_collective_s36_supports_no_non_assumption_anchor() -> None:
    register = load_claim_provenance()
    assert all(record["source_ref"] != "S36" for record in register["anchors"].values())


def test_s27_strategy_claims_are_pinned_to_sec_pages_or_slides() -> None:
    records = load_claim_provenance()["strategy_claims"]
    assert {
        "s27_declared_portfolio",
        "s27_lunar_ai_factories",
        "s27_early_stage_warning",
        "s27_terafab_framework",
        "s27_collision_avoidance",
    } <= set(records)
    assert all(record["source_ref"] == "S27" for record in records.values())
    assert all(
        "sec.gov/Archives/edgar/data/" in record["permanent_url_or_doi"]
        for record in records.values()
    )


def test_context_claims_have_exact_source_boundaries() -> None:
    records = load_claim_provenance()["context_claims"]
    expected = {
        "amodei_marginal_returns",
        "ai2027_scenario_and_revision_boundary",
        "anthropic_execution_direction_gap",
        "trammell_korinek_growth_conditions",
        "metr_task_horizon_boundary",
        "rsi_survey_method_boundary",
        "ai2040_governance_scenario_boundary",
        "autoresearch_protocol_boundary",
        "dgm_observed_agent_self_modification",
        "ai_scientist_v2_selection_boundary",
        "sakana_rsi_lab_declared_transition",
        "tesla_operating_capability_boundary",
        "tesla_recycling_boundary",
        "portfolio_sector_crosswalk_boundary",
        "orbital_ai_competitor_landscape_boundary",
        "spacexai_scenario_registry_boundary",
        "spacexai_affiliate_control_boundary",
        "orbital_ai_closure_stack_boundary",
        "openai_preparedness_ai_self_improvement_thresholds",
        "openai_paperbench_replication_boundary",
        "openai_gpt56_ai_self_improvement_suite",
        "openai_external_testing_boundary",
        "deepmind_technical_agi_feedback_boundary",
        "deepmind_fsf31_ml_rnd_thresholds",
        "spacexai_cost_per_token_boundary",
        "musk_orbital_ai_cost_forecast",
    }
    assert expected == set(records)
    assert all(record["status"] == "verified" for record in records.values())
    assert all(record["locator"] for record in records.values())
    assert all(record["permanent_url_or_doi"].startswith("https://") for record in records.values())


def test_analyst_constructed_ranges_are_explicit_assumptions() -> None:
    anchors = load_anchors()
    names = {
        "delta.catastrophic_leo",
        "delta.obsolescence_earth_adv",
        "launch.leo_per_kg",
        "power_systems.radiator_kg_per_kw",
        "compute.hw_per_kw_it",
        "compute.life_years_space",
        "earth.dc_capex_per_kw_it",
        "earth.pue",
    }
    assert all(anchors[name]["source_class"] == "ASSUMPTION" for name in names)


def test_generated_claim_provenance_table_is_current() -> None:
    assert PROVENANCE_OUTPUT.read_text(encoding="utf-8") == (render_claim_provenance_csv())


def test_claim_provenance_yaml_has_no_implicit_dates_or_numbers() -> None:
    # YAML 1.1 can silently coerce unquoted date scalars into date objects.
    # Keeping publication fields as strings makes CSV output deterministic.
    raw = yaml.safe_load((ROOT / "params" / "claim_provenance.yaml").read_text(encoding="utf-8"))
    for section in ("anchors", "strategy_claims", "context_claims"):
        for record in raw[section].values():
            assert isinstance(record["date"], str)
            assert isinstance(record["extracted_value"], str)
