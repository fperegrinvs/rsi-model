#!/usr/bin/env python3
"""Reject manuscript prose that narrates its own drafting history."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

# These patterns target editorial residue, not historical claims about the
# subject. Current edition metadata, dated evidence, source history, and
# reproducibility filenames remain valid.
RULES = {
    "draft/version comparison": re.compile(
        r"\b(?:earlier|previous|prior)\s+"
        r"(?:draft|drafts|version|versions|edition|editions)\b",
        re.IGNORECASE,
    ),
    "revision-status narration": re.compile(
        r"\b(?:is|are|was|were|has been|have been)\s+(?:now\s+)?"
        r"(?:retired|withdrawn|replaced|rewritten|revised)\b",
        re.IGNORECASE,
    ),
    "change narration": re.compile(
        r"\b(?:now|newly)\s+"
        r"(?:includes?|adds?|models?|reports?|exposes?|distinguishes?|uses?)\b"
        r"|\b(?:is|are)\s+now\b",
        re.IGNORECASE,
    ),
    "model lineage narration": re.compile(
        r"\b(?:inherited|legacy|old|new)\s+"
        r"(?:model|formulation|analysis|equation|relation)\b",
        re.IGNORECASE,
    ),
    "version-tagged analysis narration": re.compile(
        r"\br\d+(?:\.\d+)+\s+"
        r"(?:analysis|execution|extension|module|ablation|contract|model)\b",
        re.IGNORECASE,
    ),
    "revision-history narration": re.compile(
        r"\b(?:revision history|what changed under|what changed from)\b",
        re.IGNORECASE,
    ),
    "analysis-history comparison": re.compile(
        r"\b(?:the\s+)?(?:earlier|previous|former|inherited)\s+"
        r"(?:(?:[\w-]+\s+){0,3})?"
        r"(?:argument|analysis|metric|model|result|figure|calculation|boundary)\b"
        r"|\b(?:formerly|previously)\s+"
        r"(?:reported|modeled|calculated|shown)\b"
        r"|\bthe\s+(?:new|old)\s+(?:layer|model|analysis|metric)\b",
        re.IGNORECASE,
    ),
    "unversioned latest-model claim": re.compile(
        r"\b(?:the|our|a)\s+latest model\b",
        re.IGNORECASE,
    ),
    "component benchmark labeled as RSI": re.compile(
        r"\b(?:an?\s+)?RSI benchmark\b",
        re.IGNORECASE,
    ),
    "unqualified full-autonomy claim": re.compile(
        r"\b(?:is|was|are|were)\s+fully autonomous\b",
        re.IGNORECASE,
    ),
    "component result claimed as recursive closure": re.compile(
        r"\b(?:benchmark|evaluation|score|result)\s+"
        r"(?:shows?|proves?|demonstrates?)\s+"
        r"(?:recursive self-improvement|RSI)\b",
        re.IGNORECASE,
    ),
}


def main(argv: Sequence[str] | None = None) -> int:
    """Reject draft-history narration under an explicit project root."""
    parser = argparse.ArgumentParser(prog="rsi-check-prose")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    fragments = root / "docs" / "manuscript"

    failures: list[str] = []
    files = sorted(fragments.glob("*.md"))
    if not files:
        print(f"no manuscript fragments found under {fragments}", file=sys.stderr)
        return 2
    for path in files:
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in RULES.items():
                match = pattern.search(line)
                if match:
                    relative = path.relative_to(root)
                    failures.append(f"{relative}:{line_number}: {label}: {match.group(0)!r}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(
        f"PASS standalone prose audit: {len(files)} manuscript fragments, "
        f"{len(RULES)} revision-residue rules"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
