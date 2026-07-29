"""Shared read-only collection types for integrated artifact components."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .integrated import (
    CapacityGrowthResult,
    ComputeComparison,
    DebrisResult,
    EnsembleSummary,
    IntegratedParams,
    SeedDeploymentResult,
    SeedResult,
    ShellDebrisResult,
)
from .integrated_analysis import (
    AblationRow,
    AllocationRepairRow,
    CapacityRegimeSummary,
    CertificateRow,
    ClosureAblationRow,
    DiagnosticsSummary,
    EconomicTrajectory,
    ElectronicsArchitectureRow,
    EnvironmentEffectRow,
    FrontierRow,
    ImportStockRow,
    KnowledgeRegimeRow,
    ParetoSeedDesign,
    PolicyRobustnessRow,
    TerminalEndpoints,
)

type SeedResults = Mapping[str, SeedResult]
type CapacityRuns = Mapping[str, CapacityGrowthResult]
type EnsembleResults = Mapping[str, EnsembleSummary]
type ObjectiveSeedResults = Mapping[str, Mapping[str, SeedResult]]
type DeploymentResults = Mapping[str, SeedDeploymentResult]
type DebrisRuns = Sequence[DebrisResult]
type EndpointResults = Mapping[str, TerminalEndpoints]
type ImportStockResults = Mapping[str, Sequence[ImportStockRow]]
type AblationResults = Mapping[str, Sequence[AblationRow]]
type FrontierResults = Mapping[str, Sequence[FrontierRow]]
type DiagnosticsResults = Mapping[str, DiagnosticsSummary]
type CertificateResults = Mapping[str, Sequence[CertificateRow]]
type LimitedStepResults = Mapping[str, tuple[int, int]]
type RegimeResults = Mapping[str, CapacityRegimeSummary]
type AllocationRepairResults = Mapping[str, Sequence[AllocationRepairRow]]
type KnowledgeRegimeResults = Mapping[str, Sequence[KnowledgeRegimeRow]]
type EnvironmentEffectResults = Mapping[str, Sequence[EnvironmentEffectRow]]
type PolicyRobustnessResults = Mapping[str, Sequence[PolicyRobustnessRow]]
type ElectronicsArchitectureResults = Mapping[str, Sequence[ElectronicsArchitectureRow]]
type EconomicResults = Mapping[str, EconomicTrajectory]
type ParetoDesigns = Sequence[ParetoSeedDesign]
type ClosureAblations = Sequence[ClosureAblationRow]

__all__ = [
    "AblationResults",
    "AllocationRepairResults",
    "CapacityRuns",
    "CertificateResults",
    "ClosureAblations",
    "ComputeComparison",
    "DebrisRuns",
    "DeploymentResults",
    "DiagnosticsResults",
    "EconomicResults",
    "ElectronicsArchitectureResults",
    "EndpointResults",
    "EnsembleResults",
    "EnvironmentEffectResults",
    "FrontierResults",
    "ImportStockResults",
    "IntegratedParams",
    "KnowledgeRegimeResults",
    "LimitedStepResults",
    "ObjectiveSeedResults",
    "ParetoDesigns",
    "PolicyRobustnessResults",
    "RegimeResults",
    "SeedResults",
    "ShellDebrisResult",
]
