"""Claim-level source validation and deterministic provenance-table output.

Runtime provenance explains which anchor a calculation used. This module
enforces the stronger publication contract: every non-ASSUMPTION anchor has
an exact source locator, extracted value, units, transformation, and
persistent identifier. It also validates the SEC-filing claims grouped under
manuscript reference [S27].
"""
from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

import yaml

from .delta import PARAMS_DIR, load_anchors

ROOT = Path(__file__).resolve().parents[2]
PROVENANCE_PATH = PARAMS_DIR / "claim_provenance.yaml"
PROVENANCE_OUTPUT = ROOT / "outputs" / "tables" / "claim_provenance.csv"

REQUIRED_FIELDS = (
    "source_class",
    "units",
    "source_ref",
    "organization_or_authors",
    "title",
    "date",
    "locator",
    "permanent_url_or_doi",
    "extracted_value",
    "transformation",
    "status",
)
STRATEGY_REQUIRED_FIELDS = REQUIRED_FIELDS + ("claim_text",)


def load_claim_provenance(path: Path | None = None) -> dict[str, Any]:
    """Load the claim-level publication register."""
    return yaml.safe_load((path or PROVENANCE_PATH).read_text(encoding="utf-8"))


def _model_value(entry: dict[str, Any]) -> dict[str, float]:
    if "value" in entry:
        return {"value": float(entry["value"])}
    return {"low": float(entry["low"]), "high": float(entry["high"])}


def _missing(record: dict[str, Any], required: tuple[str, ...]) -> list[str]:
    return [
        field for field in required
        if field not in record or record[field] is None or record[field] == ""
    ]


def validate_claim_provenance(
    register: dict[str, Any] | None = None,
    anchors: dict[str, dict[str, Any]] | None = None,
) -> None:
    """Raise ``ValueError`` if the register violates the release contract."""
    register = register or load_claim_provenance()
    anchors = anchors or load_anchors()
    anchor_records = register.get("anchors", {})
    strategy_records = register.get("strategy_claims", {})

    expected = {
        name for name, entry in anchors.items()
        if entry["source_class"] != "ASSUMPTION"
    }
    actual = set(anchor_records)
    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(
            f"claim-provenance anchor coverage mismatch; missing={missing}, "
            f"extra={extra}"
        )

    errors: list[str] = []
    for name in sorted(expected):
        record = anchor_records[name]
        absent = _missing(record, REQUIRED_FIELDS + ("model_value",))
        if absent:
            errors.append(f"{name}: missing {absent}")
        if record.get("status") != "verified":
            errors.append(f"{name}: status must be verified")
        if record.get("source_class") != anchors[name]["source_class"]:
            errors.append(
                f"{name}: source_class {record.get('source_class')!r} != "
                f"{anchors[name]['source_class']!r}"
            )
        if record.get("model_value") != _model_value(anchors[name]):
            errors.append(
                f"{name}: model_value {record.get('model_value')!r} != "
                f"{_model_value(anchors[name])!r}"
            )
        if "S36" in str(record.get("source_ref", "")):
            errors.append(f"{name}: collective S36 is not claim-level provenance")

    if not strategy_records:
        errors.append("strategy_claims: no S27 claim records")
    for name, record in sorted(strategy_records.items()):
        absent = _missing(record, STRATEGY_REQUIRED_FIELDS)
        if absent:
            errors.append(f"{name}: missing {absent}")
        if record.get("status") != "verified":
            errors.append(f"{name}: status must be verified")
        if record.get("source_ref") != "S27":
            errors.append(f"{name}: strategy record must resolve to S27")
        locator = str(record.get("locator", "")).lower()
        if not any(token in locator for token in ("p.", "pp.", "slide")):
            errors.append(f"{name}: locator is not page- or slide-level")
        permanent = str(record.get("permanent_url_or_doi", ""))
        if "sec.gov/Archives/edgar/data/" not in permanent:
            errors.append(f"{name}: missing permanent SEC EDGAR URL")

    if errors:
        raise ValueError("invalid claim provenance:\n- " + "\n- ".join(errors))


def _format_model_value(value: dict[str, Any] | None) -> str:
    if not value:
        return ""
    if "value" in value:
        return str(value["value"])
    return f"{value['low']}..{value['high']}"


def render_claim_provenance_csv(
    register: dict[str, Any] | None = None,
    anchors: dict[str, dict[str, Any]] | None = None,
) -> str:
    """Render the validated register in a stable, reviewer-friendly table."""
    register = register or load_claim_provenance()
    anchors = anchors or load_anchors()
    validate_claim_provenance(register, anchors)

    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow([
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
    ])
    for record_type, section in (
        ("anchor", register["anchors"]),
        ("strategy_claim", register["strategy_claims"]),
    ):
        for key, record in sorted(section.items()):
            writer.writerow([
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
            ])
    return stream.getvalue()


def write_claim_provenance_csv(path: Path | None = None) -> Path:
    """Validate and write the public claim-level table."""
    target = path or PROVENANCE_OUTPUT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_claim_provenance_csv(), encoding="utf-8")
    return target
