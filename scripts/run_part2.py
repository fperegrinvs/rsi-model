"""Part II sweep: references plus current and aspirational AI1 vs responding Earth.

Central values, anchored MC, a quarantined deterministic aspiration case,
break-even distributions, crossover surface. Runtime ~1 min.
Writes outputs/report_part2.md.
"""
import sys
import time
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from rsimodel.lco import (CASES, MONTE_CARLO_CASES, AnchorSet,
                          breakeven_launch_price, crossover_grid, lco_earth,
                          lco_mc, lco_space, orbital_ai_scale)
from rsimodel.plots import crossover_contours, lco_composition, ratio_distributions
from rsimodel.report import write_part2_report

t0 = time.time()
figures = []

spaces = {c: lco_space(c, architecture="serviceable_platform")
          for c in CASES}
spaces.update({
    f"{c}_disposable": lco_space(c, architecture="integrated_disposable")
    for c in MONTE_CARLO_CASES
})
earths = {s: lco_earth(s) for s in ("tight", "base", "responsive")}
for c, s in spaces.items():
    print(f"{c:<28}: {s.lco:>10,.0f} $/kW-yr | "
          f"{s.architecture} | launched {s.mass_kg_per_kw:>4,.0f} kg/kW")
for scen, e in earths.items():
    print(f"earth/{scen:<10}: {e.lco:>10,.0f} $/kW-yr | node={e.node}")
plot_spaces = {
    key: value for key, value in spaces.items()
    if key in (
        "leo_inference", "leo_inference_disposable",
        "cislunar_batch", "lunar_surface",
        "starmind_ai1", "starmind_ai1_disposable",
        "starmind_ai1_aspirational",
    )
}
figures.append(lco_composition(plot_spaces, earths))

mcs = []
for case in MONTE_CARLO_CASES:
    for architecture in ("serviceable_platform", "integrated_disposable"):
        for scen in ("base", "responsive"):
            # crc32, not hash(): built-in hashing is process-salted, so
            # hash()-based seeds made every run nondeterministic.
            tag = f"{case}/{architecture}/{scen}"
            m = lco_mc(
                case, scen, n=2000, architecture=architecture,
                seed=zlib.crc32(tag.encode()),
            )
            mcs.append(m)
            print(f"[{time.time()-t0:5.1f}s] MC {tag}: "
                  f"ratio p50={m.ratio_pcts[50]:.1f}, "
                  f"P(space cheaper)={m.p_space_cheaper:.3f}")
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
    # the paper's efficiency boundary: off Earth, chip efficiency is a MASS multiplier (launch tax
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
                           "power_systems.radiator_kg_per_kw": 3.0}),
    life_years=7.0)
FAVORABLE = {"compute.space_qual_multiplier": 1.2,
             "compute.utilization_leo": 0.95,
             "power_systems.radiator_kg_per_kw": 3.0}
s250 = lco_space("leo_inference", launch_per_kg_leo=250.0)
s250_fav = lco_space("leo_inference", a=AnchorSet(overrides=FAVORABLE),
                     launch_per_kg_leo=250.0, life_years=7.0)
e_base = earths["base"].lco
ai1 = spaces["starmind_ai1"]
ai1_disposable = spaces["starmind_ai1_disposable"]
leo_serviceable = spaces["leo_inference"]
leo_disposable = spaces["leo_inference_disposable"]
ai1_250 = lco_space("starmind_ai1", launch_per_kg_leo=250.0)
ai1_be = breakeven_launch_price("starmind_ai1", e_base)
ai1_fav = lco_space("starmind_ai1", a=AnchorSet(overrides=FAVORABLE),
                    life_years=7.0)
ai1_fav_250 = lco_space("starmind_ai1", a=AnchorSet(overrides=FAVORABLE),
                        launch_per_kg_leo=250.0, life_years=7.0)
ai1_fav_be = breakeven_launch_price(
    "starmind_ai1", e_base, a=AnchorSet(overrides=FAVORABLE), life_years=7.0)
ai1_mass_entry = AnchorSet().anchors["starmind.vehicle_mass_kg_per_average_kw"]
ai1_asp = spaces["starmind_ai1_aspirational"]
ai1_asp_incomplete = lco_space(
    "starmind_ai1_aspirational",
    complete_costs=False,
)
# Isolate what the explicit company targets do before supplying the three
# unpublished favorable bounds that make the named best case optimistic.
central_unknowns = AnchorSet()
ai1_asp_company_only = lco_space(
    "starmind_ai1_aspirational",
    a=AnchorSet(overrides={
        "aspirations.starmind_qualification_multiplier":
            central_unknowns("compute.space_qual_multiplier"),
        "aspirations.starmind_life_years":
            central_unknowns("compute.life_years_space"),
        "aspirations.starmind_utilization":
            central_unknowns("compute.utilization_leo"),
    }),
)
# Scale arithmetic for SpaceX's own 100-GW/year long-term target. These are
# implications of the targets, not predictions that cadence is attainable.
asp_anchors = AnchorSet()
asp_gw = asp_anchors("aspirations.orbital_compute_gw_per_year")
asp_eff = asp_anchors("aspirations.starmind_vehicle_efficiency_kw_per_tonne")
v3_t = asp_anchors("aspirations.starship_v3_payload_tonnes")
v4_t = asp_anchors("aspirations.starship_v4_payload_tonnes")
ai1_avg_kw = asp_anchors("starmind.compute_payload_kw_average")
scale_v3 = orbital_ai_scale(asp_gw, asp_eff, v3_t, ai1_avg_kw)
scale_v4 = orbital_ai_scale(asp_gw, asp_eff, v4_t, ai1_avg_kw)
scale_current_eff = orbital_ai_scale(
    asp_gw, asp_anchors("starmind.vehicle_efficiency_kw_per_tonne"),
    v3_t, ai1_avg_kw)
