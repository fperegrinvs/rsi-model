"""Generate the integrated-bootstrap artifact set.

All outputs are written beneath ``outputs/integrated/``. The run is deterministic:
assumption-ensemble cells use name-keyed crc32 seeds in
``rsimodel.integrated.sample_integrated_params``.
"""
from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import numpy as np
import scipy
import yaml

from rsimodel.economic_calibration import write_economic_calibration_csv
from rsimodel.integrated import (
    compare_compute_regimes,
    load_integrated_params,
    seed_ensemble,
    simulate_capacity_growth,
    simulate_debris,
    simulate_shell_debris,
    simulate_seed_deployment,
    size_seed,
)
from rsimodel.integrated_analysis import (
    ablation_suite,
    allocation_repair_suite,
    capacity_regime_summary,
    ensemble_diagnostics,
    electronics_architecture_suite,
    environment_effect_suite,
    import_stock_composition,
    infeasibility_certificate,
    knowledge_regime_suite,
    material_limited_steps,
    oversize_frontier,
    pareto_seed_designs,
    policy_robustness_sweep,
    simulate_symmetric_economics,
    terminal_endpoints,
)
from rsimodel.process_closure import write_process_closure_gap_csv
from rsimodel.publication import write_publication_readiness_csv
from rsimodel.rehearsal import write_rehearsal_acceptance_csv

OUT = ROOT / "outputs" / "integrated"
FIG = OUT / "figures"
TAB = OUT / "tables"
SCENARIOS = (
    "terrestrial_rehearsal",
    "lunar_strategic_material_bridge",
    "lunar_strict",
    "moon_asteroid_network",
)
N_ENSEMBLE = 200
ENSEMBLE_SEED = 404
SEED_OBJECTIVES = (
    "installed_mass",
    "earth_import_mass",
    "intervention_hours",
)


def fmt(value: float | None, digits: int = 1) -> str:
    return "—" if value is None else f"{value:,.{digits}f}"


def fmt_year(value: float | None, digits: int = 1) -> str:
    return "—" if value is None else f"{value:,.{digits}f} yr"


def pct(values: tuple[float, ...]) -> tuple[float, float, float] | None:
    if not values:
        return None
    return tuple(float(v) for v in np.percentile(values, [10, 50, 90]))


def write_scenario_tables(params, seeds, runs, ensembles) -> None:
    with open(TAB / "scenario_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "feasible", "status", "seed_mass_t", "physical_seed_mass_t",
            "import_stock_mass_t", "digital_seed_mass_t", "lunar_feed_t_per_year",
            "asteroid_feed_t_per_year", "minimum_task_coverage",
            "intervention_hours_per_year", "aggregate_doubling_year",
            "operating_cells_year40", "intelligence_year40", "survived",
        ])
        for name in SCENARIOS:
            s = seeds[name]
            r = runs.get(name)
            w.writerow([
                name, int(s.feasible), s.status,
                "" if s.total_seed_mass_t is None else f"{s.total_seed_mass_t:.8f}",
                "" if s.physical_seed_mass_t is None else f"{s.physical_seed_mass_t:.8f}",
                "" if s.import_stock_mass_t is None else f"{s.import_stock_mass_t:.8f}",
                f"{s.digital_seed_mass_t:.8f}",
                f"{s.lunar_feed_t_per_year:.8f}", f"{s.asteroid_feed_t_per_year:.8f}",
                f"{s.minimum_task_coverage:.8f}",
                f"{s.intervention_hours_per_year:.8f}",
                "" if r is None or r.aggregate_doubling_year is None
                else f"{r.aggregate_doubling_year:.8f}",
                "" if r is None else f"{r.operating_cells[-1]:.8f}",
                "" if r is None else f"{r.intelligence[-1]:.8f}",
                "" if r is None else int(r.survived),
            ])

    with open(TAB / "seed_sector_capacity.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["scenario", "sector", "capacity", "embedded_mass_t",
                    "centrifuge_mass_t", "task_coverage"])
        for name in SCENARIOS:
            s = seeds[name]
            for j, sector in enumerate(params.sectors):
                w.writerow([
                    name, sector, f"{s.capacities[j]:.9f}",
                    f"{s.process.B_effective[:, j].sum() * s.capacities[j]:.9f}",
                    f"{s.process.centrifuge_mass_t[j] * s.capacities[j]:.9f}",
                    f"{s.process.coverage[j]:.9f}",
                ])

    with open(
        TAB / "sector_capacity_trajectory.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "year", "sector", "installed_capacity",
            "operating_capacity", "ordered_capacity",
            "normalized_installed_cell_equivalents",
            "normalized_operating_cell_equivalents",
        ])
        for name, run in runs.items():
            z = seeds[name].capacities
            for k, year in enumerate(run.t):
                for j, sector in enumerate(params.sectors):
                    w.writerow([
                        name, f"{year:.6f}", sector,
                        f"{run.installed_sector_capacity[k, j]:.9f}",
                        f"{run.operating_sector_capacity[k, j]:.9f}",
                        f"{run.ordered_sector_capacity[k, j]:.9f}",
                        f"{run.installed_sector_capacity[k, j] / z[j]:.9f}",
                        f"{run.operating_sector_capacity[k, j] / z[j]:.9f}",
                    ])

    with open(TAB / "element_flows.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["scenario", "element", "cell_bom_t", "initial_earth_stock_t",
                    "lunar_output_t_per_cell_year", "asteroid_output_t_per_cell_year"])
        for name in SCENARIOS:
            s = seeds[name]
            for e, element in enumerate(params.elements):
                cell_bom = float(s.process.B_effective[e] @ s.capacities)
                w.writerow([
                    name, element, f"{cell_bom:.9f}",
                    f"{s.import_stock_t[e]:.9f}",
                    f"{params.lunar_yield[e] * s.lunar_feed_t_per_year:.9f}",
                    f"{params.asteroid_yield[e] * s.asteroid_feed_t_per_year:.9f}",
                ])

    with open(TAB / "ensemble_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "n_runs", "n_feasible", "feasible_share",
            "n_survived", "survived_share", "seed_p10_t", "seed_p50_t",
            "seed_p90_t", "aggregate_doubling_p10_year",
            "aggregate_doubling_p50_year", "aggregate_doubling_p90_year",
        ])
        for name in SCENARIOS:
            e = ensembles[name]
            sm, sy = pct(e.seed_masses_t), pct(e.aggregate_doubling_years)
            w.writerow([
                name, e.n_runs, e.n_feasible, f"{e.feasible_share:.6f}",
                e.n_survived, f"{e.survived_share:.6f}",
                *(["", "", ""] if sm is None else [f"{v:.6f}" for v in sm]),
                *(["", "", ""] if sy is None else [f"{v:.6f}" for v in sy]),
            ])


def generate_figures(params, seeds, runs, ensembles, compute, debris_runs) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(9, 5.2))
    labels, data = [], []
    for name in SCENARIOS:
        values = ensembles[name].seed_masses_t
        if values:
            labels.append(name.replace("_", "\n"))
            data.append(values)
    ax.boxplot(data, tick_labels=labels, showfliers=False, whis=(10, 90))
    for i, name in enumerate([n for n in SCENARIOS if ensembles[n].seed_masses_t], 1):
        central = seeds[name]
        ax.scatter(
            [i], [central.total_seed_mass_t], marker="D", s=45, color="#d1495b",
            label="central scenario" if i == 1 else None, zorder=4,
        )
    ax.set_ylabel("Installed seed mass (scenario tonnes)")
    ax.set_title("Current seed-sizing assumption ensembles")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "seed_mass_ensemble.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    for name, run in runs.items():
        ax.plot(run.t, run.operating_cells, label=name.replace("_", " "))
    ax.axhline(
        2.0, color="#333333", ls="--", lw=1,
        label="aggregate operating-capacity doubling",
    )
    ax.set_xlabel("Years after seed activation")
    ax.set_ylabel("Sector-balanced operating-cell equivalents")
    ax.set_yscale("log")
    ax.set_ylim(0.5, max(20.0, max(r.operating_cells[-1] for r in runs.values()) * 1.2))
    ax.set_title("Slowest-sector capacity after sector-specific commissioning")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "operating_capacity.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(compute.t, compute.endogenous, lw=2.5, label="off-world endogenous total")
    ax.plot(compute.t, compute.endogenous_orbit, lw=2.0, label="Moon→orbit endogenous")
    for label in ("tight", "base", "responsive"):
        ax.plot(
            compute.t, compute.earth_fed_orbit[label], ls="--",
            label=f"Earth-fed orbit: {label}",
        )
    ax.set_xlabel("Years")
    ax.set_ylabel("Compute capacity (normalized to initial stock)")
    ax.set_title("Rate-limited deployment versus endogenous capacity growth")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "compute_growth_regimes.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    for d in debris_runs:
        ax.plot(
            d.t, d.fragments,
            label=f"{d.label} · R={d.creation_clearance_ratio:.2f}",
        )
    ax.set_xlabel("Years")
    ax.set_ylabel("Fragment index (scenario units)")
    ax.set_yscale("symlog", linthresh=0.01)
    ax.set_title("Orbital growth is conditional on debris topology and mitigation")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG / "debris_regimes.png", dpi=180)
    plt.close(fig)


