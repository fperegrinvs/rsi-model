"""Release manifests must match every recorded artifact byte-for-byte."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.manifests import (
    CANONICAL_HTML,
    CANONICAL_MANUSCRIPT,
    manifest_records,
    verify_manifest,
    verify_release_manifest,
)


def test_canonical_release_manifest_verifies_and_covers_manuscript():
    manifest = ROOT / "outputs" / "MANIFEST.md"
    assert len(verify_release_manifest(manifest, ROOT)) == len(
        manifest_records(manifest)
    )
    records = manifest_records(manifest)
    assert CANONICAL_MANUSCRIPT in records
    assert CANONICAL_HTML in records


def test_integrated_model_manifest_verifies():
    manifest = ROOT / "outputs" / "integrated" / "MANIFEST.md"
    assert len(verify_manifest(manifest, ROOT)) == len(
        manifest_records(manifest)
    )
