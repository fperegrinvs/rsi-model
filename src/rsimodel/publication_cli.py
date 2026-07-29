"""Validate external author authorization for the r4.0 paper set."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from rsimodel.publication import (
    publication_authorization_gates,
    publication_authorization_template,
)
from rsimodel.yaml_adapter import require_mapping


def main(argv: Sequence[str] | None = None) -> int:
    """Validate or create an external publication-authorization record."""
    parser = argparse.ArgumentParser(prog="rsi-publication-preflight")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--authorization-record",
        type=Path,
        help=(
            "external JSON record containing author confirmations, exact "
            "file hashes, packaging evidence, and final approval"
        ),
    )
    group.add_argument(
        "--write-authorization-template",
        type=Path,
        help="write a deliberately non-passing external approval template",
    )
    args = parser.parse_args(argv)

    if args.write_authorization_template is not None:
        args.write_authorization_template.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        args.write_authorization_template.write_text(
            json.dumps(
                publication_authorization_template(),
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(args.write_authorization_template)
        return 0

    try:
        record_value: object = json.loads(args.authorization_record.read_text(encoding="utf-8"))
        record = require_mapping(
            record_value,
            label="publication authorization record",
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"cannot read publication authorization record: {exc}", file=sys.stderr)
        return 2
    gates = publication_authorization_gates(record)
    for gate in gates:
        print(f"{'PASS' if gate.passed else 'FAIL'} {gate.name}: {gate.detail}")
    failed = [gate for gate in gates if not gate.passed]
    if failed:
        print(f"publication preflight failed: {len(failed)} gate(s)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
