# Part II report: levelized cost of compute, space vs Earth — 2026-07-27

Unit: **$ per frontier-equivalent kW-year of delivered IT load** (older-node
hardware is compute-normalized by its J/FLOP penalty). Three reference cases
(paper Section 9): LEO inference, cislunar batch, and **Earth-supplied**
lunar-surface compute (central closure fraction is zero — local manufacture
enters only through the closure sweep axis), plus separate Starmind AI1
current-disclosure and aspirational-best-case scenarios.
Two architectures are reported explicitly. In the integrated-disposable
satellite, compute, PV, radiator, storage, structure, and original launch
retire together. In the serviceable/reusable platform, compute refreshes
separately while infrastructure and its original launch spend amortize on
the longer `infrastructure_life_years`; this is a scenario assumption, not
an inference from modularity alone.
The Earth counterfactual RESPONDS: the responsive scenario prices induced
supply at the nuclear-PPA floor and may deploy older-node hardware.
Aspirational launch targets appear as sweep axes and in one explicitly labeled,
deterministic best-case sensitivity (rule 3); that case is excluded from Monte
Carlo and is not assigned a probability.
Shared draws both sides: each MC iteration resolves every anchor once per
draw-cached AnchorSet, so Earth and space see the same wacc and hardware cost.


## Complete levelized-cost specification

For WACC \(r\), useful life \(T\), and annual operations fraction \(f_o\),

\[
\operatorname{CRF}(r,T)=\frac{r}{1-(1+r)^{-T}},
\qquad
a(T)=\operatorname{CRF}(r,T)+f_o.
\]

Let \(C_h\) be qualified accelerator capex, \(C_I\) the sum of PV, radiator
and storage capex, \(M_h\) accelerator mass, \(M_I\) launched non-hardware
mass after local closure, \(\mu\) the destination launch multiplier,
\(p_L\) the LEO launch price, and \(U_s\) delivered utilization. The complete
space expression is

\[
L_s =
\frac{C_h a(T_h)+C_I a(T_I)
+p_L\mu[M_h a(T_h)+M_I a(T_I)]}{U_s}
=\alpha+\beta p_L.
\]

The integrated-disposable case sets \(T_I=T_h\): the power, thermal,
structure, compute, and original launch spend retire together. The
serviceable/reusable-platform case sets
\(T_I=\max(T_{I,\mathrm{anchor}},T_h)\) and therefore assumes compute
payload replacement without retiring the platform.

For Earth scenario \(e\), PUE \(\psi_e\), electricity price \(p_e\),
data-centre shell capex \(C_{DC}\), utilization \(U_E\), and the selected
node's frontier-equivalent penalty \(\phi_e\),

\[
L_E =
\frac{\phi_e\left[
C_{h,e}\operatorname{CRF}(r,T_{h,e})
+C_{DC}\operatorname{CRF}(r,15)
+8760\,p_e\psi_e\right]}{U_E}.
\]

The responsive Earth case evaluates both frontier and older-node hardware,
including the older node's energy/computational penalty, and selects the
lower \(L_E\). Communications and ground systems are excluded unless an
explicit anchor enters \(C_I\); the current cases do not invent such costs.
The exact affine break-even launch price is

\[
p_L^*=\frac{L_E-\alpha}{\beta},
\]

with a negative value meaning non-launch costs alone exceed the Earth
counterfactual.


For the central LEO serviceable-platform case, the resolved values are
\(C_h=63,640\), \(C_I=1,697\) $/kW,
\(M_h=17.3\), \(M_I=28.8\) kg/kW,
\(p_L=2,366\) $/kg,
\(a_h=0.3237\), \(a_I=0.1704\), and
\(U_s=0.786\). Substitution gives

\[
L_s =
\frac{63,640(0.3237)
+1,697(0.1704)
+2,366
[17.3(0.3237)
+28.8(0.1704)]}
{0.786}
= 58,264\ \$/\mathrm{kW\!-\!yr}.
\]



## Central references and deterministic aspiration case

Space cases (capex $/kW before annualization):

