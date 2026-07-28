"""Run r4.0 release-candidate or immutable-publication preflight."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.release import (
    Gate,
    release_authorization_gates,
    release_authorization_template,
    repository_gates,
)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
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
    args = parser.parse_args()
    if args.write_authorization_template is not None:
        if args.authorization_record is not None:
            parser.error(
                "--write-authorization-template cannot be combined with "
                "--authorization-record"
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
        return
    if args.mode == "publication" and args.authorization_record is None:
        parser.error(
            "--authorization-record is required in publication mode"
        )

    gates = repository_gates(
        ROOT,
        args.mode,
        os.environ.get("RELEASE_DATE"),
        os.environ.get("VERSION_DOI"),
        os.environ.get("CANONICAL_URL"),
    )
    dirty = bool(_git("status", "--porcelain"))
    gates.append(
        Gate(
            "clean_worktree",
            not dirty or args.allow_dirty,
            "dirty allowed for development" if dirty else "clean",
        )
    )
    tags = set(_git("tag", "--list").splitlines())
    head = _git("rev-parse", "HEAD")
    if args.mode == "candidate":
        gates.append(
            Gate(
                "candidate_tag_absent",
                "r4.0" not in tags,
                "r4.0 absent" if "r4.0" not in tags else "r4.0 already exists",
            )
        )
    else:
        tag_commit = _git("rev-list", "-n", "1", "r4.0") if "r4.0" in tags else ""
        gates.append(
            Gate(
                "publication_tag_at_head",
                tag_commit == head,
                tag_commit or "r4.0 missing",
            )
        )
        try:
            authorization = json.loads(
                args.authorization_record.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise SystemExit(
                f"cannot read authorization record: {exc}"
            ) from exc
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
        raise SystemExit(f"preflight failed: {len(failed)} gate(s)")


if __name__ == "__main__":
    main()
