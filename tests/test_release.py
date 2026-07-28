"""Deterministic tests for candidate and final-release metadata gates."""
import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.release import (
    release_authorization_gates,
    release_authorization_template,
    repository_gates,
    validate_publication_values,
)


def test_current_repository_passes_deterministic_candidate_gates():
    gates = repository_gates(ROOT, "candidate")
    assert gates
    assert all(gate.passed for gate in gates)


def test_publication_values_reject_concept_doi_and_mutable_main():
    with pytest.raises(ValueError, match="concept DOI"):
        validate_publication_values(
            "2026-07-28",
            "10.5281/zenodo.21619447",
            "https://example.com/releases/r4.0",
        )
    with pytest.raises(ValueError, match="immutable"):
        validate_publication_values(
            "2026-07-28",
            "10.5281/zenodo.99999999",
            "https://github.com/fperegrinvs/rsi-model/blob/main",
        )


def test_publication_mode_requires_explicit_metadata():
    with pytest.raises(ValueError, match="requires RELEASE_DATE"):
        repository_gates(ROOT, "publication")


def test_external_release_authorization_is_exact_and_fails_from_template(
    tmp_path,
):
    head = "a" * 40
    canonical = "https://zenodo.org/records/99999999"
    template = release_authorization_template()
    gates = release_authorization_gates(
        template,
        head_commit=head,
        release_date="2026-07-28",
        version_doi="10.5281/zenodo.99999999",
        canonical_url=canonical,
    )
    assert not all(gate.passed for gate in gates)

    ci_url = (
        "https://github.com/fperegrinvs/rsi-model/actions/runs/123456"
    )
    ci_evidence = tmp_path / "ci.json"
    ci_evidence.write_text(
        json.dumps({
            "repository": "https://github.com/fperegrinvs/rsi-model",
            "head_sha": head,
            "conclusion": "success",
            "html_url": ci_url,
        }),
        encoding="utf-8",
    )
    attestation = tmp_path / "authorization.sigstore"
    attestation.write_bytes(b"signed release authorization fixture")
    completed = {
        **template,
        "final_source_approved": True,
        "approved_commit": head,
        "author_or_release_manager": "Authorized release manager",
        "approval_timestamp_utc": "2026-07-28T12:00:00Z",
        "linux_ci_run_url": ci_url,
        "linux_ci_repository": "https://github.com/fperegrinvs/rsi-model",
        "linux_ci_commit": head,
        "linux_ci_conclusion": "success",
        "linux_ci_evidence_path": ci_evidence.name,
        "linux_ci_evidence_sha256": hashlib.sha256(
            ci_evidence.read_bytes()
        ).hexdigest(),
        "archive_record_url": "https://zenodo.org/records/99999999",
        "release_date": "2026-07-28",
        "version_doi": "10.5281/zenodo.99999999",
        "canonical_url": canonical,
        "attestation_path": attestation.name,
        "attestation_sha256": hashlib.sha256(
            attestation.read_bytes()
        ).hexdigest(),
    }
    assert all(
        gate.passed
        for gate in release_authorization_gates(
            completed,
            head_commit=head,
            release_date="2026-07-28",
            version_doi="10.5281/zenodo.99999999",
            canonical_url=canonical,
            evidence_root=tmp_path,
        )
    )


def test_release_authorization_rejects_url_only_claims(tmp_path):
    head = "a" * 40
    record = {
        **release_authorization_template(),
        "final_source_approved": True,
        "approved_commit": head,
        "author_or_release_manager": "release manager",
        "approval_timestamp_utc": "2026-07-28T12:00:00Z",
        "linux_ci_run_url": "https://example.com/actions/runs/1",
        "archive_record_url": "https://example.com/archive/99999999",
        "release_date": "2026-07-28",
        "version_doi": "10.5281/zenodo.99999999",
        "canonical_url": "https://example.com/archive/99999999",
    }
    gates = release_authorization_gates(
        record,
        head_commit=head,
        release_date="2026-07-28",
        version_doi="10.5281/zenodo.99999999",
        canonical_url=record["canonical_url"],
        evidence_root=tmp_path,
    )
    failed = {gate.name for gate in gates if not gate.passed}
    assert {"linux_ci_evidence", "archive_record", "authorization_canonical_url"} <= failed
