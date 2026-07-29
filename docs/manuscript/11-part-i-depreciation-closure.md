## I.4 Depreciation: the harsh term {#i.4-depreciation-the-harsh-term}

::: {#eq:hardware-net-growth .equation}
$$
\frac{\mathrm d H}{\mathrm d t} = (r-\delta)H
$$
:::

Every claim ultimately reduces to whether gross replication r exceeds
depreciation δ. Terrestrial industry operates inside an ambient repair
economy; an off-Earth system must import, pre-position, or build its own.

Published measurements constrain a few component classes without bounding
the depreciation of an autonomous industrial ecology:

- **GEO solar arrays** degrade 0.4–1.7%/yr [S19], overlapping a
  terrestrial PV median of 0.5–0.6%/yr at the low end and reaching
  several times it at the high end [S18] — one component class, silent
  about bearings, seals, lubricated mechanisms, batteries, machine tools,
  robots, radiators, dust-exposed joints, and optical metrology.
- **Constellation figures** are cohort-dependent: reported
  early-generation failure fractions near 3% fall below 0.5% for later
  generations, the underlying tracker separates early deorbit,
  uncontrolled decay, retirement, and disposal, and a fleet fraction
  without a cohort definition, observation interval, and satellite-years
  is not a hazard rate [S22].
- **Large-training-run figures** near one interruption per two thousand
  accelerator-days mix permanent component failures with recoverable
  host, network, and software events, most automatically recovered: a
  **cluster interruption frequency**, not a component hazard rate.

The space penalty is not faster wear — it is the five-to-fifteen-year
no-repair design envelope, the internality of every repair chain, and
discrete loss without salvage. Meanwhile the most advanced terrestrial
capital — fab tools on 2–5-year schedules, accelerators retired within
3–6 years — is written off faster than a space solar array physically
degrades, because obsolescence sets the terrestrial clock.

Five quantities must be kept apart: **physical degradation**,
**functional failure**, **accounting depreciation**, **economic
obsolescence**, and **frontier-equivalent capacity loss**. The last two
are not physical — an accelerator does not vanish because a better one
exists — so obsolescence enters a growth equation only where H is
measured in quality-adjusted or frontier-equivalent capacity, which is
why the terrestrial paradox above is a statement about accounting and
frontier equivalence rather than about matter. The corrected form,
decomposed per environment,

::: {#eq:depreciation-decomposition .equation}
$$
\delta_{\mathrm{total}}
= \delta_{\mathrm{wear}}
+ \delta_{\mathrm{catastrophic}}
+ \delta_{\mathrm{obsolescence}}
+ \delta_{\mathrm{logistics}}
$$
:::

is what the sector model implements per sector and location: space
raises the catastrophic and logistics terms, Earth raises the obsolescence
term, and wear differs modestly. The environment drives gross transition rates
through radiation, thermal cycling, micrometeoroids and debris, vacuum
effects, regolith dust, and service availability. Equation
[@eq:depreciation-decomposition] is a diagnostic aggregation, however; repair
and recycling must not be represented merely by lowering $\delta$.

The compute-cohort sensitivity keeps age and generation explicit. Physical
failure removes hardware units; radiation degrades delivered performance;
economic obsolescence removes a cohort from frontier training without
destroying it; and the remaining hardware is reassigned down a workload
ladder—training, inference, verification, control, and non-frontier
simulation. At year 18, both branches retain 503.3 of 700 installed physical
units after 196.7 cumulative physical failures. Under continued specialized
progress, 80.8% of surviving stock is reassigned; under the
architectural-convergence branch, new-generation performance growth slows
after year 9 but persistent workload mismatch still leaves 63.6%, or 320.1
units, economically obsolete for frontier training and physically useful
elsewhere. Convergence can reduce turnover pressure; it does not set the
obsolescence term to zero.

Rice's peer-reviewed two-asset growth model independently motivates the
distinction: specialized AI hardware is modeled as adjusting much faster
than conventional capital because economic obsolescence drives replacement
[S78]. Its approximately seven-quarter calibrated AI-capacity half-life is a
terrestrial macroeconomic result, not an off-world depreciation input.
Machine-readable:
[compute cohort summary](../outputs/integrated/tables/compute_cohort_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_cohort_summary.csv"} and
[compute cohort trajectory](../outputs/integrated/tables/compute_cohort_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_cohort_trajectory.csv"}.

The lifecycle extension instead tracks the stock vector

::: {#eq:orbital-lifecycle-state .equation}
$$
\mathbf x_{t+\Delta t}
=\mathbf x_t
+\Delta t\!\left[\mathbf Q_t^\mathsf T\mathbf x_t
-\operatorname{diag}(\mathbf Q_t\mathbf 1)\mathbf x_t
+\mathbf b_t\right],
\quad
\mathbf x=
(O,D,A_s,R,C,S,F,W,U)^\mathsf T .
$$
:::

Here $t$ is elapsed years, $\Delta t$ is the simulation step in years,
$\mathbf x$ contains operating, degraded, awaiting-service, under-repair,
cannibalized, salvaged, recycled-feedstock, disposed-waste, and
uncontrolled-debris stocks in kilograms or frontier-equivalent capacity as
declared for each run; $Q_{ij,t}\ge0$ is the transition rate per year from
state $i$ to state $j$; $\mathbf Q_t\mathbf1$ is the vector of total outward
rates; $\operatorname{diag}$ places that vector on a diagonal; and
$\mathbf b_t$ contains new deployment and external removals. Separate
transition labels record physical degradation, propellant depletion,
replaceable-part failure, repairable damage, collision damage, functional
obsolescence, controlled retirement, and irrecoverable loss. Material
accounting applies Eq. [@eq:orbital-lifecycle-state] by material category, so
capture, disassembly, sorting, cleaning, reprocessing, fabrication,
qualification, waste, and accidental fragment creation conserve mass.

Restored capacity returns from $R$ to $O$ only after diagnosis, rendezvous,
capture, parts and tooling availability, service time, verification, and a
successful return-to-service draw. Direct reuse, component harvesting,
refurbishment, remanufacture, and bulk recycling remain distinct routes.
Downtime is lost output even when repair eventually succeeds, and physical
repair does not erase frontier-equivalent obsolescence. The transparent
irreversible-loss diagnostic over horizon $T$ is

::: {#eq:effective-irreversible-loss .equation}
$$
\delta_{\mathrm{irr}}^{(T)}
=
\frac{\displaystyle
\int_0^T\!
\left(\dot W_{\mathrm{unrecoverable}}
+\dot U_{\mathrm{unrecoverable}}\right)\,\mathrm dt}
{\displaystyle\int_0^T O(t)\,\mathrm dt},
$$
:::

where the numerator is irrecoverable waste plus uncontrolled-debris loss in
capacity-equivalent units and the denominator is operating-capacity-years.
Gross failure, repair return, salvage and recycling yield, downtime,
disposal, and obsolescence are still reported separately.

This extension is a bounded scenario model, not a claim that orbital
circularity is mature. NASA’s ISAM survey distinguishes inspection, planned
and unplanned repair, refueling, manufacturing, and recycling/reuse as
different capability areas and records demonstrated precedents as well as
developmental systems [S62]. The cancellation of NASA’s OSAM-1 after
technical, cost, schedule, integration, and market-transition problems is
counterevidence to treating unprepared-spacecraft service as routine [S63].
ESA likewise describes capture of an unprepared object as complex, costly,
and not always possible [S64]. The practical comparison must therefore
separate replace, refuel or life-extend, repair, upgrade, cannibalize,
repurpose, recycle, relocate, and dispose strategies by orbit, client design,
remaining life, service risk, downtime, avoided replacement launch, recovered
value, liability, and residual value. A service architecture plausible for a
prepared high-value GEO or cislunar platform need not close for a cheap,
unprepared LEO unit.

The strategy comparison exposes design-for-service rather than treating it as
a hidden lower depreciation rate. Its legacy, modular-serviceable, and
circular portfolios vary docking/refueling interfaces, replaceable modules,
accessible fasteners/ports/grapples, material passports and separability,
passivation, and machine-readable service manuals. Those choices change
capture, repair, and recycling factors while charging 0%, 8%, and 14%
declared mass penalties. In the 20-year assumption run, operating
capacity-equivalents end at 59.0, 63.6, and 62.4, while the effective
irreversible-loss diagnostic falls from 0.074 to 0.043 and 0.026 per
operating-capacity-year. These are comparative mechanics, not evidence that
the circular design is flight-ready; the complete inputs and repair,
recycling, debris, and mass outcomes are in
[orbital lifecycle strategy comparison](../outputs/integrated/tables/orbital_lifecycle_strategy_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_lifecycle_strategy_comparison.csv"}.

The transport comparison is directional and origin-specific. A historical
NASA propulsion review gives roughly 9 km/s as the effective Earth-surface to
parking-orbit requirement after gravity and drag [S67]. A separate lunar
ascent assessment gives 1.85 km/s from the lunar surface to LLO and describes
the one-way LLO and NRHO cases as approximately 1.9 and 2.7 km/s,
respectively [S68]. Thus **local lunar-surface ascent to lunar orbit** has a
much lower first-order delta-v than **Earth-surface launch to LEO**. This does
not mean that Earth-supplied lunar orbit is cheaper than LEO, or that
Moon-supplied service of an Earth-orbiting asset is automatically cheap: the
latter also pays lunar ascent or escape, transfer, Earth-orbit insertion and
plane distribution, plus any return or disposal leg.

The transport/service-network sensitivity therefore compares four explicit
routes: Earth-launched service in Earth orbit, Earth-supplied service in lunar
orbit, lunar-supplied service in lunar orbit, and lunar-supplied service of
Earth-orbiting clients. It applies the rocket equation using a declared
specific impulse, dry mass and payload before adding propellant source,
staging abstraction, vehicle reuse, fixed infrastructure, operations,
reliability, serviceability, client value, recovered mass, and orbit
distribution. Delta-v is never converted directly into dollars. Lunar-source
routes are unavailable until the scenario's extraction, propellant,
manufacturing, launch, navigation, and service maturity gate passes.
Machine-readable central cases and one-at-a-time break-even sweeps are in
[orbital transport service network](../outputs/integrated/tables/orbital_transport_service_network.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_transport_service_network.csv"}. The
companion [orbital transport break even surface table](../outputs/integrated/tables/orbital_transport_break_even_surface.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_transport_break_even_surface.csv"} crosses client value,
failure rate, serviceability, client count, recovered mass, reuse, and lunar
maturity for all four route/plane and propellant-source architectures. Every
economic and maturity coefficient in those tables is **ASSUMPTION**-class;
the NASA sources anchor only the named delta-v comparisons.

The disposition comparison applies one boundary to **replace, refuel or
life-extend, repair, upgrade, cannibalize, repurpose, recycle, relocate, and
dispose**. For action $a$, orbit $o$, asset class $c$, and fleet $f$, define

::: {#eq:orbital-service-decision-value .equation}
$$
\begin{aligned}
V^{\mathrm{net}}_{aocf}
={}&(1-p_a)\left(
V^{\mathrm{out}}_{aoc}
+L^{\mathrm{avoid}}_{ac}
+V^{\mathrm{asset}}_{ac}
+V^{\mathrm{recover}}_{ac}
+V^{\mathrm{upgrade}}_a
+V^{\mathrm{res}}_{ac}\right)\\
&-\left(
C^{\mathrm{variable}}_{ao}
+\frac{C^{\mathrm{fixed}}_f}{N_{of}T_f}
+C^{\mathrm{route}}_{of}
+C^{\mathrm{down}}_{ac}
+C^{\mathrm{risk}}_{aoc}
+C^{\mathrm{depr}}_{ac}
\right).
\end{aligned}
$$
:::

$V^{\mathrm{out}}$ is remaining lifetime output after downtime;
$L^{\mathrm{avoid}}$ is avoided replacement launch; the next four terms are
preserved non-output asset value, recovered component/material value,
incremental upgrade value, and residual value. $p_a$ is service-failure
probability. The cost terms are variable service cost, fleet development and
infrastructure amortized over $N_{of}$ annual clients and fleet life $T_f$,
routing and replenishment, downtime, service/debris-liability risk, and
depreciation. All values are real-2025 MUSD per client event. Break-even is
$V^{\mathrm{net}}_{aocf}\ge0$; the output table also reports the maximum
service price consistent with that inequality.

This economic test is deliberately not a mission-permission test. A row is
deployable only if (1) its docking, modularity, refueling, depot, recycling,
cooperative-target, and relocation requirements are technically satisfied;
(2) Eq. [@eq:orbital-service-decision-value] is nonnegative; and (3) every
applicable authorization record is validated. The decision surface resolves
400-km and 650-km LEO, GEO, cislunar staging, LLO, and NRHO separately,
including rendezvous, inclination/routing, station-keeping, residence,
atmospheric clearance, radiation, debris exposure, tracking, and disposal.
It crosses two client classes—a prepared high-value spacecraft and a cheap,
short-lived unprepared constellation unit—with a demonstrator, regional
servicer/depot fleet, and circular network. The last two amortize fixed cost
over more clients but pay explicit scheduling, replenishment, routing, and
congestion multipliers.

[orbital service decision comparison](../outputs/integrated/tables/orbital_service_decision_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_service_decision_comparison.csv"} records all 324 combinations;
[orbital regime assumptions](../outputs/integrated/tables/orbital_regime_assumptions.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_regime_assumptions.csv"} prevents Earth-orbit and lunar-orbit
parameters from being silently shared; and [orbital fleet amortization table](../outputs/integrated/tables/orbital_fleet_amortization.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_fleet_amortization.csv"}
exposes capacity and fixed cost per client. Technical feasibility and
economic viability are reported even when governance is not ready. In the
declared 400-km LEO/regional-fleet case, upgrade, refuel/life extension, and
repair of the prepared high-value asset have positive modeled net value,
whereas the unprepared short-life unit is technically eligible only for
replacement or disposal and neither is economically positive. Moving from
the single demonstrator to the circular network lowers the assumption-class
fixed cost per 400-km LEO client from $26.90M to $3.77M while increasing
annual modeled service capacity from 1.12 to 26.53 clients; congestion and
scheduling penalties remain charged. These figures are scenario
comparisons, not prices or forecasts.

The
machine-readable governance register separately covers ownership and
consent, operating authorization, liability allocation, export-control
review, spectrum/orbit authorization, custody and provenance, and
safety-critical recycled-material qualification. Treaty jurisdiction,
ownership, authorization, and liability provide the boundary [S69]; current
U.S. export rules expressly make some spacecraft servicing/control transfers
review-dependent [S70]; and current FCC rules tie operations and end of life
to authorized debris plans [S71]. Applicability remains jurisdiction- and
mission-specific, so every non-validated item blocks a deployable claim
rather than being converted into a probability or cost.

**Collision-cascade control boundary.** Kessler risk is not an unusually large
independent shock. It is positive feedback: collisions create orbiting
fragments, those fragments raise the later collision rate, and a sufficiently
dense region can keep generating debris after new deployment stops [S45].
The implemented LEO `debris_event` instead has a fixed 0.05 yr⁻¹ Poisson
rate and removes a sampled 0.02–0.10 fraction from selected sectors; the
loss creates no debris and the event rate does not depend on deployed
capacity. The continuous catastrophic term is likewise an exogenous hazard
range. These terms can represent ordinary impact exposure but cannot test
the cascade threshold, avoidance saturation, shell-to-shell fragment
transport, or recovery through decay and active removal. Accordingly, every
LEO scale result in I.8 is conditional on a debris regime in which
fragment creation does not outrun clearance. The missing state is not
assigned a silent proxy value. The integrated layer supplies both an aggregate
stress test and a second, finite-mass diagnostic resolving 400-km LEO,
650-km LEO, and cislunar regions; active assets, intact derelicts,
trackable and untrackable fragments; collision-generated yield; avoidance
saturation; cross-shell transport; disposal, natural clearance, retrieval,
and active removal. It reports expected hazardous descendants per object as
a branching-style stress metric (I.8, D.1). The kernels and transitions
remain assumptions rather than a conjunction-assessment or validated traffic
model. Lunar orbit does not remove the issue: breakup
simulations find strongly orbit-dependent evolution, including long-lasting
debris in some low lunar orbits and nonuniform lunar impact patterns [S46].

A deployable strategy begins with physical failure domains rather than a
preferred logical cluster size. Let $\mathcal H_t$ be the set of credible
single-event exposure sets over a declared time window: collision pairs,
breakup clouds, avoidance-coordination failures, and losses of shared power,
gateway, navigation, software, or command services. The common-cause budget is

::: {#eq:orbital-common-cause-budget .equation}
$$
L_{\max}(t)
=\max_{h\in\mathcal H_t}
\sum_i K_i(t)\,\mathbf 1[i\in h]
\le \epsilon\,K_{\mathrm{total}}(t).
$$
:::

$K_i(t)$ is node $i$'s declared service capacity, $K_{\mathrm{total}}$ is
total service capacity, and $\epsilon\in(0,1)$ is the maximum
**ASSUMPTION-class** fraction one credible event may disable. Each hazard set
records altitude, inclination, plane, along-track extent, fragment
correlation, shared services, and restoration window. Equation
[@eq:orbital-common-cause-budget] makes allowable cluster size and reserve
capacity outputs of geometry and risk tolerance. Capacity is distributed
across independent domains so a damaged domain can be isolated, workloads
rerouted, command and verification preserved, and reconstruction begun.
Concentration gains—short links, shared power and thermal systems, easier
service, and lower coordination load—are evaluated against collision
cross-section, correlated loss, avoidance saturation, fragment yield, and
rebuild burden.

The controller uses a mitigation hierarchy: prevent releases and explosions
through reliability, passivation, containment and prompt disposal; avoid
tracked objects through coordinated, uncertainty-aware screening and maneuver
reserves; survive only the specified small-untracked-particle regime through
shielding, placement, redundancy and leak isolation; compartmentalize
consequences; then remove or recycle intact, massive, collision-likely
derelicts. Shielding mass and increased cross-section are charged, and no
practical shield is credited against a satellite-scale impact. Safe deorbit or
relocation counts as hazard removal, not material recycling.

Shell-resolved triggers monitor active and derelict mass, conjunction
forecast and uncertainty, maneuver workload and remaining propellant,
disposal failures, fragment creation-to-clearance ratio, expected hazardous
descendants, tracking quality, and service backlog. Crossing a threshold can
slow or stop deployment, tighten the Eq.
[@eq:orbital-common-cause-budget] cap, change planes or shells, increase
spacing or fuel reserve, dispatch removal, isolate a cluster, or retire a
shell. NASA’s mitigation guidance distinguishes creation prevention,
small-debris protection, lower-risk orbital regimes, and collision avoidance;
its conjunction handbook treats screening, risk assessment, maneuverability,
tracking, reliability, disposal, and operator coordination as lifecycle
functions [S65]. ESA’s 2025 environment report finds that mitigation
compliance remains insufficient and that fragmentation can exceed natural
clearance even without new launches, motivating active removal [S66]. These
sources bound the control architecture; they do not calibrate a future
million-node constellation or transfer Earth-orbit policy to LLO or NRHO.

The architecture search makes the failure domains concrete. Five declared
120-node layouts vary altitude dispersion, inclination, planes, along-track
spacing, cluster cap, shells, gateways, control domains, shared power,
navigation and software, and cross-link burden. The concentrated and
plane-modular layouts violate the 10% common-cause budget at 100% and 25%;
the multi-shell and sparse independent-domain layouts pass at 10% and 6.7%.
A physically distributed layout with one gateway and two control domains
still fails at 100%, demonstrating that orbital separation cannot compensate
for a shared logical choke point. [orbital cluster layout optimization table](../outputs/integrated/tables/orbital_cluster_layout_optimization.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_cluster_layout_optimization.csv"}
reports the collision/concentration/communications tradeoff and labels the
non-dominated layouts rather than declaring one optimum.

The breakup diagnostic propagates a cloud through twelve individually
specified nodes with altitude, inclination, plane, along-track phase,
capacity, gateway, and control-domain identities. It reports direct loss,
expected secondary collisions, avoidance maneuvers, service interruption,
repair load, and restoration time. In the declared one-year stress cases,
the 650-km Earth-orbit breakup generates 0.103 expected secondary collisions,
0.495 avoidance maneuvers, 72.7 capacity-days of interruption, and a
76-day 95% restoration time. The LLO case has weaker tracking, negligible
natural clearance, and slower repair: 0.122 expected secondary collisions,
0.119 maneuvers, 117.4 capacity-days, and 149 days to restore. These are
deterministic expected-count implications of an illustrative geometry and
kernel, not integer event forecasts or catalog-calibrated collision
probabilities. The full time series and summary are in
[orbital breakup cloud trajectory](../outputs/integrated/tables/orbital_breakup_cloud_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_breakup_cloud_trajectory.csv"} and
[orbital breakup cloud summary](../outputs/integrated/tables/orbital_breakup_cloud_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_breakup_cloud_summary.csv"}.

The high-conjunction stress separately removes tracking, communications,
navigation, and centralized coordination. All five degraded cases breach the
declared risk limit before intervention. The controller responds by pausing
deployment, increasing spacing, switching to independent tracking and local
safe mode, isolating control domains, and applying deterministic
right-of-way rules as applicable; all cases fall below the limit only because
the declared fallback multipliers are strong enough. That conditional result
is visible in [orbital degraded control stress](../outputs/integrated/tables/orbital_degraded_control_stress.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_degraded_control_stress.csv"} and is a test target, not
evidence of operational safety.

The mitigation comparison crosses low/high deployment cadence, disposal
reliability, removal, shielding mass, cluster cap, shell diversity, servicer
fleet size, and repair/recycling capacity. Of 256 portfolios, 39 are
non-dominated across residual risk, lifecycle cost, and delivered capacity.
[orbital mitigation portfolio pareto](../outputs/integrated/tables/orbital_mitigation_portfolio_pareto.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_mitigation_portfolio_pareto.csv"} retains the full surface so a low
risk point cannot be called universally optimal by hiding its mass, cost, or
throughput penalty. [orbital environment strategy comparison](../outputs/integrated/tables/orbital_environment_strategy_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_environment_strategy_comparison.csv"} keeps
Earth-orbit atmospheric clearance, tracking, station-keeping, residence, and
controlled reentry distinct from LLO's negligible atmospheric clearance,
weaker tracking, higher station-keeping, and lunar-impact/transfer disposal.

Finally, shell admissibility is a shared governance constraint. The
illustrative coordinated 5,200-node plan remains below the declared 10,954
node 650-km and 8,660 node LLO carrying-capacity limits and passes the 90%
operator-compliance gate. The 15,000-node case exceeds both limits and also
fails data-sharing, maneuver-coordination, disposal, and authorization
requirements. [orbital multi operator capacity table](../outputs/integrated/tables/orbital_multi_operator_capacity.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_multi_operator_capacity.csv"} makes clear that one
operator's internal policy cannot authorize or coordinate the shared shell.
All caps and workload coefficients remain **ASSUMPTION**-class pending
catalog and operator telemetry.

One environment-specific case partly cuts the other way. For **short-lived
compute payloads in very low orbit**, aligning useful life with
accelerator-obsolescence cycles reduces the economic value of repair:
hardware retired within a few years regardless costs less to be unable to
fix. The qualifications are substantial. Natural decay depends on altitude,
ballistic coefficient, and solar activity—small spacecraft near 400 km can
decay within five years, but beyond 500 km five-year decay is not assured and
some objects persist for decades. The leading published orbital-compute
architecture places its cluster near **650 km** in dawn-dusk sun-synchronous
orbit, chosen for illumination rather than disposal [S32], so the concession
does not describe that design. Nor is disposal free: station-keeping,
collision avoidance (SpaceX reports more than 1,000 automated Starlink
avoidance manoeuvres per day in 2025, Form S-1 pp. 9 and 153 [S27]),
replacement launch, network spares, and residual capital loss all remain—and
the same source that calls orbital repair impracticable proposes redundant
provisioning instead, which is a cost, not its absence [S32]. The concession
therefore covers some payload classes in very low orbit and does not
generalize: mines, refineries, machine tools, and robots must last decades to
close a loop. In these models it belongs in Part II (compute payloads), while
Part I's industrial $\delta$ decomposition governs long-lived industrial
equipment.

**The clock-setting component.** In any partially closed system, the
component with the shortest replacement horizon that cannot yet be produced
or stockpiled locally sets a hard clock on the entire complex. Closure
priority follows failure rate × non-replaceability, not mass fraction.
Viability requires:

::: {#eq:critical-component-replenishment .equation}
$$
T_{\mathrm{replenish},j} < T_{\mathrm{effective\ survival},j}
\qquad \text{for every critical component class } j
$$
:::

Effective survival includes installed redundancy, spare inventory, repair probability, and substitution — not time to first failure; the naive form ignored inventories, cannibalisation, and stockpiling, all of which the model carries explicitly. Part I.7 enforces the condition by construction, and Part I.8 identifies the clock-setting sector by computation.

## I.5 Industrial closure: the decisive threshold {#i.5-industrial-closure-the-decisive-threshold}

Self-sustaining (P ≥ D: replacing what is consumed and lost) and
self-expanding (P > D: net additional capacity) are different milestones.

::: {#eq:net-capacity-growth .equation}
$$
g_H = \frac{P-D}{H}
$$
:::

P is productive capacity manufactured during the period, D is capacity lost
or consumed, and g_H is the net growth rate of productive infrastructure H.
Industrial closure measures how much of the critical input set is produced
inside the network:

::: {#eq:closure-ratio .equation}
$$
\kappa
= \frac{\text{critical inputs produced internally}}
       {\text{total critical inputs required}}
$$
:::

At low closure, nearly all equipment arrives from Earth. At intermediate
closure, local industry supplies propellant, shielding, structural material,
tanks, roads, landing pads, and simple machines. At high closure, the network
also supplies motors, sensors, precision tools, computers, robots, spacecraft,
factory machinery, high-purity chemicals, and semiconductor equipment. The
progression is descriptive, not a scalar score: the identity and
replaceability of the residual imports determine whether the system is
actually autonomous.

The scalar form is vocabulary, not a measure of autonomy. A system supplying
99.9% of its mass locally is not autonomous if the residual 0.1% contains
irreplaceable electronics. Yet that 99.9% can still reduce entry capital and
Earth transport by orders of magnitude, support much larger deployed capacity
per unit of external supply, and buy time in which the remaining process may
be localized. Strict autonomy and import leverage must therefore be reported
separately:

::: {#eq:closure-and-import-leverage .equation}
$$
\begin{aligned}
A_{\mathrm{aut}}
&=\prod_{j\in\mathcal J_{\mathrm{crit}}}
\mathbf 1[\dot m^{\mathrm{external}}_j=0],\\
\sigma_{\mathrm{ext}}
&=\frac{\sum_j \dot m^{\mathrm{external}}_j}
{\dot H_{\mathrm{verified}}},\qquad
\Lambda_{\mathrm{import}}
=\frac{\dot H_{\mathrm{verified}}}
{\sum_j \dot m^{\mathrm{external}}_j}
=\sigma_{\mathrm{ext}}^{-1}.
\end{aligned}
$$
:::

Here $\mathcal J_{\mathrm{crit}}$ is the set of inputs whose absence stops
verified production; $\dot m^{\mathrm{external}}_j$ is external supply of
input $j$ in kilograms per year; $A_{\mathrm{aut}}\in\{0,1\}$ is strict
mass-flow autonomy; $\dot H_{\mathrm{verified}}$ is commissioned
frontier-equivalent capacity added per year; $\sigma_{\mathrm{ext}}$ is
external-support intensity in kilograms per capacity unit; and
$\Lambda_{\mathrm{import}}$ is capacity added per imported kilogram.
$\Lambda_{\mathrm{import}}$ is undefined at zero imports, where
$A_{\mathrm{aut}}=1$ is reported instead. Mass closure, purchase-value
closure, process-route closure, critical-part closure, and human-intervention
closure remain separate profiles because a high score in one cannot establish
another.

The deterministic support-policy stress test puts those metrics together
instead of publishing mass closure alone. Its illustrative bridge has 99.86%
commissioning-mass closure, 99.2% part-family closure, but only 72.8%
purchase-value closure; both named residuals remain critical, so strict
autonomy is zero in every row. The conditional entry architecture delivers a
2.5 t external seed rather than the 10 t wholly Earth-manufactured comparison;
that 75% reduction is an **ASSUMPTION**, not a launch-cost estimate, and
presupposes that the local bulk-material path already exists.

| residual-support policy | autonomy | maximum scale | first constraint/stockout | net capacity per external t | binding residual | cumulative capacity lost |
|---|---:|---:|---:|---:|---|---:|
| fixed annual imports | no | 18.66 | year 18 | 5.51 | calibration/metrology | 21.85 |
| imports proportional to capacity | no | 60.64 | year 25 | 8.37 | advanced electronics | 58.33 |
| finite initial stockpile | no | 2.60 | year 6 | 0.00 | advanced electronics | 2.60 |
| declining imports, years 12–17 outage | no | 10.67 | year 16 | 0.00 | advanced electronics | 10.67 |

: Scale and fragility under alternative residual-import policies. [View data](../outputs/integrated/tables/partial_closure_dashboard.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_dashboard.csv"}. {#tbl-residual-support-policies}

The large cumulative-loss entries are repeated waves of unsupported capacity,
including capacity rebuilt and lost again; they are not fractions of one
initial asset. The simulation serves replacement before expansion, applies
input-specific shelf life, obsolescence, radiation-storage loss,
failed-delivery derating, minimum lots, supplier caps, and synchronized
replacement waves. It reports annual delivery mass, volume and value,
inventory, replacement and commissioning demand, binding residual, and
capacity loss in
[partial closure support policies](../outputs/integrated/tables/partial_closure_support_policies.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_support_policies.csv"}; the
companion [partial closure dashboard](../outputs/integrated/tables/partial_closure_dashboard.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_dashboard.csv"} keeps autonomy, mass, part-family,
value, embodied-energy, process-work, entry mass, supplier utilization,
runway, intervention, verification, and import leverage in one view. These
coefficients are stress assumptions, not calibrated supplier or failure
forecasts.

The disrupted case also charges 15% of otherwise available expansion effort
to two discrete technical programs once their intelligence, embodiment,
materials, tooling, and test-facility gates pass. The declared
advanced-electronics program reaches its effort and development thresholds
and validates a mature-controller route that reduces, but does not eliminate,
its residual requirement; the calibration/metrology program reaches its
threshold and fails. The 0.583 capacity-years spent on both programs are
therefore unavailable for immediate expansion. Parent-tool ancestry,
evidence state, charged work, minimum development time, and the
probability-free success/failure outcome are explicit in the parameter file.
[partial closure substitution programs table](../outputs/integrated/tables/partial_closure_substitution_programs.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_substitution_programs.csv"}
allocates the consumed capacity-years across research compute, experiments,
destructive tests, metrology, process equipment, prototype lines,
qualification, failed designs, materials, and energy; the shares are
assumption accounting, while the total is the expansion opportunity cost
actually removed by the simulation.
This scenario illustrates a possible path from scale to substitution without
claiming that intelligence guarantees closure.

The external supplier is inside the hybrid system boundary rather than an
unbounded input tap. Its factory throughput, high-purity materials, skilled
labor-hours, energy, finance, and launch/transport capacity each grow at a
declared rate; the minimum resource-equivalent flow, derated by supplier
reliability, caps total deliveries before input-specific failed-delivery
losses. [partial closure supplier boundary table](../outputs/integrated/tables/partial_closure_supplier_boundary.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_supplier_boundary.csv"} reports every resource
capacity, the binding supplier resource, delivered tonnes, and utilization in
each year. This is still a stylized supplier envelope, but it prevents local
growth from demanding residual imports faster than the modeled Earth loop can
produce, finance, and transport them.

Finally, [partial closure allocation policies](../outputs/integrated/tables/partial_closure_allocation_policies.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_allocation_policies.csv"} holds the
capacity-proportional external-supply rule fixed and compares immediate
expansion, a three-year replacement reserve, a balanced reserve/substitution
policy, and substitution-first allocation. Substitution effort is removed
from current expansion, while the stockpile policies withhold inventory from
commissioning. That artifact reports maximum and terminal scale, stockout,
external support, ending inventory, capacity loss, program effort, and
validated or failed dependencies. It therefore shows when scale supplies
useful substitution effort and when it merely enlarges exposure; no smooth
automatic decline in import share is assumed.

The sector state is consequently an externally supported growth regime until
the critical import vector vanishes:

::: {#eq:externally-supported-capacity .equation}
$$
\mathbf K_{t+\Delta t}
=\mathbf K_t
+\Delta t\!\left[
\mathbf y^{\mathrm{local}}(\mathbf K_t,\mathbf x_t)
+\mathbf B\,\mathbf u_t
-\boldsymbol\delta_t\odot\mathbf K_t
\right].
$$
:::

$\mathbf K_t$ is the vector of commissioned sector capacities at elapsed year
$t$; $\mathbf y^{\mathrm{local}}$ is locally produced capacity per year after
internal material and service constraints; $\mathbf u_t$ is the external
input-flow vector; $\mathbf B$ converts imported inputs to commissioned
capacity; $\boldsymbol\delta_t$ is the sector loss-rate vector per year; and
$\odot$ denotes elementwise multiplication. This is hybrid expansion, not
closure. It can nevertheless scale if a small external flow unlocks a much
larger local material and energy base. Its ceiling, capital requirement, and
resilience depend on supplier capacity, transport cadence, shelf life,
stockpiles, substitution, and the minimum import cut sets—the smallest
combinations whose loss collapses the network.

The path to autonomy is a sequence of verified substitutions, not an assumed
trend: for each critical imported item the program must select a local process
route, build its parent tools, qualify material and output, demonstrate yield
and reliability, survive a supply interruption, and remove the import edge
from the dependency graph. Intelligence can improve search and process
development while the high-leverage external loop provides “fuel” for further
expansion, but sufficient intelligence does not guarantee that geology,
purity, equipment, energy, or safety requirements can be met within a horizon.
The clock-setting component is the scalar shadow of this vector structure.
The hardest closure problem is the deep technological stack—precision
metrology, advanced electronics, semiconductor fabrication, optics,
high-purity processing, specialized alloys, software verification, and the
machines that make those machines (Part III.2 examines the first announced
attempt on its terrestrial face).

**Lineage.** The 1980 NASA/ASEE summer study [S23] designed a proof-of-principle self-replicating lunar factory growing from a ~100-ton seed and introduced quantitative closure analysis; Freitas and Merkle catalogued the design
space [S24]. The present thesis is that lineage plus three ingredients the
1980 study lacked: general-purpose AI for coordination and redesign; a
reusable heavy-lift transport economy; mass-manufactured robotics.

**The r and κ anchors, read honestly.** Three quantities sometimes
presented as converging near one year are not commensurable: solar energy
payback (0.9–4.1 yr [S20]) measures energy self-financing only; the NASA ~1-year figure is a **strawman replication target** adopted for a proof-of-principle design, with component values its authors described as crude estimates; Gigafactory Shanghai's ten months is project execution inside a mature host economy. The
replication time of a full industrial ecosystem is *unknown* — and here it
appears only as a computed output distribution (Part I.8). For κ, the honest headline is a theory-versus-demonstration gap, stated as its authors did: the 90–96% figure is closure reported in earlier studies of *specific nonreplicating* space-production applications, cited in support of plausibility arguments, and the 1980 study explicitly placed a rigorous demonstration that its factory could produce every required part beyond its own scope [S23]. Against that sit gram-per-hour oxygen and ~20% single-output yields actually demonstrated [S21]; full-system closure has not been demonstrated at any scale. Stating the gap converts the indicators
of Part III.5 from rhetoric into measurable distance.

**The seed-factory transition.** Earth stops transporting finished
infrastructure and transports a compact industrial seed, but "seed" denotes
four inseparable layers:

1. **Physical seed:** power, extraction, refining, manufacturing, robots,
   compute, repair capability, laboratories, and initial spares.
2. **Digital seed:** AI weights, firmware, controllers, compilers, CAD/CAM,
   simulators, optimization and verification tools, and locally available
   software dependencies.
3. **Industrial memory:** process recipes, material and equipment models,
   calibration and maintenance procedures, complete build records, failure
   histories, intervention traces, and provenance.
4. **Experimental capacity:** instrumentation, metrology, test stands,
   flexible machine tools, and the ability to run controlled experiments
   that produce missing knowledge.

The package is viable only if it grows its productive base before critical
imported components fail. A credible design requires redundancy, recycling,
buffers, and an explicit path for every nonlocal dependency. No finite seed
can encode "all necessary industrial knowledge"; the operational criterion
is a sufficient foundation plus the capacity to diagnose gaps, run
experiments, validate new processes, and incorporate the results into
industrial memory. The ten-sector model represents only part of
the physical layer: spares are a shelf-life-limited stockpile state;
nonlocal dependencies are import lines that can be cut; and the "explicit
path" is an abstract sector requirement matrix. The integrated layer sizes
the seed and adds stylized representations of the remaining layers — a
fixed 5 t digital-seed mass, task-coverage autonomy, intervention
budgets, and commissioning dynamics (I.7, D.1). Those are declared
proxies, not resolved requirements: collapsing storage, compute,
calibration standards, laboratory machinery, consumables, and test
articles into one constant means the model cannot yet determine which
component of knowledge closure binds.

## I.6 Intelligence, coordination, and time {#i.6-intelligence-coordination-and-time}

A sufficiently capable AI converts much of organizational coordination from
human management into a computational service: scheduling machines,
allocating energy, routing materials, diagnosing failures, redesigning
components, balancing inventories, planning construction, and proposing and
coordinating candidate bottleneck-expansion projects. Observation,
verification, materials, productive capacity, and authorization determine
whether any proposal becomes operating hardware. A testable
**ASSUMPTION-class** sensitivity form is

::: {#eq:coordination-workload .equation}
$$
B_{\mathrm{coord}}
=B_{\mathrm{irred}}
+\frac{
B_0(E_G/E_0)^\alpha(\chi/\chi_0)^\beta(u/u_0)^\gamma
}{
1+\eta(I_{\mathrm{eff}}/I_0)^\delta
}.
$$
:::

$B_{\mathrm{coord}}$ is coordination work in agent-hours per unit of verified
production; $B_{\mathrm{irred}}$ is the irreducible floor in the same unit;
$B_0>0$ is a reference workload; $E_G$ is the weighted number of active
dependency and communication edges in the task graph; $\chi$ is operational
complexity measured from normalized dependency depth, coupling, and
replanning frequency; $u$ is uncertainty measured from calibrated forecast
error, unresolved-state entropy, and epistemic/aleatoric components;
$I_{\mathrm{eff}}$ is measured coordination-relevant planning,
communication-compression, conflict-resolution, calibration, monitoring, and
recovery capability; and $(E_0,\chi_0,u_0,I_0)$ are positive reference values
that make every power dimensionless. The coefficients
$\alpha,\beta,\gamma,\delta,\eta>0$ require calibration and uncertainty
propagation; they are not presented as a law.

Raw agent count is not a coordination structure. $E_G$ is derived from the
active machine, software-agent, human-supervisor, supplier, regulator, and
verification graph. Centralized, hierarchical, modular, sparse, and
all-to-all organizations can therefore have the same number of agents and
different burdens. Bandwidth, latency, context, embodiment, and verification
limits constrain $I_{\mathrm{eff}}$ rather than disappearing into a generic
model score.

Nor does greater task or coordination capability establish
controllability. The authorized-capacity state in Equation
[@eq:authorized-capacity-control] keeps task, coordination, evaluator, and
controllability coordinates separate. It permits the first two to rise while
independent evaluation or stop bandwidth binds, so a more productive system
can simultaneously create a larger unauthorized-capacity gap.

A bottleneck is not relaxed when a design is merely proposed. For candidate
upgrade $p$, the accounting gate is

::: {#eq:bottleneck-upgrade-gate .equation}
$$
\Delta B_p(t)
=\Delta\bar B_p\,
\mathbf 1[t\ge \tau_{p,\mathrm{design}}+
                 \tau_{p,\mathrm{build}}+
                 \tau_{p,\mathrm{verify}}]\,
\mathbf 1[C_p\le \bar C_p]\,
\mathbf 1[P_p=1]\,
\mathbf 1[V_p=1].
$$
:::

$\Delta B_p(t)$ is commissioned bottleneck-capacity increment at time $t$;
$\Delta\bar B_p$ is the proposed increment; the three $\tau$ terms are
design, construction, and verification lags; $C_p$ and $\bar C_p$ are
project cost and available productive-capacity budget in capacity-years;
$P_p$ records that the required producing sector exists; and $V_p$ records a
verified causal path from design through construction to held-out acceptance.
For physical floors, observations that have not yet occurred, and
externally controlled legal decisions, the model sets
$\Delta\bar B_p=0$: intelligence may reduce surrounding demand or improve a
proposal, but it cannot repeal the constraint.

As intelligence and local autonomy improve, human management per unit of
infrastructure can decline. The likely architecture is hierarchical rather
than perfectly centralized: local controllers manage fast operations;
facility-level agents coordinate production; higher-level planners allocate
resources across the network.

An early terrestrial version is documented inside the same corporate
ecosystem, though more weakly than some commentary claims. The confirmed
systems provide real-time monitoring, production scheduling, quality
management, and linked operational data at factory scale [S14–S17]. That is
evidence that coordination functions traditionally mediated by human
management are already becoming industrial data infrastructure. Claims that
the systems replace management wholesale remain commentary-class and are not
used here.

Coordination cannot reach zero. Machines must sense their environment;
signals require propagation time; fabrication and motion take time;
uncertain results require verification; and two projects cannot consume the
same indivisible machine or stored resource simultaneously:

::: {#eq:coordination-burden .equation}
$$
B_{\mathrm{irred}}
= B_{\mathrm{sensing}}
+ B_{\mathrm{latency}}
+ B_{\mathrm{synchronization}}
+ B_{\mathrm{safety}}
+ B_{\mathrm{verification}}
+ B_{\mathrm{contention}}.
$$
:::

Each term is converted to the declared agent-hour-equivalent account by an
explicit scenario conversion; unlike burdens are otherwise reported
separately. For a truly independent one-agent task some synchronization and
contention terms may be zero, but sensing, actuation, safety, and verification
do not vanish merely because intelligence increases. The strongest claim is
therefore that Eq. [@eq:coordination-workload] approaches a physical and
governance floor, not zero.

Required tests vary one-agent and zero-coupling cases, modular versus
all-to-all graphs, low and high uncertainty, degraded communications, and
sufficiently high intelligence. The assumed comparative statics are
$\partial B_{\mathrm{coord}}/\partial E_G>0$,
$\partial B_{\mathrm{coord}}/\partial\chi>0$,
$\partial B_{\mathrm{coord}}/\partial u>0$, and
$\partial B_{\mathrm{coord}}/\partial I_{\mathrm{eff}}<0$ above the floor.
Telemetry must also distinguish total work from elapsed time: adding capable
agents may shorten completion while increasing aggregate coordination hours.

### Cognitive copies and effective physical labor {#cognitive-copies-and-effective-physical-labor}

Model instances, inference capacity, robots and machines, experimental
stations, and independently verifiable work cells are separate stocks. Their
conversion to physical work and experiment time is bounded by

::: {#eq:cognitive-physical-labor .equation}
$$
\begin{aligned}
N_{\mathrm{phys}}^{\mathrm{eff}}
&=\min\!\left\{
N_{\mathrm{model}},N_{\mathrm{inf}},N_{\mathrm{robot}},
N_{\mathrm{sensor}},N_{\mathrm{safe}},N_{\mathrm{task}},
N_{\mathrm{tool}},N_{\mathrm{vcell}}
\right\},\\
T_{\mathrm{experiment}}
&\ge
d_{\mathrm{serial}}\tau_{\mathrm{phys}}
+\left\lceil
\frac{N_{\mathrm{indep}}}{P_{\mathrm{experiment}}}
\right\rceil\tau_{\mathrm{phys}} .
\end{aligned}
$$
:::

$N_{\mathrm{phys}}^{\mathrm{eff}}$ is effective physical-agent capacity.
$N_{\mathrm{model}}$ counts model copies; $N_{\mathrm{inf}}$ is the number
supportable by inference compute; and the remaining $N$ terms count physical
robots/machines, sensor channels, safe simultaneous work envelopes,
independent tasks, tool/material slots, and independently verifiable work
cells. $T_{\mathrm{experiment}}$ is wall-clock experiment-program time;
$d_{\mathrm{serial}}$ is the dependent physical depth;
$\tau_{\mathrm{phys}}$ is one physical experiment cycle;
$N_{\mathrm{indep}}$ is the independent experiment count; and
$P_{\mathrm{experiment}}$ is simultaneous station capacity. Copies can help
simulation, planning, or monitoring, but cannot reduce the first term or
exceed the physical channels in the second.

The limiting-case sweep makes the distinction visible. With one million
declared model copies, compute can keep only 200,000 active; 40 machines, 25
experimental stations, and 20 independently verifiable work cells limit
effective physical agents and annual physical output to 20. Another 6,500
instances can occupy declared simulation, planning, and monitoring tasks,
while 993,480 copies wait or contend. A 12-step serial experiment chain at
0.1 year per physical result retains a 1.2-year floor; 1,000 independent
experiments add four years on 25 parallel stations. Per-instance onboarding
falls as copies share context, but aggregate onboarding, coordination edges,
duplicate work, and verification demand rise. All counts are
ASSUMPTION-class stress values. Machine-readable:
[cognitive physical labor table](../outputs/integrated/tables/cognitive_physical_labor.csv){.artifact-link data-artifact="outputs/integrated/tables/cognitive_physical_labor.csv"}.
The uncertainty comparison evaluates power, logarithmic-edge, and
saturating-edge responses on the same reference case. It draws the
irreducible floor, reference work, four elasticities, intelligence response,
and saturation scale from declared bounds, using common draws across forms.
No timestamped task-graph, handoff, delay, defect, supervisor, or verification
telemetry is available, so this is a bound comparison with
`telemetry_status=unavailable`, not a calibration.
[coordination form uncertainty](../outputs/integrated/tables/coordination_form_uncertainty.csv){.artifact-link data-artifact="outputs/integrated/tables/coordination_form_uncertainty.csv"} retains all 768 draws and
[coordination form summary](../outputs/integrated/tables/coordination_form_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/coordination_form_summary.csv"} reports p10/p50/p90 consequences.
Median burden is 142.0 agent-hours for the power form, 141.5 for the
logarithmic-edge form, and 149.3 for the saturating-edge form; the
corresponding p10–p90 ranges overlap broadly. Structural-form uncertainty is
therefore comparable to coefficient uncertainty in this one reference case,
which is why no form is promoted.

The resulting burden enters one primary coordination-hours account.
Schedule delay equals hours divided by declared staffing throughput;
foregone verified output and failure probability are reported physical
consequences. Lifecycle cost prices coordination labor only and does not also
monetize the reported capacity loss. This one-way mapping connects schedule,
capacity, reliability, and cost without charging the same burden under each
label. Rehearsal telemetry must replace the assumption bounds before the
relation is promoted.

After high closure the central allocation question changes from "can the
system obtain land, permits, workers, components?" to "how much productive
throughput should be assigned, and when will output be complete?"

::: {#eq:cumulative-created-hardware .equation}
$$
H_{\mathrm{created}}(t)
= \int_0^t \operatorname{throughput}(\tau)\,\mathrm d\tau
$$
:::

Scarcity becomes latency: outputs remain scarce because machines, energy,
compute, transport capacity, and time have alternative uses, but the
accounting unit shifts toward joules, kilograms processed, machine-hours,
compute-hours, delta-v, and completion time. In the mature regime, growth is
bottleneck-limited:

::: {#eq:coupled-hardware-growth .equation}
$$
\frac{\mathrm d H}{\mathrm d t}
= \bigl(r(I,E,M)-\delta\bigr)H
$$
:::

When r exceeds δ, the idealized solution is exponential growth; real
systems instead move through phases in which extraction, refining, power,
thermal control, transport, precision manufacturing, compute, or maintenance
is slowest. Intelligence accelerates growth by detecting and expanding that
active bottleneck. The model below is an **idealized, perfectly informed
coordination benchmark**, not a demonstration that an AI can observe,
verify, and execute the allocation across a distributed factory. Within
that benchmark, the co-binding set reported each step identifies the
modeled active bottleneck.
