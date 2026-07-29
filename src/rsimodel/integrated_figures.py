"""Generated-artifact component for the integrated pipeline."""

from __future__ import annotations

import numpy as np

from .integrated_artifacts import (
    SCENARIOS,
    ArtifactWorkspace,
)
from .integrated_types import (
    CapacityRuns,
    ComputeComparison,
    DebrisRuns,
    EnsembleResults,
    FrontierResults,
    SeedResults,
)
from .plotting_adapter import close_figure, single_axes, use_style


def generate_figures(
    workspace: ArtifactWorkspace,
    seeds: SeedResults,
    runs: CapacityRuns,
    ensembles: EnsembleResults,
    compute: ComputeComparison,
    debris_runs: DebrisRuns,
) -> None:
    use_style("seaborn-v0_8-whitegrid")

    fig, ax = single_axes(figsize=(9, 5.2))
    labels, data = [], []
    for name in SCENARIOS:
        values = ensembles[name].seed_masses_t
        if values:
            labels.append(name.replace("_", "\n"))
            data.append(values)
    if data:
        ax.boxplot(data, tick_labels=labels, showfliers=False, whis=(10, 90))
        for i, name in enumerate([n for n in SCENARIOS if ensembles[n].seed_masses_t], 1):
            central = seeds[name]
            ax.scatter(
                [i],
                [central.required_masses()[0]],
                marker="D",
                s=45,
                color="#d1495b",
                label="central scenario" if i == 1 else None,
                zorder=4,
            )
        ax.legend(loc="upper left")
    else:
        ax.text(
            0.5,
            0.5,
            "No feasible ensemble draws",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        ax.set_xticks([])
    ax.set_ylabel("Installed seed mass (scenario tonnes)")
    ax.set_title("Current seed-sizing assumption ensembles")
    fig.tight_layout()
    fig.savefig(workspace.figure_directory / "seed_mass_ensemble.png", dpi=180)
    close_figure(fig)

    fig, ax = single_axes(figsize=(9, 5.2))
    for name, run in runs.items():
        ax.plot(run.t, run.operating_cells, label=name.replace("_", " "))
    ax.axhline(
        2.0,
        color="#333333",
        ls="--",
        lw=1,
        label="aggregate operating-capacity doubling",
    )
    ax.set_xlabel("Years after seed activation")
    ax.set_ylabel("Sector-balanced operating-cell equivalents")
    ax.set_yscale("log")
    ax.set_ylim(0.5, max(20.0, max(r.operating_cells[-1] for r in runs.values()) * 1.2))
    ax.set_title("Slowest-sector capacity after sector-specific commissioning")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(workspace.figure_directory / "operating_capacity.png", dpi=180)
    close_figure(fig)

    fig, ax = single_axes(figsize=(9, 5.2))
    ax.plot(compute.t, compute.endogenous, lw=2.5, label="off-world endogenous total")
    ax.plot(compute.t, compute.endogenous_orbit, lw=2.0, label="Moon→orbit endogenous")
    for label in ("tight", "base", "responsive"):
        ax.plot(
            compute.t,
            compute.earth_fed_orbit[label],
            ls="--",
            label=f"Earth-fed orbit: {label}",
        )
    ax.set_xlabel("Years")
    ax.set_ylabel("Compute capacity (normalized to initial stock)")
    ax.set_title("Rate-limited deployment versus endogenous capacity growth")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(workspace.figure_directory / "compute_growth_regimes.png", dpi=180)
    close_figure(fig)

    fig, ax = single_axes(figsize=(9, 5.2))
    for d in debris_runs:
        ax.plot(
            d.t,
            d.fragments,
            label=f"{d.label} · R={d.creation_clearance_ratio:.2f}",
        )
    ax.set_xlabel("Years")
    ax.set_ylabel("Fragment index (scenario units)")
    ax.set_yscale("symlog", linthresh=0.01)
    ax.set_title("Orbital growth is conditional on debris topology and mitigation")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(workspace.figure_directory / "debris_regimes.png", dpi=180)
    close_figure(fig)


def generate_analysis_figures(
    workspace: ArtifactWorkspace,
    frontiers: FrontierResults,
) -> None:
    fig, ax = single_axes(figsize=(8.5, 5.0))
    for name, rows in frontiers.items():
        xs = [r.installed_mass_t for r in rows]
        ys = [
            np.nan if r.time_to_one_additional_cell is None else r.time_to_one_additional_cell
            for r in rows
        ]
        ax.plot(xs, ys, marker="o", label=name)
        for r in rows:
            if r.time_to_one_additional_cell is not None:
                ax.annotate(
                    f"×{r.oversize_factor:g}",
                    (r.installed_mass_t, r.time_to_one_additional_cell),
                    textcoords="offset points",
                    xytext=(4, 4),
                    fontsize=8,
                )
    ax.set_xlabel("Installed seed mass (scenario tonnes)")
    ax.set_ylabel("Years to one additional operating cell-equivalent")
    ax.set_title("Oversize frontier: mass versus aggregate-capacity doubling")
    ax.legend()
    fig.tight_layout()
    fig.savefig(workspace.figure_directory / "oversize_frontier.png", dpi=180)
    close_figure(fig)