def write_compute_and_debris_tables(compute, debris_runs) -> None:
    with open(TAB / "compute_curves.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "year", "endogenous_total", "endogenous_orbit",
            "earth_tight", "earth_base", "earth_responsive",
            "earth_fed_orbit_tight", "earth_fed_orbit_base",
            "earth_fed_orbit_responsive",
        ])
        for k, year in enumerate(compute.t):
            w.writerow([
                f"{year:.6f}", f"{compute.endogenous[k]:.9f}",
                f"{compute.endogenous_orbit[k]:.9f}",
                f"{compute.terrestrial['tight'][k]:.9f}",
                f"{compute.terrestrial['base'][k]:.9f}",
                f"{compute.terrestrial['responsive'][k]:.9f}",
                f"{compute.earth_fed_orbit['tight'][k]:.9f}",
                f"{compute.earth_fed_orbit['base'][k]:.9f}",
                f"{compute.earth_fed_orbit['responsive'][k]:.9f}",
            ])

    with open(TAB / "debris_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "case", "creation_clearance_ratio_last5y", "subcritical",
            "active_year40", "derelict_year40", "fragment_index_year40",
        ])
        for d in debris_runs:
            w.writerow([
                d.label, f"{d.creation_clearance_ratio:.9f}", int(d.subcritical),
                f"{d.active[-1]:.9f}", f"{d.derelict[-1]:.9f}",
                f"{d.fragments[-1]:.9f}",
            ])


def write_shell_debris_tables(shell_debris) -> None:
    with open(TAB / "orbital_mass_balance.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "year", "uncaptured_reservoir_t", "feed_inventory_t",
            "accessible_orbital_mass_t", "earth_imported_t", "captured_t",
            "recovered_t", "unrecoverable_loss_t",
            "requested_deployment_units", "served_deployment_units",
            "deployment_shortfall_units",
        ])
        for k, year in enumerate(shell_debris.t):
            w.writerow([
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
            ])

    with open(TAB / "shell_debris_trajectory.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "year", "shell", "active_capacity", "intact_derelicts",
            "trackable_fragments", "untrackable_fragments",
            "terminal_branching_ratio",
        ])
        for k, year in enumerate(shell_debris.t):
            for s, shell in enumerate(shell_debris.shells):
                w.writerow([
                    f"{year:.6f}", shell,
                    f"{shell_debris.active_capacity[k, s]:.6f}",
                    f"{shell_debris.intact_derelicts[k, s]:.6f}",
                    f"{shell_debris.trackable_fragments[k, s]:.6f}",
                    f"{shell_debris.untrackable_fragments[k, s]:.6f}",
                    f"{shell_debris.branching_ratio_by_shell[s]:.6f}",
                ])


def write_governance_traceability() -> Path:
    source = ROOT / "params" / "governance_controls.yaml"
    governance = yaml.safe_load(source.read_text(encoding="utf-8"))
    target = TAB / "governance_threat_control_traceability.csv"
    with open(target, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "threat", "class", "affected_assets", "physical_state_trigger",
            "control", "control_action", "verification", "rollback",
            "control_status", "residual_risk",
        ])
        for threat, threat_cfg in governance["threats"].items():
            for control in threat_cfg["controls"]:
                control_cfg = governance["controls"][control]
                w.writerow([
                    threat, threat_cfg["class"],
                    "; ".join(threat_cfg["affected_assets"]),
                    threat_cfg["physical_state_trigger"],
                    control, control_cfg["action"],
                    control_cfg["verification"], control_cfg["rollback"],
                    control_cfg["status"], threat_cfg["residual_risk"],
                ])
    return target


def write_long_horizon_table(params, seeds, extended_runs) -> None:
    with open(
        TAB / "long_horizon_endpoints.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "year", "aggregate_operating_cell_equivalents",
            "net_capacity_change_prior5y", "bottleneck_sector",
            "bottleneck_sector_equivalents", "aggregate_doubling_year",
        ])
        for name, run in extended_runs.items():
            z = seeds[name].capacities
            for year in (40.0, 60.0, 80.0):
                k = int(np.searchsorted(run.t, year))
                ratios = run.operating_sector_capacity[k] / z
                bottleneck = int(np.argmin(ratios))
                k0 = int(np.searchsorted(run.t, year - 5.0))
                net = float(run.operating_cells[k] - run.operating_cells[k0])
                w.writerow([
                    name, f"{year:.1f}", f"{run.operating_cells[k]:.9f}",
                    f"{net:.9f}", params.sectors[bottleneck],
                    f"{ratios[bottleneck]:.9f}",
                    "" if run.aggregate_doubling_year is None
                    else f"{run.aggregate_doubling_year:.6f}",
                ])


def write_seed_objective_table(params, objective_seeds) -> None:
    with open(
        TAB / "seed_objective_comparison.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "objective", "feasible", "installed_seed_mass_t",
            "earth_import_mass_t", "intervention_hours_per_year",
            "capacity_l1_distance_from_mass_optimum",
            "sector_balanced_equivalents_year40",
            "aggregate_doubling_year_80y_extension",
        ])
        for name, by_objective in objective_seeds.items():
            baseline = by_objective["installed_mass"]
            for objective in SEED_OBJECTIVES:
                seed = by_objective[objective]
                if not seed.feasible:
                    w.writerow([name, objective, 0, "", "", "", "", "", ""])
                    continue
                run40 = simulate_capacity_growth(
                    params, seed, years=40.0, dt=0.25
                )
                run80 = simulate_capacity_growth(
                    params, seed, years=80.0, dt=0.25
                )
                distance = float(np.abs(
                    seed.capacities - baseline.capacities
                ).sum())
                w.writerow([
                    name, objective, 1,
                    f"{seed.total_seed_mass_t:.9f}",
                    f"{seed.import_stock_mass_t:.9f}",
                    f"{seed.intervention_hours_per_year:.9f}",
                    f"{distance:.9f}",
                    f"{run40.operating_cells[-1]:.9f}",
                    "" if run80.aggregate_doubling_year is None
                    else f"{run80.aggregate_doubling_year:.6f}",
                ])


def write_deployment_table(deployments) -> None:
    with open(TAB / "seed_deployment_trajectory.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "year", "delivered_core_t", "staged_core_t",
            "installed_uncommissioned_core_t", "commissioned_core_t",
            "operating_core_t", "recovery_backlog_t", "spares_remaining_t",
            "installed_seed_mass_t", "delivered_seed_mass_t",
            "startup_energy_mwh", "full_operating_seed_year", "success",
        ])
        for name, d in deployments.items():
            for k, year in enumerate(d.t):
                w.writerow([
                    name, f"{year:.6f}", f"{d.delivered_core_t[k]:.6f}",
                    f"{d.staged_core_t[k]:.6f}",
                    f"{d.installed_core_t[k]:.6f}",
                    f"{d.commissioned_core_t[k]:.6f}",
                    f"{d.operating_core_t[k]:.6f}",
                    f"{d.recovery_backlog_t[k]:.6f}",
                    f"{d.spares_remaining_t[k]:.6f}",
                    f"{d.installed_seed_mass_t:.6f}",
                    f"{d.delivered_seed_mass_t:.6f}",
                    f"{d.startup_energy_mwh:.6f}",
                    "" if d.full_operating_seed_year is None
                    else f"{d.full_operating_seed_year:.6f}",
                    int(d.success),
                ])


