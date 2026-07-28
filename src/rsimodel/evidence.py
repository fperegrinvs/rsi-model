"""Shared fail-closed helpers for empirical evidence bundles."""
from __future__ import annotations

import hashlib
from pathlib import Path
import re
from typing import Any, Iterable

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA256_PLACEHOLDER = "REPLACE_WITH_64_CHARACTER_LOWERCASE_SHA256"


def required_field_template(
    fields: Iterable[str],
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic, visibly incomplete record template."""
    record = {field: None for field in fields}
    record.update(overrides or {})
    return record


def binary_results_template(ids: Iterable[str]) -> dict[str, dict[str, Any]]:
    """Build binary-result placeholders that cannot pass validation."""
    return {
        record_id: {
            "status": None,
            "evidence_query_sha256": SHA256_PLACEHOLDER,
            "evaluator_id": None,
            "witness_hash": SHA256_PLACEHOLDER,
        }
        for record_id in sorted(ids)
    }


def require_fields(
    record: Any,
    fields: list[str] | set[str],
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(record, dict):
        errors.append(f"{label}: must be an object")
        return
    missing = [
        field
        for field in fields
        if field not in record or record[field] in (None, "", [])
    ]
    if missing:
        errors.append(f"{label}: missing fields {sorted(missing)}")


def require_sha256(
    record: Any,
    field: str,
    label: str,
    errors: list[str],
) -> None:
    value = record.get(field) if isinstance(record, dict) else None
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        errors.append(f"{label}: {field} must be a lowercase sha256")


def require_mapping(
    value: Any,
    label: str,
    errors: list[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label}: must be an object")
        return {}
    return value


def require_list(
    value: Any,
    label: str,
    errors: list[str],
) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label}: must be an array")
        return []
    return value


def require_nonnegative_number(
    record: Any,
    field: str,
    label: str,
    errors: list[str],
) -> None:
    value = record.get(field) if isinstance(record, dict) else None
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or value < 0
    ):
        errors.append(f"{label}: {field} must be a nonnegative number")


def require_exact_ids(
    records: Any,
    expected: set[str],
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(records, dict):
        errors.append(f"{label}: must be an object")
        return
    actual = set(records)
    missing, extra = expected - actual, actual - expected
    if missing:
        errors.append(f"{label}: missing ids {sorted(missing)}")
    if extra:
        errors.append(f"{label}: unexpected ids {sorted(extra)}")


def validate_binary_results(
    records: Any,
    expected: set[str],
    label: str,
    errors: list[str],
) -> None:
    require_exact_ids(records, expected, label, errors)
    if not isinstance(records, dict):
        return
    for record_id, record in records.items():
        require_fields(
            record,
            {"status", "evidence_query_sha256", "evaluator_id", "witness_hash"},
            f"{label}.{record_id}",
            errors,
        )
        if record.get("status") not in {"pass", "fail"}:
            errors.append(f"{label}.{record_id}: status must be pass or fail")
        require_sha256(
            record,
            "evidence_query_sha256",
            f"{label}.{record_id}",
            errors,
        )
        require_sha256(record, "witness_hash", f"{label}.{record_id}", errors)


def artifact_files_template() -> dict[str, dict[str, Any]]:
    """Return a visibly incomplete content-addressed evidence index."""
    return {
        "REPLACE_WITH_ARTIFACT_ID": {
            "path": None,
            "sha256": SHA256_PLACEHOLDER,
        }
    }


def _referenced_hashes(value: Any, *, parent_key: str = "") -> set[str]:
    hashes: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "artifact_files":
                continue
            if (
                isinstance(child, str)
                and (
                    key.endswith("sha256")
                    or key.endswith("_hash")
                    or key in {"witness_hash", "source_document_hash"}
                )
                and SHA256_RE.fullmatch(child)
            ):
                hashes.add(child)
            hashes.update(_referenced_hashes(child, parent_key=key))
    elif isinstance(value, list):
        for child in value:
            hashes.update(_referenced_hashes(child, parent_key=parent_key))
    return hashes


def verify_artifact_files(
    bundle: Any,
    archive_root: Path | None,
    errors: list[str],
) -> set[str]:
    """Verify every evidence hash against a file inside ``archive_root``.

    A syntactically valid digest is not evidence. Completed bundles therefore
    carry a content-addressed file index, and every hash referenced elsewhere
    in the bundle must resolve to a byte-for-byte verified local artifact.
    """
    if archive_root is None:
        errors.append(
            "archive_root is required to verify a completed evidence bundle"
        )
        return set()
    root = archive_root.resolve()
    if not root.is_dir():
        errors.append(f"archive_root is not a directory: {archive_root}")
        return set()

    records = require_mapping(
        bundle.get("artifact_files") if isinstance(bundle, dict) else None,
        "artifact_files",
        errors,
    )
    if not records:
        errors.append("artifact_files: no evidence artifacts supplied")
        return set()

    verified: set[str] = set()
    seen_paths: set[Path] = set()
    for artifact_id, raw_record in records.items():
        label = f"artifact_files.{artifact_id}"
        record = require_mapping(raw_record, label, errors)
        require_fields(record, {"path", "sha256"}, label, errors)
        require_sha256(record, "sha256", label, errors)
        relative_value = record.get("path")
        if not isinstance(relative_value, str) or not relative_value:
            errors.append(f"{label}: path must be a nonempty relative path")
            continue
        relative = Path(relative_value)
        if relative.is_absolute():
            errors.append(f"{label}: path must be relative")
            continue
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            errors.append(f"{label}: path escapes archive_root")
            continue
        if target in seen_paths:
            errors.append(f"{label}: duplicate artifact path {relative}")
            continue
        seen_paths.add(target)
        if not target.is_file():
            errors.append(f"{label}: artifact is missing: {relative}")
            continue
        expected = record.get("sha256")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(
                f"{label}: sha256 mismatch; expected {expected}, found {actual}"
            )
            continue
        verified.add(actual)

    referenced = _referenced_hashes(bundle)
    missing = referenced - verified
    if missing:
        errors.append(
            "artifact_files: referenced hashes are not backed by verified "
            f"files {sorted(missing)}"
        )
    return verified
