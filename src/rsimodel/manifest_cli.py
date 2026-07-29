"""Verify both committed artifact manifests byte-for-byte."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from rsimodel.manifests import verify_manifest, verify_release_manifest


def main(argv: Sequence[str] | None = None) -> int:
    """Verify release and integrated manifests under an explicit project root."""
    parser = argparse.ArgumentParser(prog="rsi-verify-manifests")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    release_manifest = root / "outputs" / "MANIFEST.md"
    integrated_manifest = root / "outputs" / "integrated" / "MANIFEST.md"
    try:
        release_verified = verify_release_manifest(release_manifest, root)
        integrated_verified = verify_manifest(integrated_manifest, root)
    except (OSError, ValueError) as exc:
        print(f"manifest verification failed: {exc}", file=sys.stderr)
        return 2
    total = len(release_verified) + len(integrated_verified)
    for manifest, verified in (
        (release_manifest, release_verified),
        (integrated_manifest, integrated_verified),
    ):
        print(f"verified {manifest.relative_to(root)} ({len(verified)} paths)")
    print(f"verified {total} manifest records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
