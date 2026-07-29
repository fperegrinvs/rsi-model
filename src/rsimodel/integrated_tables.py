"""Generated-artifact component for the integrated pipeline."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from pathlib import Path

import numpy as np

from rsimodel.extension_config import (
    BottleneckUpgradeConfig,
    ComputeDemandConfig,
    IntelligenceMarginalResponseConfig,
)
from rsimodel.governance import load_governance_controls
from rsimodel.integrated import (
    simulate_capacity_growth,
)
from rsimodel.integrated_analysis import (
    BottleneckUpgradeResult,
    ComputeDemandAllocationResult,
    IntelligenceMarginalResponseRow,
)

from .integrated_artifacts import (
    SCENARIOS,
    SEED_OBJECTIVES,
    ArtifactWorkspace,
)
from .integrated_artifacts import (
    percentile_summary as pct,
)
from .integrated_types import (
    AblationResults,
    AllocationRepairResults,
    CapacityRuns,
    CertificateResults,
    ClosureAblations,
    ComputeComparison,
    DebrisRuns,
    DeploymentResults,
    DiagnosticsResults,
    EconomicResults,
    ElectronicsArchitectureResults,
    EndpointResults,
    EnsembleResults,
    EnvironmentEffectResults,
    FrontierResults,
    ImportStockResults,
    IntegratedParams,
    KnowledgeRegimeResults,
    ObjectiveSeedResults,
    ParetoDesigns,
    PolicyRobustnessResults,
    RegimeResults,
    SeedResults,
    ShellDebrisResult,
)


def write_scenario_tables(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    seeds: SeedResults,
    runs: CapacityRuns,
    ensembles: EnsembleResults,
) -> None:
    with open(
        workspace.table_directory / "scenario_summary.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "feasible",
                "status",
                "seed_mass_t",
                "physical_seed_mass_t",
                "import_stock_mass_t",
                "digital_seed_mass_t",
                "lunar_feed_t_per_year",
                "asteroid_feed_t_per_year",
                "minimum_task_coverage",
                "intervention_hours_per_year",
                "aggregate_doubling_year",
                "operating_cells_year40",
                "intelligence_year40",
                "survived",
            ]
        )
        for name in SCENARIOS:
            s = seeds[name]
            r = runs.get(name)
            w.writerow(
                [
                    name,
                    int(s.feasible),
                    s.status,
                    "" if s.total_seed_mass_t is None else f"{s.total_seed_mass_t:.8f}",
                    "" if s.physical_seed_mass_t is None else f"{s.physical_seed_mass_t:.8f}",
                    "" if s.import_stock_mass_t is None else f"{s.import_stock_mass_t:.8f}",
                    f"{s.digital_seed_mass_t:.8f}",
                    f"{s.lunar_feed_t_per_year:.8f}",
                    f"{s.asteroid_feed_t_per_year:.8f}",
                    f"{s.minimum_task_coverage:.8f}",
                    f"{s.intervention_hours_per_year:.8f}",
                    ""
                    if r is None or r.aggregate_doubling_year is None
                    else f"{r.aggregate_doubling_year:.8f}",
                    "" if r is None else f"{r.operating_cells[-1]:.8f}",
                    "" if r is None else f"{r.intelligence[-1]:.8f}",
                    "" if r is None else int(r.survived),
                ]
            )

    with open(
        workspace.table_directory / "seed_sector_capacity.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "sector",
                "capacity",
                "embedded_mass_t",
                "centrifuge_mass_t",
                "task_coverage",
            ]
        )
        for name in SCENARIOS:
            s = seeds[name]
            for j, sector in enumerate(params.sectors):
                w.writerow(
                    [
                        name,
                        sector,
                        f"{s.capacities[j]:.9f}",
                        f"{s.process.B_effective[:, j].sum() * s.capacities[j]:.9f}",
                        f"{s.process.centrifuge_mass_t[j] * s.capacities[j]:.9f}",
                        f"{s.process.coverage[j]:.9f}",
                    ]
                )

    with open(
        workspace.table_directory / "sector_capacity_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "year",
                "sector",
                "installed_capacity",
                "operating_capacity",
                "ordered_capacity",
                "normalized_installed_cell_equivalents",
                "normalized_operating_cell_equivalents",
            ]
        )
        for name, run in runs.items():
            z = seeds[name].capacities
            for k, year in enumerate(run.t):
                for j, sector in enumerate(params.sectors):
                    w.writerow(
                        [
                            name,
                            f"{year:.6f}",
                            sector,
                            f"{run.installed_sector_capacity[k, j]:.9f}",
                            f"{run.operating_sector_capacity[k, j]:.9f}",
                            f"{run.ordered_sector_capacity[k, j]:.9f}",
                            f"{run.installed_sector_capacity[k, j] / z[j]:.9f}",
                            f"{run.operating_sector_capacity[k, j] / z[j]:.9f}",
                        ]
                    )

    with open(
        workspace.table_directory / "element_flows.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "element",
                "cell_bom_t",
                "initial_earth_stock_t",
                "lunar_output_t_per_cell_year",
                "asteroid_output_t_per_cell_year",
            ]
        )
        for name in SCENARIOS:
            s = seeds[name]
            for e, element in enumerate(params.elements):
                cell_bom = float(s.process.B_effective[e] @ s.capacities)
                w.writerow(
                    [
                        name,
                        element,
                        f"{cell_bom:.9f}",
                        f"{s.import_stock_t[e]:.9f}",
                        f"{params.lunar_yield[e] * s.lunar_feed_t_per_year:.9f}",
                        f"{params.asteroid_yield[e] * s.asteroid_feed_t_per_year:.9f}",
                    ]
                )

    with open(
        workspace.table_directory / "ensemble_summary.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "n_runs",
                "n_feasible",
                "feasible_share",
                "n_survived",
                "survived_share",
                "seed_p10_t",
                "seed_p50_t",
                "seed_p90_t",
                "aggregate_doubling_p10_year",
                "aggregate_doubling_p50_year",
                "aggregate_doubling_p90_year",
            ]
        )
        for name in SCENARIOS:
            e = ensembles[name]
            sm, sy = pct(e.seed_masses_t), pct(e.aggregate_doubling_years)
            w.writerow(
                [
                    name,
                    e.n_runs,
                    e.n_feasible,
                    f"{e.feasible_share:.6f}",
                    e.n_survived,
                    f"{e.survived_share:.6f}",
                    *(["", "", ""] if sm is None else [f"{v:.6f}" for v in sm]),
                    *(["", "", ""] if sy is None else [f"{v:.6f}" for v in sy]),
                ]
            )


def write_compute_and_debris_tables(
    workspace: ArtifactWorkspace,
    compute: ComputeComparison,
    debris_runs: DebrisRuns,
) -> None:
    with open(
        workspace.table_directory / "compute_curves.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "year",
                "endogenous_total",
                "endogenous_orbit",
                "earth_tight",
                "earth_base",
                "earth_responsive",
                "earth_fed_orbit_tight",
                "earth_fed_orbit_base",
                "earth_fed_orbit_responsive",
            ]
        )
        for k, year in enumerate(compute.t):
            w.writerow(
                [
                    f"{year:.6f}",
                    f"{compute.endogenous[k]:.9f}",
                    f"{compute.endogenous_orbit[k]:.9f}",
                    f"{compute.terrestrial['tight'][k]:.9f}",
                    f"{compute.terrestrial['base'][k]:.9f}",
                    f"{compute.terrestrial['responsive'][k]:.9f}",
                    f"{compute.earth_fed_orbit['tight'][k]:.9f}",
                    f"{compute.earth_fed_orbit['base'][k]:.9f}",
                    f"{compute.earth_fed_orbit['responsive'][k]:.9f}",
                ]
            )

    with open(
        workspace.table_directory / "debris_summary.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "case",
                "creation_clearance_ratio_last5y",
                "subcritical",
                "active_year40",
                "derelict_year40",
                "fragment_index_year40",
            ]
        )
        for d in debris_runs:
            w.writerow(
                [
                    d.label,
                    f"{d.creation_clearance_ratio:.9f}",
                    int(d.subcritical),
                    f"{d.active[-1]:.9f}",
                    f"{d.derelict[-1]:.9f}",
                    f"{d.fragments[-1]:.9f}",
                ]
            )


def write_shell_debris_tables(
    workspace: ArtifactWorkspace,
    shell_debris: ShellDebrisResult,
) -> None:
    with open(
        workspace.table_directory / "orbital_mass_balance.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "year",
                "uncaptured_reservoir_t",
                "feed_inventory_t",
                "accessible_orbital_mass_t",
                "earth_imported_t",
                "captured_t",
                "recovered_t",
                "unrecoverable_loss_t",
                "requested_deployment_units",
                "served_deployment_units",
                "deployment_shortfall_units",
            ]
        )
        for k, year in enumerate(shell_debris.t):
            w.writerow(
                [
                    f"{year:.6f}",
                    f"{shell_debris.uncaptured_reservoir_t[k]:.6f}",
                    f"{shell_debris.feed_inventory_t[k]:.6f}",
                    f"{shell_debris.accessible_orbital_mass_t[k]:.6f}",
                    f"{shell_debris.earth_imported_t[k]:.6f}",
                    f"{shell_debris.captured_t[k]:.6f}",
                    f"{shell_debris.recovered_t[k]:.6f}",
                    f"{shell_debris.unrecoverable_loss_t[k]:.6f}",
                    f"{shell_debris.requested_deployment_units[k]:.6f}",
                    f"{shell_debris.served_deployment_units[k]:.6f}",
                    f"{shell_debris.deployment_shortfall_units[k]:.6f}",
                ]
            )

    with open(
        workspace.table_directory / "shell_debris_trajectory.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "year",
                "shell",
                "active_capacity",
                "intact_derelicts",
                "trackable_fragments",
                "untrackable_fragments",
                "terminal_branching_ratio",
            ]
        )
        for k, year in enumerate(shell_debris.t):
            for s, shell in enumerate(shell_debris.shells):
                w.writerow(
                    [
                        f"{year:.6f}",
                        shell,
                        f"{shell_debris.active_capacity[k, s]:.6f}",
                        f"{shell_debris.intact_derelicts[k, s]:.6f}",
                        f"{shell_debris.trackable_fragments[k, s]:.6f}",
                        f"{shell_debris.untrackable_fragments[k, s]:.6f}",
                        f"{shell_debris.branching_ratio_by_shell[s]:.6f}",
                    ]
                )


def write_governance_traceability(
    workspace: ArtifactWorkspace,
) -> Path:
    source = workspace.project_root / "params" / "governance_controls.yaml"
    governance = load_governance_controls(source)
    target = workspace.table_directory / "governance_threat_control_traceability.csv"
    with open(target, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "threat",
                "class",
                "affected_assets",
                "physical_state_trigger",
                "control",
                "control_action",
                "verification",
                "rollback",
                "control_status",
                "residual_risk",
            ]
        )
        for threat, threat_cfg in governance["threats"].items():
            for control in threat_cfg["controls"]:
                control_cfg = governance["controls"][control]
                w.writerow(
                    [
                        threat,
                        threat_cfg["class_"],
                        "; ".join(threat_cfg["affected_assets"]),
                        threat_cfg["physical_state_trigger"],
                        control,
                        control_cfg["action"],
                        control_cfg["verification"],
                        control_cfg["rollback"],
                        control_cfg["status"],
                        threat_cfg["residual_risk"],
                    ]
                )
    return target


def write_long_horizon_table(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    seeds: SeedResults,
    extended_runs: CapacityRuns,
) -> None:
    with open(
        workspace.table_directory / "long_horizon_endpoints.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "year",
                "aggregate_operating_cell_equivalents",
                "net_capacity_change_prior5y",
                "bottleneck_sector",
                "bottleneck_sector_equivalents",
                "aggregate_doubling_year",
            ]
        )
        for name, run in extended_runs.items():
            z = seeds[name].capacities
            for year in (40.0, 60.0, 80.0):
                k = int(np.searchsorted(run.t, year))
                ratios = run.operating_sector_capacity[k] / z
                bottleneck = int(np.argmin(ratios))
                k0 = int(np.searchsorted(run.t, year - 5.0))
                net = float(run.operating_cells[k] - run.operating_cells[k0])
                w.writerow(
                    [
                        name,
                        f"{year:.1f}",
                        f"{run.operating_cells[k]:.9f}",
                        f"{net:.9f}",
                        params.sectors[bottleneck],
                        f"{ratios[bottleneck]:.9f}",
                        ""
                        if run.aggregate_doubling_year is None
                        else f"{run.aggregate_doubling_year:.6f}",
                    ]
                )


def write_seed_objective_table(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    objective_seeds: ObjectiveSeedResults,
) -> None:
    with open(
        workspace.table_directory / "seed_objective_comparison.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "objective",
                "feasible",
                "installed_seed_mass_t",
                "earth_import_mass_t",
                "intervention_hours_per_year",
                "capacity_l1_distance_from_mass_optimum",
                "sector_balanced_equivalents_year40",
                "aggregate_doubling_year_80y_extension",
            ]
        )
        for name, by_objective in objective_seeds.items():
            baseline = by_objective["installed_mass"]
            for objective in SEED_OBJECTIVES:
                seed = by_objective[objective]
                if not seed.feasible:
                    w.writerow([name, objective, 0, "", "", "", "", "", ""])
                    continue
                run40 = simulate_capacity_growth(params, seed, years=40.0, dt=0.25)
                run80 = simulate_capacity_growth(params, seed, years=80.0, dt=0.25)
                distance = float(np.abs(seed.capacities - baseline.capacities).sum())
                w.writerow(
                    [
                        name,
                        objective,
                        1,
                        f"{seed.total_seed_mass_t:.9f}",
                        f"{seed.import_stock_mass_t:.9f}",
                        f"{seed.intervention_hours_per_year:.9f}",
                        f"{distance:.9f}",
                        f"{run40.operating_cells[-1]:.9f}",
                        ""
                        if run80.aggregate_doubling_year is None
                        else f"{run80.aggregate_doubling_year:.6f}",
                    ]
                )


def write_deployment_table(
    workspace: ArtifactWorkspace,
    deployments: DeploymentResults,
) -> None:
    with open(
        workspace.table_directory / "seed_deployment_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "year",
                "delivered_core_t",
                "staged_core_t",
                "installed_uncommissioned_core_t",
                "commissioned_core_t",
                "operating_core_t",
                "recovery_backlog_t",
                "spares_remaining_t",
                "installed_seed_mass_t",
                "delivered_seed_mass_t",
                "startup_energy_mwh",
                "full_operating_seed_year",
                "success",
            ]
        )
        for name, d in deployments.items():
            for k, year in enumerate(d.t):
                w.writerow(
                    [
                        name,
                        f"{year:.6f}",
                        f"{d.delivered_core_t[k]:.6f}",
                        f"{d.staged_core_t[k]:.6f}",
                        f"{d.installed_core_t[k]:.6f}",
                        f"{d.commissioned_core_t[k]:.6f}",
                        f"{d.operating_core_t[k]:.6f}",
                        f"{d.recovery_backlog_t[k]:.6f}",
                        f"{d.spares_remaining_t[k]:.6f}",
                        f"{d.installed_seed_mass_t:.6f}",
                        f"{d.delivered_seed_mass_t:.6f}",
                        f"{d.startup_energy_mwh:.6f}",
                        ""
                        if d.full_operating_seed_year is None
                        else f"{d.full_operating_seed_year:.6f}",
                        int(d.success),
                    ]
                )


def write_closure_ablation_table(
    workspace: ArtifactWorkspace,
    rows: ClosureAblations,
) -> None:
    with open(
        workspace.table_directory / "closure_loop_ablation_matrix.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "verified_ai_rd_loop",
                "reproductive_capital_loop",
                "conceptual_regime",
                "aggregate_doubling_year",
                "operating_at_horizon",
                "intelligence_at_horizon",
                "physical_doubling_occurs",
                "source_class",
                "boundary",
            ]
        )
        for row in rows:
            w.writerow(
                [
                    int(row.verified_ai_rd_loop),
                    int(row.reproductive_capital_loop),
                    row.conceptual_regime,
                    (
                        ""
                        if row.aggregate_doubling_year is None
                        else f"{row.aggregate_doubling_year:.6f}"
                    ),
                    f"{row.operating_at_horizon:.9f}",
                    f"{row.intelligence_at_horizon:.9f}",
                    int(row.physical_doubling_occurs),
                    "ASSUMPTION",
                    (
                        "AI-R&D loop is the implemented verified capability-growth "
                        "proxy; capital closure is isolated by permitting or "
                        "blocking every new-capacity order"
                    ),
                ]
            )


def write_intelligence_response_tables(
    workspace: ArtifactWorkspace,
    response_rows: Sequence[IntelligenceMarginalResponseRow],
    upgrade_rows: Sequence[BottleneckUpgradeResult],
    response_cfg: IntelligenceMarginalResponseConfig,
    upgrade_cfg: BottleneckUpgradeConfig,
) -> None:
    with open(
        workspace.table_directory / "intelligence_marginal_response.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "regime",
                "scenario",
                "intelligence_uplift",
                "baseline_operating_capacity_at_horizon",
                "uplifted_operating_capacity_at_horizon",
                "marginal_operating_capacity_per_intelligence_unit",
                "baseline_doubling_year",
                "uplifted_doubling_year",
                "doubling_year_acceleration_per_intelligence_unit",
                "dominant_constraint",
                "material_constraint_share",
                "leading_limiting_material",
                "response_class",
                "complementary_stock_boundary",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in response_rows:
            w.writerow(
                [
                    row.regime,
                    row.scenario,
                    f"{row.intelligence_uplift:.6f}",
                    f"{row.baseline_operating_capacity:.9f}",
                    f"{row.uplifted_operating_capacity:.9f}",
                    (f"{row.marginal_operating_capacity_per_intelligence_unit:.9f}"),
                    (
                        ""
                        if row.baseline_doubling_year is None
                        else f"{row.baseline_doubling_year:.6f}"
                    ),
                    (
                        ""
                        if row.uplifted_doubling_year is None
                        else f"{row.uplifted_doubling_year:.6f}"
                    ),
                    (
                        ""
                        if row.doubling_year_acceleration_per_intelligence_unit is None
                        else (f"{row.doubling_year_acceleration_per_intelligence_unit:.9f}")
                    ),
                    row.dominant_constraint,
                    f"{row.material_constraint_share:.9f}",
                    row.leading_limiting_material or "",
                    row.response_class,
                    row.complementary_stock_boundary,
                    response_cfg["evidence_status"],
                    response_cfg["source_class"],
                    response_cfg["boundary"].strip(),
                ]
            )

    with open(
        workspace.table_directory / "bottleneck_upgrade_projects.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "project",
                "constraint",
                "constraint_class",
                "intelligence_can_reduce",
                "cost_capacity_years",
                "available_budget_capacity_years",
                "design_lag_years",
                "construction_lag_years",
                "verification_lag_years",
                "commission_year",
                "initial_capacity",
                "capacity_increment",
                "capacity_at_horizon",
                "productive_capacity_available",
                "verified_causal_path",
                "productive_sector",
                "causal_path",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in upgrade_rows:
            w.writerow(
                [
                    row.project,
                    row.constraint,
                    row.constraint_class,
                    int(row.intelligence_can_reduce),
                    f"{row.cost_capacity_years:.6f}",
                    f"{row.available_budget_capacity_years:.6f}",
                    f"{row.design_lag_years:.6f}",
                    f"{row.construction_lag_years:.6f}",
                    f"{row.verification_lag_years:.6f}",
                    ("" if row.commission_year is None else f"{row.commission_year:.6f}"),
                    f"{row.initial_capacity:.9f}",
                    f"{row.capacity_increment:.9f}",
                    f"{row.capacity_at_horizon:.9f}",
                    int(row.productive_capacity_available),
                    int(row.verified_causal_path),
                    row.productive_sector,
                    row.causal_path,
                    upgrade_cfg["evidence_status"],
                    upgrade_cfg["source_class"],
                    upgrade_cfg["boundary"].strip(),
                ]
            )

    with open(
        workspace.table_directory / "bottleneck_upgrade_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "project",
                "year",
                "available_bottleneck_capacity",
                "commissioned",
                "source_class",
            ]
        )
        for row in upgrade_rows:
            for k, year in enumerate(row.t):
                w.writerow(
                    [
                        row.project,
                        f"{year:.6f}",
                        f"{row.capacity[k]:.9f}",
                        int(
                            row.commission_year is not None and year + 1e-12 >= row.commission_year
                        ),
                        upgrade_cfg["source_class"],
                    ]
                )


def write_compute_demand_tables(
    workspace: ArtifactWorkspace,
    rows: Sequence[ComputeDemandAllocationResult],
    config: ComputeDemandConfig,
) -> None:
    with open(
        workspace.table_directory / "compute_demand_allocation_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "branch",
                "demand_type",
                "year",
                "available_compute",
                "valuable_demand",
                "used_compute",
                "unmet_demand",
                "humanitarian_compute",
                "science_public_goods_compute",
                "industrial_expansion_compute",
                "relocated_harmful_activity",
                "expanded_activity_above_initial",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in rows:
            for k, year in enumerate(row.t):
                w.writerow(
                    [
                        row.branch,
                        row.demand_type,
                        f"{year:.6f}",
                        f"{row.available_compute[k]:.9f}",
                        f"{row.valuable_demand[k]:.9f}",
                        f"{row.used_compute[k]:.9f}",
                        f"{row.unmet_demand[k]:.9f}",
                        f"{row.humanitarian_compute[k]:.9f}",
                        f"{row.science_public_goods_compute[k]:.9f}",
                        f"{row.industrial_expansion_compute[k]:.9f}",
                        f"{row.relocated_harmful_activity[k]:.9f}",
                        f"{row.expanded_activity_above_initial[k]:.9f}",
                        config["evidence_status"],
                        config["source_class"],
                        config["boundary"].strip(),
                    ]
                )
    with open(
        workspace.table_directory / "compute_demand_allocation_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "branch",
                "demand_type",
                "compute_capacity_at_horizon",
                "valuable_demand_at_horizon",
                "used_compute_at_horizon",
                "unmet_demand_at_horizon",
                "cumulative_humanitarian_compute",
                "cumulative_science_public_goods_compute",
                "cumulative_industrial_expansion_compute",
                "cumulative_relocated_harmful_activity",
                "cumulative_expanded_activity_above_initial",
                "humanitarian_share_before_priority_switch",
                "evidence_status",
                "source_class",
                "boundary",
            ]
        )
        for row in rows:
            early = row.t < float(config["branches"][row.branch]["priority_switch_year"])
            early_total = float(row.used_compute[early].sum())
            early_humanitarian_share = (
                float(row.humanitarian_compute[early].sum()) / early_total
                if early_total > 0.0
                else 0.0
            )
            w.writerow(
                [
                    row.branch,
                    row.demand_type,
                    f"{row.available_compute[-1]:.9f}",
                    f"{row.valuable_demand[-1]:.9f}",
                    f"{row.used_compute[-1]:.9f}",
                    f"{row.unmet_demand[-1]:.9f}",
                    f"{row.humanitarian_compute.sum():.9f}",
                    f"{row.science_public_goods_compute.sum():.9f}",
                    f"{row.industrial_expansion_compute.sum():.9f}",
                    f"{row.relocated_harmful_activity.sum():.9f}",
                    f"{row.expanded_activity_above_initial.sum():.9f}",
                    f"{early_humanitarian_share:.9f}",
                    config["evidence_status"],
                    config["source_class"],
                    config["boundary"].strip(),
                ]
            )


def write_analysis_tables(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    seeds: SeedResults,
    endpoints: EndpointResults,
    import_stocks: ImportStockResults,
    ablations: AblationResults,
    frontiers: FrontierResults,
    allocation_repair: AllocationRepairResults,
    knowledge_regimes: KnowledgeRegimeResults,
    environment_effects: EnvironmentEffectResults,
    policy_robustness: PolicyRobustnessResults,
    electronics_architectures: ElectronicsArchitectureResults,
    economics: EconomicResults,
    pareto_designs: ParetoDesigns,
    regimes: RegimeResults,
    diags: DiagnosticsResults,
    certs: CertificateResults,
) -> None:
    with open(
        workspace.table_directory / "terminal_endpoints.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "aggregate_doubling_year",
                "operating_at_horizon",
                "retained_at_horizon",
                "net_capacity_change_final5y",
                "terminal_window_expanding",
                "import_pools_exhausted_year",
                "ensemble_n_feasible",
                "ensemble_n_retained",
                "ensemble_n_terminal_window_expanding",
            ]
        )
        for name, d in diags.items():
            e = endpoints.get(name)
            w.writerow(
                [
                    name,
                    ""
                    if e is None or e.aggregate_doubling_year is None
                    else f"{e.aggregate_doubling_year:.6f}",
                    "" if e is None else f"{e.operating_at_horizon:.6f}",
                    "" if e is None else int(e.retained_at_horizon),
                    "" if e is None else f"{e.net_capacity_change_final5:.6f}",
                    "" if e is None else int(e.terminal_window_expanding),
                    ""
                    if e is None or e.import_pools_exhausted_year is None
                    else f"{e.import_pools_exhausted_year:.6f}",
                    d.n_feasible,
                    d.n_retained,
                    d.n_terminal_window_expanding,
                ]
            )

    with open(
        workspace.table_directory / "import_stock_composition.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "element",
                "initial_stock_t",
                "share_of_import_stock",
                "initial_rate_coverage_years",
                "pool_min_t",
                "pool_at_aggregate_doubling_t",
                "pool_at_horizon_t",
                "pool_first_exhaustion_year",
            ]
        )
        for name, rows in import_stocks.items():
            for r in rows:
                w.writerow(
                    [
                        name,
                        r.element,
                        f"{r.initial_stock_t:.6f}",
                        f"{r.share_of_import_stock:.6f}",
                        ""
                        if r.initial_rate_coverage_years is None
                        else f"{r.initial_rate_coverage_years:.4f}",
                        f"{r.pool_min_t:.6f}",
                        ""
                        if r.pool_at_aggregate_doubling_t is None
                        else f"{r.pool_at_aggregate_doubling_t:.6f}",
                        f"{r.pool_at_horizon_t:.6f}",
                        "" if r.pool_exhaustion_year is None else f"{r.pool_exhaustion_year:.4f}",
                    ]
                )

    with open(workspace.table_directory / "ablations.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "variant",
                "definition",
                "feasible",
                "aggregate_doubling_year",
                "operating_at_horizon",
                "growth_share_of_baseline",
            ]
        )
        for name, rows in ablations.items():
            for a in rows:
                w.writerow(
                    [
                        name,
                        a.variant,
                        a.definition,
                        int(a.feasible),
                        ""
                        if a.aggregate_doubling_year is None
                        else f"{a.aggregate_doubling_year:.6f}",
                        "" if a.operating_at_horizon is None else f"{a.operating_at_horizon:.6f}",
                        ""
                        if a.growth_share_of_baseline is None
                        else f"{a.growth_share_of_baseline:.6f}",
                    ]
                )

    with open(
        workspace.table_directory / "oversize_frontier.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "oversize_factor",
                "installed_mass_t",
                "time_to_one_additional_cell_year",
                "additional_cells_at_horizon",
                "retained_plus_one_at_horizon",
            ]
        )
        for name, rows in frontiers.items():
            for r in rows:
                w.writerow(
                    [
                        name,
                        f"{r.oversize_factor:.2f}",
                        f"{r.installed_mass_t:.6f}",
                        ""
                        if r.time_to_one_additional_cell is None
                        else f"{r.time_to_one_additional_cell:.6f}",
                        f"{r.additional_cells_at_horizon:.6f}",
                        int(r.retained_plus_one_at_horizon),
                    ]
                )

    with open(
        workspace.table_directory / "ensemble_sensitivity.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "multiplier",
                "rho_seed_mass",
                "rho_aggregate_doubling_year",
                "rho_operating_at_horizon",
            ]
        )
        for name, d in diags.items():
            if d.n_feasible < 8:
                continue
            for mult, s in d.sensitivity.items():
                w.writerow(
                    [
                        name,
                        mult,
                        f"{s['seed_mass_t']:.4f}",
                        f"{s['aggregate_doubling_year']:.4f}",
                        f"{s['operating_at_horizon']:.4f}",
                    ]
                )

    with open(
        workspace.table_directory / "diagnostics_histograms.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["scenario", "kind", "key", "count"])
        for name, d in diags.items():
            for key, count in sorted(d.failure_histogram.items(), key=lambda kv: -kv[1]):
                w.writerow([name, "failure_reason", key, count])
            for key, count in sorted(d.binding_histogram.items(), key=lambda kv: -kv[1]):
                w.writerow([name, "top_binding_constraint", key, count])

    with open(
        workspace.table_directory / "dynamic_regime_summary.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "total_steps",
                "material_limited_steps",
                "service_limited_steps",
                "order_rate_limited_steps",
                "autonomy_limited_steps",
                "verification_limited_steps",
                "repair_limited_steps",
                "compute_limited_steps",
            ]
        )
        for name, r in regimes.items():
            w.writerow(
                [
                    name,
                    r.total_steps,
                    r.material_limited,
                    r.service_limited,
                    r.order_rate_limited,
                    r.autonomy_limited,
                    r.verification_limited,
                    r.repair_limited,
                    r.compute_limited,
                ]
            )

    with open(
        workspace.table_directory / "allocation_repair_comparison.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "allocation_policy",
                "repair_enabled",
                "shock",
                "aggregate_doubling_year",
                "operating_at_horizon",
                "minimum_sector_margin_at_horizon",
                "survived",
                "shock_recovery_year",
                "cumulative_repaired_capacity",
            ]
        )
        for name, rows in allocation_repair.items():
            for r in rows:
                w.writerow(
                    [
                        name,
                        r.policy,
                        int(r.repair_enabled),
                        r.shock,
                        ""
                        if r.aggregate_doubling_year is None
                        else f"{r.aggregate_doubling_year:.6f}",
                        f"{r.operating_at_horizon:.6f}",
                        f"{r.minimum_sector_margin_at_horizon:.6f}",
                        int(r.survived),
                        "" if r.shock_recovery_year is None else f"{r.shock_recovery_year:.6f}",
                        f"{r.cumulative_repaired_capacity:.6f}",
                    ]
                )

    with open(
        workspace.table_directory / "knowledge_autonomy_observables.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "sector",
                "named_task_completion_rate",
                "intervention_hours_per_capacity_year",
                "fault_diagnosis_fraction",
                "verification_throughput_per_year",
                "engineering_cycle_years",
                "process_yield",
                "repair_success_fraction",
                "mean_time_to_recovery_days",
                "stop_line_task_pass",
            ]
        )
        for name, seed in seeds.items():
            profile = seed.process
            for j, sector in enumerate(params.sectors):
                w.writerow(
                    [
                        name,
                        sector,
                        f"{profile.named_task_completion_rate[j]:.6f}",
                        f"{profile.intervention_hours_per_year[j]:.6f}",
                        f"{profile.fault_diagnosis_fraction[j]:.6f}",
                        f"{profile.verification_throughput_per_year[j]:.6f}",
                        f"{profile.engineering_cycle_years[j]:.6f}",
                        f"{profile.process_yield[j]:.6f}",
                        f"{profile.repair_success_fraction[j]:.6f}",
                        f"{profile.mean_time_to_recovery_days[j]:.6f}",
                        int(profile.stop_line_task_pass[j]),
                    ]
                )

    with open(
        workspace.table_directory / "knowledge_regime_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "variant",
                "operating_at_horizon",
                "aggregate_doubling_year",
                "material_steps",
                "autonomy_steps",
                "verification_steps",
                "repair_steps",
                "compute_steps",
                "service_steps",
                "order_rate_steps",
            ]
        )
        for name, rows in knowledge_regimes.items():
            for r in rows:
                w.writerow(
                    [
                        name,
                        r.variant,
                        f"{r.operating_at_horizon:.6f}",
                        ""
                        if r.aggregate_doubling_year is None
                        else f"{r.aggregate_doubling_year:.6f}",
                        r.material_steps,
                        r.autonomy_steps,
                        r.verification_steps,
                        r.repair_steps,
                        r.compute_steps,
                        r.service_steps,
                        r.order_rate_steps,
                    ]
                )

    with open(
        workspace.table_directory / "environment_process_effects.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "environment_profile",
                "feasible",
                "seed_mass_t",
                "top_binding_constraint",
                "operating_at_horizon",
                "aggregate_doubling_year",
                "survived",
            ]
        )
        for name, rows in environment_effects.items():
            for r in rows:
                w.writerow(
                    [
                        name,
                        r.environment_profile,
                        int(r.feasible),
                        "" if r.seed_mass_t is None else f"{r.seed_mass_t:.6f}",
                        r.top_binding_constraint or "",
                        "" if r.operating_at_horizon is None else f"{r.operating_at_horizon:.6f}",
                        ""
                        if r.aggregate_doubling_year is None
                        else f"{r.aggregate_doubling_year:.6f}",
                        "" if r.survived is None else int(r.survived),
                    ]
                )

    with open(
        workspace.table_directory / "policy_robustness_sweep.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "sweep_dimension",
                "sweep_value",
                "policy",
                "horizon_years",
                "survived",
                "terminal_window_expanding",
                "operating_at_horizon",
                "minimum_sector_margin_at_horizon",
                "aggregate_doubling_year",
            ]
        )
        for name, rows in policy_robustness.items():
            for r in rows:
                w.writerow(
                    [
                        name,
                        r.sweep_dimension,
                        f"{r.sweep_value:.6f}",
                        r.policy,
                        f"{r.horizon_years:.6f}",
                        int(r.survived),
                        int(r.terminal_window_expanding),
                        f"{r.operating_at_horizon:.6f}",
                        f"{r.minimum_sector_margin_at_horizon:.6f}",
                        ""
                        if r.aggregate_doubling_year is None
                        else f"{r.aggregate_doubling_year:.6f}",
                    ]
                )

    with open(
        workspace.table_directory / "electronics_architecture_comparison.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "architecture",
                "tier",
                "replacement_demand_capacity",
                "local_supply_capacity",
                "imported_supply_capacity",
                "cannibalized_supply_capacity",
                "substitution_credit_capacity",
                "expired_inventory_capacity",
                "terminal_import_inventory_capacity",
                "shortfall_capacity",
                "first_shortfall_year",
                "viable",
                "imported_mass_t",
                "measurement_priority",
            ]
        )
        for name, rows in electronics_architectures.items():
            for r in rows:
                w.writerow(
                    [
                        name,
                        r.architecture,
                        r.tier,
                        f"{r.replacement_demand_capacity:.6f}",
                        f"{r.local_supply_capacity:.6f}",
                        f"{r.imported_supply_capacity:.6f}",
                        f"{r.cannibalized_supply_capacity:.6f}",
                        f"{r.substitution_credit_capacity:.6f}",
                        f"{r.expired_inventory_capacity:.6f}",
                        f"{r.terminal_import_inventory_capacity:.6f}",
                        f"{r.shortfall_capacity:.6f}",
                        "" if r.first_shortfall_year is None else f"{r.first_shortfall_year:.6f}",
                        int(r.viable),
                        f"{r.imported_mass_t:.6f}",
                        r.measurement_priority,
                    ]
                )

    with open(
        workspace.table_directory / "symmetric_dynamic_economics.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "market",
                "year",
                "technical_space_capacity",
                "funded_space_capacity",
                "earth_capacity",
                "market_demand",
                "space_cash_musd",
                "earth_cash_musd",
                "space_debt_musd",
                "earth_debt_musd",
                "space_investment_musd",
                "earth_investment_musd",
                "space_finance_constrained_steps",
                "earth_finance_constrained_steps",
                "space_self_financing_year",
                "earth_self_financing_year",
            ]
        )
        for market, r in economics.items():
            for k, year in enumerate(r.t):
                w.writerow(
                    [
                        market,
                        f"{year:.6f}",
                        f"{r.technical_space_capacity[k]:.6f}",
                        f"{r.funded_space_capacity[k]:.6f}",
                        f"{r.earth_capacity[k]:.6f}",
                        f"{r.market_demand[k]:.6f}",
                        f"{r.space_cash_musd[k]:.6f}",
                        f"{r.earth_cash_musd[k]:.6f}",
                        f"{r.space_debt_musd[k]:.6f}",
                        f"{r.earth_debt_musd[k]:.6f}",
                        f"{r.space_investment_musd[k]:.6f}",
                        f"{r.earth_investment_musd[k]:.6f}",
                        r.space_finance_constrained_steps,
                        r.earth_finance_constrained_steps,
                        ""
                        if r.space_self_financing_year is None
                        else f"{r.space_self_financing_year:.6f}",
                        ""
                        if r.earth_self_financing_year is None
                        else f"{r.earth_self_financing_year:.6f}",
                    ]
                )

    with open(
        workspace.table_directory / "robust_seed_pareto.csv", "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "route",
                "redundancy",
                "source_portfolio",
                "delivered_mass_t",
                "import_mass_t",
                "intervention_hours_per_year",
                "aggregate_doubling_year",
                "operating_at_horizon",
                "terminal_window_expanding",
                "source_outage_operating_at_horizon",
                "source_outage_survived",
                "non_dominated",
                "robust_candidate",
            ]
        )
        for r in pareto_designs:
            w.writerow(
                [
                    r.scenario,
                    r.route,
                    r.redundancy,
                    r.source_portfolio,
                    f"{r.delivered_mass_t:.6f}",
                    f"{r.import_mass_t:.6f}",
                    f"{r.intervention_hours_per_year:.6f}",
                    "" if r.aggregate_doubling_year is None else f"{r.aggregate_doubling_year:.6f}",
                    f"{r.operating_at_horizon:.6f}",
                    int(r.terminal_window_expanding),
                    f"{r.source_outage_operating_at_horizon:.6f}",
                    int(r.source_outage_survived),
                    int(r.non_dominated),
                    int(r.robust_candidate),
                ]
            )

    with open(
        workspace.table_directory / "infeasibility_certificate.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["scenario", "constraint", "minimum_violation", "units"])
        for name, rows in certs.items():
            for r in rows:
                w.writerow([name, r.constraint, f"{r.minimum_violation:.6f}", r.units])
