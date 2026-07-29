"""Typed paths and shared constants for integrated artifact generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

import numpy as np

from .run_config import IntegratedRunConfig

SCENARIOS: Final = (
    "terrestrial_rehearsal",
    "lunar_strategic_material_bridge",
    "lunar_strict",
    "moon_asteroid_network",
)
SEED_OBJECTIVES: Final = (
    "installed_mass",
    "earth_import_mass",
    "intervention_hours",
)


@dataclass(frozen=True, slots=True)
class ArtifactWorkspace:
    """Resolved paths and deterministic ensemble controls for one pipeline run."""

    project_root: Path
    output_directory: Path
    figure_directory: Path
    table_directory: Path
    ensemble_size: int
    ensemble_seed: int

    @classmethod
    def from_config(cls, config: IntegratedRunConfig) -> ArtifactWorkspace:
        validated = config.validated()
        return cls(
            project_root=validated.project_root,
            output_directory=validated.output_directory,
            figure_directory=validated.figure_directory,
            table_directory=validated.table_directory,
            ensemble_size=validated.ensemble_size,
            ensemble_seed=validated.ensemble_seed,
        )

    def prepare(self) -> None:
        """Create only the directories owned by this artifact run."""
        self.output_directory.mkdir(parents=True, exist_ok=True)
        self.figure_directory.mkdir(parents=True, exist_ok=True)
        self.table_directory.mkdir(parents=True, exist_ok=True)


def format_number(value: float | None, digits: int = 1) -> str:
    """Render an optional numeric result for the generated report."""
    return "—" if value is None else f"{value:,.{digits}f}"


def format_year(value: float | None, digits: int = 1) -> str:
    """Render an optional year-valued result for the generated report."""
    return "—" if value is None else f"{value:,.{digits}f} yr"


def percentile_summary(values: tuple[float, ...]) -> tuple[float, float, float] | None:
    """Return the 10th, 50th, and 90th percentiles for a non-empty sample."""
    if not values:
        return None
    low, median, high = np.percentile(values, [10, 50, 90])
    return float(low), float(median), float(high)
