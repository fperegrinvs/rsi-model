"""Verify both committed artifact manifests byte-for-byte."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.manifests import verify_manifest, verify_release_manifest


def main() -> None:
    release_manifest = ROOT / "outputs" / "MANIFEST.md"
    integrated_manifest = ROOT / "outputs" / "integrated" / "MANIFEST.md"
    release_verified = verify_release_manifest(release_manifest, ROOT)
    integrated_verified = verify_manifest(integrated_manifest, ROOT)
    total = len(release_verified) + len(integrated_verified)
    for manifest, verified in (
        (release_manifest, release_verified),
        (integrated_manifest, integrated_verified),
    ):
        print(f"verified {manifest.relative_to(ROOT)} ({len(verified)} paths)")
    print(f"verified {total} manifest records")


if __name__ == "__main__":
    main()
