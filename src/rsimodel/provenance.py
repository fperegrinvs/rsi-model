"""Claim-level source validation and deterministic provenance-table output.

Runtime provenance explains which anchor a calculation used. This module
enforces the stronger publication contract: every non-ASSUMPTION anchor has
an exact source locator, extracted value, units, transformation, and
persistent identifier. It also validates the SEC-filing claims grouped under
manuscript reference [S27] and the contextual evidence claims used to bound
the digital-loop discussion.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Mapping
from pathlib import Path
from typing import NotRequired, Protocol, TypedDict

from .delta import PARAMS_DIR, AnchorMap, AnchorRecord, load_anchors
from .yaml_adapter import (
    load_yaml_mapping,
    require_mapping,
    require_string,
)

ROOT = Path(__file__).resolve().parents[2]
PROVENANCE_PATH = PARAMS_DIR / "claim_provenance.yaml"
PROVENANCE_OUTPUT = ROOT / "outputs" / "tables" / "claim_provenance.csv"


type Numeric = int | float


class ScalarModelValue(TypedDict):
    value: Numeric


class RangeModelValue(TypedDict):
    low: Numeric
    high: Numeric


type ModelValue = ScalarModelValue | RangeModelValue


class ClaimRecord(TypedDict):
    source_class: str
    units: str
    source_ref: str
    organization_or_authors: str
    title: str
    date: str
    locator: str
    permanent_url_or_doi: str
    extracted_value: str
    transformation: str
    status: str
    archive_path: NotRequired[str]


class AnchorClaimRecord(ClaimRecord):
    model_value: ModelValue


class TextClaimRecord(ClaimRecord):
    claim_text: str


class ClaimProvenanceRegistry(TypedDict):
    anchors: Mapping[str, AnchorClaimRecord]
    strategy_claims: Mapping[str, TextClaimRecord]
    context_claims: Mapping[str, TextClaimRecord]


class RecordParser[Record](Protocol):
    def __call__(self, value: object, *, label: str) -> Record: ...


def _claim_record(value: object, *, label: str) -> ClaimRecord:
    raw = require_mapping(value, label=label)
    record: ClaimRecord = {
        "source_class": require_string(
            raw.get("source_class"),
            label=f"{label}.source_class",
        ),
        "units": require_string(raw.get("units"), label=f"{label}.units"),
        "source_ref": require_string(
            raw.get("source_ref"),
            label=f"{label}.source_ref",
        ),
        "organization_or_authors": require_string(
            raw.get("organization_or_authors"),
            label=f"{label}.organization_or_authors",
        ),
        "title": require_string(raw.get("title"), label=f"{label}.title"),
        "date": require_string(raw.get("date"), label=f"{label}.date"),
        "locator": require_string(raw.get("locator"), label=f"{label}.locator"),
        "permanent_url_or_doi": require_string(
            raw.get("permanent_url_or_doi"),
            label=f"{label}.permanent_url_or_doi",
        ),
        "extracted_value": require_string(
            raw.get("extracted_value"),
            label=f"{label}.extracted_value",
        ),
        "transformation": require_string(
            raw.get("transformation"),
            label=f"{label}.transformation",
        ),
        "status": require_string(raw.get("status"), label=f"{label}.status"),
    }
    if "archive_path" in raw:
        record["archive_path"] = require_string(
            raw["archive_path"],
            label=f"{label}.archive_path",
        )
    return record


def _model_value_record(value: object, *, label: str) -> ModelValue:
    raw = require_mapping(value, label=label)
    if set(raw) == {"value"}:
        return {
            "value": _numeric(raw["value"], label=f"{label}.value"),
        }
    if set(raw) == {"low", "high"}:
        low = _numeric(raw["low"], label=f"{label}.low")
        high = _numeric(raw["high"], label=f"{label}.high")
        if low > high:
            raise ValueError(f"{label}: low exceeds high")
        return {"low": low, "high": high}
    raise ValueError(f"{label}: expected exactly value or low/high")


def _numeric(value: object, *, label: str) -> Numeric:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label}: expected a number")
    return value


def _anchor_claim(value: object, *, label: str) -> AnchorClaimRecord:
    raw = require_mapping(value, label=label)
    return {
        **_claim_record(value, label=label),
        "model_value": _model_value_record(
            raw.get("model_value"),
            label=f"{label}.model_value",
        ),
    }


def _text_claim(value: object, *, label: str) -> TextClaimRecord:
    raw = require_mapping(value, label=label)
    return {
        **_claim_record(value, label=label),
        "claim_text": require_string(
            raw.get("claim_text"),
            label=f"{label}.claim_text",
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


def load_claim_provenance(path: Path | None = None) -> ClaimProvenanceRegistry:
    """Load and structurally validate the claim-level publication register."""
    raw = load_yaml_mapping(path or PROVENANCE_PATH)
    return {
        "anchors": _named_records(
            raw.get("anchors"),
            label="claim_provenance.anchors",
            parser=_anchor_claim,
        ),
        "strategy_claims": _named_records(
            raw.get("strategy_claims"),
            label="claim_provenance.strategy_claims",
            parser=_text_claim,
        ),
        "context_claims": _named_records(
            raw.get("context_claims"),
            label="claim_provenance.context_claims",
            parser=_text_claim,
        ),
    }


def _model_value(entry: AnchorRecord) -> dict[str, float]:
    if "value" in entry:
        return {"value": float(entry["value"])}
    return {"low": float(entry["low"]), "high": float(entry["high"])}


def validate_claim_provenance(
    register: ClaimProvenanceRegistry | None = None,
    anchors: AnchorMap | None = None,
) -> None:
    """Raise ``ValueError`` if the register violates the release contract."""
    if register is None:
        register = load_claim_provenance()
    resolved_anchors = anchors if anchors is not None else load_anchors()
    anchor_records = register.get("anchors", {})
    strategy_records = register.get("strategy_claims", {})
    context_records = register.get("context_claims", {})

    expected = {
        name for name, entry in resolved_anchors.items() if entry["source_class"] != "ASSUMPTION"
    }
    actual = set(anchor_records)
    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(
            f"claim-provenance anchor coverage mismatch; missing={missing}, extra={extra}"
        )

    errors: list[str] = []
    for name in sorted(expected):
        record = anchor_records[name]
        if record["status"] != "verified":
            errors.append(f"{name}: status must be verified")
        if record["source_class"] != resolved_anchors[name]["source_class"]:
            errors.append(
                f"{name}: source_class {record['source_class']!r} != "
                f"{resolved_anchors[name]['source_class']!r}"
            )
        if record["model_value"] != _model_value(resolved_anchors[name]):
            errors.append(
                f"{name}: model_value {record['model_value']!r} != "
                f"{_model_value(resolved_anchors[name])!r}"
            )
        if "S36" in record["source_ref"]:
            errors.append(f"{name}: collective S36 is not claim-level provenance")

    if not strategy_records:
        errors.append("strategy_claims: no S27 claim records")
    for name, record in sorted(strategy_records.items()):
        if record["status"] != "verified":
            errors.append(f"{name}: status must be verified")
        if record["source_ref"] != "S27":
            errors.append(f"{name}: strategy record must resolve to S27")
        locator = record["locator"].lower()
        if not any(token in locator for token in ("p.", "pp.", "slide")):
            errors.append(f"{name}: locator is not page- or slide-level")
        permanent = record["permanent_url_or_doi"]
        if "sec.gov/Archives/edgar/data/" not in permanent:
            errors.append(f"{name}: missing permanent SEC EDGAR URL")

    if not context_records:
        errors.append("context_claims: no contextual evidence records")
    for name, record in sorted(context_records.items()):
        if record["status"] != "verified":
            errors.append(f"{name}: status must be verified")
        source_ref = record["source_ref"]
        if not source_ref.startswith("S"):
            errors.append(f"{name}: source_ref must be a manuscript source ID")
        if not record["locator"].strip():
            errors.append(f"{name}: exact locator required")
        permanent = record["permanent_url_or_doi"]
        if not permanent.startswith(("https://", "http://")):
            errors.append(f"{name}: persistent URL or DOI required")

    if errors:
        raise ValueError("invalid claim provenance:\n- " + "\n- ".join(errors))


def _format_model_value(value: ModelValue | None) -> str:
    if not value:
        return ""
    if "value" in value:
        return str(value["value"])
    return f"{value['low']}..{value['high']}"


def render_claim_provenance_csv(
    register: ClaimProvenanceRegistry | None = None,
    anchors: AnchorMap | None = None,
    *,
    provenance_path: Path | None = None,
    anchors_path: Path | None = None,
) -> str:
    """Render the validated register in a stable, reviewer-friendly table."""
    if register is None:
        register = load_claim_provenance(provenance_path)
    resolved_anchors = anchors if anchors is not None else load_anchors(anchors_path)
    validate_claim_provenance(register, resolved_anchors)

    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(
        [
            "record_type",
            "key",
            "source_class",
            "model_value",
            "units",
            "source_ref",
            "organization_or_authors",
            "title",
            "date",
            "locator",
            "permanent_url_or_doi",
            "extracted_value",
            "transformation",
            "archive_path",
            "claim_text",
            "status",
        ]
    )
    for record_type, section in (
        ("anchor", register["anchors"]),
        ("strategy_claim", register["strategy_claims"]),
        ("context_claim", register["context_claims"]),
    ):
        for key, record in sorted(section.items()):
            writer.writerow(
                [
                    record_type,
                    key,
                    record["source_class"],
                    _format_model_value(record.get("model_value")),
                    record["units"],
                    record["source_ref"],
                    record["organization_or_authors"],
                    record["title"],
                    record["date"],
                    record["locator"],
                    record["permanent_url_or_doi"],
                    record["extracted_value"],
                    record["transformation"],
                    record.get("archive_path", ""),
                    record.get("claim_text", ""),
                    record["status"],
                ]
            )
    return stream.getvalue()


def write_claim_provenance_csv(
    path: Path | None = None,
    *,
    provenance_path: Path | None = None,
    anchors_path: Path | None = None,
) -> Path:
    """Validate and write the public claim-level table."""
    target = path or PROVENANCE_OUTPUT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        render_claim_provenance_csv(
            provenance_path=provenance_path,
            anchors_path=anchors_path,
        ),
        encoding="utf-8",
    )
    return target
