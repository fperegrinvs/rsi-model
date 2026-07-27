from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .model import RunResult

FIGDIR = Path(__file__).resolve().parents[2] / "outputs" / "figures"


def trajectories(results: dict[str, RunResult], fname: str = "capacity_by_set.png") -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for label, r in results.items():
        axes[0].plot(r.t, r.K.sum(axis=1), label=label)
        axes[1].plot(r.t, r.g, label=label)
    axes[0].set(title="Total capacity (all sectors)", xlabel="years", ylabel="capacity units")
    axes[0].set_yscale("log")
    axes[1].set(title="Maximin sector growth rate g(t)", xlabel="years", ylabel="1/yr")
    axes[1].axhline(0, color="k", lw=0.6)
    for ax in axes:
        ax.legend(fontsize=8)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out


def cutoff_experiment(r_open: RunResult, r_cut: RunResult, cutoff_year: float,
                      fname: str = "import_cutoff.png", what: str = "all imports") -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(r_open.t, r_open.K.sum(axis=1), label="imports on ramp")
    axes[0].plot(r_cut.t, r_cut.K.sum(axis=1), label=f"{what} cut at yr {cutoff_year:g}")
    axes[0].set(title="Clock-setting probe: total capacity",
                xlabel="years", ylabel="capacity units")
    axes[0].set_yscale("log")
    axes[1].plot(r_open.t, r_open.g, label="imports on ramp")
    axes[1].plot(r_cut.t, r_cut.g, label=f"{what} cut at yr {cutoff_year:g}")
    axes[1].axhline(0, color="k", lw=0.6)
    axes[1].set(title="Maximin growth rate g(t)", xlabel="years", ylabel="1/yr")
    for ax in axes:
        ax.axvline(cutoff_year, color="r", ls="--", lw=0.8)
        ax.legend(fontsize=8)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out


def delta_decomposition(params_by_env: dict[str, "Params"],
                        fname: str = "delta_decomposition.png") -> Path:
    """Stacked per-sector bars of wear/catastrophic/obsolescence/logistics per environment."""
    from .delta import DELTA_COMPONENTS
    envs = list(params_by_env)
    fig, axes = plt.subplots(1, len(envs), figsize=(4.2 * len(envs), 4.4), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, env in zip(axes, envs):
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
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140, bbox_inches="tight"); plt.close(fig)
    return out


def stockpiles(r: RunResult, fname: str = "stockpiles.png") -> Path:
    p = r.params
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for i in np.flatnonzero(p.stockable):
        ax.plot(r.t, r.S[:, i], label=p.sectors[i])
    ax.set(title=f"Vitamin-part stockpiles ({p.label}/{p.environment})",
           xlabel="years", ylabel="output units held")
    ax.legend(fontsize=8)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out


def survival_curves(mcs: list, fname: str = "survival.png") -> Path:
    """P(g(t) > 0) per MCResult (label/environment in the legend)."""
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for mc in mcs:
        ax.plot(mc.t, mc.survival, label=f"{mc.label}/{mc.environment} (n={mc.n_runs})")
    ax.set(title="Survival: fraction of runs with positive maximin growth",
           xlabel="years", ylabel="P(g(t) > 0)", ylim=(-0.02, 1.02))
    ax.legend(fontsize=8)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out


def lco_composition(spaces: dict[str, "SpaceLCO"], earths: dict[str, "EarthLCO"],
                    fname: str = "lco_composition.png") -> Path:
    """Annualized $/kW-yr stacked by capex component, vs Earth scenario lines."""
    fig, ax = plt.subplots(figsize=(8, 4.6))
    cases = list(spaces)
    xpos = np.arange(len(cases))
    comps = ["hardware", "pv", "radiator", "storage", "launch"]
    bottom = np.zeros(len(cases))
    for comp in comps:
        vals = []
        for c in cases:
            s = spaces[c]
            annualize = s.lco / sum(s.capex_per_kw.values())  # $/yr per $ capex, incl util
            vals.append(s.capex_per_kw[comp] * annualize)
        ax.bar(xpos, vals, bottom=bottom, label=comp, width=0.6)
        bottom += np.array(vals)
    for style, (scen, e) in zip(("-", "--", ":"), earths.items()):
        ax.axhline(e.lco, color="k", ls=style, lw=1.0,
                   label=f"Earth {scen} ({e.node})")
    ax.set_xticks(xpos)
    ax.set_xticklabels(cases)
    ax.set(title="Levelized cost of compute (central anchor values)",
           ylabel="$ per frontier-equiv kW-yr")
    ax.set_yscale("log")
    ax.legend(fontsize=7, ncol=2)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out


