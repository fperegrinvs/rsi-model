from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from .array_types import FloatArray
from .lco import LCOMC
from .model import RunResult
from .montecarlo import MCResult
from .orbital_ai_scenarios import (
    LCO_COMPONENT_HATCHES,
    LCO_SCENARIO_DISPLAY_LABELS,
    RATIO_CASE_LABELS,
    RATIO_LINE_STYLES,
)
from .plotting_adapter import (
    axes_row,
    close_figure,
    diverging_norm,
    legend_patch,
    new_figure,
    single_axes,
)

if TYPE_CHECKING:
    from .lco import EarthLCO, SpaceLCO
    from .model import Params

FIGDIR = Path(__file__).resolve().parents[2] / "outputs" / "figures"


def _figure_path(fname: str | Path) -> Path:
    target = Path(fname)
    output = target if target.is_absolute() else FIGDIR / target
    output.parent.mkdir(parents=True, exist_ok=True)
    return output


def trajectories(
    results: Mapping[str, RunResult],
    fname: str | Path = "capacity_by_set.png",
) -> Path:
    fig, axes = axes_row(2, figsize=(11, 4.2))
    for label, r in results.items():
        axes[0].plot(r.t, r.K.sum(axis=1), label=label)
        axes[1].plot(r.t, r.g, label=label)
    axes[0].set(title="Total capacity (all sectors)", xlabel="years", ylabel="capacity units")
    axes[0].set_yscale("log")
    axes[1].set(title="Maximin sector growth rate g(t)", xlabel="years", ylabel="1/yr")
    axes[1].axhline(0, color="k", lw=0.6)
    for ax in axes:
        ax.legend(fontsize=8)
    out = _figure_path(fname)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    close_figure(fig)
    return out


def cutoff_experiment(
    r_open: RunResult,
    r_cut: RunResult,
    cutoff_year: float,
    fname: str | Path = "import_cutoff.png",
    what: str = "all imports",
) -> Path:
    fig, axes = axes_row(2, figsize=(11, 4.2))
    axes[0].plot(r_open.t, r_open.K.sum(axis=1), label="imports on ramp")
    axes[0].plot(r_cut.t, r_cut.K.sum(axis=1), label=f"{what} cut at yr {cutoff_year:g}")
    axes[0].set(
        title="Clock-setting probe: total capacity", xlabel="years", ylabel="capacity units"
    )
    axes[0].set_yscale("log")
    axes[1].plot(r_open.t, r_open.g, label="imports on ramp")
    axes[1].plot(r_cut.t, r_cut.g, label=f"{what} cut at yr {cutoff_year:g}")
    axes[1].axhline(0, color="k", lw=0.6)
    axes[1].set(title="Maximin growth rate g(t)", xlabel="years", ylabel="1/yr")
    for ax in axes:
        ax.axvline(cutoff_year, color="r", ls="--", lw=0.8)
        ax.legend(fontsize=8)
    out = _figure_path(fname)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    close_figure(fig)
    return out


def delta_decomposition(
    params_by_env: Mapping[str, Params],
    fname: str | Path = "delta_decomposition.png",
) -> Path:
    """Stacked per-sector bars of wear/catastrophic/obsolescence/logistics per environment."""
    from .delta import DELTA_COMPONENTS

    envs = list(params_by_env)
    fig, axes = axes_row(
        len(envs),
        figsize=(4.2 * len(envs), 4.4),
        sharey=True,
    )
    for ax, env in zip(axes, envs, strict=True):
        p = params_by_env[env]
        xpos = np.arange(p.n)
        bottom = np.zeros(p.n)
        for comp in DELTA_COMPONENTS:
            v = p.delta_comps[comp]
            ax.bar(xpos, v, bottom=bottom, label=comp, width=0.7)
            bottom += v
        ax.set_xticks(xpos)
        ax.set_xticklabels(p.sectors, rotation=60, ha="right", fontsize=7)
        ax.set(title=env)
    axes[0].set_ylabel("capacity loss / yr")
    axes[0].legend(fontsize=7)
    fig.suptitle("delta decomposed by component (central values)", y=1.0)
    out = _figure_path(fname)
    fig.tight_layout()
    fig.savefig(out, dpi=140, bbox_inches="tight")
    close_figure(fig)
    return out


