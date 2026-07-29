"""Venue selection and fail-closed submission-readiness evaluation."""

from __future__ import annotations

import csv
import hashlib
import io
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal, NotRequired, Protocol, TypedDict

from .yaml_adapter import (
    load_yaml_mapping,
    require_boolean,
    require_mapping,
    require_string,
    require_string_sequence,
)

ROOT = Path(__file__).resolve().parents[2]
TARGETS_PATH = ROOT / "params" / "publication_targets.yaml"
WORD_RE = re.compile(r"\b[\w$%×./+−-]+\b", re.UNICODE)
PUBLICATION_AUTHORIZATION_SCHEMA = "r4.0-publication-authorization-v1"


@dataclass(frozen=True)
class PublicationGate:
    name: str
    passed: bool
    detail: str


class ManuscriptMetrics(TypedDict):
    word_count: int
    abstract_words: int
    keyword_count: int
    highlights: tuple[str, ...]
    numbered_sections: bool
    citation_style: Literal["numbered", "author_date", "mixed", "none"]
    has_references: bool
    reference_count: int
    has_citations: bool
    references_resolved: bool
    has_data_statement: bool
    data_statement_final: bool
    immutable_release_coordinates: bool
    has_proposition_boundary: bool


class HighlightRequirements(TypedDict):
    required: bool
    min_items: int
    max_items: int
    max_chars_each: int


class PublicationRoute(TypedDict):
    venue: str
    article_type: str
    official_url: str
    rationale: str
    review: str
    abstract_max_words: int | None
    keywords_min: int | None
    keywords_max: int | None
    highlights: HighlightRequirements
    numbered_sections: bool
    editable_source: bool
    reference_style: str
    data_statement: str
    separate_title_page: bool | str
    word_count_min: int | None
    word_count_max: int | None
    portal_confirmation_required: NotRequired[tuple[str, ...]]


class PublicationPaper(TypedDict):
    manuscript: str
    supplement: str
    minimum_references: int
    selected_route: Literal["target", "fallback"]
    target: PublicationRoute
    fallback: PublicationRoute


type SubmissionApplicability = Literal[
    "always",
    "when_anonymized_review",
    "when_separate_title_page",
]


class CommonSubmissionRequirements(TypedDict):
    machine_checkable: tuple[str, ...]
    author_confirmation_required: tuple[str, ...]
    submission_actions: tuple[str, ...]
    submission_action_applicability: Mapping[str, SubmissionApplicability]


class PublicationTargets(TypedDict):
    version: str
    decision_date: str
    status: str
    source_class: str
    epistemic_status: str
    papers: Mapping[str, PublicationPaper]
    common_submission_requirements: CommonSubmissionRequirements
    publication_boundary: str


class AuthorConfirmation(TypedDict):
    status: str | None
    value_or_attestation: str | None


class SubmissionAction(TypedDict):
    status: str | None
    evidence_or_note: str | None


class PaperAuthorization(TypedDict):
    selected_route: Literal["target", "fallback"]
    manuscript_sha256: str
    supplement_sha256: str
    author_confirmations: dict[str, AuthorConfirmation]
    submission_actions: dict[str, SubmissionAction]
    final_submission_approved: bool
    approver: str | None
    approval_timestamp_utc: str | None
    signature_or_attestation_id: str | None


class PublicationAuthorizationRecord(TypedDict):
    schema: str
    version: str
    privacy_boundary: str
    papers: dict[str, PaperAuthorization]


class RecordParser[Record](Protocol):
    def __call__(self, value: object, *, label: str) -> Record: ...


def _integer(value: object, *, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label}: expected an integer")
    return value


def _optional_integer(value: object, *, label: str) -> int | None:
    if value is None:
        return None
    return _integer(value, label=label)


def _boolean_or_string(value: object, *, label: str) -> bool | str:
    if isinstance(value, bool):
        return value
    return require_string(value, label=label)


