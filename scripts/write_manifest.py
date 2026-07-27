"""Write outputs/MANIFEST.md: sha256 of every inherited release artifact.

Run AFTER the three run scripts and HTML build. The
manuscript cites this manifest; CI (or a reviewer) regenerates the artifacts
from a clean checkout and diffs the checksums (r3.5 reproducibility freeze).
The manifest deliberately omits a Git commit/dirty flag: embedding the commit
that contains the manifest creates a circular release artifact.
"""
import hashlib
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


release_docs = [
    ROOT / "docs" / "Recursive_Industrial_Intelligence_3rd_Ed_r3.5.md",
    ROOT / "docs" / "Recursive_Industrial_Intelligence_3rd_Ed_r3.5.html",
]
artifacts = sorted(
    list(OUT.glob("*.md")) + list((OUT / "tables").glob("*.csv"))
    + list((OUT / "figures").glob("*.png")) + release_docs)
artifacts = [p for p in artifacts if p.name != "MANIFEST.md"]
missing = [p for p in artifacts if not p.exists()]
if missing:
    raise SystemExit(
        "Build release artifacts before the manifest; missing: "
        + ", ".join(str(p.relative_to(ROOT)) for p in missing)
    )

import numpy, osqp, scipy, yaml  # noqa: E402
lines = [
    "# Output manifest",
    "",
    f"- generated: {date.today().isoformat()}",
    f"- python: {sys.version.split()[0]}, numpy {numpy.__version__}, "
    f"scipy {scipy.__version__}, osqp {osqp.__version__}",
    "- generators: scripts/run_baseline.py, scripts/run_part2.py, "
    "scripts/run_deep.py, npm run build:manuscript "
    "(in that order), then this script",
    "",
    "| artifact | sha256 |",
    "|---|---|",
]
lines += [f"| {p.relative_to(ROOT)} | {sha256(p)} |" for p in artifacts]
(OUT / "MANIFEST.md").write_text("\n".join(lines) + "\n")
print(f"wrote {OUT / 'MANIFEST.md'} ({len(artifacts)} artifacts)")
