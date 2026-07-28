"""Publication-level source-provenance contract for r4.0."""
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel import load_anchors
from rsimodel.provenance import (
    PROVENANCE_OUTPUT,
    load_claim_provenance,
    render_claim_provenance_csv,
    validate_claim_provenance,
)

def test_every_non_assumption_anchor_has_verified_claim_level_provenance():
    register = load_claim_provenance()
    validate_claim_provenance(register, load_anchors())


def test_collective_s36_supports_no_non_assumption_anchor():
    register = load_claim_provenance()
    assert all(
        record["source_ref"] != "S36"
        for record in register["anchors"].values()
    )


def test_s27_strategy_claims_are_pinned_to_sec_pages_or_slides():
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


def test_analyst_constructed_ranges_are_explicit_assumptions():
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


def test_generated_claim_provenance_table_is_current():
    assert PROVENANCE_OUTPUT.read_text(encoding="utf-8") == (
        render_claim_provenance_csv()
    )


def test_claim_provenance_yaml_has_no_implicit_dates_or_numbers():
    # YAML 1.1 can silently coerce unquoted date scalars into date objects.
    # Keeping publication fields as strings makes CSV output deterministic.
    raw = yaml.safe_load(
        (ROOT / "params" / "claim_provenance.yaml").read_text(encoding="utf-8")
    )
    for section in ("anchors", "strategy_claims"):
        for record in raw[section].values():
            assert isinstance(record["date"], str)
            assert isinstance(record["extracted_value"], str)
