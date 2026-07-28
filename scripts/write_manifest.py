"""Write the canonical release manifest after all generators and HTML build."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
MANIFEST = OUT / "MANIFEST.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _files(directory: Path, pattern: str) -> set[Path]:
    return {path for path in directory.glob(pattern) if path.is_file()}


def release_artifacts() -> list[Path]:
    """Return the exact non-circular set covered by the release manifest."""
    paths = {
        ROOT / "CHANGELOG.md",
        ROOT / "CITATION.cff",
        ROOT / "CLAUDE.md",
        ROOT / "LICENSE",
        ROOT / "README.md",
        ROOT / "ROADMAP.md",
        ROOT / "package.json",
        ROOT / "requirements.lock",
        ROOT / "requirements.txt",
        ROOT / "docs" / "LICENSE",
        ROOT / "docs" / "Recursive_Industrial_Intelligence_r4.0.md",
        ROOT / "docs" / "Recursive_Industrial_Intelligence_r4.0.html",
    }
    for directory, pattern in (
        (ROOT / ".github" / "workflows", "*.yml"),
        (ROOT / "docs", "*.md"),
        (ROOT / "docs" / "assets", "*"),
        (ROOT / "papers", "*.md"),
        (ROOT / "params", "*.yaml"),
        (ROOT / "scripts", "*.py"),
        (ROOT / "scripts", "*.cjs"),
        (ROOT / "src" / "rsimodel", "*.py"),
        (ROOT / "tests", "*.py"),
        (OUT, "**/*"),
    ):
        paths.update(_files(directory, pattern))
    paths.discard(MANIFEST)
    return sorted(paths)


def main() -> None:
    artifacts = release_artifacts()
    missing = [path for path in artifacts if not path.is_file()]
    if missing:
        raise SystemExit(
            "Build release artifacts before the manifest; missing: "
            + ", ".join(str(path.relative_to(ROOT)) for path in missing)
        )

    lines = [
        "# Release manifest",
        "",
        "- scope: canonical manuscript, release inputs, tests, and generated artifacts",
        "- generator: `scripts/write_manifest.py` (run after every model generator and `npm run build:manuscript`)",
        "- note: this manifest omits itself to avoid a circular digest",
        "",
        "| artifact | sha256 |",
        "|---|---|",
    ]
    lines.extend(
        f"| {path.relative_to(ROOT)} | {sha256(path)} |"
        for path in artifacts
    )
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST} ({len(artifacts)} artifacts)")


if __name__ == "__main__":
    main()
