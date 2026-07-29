"""Typed paths and parameters for deterministic artifact-generation commands."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

DEFAULT_ENSEMBLE_SIZE: Final = 200
DEFAULT_ENSEMBLE_SEED: Final = 404


@dataclass(frozen=True, slots=True)
class IntegratedRunConfig:
    """All mutable filesystem and ensemble inputs to the integrated pipeline."""

    project_root: Path
    parameters: Path
    output_directory: Path
    ensemble_size: int = DEFAULT_ENSEMBLE_SIZE
    ensemble_seed: int = DEFAULT_ENSEMBLE_SEED

    @classmethod
    def default(cls, project_root: Path) -> IntegratedRunConfig:
        root = project_root.resolve()
        return cls(
            project_root=root,
            parameters=root / "params" / "integrated_model.yaml",
            output_directory=root / "outputs" / "integrated",
        )

    @property
    def figure_directory(self) -> Path:
        return self.output_directory / "figures"

    @property
    def table_directory(self) -> Path:
        return self.output_directory / "tables"

    def validated(self) -> IntegratedRunConfig:
        """Return a normalized configuration or raise before any output is written."""
        root = self.project_root.resolve()
        parameters = self.parameters.resolve()
        output = self.output_directory.resolve()
        if not root.is_dir():
            raise ValueError(f"project root is not a directory: {root}")
        if not parameters.is_file():
            raise ValueError(f"integrated parameter file is missing: {parameters}")
        if self.ensemble_size <= 0:
            raise ValueError("ensemble size must be positive")
        return IntegratedRunConfig(
            project_root=root,
            parameters=parameters,
            output_directory=output,
            ensemble_size=self.ensemble_size,
            ensemble_seed=self.ensemble_seed,
        )
