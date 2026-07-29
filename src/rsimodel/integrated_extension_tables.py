"""Bounded domain dispatch for integrated extension tables."""

from __future__ import annotations

from .integrated_artifacts import ArtifactWorkspace
from .integrated_closure_tables import _write_partial_closure_tables
from .integrated_coordination_tables import _write_coordination_extension_tables
from .integrated_digital_tables import _write_digital_extension_tables
from .integrated_embodiment_tables import _write_embodiment_extension_tables
from .integrated_orbital_tables import _write_orbital_extension_tables
from .integrated_types import (
    CapacityRuns,
    DebrisRuns,
    IntegratedParams,
    SeedResults,
    ShellDebrisResult,
)


def write_extension_tables(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    seeds: SeedResults,
    runs: CapacityRuns,
    debris_runs: DebrisRuns,
    shell_debris: ShellDebrisResult,
) -> None:
    """Write extension diagnostics through bounded domain components."""
    _write_digital_extension_tables(workspace, params)
    _write_coordination_extension_tables(workspace, params)
    _write_embodiment_extension_tables(workspace, params, runs)
    _write_orbital_extension_tables(workspace, params, debris_runs, shell_debris)
    _write_partial_closure_tables(workspace, params, seeds, runs)