def write_analysis_tables(params, seeds, endpoints, import_stocks, ablations,
                          frontiers, allocation_repair, knowledge_regimes,
                          environment_effects, policy_robustness,
                          electronics_architectures, economics, pareto_designs,
                          regimes, diags,
                          certs) -> None:
    with open(TAB / "terminal_endpoints.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "aggregate_doubling_year", "operating_at_horizon",
            "retained_at_horizon", "net_capacity_change_final5y",
            "terminal_window_expanding", "import_pools_exhausted_year",
            "ensemble_n_feasible", "ensemble_n_retained",
            "ensemble_n_terminal_window_expanding",
        ])
        for name, d in diags.items():
            e = endpoints.get(name)
            w.writerow([
                name,
                "" if e is None or e.aggregate_doubling_year is None
                else f"{e.aggregate_doubling_year:.6f}",
                "" if e is None else f"{e.operating_at_horizon:.6f}",
                "" if e is None else int(e.retained_at_horizon),
                "" if e is None else f"{e.net_capacity_change_final5:.6f}",
                "" if e is None else int(e.terminal_window_expanding),
                "" if e is None or e.import_pools_exhausted_year is None
                else f"{e.import_pools_exhausted_year:.6f}",
                d.n_feasible, d.n_retained, d.n_terminal_window_expanding,
            ])

    with open(TAB / "import_stock_composition.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "element", "initial_stock_t",
            "share_of_import_stock", "initial_rate_coverage_years",
            "pool_min_t", "pool_at_aggregate_doubling_t", "pool_at_horizon_t",
            "pool_first_exhaustion_year",
        ])
        for name, rows in import_stocks.items():
            for r in rows:
                w.writerow([
                    name, r.element, f"{r.initial_stock_t:.6f}",
                    f"{r.share_of_import_stock:.6f}",
                    "" if r.initial_rate_coverage_years is None
                    else f"{r.initial_rate_coverage_years:.4f}",
                    f"{r.pool_min_t:.6f}",
                    "" if r.pool_at_aggregate_doubling_t is None
                    else f"{r.pool_at_aggregate_doubling_t:.6f}",
                    f"{r.pool_at_horizon_t:.6f}",
                    "" if r.pool_exhaustion_year is None
                    else f"{r.pool_exhaustion_year:.4f}",
                ])

    with open(TAB / "ablations.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "variant", "definition", "feasible",
            "aggregate_doubling_year", "operating_at_horizon",
            "growth_share_of_baseline",
        ])
        for name, rows in ablations.items():
            for a in rows:
                w.writerow([
                    name, a.variant, a.definition, int(a.feasible),
                    "" if a.aggregate_doubling_year is None
                    else f"{a.aggregate_doubling_year:.6f}",
                    "" if a.operating_at_horizon is None
                    else f"{a.operating_at_horizon:.6f}",
                    "" if a.growth_share_of_baseline is None
                    else f"{a.growth_share_of_baseline:.6f}",
                ])

    with open(TAB / "oversize_frontier.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "oversize_factor", "installed_mass_t",
            "time_to_one_additional_cell_year",
            "additional_cells_at_horizon", "retained_plus_one_at_horizon",
        ])
        for name, rows in frontiers.items():
            for r in rows:
                w.writerow([
                    name, f"{r.oversize_factor:.2f}",
                    f"{r.installed_mass_t:.6f}",
                    "" if r.time_to_one_additional_cell is None
                    else f"{r.time_to_one_additional_cell:.6f}",
                    f"{r.additional_cells_at_horizon:.6f}",
                    int(r.retained_plus_one_at_horizon),
                ])

    with open(TAB / "ensemble_sensitivity.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "multiplier", "rho_seed_mass",
            "rho_aggregate_doubling_year", "rho_operating_at_horizon",
        ])
        for name, d in diags.items():
            if d.n_feasible < 8:
                continue
            for mult, s in d.sensitivity.items():
                w.writerow([
                    name, mult,
                    f"{s['seed_mass_t']:.4f}",
                    f"{s['aggregate_doubling_year']:.4f}",
                    f"{s['operating_at_horizon']:.4f}",
                ])

    with open(TAB / "diagnostics_histograms.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["scenario", "kind", "key", "count"])
        for name, d in diags.items():
            for key, count in sorted(d.failure_histogram.items(),
                                     key=lambda kv: -kv[1]):
                w.writerow([name, "failure_reason", key, count])
            for key, count in sorted(d.binding_histogram.items(),
                                     key=lambda kv: -kv[1]):
                w.writerow([name, "top_binding_constraint", key, count])

    with open(TAB / "dynamic_regime_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "total_steps", "material_limited_steps",
            "service_limited_steps", "order_rate_limited_steps",
            "autonomy_limited_steps", "verification_limited_steps",
            "repair_limited_steps", "compute_limited_steps",
        ])
        for name, r in regimes.items():
            w.writerow([
                name, r.total_steps, r.material_limited,
                r.service_limited, r.order_rate_limited,
                r.autonomy_limited, r.verification_limited,
                r.repair_limited, r.compute_limited,
            ])

    with open(TAB / "allocation_repair_comparison.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "allocation_policy", "repair_enabled", "shock",
            "aggregate_doubling_year", "operating_at_horizon",
            "minimum_sector_margin_at_horizon", "survived",
            "shock_recovery_year", "cumulative_repaired_capacity",
        ])
        for name, rows in allocation_repair.items():
            for r in rows:
                w.writerow([
                    name, r.policy, int(r.repair_enabled), r.shock,
                    "" if r.aggregate_doubling_year is None
                    else f"{r.aggregate_doubling_year:.6f}",
                    f"{r.operating_at_horizon:.6f}",
                    f"{r.minimum_sector_margin_at_horizon:.6f}",
                    int(r.survived),
                    "" if r.shock_recovery_year is None
                    else f"{r.shock_recovery_year:.6f}",
                    f"{r.cumulative_repaired_capacity:.6f}",
                ])

    with open(TAB / "knowledge_autonomy_observables.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "sector", "named_task_completion_rate",
            "intervention_hours_per_capacity_year",
            "fault_diagnosis_fraction", "verification_throughput_per_year",
            "engineering_cycle_years", "process_yield",
            "repair_success_fraction", "mean_time_to_recovery_days",
            "stop_line_task_pass",
        ])
        for name, seed in seeds.items():
            profile = seed.process
            for j, sector in enumerate(params.sectors):
                w.writerow([
                    name, sector,
                    f"{profile.named_task_completion_rate[j]:.6f}",
                    f"{profile.intervention_hours_per_year[j]:.6f}",
                    f"{profile.fault_diagnosis_fraction[j]:.6f}",
                    f"{profile.verification_throughput_per_year[j]:.6f}",
                    f"{profile.engineering_cycle_years[j]:.6f}",
                    f"{profile.process_yield[j]:.6f}",
                    f"{profile.repair_success_fraction[j]:.6f}",
                    f"{profile.mean_time_to_recovery_days[j]:.6f}",
                    int(profile.stop_line_task_pass[j]),
                ])

    with open(TAB / "knowledge_regime_summary.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "variant", "operating_at_horizon",
            "aggregate_doubling_year", "material_steps", "autonomy_steps",
            "verification_steps", "repair_steps", "compute_steps",
            "service_steps", "order_rate_steps",
        ])
        for name, rows in knowledge_regimes.items():
            for r in rows:
                w.writerow([
                    name, r.variant, f"{r.operating_at_horizon:.6f}",
                    "" if r.aggregate_doubling_year is None
                    else f"{r.aggregate_doubling_year:.6f}",
                    r.material_steps, r.autonomy_steps, r.verification_steps,
                    r.repair_steps, r.compute_steps, r.service_steps,
                    r.order_rate_steps,
                ])

    with open(TAB / "environment_process_effects.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "environment_profile", "feasible", "seed_mass_t",
            "top_binding_constraint", "operating_at_horizon",
            "aggregate_doubling_year", "survived",
        ])
        for name, rows in environment_effects.items():
            for r in rows:
                w.writerow([
                    name, r.environment_profile, int(r.feasible),
                    "" if r.seed_mass_t is None else f"{r.seed_mass_t:.6f}",
                    r.top_binding_constraint or "",
                    "" if r.operating_at_horizon is None
                    else f"{r.operating_at_horizon:.6f}",
                    "" if r.aggregate_doubling_year is None
                    else f"{r.aggregate_doubling_year:.6f}",
                    "" if r.survived is None else int(r.survived),
                ])

    with open(TAB / "policy_robustness_sweep.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "sweep_dimension", "sweep_value", "policy",
            "horizon_years", "survived", "terminal_window_expanding",
            "operating_at_horizon", "minimum_sector_margin_at_horizon",
            "aggregate_doubling_year",
        ])
        for name, rows in policy_robustness.items():
            for r in rows:
                w.writerow([
                    name, r.sweep_dimension, f"{r.sweep_value:.6f}",
                    r.policy, f"{r.horizon_years:.6f}", int(r.survived),
                    int(r.terminal_window_expanding),
                    f"{r.operating_at_horizon:.6f}",
                    f"{r.minimum_sector_margin_at_horizon:.6f}",
                    "" if r.aggregate_doubling_year is None
                    else f"{r.aggregate_doubling_year:.6f}",
                ])

    with open(TAB / "electronics_architecture_comparison.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "architecture", "tier",
            "replacement_demand_capacity", "local_supply_capacity",
            "imported_supply_capacity", "cannibalized_supply_capacity",
            "substitution_credit_capacity", "expired_inventory_capacity",
            "terminal_import_inventory_capacity", "shortfall_capacity",
            "first_shortfall_year", "viable", "imported_mass_t",
            "measurement_priority",
        ])
        for name, rows in electronics_architectures.items():
            for r in rows:
                w.writerow([
                    name, r.architecture, r.tier,
                    f"{r.replacement_demand_capacity:.6f}",
                    f"{r.local_supply_capacity:.6f}",
                    f"{r.imported_supply_capacity:.6f}",
                    f"{r.cannibalized_supply_capacity:.6f}",
                    f"{r.substitution_credit_capacity:.6f}",
                    f"{r.expired_inventory_capacity:.6f}",
                    f"{r.terminal_import_inventory_capacity:.6f}",
                    f"{r.shortfall_capacity:.6f}",
                    "" if r.first_shortfall_year is None
                    else f"{r.first_shortfall_year:.6f}",
                    int(r.viable), f"{r.imported_mass_t:.6f}",
                    r.measurement_priority,
                ])

    with open(TAB / "symmetric_dynamic_economics.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "market", "year", "technical_space_capacity",
            "funded_space_capacity", "earth_capacity", "market_demand",
            "space_cash_musd", "earth_cash_musd", "space_debt_musd",
            "earth_debt_musd", "space_investment_musd",
            "earth_investment_musd", "space_finance_constrained_steps",
            "earth_finance_constrained_steps", "space_self_financing_year",
            "earth_self_financing_year",
        ])
        for market, r in economics.items():
            for k, year in enumerate(r.t):
                w.writerow([
                    market, f"{year:.6f}",
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
                    "" if r.space_self_financing_year is None
                    else f"{r.space_self_financing_year:.6f}",
                    "" if r.earth_self_financing_year is None
                    else f"{r.earth_self_financing_year:.6f}",
                ])

    with open(TAB / "robust_seed_pareto.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "route", "redundancy", "source_portfolio",
            "delivered_mass_t", "import_mass_t",
            "intervention_hours_per_year", "aggregate_doubling_year",
            "operating_at_horizon", "terminal_window_expanding",
            "source_outage_operating_at_horizon",
            "source_outage_survived", "non_dominated", "robust_candidate",
        ])
        for r in pareto_designs:
            w.writerow([
                r.scenario, r.route, r.redundancy, r.source_portfolio,
                f"{r.delivered_mass_t:.6f}", f"{r.import_mass_t:.6f}",
                f"{r.intervention_hours_per_year:.6f}",
                "" if r.aggregate_doubling_year is None
                else f"{r.aggregate_doubling_year:.6f}",
                f"{r.operating_at_horizon:.6f}",
                int(r.terminal_window_expanding),
                f"{r.source_outage_operating_at_horizon:.6f}",
                int(r.source_outage_survived), int(r.non_dominated),
                int(r.robust_candidate),
            ])

    with open(TAB / "infeasibility_certificate.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["scenario", "constraint", "minimum_violation", "units"])
        for name, rows in certs.items():
            for r in rows:
                w.writerow([name, r.constraint,
                            f"{r.minimum_violation:.6f}", r.units])


def generate_analysis_figures(frontiers) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    for name, rows in frontiers.items():
        xs = [r.installed_mass_t for r in rows]
        ys = [r.time_to_one_additional_cell for r in rows]
        ax.plot(xs, ys, marker="o", label=name)
        for r in rows:
            if r.time_to_one_additional_cell is not None:
                ax.annotate(f"×{r.oversize_factor:g}",
                            (r.installed_mass_t, r.time_to_one_additional_cell),
                            textcoords="offset points", xytext=(4, 4),
                            fontsize=8)
    ax.set_xlabel("Installed seed mass (scenario tonnes)")
    ax.set_ylabel("Years to one additional operating cell-equivalent")
    ax.set_title("Oversize frontier: mass versus aggregate-capacity doubling")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "oversize_frontier.png", dpi=180)
    plt.close(fig)


