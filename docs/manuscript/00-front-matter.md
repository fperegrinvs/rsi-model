# Recursive Industrial Intelligence {#recursive-industrial-intelligence}

## r4.0 · July 2026 {#r4.0-july-2026}

**Leonardo Stern · Independent researcher**

*Orbital compute may be more than a data-center product: it can be tested as
the first anchor demand for a physical stack that capable AI could improve
and eventually expand beyond Earth. This paper prices that Earth-dependent
bridge and models the conditions under which an autonomous industrial seed
could maintain and expand operating capacity.*

## Abstract {#abstract}

SpaceX's orbital-compute program motivates a broader conditional thesis:
Starmind could function as an industrial seed rather than only as a
standalone data-center product. An initially expensive, Earth-dependent
deployment could create anchor demand and operating experience across
reusable launch, spacecraft manufacturing, energy, thermal management,
communications, silicon, robotics, and servicing. If capable AI accelerates
the improvement of that physical stack, additional industrial capacity could
support more compute and intelligence, coupling digital and physical growth.
This paper tests the engineering and economic conditions for that
interpretation without treating it as established corporate intent.

This paper expands the object of analysis from
an abstract industrial substrate to a capacity-expanding autonomous seed:
physical equipment, embodied autonomy, software and simulation, industrial
memory, experimental capacity, and material-category-resolved supply. Part I implements a ten-sector, multisector
capacity model with decomposed depreciation, repair, recycling, stockpiles,
imports, common-cause shocks, and architecture-specific constraints for LEO,
the lunar surface, and Mars. Its unit-invariant replication metric is
balanced capacity doubling; its endpoint is realized post-shock growth, and
its bottleneck diagnostic is a finite 1% supply-response test with explicit
co-binding. The assumption ensembles produce outcomes ranging from collapse
to sustained expansion, with electronics dominant on the Moon, electronics
and power on Mars, and captured/recovered feed dominant in LEO.
The ten-sector model begins with positive capacity in all ten sectors and
omits construction lags, commissioning, yield ramps, and minimum efficient
scales; its doubling times are stylized capacity-model first passages, not
factory-construction or seed-commissioning forecasts. Part II
builds an affine levelized-cost model for terrestrial and space compute,
separating integrated disposable satellites from serviceable/reusable
platforms. After completing the system boundary with communications,
ground network, spacecraft bus, program NRE, insurance, regulatory and
disposal costs, residual value, thermal margins, and separate financing,
generic LEO compute costs 5.29 times Earth on the serviceable-platform
architecture and 6.74 times Earth if integrated and disposable; the
SpaceXAI AI1 disclosed-design case remains 3.17 and 3.80 times Earth,
respectively. The analysis therefore supports neither a point
forecast of autonomous industry nor present orbital-compute parity. It
identifies the architecture-dependent measurements and demonstrations that
would most change those conclusions. An 18-sector, 17-material-group
integrated-bootstrap model then represents an installed operating seed —
physical equipment with stylized autonomy, intervention, construction, and
commissioning constraints — and asks how much installed mass is
sufficient, whether its material graph can close first on the Moon and
later across asteroidal sources, and whether aggregate operating capacity
can double without routine human intervention. Under the declared central
assumptions, the minimum-mass lunar design retaining an Earth-supplied
strategic-material import stock is 217.0 t installed — 58.2 t (27%) of
it that stock — but its slowest normalized sector falls to 0.54 operating
cell-equivalents by year 40; the configured strict lunar-only source graph is
structurally infeasible, with the shortfall quantified per material
category; and a synthetic composite Moon–asteroid portfolio satisfies
the same seed-LP constraints at 187.9 t, crosses two at 35.25 years, and
reaches 3.28 sector-balanced equivalents at year 40. Keeping all 18 sectors
stateful changes the interpretation: the intelligence–industry coupling is
nearly inert in the
material-starved terrestrial and lunar-bridge cases but operative in the
Moon–asteroid network, where removing it reduces year-40 balanced capacity
from 3.28 to 2.71. The assumed AI level also binds statically through seed
feasibility. These are deterministic
consequences of a stipulated architecture and assumption ensemble
(Part I.8), not seed designs, engineering estimates, or forecasts. The
model operationalizes the coupled loop and sharpens its material and
autonomy conditions; it does not demonstrate that the assumed processes,
source portfolio, AI gains, or industrial closure exist.

