"""Byte-for-byte verification of committed release manifests."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CANONICAL_MANUSCRIPT = Path("docs/Recursive_Industrial_Intelligence_r4.0.md")
CANONICAL_HTML = Path("docs/Recursive_Industrial_Intelligence_r4.0.html")
REQUIRED_RELEASE_PATHS = {
    CANONICAL_MANUSCRIPT,
    CANONICAL_HTML,
    Path("CITATION.cff"),
    Path(".bun-version"),
    Path(".gitattributes"),
    Path(".gitignore"),
    Path(".python-version"),
    Path("uv.lock"),
    Path("pyproject.toml"),
    Path("package.json"),
    Path("pnpm-lock.yaml"),
    Path("pnpm-workspace.yaml"),
    Path("scripts/build-manuscript.ts"),
    Path("scripts/build-site.ts"),
    Path("scripts/artifacts.ts"),
    Path("scripts/inline-viewer.ts"),
    Path("scripts/check-accessibility.ts"),
    Path("scripts/check-artifact-viewer.ts"),
    Path("scripts/check-equation-explanations.ts"),
    Path("scripts/check-math-layout.ts"),
    Path("src/rsimodel/math_font_gate.py"),
    Path("src/rsimodel/external_links.py"),
    Path("src/rsimodel/notation_gate.py"),
    Path("src/rsimodel/prose_gate.py"),
    Path("scripts/check-scenario-policy.ts"),
    Path("scripts/check-site.ts"),
    Path("scripts/check-tables.ts"),
    Path("scripts/check-table-layout.ts"),
    Path("scripts/equation_numbering.lua"),
    Path("scripts/table_numbering.lua"),
    Path("scripts/equation_explanations.lua"),
    Path("scripts/site_adjustments.lua"),
    Path("scripts/manuscript-config.ts"),
    Path("scripts/tables.ts"),
    Path("src/rsimodel/release_manifest.py"),
    Path("docs/EDITORIAL_STYLE.md"),
    Path("docs/ORBITAL_AI_SCENARIO_POLICY.md"),
    Path("docs/EQUATION_LAYOUT_AUDIT.md"),
    Path("docs/assets/fonts/STIXTwoMath-Regular.woff2"),
    Path("docs/assets/fonts/STIXTwoMath-OFL.txt"),
    Path("docs/assets/fonts/STIXTwoMath-METADATA.json"),
    Path(".github/workflows/publication.yml"),
    Path("site/_quarto.yml"),
    Path("site/favicon.svg"),
    Path("docs/manuscript/00-front-matter.md"),
    Path("docs/manuscript/53-notation-register.md"),
    Path("params/integrated_model.yaml"),
    Path("params/artifact_registry.json"),
    Path("outputs/quality/artifact_viewer_size_report.json"),
    Path("params/ai_rnd_evidence_registry.json"),
    Path("params/equation_explanations.json"),
    Path("params/notation_registry.json"),
    Path("params/propositions.json"),
    Path("params/orbital_ai_scenario_registry.json"),
    Path("params/spacexai_economic_case.json"),
    Path("docs/sources/spacexai-economic-thesis-2026-07-29.md"),
    Path("docs/reviews/readability-review.json"),
    Path("src/rsimodel/integrated_pipeline.py"),
    Path("web/artifact-viewer-shell.ts"),
    Path("web/artifact-viewer.css"),
    Path("web/artifact-viewer.ts"),
    Path("web/standalone.ts"),
    Path("src/rsimodel/ai_rnd_evidence.py"),
    Path("src/rsimodel/integrated_artifacts.py"),
    Path("src/rsimodel/integrated_tables.py"),
    Path("src/rsimodel/integrated_figures.py"),
    Path("src/rsimodel/integrated_report.py"),
    Path("src/rsimodel/integrated_extension_tables.py"),
    Path("src/rsimodel/integrated_digital_tables.py"),
    Path("src/rsimodel/integrated_coordination_tables.py"),
    Path("src/rsimodel/integrated_embodiment_tables.py"),
    Path("src/rsimodel/integrated_orbital_tables.py"),
    Path("src/rsimodel/integrated_closure_tables.py"),
    Path("src/rsimodel/integrated_runner.py"),
    Path("src/rsimodel/run_config.py"),
    Path("src/rsimodel/orbital_ai_scenarios.py"),
    Path("src/rsimodel/spacexai_economics.py"),
    Path("src/rsimodel/extensions.py"),
    Path("src/rsimodel/extensions_digital.py"),
    Path("src/rsimodel/extensions_coordination.py"),
    Path("src/rsimodel/extensions_orbital.py"),
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
            failures.append(f"{relative}: expected {expected}, found {actual}")
            continue
        verified.append(relative)
    if failures:
        raise ValueError(f"{manifest}: verification failed\n- " + "\n- ".join(failures))
    return verified


def verify_release_manifest(manifest: Path, root: Path) -> list[Path]:
    """Verify bytes and reject an incomplete or historically named release."""
    records = manifest_records(manifest)
    failures: list[str] = []
    missing_required = REQUIRED_RELEASE_PATHS - set(records)
    if missing_required:
        failures.append(
            f"missing required release paths {sorted(str(path) for path in missing_required)}"
        )

    output_files = {
        path.relative_to(root)
        for path in (root / "outputs").glob("**/*")
        if path.is_file()
        and path != manifest
        and path.name != ".DS_Store"
        and root / "outputs" / "quality" not in path.parents
    }
    missing_outputs = output_files - set(records)
    if missing_outputs:
        failures.append(
            f"generated outputs omitted {sorted(str(path) for path in missing_outputs)}"
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
        raise ValueError(f"{manifest}: release policy failed\n- " + "\n- ".join(failures))
    return verify_manifest(manifest, root)
