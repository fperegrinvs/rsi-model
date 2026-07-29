"""Validate a process, rehearsal, or economic empirical evidence bundle."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from rsimodel.economic_calibration import (
    economic_calibration_bundle_template,
    evaluate_economic_calibration_bundle,
)
from rsimodel.process_closure import (
    evaluate_process_closure_bundle,
    process_closure_bundle_template,
)
from rsimodel.rehearsal import (
    evaluate_rehearsal_evidence_bundle,
    rehearsal_evidence_bundle_template,
)
from rsimodel.yaml_adapter import require_mapping

EVALUATORS = {
    "process_closure": evaluate_process_closure_bundle,
    "rehearsal": evaluate_rehearsal_evidence_bundle,
    "economic_calibration": evaluate_economic_calibration_bundle,
}
TEMPLATES = {
    "process_closure": process_closure_bundle_template,
    "rehearsal": rehearsal_evidence_bundle_template,
    "economic_calibration": economic_calibration_bundle_template,
}


def main(argv: Sequence[str] | None = None) -> int:
    """Evaluate or create one evidence-bundle record."""
    parser = argparse.ArgumentParser(prog="rsi-evaluate-evidence")
    parser.add_argument("kind", choices=tuple(EVALUATORS))
    parser.add_argument("bundle", type=Path, nargs="?")
    parser.add_argument(
        "--archive-root",
        type=Path,
        help=(
            "directory containing every content-addressed artifact named by the completed bundle"
        ),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--write-template",
        type=Path,
        help=(
            "write a complete-shape JSON template that remains invalid "
            "until real evidence replaces every placeholder"
        ),
    )
    args = parser.parse_args(argv)
    if args.write_template is not None:
        if args.bundle is not None or args.output is not None or args.archive_root is not None:
            parser.error("--write-template cannot be combined with bundle or --output")
        args.write_template.parent.mkdir(parents=True, exist_ok=True)
        args.write_template.write_text(
            json.dumps(
                TEMPLATES[args.kind](),
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(args.write_template)
        return 0
    if args.bundle is None:
        parser.error("bundle is required unless --write-template is used")
    if args.archive_root is None:
        parser.error("--archive-root is required for bundle evaluation")
    try:
        bundle_value: object = json.loads(args.bundle.read_text(encoding="utf-8"))
        bundle = require_mapping(bundle_value, label="evidence bundle")
        result = EVALUATORS[args.kind](
            bundle,
            archive_root=args.archive_root,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
