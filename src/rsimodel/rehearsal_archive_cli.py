"""Command-line capture and verification for Stage-0 rehearsal events."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

from rsimodel.rehearsal_archive import (
    append_rehearsal_event,
    initialize_rehearsal_archive,
    rehearsal_archive_report,
    write_rehearsal_archive_report,
)


def _event_from_path(path: Path) -> dict[str, object]:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("event JSON must contain one object")
    raw = cast(Mapping[object, object], value)
    if not all(isinstance(key, str) for key in raw):
        raise ValueError("event JSON object keys must be strings")
    return {str(key): child for key, child in raw.items()}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rsi-rehearsal-archive")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("archive", type=Path)

    append_parser = subparsers.add_parser("append")
    append_parser.add_argument("archive", type=Path)
    append_parser.add_argument("event", type=Path)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("archive", type=Path)
    verify_parser.add_argument("--output", type=Path)

    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            print(initialize_rehearsal_archive(args.archive))
            return 0
        if args.command == "append":
            print(append_rehearsal_event(args.archive, _event_from_path(args.event)))
            return 0
        report = rehearsal_archive_report(args.archive)
        if args.output is None:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print(write_rehearsal_archive_report(args.archive, args.output))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