| case | architecture | LCO $/kW-yr | launched kg/kW | hardware | pv | radiator | storage | launch |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| leo_inference | serviceable/reusable platform | 58,264 | 46 | 63,640 | 1,173 | 524 | 0 | 109,205 |
| cislunar_batch | serviceable/reusable platform | 96,726 | 46 | 63,640 | 1,173 | 524 | 0 | 308,879 |
| lunar_surface (Earth-supplied) | serviceable/reusable platform | 2,773,476 | 454 | 63,640 | 2,580 | 524 | 11,726 | 9,599,021 |
| starmind_ai1 (company-statement scenario) | serviceable/reusable platform | 37,483 | 16 | 63,640 | 1,250 | 559 | 0 | 37,796 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | serviceable/reusable platform | 11,156 | 10 | 40,249 | 1,250 | 559 | 0 | 1,850 |
| leo_inference | integrated disposable satellite | 71,901 | 46 | 63,640 | 1,173 | 524 | 0 | 109,205 |
| cislunar_batch | integrated disposable satellite | 128,333 | 46 | 63,640 | 1,173 | 524 | 0 | 308,879 |
| lunar_surface (Earth-supplied) | integrated disposable satellite | 5,065,254 | 454 | 63,640 | 2,580 | 524 | 11,726 | 9,599,021 |
| starmind_ai1 (company-statement scenario) | integrated disposable satellite | 42,531 | 16 | 63,640 | 1,250 | 559 | 0 | 37,796 |

Earth scenarios:

| scenario | LCO $/kW-yr | node choice |
|---|---|---|
| tight | 15,980 | frontier |
| base | 14,669 | frontier |
| responsive | 12,783 | older |

A calibration check: the Earth base LCO corresponds to ≈ $1.67/kW-hr,
consistent with published accelerator rental rates — the model is anchored at
the right order of magnitude.


## Disclosed and aspirational scenario inputs

These company statements and separately source-classed model assumptions define conditional scenarios; they do not replace the generic reference cases or establish achieved cost, lifetime, or availability.