asp_launch_bill = (
    scale_v3["mass_tonnes"] * 1000.0
    * asp_anchors("aspirations.starship_leo_cost_per_kg")
)
ai1_be_text = (
    f"its central break-even launch price is {ai1_be:,.0f} $/kg"
    if ai1_be >= 0 else
    f"its fixed non-launch costs still exceed Earth base "
    f"(break-even {ai1_be:,.0f} $/kg)"
)
ai1_fav_be_text = (
    f"breaks even at {ai1_fav_be:,.0f} $/kg"
    if ai1_fav_be >= 0 else
    f"has no positive break-even launch price ({ai1_fav_be:,.0f} $/kg)"
)
# chip-efficiency vs launch-price channel comparison, computed (no hardcoded
# ratios: they went stale when the cost structure changed — current)
r_3000 = lco_space("leo_inference", launch_per_kg_leo=3000.0).lco / e_base
r_eff2 = lco_space("leo_inference", launch_per_kg_leo=3000.0,
                   chip_efficiency_advantage=2.0).lco / e_base
r_half = lco_space("leo_inference", launch_per_kg_leo=1500.0).lco / e_base
eff_frac = (r_3000 - r_eff2) / (r_3000 - r_half)
pub_lo, pub_hi = 1400.0, 4000.0            # published $/kg band (anchors.yaml)
below = (f"~{pub_lo / be_best:,.0f}-{pub_hi / be_best:,.0f}x below published prices"
         if be_best > 0 else "below any positive launch price (negative break-even)")