**Keywords:** recursive industrial improvement; space manufacturing;
industrial closure; orbital compute; lunar industry; multisector capacity;
autonomous industrial seed; embodied autonomy; lunar materials;
techno-economics; Monte Carlo.

**On this page:** [Executive Summary](#executive-summary) ·
[Scope, Claims, and Evidence](#scope-claims-and-evidence) ·
[Proposition ladder](#proposition-ladder) ·
[How to read this document](#how-to-read-this-document)

## Executive Summary {#executive-summary}

SpaceX's orbital data centers may be more ambitious than the product category
suggests. This document examines whether they could serve as an industrial
seed: initially costly, Earth-dependent infrastructure that creates anchor
demand and operating experience for the launch, energy, manufacturing,
communications, silicon, robotics, and servicing capabilities needed by a
larger AI-driven space economy. If more capable AI can improve how that stack
is designed, built, and operated, better intelligence could create more
physical capacity, which could in turn support more intelligence.

This is not a comparative claim that the pathway outweighs
health, science, terrestrial abundance, climate, governance, or other uses of
advanced AI. The end state is not merely a rocket fleet,
a settlement, a humanoid robot, or a frontier model, but a distributed
industrial ecology able to sustain itself, expand productive capacity, and
progressively reduce Earth dependence.

Three questions remain separate throughout: which uses of advanced AI most
benefit humanity; which architecture creates the largest long-horizon
physical-growth option; and which hypothesis best explains the observed
corporate portfolio. The paper models the second and tests evidence relevant
to the third. It does not rank the first against health, poverty reduction,
science, climate, governance, or other welfare objectives.

Powerful AI could be transformative without any space-industrial program.
Conversely, an industrial system that achieves embodied-production and
reproductive-capital closure can compound under a bounded controller without
open-ended AI self-improvement. Their conjunction may accelerate the pathway;
neither thesis establishes the other.

> **Central proposition.** Once a space-based industrial system can obtain
> local energy and materials, maintain its machinery, manufacture additional
> productive equipment, and coordinate itself through AI, the primary
> constraint shifts from acquiring terrestrial inputs to allocating
> productive throughput over time.

That proposition distinguishes two growth regimes. An orbital data center
whose servers, structures, power systems, and replacements continue to be
made on Earth is **deployed capacity**, not a self-expanding industry:

::: {#eq:orbital-deployment .equation}
$$
\frac{\mathrm d C_{\mathrm{orbit}}}{\mathrm d t}
= q_c L_{E\rightarrow O}(t)-\delta_C C_{\mathrm{orbit}}.
$$
:::

At a constant Earth-to-orbit delivery rate $L_{E\rightarrow O}$, capacity
grows approximately linearly while depreciation is small and ultimately
approaches $q_cL_{E\rightarrow O}/\delta_C$. By contrast, a closed
industrial stock that allocates a fraction of its own output to producing
additional productive equipment follows the idealized endogenous law

::: {#eq:endogenous-hardware-growth .equation}
$$
\frac{\mathrm d H}{\mathrm d t}=(r-\delta_H)H,
$$
:::

and compounds only when $r>\delta_H$. Off-Earth location does not create
that acceleration: **reproductive closure does**. The role of off-Earth
industry is to combine that endogenous growth regime with access to matter,
energy, and usable area outside Earth's biosphere and society-priced siting
constraints. Earth-fed orbital compute can therefore raise intelligence at
a constant deployment rate without crossing the industrial-reproduction
threshold; the two cases must not be conflated.

The framework separates three closures. **Verified AI-R&D closure** can
produce and safely deploy accepted successor improvements.
**Embodied-production closure** can execute every task on the active
industrial minimum cut with available sensors, actuators, experiments, and
recovery. **Reproductive-capital closure** can replace and expand every
indispensable capital stock after depreciation and obsolescence. None implies
the others. When all are present, the digital and physical loops can reinforce
one another:

::: {#eq:coupled-rsi-system .equation}
$$
\begin{aligned}
\mathbf c_{t+1}
  &= \Pi_{[0,\mathbf c^{\max}]}\!\left[
       \mathbf c_t+f_c(I_t;\theta_c)\right],\\
\mathbf K_{t+1}
  &= (1-\Delta t\,\boldsymbol\delta_K)\odot\mathbf K_t
     +\boldsymbol\Gamma_{K,t}\odot
      f_K(\mathbf c_{t-\tau_c},\mathbf R_t;\theta_K),\\
C_{t+1}
  &= (1-\Delta t\,\delta_C)C_t
     +\Gamma_{C,t}f_C(\mathbf K_{t-\tau_K},E_t,H_t;\theta_C),\\
I_{t+1}
  &= \Pi_{[0,I^{\max}]}\!\left[
       I_t+\Gamma_{I,t}f_I(C_{t-\tau_C},D_t,V_t;\theta_I)\right].
\end{aligned}
$$
:::

Here $I_t$ is the intelligence-capability index, $\mathbf c_t$ is the
vector of task coverage and autonomy, $\mathbf K_t$ is installed productive
capacity by sector, and $C_t$ is usable compute. $\mathbf R_t$, $E_t$, $H_t$,
$D_t$, and $V_t$ are the limiting material-resource, energy, compute-hardware,
data, and verification states. The $\tau$ terms are stage-specific delays;
$\boldsymbol\delta_K$ and $\delta_C$ are depreciation rates; the
$\Gamma$ terms collect construction, commissioning, verification, and
authorization gates; and $\Pi$ imposes declared capability ceilings.
The response functions are saturating, resource-bounded mappings, not
constant gains. In plain language: better intelligence can improve
automation; verified automation can expand productive capacity; commissioned
capacity can add usable compute; and usable compute can support further
verified intelligence improvement.

A dimensionless local diagnostic may be formed from the product of the four
elasticities around this path,
$G_{\mathrm{loc}}=\epsilon_{cI}\epsilon_{Kc}\epsilon_{CK}\epsilon_{IC}$,
or, for the complete coupled state, from the spectral radius
$\rho(J_t)$ of its one-step Jacobian. A value above one means only that a
small perturbation is locally amplified at that state and under those active
gates. It is not sufficient for physical closure, stable or safe operation,
global growth, or indefinite improvement.

That coupled case is the strongest acceleration branch, not the definition of
all endogenous growth. The central Moon–asteroid model still reaches balanced
physical doubling in 36.75 years when digital capability growth is frozen,
versus 35.25 years with both loops active; with capital reproduction blocked,
digital improvement alone never produces physical doubling. Control and
verification are separate constraints in every branch.

The economic argument compresses to two walls and two escapes. The capital
wall: expansion purchased through markets runs into scarcity pricing and
supply-elasticity limits as ambitions scale; the escape is self-replication,
which re-denominates expansion from dollars into materials, energy, and
time. The operating wall: on Earth, society-priced costs — land, permits,
politics, waste heat — rise with scale and cannot be closed away; the
escape is space, where permission attaches to the gateway rather than the
complex. Both escapes pass through one passage: the bridge, in which the
first self-replicating seed is bought at full market price, operated where
depreciation is most severe, and financed by intermediate products.

Orbital compute is a candidate bridge product because it exercises many of
the required systems before they are locally reproducible. Its first
generation need not be cost-optimal to create learning across launch cadence,
spacecraft production, power, thermal management, communications, silicon,
autonomy, and servicing. That strategic value is a hypothesis, not a free
credit in the economic model: it must appear as attributable cost reduction,
faster capacity activation, cross-program reuse, or declining Earth
dependence. Capable AI could accelerate design and operating cycles across
the stack, but it cannot remove construction, qualification, heat-rejection,
or material-flow constraints.

This paper prices the passage and models the seed. Five headline results:

1. **The active bottleneck is architecture-specific.** A unit-invariant
   finite-response diagnostic relaxes each material balance by 1%, then
   divides credit among rows whose positive response is within 5% of the
   largest. Electronics receives about 94–97% of co-binding credit on the
   lunar surface; electronics and power divide most credit on Mars; and
   capture/mining receives about 86–100% in LEO. The LEO architecture has
   no ore body and depends on captured and recovered feed. Import-cut
   experiments are small, margin-conditional samples, so their defensible
   executive-level result is ordinal rather than a precise frequency:
   import dependency is architecture-dependent, and electronics is often
   load-bearing where the sampled strategic-material gap is deepest. That identity is
   conditional on a homogeneous electronics-productivity assumption, not a
   measurement of real electronics closure.
2. **Balanced-capacity doubling and sustained expansion are different
   outcomes.** The headline replication metric is λ(t) =
   min_j K_j(t)/K_j(0) ≥ 2: every modeled sector has doubled in its own
   capacity units. It is not a claim that a commissioned second physical
   factory exists. The endpoint records realized, post-shock growth; the
   pre-shock allocation endpoint remains a diagnostic. In the declared
   central sampling measure, expansion at year 30 occupies a much larger
   region than sustained positive realized growth throughout years 25–30.
   Median balanced doubling among sampled runs that reach it is about
   26.0 years in LEO, 5.0 on the Moon, and 11.0 on Mars. Exact occupancy
   counts and intervals are reported in Part I.8. The Earth-import-cut LEO
   result is expressly
   conditional on continued capture feed and is not an autonomous-ecology
   result.
3. **The space-compute crossover is an architecture story, not a
   launch-price story.** At central inputs, generic LEO compute is 5.29×
   Earth on a serviceable/reusable platform and 6.74× if the satellite is
   integrated and disposable. The SpaceXAI AI1 disclosed-design scenario is
   3.17× and 3.80×, respectively. No sampled point in the declared
   2,000-draw shared design-space sweep favors space in any reported
   architecture/reference cell. This is design-space occupancy under the
   stated measure, not a calibrated probability. Negative
   median break-even launch prices show why: qualification cost, hardware
   and platform life, and utilization can dominate launch. The
   deterministic aspirational case is still 1.09× Earth after the completed
   cost boundary, versus 0.76× for the deliberately omitted-cost diagnostic. It
   combines company targets with three favorable, unpublished model bounds
   and is assigned no probability.
4. **The installed seed is a material-and-knowledge graph, not a cargo
   total.** The 18-sector, 17-material-group layer requires physical
   equipment, digital tools, industrial memory, experiments, task-resolved
   autonomy, gravity-compatible processes, and aggregate operating-capacity
   growth. The LP sizes an installed seed, while a separate deployment
   diagnostic moves delivered mass through staged, installed, commissioned,
   startup-failure, recovery, and operating states. For the lunar bridge,
   217.0 t installed corresponds to 303.6 t delivered under the declared
   packaging, site, spares, calibration, and startup-energy assumptions. Its
   doubling metric is first passage of the *slowest normalized sector*
   to two operating-cell equivalents, not a discretely commissioned second
   factory. Under the declared central assumptions, the lunar
   strategic-material bridge requires 217.0 t installed, of which 58.2 t
   (27%) is Earth-supplied strategic-material stock — a substantially
   Earth-provisioned seed, not a nearly closed one — but the slowest sector
   reaches only 0.54 cell-equivalents at year 40. The terrestrial rehearsal
   similarly reaches only 0.47. The configured strict lunar-only source graph is
   structurally infeasible — its trace inputs cannot supply the assumed electronics
   and process-equipment stack, in the central case and in every draw. A
   deliberately synthetic composite Moon–asteroid portfolio satisfies the
   same seed-LP constraints at 187.9 t, crosses two at 35.25 years, and
   reaches 3.28 sector-balanced equivalents at year 40. Across 200 deterministic
   assumption draws, the lunar-bridge, strict-lunar, and Moon–asteroid
   cases occupy the satisfying region in 126, 0, and 187 of 200 declared
   draws (the terrestrial rehearsal in 81). These counts describe
   design-space occupancy under the stated log-uniform measure, not
   empirical frequencies or success probabilities.
5. **The declared AI coupling matters only after material bottlenecks
   relax.** In the terrestrial and lunar-bridge cases, material availability
   caps construction in roughly nine-tenths of quarterly steps, so coupling
   ablations change the year-40 endpoint by less than 0.1%. In the
   Moon–asteroid network, only 48/160 steps are material-limited and the
   fully uncoupled run reaches 2.71 balanced equivalents versus 3.28 at
   baseline — 75% of baseline net growth. This is a within-model regime
   change, not evidence that the stipulated AI coefficients are real. The
   assumed AI level is also load-bearing *statically*:
   at base autonomy the lunar-bridge and Moon–asteroid seeds fail the
   feasibility threshold outright. Only the Moon–asteroid network reaches
   two equivalents by year 40 and is terminal-window expanding.

The integrated layer also makes one architecture boundary stateful:
**industrial closure does not license a dense orbital shell.** Active,
derelict, and fragment stocks feed a **five-year fragment
creation-to-clearance ratio** $R_{\mathrm{debris}}$ — a flow ratio over
the final five years, not a branching-process reproduction number or a
derived criticality threshold. In the declared year-40 scenarios, the
Earth-fed orbital cases clear more fragments than they create
($R_{\mathrm{debris}}=0.61$ with weak mitigation and 0.35 with strong),
while dense endogenous deployment creates substantially more than it clears
under both mitigation levels ($R=4.40$ weak and 3.97 strong, while the
fragment index falls from 3.18 to 1.69). This remains a stress-test
indicator rather than
a safety measure. A sparse distributed topology sits at the boundary
ratio of 1.00 with an empty fragment stock only because its
collision-kernel multiplier is explicitly set to 0.01. These are
topology stress tests, not orbital traffic forecasts or
cascade-threshold results [S45–S49].

The strategic assessment (Part III): the evidence **documents an integrated
off-world portfolio direction ([P4a — Documented portfolio direction](proposition:P4a){.proposition-ref}) but does not establish one coordinated
technical architecture**. The initiative list and first-party messaging
rule out a purely terrestrial reading. They are consistent with a
physical-stack seeding hypothesis in which orbital compute creates anchor
demand and shared learning, while the matched H0 still explains co-ownership,
portfolio promotion, supply hedging, and adjacent commercial projects without
a common systems plan. The evidence therefore does not establish the seeding
hypothesis as management's actual strategy.

It also **does not establish recursive
closure as the objective ([P4b — Recursive-closure intent](proposition:P4b){.proposition-ref})**: the closure-specific observables — seed
bills of materials, reproduction metrics, minimum-cut roadmaps, locally
reproducible production equipment — remain absent. The discriminating
indicators are *model-ranked*: the rational
next moves of a closure-seeking actor — electronics-closure engineering,
loss-tolerant orbital-compute persistence, materials-recovery recycling —
are exactly the observations the models identify as informative.

<span id="scope-and-status"></span>

## Scope, Claims, and Evidence {#scope-claims-and-evidence}

This is a strategic hypothesis and research program with an
quantitative core — not a techno-economic demonstration. It identifies
necessary conditions, bottlenecks, and discriminating tests for a
self-expanding industrial system, computes what its own assumptions imply,
and states throughout which of its six propositions each conclusion rests on.

The reference system in this paper is **machine-only**: no resident human
population, agriculture, or biosphere-scale life-support loop is required
for industrial reproduction. Human settlement can create demand and impose
additional requirements, but it is not a prerequisite of the thesis. Water,
hydrogen, carbon, nitrogen, and oxygen remain important as propellants,
reductants, coolants, lubricants, polymers, process gases, and chemical
feedstocks; removing agriculture narrows the closure problem but does not
remove volatile chemistry from it.

## Proposition ladder {#proposition-ladder}

The six claims assessed in this document have one canonical definition and
current evidential status:

::: {.proposition-ladder}

### P1 — Conceptual possibility {#proposition-p1 .proposition-definition}

**Canonical claim:** A recursively expanding industrial system is conceptually possible.

**Current status:** A respectable conceptual case is made; no demonstrated closure is required.

### P2 — Technical feasibility {#proposition-p2 .proposition-definition}

**Canonical claim:** A recursively expanding industrial system might eventually be technically feasible.

**Current status:** Quantitatively explored across named assumption sets; complete-system feasibility is not demonstrated.

### P3a — Earth-dependent bridge economics {#proposition-p3a .proposition-definition}

**Canonical claim:** Orbital and lunar compute during the Earth-dependent bridge would be economically competitive.

**Current status:** Quantified and negative at anchored values; crossover requires a specific, currently unanchored parameter corner.

### P3b — Mature high-closure economics {#proposition-p3b .proposition-definition}

**Canonical claim:** A mature, high-physical-closure space-industrial ecology would eventually obtain a structural economic advantage over terrestrial expansion.

**Current status:** Scenario-modeled but unresolved; neither tested space case becomes self-financing inside 40 years under the declared assumptions.

### P4a — Documented portfolio direction {#proposition-p4a .proposition-definition}

**Canonical claim:** The companies are deliberately integrating launch, communications, AI, compute, chip manufacture, and prospective off-world energy and manufacturing.

**Current status:** The portfolio direction is documented; shared technical interfaces, binding milestones, and joint resource allocation are not publicly established.

### P4b — Recursive-closure intent {#proposition-p4b .proposition-definition}

**Canonical claim:** The integrated portfolio is intended to produce recursive industrial closure.

**Current status:** Inferential; no closure program, seed bill of materials, reproduction metric, or minimum-cut roadmap is published.

:::

The filing record behind the documented portfolio direction names orbital
compute, lunar manufacturing and energy, in-orbit manufacturing,
manufacturing on the Moon and Mars, asteroid mining, and “interplanetary
industrialization” among the initiatives (Form S-1 pp. 164, 171; roadshow
slides 42–44) [S27]. The recursive-closure reading remains assessed against
competing explanations in Part III.

The P4 split matters because its two halves carry materially different
evidential status. Conclusions are
licensed by the strongest proposition they rest on, not by the
conjunction of all six.

**Evidential classes.** Documented statements; announced initiatives;
technically grounded pathways; inferred strategy; and speculative closure are
supplemented by one additional rung: **computed**, meaning derived
mechanically from stated assumptions by the companion model (public repository with checksummed output manifest, Appendix C). A computed result
inherits the epistemic class of its weakest input; structural coefficients
are ASSUMPTION-class throughout, so no computed result is a measurement.
Every computed number below carries its assumption-set label
(conservative / central / optimistic); a result quoted without its set
label is a misquotation.

Claim status and input provenance are separate taxonomies. The six
evidential classes above qualify propositions and conclusions. Model inputs
instead use five source classes: `peer_reviewed`, `technical_report`,
`reporting`, `company_statement`, and `ASSUMPTION`. A computed output
inherits the weakest input class in its dependency chain.

| evidential category | proposition or observation | current status |
|---|---|---|
| Documented | Mars-city objective; integrated energy and manufacturing programs; AI research mission; the SEC-filed off-world initiative list ([P4a — Documented portfolio direction](proposition:P4a){.proposition-ref}) | direct statements and regulatory filing |
| Announced / partly advanced | Terafab, Intel participation, executed county agreements, and a named orbital-silicon line | declared initiative with unsettled implementation |
| Technically grounded | ISRU, autonomous excavation, robotic construction, and the self-replicating-factory literature ([P1 — Conceptual possibility](proposition:P1){.proposition-ref}/[P2 — Technical feasibility](proposition:P2){.proposition-ref} pathway) [S4] [S5] [S23] [S24] | recognized engineering pathway; system closure undemonstrated |
| Computed | industrial-substrate feasibility, material-category-resolved seed and aggregate-capacity-growth scenarios ([P2 — Technical feasibility](proposition:P2){.proposition-ref}), and bridge-economy compute costs ([P3a — Earth-dependent bridge economics](proposition:P3a){.proposition-ref}) | mechanical implications of assumption-class inputs, not measurements or empirical probabilities |
| Inferred | the observed portfolio is intended to progress from integrated off-world industry to recursive closure ([P4b — Recursive-closure intent](proposition:P4b){.proposition-ref}) | strategic synthesis; closure-specific observables remain absent |
| Speculative | a mature high-closure ecology obtains a structural economic advantage ([P3b — Mature high-closure economics](proposition:P3b){.proposition-ref}) | symmetric dynamic economics are implemented as assumption-class scenarios; neither tested space case self-finances inside 40 years, and empirical mature-system advantage remains unresolved |

: Evidential status of the article's proposition ladder. {#tbl-evidential-status}

## How to read this document {#how-to-read-this-document}

The four parts carry different kinds of claim and can be read
independently:

- **Part I** is model: the ten-sector capacity model and the
  integrated-bootstrap layer. Its results are computed implications
  of declared assumption sets, never measurements. The canonical numeric
  tables are in I.8; every restatement elsewhere (Abstract, this
  summary, III.6, IV.1) follows them.
- **Part II** is techno-economics: the levelized-cost crossover model and
  its reconciliation with independent studies. Canonical tables in II.3.
- **Part III** is interpretation: an ordinal, evidence-tabled assessment
  of corporate strategy. It contains no model outputs, only their use as
  ranking criteria for observables.
- **Part IV** is quarantined scenario extrapolation plus the limitations
  statement; nothing in it feeds back into Parts I–II.

Readers who want only the load-bearing results should read the
Executive Summary, I.8, II.3, and the Limitations section. The
epistemic rules — source classes, ASSUMPTION labeling, and the
frequency-not-probability convention — are defined in
[Scope, Claims, and Evidence](#scope-claims-and-evidence)
and apply everywhere. Appendix A carries parameter provenance,
Appendix B the implementation and provenance record, Appendix C
reproducibility, and Appendix D the
complete model specification.

* * *