def ratio_distributions(mcs: list, fname: str = "lco_ratio_mc.png") -> Path:
    """MC distribution of space/earth cost ratio per case x scenario."""
    fig, ax = plt.subplots(figsize=(8, 4.6))
    for mc in mcs:
        ax.hist(np.log10(mc.ratio_samples), bins=50, density=True, alpha=0.5,
                label=f"{mc.case} vs {mc.scenario} (P(<1)={mc.p_space_cheaper:.2f})")
    ax.axvline(0, color="k", lw=1.0)
    ax.set(title="Space/Earth cost ratio over anchored MC",
           xlabel="log10(space LCO / Earth LCO)", ylabel="density")
    ax.legend(fontsize=7)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out


def crossover_contours(panels: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, str]],
                       published_band: tuple[float, float] = (1400.0, 4000.0),
                       target_band: tuple[float, float] = (30.0, 150.0),
                       fname: str = "crossover_surface.png") -> Path:
    """Each panel: (launch_prices, other_values, ratio_grid, ylabel).
    Contour space/earth ratio with the =1 crossover line; launch price on log x.
    Shaded bands: published prices (company price sheets) and aspirational
    targets (company statements — evidence of intent, not feasibility)."""
    from matplotlib.colors import TwoSlopeNorm
    n = len(panels)
    fig, axes = plt.subplots(1, n, figsize=(4.6 * n, 4.2))
    axes = np.atleast_1d(axes)
    norm = TwoSlopeNorm(vmin=-0.7, vcenter=0.0, vmax=3.0)
    levels = np.concatenate([np.linspace(-0.7, 0, 8), np.linspace(0.2, 3.0, 15)])
    for ax, (title, (lp, ov, grid, ylab)) in zip(axes, panels.items()):
        lg = np.log10(grid)
        cs = ax.contourf(lp, ov, np.clip(lg, -0.7, 3.0), levels=levels,
                         cmap="RdYlGn_r", norm=norm, alpha=0.9)
        if lg.min() < 0 < lg.max():
            c1 = ax.contour(lp, ov, lg, levels=[0.0], colors="k", linewidths=1.6)
            ax.clabel(c1, fmt=lambda _: "space = earth")
        ax.axvspan(*published_band, color="tab:blue", alpha=0.15)
        ax.axvspan(*target_band, color="tab:orange", alpha=0.15)
        ax.set_xscale("log")
        ax.set(title=title, xlabel="LEO launch $/kg", ylabel=ylab)
    cb = fig.colorbar(cs, ax=axes[-1], ticks=[-0.7, 0, 1, 2, 3])
    cb.set_label("space/earth LCO ratio")
    cb.ax.set_yticklabels(["0.2x", "1x", "10x", "100x", "1000x"])
    fig.suptitle("Crossover surface (blue band: published prices; "
                 "orange: aspirational targets — intent, not feasibility)",
                 fontsize=9, y=1.02)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140, bbox_inches="tight"); plt.close(fig)
    return out


def decay_sweep(curves: dict[str, tuple[np.ndarray, np.ndarray]],
                horizon: float, fname: str = "import_decay_sweep.png") -> Path:
    """P(expansion by horizon) vs import ramp-down e-folding time."""
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for label, (grid, ps) in curves.items():
        ax.plot(grid, ps, marker="o", label=label)
    ax.set(title=f"P(self-expanding by {horizon:g} yr) vs import ramp-down",
           xlabel="import decay e-folding (years)", ylabel="probability",
           ylim=(-0.02, 1.02))
    ax.legend(fontsize=8)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / fname
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)
    return out