def _highlights(value: object, *, label: str) -> HighlightRequirements:
    raw = require_mapping(value, label=label)
    return {
        "required": require_boolean(raw.get("required"), label=f"{label}.required"),
        "min_items": _integer(raw.get("min_items"), label=f"{label}.min_items"),
        "max_items": _integer(raw.get("max_items"), label=f"{label}.max_items"),
        "max_chars_each": _integer(
            raw.get("max_chars_each"),
            label=f"{label}.max_chars_each",
        ),
    }


def _publication_route(value: object, *, label: str) -> PublicationRoute:
    raw = require_mapping(value, label=label)
    route: PublicationRoute = {
        "venue": require_string(raw.get("venue"), label=f"{label}.venue"),
        "article_type": require_string(
            raw.get("article_type"),
            label=f"{label}.article_type",
        ),
        "official_url": require_string(
            raw.get("official_url"),
            label=f"{label}.official_url",
        ),
        "rationale": require_string(raw.get("rationale"), label=f"{label}.rationale"),
        "review": require_string(raw.get("review"), label=f"{label}.review"),
        "abstract_max_words": _optional_integer(
            raw.get("abstract_max_words"),
            label=f"{label}.abstract_max_words",
        ),
        "keywords_min": _optional_integer(
            raw.get("keywords_min"),
            label=f"{label}.keywords_min",
        ),
        "keywords_max": _optional_integer(
            raw.get("keywords_max"),
            label=f"{label}.keywords_max",
        ),
        "highlights": _highlights(
            raw.get("highlights"),
            label=f"{label}.highlights",
        ),
        "numbered_sections": require_boolean(
            raw.get("numbered_sections"),
            label=f"{label}.numbered_sections",
        ),
        "editable_source": require_boolean(
            raw.get("editable_source"),
            label=f"{label}.editable_source",
        ),
        "reference_style": require_string(
            raw.get("reference_style"),
            label=f"{label}.reference_style",
        ),
        "data_statement": require_string(
            raw.get("data_statement"),
            label=f"{label}.data_statement",
        ),
        "separate_title_page": _boolean_or_string(
            raw.get("separate_title_page"),
            label=f"{label}.separate_title_page",
        ),
        "word_count_min": _optional_integer(
            raw.get("word_count_min"),
            label=f"{label}.word_count_min",
        ),
        "word_count_max": _optional_integer(
            raw.get("word_count_max"),
            label=f"{label}.word_count_max",
        ),
    }
    if "portal_confirmation_required" in raw:
        route["portal_confirmation_required"] = require_string_sequence(
            raw["portal_confirmation_required"],
            label=f"{label}.portal_confirmation_required",
        )
    return route


def _publication_paper(value: object, *, label: str) -> PublicationPaper:
    raw = require_mapping(value, label=label)
    selected_route = require_string(
        raw.get("selected_route"),
        label=f"{label}.selected_route",
    )
    if selected_route == "target":
        typed_route: Literal["target", "fallback"] = "target"
    elif selected_route == "fallback":
        typed_route = "fallback"
    else:
        raise ValueError(f"{label}.selected_route: expected target or fallback")
    return {
        "manuscript": require_string(
            raw.get("manuscript"),
            label=f"{label}.manuscript",
        ),
        "supplement": require_string(
            raw.get("supplement"),
            label=f"{label}.supplement",
        ),
        "minimum_references": _integer(
            raw.get("minimum_references"),
            label=f"{label}.minimum_references",
        ),
        "selected_route": typed_route,
        "target": _publication_route(
            raw.get("target"),
            label=f"{label}.target",
        ),
        "fallback": _publication_route(
            raw.get("fallback"),
            label=f"{label}.fallback",
        ),
    }


def _named_records[Record](
    value: object,
    *,
    label: str,
    parser: RecordParser[Record],
) -> dict[str, Record]:
    raw = require_mapping(value, label=label)
    return {key: parser(item, label=f"{label}.{key}") for key, item in raw.items()}


def _submission_applicability(
    value: object,
    *,
    label: str,
) -> dict[str, SubmissionApplicability]:
    raw = require_mapping(value, label=label)
    result: dict[str, SubmissionApplicability] = {}
    for action, item in raw.items():
        rule = require_string(item, label=f"{label}.{action}")
        if rule not in {
            "always",
            "when_anonymized_review",
            "when_separate_title_page",
        }:
            raise ValueError(f"{label}.{action}: unknown applicability rule {rule}")
        if rule == "always":
            typed_rule: SubmissionApplicability = "always"
        elif rule == "when_anonymized_review":
            typed_rule = "when_anonymized_review"
        else:
            typed_rule = "when_separate_title_page"
        result[action] = typed_rule
    return result