def stockpiles(r: RunResult, fname: str | Path = "stockpiles.png") -> Path:
    p = r.params
    fig, ax = single_axes(figsize=(7, 4.2))
    for i in np.flatnonzero(p.stockable):
        ax.plot(r.t, r.S[:, i], label=p.sectors[i])
    ax.set(
        title=f"Vitamin-part stockpiles ({p.label}/{p.environment})",
        xlabel="years",
        ylabel="output units held",
    )
    ax.legend(fontsize=8)
    out = _figure_path(fname)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    close_figure(fig)
    return out


def survival_curves(
    mcs: Sequence[MCResult],
    fname: str | Path = "survival.png",
) -> Path:
    """P(g(t) > 0) per MCResult (label/environment in the legend)."""
    fig, ax = single_axes(figsize=(7, 4.2))
    for mc in mcs:
        ax.plot(mc.t, mc.survival, label=f"{mc.label}/{mc.environment} (n={mc.n_runs})")
    ax.set(
        title="Survival: fraction of runs with positive maximin growth",
        xlabel="years",
        ylabel="P(g(t) > 0)",
        ylim=(-0.02, 1.02),
    )
    ax.legend(fontsize=8)
    out = _figure_path(fname)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    close_figure(fig)
    return out


def lco_composition(
    spaces: Mapping[str, SpaceLCO],
    earths: Mapping[str, EarthLCO],
    fname: str | Path = "lco_composition.png",
) -> Path:
    """Annualized $/kW-yr stacked by capex component, vs Earth scenario lines."""
    fig, ax = single_axes(figsize=(8, 4.6))
    cases = list(spaces)
    xpos = np.arange(len(cases))
    comps = ["hardware", "pv", "radiator", "storage", "launch"]
    bottom = np.zeros(len(cases))
    for comp, hatch in zip(comps, LCO_COMPONENT_HATCHES, strict=True):
        vals = []
        for c in cases:
            s = spaces[c]
            annualize = s.lco / sum(s.capex_per_kw.values())  # $/yr per $ capex, incl util
            vals.append(s.capex_per_kw[comp] * annualize)
        ax.bar(
            xpos,
            vals,
            bottom=bottom,
            label=comp,
            width=0.6,
            hatch=hatch,
            edgecolor="black",
            linewidth=0.35,
        )
        bottom += np.array(vals)
    for style, (scen, e) in zip(("-", "--", ":"), earths.items(), strict=True):
        ax.axhline(e.lco, color="k", ls=style, lw=1.0, label=f"Earth {scen} ({e.node})")
    ax.set_xticks(xpos)
    ax.set_xticklabels([LCO_SCENARIO_DISPLAY_LABELS.get(c, c) for c in cases])
    ax.set(
        title="Levelized cost of compute (neutral references + named scenarios)",
        ylabel="$ per frontier-equiv kW-yr",
    )
    ax.set_yscale("log")
    ax.legend(fontsize=7, ncol=2)
    out = _figure_path(fname)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    close_figure(fig)
    return out


def ratio_distributions(
    mcs: Sequence[LCOMC],
    fname: str | Path = "lco_ratio_mc.png",
) -> Path:
    """MC distribution of space/earth cost ratio per case x scenario."""
    fig, ax = single_axes(figsize=(8, 4.6))
    for index, mc in enumerate(mcs):
        arch = "reuse" if mc.architecture == "serviceable_platform" else "disposable"
        ax.hist(
            np.log10(mc.ratio_samples),
            bins=50,
            density=True,
            histtype="step",
            linewidth=1.4,
            linestyle=RATIO_LINE_STYLES[index % len(RATIO_LINE_STYLES)],
            label=(
                f"{RATIO_CASE_LABELS.get(mc.case, mc.case)}/{arch} vs {mc.scenario} "
                f"(P(<1)={mc.p_space_cheaper:.2f})"
            ),
        )
    ax.axvline(0, color="k", lw=1.0)
    ax.set(
        title="Space/Earth cost ratio over anchored MC",
        xlabel="log10(space LCO / Earth LCO)",
        ylabel="density",
    )
    ax.legend(fontsize=7)
    out = _figure_path(fname)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    close_figure(fig)
    return out


