# Part II — Comparative Economics {#part-ii-comparative-economics}

## II.1 The bridge economy {#ii.1-the-bridge-economy}

Each stage of the recursion must be independently profitable or deliberately
financed: a staircase of self-supporting steps, not a single leap to closure.
The first candidate tread is terrestrial output from the same machinery:
vehicles, storage, and robots pay rent while turning the autonomous seed into
an audited industrial experiment. Launch services and Starlink connectivity
form the next tread by funding transport. Orbital compute, priced explicitly
in II.2–II.4, could then become an anchor customer for launch, spacecraft
production, power, thermal management, communications, silicon, autonomy,
and servicing. In-space industrial services enter at higher closure.

The test of the staircase: at every stage, revenue plus strategic
financing must exceed the burn required to reach the next stage before the
clock-setting components of Part I.4 expire — and Part I.8 makes the clock
concrete: the electronics stockpile shelf life against the import ramp.
The commissioning trajectories in Figure [@fig-operating-capacity] are the
physical schedule that this bridge economy must finance.

Stage 0 has a second economic role. Building the candidate lunar industries
first on Earth captures process knowledge, failure data, tool interfaces,
simulation residuals, and commissioning procedures while the repair economy
is still accessible. Selling terrestrial output can finance that learning,
but the decisive deliverable is the measured ability to build and
commission a second cell under lunar-palette and no-routine-entry
constraints. A factory that is profitable yet requires tacit human rescue
has not validated the exported loop.

The bridge-economy claim is therefore narrower than first-generation cost
parity. Orbital compute could function as an industrial seed while remaining
more expensive than Earth only if attributable learning, faster capacity
activation, cross-program reuse, or declining external dependence earns the
difference. Those terms receive no automatic credit in the levelized-cost
model; II.2–II.4 price the delivered compute product, and the evidence needed
to value shared-stack effects remains a separate measurement requirement.

## II.2 The crossover model {#ii.2-the-crossover-model}

Unit: **dollars per frontier-equivalent kilowatt-year of delivered IT
load** — defined as one kilowatt-year of IT electrical load powering
accelerators of frontier-generation efficiency, delivered at the case's
utilization; older-node capacity is converted by its J/FLOP penalty, so a
frontier-equivalent kilowatt-year buys the same computational output
regardless of which hardware generation supplies it.
Three reference cases: a LEO inference service; high-orbit/cislunar batch
compute; and Earth-supplied lunar-surface compute, with local manufacture
entering only through the closure sweep. Mass and
power budgets resolve from anchored ranges — launch price sheets
(company_statement), flexible-array specific power and deployable-radiator
specific mass (technical_report), accelerator system cost and lives
(reporting), DC capex, PUE, WACC (reporting), qualification multiplier and
utilization (ASSUMPTION, evidence-tempered) — each with a source class and
per-run provenance. The space cost is affine in launch $/kg, so break-even
launch prices are exact. Chip efficiency is a first-class parameter: off
Earth, every watt not computed must be radiated, and radiator, PV, storage,
and structure are launched mass, so a FLOPS/W advantage scales the entire
power side per unit of delivered compute — efficiency and launch price
enter the crossover multiplicatively, with a quantitative refinement below.
This makes the popular framing of orbital compute as a launch-price race
incomplete and supplies a thermodynamic rationale for internalizing chip
*design*, not merely fabrication or supply security: the most efficient
accelerator can tolerate a higher launch price because it carries less power
and heat-rejection mass per useful computation.

Two lifecycle architectures are reported separately:

- **Integrated disposable satellite:** compute, PV, radiator, storage,
  structure, and original launch spend retire together.
- **Serviceable/reusable platform:** the compute payload refreshes on its
  hardware life while the power/thermal/structure platform and its original
  launch spend amortize over a longer infrastructure life. This is an
  explicit scenario assumption; modularity alone does not demonstrate
  serviceability.

For WACC $r$, useful life $T$, annual operations fraction $f_o$, insurance
fraction $f_{\mathrm{ins}}$, and terminal residual fraction $\rho$,

