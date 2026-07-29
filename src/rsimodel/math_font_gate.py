#!/usr/bin/env python3
"""Validate the pinned self-hosted MathML font and its publication metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from .font_adapter import inspect_font


def digest(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()


def report_failures(messages: Sequence[str]) -> int:
    for message in messages:
        print(f"FAIL {message}", file=sys.stderr)
    return 1


def read_metadata(metadata_file: Path, failures: list[str]) -> dict[str, object]:
    try:
        loaded: object = json.loads(metadata_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"font metadata cannot be read: {error}")
        return {}
    if not isinstance(loaded, dict):
        failures.append("font metadata must be a JSON object")
        return {}
    return cast(dict[str, object], loaded)


def main(argv: Sequence[str] | None = None) -> int:
    """Validate the pinned MathML font under an explicit project root."""
    parser = argparse.ArgumentParser(prog="rsi-check-math-font")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    font_directory = root / "docs" / "assets" / "fonts"
    font = font_directory / "STIXTwoMath-Regular.woff2"
    license_file = font_directory / "STIXTwoMath-OFL.txt"
    metadata_file = font_directory / "STIXTwoMath-METADATA.json"

    failures: list[str] = []
    failures.extend(
        f"missing font asset {file.relative_to(root)}"
        for file in (font, license_file, metadata_file)
        if not file.is_file()
    )
    if failures:
        return report_failures(failures)

    metadata = read_metadata(metadata_file, failures)
    if metadata.get("sha256") != digest(font):
        failures.append("font checksum differs from pinned metadata")
    if metadata.get("licenseSha256") != digest(license_file):
        failures.append("font-license checksum differs from pinned metadata")
    if metadata.get("license") != "SIL Open Font License 1.1":
        failures.append("font metadata must name the SIL Open Font License 1.1")
    if "SIL OPEN FONT LICENSE Version 1.1" not in license_file.read_text(encoding="utf-8"):
        failures.append("font license text is not OFL 1.1")

    inspection = inspect_font(font)
    required_tables = metadata.get("requiredTables")
    raw_tables = cast(list[object], required_tables) if isinstance(required_tables, list) else []
    if not isinstance(required_tables, list) or not all(
        isinstance(table, str) for table in raw_tables
    ):
        failures.append("font metadata requiredTables must be a string array")
    else:
        typed_required_tables = cast(list[str], required_tables)
        missing_tables = sorted(set(typed_required_tables) - inspection.tables)
        if missing_tables:
            failures.append(f"font is missing required tables: {', '.join(missing_tables)}")
    expected_names = {
        "family": inspection.family,
        "style": inspection.style,
        "internalVersion": inspection.internal_version,
    }
    for field, actual in expected_names.items():
        if metadata.get(field) != actual:
            failures.append(f"font metadata {field} differs from the font name table")
    if inspection.flavor != "woff2":
        failures.append(f"font flavor must be woff2; found {inspection.flavor or 'raw sfnt'}")

    css_contracts = {
        root / "docs" / "assets" / "manuscript.css": "fonts/STIXTwoMath-Regular.woff2",
        root / "site" / "quarto.css": "assets/fonts/STIXTwoMath-Regular.woff2",
    }
    for css_file, expected_url in css_contracts.items():
        css = css_file.read_text(encoding="utf-8")
        if f'url("{expected_url}") format("woff2")' not in css:
            failures.append(f"{css_file.relative_to(root)} does not load the pinned font")
        if 'math {\n  font-family: "STIX Two Math", math;' not in css:
            failures.append(f"{css_file.relative_to(root)} lacks the explicit MathML font rule")
        if "font-display: swap" not in css:
            failures.append(f"{css_file.relative_to(root)} lacks the declared font-display policy")

    if failures:
        return report_failures(failures)
    print(
        "PASS math font: STIX Two Math "
        f"{metadata.get('upstreamRelease')} ({font.stat().st_size:,} bytes), "
        "pinned checksum, OFL-1.1, WOFF2, and OpenType MATH table"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
