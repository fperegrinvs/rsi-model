"""Baseline artifact command: assumption sets x locations, cutoff probes, cut sets,
Monte Carlo survival, import-decay sweep, and a provenance-carrying report.

Runtime ~2-4 min. Nothing here is "the" answer; see outputs/report.md.
"""

from __future__ import annotations

import argparse
import time
from collections.abc import Sequence
from pathlib import Path


def baseline_main(argv: Sequence[str] | None = None) -> int:
    """Generate artifacts under an explicit output directory."""
    parser = argparse.ArgumentParser(prog="rsi-run-baseline")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd() / "outputs")
    parser.add_argument("--check-config", action="store_true")
    args = parser.parse_args(argv)
    output_dir = args.output_dir.resolve()
    figure_dir = output_dir / "figures"
    if args.check_config:
        print(f"PASS rsi-run-baseline configuration: output={output_dir}")
        return 0
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    from rsimodel import load_params, run
    from rsimodel.cutsets import find_cut_sets
    from rsimodel.montecarlo import ensemble, sweep_import_decay
    from rsimodel.plots import (
        cutoff_experiment,
        decay_sweep,
        delta_decomposition,
        stockpiles,
        survival_curves,
        trajectories,
    )
    from rsimodel.report import write_report

    t0 = time.time()
    SETS = ("conservative", "central", "optimistic")
    ENVS = ("leo", "lunar", "mars")
    figures = []

    # --- deterministic sweeps -------------------------------------------------
    results = {}
    for set_name in SETS:
        for env in ENVS:
            r = run(load_params(set_name, env=env), years=40)
            results[(set_name, env)] = r
            d = r.doubling_time()
            print(
                f"{set_name:>13}/{env:<5}: g(30) = {r.g[min(120, len(r.g) - 1)]:+.3f}/yr | "
                f"doubling = {'never' if d is None else f'{d:.1f} yr'} | "
                f"binding = {r.params.sectors[r.binding[-1]]}"
            )

    figures.append(
        trajectories(
            {s: results[(s, "lunar")] for s in SETS}, fname=figure_dir / "capacity_by_set_lunar.png"
        )
    )
    figures.append(
        delta_decomposition(
            {env: load_params("central", env=env) for env in (*ENVS, "earth")},
            fname=figure_dir / "delta_decomposition.png",
        )
    )

    # --- electronics-class cutoff probe (the vitamin scenario) ----------------
    central_lunar = load_params("central", env="lunar")
    r_open = results[("central", "lunar")]
    r_cut = run(central_lunar, years=40, cutoff_year=8.0, cutoff_sectors=["electronics"])
    figures.append(
        cutoff_experiment(
            r_open,
            r_cut,
            8.0,
            fname=figure_dir / "electronics_cutoff.png",
            what="electronics imports",
        )
    )
    figures.append(stockpiles(r_cut, fname=figure_dir / "stockpiles_cutoff.png"))
    print(f"[{time.time() - t0:5.1f}s] deterministic sweeps + cutoff probe done")

    # --- minimum cut sets -----------------------------------------------------
    cuts = {}
    for label, (set_name, env) in {
        "central/lunar": ("central", "lunar"),
        "central/leo": ("central", "leo"),
    }.items():
        cuts[label] = find_cut_sets(load_params(set_name, env=env), horizon=30, dt=0.5)
        cs = cuts[label]
        print(
            f"[{time.time() - t0:5.1f}s] cuts {label}: baseline="
            f"{'expands' if cs.baseline_expanding else 'FAILS'} | "
            f"minimal cuts: {cs.minimal_cuts or 'none'} | "
            f"indispensable: {', '.join(cs.indispensable)}"
        )

    # --- Monte Carlo ----------------------------------------------------------
    mcs = []
    for set_name, env in (("central", "lunar"), ("conservative", "lunar"), ("central", "mars")):
        mc = ensemble(set_name, env, n_runs=40, years=35, horizon=30)
        mcs.append(mc)
        print(f"[{time.time() - t0:5.1f}s] MC {mc.summary()}")
    figures.append(survival_curves(mcs, fname=figure_dir / "survival.png"))

    grid, ps = sweep_import_decay("central", "lunar", n_runs=24, years=35, horizon=30)
    figures.append(
        decay_sweep(
            {"central/lunar": (grid, ps)},
            horizon=30,
            fname=figure_dir / "import_decay_sweep.png",
        )
    )
    print(
        f"[{time.time() - t0:5.1f}s] decay sweep: "
        + ", ".join(f"{d:g}yr->{p:.2f}" for d, p in zip(grid, ps, strict=True))
    )

    # --- report ---------------------------------------------------------------
    rep = write_report(
        results,
        mcs,
        cuts,
        figures,
        provenance_of=central_lunar,
        path=output_dir / "report.md",
    )
    print(f"[{time.time() - t0:5.1f}s] report: {rep}")
    for f in figures:
        print("figure:", f)
    return 0


if __name__ == "__main__":
    raise SystemExit(baseline_main())
