"""Deep Monte Carlo run: larger ensembles, sampled-anchor cut probabilities.

Runtime ~15-25 min (all statistics, no shortcuts). Writes outputs/report_deep.md.
Use run_baseline.py for the fast smoke sweep.
"""
import sys
import time
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rsimodel import load_params, run
from rsimodel.cutsets import cut_probability, find_cut_sets
from rsimodel.montecarlo import ensemble, sweep_import_decay
from rsimodel.plots import decay_sweep, survival_curves
from rsimodel.report import OUTDIR, write_report

t0 = time.time()
SETS = ("conservative", "central", "optimistic")
ENVS = ("leo", "lunar", "mars")
figures = []

results = {(s, e): run(load_params(s, env=e), years=40)
           for s in SETS for e in ENVS}
print(f"[{time.time()-t0:6.1f}s] deterministic grid done")

# --- large ensembles: every set x env ------------------------------------
mcs = []
for set_name in SETS:
    for env in ENVS:
        mc = ensemble(set_name, env, n_runs=400, years=35, horizon=30,
                      seed=zlib.crc32(f"{set_name}/{env}".encode()))
        mcs.append(mc)
        print(f"[{time.time()-t0:6.1f}s] MC {mc.summary()}")

# machine-readable headline table
import csv
tables = OUTDIR / "tables"
tables.mkdir(parents=True, exist_ok=True)
with open(tables / "mc_deep.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["set", "env", "n_expanding", "n_runs", "share", "ci95_lo",
                "ci95_hi", "n_ever_doubled", "dbl_all_med", "dbl_all_q25",
                "dbl_all_q75", "n_survivor_doubled", "dbl_srv_med",
                "dbl_srv_q25", "dbl_srv_q75", "top_binding_sector",
                "top_binding_share"])
    import numpy as np
    for mc in mcs:
        lo, hi = mc.expanding_ci
        d = np.array(mc.doubling_times)
        ds = np.array(mc.doubling_times_survivors)
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
                    top[0], f"{top[1]:.3f}"])
print(f"[{time.time()-t0:6.1f}s] wrote {tables/'mc_deep.csv'}")
figures.append(survival_curves([m for m in mcs if m.environment == "lunar"],
                               fname="survival_deep_lunar.png"))
figures.append(survival_curves([m for m in mcs if m.label == "central"],
                               fname="survival_deep_central.png"))

# --- decay sweep, larger n ------------------------------------------------
curves = {}
for env in ("lunar", "leo"):
    grid, ps = sweep_import_decay("central", env, n_runs=60, years=35, horizon=30)
    curves[f"central/{env}"] = (grid, ps)
    print(f"[{time.time()-t0:6.1f}s] decay sweep central/{env}: "
          + ", ".join(f"{d:g}yr->{p:.2f}" for d, p in zip(grid, ps)))
figures.append(decay_sweep(curves, horizon=30, fname="import_decay_sweep_deep.png"))

# --- cut-set fatality over sampled anchors --------------------------------
cut_probs = []
for set_name, env in (("central", "lunar"), ("central", "leo"),
                      ("central", "mars"), ("optimistic", "lunar")):
    cp = cut_probability(set_name, env, n_runs=40, horizon=30, dt=0.5,
                         seed=zlib.crc32(f"{set_name}/{env}/cp".encode()))
    cut_probs.append(cp)
    top = sorted(cp.p_fatal.items(), key=lambda kv: -kv[1])[:2]
    print(f"[{time.time()-t0:6.1f}s] cutP {set_name}/{env}: base={cp.p_baseline:.2f} | "
          + " | ".join(f"{('ALL' if len(c) > 1 else c[0])}:{p:.2f}" for c, p in top))

# central-value cut sets for the same report
cuts = {f"central/{env}": find_cut_sets(load_params("central", env=env),
                                        horizon=30, dt=0.5)
        for env in ("lunar", "leo")}
print(f"[{time.time()-t0:6.1f}s] central-value cut sets done")

# --- policy robustness + sensitivity (r3.3 review requirements) -----------
from rsimodel.montecarlo import sensitivity
from rsimodel.policies import compare_policies

extra = ["\n## Allocation-policy robustness (paired draws, shocks off)\n"]
for env in ("lunar", "leo"):
    pc = compare_policies("central", env, n_runs=30, seed=11)
    extra.append(f"**central/{env}** (n={pc.n_runs}): "
                 + " | ".join(f"{pol}: {k}/{pc.n_runs} expanding"
                              for pol, (k, _, _, _) in pc.results.items()))
    print(f"[{time.time()-t0:6.1f}s] policies central/{env}: "
          + ", ".join(f"{pol}={k}/{pc.n_runs}"
                      for pol, (k, _, _, _) in pc.results.items()))
extra.append("\nReceding-horizon lookahead reproduces the myopic maximin; the "
             "aggregate-growth-with-floor policy collapses. The maximin "
             "allocation is load-bearing, not incidental.\n")

extra.append("\n## Global sensitivity (Spearman rho of anchor draw vs g@30yr)\n")
sens = sensitivity("central", "lunar", n_runs=300, seed=5)
null_band = 1.96 / (300 ** 0.5)
extra.append(f"central/lunar, n=300, null band ~ +/-{null_band:.2f} "
             "(wider under multiplicity):\n")
for name, rg, re_ in sens.ranked(8):
    extra.append(f"- `{name}`: rho_g30 = {rg:+.2f}, rho_expand = {re_:+.2f}")
    print(f"[{time.time()-t0:6.1f}s] sens {name}: {rg:+.2f}")

rep = write_report(results, mcs, cuts, figures,
                   provenance_of=load_params("central", env="lunar"),
                   path=OUTDIR / "report_deep.md", cut_probs=cut_probs)
with open(rep, "a") as f:
    f.write("\n".join(extra) + "\n")
print(f"[{time.time()-t0:6.1f}s] report: {rep}")