| case | disclosed/derived quantity | central value | source_class | model role |
|---|---|---:|---|---|
| starmind_ai1 (company-statement scenario) | `starmind.compute_payload_kw_peak` | 150 | company_statement | AI1 disclosed compute payload peak, kW. CONTEXT: not used as delivered-average model denominator; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 (company-statement scenario) | `starmind.compute_payload_kw_average` | 120 | company_statement | AI1 disclosed average compute payload, kW. USED with solar_array_kw to set the scenario's 1.25 array-power/average-compute ratio; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 (company-statement scenario) | `starmind.vehicle_efficiency_kw_per_tonne` | 70 | company_statement | AI1 disclosed vehicle efficiency, kW/tonne. The page does not state whether kW means peak or average; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 (company-statement scenario) | `starmind.vehicle_mass_kg_per_average_kw` | 15.97 | ASSUMPTION | DERIVED interpretation range from the disclosed 70 kW/tonne and 120 average / 150 peak kW: low assumes the efficiency numerator is average power (1000/70); high assumes it is peak power and converts total vehicle mass to an average-kW denominator ((150/70 t)/120 kW). USED as aggregate launched vehicle mass; the generic component budget supplies only the lifecycle split |
| starmind_ai1 (company-statement scenario) | `starmind.solar_array_kw` | 150 | company_statement | AI1 disclosed solar-array rating, kW. USED with average compute payload to set the 1.25 design power ratio; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 (company-statement scenario) | `starmind.solar_power_density_w_per_m2` | 250 | company_statement | AI1 disclosed solar power density, W/m^2. CONTEXT ONLY: the cost model prices PV per kW and the aggregate vehicle mass constraint already captures array mass; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 (company-statement scenario) | `starmind.radiator_area_m2` | 110 | company_statement | AI1 disclosed deployable liquid-radiator area, m^2. CONTEXT ONLY: no radiator areal mass or cost is disclosed, so the scenario retains the generic radiator cost and uses the aggregate vehicle mass constraint; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 (company-statement scenario) | `starmind.deployed_height_m` | 20 | company_statement | AI1 disclosed deployed height, m. CONTEXT ONLY; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 (company-statement scenario) | `starmind.wingspan_m` | 70 | company_statement | AI1 disclosed wingspan, m. CONTEXT ONLY; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `starmind.compute_payload_kw_peak` | 150 | company_statement | AI1 disclosed compute payload peak, kW. CONTEXT: not used as delivered-average model denominator; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `starmind.compute_payload_kw_average` | 120 | company_statement | AI1 disclosed average compute payload, kW. USED with solar_array_kw to set the scenario's 1.25 array-power/average-compute ratio; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `starmind.solar_array_kw` | 150 | company_statement | AI1 disclosed solar-array rating, kW. USED with average compute payload to set the 1.25 design power ratio; official Starmind page, accessed 2026-07-27 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.starmind_vehicle_efficiency_kw_per_tonne` | 100 | company_statement | LONG-TERM TARGET/ASSUMPTION in SpaceX scale arithmetic: 100 kW of AI compute per deployed tonne. The later AI1 product page discloses only 70 kW/t, 30% below this target. USED only in the aspirational deterministic sensitivity; EU Prospectus 2026-06-05, p. 82 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.starmind_vehicle_mass_kg_per_average_kw` | 10 | ASSUMPTION | DERIVED exactly as 1000 kg/t divided by the company-target 100 kW/t. USED as aggregate launched mass only in the aspirational deterministic sensitivity |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.starship_leo_cost_per_kg` | 185 | company_statement | TARGET, not achieved price: exact arithmetic ceiling from SpaceX's aim to reduce its stated historical $18,500/kg launch cost by 99% or more (0.01 x $18,500 = $185/kg). USED only in the aspirational deterministic sensitivity; EU Prospectus 2026-06-05, pp. 63, 70, 137 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.starship_v3_payload_tonnes` | 100 | company_statement | DESIGN TARGET: Starship V3 reusable payload capacity to orbit. CONTEXT ONLY for scale arithmetic; EU Prospectus 2026-06-05, pp. 71-72 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.starship_v4_payload_tonnes` | 200 | company_statement | FUTURE TARGET: possible Starship V4 reusable payload capacity to orbit. CONTEXT ONLY for scale arithmetic; EU Prospectus 2026-06-05, pp. 71-72 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.orbital_compute_gw_per_year` | 100 | company_statement | LONG-TERM TARGET: up to 100 GW of AI-compute power deployed to orbit annually. CONTEXT ONLY for scale arithmetic; EU Prospectus 2026-06-05, pp. 82, 97 |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.starmind_qualification_multiplier` | 1.2 | ASSUMPTION | FAVORABLE MODEL BOUND, not published by SpaceX: low end of compute.space_qual_multiplier. USED only in the aspirational deterministic sensitivity |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.starmind_life_years` | 7 | ASSUMPTION | FAVORABLE MODEL BOUND, not published by SpaceX: high end of compute.life_years_space. USED only in the aspirational deterministic sensitivity |
| starmind_ai1 aspirational best case (targets + favorable assumptions) | `aspirations.starmind_utilization` | 0.95 | ASSUMPTION | FAVORABLE MODEL BOUND, not achieved AI1 availability: high end of compute.utilization_leo. Starlink's reported network uptime is not evidence of AI1 spacecraft compute availability. USED only in the aspirational deterministic sensitivity |

## Monte Carlo over anchored ranges (shared draws both sides)

The aspirational best case is excluded: company targets and deliberately
favorable unpublished assumptions are point sensitivities, not probability
distributions.

| case | architecture | vs Earth | ratio p10/p50/p90 | P(space cheaper) | break-even LEO $/kg p50 (p90) |
|---|---|---|---|---|---|
| leo_inference | serviceable/reusable platform | base | 2.7 / 4.2 / 6.4 | 0.000 | -844 (-132) |
| leo_inference | serviceable/reusable platform | responsive | 3.3 / 5.1 / 8.2 | 0.000 | -1,035 (-339) |
| leo_inference | integrated disposable satellite | base | 3.3 / 5.1 / 8.2 | 0.000 | -606 (-124) |
| leo_inference | integrated disposable satellite | responsive | 3.9 / 6.3 / 10.4 | 0.000 | -764 (-239) |
| cislunar_batch | serviceable/reusable platform | base | 4.2 / 6.8 / 11.7 | 0.000 | -211 (17) |
| cislunar_batch | serviceable/reusable platform | responsive | 5.1 / 8.6 / 14.5 | 0.000 | -299 (-49) |
| cislunar_batch | integrated disposable satellite | base | 5.3 / 9.1 / 15.8 | 0.000 | -158 (12) |
| cislunar_batch | integrated disposable satellite | responsive | 6.4 / 11.5 / 19.8 | 0.000 | -216 (-41) |
| lunar_surface (Earth-supplied) | serviceable/reusable platform | base | 78.5 / 189.6 / 448.8 | 0.000 | -19 (-7) |
| lunar_surface (Earth-supplied) | serviceable/reusable platform | responsive | 98.3 / 240.8 / 570.9 | 0.000 | -21 (-8) |
| lunar_surface (Earth-supplied) | integrated disposable satellite | base | 144.4 / 354.2 / 887.2 | 0.000 | -12 (-5) |
| lunar_surface (Earth-supplied) | integrated disposable satellite | responsive | 186.5 / 448.2 / 1055.0 | 0.000 | -13 (-6) |
| starmind_ai1 (company-statement scenario) | serviceable/reusable platform | base | 1.8 / 2.6 / 3.9 | 0.000 | -2,555 (-524) |
| starmind_ai1 (company-statement scenario) | serviceable/reusable platform | responsive | 2.1 / 3.3 / 5.0 | 0.000 | -3,215 (-1,040) |
| starmind_ai1 (company-statement scenario) | integrated disposable satellite | base | 2.0 / 2.9 / 4.4 | 0.000 | -1,771 (-402) |
| starmind_ai1 (company-statement scenario) | integrated disposable satellite | responsive | 2.4 / 3.7 / 6.0 | 0.000 | -2,345 (-839) |

Break-even prices are the LEO $/kg at which the space case matches Earth;
**negative means fixed (non-launch) costs alone exceed the Earth cost** — at
those draws no launch price, even zero, closes the gap.

**Architecture split** — the serviceable/reusable-platform baseline is 3.97x Earth base for generic LEO and 2.56x for the AI1 disclosure scenario. The integrated disposable-satellite baseline, in which infrastructure and compute retire together, is 4.90x and 2.90x, respectively. Modularity supports standardisation but does not establish in-orbit replacement; neither architecture is silently treated as demonstrated.

**Starmind AI1 disclosure scenario** — SpaceX publishes 150 kW peak / 120 kW average compute, a 150 kW array, and 70 kW/tonne vehicle efficiency (official Starmind page, accessed 2026-07-27; provenance snapshot in `docs/sources/starmind-ai1-2026-07-27.md`). The model uses the 1.25 array/average-load ratio and, because SpaceX does not say whether the efficiency numerator is peak or average, samples 14.3-17.9 kg per average kW (central 16.0, versus 46.1 kg/kW generic LEO). At current central launch and retained cost/life/availability anchors, the serviceable-platform AI1 case is 2.56x Earth base; at $250/kg it is 1.89x, and its fixed non-launch costs still exceed Earth base (break-even -2,598 $/kg). The mass disclosure therefore materially lowers the launch term but does not resolve the qualification, hardware-cost, lifetime, or availability gates. With the remaining anchors simultaneously favorable (qualification x1.2, seven-year life, 0.95 utilization), AI1 becomes 1.28x at central launch, breaks even at 1,152 $/kg (just below the published $1,400-4,000/kg band), and reaches 0.79x at $250/kg. The disclosure thus moves the favorable-corner crossover from target-class launch prices to near the bottom of today's published band, but only conditionally on performance values SpaceX has not published. Radiator area, dimensions, redundant loops, debris shielding, and laser links are recorded but do not receive invented costs where the page supplies none.

**Aspirational best case (deterministic; excluded from Monte Carlo)** — SpaceX's EU prospectus says it aims to cut its stated historical launch cost of $18,500/kg by 99% or more, so the model uses $185/kg as the exact 99%-reduction ceiling; it also uses the prospectus's long-term 100 kW/t deployment assumption (10 kg per average kW). Those two company targets alone, while leaving unpublished inputs at their central values, yield 27,140 $/kW-yr or 1.85x Earth base. The displayed best case additionally selects the favorable, NON-COMPANY bounds of 1.2x qualification, seven-year hardware life, and 0.95 utilization; it yields 11,156 $/kW-yr or 0.76x Earth base. This is the first scenario here in which orbital AI is cheaper than the central Earth counterfactual, but the model assigns it no success probability: targets and favorable analyst assumptions are point values, not empirical distributions.

**Feasibility audit of that best case** — the latest AI1 page's 70 kW/t is 30% below the older 100 kW/t scale assumption (reaching the target requires 43% more kW/t than AI1). At 100 GW deployed per year, 100 kW/t implies 1.00 million tonnes/year, about 10,000 full 100-t V3 launches/year (27.4/day) or 5,000 full 200-t V4 launches/year (13.7/day), plus roughly 833,333 120-kW spacecraft. At AI1's disclosed 70 kW/t the mass rises to 1.43 million tonnes and 14,286 V3 launches/year. Even at $185/kg, the 100-kW/t flow corresponds to $185 billion/year of launch cost before spacecraft manufacture. Full rapid reuse and this cadence are therefore load-bearing; so are seven-year whole-system reliability and 95% compute utilization, neither of which SpaceX publishes for AI1. Regulatory approvals, spectrum, collision avoidance/debris mitigation, constellation replenishment, networking, insurance, program NRE, and landing/turnaround infrastructure remain outside the LCO, while the Earth alternative can also improve. The case is useful as a boundary: it shows what must all go right, not what is likely to happen.

**Sensitivity probe** — everything favorable *within* the anchored ranges at once (qual x1.2, utilization 0.95, radiator 3 kg/kW, life 7 yr): LEO space LCO becomes 31,660 $/kW-yr at central launch prices, and the break-even launch price becomes 444 $/kg — above the defined Starship aspiration/sensitivity band ($30-185/kg) but ~3-9x below published prices. The generic LEO reference therefore still requires the UNANCHORED qual/life/util corner plus launch below roughly $444/kg; the target band would clear that threshold but is more aggressive than necessary. The separate disclosed-mass AI1 scenario above moves the threshold materially closer to published prices.

**External claim check** — a Google/Planet study (reported by Will Marshall, Moonshots #266, June 2026; recorded as `claims.google_planet_crossover_launch_per_kg`, company_statement, never a model input) puts the crossover at $200-300/kg to LEO. In our model, $250/kg at central anchors gives space/Earth = 2.04 (no crossover); with the favorable corner above it gives 0.88. The claim is therefore reproducible here only under COTS-class qualification (~1.2x), ~7-yr life, and ~0.95 utilization SIMULTANEOUSLY — assumptions consistent with Planet's own practice of flying unmodified Nvidia GPUs at LEO (docs/transcripts/moonshots-266-2026-06-26.md). The disagreement between the claim and our central result is not about launch price at all; it is about the qualification premium, equipment life, and utilization.

The published Suncatcher design study (arXiv:2511.19468v2, 2026-06-17; `claims.suncatcher_launch_feasibility_per_kg`, technical_report) is a LAUNCH-COST FEASIBILITY MARKER, not a crossover claim — its own text says twice it is not a full economic analysis: at $200/kg it compares amortized launch cost per kW-yr against terrestrial electricity spend only, excluding infrastructure, buildings, and chips. Launch-vs-electricity is not system-vs-system; this model supplies the missing system-level comparison, and its negative break-evens quantify exactly what the launch-only framing omits. On radiation: the proton-beam results SUPPORT 5-yr TID survivability with margin (HBM irregularities from ~2 krad vs ~750 rad 5-yr requirement; no hard failures to 15 krad) and do not contradict 7-yr TID; what they do not establish is 7-yr SYSTEM reliability — SEE-induced corruption (core logic/SRAM most sensitive), training-workload impact (reserved by the authors), thermal, and whole-spacecraft failure remain unresolved. Note also the chip-efficiency panel of the crossover figure (r2.10 §16: efficiency is a mass multiplier off Earth — the 'launch tax vs Nvidia tax' argument made quantitative). Our refinement of that argument: at anchored values a 2x FLOPS/W advantage buys ~39% of the benefit of halving launch price (ratio 4.0 vs 3.2 at $3,000/kg, both from 4.5), because the hardware term — which efficiency does not touch — is the larger share of both mass and capex. The mass-multiplier mechanism is real but subdominant to the hardware cost channel at central anchors; efficiency dominance emerges only after the qualification premium and hw $/kW fall.

## Figures

![lco_composition](figures/lco_composition.png)

![lco_ratio_mc](figures/lco_ratio_mc.png)

![crossover_surface](figures/crossover_surface.png)

## Parameter provenance (anchors used)

| anchor | central value | source_class | note |
|---|---|---|---|
| aspirations.orbital_compute_gw_per_year | 100 | company_statement | LONG-TERM TARGET: up to 100 GW of AI-compute power deployed to orbit annually. CONTEXT ONLY for scale arithmetic; EU Prospectus 2026-06-05, pp. 82, 97 |
| aspirations.starmind_life_years | 7 | ASSUMPTION | FAVORABLE MODEL BOUND, not published by SpaceX: high end of compute.life_years_space. USED only in the aspirational deterministic sensitivity |
| aspirations.starmind_qualification_multiplier | 1.2 | ASSUMPTION | FAVORABLE MODEL BOUND, not published by SpaceX: low end of compute.space_qual_multiplier. USED only in the aspirational deterministic sensitivity |
| aspirations.starmind_utilization | 0.95 | ASSUMPTION | FAVORABLE MODEL BOUND, not achieved AI1 availability: high end of compute.utilization_leo. Starlink's reported network uptime is not evidence of AI1 spacecraft compute availability. USED only in the aspirational deterministic sensitivity |
| aspirations.starmind_vehicle_efficiency_kw_per_tonne | 100 | company_statement | LONG-TERM TARGET/ASSUMPTION in SpaceX scale arithmetic: 100 kW of AI compute per deployed tonne. The later AI1 product page discloses only 70 kW/t, 30% below this target. USED only in the aspirational deterministic sensitivity; EU Prospectus 2026-06-05, p. 82 |
| aspirations.starmind_vehicle_mass_kg_per_average_kw | 10 | ASSUMPTION | DERIVED exactly as 1000 kg/t divided by the company-target 100 kW/t. USED as aggregate launched mass only in the aspirational deterministic sensitivity |
| aspirations.starship_leo_cost_per_kg | 185 | company_statement | TARGET, not achieved price: exact arithmetic ceiling from SpaceX's aim to reduce its stated historical $18,500/kg launch cost by 99% or more (0.01 x $18,500 = $185/kg). USED only in the aspirational deterministic sensitivity; EU Prospectus 2026-06-05, pp. 63, 70, 137 |
| aspirations.starship_v3_payload_tonnes | 100 | company_statement | DESIGN TARGET: Starship V3 reusable payload capacity to orbit. CONTEXT ONLY for scale arithmetic; EU Prospectus 2026-06-05, pp. 71-72 |
| aspirations.starship_v4_payload_tonnes | 200 | company_statement | FUTURE TARGET: possible Starship V4 reusable payload capacity to orbit. CONTEXT ONLY for scale arithmetic; EU Prospectus 2026-06-05, pp. 71-72 |
| compute.hw_mass_kg_per_kw | 17.32 | ASSUMPTION | server mass per kW IT stripped of air-cooling chassis; UNANCHORED |
| compute.hw_per_kw_it | 3.354e+04 | reporting | accelerator+system $ per kW of IT load, 2024-26 (H100 ~0.7 kW ~$25-30k; B200 ~1 kW ~$30-40k incl. system share) |
| compute.life_years_earth | 4.243 | technical_report | accelerator refresh cycles (Appendix A: obsolescence-driven) |
| compute.life_years_space | 4.583 | reporting | LEO design lives ~5 yr; radiation + obsolescence for compute payloads |
| compute.ops_fraction_per_year | 0.03464 | ASSUMPTION | ground segment, downlink, ops as fraction of space capex per year |
| compute.power_overhead_space | 1.173 | ASSUMPTION | conversion + pumping losses; the space analogue of PUE |
| compute.space_qual_multiplier | 1.897 | ASSUMPTION | rad-tolerant COTS screening/derating cost factor on hw. Low end has reporting-class support: Planet flies unmodified Nvidia GPUs on Pelican imaging satellites (in-orbit inference demo April 2026, now standard on the line; Moonshots #266, docs/transcripts/moonshots-266-2026-06-26.md) — COTS survives benign LEO for inference-class workloads. Suncatcher proton testing (arXiv:2511.19468v2, 2026-06-17): TPU v6e HBM most TID-sensitive, irregularities from ~2 krad(Si) vs ~750 rad 5-yr shielded requirement (~150 rad/yr), no hard TID failures to 15 krad — SUPPORTS 5-yr TID survivability with margin and does not contradict 7-yr TID; core logic/SRAM most SEE-sensitive, inference error ~1 per 3M inferences, training impact reserved. What remains unresolved is SYSTEM reliability (SEE, training workloads, thermal, whole-spacecraft). High end (hardened, long-life, training-class) remains UNANCHORED |
| compute.utilization_cislunar | 0.9439 | ASSUMPTION | near-continuous sunlight at high orbit |
| compute.utilization_leo | 0.7858 | ASSUMPTION | eclipse fraction (orbit-dependent; dawn-dusk SSO near 1.0) x availability. High end supported by the Suncatcher reference design (81-sat cluster in dawn-dusk sun-synchronous orbit, near-continuous sunlight; r2.10 [S32]) |
| compute.utilization_lunar | 0.6185 | ASSUMPTION | 14-day night: low end = solar+partial storage; high end = polar site / oversized storage |
| earth.dc_capex_per_kw_it | 2e+04 | OVERRIDE | scenario/sweep override |
| earth.gas_power_price_floor_kwh | 0.04899 | reporting | firm CCGT power at shale-gas fuel cost + capex + O&M (Situational Awareness ch. IIIa, 2024, docs/sources/: <$1000/kW plant capex, ~2yr combined-cycle build, Marcellus alone could feed ~150-250 GW). POLITICALLY CONDITIONAL: assumes permitting/climate commitments yield — the responsive scenario's premise; the tight scenario is the politics-binds branch |
| earth.nuclear_ppa_kwh | 0.1082 | reporting | restart PPAs (e.g. TMI ~$100-115/MWh reported 2024); long-run firm clean floor |
| earth.older_node_energy_penalty | 2.121 | technical_report | J/FLOP penalty vs frontier node (~2-3x per 2 process generations) |
| earth.older_node_hw_per_kw | 1.095e+04 | reporting | prior-gen accelerators $/kW IT on secondary/extended supply |
| earth.power_price_kwh | 0.12 | OVERRIDE | scenario/sweep override |
| earth.pue | 1.241 | reporting | hyperscale AI facilities |
| earth.wacc | 0.1095 | ASSUMPTION | capital recovery rate, both sides |
| launch.cislunar_multiplier | 2.828 | ASSUMPTION | $/kg to high orbit / TLI vs LEO; staging + kick stages |
| launch.leo_per_kg | 2,366 | company_statement | published price sheets 2024-26: F9 ~$70M/22.8t ≈ $3.0k/kg; FH reusable ~$97M/~63t ≈ $1.4-1.5k/kg. List prices, not costs |
| launch.lunar_surface_multiplier | 8.944 | ASSUMPTION | landed $/kg vs LEO AT SCALE. Today's CLPS missions are ~$1M/kg (100x LEO); range assumes maturing landers. Wide on purpose |
| power_systems.infrastructure_life_years | 15.81 | ASSUMPTION | amortization life for PV/radiator/storage/structure and the launch spend that emplaced them, DISTINCT from the compute refresh cycle (r3.5 review fix: a single short compute life over-annualized long-lived infrastructure). Bounding: GEO comsat buses design to ~15 yr and ISS EATCS radiators exceed 20 yr service (upper); LEO debris/UV/thermal-cycling and lunar dust + 300-K-swing degradation argue the lower end. UNANCHORED within the range |
| power_systems.lunar_storage_kg_per_kwh | 6.325 | technical_report | Li-ion pack-level 100-250 Wh/kg; night-survival storage for lunar surface |
| power_systems.pv_cost_per_kw | 1,000 | reporting | space-qualified array $/kW at volume; terrestrial is ~10x cheaper |
| power_systems.pv_specific_power_w_per_kg | 109.5 | technical_report | flexible blanket arrays; ROSA ~150 W/kg BOL at 1 AU, rigid panels low end |
| power_systems.radiator_cost_per_kw | 447.2 | ASSUMPTION | manufactured cost at volume; UNANCHORED |
| power_systems.radiator_kg_per_kw | 6 | technical_report | deployable radiators at electronics-friendly reject temps; ISS EATCS practice ~6 kg/kW_rejected; advanced concepts 1-3 |
| power_systems.structure_overhead_fraction | 0.3162 | ASSUMPTION | bus/harness/avionics/shielding mass as fraction of (hw+pv+radiator) mass |
| starmind.compute_payload_kw_average | 120 | company_statement | AI1 disclosed average compute payload, kW. USED with solar_array_kw to set the scenario's 1.25 array-power/average-compute ratio; official Starmind page, accessed 2026-07-27 |
| starmind.compute_payload_kw_peak | 150 | company_statement | AI1 disclosed compute payload peak, kW. CONTEXT: not used as delivered-average model denominator; official Starmind page, accessed 2026-07-27 |
| starmind.deployed_height_m | 20 | company_statement | AI1 disclosed deployed height, m. CONTEXT ONLY; official Starmind page, accessed 2026-07-27 |
| starmind.radiator_area_m2 | 110 | company_statement | AI1 disclosed deployable liquid-radiator area, m^2. CONTEXT ONLY: no radiator areal mass or cost is disclosed, so the scenario retains the generic radiator cost and uses the aggregate vehicle mass constraint; official Starmind page, accessed 2026-07-27 |
| starmind.solar_array_kw | 150 | company_statement | AI1 disclosed solar-array rating, kW. USED with average compute payload to set the 1.25 design power ratio; official Starmind page, accessed 2026-07-27 |
| starmind.solar_power_density_w_per_m2 | 250 | company_statement | AI1 disclosed solar power density, W/m^2. CONTEXT ONLY: the cost model prices PV per kW and the aggregate vehicle mass constraint already captures array mass; official Starmind page, accessed 2026-07-27 |
| starmind.vehicle_efficiency_kw_per_tonne | 70 | company_statement | AI1 disclosed vehicle efficiency, kW/tonne. The page does not state whether kW means peak or average; official Starmind page, accessed 2026-07-27 |
| starmind.vehicle_mass_kg_per_average_kw | 15.97 | ASSUMPTION | DERIVED interpretation range from the disclosed 70 kW/tonne and 120 average / 150 peak kW: low assumes the efficiency numerator is average power (1000/70); high assumes it is peak power and converts total vehicle mass to an average-kW denominator ((150/70 t)/120 kW). USED as aggregate launched vehicle mass; the generic component budget supplies only the lifecycle split |
| starmind.wingspan_m | 70 | company_statement | AI1 disclosed wingspan, m. CONTEXT ONLY; official Starmind page, accessed 2026-07-27 |
