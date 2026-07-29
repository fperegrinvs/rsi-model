"""Installed command-line boundary for the integrated artifact pipeline."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from .run_config import (
    DEFAULT_ENSEMBLE_SEED,
    DEFAULT_ENSEMBLE_SIZE,
    IntegratedRunConfig,
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rsi-run-integrated",
        description="Generate the deterministic integrated-model publication artifacts.",
    )
    parser.add_argument("--project-root", type=Path, default=_project_root())
    parser.add_argument(
        "--params",
        type=Path,
        help="integrated YAML parameter file (default: PROJECT_ROOT/params/integrated_model.yaml)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="artifact directory (default: PROJECT_ROOT/outputs/integrated)",
    )
    parser.add_argument("--ensemble-size", type=int, default=DEFAULT_ENSEMBLE_SIZE)
    parser.add_argument("--ensemble-seed", type=int, default=DEFAULT_ENSEMBLE_SEED)
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="validate and print resolved inputs without running the model",
    )
    return parser


def _config(namespace: argparse.Namespace) -> IntegratedRunConfig:
    root = cast(Path, namespace.project_root).resolve()
    defaults = IntegratedRunConfig.default(root)
    return IntegratedRunConfig(
        project_root=root,
        parameters=(cast(Path | None, namespace.params) or defaults.parameters),
        output_directory=(cast(Path | None, namespace.output_dir) or defaults.output_directory),
        ensemble_size=cast(int, namespace.ensemble_size),
        ensemble_seed=cast(int, namespace.ensemble_seed),
    ).validated()


def integrated_main(argv: Sequence[str] | None = None) -> int:
    """Validate explicit inputs and run the integrated artifact pipeline."""
    namespace = _parser().parse_args(argv)
    try:
        config = _config(namespace)
    except ValueError as exc:
        print(f"FAIL integrated configuration: {exc}", file=sys.stderr)
        return 2
    if cast(bool, namespace.check_config):
        print(
            "PASS integrated configuration: "
            f"params={config.parameters}; output={config.output_directory}; "
            f"ensemble={config.ensemble_size}; seed={config.ensemble_seed}"
        )
        return 0

    from .integrated_pipeline import run

    run(config)
    return 0
