# Part II report: levelized cost of compute, space vs Earth — 2026-07-29

Unit: **$ per frontier-equivalent kW-year of delivered IT load** (older-node
hardware is compute-normalized by its J/FLOP penalty). Three reference cases
(paper Section 9): LEO inference, cislunar batch, and **Earth-supplied**
lunar-surface compute (central closure fraction is zero — local manufacture
enters only through the closure sweep axis), plus separate Starmind AI1
disclosed-design and stated-aspiration scenarios.
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
Shared draws both sides: each MC iteration resolves every common anchor once
per draw-cached AnchorSet, so Earth and space see the same hardware-cost draw;
their financing anchors are intentionally separate.


## Complete levelized-cost specification

For WACC \(r\), useful life \(T\), annual operations fraction \(f_o\),
insurance fraction \(f_i\), and residual-value fraction \(s\),

\[
\operatorname{CRF}(r,T)=\frac{r}{1-(1+r)^{-T}},
\qquad
a(T,s)=\operatorname{CRF}(r,T)
\left[1-\frac{s}{(1+r)^T}\right]+f_o+f_i.
\]

Let \(C_h\) be qualified accelerator capex, \(C_I\) the sum of PV, radiator,
storage, communications, ground network, spacecraft bus, disposal, and NRE
capex, \(R\) annual spectrum/regulatory cost, \(M_h\) accelerator mass,
\(M_I\) launched non-hardware
mass after local closure, \(\mu\) the destination launch multiplier,
\(p_L\) the LEO launch price, and \(U_s\) delivered utilization. The complete
space expression is

