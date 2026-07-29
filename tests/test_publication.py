"""Venue-selection and submission-readiness contract tests."""

import csv
import io
from pathlib import Path

from rsimodel.publication import (
    load_publication_targets,
    manuscript_metrics,
    publication_authorization_gates,
    publication_authorization_template,
    render_publication_readiness_csv,
    validate_publication_targets,
)

ROOT = Path(__file__).resolve().parents[1]


def test_three_papers_have_explicit_target_and_fallback_venues() -> None:
    targets = load_publication_targets()
    validate_publication_targets(targets)
    assert set(targets["papers"]) == {
        "technical",
        "economics",
        "strategy_governance",
    }
    assert all(
        paper[route]["official_url"].startswith("https://")
        for paper in targets["papers"].values()
        for route in ("target", "fallback")
    )


def test_readiness_fails_closed_on_author_and_portal_requirements() -> None:
    rows = list(csv.DictReader(io.StringIO(render_publication_readiness_csv())))
    assert rows
    statuses = {row["status"] for row in rows}
    assert "author_confirmation_pending" in statuses
    assert "submission_action_pending" in statuses
    assert "portal_recheck_pending" in statuses
    assert "release_pending" in statuses
    assert "contingency_not_selected" in statuses
    assert "content_expansion_pending" not in statuses
    assert all(row["status"] != "submission_ready" for row in rows)


def test_acta_highlight_limits_and_space_policy_anonymization_are_encoded() -> None:
    papers = load_publication_targets()["papers"]
    assert all(paper["selected_route"] == "target" for paper in papers.values())
    acta = papers["technical"]["target"]
    assert acta["highlights"] == {
        "required": True,
        "min_items": 3,
        "max_items": 5,
        "max_chars_each": 85,
    }
    assert papers["economics"]["target"]["review"] == "double_anonymized"
    assert papers["economics"]["target"]["separate_title_page"] is True
    astropolitics = papers["strategy_governance"]["target"]
    assert astropolitics["article_type"] == "Article"
    assert astropolitics["abstract_max_words"] == 200
    assert (astropolitics["keywords_min"], astropolitics["keywords_max"]) == (3, 5)
    assert (astropolitics["word_count_min"], astropolitics["word_count_max"]) == (
        5000,
        10000,
    )
    assert astropolitics["reference_style"] == "chicago_author_date"
    assert astropolitics.get("portal_confirmation_required") == (
        "peer_review_anonymization",
        "title_page_packaging",
    )


def test_selected_routes_use_their_required_reference_styles() -> None:
    targets = load_publication_targets()
    expected = {
        "technical": "numbered",
        "economics": "numbered",
        "strategy_governance": "author_date",
    }
    for paper_id, paper in targets["papers"].items():
        metrics = manuscript_metrics(ROOT / paper["manuscript"])
        assert metrics["citation_style"] == expected[paper_id]


def test_selected_routes_have_no_repository_controlled_content_defects() -> None:
    rows = csv.DictReader(io.StringIO(render_publication_readiness_csv()))
    selected = [row for row in rows if row["record_type"] == "machine_conformance"]
    assert selected
    assert {row["status"] for row in selected} <= {
        "pass",
        "release_pending",
        "portal_recheck_pending",
    }
    assert {row["id"] for row in selected if row["status"] == "portal_recheck_pending"} == {
        "strategy_governance.target.peer_review_anonymization",
        "strategy_governance.target.title_page_packaging",
    }


def test_submission_papers_do_not_narrate_previous_draft_states() -> None:
    targets = load_publication_targets()
    prohibited = (
        "earlier draft",
        "previous version",
        "former scalar",
        "former incomplete",
        "relation used in",
        "is therefore retired",
    )
    for paper in targets["papers"].values():
        text = (ROOT / paper["manuscript"]).read_text(encoding="utf-8").lower()
        assert not any(phrase in text for phrase in prohibited)