def _common_requirements(value: object, *, label: str) -> CommonSubmissionRequirements:
    raw = require_mapping(value, label=label)
    return {
        "machine_checkable": require_string_sequence(
            raw.get("machine_checkable"),
            label=f"{label}.machine_checkable",
        ),
        "author_confirmation_required": require_string_sequence(
            raw.get("author_confirmation_required"),
            label=f"{label}.author_confirmation_required",
        ),
        "submission_actions": require_string_sequence(
            raw.get("submission_actions"),
            label=f"{label}.submission_actions",
        ),
        "submission_action_applicability": _submission_applicability(
            raw.get("submission_action_applicability"),
            label=f"{label}.submission_action_applicability",
        ),
    }


def load_publication_targets(path: Path | None = None) -> PublicationTargets:
    """Load and structurally validate venue and submission requirements."""
    raw = load_yaml_mapping(path or TARGETS_PATH)
    return {
        "version": require_string(raw.get("version"), label="publication.version"),
        "decision_date": require_string(
            raw.get("decision_date"),
            label="publication.decision_date",
        ),
        "status": require_string(raw.get("status"), label="publication.status"),
        "source_class": require_string(
            raw.get("source_class"),
            label="publication.source_class",
        ),
        "epistemic_status": require_string(
            raw.get("epistemic_status"),
            label="publication.epistemic_status",
        ),
        "papers": _named_records(
            raw.get("papers"),
            label="publication.papers",
            parser=_publication_paper,
        ),
        "common_submission_requirements": _common_requirements(
            raw.get("common_submission_requirements"),
            label="publication.common_submission_requirements",
        ),
        "publication_boundary": require_string(
            raw.get("publication_boundary"),
            label="publication.publication_boundary",
        ),
    }


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


def _author_date_reference_labels(references: str) -> tuple[tuple[str, str], ...]:
    """Return author labels and years from author-date reference paragraphs."""
    labels: list[tuple[str, str]] = []
    for paragraph in re.split(r"\n\s*\n", references):
        normalized = " ".join(paragraph.split())
        match = re.match(r"^(.+?)\s+(\d{4}[a-z]?)\.\s+", normalized)
        if match is None:
            continue
        author_field, year = match.groups()
        if "," in author_field:
            citation_author = author_field.split(",", maxsplit=1)[0].strip()
        else:
            citation_author = author_field.strip()
        labels.append((citation_author, year))
    return tuple(labels)


def _author_date_references_resolved(
    body: str,
    labels: tuple[tuple[str, str], ...],
) -> bool:
    if not labels:
        return False
    return all(
        re.search(
            rf"\b{re.escape(author)}(?:\s+et al\.)?\s+{re.escape(year)}\b",
            body,
        )
        is not None
        for author, year in labels
    )


