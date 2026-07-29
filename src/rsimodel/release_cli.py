"""Run r4.0 release-candidate or immutable-publication preflight."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from rsimodel.release import (
    Gate,
    release_authorization_gates,
    release_authorization_template,
    repository_gates,
)
from rsimodel.yaml_adapter import require_mapping

GIT = shutil.which("git")


def _git(root: Path, *args: str) -> str:
    if GIT is None:
        raise RuntimeError("git is required for release preflight")
    return subprocess.run(  # noqa: S603 -- resolved git binary and explicit argument vector.
        [GIT, *args],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def main(argv: Sequence[str] | None = None) -> int:
    """Run candidate or immutable-publication checks for one repository."""
    parser = argparse.ArgumentParser(prog="rsi-release-preflight")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--mode",
        choices=("candidate", "publication"),
        default="candidate",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Development only: report rather than fail the clean-tree gate.",
    )
    parser.add_argument(
        "--authorization-record",
        type=Path,
        help=(
            "external JSON approval tied to the exact publication commit; "
            "required in publication mode"
        ),
    )
    parser.add_argument(
        "--write-authorization-template",
        type=Path,
        help="write a deliberately non-passing external approval template",
    )
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    if not (root / ".git").exists() or not (root / "pyproject.toml").is_file():
        print(f"not an rsi-model Git repository: {root}", file=sys.stderr)
        return 2
    if args.write_authorization_template is not None:
        if args.authorization_record is not None:
            parser.error(
                "--write-authorization-template cannot be combined with --authorization-record"
            )
        args.write_authorization_template.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        args.write_authorization_template.write_text(
            json.dumps(
                release_authorization_template(),
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(args.write_authorization_template)
        return 0
    if args.mode == "publication" and args.authorization_record is None:
        parser.error("--authorization-record is required in publication mode")

    try:
        gates = repository_gates(
            root,
            args.mode,
            os.environ.get("RELEASE_DATE"),
            os.environ.get("VERSION_DOI"),
            os.environ.get("CANONICAL_URL"),
        )
    except ValueError as exc:
        print(f"invalid publication metadata: {exc}", file=sys.stderr)
        return 2
    dirty = bool(_git(root, "status", "--porcelain"))
    gates.append(
        Gate(
            "clean_worktree",
            not dirty or args.allow_dirty,
            "dirty allowed for development" if dirty else "clean",
        )
    )
    tags = set(_git(root, "tag", "--list").splitlines())
    head = _git(root, "rev-parse", "HEAD")
    if args.mode == "candidate":
        gates.append(
            Gate(
                "candidate_tag_absent",
                "r4.0" not in tags,
                "r4.0 absent" if "r4.0" not in tags else "r4.0 already exists",
            )
        )
    else:
        tag_commit = _git(root, "rev-list", "-n", "1", "r4.0") if "r4.0" in tags else ""
        gates.append(
            Gate(
                "publication_tag_at_head",
                tag_commit == head,
                tag_commit or "r4.0 missing",
            )
        )
        try:
            authorization_value: object = json.loads(
                args.authorization_record.read_text(encoding="utf-8")
            )
            authorization = require_mapping(
                authorization_value,
                label="authorization record",
            )
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"cannot read authorization record: {exc}", file=sys.stderr)
            return 2
        gates.extend(
            release_authorization_gates(
                authorization,
                head_commit=head,
                release_date=os.environ["RELEASE_DATE"],
                version_doi=os.environ["VERSION_DOI"],
                canonical_url=os.environ["CANONICAL_URL"],
                evidence_root=args.authorization_record.parent,
            )
        )

    for gate in gates:
        print(f"{'PASS' if gate.passed else 'FAIL'} {gate.name}: {gate.detail}")
    failed = [gate for gate in gates if not gate.passed]
    if failed:
        print(f"preflight failed: {len(failed)} gate(s)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
