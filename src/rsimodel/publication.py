"""Venue selection and fail-closed submission-readiness evaluation."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
import hashlib
import io
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
TARGETS_PATH = ROOT / "params" / "publication_targets.yaml"
WORD_RE = re.compile(r"\b[\w$%×./+−-]+\b", re.UNICODE)
PUBLICATION_AUTHORIZATION_SCHEMA = "r4.0-publication-authorization-v1"


@dataclass(frozen=True)
class PublicationGate:
    name: str
    passed: bool
    detail: str


def load_publication_targets(path: Path | None = None) -> dict[str, Any]:
    return yaml.safe_load((path or TARGETS_PATH).read_text(encoding="utf-8"))


def _word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def _section(markdown: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
    return "" if match is None else match.group(1).strip()


def _citation_ids(markdown: str) -> set[int]:
    """Return numeric citation ids, expanding comma lists and ranges."""
    cited: set[int] = set()
    for expression in re.findall(
        r"\[([0-9]+(?:\s*(?:,|[-–])\s*[0-9]+)*)\]",
        markdown,
    ):
        for item in re.split(r"\s*,\s*", expression):
            endpoints = re.split(r"\s*[-–]\s*", item)
            if len(endpoints) == 1:
                cited.add(int(endpoints[0]))
            elif len(endpoints) == 2:
                low, high = (int(value) for value in endpoints)
                if low <= high:
                    cited.update(range(low, high + 1))
    return cited


def manuscript_metrics(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    abstract = _section(text, "Abstract")
    keywords = _section(text, "Keywords")
    highlights = _section(text, "Highlights")
    highlight_items = re.findall(r"^- (.+)$", highlights, re.MULTILINE)
    references = _section(text, "References")
    reference_items = re.findall(
        r"^\[([0-9]+)\]\s+",
        references,
        re.MULTILINE,
    )
    reference_ids = {int(item) for item in reference_items}
    body = text.split("\n## References", maxsplit=1)[0]
    citation_ids = _citation_ids(body)
    data_statement = _section(text, "Data and code availability")
    unresolved_release_markers = (
        "must identify",
        "must replace",
        "must cite",
        "before submission",
        "release-candidate",
        "release candidate",
        "to be added",
        "forthcoming doi",
    )
    data_statement_lower = data_statement.lower()
    version_doi_present = bool(
        re.search(r"\b10\.5281/zenodo\.\d+\b", data_statement)
    )
    immutable_url_present = bool(
        re.search(r"https://(?:doi\.org/10\.5281/zenodo\.\d+|zenodo\.org/records/\d+)", data_statement)
    )
    immutable_release_coordinates = (
        version_doi_present
        and immutable_url_present
        and not any(
            marker in data_statement_lower
            for marker in unresolved_release_markers
        )
    )
    return {
        "word_count": _word_count(text),
        "abstract_words": _word_count(abstract),
        "keyword_count": len(
            [item for item in re.split(r"[;,]\s*", keywords) if item.strip()]
        ) if keywords else 0,
        "highlights": highlight_items,
        "numbered_sections": bool(re.search(r"^## 1[.\s]", text, re.MULTILINE)),
        "has_references": bool(references),
        "reference_count": len(reference_items),
        "has_citations": bool(citation_ids),
        "references_resolved": (
            bool(reference_ids)
            and citation_ids == reference_ids
            and reference_ids == set(range(1, len(reference_ids) + 1))
        ),
        "has_data_statement": bool(data_statement),
        "data_statement_final": bool(data_statement)
        and immutable_release_coordinates,
        "immutable_release_coordinates": immutable_release_coordinates,
        "has_proposition_boundary": (
            "proposition" in text.lower()
            or "does not establish" in text.lower()
        ),
    }


def validate_publication_targets(
    targets: dict[str, Any] | None = None,
) -> None:
    targets = targets or load_publication_targets()
    errors: list[str] = []
    required_papers = {"technical", "economics", "strategy_governance"}
    if set(targets.get("papers", {})) != required_papers:
        errors.append("publication targets must cover exactly three papers")
    if targets.get("status") != "venues_selected_conformance_in_progress":
        errors.append("status must keep submission conformance in progress")

    for paper_id, paper in targets.get("papers", {}).items():
        manuscript = ROOT / paper.get("manuscript", "")
        if not manuscript.is_file():
            errors.append(f"{paper_id}: manuscript missing")
        if not isinstance(paper.get("minimum_references"), int) or (
            paper["minimum_references"] < 3
        ):
            errors.append(
                f"{paper_id}: minimum_references must be an integer >= 3"
            )
        if paper.get("selected_route") not in {"target", "fallback"}:
            errors.append(
                f"{paper_id}: selected_route must be target or fallback"
            )
        for route_name in ("target", "fallback"):
            route = paper.get(route_name, {})
            for field in (
                "venue",
                "article_type",
                "official_url",
                "rationale",
                "review",
                "highlights",
                "editable_source",
                "reference_style",
                "data_statement",
            ):
                if field not in route:
                    errors.append(f"{paper_id}.{route_name}: missing {field}")
            if not str(route.get("official_url", "")).startswith("https://"):
                errors.append(
                    f"{paper_id}.{route_name}: official_url must be https"
                )
            highlights = route.get("highlights", {})
            if highlights.get("required"):
                if not (
                    1 <= highlights.get("min_items", 0)
                    <= highlights.get("max_items", 0)
                ):
                    errors.append(
                        f"{paper_id}.{route_name}: invalid highlights count"
                    )
                if highlights.get("max_chars_each", 0) <= 0:
                    errors.append(
                        f"{paper_id}.{route_name}: missing highlight limit"
                    )

    common = targets.get("common_submission_requirements", {})
    if len(common.get("author_confirmation_required", [])) < 8:
        errors.append("author-confirmation register is incomplete")
    if len(common.get("submission_actions", [])) < 6:
        errors.append("submission action register is incomplete")
    applicability = common.get("submission_action_applicability", {})
    if set(applicability) != set(common.get("submission_actions", [])):
        errors.append("submission-action applicability register is incomplete")
    allowed_applicability = {
        "always",
        "when_anonymized_review",
        "when_separate_title_page",
    }
    for action, rule in applicability.items():
        if rule not in allowed_applicability:
            errors.append(f"{action}: unknown applicability rule {rule}")
    if not targets.get("publication_boundary"):
        errors.append("publication boundary is missing")
    if errors:
        raise ValueError(
            "invalid publication target contract:\n- " + "\n- ".join(errors)
        )


def _route_checks(
    paper_id: str,
    route_name: str,
    route: dict[str, Any],
    metrics: dict[str, Any],
    minimum_references: int,
) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []

    def add(check: str, observed: Any, status: str) -> None:
        rows.append((f"{paper_id}.{route_name}.{check}", str(observed), status, route["venue"]))

    abstract_max = route.get("abstract_max_words")
    add(
        "abstract_words",
        metrics["abstract_words"],
        (
            "portal_recheck_pending"
            if abstract_max is None
            else "pass" if 0 < metrics["abstract_words"] <= abstract_max
            else "content_revision_pending"
        ),
    )
    keyword_min = route.get("keywords_min")
    keyword_max = route.get("keywords_max")
    keyword_status = "portal_recheck_pending" if keyword_min is None else (
        "pass"
        if metrics["keyword_count"] >= keyword_min
        and (keyword_max is None or metrics["keyword_count"] <= keyword_max)
        else "content_revision_pending"
    )
    add("keyword_count", metrics["keyword_count"], keyword_status)

    highlights = route["highlights"]
    if highlights["required"]:
        items = metrics["highlights"]
        valid = (
            highlights["min_items"] <= len(items) <= highlights["max_items"]
            and all(len(item) <= highlights["max_chars_each"] for item in items)
        )
        add("highlights", len(items), "pass" if valid else "content_revision_pending")
    if route.get("numbered_sections"):
        add(
            "numbered_sections",
            metrics["numbered_sections"],
            "pass" if metrics["numbered_sections"] else "content_revision_pending",
        )
    low, high = route.get("word_count_min"), route.get("word_count_max")
    if low is not None or high is not None:
        valid = (low is None or metrics["word_count"] >= low) and (
            high is None or metrics["word_count"] <= high
        )
        add("word_count", metrics["word_count"], "pass" if valid else "content_expansion_pending")
    references_valid = (
        metrics["has_references"]
        and metrics["has_citations"]
        and metrics["references_resolved"]
        and metrics["reference_count"] >= minimum_references
    )
    add(
        "references",
        (
            f'{metrics["reference_count"]}/{minimum_references}; '
            f'resolved={metrics["references_resolved"]}'
        ),
        "pass" if references_valid else "references_pending",
    )
    add(
        "data_statement",
        metrics["has_data_statement"],
        "pass" if metrics["has_data_statement"] else "content_revision_pending",
    )
    add(
        "immutable_release_coordinates",
        metrics["immutable_release_coordinates"],
        (
            "pass"
            if metrics["immutable_release_coordinates"]
            else "release_pending"
        ),
    )
    add(
        "proposition_boundary",
        metrics["has_proposition_boundary"],
        "pass" if metrics["has_proposition_boundary"] else "content_revision_pending",
    )
    for field in route.get("portal_confirmation_required", []):
        add(field, "not encoded by publisher page", "portal_recheck_pending")
    return rows


def render_publication_readiness_csv(
    targets: dict[str, Any] | None = None,
) -> str:
    targets = targets or load_publication_targets()
    validate_publication_targets(targets)
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow([
        "record_type",
        "id",
        "observed_or_required",
        "status",
        "venue_or_scope",
    ])
    for paper_id, paper in targets["papers"].items():
        metrics = manuscript_metrics(ROOT / paper["manuscript"])
        for route_name in ("target", "fallback"):
            for record_id, observed, status, venue in _route_checks(
                paper_id,
                route_name,
                paper[route_name],
                metrics,
                paper["minimum_references"],
            ):
                selected = route_name == paper["selected_route"]
                writer.writerow([
                    (
                        "machine_conformance"
                        if selected
                        else "contingency_conformance"
                    ),
                    record_id,
                    observed,
                    status if selected else "contingency_not_selected",
                    venue,
                ])
        for field in targets["common_submission_requirements"][
            "author_confirmation_required"
        ]:
            writer.writerow([
                "author_confirmation",
                f"{paper_id}.{field}",
                "author must supply or confirm",
                "author_confirmation_pending",
                "all routes",
            ])
        for action in targets["common_submission_requirements"][
            "submission_actions"
        ]:
            writer.writerow([
                "submission_action",
                f"{paper_id}.{action}",
                "execute after author confirmation and final route selection",
                "submission_action_pending",
                "all routes",
            ])
    return stream.getvalue()


def write_publication_readiness_csv(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_publication_readiness_csv(), encoding="utf-8")
    return path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def publication_authorization_template(
    targets: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an external submission-approval template that cannot pass."""
    targets = targets or load_publication_targets()
    validate_publication_targets(targets)
    confirmations = targets["common_submission_requirements"][
        "author_confirmation_required"
    ]
    actions = targets["common_submission_requirements"]["submission_actions"]
    papers = {}
    for paper_id, paper in targets["papers"].items():
        papers[paper_id] = {
            "selected_route": paper["selected_route"],
            "manuscript_sha256": _sha256(ROOT / paper["manuscript"]),
            "supplement_sha256": _sha256(ROOT / paper["supplement"]),
            "author_confirmations": {
                field: {
                    "status": None,
                    "value_or_attestation": None,
                }
                for field in confirmations
            },
            "submission_actions": {
                action: {
                    "status": None,
                    "evidence_or_note": None,
                }
                for action in actions
            },
            "final_submission_approved": False,
            "approver": None,
            "approval_timestamp_utc": None,
            "signature_or_attestation_id": None,
        }
    return {
        "schema": PUBLICATION_AUTHORIZATION_SCHEMA,
        "version": "r4.0",
        "privacy_boundary": (
            "external record; do not commit private identity, correspondence, "
            "or signature material"
        ),
        "papers": papers,
    }


