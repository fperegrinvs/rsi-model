"""Validate claim-level sources and write outputs/tables/claim_provenance.csv."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from rsimodel.provenance import write_claim_provenance_csv


def main(argv: Sequence[str] | None = None) -> int:
    """Write provenance CSV to an explicit path."""
    parser = argparse.ArgumentParser(prog="rsi-write-provenance")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    output = (args.output or root / "outputs" / "tables" / "claim_provenance.csv").resolve()
    provenance_path = root / "params" / "claim_provenance.yaml"
    anchors_path = root / "params" / "anchors.yaml"
    if not provenance_path.is_file() or not anchors_path.is_file():
        print(f"not an rsi-model project: {root}", file=sys.stderr)
        return 2
    path = write_claim_provenance_csv(
        output,
        provenance_path=provenance_path,
        anchors_path=anchors_path,
    )
    try:
        label = path.relative_to(root)
    except ValueError:
        label = path
    print(f"wrote {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
