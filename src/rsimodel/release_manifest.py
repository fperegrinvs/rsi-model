"""Write the canonical release manifest after all generators and HTML build."""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections.abc import Sequence
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _files(directory: Path, pattern: str, quality_directory: Path) -> set[Path]:
    return {
        path
        for path in directory.glob(pattern)
        if path.is_file()
        and path.name != ".DS_Store"
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
        and quality_directory not in path.parents
    }


def release_artifacts(root: Path) -> list[Path]:
    """Return the exact non-circular set covered by the release manifest."""
    output_directory = root / "outputs"
    manifest = output_directory / "MANIFEST.md"
    quality_directory = output_directory / "quality"
    paths = {
        root / "CHANGELOG.md",
        root / "CITATION.cff",
        root / "CLAUDE.md",
        root / "LICENSE",
        root / "README.md",
        root / "ROADMAP.md",
        root / ".bun-version",
        root / ".markdownlint-cli2.jsonc",
        root / ".python-version",
        root / ".yamllint.yaml",
        root / "biome.json",
        root / "eslint.config.mjs",
        root / "package.json",
        root / "pnpm-lock.yaml",
        root / "pnpm-workspace.yaml",
        root / "pyproject.toml",
        root / "tsconfig.json",
        root / "uv.lock",
        root / "vite.config.ts",
        root / "docs" / "LICENSE",
        root / "docs" / "Recursive_Industrial_Intelligence_r4.0.md",
        root / "docs" / "Recursive_Industrial_Intelligence_r4.0.html",
        root / "outputs" / "quality" / "artifact_viewer_size_report.json",
        root / "web" / "artifact-viewer.css",
    }
    for directory, pattern in (
        (root / ".github" / "workflows", "*.yml"),
        (root / ".github", "*.yml"),
        (root / "docs", "*.md"),
        (root / "docs" / "manuscript", "*.md"),
        (root / "docs" / "reviews", "*.json"),
        (root / "docs" / "reviews", "*.md"),
        (root / "docs" / "sources", "**/*.md"),
        (root / "docs" / "assets", "**/*"),
        (root / "papers", "*.md"),
        (root / "params", "*.yaml"),
        (root / "params", "*.json"),
        (root / "scripts", "*.py"),
        (root / "scripts", "*.ts"),
        (root / "scripts", "*.lua"),
        (root / "src" / "rsimodel", "*.py"),
        (root / "tests", "**/*"),
        (root / "site", "*.qmd"),
        (root / "site", "*.yml"),
        (root / "site", "*.css"),
        (root / "site", "*.svg"),
        (root / "site", "**/*.qmd"),
        (root / "web", "*.ts"),
        (output_directory, "**/*"),
    ):
        paths.update(_files(directory, pattern, quality_directory))
    paths.discard(manifest)
    return sorted(paths)


def main(argv: Sequence[str] | None = None) -> int:
    """Write the canonical release manifest for one explicit project root."""
    parser = argparse.ArgumentParser(prog="rsi-write-manifest")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    if not (root / "pyproject.toml").is_file():
        print(f"not an rsi-model project: {root}", file=sys.stderr)
        return 2
    manifest = (args.output or root / "outputs" / "MANIFEST.md").resolve()
    artifacts = release_artifacts(root)
    missing = [path for path in artifacts if not path.is_file()]
    if missing:
        print(
            "Build release artifacts before the manifest; missing: "
            + ", ".join(str(path.relative_to(root)) for path in missing),
            file=sys.stderr,
        )
        return 1

    lines = [
        "# Release manifest",
        "",
        "- scope: canonical manuscript, release inputs, tests, and generated artifacts",
        "- generator: `rsi-write-manifest` (run after every model generator "
        "and the Pandoc/Quarto builds)",
        "- note: this manifest omits itself to avoid a circular digest",
        "",
        "| artifact | sha256 |",
        "|---|---|",
    ]
    lines.extend(f"| {path.relative_to(root)} | {sha256(path)} |" for path in artifacts)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {manifest} ({len(artifacts)} artifacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
