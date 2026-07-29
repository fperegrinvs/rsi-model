"""Typed command-line entry points for repository maintenance."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tomllib
from collections.abc import Sequence
from importlib import import_module
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Final, cast

EXPECTED_PYTHON: Final = (3, 13)
EXPECTED_UV: Final = "0.9.18"
REQUIRED_DISTRIBUTIONS: Final[dict[str, str]] = {
    "matplotlib": "matplotlib",
    "numpy": "numpy",
    "osqp": "osqp",
    "pyyaml": "yaml",
    "scipy": "scipy",
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rsi-check-dependencies",
        description=(
            "Validate project metadata, the checked uv lock, and the active Python environment."
        ),
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="repository root containing pyproject.toml and uv.lock (default: current directory)",
    )
    return parser


def _load_project(root: Path) -> dict[str, object]:
    metadata_path = root / "pyproject.toml"
    if not metadata_path.is_file():
        raise ValueError(f"project metadata not found: {metadata_path}")
    with metadata_path.open("rb") as stream:
        document = tomllib.load(stream)
    project = document.get("project")
    if not isinstance(project, dict):
        raise ValueError(f"{metadata_path} has no [project] table")
    return cast(dict[str, object], project)


def _uv_executable() -> str:
    executable = shutil.which("uv")
    if executable is None:
        raise ValueError("uv is unavailable; install the project-pinned uv release")
    return executable


def _uv_version() -> str:
    result = subprocess.run(  # noqa: S603 -- resolved local executable, fixed arguments.
        [_uv_executable(), "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ValueError("uv failed while reporting its version")
    fields = result.stdout.strip().split()
    if len(fields) < 2:
        raise ValueError(f"unexpected uv version output: {result.stdout.strip()!r}")
    return fields[1]


def _check_lock(root: Path) -> None:
    lock_path = root / "uv.lock"
    if not lock_path.is_file():
        raise ValueError(f"checked lock not found: {lock_path}")
    result = subprocess.run(  # noqa: S603 -- fixed command; root is one non-shell argument.
        [_uv_executable(), "lock", "--check", "--project", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"uv.lock is stale or invalid: {detail}")


def _installed_versions() -> list[str]:
    installed: list[str] = []
    missing: list[str] = []
    for distribution, module in REQUIRED_DISTRIBUTIONS.items():
        try:
            import_module(module)
            installed.append(f"{distribution}=={version(distribution)}")
        except (ImportError, ModuleNotFoundError, PackageNotFoundError):
            missing.append(distribution)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(
            f"active environment is missing locked dependencies: {names}; "
            "run `uv sync --locked --all-groups`"
        )
    return installed


def check_dependencies_main(argv: Sequence[str] | None = None) -> int:
    """Validate the locked project and return a process exit code."""
    args = _parser().parse_args(argv)
    root = args.project_root.resolve()
    failures: list[str] = []

    try:
        project = _load_project(root)
        if project.get("name") != "rsi-model":
            failures.append("pyproject.toml [project].name must be 'rsi-model'")
        if project.get("requires-python") != ">=3.13,<3.14":
            failures.append("pyproject.toml must declare requires-python = '>=3.13,<3.14'")
    except ValueError as exc:
        failures.append(str(exc))

    if sys.version_info[:2] != EXPECTED_PYTHON:
        actual = ".".join(str(part) for part in sys.version_info[:2])
        failures.append(f"Python 3.13 is required; active interpreter is {actual}")
    if sys.prefix == sys.base_prefix:
        failures.append(
            "the project is not running in a managed environment; "
            "use `uv run --locked rsi-check-dependencies`"
        )

    try:
        actual_uv = _uv_version()
        if actual_uv != EXPECTED_UV:
            failures.append(f"uv {EXPECTED_UV} is required; found {actual_uv}")
    except ValueError as exc:
        failures.append(str(exc))

    try:
        _check_lock(root)
    except ValueError as exc:
        failures.append(str(exc))

    try:
        installed = _installed_versions()
    except ValueError as exc:
        failures.append(str(exc))
        installed = []

    if failures:
        for failure in failures:
            print(f"FAIL dependency check: {failure}", file=sys.stderr)
        return 1

    print(
        "PASS dependencies: "
        f"Python {sys.version_info.major}.{sys.version_info.minor}, "
        f"uv {EXPECTED_UV}, " + ", ".join(installed)
    )
    return 0
