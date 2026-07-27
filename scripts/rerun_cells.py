"""r3.4: rerun the nine headline cells with the doubling-denominator split.

Writes outputs/tables/mc_deep.csv with ever-doubled AND survivor-conditioned
doubling columns. Same seeds as run_deep.py, so the expansion counts match.
"""
import csv
import sys
import time
import zlib
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rsimodel.montecarlo import ensemble
from rsimodel.report import OUTDIR

t0 = time.time()
tables = OUTDIR / "tables"
tables.mkdir(parents=True, exist_ok=True)

rows = []
for set_name in ("conservative", "central", "optimistic"):
    for env in ("leo", "lunar", "mars"):
        mc = ensemble(set_name, env, n_runs=400, years=35, horizon=30,
                      seed=zlib.crc32(f"{set_name}/{env}".encode()))
        d_all = np.array(mc.doubling_times)
        d_srv = np.array(mc.doubling_times_survivors)
        lo, hi = mc.expanding_ci
        top = max(mc.binding_hist.items(), key=lambda kv: kv[1])
        rows.append([
            mc.label, mc.environment, mc.n_expanding, mc.n_runs,
            f"{mc.p_expanding:.4f}", f"{lo:.4f}", f"{hi:.4f}",
            len(d_all),
            f"{np.median(d_all):.2f}" if len(d_all) else "",
            f"{np.percentile(d_all, 25):.2f}" if len(d_all) else "",
            f"{np.percentile(d_all, 75):.2f}" if len(d_all) else "",
            len(d_srv),
            f"{np.median(d_srv):.2f}" if len(d_srv) else "",
            f"{np.percentile(d_srv, 25):.2f}" if len(d_srv) else "",
            f"{np.percentile(d_srv, 75):.2f}" if len(d_srv) else "",
            top[0], f"{top[1]:.3f}",
        ])
        print(f"[{time.time()-t0:6.1f}s] {mc.summary()} | ever-doubled "
              f"{len(d_all)}/400, survivor-doubled {len(d_srv)}/400")

with open(tables / "mc_deep.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["set", "env", "n_expanding", "n_runs", "share", "ci95_lo",
                "ci95_hi", "n_ever_doubled", "dbl_all_med", "dbl_all_q25",
                "dbl_all_q75", "n_survivor_doubled", "dbl_srv_med",
                "dbl_srv_q25", "dbl_srv_q75", "top_binding_sector",
                "top_binding_share"])
    w.writerows(rows)
print(f"[{time.time()-t0:6.1f}s] wrote {tables/'mc_deep.csv'}")
