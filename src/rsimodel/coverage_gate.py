"""Machine-readable aggregate and critical-module coverage policy."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Final, cast

AGGREGATE_FLOOR: Final = 85.0
CRITICAL_MODULE_FLOORS: Final[dict[str, float]] = {
    "src/rsimodel/economic_calibration.py": 70.0,
    "src/rsimodel/evidence.py": 70.0,
    "src/rsimodel/integrated.py": 85.0,
    "src/rsimodel/lco.py": 85.0,
    "src/rsimodel/manifests.py": 70.0,
    "src/rsimodel/model.py": 85.0,
    "src/rsimodel/process_closure.py": 70.0,
    "src/rsimodel/provenance.py": 70.0,
    "src/rsimodel/publication.py": 70.0,
    "src/rsimodel/rehearsal.py": 70.0,
    "src/rsimodel/release.py": 70.0,
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rsi-check-coverage",
        description="Enforce aggregate and critical-module floors from coverage.py JSON.",
    )
    parser.add_argument(
        "report",
        type=Path,
        nargs="?",
        default=Path("outputs/quality/coverage.json"),
    )
    return parser


def _percent(mapping: Mapping[str, object], label: str) -> float:
    value = mapping.get("percent_covered")
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label}: missing numeric percent_covered")
    return float(value)


def coverage_failures(report: Mapping[str, object]) -> list[str]:
    """Return every failed floor rather than stopping at the first module."""
    totals = report.get("totals")
    files = report.get("files")
    if not isinstance(totals, Mapping) or not isinstance(files, Mapping):
        raise ValueError("coverage report must contain object-valued totals and files")
    typed_totals = cast(Mapping[str, object], totals)
    typed_files = cast(Mapping[str, object], files)

    failures: list[str] = []
    aggregate = _percent(typed_totals, "totals")
    if aggregate < AGGREGATE_FLOOR:
        failures.append(f"aggregate coverage {aggregate:.2f}% is below {AGGREGATE_FLOOR:.2f}%")

    for module, floor in CRITICAL_MODULE_FLOORS.items():
        entry = typed_files.get(module)
        if not isinstance(entry, Mapping):
            failures.append(f"critical module is absent from coverage: {module}")
            continue
        typed_entry = cast(Mapping[str, object], entry)
        summary = typed_entry.get("summary")
        if not isinstance(summary, Mapping):
            failures.append(f"{module}: missing summary")
            continue
        percent = _percent(cast(Mapping[str, object], summary), module)
        if percent < floor:
            failures.append(f"{module}: coverage {percent:.2f}% is below {floor:.2f}%")
    return failures


def coverage_main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        document: object = json.loads(args.report.read_text(encoding="utf-8"))
        if not isinstance(document, Mapping):
            raise ValueError("coverage report root must be an object")
        failures = coverage_failures(cast(Mapping[str, object], document))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL coverage policy: {exc}", file=sys.stderr)
        return 2

    if failures:
        for failure in failures:
            print(f"FAIL coverage policy: {failure}", file=sys.stderr)
        return 1
    print(
        "PASS coverage policy: "
        f"aggregate >= {AGGREGATE_FLOOR:.0f}% and "
        f"{len(CRITICAL_MODULE_FLOORS)} critical-module floors"
    )
    return 0