\[
L_s =
\frac{C_h a(T_h,s)+C_I a(T_I,s)+R
+p_L\mu[M_h a(T_h,s)+M_I a(T_I,s)]}{U_s}
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
lower \(L_E\). Space and Earth WACC are sampled separately. Thermal mass
also responds to rejection temperature, chip-to-emitter drop, environmental
view, pumping power, and reliability margin.
The exact affine break-even launch price is

\[
p_L^*=\frac{L_E-\alpha}{\beta},
\]

with a negative value meaning non-launch costs alone exceed the Earth
counterfactual.


For the central LEO serviceable-platform case, the resolved values are
\(C_h=63,640\), \(C_I=15,003\) $/kW,
\(M_h=17.3\), \(M_I=36.9\) kg/kW,
\(p_L=2,366\) $/kg,
\(a_h=0.3584\), \(a_I=0.2277\), and
\(U_s=0.786\). Substitution gives

\[
L_s =
\frac{63,640(0.3584)
+15,003(0.2277)
+158
+2,366
[17.3(0.3584)
+36.9(0.2277)]}
{0.786}
= 77,559\ \$/\mathrm{kW\!-\!yr}.
\]



## Central references and deterministic aspiration case

Space cases (capex $/kW before annualization):

| case | architecture | LCO $/kW-yr | launched kg/kW | hardware | pv | radiator | storage | other infrastructure + NRE | launch |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| leo_inference | serviceable/reusable platform | 77,559 | 54 | 63,640 | 1,225 | 945 | 0 | 12,833 | 128,281 |
| cislunar_batch | serviceable/reusable platform | 131,524 | 54 | 63,640 | 1,225 | 945 | 0 | 12,833 | 362,833 |
| lunar_surface (Earth-supplied) | serviceable/reusable platform | 3,864,754 | 480 | 63,640 | 2,695 | 945 | 12,250 | 14,367 | 10,155,238 |
| SpaceXAI — AI1 disclosed design | serviceable/reusable platform | 46,523 | 16 | 63,640 | 1,250 | 964 | 0 | 12,838 | 37,796 |
| SpaceXAI — long-term targets plus favorable model assumptions | serviceable/reusable platform | 15,957 | 10 | 40,249 | 1,250 | 964 | 0 | 10,223 | 1,850 |
| leo_inference | integrated disposable satellite | 98,871 | 54 | 63,640 | 1,225 | 945 | 0 | 12,833 | 128,281 |
| cislunar_batch | integrated disposable satellite | 175,418 | 54 | 63,640 | 1,225 | 945 | 0 | 12,833 | 362,833 |
| lunar_surface (Earth-supplied) | integrated disposable satellite | 6,209,841 | 480 | 63,640 | 2,695 | 945 | 12,250 | 14,367 | 10,155,238 |
| SpaceXAI — AI1 disclosed design | integrated disposable satellite | 55,748 | 16 | 63,640 | 1,250 | 964 | 0 | 12,838 | 37,796 |

Earth scenarios:

| scenario | LCO $/kW-yr | node choice |
|---|---|---|
| tight | 15,980 | frontier |
| base | 14,669 | frontier |
| responsive | 12,783 | older |

Workload-normalized boundaries (the inference unit requires a declared model,
latency, accuracy, batch, memory, and precision; the training unit applies an
explicit network-efficiency gate):

| case | cost / million defined inferences | cost / network-effective training kW-yr | training network efficiency |
|---|---:|---:|---:|
| leo_inference · serviceable/reusable platform | $16,902 | $490,528 | 0.158 |
| cislunar_batch · serviceable/reusable platform | $28,662 | $831,829 | 0.158 |
| lunar_surface (Earth-supplied) · serviceable/reusable platform | $842,220 | $24,442,853 | 0.158 |
| SpaceXAI — AI1 disclosed design · serviceable/reusable platform | $10,138 | $294,235 | 0.158 |
| SpaceXAI — long-term targets plus favorable model assumptions · serviceable/reusable platform | $3,477 | $100,921 | 0.158 |
| leo_inference · integrated disposable satellite | $21,546 | $625,314 | 0.158 |
| cislunar_batch · integrated disposable satellite | $38,228 | $1,109,441 | 0.158 |
| lunar_surface (Earth-supplied) · integrated disposable satellite | $1,353,270 | $39,274,483 | 0.158 |
| SpaceXAI — AI1 disclosed design · integrated disposable satellite | $12,149 | $352,579 | 0.158 |
| Earth · tight | $3,482 | $19,596 | 0.815 |
| Earth · base | $3,197 | $17,989 | 0.815 |
| Earth · responsive | $2,786 | $15,675 | 0.815 |

A calibration check: the Earth base LCO corresponds to
≈ $1.67/kW-hr,
consistent with published accelerator rental rates — the model is anchored at
the right order of magnitude.


## Disclosed and aspirational scenario inputs

These company statements and separately source-classed model assumptions define conditional scenarios; they do not replace the generic reference cases or establish achieved cost, lifetime, or availability.

| case | disclosed/derived quantity | central value | source_class | model role |
|---|---|---:|---|---|
| SpaceXAI — AI1 disclosed design | `starmind.compute_payload_kw_peak` | 150 | company_statement | Context only; peak power is not the delivered-average model denominator. Source S38; accessed 2026-07-27; AI1 technical specifications: compute payload. |
| SpaceXAI — AI1 disclosed design | `starmind.compute_payload_kw_average` | 120 | company_statement | Used as the delivered-load denominator and with solar-array power to set the 1.25 design power ratio. Source S38; accessed 2026-07-27; AI1 technical specifications: compute payload. |
| SpaceXAI — AI1 disclosed design | `starmind.vehicle_efficiency_kw_per_tonne` | 70 | company_statement | The source does not say whether kW is peak or average; the derived mass range preserves both interpretations. Source S38; accessed 2026-07-27; AI1 technical specifications: vehicle efficiency. |
| SpaceXAI — AI1 disclosed design | `starmind.vehicle_mass_kg_per_average_kw` | 15.97 | ASSUMPTION | Interpretation range, not a direct company value; generic component weights supply only the lifecycle split. Source S38; derived 2026-07-27; 1000/70 and (150/70 tonnes)/120 kW. |
| SpaceXAI — AI1 disclosed design | `starmind.solar_array_kw` | 150 | company_statement | Nameplate solar power is not delivered IT load. Source S38; accessed 2026-07-27; AI1 technical specifications: solar array. |
| SpaceXAI — AI1 disclosed design | `starmind.solar_power_density_w_per_m2` | 250 | company_statement | Context only; the aggregate mass constraint already captures array mass. Source S38; accessed 2026-07-27; AI1 technical specifications: solar power density. |
| SpaceXAI — AI1 disclosed design | `starmind.radiator_area_m2` | 110 | company_statement | No radiator areal mass, thermal duty, temperature, or cost is disclosed. Source S38; accessed 2026-07-27; AI1 technical specifications: radiator. |
| SpaceXAI — AI1 disclosed design | `starmind.deployed_height_m` | 20 | company_statement | Geometry marker only; it does not determine a complete collision cross-section or topology. Source S38; accessed 2026-07-27; AI1 technical specifications: deployed envelope. |
| SpaceXAI — AI1 disclosed design | `starmind.wingspan_m` | 70 | company_statement | Geometry marker only; attitude, spacing, shell, maneuver, and failure behavior remain undisclosed. Source S38; accessed 2026-07-27; AI1 technical specifications: deployed envelope. |
| SpaceXAI — long-term targets plus favorable model assumptions | `starmind.compute_payload_kw_peak` | 150 | company_statement | Context only; peak power is not the delivered-average model denominator. Source S38; accessed 2026-07-27; AI1 technical specifications: compute payload. |
| SpaceXAI — long-term targets plus favorable model assumptions | `starmind.compute_payload_kw_average` | 120 | company_statement | Used as the delivered-load denominator and with solar-array power to set the 1.25 design power ratio. Source S38; accessed 2026-07-27; AI1 technical specifications: compute payload. |
| SpaceXAI — long-term targets plus favorable model assumptions | `starmind.solar_array_kw` | 150 | company_statement | Nameplate solar power is not delivered IT load. Source S38; accessed 2026-07-27; AI1 technical specifications: solar array. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.starmind_vehicle_efficiency_kw_per_tonne` | 100 | company_statement | Long-run target; the later AI1 disclosed design is 70 kW/t. Source S37; 2026-06-05; EU Prospectus p. 82. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.starmind_vehicle_mass_kg_per_average_kw` | 10 | ASSUMPTION | Derived assumption; not a direct vehicle specification. Source S37; derived 2026-06-05; 1000 kg/t divided by 100 kW/t. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.starship_leo_cost_per_kg` | 185 | company_statement | Target arithmetic ceiling, not achieved launch price or customer quote. Source S37; 2026-06-05; EU Prospectus pp. 63, 70, and 137; exact 99% reduction ceiling from USD 18,500/kg. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.starship_v3_payload_tonnes` | 100 | company_statement | Design target, not demonstrated reusable payload. Source S37; 2026-06-05; EU Prospectus pp. 71-72. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.starship_v4_payload_tonnes` | 200 | company_statement | Future target, not demonstrated reusable payload. Source S37; 2026-06-05; EU Prospectus pp. 71-72. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.orbital_compute_gw_per_year` | 100 | company_statement | Annual flow target, not cumulative operating stock or achieved cadence. Source S37; 2026-06-05; EU Prospectus pp. 82 and 97. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.starmind_qualification_multiplier` | 1.2 | ASSUMPTION | Favorable model assumption, not published by SpaceX. Source S37; selected 2026-07-27; favorable lower bound of compute.space_qual_multiplier. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.starmind_life_years` | 7 | ASSUMPTION | Favorable model assumption, not achieved AI1 service life. Source S37; selected 2026-07-27; favorable upper bound of compute.life_years_space. |
| SpaceXAI — long-term targets plus favorable model assumptions | `aspirations.starmind_utilization` | 0.95 | ASSUMPTION | Favorable model assumption; Starlink network uptime is not AI1 compute availability. Source S37; selected 2026-07-27; favorable upper bound of compute.utilization_leo. |

## Monte Carlo over anchored ranges (shared draws both sides)

The stated-aspiration case is excluded: company targets and deliberately
favorable unpublished assumptions are point sensitivities, not probability
distributions.

| case | architecture | vs Earth | ratio p10/p50/p90 | P(space cheaper) | break-even LEO $/kg p50 (p90) |
|---|---|---|---|---|---|
| leo_inference | serviceable/reusable platform | base | 3.6 / 5.7 / 8.8 | 0.000 | -987 (-385) |
| leo_inference | serviceable/reusable platform | responsive | 4.5 / 7.1 / 11.4 | 0.000 | -1,129 (-543) |
| leo_inference | integrated disposable satellite | base | 4.6 / 7.3 / 11.5 | 0.000 | -883 (-425) |
| leo_inference | integrated disposable satellite | responsive | 5.5 / 9.0 / 14.8 | 0.000 | -980 (-491) |
| cislunar_batch | serviceable/reusable platform | base | 5.8 / 9.7 / 16.6 | 0.000 | -291 (-96) |
| cislunar_batch | serviceable/reusable platform | responsive | 6.9 / 12.1 / 20.8 | 0.000 | -349 (-136) |
| cislunar_batch | integrated disposable satellite | base | 7.4 / 12.8 / 22.7 | 0.000 | -277 (-108) |
| cislunar_batch | integrated disposable satellite | responsive | 9.0 / 16.0 / 28.3 | 0.000 | -308 (-145) |
| lunar_surface (Earth-supplied) | serviceable/reusable platform | base | 112.0 / 263.9 / 652.8 | 0.000 | -21 (-9) |
| lunar_surface (Earth-supplied) | serviceable/reusable platform | responsive | 138.5 / 343.8 / 821.2 | 0.000 | -22 (-10) |
| lunar_surface (Earth-supplied) | integrated disposable satellite | base | 183.3 / 449.4 / 1092.7 | 0.000 | -16 (-7) |
| lunar_surface (Earth-supplied) | integrated disposable satellite | responsive | 232.4 / 562.4 / 1313.0 | 0.000 | -17 (-8) |
| SpaceXAI — AI1 disclosed design | serviceable/reusable platform | base | 2.3 / 3.3 / 4.9 | 0.000 | -3,567 (-1,624) |
| SpaceXAI — AI1 disclosed design | serviceable/reusable platform | responsive | 2.7 / 4.2 / 6.4 | 0.000 | -4,087 (-1,964) |
| SpaceXAI — AI1 disclosed design | integrated disposable satellite | base | 2.7 / 4.0 / 5.9 | 0.000 | -3,097 (-1,590) |
| SpaceXAI — AI1 disclosed design | integrated disposable satellite | responsive | 3.3 / 4.9 / 8.0 | 0.000 | -3,579 (-1,924) |

Break-even prices are the LEO $/kg at which the space case matches Earth;
**negative means fixed (non-launch) costs alone exceed the Earth cost** — at
those draws no launch price, even zero, closes the gap.

**Architecture split** — the serviceable/reusable-platform baseline is 5.29x Earth base for generic LEO and 3.17x for the AI1 disclosure scenario. The integrated disposable-satellite baseline, in which infrastructure and compute retire together, is 6.74x and 3.80x, respectively. Modularity supports standardisation but does not establish in-orbit replacement; neither architecture is silently treated as demonstrated.

**SpaceXAI — AI1 disclosed design** — SpaceX publishes 150 kW peak / 120 kW average compute, a 150 kW array, and 70 kW/tonne vehicle efficiency (official Starmind page, accessed 2026-07-27; provenance snapshot in `docs/sources/starmind-ai1-2026-07-27.md`). The model uses the 1.25 array/average-load ratio and, because SpaceX does not say whether the efficiency numerator is peak or average, samples 14.3-17.9 kg per average kW (central 16.0, versus 54.2 kg/kW generic LEO). At current central launch and retained cost/life/availability anchors, the serviceable-platform AI1 case is 3.17x Earth base; at $250/kg it is 2.38x, and its fixed non-launch costs still exceed Earth base (break-even -3,460 $/kg). The mass disclosure therefore materially lowers the launch term but does not resolve the qualification, hardware-cost, lifetime, or availability gates. With the remaining anchors simultaneously favorable (qualification x1.2, seven-year life, 0.95 utilization), AI1 becomes 1.74x at central launch, has no positive break-even launch price (-191 $/kg), and reaches 1.13x at $250/kg. Completing communications, bus, NRE, insurance, spectrum, disposal, thermal-margin, and financing terms leaves no favorable-corner crossover at these assumptions. Radiator area, dimensions, redundant loops, debris shielding, and laser links are recorded but do not receive invented costs where the page supplies none.

**SpaceXAI long-term targets plus favorable model assumptions (deterministic; excluded from Monte Carlo)** — SpaceX's EU prospectus says it aims to cut its stated historical launch cost of $18,500/kg by 99% or more, so the model uses $185/kg as the exact 99%-reduction ceiling; it also uses the prospectus's long-term 100 kW/t deployment assumption (10 kg per average kW). Those two company targets alone, while leaving unpublished inputs at their central values, yield 34,219 $/kW-yr or 2.33x Earth base. The displayed best case additionally selects the favorable, NON-COMPANY bounds of 1.2x qualification, seven-year hardware life, and 0.95 utilization; it yields 15,957 $/kW-yr or 1.09x Earth base. The deliberately omitted-cost diagnostic is 0.76x, while the complete boundary is 1.09x. The model assigns the aspirational case no success probability: targets and favorable analyst assumptions are point values, not empirical distributions.

**Feasibility audit of that best case** — the latest AI1 page's 70 kW/t is 30% below the older 100 kW/t scale assumption (reaching the target requires 43% more kW/t than AI1). At 100 GW deployed per year, 100 kW/t implies 1.00 million tonnes/year, about 10,000 full 100-t V3 launches/year (27.4/day) or 5,000 full 200-t V4 launches/year (13.7/day), plus roughly 833,333 120-kW spacecraft. At AI1's disclosed 70 kW/t the mass rises to 1.43 million tonnes and 14,286 V3 launches/year. Even at $185/kg, the 100-kW/t flow corresponds to $185 billion/year of launch cost before spacecraft manufacture. Full rapid reuse and this cadence are therefore load-bearing; so are seven-year whole-system reliability and 95% compute utilization, neither of which SpaceX publishes for AI1. Communications/downlink, ground network, spacecraft-bus functions, program NRE, insurance, spectrum and regulatory cost, disposal, residual value, thermal margins, and separate space financing are now explicit wide-bound terms. Collision externalities, constellation replenishment logistics, and landing/turnaround infrastructure remain outside the LCO, while the Earth alternative can also improve. The case is useful as a boundary: it shows what must all go right, not what is likely to happen.

**Sensitivity probe** — everything favorable *within* the anchored ranges at once (qual x1.2, utilization 0.95, radiator 3 kg/kW, life 7 yr): LEO space LCO becomes 44,206 $/kW-yr at central launch prices, and the break-even launch price becomes -65 $/kg — below any positive launch price (negative break-even). The completed fixed-cost boundary therefore prevents parity even at zero launch price in this favorable single-axis corner; further architectural changes, not launch alone, are required.

**External claim check** — a Google/Planet study (reported by Will Marshall, Moonshots #266, June 2026; recorded as `claims.google_planet_crossover_launch_per_kg`, company_statement, never a model input) puts the crossover at $200-300/kg to LEO. In our model, $250/kg at central anchors gives space/Earth = 2.61 (no crossover); with the favorable corner above it gives 1.26. The claim is not reproduced after the omitted-cost boundary is completed, even with COTS-class qualification (~1.2x), ~7-yr life, and ~0.95 utilization simultaneously. The disagreement is therefore architectural and accounting-wide, not a launch-price threshold alone.

The published Suncatcher design study (arXiv:2511.19468v2, 2026-06-17; `claims.suncatcher_launch_feasibility_per_kg`, technical_report) is a LAUNCH-COST FEASIBILITY MARKER, not a crossover claim — its own text says twice it is not a full economic analysis: at $200/kg it compares amortized launch cost per kW-yr against terrestrial electricity spend only, excluding infrastructure, buildings, and chips. Launch-vs-electricity is not system-vs-system; this model supplies the missing system-level comparison, and its negative break-evens quantify exactly what the launch-only framing omits. On radiation: the proton-beam results SUPPORT 5-yr TID survivability with margin (HBM irregularities from ~2 krad vs ~750 rad 5-yr requirement; no hard failures to 15 krad) and do not contradict 7-yr TID; what they do not establish is 7-yr SYSTEM reliability — SEE-induced corruption (core logic/SRAM most sensitive), training-workload impact (reserved by the authors), thermal, and whole-spacecraft failure remain unresolved. Note also the chip-efficiency panel of the crossover figure (the paper's efficiency boundary: efficiency is a mass multiplier off Earth — the 'launch tax vs Nvidia tax' argument made quantitative). Our refinement of that argument: at anchored values a 2x FLOPS/W advantage buys ~50% of the benefit of halving launch price (ratio 5.1 vs 4.2 at $3,000/kg, both from 6.1), because the hardware term — which efficiency does not touch — is the larger share of both mass and capex. The mass-multiplier mechanism is real but subdominant to the hardware cost channel at central anchors; efficiency dominance emerges only after the qualification premium and hw $/kW fall.

## Figures

![lco_composition](figures/lco_composition.png)

![lco_ratio_mc](figures/lco_ratio_mc.png)

![crossover_surface](figures/crossover_surface.png)

## Parameter provenance (anchors used)

| anchor | central value | source_class | note |
|---|---|---|---|
| aspirations.orbital_compute_gw_per_year | 100 | company_statement | Annual flow target, not cumulative operating stock or achieved cadence. Source S37; 2026-06-05; EU Prospectus pp. 82 and 97. |
| aspirations.starmind_life_years | 7 | ASSUMPTION | Favorable model assumption, not achieved AI1 service life. Source S37; selected 2026-07-27; favorable upper bound of compute.life_years_space. |
| aspirations.starmind_qualification_multiplier | 1.2 | ASSUMPTION | Favorable model assumption, not published by SpaceX. Source S37; selected 2026-07-27; favorable lower bound of compute.space_qual_multiplier. |
| aspirations.starmind_utilization | 0.95 | ASSUMPTION | Favorable model assumption; Starlink network uptime is not AI1 compute availability. Source S37; selected 2026-07-27; favorable upper bound of compute.utilization_leo. |
| aspirations.starmind_vehicle_efficiency_kw_per_tonne | 100 | company_statement | Long-run target; the later AI1 disclosed design is 70 kW/t. Source S37; 2026-06-05; EU Prospectus p. 82. |
| aspirations.starmind_vehicle_mass_kg_per_average_kw | 10 | ASSUMPTION | Derived assumption; not a direct vehicle specification. Source S37; derived 2026-06-05; 1000 kg/t divided by 100 kW/t. |
| aspirations.starship_leo_cost_per_kg | 185 | company_statement | Target arithmetic ceiling, not achieved launch price or customer quote. Source S37; 2026-06-05; EU Prospectus pp. 63, 70, and 137; exact 99% reduction ceiling from USD 18,500/kg. |
| aspirations.starship_v3_payload_tonnes | 100 | company_statement | Design target, not demonstrated reusable payload. Source S37; 2026-06-05; EU Prospectus pp. 71-72. |
| aspirations.starship_v4_payload_tonnes | 200 | company_statement | Future target, not demonstrated reusable payload. Source S37; 2026-06-05; EU Prospectus pp. 71-72. |
| compute.hw_mass_kg_per_kw | 17.32 | ASSUMPTION | server mass per kW IT stripped of air-cooling chassis; UNANCHORED |
| compute.hw_per_kw_it | 3.354e+04 | ASSUMPTION | Analyst-normalized 2024-26 accelerator-plus-system price band per kW IT; product prices, board power, and host allocation do not form a stable common-denominator source |
| compute.life_years_earth | 4.243 | ASSUMPTION | Analyst accelerator economic-retirement band; refresh practice is not a physical lifetime distribution |
| compute.life_years_space | 4.583 | ASSUMPTION | Analyst compute-payload service-life band around a ~5-year LEO convention; radiation, replacement, and obsolescence are architecture-specific |
| compute.ops_fraction_per_year | 0.03464 | ASSUMPTION | ground segment, downlink, ops as fraction of space capex per year |
| compute.power_overhead_space | 1.173 | ASSUMPTION | conversion + pumping losses; the space analogue of PUE |
| compute.space_qual_multiplier | 1.897 | ASSUMPTION | rad-tolerant COTS screening/derating cost factor on hw. Low end has reporting-class support: Planet flies unmodified Nvidia GPUs on Pelican imaging satellites (in-orbit inference demo April 2026, now standard on the line; Moonshots #266, docs/transcripts/moonshots-266-2026-06-26.md) — COTS survives benign LEO for inference-class workloads. Suncatcher proton testing (arXiv:2511.19468v2, 2026-06-17): TPU v6e HBM most TID-sensitive, irregularities from ~2 krad(Si) vs ~750 rad 5-yr shielded requirement (~150 rad/yr), no hard TID failures to 15 krad — SUPPORTS 5-yr TID survivability with margin and does not contradict 7-yr TID; core logic/SRAM most SEE-sensitive, inference error ~1 per 3M inferences, training impact reserved. What remains unresolved is SYSTEM reliability (SEE, training workloads, thermal, whole-spacecraft). High end (hardened, long-life, training-class) remains UNANCHORED |
| compute.utilization_cislunar | 0.9439 | ASSUMPTION | near-continuous sunlight at high orbit |
| compute.utilization_leo | 0.7858 | ASSUMPTION | eclipse fraction (orbit-dependent; dawn-dusk SSO near 1.0) x availability. High end supported by the Suncatcher reference design (81-sat cluster in dawn-dusk sun-synchronous orbit, near-continuous sunlight; [S32]) |
| compute.utilization_lunar | 0.6185 | ASSUMPTION | 14-day night: low end = solar+partial storage; high end = polar site / oversized storage |
| earth.dc_capex_per_kw_it | 2e+04 | OVERRIDE | scenario/sweep override |
| earth.gas_power_price_floor_kwh | 0.04899 | ASSUMPTION | Analyst CCGT floor derived from shale-gas fuel, capex, and O&M rather than quoted by the contextual source (Situational Awareness ch. IIIa, 2024, docs/sources/: <$1000/kW plant capex, ~2yr combined-cycle build, Marcellus alone could feed ~150-250 GW). POLITICALLY CONDITIONAL: assumes permitting/climate commitments yield — the responsive scenario's premise; the tight scenario is the politics-binds branch |
| earth.nuclear_ppa_kwh | 0.1082 | ASSUMPTION | Analyst firm-clean-power scenario band informed by reported restart PPAs; not a general long-run nuclear cost distribution |
| earth.older_node_energy_penalty | 2.121 | ASSUMPTION | Analyst workload-level energy-efficiency penalty for older nodes; no single technical record supports this cross-generation range at equal service quality |
| earth.older_node_hw_per_kw | 1.095e+04 | ASSUMPTION | Analyst prior-generation accelerator price-per-kW scenario; secondary-market price and useful workload equivalence are not stable |
| earth.power_price_kwh | 0.12 | OVERRIDE | scenario/sweep override |
| earth.pue | 1.241 | ASSUMPTION | Analyst scenario band spanning efficient hyperscale and less favorable AI facilities; climate, load, and boundary vary |
| earth.wacc | 0.1095 | ASSUMPTION | capital recovery rate, both sides |
| launch.cislunar_multiplier | 2.828 | ASSUMPTION | $/kg to high orbit / TLI vs LEO; staging + kick stages |
| launch.leo_per_kg | 2,366 | ASSUMPTION | Analyst-expanded band around published SpaceX price/performance sheets: F9 ~$69.75M/22t ≈ $3.17k/kg; FH price/performance produces a lower reference near $1.5k/kg. The rounded 1.4-4.0k endpoints are deliberately wider than the disclosed arithmetic; list prices, not costs |
| launch.lunar_surface_multiplier | 8.944 | ASSUMPTION | landed $/kg vs LEO AT SCALE. Today's CLPS missions are ~$1M/kg (100x LEO); range assumes maturing landers. Wide on purpose |
| power_systems.infrastructure_life_years | 15.81 | ASSUMPTION | amortization life for PV/radiator/storage/structure and the launch spend that emplaced them, DISTINCT from the compute refresh cycle (review correction: a single short compute life over-annualized long-lived infrastructure). Bounding: GEO comsat buses design to ~15 yr and ISS EATCS radiators exceed 20 yr service (upper); LEO debris/UV/thermal-cycling and lunar dust + 300-K-swing degradation argue the lower end. UNANCHORED within the range |
| power_systems.lunar_storage_kg_per_kwh | 6.325 | ASSUMPTION | Reciprocal of an analyst-selected 100-250 Wh/kg pack-level range; lunar night survival, thermal control, degradation, redundancy, and packaging are architecture-specific |
| power_systems.pv_cost_per_kw | 1,000 | ASSUMPTION | Analyst volume-manufacturing bound for space-qualified arrays; no exact claim-level source supports both endpoints |
| power_systems.pv_specific_power_w_per_kg | 109.5 | ASSUMPTION | Analyst architecture band spanning rigid and flexible blanket arrays; no single technical record supports both endpoints on a common BOL/system-mass basis |
| power_systems.radiator_cost_per_kw | 447.2 | ASSUMPTION | manufactured cost at volume; UNANCHORED |
| power_systems.radiator_kg_per_kw | 6 | ASSUMPTION | Analyst architecture band. NASA/TM-2005-213442 supports roughly 7-12 kg/kW for complete systems at one reject temperature; the 3 kg/kW advanced-concept endpoint is not comparably demonstrated |
| power_systems.structure_overhead_fraction | 0.3162 | ASSUMPTION | bus/harness/avionics/shielding mass as fraction of (hw+pv+radiator) mass |
| space_cost_completion.chip_to_radiator_temperature_drop_k | 34.64 | ASSUMPTION | Chip/coolant/transport-to-emitter temperature drop |
| space_cost_completion.communications_capex_per_kw | 1,581 | ASSUMPTION | Payload and gateway communications capex per delivered kW; explicit wide bound pending architecture-specific link budgets |
| space_cost_completion.disposal_capex_per_kw | 346.4 | ASSUMPTION | End-of-life passivation, deorbit, transfer, or retrieval provision per delivered kW |
| space_cost_completion.environmental_view_factor | 0.755 | ASSUMPTION | Net cold-space radiative view after solar and planetary geometry |
| space_cost_completion.ground_network_capex_per_kw | 547.7 | ASSUMPTION | Ground terminals, routing, and control-network capex per delivered kW; wide boundary |
| space_cost_completion.insurance_fraction_per_year | 0.02828 | ASSUMPTION | Annual insurance and risk-transfer cost as a fraction of deployed capex |
| space_cost_completion.program_nre_fraction | 0.1118 | ASSUMPTION | Program non-recurring engineering as a fraction of recurring non-launch capex |
| space_cost_completion.pumping_power_fraction | 0.04472 | ASSUMPTION | Thermal-loop pumping fraction of IT power |
| space_cost_completion.radiator_rejection_temperature_k | 358.7 | ASSUMPTION | Radiator surface rejection temperature boundary; workload/hardware qualification must support the selected value |
| space_cost_completion.residual_value_fraction_disposable | 0.025 | ASSUMPTION | Residual value at the end of integrated disposable life |
| space_cost_completion.residual_value_fraction_serviceable | 0.1225 | ASSUMPTION | Recoverable infrastructure value at the end of serviceable-platform life |
| space_cost_completion.spacecraft_bus_capex_per_kw | 2,449 | ASSUMPTION | Avionics, attitude control, propulsion, shielding, harness, and integration not already in generic power/thermal budgets |
| space_cost_completion.spectrum_regulatory_per_kw_year | 158.1 | ASSUMPTION | Spectrum, licensing, compliance, and regulatory program cost per delivered kW-year |
| space_cost_completion.thermal_reliability_mass_margin | 1.285 | ASSUMPTION | Redundancy, micrometeoroid isolation, degradation, and pumping hardware mass multiplier |
| space_cost_completion.wacc | 0.1483 | ASSUMPTION | Space-project financing bound, separated from Earth WACC |
| starmind.compute_payload_kw_average | 120 | company_statement | Used as the delivered-load denominator and with solar-array power to set the 1.25 design power ratio. Source S38; accessed 2026-07-27; AI1 technical specifications: compute payload. |
| starmind.compute_payload_kw_peak | 150 | company_statement | Context only; peak power is not the delivered-average model denominator. Source S38; accessed 2026-07-27; AI1 technical specifications: compute payload. |
| starmind.deployed_height_m | 20 | company_statement | Geometry marker only; it does not determine a complete collision cross-section or topology. Source S38; accessed 2026-07-27; AI1 technical specifications: deployed envelope. |
| starmind.radiator_area_m2 | 110 | company_statement | No radiator areal mass, thermal duty, temperature, or cost is disclosed. Source S38; accessed 2026-07-27; AI1 technical specifications: radiator. |
| starmind.solar_array_kw | 150 | company_statement | Nameplate solar power is not delivered IT load. Source S38; accessed 2026-07-27; AI1 technical specifications: solar array. |
| starmind.solar_power_density_w_per_m2 | 250 | company_statement | Context only; the aggregate mass constraint already captures array mass. Source S38; accessed 2026-07-27; AI1 technical specifications: solar power density. |
| starmind.vehicle_efficiency_kw_per_tonne | 70 | company_statement | The source does not say whether kW is peak or average; the derived mass range preserves both interpretations. Source S38; accessed 2026-07-27; AI1 technical specifications: vehicle efficiency. |
| starmind.vehicle_mass_kg_per_average_kw | 15.97 | ASSUMPTION | Interpretation range, not a direct company value; generic component weights supply only the lifecycle split. Source S38; derived 2026-07-27; 1000/70 and (150/70 tonnes)/120 kW. |
| starmind.wingspan_m | 70 | company_statement | Geometry marker only; attitude, spacing, shell, maneuver, and failure behavior remain undisclosed. Source S38; accessed 2026-07-27; AI1 technical specifications: deployed envelope. |
| workloads.inference_latency_availability_fraction | 0.8283 | ASSUMPTION | Share of nominal inference throughput delivered inside the declared latency and availability envelope |
| workloads.inference_requests_per_kwh | 632.5 | ASSUMPTION | Defined-workload inference throughput boundary; requires declared model, latency, accuracy, batch, memory, and precision |
| workloads.training_network_efficiency_earth | 0.8155 | ASSUMPTION | Useful frontier-training work after terrestrial interconnect and synchronization overhead |
| workloads.training_network_efficiency_space | 0.1581 | ASSUMPTION | Useful frontier-training work after orbital interconnect, synchronization, and fault overhead |