def crossover_contours(
    panels: Mapping[str, tuple[FloatArray, FloatArray, FloatArray, str]],
    published_band: tuple[float, float] = (1400.0, 4000.0),
    target_band: tuple[float, float] = (30.0, 185.0),
    fname: str | Path = "crossover_surface.png",
) -> Path:
    """Each panel: (launch_prices, other_values, ratio_grid, ylabel).
    Contour space/earth ratio with the =1 crossover line; launch price on log x.
    Shaded bands: published prices (company price sheets) and aspirational
    targets (company statements — evidence of intent, not feasibility)."""
    n = len(panels)
    if n == 0:
        raise ValueError("at least one crossover panel is required")
    if n > 5:
        raise ValueError("the crossover layout supports at most five panels")
    fig = new_figure(figsize=(12.2, 7.4), layout="constrained")
    grid = fig.add_gridspec(2, 3)
    axes = [fig.add_subplot(grid[index // 3, index % 3]) for index in range(n)]
    key_ax = fig.add_subplot(grid[1, 2])
    norm = diverging_norm(vmin=-0.7, vcenter=0.0, vmax=3.0)
    levels = np.concatenate([np.linspace(-0.7, 0, 8), np.linspace(0.2, 3.0, 15)])
    cs = None
    for ax, (title, (lp, ov, grid, ylab)) in zip(axes, panels.items(), strict=True):
        lg = np.log10(grid)
        cs = ax.contourf(
            lp, ov, np.clip(lg, -0.7, 3.0), levels=levels, cmap="RdYlGn_r", norm=norm, alpha=0.9
        )
        if lg.min() < 0 < lg.max():
            c1 = ax.contour(lp, ov, lg, levels=[0.0], colors="k", linewidths=1.6)
            ax.clabel(c1, fmt=lambda _: "space = earth")
        ax.axvspan(*published_band, color="tab:blue", alpha=0.15)
        ax.axvspan(*target_band, color="tab:orange", alpha=0.15)
        ax.set_xscale("log")
        ax.set(title=title, xlabel="LEO launch $/kg", ylabel=ylab)
        ax.tick_params(labelsize=8)
        ax.title.set_fontsize(10)
    if cs is None:
        raise RuntimeError("crossover contour rendering produced no contour set")
    key_ax.set_axis_off()
    color_ax = key_ax.inset_axes((0.02, 0.1, 0.13, 0.78))
    cb = fig.colorbar(cs, cax=color_ax, ticks=[-0.7, 0, 1, 2, 3])
    cb.set_label("space/earth LCO ratio")
    cb.ax.yaxis.set_label_position("left")
    cb.ax.set_yticklabels(["0.2x", "1x", "10x", "100x", "1000x"])
    key_ax.legend(
        handles=[
            legend_patch(
                facecolor="tab:blue",
                alpha=0.15,
                label="Published launch-price band",
            ),
            legend_patch(
                facecolor="tab:orange",
                alpha=0.15,
                label="Aspirational target band",
            ),
        ],
        loc="center left",
        bbox_to_anchor=(0.48, 0.47),
        frameon=False,
        fontsize=9,
    )
    key_ax.text(
        0.48,
        0.74,
        "Shared scale",
        transform=key_ax.transAxes,
        fontsize=10,
        fontweight="bold",
    )
    fig.suptitle(
        "Generic-LEO crossover surface\n"
        "Bands locate price claims; they do not establish feasibility",
        fontsize=12,
    )
    out = _figure_path(fname)
    fig.savefig(out, dpi=160, bbox_inches="tight")
    close_figure(fig)
    return out


def decay_sweep(
    curves: Mapping[str, tuple[FloatArray, FloatArray]],
    horizon: float,
    fname: str | Path = "import_decay_sweep.png",
) -> Path:
    """P(expansion by horizon) vs import ramp-down e-folding time."""
    fig, ax = single_axes(figsize=(7, 4.2))
    for label, (grid, ps) in curves.items():
        ax.plot(grid, ps, marker="o", label=label)
    ax.set(
        title=f"P(self-expanding by {horizon:g} yr) vs import ramp-down",
        xlabel="import decay e-folding (years)",
        ylabel="probability",
        ylim=(-0.02, 1.02),
    )
    ax.legend(fontsize=8)
    out = _figure_path(fname)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    close_figure(fig)
    return out
