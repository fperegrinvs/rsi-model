"""Venue-selection and submission-readiness contract tests."""
import csv
import io
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.publication import (
    load_publication_targets,
    manuscript_metrics,
    publication_authorization_gates,
    publication_authorization_template,
    render_publication_readiness_csv,
    validate_publication_targets,
)


def test_three_papers_have_explicit_target_and_fallback_venues():
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


def test_readiness_fails_closed_on_author_and_portal_requirements():
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


def test_acta_highlight_limits_and_space_policy_anonymization_are_encoded():
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


def test_each_paper_meets_its_nontrivial_reference_floor():
    targets = load_publication_targets()
    for paper in targets["papers"].values():
        metrics = manuscript_metrics(ROOT / paper["manuscript"])
        assert metrics["has_citations"]
        assert metrics["references_resolved"]
        assert metrics["reference_count"] >= paper["minimum_references"]


def test_external_publication_authorization_binds_exact_files_and_approval():
    record = publication_authorization_template()
    assert not all(
        gate.passed for gate in publication_authorization_gates(record)
    )
    for approval in record["papers"].values():
        for item in approval["author_confirmations"].values():
            item.update({
                "status": "confirmed",
                "value_or_attestation": "confirmed in external author record",
            })
        for item in approval["submission_actions"].values():
            item.update({
                "status": "completed",
                "evidence_or_note": "completed; evidence retained externally",
            })
        approval.update({
            "final_submission_approved": True,
            "approver": "Authorized corresponding author",
            "approval_timestamp_utc": "2026-07-28T12:00:00Z",
            "signature_or_attestation_id": "signed-record-001",
        })
    gates = publication_authorization_gates(record)
    release_coordinate_gates = [
        gate
        for gate in gates
        if "immutable_release_coordinates" in gate.name
    ]
    assert release_coordinate_gates
    assert all(not gate.passed for gate in release_coordinate_gates)
    assert all(
        gate.passed
        for gate in gates
        if gate not in release_coordinate_gates
    )


def test_authorization_rejects_blanket_not_applicable_bypass():
    record = publication_authorization_template()
    for approval in record["papers"].values():
        for item in approval["author_confirmations"].values():
            item.update({
                "status": "not_applicable",
                "value_or_attestation": "claimed N/A",
            })
        for item in approval["submission_actions"].values():
            item.update({
                "status": "not_applicable",
                "evidence_or_note": "claimed N/A",
            })
    failed = {
        gate.name
        for gate in publication_authorization_gates(record)
        if not gate.passed
    }
    assert any("author_confirmation" in name for name in failed)
    assert any("submission_action" in name for name in failed)


def test_data_statements_are_present_but_release_coordinates_pending():
    targets = load_publication_targets()
    for paper in targets["papers"].values():
        metrics = manuscript_metrics(ROOT / paper["manuscript"])
        assert metrics["has_data_statement"]
        assert not metrics["data_statement_final"]
        assert not metrics["immutable_release_coordinates"]


def test_committed_publication_readiness_table_is_current():
    target = ROOT / "outputs" / "integrated" / "tables" / (
        "publication_readiness.csv"
    )
    assert target.read_text(encoding="utf-8") == (
        render_publication_readiness_csv()
    )