notes = (
    "**Architecture split** — the serviceable/reusable-platform baseline is "
    f"{leo_serviceable.lco / e_base:.2f}x Earth base for generic LEO and "
    f"{ai1.lco / e_base:.2f}x for the AI1 disclosure scenario. The integrated "
    "disposable-satellite baseline, in which infrastructure and compute retire "
    f"together, is {leo_disposable.lco / e_base:.2f}x and "
    f"{ai1_disposable.lco / e_base:.2f}x, respectively. Modularity supports "
    "standardisation but does not establish in-orbit replacement; neither "
    "architecture is silently treated as demonstrated.\n\n"
    "**Starmind AI1 disclosure scenario** — SpaceX publishes 150 kW peak / "
    "120 kW average compute, a 150 kW array, and 70 kW/tonne vehicle efficiency "
    "(official Starmind page, accessed 2026-07-27; provenance snapshot in "
    "`docs/sources/starmind-ai1-2026-07-27.md`). The model uses the 1.25 "
    "array/average-load ratio and, because SpaceX does not say whether the "
    "efficiency numerator is peak or average, samples "
    f"{ai1_mass_entry['low']:.1f}-{ai1_mass_entry['high']:.1f} kg per average kW "
    f"(central {ai1.mass_kg_per_kw:.1f}, versus "
    f"{spaces['leo_inference'].mass_kg_per_kw:.1f} kg/kW generic LEO). At current "
    f"central launch and retained cost/life/availability anchors, the "
    f"serviceable-platform AI1 case is "
    f"{ai1.lco / e_base:.2f}x Earth base; at $250/kg it is "
    f"{ai1_250.lco / e_base:.2f}x, and {ai1_be_text}. The mass disclosure therefore "
    "materially lowers the launch term but does not resolve the qualification, "
    "hardware-cost, lifetime, or availability gates. With the remaining anchors "
    "simultaneously favorable (qualification x1.2, seven-year life, 0.95 "
    f"utilization), AI1 becomes {ai1_fav.lco / e_base:.2f}x at central launch, "
    f"{ai1_fav_be_text}, and reaches {ai1_fav_250.lco / e_base:.2f}x at "
    "$250/kg. Completing communications, bus, NRE, insurance, spectrum, "
    "disposal, thermal-margin, and financing terms removes the formerly "
    "reported favorable-corner crossover. "
    "Radiator area, dimensions, "
    "redundant loops, debris shielding, and laser links are recorded but do not "
    "receive invented costs where the page supplies none.\n\n"
    "**Aspirational best case (deterministic; excluded from Monte Carlo)** — "
    "SpaceX's EU prospectus says it aims to cut its stated historical launch "
    "cost of $18,500/kg by 99% or more, so the model uses $185/kg as the exact "
    "99%-reduction ceiling; it also uses the prospectus's long-term 100 kW/t "
    "deployment assumption (10 kg per average kW). Those two company targets "
    f"alone, while leaving unpublished inputs at their central values, yield "
    f"{ai1_asp_company_only.lco:,.0f} $/kW-yr or "
    f"{ai1_asp_company_only.lco / e_base:.2f}x Earth base. The displayed "
    f"best case additionally selects the favorable, NON-COMPANY bounds of 1.2x "
    f"qualification, seven-year hardware life, and 0.95 utilization; it yields "
    f"{ai1_asp.lco:,.0f} $/kW-yr or {ai1_asp.lco / e_base:.2f}x Earth base. "
    f"The earlier incomplete-cost form would have produced "
    f"{ai1_asp_incomplete.lco / e_base:.2f}x; the completed boundary is "
    "therefore a direct reversal, not a small adjustment. The model assigns "
    "the aspirational case no success probability: targets and favorable "
    "analyst assumptions are point values, not empirical distributions.\n\n"
    "**Feasibility audit of that best case** — the latest AI1 page's 70 kW/t "
    "is 30% below the older 100 kW/t scale assumption (reaching the target "
    "requires 43% more kW/t than AI1). At 100 GW deployed per year, 100 kW/t "
    f"implies {scale_v3['mass_tonnes']/1e6:.2f} million tonnes/year, about "
    f"{scale_v3['launches_per_year']:,.0f} full 100-t V3 launches/year "
    f"({scale_v3['launches_per_day']:.1f}/day) or "
    f"{scale_v4['launches_per_year']:,.0f} full 200-t V4 launches/year "
    f"({scale_v4['launches_per_day']:.1f}/day), plus roughly "
    f"{scale_v3['spacecraft_count']:,.0f} 120-kW spacecraft. At AI1's disclosed "
    f"70 kW/t the mass rises to {scale_current_eff['mass_tonnes']/1e6:.2f} "
    f"million tonnes and {scale_current_eff['launches_per_year']:,.0f} V3 "
    f"launches/year. Even at $185/kg, the 100-kW/t flow corresponds to "
    f"${asp_launch_bill/1e9:,.0f} billion/year of launch cost before spacecraft "
    "manufacture. Full rapid reuse and this cadence are therefore load-bearing; "
    "so are seven-year whole-system reliability and 95% compute utilization, "
    "neither of which SpaceX publishes for AI1. Communications/downlink, ground "
    "network, spacecraft-bus functions, program NRE, insurance, spectrum and "
    "regulatory cost, disposal, residual value, thermal margins, and separate "
    "space financing are now explicit wide-bound terms. Collision externalities, "
    "constellation replenishment logistics, and landing/turnaround infrastructure "
    "remain outside the LCO, while the Earth alternative can also improve. The "
    "case is useful as a boundary: it shows what must all go right, not what is "
    "likely to happen.\n\n"
    "**Sensitivity probe** — everything favorable *within* the anchored ranges at once "
    "(qual x1.2, utilization 0.95, radiator 3 kg/kW, life 7 yr): LEO space LCO becomes "
    f"{s_best.lco:,.0f} $/kW-yr at central launch prices, and the break-even launch price "
    f"becomes {be_best:,.0f} $/kg — {below}. The completed fixed-cost boundary "
    "therefore prevents parity even at zero launch price in this favorable "
    "single-axis corner; further architectural changes, not launch alone, are "
    "required.\n\n"
    "**External claim check** — a Google/Planet study (reported by Will Marshall, "
    "Moonshots #266, June 2026; recorded as `claims.google_planet_crossover_launch_per_kg`, "
    "company_statement, never a model input) puts the crossover at $200-300/kg to LEO. "
    f"In our model, $250/kg at central anchors gives space/Earth = {s250.lco / e_base:.2f} "
    f"(no crossover); with the favorable corner above it gives {s250_fav.lco / e_base:.2f}. "
    "The claim is not reproduced after the omitted-cost boundary is completed, "
    "even with COTS-class qualification (~1.2x), ~7-yr life, and ~0.95 "
    "utilization simultaneously. The disagreement is therefore architectural "
    "and accounting-wide, not a launch-price threshold alone.\n\n"
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
    "the chip-efficiency panel of the crossover figure (the paper's efficiency boundary: efficiency is a "
    "mass multiplier off Earth — the 'launch tax vs Nvidia tax' argument made "
    "quantitative). Our refinement of that argument: at anchored values a 2x FLOPS/W "
    f"advantage buys ~{eff_frac:.0%} of the benefit of halving launch price (ratio "
    f"{r_eff2:.1f} vs {r_half:.1f} at $3,000/kg, both from {r_3000:.1f}), because the "
    "hardware term — which efficiency does not touch — "
    "is the larger share of both mass and capex. The mass-multiplier mechanism is real "
    "but subdominant to the hardware cost channel at central anchors; efficiency "
    "dominance emerges only after the qualification premium and hw $/kW fall.")
print(notes)

rep = write_part2_report(spaces, earths, mcs, figures, breakeven_notes=notes)
print(f"[{time.time()-t0:5.1f}s] report: {rep}")