def _timestamp_is_aware(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _submission_action_required(
    action: str,
    route: dict[str, Any],
    targets: dict[str, Any],
) -> bool:
    rule = targets["common_submission_requirements"][
        "submission_action_applicability"
    ][action]
    if rule == "always":
        return True
    if rule == "when_anonymized_review":
        return "anonym" in str(route.get("review", "")).lower()
    if rule == "when_separate_title_page":
        return route.get("separate_title_page") is True
    raise ValueError(f"unknown submission-action applicability rule {rule}")


def publication_authorization_gates(
    record: dict[str, Any],
    targets: dict[str, Any] | None = None,
) -> list[PublicationGate]:
    """Validate exact files, route conformance, actions, and author approval."""
    targets = targets or load_publication_targets()
    validate_publication_targets(targets)
    gates = [
        PublicationGate(
            "authorization_schema",
            record.get("schema") == PUBLICATION_AUTHORIZATION_SCHEMA,
            str(record.get("schema")),
        ),
        PublicationGate(
            "authorization_version",
            record.get("version") == "r4.0",
            str(record.get("version")),
        ),
    ]
    papers = record.get("papers", {})
    expected_papers = set(targets["papers"])
    gates.append(
        PublicationGate(
            "authorization_paper_set",
            isinstance(papers, dict) and set(papers) == expected_papers,
            "; ".join(sorted(papers)) if isinstance(papers, dict) else "invalid",
        )
    )
    expected_confirmations = set(
        targets["common_submission_requirements"][
            "author_confirmation_required"
        ]
    )
    expected_actions = set(
        targets["common_submission_requirements"]["submission_actions"]
    )
    for paper_id, paper in targets["papers"].items():
        candidate = (
            papers.get(paper_id, {}) if isinstance(papers, dict) else {}
        )
        approval = candidate if isinstance(candidate, dict) else {}
        route_name = approval.get("selected_route")
        route_valid = route_name == paper["selected_route"]
        gates.append(
            PublicationGate(
                f"{paper_id}.selected_route",
                route_valid,
                str(route_name),
            )
        )
        gates.extend([
            PublicationGate(
                f"{paper_id}.manuscript_sha256",
                approval.get("manuscript_sha256")
                == _sha256(ROOT / paper["manuscript"]),
                str(approval.get("manuscript_sha256")),
            ),
            PublicationGate(
                f"{paper_id}.supplement_sha256",
                approval.get("supplement_sha256")
                == _sha256(ROOT / paper["supplement"]),
                str(approval.get("supplement_sha256")),
            ),
        ])

        confirmations = approval.get("author_confirmations", {})
        confirmation_set_valid = (
            isinstance(confirmations, dict)
            and set(confirmations) == expected_confirmations
        )
        gates.append(
            PublicationGate(
                f"{paper_id}.author_confirmation_set",
                confirmation_set_valid,
                (
                    "; ".join(sorted(confirmations))
                    if isinstance(confirmations, dict)
                    else "invalid"
                ),
            )
        )
        for field in sorted(expected_confirmations):
            item = (
                confirmations.get(field, {})
                if isinstance(confirmations, dict)
                else {}
            )
            gates.append(
                PublicationGate(
                    f"{paper_id}.author_confirmation.{field}",
                    item.get("status") == "confirmed"
                    and bool(item.get("value_or_attestation")),
                    str(item.get("status")),
                )
            )

        actions = approval.get("submission_actions", {})
        action_set_valid = (
            isinstance(actions, dict) and set(actions) == expected_actions
        )
        gates.append(
            PublicationGate(
                f"{paper_id}.submission_action_set",
                action_set_valid,
                (
                    "; ".join(sorted(actions))
                    if isinstance(actions, dict)
                    else "invalid"
                ),
            )
        )
        for action in sorted(expected_actions):
            item = actions.get(action, {}) if isinstance(actions, dict) else {}
            required = (
                _submission_action_required(
                    action,
                    paper[route_name],
                    targets,
                )
                if route_valid
                else True
            )
            action_passed = (
                item.get("status") == "completed"
                if required
                else item.get("status") in {"completed", "not_applicable"}
            ) and bool(item.get("evidence_or_note"))
            gates.append(
                PublicationGate(
                    f"{paper_id}.submission_action.{action}",
                    action_passed,
                    f"{item.get('status')}; required={required}",
                )
            )

        portal_confirmed = (
            isinstance(actions, dict)
            and actions.get("recheck_live_portal_requirements", {}).get(
                "status"
            )
            == "completed"
            and bool(
                actions.get("recheck_live_portal_requirements", {}).get(
                    "evidence_or_note"
                )
            )
        )
        if route_valid:
            metrics = manuscript_metrics(ROOT / paper["manuscript"])
            for record_id, observed, status, venue in _route_checks(
                paper_id,
                route_name,
                paper[route_name],
                metrics,
                paper["minimum_references"],
            ):
                conformance_passed = status == "pass" or (
                    status == "portal_recheck_pending" and portal_confirmed
                )
                gates.append(
                    PublicationGate(
                        f"{record_id}.authorized",
                        conformance_passed,
                        f"{status}; {observed}; {venue}",
                    )
                )

        gates.extend([
            PublicationGate(
                f"{paper_id}.final_submission_approved",
                approval.get("final_submission_approved") is True,
                str(approval.get("final_submission_approved")),
            ),
            PublicationGate(
                f"{paper_id}.approver",
                bool(approval.get("approver")),
                str(approval.get("approver")),
            ),
            PublicationGate(
                f"{paper_id}.approval_timestamp",
                _timestamp_is_aware(approval.get("approval_timestamp_utc")),
                str(approval.get("approval_timestamp_utc")),
            ),
            PublicationGate(
                f"{paper_id}.attestation",
                bool(approval.get("signature_or_attestation_id")),
                str(approval.get("signature_or_attestation_id")),
            ),
        ])
    return gates
