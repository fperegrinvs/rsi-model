"""Part II sweep: three space reference cases vs a responding Earth.

Central values, anchored MC, break-even distributions, crossover surface.
Runtime ~1 min. Writes outputs/report_part2.md.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from rsimodel.lco import (CASES, AnchorSet, breakeven_launch_price,
                          crossover_grid, lco_earth, lco_mc, lco_space)
from rsimodel.plots import crossover_contours, lco_composition, ratio_distributions
from rsimodel.report import write_part2_report

t0 = time.time()
figures = []

spaces = {c: lco_space(c) for c in CASES}
earths = {s: lco_earth(s) for s in ("tight", "base", "responsive")}
for c, s in spaces.items():
    print(f"{c:<15}: {s.lco:>10,.0f} $/kW-yr | launched {s.mass_kg_per_kw:>4,.0f} kg/kW")
for scen, e in earths.items():
    print(f"earth/{scen:<10}: {e.lco:>10,.0f} $/kW-yr | node={e.node}")
figures.append(lco_composition(spaces, earths))

mcs = []
for case in CASES:
    for scen in ("base", "responsive"):
        m = lco_mc(case, scen, n=2000, seed=hash((case, scen)) % 2**31)
        mcs.append(m)
        print(f"[{time.time()-t0:5.1f}s] MC {case}/{scen}: "
              f"ratio p50={m.ratio_pcts[50]:.1f}, P(space cheaper)={m.p_space_cheaper:.3f}")
figures.append(ratio_distributions([m for m in mcs if m.scenario == "base"]))

# --- crossover surface ----------------------------------------------------
lp = np.geomspace(20, 5000, 60)
e_base = earths["base"].lco
panels = {
    "LEO: equipment life": (lp, np.linspace(3, 12, 40),
                            crossover_grid("leo_inference", lp, "life_years",
                                           np.linspace(3, 12, 40), e_base), "life (years)"),
    "LEO: space-qual multiplier": (lp, np.linspace(1.0, 3.0, 40),
                                   crossover_grid("leo_inference", lp,
                                                  "compute.space_qual_multiplier",
                                                  np.linspace(1.0, 3.0, 40), e_base),
                                   "hw cost multiplier"),
    "LEO: radiator mass": (lp, np.linspace(1, 15, 40),
                           crossover_grid("leo_inference", lp,
                                          "power_systems.radiator_kg_per_kw",
                                          np.linspace(1, 15, 40), e_base), "kg/kW"),
    "Lunar: closure fraction": (lp, np.linspace(0, 0.95, 40),
                                crossover_grid("lunar_surface", lp, "closure_fraction",
                                               np.linspace(0, 0.95, 40), e_base),
                                "non-hw mass closed locally"),
    # r2.10 §16: off Earth, chip efficiency is a MASS multiplier (launch tax
    # vs Nvidia tax — the two enter the crossover multiplicatively)
    "LEO: chip efficiency": (lp, np.linspace(0.5, 4.0, 40),
                             crossover_grid("leo_inference", lp,
                                            "chip_efficiency_advantage",
                                            np.linspace(0.5, 4.0, 40), e_base),
                             "FLOPS/W vs reference (x)"),
}
figures.append(crossover_contours(panels))
print(f"[{time.time()-t0:5.1f}s] crossover surface done")

# what actually moves the answer: joint best-case-within-anchors probe
best = AnchorSet(overrides={"compute.space_qual_multiplier": 1.2,
                            "compute.utilization_leo": 0.95,
                            "power_systems.radiator_kg_per_kw": 3.0})
s_best = lco_space("leo_inference", a=best, life_years=7.0)
be_best = breakeven_launch_price(
    "leo_inference", earths["base"].lco,
    a=AnchorSet(overrides={"compute.space_qual_multiplier": 1.2,
                           "compute.utilization_leo": 0.95,
                           "power_systems.radiator_kg_per_kw": 3.0}))
FAVORABLE = {"compute.space_qual_multiplier": 1.2,
             "compute.utilization_leo": 0.95,
             "power_systems.radiator_kg_per_kw": 3.0}
s250 = lco_space("leo_inference", launch_per_kg_leo=250.0)
s250_fav = lco_space("leo_inference", a=AnchorSet(overrides=FAVORABLE),
                     launch_per_kg_leo=250.0, life_years=7.0)
e_base = earths["base"].lco
notes = (
    "**Sensitivity probe** — everything favorable *within* the anchored ranges at once "
    "(qual x1.2, utilization 0.95, radiator 3 kg/kW, life 7 yr): LEO space LCO becomes "
    f"{s_best.lco:,.0f} $/kW-yr at central launch prices, and the break-even launch price "
    f"becomes {be_best:,.0f} $/kg — at the bottom edge of the aspirational-target band "
    "($30-150/kg, company statements) and ~50-100x below published prices. Crossover "
    "therefore requires the UNANCHORED qual/life/util corner AND the most aggressive "
    "target-class launch prices simultaneously; no single anchored number gets there.\n\n"
    "**External claim check** — a Google/Planet study (reported by Will Marshall, "
    "Moonshots #266, June 2026; recorded as `claims.google_planet_crossover_launch_per_kg`, "
    "company_statement, never a model input) puts the crossover at $200-300/kg to LEO. "
    f"In our model, $250/kg at central anchors gives space/Earth = {s250.lco / e_base:.2f} "
    f"(no crossover); with the favorable corner above it gives {s250_fav.lco / e_base:.2f}. "
    "The claim is therefore reproducible here only under COTS-class qualification (~1.2x), "
    "~7-yr life, and ~0.95 utilization SIMULTANEOUSLY — assumptions consistent with "
    "Planet's own practice of flying unmodified Nvidia GPUs at LEO "
    "(docs/transcripts/moonshots-266-2026-06-26.md). The disagreement between the claim "
    "and our central result is not about launch price at all; it is about the "
    "qualification premium, equipment life, and utilization.\n\n"
    "The published Suncatcher design study (arXiv:2511.19468v2, 2026-06-17; "
    "`claims.suncatcher_launch_feasibility_per_kg`, technical_report) is a "
    "LAUNCH-COST FEASIBILITY MARKER, not a crossover claim — its own text says "
    "twice it is not a full economic analysis: at $200/kg it compares amortized "
    "launch cost per kW-yr against terrestrial electricity spend only, excluding "
    "infrastructure, buildings, and chips. Launch-vs-electricity is not "
    "system-vs-system; this model supplies the missing system-level comparison, "
    "and its negative break-evens quantify exactly what the launch-only framing "
    "omits. On radiation: the proton-beam results SUPPORT 5-yr TID survivability "
    "with margin (HBM irregularities from ~2 krad vs ~750 rad 5-yr requirement; "
    "no hard failures to 15 krad) and do not contradict 7-yr TID; what they do "
    "not establish is 7-yr SYSTEM reliability — SEE-induced corruption (core "
    "logic/SRAM most sensitive), training-workload impact (reserved by the "
    "authors), thermal, and whole-spacecraft failure remain unresolved. Note also "
    "the chip-efficiency panel of the crossover figure (r2.10 §16: efficiency is a "
    "mass multiplier off Earth — the 'launch tax vs Nvidia tax' argument made "
    "quantitative). Our refinement of that argument: at anchored values a 2x FLOPS/W "
    "advantage buys only ~2/3 of the benefit of halving launch price (ratio 4.7 vs "
    "3.8 at $3,000/kg), because the hardware term — which efficiency does not touch — "
    "is the larger share of both mass and capex. The mass-multiplier mechanism is real "
    "but subdominant to the hardware cost channel at central anchors; efficiency "
    "dominance emerges only after the qualification premium and hw $/kW fall.")
print(notes)

rep = write_part2_report(spaces, earths, mcs, figures, breakeven_notes=notes)
print(f"[{time.time()-t0:5.1f}s] report: {rep}")