def manuscript_metrics(path: Path) -> ManuscriptMetrics:
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
    author_date_labels = _author_date_reference_labels(references)
    body = text.split("\n## References", maxsplit=1)[0]
    citation_ids = _citation_ids(body)
    author_date_resolved = _author_date_references_resolved(
        body,
        author_date_labels,
    )
    has_numbered_citations = bool(citation_ids)
    has_author_date_citations = bool(author_date_labels) and any(
        re.search(
            rf"\b{re.escape(author)}(?:\s+et al\.)?\s+{re.escape(year)}\b",
            body,
        )
        is not None
        for author, year in author_date_labels
    )
    if has_numbered_citations and has_author_date_citations:
        citation_style: Literal["numbered", "author_date", "mixed", "none"] = "mixed"
    elif has_numbered_citations:
        citation_style = "numbered"
    elif has_author_date_citations:
        citation_style = "author_date"
    else:
        citation_style = "none"
    numbered_references_resolved = (
        bool(reference_ids)
        and citation_ids == reference_ids
        and reference_ids == set(range(1, len(reference_ids) + 1))
    )
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
    version_doi_present = bool(re.search(r"\b10\.5281/zenodo\.\d+\b", data_statement))
    immutable_url_present = bool(
        re.search(
            r"https://(?:doi\.org/10\.5281/zenodo\.\d+|zenodo\.org/records/\d+)", data_statement
        )
    )
    immutable_release_coordinates = (
        version_doi_present
        and immutable_url_present
        and not any(marker in data_statement_lower for marker in unresolved_release_markers)
    )
    return {
        "word_count": _word_count(text),
        "abstract_words": _word_count(abstract),
        "keyword_count": len([item for item in re.split(r"[;,]\s*", keywords) if item.strip()])
        if keywords
        else 0,
        "highlights": tuple(highlight_items),
        "numbered_sections": bool(re.search(r"^## 1[.\s]", text, re.MULTILINE)),
        "citation_style": citation_style,
        "has_references": bool(references),
        "reference_count": len(reference_items) or len(author_date_labels),
        "has_citations": has_numbered_citations or has_author_date_citations,
        "references_resolved": numbered_references_resolved or author_date_resolved,
        "has_data_statement": bool(data_statement),
        "data_statement_final": bool(data_statement) and immutable_release_coordinates,
        "immutable_release_coordinates": immutable_release_coordinates,
        "has_proposition_boundary": (
            "proposition" in text.lower() or "does not establish" in text.lower()
        ),
    }


def validate_publication_targets(
    targets: PublicationTargets | None = None,
) -> None:
    if targets is None:
        targets = load_publication_targets()
    errors: list[str] = []
    required_papers = {"technical", "economics", "strategy_governance"}
    if set(targets["papers"]) != required_papers:
        errors.append("publication targets must cover exactly three papers")
    if targets.get("status") != "venues_selected_conformance_in_progress":
        errors.append("status must keep submission conformance in progress")

    for paper_id, paper in targets["papers"].items():
        manuscript = ROOT / paper["manuscript"]
        if not manuscript.is_file():
            errors.append(f"{paper_id}: manuscript missing")
        if paper["minimum_references"] < 3:
            errors.append(f"{paper_id}: minimum_references must be an integer >= 3")
        if paper["selected_route"] not in {"target", "fallback"}:
            errors.append(f"{paper_id}: selected_route must be target or fallback")
        for route_name in ("target", "fallback"):
            route = paper[route_name]
            if not route["official_url"].startswith("https://"):
                errors.append(f"{paper_id}.{route_name}: official_url must be https")
            highlights = route["highlights"]
            if highlights["required"]:
                if not (1 <= highlights["min_items"] <= highlights["max_items"]):
                    errors.append(f"{paper_id}.{route_name}: invalid highlights count")
                if highlights["max_chars_each"] <= 0:
                    errors.append(f"{paper_id}.{route_name}: missing highlight limit")

    common = targets["common_submission_requirements"]
    if len(common["author_confirmation_required"]) < 8:
        errors.append("author-confirmation register is incomplete")
    if len(common["submission_actions"]) < 6:
        errors.append("submission action register is incomplete")
    applicability = common["submission_action_applicability"]
    if set(applicability) != set(common["submission_actions"]):
        errors.append("submission-action applicability register is incomplete")
    allowed_applicability = {
        "always",
        "when_anonymized_review",
        "when_separate_title_page",
    }
    for action, rule in applicability.items():
        if rule not in allowed_applicability:
            errors.append(f"{action}: unknown applicability rule {rule}")
    if not targets["publication_boundary"]:
        errors.append("publication boundary is missing")
    if errors:
        raise ValueError("invalid publication target contract:\n- " + "\n- ".join(errors))


