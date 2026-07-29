"""Build and exercise distributions outside the source checkout."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Final

EXPECTED_DISTRIBUTIONS: Final = ("rsi_model-*.tar.gz", "rsi_model-*.whl")
CONSOLE_COMMANDS: Final = (
    "rsi-check-coverage",
    "rsi-check-dependencies",
    "rsi-check-external-links",
    "rsi-check-math-font",
    "rsi-check-notation",
    "rsi-check-package",
    "rsi-check-prose",
    "rsi-evaluate-evidence",
    "rsi-publication-preflight",
    "rsi-release-preflight",
    "rsi-run-baseline",
    "rsi-run-deep",
    "rsi-run-integrated",
    "rsi-run-part2",
    "rsi-verify-manifests",
    "rsi-write-manifest",
    "rsi-write-provenance",
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rsi-check-package",
        description="Build the sdist/wheel and smoke-test the wheel in an isolated uv environment.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="repository root containing pyproject.toml (default: current directory)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("dist"),
        help="distribution output directory, relative to project root by default",
    )
    return parser


def _run(command: Sequence[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    return subprocess.run(  # noqa: S603 -- explicit argv and resolved, pinned uv executable.
        command,
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def _require_success(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{label} failed: {detail}")


def package_main(argv: Sequence[str] | None = None) -> int:
    """Build both distributions and verify imports/entry points from a temporary directory."""
    args = _parser().parse_args(argv)
    root = args.project_root.resolve()
    out_dir = args.out_dir
    if not out_dir.is_absolute():
        out_dir = root / out_dir
    if not (root / "pyproject.toml").is_file() or not (root / "uv.lock").is_file():
        print(f"FAIL package gate: not a locked Python project: {root}", file=sys.stderr)
        return 2
    uv = shutil.which("uv")
    if uv is None:
        print("FAIL package gate: uv is unavailable", file=sys.stderr)
        return 2

    try:
        with tempfile.TemporaryDirectory(prefix="rsi-package-") as temporary_name:
            temporary = Path(temporary_name)
            build = _run([uv, "build", "--out-dir", str(out_dir), str(root)], cwd=temporary)
            _require_success(build, "uv build")
            distributions: list[Path] = []
            for pattern in EXPECTED_DISTRIBUTIONS:
                matches = sorted(out_dir.glob(pattern))
                if len(matches) != 1:
                    raise RuntimeError(f"expected one {pattern} distribution; found {len(matches)}")
                distributions.append(matches[0])
            wheel = next(path for path in distributions if path.suffix == ".whl")
            isolated_prefix = [
                uv,
                "run",
                "--isolated",
                "--no-project",
                "--with",
                str(wheel),
            ]
            _require_success(
                _run(
                    [
                        *isolated_prefix,
                        "python",
                        "-c",
                        (
                            "import pathlib, rsimodel; "
                            "assert not pathlib.Path(rsimodel.__file__).resolve()"
                            f".is_relative_to(pathlib.Path({str(root)!r}))"
                        ),
                    ],
                    cwd=temporary,
                ),
                "isolated import",
            )
            for command in CONSOLE_COMMANDS:
                _require_success(
                    _run([*isolated_prefix, command, "--help"], cwd=temporary),
                    f"{command} help",
                )
    except (OSError, RuntimeError, StopIteration) as exc:
        print(f"FAIL package gate: {exc}", file=sys.stderr)
        return 1

    print(
        "PASS package gate: sdist, wheel, isolated import, and "
        f"{len(CONSOLE_COMMANDS)} console entry points"
    )
    return 0