def test_publication_audit_and_requirement_snapshot_are_present() -> None:
    audit = ROOT / "docs" / "reviews" / "publication-package-audit-2026-07-29.md"
    snapshot = ROOT / "docs" / "sources" / "publication-venue-requirements-2026-07-29.md"
    assert audit.is_file()
    assert snapshot.is_file()
    audit_text = audit.read_text(encoding="utf-8")
    for claim_id in ("T-C01", "E-C01", "S-C01"):
        assert claim_id in audit_text


def test_technical_paper_key_results_match_generated_scenario_table() -> None:
    paper = (ROOT / "papers" / "TECHNICAL_PAPER_r4.0.md").read_text(encoding="utf-8")
    table = ROOT / "outputs" / "integrated" / "tables" / "scenario_summary.csv"
    rows = {
        row["scenario"]: row
        for row in csv.DictReader(io.StringIO(table.read_text(encoding="utf-8")))
    }
    expected_seed_masses = {
        "terrestrial_rehearsal": "207 t",
        "lunar_strategic_material_bridge": "217 t",
        "moon_asteroid_network": "188 t",
    }
    for scenario, rendered in expected_seed_masses.items():
        assert round(float(rows[scenario]["seed_mass_t"])) == int(rendered.split()[0])
        assert rendered in paper
    network = rows["moon_asteroid_network"]
    assert f"{float(network['operating_cells_year40']):.2f}" in paper
    assert f"{float(network['aggregate_doubling_year']):.2f}" in paper


def test_each_paper_meets_its_nontrivial_reference_floor() -> None:
    targets = load_publication_targets()
    for paper in targets["papers"].values():
        metrics = manuscript_metrics(ROOT / paper["manuscript"])
        assert metrics["has_citations"]
        assert metrics["references_resolved"]
        assert metrics["reference_count"] >= paper["minimum_references"]


def test_external_publication_authorization_binds_exact_files_and_approval() -> None:
    record = publication_authorization_template()
    assert not all(gate.passed for gate in publication_authorization_gates(record))
    for approval in record["papers"].values():
        for item in approval["author_confirmations"].values():
            item.update(
                {
                    "status": "confirmed",
                    "value_or_attestation": "confirmed in external author record",
                }
            )
        for item in approval["submission_actions"].values():
            item.update(
                {
                    "status": "completed",
                    "evidence_or_note": "completed; evidence retained externally",
                }
            )
        approval.update(
            {
                "final_submission_approved": True,
                "approver": "Authorized corresponding author",
                "approval_timestamp_utc": "2026-07-28T12:00:00Z",
                "signature_or_attestation_id": "signed-record-001",
            }
        )
    gates = publication_authorization_gates(record)
    release_coordinate_gates = [
        gate for gate in gates if "immutable_release_coordinates" in gate.name
    ]
    assert release_coordinate_gates
    assert all(not gate.passed for gate in release_coordinate_gates)
    assert all(gate.passed for gate in gates if gate not in release_coordinate_gates)


def test_authorization_rejects_blanket_not_applicable_bypass() -> None:
    record = publication_authorization_template()
    for approval in record["papers"].values():
        for item in approval["author_confirmations"].values():
            item.update(
                {
                    "status": "not_applicable",
                    "value_or_attestation": "claimed N/A",
                }
            )
        for item in approval["submission_actions"].values():
            item.update(
                {
                    "status": "not_applicable",
                    "evidence_or_note": "claimed N/A",
                }
            )
    failed = {gate.name for gate in publication_authorization_gates(record) if not gate.passed}
    assert any("author_confirmation" in name for name in failed)
    assert any("submission_action" in name for name in failed)


def test_data_statements_are_present_but_release_coordinates_pending() -> None:
    targets = load_publication_targets()
    for paper in targets["papers"].values():
        metrics = manuscript_metrics(ROOT / paper["manuscript"])
        assert metrics["has_data_statement"]
        assert not metrics["data_statement_final"]
        assert not metrics["immutable_release_coordinates"]


def test_committed_publication_readiness_table_is_current() -> None:
    target = ROOT / "outputs" / "integrated" / "tables" / ("publication_readiness.csv")
    assert target.read_text(encoding="utf-8") == (render_publication_readiness_csv())