def _route_checks(
    paper_id: str,
    route_name: str,
    route: PublicationRoute,
    metrics: ManuscriptMetrics,
    minimum_references: int,
) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    portal_fields = set(route.get("portal_confirmation_required", ()))

    def add(check: str, observed: object, status: str) -> None:
        rows.append((f"{paper_id}.{route_name}.{check}", str(observed), status, route["venue"]))

    abstract_max = route["abstract_max_words"]
    add(
        "abstract_words",
        metrics["abstract_words"],
        (
            "content_revision_pending"
            if metrics["abstract_words"] <= 0
            else (
                "portal_recheck_pending"
                if abstract_max is None and {"abstract_limit", "abstract_max_words"} & portal_fields
                else "pass"
                if abstract_max is None or metrics["abstract_words"] <= abstract_max
                else "content_revision_pending"
            )
        ),
    )
    keyword_min = route["keywords_min"]
    keyword_max = route["keywords_max"]
    keyword_status = (
        "portal_recheck_pending"
        if keyword_min is None
        else (
            "pass"
            if metrics["keyword_count"] >= keyword_min
            and (keyword_max is None or metrics["keyword_count"] <= keyword_max)
            else "content_revision_pending"
        )
    )
    add("keyword_count", metrics["keyword_count"], keyword_status)

    highlights = route["highlights"]
    if highlights["required"]:
        items = metrics["highlights"]
        valid = highlights["min_items"] <= len(items) <= highlights["max_items"] and all(
            len(item) <= highlights["max_chars_each"] for item in items
        )
        add("highlights", len(items), "pass" if valid else "content_revision_pending")
    if route["numbered_sections"]:
        add(
            "numbered_sections",
            metrics["numbered_sections"],
            "pass" if metrics["numbered_sections"] else "content_revision_pending",
        )
    low, high = route["word_count_min"], route["word_count_max"]
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
            f"{metrics['reference_count']}/{minimum_references}; "
            f"resolved={metrics['references_resolved']}"
        ),
        "pass" if references_valid else "references_pending",
    )
    reference_style = route["reference_style"]
    if reference_style == "numbered_square_brackets_order_of_appearance":
        reference_style_status = (
            "pass"
            if metrics["citation_style"] == "numbered" and metrics["references_resolved"]
            else "content_revision_pending"
        )
    elif reference_style == "chicago_author_date":
        reference_style_status = (
            "pass"
            if metrics["citation_style"] == "author_date" and metrics["references_resolved"]
            else "content_revision_pending"
        )
    elif reference_style == "publisher_style_recheck_required":
        reference_style_status = "portal_recheck_pending"
    else:
        reference_style_status = "pass" if metrics["references_resolved"] else "references_pending"
    add(
        "reference_style",
        f"required={reference_style}; observed={metrics['citation_style']}",
        reference_style_status,
    )
    add(
        "data_statement",
        metrics["has_data_statement"],
        "pass" if metrics["has_data_statement"] else "content_revision_pending",
    )
    add(
        "immutable_release_coordinates",
        metrics["immutable_release_coordinates"],
        ("pass" if metrics["immutable_release_coordinates"] else "release_pending"),
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
    targets: PublicationTargets | None = None,
) -> str:
    if targets is None:
        targets = load_publication_targets()
    validate_publication_targets(targets)
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(
        [
            "record_type",
            "id",
            "observed_or_required",
            "status",
            "venue_or_scope",
        ]
    )
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
                writer.writerow(
                    [
                        ("machine_conformance" if selected else "contingency_conformance"),
                        record_id,
                        observed,
                        status if selected else "contingency_not_selected",
                        venue,
                    ]
                )
        for field in targets["common_submission_requirements"]["author_confirmation_required"]:
            writer.writerow(
                [
                    "author_confirmation",
                    f"{paper_id}.{field}",
                    "author must supply or confirm",
                    "author_confirmation_pending",
                    "all routes",
                ]
            )
        for action in targets["common_submission_requirements"]["submission_actions"]:
            writer.writerow(
                [
                    "submission_action",
                    f"{paper_id}.{action}",
                    "execute after author confirmation and final route selection",
                    "submission_action_pending",
                    "all routes",
                ]
            )
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
    targets: PublicationTargets | None = None,
) -> PublicationAuthorizationRecord:
    """Return an external submission-approval template that cannot pass."""
    if targets is None:
        targets = load_publication_targets()
    validate_publication_targets(targets)
    confirmations = targets["common_submission_requirements"]["author_confirmation_required"]
    actions = targets["common_submission_requirements"]["submission_actions"]
    papers: dict[str, PaperAuthorization] = {}
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
            "external record; do not commit private identity, correspondence, or signature material"
        ),
        "papers": papers,
    }


