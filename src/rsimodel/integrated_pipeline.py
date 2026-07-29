"""Typed orchestration for the integrated-bootstrap artifact set."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from rsimodel.ai_rnd_evidence import write_ai_rnd_evidence_csvs
from rsimodel.economic_calibration import write_economic_calibration_csv
from rsimodel.integrated import (
    compare_compute_regimes,
    load_integrated_params,
    seed_ensemble,
    simulate_capacity_growth,
    simulate_debris,
    simulate_seed_deployment,
    simulate_shell_debris,
    size_seed,
)
from rsimodel.integrated_analysis import (
    ablation_suite,
    allocation_repair_suite,
    bottleneck_upgrade_suite,
    capacity_regime_summary,
    closure_ablation_suite,
    compute_demand_allocation_suite,
    electronics_architecture_suite,
    ensemble_diagnostics,
    environment_effect_suite,
    import_stock_composition,
    infeasibility_certificate,
    intelligence_marginal_response_suite,
    knowledge_regime_suite,
    material_limited_steps,
    oversize_frontier,
    pareto_seed_designs,
    policy_robustness_sweep,
    simulate_symmetric_economics,
    terminal_endpoints,
)
from rsimodel.orbital_ai_scenarios import write_orbital_ai_scenario_csvs
from rsimodel.portfolio_coverage import write_portfolio_coverage_csvs
from rsimodel.precursor_telemetry import write_precursor_telemetry_csv
from rsimodel.process_closure import write_process_closure_gap_csv
from rsimodel.publication import write_publication_readiness_csv
from rsimodel.rehearsal import write_rehearsal_acceptance_csv
from rsimodel.run_config import IntegratedRunConfig
from rsimodel.solver_adapter import scipy_version
from rsimodel.spacexai_economics import write_spacexai_economic_artifacts
from rsimodel.yaml_adapter import pyyaml_version

from .integrated_artifacts import SCENARIOS, SEED_OBJECTIVES, ArtifactWorkspace
from .integrated_extension_tables import write_extension_tables
from .integrated_figures import generate_analysis_figures, generate_figures
from .integrated_report import write_report
from .integrated_tables import (
    write_analysis_tables,
    write_closure_ablation_table,
    write_compute_and_debris_tables,
    write_compute_demand_tables,
    write_deployment_table,
    write_governance_traceability,
    write_intelligence_response_tables,
    write_long_horizon_table,
    write_scenario_tables,
    write_seed_objective_table,
    write_shell_debris_tables,
)


def _display_path(path: Path, workspace: ArtifactWorkspace) -> Path:
    """Return a repository-relative path when possible, otherwise the resolved path."""
    try:
        return path.relative_to(workspace.project_root)
    except ValueError:
        return path


def write_manifest(workspace: ArtifactWorkspace, files: list[Path]) -> Path:
    lines = [
        "# Current artifact manifest",
        "",
        "- generated: 2026-07-28",
        f"- python: {platform.python_version()}",
        f"- numpy: {np.__version__}",
        f"- scipy: {scipy_version()}",
        f"- PyYAML: {pyyaml_version()}",
        "- generator: `rsi-run-integrated` (`rsimodel.integrated_pipeline`)",
        "",
        "| artifact/input | sha256 |",
        "|---|---|",
    ]
    for path in sorted(set(files), key=lambda p: str(p)):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        try:
            label = path.relative_to(workspace.project_root)
        except ValueError:
            label = Path("OUTPUT") / path.relative_to(workspace.output_directory)
        lines.append(f"| `{label}` | `{digest}` |")
    manifest = workspace.output_directory / "MANIFEST.md"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def run(config: IntegratedRunConfig) -> None:
    """Execute one deterministic artifact run in its explicit workspace."""
    workspace = ArtifactWorkspace.from_config(config)
    workspace.prepare()

    params = load_integrated_params(config.parameters)
    seeds = {name: size_seed(params, name) for name in SCENARIOS}
    runs = {
        name: simulate_capacity_growth(params, seed, years=40.0, dt=0.25)
        for name, seed in seeds.items()
        if seed.feasible
    }
    extended_runs = {
        name: simulate_capacity_growth(params, seed, years=80.0, dt=0.25)
        for name, seed in seeds.items()
        if seed.feasible
    }
    objective_seeds = {
        name: {
            objective: size_seed(params, name, objective=objective) for objective in SEED_OBJECTIVES
        }
        for name in SCENARIOS
    }
    deployments = {
        name: simulate_seed_deployment(params, seed)
        for name, seed in seeds.items()
        if seed.feasible
    }
    ensembles = {
        name: seed_ensemble(
            params,
            name,
            n_runs=workspace.ensemble_size,
            seed=workspace.ensemble_seed,
            years=40.0,
            dt=0.5,
        )
        for name in SCENARIOS
    }
    network_run = runs["moon_asteroid_network"]
    compute = compare_compute_regimes(params, network_run)
    debris_runs = [
        simulate_debris(
            params,
            compute.earth_fed_orbit["base"],
            compute.t,
            "weak_mitigation",
            label="Earth-fed orbit / weak mitigation",
        ),
        simulate_debris(
            params,
            compute.earth_fed_orbit["base"],
            compute.t,
            "strong_mitigation",
            label="Earth-fed orbit / strong mitigation",
        ),
        simulate_debris(
            params,
            compute.endogenous,
            compute.t,
            "weak_mitigation",
            label="dense endogenous / weak mitigation",
        ),
        simulate_debris(
            params,
            compute.endogenous,
            compute.t,
            "strong_mitigation",
            label="dense endogenous / strong mitigation",
        ),
        simulate_debris(
            params,
            compute.endogenous_orbit,
            compute.t,
            "distributed_heliocentric",
            label="distributed endogenous / sparse topology",
        ),
    ]
    shell_debris = simulate_shell_debris(
        params,
        compute.endogenous_orbit,
        compute.t,
    )

    endpoints = {n: terminal_endpoints(params, seeds[n], runs[n]) for n in runs}
    import_stocks = {n: import_stock_composition(params, seeds[n], runs[n]) for n in runs}
    ablations = {n: ablation_suite(params, n) for n in SCENARIOS if seeds[n].feasible}
    closure_matrix = closure_ablation_suite(
        params,
        "moon_asteroid_network",
    )
    intelligence_response_cfg = params.intelligence_marginal_response
    intelligence_responses = intelligence_marginal_response_suite(
        params,
        intelligence_response_cfg,
    )
    bottleneck_upgrade_cfg = params.bottleneck_upgrade_projects
    bottleneck_upgrades = bottleneck_upgrade_suite(bottleneck_upgrade_cfg)
    compute_demand_cfg = params.compute_demand_allocation
    compute_demand_rows = compute_demand_allocation_suite(compute_demand_cfg)
    frontiers = {n: oversize_frontier(params, n) for n in SCENARIOS if seeds[n].feasible}
    diags = {
        n: ensemble_diagnostics(
            params,
            n,
            n_runs=workspace.ensemble_size,
            seed=workspace.ensemble_seed,
            years=40.0,
            dt=0.5,
        )
        for n in SCENARIOS
    }
    certs = {n: infeasibility_certificate(params, n) for n in SCENARIOS if not seeds[n].feasible}
    limited = {n: material_limited_steps(params, seeds[n], runs[n]) for n in runs}
    regimes = {n: capacity_regime_summary(params, seeds[n], runs[n]) for n in runs}
    allocation_repair = {
        n: allocation_repair_suite(params, n) for n in SCENARIOS if seeds[n].feasible
    }
    knowledge_regimes = {
        n: knowledge_regime_suite(params, n) for n in SCENARIOS if seeds[n].feasible
    }
    environment_effects = {n: environment_effect_suite(params, n) for n in SCENARIOS}
    policy_robustness = {
        n: policy_robustness_sweep(params, n)
        for n in (
            "lunar_strategic_material_bridge",
            "moon_asteroid_network",
        )
    }
    electronics_architectures = {
        n: electronics_architecture_suite(params, n)
        for n in (
            "lunar_strategic_material_bridge",
            "moon_asteroid_network",
        )
    }
    economics = {
        market: simulate_symmetric_economics(
            params,
            seeds["moon_asteroid_network"],
            runs["moon_asteroid_network"],
            market,
        )
        for market in params.dynamic_economics["markets"]
    }
    pareto_designs = pareto_seed_designs(params)

    write_scenario_tables(workspace, params, seeds, runs, ensembles)
    write_compute_and_debris_tables(workspace, compute, debris_runs)
    write_shell_debris_tables(workspace, shell_debris)
    write_extension_tables(
        workspace,
        params,
        seeds,
        runs,
        debris_runs,
        shell_debris,
    )
    write_governance_traceability(workspace)
    write_rehearsal_acceptance_csv(workspace.table_directory / "rehearsal_acceptance_matrix.csv")
    write_economic_calibration_csv(workspace.table_directory / "economic_calibration_readiness.csv")
    write_process_closure_gap_csv(workspace.table_directory / "process_closure_gap_register.csv")
    write_precursor_telemetry_csv(
        workspace.table_directory / "observed_precursor_telemetry.csv",
        workspace.project_root / "params" / "observed_precursor_telemetry.json",
    )
    write_ai_rnd_evidence_csvs(
        workspace.table_directory / "ai_rnd_benchmark_registry.csv",
        workspace.table_directory / "ai_rnd_evidence_crosswalk.csv",
        workspace.project_root / "params" / "ai_rnd_evidence_registry.json",
    )
    write_portfolio_coverage_csvs(
        workspace.table_directory / "portfolio_sector_coverage.csv",
        workspace.table_directory / "portfolio_sector_coverage_summary.csv",
        workspace.table_directory / "portfolio_sector_group_summary.csv",
        workspace.project_root / "params" / "portfolio_sector_coverage.json",
    )
    write_orbital_ai_scenario_csvs(
        workspace.table_directory / "orbital_ai_scenario_inputs.csv",
        workspace.table_directory / "simulation_scenario_coverage.csv",
        workspace.table_directory / "orbital_ai_closure_stack.csv",
        workspace.table_directory / "orbital_ai_closure_summary.csv",
        workspace.table_directory / "orbital_ai_scenario_results.csv",
        workspace.project_root / "params" / "orbital_ai_scenario_registry.json",
    )
    write_spacexai_economic_artifacts(
        workspace.table_directory,
        workspace.figure_directory,
        workspace.project_root / "params" / "spacexai_economic_case.json",
    )
    write_publication_readiness_csv(workspace.table_directory / "publication_readiness.csv")
    write_long_horizon_table(workspace, params, seeds, extended_runs)
    write_seed_objective_table(workspace, params, objective_seeds)
    write_deployment_table(workspace, deployments)
    write_closure_ablation_table(workspace, closure_matrix)
    write_intelligence_response_tables(
        workspace,
        intelligence_responses,
        bottleneck_upgrades,
        intelligence_response_cfg,
        bottleneck_upgrade_cfg,
    )
    write_compute_demand_tables(workspace, compute_demand_rows, compute_demand_cfg)
    write_analysis_tables(
        workspace,
        params,
        seeds,
        endpoints,
        import_stocks,
        ablations,
        frontiers,
        allocation_repair,
        knowledge_regimes,
        environment_effects,
        policy_robustness,
        electronics_architectures,
        economics,
        pareto_designs,
        regimes,
        diags,
        certs,
    )
    generate_figures(workspace, seeds, runs, ensembles, compute, debris_runs)
    generate_analysis_figures(workspace, frontiers)
    report = write_report(
        workspace,
        params,
        seeds,
        runs,
        extended_runs,
        objective_seeds,
        deployments,
        ensembles,
        compute,
        debris_runs,
        shell_debris,
        endpoints,
        ablations,
        closure_matrix,
        frontiers,
        diags,
        certs,
        limited,
        regimes,
        allocation_repair,
        knowledge_regimes,
        environment_effects,
        policy_robustness,
        electronics_architectures,
        economics,
        pareto_designs,
    )

    inputs = [
        workspace.project_root / "params" / "integrated_model.yaml",
        workspace.project_root / "params" / "claim_glossary.yaml",
        workspace.project_root / "params" / "governance_controls.yaml",
        workspace.project_root / "params" / "rehearsal_protocol.yaml",
        workspace.project_root / "params" / "economic_calibration.yaml",
        workspace.project_root / "params" / "process_closure_requirements.yaml",
        workspace.project_root / "params" / "observed_precursor_telemetry.json",
        workspace.project_root / "params" / "ai_rnd_evidence_registry.json",
        workspace.project_root / "params" / "portfolio_sector_coverage.json",
        workspace.project_root / "params" / "orbital_ai_scenario_registry.json",
        workspace.project_root / "params" / "spacexai_economic_case.json",
        workspace.project_root / "params" / "publication_targets.yaml",
        workspace.project_root / "docs" / "sources" / "orbital-ai-landscape-2026-07-28.md",
        workspace.project_root / "docs" / "sources" / "spacex-ai-aspirations-2026-06.md",
        workspace.project_root / "docs" / "sources" / "starmind-ai1-2026-07-27.md",
        workspace.project_root / "docs" / "sources" / "spacexai-economic-thesis-2026-07-29.md",
        workspace.project_root / "src" / "rsimodel" / "integrated.py",
        workspace.project_root / "src" / "rsimodel" / "extensions.py",
        workspace.project_root / "src" / "rsimodel" / "extensions_digital.py",
        workspace.project_root / "src" / "rsimodel" / "extensions_coordination.py",
        workspace.project_root / "src" / "rsimodel" / "extensions_orbital.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_analysis.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_artifacts.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_tables.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_figures.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_report.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_extension_tables.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_digital_tables.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_coordination_tables.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_embodiment_tables.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_orbital_tables.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_closure_tables.py",
        workspace.project_root / "src" / "rsimodel" / "rehearsal.py",
        workspace.project_root / "src" / "rsimodel" / "economic_calibration.py",
        workspace.project_root / "src" / "rsimodel" / "process_closure.py",
        workspace.project_root / "src" / "rsimodel" / "precursor_telemetry.py",
        workspace.project_root / "src" / "rsimodel" / "ai_rnd_evidence.py",
        workspace.project_root / "src" / "rsimodel" / "portfolio_coverage.py",
        workspace.project_root / "src" / "rsimodel" / "orbital_ai_scenarios.py",
        workspace.project_root / "src" / "rsimodel" / "spacexai_economics.py",
        workspace.project_root / "src" / "rsimodel" / "manifests.py",
        workspace.project_root / "src" / "rsimodel" / "publication.py",
        workspace.project_root / "src" / "rsimodel" / "release.py",
        workspace.project_root / "src" / "rsimodel" / "evidence.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_pipeline.py",
        workspace.project_root / "src" / "rsimodel" / "integrated_runner.py",
        workspace.project_root / "src" / "rsimodel" / "run_config.py",
        workspace.project_root / "src" / "rsimodel" / "manifest_cli.py",
        workspace.project_root / "src" / "rsimodel" / "release_cli.py",
        workspace.project_root / "src" / "rsimodel" / "publication_cli.py",
        workspace.project_root / "src" / "rsimodel" / "evidence_cli.py",
        workspace.project_root / "tests" / "test_integrated.py",
        workspace.project_root / "tests" / "test_extensions.py",
        workspace.project_root / "tests" / "test_integrated_analysis.py",
        workspace.project_root / "tests" / "test_rehearsal.py",
        workspace.project_root / "tests" / "test_economic_calibration.py",
        workspace.project_root / "tests" / "test_process_closure.py",
        workspace.project_root / "tests" / "test_ai_rnd_evidence.py",
        workspace.project_root / "tests" / "test_spacexai_economics.py",
        workspace.project_root / "tests" / "test_manifests.py",
        workspace.project_root / "tests" / "test_publication.py",
        workspace.project_root / "tests" / "test_release.py",
        workspace.project_root / "tests" / "test_evidence_bundles.py",
        workspace.project_root / "docs" / "GOVERNANCE_THREAT_MODEL.md",
        workspace.project_root / "docs" / "TERRESTRIAL_REHEARSAL_PROTOCOL.md",
        workspace.project_root / "docs" / "ECONOMIC_CALIBRATION_PROTOCOL.md",
        workspace.project_root / "docs" / "PROCESS_CLOSURE_ACCEPTANCE_CONTRACT.md",
        workspace.project_root / "docs" / "VENUE_SELECTION_AND_CONFORMANCE.md",
        workspace.project_root / "docs" / "RELEASE_RUNBOOK.md",
        workspace.project_root / "papers" / "README.md",
        workspace.project_root / "papers" / "TECHNICAL_PAPER_r4.0.md",
        workspace.project_root / "papers" / "ORBITAL_COMPUTE_ECONOMICS_r4.0.md",
        workspace.project_root / "papers" / "STRATEGY_GOVERNANCE_CASE_STUDY_r4.0.md",
        workspace.project_root / "papers" / "TECHNICAL_SUPPLEMENT_r4.0.md",
    ]
    artifacts = [
        report,
        *workspace.table_directory.glob("*.csv"),
        *workspace.figure_directory.glob("*.png"),
    ]
    manifest = write_manifest(workspace, inputs + artifacts)

    summary = {
        name: {
            "feasible": seeds[name].feasible,
            "seed_mass_t": seeds[name].total_seed_mass_t,
            "aggregate_doubling_year": (
                runs[name].aggregate_doubling_year if name in runs else None
            ),
            "ensemble_feasible": f"{ensembles[name].n_feasible}/{workspace.ensemble_size}",
        }
        for name in SCENARIOS
    }
    print(json.dumps(summary, indent=2))
    print(_display_path(report, workspace))
    print(_display_path(manifest, workspace))
