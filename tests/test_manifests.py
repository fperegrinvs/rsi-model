"""Release manifests must match every recorded artifact byte-for-byte."""

from pathlib import Path

from rsimodel.manifests import (
    CANONICAL_HTML,
    CANONICAL_MANUSCRIPT,
    manifest_records,
    verify_manifest,
    verify_release_manifest,
)

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_release_manifest_verifies_and_covers_manuscript() -> None:
    manifest = ROOT / "outputs" / "MANIFEST.md"
    assert len(verify_release_manifest(manifest, ROOT)) == len(manifest_records(manifest))
    records = manifest_records(manifest)
    assert CANONICAL_MANUSCRIPT in records
    assert CANONICAL_HTML in records
    for path in (
        Path("params/artifact_registry.json"),
        Path("params/equation_explanations.json"),
        Path("params/notation_registry.json"),
        Path("docs/assets/fonts/STIXTwoMath-Regular.woff2"),
        Path("docs/assets/fonts/STIXTwoMath-OFL.txt"),
        Path("docs/assets/fonts/STIXTwoMath-METADATA.json"),
        Path("docs/sources/spacexai-economic-thesis-2026-07-29.md"),
        Path("tests/visual/math/desktop-diminishing-frontier.png"),
    ):
        assert path in records


def test_integrated_model_manifest_verifies() -> None:
    manifest = ROOT / "outputs" / "integrated" / "MANIFEST.md"
    assert len(verify_manifest(manifest, ROOT)) == len(manifest_records(manifest))