def write_report(params, seeds, runs, extended_runs, objective_seeds,
                 deployments, ensembles, compute, debris_runs,
                 shell_debris,
                 endpoints, import_stocks, ablations, frontiers, diags,
                 certs, limited, regimes, allocation_repair,
                 knowledge_regimes, environment_effects,
                 policy_robustness, electronics_architectures,
                 economics, pareto_designs) -> Path:
    lines = [
        "# Current integrated-bootstrap model",
        "",
        f"- model version: `{params.version}`",
        f"- assumption ensemble: n={N_ENSEMBLE} per scenario, seed={ENSEMBLE_SEED}",
        "- epistemic status: scenario implications, not measurements or forecasts",
        "",
        "## Headline results",
        "",
        "| scenario | central installed seed mass | Earth strategic-material import stock | "
        "aggregate operating-capacity doubling (80y extension) | "
        "cell-equivalents at year 40 | design-space occupancy | ensemble seed p10/p50/p90 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in SCENARIOS:
        s, e = seeds[name], ensembles[name]
        r = runs.get(name)
        extended = extended_runs.get(name)
        mass_p = pct(e.seed_masses_t)
        mass_text = (
            "—" if mass_p is None
            else "/".join(f"{v:,.0f}" for v in mass_p) + " t"
        )
        if not s.feasible:
            lines.append(
                f"| {name} | infeasible | — | — | — | "
                f"{e.n_feasible}/{e.n_runs} | {mass_text} |"
            )
        else:
            lines.append(
                f"| {name} | {fmt(s.total_seed_mass_t)} t | "
                f"{fmt(s.import_stock_mass_t)} t | "
                f"{fmt_year(None if extended is None else extended.aggregate_doubling_year)} | "
                f"{fmt(None if r is None else r.operating_cells[-1], 2)} | "
                f"{e.n_feasible}/{e.n_runs} | {mass_text} |"
            )
    lines += [
        "",
        "The ensemble counts are occupancy under the declared log-uniform "
        "sampling measure. They are neither calibrated probabilities nor "
        "empirical success rates.",
        "",
        "The strict lunar-only case is a structural infeasibility inside the declared "
        "architecture: trace lunar yields cannot supply the configured "
        "electronics and process-equipment stack, in the central case and in every "
        "ensemble draw. It is not a proof that lunar-only "
        "closure is physically impossible; substitution, different recipes, new "
        "processes, or measured richer deposits could change the constraint graph.",
        "",
        "The Moon–asteroid case is likewise conditional. Its `diverse_asteroid_portfolio` "
        "is a deliberately composite source with ASSUMPTION-class recoverable yields. "
        "The model says what those yields would imply; it does not establish that a "
        "specific accessible portfolio has them.",
        "",
        "The aggregate material model is now paired with a process-closure "
        "acceptance contract covering typed source, species, process, part, "
        "parent-tool, transport, and waste nodes; grade progression; critical "
        "part ancestry; source/fleet evidence; and eight binary gates. Every "
        "gap-register row remains `evidence_pending`; no process-feasible "
        "closure is claimed. See "
        "`docs/PROCESS_CLOSURE_ACCEPTANCE_CONTRACT.md` and "
        "`tables/process_closure_gap_register.csv`.",
        "",
        "## What changed from the inherited model",
        "",
        f"- {params.n} sectors, including seven separate electronics tiers.",
        f"- {params.m} element/material categories with explicit bills of material.",
        "- Earth→Moon strategic-material import stock, asteroid→Moon feed, and "
        "Moon→orbit finished-compute arcs.",
        "- Task coverage, intervention demand, lunar-gravity process compatibility, and "
        "centrifuge mass/power overhead.",
        "- Construction lag, commissioning ramp, minimum viable scale, and an explicit "
        "aggregate operating-capacity doubling threshold.",
        "- All 18 sector capacities remain stateful through commissioning, "
        "cohort-resolved ramp, and depreciation; aggregate cell-equivalents are the slowest "
        "normalized operating sector, not the state.",
        "- A diagnostic allocator can build sectors independently, and the "
        "repair diagnostic consumes parts, repair service, intervention "
        "capacity, and queue time before returning failures to operation.",
        "- Delivered, staged, installed, commissioned, failed-startup, "
        "recovered, and operating seed states are explicit; delivered mass "
        "includes logistics hardware, packaging, spares, calibration, and "
        "startup-energy storage.",
        "- Coupled local compute, verified intelligence improvement, autonomy, and productivity.",
        "- Rate-limited Earth and Earth-fed orbital counterfactuals.",
        "- Active, derelict, and fragment stocks with a five-year fragment "
        "creation-to-clearance ratio.",
        "",
        "## Central process and seed diagnostics",
        "",
    ]
    for name in SCENARIOS:
        s = seeds[name]
        lines += [
            f"### {name}",
            "",
            f"- status: {s.status}",
            f"- minimum task coverage: {s.minimum_task_coverage:.3f}",
        ]
        if s.feasible:
            lines += [
                f"- residual intervention: {s.intervention_hours_per_year:,.1f} h/year",
                f"- lunar feed: {s.lunar_feed_t_per_year:,.1f} t/year",
                f"- asteroid feed: {s.asteroid_feed_t_per_year:,.1f} t/year",
                "- tight constraints: " + ", ".join(
                    f"`{label}` ({slack:+.2e})"
                    for label, slack in s.binding_constraints[:5]
                ),
            ]
        lines.append("")

    lines += [
        "## Delivered-to-operating seed stage (r4.0)",
        "",
        "The LP mass is an installed-seed quantity. The deployment diagnostic "
        "adds transport packaging, unloading and site equipment, calibration "
        "references, initial spares, and startup-energy storage, then moves "
        "the core seed through distinct states. Eight percent of newly "
        "commissioned core mass enters a declared startup-failure queue and "
        "must consume spares before it can operate. All deployment "
        "coefficients are explicit `ASSUMPTION`s with a bounding argument; "
        "they are not a mission estimate. Machine-readable: "
        "`tables/seed_deployment_trajectory.csv`.",
        "",
        "| scenario | installed seed | delivered seed | logistics increment | "
        "startup energy | first operation | full operating seed | recovered startup failures |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, d in deployments.items():
        lines.append(
            f"| {name} | {d.installed_seed_mass_t:.1f} t | "
            f"{d.delivered_seed_mass_t:.1f} t | {d.logistics_mass_t:.1f} t | "
            f"{d.startup_energy_mwh:.1f} MWh | "
            f"{fmt_year(d.first_operating_year)} | "
            f"{fmt_year(d.full_operating_seed_year)} | "
            f"{d.recovered_startup_failure_t:.1f} t |"
        )
    lines += [
        "",
        "## Compute regimes at year 40",
        "",
        "| regime | normalized capacity |",
        "|---|---:|",
        f"| off-world endogenous total | {compute.endogenous[-1]:.2f} |",
        f"| Moon→orbit endogenous export | {compute.endogenous_orbit[-1]:.2f} |",
    ]
    for label in ("tight", "base", "responsive"):
        lines.append(
            f"| Earth-fed orbit, {label} | {compute.earth_fed_orbit[label][-1]:.2f} |"
        )
    lines += [
        "",
        "The endogenous curve compounds only after the seed survives commissioning "
        "and source constraints. Earth-fed orbital capacity remains an affine "
        "deployment process and approaches a depreciation-limited stock at constant "
        "delivery. The terrestrial curves are rate-and-site-ceiling scenarios, not "
        "forecasts of actual buildout.",
        "",
        "## Debris condition",
        "",
        "| case | creation-to-clearance ratio, last 5 yr | clearance >= creation | fragment index, year 40 |",
        "|---|---:|:---:|---:|",
    ]
    for d in debris_runs:
        lines.append(
            f"| {d.label} | {d.creation_clearance_ratio:.2f} | "
            f"{'yes' if d.subcritical else 'no'} | {d.fragments[-1]:.3f} |"
        )
    lines += [
        "",
        "A dense shell is not licensed by industrial closure alone. In this scenario "
        "record, rapid endogenous deployment creates several times the fragments it "
        "clears under both weak and strong shell mitigation (the ratio is a flow "
        "ratio, not a branching-process reproduction number). The "
        "sparse/distributed topology sits at the "
        "boundary ratio only because its collision kernel is explicitly lower; "
        "that multiplier is an assumption to be replaced by shell- and trajectory-specific data.",
        "",
        "### Finite-mass, shell-resolved diagnostic",
        "",
        "A second diagnostic resolves 400-km LEO, 650-km LEO, and cislunar "
        "regions; active assets, intact derelicts, trackable fragments, and "
        "untrackable fragments; density/volume kernels; avoidance saturation; "
        "cross-shell fragment transport; disposal, natural clearance, "
        "retrieval, and active removal. Requested deployment consumes a finite "
        "feed inventory supplied by time-limited Earth import, depletion of a "
        "finite capture reservoir, and recovered retirements. Collision losses "
        "reduce returned active capacity and enter replacement/import cost.",
        "",
        "| shell | active capacity, year 40 | intact derelicts | trackable | "
        "untrackable | expected hazardous-descendant ratio |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for s, shell in enumerate(shell_debris.shells):
        lines.append(
            f"| {shell} | {shell_debris.active_capacity[-1, s]:.3f} | "
            f"{shell_debris.intact_derelicts[-1, s]:.3f} | "
            f"{shell_debris.trackable_fragments[-1, s]:.3f} | "
            f"{shell_debris.untrackable_fragments[-1, s]:.3f} | "
            f"{shell_debris.branching_ratio_by_shell[s]:.3f} |"
        )
    lines += [
        "",
        f"At year 40 the finite reservoir retains "
        f"{shell_debris.uncaptured_reservoir_t[-1]:.1f} t and feed inventory "
        f"retains {shell_debris.feed_inventory_t[-1]:.1f} t; cumulative "
        f"requested-deployment shortfall is "
        f"{shell_debris.deployment_shortfall_units.sum():.2f} normalized "
        f"units. Replacement/import cost under the declared delivered-mass "
        f"price is ${shell_debris.replacement_and_import_cost_usd / 1e6:.1f}M. "
        "The descendant ratio is a branching-style stress metric rather than "
        "the legacy creation/clearance flow ratio. Machine-readable: "
        "`tables/orbital_mass_balance.csv` and "
        "`tables/shell_debris_trajectory.csv`.",
        "",
        "## Governance threat/control traceability (r4.0)",
        "",
        "The governance model now names actors, assets, trust boundaries, "
        "normal/delayed/lost-link authority, eight threat paths, and nine "
        "controls with verification, rollback, and residual risk. Controls "
        "map to live build rate, sector floors, repair queues, source flows, "
        "commissioning cohorts, debris state, and independent inventory "
        "measurements. Every control remains `requirement_unvalidated`; this "
        "is not a solved safety case. See `docs/GOVERNANCE_THREAT_MODEL.md` "
        "and `tables/governance_threat_control_traceability.csv`.",
        "",
        "The linked Stage-0 protocol converts those controls into ten binary "
        "acceptance gates, a typed raw-event contract, a fault campaign that "
        "covers every registered threat plus communication loss, and explicit "
        "model-parameter replacement rules. Every checklist row is still "
        "`execution_pending` or `data_pending`: the protocol is executable, "
        "but no physical rehearsal result is claimed. See "
        "`docs/TERRESTRIAL_REHEARSAL_PROTOCOL.md` and "
        "`tables/rehearsal_acceptance_matrix.csv`.",
        "",
        "## Terminal-window operating-capacity endpoints (r4.0)",
        "",
        "Aggregate operating-capacity doubling is a threshold crossing of "
        "the slowest normalized sector; these endpoints separately report "
        "retention and final-five-year direction. The central 80-year "
        "extension is in `tables/long_horizon_endpoints.csv`; the complete "
        "sector trajectory is in `tables/sector_capacity_trajectory.csv`.",
        "",
        "| scenario | aggregate doubling | at year 40 | retained >= 2 | net final-5y | "
        "ensemble retained | ensemble terminal-window expanding |",
        "|---|---:|---:|:---:|---:|---:|---:|",
    ]
    for name, d in diags.items():
        e = endpoints.get(name)
        if e is None:
            lines.append(f"| {name} | — | — | — | — | 0/{d.n_runs} | 0/{d.n_runs} |")
        else:
            lines.append(
                f"| {name} | {fmt_year(e.aggregate_doubling_year)} | "
                f"{e.operating_at_horizon:.2f} | "
                f"{'yes' if e.retained_at_horizon else 'no'} | "
                f"{e.net_capacity_change_final5:+.3f} | "
                f"{d.n_retained}/{d.n_feasible} | "
                f"{d.n_terminal_window_expanding}/{d.n_feasible} |"
            )
    network_endpoint = endpoints["moon_asteroid_network"]
    lines += [
        "",
        "Reading: the terrestrial rehearsal and lunar strategic-material "
        "bridge never reach aggregate doubling in the 80-year extension and "
        "are contracting at year 40. The Moon–asteroid network is "
        f"terminal-window expanding, reaches "
        f"{network_endpoint.operating_at_horizon:.2f} equivalents at year 40, "
        f"and first crosses two at year "
        f"{network_endpoint.aggregate_doubling_year:.2f}. "
        "Import-pool "
        "exhaustion years are per-category first "
        "dips of the pooled inventory (initial Earth stock plus recycled "
        "returns and local production) and are reported in "
        "`tables/import_stock_composition.csv`; pools can refill later from "
        "local production, so a first dip is not permanent depletion.",
        "",
        "## Intelligence-coupling ablations (r4.0)",
        "",
        "Zero/freeze ablations of the declared coupling coefficients; the "
        "seed LP does not read the intelligence block, so dynamics variants "
        "share the central seed. Machine-readable: `tables/ablations.csv`.",
        "",
        "| scenario | variant | aggregate doubling | at year 40 | growth share of baseline |",
        "|---|---|---:|---:|---:|",
    ]
    for name, rows in ablations.items():
        for a in rows:
            lines.append(
                f"| {name} | {a.variant} | "
                f"{'—' if a.aggregate_doubling_year is None else f'{a.aggregate_doubling_year:.2f} yr'} | "
                f"{'infeasible' if not a.feasible else f'{a.operating_at_horizon:.2f}'} | "
                f"{'—' if a.growth_share_of_baseline is None else f'{a.growth_share_of_baseline:.0%}'} |"
            )
    lim_text = "; ".join(
        f"{name}: {lim}/{tot}" for name, (lim, tot) in limited.items()
    )
    regime_text = "; ".join(
        f"{name}: material {r.material_limited}, service {r.service_limited}, "
        f"order-cap {r.order_rate_limited}"
        for name, r in regimes.items()
    )
    network_ablation = {
        row.variant: row for row in ablations["moon_asteroid_network"]
    }
    network_baseline = network_ablation["baseline"]
    network_uncoupled = network_ablation["fully_uncoupled"]
    lines += [
        "",
        "Finding: sector resolution separates regimes that the former scalar "
        f"state conflated ({lim_text} steps material-limited). The terrestrial "
        "and lunar-bridge trajectories remain overwhelmingly material-limited, "
        "so coupling ablations move their year-40 endpoints by less than a "
        "tenth of one percent. In the Moon–asteroid network, however, the "
        f"fully uncoupled run reaches "
        f"{network_uncoupled.operating_at_horizon:.2f} sector-balanced "
        f"equivalents versus {network_baseline.operating_at_horizon:.2f} at "
        f"baseline, retaining about "
        f"{network_uncoupled.growth_share_of_baseline:.0%} of baseline net "
        "growth. The "
        "dynamic coupling is therefore operative only after the diverse "
        "source vector relaxes the material bottleneck. The declared starting "
        "AI level also remains load-bearing statically: sizing at base "
        "autonomy makes the bridge and network seeds infeasible.",
        "",
        "The exhaustive primary-constraint classification is "
        f"{regime_text} (160 quarterly steps each). Machine-readable: "
        "`tables/dynamic_regime_summary.csv`.",
        "",
        "## Knowledge and observable autonomy gates (r4.0)",
        "",
        "The 5 t knowledge package is now decomposed into storage/compute, "
        "software/toolchains, calibration references, laboratory equipment, "
        "consumables/recipes, and test articles. Each sector reports named-task "
        "completion, intervention demand, fault diagnosis, verification "
        "throughput, engineering-cycle time, process yield, repair success, "
        "mean time to recovery, and a non-divisible stop-line pass. These are "
        "ASSUMPTION-class diagnostic mappings pending Stage-0 measurements, "
        "not evidence that the capabilities exist. Machine-readable: "
        "`tables/knowledge_autonomy_observables.csv`.",
        "",
        "Two-year zero-capacity windows isolate the autonomy, verification, "
        "and compute regimes; a 90% advanced-logic/memory loss at year 5 "
        "isolates repair. The zero-capacity windows are adversarial boundary "
        "tests, not frequency estimates.",
        "",
        "| scenario | variant | at year 40 | doubling | material | autonomy | "
        "verification | repair | compute | service | order-cap |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, rows in knowledge_regimes.items():
        for r in rows:
            lines.append(
                f"| {name} | {r.variant} | {r.operating_at_horizon:.2f} | "
                f"{fmt_year(r.aggregate_doubling_year)} | "
                f"{r.material_steps} | {r.autonomy_steps} | "
                f"{r.verification_steps} | {r.repair_steps} | "
                f"{r.compute_steps} | {r.service_steps} | "
                f"{r.order_rate_steps} |"
            )
    lines += [
        "",
        "The declared central cases remain material/order-cap limited. The "
        "adversarial windows create the named regimes mechanically and reduce "
        "the Moon–asteroid endpoint; this demonstrates classification and "
        "falsification plumbing, not calibrated outage risk. Machine-readable: "
        "`tables/knowledge_regime_summary.csv`.",
        "",
        "## Operating-environment/process coupling (r4.0)",
        "",
        "The central release remains on the identity `centrifuge_only` profile "
        "for continuity. Separate nominal and adverse lunar profiles apply "
        "process-specific throughput, quality-yield, power-demand, and "
        "depreciation multipliers for dust, traction, reduced convection, "
        "vacuum behavior, radiation, thermal cycling, contamination, and "
        "calibration drift. Every multiplier is an explicit bounding "
        "`ASSUMPTION`; Earth rehearsal results do not transfer to these "
        "profiles automatically.",
        "",
        "| scenario | environment | feasible | seed mass | top binding row | "
        "at year 40 | doubling | survived |",
        "|---|---|:---:|---:|---|---:|---:|:---:|",
    ]
    for name, rows in environment_effects.items():
        for r in rows:
            lines.append(
                f"| {name} | {r.environment_profile} | "
                f"{'yes' if r.feasible else 'no'} | "
                f"{fmt(r.seed_mass_t)} t | "
                f"{r.top_binding_constraint or '—'} | "
                f"{fmt(r.operating_at_horizon, 2)} | "
                f"{fmt_year(r.aggregate_doubling_year)} | "
                f"{'—' if r.survived is None else ('yes' if r.survived else 'no')} |"
            )
    lines += [
        "",
        "The nominal/adverse penalties change seed mass and binding rows; the "
        "adverse lunar bridge becomes LP-infeasible. Some feasible penalized "
        "profiles can improve the year-40 trajectory because the minimum-mass "
        "LP responds by installing more initial capacity. That is an objective "
        "frontier artifact, not evidence that a harsher environment helps. "
        "Machine-readable: `tables/environment_process_effects.csv`.",
        "",
        "## Policy and structural-uncertainty robustness (r4.0)",
        "",
        "A one-factor-at-a-time sweep varies advanced-logic knockout fraction, "
        "event time, horizon, retained initial import stock, initial surplus, "
        "and obsolescence/depreciation. It compares balanced, live maximin, "
        "20%-reserve surplus-preserving, generic shock-aware, and exact "
        "perfect-foresight policies. Counts below are design-case occupancy "
        "over the enumerated deterministic cases, not probabilities.",
        "",
        "| scenario | policy | cases | survived | survived + terminally expanding |",
        "|---|---|---:|---:|---:|",
    ]
    for name, rows in policy_robustness.items():
        for policy in (
            "balanced",
            "maximin_sector",
            "surplus_preserving",
            "shock_aware",
            "perfect_foresight",
        ):
            selected = [r for r in rows if r.policy == policy]
            survived_count = sum(r.survived for r in selected)
            robust_count = sum(
                r.survived and r.terminal_window_expanding
                for r in selected
            )
            lines.append(
                f"| {name} | {policy} | {len(selected)} | "
                f"{survived_count} | {robust_count} |"
            )
    lines += [
        "",
        "The machine-readable sweep reports minimum live sector margin and "
        "first aggregate doubling for every case, making failure boundaries "
        "inspectable rather than reducing them to one rank correlation. "
        "`tables/policy_robustness_sweep.csv` is authoritative.",
        "",
        "## Tiered electronics closure and inventory life (r4.0)",
        "",
        "The integrated layer no longer uses the inherited scalar electronics "
        "productivity range in its headline analysis. Seven tiers now carry "
        "separate local-producibility, replacement, shelf-life, obsolescence, "
        "and substitution assumptions. Imported tier inventory decays before "
        "use, and the architecture comparison includes frontier-local, "
        "permanent-import, mature/repairable, and cannibalization-based cases.",
        "",
        "| scenario | architecture | viable tiers | total tier shortfall | "
        "gross permanent-import mass | first shortfall |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for name, rows in electronics_architectures.items():
        for architecture in params.raw["electronics_closure"]["architectures"]:
            selected = [
                r for r in rows if r.architecture == architecture
            ]
            first = [
                r.first_shortfall_year
                for r in selected
                if r.first_shortfall_year is not None
            ]
            lines.append(
                f"| {name} | {architecture} | "
                f"{sum(r.viable for r in selected)}/{len(selected)} | "
                f"{sum(r.shortfall_capacity for r in selected):.3f} | "
                f"{sum(r.imported_mass_t for r in selected):.1f} t | "
                f"{fmt_year(min(first) if first else None)} |"
            )
    lines += [
        "",
        "Every tested architecture still develops a shortfall in advanced "
        "logic/memory or process-equipment/metrology under the expanding "
        "Moon–asteroid demand path; fixed imports proportional to the initial "
        "seed do not scale with endogenous demand. The most decision-reducing "
        "measurements are therefore demonstrated mature-node wafer yield and "
        "parent-tool/calibration replacement demand, followed by useful life "
        "and permanent-import mass per service-year. The strict-lunar minimum "
        "cut remains tiered in the seed LP and is not erased by these dynamic "
        "inventory cases. Machine-readable: "
        "`tables/electronics_architecture_comparison.csv`.",
        "",
        "The empirical-calibration contract separates the Earth reference, "
        "serviceable space platform, and integrated disposable cases; requires "
        "equal-workload records; binds six evidence packages to current model "
        "parameters; preserves correlated reliability, link, thermal, Earth-"
        "resource, demand, and financing uncertainty; and defines an audited "
        "cash-flow event ledger with chronological holdout validation. All "
        "readiness rows remain `data_pending`. See "
        "`docs/ECONOMIC_CALIBRATION_PROTOCOL.md` and "
        "`tables/economic_calibration_readiness.csv`.",
        "",
        "The publication contract names target and fallback venues for all "
        "three papers and measures each draft against current publisher "
        "requirements. Machine-checkable structure now passes where supplied, "
        "while references, fallback word-count expansion, live-portal fields, "
        "and every author-controlled declaration remain explicitly pending. "
        "See `docs/VENUE_SELECTION_AND_CONFORMANCE.md` and "
        "`tables/publication_readiness.csv`.",
        "",
        "## Symmetric dynamic economics (r4.0)",
        "",
        "Earth and space now use the same reinvestment/debt logic: endogenous "
        "investment, learning, depreciation/obsolescence, regulatory build "
        "queues, debt-to-revenue limits, interest, bridge financing, market "
        "demand, and expanding resource ceilings. Space is additionally capped "
        "by the physical model and pays for its funded share of industrial "
        "orders, source transfer, and intervention. The coefficients are "
        "ASSUMPTION-class scenario mechanics, not a valuation.",
        "",
        "| market | technical space at year 40 | funded space | Earth | "
        "space finance-limited steps | Earth finance-limited steps | "
        "space self-financing | Earth self-financing |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for market, r in economics.items():
        lines.append(
            f"| {market} | {r.technical_space_capacity[-1]:.2f} | "
            f"{r.funded_space_capacity[-1]:.2f} | "
            f"{r.earth_capacity[-1]:.2f} | "
            f"{r.space_finance_constrained_steps} | "
            f"{r.earth_finance_constrained_steps} | "
            f"{fmt_year(r.space_self_financing_year)} | "
            f"{fmt_year(r.earth_self_financing_year)} |"
        )
    lines += [
        "",
        "Physical compounding does not automatically fund deployment. In the "
        "commodity case, finance activates only a small fraction of technically "
        "available space capacity while Earth expands endogenously. A "
        "space-native price premium funds more of the physical path, but the "
        "space case still does not repay its declared external capital inside "
        "40 years. P3b therefore remains a conditional economic proposition, "
        "not a consequence of the physical growth curve. Machine-readable: "
        "`tables/symmetric_dynamic_economics.csv`.",
        "",
        "## Composition-changing robust-seed Pareto search (r4.0)",
        "",
        "The design search now changes process route, sector redundancy, and "
        "lunar/asteroid source allocation instead of merely relabeling one LP "
        "objective or scaling a fixed vector. It minimizes delivered mass, "
        "Earth import, intervention, and doubling time while maximizing "
        "year-40 capacity and capacity after a five-year asteroid-source "
        "outage. Dominance is computed across all six objectives.",
        "",
        "| route | redundancy | source portfolio | delivered mass | doubling | "
        "year 40 | after outage | Pareto | robust |",
        "|---|---|---|---:|---:|---:|---:|:---:|:---:|",
    ]
    for r in pareto_designs:
        if not r.non_dominated:
            continue
        lines.append(
            f"| {r.route} | {r.redundancy} | {r.source_portfolio} | "
            f"{r.delivered_mass_t:.1f} t | "
            f"{fmt_year(r.aggregate_doubling_year)} | "
            f"{r.operating_at_horizon:.2f} | "
            f"{r.source_outage_operating_at_horizon:.2f} | yes | "
            f"{'yes' if r.robust_candidate else 'no'} |"
        )
    robust = [r for r in pareto_designs if r.robust_candidate]
    minimum_robust = min(robust, key=lambda r: r.delivered_mass_t)
    lines += [
        "",
        f"The minimum delivered-mass robust candidate in this enumerated "
        f"design space is `{minimum_robust.route}` / "
        f"`{minimum_robust.redundancy}` / "
        f"`{minimum_robust.source_portfolio}` at "
        f"{minimum_robust.delivered_mass_t:.1f} t. This is an "
        "ASSUMPTION-conditioned discrete frontier, not a globally optimal "
        "mission design. Machine-readable dominated and non-dominated points: "
        "`tables/robust_seed_pareto.csv`.",
        "",
        "## Allocation, repair, and shock-policy comparison (r4.0)",
        "",
        "The published central case retains balanced build packets for "
        "continuity. The structural diagnostic below instead maximizes the "
        "weakest live sector margin, then minimizes installed mass at that "
        "margin. Repair uses the declared ASSUMPTION-class parts, service, "
        "intervention, and lag coefficients. The shock removes 50% of the "
        "advanced-logic/memory sector at year 20; it is a deterministic "
        "stress case, not a frequency estimate. Machine-readable: "
        "`tables/allocation_repair_comparison.csv`.",
        "",
        "| scenario | policy | repair | shock | doubling | at year 40 | "
        "minimum sector margin | survived | shock recovery |",
        "|---|---|:---:|---|---:|---:|---:|:---:|---:|",
    ]
    for name, rows in allocation_repair.items():
        for r in rows:
            lines.append(
                f"| {name} | {r.policy} | "
                f"{'yes' if r.repair_enabled else 'no'} | {r.shock} | "
                f"{fmt_year(r.aggregate_doubling_year)} | "
                f"{r.operating_at_horizon:.2f} | "
                f"{r.minimum_sector_margin_at_horizon:.2f} | "
                f"{'yes' if r.survived else 'no'} | "
                f"{fmt_year(r.shock_recovery_year)} |"
            )
    lines += [
        "",
        "These policy outcomes are not new feasibility claims: the allocator "
        "and repair coefficients expose how strongly the result depends on "
        "construction policy and recoverability. They replace the earlier "
        "implicit claim that only balanced copies can be ordered.",
        "",
        "## Installed-mass versus aggregate-doubling frontier (r4.0)",
        "",
        "A factor-f seed installs f cell-equivalents of the minimum-mass "
        "design (capacities, feeds, strategic import stock scale with f; "
        "the digital package is shared). Time is first passage to one *additional* "
        "operating cell-equivalent, so f = 1 coincides with the canonical "
        "metric. The oversize factor is a sweep axis, not a new assumption. "
        "Machine-readable: `tables/oversize_frontier.csv`; figure: "
        "`figures/oversize_frontier.png`.",
        "",
        "| scenario | factor | installed mass | time to +1 cell | additional cells at year 40 |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, rows in frontiers.items():
        for r in rows:
            lines.append(
                f"| {name} | ×{r.oversize_factor:g} | "
                f"{r.installed_mass_t:,.1f} t | "
                f"{'—' if r.time_to_one_additional_cell is None else f'{r.time_to_one_additional_cell:.2f} yr'} | "
                f"{r.additional_cells_at_horizon:+.2f} |"
            )
    lines += [
        "",
        "The sector-resolved frontier reverses the earlier scalar-state "
        "reading. Neither the terrestrial nor lunar bridge design reaches "
        "one additional balanced cell-equivalent at any tested scale by "
        "year 40. The Moon–asteroid minimum-mass design also misses that "
        "threshold, while 1.25x, 1.5x, and 2x scaled designs reach it at "
        "39.25, 38.5, and 37.25 years. Scaling one fixed composition is "
        "still not a "
        "multi-objective redesign.",
        "",
        "## Alternative seed objectives (r4.0)",
        "",
        "The same seed LP was solved lexicographically for minimum installed "
        "mass, minimum Earth-import mass, and minimum annual intervention, "
        "with installed mass as the secondary tie-break for the latter two. "
        "Machine-readable: `tables/seed_objective_comparison.csv`.",
        "",
        "| scenario | objective | installed mass | import mass | intervention | "
        "capacity-vector distance from mass optimum |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for name, by_objective in objective_seeds.items():
        baseline = by_objective["installed_mass"]
        for objective in SEED_OBJECTIVES:
            seed = by_objective[objective]
            if not seed.feasible:
                lines.append(
                    f"| {name} | {objective} | infeasible | — | — | — |"
                )
                continue
            distance = float(np.abs(
                seed.capacities - baseline.capacities
            ).sum())
            lines.append(
                f"| {name} | {objective} | {seed.total_seed_mass_t:.1f} t | "
                f"{seed.import_stock_mass_t:.1f} t | "
                f"{seed.intervention_hours_per_year:.1f} h/yr | "
                f"{distance:.3g} |"
            )
    lines += [
        "",
        "All three objectives return the identical central design in every "
        "LP-feasible scenario. This is a negative structural result: the "
        "current variables and constraints do not expose a mass/import/"
        "intervention tradeoff for the optimizer to choose. A genuine Pareto "
        "front requires alternative process routes, sector composition, "
        "redundancy, or deployment decisions; relabeling the objective alone "
        "cannot create it.",
        "",
        "## Ensemble diagnostics (r4.0)",
        "",
        "Per-draw failure reasons, top binding constraints among feasible "
        "draws, and Spearman rank sensitivity of the named multipliers "
        "(machine-readable: `tables/diagnostics_histograms.csv`, "
        "`tables/ensemble_sensitivity.csv`):",
        "",
    ]
    for name, d in diags.items():
        fh = ", ".join(f"{k} {v}" for k, v in
                       sorted(d.failure_histogram.items(), key=lambda kv: -kv[1]))
        bh = ", ".join(f"{k} {v}" for k, v in
                       sorted(d.binding_histogram.items(), key=lambda kv: -kv[1])[:4])
        lines.append(f"- **{name}**: failures — {fh or 'none'}; "
                     f"top binding — {bh or 'n/a'}.")
    lines += [
        "",
        "These are rank screens inside the declared independent multiplier "
        "measure, not causal effects or global sensitivity. Sector resolution "
        "changes both signs and magnitudes relative to the scalar-state run; "
        "the machine-readable table is authoritative and no previous "
        "depreciation-direction claim is carried forward.",
        "",
        "## Strict-lunar infeasibility certificate (r4.0)",
        "",
        "Elastic relaxation of the exact seed LP (every row receives a "
        "nonnegative slack; the slack sum is minimized in row-native "
        "units). This is a minimum total-violation certificate, not a "
        "strict irreducible infeasible subsystem. Machine-readable: "
        "`tables/infeasibility_certificate.csv`.",
        "",
    ]
    for name, rows in certs.items():
        if not rows:
            continue
        lines.append(f"**{name}** — unsatisfiable requirement rows "
                     "(minimum shortfall over the horizon):")
        lines.append("")
        lines.append("| constraint | minimum shortfall | units |")
        lines.append("|---|---:|---|")
        for r in rows:
            lines.append(f"| {r.constraint} | {r.minimum_violation:,.2f} | {r.units} |")
        lines.append("")
    lines += [
        "The strict-lunar cut is material, category-specific, and "
        "quantified: the configured lunar yields cannot supply the Ni, Cu, "
        "C, Co, Cr, rare-earth, Li, and H demands of the declared "
        "electronics and process-equipment stack within the horizon's "
        "throughput and energy limits. Substituting recipes, richer "
        "measured deposits, or a different electronics architecture would "
        "change this table, which is exactly what makes it a useful "
        "engineering target list.",
        "",
        "## Reproducibility",
        "",
        "```bash",
        "python scripts/run_integrated.py",
        "pytest tests/test_integrated.py tests/test_integrated_analysis.py -q",
        "```",
        "",
        "Every generated table is derived from the same in-memory run. "
        "`outputs/integrated/MANIFEST.md` hashes the parameter file, implementation, "
        "runner, report, tables, and figures.",
    ]
    path = OUT / "report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_manifest(files: list[Path]) -> Path:
    lines = [
        "# Current artifact manifest",
        "",
        "- generated: 2026-07-28",
        f"- python: {platform.python_version()}",
        f"- numpy: {np.__version__}",
        f"- scipy: {scipy.__version__}",
        f"- PyYAML: {yaml.__version__}",
        "- generator: `scripts/run_integrated.py`",
        "",
        "| artifact/input | sha256 |",
        "|---|---|",
    ]
    for path in sorted(set(files), key=lambda p: str(p)):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"| `{path.relative_to(ROOT)}` | `{digest}` |")
    manifest = OUT / "MANIFEST.md"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)

    params = load_integrated_params()
    seeds = {name: size_seed(params, name) for name in SCENARIOS}
    runs = {
        name: simulate_capacity_growth(params, seed, years=40.0, dt=0.25)
        for name, seed in seeds.items() if seed.feasible
    }
    extended_runs = {
        name: simulate_capacity_growth(params, seed, years=80.0, dt=0.25)
        for name, seed in seeds.items() if seed.feasible
    }
    objective_seeds = {
        name: {
            objective: size_seed(params, name, objective=objective)
            for objective in SEED_OBJECTIVES
        }
        for name in SCENARIOS
    }
    deployments = {
        name: simulate_seed_deployment(params, seed)
        for name, seed in seeds.items() if seed.feasible
    }
    ensembles = {
        name: seed_ensemble(
            params, name, n_runs=N_ENSEMBLE, seed=ENSEMBLE_SEED,
            years=40.0, dt=0.5,
        )
        for name in SCENARIOS
    }
    network_run = runs["moon_asteroid_network"]
    compute = compare_compute_regimes(params, network_run)
    debris_runs = [
        simulate_debris(
            params, compute.earth_fed_orbit["base"], compute.t,
            "weak_mitigation", label="Earth-fed orbit / weak mitigation",
        ),
        simulate_debris(
            params, compute.earth_fed_orbit["base"], compute.t,
            "strong_mitigation", label="Earth-fed orbit / strong mitigation",
        ),
        simulate_debris(
            params, compute.endogenous, compute.t,
            "weak_mitigation", label="dense endogenous / weak mitigation",
        ),
        simulate_debris(
            params, compute.endogenous, compute.t,
            "strong_mitigation", label="dense endogenous / strong mitigation",
        ),
        simulate_debris(
            params, compute.endogenous_orbit, compute.t,
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
    import_stocks = {
        n: import_stock_composition(params, seeds[n], runs[n]) for n in runs
    }
    ablations = {n: ablation_suite(params, n)
                 for n in SCENARIOS if seeds[n].feasible}
    frontiers = {n: oversize_frontier(params, n)
                 for n in SCENARIOS if seeds[n].feasible}
    diags = {n: ensemble_diagnostics(params, n, n_runs=N_ENSEMBLE,
                                     seed=ENSEMBLE_SEED, years=40.0, dt=0.5)
             for n in SCENARIOS}
    certs = {n: infeasibility_certificate(params, n)
             for n in SCENARIOS if not seeds[n].feasible}
    limited = {n: material_limited_steps(params, seeds[n], runs[n])
               for n in runs}
    regimes = {
        n: capacity_regime_summary(params, seeds[n], runs[n])
        for n in runs
    }
    allocation_repair = {
        n: allocation_repair_suite(params, n)
        for n in SCENARIOS if seeds[n].feasible
    }
    knowledge_regimes = {
        n: knowledge_regime_suite(params, n)
        for n in SCENARIOS if seeds[n].feasible
    }
    environment_effects = {
        n: environment_effect_suite(params, n)
        for n in SCENARIOS
    }
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
        for market in params.raw["dynamic_economics"]["markets"]
    }
    pareto_designs = pareto_seed_designs(params)

    write_scenario_tables(params, seeds, runs, ensembles)
    write_compute_and_debris_tables(compute, debris_runs)
    write_shell_debris_tables(shell_debris)
    governance_table = write_governance_traceability()
    rehearsal_table = write_rehearsal_acceptance_csv(
        TAB / "rehearsal_acceptance_matrix.csv"
    )
    economic_calibration_table = write_economic_calibration_csv(
        TAB / "economic_calibration_readiness.csv"
    )
    process_closure_table = write_process_closure_gap_csv(
        TAB / "process_closure_gap_register.csv"
    )
    publication_table = write_publication_readiness_csv(
        TAB / "publication_readiness.csv"
    )
    write_long_horizon_table(params, seeds, extended_runs)
    write_seed_objective_table(params, objective_seeds)
    write_deployment_table(deployments)
    write_analysis_tables(
        params, seeds, endpoints, import_stocks, ablations, frontiers,
        allocation_repair, knowledge_regimes, environment_effects,
        policy_robustness, electronics_architectures, economics,
        pareto_designs, regimes, diags,
        certs
    )
    generate_figures(params, seeds, runs, ensembles, compute, debris_runs)
    generate_analysis_figures(frontiers)
    report = write_report(
        params, seeds, runs, extended_runs, objective_seeds, deployments, ensembles,
        compute, debris_runs, shell_debris, endpoints, import_stocks, ablations,
        frontiers, diags, certs, limited, regimes, allocation_repair,
        knowledge_regimes, environment_effects,
        policy_robustness, electronics_architectures, economics,
        pareto_designs,
    )

    inputs = [
        ROOT / "params" / "integrated_model.yaml",
        ROOT / "params" / "claim_glossary.yaml",
        ROOT / "params" / "governance_controls.yaml",
        ROOT / "params" / "rehearsal_protocol.yaml",
        ROOT / "params" / "economic_calibration.yaml",
        ROOT / "params" / "process_closure_requirements.yaml",
        ROOT / "params" / "publication_targets.yaml",
        ROOT / "src" / "rsimodel" / "integrated.py",
        ROOT / "src" / "rsimodel" / "integrated_analysis.py",
        ROOT / "src" / "rsimodel" / "rehearsal.py",
        ROOT / "src" / "rsimodel" / "economic_calibration.py",
        ROOT / "src" / "rsimodel" / "process_closure.py",
        ROOT / "src" / "rsimodel" / "manifests.py",
        ROOT / "src" / "rsimodel" / "publication.py",
        ROOT / "src" / "rsimodel" / "release.py",
        ROOT / "src" / "rsimodel" / "evidence.py",
        ROOT / "scripts" / "run_integrated.py",
        ROOT / "scripts" / "verify_manifests.py",
        ROOT / "scripts" / "release_preflight.py",
        ROOT / "scripts" / "publication_preflight.py",
        ROOT / "scripts" / "evaluate_evidence_bundle.py",
        ROOT / "tests" / "test_integrated.py",
        ROOT / "tests" / "test_integrated_analysis.py",
        ROOT / "tests" / "test_rehearsal.py",
        ROOT / "tests" / "test_economic_calibration.py",
        ROOT / "tests" / "test_process_closure.py",
        ROOT / "tests" / "test_manifests.py",
        ROOT / "tests" / "test_publication.py",
        ROOT / "tests" / "test_release.py",
        ROOT / "tests" / "test_evidence_bundles.py",
        ROOT / "docs" / "GOVERNANCE_THREAT_MODEL.md",
        ROOT / "docs" / "TERRESTRIAL_REHEARSAL_PROTOCOL.md",
        ROOT / "docs" / "ECONOMIC_CALIBRATION_PROTOCOL.md",
        ROOT / "docs" / "PROCESS_CLOSURE_ACCEPTANCE_CONTRACT.md",
        ROOT / "docs" / "VENUE_SELECTION_AND_CONFORMANCE.md",
        ROOT / "docs" / "RELEASE_RUNBOOK.md",
        ROOT / "papers" / "README.md",
        ROOT / "papers" / "TECHNICAL_PAPER_r4.0.md",
        ROOT / "papers" / "ORBITAL_COMPUTE_ECONOMICS_r4.0.md",
        ROOT / "papers" / "STRATEGY_GOVERNANCE_CASE_STUDY_r4.0.md",
        ROOT / "papers" / "TECHNICAL_SUPPLEMENT_r4.0.md",
    ]
    artifacts = [report, *TAB.glob("*.csv"), *FIG.glob("*.png")]
    manifest = write_manifest(inputs + artifacts)

    summary = {
        name: {
            "feasible": seeds[name].feasible,
            "seed_mass_t": seeds[name].total_seed_mass_t,
            "aggregate_doubling_year": (
                runs[name].aggregate_doubling_year if name in runs else None
            ),
            "ensemble_feasible": f"{ensembles[name].n_feasible}/{N_ENSEMBLE}",
        }
        for name in SCENARIOS
    }
    print(json.dumps(summary, indent=2))
    print(report.relative_to(ROOT))
    print(manifest.relative_to(ROOT))


if __name__ == "__main__":
    main()
