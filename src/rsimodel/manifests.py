"""Byte-for-byte verification of committed release manifests."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CANONICAL_MANUSCRIPT = Path(
    "docs/Recursive_Industrial_Intelligence_r4.0.md"
)
CANONICAL_HTML = Path(
    "docs/Recursive_Industrial_Intelligence_r4.0.html"
)
REQUIRED_RELEASE_PATHS = {
    CANONICAL_MANUSCRIPT,
    CANONICAL_HTML,
    Path("CITATION.cff"),
    Path("requirements.lock"),
    Path("package.json"),
    Path("scripts/build_manuscript.cjs"),
    Path("scripts/write_manifest.py"),
    Path(".github/workflows/publication.yml"),
    Path("params/integrated_model.yaml"),
    Path("scripts/run_integrated.py"),
    Path("src/rsimodel/integrated.py"),
    Path("src/rsimodel/integrated_analysis.py"),
    Path("outputs/integrated/MANIFEST.md"),
}


def manifest_records(manifest: Path) -> dict[Path, str]:
    """Parse the two-column Markdown artifact table."""
    records: dict[Path, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) != 2 or not SHA256_RE.fullmatch(cells[1]):
            continue
        path = Path(cells[0])
        if path in records:
            raise ValueError(f"{manifest}: duplicate artifact {path}")
        records[path] = cells[1]
    if not records:
        raise ValueError(f"{manifest}: no artifact records")
    return records


def verify_manifest(manifest: Path, root: Path) -> list[Path]:
    """Return verified paths or raise with every missing/mismatched record."""
    root = root.resolve()
    failures: list[str] = []
    verified: list[Path] = []
    for relative, expected in manifest_records(manifest).items():
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            failures.append(f"{relative}: escapes repository root")
            continue
        if not target.is_file():
            failures.append(f"{relative}: missing")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            failures.append(
                f"{relative}: expected {expected}, found {actual}"
            )
            continue
        verified.append(relative)
    if failures:
        raise ValueError(
            f"{manifest}: verification failed\n- " + "\n- ".join(failures)
        )
    return verified


def verify_release_manifest(manifest: Path, root: Path) -> list[Path]:
    """Verify bytes and reject an incomplete or historically named release."""
    records = manifest_records(manifest)
    failures: list[str] = []
    missing_required = REQUIRED_RELEASE_PATHS - set(records)
    if missing_required:
        failures.append(
            "missing required release paths "
            f"{sorted(str(path) for path in missing_required)}"
        )

    output_files = {
        path.relative_to(root)
        for path in (root / "outputs").glob("**/*")
        if path.is_file() and path != manifest
    }
    missing_outputs = output_files - set(records)
    if missing_outputs:
        failures.append(
            "generated outputs omitted "
            f"{sorted(str(path) for path in missing_outputs)}"
        )

    historical = {
        path
        for path in records
        if re.search(
            r"(?:^|[/_ -])(?:2nd|3rd|4th)[_ -]Ed[^/]*",
            str(path),
            flags=re.IGNORECASE,
        )
    }
    if historical:
        failures.append(
            "historically named release paths are forbidden "
            f"{sorted(str(path) for path in historical)}"
        )
    if failures:
        raise ValueError(
            f"{manifest}: release policy failed\n- "
            + "\n- ".join(failures)
        )
    return verify_manifest(manifest, root)
