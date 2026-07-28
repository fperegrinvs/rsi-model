"""Fail-closed r4.0 candidate and immutable-publication preflight."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml

from rsimodel.manifests import verify_manifest, verify_release_manifest

CONCEPT_DOI = "10.5281/zenodo.21619447"
RELEASE_AUTHORIZATION_SCHEMA = "r4.0-release-authorization-v1"
REPOSITORY_URL = "https://github.com/fperegrinvs/rsi-model"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class Gate:
    name: str
    passed: bool
    detail: str


def release_authorization_template() -> dict[str, Any]:
    """Return an external authorization template that cannot yet pass."""
    return {
        "schema": RELEASE_AUTHORIZATION_SCHEMA,
        "version": "r4.0",
        "final_source_approved": False,
        "approved_commit": None,
        "author_or_release_manager": None,
        "approval_timestamp_utc": None,
        "linux_ci_run_url": None,
        "linux_ci_repository": REPOSITORY_URL,
        "linux_ci_commit": None,
        "linux_ci_conclusion": None,
        "linux_ci_evidence_path": None,
        "linux_ci_evidence_sha256": None,
        "archive_record_url": None,
        "release_date": None,
        "version_doi": None,
        "canonical_url": None,
        "attestation_path": None,
        "attestation_sha256": None,
    }


def _verified_file(
    evidence_root: Path | None,
    relative_value: Any,
    expected: Any,
) -> tuple[bool, str, bytes | None]:
    if evidence_root is None:
        return False, "evidence_root is required", None
    if not isinstance(relative_value, str) or not relative_value:
        return False, "missing relative evidence path", None
    relative = Path(relative_value)
    if relative.is_absolute():
        return False, "evidence path must be relative", None
    root = evidence_root.resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        return False, "evidence path escapes evidence_root", None
    if not target.is_file():
        return False, f"evidence file missing: {relative}", None
    if not isinstance(expected, str) or not SHA256_RE.fullmatch(expected):
        return False, "evidence sha256 is invalid", None
    content = target.read_bytes()
    actual = hashlib.sha256(content).hexdigest()
    if actual != expected:
        return False, f"evidence sha256 mismatch: {actual}", None
    return True, f"{relative}; sha256={actual}", content


def release_authorization_gates(
    record: dict[str, Any],
    *,
    head_commit: str,
    release_date: str,
    version_doi: str,
    canonical_url: str,
    evidence_root: Path | None = None,
) -> list[Gate]:
    """Validate external approval against the exact publication candidate."""
    timestamp = record.get("approval_timestamp_utc")
    timestamp_valid = False
    if isinstance(timestamp, str):
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            timestamp_valid = parsed.tzinfo is not None
        except ValueError:
            pass
    approved_commit = record.get("approved_commit")
    ci_evidence_valid, ci_evidence_detail, ci_content = _verified_file(
        evidence_root,
        record.get("linux_ci_evidence_path"),
        record.get("linux_ci_evidence_sha256"),
    )
    ci_payload: dict[str, Any] = {}
    if ci_evidence_valid and ci_content is not None:
        try:
            candidate = json.loads(ci_content)
            if isinstance(candidate, dict):
                ci_payload = candidate
            else:
                ci_evidence_valid = False
                ci_evidence_detail = "CI evidence must be a JSON object"
        except (UnicodeDecodeError, json.JSONDecodeError):
            ci_evidence_valid = False
            ci_evidence_detail = "CI evidence must be valid JSON"
    ci_url = record.get("linux_ci_run_url")
    expected_ci_url = re.compile(
        r"^https://github\.com/fperegrinvs/rsi-model/actions/runs/\d+"
        r"(?:/attempts/\d+)?$"
    )
    ci_claims_valid = (
        record.get("linux_ci_repository") == REPOSITORY_URL
        and record.get("linux_ci_commit") == head_commit
        and record.get("linux_ci_conclusion") == "success"
        and isinstance(ci_url, str)
        and bool(expected_ci_url.fullmatch(ci_url))
        and ci_payload.get("repository") == REPOSITORY_URL
        and ci_payload.get("head_sha") == head_commit
        and ci_payload.get("conclusion") == "success"
        and ci_payload.get("html_url") == ci_url
    )
    attestation_valid, attestation_detail, _ = _verified_file(
        evidence_root,
        record.get("attestation_path"),
        record.get("attestation_sha256"),
    )
    version_record_id = version_doi.rsplit(".", 1)[-1]
    expected_archive_urls = {
        f"https://zenodo.org/records/{version_record_id}",
        f"https://www.zenodo.org/records/{version_record_id}",
    }
    archive_url = record.get("archive_record_url")
    canonical_allowed = expected_archive_urls | {
        f"https://doi.org/{version_doi}",
    }
    return [
        Gate(
            "authorization_schema",
            record.get("schema") == RELEASE_AUTHORIZATION_SCHEMA,
            str(record.get("schema")),
        ),
        Gate(
            "authorization_version",
            record.get("version") == "r4.0",
            str(record.get("version")),
        ),
        Gate(
            "final_source_approved",
            record.get("final_source_approved") is True,
            str(record.get("final_source_approved")),
        ),
        Gate(
            "authorized_commit_at_head",
            isinstance(approved_commit, str)
            and bool(re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", approved_commit))
            and approved_commit == head_commit,
            str(approved_commit),
        ),
        Gate(
            "authorization_identity",
            bool(record.get("author_or_release_manager")),
            str(record.get("author_or_release_manager")),
        ),
        Gate(
            "authorization_timestamp",
            timestamp_valid,
            str(timestamp),
        ),
        Gate(
            "linux_ci_evidence",
            ci_evidence_valid and ci_claims_valid,
            (
                f"{ci_evidence_detail}; url={ci_url}; "
                f"commit={record.get('linux_ci_commit')}; "
                f"conclusion={record.get('linux_ci_conclusion')}"
            ),
        ),
        Gate(
            "archive_record",
            archive_url in expected_archive_urls,
            str(archive_url),
        ),
        Gate(
            "authorization_release_date",
            record.get("release_date") == release_date,
            str(record.get("release_date")),
        ),
        Gate(
            "authorization_version_doi",
            record.get("version_doi") == version_doi,
            str(record.get("version_doi")),
        ),
        Gate(
            "authorization_canonical_url",
            record.get("canonical_url") == canonical_url
            and canonical_url in canonical_allowed,
            str(record.get("canonical_url")),
        ),
        Gate(
            "authorization_attestation",
            attestation_valid,
            attestation_detail,
        ),
    ]


def _meta(html: str, name: str) -> str | None:
    match = re.search(
        rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]+)"',
        html,
    )
    return None if match is None else match.group(1)


def _canonical(html: str) -> str | None:
    match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    return None if match is None else match.group(1)


def validate_publication_values(
    release_date: str,
    version_doi: str,
    canonical_url: str,
) -> None:
    errors: list[str] = []
    try:
        date.fromisoformat(release_date)
    except ValueError:
        errors.append("RELEASE_DATE must be ISO YYYY-MM-DD")
    if not re.fullmatch(r"10\.5281/zenodo\.\d+", version_doi):
        errors.append("VERSION_DOI must be a Zenodo DOI")
    if version_doi == CONCEPT_DOI:
        errors.append("VERSION_DOI must not equal the all-versions concept DOI")
    if not canonical_url.startswith("https://"):
        errors.append("CANONICAL_URL must be https")
    if "/blob/main" in canonical_url or canonical_url.endswith("/main"):
        errors.append("CANONICAL_URL must be immutable, not a main-branch URL")
    if errors:
        raise ValueError("invalid publication metadata:\n- " + "\n- ".join(errors))


def repository_gates(
    root: Path,
    mode: str,
    release_date: str | None = None,
    version_doi: str | None = None,
    canonical_url: str | None = None,
) -> list[Gate]:
    """Evaluate deterministic repository contents; Git gates are CLI-level."""
    if mode not in {"candidate", "publication"}:
        raise ValueError("mode must be candidate or publication")

    cff = yaml.safe_load((root / "CITATION.cff").read_text(encoding="utf-8"))
    manuscript = (
        root / "docs" / "Recursive_Industrial_Intelligence_r4.0.md"
    ).read_text(encoding="utf-8")
    html = (
        root / "docs" / "Recursive_Industrial_Intelligence_r4.0.html"
    ).read_text(encoding="utf-8")
    gates = [
        Gate("cff_version", cff.get("version") == "r4.0", str(cff.get("version"))),
        Gate(
            "manuscript_identity",
            "## r4.0 · July 2026" in manuscript,
            "r4.0",
        ),
    ]
    for manifest in (
        root / "outputs" / "MANIFEST.md",
        root / "outputs" / "integrated" / "MANIFEST.md",
    ):
        try:
            verified = (
                verify_release_manifest(manifest, root)
                if manifest.parent == root / "outputs"
                else verify_manifest(manifest, root)
            )
            gates.append(
                Gate(
                    f"manifest:{manifest.parent.name}",
                    True,
                    f"{len(verified)} records",
                )
            )
        except ValueError as exc:
            gates.append(Gate(f"manifest:{manifest.parent.name}", False, str(exc)))

    if mode == "candidate":
        gates.extend([
            Gate(
                "candidate_wording",
                "r4.0 release candidate" in manuscript,
                "manuscript must identify the candidate",
            ),
            Gate(
                "candidate_no_version_doi",
                _meta(html, "citation_doi") is None
                and "date-released" not in cff,
                "version DOI and release date intentionally absent",
            ),
            Gate(
                "candidate_no_canonical",
                _canonical(html) is None
                and _meta(html, "citation_public_url") is None,
                "immutable canonical URL intentionally absent",
            ),
        ])
        return gates

    if release_date is None or version_doi is None or canonical_url is None:
        raise ValueError(
            "publication mode requires RELEASE_DATE, VERSION_DOI, and CANONICAL_URL"
        )
    validate_publication_values(release_date, version_doi, canonical_url)
    identifiers = {
        item.get("value")
        for item in cff.get("identifiers", [])
        if item.get("type") == "doi"
    }
    gates.extend([
        Gate(
            "final_wording",
            "r4.0 release candidate" not in manuscript,
            "candidate wording removed",
        ),
        Gate(
            "cff_release_date",
            str(cff.get("date-released", "")) == release_date,
            str(cff.get("date-released", "")),
        ),
        Gate(
            "cff_version_doi",
            version_doi in identifiers,
            "; ".join(sorted(str(value) for value in identifiers)),
        ),
        Gate(
            "html_release_date",
            _meta(html, "citation_publication_date") == release_date,
            str(_meta(html, "citation_publication_date")),
        ),
        Gate(
            "html_version_doi",
            _meta(html, "citation_doi") == version_doi,
            str(_meta(html, "citation_doi")),
        ),
        Gate(
            "html_canonical",
            _canonical(html) == canonical_url
            and _meta(html, "citation_public_url") == canonical_url,
            str(_canonical(html)),
        ),
    ])
    return gates
