"""Deep Monte Carlo run: larger ensembles, sampled-anchor cut probabilities.

Writes outputs/report_deep.md AND outputs/tables/mc_deep.csv from the SAME
objects in the same execution — this script is the only generator of both, so
the r3.4 stale-artifact failure mode (CSV and report from different runs) is
structurally excluded. Use run_baseline.py for the fast smoke sweep.

r3.5: the independent Monte Carlo stages fan out over a process pool, with
each 400-run cell further split into 4 independently seeded 100-run chunks
for load balancing. Every task carries its own stable crc32-derived seed and
consumes its own RNG stream, so results are identical regardless of
scheduling — parallelism buys wall-clock only (~3 min on a 10-core machine
vs ~40 min for the serial r3.4 script). Per-anchor draws are keyed by anchor
NAME (delta.draw_anchors), so results are also stable under anchor-list
growth.
"""
import csv
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from rsimodel import load_params, run
from rsimodel.cutsets import cut_probability, find_cut_sets
from rsimodel.montecarlo import (ensemble, merge_ensembles, sensitivity,
                                 sweep_import_decay)
from rsimodel.plots import decay_sweep, survival_curves
from rsimodel.policies import compare_policies
from rsimodel.report import OUTDIR, write_report

SETS = ("conservative", "central", "optimistic")
ENVS = ("leo", "lunar", "mars")


# --- module-level workers (picklable under macOS spawn) ---------------------

def _ensemble(kw: dict):
    return ensemble(**kw)


def _decay(env: str):
    return env, sweep_import_decay("central", env, n_runs=60, years=35, horizon=30)


def _cutp(args: tuple[str, str]):
    set_name, env = args
    return cut_probability(set_name, env, n_runs=40, horizon=30, dt=0.5,
                           seed=zlib.crc32(f"{set_name}/{env}/cp".encode()))


def _cuts(env: str):
    return env, find_cut_sets(load_params("central", env=env), horizon=30, dt=0.5)


def _policies(env: str):
    return env, compare_policies("central", env, n_runs=30, seed=11)


def _sens(_):
    return sensitivity("central", "lunar", n_runs=300, seed=5)