def _timestamp_is_aware(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _submission_action_required(
    action: str,
    route: PublicationRoute,
    targets: PublicationTargets,
) -> bool:
    rule = targets["common_submission_requirements"]["submission_action_applicability"][action]
    if rule == "always":
        return True
    if rule == "when_anonymized_review":
        return "anonym" in route["review"].lower()
    if rule == "when_separate_title_page":
        return route.get("separate_title_page") is True
    raise ValueError(f"unknown submission-action applicability rule {rule}")


def _mapping_or_empty(value: object) -> dict[str, object]:
    try:
        return require_mapping(value, label="publication authorization")
    except ValueError:
        return {}


def publication_authorization_gates(
    record: Mapping[str, object],
    targets: PublicationTargets | None = None,
) -> list[PublicationGate]:
    """Validate exact files, route conformance, actions, and author approval."""
    if targets is None:
        targets = load_publication_targets()
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
    papers = _mapping_or_empty(record.get("papers"))
    expected_papers = set(targets["papers"])
    gates.append(
        PublicationGate(
            "authorization_paper_set",
            set(papers) == expected_papers,
            "; ".join(sorted(papers)),
        )
    )
    expected_confirmations = set(
        targets["common_submission_requirements"]["author_confirmation_required"]
    )
    expected_actions = set(targets["common_submission_requirements"]["submission_actions"])
    for paper_id, paper in targets["papers"].items():
        approval = _mapping_or_empty(papers.get(paper_id))
        route_name = approval.get("selected_route")
        route_valid = route_name == paper["selected_route"]
        gates.append(
            PublicationGate(
                f"{paper_id}.selected_route",
                route_valid,
                str(route_name),
            )
        )
        gates.extend(
            [
                PublicationGate(
                    f"{paper_id}.manuscript_sha256",
                    approval.get("manuscript_sha256") == _sha256(ROOT / paper["manuscript"]),
                    str(approval.get("manuscript_sha256")),
                ),
                PublicationGate(
                    f"{paper_id}.supplement_sha256",
                    approval.get("supplement_sha256") == _sha256(ROOT / paper["supplement"]),
                    str(approval.get("supplement_sha256")),
                ),
            ]
        )

        confirmations = _mapping_or_empty(approval.get("author_confirmations"))
        confirmation_set_valid = set(confirmations) == expected_confirmations
        gates.append(
            PublicationGate(
                f"{paper_id}.author_confirmation_set",
                confirmation_set_valid,
                "; ".join(sorted(confirmations)),
            )
        )
        for field in sorted(expected_confirmations):
            item = _mapping_or_empty(confirmations.get(field))
            gates.append(
                PublicationGate(
                    f"{paper_id}.author_confirmation.{field}",
                    item.get("status") == "confirmed" and bool(item.get("value_or_attestation")),
                    str(item.get("status")),
                )
            )

        actions = _mapping_or_empty(approval.get("submission_actions"))
        action_set_valid = set(actions) == expected_actions
        gates.append(
            PublicationGate(
                f"{paper_id}.submission_action_set",
                action_set_valid,
                "; ".join(sorted(actions)),
            )
        )
        for action in sorted(expected_actions):
            item = _mapping_or_empty(actions.get(action))
            required = (
                _submission_action_required(
                    action,
                    paper[paper["selected_route"]],
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

        portal_action = _mapping_or_empty(actions.get("recheck_live_portal_requirements"))
        portal_confirmed = portal_action.get("status") == "completed" and bool(
            portal_action.get("evidence_or_note")
        )
        if route_valid and isinstance(route_name, str):
            metrics = manuscript_metrics(ROOT / paper["manuscript"])
            for record_id, observed, status, venue in _route_checks(
                paper_id,
                paper["selected_route"],
                paper[paper["selected_route"]],
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

        gates.extend(
            [
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
            ]
        )
    return gates
