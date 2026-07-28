"""Validate external author authorization for the r4.0 paper set."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.publication import (
    publication_authorization_gates,
    publication_authorization_template,
)


def main() -> None:
    parser = argparse.ArgumentParser()
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
    args = parser.parse_args()

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
        return

    try:
        record = json.loads(
            args.authorization_record.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(
            f"cannot read publication authorization record: {exc}"
        ) from exc
    gates = publication_authorization_gates(record)
    for gate in gates:
        print(
            f"{'PASS' if gate.passed else 'FAIL'} "
            f"{gate.name}: {gate.detail}"
        )
    failed = [gate for gate in gates if not gate.passed]
    if failed:
        raise SystemExit(
            f"publication preflight failed: {len(failed)} gate(s)"
        )


if __name__ == "__main__":
    main()