def main() -> None:
    t0 = time.time()
    figures = []

    results = {(s, e): run(load_params(s, env=e), years=40)
               for s in SETS for e in ENVS}
    print(f"[{time.time()-t0:6.1f}s] deterministic grid done")

    # --- fan out every independent MC stage --------------------------------
    # Each 400-run cell is split into CHUNKS independently seeded chunks so
    # the pool load-balances (wall-clock ~ total CPU / workers instead of
    # being quantized by whole ~3-min cells). Chunk seeds are stable crc32
    # strings; merge_ensembles recombines counts/lists exactly.
    CHUNKS, RUNS_PER_CHUNK = 4, 100

    def chunk_kws(tag: str, **kw) -> list[dict]:
        return [dict(seed=zlib.crc32(f"{tag}/chunk{i}".encode()), **kw)
                for i in range(CHUNKS)]

    main_groups = [chunk_kws(f"{s}/{e}", set_name=s, env=e,
                             n_runs=RUNS_PER_CHUNK, years=35, horizon=30)
                   for s in SETS for e in ENVS]
    # Endpoint 4 probe: central set, ALL Earth imports cut at year 30.
    # LEO's exogenous orbital capture feed continues and is stated in its
    # label, so that row is not called autonomous. Stock drawdown is allowed; a
    # minimum-viable-scale floor needs an authorial threshold and is flagged
    # in ROADMAP, not silently invented.
    auto_groups = [chunk_kws(f"central/{e}/noimport30", set_name="central",
                             env=e, n_runs=RUNS_PER_CHUNK, years=36,
                             horizon=35, cutoff_year=30.0,
                             label=("central_import_cut_capture_continues"
                                    if e == "leo" else "central_noimport30"))
                   for e in ENVS]

    workers = max(1, min(12, (os.cpu_count() or 4) - 1))
    print(f"[{time.time()-t0:6.1f}s] fanning out on {workers} workers, "
          f"{CHUNKS} chunks x {RUNS_PER_CHUNK} runs per cell")
    with ProcessPoolExecutor(max_workers=workers) as ex:
        f_main = [[ex.submit(_ensemble, kw) for kw in grp]
                  for grp in main_groups]
        f_auto = [[ex.submit(_ensemble, kw) for kw in grp]
                  for grp in auto_groups]
        f_decay = [ex.submit(_decay, env) for env in ("lunar", "leo")]
        f_cutp = [ex.submit(_cutp, a) for a in (("central", "lunar"),
                                                ("central", "leo"),
                                                ("central", "mars"),
                                                ("optimistic", "lunar"))]
        f_cuts = [ex.submit(_cuts, env) for env in ("lunar", "leo")]
        f_pol = [ex.submit(_policies, env) for env in ("lunar", "leo")]
        f_sens = ex.submit(_sens, None)

        mcs = []
        for grp in f_main:
            mc = merge_ensembles([f.result() for f in grp])
            mcs.append(mc)
            print(f"[{time.time()-t0:6.1f}s] MC {mc.summary()}")
        mcs_auto = []
        for grp in f_auto:
            mc = merge_ensembles([f.result() for f in grp])
            mcs_auto.append(mc)
            print(f"[{time.time()-t0:6.1f}s] MC {mc.summary()}")

        curves = {}
        for f in f_decay:
            env, (grid, ps) = f.result()
            curves[f"central/{env}"] = (grid, ps)
            print(f"[{time.time()-t0:6.1f}s] decay sweep central/{env}: "
                  + ", ".join(f"{d:g}yr->{p:.2f}" for d, p in zip(grid, ps)))

        cut_probs = []
        for f in f_cutp:
            cp = f.result()
            cut_probs.append(cp)
            top = sorted(cp.p_fatal.items(), key=lambda kv: -kv[1])[:2]
            print(f"[{time.time()-t0:6.1f}s] cutP {cp.label}/{cp.environment}: "
                  f"base={cp.p_baseline:.2f} | "
                  + " | ".join(f"{('ALL' if len(c) > 1 else c[0])}:{p:.2f}"
                               for c, p in top))

        cuts = {}
        for f in f_cuts:
            env, cs = f.result()
            cuts[f"central/{env}"] = cs
        print(f"[{time.time()-t0:6.1f}s] central-value cut sets done")

        pol_results = [f.result() for f in f_pol]
        sens = f_sens.result()

    # --- machine-readable headline table ------------------------------------
    tables = OUTDIR / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    with open(tables / "mc_deep.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["set", "env", "n_expanding", "n_runs", "share", "ci95_lo",
                    "ci95_hi", "n_ever_doubled", "dbl_all_med", "dbl_all_q25",
                    "dbl_all_q75", "n_survivor_doubled", "dbl_srv_med",
                    "dbl_srv_q25", "dbl_srv_q75", "top_binding_sector",
                    "top_binding_share",
                    "n_sustained", "n_alloc_expanding",
                    "n_alloc_sustained",
                    "n_bal_doubled", "bal_dbl_med", "bal_dbl_q25",
                    "bal_dbl_q75", "n_bal_srv_doubled", "bal_srv_med",
                    "lambda_h_med"])
        for mc in mcs + mcs_auto:
            lo, hi = mc.expanding_ci
            d = np.array(mc.doubling_times)
            ds = np.array(mc.doubling_times_survivors)
            b = np.array(mc.doubling_times_balanced)
            bs = np.array(mc.doubling_times_balanced_survivors)
            lam = np.array(mc.lambda_horizon)
            top = max(mc.binding_hist.items(), key=lambda kv: kv[1])
            w.writerow([mc.label, mc.environment, mc.n_expanding, mc.n_runs,
                        f"{mc.p_expanding:.4f}", f"{lo:.4f}", f"{hi:.4f}",
                        len(d),
                        f"{np.median(d):.2f}" if len(d) else "",
                        f"{np.percentile(d, 25):.2f}" if len(d) else "",
                        f"{np.percentile(d, 75):.2f}" if len(d) else "",
                        len(ds),
                        f"{np.median(ds):.2f}" if len(ds) else "",
                        f"{np.percentile(ds, 25):.2f}" if len(ds) else "",
                        f"{np.percentile(ds, 75):.2f}" if len(ds) else "",
                        top[0], f"{top[1]:.3f}",
                        mc.n_sustained, mc.n_alloc_expanding,
                        mc.n_alloc_sustained,
                        len(b),
                        f"{np.median(b):.2f}" if len(b) else "",
                        f"{np.percentile(b, 25):.2f}" if len(b) else "",
                        f"{np.percentile(b, 75):.2f}" if len(b) else "",
                        len(bs),
                        f"{np.median(bs):.2f}" if len(bs) else "",
                        f"{np.median(lam):.3f}" if len(lam) else ""])
    print(f"[{time.time()-t0:6.1f}s] wrote {tables/'mc_deep.csv'}")

    # Machine-readable import-decay sweep: previously these shares existed
    # only in the figure, so the manuscript's quoted values were uncommitted.
    with open(tables / "import_decay_deep.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["set", "env", "decay_efolding_years",
                    "share_expanding_at_30", "n_runs"])
        for key, (grid, ps) in sorted(curves.items()):
            set_name, env = key.split("/")
            for d, p in zip(grid, ps):
                w.writerow([set_name, env, f"{d:g}", f"{p:.4f}", 60])
    print(f"[{time.time()-t0:6.1f}s] wrote {tables/'import_decay_deep.csv'}")

    figures.append(survival_curves([m for m in mcs if m.environment == "lunar"],
                                   fname="survival_deep_lunar.png"))
    figures.append(survival_curves([m for m in mcs if m.label == "central"],
                                   fname="survival_deep_central.png"))
    figures.append(decay_sweep(curves, horizon=30, fname="import_decay_sweep_deep.png"))

    # --- policy robustness + sensitivity (r3.3 review requirements) ---------
    extra = ["\n## Allocation-policy robustness (paired draws, shocks off)\n"]
    for env, pc in pol_results:
        extra.append(f"**central/{env}** (n={pc.n_runs}): "
                     + " | ".join(f"{pol}: {k}/{pc.n_runs} expanding"
                                  for pol, (k, _, _, _) in pc.results.items()))
        print(f"[{time.time()-t0:6.1f}s] policies central/{env}: "
              + ", ".join(f"{pol}={k}/{pc.n_runs}"
                          for pol, (k, _, _, _) in pc.results.items()))
        tops = {pol: (sec, share) for pol, (_, _, sec, share) in pc.results.items()}
        extra.append("  co-binding credit (same 1% finite-response definition "
                     "as the baseline): "
                     + " | ".join(f"{pol}: {sec} {share:.0%}"
                                  for pol, (sec, share) in tops.items()))
    extra.append("\nReceding-horizon lookahead reproduces the myopic maximin; the "
                 "aggregate-growth-with-floor policy collapses. The maximin "
                 "allocation is load-bearing, not incidental.\n")

    extra.append("\n## Import-decay e-folding sweep (central set, n=60 per point)\n")
    extra.append("Share of runs with realized g > 0 at year 30 vs the e-folding "
                 "time of Earth-supply withdrawal (machine-readable: "
                 "`tables/import_decay_deep.csv`). At n=60 per point the "
                 "non-monotonic wobble is within binomial noise; the sweep is "
                 "suggestive, not a stable response curve:\n")
    for key, (grid, ps) in sorted(curves.items()):
        extra.append(f"- **{key}**: "
                     + ", ".join(f"{d:g} yr -> {p:.2f}"
                                 for d, p in zip(grid, ps)))

    extra.append("\n## Scalar-anchor sensitivity screening "
                 "(Spearman rho of anchor draw vs g at year 30)\n")
    null_band = 1.96 / (300 ** 0.5)
    extra.append(f"central/lunar, n=300, null band ~ +/-{null_band:.2f} "
                 "(wider under multiplicity):\n")
    for name, rg, re_ in sens.ranked(8):
        extra.append(f"- `{name}`: rho_g30 = {rg:+.2f}, rho_expand = {re_:+.2f}")
        print(f"[{time.time()-t0:6.1f}s] sens {name}: {rg:+.2f}")

    rep = write_report(results, mcs + mcs_auto, cuts, figures,
                       provenance_of=load_params("central", env="lunar"),
                       path=OUTDIR / "report_deep.md", cut_probs=cut_probs)
    with open(rep, "a") as f:
        f.write("\n".join(extra) + "\n")
    print(f"[{time.time()-t0:6.1f}s] report: {rep}")


if __name__ == "__main__":
    main()