::: {#eq:capital-recovery-factor .equation}
$$
\operatorname{CRF}(r,T)=\frac{r}{1-(1+r)^{-T}},
\qquad
a_s(T)=\operatorname{CRF}(r,T)
+\!f_o+f_{\mathrm{ins}}
-\operatorname{CRF}(r,T)\frac{\rho}{(1+r)^T}.
$$
:::

Let $C_h$ be qualified accelerator capex, $C_I$ the sum of PV,
radiator, and storage capex, $M_h$ accelerator mass, $M_I$ launched
non-hardware mass after local closure, $\mu$ the destination launch
multiplier, $p_L$ the LEO launch price, $U_s$ delivered utilization, and
$C_{\mathrm{reg}}$ the annual spectrum and regulatory flow per installed
kilowatt. The complete space expression is

::: {#eq:space-lifecycle-cost .equation}
$$
L_s =
\frac{C_h a_s(T_h)+C_I a_s(T_I)
+p_L\mu[M_h a_s(T_h)+M_I a_s(T_I)]
+C_{\mathrm{reg}}}{U_s}
=\alpha+\beta p_L.
$$
:::

The integrated-disposable case sets $T_I=T_h$. The
serviceable/reusable-platform case sets
$T_I=\max(T_{I,\mathrm{anchor}},T_h)$. For Earth scenario $e$, PUE
$\psi_e$, electricity price $p_e$, data-center shell capex $C_{DC}$,
utilization $U_E$, and frontier-equivalent node penalty $\phi_e$,

::: {#eq:earth-lifecycle-cost .equation}
$$
L_E =
\frac{\phi_e\left[
C_{h,e}\operatorname{CRF}(r,T_{h,e})
+C_{DC}\operatorname{CRF}(r,15)
+8760p_e\psi_e\right]}{U_E}.
$$
:::

The responsive Earth case evaluates frontier and older-node hardware and
selects the lower $L_E$. Because $L_s$ is affine in launch price, the
exact break-even is

::: {#eq:launch-price-break-even .equation}
$$
p_L^*=\frac{L_E-\alpha}{\beta};
$$
:::

a negative value means non-launch costs alone exceed the Earth
counterfactual.

For the central LEO serviceable-platform case,
$C_h=\$63{,}640/\mathrm{kW}$, $C_I=\$15{,}003/\mathrm{kW}$,
$M_h=17.3$ and $M_I=36.9\ \mathrm{kg/kW}$,
$p_L=\$2{,}366/\mathrm{kg}$, $a_h=0.3584$, $a_I=0.2277$,
$C_{\mathrm{reg}}=\$158/\mathrm{kW\!-\!yr}$, and $U_s=0.786$.
Substitution gives

::: {#eq:space-cost-substitution .equation}
$$
\begin{aligned}
L_s
&=
\frac{
\begin{aligned}
&63{,}640(0.3584)+15{,}003(0.2277)\\
&+2{,}366[17.3(0.3584)+36.9(0.2277)]+158
\end{aligned}
}{0.786}\\
&=\$77{,}559/\mathrm{kW\!-\!yr}.
\end{aligned}
$$
:::

The matched lifecycle decomposition tests what “the cost changes kind”
actually means. Values below are central annualized
USD/frontier-equivalent-kW-year, with paired Monte Carlo p10–p90 in
parentheses. “Omitted” is not zero social cost or a favorable result; it
means that the implemented Part II boundary does not price the category.

| common lifecycle category | Earth base | LEO serviceable | space − Earth |
|---|---:|---:|---:|
| site or access rights | omitted | omitted | +0 |
| regulation and permitting | omitted | 201 (74–526) | +201 |
| transport and logistics | omitted | 35,042 (21,053–60,624) | +35,042 |
| energy | 936 (651–1,302) | 260 (148–467) | −675 |
| feedstock and materials | omitted | omitted | +0 |
| extraction and processing | omitted | omitted | +0 |
| manufacturing and hardware | 11,448 (8,116–15,175) | 25,589 (15,115–42,016) | +14,142 |
| construction and commissioning | 2,286 (1,708–3,154) | 2,403 (1,609–4,585) | +117 |
| labor or human intervention | omitted | omitted | +0 |
| maintenance, replacement and insurance | omitted | 16,570 (10,588–33,290) | +16,570 |
| coordination and verification | omitted | 453 (235–1,071) | +453 |
| decommissioning and disposal | omitted | 74 (27–199) | +74 |
| externalities | omitted | omitted | +0 |
| financing | allocated within annualized asset terms | allocated within annualized asset terms | +0 |
| residual-value credit | omitted | −3,033 (−7,312–−1,358) | −3,033 |
| **implemented total** | **14,669** | **77,559** | **+62,890** |

: Matched central lifecycle-cost contributions for terrestrial and orbital compute. [View data](../outputs/integrated/tables/matched_lifecycle_cost_contributions.csv){.artifact-link data-artifact="outputs/integrated/tables/matched_lifecycle_cost_contributions.csv"}. {#tbl-lifecycle-cost-contributions}

The contribution shares do change materially: hardware is about 78% of the
implemented Earth total, whereas the LEO total is led by transport (45%),
hardware (33%), and maintenance/replacement/insurance (21%), before the
negative residual-value credit. In this central case, changing the
composition does **not** create an advantage—the space/Earth ratio is 5.29.
The machine-readable table
[matched lifecycle cost contributions table](../outputs/integrated/tables/matched_lifecycle_cost_contributions.csv){.artifact-link data-artifact="outputs/integrated/tables/matched_lifecycle_cost_contributions.csv"} preserves
all 15 categories, paired ranges, shares, and difference ranks. Its omission
flags prevent the result from being read as a complete societal-cost
comparison.

### The SpaceXAI economic thesis {#ii.3-spacexai-economic-thesis}

:::: {.economic-thesis}
**The strongest documented case is broader than cheap solar.** SpaceX defines
cost per token as a function of the model, compute hardware, and energy. Its
filings argue that near-continuous orbital solar can lower the energy term;
radiative rejection can reduce cooling power; reusable launch, satellite mass
production, and Starlink links can lower deployment and distribution costs;
and faster access to power can put newer, more efficient chips into service
before a terrestrial facility clears construction and interconnection
queues. Proprietary chips and prospective vertical integration are meant to
attack compute depreciation, which SpaceX itself calls the largest current
cost-per-token component [S37] [S38] [S102].

That is a testable thesis, not a disclosed cost result. SpaceX tells the SEC
that it does **not** publish a specific comparable cost-per-token figure, that
the metric was not then used by management to evaluate performance or
allocate resources, and that the filed comparison does not promise the
industry's lowest cost per token [S102]. The public record also lacks a fixed
workload and
quality boundary, full lifecycle bill, achieved AI1 availability and life,
delivered communications goodput, and a commissioning/replacement record.
::::

Musk supplied a separate dated prediction at the World Economic Forum on
**January 22, 2026**: space would become the lowest-cost place to put AI
“within two years, maybe three, three at the latest” [S103]. The comparison
window is therefore January 22, 2028 through January 22, 2029. “Place to put
AI” leaves the denominator ambiguous—it may mean marginal energy, installed
compute, inference service, accepted output, or full lifecycle cost—so the
statement is retained as a falsifiable comparison target, never as an
engineering input.

| proponent claim | model term | observable that would discriminate | current boundary |
|---|---|---|---|
| continuous solar lowers energy cost | energy, utilization, power overhead | delivered IT kWh, losses, degradation, achieved availability | nameplate values disclosed; full energy cost and availability absent |
| radiative rejection lowers cooling overhead | radiator and thermal-loop mass, capex, pumping | sustained heat rejection, junction temperature, full-loop mass/power/life | 110 m² disclosed; system performance and cost absent |
| reuse lowers deployment cost | launch $/kg, cadence, vehicle depreciation | achieved reusable payload, allocated cost/kg, turnaround, reliability | $185/kg is a target-derived ceiling; flight-asset depreciation remains a cost |
| satellite mass production lowers cost | manufacturing, bus, NRE | recurring factory cost/kW, yield, throughput, acceptance cost | scale asserted; unit cost and yield absent |
| high kW/t lowers launch mass | kg per sustained average delivered kW | as-flown mass and sustained service-quality IT load | AI1 states 70 kW/t; long-run target 100 kW/t; independent conventional range 34–59 kg/kW |
| proprietary chips lower depreciation | qualified hardware capex, efficiency, refresh life | qualified cost, accepted tokens/W, yield, failures, economic life | depreciation called largest component; no comparable value disclosed |
| orbital hardware amortizes long enough | hardware/infrastructure life | cohort survival, radiation faults, repair, retirement | AI1 achieved life absent |
| laser links deliver useful output | service goodput, communications capex, latency | application goodput, latency, contention, outage and gateway cost | architecture described; service result absent |
| modular replacement preserves value | replacement launch, serviceability, residual value | demonstrated exchange/repair, downtime, recovered value | no AI1 orbital repair or replacement record |
| orbit reaches useful power faster | production, launch, commissioning, ramp | matched contract-to-service and accepted-output trajectories | possible 2028 deployment; commissioning and ramp absent |
| terrestrial scarcity widens the gap | Earth power, PUE, site and schedule | matched forward power and construction trajectories | responsive/tight model cases exist; no company-matched path |
| space is lowest cost by 2028–2029 | lifecycle and accepted-output ratios plus schedule | frozen comparator, workload, quality, bill and commissioned output | company-only comparison is not computable |

: SpaceXAI proponent claim, model term, required observable, and current evidence boundary. [View data](../outputs/integrated/tables/spacexai_proponent_claim_crosswalk.csv){.artifact-link data-artifact="outputs/integrated/tables/spacexai_proponent_claim_crosswalk.csv"}. {#tbl-spacexai-claim-crosswalk}

#### Matching the denominator

The engineering reference remains 2026 USD per frontier-equivalent kW-year:
it exposes spacecraft mass, qualification, life, replacement, availability,
communications, and financing. The commercial translation is
**inference-only**. It fixes one reference model, FP8 precision, batch 64,
1,024 input and 256 output tokens, a frozen held-out acceptance rule, and the
same lifecycle boundary. For environment $e$, accepted annual output is
defined inline as $N_{\mathrm{acc},e}=8760q_{\mathrm{req}}n_{\mathrm{out}}
a_Qg_e$, and accepted-output cost as
$C_{\mathrm{acc},e}=10^6C_e/N_{\mathrm{acc},e}$. Here
$q_{\mathrm{req}}$ is raw fixed-workload requests per delivered kWh,
$n_{\mathrm{out}}$ is output tokens per request, $a_Q$ is the held-out
quality-pass fraction, and $g_e$ is the fraction delivered inside the
latency, network, and service boundary. Training tokens and changes in model
quality are excluded. Because $C_e$ already divides by physical
utilization, $g_e$ does not count physical uptime twice.

| case | evidence boundary | lifecycle $/kW-yr | versus Earth | $/million accepted output tokens | accepted-output ratio |
|---|---|---:|---:|---:|---:|
| terrestrial reference | generic Earth base | 14,669 | 1.00× | 12.10 | 1.00× |
| generic orbital model | generic serviceable LEO | 77,559 | 5.29× | 81.01 | 6.70× |
| independent conventional-mass reference | 46.5 kg/kW midpoint of 34–59 kg/kW; other terms held common | 71,304 | 4.86× | 69.82 | 5.77× |
| `spacexai_proponent_case` | dated company quantities only | not computable | — | not computable | — |
| `spacexai_proponent_hybrid` | company targets plus visible model completions | 15,957 | 1.09× | 14.71 | 1.22× |

: Denominator-matched SpaceXAI economic comparison under one fixed inference workload and lifecycle boundary. [View data](../outputs/integrated/tables/spacexai_economic_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/spacexai_economic_comparison.csv"}. {#tbl-spacexai-economic-comparison}

The company-only case is deterministic but incomplete: every dated company
quantity is retained, while hardware capex, manufacturing cost, life,
availability, communications goodput, replacement, and useful-capacity ramp
remain `not_disclosed`. Its
[company-only register](../outputs/integrated/tables/spacexai_proponent_case.csv){.artifact-link data-artifact="outputs/integrated/tables/spacexai_proponent_case.csv"} therefore
does not produce a cost. The
[proponent-hybrid register](../outputs/integrated/tables/spacexai_proponent_hybrid.csv){.artifact-link data-artifact="outputs/integrated/tables/spacexai_proponent_hybrid.csv"}
separately exposes the $185/kg and 100 kW/t company targets and the
non-company completions—1.2× qualification, seven-year life, 0.95
utilization, 0.85 service goodput, and a nine-month ramp. It is a model
boundary, not “Musk's cost estimate.”

#### Time to useful compute and joint conditions

Ordinary WACC does not price the option value of earlier useful capacity. A
separate schedule calculation therefore starts at January 22, 2026, applies a
common 10% discount rate, and integrates accepted output through both forecast
deadlines. The Earth scenario assumes two years for construction,
interconnection, and commissioning followed by a six-month ramp. The
company-only case preserves the possible-2028 deployment statement but
returns `not_computable` because commissioning and useful-output ramp are
undisclosed. The hybrid starts useful output on January 22, 2028 and assumes a
nine-month ramp. Through January 22, 2029, it supplies 0.528 billion
discounted accepted tokens per final kW versus Earth's 0.710 billion, or
0.743×. Matching Earth's dated output requires, one axis at a time, first
useful output within about **1.79 years** of the statement or a ramp below
about **0.33 years**. These are thresholds, not forecasts. The complete
[time-to-useful-compute table](../outputs/integrated/tables/spacexai_time_to_useful_compute.csv){.artifact-link data-artifact="outputs/integrated/tables/spacexai_time_to_useful_compute.csv"}
keeps every schedule class and missing value visible.

| one-at-a-time condition | tested range | lifecycle ratio range | accepted-output ratio range | parity threshold within range |
|---|---:|---:|---:|---|
| launch price | $0–3,000/kg | 1.05–1.59× | 1.18–1.77× | none |
| total mass | 5–20 kg/kW | 1.07–1.12× | 1.20–1.25× | none |
| qualification | 1.0–3.0× | 0.94–2.46× | 1.05–2.75× | LCO at 1.085×; no accepted-token parity |
| hardware life | 3–10 yr | 1.60–0.98× | 1.78–1.10× | LCO at 9.29 yr; no accepted-token parity |
| utilization | 0.65–0.99 | 1.59–1.04× | 1.78–1.17× | none |
| hardware capex | $20,000–45,000/kW | 0.72–1.40× | 0.80–1.56× | LCO at $30,319; accepted output at $26,456 |
| space WACC | 0.08–0.22 | 0.89–1.31× | 0.99–1.47× | LCO at 0.119; accepted output at 0.082 |
| service goodput | 0.50–1.00 | 1.09× | 2.07–1.03× | none |

: One-at-a-time sensitivity around `spacexai_proponent_hybrid`; every unvaried term remains at the registered hybrid boundary. [View data](../outputs/integrated/tables/spacexai_threshold_tornado.csv){.artifact-link data-artifact="outputs/integrated/tables/spacexai_threshold_tornado.csv"}. {#tbl-spacexai-thresholds}

Figure [@fig-spacexai-threshold-tornado] shows the full one-at-a-time
accepted-output spread, including schedule variables that affect dated output
without changing steady-state LCO.

![One-at-a-time SpaceXAI proponent-hybrid sensitivity. Horizontal spans show
the accepted-output cost ratio produced by each registered low and high
endpoint; diamonds mark the hybrid base and the dashed line marks Earth
parity.](../outputs/integrated/figures/spacexai_threshold_tornado.png){#fig-spacexai-threshold-tornado
.figure-wide fig-alt="Horizontal sensitivity ranges for eleven SpaceXAI economic and
schedule parameters, with the hybrid base above Earth parity."}

No single launch-price, mass, utilization, communication, or goodput change
in the registered range makes the hybrid cheaper on both denominators. An
explicitly **joint** favorable corner—$0/kg launch, 5 kg/kW, 1.0×
qualification, ten-year life, 0.99 utilization, zero communications capex,
$20,000/kW hardware, 8% space WACC, full service goodput, first output in
1.75 years, and a three-month ramp—does reach 0.39× Earth LCO, 0.37×
accepted-output cost, and 1.61× Earth's discounted output by January 2029.
That corner establishes genuine agreement: orbital solar and an extremely
favorable integrated architecture can win. The present disagreement is over
the simultaneous achievement of qualification, hardware cost, lifetime,
availability, thermal-system mass, replacement, communications, and
schedule—not over personalities and not over solar's direction of effect.

A fourth, explicitly conditional **SpaceXAI — AI1 disclosed design** does
not replace those references. SpaceX publishes a 150 kW peak / 120 kW
average compute payload, 150 kW solar array, 70 kW/tonne vehicle efficiency,
110 m² liquid radiator, and deployed dimensions of 20 by 70 m [S38]. The
model uses the array/average-load ratio of 1.25. Because the page does not
say whether the 70 kW/tonne numerator is peak or average, aggregate vehicle
mass is sampled over the derived **14.3–17.9 kg per average kW** range and
the direct disclosures retain `company_statement` provenance while the
interpretation range is labeled `ASSUMPTION`. Radiator area, dimensions,
redundant loops, shielding, and laser links are recorded but receive no
invented mass or cost where none is disclosed. Hardware cost, qualification,
life, achieved availability, and launch price retain the existing anchors.

The lifecycle split is explicit and assumption-class. AI1 publishes only
aggregate vehicle mass, so the model first constructs the generic
accelerator/PV/radiator/storage/structure mass budget and then scales every
component by one common factor until its sum equals the sampled AI1 total.
The resulting generic **hardware-versus-infrastructure proportion** assigns
accelerator mass to the hardware refresh life and the balance to the
infrastructure life in the serviceable case; the disposable case amortizes
both on the hardware life. Capex is not inferred from vehicle mass:
qualified generic accelerator capex is retained, while generic PV,
radiator, and storage capex is evaluated at AI1's disclosed 1.25
array-to-average-load ratio. The aspirational 10 kg/kW case uses the same
proportional split. Neither that mass decomposition nor physical
serviceability is disclosed by SpaceX; both are `ASSUMPTION`, and the
serviceable AI1 and 0.76× boundary depend on them.

A fifth case is a deliberately optimistic, deterministic boundary rather
than a new baseline: **SpaceXAI — long-term targets plus favorable model
assumptions**. It uses
SpaceX's formal ≥99% launch-cost-reduction target as **$185/kg** and the
prospectus's long-term **100 kW/t** orbital-compute scaling assumption
(10 kg per average kW) [S37]. Because the company does not publish achieved
AI1 qualification cost, useful life, or compute availability, the case
separately labels as `ASSUMPTION` the favorable existing model bounds:
1.2× qualification, seven-year hardware life, and 0.95 utilization. It is
excluded from Monte Carlo. Treating a target and three selected favorable
bounds as probability distributions would manufacture a spurious
probability of success.

**Dated scenario policy.** The named line is retained for the specificity of
its public design inputs, not because SpaceXAI is the only orbital-AI
program. As of July 28, 2026, the comparison class is publicly documented
programs proposing or demonstrating space-based machine-learning or
data-center compute, together with the launch, spacecraft, communications,
and industrial capabilities of their named legal entities or disclosed
partners. In that class, Google and Planet target two Project Suncatcher
prototype satellites for early 2027 [S92]; Starcloud reports an H100
demonstrator launched in November 2025 [S93]; and Blue Origin's Project
Sunrise application was accepted for filing, not authorized or deployed
[S94].

Every relevant model family therefore keeps the same ordered tracks:
`generic_reference`, `independent_reference`,
`spacexai_disclosed_design`, `spacexai_stated_aspiration`, and an
affiliate hybrid only where a separately identified input is necessary.
An independent result appears only when units and denominators match;
otherwise the registry publishes `not_parameterizable` and the missing
fields. The [scenario input register](../outputs/integrated/tables/orbital_ai_scenario_inputs.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_ai_scenario_inputs.csv"},
[simulation coverage audit](../outputs/integrated/tables/simulation_scenario_coverage.csv){.artifact-link data-artifact="outputs/integrated/tables/simulation_scenario_coverage.csv"},
and [scenario results and axis markers](../outputs/integrated/tables/orbital_ai_scenario_results.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_ai_scenario_results.csv"}
preserve stable scenario identifiers, evidence classes, source snapshots,
parameter completeness, actor boundaries, and the reasons a numerical line
cannot be constructed. The disclosed design supplies six of the 24
full-lifecycle fields; the target case supplies nine only after its
analyst-selected completion values are counted. No target, specification,
or filing is represented as commissioned capacity.

**Post-IPO architecture calibration.** The technical literature available
by late July 2026 does not supply one new "correct" mass-to-power ratio. It
separates three architectures that should not be blended into one Monte
Carlo distribution.
Turyshev's independent 1 MW high-sunlight closure allocates 29.4 kg/kW to
PV, storage, and radiators; fixed spacecraft functions raise the total to
**34–59 kg/kW** [S39]. This independently brackets the model's 46 kg/kW
central generic LEO case and supports its order-of-magnitude placement,
although the
model's full component-corner envelope (about 25–91 kg/kW) is wider. AI1's
derived 14.3–17.9 kg/kW sits below that conventional envelope and remains a
separate company-specification case. Below both are research architectures:
an integrated solar-compute-radiator panel concept at about **8.9 kg/kW**
and a tethered inference architecture at about **5 kg/kW** [S40]. Those
figures are legitimate lower-bound scenarios, but depend respectively on
kilometer-scale integrated arrays, unqualified vapor chambers, thin tandem
PV and custom ASICs, or on long tethers, distributed deployment, shielding,
station-keeping, and micrometeoroid tolerance. They are pre-prototype
architecture claims, not evidence that the generic spacecraft prior should
move to 5–10 kg/kW.

**Thermal closure is a system, not a radiator-panel coefficient.** NASA's
flight and mission studies distinguish 2.75 kg/m² ISS radiator panels from
**8.8 kg/m²** after fluid loops and deployment are included; a JIMO study
estimated **5 kg/m²** for the complete system. At 353 K radiator temperature,
0.86 emissivity, and a 173 K environmental sink, the cited sizing is about
1.4 m²/kW, implying roughly **7–12 kg/kW** for the complete heat-rejection
system [S43]. This supports the middle and upper part of the model's
3–12 kg/kW range, but shows that its low end represents advanced emitters,
not a demonstrated full stack of cold plates, pumps, transport lines,
deployment, and controls.

AI1 makes the ambiguity visible. Its published 110 m² radiator for 120 kW
average compute is 0.92 m²/kW of quoted area [S38]. The one-face versus
two-face convention alone moves the idealized surface-temperature result
materially.[^p2-ai1-radiator-area] The disclosure is not thermodynamically
impossible, but its area convention, coolant temperature, and full
thermal-system mass are crossover-critical unresolved measurements.

[^p2-ai1-radiator-area]: If 110 m² is physical footprint and both faces emit,
    the mean flux is about 545 W/m² and the ideal surface is about 332 K
    (59 °C); if it is total emitting area, the values are about 1,090 W/m² and
    391 K (118 °C). The check uses
    $q=\epsilon\sigma(T^4-T_{\mathrm{env}}^4)$ with the NASA reference
    conditions [S43], and omits view factors,
    degradation, nonuniformity, pumping, and the chip-to-radiator temperature
    drop.

The terrestrial counterfactual **responds** — the epistemic requirement
the static comparison missed. Three scenarios: *tight* prices scarcity (the
politics-binds branch: permitting and climate commitments hold); *base*
takes the anchors; *responsive* prices induced supply at the cheapest
permitted firm-power floor — nuclear PPA, or the politically conditional
natural-gas floor at $0.04–0.06/kWh (CCGT under $1,000/kW, ~2-year builds
[S35]) — with an older-node hardware option taken when it wins on
compute-normalized cost. Aspirational launch targets are sweep axes except
in the explicitly labeled deterministic best case above; they never enter
the probabilistic baseline.

**Starship V3/V4 aspiration, normalized.** SpaceX's June 2026 prospectus
does not quote a V3 or V4 customer price or a vehicle-specific cost per
flight. It states instead that fully reusable V3 is designed to carry
100 metric tonnes to orbit, that a future generation could reach 200
tonnes as soon as V4, and that mature Starship is intended to reduce the
historical $18,500/kg cost benchmark by 99% or more [S37]. Exactly 99%
implies **$185/kg**; "or more" implies a lower value. Table
[@tbl-launch-cost-sensitivities] converts
that formal aspiration and three more aggressive sensitivity cases into
full-payload flight-cost equivalents:

| LEO sensitivity case | $/kg | V3: 100 t full-load equivalent | V4: 200 t full-load equivalent | status |
|---|---:|---:|---:|---|
| formal corporate aspiration | ≤$185 | ≤$18.5M | ≤$37M | derived from the stated ≥99% reduction; not a price quote |
| aggressive mature-Starship case | $100 | $10M | $20M | scenario axis |
| extreme fuel-like case | $50 | $5M | $10M | scenario axis |
| extreme lower case | $30 | $3M | $6M | scenario axis |

: Mature-Starship launch-cost sensitivity axes and full-load equivalents. {#tbl-launch-cost-sensitivities}

The dollar-per-flight columns are arithmetic (`$/kg × full payload`), not
company forecasts.[^p2-flight-arithmetic] Under-filled flights cost more per delivered kilogram;
external customer prices can exceed internal marginal cost; and none of
these figures includes a demonstrated cadence, reuse count, refurbishment
burden, or capital-recovery schedule. This analysis therefore uses
**$185/kg as the traceable corporate aspiration, $100/kg as an aggressive
case, and $30–50/kg only as an extreme fuel-like sensitivity band**. All
remain comparison axes; $185/kg also enters the quarantined deterministic
best case, never the Monte Carlo.

[^p2-flight-arithmetic]: The V4 full-load totals rise because Table
    [@tbl-launch-cost-sensitivities] holds
    dollars per kilogram constant while payload doubles. Holding flight cost
    instead constant gives the inverse comparison: a $10 million flight is
    $100/kg on a full 100-tonne V3 and $50/kg on a full 200-tonne V4.

Two financing caveats are deliberate modeling choices. Earth uses an
8–15% WACC range and space a separate 10–22% range. Qualification
multiplier, service life, repairability, and utilization are still sampled
as separate anchored quantities; the favorable corner likely has correlated
engineering causes, so its deterministic result is a boundary rather than a
joint probability claim.
Calibration: the Earth base case works out to ≈$1.7/kWh, matching
published accelerator rental rates.

**Cost accounting — included and excluded.** Included: IT hardware with
qualification premium; PV, radiators, storage, structure and their launched
mass (with cislunar/lunar delivery multipliers); pumping power, rejection
temperature, chip-to-radiator temperature drop, environmental view factor,
and a thermal-reliability mass margin; spacecraft bus, communications,
ground network, program NRE, insurance, spectrum/regulatory cost, disposal,
and residual value; capital recovery at the architecture-specific WACC with
component-specific lives; compute-hardware replacement and its launch mass
on the refresh cycle; an operations fraction for ongoing ground segment,
downlink, and station-keeping; utilization derating; Earth-side DC capex,
PUE, hardware refresh, and firm-power floors. Excluded: launch-site,
landing, turnaround, and fleet infrastructure beyond whatever is implicit
in the $/kg target; launch failure beyond the insurance proxy; collision
externalities and constellation-replenishment logistics; tax treatment; and
architecture-specific link budgets or regulatory outcomes. Turyshev's
independent inequality remains a useful cross-check: at
40 kg/kW, a terrestrial infrastructure allowance of $10,000–40,000/kW
permits only **$250–1,000/kg for launch and spacecraft build combined**
before communications, operations, utilization, and finite-life penalties
[S39].
The net direction of the remaining exclusions is **not** claimed to be
uniformly conservative. The reported multiples are stylized-architecture
outputs with wide `ASSUMPTION` ranges; the robust conclusion is
structural — *which* terms dominate — not the exact ratios.

## II.3 Results {#ii.3-results}

Central reference values plus the deterministic aspiration case ($ per
kW-yr, rounded to three significant figures — these are
assumption-conditioned outputs, not measurements; exact machine-readable
values regenerate in `outputs/`):

| case | architecture | LCO | launched mass | vs Earth base (≈14,700) |
|---|---|---:|---:|---:|
| LEO inference | serviceable/reusable platform | 77,559 | 54 kg/kW | 5.29× |
| LEO inference | integrated disposable satellite | 98,871 | 54 kg/kW | 6.74× |
| cislunar batch | serviceable/reusable platform | 131,524 | 54 kg/kW | 8.97× |
| cislunar batch | integrated disposable satellite | 175,418 | 54 kg/kW | 11.96× |
| lunar surface (Earth-supplied) | serviceable/reusable platform | 3,864,754 | 480 kg/kW | 263× |
| lunar surface (Earth-supplied) | integrated disposable satellite | 6,209,841 | 480 kg/kW | 423× |
| SpaceXAI — AI1 disclosed design | serviceable/reusable platform | 46,523 | 16 kg/kW | 3.17× |
| SpaceXAI — AI1 disclosed design | integrated disposable satellite | 55,748 | 16 kg/kW | 3.80× |
| SpaceXAI — long-term targets plus favorable model assumptions | serviceable/reusable platform | 15,957 | 10 kg/kW | 1.09× |
| Earth tight | — | 15,980 | — | — |
| Earth responsive | — | 12,783 | — | — |

: Deterministic lifecycle-cost results across modeled architectures and scenarios. {#tbl-deterministic-lco-results}

The integrated-disposable and serviceable-platform rows use different
lifecycle boundaries.[^p2-lifecycle-boundary] The lunar case is labeled
**Earth-supplied** because its central closure fraction is zero; local
manufacture enters only through the closure sweep axis.

[^p2-lifecycle-boundary]: Integrated-disposable rows annualize PV, radiators,
    storage, structure, and emplacement launch on the short compute-refresh
    life. Serviceable-platform rows instead use the declared
    `infrastructure_life_years` range of 10–25 years, while replacement chips
    and their launch mass recur on the compute life; Appendix B gives the full
    cost boundary.

Monte Carlo over anchored ranges, shared draws both sides (n = 2,000
sampled runs per row; frequencies under this ensemble, not empirical
probabilities). The stated-aspiration case is excluded because its company
targets and favorable unpublished assumptions are point sensitivities, not
probability distributions:

| case | architecture | vs Earth | ratio p10/p50/p90 | space-cheaper runs | break-even $/kg p50 (p90) |
|---|---|---|---|---|---|
| LEO inference | serviceable/reusable | base | 3.6 / 5.7 / 8.8 | 0 / 2,000 | −987 (−385) |
| LEO inference | serviceable/reusable | responsive | 4.5 / 7.1 / 11.4 | 0 / 2,000 | −1,129 (−543) |
| LEO inference | integrated disposable | base | 4.6 / 7.3 / 11.5 | 0 / 2,000 | −883 (−425) |
| LEO inference | integrated disposable | responsive | 5.5 / 9.0 / 14.8 | 0 / 2,000 | −980 (−491) |
| cislunar batch | serviceable/reusable | base | 5.8 / 9.7 / 16.6 | 0 / 2,000 | −291 (−96) |
| cislunar batch | serviceable/reusable | responsive | 6.9 / 12.1 / 20.8 | 0 / 2,000 | −349 (−136) |
| cislunar batch | integrated disposable | base | 7.4 / 12.8 / 22.7 | 0 / 2,000 | −277 (−108) |
| cislunar batch | integrated disposable | responsive | 9.0 / 16.0 / 28.3 | 0 / 2,000 | −308 (−145) |
| lunar surface (Earth-supplied) | serviceable/reusable | base | 112.0 / 263.9 / 652.8 | 0 / 2,000 | −21 (−9) |
| lunar surface (Earth-supplied) | serviceable/reusable | responsive | 138.5 / 343.8 / 821.2 | 0 / 2,000 | −22 (−10) |
| lunar surface (Earth-supplied) | integrated disposable | base | 183.3 / 449.4 / 1,092.7 | 0 / 2,000 | −16 (−7) |
| lunar surface (Earth-supplied) | integrated disposable | responsive | 232.4 / 562.4 / 1,313.0 | 0 / 2,000 | −17 (−8) |
| SpaceXAI — AI1 disclosed design | serviceable/reusable | base | 2.3 / 3.3 / 4.9 | 0 / 2,000 | −3,567 (−1,624) |
| SpaceXAI — AI1 disclosed design | serviceable/reusable | responsive | 2.7 / 4.2 / 6.4 | 0 / 2,000 | −4,087 (−1,964) |
| SpaceXAI — AI1 disclosed design | integrated disposable | base | 2.7 / 4.0 / 5.9 | 0 / 2,000 | −3,097 (−1,590) |
| SpaceXAI — AI1 disclosed design | integrated disposable | responsive | 3.3 / 4.9 / 8.0 | 0 / 2,000 | −3,579 (−1,924) |

: Paired Monte Carlo lifecycle-cost ratios and break-even launch prices. {#tbl-monte-carlo-lco-results}

Earth and space see the same sampled hardware properties in every draw,
while their WACC anchors remain deliberately separate.[^p2-shared-draws]
The frequencies belong to this declared ensemble and are not empirical
probabilities.

[^p2-shared-draws]: Each anchor draw is cached per iteration and keyed by a
    process-stable seed, making the tables deterministic across processes.
    Appendix C specifies the keyed-draw and seed protocol.

All sixteen architecture/reference rows have zero sampled points below
parity in 2,000 draws. This is a design-space statement under the declared
sampling measure, not a confidence bound on real-world success. Figure
[@fig-lco-ratio-monte-carlo] shows the separation from parity across the
sampled cells without assigning real-world probabilities to them.

![Distribution of the space/Earth cost ratio over the anchored Monte
Carlo, shared draws both sides. No draw crosses parity in any
architecture/reference cell.](../outputs/figures/lco_ratio_mc.png){#fig-lco-ratio-monte-carlo
.figure-wide fig-alt="Distribution plot of space-to-Earth lifecycle-cost ratios
for sixteen architecture and Earth-reference combinations."}

AI1's aggregate mass disclosure is material but not sufficient at the
retained central values: it cuts launched mass from about 54 to 16 kg/kW
and LCO from about $77,600 to $46,500/kW-yr, yet fixed non-launch costs
still exceed Earth base (central break-even approximately −$3,460/kg).
With the remaining anchors simultaneously favorable — qualification ×1.2,
seven-year life, and 0.95 utilization — AI1 is 1.74× Earth at the central
launch anchor, has no positive break-even launch price (approximately
−$191/kg), and reaches 1.13× at $250/kg. Completing communications, bus,
NRE, insurance, spectrum, disposal, thermal-margin, and financing terms
leaves no favorable-corner crossover at these assumptions.

The aspirational case makes that conditionality explicit. The two company
numbers alone—$185/kg and 100 kW/t—still produce about **$34,200/kW-yr,
2.33× Earth base** when qualification, life, and utilization remain at
their central values. Selecting the three favorable non-company bounds as
well produces about **$16,000/kW-yr, 1.09× Earth base**. The
incomplete-cost boundary produces 0.76×; including the omitted system
terms reverses that result. All five favorable conditions must hold
together, and the model assigns no probability to them.

The company's own scale target exposes the feasibility burden. At 100 GW
deployed annually and 100 kW/t, the flow is **one million tonnes/year**:
10,000 full 100-t V3 launches (27.4/day), or 5,000 full 200-t V4 launches
(13.7/day), and roughly 833,000 AI1-sized 120-kW-average spacecraft. Even
at $185/kg, launch cost alone is $185 billion/year before spacecraft
manufacture. At the later AI1 page's disclosed 70 kW/t, the same flow rises
to 1.43 million tonnes and 14,286 full V3 launches/year. The current design
is therefore 30% below the older 100 kW/t assumption; reaching it requires
43% more kW/t. Full rapid reuse, daily turnaround at unprecedented cadence,
upper-stage recovery, fleet size, range capacity, and manufacturing are
load-bearing. So are seven-year whole-system reliability and 95% compute
utilization, neither published for AI1. Collision externalities,
constellation replenishment logistics, and landing/turnaround infrastructure
remain excluded, while
terrestrial energy, chips, cooling, permitting, and construction can also
improve. The prospectus itself identifies approvals and spectrum as
dependencies and warns that better terrestrial energy could reduce the
orbital advantage [S37].

The lifetime interpretation is architecture-dependent. The model's
10–25-year infrastructure life is defensible only if the power and thermal
platform survives multiple accelerator generations and the compute payload
can actually be exchanged, serviced, or economically separated. For an
integrated, non-serviceable LEO vehicle, the relevant infrastructure life is
instead close to the spacecraft or compute life—typically about five years
in the studies reviewed here [S39–S42]. The serviceable-platform and
integrated-disposable results above expose both lifecycle readings.
Shortening every component to five years is appropriate for an integrated
vehicle, but too pessimistic once modular payload replacement is
demonstrated. Platform reuse is a named architecture gate, not an innocuous
amortization choice.

A negative break-even means fixed, non-launch costs alone exceed the Earth
cost: at those draws no launch price, even zero, closes the gap. The
structural finding: **the crossover is gated by the space-qualification
premium, equipment life, and utilization — not launch price alone.** The
generic-LEO crossover surface (launch $/kg × life × qualification ×
radiator × closure × chip efficiency) shows no ratio-below-1 region at
published prices on any single axis, and near-parity only in the defined
Starship aspiration cases
($185/kg formal; $100/kg aggressive; $30–50/kg extreme) combined with
favorable values on at least two other axes. AI1's disclosed aggregate
mass is a multi-parameter architecture constraint rather than a single-axis
point on that generic surface; it produces the conditional near-published
break-even above while leaving no competitive draw in either lifecycle
ensemble. At the
central LEO
architecture's approximately 54 kg/kW, those prices correspond to initial
launch expenditures of about **$9,990, $5,400, $2,700, and $1,620 per
installed IT kW**, respectively, before annualization. They largely remove
the current launch bill, but a negative break-even still means they cannot
overcome the fixed qualification/life/utilization gap on their own. Lunar
closure is the weakest
lever: chips are never closed, so even 95% closure of non-chip mass leaves
the lunar case roughly 15–30× Earth at published prices — still more than
an order of magnitude from parity. Figure [@fig-crossover-surface] displays
the five one-axis sweeps on a common logarithmic cost-ratio scale.

![The generic-LEO crossover surface: space/Earth cost ratio against
launch price with each companion axis varied over its anchored range. No
single-axis path reaches parity at published prices.](../outputs/figures/crossover_surface.png){#fig-crossover-surface
.figure-wide fig-alt="Crossover sensitivity panels showing the generic
LEO-to-Earth cost ratio against launch price and one companion parameter at a
time."}

The mass-multiplier refinement: at anchored values a 2× FLOPS/W advantage
buys about 50% of the benefit of halving launch price (ratio 5.1 vs
4.2 at $3,000/kg, both from 6.1), because the hardware term — untouched by
efficiency — dominates both mass and capex. "The compute tax outweighs the
launch tax" [S34] becomes true only after the qualification premium and
hardware $/kW fall; near-term, both taxes are subordinate to qualification
and life.

## II.4 External claim and independent-study checks {#ii.4-external-claim-and-independent-study-checks}

The public crossover claims are recorded as comparison targets (never
inputs). The completed-cost model does not reproduce the stronger
Google/Planet crossover claim, even at its favorable anchored corner; this
converts the disagreement into an architecture- and accounting-wide,
testable one. The
post-IPO review of independent studies below then checks the model rather
than merely restating corporate claims. The Suncatcher design study does
**not** claim system-level parity. Its cost section states twice that it
is not a full economic analysis and not a comprehensive economic feasibility
study, and its comparison sets the **amortised launch component alone**
(≈$810/kW-yr for a Starlink-v2-class mass-to-power ratio at $200/kg;
$810–7,500 across satellite classes) beside terrestrial data-center
**electricity spend** (≈$570–3,000/kW-yr), explicitly excluding
infrastructure, building, and chip costs [S32]. That is a launch-cost
feasibility marker — the finding that launch need not remain independently
prohibitive — not a parity claim, and it is consistent with this model,
which reproduces launch as a minor term. The crossover claim this model
contradicts is the stronger reading in circulation [S34], not the study's
own.

- **The Google/Planet study** (reported: crossover at $200–300/kg [S34]).
  At $250/kg with central anchors: space/Earth = 2.61 — no crossover.
  Under the favorable corner *within anchored ranges* (qualification ×1.2,
  7-year life, 0.95 utilization, 3 kg/kW radiators): **1.26** — still no
  crossover. The disagreement is no longer localized to launch price or
  three performance inputs; the completed non-launch system boundary is
  load-bearing.
- **The Suncatcher design study** [S32] describes an 81-satellite
  dawn-dusk sun-synchronous cluster near 650 km with terabit-class
  optical links (an 800 Gbps unidirectional bench demonstration against
  a stated ~10 Tbps per-link requirement) and a learning-curve projection
  of ≲$200/kg by the mid-2030s — itself conditional on roughly 370,000
  tonnes of additional cumulative mass launched, on the order of 1,800
  Starship-class flights averaging ~180 per year, which the authors call
  ambitious. Its engineering results should be read precisely (arXiv v2,
  17 June 2026):
  - HBM was the most **TID**-sensitive subsystem — irregularities from
    ~2 krad(Si) against a ~750 rad(Si) shielded five-year requirement,
    with no hard total-dose failures to 15 krad(Si) — while core logic
    and on-chip SRAM were the most **SEE**-sensitive. The reported
    inference error probability is roughly one per three million
    inferences under the stated assumptions, with the effect on
    **training** explicitly reserved.
  - At ~150 rad(Si)/yr, a seven-year dose (~1.05 krad) sits below the
    ~2 krad irregularity onset — the radiation results support five-year
    TID survivability with margin and *do not obviously contradict
    seven-year TID survival*.
  - What they do not establish is seven-year **system** reliability:
    SEE-induced corruption, host interruptions, training sensitivity,
    thermal management, and whole-spacecraft failure remain unresolved,
    with orbital repair called impracticable and redundant provisioning
    proposed instead — a cost, not an absence of one. The COTS practice
    supporting a low qualification premium (unmodified accelerators
    flying on imaging satellites [S34]) demonstrates cheapness, not
    five-year reliability.

The independent checks localize four additional gates:

- **Conventional mass and economic closure.** Turyshev closes PV, eclipse
  reserve, thermal rejection, fixed spacecraft functions, sustained
  communication, utilization, and finite life in a single framework
  [S39]. Its 34–59 kg/kW total independently brackets and supports the
  generic central mass at the order-of-magnitude level. Its more
  important result is the combined launch-plus-build ceiling:
  $250–1,000/kg at 40 kg/kW before communications and lifecycle penalties.
  Every additional $1,000/kW of communication or operations cost reduces
  that allowance by $25/kg. Current public launch prices consume more than
  the entire allowance before a spacecraft is built.
- **Low-mass architectures are conditional, not contradictory.** The
  integrated-panel and tether studies reach 8.9 and roughly 5 kg/kW
  respectively [S40], demonstrating that mass is an architecture variable
  rather than a universal constant. Both target inference and both exchange
  conventional subsystem maturity for deployment, structural, thermal, and
  custom-silicon risk. They justify explicit stretch scenarios; they do not
  justify assigning conventional spacecraft a five-kilogram prior.
- **Inference and training are different products.** Van Berkel compares a
  terrestrial 8,000-accelerator Clos fabric with orbital meshes: about
  28,800 TB/s of terrestrial bisection bandwidth versus approximately
  2.25 TB/s for a two-dimensional and 10 TB/s for a three-dimensional
  orbital mesh at 100 Gbps links, with network latency 150–450 times higher
  [S41]. Even much faster optical links do not remove multi-hop diameter and
  collective-communication latency. The appropriate early comparison is
  therefore per-satellite or loosely coupled **inference**, preprocessing,
  and communication-integrated edge work—not frontier distributed training.
  Training should receive a network-performance model, not an ordinary
  utilization scalar.
- **Small space-native nodes already have a different cost structure.** The
  peer-reviewed HPCA microdatacenter study finds power and thermal systems
  dominate bespoke small-satellite TCO, while compute hardware can be less
  than one percent; energy-efficiency improvements can reduce TCO by about
  two-thirds and are up to 2.5 times more valuable in space [S42]. This is
  encouraging for 0.5–10 kW Earth-observation preprocessing, where data
  originates in orbit and downlink is avoided. It is not evidence that a
  megawatt terrestrial-substitution service has the same economics.

The broader policy cross-check reaches the same conditional result by a
different route. A University of Virginia assessment reports a simplified
five-year 1 GW case at $135.6 billion in orbit versus $16.6 billion on Earth
under present-style assumptions; near-parity appears only when launch falls
to $30/kg, satellite hardware to $10/W, specific power rises to 100 W/kg,
sunlight availability to 80%, and degradation and GPU failure both fall to
1% [S44]. Its model omits GPU cost, financing, insurance, logistics, and
downtime and should not be treated as a precise forecast. Its contribution
is the joint-condition result: parity emerges from several simultaneous
improvements, not from launch price alone.

Consequence for the staircase, stated within the model's service
definition: **the modeled orbital architectures are not cost-competitive as
substitutes for terrestrial frontier compute at the stated assumptions.**
That conclusion has a workload boundary: it applies directly to
per-node inference in the cost model, while the cited network evidence makes
frontier distributed training less favorable than the scalar model shows.
It does not price differentiated orbital products (in-orbit sensor
processing, sovereign or military demand, resilience niches), which could
be profitable while losing the commodity comparison. What follows for the
staircase is correspondingly bounded: *commodity-scale* deployment ahead of
the enabling corner is strategic positioning or learning investment rather
than substitute-compute profit — an observation Part III converts into a
discriminating test.

The electrical comparison is also reported in workload-specific units so a
kW-year is not silently treated as equivalent computational output:

| central service case | cost per million defined inferences | cost per network-effective training kW-year |
|---|---:|---:|
| Earth base | $3,197 | $17,989 |
| generic LEO, serviceable | $16,902 | $490,528 |
| SpaceXAI — AI1 disclosed design, serviceable | $10,138 | $294,235 |

: Workload-normalized costs for central terrestrial and orbital service cases. {#tbl-workload-normalized-costs}

The inference denominator is an `ASSUMPTION`-class workload requiring a
named model, latency, accuracy, batch, memory, precision, and availability
envelope. The training denominator applies explicit central network
efficiencies of 0.158 in space and 0.815 on Earth. These values expose the
interconnect gate; they are not benchmark measurements.

## II.5 Competition and milestone order {#ii.5-competition-and-milestone-order}

A one-dimensional “takeoff speed” label hides the relative order of digital,
embodied, capital, and control milestones. The branch screen therefore
crosses fast/slow digital progress with fast/slow physical closure. Its years
are named `ASSUMPTION` coordinates, not forecasts:

| branch | $T_{\mathrm{AIR\&D}}$ | $T_{\mathrm{emb}}$ | $T_{\mathrm{cl},E}$ | $T_{\mathrm{cl},S}$ | consequence |
|---|---:|---:|---:|---:|---|
| fast digital / slow physical | 4 | 12 | 16 | 26 | eight-year intelligence overhang before embodiment; off-world closure is post-AI construction |
| slow digital / fast physical | 18 | 6 | 9 | 14 | bounded intelligence can accompany physical closure; off-world closure precedes AI-R&D closure |
| fast digital / fast physical | 4 | 5 | 7 | 9 | both loops advance, but Earth still closes first |
| slow digital / slow physical | 18 | 14 | 20 | 28 | bridge capital and depreciation dominate both clocks |

: Milestone order under fast and slow digital and physical progress branches. [View data](../outputs/integrated/tables/milestone_order_branches.csv){.artifact-link data-artifact="outputs/integrated/tables/milestone_order_branches.csv"}. {#tbl-milestone-order-branches}

Fast digital progress does not remove experiment, actuator, factory,
material, deployment, or commissioning latency. It creates an intelligence
overhang whose useful product is limited by those complementary stocks.
Conversely, fast physical closure can compound with a bounded controller.
The article's off-world pathway is strategically causal rather than solely a
post-AI construction program only in orderings where off-world closure
changes the growth path before $T_{\mathrm{AIR\&D}}$; the sufficient screen
used here is $T_{\mathrm{cl},S}<T_{\mathrm{AIR\&D}}$. The matrix does not
assign that ordering a probability.

The fast-digital/slow-physical branch is a stress test against *AI 2027*,
not a copy of its calendar [S80]. That source explicitly focuses on a
software-driven feedback loop because improved hardware takes longer to
produce at scale, distinguishes coding execution from research taste, and
publishes wide uncertainty. Its site later corrected a plotted trajectory
and moved a median back while retaining a fast branch. Versioning is
therefore substantive: no date or compute allocation from that scenario
enters this model. [S35] supplies a separate fast-takeoff and
capital-mobilization countercase under its existing source entry. Its
ordering permits AI-R&D automation to precede broad robotics; the article's
embodied-closure path instead asks when physical tasks and capital
reproduction pass their own gates. Amodei's complement taxonomy [S79]
explains why both can be coherent: digital capability may move first while
hardware, data, experiments, human constraints, and physical law continue to
set the realized rate.

Control is an independent feasibility gate:

::: {#eq:milestone-control-gate .equation}
$$
\Gamma_{\mathrm{ctrl}}
=\mathbf 1\!\left[T_{\mathrm{ctrl}}\le T_{\mathrm{AIR\&D}}\right]
 \mathbf 1\!\left[T_{\mathrm{ctrl}}\le T_{\mathrm{cl},E}\right]
 \mathbf 1\!\left[T_{\mathrm{ctrl}}\le T_{\mathrm{cl},S}\right].
$$
:::

$\Gamma_{\mathrm{ctrl}}\in\{0,1\}$ is the branch-level control-admissibility
indicator and $\mathbf 1[\cdot]$ is one when its condition holds. Gross
capability or capacity that arrives before the relevant authorization and
verification regime is not counted as a successful endpoint.

A fifth branch makes the terrestrial counterfactual explicit. Powerful AI
first accelerates terrestrial robotics, fabs, power, and launch supply;
the illustrative screen closes Earth at year 10 and space at year 18 while
reducing the off-world bridge-cost index to 0.65. Lower bridge cost helps
space, but earlier Earth compounding raises the benchmark it must beat.
Machine-readable:
[milestone order branches](../outputs/integrated/tables/milestone_order_branches.csv){.artifact-link data-artifact="outputs/integrated/tables/milestone_order_branches.csv"}. The fast
AI-R&D countercase remains represented by [S35], without treating its
calendar as established.

The system is not alone. China is the closest existing implementation of
the terrestrial stages at national scale (solar, batteries, robotics,
rare-earth refining, trailing-edge fabrication) lacking, for now, a
reusable heavy-lift economy. Hyperscalers close the same inputs with
capital rather than ownership — power agreements, custom silicon, supply
contracts — which works until aggregate demand outruns what markets can
scale. State programs hold ISRU roadmaps but iterate slowly.

Two corrections to the launch-chokepoint assumption, both cutting against
a durable launch monopoly: payload cost-performance improved by two to
three orders of magnitude over the decade against a smaller multiple for
launch price [S34] — a crossover model treating launch as the primary axis
mis-weights its own sensitivity analysis (borne out in II.3, where the
crossover is not launch-gated); and chemical rockets are a local optimum —
mass-manufactured vehicles, electromagnetic or kinetic launch, and mass
drivers from a low-gravity surface (named in the fabrication initiative's
own material [S29]) would reset the launch axis rather than move along it.

**Externally induced supply versus internally controlled reproduction.**
Expansion purchased through markets can pay stacked scarcity rents when
demand outruns supply.
Properly qualified: markets are not static — the right formulation is a
race between demand growth and induced supply with multi-year capacity
lags as the binding term, and whether internal replication beats inducing
market expansion is a *rate comparison* (which is what the responsive
counterfactual of II.2 implements on the power axis). A self-replicating base escapes *mandatory dependence on external Earth markets* — not economic allocation, opportunity cost, or internal pricing, which persist in any multi-firm or internally-priced closed ecology: expansion re-denominates from currency into materials, energy, and time. Two caveats: the entry ticket is
still paid in dollars — the first self-replicating unit is bought, not
grown, which is what the bridge economy exists to finance — and the logic
predicts *convergence, not uniqueness*: every serious actor eventually
verticalizes or plateaus; the durable advantage is the shortest hardware
doubling time once everyone is. Historical reference classes calibrate
"unprecedented": Manhattan and Apollo peaked near 0.4% of GDP; British
railway investment ran ~40% of GDP over a decade; wartime borrowing far
exceeded either [S35]. Trillion-scale buildout is extreme but inside the
envelope. The relevant question is therefore the relative rate, financing,
and dependency structure—not escape from capital itself. The symmetric
dynamic diagnostic gives both Earth and space endogenous investment and
finds that physical space compounding does not become self-financing in
either declared 40-year case.

**Integration versus modularity (the Coasean resolution).** Markets scaled
semiconductors a billionfold through *dis*integration; why would this time
differ? A firm's boundary sits where internal coordination costs exceed
market transaction costs [S25]. AI attacks the internal term (Part I.6) — but it attacks the external one too, improving supplier discovery, specification, contracting, monitoring, quality assurance, pricing, logistics, and modular interface design. The correct conditional is therefore that **AI moves the efficient boundary toward integration only if it reduces internal coordination costs faster than it reduces interfirm transaction costs**, an empirical question this document does not settle; what does survive is that the market interface retains an irreducible capital requirement efficiency gains do not remove. The defensible conclusion is bounded: AI may move the efficient boundary toward integration — not that ownership integration outperforms modular ecosystems in general. Three qualifications are
central: markets also supply experimentation, selection, redundancy, and
price signals, which an integrated complex must replicate internally or
decay into soft-budget pathologies; technical closure (the network can
produce its inputs) must not be conflated with contractual or ownership
closure — this thesis requires only the first; and the in-domain
integration success story confounds integration with reusability, cadence,
and incentives [S1].

**The operating wall.** Physics-priced inputs (energy, materials,
machine-hours) fall with scale; society-priced inputs (land, permits,
interconnection, litigation, goodwill) rise with it — on Earth, closure
has a structural ceiling because land, law, and neighbors cannot be
internalized. Space shrinks and relocates the society-priced term rather
than abolishing it, with one favorable property: permission attaches to
the gateway (launches, spectrum) rather than the complex, so the millionth
robot needs no new municipal permit. The hard physical version: Earth has
a planetary waste-heat budget; space offers radiator area not bounded by a planetary surface (though still bounded by matter, transport, geometry, and maintenance — Part IV) —
though not free rejection. Two external observations bracket how hard the
wall binds *now*: data-center siting is already politically contested over
electricity, water, and land — the society-priced curve observed from
inside the industry [S34] — while the AGI-buildout literature meets the
same wall with natural gas and deregulation at a firm-power floor below
the nuclear PPA, never mentioning orbit [S35]. The wall binds through
politics more than physics or long-run capital — though near-term hardware (turbines, transformers, cooling, construction capacity) can also bind — and the difference between branches is a
parameter in this model, not a mood. And the sequence remains
brutal: before high closure, space is the most *expensive* place to
operate — every kilogram of spares travels at full launch freight while
depreciation runs at its worst (II.3's ~4–9×) — so the declining-cost
regime switches on only after κ is high, which is why the bridge economy
and the clock-setting components decide who survives to reach it.

**The threshold-model argument.** If RSI capability is a threshold — a
base model good enough to run verified improvement loops — a smarter
starting model confers a head start that the loop erodes; the durable
variable becomes who runs more loops, which is hardware. Mid-2026 evidence supports continued benchmark compression between open and proprietary models (open-weight releases benchmarking near the frontier [S12]); it does not establish commoditization at an autonomous-R&D threshold, so hardware dominance is the small-α branch of the model rather than the established trajectory. If RSI-grade capability does arrive in open weights, model advantage weakens sharply without evaporating — post-training, proprietary data, evaluation systems, inference infrastructure, tool integration, operational reliability, distribution, and the capacity to run physical experiments all persist as differentiators — and to that extent the contest shifts onto the physical loop, the strongest form of the verticalization thesis. The counterpoint: the argument holds only if
capability is threshold-like rather than continuously compounding
(L_RSI ∝ A^α·C^β·V^γ, with α unknown); benchmark convergence does not
establish that autonomous R&D capability is threshold-like. And the
structural counterweight: models converge because they train on the same
public data, so residual differentiation concentrates exactly in
proprietary physical-process data (Part I.2) — if general capability
commoditizes, the model contest narrows to the domains where training data
is generated by owned industry, folding the model race back into the
physical loop.

* * *
