# Appendix A: Parameter Anchors {#appendix-a-parameter-anchors}

<!-- markdownlint-disable MD051 -->

The authoritative, machine-readable anchor set is `params/anchors.yaml`
[S28]; every generated report carries a per-run provenance table. Ranges
reflect genuine disagreement across sources; values are anchors, not
precision claims. The discipline of normalizing quantities by type and
never averaging rate quantities into one "r" is implemented in
code (`delta.py`) rather than prose. Rows marked *(context)* are
documentary quantities cited for interpretation only: they are not wired
model inputs and have no YAML entry. Every other row resolves from the
YAML, and source classes use only the five input-source classes defined
in [Scope, Claims, and Evidence](#scope-claims-and-evidence).

<!-- markdownlint-enable MD051 -->

**Claim-level provenance contract.** `params/claim_provenance.yaml` records
author or organization, title, date, page/table/section, permanent URL, DOI
or content-hashed repository snapshot, extracted value, units,
transformation, source class, and verification status for every
non-`ASSUMPTION` anchor. The same register pins the load-bearing [S27]
strategy claims to SEC pages or roadshow slides. A test rejects missing
records, endpoint drift, source-class drift, collective [S36] support for a
non-assumption anchor, and unpinned [S27] claims. The deterministic public
render is [claim-provenance register](../outputs/tables/claim_provenance.csv){.artifact-link data-artifact="outputs/tables/claim_provenance.csv"}. Ranges whose exact endpoints
remain analyst-constructed are explicitly `ASSUMPTION`, even when
reporting or technical literature provides contextual bounds.

## A.1 Capacity-loss quantities (δ), by type {#a.1-capacity-loss-quantities-δ-by-type}

| quantity | range | class [ref] | type |
|---|---|---|---|
| Solar-array degradation, GEO | 0.4–1.7 %/yr | peer_reviewed [S19] | continuous degradation |
| Terrestrial PV degradation | 0.5–0.6 %/yr median | peer_reviewed [S18] | continuous degradation |
| LEO constellation failure | 0.001–0.03 /yr | **ASSUMPTION** (context: [S22]) | analyst conversion of cohort fractions mixing failure, retirement, and disposal; not a measured hazard rate |
| Satellite design life | ~15 yr GEO; ~5 yr LEO | **ASSUMPTION** | representative mission conventions, not lifetime distributions |
| Fab-tool depreciation | 2–5 yr *(context)* | reporting [S36] | accounting schedule; not a model input or capability-loss measurement |
| Advanced-node obsolescence rate, Earth | 0.15–0.35 /yr | **ASSUMPTION** | analyst conversion to frontier-equivalent capacity loss |
| Accelerator retirement | 3–6 yr | **ASSUMPTION** | analyst economic-retirement interval; `compute.life_years_earth` |
| Cluster interruption frequency | ~1 / 2,000 accelerator-days *(context)* | reporting [S36] | mixes component, host, network, software events, mostly auto-recovered — NOT a component hazard rate |
| Space logistics penalty | 1–5 %/yr | **ASSUMPTION** | internal repair-chain tax; unanchored |

: Capacity-loss anchors by mechanism and evidence class. {#tbl-a-capacity-loss-anchors}

These are not interchangeable; the model converts each to
capacity-loss-per-year per component class before it enters a growth
equation. Solar-array and satellite data do not establish the depreciation
of mines, bearings, seals, machine tools, batteries, robots, or
dust-exposed thermal equipment — those entries are per-sector ASSUMPTIONS
in `params/environments.yaml`.

## A.2 Rate quantities previously conflated as "r" — separated {#a.2-rate-quantities-previously-conflated-as-r-separated}

| quantity | range | class [ref] | what it does NOT measure |
|---|---|---|---|
| PV energy payback | 0.9–1.1 yr Europe; 1.0–4.1 harmonized | peer_reviewed [S20] | reproduction of mines, refineries, tools, or the panel line |
| Strawman replication design target | ~1 yr (assumed) *(context)* | technical_report [S23] | an estimate or measurement of anything — it is a proof-of-principle design assumption |
| Construction-execution cadence | ~10 months | **ASSUMPTION** (reporting context) | recursive reproduction; used a mature host economy |
| Humanoid robot production | 50–100k targeted *(context)* | company_statement | feasibility — targets evidence intent |

: Rates and targets that require distinct interpretations. {#tbl-a-rate-quantities}

System replication time is unknown as a measurement. In this paper it
exists only as a computed output distribution (Part I.8), set-labeled.

## A.3 Closure and data quantities {#a.3-closure-and-data-quantities}

| quantity | range | class [ref] | note |
|---|---|---|---|
| Closure reported in cited nonreplicating applications | 90–96 % | technical_report [S23] | not a demonstrated result for the proposed factory; complete parts closure was outside its scope |
| Demonstrated ISRU O₂, Mars | 6–12 g/hr *(context)* | peer_reviewed [S21] | single output, small scale |
| Demonstrated lunar O₂ yield | ~20 %, TRL 5/6 | technical_report [S21] | full-system closure undemonstrated |
| Residual high-complexity import fraction | 4–10 % | technical_report [S23] | CP-2255 residual, historically called “vitamin” imports |
| **Space electronics q-scale** | **0.10–0.30** | **ASSUMPTION** | **the electronics strategic-material gap — the results-driving unanchored number** |
| Fleet data scale | >10B supervised miles; ~220M fully driverless miles at another operator *(context)* | company_statement [S17] [S30] | no conversion between regimes; not an advantage multiple or a model input |
| Heavy-lift flight tests | 13 through mid-2026 *(context)* | reporting [S31] | low-volume, high-information development proxy; not a capacity or reliability input |

: Closure, data and development quantities used as evidence or context. {#tbl-a-closure-data-quantities}

## A.4 Comparative-economics budgets (Part II) {#a.4-comparative-economics-budgets-part-ii}

Every row resolves from `params/anchors.yaml`. Exact claim-level details for
non-assumption rows are in `params/claim_provenance.yaml` and its generated
CSV. Reporting-derived bands without a direct endpoint-to-transformation
record remain useful scenario bounds but are labeled `ASSUMPTION`; [S36]
therefore supplies context only.

| quantity | range | class [ref] |
|---|---|---|
| LEO launch scenario band | $1,400–4,000 /kg | ASSUMPTION (published-price context: [S36]) |
| Cislunar / lunar-surface $/kg multipliers | 2–4× / 4–20× | ASSUMPTION [today's CLPS landed costs are ~100× LEO; range assumes maturing landers] |
| PV specific power | 80–150 W/kg | ASSUMPTION (array-performance context: [S36]) |
| Radiator specific mass | 3–12 kg/kW | ASSUMPTION (NASA complete-system cross-check supports ~7–12 kg/kW at one reject temperature [S43]) |
| Accelerator system cost | $25–45k /kW IT | ASSUMPTION (product-pricing context: [S36]) |
| Space qualification multiplier | 1.2–3.0× | ASSUMPTION (low end: COTS practice [S34]; [S32] radiation data supports 5-yr TID at the low end, system reliability open) |
| Equipment life, space / Earth | 3–7 / 3–6 yr | ASSUMPTION |
| Accelerator mass | 10–30 kg/kW IT | ASSUMPTION |
| Space power overhead | 1.10–1.25× | ASSUMPTION |
| Operations fraction | 2–6 % of capex/yr | ASSUMPTION |
| PV cost | $500–2,000 /kW | ASSUMPTION |
| Radiator cost | $200–1,000 /kW | ASSUMPTION |
| Structure overhead fraction | 0.20–0.50 | ASSUMPTION |
| Lunar night storage | 4–10 kg/kWh | ASSUMPTION |
| Serviceable-platform infrastructure life | 10–25 yr | ASSUMPTION; requires power/thermal/structure reuse across compute refreshes |
| Integrated-disposable infrastructure life | equal to space equipment life | architecture definition; all assets retire together |
| Utilization LEO / cislunar / lunar | 0.65–0.95 / 0.90–0.99 / 0.45–0.85 | ASSUMPTION ([S32] dawn-dusk cluster design supports the LEO high end) |
| Starmind AI1 compute / solar / vehicle efficiency | 150 kW peak, 120 kW average / 150 kW / 70 kW·t⁻¹ | company_statement [S38]; conditional scenario |
| Starmind AI1 aggregate mass | 14.3–17.9 kg per average kW | ASSUMPTION derived from [S38]'s unspecified peak-vs-average efficiency denominator |
| Starmind AI1 radiator area / deployed envelope | 110 m² / 20 m × 70 m | company_statement [S38]; context only, no disclosed mass or cost |
| Aspirational AI1 launch cost / efficiency / mass | $185/kg / 100 kW·t⁻¹ / 10 kg per average kW | company targets plus derived arithmetic [S37]; deterministic case only |
| Aspirational AI1 qualification / life / utilization | 1.2× / 7 yr / 0.95 | ASSUMPTION; favorable existing bounds, not SpaceX specifications |
| DC capex | $11–20k /kW IT | ASSUMPTION (project-reporting context: [S36]) |
| PUE | 1.10–1.40 | ASSUMPTION (facility-reporting context: [S36]) |
| Firm-power floors: nuclear PPA / gas | $0.09–0.13 / $0.04–0.06 per kWh | ASSUMPTION (restart-PPA and CCGT context: [S35] [S36]) |
| Earth electricity price | $0.05–0.12 /kWh | ASSUMPTION |
| Gas power capex | $700–1,200 /kW | ASSUMPTION (contextual estimate below $1,000/kW: [S35]) |
| Older-node hardware | $8,000–15,000 /kW | ASSUMPTION |
| Older-node energy penalty | 1.5–3.0× | ASSUMPTION |
| Starmind AI1 solar power density | 250 W/m² | company_statement [S38] |
| Orbital-compute scale target | 100 GW/yr | company_statement [S37]; enters II.3's scale audit only |
| WACC | 8–15 % | ASSUMPTION |

: Economic and architecture inputs for the comparative-cost model. {#tbl-a-economic-inputs}

## A.5 External claims and quarantined sensitivity targets {#a.5-external-claims-and-quarantined-sensitivity-targets}

| claim | value | class [ref] |
|---|---|---|
| Mature-Starship formal aspiration | ≤$185/kg to orbit, derived from a stated ≥99% reduction from $18,500/kg; V3 100 t and possible V4 200 t | company_statement [S37]; comparison axis and deterministic best-case input, not a quoted price or MC prior |
| Aggressive / extreme Starship sensitivities | $100/kg / $30–50/kg; full-load equivalents: V3 $10M / $3–5M, V4 $20M / $6–10M | derived scenario axes; no demonstrated cost or customer price |
| Google/Planet crossover threshold | $200–300 /kg | company_statement [S34] |
| Suncatcher launch-cost feasibility marker (not a parity claim) | ≲$200 /kg by mid-2030s; launch-only vs electricity-only | technical_report [S32] |

: External claims retained as quarantined sensitivity targets. {#tbl-a-external-sensitivity-targets}

## A.6 Engineering cross-checks added after the IPO — not model inputs {#a.6-engineering-cross-checks-added-after-the-ipo-not-model-inputs}

These values test or partition the Part II architecture rather than silently
changing its priors. Where they become model inputs in a future calibration,
each must enter a named architecture scenario with its own life,
qualification, communications, and manufacturing assumptions.

| cross-check | reported or derived value | interpretation |
|---|---|---|
| Conventional 1 MW high-sunlight spacecraft | 29.4 kg/kW PV + storage + radiator; 34–59 kg/kW total [S39] | Brackets the generic central 46 kg/kW; best system-level mass calibration |
| AI1 aggregate vehicle | 14.3–17.9 kg per average kW, derived from 70 kW/t and 120/150 kW average/peak [S38] | Company-specification scenario; component split and achieved performance undisclosed |
| Integrated solar-compute-radiator array | 150 t / 16 MW ≈9.4 kg/kW by gross ratio; authors report 112.5 kW/t ≈8.9 kg/kW for the design basis [S40] | Pre-prototype lower bound; 2.2 km array, integrated vapor chambers, thin PV, custom ASIC |
| Tethered inference nodes | ≈5 kg/kW [S40] | Pre-prototype lower bound; tether deployment, collision, shielding, and station-keeping gates |
| Complete pumped radiator system | 5 kg/m² JIMO estimate; 8.8 kg/m² ISS panels + loop + deployment; ≈1.4 m²/kW at 353 K [S43] | Roughly 7–12 kg/kW at the stated temperature; low emitter-only masses are not complete thermal systems |
| Five-year lifetime penalty | 1.27× at 10% annual hazard; 1.58× at 20%, illustrative [S39] | Stress-test range, not a measured fleet prior |
| Orbital mesh versus terrestrial Clos | 2.25–10 TB/s versus 28,800 TB/s bisection in the compared 8,000-node systems; 150–450× latency [S41] | Exclude frontier training from the inference cost case until a network-performance model closes |
| Peer-reviewed small microdatacenters | power/thermal about one-third of bespoke satellite TCO; compute hardware <1%; energy efficiency up to 2.5× more valuable [S42] | Supports space-native preprocessing and inference, not hyperscale terrestrial substitution |
| Simplified 1 GW five-year cost cross-check | $135.6B orbital versus $16.6B terrestrial; $15.4B orbital only in a joint aggressive technology corner [S44] | Directional joint-condition check; excludes several major costs |

: Independent and first-party orbital-compute architecture cross-checks. {#tbl-a-orbital-crosschecks}

## A.7 Provisional hiring-sweep note — not an evidence-table item {#a.7-provisional-hiring-sweep-note-not-an-evidence-table-item}

A July 2026 search across 1,170 open OpenAI and Anthropic postings found
multiple roles explicitly concerned with software-RSI preparation and
measurement, including early-warning metrics, recursive-self-improvement
preparation, chip-design reinforcement learning, and long-horizon training
environments. The same search found no roles in fabrication,
packaging/test, materials, or production-equipment reproduction. This is a
provisional negative-search observation, not evidence of capability or a
model input. Its value depends on the unpublished search vocabulary,
deduplication rules, per-lab counts, and stability of a changing jobs
corpus. The working snapshot is
`docs/transcripts/lab-job-listings-2026-07-26.md`; it should not enter the
main evidence table until a public dated audit artifact exists.

# Appendix B: Implementation and Provenance {#appendix-b-implementation-and-provenance}

The executable release combines the ten-sector capacity model, the comparative
economics model, and an 18-sector, 17-material integrated-bootstrap layer.
The integrated layer includes material-category-resolved bills of material,
explicit source and transfer arcs, minimum-mass seed sizing, autonomy and
intervention constraints, process-environment effects, construction and
commissioning dynamics, compute–intelligence–productivity coupling, tiered
electronics, finite shell mass, debris dynamics, symmetric economics, and
composition-changing robust-seed searches.

Central and 200-draw deterministic assumption-ensemble results are reported in
Part I.8 and regenerate from `rsi-run-integrated`. The release includes
sector-resolved cohort dynamics, independent allocation and repair, delivered-
seed deployment, observable autonomy and outage regimes, policy and structural
sweeps, terminal-window diagnostics, import-stock resolution, coupling
ablations, an oversize frontier, and a quantified strict-lunar infeasibility
certificate. All remain assumption-conditioned structures pending empirical
calibration.

Machine-validated contracts define the still-missing evidence for
process-feasible closure, the physical Stage-0 rehearsal, and economic
calibration. Their templates are deliberately non-passing: completed bundles
must bind every referenced digest to a verified file, and success states must
satisfy the underlying fault, holdout, review, and graph-consistency rules.
Venue-specific paper drafts and submission contracts are included, but final
source/style review, live-portal checks, author-controlled declarations,
immutable release coordinates, and submission approval remain pending.

Every generated result is reproducible from the declared configuration, code,
and deterministic seeds. `outputs/MANIFEST.md` binds the canonical manuscript,
HTML, source/configuration files, and generated artifacts;
`outputs/integrated/MANIFEST.md` additionally records the integrated run inputs
and outputs. No model output is presented as a measurement, empirical
probability, engineering estimate, or forecast.
