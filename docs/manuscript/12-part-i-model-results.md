## I.7 The multisector model {#i.7-the-multisector-model}

The model that produces a real number needs, per critical sector, a capacity, a sector-specific depreciation, a requirement matrix, and import terms — with self-expansion defined as feasible positive net growth in *every* indispensable sector. The framework specifies it and the repository builds and runs it [S28]. Its elements:

- **Ten sectors**: power, mining, refining, robotics, machine tools,
  electronics, thermal, transport, and — as first-class *service* sectors —
  repair and recycling. Repair offsets the wear component of δ only, at an
  efficiency cost and a spares bill drawn from the requirement matrix;
  recycling converts retiring capacity into secondary mining/refining feed,
  capped by the scrap flow.
- **Requirement matrix** A[i,j]: units of sector-i output consumed to build
  one unit of sector-j capacity. ASSUMPTION-class, existing only inside
  named assumption sets (conservative / central / optimistic).
- **Decomposed δ per environment** (I.4's four components, per sector),
  assembled from anchored ranges where anchors exist and declared
  ASSUMPTION entries elsewhere. Retirement does not become fully recyclable
  scrap: environment- and loss-specific recovery factors distinguish wear,
  catastrophic loss, obsolescence, and logistics loss, and repaired wear is
  subtracted from retirement. Each resolved value carries a provenance
  record into the generated reports.
- **The allocation step**: a three-stage lexicographic optimization. Stage
  1 maximizes worst-case sector growth g over builds, wear repair,
  recycling, and stockpile drawdown. Stage 2 holds g at its optimum and
  minimizes normalized stock draw. Stage 3 holds both objectives and solves
  a strictly convex, normalized quadratic program over actions. This final
  tie-breaker makes the state transition unique instead of accepting an
  arbitrary LP vertex.
- **Strategic imported-part stockpiles** with shelf life (electronics-class parts
  decay in storage), per-sector import cutoffs, Mars synodic pulse
  deliveries, and Poisson common-cause shocks hitting correlated sector
  groups (dust storms, solar storms, common design faults).
- **Three reference architectures**: LEO (no ore body — feed imported or
  recycled from on-orbit mass), lunar surface (regolith feed, abrasive
  dust, no magnetosphere), Mars (deepest logistics penalty, ~26-month
  synodic resupply pulses, dust storms).

**The electronics strategic-material gap.** One structural parameter dominates the scoped
scalar-anchor screen in I.8: the
fraction of the electronics sector's output mix producible off-world
(sampled 0.10–0.30; ASSUMPTION with a documented bounding argument —
advanced-node logic and memory are not locally closable in this scenario
class; boards, passives, and power electronics plausibly are). No published
measurement exists. Among the quantities currently parameterized,
anchoring it is the highest-value observation this program could acquire;
that ranking does not cover omitted structural uncertainties.

An AI accelerator is already a supply-chain assembly rather than a single
“chip.” NVIDIA's H100 specification separately reports 80 GB of HBM3,
3.35 TB/s memory bandwidth, and 900 GB/s NVLink for the SXM product [S76].
TSMC separately describes front-end wafer fabrication and back-end advanced
packaging, including CoWoS interposers; its 2025 annual report records
qualification of a 5.5-reticle-size CoWoS solution and planned 2026 volume
production [S77]. These primary-source quantities anchor the structural split,
not the off-world coefficients.

The dedicated sensitivity resolves eight tiers: front-end logic fabrication,
memory fabrication, advanced packaging, substrates/interposers, high-speed
interconnect, power electronics, test/metrology, and radiation-qualified
system integration. Each has its own shelf life, physical failure,
economic-obsolescence, local production, import, reuse/down-bin, and
shortfall account. The declared sequence localizes test/metrology, system
integration/repair, and power electronics first; those three deliver more
early fulfilled demand per illustrative localization effort than memory or
front-end logic fabrication. The latter two retain a continuing Earth
umbilical in this branch. This is a resilience sequence, not a claim that
frontier fabrication is unnecessary. Machine-readable:
[AI electronics supply chain table](../outputs/integrated/tables/ai_electronics_supply_chain.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_electronics_supply_chain.csv"}.

**Integrated-bootstrap layer.** The ten-sector model asks
whether ten abstract capacities can grow together. The integrated model asks
whether a declared physical seed can supply the material, service,
autonomy, and commissioning requirements of another operating cell. It
expands the graph to 18 sectors — separating interconnects/boards,
passives/power, sensors/control, packaging/test, mature logic, advanced
logic/memory, and process equipment/metrology — and 17 material
categories (15 elements plus rare-earth and dopant classes; the model is
material-category-resolved, not element-resolved — stoichiometric and
process-chemical closure is not checked at the species level). Its
material balance is

::: {#eq:material-balance .equation}
$$
\Delta M_e
= \sum_s Y_{s,e}X_s + I_e + \sum_a F^{\mathrm{in}}_{a,e}
- \sum_j B_{e,j}x_j - L_e - \sum_a F^{\mathrm{out}}_{a,e},
$$
:::

with explicit Earth→Moon strategic-material stock, asteroid→Moon feed, and Moon→orbit
finished-compute arcs. The seed optimizer includes task coverage and
residual intervention, construction lags, yield ramps, minimum viable
scale, and process-specific gravity or centrifuge overhead. A dynamic pass
then requires constructed capacity to ramp through commissioning before it
contributes to the operating cell-equivalent aggregate. The equations, scenario definitions,
and reproducibility record are in Appendix D and
`outputs/integrated/MANIFEST.md`.

## I.8 Results {#i.8-results}

Monte Carlo over anchored ranges with common-cause shocks (n = 400 sampled
runs per cell; one shared draw per anchor per run, correlating parameter
uncertainty across sectors; every replication time is an output). The state
metrics are:

- **Balanced doubling (headline replication metric).** λ(t) =
  min_j K_j(t)/K_j(0); balanced doubling occurs when λ ≥ 2 — every modeled
  sector has at least doubled in its own capacity units. This is a
  balanced-capacity event, not a claim that a complete commissioned second
  plant or physical seed exists. λ is invariant to each sector's arbitrary
  capacity unit.
- **Aggregate doubling (secondary diagnostic).** First passage of Σ_j K_j to
  2× its initial value. This depends on the arbitrary units the sectors
  are denominated in and can be reached by overbuilding easy sectors while
  a hard sector lags and is therefore not the replication headline.
- **Endpoint hierarchy.** Reported timestamps are step ends. (1)
  *expanding@30* — realized post-shock worst-sector state change g > 0 at
  year 30, the weakest endpoint: such a run may still be import- and
  stock-supported; (2) *pre-shock allocation endpoint* — the optimizer's
  intended g before shocks, retained as a diagnostic rather than the
  headline; (3) *sustained* — realized g > 0 at every step ending in years
  25–30; (4) *Earth-import cutoff* — a separate central-set ensemble with
  all Earth imports cut at year 30, counting runs with realized g > 0
  throughout 30–35 (stock draw permitted). In LEO, captured feed continues,
  so that row is labeled **Earth import cutoff with continued capture
  feed**, not autonomy. None of these frequencies is called a real-world
  probability.
- **Binding sector and co-binding.** Each material-balance supply is
  relaxed by 1%, the allocation is re-solved, and the finite improvement
  in worst-case growth is measured. The perturbation is relative and
  therefore invariant to row units. Rows within 5% of the largest positive
  response form a co-binding set and share fractional credit. This replaces
  both the unit-sensitive slack heuristic and the degenerate LP-dual label.

The machine-readable outputs report two doubling denominators because they
answer different questions: *ever doubled* is the first-passage time among
all runs that ever reach the criterion within 35 yr (transient growth
capacity); *survivor-conditioned* restricts to runs also expanding at year
30 (sustained expansion performance). Table [@tbl-baseline-ensemble-outcomes] displays the
ever-doubled denominator; survivor-conditioned counts and times remain in
the CSV. The difference is a distinct outcome class — runs that doubled
early and then lost viability. All shares are frequencies across this
stipulated assumption ensemble and shock process — not empirical
probabilities of real-world success (machine-readable table:
[deep Monte Carlo table](../outputs/tables/mc_deep.csv){.artifact-link data-artifact="outputs/tables/mc_deep.csv"}):

> **Ten-sector model boundary.** Every run starts with positive capacity in
> all ten sectors. This layer has no construction lag, commissioning, yield
> ramp, or minimum efficient plant scale, and it permits continuous
> fractional capacity. Its reported years are stylized first-passage times
> inside an already complete abstract seed, not engineering schedules for a
> transported factory. The separate integrated layer below adds a physical seed
> and commissioning dynamics, but remains assumption-class.

All doubling columns below are **balanced capacity** events (λ ≥ 2: every
modeled sector doubled in its own units);
the aggregate-metric columns live in the CSV. LEO rows describe the
**import/capture-supported orbital recycling network** of I.6, not an
autonomous ecology.

| set | env | realized expanding@30 (share, 95% CI) | sustained 25–30 | pre-shock allocation endpoint | balanced doubled: n, median (IQR) | λ@30 median | co-binds most |
|---|---|---|---|---|---|---|---|
| conservative | LEO | 12/400 (0.03, 0.02–0.05) | 5 | 13 | 0 | 0.40 | mining 99.5% |
| conservative | lunar | 33/400 (0.08, 0.06–0.11) | 4 | 36 | 51, 9.5 (8.5–12.6) | 0.84 | electronics 93.8%, power 5% |
| conservative | Mars | 2/400 (0.01, 0.00–0.02) | 0 | 2 | 0 | 0.12 | power 51.8%, electronics 48% |
| central | LEO | 268/400 (0.67, 0.62–0.71) | 123 | 277 | 67, 26.0 (23.2–30.0) | 1.26 | mining 97.7% |
| central | lunar | 224/400 (0.56, 0.51–0.61) | 20 | 255 | 379, 5.0 (4.2–6.2) | 2.87 | electronics 95.5% |
| central | Mars | 60/400 (0.15, 0.12–0.19) | 4 | 66 | 33, 11.0 (8.0–11.2) | 0.55 | electronics 61.7%, power 38% |
| optimistic | LEO | 387/400 (0.97, 0.95–0.98) | 173 | 400 | 399, 10.8 (9.2–12.8) | 4.61 | mining 86.5%, electronics 14% |
| optimistic | lunar | 347/400 (0.87, 0.83–0.90) | 56 | 394 | 400, 2.8 (2.5–3.2) | 8.20 | electronics 96.5% |
| optimistic | Mars | 195/400 (0.49, 0.44–0.54) | 10 | 232 | 275, 5.5 (5.0–8.4) | 1.43 | electronics 66.8%, power 33% |

: Thirty-year baseline ensemble outcomes by assumption set and environment. [View data](../outputs/integrated/tables/ensemble_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/ensemble_summary.csv"}. {#tbl-baseline-ensemble-outcomes}

Earth-import cutoff (central set, all Earth imports cut at year 30; endpoint
= realized g > 0 at each step ending in the 30–35 window):

| env / qualification | positive realized growth at year 35 after Earth-import cutoff, stock draw permitted (share, 95% CI) | sustained positive realized growth throughout years 30–35 | pre-shock allocation endpoint |
|---|---|---|---|
| LEO — **Earth import cutoff with continued capture feed** | 210/400 (0.53, 0.48–0.57) | 88 | 224 |
| lunar | 170/400 (0.42, 0.38–0.47) | 23 | 187 |
| Mars | 53/400 (0.13, 0.10–0.17) | 2 | 64 |

: Five-year response to a year-30 Earth-import cutoff. {#tbl-earth-import-cutoff}

Reading: the conservative ensemble mostly fails on the realized endpoint:
3% of LEO, 8% of lunar, and 0.5% (2/400) of Mars runs are expanding at
year 30.
Central results are architecture-dependent: the realized endpoint is 67%
in LEO, 56% on the Moon, and 15% on Mars, while only 31%, 5%, and 1% of
all runs, respectively, remain positive throughout years 25–30. The gap
between the pre-shock allocation endpoint and the realized endpoint is the
cost of shocks at the reported step. The Mars synodic pulse can still
flatter a single endpoint; λ = 0.55 and 4/400 sustained central runs show
that contraction is the more informative reading there. Figure
[@fig-survival-central] exposes the full time path rather than privileging
one endpoint.

![Survival curves, central assumption set: fraction of runs with positive
realized maximin growth over time, by architecture. Ensemble frequencies
under the stipulated assumption set, not empirical
probabilities.](../outputs/figures/survival_deep_central.png){#fig-survival-central
.figure-standard fig-alt="Line chart of the fraction of simulated runs with
positive maximin growth over 30 years for LEO, lunar, and Mars architectures."}

Balanced doubling is faster on the Moon but the endpoint is more sustained
in LEO: among runs that ever reach λ ≥ 2, the central median is 5.0 years
on the Moon versus 26.0 in LEO. These are balanced-capacity first passages,
not construction records for complete second factories. LEO has no ore
body, so growth is throttled by captured and recovered material. Recycling
yield is below unity and recovery depends on loss type; recycling alone
cannot fund net expansion. The LEO Earth-import-cut row therefore preserves
capture feed and must not be described as autonomy. The lunar surface has
regolith feed and can grow quickly when electronics permits, while the
finite-response diagnostic assigns about 96% of central lunar co-binding
credit to electronics. The spread is the result: current evidence does not
close feasibility, but the model identifies the conditional measurements
that would.

**Cut sets and the ensemble-frequent minimum cut.** At central anchor values no
import cut set is fatal by year 30 anywhere — imports accelerate but are
not load-bearing *at central values*. That statement misleads alone,
because cuts appear near the feasibility margin. Over sampled anchors
(n = 40 draws per cell), conditional on an otherwise-expanding draw,
central lunar electronics and the all-import cut coincide in this
regeneration; central LEO is more exposed to the feed loop as a whole than
to electronics alone; and the small central Mars survivor set produces no
fatal candidate cut in this regeneration. Exact conditional frequencies
have moved materially across equally valid small-n regenerations. They are
reported in `outputs/report_deep.md` for reproducibility, but the defensible
claim is ordinal: cut dependence appears near the feasibility margin and is
architecture-specific; this experiment does not estimate a stable
real-world probability. Capacity knockouts at central
values: the eight physical production sectors (power, mining, refining,
robotics, machine tools, electronics, thermal, transport) are
knockout-indispensable in both architectures tested; repair is
additionally indispensable on the lunar surface. With LEO's 5% capture
feed, a recycling knockout is survivable at central values. The structural point is:
the LEO architecture lives on recovered and captured mass (capture/mining
receives 98% of central co-binding credit), so its dependency is the feed loop as a whole
rather than any single import line.

**The clock-setting curve.** Expansion frequency against the e-folding
time of Earth-supply withdrawal (n = 60 per grid point; machine-readable:
[import decay deep table](../outputs/tables/import_decay_deep.csv){.artifact-link data-artifact="outputs/tables/import_decay_deep.csv"}): on the lunar
surface under central assumptions, the realized year-30 endpoint is 0.40,
0.57, 0.43, 0.57, and 0.73 at 4-, 7-, 10-, 15-, and 25-year e-folding
times. The non-monotonic wobble is within binomial noise at this n. The
experiment is suggestive of a penalty for withdrawing the umbilical faster
than the closure ramp, with electronics stockpile shelf life as a plausible
mechanism. At $n=60$ per point it does not estimate a stable response
curve or its steepness; Figure [@fig-import-decay-sweep] therefore preserves
the observed sampling wobble.

![Expansion frequency at year 30 versus the e-folding time of
Earth-supply withdrawal, central set, n = 60 per grid point. The wobble is
within binomial noise at this n.](../outputs/figures/import_decay_sweep_deep.png){#fig-import-decay-sweep
.figure-compact fig-alt="Line chart of year-30 expansion frequency against the
Earth-import withdrawal e-folding time for LEO, lunar, and Mars cases."}

**Allocation-policy robustness.** The results above could in principle be
an artifact of the myopic one-step maximin allocator — a forward-looking
operator might accept lower current worst-case growth to build future
capacity. Because the dynamics and balances are linear, the finite-horizon
LP is solved exactly — though receding-horizon control remains an
approximation to full-horizon optimization (truncation and terminal-value
effects persist; an investment paying off after year six is invisible to a
six-year window). On paired
draws (identical parameter samples per policy, shocks off), a six-year
receding-horizon maximin reproduces the myopic policy essentially exactly
— 16/30 vs 16/30 sampled runs expanding on the lunar surface, 11/30 vs
11/30 in LEO, with co-binding shares computed under the same finite 1%
response definition as the baseline. The absolute level is not stable at
this small paired n — the lunar count has swung across equally valid
regenerations, so the policy *equality* is the stable finding, not the
level. The agreement holds because the maximin criterion already directs
each step's investment at the worst-off sector, which is the future
bottleneck. A third policy, maximizing aggregate
growth subject to no sector shrinking, collapses (0/30 in both
architectures): worst-case allocation is load-bearing, not incidental.
Bottleneck-first heuristics are subsumed by the maximin construction
itself. The defensible conclusion is correspondingly scoped: under paired,
shock-free draws for the tested LEO and lunar central cases, a six-year
receding horizon did not materially change the outcomes; global
allocation-policy robustness (longer horizons, perfect foresight, robust
control under shocks) is not established — and the retooling analysis of
Part IV exhibits one regime where allocation family genuinely matters. (`policies.py`; paired-draw comparison in
`outputs/report_deep.md`.)

**Scalar-anchor sensitivity screening — with its scope stated.** The claim that
the strategic-material gap and logistics penalty dominate is a computation, not an
assertion, and it is a *scoped* one — central assumptions, lunar
architecture, shocks off, scalar anchors only; it does not rank structural
requirement-matrix uncertainty, policy choices, shock distributions, or
interaction effects, and repeating it across environments and sets with
interaction-capable methods remains open cross-environment work:
Spearman rank correlation between each anchor's shared draw and the
worst-case growth rate at year 30 across the ensemble (n = 300, central/
lunar, shocks off; anchors are drawn independently, so per-anchor rank
correlation needs no independence corrections beyond the null band of
roughly ±0.11, wider under multiplicity). Two parameters tower above the
band: the space-electronics closure fraction (ρ ≈ +0.80) and the space
logistics penalty (ρ ≈ −0.48) — both ASSUMPTION-class, which is the
epistemic point: within this scalar screen, variation in year-30 growth is
dominated by exactly the two numbers no one has measured. Every other
screened anchor sits at or near
the null band. (`montecarlo.sensitivity`; ranked table in
`outputs/report_deep.md`.)

**Integrated seed and aggregate-capacity results.** The integrated layer is a
second, explicitly assumption-class model, not a relabeling of the
ten-sector balanced-capacity runs. Structurally it is a two-stage hybrid:
a multisector, multi-material seed-sizing LP, followed by sector-resolved
capacity-growth dynamics. All 18 sector capacities retain their own
commissioning lag, ramp, and depreciation; the continuous operating-cell
equivalent is derived as the slowest normalized operating sector rather
than advanced as the state. The published central trajectory orders balanced
seed-composition packets for continuity, while diagnostics compare
independent maximin-sector, surplus-preserving, shock-aware, and
perfect-foresight allocation. Failures enter explicit repair queues whose
return to service consumes parts, repair service, intervention capacity, and
time. Construction and commissioning are cohort-resolved.
A scenario is **LP-feasible** when the seed LP admits a solution
satisfying every material, service, autonomy, intervention, and
throughput constraint over the scenario horizon. The doubling metric is
**first passage to two operating-cell equivalents** — a continuous
aggregate crossing, not a discretely commissioned second factory. The
year-40 and terminal-window endpoints are separate. Central
deterministic scenarios and deterministic 200-draw assumption ensembles:

| bootstrap architecture | central minimum-mass installed seed | Earth strategic-material import stock (share of seed) | aggregate operating-capacity doubling, 80-year extension | sector-balanced cell-equivalents, year 40 | design-space occupancy (LP-feasible / 200) | feasible-draw seed p10 / p50 / p90 |
|---|---:|---:|---:|---:|---:|---:|
| terrestrial closure rehearsal | 206.9 t | 48.1 t (23%) | — | 0.47 | 81/200 | 171 / 201 / 228 t |
| lunar strategic-material bridge | 217.0 t | 58.2 t (27%) | — | 0.54 | 126/200 | 181 / 212 / 248 t |
| strict lunar-only | infeasible | — | — | — | 0/200 | — |
| Moon–asteroid network | 187.9 t | 0.0 t | 35.25 yr | 3.28 | 187/200 | 156 / 207 / 322 t |

: Bootstrap architecture sizing and growth outcomes. [View data](../outputs/integrated/tables/seed_objective_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/seed_objective_comparison.csv"}. {#tbl-bootstrap-architectures}

The occupancy column is a count under the declared log-uniform sampling
measure. It is not a calibrated probability, posterior, or empirical
success rate.

"Minimum-mass installed seed" is the LP's installed-equipment boundary, not
delivered cargo. A separate deployment model adds packaging, unloading and
site equipment, calibration references, initial spares, and startup-energy
storage, then tracks delivered, staged, installed, commissioned, failed,
recovered, and operating mass. Under those declared assumptions the 217.0 t
lunar-bridge seed is 303.6 t delivered and reaches full operation at about
5.8 years. The LP result remains conditional rather than a global optimum
over unknown processes or designs. A composition-changing Pareto search
varies process route, redundancy, and source portfolio; its 36-point frontier
is a design-space diagnostic, not a claim that the enumerated alternatives
are exhaustive. The
import-stock share is worth stating plainly: at 27% of installed
mass, the central lunar bridge is a substantially Earth-provisioned seed
whose local loop supplies bulk mass, not a nearly closed system with
trace imports. The year-40 column carries the crossing-versus-retention
distinction: neither the terrestrial rehearsal nor the lunar bridge ever
reaches sector-balanced doubling in the 80-year extension, and their
compute sectors fall to 0.47 and 0.54 equivalents at year 40. The
Moon–asteroid case crosses two at 35.25 years and reaches 3.28 at year 40
while expanding. The strategic import stock's
composition is resolved in
[import stock composition table](../outputs/integrated/tables/import_stock_composition.csv){.artifact-link data-artifact="outputs/integrated/tables/import_stock_composition.csv"}: Ni, Cu, and C dominate
at roughly 80% of the lunar-bridge stock, with initial-rate coverage
near five years per category.

The strict lunar-only case is a structural infeasibility, not a sampled
tail: the central LP is infeasible — the configured trace-material yields
cannot supply the assumed electronics and process-equipment stack — and
all 200 draws preserve that infeasibility, so 0/200 restates the
structure rather than measuring an uncertainty. Substitution, a different
electronics stack, a new refining route, or a richer measured deposit can
change it; the result is not a proof that lunar-only industry is
impossible. The Moon–asteroid case assumes a deliberately synthetic
composite portfolio rather than a known accessible body: 187/200 states
what a sufficiently diverse source network would have to supply, not that
such a portfolio is accessible, jointly recoverable on the assumed
timetable, or economical. In its central solution the Moon supplies 360.3
t/yr of feed and the asteroid portfolio 179.7 t/yr. Source occurrence
[S51–S56] bounds plausibility; it does not validate recoverable yield,
reserve, throughput, purity, or transfer cost.
Figures [@fig-seed-mass-ensemble] and [@fig-operating-capacity] separate
the installed-mass distributions from the resulting commissioning schedule.

![Installed seed mass across the 200-draw assumption ensembles, by
scenario. Distributions describe the declared parameter box, not
engineering uncertainty.](../outputs/integrated/figures/seed_mass_ensemble.png){#fig-seed-mass-ensemble
.figure-compact fig-alt="Interval plot of installed seed mass across four
scenarios and their 200-draw assumption ensembles."}

![Operating cell-equivalents over time in the central scenarios:
construction and commissioning lags separate ordering from operating
capacity.](../outputs/integrated/figures/operating_capacity.png){#fig-operating-capacity
.figure-standard fig-alt="Time-series chart of operating cell-equivalents in
the terrestrial, lunar bridge, strict lunar, and Moon-asteroid scenarios."}

**Terminal-window, ablation, and frontier diagnostics.** Five analysis
passes interrogate the same declared architecture without introducing any
new coefficient (machine-readable tables in `outputs/integrated/tables/`;
all regenerate with `rsi-run-integrated`):

- **Sector resolution invalidates the scalar crossing result.** The
  terrestrial and lunar-bridge cases are contracting (−0.022 and −0.027
  equivalents over years 35–40), never cross two in the 80-year extension,
  and are bottlenecked by compute at year 40. The Moon–asteroid network
  crosses two at 35.25 years, reaches 3.28 at year 40, and is expanding
  (+1.323); advanced logic/memory is its slowest normalized sector.
  Machine-readable 40/60/80-year endpoints are in
  [long horizon endpoints](../outputs/integrated/tables/long_horizon_endpoints.csv){.artifact-link data-artifact="outputs/integrated/tables/long_horizon_endpoints.csv"}, and the full 18-sector state is in
  [sector capacity trajectory](../outputs/integrated/tables/sector_capacity_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/sector_capacity_trajectory.csv"}.
- **The dynamic intelligence coupling is regime-dependent.** The
  terrestrial and lunar-bridge cases are each material-limited in 145/160
  quarterly steps, and separate freezes of research automation,
  task-autonomy improvement, and industrial-productivity improvement move
  their endpoints by less than 0.1%. The source-diverse network is
  material-limited in only 48/160 steps: removing both coupling channels
  reduces year-40 balanced capacity from 3.28 to 2.71, or 75% of baseline net
  growth. The 2×2 closure ablation supplies the stronger causal distinction:
  the bounded-controller, capital-reproducing branch still doubles at 36.75
  years, whereas an active digital loop with every new-capacity order blocked
  never doubles. This does not validate the coefficients; it shows that the
  implemented feedback becomes operative only after the stipulated source
  vector relaxes material supply and that reproductive capital is a separate
  switch ([ablations](../outputs/integrated/tables/ablations.csv){.artifact-link data-artifact="outputs/integrated/tables/ablations.csv"}; [closure loop ablation matrix](../outputs/integrated/tables/closure_loop_ablation_matrix.csv){.artifact-link data-artifact="outputs/integrated/tables/closure_loop_ablation_matrix.csv"}).
  The starting AI level also binds statically: re-sizing at base autonomy
  makes the bridge and network seeds infeasible. The exhaustive primary-cap
  classification assigns the remaining 14, 15, and 112 steps respectively
  to the declared gross order-rate cap; live service capacity is never the
  primary dynamic cap ([dynamic regime summary](../outputs/integrated/tables/dynamic_regime_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/dynamic_regime_summary.csv"}).
- **The finite response to intelligence changes with complements.** Holding
  every named complement fixed, a 0.1 capability-index uplift changes the
  terrestrial and lunar-bridge year-40 endpoints by −0.00016 and −0.00015
  balanced units, respectively: both quotients are near zero while material
  binds in 90.6% of steps. In the declared Moon–asteroid network, the same
  perturbation raises the endpoint from 3.280 to 3.636 and advances doubling
  from 35.25 to 34.50 years, a local quotient of 3.560 capacity units per
  capability-index unit. The tiny negative values in the material-starved
  cases are numerical/path effects, not evidence that intelligence is
  intrinsically harmful. A separate upgrade registry prevents proposed
  designs from becoming free capacity: the illustrative metrology line pays
  0.30 capacity-years and waits 1.25 years for design, 2.00 for construction,
  and 0.75 for verification before its increment appears at year 4; an
  underfunded radiator project never commissions. Light-speed latency,
  unavailable longitudinal observations, and external treaty authorization
  receive no automatic capacity increment
  ([intelligence marginal response table](../outputs/integrated/tables/intelligence_marginal_response.csv){.artifact-link data-artifact="outputs/integrated/tables/intelligence_marginal_response.csv"};
  [bottleneck upgrade projects](../outputs/integrated/tables/bottleneck_upgrade_projects.csv){.artifact-link data-artifact="outputs/integrated/tables/bottleneck_upgrade_projects.csv"};
  [bottleneck upgrade trajectory](../outputs/integrated/tables/bottleneck_upgrade_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/bottleneck_upgrade_trajectory.csv"}).
- **Scaling is not redesign.** Installing scaled copies of the minimum-mass
  composition does not rescue the terrestrial or lunar bridge case by year
  40. In the Moon–asteroid case, the 1.0×, 1.25×, 1.5×, and 2× seeds reach
  the first additional balanced equivalent at 35.25, 34.25, 33.5, and
  32.5 years. This sweep does not choose a different sector mix.
- **Relabeling the LP objective is also not redesign.** Lexicographic
  solutions for minimum installed mass, minimum Earth-import mass, and
  minimum intervention demand return the identical capacity vector in all
  three LP-feasible central scenarios. The current variables expose no
  tradeoff for those objectives to choose. A genuine Pareto front requires
  alternative process routes, redundancy, sector composition, or deployment
  decisions. The separate robust-seed search supplies those choices and
  reports dominated and non-dominated designs
  ([seed objective comparison](../outputs/integrated/tables/seed_objective_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/seed_objective_comparison.csv"}; [robust seed pareto](../outputs/integrated/tables/robust_seed_pareto.csv){.artifact-link data-artifact="outputs/integrated/tables/robust_seed_pareto.csv"}).
- **Failure reasons and binding constraints are per-draw.** Infeasible
  draws split between the autonomy threshold and the material LP
  (terrestrial 77/40, bridge 54/20, strict 33/167); feasible draws bind
  most often on Cu, C, Ni, and Cr (terrestrial and bridge) and on
  dopants plus refining and asteroid-transport throughput (network).
  The scalar-state claim that depreciation correlated positively with
  year-40 capacity is not retained: sector resolution makes depreciation
  and lag multipliers strongly negative against balanced year-40 capacity.
  The rank screen remains local to the declared independent multiplier
  measure, not a causal or global sensitivity result.
- **The strict-lunar cut is quantified.** An elastic relaxation of the
  exact seed LP names the unsatisfiable rows and their minimum
  shortfalls over the horizon: Ni 19.0 t, Cu 18.4 t, C 15.3 t, Co
  3.6 t, Cr 3.1 t, rare earths 2.3 t, Li 2.3 t, H 0.2 t, and dopants
  0.1 t. The infeasibility is a distributed material cut, and the
  machine-readable infeasibility certificate
  doubles as the engineering target list any lunar-only architecture
  claim would have to defeat.

Figure [@fig-oversize-frontier] makes the limited timing benefit of scaling
the unchanged seed composition visible.

![Oversize frontier: installed seed mass versus years to one additional
operating cell-equivalent, central
scenarios.](../outputs/integrated/figures/oversize_frontier.png){#fig-oversize-frontier
.figure-standard fig-alt="Scatter plot of installed seed mass against time to
one additional operating cell-equivalent for several oversize factors."}

The coupled run distinguishes installed compute from the slowest-sector
industrial aggregate. Figure [@fig-compute-growth-regimes] compares those
endogenous trajectories with rate-limited Earth-fed deployment. At year 40,
the Moon–asteroid scenario has 5.11
normalized total endogenous compute capacity while its balanced aggregate
is 3.28; compute is an independently constrained sector rather than a copy of the scalar
cell count. The run exports 0.66 normalized units to orbit. Constant-rate
Earth-fed orbital deployment reaches 1.56, 2.81, or
4.99 units under the tight, base, and responsive rate cases. Those curves
show the difference between rate-limited deployment and endogenous
capacity growth under the configured coefficients; they do not forecast
datacenter capacity.

![Rate-limited Earth-fed deployment versus endogenous capacity growth,
normalized compute capacity under the configured
coefficients.](../outputs/integrated/figures/compute_growth_regimes.png){#fig-compute-growth-regimes
.figure-standard fig-alt="Time-series comparison of rate-limited Earth-fed
orbital compute and endogenous Moon-asteroid compute capacity."}

The stateful debris stress test reports the **five-year fragment
creation-to-clearance ratio** $R_{\mathrm{debris}}$ — fragments created
divided by fragments cleared over the final five years, a flow ratio
rather than a branching-process reproduction number:

| deployment topology / mitigation | creation-to-clearance ratio, last 5 yr | fragment index, year 40 |
|---|---:|---:|
| Earth-fed orbit / weak | 0.61 | 1.602 |
| Earth-fed orbit / strong | 0.35 | 0.284 |
| dense endogenous / weak | 4.40 | 3.179 |
| dense endogenous / strong | 3.97 | 1.687 |
| distributed endogenous / sparse topology | 1.00 | 0.000 |

: Debris creation and clearance under alternative deployment strategies. [View data](../outputs/integrated/tables/debris_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/debris_summary.csv"}. {#tbl-debris-mitigation}

A ratio above one means only that more fragments were created than
cleared in the window; it is not a cascade threshold. Strong mitigation
lowers the dense case's fragment index (3.18 → 1.69) and its flow ratio
(4.40 → 3.97), but neither output establishes shell safety. The sparse
case's exact 1.00 is a zero-stock boundary, not a computed
equilibrium,[^p1-debris-zero-stock] and appears only under an assumed 0.01
collision-kernel multiplier. The result supports topology as a co-designed industrial
constraint; it does not establish a safe orbit, validate a debris
environment model, or locate a cascade threshold. Complete tables and
figures are generated from the same run in `outputs/integrated/`; Figure
[@fig-debris-regimes] shows the stock trajectories behind the windowed ratios.

[^p1-debris-zero-stock]: Realized clearance is capped by the fragments
    available. When the stock is empty, the reported creation-to-clearance
    ratio lands at its boundary value even though no positive-stock
    equilibrium has been demonstrated.

![Fragment-index trajectories by deployment topology and mitigation: the
debris stress test that produces the creation-to-clearance table
above.](../outputs/integrated/figures/debris_regimes.png){#fig-debris-regimes
.figure-standard fig-alt="Time-series chart of fragment index under concentrated,
distributed, and actively mitigated orbital deployment cases."}

**What Part I establishes and does not.** It establishes structure: which
sector binds, what the minimum cut is, how locations differ qualitatively
(lunar fastest-doubling but hostage to the electronics cut; LEO
feed-constrained but recycling-viable; Mars most path-dependent and
import-fragile, with no normalized scalar robustness ranking), and where
the feasibility margin lies — structure that survives the allocation-policy
variation above. The integrated layer additionally establishes which declared
material, autonomy, gravity, source, and commissioning constraints explain
its own seed scenarios. Neither establishes point feasibility: both
requirement matrices, element recipes and yields, strategic-material gap, repair
efficiencies, stockpiles, autonomy coefficients, lags, source portfolio,
and shock/debris rates are ASSUMPTION-class. Solar-array, regolith, sample,
or satellite data do not establish the coupled behavior of mines, bearings,
machine tools, electronics production, or dust-exposed radiators.

## I.9 Development path, annotated {#i.9-development-path-annotated}

0. **Terrestrial autonomous-closure rehearsal.** Before launch, operate an
   integrated seed factory on Earth using only the material forms, energy
   intermittency, communications constraints, spares allowance, and
   production methods intended for the lunar deployment. Exclude routine
   human entry; route every human intervention through a logged maintenance
   interface; inject equipment faults and communication outages; and require
   the system to manufacture, assemble, calibrate, and commission a second
   production cell. This stage does not reproduce lunar gravity, vacuum,
   radiation, or abrasive dust, so environmental qualification remains
   separate. It does test whether the industrial graph and its encoded
   operating knowledge are autonomous enough to export. Report intervention
   hours per machine-hour, imported mass per unit of added local capacity,
   critical bill-of-material lines producible, autonomous recovery fraction,
   time to a commissioned second cell, and every remaining single-point
   dependency. The execution contract in
   `params/rehearsal_protocol.yaml` fixes the boundary, typed event schema,
   ten binary gates, threat-complete fault campaign, 30-day retained-cell
   test, and parameter-replacement rules. Its generated matrix remains
   entirely `execution_pending` or `data_pending`; it is a protocol, not a
   result.
1. **Earth-dependent operations.** Earth supplies vehicles, energy systems,
   consumables, spares, electronics, and nearly all machinery; space assets
   perform narrow missions.
2. **Local-resource supplementation.** Local water, oxygen, shielding,
   construction feedstock, and selected propellant inputs reduce imported
   mass without yet closing the industrial loop.
3. **Heavy-industry closure.** The network produces bulk metals, glass,
   ceramics, structural parts, tanks, simple mechanisms, roads, pads, and
   large power structures.
4. **Advanced-manufacturing closure.** It adds motors, actuators, sensors,
   precision tools, robots, spacecraft subsystems, computers, and factory
   machinery. Terafab is best read as a terrestrial rehearsal of this stage
   (Part III.2): advanced-manufacturing integration practiced on Earth before
   any attempt to export it.
5. **Self-sustenance.** Internal production replaces depreciation and
   failure across every mission-critical category; Earth supply becomes
   optional rather than load-bearing.
6. **Self-expansion.** The system builds more mines, refineries, factories,
   power systems, robots, transports, and compute than replacement requires.
7. **Intelligence-industry recursion.** Additional compute improves
   intelligence; improved intelligence raises industrial replication
   efficiency; higher output creates still more compute.

This is the implemented industrial branch of Equation
[@eq:coupled-rsi-system]: intelligence raises verified task coverage and
replication efficiency; commissioned infrastructure adds usable compute; and
that compute can support a further verified intelligence update.

The bridge economy maps onto the ladder: terrestrial products carry the
early stages; launch and connectivity carry Stages 2–4; orbital compute is a
candidate Stage 4–5 tread; and in-space industrial services carry Stages
5–6. The model adds stage warnings. The Stage 4→5 transition is where the
strategic-material gap binds — no amount of Stage 3 bulk closure substitutes for an
electronics tier. Stage 5 is location-dependent: LEO requires a sustained
capture-and-recovery feed loop; under the present 5% capture assumption,
recycling is valuable but not knockout-indispensable at central values.
Mars requires electronics stockpiles engineered to synodic shelf life or a
local electronics tier. The lunar surface has the fastest conditional
balanced-doubling pathway when electronics closes sufficiently; LEO has the
more sustained central endpoint under its continuing-capture assumption.

**Location sequence and the lunar hybrid.** The development ladder is not a
ladder of orbital altitudes. In particular, *Sun-synchronous orbit* is a
planet-centered orbit whose plane precesses to preserve approximately the
same local solar time [S49]. The familiar dawn-dusk SSO is still LEO—the
650 km orbital-compute design assessed in Part II is an example—not the
destination after a lunar surface base.

For closure, the more coherent topology is:

1. **LEO as a bridge, not the terminal reservoir.** Communications,
   observation, early compute, assembly demonstrations, and transport can
   earn revenue and test systems, but bulk growth remains exposed to finite
   imported/captured feed and density-dependent collision risk.
2. **Lunar surface as the material backbone.** Extraction, bulk refining,
   construction, durable storage, shielding, and long-life machinery use a
   physical foundation and local regolith. South-polar planning seeks the
   conjunction of long illumination intervals and access to shadowed
   volatile deposits, while leaving reserve size and extraction economics
   unresolved; dust and landing ejecta remain major surface penalties
   [S47].
3. **Sparse lunar/cislunar orbit as the service layer.** Communications,
   navigation, observation, reusable transports, depots, assembly, and
   selected compute occupy orbit only where zero-g or illumination benefits
   repay shielding, stationkeeping, and service costs. NRHO is a candidate
   gateway geometry designed for eclipse avoidance and low stationkeeping,
   not a substitute ore body or a passive maintenance-free base [S48].
4. **Distributed heliocentric expansion after lunar export closure.**
   Productive nodes then spread across separated Sun-orbiting trajectories
   and resource paths—potentially including near-Earth objects—rather than
   reproducing one dense shell. The point is diversity of orbital elements
   and feedstocks, not one privileged "solar orbit." Moving inward raises
   solar flux but also heat-rejection, radiation, communications, and
   materials constraints, so no optimal solar radius is claimed.

**Material-source sequence.** The Moon is not chemically equivalent to
Earth, but neither is it short of bulk machine-building elements. Its crust
is dominated by oxygen, silicon, magnesium, iron, calcium, and aluminum,
with smaller titanium-bearing and other phases; composition varies strongly
between highlands and mare terrains [S51]. Those elements support oxygen,
glass and ceramics, aluminum, iron-bearing alloys, silicon feed, shielding,
structures, and many bulk machine parts, subject to extraction energy,
purification, alloying, yield, and process-equipment constraints. The early
system can therefore treat the lunar surface as a **bulk-material backbone**
while importing low-mass, high-criticality **material vitamins** from Earth:
advanced chips, dopants, catalysts, specialty chemicals, bearings, sensors,
precision tools, metrology, and any alloying elements whose local recovery
is not yet viable.

An order-of-magnitude inventory check prevents "no iron" from becoming a
false premise. At an average regolith bulk density near 1.5 t/m³ [S52],
one square kilometer excavated to one meter contains about 1.5 million
tonnes of regolith. Applying the approximately 3 wt% iron reported for lunar
highlands material [S53] gives roughly 45,000 tonnes of iron **in place**.
This is an illustrative inventory, not an ore reserve: it says nothing
about site homogeneity, mineral form, excavation losses, energy, recovery
yield, environmental impact, economics, or how much is practically
extractable. It does show why asteroid mining is not a prerequisite for
initial lunar iron.

The harder question is diversity. Lunar carbon and nitrogen occur at low
concentrations in returned fines, while polar water evidence remains
spatially heterogeneous and does not yet provide a bankable reserve
estimate [S54] [S55]. A robot-only ecology avoids agricultural and
biosphere-scale demand, but it still uses volatiles and specialty elements
for propellant, reduction chemistry, cooling, lubrication, polymers,
process gases, electronics, and high-performance alloys. Carbonaceous
asteroids and differentiated metal-rich bodies can eventually add water,
carbon-bearing material, nickel, cobalt, and other feedstocks; returned
Bennu material confirms carbon-rich organics and a history of water-related
mineral chemistry in at least one carbonaceous body [S56]. Asteroids are
therefore modeled as a **follow-on route to diversity and supply
sovereignty**, not invoked as the first source of every machine metal.

Current demonstrations make individual conversion paths more concrete
without closing the system. NASA describes integrated autonomous processing
of regolith simulant into silicon solar cells, aluminum wire, oxygen, iron,
and slag, alongside vacuum tests of molten-regolith electrolysis [S57].
These are meaningful subsystem demonstrations; they are not a lunar mine,
an operational supply chain, a factory reproducing its own equipment, or an
audited second production cell.

This ranks functions, not prestige destinations. Surface and orbit are
complements: orbit is the transfer and service network; the surface supplies
bulk matter and shielding. The ten-sector and Part II models
cannot compare that hybrid directly: they isolate lunar-surface capacity,
cislunar compute, and Earth-supplied lunar compute, and they aggregate
elements into industries. The integrated layer adds material-category bills
of material, source yields, Earth–Moon–orbit–asteroid arcs, and aggregate
endogenous debris states. It therefore computes an explicit hybrid scenario, but its
recipes, yields, transfer capacities, composite asteroid source, and
collision kernels are declared assumptions. It does not establish lunar
material sufficiency, a recoverable reserve, a launch date for asteroid
supply, or an orbital safety case.

## I.10 Binding bottlenecks and failure modes {#i.10-binding-bottlenecks-and-failure-modes}

With model annotations:

- **Lithography and fabrication equipment** — the named residual
  chokepoint one layer below foundries, and the deepest single closure
  problem in this framework.
- **Reliability and repair** — the model makes mean-time-to-repair and
  spares closure first-class: repair is an explicit sector with an
  efficiency and a spares bill.
- **Thermal management** — radiators are launched mass; Part II's
  radiator axis.
- **Energy storage and continuity** — the lunar night storage mass term;
  Mars dust-storm shocks.
- **Resource quality** — LEO has no ore body, so the sustained
  capture-and-recovery feed loop binds even though the separately modeled
  recycling sector is not knockout-indispensable at central values.
- **Verification and control** — Part III.4.
- **Political and legal environment.**
- **Economic survival of the transition** — Part II.1.
- **Concentrated coordination** — single points of failure a distributed
  competitor lacks.
- **Paradigm-shift stranding** — Part IV.3; exposure concentrated in the
  fabrication layer, while the fleet self-insures through its own
  3–6-year depreciation.

* * *
