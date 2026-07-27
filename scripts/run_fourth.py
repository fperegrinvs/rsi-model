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


def write_report(params, seeds, runs, ensembles, compute, debris_runs) -> Path:
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
        "- generated: 2026-07-27",
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

    write_scenario_tables(params, seeds, runs, ensembles)
    write_compute_and_debris_tables(compute, debris_runs)
    generate_figures(params, seeds, runs, ensembles, compute, debris_runs)
    report = write_report(params, seeds, runs, ensembles, compute, debris_runs)

    inputs = [
        ROOT / "params" / "fourth_edition.yaml",
        ROOT / "src" / "rsimodel" / "fourth.py",
        ROOT / "scripts" / "run_fourth.py",
        ROOT / "tests" / "test_fourth.py",
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
