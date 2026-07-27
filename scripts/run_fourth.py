"""Generate the Fourth Edition integrated-bootstrap artifact set.

All outputs are written beneath ``outputs/fourth/`` so the frozen r3.5
reports and manifest are not modified.  The run is deterministic:
assumption-ensemble cells use name-keyed crc32 seeds in
``rsimodel.fourth.sample_fourth_params``.
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

from rsimodel.fourth import (
    compare_compute_regimes,
    load_fourth_params,
    seed_ensemble,
    simulate_debris,
    simulate_reproduction,
    size_seed,
)
from rsimodel.fourth_analysis import (
    ablation_suite,
    durable_endpoints,
    ensemble_diagnostics,
    infeasibility_certificate,
    material_limited_steps,
    oversize_frontier,
    vitamin_composition,
)

OUT = ROOT / "outputs" / "fourth"
FIG = OUT / "figures"
TAB = OUT / "tables"
SCENARIOS = (
    "terrestrial_rehearsal",
    "lunar_vitamin_bridge",
    "lunar_strict",
    "moon_asteroid_network",
)
N_ENSEMBLE = 200
ENSEMBLE_SEED = 404


def fmt(value: float | None, digits: int = 1) -> str:
    return "infeasible" if value is None else f"{value:,.{digits}f}"


def pct(values: tuple[float, ...]) -> tuple[float, float, float] | None:
    if not values:
        return None
    return tuple(float(v) for v in np.percentile(values, [10, 50, 90]))


def write_scenario_tables(params, seeds, runs, ensembles) -> None:
    with open(TAB / "scenario_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "feasible", "status", "seed_mass_t", "physical_seed_mass_t",
            "vitamin_stock_mass_t", "digital_seed_mass_t", "lunar_feed_t_per_year",
            "asteroid_feed_t_per_year", "minimum_task_coverage",
            "intervention_hours_per_year", "second_cell_year",
            "operating_cells_year40", "intelligence_year40", "survived",
        ])
        for name in SCENARIOS:
            s = seeds[name]
            r = runs.get(name)
            w.writerow([
                name, int(s.feasible), s.status,
                "" if s.total_seed_mass_t is None else f"{s.total_seed_mass_t:.8f}",
                "" if s.physical_seed_mass_t is None else f"{s.physical_seed_mass_t:.8f}",
                "" if s.vitamin_stock_mass_t is None else f"{s.vitamin_stock_mass_t:.8f}",
                f"{s.digital_seed_mass_t:.8f}",
                f"{s.lunar_feed_t_per_year:.8f}", f"{s.asteroid_feed_t_per_year:.8f}",
                f"{s.minimum_task_coverage:.8f}",
                f"{s.intervention_hours_per_year:.8f}",
                "" if r is None or r.second_cell_year is None else f"{r.second_cell_year:.8f}",
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
                    f"{s.vitamin_stock_t[e]:.9f}",
                    f"{params.lunar_yield[e] * s.lunar_feed_t_per_year:.9f}",
                    f"{params.asteroid_yield[e] * s.asteroid_feed_t_per_year:.9f}",
                ])

    with open(TAB / "ensemble_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "n_runs", "n_feasible", "feasible_share",
            "n_survived", "survived_share", "seed_p10_t", "seed_p50_t",
            "seed_p90_t", "second_cell_p10_year", "second_cell_p50_year",
            "second_cell_p90_year",
        ])
        for name in SCENARIOS:
            e = ensembles[name]
            sm, sy = pct(e.seed_masses_t), pct(e.second_cell_years)
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
    ax.set_title("Fourth Edition seed-sizing assumption ensembles")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "seed_mass_ensemble.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    for name, run in runs.items():
        ax.plot(run.t, run.operating_cells, label=name.replace("_", " "))
    ax.axhline(2.0, color="#333333", ls="--", lw=1, label="commissioned second cell")
    ax.set_xlabel("Years after seed activation")
    ax.set_ylabel("Operating production-cell equivalents")
    ax.set_yscale("log")
    ax.set_ylim(0.5, max(20.0, max(r.operating_cells[-1] for r in runs.values()) * 1.2))
    ax.set_title("Commissioning lags separate ordering from operating capacity")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "cell_reproduction.png", dpi=180)
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
    ax.set_title("Rate-limited deployment versus endogenous reproduction")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "compute_growth_regimes.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    for d in debris_runs:
        ax.plot(d.t, d.fragments, label=f"{d.label} · R={d.reproduction_ratio:.2f}")
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
            "case", "reproduction_ratio_last5y", "subcritical",
            "active_year40", "derelict_year40", "fragment_index_year40",
        ])
        for d in debris_runs:
            w.writerow([
                d.label, f"{d.reproduction_ratio:.9f}", int(d.subcritical),
                f"{d.active[-1]:.9f}", f"{d.derelict[-1]:.9f}",
                f"{d.fragments[-1]:.9f}",
            ])


def write_analysis_tables(endpoints, vitamins, ablations, frontiers,
                          diags, certs) -> None:
    with open(TAB / "durable_endpoints.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "first_passage_year", "operating_at_horizon",
            "retained_at_horizon", "net_reproduction_final5y",
            "durable_final5y", "vitamin_pools_exhausted_year",
            "ensemble_n_feasible", "ensemble_n_retained",
            "ensemble_n_durable_final5y",
        ])
        for name, d in diags.items():
            e = endpoints.get(name)
            w.writerow([
                name,
                "" if e is None or e.first_passage_year is None
                else f"{e.first_passage_year:.6f}",
                "" if e is None else f"{e.operating_at_horizon:.6f}",
                "" if e is None else int(e.retained_at_horizon),
                "" if e is None else f"{e.net_reproduction_final5:.6f}",
                "" if e is None else int(e.durable_final5),
                "" if e is None or e.vitamin_pools_exhausted_year is None
                else f"{e.vitamin_pools_exhausted_year:.6f}",
                d.n_feasible, d.n_retained, d.n_durable_final5,
            ])

    with open(TAB / "vitamin_composition.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "element", "initial_stock_t",
            "share_of_vitamin_stock", "initial_rate_coverage_years",
            "pool_min_t", "pool_at_first_passage_t", "pool_at_horizon_t",
            "pool_first_exhaustion_year",
        ])
        for name, rows in vitamins.items():
            for r in rows:
                w.writerow([
                    name, r.element, f"{r.initial_stock_t:.6f}",
                    f"{r.share_of_vitamin_stock:.6f}",
                    "" if r.initial_rate_coverage_years is None
                    else f"{r.initial_rate_coverage_years:.4f}",
                    f"{r.pool_min_t:.6f}",
                    "" if r.pool_at_first_passage_t is None
                    else f"{r.pool_at_first_passage_t:.6f}",
                    f"{r.pool_at_horizon_t:.6f}",
                    "" if r.pool_exhaustion_year is None
                    else f"{r.pool_exhaustion_year:.4f}",
                ])

    with open(TAB / "ablations.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([
            "scenario", "variant", "definition", "feasible",
            "first_passage_year", "operating_at_horizon",
            "growth_share_of_baseline",
        ])
        for name, rows in ablations.items():
            for a in rows:
                w.writerow([
                    name, a.variant, a.definition, int(a.feasible),
                    "" if a.first_passage_year is None
                    else f"{a.first_passage_year:.6f}",
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
            "rho_first_passage_year", "rho_operating_at_horizon",
        ])
        for name, d in diags.items():
            if d.n_feasible < 8:
                continue
            for mult, s in d.sensitivity.items():
                w.writerow([
                    name, mult,
                    f"{s['seed_mass_t']:.4f}",
                    f"{s['first_passage_year']:.4f}",
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
    ax.set_title("Oversize frontier: installed mass versus reproduction time")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "oversize_frontier.png", dpi=180)
    plt.close(fig)


def write_report(params, seeds, runs, ensembles, compute, debris_runs,
                 endpoints, vitamins, ablations, frontiers, diags,
                 certs, limited) -> Path:
    lines = [
        "# Fourth Edition integrated-bootstrap model",
        "",
        f"- model version: `{params.version}`",
        f"- assumption ensemble: n={N_ENSEMBLE} per scenario, seed={ENSEMBLE_SEED}",
        "- epistemic status: scenario implications, not measurements or forecasts",
        "",
        "## Headline results",
        "",
        "| scenario | central installed seed mass | Earth vitamin stock | "
        "first passage to two cell-equivalents | "
        "cell-equivalents at year 40 | model-feasible draws | ensemble seed p10/p50/p90 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in SCENARIOS:
        s, e = seeds[name], ensembles[name]
        r = runs.get(name)
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
                f"{fmt(s.vitamin_stock_mass_t)} t | "
                f"{fmt(None if r is None else r.second_cell_year)} yr | "
                f"{fmt(None if r is None else r.operating_cells[-1], 2)} | "
                f"{e.n_feasible}/{e.n_runs} | {mass_text} |"
            )
    lines += [
        "",
        "The strict lunar-only case is a structural infeasibility inside the declared "
        "architecture: trace lunar yields cannot reproduce the configured "
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
        "## What changed from the inherited model",
        "",
        f"- {params.n} sectors, including seven separate electronics tiers.",
        f"- {params.m} element/material categories with explicit bills of material.",
        "- Earth→Moon vitamin stock, asteroid→Moon feed, and Moon→orbit finished-compute arcs.",
        "- Task coverage, intervention demand, lunar-gravity process compatibility, and "
        "centrifuge mass/power overhead.",
        "- Construction lag, commissioning ramp, minimum viable scale, and an explicit "
        "second operating production cell.",
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
            f"| {d.label} | {d.reproduction_ratio:.2f} | "
            f"{'yes' if d.subcritical else 'no'} | {d.fragments[-1]:.3f} |"
        )
    lines += [
        "",
        "A dense shell is not licensed by industrial closure alone. In this scenario "
        "record, rapid endogenous deployment creates several times the fragments it "
        "clears under both weak and strong shell mitigation (the ratio is a flow "
        "ratio, not a branching-process reproduction number, and is not monotonic "
        "in mitigation strength). The sparse/distributed topology sits at the "
        "boundary ratio only because its collision kernel is explicitly lower; "
        "that multiplier is an assumption to be replaced by shell- and trajectory-specific data.",
        "",
        "## Durable reproduction endpoints (r4.1)",
        "",
        "First passage to two cell-equivalents is a reproduction *event*; "
        "these endpoints ask whether it was durable. Machine-readable: "
        "`tables/durable_endpoints.csv`.",
        "",
        "| scenario | first passage | at year 40 | retained >= 2 | net final-5y | "
        "ensemble retained | ensemble durable final-5y |",
        "|---|---:|---:|:---:|---:|---:|---:|",
    ]
    for name, d in diags.items():
        e = endpoints.get(name)
        if e is None:
            lines.append(f"| {name} | — | — | — | — | 0/{d.n_runs} | 0/{d.n_runs} |")
        else:
            lines.append(
                f"| {name} | {fmt(e.first_passage_year)} yr | "
                f"{e.operating_at_horizon:.2f} | "
                f"{'yes' if e.retained_at_horizon else 'no'} | "
                f"{e.net_reproduction_final5:+.3f} | "
                f"{d.n_retained}/{d.n_feasible} | "
                f"{d.n_durable_final5}/{d.n_feasible} |"
            )
    lines += [
        "",
        "Reading: the lunar vitamin bridge retains two cell-equivalents in "
        "every feasible draw but is contracting over the final five years in "
        "every one of them; the terrestrial rehearsal reproduces once and "
        "falls back below two; only the Moon-asteroid network is durably "
        "expanding. Vitamin-pool exhaustion years are per-category first "
        "dips of the pooled inventory (initial Earth stock plus recycled "
        "returns and local production) and are reported in "
        "`tables/vitamin_composition.csv`; pools can refill later from "
        "local production, so a first dip is not permanent depletion.",
        "",
        "## Intelligence-coupling ablations (r4.1)",
        "",
        "Zero/freeze ablations of the declared coupling coefficients; the "
        "seed LP does not read the intelligence block, so dynamics variants "
        "share the central seed. Machine-readable: `tables/ablations.csv`.",
        "",
        "| scenario | variant | first passage | at year 40 | growth share of baseline |",
        "|---|---|---:|---:|---:|",
    ]
    for name, rows in ablations.items():
        for a in rows:
            lines.append(
                f"| {name} | {a.variant} | "
                f"{'—' if a.first_passage_year is None else f'{a.first_passage_year:.2f} yr'} | "
                f"{'infeasible' if not a.feasible else f'{a.operating_at_horizon:.2f}'} | "
                f"{'—' if a.growth_share_of_baseline is None else f'{a.growth_share_of_baseline:.0%}'} |"
            )
    lim_text = "; ".join(
        f"{name}: {lim}/{tot}" for name, (lim, tot) in limited.items()
    )
    lines += [
        "",
        "Finding: every dynamics ablation reproduces the baseline exactly, "
        "because realized cell orders are capped by material availability at "
        f"every step ({lim_text} steps material-limited). Under the central "
        "coefficients the recursive intelligence-industry coupling "
        "contributes nothing to the reported growth trajectories; the "
        "declared AI level is instead load-bearing *statically*, through "
        "seed feasibility and sizing — re-sizing the seed at AI level 1.0 "
        "(base autonomy) leaves the terrestrial rehearsal unchanged and "
        "makes the lunar-bridge and Moon-asteroid scenarios infeasible on "
        "the autonomy threshold. The headline growth numbers are therefore "
        "material-throughput results, not artifacts of the assumed AI "
        "feedback; and the coupling's dynamic coefficients are currently "
        "untestable from these trajectories.",
        "",
        "## Installed-mass versus reproduction-time frontier (r4.1)",
        "",
        "A factor-f seed installs f cell-equivalents of the minimum-mass "
        "design (capacities, feeds, vitamin stock scale with f; the digital "
        "package is shared). Time is first passage to one *additional* "
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
        "Minimum mass is not time-optimal: oversizing the lunar-bridge seed "
        "by 2x cuts the first reproduction from 11.25 to 8.0 years. Returns "
        "diminish along the axis, and mass-optimal versus time-optimal "
        "designs are different points on this frontier.",
        "",
        "## Ensemble diagnostics (r4.1)",
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
        "The depreciation multiplier correlates *positively* with year-40 "
        "cell-equivalents (rho about +0.8 to +0.98) while shortening first "
        "passage: higher assumed sector depreciation forces the minimum-mass "
        "LP to install more service and feed capacity per cell, and that "
        "oversizing accelerates reproduction — the same mechanism the "
        "oversize frontier isolates deliberately. It is a within-model "
        "consequence of minimum-mass sizing, not a claim that wear helps.",
        "",
        "## Strict-lunar infeasibility certificate (r4.1)",
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
        "python scripts/run_fourth.py",
        "pytest tests/test_fourth.py -q",
        "```",
        "",
        "Every generated table is derived from the same in-memory run. "
        "`outputs/fourth/MANIFEST.md` hashes the parameter file, implementation, "
        "runner, report, tables, and figures.",
    ]
    path = OUT / "report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_manifest(files: list[Path]) -> Path:
    lines = [
        "# Fourth Edition artifact manifest",
        "",
        "- generated: 2026-07-28",
        f"- python: {platform.python_version()}",
        f"- numpy: {np.__version__}",
        f"- scipy: {scipy.__version__}",
        f"- PyYAML: {yaml.__version__}",
        "- generator: `scripts/run_fourth.py`",
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

    params = load_fourth_params()
    seeds = {name: size_seed(params, name) for name in SCENARIOS}
    runs = {
        name: simulate_reproduction(params, seed, years=40.0, dt=0.25)
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

    endpoints = {n: durable_endpoints(params, seeds[n], runs[n]) for n in runs}
    vitamins = {n: vitamin_composition(params, seeds[n], runs[n]) for n in runs}
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

    write_scenario_tables(params, seeds, runs, ensembles)
    write_compute_and_debris_tables(compute, debris_runs)
    write_analysis_tables(endpoints, vitamins, ablations, frontiers,
                          diags, certs)
    generate_figures(params, seeds, runs, ensembles, compute, debris_runs)
    generate_analysis_figures(frontiers)
    report = write_report(params, seeds, runs, ensembles, compute,
                          debris_runs, endpoints, vitamins, ablations,
                          frontiers, diags, certs, limited)

    inputs = [
        ROOT / "params" / "fourth_edition.yaml",
        ROOT / "src" / "rsimodel" / "fourth.py",
        ROOT / "src" / "rsimodel" / "fourth_analysis.py",
        ROOT / "scripts" / "run_fourth.py",
        ROOT / "tests" / "test_fourth.py",
        ROOT / "tests" / "test_fourth_analysis.py",
    ]
    artifacts = [report, *TAB.glob("*.csv"), *FIG.glob("*.png")]
    manifest = write_manifest(inputs + artifacts)

    summary = {
        name: {
            "feasible": seeds[name].feasible,
            "seed_mass_t": seeds[name].total_seed_mass_t,
            "second_cell_year": (
                runs[name].second_cell_year if name in runs else None
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
