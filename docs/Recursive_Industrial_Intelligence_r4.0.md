# Recursive Industrial Intelligence {#recursive-industrial-intelligence}

## r4.0 · July 2026 {#r4.0-july-2026}

**Leonardo Stern · Independent researcher**

*A self-sustaining, self-expanding space industrial system is coherent as an argument; whether it is feasible or economical is a question for models. This paper combines the executed models with an explicit autonomous seed, its knowledge package, its material flows, and the dynamics by which it attempts to expand operating capacity.*

## Abstract {#abstract}

This paper develops and tests a conditional thesis: advanced AI, reusable
launch, robotics, energy systems, and automated manufacturing could be
combined into an industrial system beyond Earth that maintains and expands
its own productive capacity. This paper expands the object of analysis from
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

This document examines one possible long-horizon infrastructure value of
advanced AI, reusable launch, energy systems, robotics, and automated
manufacturing: combining them into a recursively improving industrial system
beyond Earth. This is not a comparative claim that the pathway outweighs
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
rule out a purely terrestrial reading, while the matched H0 still explains
co-ownership, portfolio promotion, supply hedging, and adjacent commercial
projects without a common systems plan. It **does not establish recursive
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

# Part I — Technical Feasibility {#part-i-technical-feasibility}

## I.1 Recursive self-improvement: the digital loop {#i.1-recursive-self-improvement-the-digital-loop}

Recursive self-improvement (RSI) occurs when an intelligent system
contributes to the process that produces a more capable successor. The
useful unit must be named relative to the use being claimed. A technically
validated gain has survived the applicable held-out and regression tests. An
authorized internal loop additionally permits that gain to advise or act in a
specified monitored role, with consequence-appropriate access, rollback, and
observation. A public release is a later and separate event requiring broader
external assurance. The common pipeline is: identify a weakness, form a
hypothesis, implement a change, train or run an experiment, evaluate it,
authorize its claimed use, and observe the result. A proposal or training run
that has not passed technical validation is work performed, not a capability
gain; public release is not required to complete a bounded internal loop.

### Observed precursors are narrower than closure {#observed-ai-rd-loop-precursors}

Three public systems implement substantial pieces of that pipeline, but they
modify different objects and stop at different gates:

| system | object modified | search topology | evaluation signal and observed result | human role | verification boundary | does not demonstrate |
|---|---|---|---|---|---|---|
| Karpathy `autoresearch` [S86] | `train.py`: model architecture and training procedure, not the acting model's weights | serial keep/discard hill climb | fixed `val_bpb` after five minutes on one GPU; approximately 12 attempts/hour and 100 overnight are design capacity, while the canonical run ledger is unpublished | supplies or approves the agent instructions and starts/stops the run | fixed evaluator; no independent transfer, safety, or deployment gate | a measured success rate, successor-model closure, or open-ended improvement |
| Darwin Gödel Machine (DGM) [S87] | coding-agent scaffold, tools, and workflow around frozen foundation models | branching archive search that can retain weaker stepping stones | after 80 iterations, SWE-bench rose from 20.0% to 50.0% and full Polyglot from 14.2% to 30.7%; both no-self-improvement and no-archive ablations were weaker | fixes the search process, benchmarks, model APIs, sandbox, and oversight | staged benchmark tests plus transfer checks, lineage inspection, and sandboxing; objective hacking was found separately | improvement of foundation-model weights, indefinite returns, or an authorized successor-model loop |
| AI Scientist-v2 [S88] | hypotheses, experiment code, results, figures, and manuscripts, not foundation-model weights | progressive agentic tree search followed by human portfolio selection | three selected manuscripts entered an ICLR-workshop experiment; one scored 6, 6, and 7 (mean 6.33/10), while two were rejected | supplies the theme, selects three ideas from roughly forty, allocates multiple runs, and selects the strongest complete outputs | independent workshop review of selected outputs; under the prearranged protocol, the authors withdrew the potentially accepted paper | an autonomous success frequency, main-conference-quality research closure, or successor-model improvement |

: Observed bounded self-improvement and automated-research systems. [View data](../outputs/integrated/tables/observed_precursor_telemetry.csv){.artifact-link data-artifact="outputs/integrated/tables/observed_precursor_telemetry.csv"}. {#tbl-observed-self-improvement}

These are observed, bounded precursors—not evidence that verified AI-R&D
closure, recurrent successor-model improvement, or any milestone time in this
article has been reached. `autoresearch` contributes candidate throughput and
a narrow accept/reject gate; DGM contributes self-modification, lineage/archive
memory, transfer tests, and direct evidence of evaluator gaming; AI
Scientist-v2 covers more of the research workflow but retains human
meta-selection. The non-monotone DGM lineage is especially important:
industrial memory should preserve provenance-linked branches and failed
stepping stones rather than assume a single improving lineage. Because the
tasks, budgets, evaluators, interventions, and success units are not
commensurable, none of the reported values calibrates
$\nu_{\mathrm{verified}}$, $\mathbb E[\mathbf G_n]$, or
$T_{\mathrm{AIR\&D}}$. The generated
[observed-precursor telemetry register](../outputs/integrated/tables/observed_precursor_telemetry.csv){.artifact-link data-artifact="outputs/integrated/tables/observed_precursor_telemetry.csv"}
keeps unavailable attempt, retention, elapsed-compute, and independence
fields blank rather than converting absence into a favorable value.

Sakana AI's 2026 RSI Lab announcement proposes a future loop in which
Agent-Native Models power an AI Scientist that builds better Agent-Native
Models [S89]. That is a declared strategy and intended transition. It becomes
closure evidence only after a versioned model-to-research-to-successor-model
cycle records candidate and retained counts, independent evaluation, safe
deployment, and recurrence.

### Closure and milestone taxonomy {#closure-and-milestone-taxonomy}

Three different closure claims must be tested independently:

| closure | operational gate | what it does not imply |
|---|---|---|
| verified AI-R&D closure | a system proposes, tests, independently evaluates, and safely deploys accepted changes to successors | physical task execution or capital reproduction |
| embodied-production closure | controllers complete the active industrial minimum cut with available sensing, actuation, experiments, and recovery | successor-model improvement or replacement of every indispensable machine |
| reproductive-capital closure | the system replaces and expands every indispensable capital stock after depreciation and obsolescence | open-ended AI improvement or legitimate authorization |

: Distinct operational closure gates. {#tbl-closure-taxonomy}

Their milestone times are $T_{\mathrm{AIR\&D}}$, $T_{\mathrm{emb}}$,
$T_{\mathrm{cl},E}$, $T_{\mathrm{cl},S}$, and $T_{\mathrm{ctrl}}$:
verified AI-R&D closure, adequate embodiment, terrestrial reproductive
closure, off-world reproductive closure, and control readiness,
respectively. “Control readiness” means independent verification,
authorization, secure command, audit, and stop capacity adequate for the
corresponding capability and replication rate. These are separate clocks,
not five names for a single takeoff event.

The distinction creates a 2×2 causal map:

| | production not reproductively closed | production reproductively closed |
|---|---|---|
| verified AI-R&D loop absent | externally supplied capital with bounded technical progress | endogenous physical growth with a bounded controller |
| verified AI-R&D loop active | digital improvement bottlenecked by externally supplied capital | coupled recursive industrial intelligence |

: Coupling between verified AI-R&D and reproductive-production closure. {#tbl-coupled-closure-map}

The Moon–asteroid ablation makes Table [@tbl-coupled-closure-map]
executable. With the implemented
verified AI-R&D proxy frozen but new-capacity orders permitted, balanced
physical doubling occurs at 36.75 years and the system reaches 2.71
cell-equivalents at year 40. With both channels active, it doubles at 35.25
years and reaches 3.28. Either row with capital reproduction blocked fails to
double and depreciates to 0.0015 balanced equivalents by year 40. The
AI-R&D switch is a stylized verified capability-growth channel, not evidence
that full research closure exists. Machine-readable:
[closure loop ablation matrix](../outputs/integrated/tables/closure_loop_ablation_matrix.csv){.artifact-link data-artifact="outputs/integrated/tables/closure_loop_ablation_matrix.csv"}.

Mapped to the canonical proposition ladder through the six semantic links
below, the closure dependencies are:

| proposition | abbreviated claim | closure premise or evidence |
|---|---|---|
| [P1 — Conceptual possibility](proposition:P1){.proposition-ref} | logical coherence of recursive industrial expansion | no demonstrated closure required |
| [P2 — Technical feasibility](proposition:P2){.proposition-ref} | eventual complete-system feasibility | embodied-production and reproductive-capital closure; verified AI-R&D closure is an accelerator, not a logical prerequisite |
| [P3a — Earth-dependent bridge economics](proposition:P3a){.proposition-ref} | operating economics while Earth inputs remain load-bearing | compares an Earth-dependent regime; no AI-R&D closure premise |
| [P3b — Mature high-closure economics](proposition:P3b){.proposition-ref} | stipulated mature high-physical-closure economics | assumes a declared high-physical-closure regime but does not require AI-R&D closure |
| [P4a — Documented portfolio direction](proposition:P4a){.proposition-ref} | observed program direction | documented initiatives and integration evidence; no closure proof |
| [P4b — Recursive-closure intent](proposition:P4b){.proposition-ref} | inferred intent to transition toward closure | closure-specific indicators of intent, not proof of achieved closure |

: Proposition-to-closure dependency map. {#tbl-proposition-closure-dependencies}

The external record supports pieces of this loop at very different evidence
levels. Table [@tbl-ai-rnd-evidence] keeps company self-evaluation, external evaluation,
framework thresholds and scenario assumptions visibly separate.

| source and version/date | construct | unit of evaluation | threshold or comparator | published result or status | article loop stage informed | what this does not establish |
|---|---|---|---|---|---|---|
| Anthropic operational account, 2025-09-17 [S81] | execution throughput versus research direction | reported internal coding and research workflow | prior human-led workflow | substantial assistance and fixed-goal execution reported; research taste remains human-led | implementation, experiment execution, debugging | audited productivity, autonomous successor design or closure |
| METR Time Horizon 1.1 [S83] | long-horizon software and research task completion | human-equivalent task duration at 50% success | skilled-human completion time | rising horizon on the tested distribution; the GPT-5.6 Sol estimate was not considered robust because of detected cheating [S98] | implementation, experiment execution, debugging, evaluation | delegation reliability, realized R&D acceleration, an automation fraction or physical transfer |
| RSI survey, arXiv v1, 2026-07-14 [S84] | taxonomy of self-improvement research | 1,250-paper corpus | two-axis classification | maps a young and rapidly changing literature | taxonomy across candidate loop stages | mature consensus or demonstrated open-ended improvement |
| *AI 2027*, June 2025 update [S80] | fast digital feedback scenario | forecast trajectory | authors' scenario counterfactual | explicit software/hardware and internal/public clocks | scenario structure across the loop | observed capability, its calendar or any measured multiplier |
| OpenAI Preparedness Framework v2, 2025-04-15 [S96] | AI Self-Improvement High and Critical thresholds | lab-wide assistant impact or generational improvement | 2024 research-engineer and AI-R&D baselines | High is assistant-equivalent acceleration; Critical includes superhuman research agency or sustained generational improvement in about one-fifth the 2024-equivalent time | four analytic gates, especially assistant capability and recursive closure | that a current model has crossed either threshold |
| PaperBench initial release, 2025-04-02 [S97] | AI-research replication | 20 ICML 2024 papers and 8,316 rubric items | author-developed rubric and a top-ML-PhD subset baseline | Claude 3.5 Sonnet (New) with the open-source scaffold averaged 21.0%, below the reported human baseline | hypothesis generation, implementation, execution, debugging, evaluation | research taste, frontier training, successor gain or recurrence |
| GPT-5.6 system card, 2026-07-09 [S98] | debugging, kernels, small pretraining, post-training, ML engineering and long-horizon work | six component evaluations with distinct budgets and harnesses | suite-specific baselines and Preparedness High | OpenAI assessed Sol, Terra and Luna below High as of July 2026 | multiple component stages and safety verification | no acceleration, no risk, general safety, broad automation or closure |
| DeepMind technical AGI-safety analysis, 2025-04-02 [S100] | automated-R&D positive feedback | conceptual mechanism under stated assumptions | more- versus less-than-proportional subsequent R&D output | treats the mechanism as plausible and safety-relevant | research-to-successor feedback | a realized loop, a timeline, safe recurrence or physical closure |
| DeepMind Frontier Safety Framework 3.1, 2026-04-17 [S101] | realized ML-R&D acceleration and broad ML-R&D automation | organization-level progress or team-equivalent work | historical progress rates or comparable all-inclusive team cost | defines distinct capability levels; does not report either as reached | realized-acceleration and broad-automation gates | verified safe-successor deployment or recurring closure |

: Cross-lab AI-R&D evidence and its bounded interpretation. [View data](../outputs/integrated/tables/ai_rnd_benchmark_registry.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rnd_benchmark_registry.csv"}. {#tbl-ai-rnd-evidence}

The comparison is intentionally not a score ranking. Anthropic supplies an
operational self-report and makes the execution-versus-direction gap concrete;
METR supplies independent task-horizon measurements; *AI 2027* supplies a
fast-digital scenario rather than observed evidence; OpenAI publishes
AI-self-improvement thresholds plus component and end-to-end AI-R&D
evaluations; and Google DeepMind separates realized R&D acceleration from
broad R&D automation while locating capability in models integrated with
workflows. The benchmark, harness, compute, tool, scaffold, human and
evaluation boundaries are therefore part of every observation, not optional
metadata.

OpenAI's High threshold is comparable to giving every OpenAI researcher a
strong mid-career research-engineer assistant relative to a 2024 baseline.
Its Critical threshold instead covers a superhuman research-scientist agent
or sustained generational improvement in roughly one-fifth of the
2024-equivalent wall-clock time [S96]. High is an assistant/acceleration
threshold, not loop closure. PaperBench is an AI-research-replication
benchmark—not a recursive-improvement benchmark. Its initial release asks
agents to reproduce 20 ICML 2024 Spotlight or Oral papers from scratch
against 8,316 author-developed rubric items. The best tested configuration,
Claude 3.5 Sonnet (New) with the released open-source scaffold, averaged
21.0% and remained below the reported top-ML-PhD subset baseline [S97].

The July 9, 2026 GPT-5.6 card decomposes OpenAI's current evaluation suite:
41 real internal research-code bugs plus six alignment-auditing tasks;
KernelGen 1P correctness and non-gamed latency improvement; NanoGPT
pretraining-loop improvement on one H100; PostTrainBench Lite over twelve
model-task combinations with one H100, internet and five hours; MLE-Bench
Revised over 72 Kaggle-style problems; and METR Time Horizon 1.1, run by the
external evaluator [S98]. The internal tasks and some rubrics are only partly
auditable. Benchmark saturation, unsolvable items, contamination, invalid
shortcuts, scaffolding dependence, evaluator validity and the gap between
small-scale tasks and frontier training remain load-bearing qualifications.
METR's GPT-5.6 observation appears once in the registry with both source
references; it is not counted again as independent OpenAI evidence.

DeepMind's technical safety analysis supplies conceptual support for the
positive-feedback mechanism while labeling its paradigm, timeline and
continuity premises as assumptions and leaving some superintelligence
questions outside its scope [S100]. Frontier Safety Framework 3.1 then keeps
two different thresholds separate. “ML R&D acceleration level 1” is a
lagging outcome: systems have actually accelerated AI progress substantially
beyond historical rates. “ML R&D automation level 1” is a capability and
economic-substitution threshold: a system can automate any Google
AI-capabilities research team's work at approximately comparable
all-inclusive cost [S101]. DeepMind expects acceleration from systems of
models integrated into workflows, not a model in isolation, and separately
governs external release and high-risk internal deployment. This reinforces
the article's split between internal capability and public observation
without treating internal use as automatically safe.

Across the record, frontier labs increasingly treat AI-enabled R&D as
measurable and safety-relevant, and public evaluations show meaningful
performance on several component tasks. No cited public source demonstrates
a verified, recurring, end-to-end successor-model loop. OpenAI's Critical
threshold helps operationalize that endpoint and DeepMind's feedback account
supports the mechanism; neither establishes embodied-production or
reproductive-capital closure. The normalized evidence boundaries are
available in the [benchmark registry](../outputs/integrated/tables/ai_rnd_benchmark_registry.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rnd_benchmark_registry.csv"}
and [stage/gate crosswalk](../outputs/integrated/tables/ai_rnd_evidence_crosswalk.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rnd_evidence_crosswalk.csv"}.

The Anthropic figures remain `company_statement`: selection, attribution,
counterfactual, and same-family evaluator bias are unresolved, so code share
or lines of code cannot become a capability-growth coefficient. METR's own
limitations are equally load-bearing: its time horizon is serial human labor
replaced at a stated reliability level, differs sharply by domain, is not
a delegation threshold, and does not determine human intervention or
research uplift. The July 2026 survey is arXiv v1; 74% of its papers were
posted in 2026, classification used one annotator, and the authors disclose
recency bias, peripheral-query bleed, and lab-publication censoring [S84].
It maps a moving field rather than certifying closure.

Indexing candidate-improvement attempts by $n$ and public-release events by
$r$, the resource-constrained internal update and public observation are

::: {#eq:digital-capability-update .equation}
$$
\begin{aligned}
\mathbf I^{\mathrm{int}}_{n+1}
&=\mathbf I^{\mathrm{int}}_n
+z^{\mathrm{tech}}_n z^{\mathrm{int}}_n\,\mathbf G_n
 \!\left(\mathbf I^{\mathrm{int}}_n,\mathcal D_n,\mathcal A_n,
 C_{\mathrm{eff},n},\mathcal V_n\right),\\
\mathbf I^{\mathrm{pub}}_{r+1}
&=\mathbf R_r\!\left(
\mathbf I^{\mathrm{int}}_{\tau(r)};
z^{\mathrm{pub}}_r,\mathcal E^{\mathrm{pub}}_r
\right).
\end{aligned}
$$
:::

Here $\mathbf I^{\mathrm{int}}_n$ and $\mathbf I^{\mathrm{pub}}_r$ are vectors
of internally available and publicly observable task-relevant capability.
$z^{\mathrm{tech}}_n$ records whether the candidate is a genuine validated
gain rather than noise, leakage, reward hacking, or regression;
$z^{\mathrm{int}}_n$ records authorization for the claimed bounded internal
role; and $z^{\mathrm{pub}}_r$ records external/public authorization. All
three are binary conceptual indicators, not estimated probabilities.
$\mathbf G_n$ is the observed vector gain and depends on the current data
state $\mathcal D_n$, architecture and algorithm state $\mathcal A_n$,
effective training effort $C_{\mathrm{eff},n}$, and technical-verification
regime $\mathcal V_n$. The release mapping $\mathbf R_r$ exposes the internal
state selected by $\tau(r)$ under the public evidence and exposure conditions
$\mathcal E^{\mathrm{pub}}_r$; it can lag, narrow, or differently optimize the
public capability slice. The equation therefore does not require componentwise
nesting in every product, although the implemented illustrative branches use
nested slices. Components retain their own units or normalized scales; this
paper does not collapse loss, benchmark scores, parameter count, and physical
productivity into one scalar “intelligence.”

Within a stable architecture, dataset, objective, and evaluation regime, a
useful sensitivity model for capability component $m$ is a saturating
frontier,

::: {#eq:digital-saturating-frontier .equation}
$$
I_m(C_{\mathrm{eff}})
= I_{m,0}
+ A_m\!\left[
1-\left(1+\frac{C_{\mathrm{eff}}}{C_{m,0}}\right)^{-\beta_m}
\right].
$$
:::

In Eq. [@eq:digital-saturating-frontier], $I_m$ is held-out performance on
capability component $m$; $C_{\mathrm{eff}}\ge0$ is cumulative effective
training or search effort in equivalent useful FLOP; $I_{m,0}$ is starting
performance; $A_m\ge0$ is the regime-specific attainable improvement;
$C_{m,0}>0$ is a scale constant in the same units as $C_{\mathrm{eff}}$; and
$\beta_m>0$ controls curvature. The imposed shape has
$\partial I_m/\partial C_{\mathrm{eff}}>0$ and
$\partial^2 I_m/\partial C_{\mathrm{eff}}^2<0$: more effective effort helps,
but each additional unit helps less. This is an **ASSUMPTION-class sensitivity
form**, not an empirical law of RSI. It makes diminishing marginal gain a
function of cumulative effort rather than calendar time. The analysis retains three
regimes: a power-law-like smooth decline over the observed range; the
saturating case above; and a piecewise frontier in which a discrete
architecture, algorithm, data, post-training, tool-use, or test-time-compute
innovation changes $(A_m,C_{m,0},\beta_m)$ after paying its own search and
verification cost.

Training compute is not itself effective effort. For a fixed held-out target,
the accounting identity used here is

::: {#eq:effective-training-compute .equation}
$$
C_{\mathrm{eff}}
= C_{\mathrm{train}}\,
\eta_{\mathrm{hw}}\eta_{\mathrm{util}}
\eta_{\mathrm{alg}}\eta_{\mathrm{arch}},
\qquad
C_{\mathrm{train}}\simeq k_{\mathrm{train}}N_{\mathrm{act}}D.
$$
:::

$C_{\mathrm{train}}$ is realized training compute in FLOP;
$N_{\mathrm{act}}$ is the mean number of parameters activated per token; $D$
is the number of training tokens after deduplication and filtering; and
$k_{\mathrm{train}}$ is an operation-count coefficient fixed by the training
procedure. The dimensionless factors $\eta_{\mathrm{hw}}$,
$\eta_{\mathrm{util}}$, $\eta_{\mathrm{alg}}$, and
$\eta_{\mathrm{arch}}$ measure, respectively, hardware efficiency, realized
utilization after memory/interconnect/restart losses, algorithmic efficiency,
and architecture efficiency relative to a named baseline at the same held-out
target. They are comparative measurements, not free multipliers. Peak FLOP/s,
FLOP/J, memory traffic, communication overhead, power, cooling, and wall-clock
duration determine the first two; compute or data required to reach a fixed
score determines the latter two.

Those hours also have mutually exclusive uses. The annual allocation model
partitions physical accelerator time among successor training, inference for
research agents, research experiments, data generation and filtering,
verification and safety, and external productive service:

::: {#eq:ai-rd-compute-allocation .equation}
$$
\begin{aligned}
\sum_{s\in\mathcal S_C} C_s^{\mathrm{phys}}
&=C_{\mathrm{tot}}^{\mathrm{phys}},
\qquad
C_s^{\mathrm{eff}}=\eta_s C_s^{\mathrm{phys}},\\
R_{\mathrm{eff}}
&=\min\!\left\{
\frac{C_{\mathrm{inf}}^{\mathrm{phys}}}{c_R},
U_R
\right\},\\
\nu_{\mathrm{verified}}
&=\min\!\left\{
\rho_R R_{\mathrm{eff}},
\frac{C_{\mathrm{exp}}^{\mathrm{eff}}}{c_{\mathrm{exp}}},
\frac{y_D C_{\mathrm{data}}^{\mathrm{phys}}}{c_D},
\frac{q_V C_{\mathrm{ver}}^{\mathrm{phys}}}{c_V},
\frac{1}{\tau_{\mathrm{serial}}}
\right\}.
\end{aligned}
$$
:::

$\mathcal S_C$ is the six-use partition; $C_{\mathrm{tot}}^{\mathrm{phys}}$
is the conserved physical accelerator-hour budget; $C_s^{\mathrm{phys}}$ and
$C_s^{\mathrm{eff}}$ are physical and effective hours for use $s$; and
$\eta_s$ is its declared efficiency conversion. $R_{\mathrm{eff}}$ is the
effective automated-researcher count, limited by inference hours per instance
$c_R$ and useful research tasks $U_R$. $\rho_R$ is candidate output per
effective researcher. The remaining rates are experiment compute
$C_{\mathrm{exp}}^{\mathrm{eff}}/c_{\mathrm{exp}}$, accepted-data signal
$y_D C_{\mathrm{data}}^{\mathrm{phys}}/c_D$, independent verification
$q_V C_{\mathrm{ver}}^{\mathrm{phys}}/c_V$, and the inverse serial
experiment-cycle floor $1/\tau_{\mathrm{serial}}$. Algorithmic improvement
changes $\eta_s$; it does not enlarge
$C_{\mathrm{tot}}^{\mathrm{phys}}$.

At the central efficiency setting, the 5%-grid raw-capability optimizer
allocates 25%, 35%, 20%, 15%, 0%, and 5% to the six uses. It reports 35 raw
candidate units/year but zero verified progress because it reserves no
verification compute. The verified-progress optimizer allocates 20%, 30%,
15%, 15%, 15%, and 5%, producing 30 verified units/year while foregoing
$1.9 million of the illustrative all-service revenue account. The
physical-growth score assigns all hours to current external productive
service and produces no research progress. Raising the effective-compute
conversion from 0.75 to 1.50 increases the best verified rate from 25 to 35
without changing the one-million-hour physical budget. These are
ASSUMPTION-class allocation comparisons, not organizational prescriptions;
no scenario share is imported from a narrative forecast. Machine-readable:
[AI R&D compute allocation](../outputs/integrated/tables/ai_rd_compute_allocation.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rd_compute_allocation.csv"}.

Empirical language-model scaling laws show diminishing loss improvements with
model size, data, and compute, while the Chinchilla experiments show that
compute-optimal training requires joint allocation between model size and
training tokens [S58] [S59]. These are evidence about loss in observed model
families, not evidence that a scalar intelligence must keep rising or that RSI
is active. Architecture also changes the resource surface: selective
state-space models trade attention’s sequence-length behavior for different
hardware kernels, while sparsely activated mixture-of-experts models separate
total from active parameters but add routing, load-balancing, communication,
and stability costs [S60] [S61]. “Transformer versus Mamba” and “dense versus
sparse” therefore name sensitivity branches, not universal efficiency
rankings. Observed algorithmic progress at fixed performance can shift the
frontier, but its historical rate cannot be extrapolated unchanged into
autonomous research [S26].

The implemented attribution screen therefore avoids fitting one historical
headline rate. It gives compute, data, model-size, hardware, algorithm, and
architecture elasticities separate low/central/high **ASSUMPTION** bounds and
retains a declared positive-semidefinite correlation matrix among them.
A companion log-additive accounting sensitivity freezes compute, data,
hardware, algorithm, or architecture progress one at a time. Under the
illustrative annual channel rates, the full annual multiplier is 1.821; the
one-channel counterfactuals range from 1.543 when compute is frozen to 1.686
when architecture is frozen. Those numbers are neither a causal
decomposition nor a forecast—they expose how much of the assumed composite
rate was assigned to each channel. The exact bounds, correlations, and
freezes are in [digital elasticity bounds](../outputs/integrated/tables/digital_elasticity_bounds.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_elasticity_bounds.csv"} and
[digital channel ablations](../outputs/integrated/tables/digital_channel_ablations.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_channel_ablations.csv"}.

A chronological release backtest provides a deliberately narrow external
screen. The split was fixed before fitting: GPT-3, Gopher, Chinchilla, and
PaLM releases from 2020–2022 form the training set [S59] [S72]; LLaMA and
Llama 2 releases from 2023 form the validation set [S73] [S74]; and Llama 3.1
70B is the 2024 holdout [S75]. Every observation is a base pretrained dense
model evaluated on five-shot MMLU. The candidate relation is

::: {#eq:chronological-release-backtest .equation}
$$
\begin{aligned}
\operatorname{logit}(p_i)
&=\beta_0+\beta_C\log_{10}\!\left(\frac{6N_iD_i}{C_{\mathrm{ref}}}\right)
+\beta_B\log_{10}(b_i),
\\
p_i&=\frac{M_i-25}{100-25},
\qquad
b_i=\min\!\left\{
\frac{D_i}{20N_i},\frac{20N_i}{D_i}
\right\}.
\end{aligned}
$$
:::

Here $M_i$ is release $i$'s five-shot MMLU accuracy in percentage points;
$p_i$ is its chance-adjusted score; $N_i$ and $D_i$ are dense parameter and
pretraining-token counts; $6N_iD_i$ is a training-FLOP proxy;
$C_{\mathrm{ref}}=10^{23}$ FLOP fixes the log scale; $b_i\in(0,1]$ measures
distance from the declared Chinchilla-style allocation of 20 tokens per
parameter; and $\beta_0,\beta_C,\beta_B$ are fitted only on the four training
observations. The compute-only comparison sets $\beta_B=0$.

The compute-only relation has 6.64 percentage-point mean absolute error on
the two 2023 validation releases and 1.48 points on the single 2024 holdout.
Including the declared data-balance term reduces 2023 validation error to
0.99 points but gives 1.71 points on the holdout. The holdout token input is
the published lower bound of 15 trillion tokens, not an exact training count.
These results are too small, family-confounded, and protocol-sensitive to
calibrate capability growth: the apparent validation benefit does not improve
the one-observation holdout. The coefficients therefore remain a
retrospective screen and do not enter the recursive-loop dynamics. The
release rows, source locators, fitted coefficients, and split errors are in
[digital release backtest table](../outputs/integrated/tables/digital_release_backtest.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_release_backtest.csv"} and
[digital release backtest summary](../outputs/integrated/tables/digital_release_backtest_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_release_backtest_summary.csv"}.

Calendar speed is a separate quantity. Let $\nu_v(t)$ be verified loops per
elapsed calendar year at time $t$. It is constrained by the slowest required
stage:

::: {#eq:verified-loop-bottleneck .equation}
$$
\nu_v(t)=\min\!\left\{
\nu_{\mathrm{train}},\nu_{\mathrm{data}},\nu_{\mathrm{experiment}},
\nu_{\mathrm{evaluate}},\nu_{\mathrm{safety}},
\nu_{\mathrm{deploy}},\nu_{\mathrm{observe}}
\right\}.
$$
:::

Each $\nu_{\cdot}$ is stage capacity in completed-loop equivalents per year.
The training stage is itself limited by model and active-parameter size,
tokens, context length, memory capacity and bandwidth, accelerator
interconnect, parallelism efficiency, power, cooling, wall-clock training
time, failures, and restart policy. The experiment and observation stages
also impose irreducible physical time. Multiplying throughput by conditional
gain gives a rate without resurrecting constant $G$:

::: {#eq:digital-capability-rate .equation}
$$
\frac{\mathrm d\mathbf I}{\mathrm dt}
=\nu_v(t)\,
\mathbb E\!\left[\mathbf G_n\mid
\mathbf I(t),\mathcal D(t),\mathcal A(t),\mathcal V(t)\right].
$$
:::

In Equation [@eq:digital-capability-rate], $t$ is elapsed calendar time in
years and the conditional expectation averages heterogeneous successes,
failures, and regressions in a declared regime. Higher capability may improve
coding, architecture search, synthetic-data generation, hardware design,
factory scheduling, scientific modeling, and evaluation design, but the
result is bounded by Eq. [@eq:verified-loop-bottleneck] and by the frontier
being approached. Superlinear, linear, logarithmic, and saturating trajectories
remain hypotheses to distinguish with completed-loop telemetry.

The period ledger makes the bottleneck visible rather than reporting only
$\nu_v$. In the declared 0–7 year baseline, observation binds at 2 verified
loops/year while progress moves along the fixed scaling curve. The year-7
frontier event is followed by a safety-limited 3 loops/year during years
7–14; after the year-14 frontier event, experiment throughput binds at 4
loops/year through year 20. These are scenario mechanics, not forecasts.
[digital loop bottlenecks](../outputs/integrated/tables/digital_loop_bottlenecks.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_loop_bottlenecks.csv"} records every stage
rate and distinguishes movement along a curve from a discrete frontier shift.

Verification is not one fungible stage. For verifier class $k$,

::: {#eq:verification-hierarchy .equation}
$$
\begin{aligned}
\nu_{v,k}
&=\min\{\nu_{\mathrm{candidate},k},\nu_{\mathrm{capacity},k}\}
\,y_k(1-f_k)q_k,\\
\nu_{\mathrm{licensed},k}
&=\min\{\nu_{v,k},\nu_{\mathrm{direction}},
\nu_{\mathrm{execution}}\}.
\end{aligned}
$$
:::

$\nu_{v,k}$ is independently supported throughput for class $k$;
$\nu_{\mathrm{candidate},k}$ and $\nu_{\mathrm{capacity},k}$ are candidate
and verifier capacity; $y_k$ is acceptance yield; $f_k$ is false-positive
fraction; and $q_k$ is evaluator independence across model lineage, training
data, tools, authority, and audit access. $\nu_{\mathrm{licensed},k}$ is
licensed loop throughput, additionally bounded by research direction-setting
$\nu_{\mathrm{direction}}$ and fixed-target execution
$\nu_{\mathrm{execution}}$. The six classes are reported separately, from
formal/executable invariants and destructive physical acceptance tests
through independent held-out experiments, causal operational outcomes,
human/AI rubrics, and model self-assessment. They are not added into a
universal “verified-equivalent” total.

The limiting test gives the self-assessing producer zero independence by
definition: 1,000 self-scored iterations do not become independent evidence,
whereas one destructive physical test can license its narrow physical claim.
Stress rows separately apply evaluator drift, reward hacking,
self-confirming selection, evaluator-diversity collapse, and synthetic-data
model collapse. In the self-confirming case, preserving all positive records
but only 10% of negative and 5% of null records raises the apparent positive
share from 0.10 to 0.625 without improving the underlying record. This is the
survivorship-bias failure the industrial-memory pipeline must prevent.
Machine-readable:
[verification hierarchy table](../outputs/integrated/tables/verification_hierarchy.csv){.artifact-link data-artifact="outputs/integrated/tables/verification_hierarchy.csv"}.

Operational experience closes the loop only if it survives deployment and is
converted into a verified change. A durable learning record binds
observations, actions, outcomes, task and hardware state, environment,
model/controller version, human intervention, timestamps, and provenance.
It retains failures, near misses, null results, unsuccessful recoveries, and
negative experiments as well as successes. The versioned pipeline is:
ingestion; integrity and access checks; episode construction; causal
attribution with uncertainty; replay or simulation; conversion into a
procedure, controller, retrieval item, or training example; held-out
evaluation; staged deployment; monitoring; and rollback. Temporary context,
persistent retrieval within one generation, revised recipes or control
policies, offline post-training, and transfer into a successor generation are
five distinct mechanisms. Continuous weight updates are unnecessary, but a
later generation must be able to trace every accepted lesson back to evidence
and every rejected lesson to its gate. Learning yield and latency—not bytes
stored—are the relevant outputs.

The synthetic intergenerational rehearsal makes that condition executable
without pretending that the physical campaign has occurred. Four fault
families—sensor bias, actuator stiction, calibration shift, and
communications partition—each have a training case and a structurally
similar hidden transfer case. Across four controller generations, the hidden
case is never exposed to training; the output records learning latency,
retention, transfer success, recurrence, recovery time, verification compute,
and regression on earlier tasks. A post-update row passes only if transfer
and retention exceed their preregistered gates and prior-task regression
stays below its gate. [intergenerational learning faults](../outputs/integrated/tables/intergenerational_learning_faults.csv){.artifact-link data-artifact="outputs/integrated/tables/intergenerational_learning_faults.csv"} carries the
complete split and result record with
`evidence_status=synthetic_protocol_execution`; it does not replace the
execution-pending terrestrial rehearsal.

Those observed synthetic metrics feed the digital loop rather than remaining
a disconnected dashboard. Median event-to-deployment latency caps observation
and deployment rates; verification compute per fault family caps evaluation
and safety throughput; and retention, hidden-case transfer, and non-recurrence
multiply into the technical-validation fraction for retained learning.
[digital learning feedback table](../outputs/integrated/tables/digital_learning_feedback.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_learning_feedback.csv"}
compares the unadjusted assumption case with that constrained case. In the
declared synthetic campaign, median latency is 183 days, mean retained lesson
strength is 0.804, mean hidden-case transfer is 0.846, mean recurrence is
0.088, and mean verification cost is 1,312.5 compute-hours per family and
generation. Evaluation/safety capacity then limits verified throughput to
1.524 loops/year, the combined technical-validation fraction is 0.620, and year-20
capability is 1.480 rather than the unadjusted 1.765. The
connection demonstrates data flow and prevents instantaneous learning; only
physical rehearsal measurements can replace the synthetic inputs.

Synthetic volume and accepted signal are also separate states. For generation
$g$, the sensitivity records

::: {#eq:accepted-training-signal .equation}
$$
S_g
=V_g^{\mathrm{syn}}(1-d_g)y_g p_g(1-e_g)D_g
+N_g^{\mathrm{phys}}c_g(1-e_g).
$$
:::

$S_g$ is accepted training-signal units; $V_g^{\mathrm{syn}}$ is generated
synthetic records; $d_g$ is deduplication fraction; $y_g$ is filtering
acceptance; $p_g$ is valid provenance; $e_g$ is evaluator error; $D_g$ is
data-diversity retention; $N_g^{\mathrm{phys}}$ is the number of
resource-limited physical episodes; and $c_g$ is their causal-linkage
fraction across state, action, outcome, and hardware configuration.
Physical episodes are capped independently by experiment time, equipment
wear, destructive samples, and verification capacity.

The volume-maximizing branch expands from 1,000 to 2.187 million synthetic
records by generation 7 and raises its apparent-progress index above the
governed branch. Yet evaluator error rises to 0.643, bias to 0.582, diversity
falls to 0.350, and held-out transfer falls to 0.626 versus 6.993 in the
governed branch. More generated data can therefore create stronger apparent
progress and weaker transfer. A third branch applies open publication,
espionage, employee mobility, distillation, and independent replication to
the proprietary-data state; its advantage index falls to 0.003 versus 0.255
under the lower-leakage branch. These are scenario mechanics, not leakage
estimates. Machine-readable:
[data evaluator coevolution table](../outputs/integrated/tables/data_evaluator_coevolution.csv){.artifact-link data-artifact="outputs/integrated/tables/data_evaluator_coevolution.csv"}.

Public releases are lagging indicators: benchmarks, open weights, products,
and launches observe the public frontier, not necessarily the latent internal
frontier. An organization can obtain research, engineering, operational, and
successor-training benefits from a validated change in a bounded internal role
before completing broader assurance for heterogeneous users, uncontrolled
distribution, external misuse, legal exposure, and unfamiliar environments.
Release cadence can therefore understate the feedback-loop speed that matters
to this thesis. Internal use is not gate-free: technical validation must
reject noise, evaluator leakage, reward hacking, and regression, while
risk-based authorization must match consequence, authority, reversibility,
containment, and privileged access. Advice with human execution and rollback
can be authorized earlier than autonomous authority; live infrastructure,
physical actuation, destructive experiments, cyber or biological work,
weight modification, and successor training can require stringent controls
even when wholly internal.

The internal frontier is only partially observable. Relevant indirect
observations include internal task productivity, experiment throughput,
code or research contribution, training cadence, inference use, access tiers,
staged deployment, and later disclosure of prerelease performance. None is a
direct overhang measurement. A long release interval may instead reflect
assurance, product strategy, compute scheduling, integration, regulation, or
weak results; secrecy and capability are different variables. The implemented
zero-lag, slower-publication, and internal-overhang cases are consequently
**ASSUMPTION** sensitivities, with separate experiment, technical-validation,
internal-adoption, and public-release clocks:
[internal/public capability trajectories](../outputs/integrated/tables/internal_public_capability_trajectories.csv){.artifact-link data-artifact="outputs/integrated/tables/internal_public_capability_trajectories.csv"}.
The nested public slices in those three cases are illustrative, not a claim
that every public product is componentwise weaker than every internal system.
*AI 2027* distinguishes in-house deployment from external exposure and task
performance from honest oversight [S80]; that scenario motivates the state
separation but supplies no numerical lag parameter. Part III.4 attaches the
three gates to their distinct hazards.

### Gross capability is not authorized capacity {#gross-capability-is-not-authorized-capacity}

The control state is deliberately not one “intelligence” scalar. It records
task capability $I_{\mathrm{task}}$, coordination capability
$I_{\mathrm{coord}}$, evaluator capability $I_{\mathrm{eval}}$, and
controllability confidence $p_{\mathrm{ctrl}}$ separately. For
high-consequence physical actions, gross production becomes authorized
operating capacity only at the slowest required control channel:

::: {#eq:authorized-capacity-control .equation}
$$
\begin{aligned}
\dot K_{\mathrm{auth}}(t)
&=\frac{1}{a_K}\min\!\left\{
 a_K\dot K_{\mathrm{gross}}^{+}(t),
 V_{\mathrm{rel}}(t),V_{\mathrm{adv}}(t),C_{\mathrm{cmd}}(t),
 E_{\mathrm{env}}(t),L_{\mathrm{treaty}}(t),H_{\mathrm{human}}(t)
\right\},\\
K_{\mathrm{unauth}}(t)
&=\max\!\left\{K_{\mathrm{gross}}(t)-K_{\mathrm{auth}}(t),0\right\}.
\end{aligned}
$$
:::

$K_{\mathrm{gross}}$, $K_{\mathrm{auth}}$, and $K_{\mathrm{unauth}}$ are
gross, authorized, and unauthorized capacity; $\dot
K_{\mathrm{gross}}^{+}$ is the proposed positive capacity-addition rate; and
$a_K$ is the number of high-impact authorization actions required per unit
of added capacity. $V_{\mathrm{rel}}$ and $V_{\mathrm{adv}}$ are reliability
and independent adversarial-verification throughput;
$C_{\mathrm{cmd}}$ is secure-command throughput; $E_{\mathrm{env}}$ and
$L_{\mathrm{treaty}}$ are environmental and treaty limits; and
$H_{\mathrm{human}}$ is included only when human approval is required. The
minimum is a rate constraint, not a claim that these unlike quantities can
be substituted for one another.

Five ASSUMPTION-class stress cases make the distinction executable. In the
balanced case, gross and authorized capacity both reach 2.587 at year 12.
The verification-lag case reaches 97.017 gross but only 1.864 authorized
capacity; proposed actions exceed human comprehension from year zero, so a
nominal human signature would be ceremonial rather than substantive. A
matched monitor pair isolates common mode: independent monitors authorize
all 8.271 units, whereas shared lineage, data, tools, and observations leave
only 6.037 authorized despite the same gross trajectory. A final case is
limited by treaty throughput and authorizes only 1.600 of 6.571 gross units.
These are stress-test implications, not empirical forecasts. Machine-readable:
[authorized capacity control summary](../outputs/integrated/tables/authorized_capacity_control_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/authorized_capacity_control_summary.csv"} and
[authorized capacity control trajectory](../outputs/integrated/tables/authorized_capacity_control_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/authorized_capacity_control_trajectory.csv"}.

## I.2 Recursive industrial improvement: the physical loop {#i.2-recursive-industrial-improvement-the-physical-loop}

Digital intelligence depends on a physical substrate: chips, data centers,
electricity, cooling, networks, factories, labor, materials, logistics,
maintenance — a dependency inventory, not a sum; any term can bind. The
physical recursive loop begins when AI and robotics improve the production
of those inputs: better intelligence designs and operates better machines;
better machines expand energy and manufacturing; expanded industry produces
more compute; more compute supports better intelligence.

The loop does not require an indefinitely self-improving controller once
embodied production and reproductive capital are closed. A bounded controller
can operate a fixed productive recipe that replaces and expands its own
capital; verified AI-R&D then improves the rate or reachable designs rather
than creating the logical possibility of physical compounding.

Trammell and Korinek provide the closest formal economic lineage for that
split [S82]. In their aggregate framework, production automation can
accelerate growth when capital substitutes sufficiently for labor and can
self-replicate; the result also depends on saving relative to depreciation,
returns to scale, substitution, and fixed natural-resource factors.
Automating R&D accelerates the transformation but need not generate
explosive growth in isolation when research is weakly parallelizable or
retains serial and fixed-input constraints. Their capital stock is aggregate.
The balanced minimum-sector doubling test used here is stricter: every
indispensable sector must replace and expand, so a surplus of structures or
compute cannot compensate for a missing metrology, electronics, power, or
repair capability. The formal result is a conceptual cross-check, not proof
that this off-world engineering graph closes.

Intelligence is therefore one factor among complementary stocks: experiment
capacity, high-quality causal data, inference compute, embodiment, materials,
energy, deployment capacity, verification, legal authority, and human
consent. Its local physical return in regime $r$ is measured here by a finite
response with every named complement held fixed:

::: {#eq:marginal-intelligence-response .equation}
$$
\operatorname{MP}_{I}^{(r)}(T;\Delta I)
=
\frac{
K_r(T;I_{r,0}+\Delta I,\mathbf X_r)
-K_r(T;I_{r,0},\mathbf X_r)
}{\Delta I}.
$$
:::

$\operatorname{MP}_{I}^{(r)}$ is the change in balanced operating-capacity
units at horizon $T$ per capability-index unit; $K_r$ is the regime-$r$
operating-capacity endpoint; $I_{r,0}$ is its baseline capability;
$\Delta I>0$ is the declared perturbation; and $\mathbf X_r$ is the fixed
vector of complementary stocks and gates. The quotient is a local scenario
diagnostic, not a price, welfare measure, or universal production-function
coefficient.

This is also the transferable part of Amodei's “marginal returns to
intelligence” framework [S79]. His “country of geniuses in a datacenter”
assumes millions of copies operating 10–100 times faster; those quantities
remain scenario assumptions. The useful classification is the complement
set: outside-world speed, missing data, intrinsic complexity, human
constraints, and physical law. Intelligence can sometimes design around the
first four over time, but construction, observation, reaction, and
propagation still have elapsed-time costs, and physical law is not an
optimization target. The bottleneck-project sensitivity separates reducible
constraints, observation-time floors, physical floors, and
external-authority constraints accordingly.

Energy hardware is not energy: "with solar, energy equals hardware"
expresses a recursion, not an identity. Installed arrays generate power
that supports production of additional arrays; the system still pays in
materials, machine-hours, maintenance, and conversion losses. Robotic labor
is manufactured productive capacity: when robots participate in producing
factories, energy systems, and additional robots, labor becomes partially
reproducible, and the robot reproduction ratio must exceed one *after* depreciation, failures, and the equipment needed for high-complexity components — stated with the horizon and unit it requires, R_robot,T = discounted lifetime robot-equivalent capacity produced over T ÷ robot-equivalent capacity retired, consumed, or irreversibly committed over T, since a factory is not "consumed" merely because it helped build robots. In the long run the
decisive competitive variable — under the threshold-like, small-α branch of the capability model examined in II.5 — is not model quality but the doubling time of
productive hardware — and Part I.4 examines what that replication must
outrun.

**The intelligence–embodiment compatibility frontier.** The durable question
is two-sided: for task $k$, does the available embodiment expose enough
observable state and controllable action for a sufficiently capable
controller, and has intelligence actually reached the level required for that
particular hardware? RSI being active is not the same event as reaching that
level, and neither event proves that the system can design and manufacture a
better embodiment.

Let the embodiment vector $\mathbf E$ record degrees of freedom, workspace,
reach, payload, force, torque, compliance, dexterity, tool compatibility;
sensor modality, coverage, resolution, accuracy, sample rate, calibration and
occlusion; local servo and planning latency, jitter, bandwidth and compute;
precision, repeatability, stability and vibration; power, thermal margin, duty
cycle, mobility and environmental tolerance; interfaces and fixtures; and
fault detection, redundancy, safe states, maintainability and repairability.
Let $\mathbf R_k$ state task $k$'s requirements in the same dimensions. The
non-substitutable physical gate is

::: {#eq:embodiment-adequacy-gate .equation}
$$
A_k(\mathbf E,\mathbf R_k,\mathcal E)
=\prod_{p\in\mathcal P_k}
\mathbf 1\!\left[E_p(\mathcal E)\ge R_{k,p}\right],
\qquad A_k\in\{0,1\}.
$$
:::

Here $\mathcal E$ is the operating environment; $\mathcal P_k$ is the set of
hard physical, observability, controllability, safety, and process dimensions
for task $k$; and $\mathbf 1[\cdot]$ is one when its condition is true and zero
otherwise. The direction of a dimension is normalized so that higher is
adequate; maximum latency, vibration, or error limits are represented by
their signed margins. Failure of one hard gate cannot be averaged away by
excellent scores elsewhere.

Conditional on physical adequacy, the manuscript uses the following bounded
compatibility surface as an **ASSUMPTION-class** sensitivity form:

::: {#eq:intelligence-embodiment-compatibility .equation}
$$
S_k(I,\mathbf E,\mathbf R_k,\mathcal E)
=A_k\,S_{k,\max}(\mathbf E,\mathcal E)
\left[1-\exp\!\left(
-\left[\frac{I-I_{k,0}(\mathbf E)}{\sigma_k}\right]_+
\right)\right].
$$
:::

$S_k$ is a dimensionless verified task score, not a calibrated probability;
$S_{k,\max}\in[0,1]$ is the hardware-and-environment ceiling; $I$ is a
declared coordination, perception, planning, recovery, and tool-use
capability measure; $I_{k,0}(\mathbf E)$ is the onset level for that
embodiment; $\sigma_k>0$ is an intelligence scale; and
$[x]_+=\max(x,0)$. Increasing intelligence approaches but cannot exceed the
embodiment ceiling. Better sensing, standardized tool APIs, telemetry,
digital twins, fixtures, machine-readable interfaces, or actuators can raise
that ceiling and reduce the controller burden without adding generic
“intelligence.”

For a required verified score $\bar S_k$, define the embodiment-specific
threshold and its first-passage time by

::: {#eq:embodied-task-first-passage .equation}
$$
I_k^\ast(\mathbf E)
=\inf\{I:S_k(I,\mathbf E,\mathbf R_k,\mathcal E)\ge\bar S_k\},
\qquad
T_k^\ast
=\inf\{t:I(t)\ge I_k^\ast(\mathbf E)
\ \land\ V_k(t)=1\}.
$$
:::

$I_k^\ast$ is infinite when the embodiment cannot attain $\bar S_k$;
$T_k^\ast$ is elapsed years from the declared baseline; and $V_k(t)$ is the
independent task-verification gate. “Not reached within the modeled horizon”
is an outcome, not missing data. Higher intelligence means sufficiently high
intelligence for this task–embodiment pair after a potentially long sequence
of training, evaluation, failed loops, and deployments—not instant competence
when RSI begins.

In the limiting hypothesis, sufficiently capable intelligence can learn to
operate unfamiliar hardware *within* a physically adequate, observable, and
controllable envelope. It cannot infer state from absent sensors, supply
unavailable motion or force, defeat excessive latency, or exceed precision,
energy, reliability, or process limits. It may compensate by active
perception, planning, tool use, calibration, recovery, or multi-agent work,
but those consume time, energy, wear, risk, and capacity. Redesigning,
manufacturing, commissioning, and validating a better embodiment is a
separate physical loop; a versatile robot also does not replace a furnace,
vacuum chamber, cleanroom, or metrology stack. Present humanoid programs,
including Optimus, evidence an intended general-purpose form, not closure of
the unscripted diagnosis, construction, repair, recovery, and verification
task set.

The validation outputs test both causal directions independently. For every
declared industrial task,
[embodiment two direction sweep table](../outputs/integrated/tables/embodiment_two_direction_sweep.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_two_direction_sweep.csv"} holds the
hybrid embodiment fixed while sweeping intelligence, then holds intelligence
at 4.0 while scaling embodiment quality. The terrestrial rehearsal fault
matrix separately degrades sensors, actuators, calibration, communications,
tool familiarity, observability, and out-of-distribution tolerance. Hard-gate
failures remain `embodiment_limited` even at the high intelligence setting;
low scores with adequate hardware remain `intelligence_limited`.
[terrestrial rehearsal embodiment faults](../outputs/integrated/tables/terrestrial_rehearsal_embodiment_faults.csv){.artifact-link data-artifact="outputs/integrated/tables/terrestrial_rehearsal_embodiment_faults.csv"} records the failed dimensions
and score for all eight tasks. These are normalized **ASSUMPTION** tests; the
thresholds must be replaced with measured task, bill-of-material, and fault
logs before they support deployment claims.

Benchmark success is only the first rung of an industrial reliability ladder:
single attempt; repeated success; low-context long task; high-context
production task; safety-critical field task; unscripted recovery; and
sustained operation with bounded intervention. Each task row records duration,
consequence, verifier class, trials, reliability, prompting/checking time,
failure recovery and cleanup, rollback, out-of-distribution recovery, and
intervention events. Economic substitution requires both the task's rung and
its consequence-specific reliability threshold.

The limiting cases prevent a benchmark score from becoming a deployment
claim. A 50% success rate passes the single-attempt gate for cheap reversible
search. The configured 99.5% destructive-fabrication, 99.9% launch, 99.95%
critical-power, and 99.99% replication-authorization tasks all fail their
stricter reliability or rung requirements. A separate synthetic
commissioning row passes only because it supplies destructive physical
verification, unscripted recovery, 1,000 sustained operating hours, at most
two interventions per 100 tasks, and sufficient rollback and
out-of-distribution recovery. Rare failure can dominate labor: the launch
row has fewer interventions than production coding but more expected human
recovery/cleanup hours per task. Software task-duration trends are therefore
not extrapolated into mining, chemistry, maintenance, or commissioning.
Machine-readable:
[industrial reliability ladder table](../outputs/integrated/tables/industrial_reliability_ladder.csv){.artifact-link data-artifact="outputs/integrated/tables/industrial_reliability_ladder.csv"}.

This compatibility layer is not costless. The integrated seed and growth
graphs add six explicit hardware classes—sensors, actuators, end effectors,
modular spares, calibration equipment, and local controllers—to each
applicable sector's material bill and annual replacement-service demand.
[embodiment bill-of-materials requirements](../outputs/integrated/tables/embodiment_bom_requirements.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_bom_requirements.csv"} exposes every added coefficient and its
producer-sector dependency. These values are bounding assumptions pending a
task-resolved hardware inventory and terrestrial maintenance logs; their
purpose is to prevent adequate embodiment from entering the model as a free
capability.

The loops couple through a second channel: **data as the exhaust of the
physical loop**. Operating physical industry generates data that exists
nowhere else — test telemetry, process parameters, failure archives, fleet traces. It commoditizes less readily than public text, for four reasons: negative
results (the map of what does not work survives only in the archives of
whoever paid for the failures); sim-to-real ground truth (real telemetry is
the verification fuel for AI-proposed physical designs); legal fencing
(export-controlled data cannot lawfully enter open corpora — and equally
cannot feed publicly served models, so the strongest-moat data is
harvestable only in an internal, access-controlled variant); and temporal lead time (longitudinal data imposes a minimum calendar-time barrier to a like-for-like archive: a rival beginning today matches the sampling rate but cannot reproduce the historical intervention-and-outcome sequence retroactively, though capital compresses much of the disadvantage through acquisition, larger current fleets, accelerated and parallel experimentation, simulation, transfer learning, and newer processes that make the old archive less relevant [S34] — a lead-time barrier, not an impossibility). The
data-closure index κ_D is a direction-of-effort indicator, not a computable
ratio: its denominator is not measurable, and value depends on quality,
linkage, and integration, not origin. The honest caveat: proprietary
physical data is lead time, not permanence — any actor operating comparable
fleets and factories generates comparable exhaust, at national scale in
China's case.

The public record supplies two applications of the same supplemental-training
mechanism, which is evidence of an emerging pattern rather than proof of a
repeatable one. In July 2026, days after an in-house engineering model was
reported to have received a supplemental pass over the coding data of an
acquired developer-tools company, Musk said that the SpaceX engineering
corpus — excluding ITAR-controlled material — would enter supplemental
training of its roughly two-trillion-parameter successor [S11–S13]. The
relevant advantage is therefore not raw ownership alone:

::: {#eq:data-advantage-profile .equation}
$$
\mathbf d
=\left(
d_{\mathrm{unique}},d_{\mathrm{causal}},d_{\mathrm{coverage}},
d_{\mathrm{quality}},d_{\mathrm{access}},d_{\mathrm{integration}},
d_{\mathrm{verification}}
\right),
\qquad
\kappa_D=F(\mathbf d).
$$
:::

The primary output of Equation [@eq:data-advantage-profile] is the
seven-component profile $\mathbf d$, not the aggregate $\kappa_D$. Each
component is normalized to $[0,1]$, higher is better, and must be accompanied
by an uncertainty interval and evidence class:

| component | operational measurement |
|---|---|
| uniqueness | one minus the estimated fraction reproducible from lawful, contemporaneously available substitute corpora at matched cost |
| causal linkage | fraction of sampled episodes linking intervention, state, and outcome strongly enough for the declared causal-identification procedure |
| coverage | weighted fraction of the target task, environment, failure-mode, and operating-regime matrix represented above minimum sample support |
| quality | fraction passing declared integrity, calibration, labeling, timestamp, and contamination checks |
| access | fraction legally and technically usable by the named training or retrieval system at decision time |
| integration | fraction transformed into the versioned schema and retrievable within the required training or operational latency |
| verification | fraction whose proposed lesson survives held-out, counterfactual, safety, and regression tests |

: Operational components of the data-advantage vector. [View data](../outputs/integrated/tables/data_advantage_profile.csv){.artifact-link data-artifact="outputs/integrated/tables/data_advantage_profile.csv"}. {#tbl-data-advantage-components}

These fractions are measured on declared samples and weighting schemes, not
assumed from data ownership. Missing observations remain missing rather than
being imputed as average. Because inaccessible, causally unlinked,
unintegrated, or unverifiable records can have zero learning value, a
compensatory weighted sum is unsafe. If a scalar sensitivity is required, the
explicit **ASSUMPTION-class** candidate is

::: {#eq:data-advantage-scalarization .equation}
$$
\begin{aligned}
\kappa_D^{(\mathrm{assump})}
={}&
\mathbf 1[d_{\mathrm{access}}\ge a_{\min}]
\mathbf 1[d_{\mathrm{causal}}\ge c_{\min}]
\mathbf 1[d_{\mathrm{verification}}\ge v_{\min}]\\
&{}\times
\prod_{j\in\mathcal J_D} d_j^{\,w_j},
\\
w_j&\ge0,\quad \sum_{j\in\mathcal J_D}w_j=1.
\end{aligned}
$$
:::

Here $\mathcal J_D$ indexes the seven components; $w_j$ are declared
dimensionless weights; and $a_{\min}$, $c_{\min}$, and $v_{\min}$ are minimum
access, causal-linkage, and verification thresholds. The indicators impose
hard gates and the weighted geometric mean prevents a zero component from
being hidden by another. No empirical calibration for $F$, the weights, or
the gates is claimed; reported results must therefore retain $\mathbf d$ and
sweep alternative weights, gates, and missing-data assumptions.

Generation alone is insufficient. Telemetry creates an advantage only after
the industrial-memory pipeline defined in I.1 preserves provenance, attributes
cause with uncertainty, grants lawful access, integrates the record, and
transfers a lesson into a procedure, controller, retrieval system, current
model, or successor generation that passes held-out verification. Tesla's
first CIO has described building the custom Warp enterprise system in roughly
four months in 2012 after the company rejected off-the-shelf ERP, then
extending it continuously so operations could change without waiting on a
vendor [S15]. SpaceX independently built its own internal manufacturing and
enterprise system, Warp Drive [S16]. The convergence on the same
build-don't-buy pattern is evidence that iteration speed, not a common brand
name, drives the architecture.

Commentary describes the resulting ideal as a **unified build record** for
each produced unit: *as designed* (models and simulations), *as built*
(supplier batches, process settings, torques, and factory tests), and *as
deployed* (fleet telemetry). Integrated cross-functional data and
over-the-air learning are independently documented; the exact tri-phase
schema is only partially confirmed and is treated as indicative [S14–S17].
Its analytical importance is the causal linkage from design intent through
production parameters to field behavior — the quality dimension of κ_D.

For an autonomous seed, this record is more than training data: it is part
of the transported productive system. Process recipes, material models,
calibration procedures, controller firmware, CAD/CAM files, compilers,
simulators, verification suites, dependency mirrors, failure histories, and
intervention records determine whether physical equipment can be operated,
repaired, and adapted after communication or supply is cut. The manuscript
calls this package **industrial memory**. It is not equivalent to "all
industrial knowledge," an incoherent completion standard; it is a
machine-readable operating foundation coupled to the experimental capacity
to discover what the initial package omitted.

Scale proxies require disciplined interpretation. By mid-2026 the vehicle
fleet had accumulated more than ten billion miles under supervised autonomy,
against roughly 220 million fully driverless miles disclosed by another
operator [S17] [S30]. No valid conversion exists between those regimes, so the
figures are not an advantage multiple. More informative disclosures concern
structure: an occupancy network trained on 1.4 billion fleet video frames and
an auto-labeling system replacing roughly five million hours of manual
annotation [S17]. The aerospace analogue is thirteen heavy-lift flight tests
by mid-2026: few observations, each with high information content [S31].
These quantities demonstrate data generation and integration capacity, not
autonomous industrial closure.

## I.3 Why space changes the cost structure {#i.3-why-space-changes-the-cost-structure}

On Earth, useful locations compete with communities, ecosystems,
jurisdictions, and alternative uses. Off Earth, the monetary price of
unused area approaches zero — but infrastructure does not become free; the
composition may change. A matched comparison uses the same lifecycle
categories in each environment $e\in\{\mathrm{Earth},\mathrm{space}\}$:

::: {#eq:matched-lifecycle-cost .equation}
$$
\begin{aligned}
C_e(u,T)
={}&
\sum_{k\in\mathcal K}
\operatorname{PV}_e\!\left(C_{k,e}^{\mathrm{external}}
+C_{k,e}^{\mathrm{internal}}\right)
\\
&-\operatorname{PV}_e(V_{\mathrm{residual},e}),\\
R_C&=\frac{C_{\mathrm{space}}}{C_{\mathrm{Earth}}},
\qquad
\Delta C=C_{\mathrm{space}}-C_{\mathrm{Earth}}.
\end{aligned}
$$
:::

In Equation [@eq:matched-lifecycle-cost], $C_e(u,T)$ is discounted lifecycle
cost in a stated currency year per functional unit $u$ over lifetime $T$;
$\operatorname{PV}_e$ converts dated flows to present value using the
environment-specific discount-rate scenario; $k$ indexes the common category
set $\mathcal K$; “external” is a purchase across the modeled system boundary;
“internal” is the opportunity cost of capacity consumed inside it; and
$V_{\mathrm{residual},e}$ is terminal residual value. The categories are site
or access rights; regulation and permitting; transport and logistics; energy;
feedstock and materials; extraction and processing; manufacturing;
construction and commissioning; labor or human intervention; maintenance,
repair and replacement; coordination and verification;
decommissioning/disposal; externalities; financing; and residual value. A
term is zero only when the scenario and evidence justify zero.

The comparison reports both $R_C$ and $\Delta C$. A positive denominator is
required for $R_C$; a zero or negative Earth cost makes the ratio undefined
and leaves the signed difference as the valid comparison. Monetary cost,
physical mass and energy, intervention time, environmental burden, and
coordination or verification work remain parallel accounts unless a
documented conversion prices them. The declared Part II functional unit is
discounted dollars per frontier-equivalent kilowatt-year of delivered IT load;
its system boundary, utilization, availability, currency convention,
financing, replacement lives, and terminal value are specified in II.2.

The conceptual categories and the implemented Part II boundary reconcile as
follows:

| common lifecycle account | Part II treatment |
|---|---|
| hardware; power, thermal, storage, structure; construction shell | priced as component capex with component-specific lives |
| transport and logistics | launch mass and destination multiplier priced; launch-site, turnaround, and replenishment logistics omitted |
| energy and operations | electricity, PUE, pumping, ground segment, station-keeping, and utilization priced |
| regulation, insurance, disposal, financing, residual value | explicit scenario terms |
| extraction, feedstock, manufacturing, repair and replacement | local-closure and serviceable/disposable scenarios; physical capacity constraints remain in Part I |
| intervention, coordination, verification, externalities | partially represented through operations and utilization; collision externality and detailed intervention/coordination accounts remain omitted |

: Mapping from a common lifecycle account to the implemented Part II boundary. {#tbl-lifecycle-account-boundary}

Part II therefore does not infer an advantage merely because off-Earth land is
cheap. Its contribution outputs must use this category order, show uncertainty
ranges, and expose the terms driving $\Delta C$. The claim that cost “changes
kind” is supported only where contribution shares actually change under
sensitivity analysis.

The land term declines sharply, but useful positions can remain scarce
because of illumination, thermal conditions, communications geometry,
orbital stability, resource proximity, political accessibility, and
transport energy. The first system must still arrive, survive, obtain or
import matter, reject heat, maintain operations, and replace failed
equipment. Space removes neither scarcity nor cost; it changes their
composition.

The standard external objections — station-keeping, collision management,
imported mass, maintenance, coordination — become *internal product
categories* once the complex can manufacture the required systems:
propellant lines, tracking and maneuver capability, local extraction and
recycling, inspection robots and modular spares, compute and communications.
The crucial question is never whether these requirements exist but whether
the complex can reproduce the industries that satisfy them faster than the
system depreciates.

This is the causal boundary of the expansion claim. Moving an
Earth-manufactured factory or data center into orbit changes its
environmental and transport terms but leaves its growth exogenous to the
off-world system. Moving a reproducible production graph off Earth does two
different things: closure makes growth endogenous, while location relaxes
terrestrial biosphere, land, and political rate limits. Either property can
exist without the other. "Free industrial expansion" is shorthand for
their conjunction, never for costless matter, energy, control, or time.

**Gravity is a process variable, not a system prerequisite.** Industrial
operations divide into at least three classes: processes that tolerate or
benefit from microgravity; bulk operations for which a stable downward
acceleration assists excavation, hopper flow, phase separation, drainage,
and conventional machine layout; and processes that need a specified
acceleration, hydrostatic head, or convection regime. Lunar gravity
(approximately $0.165g$) supplies the second class with a persistent
"down," although lower weight also reduces traction and changes granular
flow. It cannot be declared sufficient for every casting, chemical,
lubrication, thermal, or separation process without testing that process.

Where greater acceleration is needed, the relevant intervention is normally
a rotating drum, centrifuge, or production module—not artificial gravity
for the entire industrial ecology. For radius $R$ and angular speed
$\omega$,

::: {#eq:centrifugal-acceleration .equation}
$$
a_c=\omega^2R.
$$
:::

One terrestrial $g$ requires about 30 rpm at a one-meter radius or
9.5 rpm at ten meters. An ideal rotor consumes energy to spin up and stores
$E_{\mathrm{rot}}=\tfrac12 J_{\mathrm{rot}}\omega^2$, where
$E_{\mathrm{rot}}$ is rotational energy in joules and $J_{\mathrm{rot}}$ is
rotor moment of inertia in $\mathrm{kg\,m^2}$; $I$ is reserved for
intelligence capability. Uniform rotation does not itself require continuous
power. The engineering cost lies in structural mass,
containment, bearings or magnetic suspension, balance control, vibration,
rotating power/data interfaces, spin losses, maintenance, and the inability
to share one acceleration geometry across every process. Lunar gravity is
therefore plausibly enough for many bulk operations, while local
centrifugation is the fallback for gravity-sensitive steps. No credible
single dollar estimate exists without a process list, throughput, rotor
radius, and maintenance architecture. The ten-sector model has
none of these variables; the integrated layer adds declared per-process
gravity requirements, centrifuge radii, and structural-mass and
parasitic-power penalties (D.1) — stylized equipment overheads, not
simulations of the underlying processes.

The complex need not be one self-contained factory: a distributed network
of specialized nodes — lunar mines, orbital refineries, propellant depots,
solar arrays, shipyards, robot factories, compute centers — whose combined
input-output graph is closed. A caution on aggregation applies to every use
of the word "space" in this document: LEO, high orbit, cislunar space, the
lunar poles, Mars, and asteroids differ in radiation, thermal cycling,
illumination, dust, gravity, resources, transport energy, and
serviceability. Feasibility claims cannot be aggregated across them; the
model of Part I.7 therefore uses three explicit reference architectures
(LEO / lunar surface / Mars) rather than "space."

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
| central | LEO | 267/400 (0.67, 0.62–0.71) | 122 | 277 | 67, 26.0 (23.2–30.0) | 1.26 | mining 97.7% |
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

# Part II — Comparative Economics {#part-ii-comparative-economics}

## II.1 The bridge economy {#ii.1-the-bridge-economy}

Each stage of the recursion must be independently profitable or deliberately
financed: a staircase of self-supporting steps, not a single leap to
closure. The plausible treads, in order: terrestrial products of the same
machinery (vehicles, storage, robots — the ground floor pays rent **and**
turns the autonomous seed into an audited industrial experiment); launch
and connectivity (Starlink revenue and launch services fund transport);
orbital compute services — a candidate tread priced explicitly in
II.2–II.4; and in-space industrial services at higher
closure. The test of the staircase: at every stage, revenue plus strategic
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

# Part III — Strategy Interpretation and Governance {#part-iii-strategy-interpretation-and-governance}

## III.1 A Musk-associated technology stack {#iii.1-a-musk-associated-technology-stack}

The following mapping is an analytical interpretation of how existing
companies could supply layers of the proposed system — not proof that they
are managed as one program, although the 2026 developments (the Terafab
initiative; SpaceX's absorption of xAI) bind the transport, communications,
intelligence, and fabrication layers by overlapping control, strategic
coordination, and contractual collaboration. Tesla remains a separate
public company; a shared controlling figure and a framework agreement are
not common ownership (Form S-1 pp. 7, 10, 154) [S27].

| layer | contributor | capability | role in recursion |
|---|---|---|---|
| Intelligence | xAI (within SpaceX) | AI research, large-scale compute [S3] | design, coordination, recursive digital improvement |
| Energy | Tesla Energy | generation, storage, power electronics [S2] | power for compute, factories, robots |
| Robotic labor | Optimus | manipulation, maintenance; stated Terafab construction role | manufactured labor capacity |
| Manufacturing | Tesla | high-volume factories, batteries, motors | factory design, machine production at scale |
| Fabrication | Terafab (Tesla, SpaceX, xAI; Intel from Apr 2026) | declared: chip design, lithography operation, fabrication, memory, packaging [S6–S10, S27, S29] | declared compute-substrate layer; framework stage |
| Transport | SpaceX / Starship | reusable heavy lift | seed deployment, materials movement |
| Communications | Starlink | distributed connectivity | coordination across remote nodes |
| Compute deployment | planned D3 constellation | radiation-tolerant silicon | space-based compute as stated product |
| Data | fleet, factories, test programs | telemetry, process parameters, failure archives | the physical loop's exhaust (I.2) |
| Industrial knowledge | Tesla / SpaceX / xAI / Terafab | CAD/CAM, simulation, software toolchains, process recipes, material models, build records, and failure archives | portable digital seed and industrial memory |
| Settlement | Mars objective | self-sufficient city as stated goal | demand center; survival independent of Earth |

: Publicly documented portfolio layers relevant to recursive industry. {#tbl-portfolio-recursion-layers}

**The dated comparative claim.** As of July 28, 2026, and within the
comparison class of publicly documented programs proposing or demonstrating
space-based machine-learning or data-center compute, SpaceXAI presents the
broadest and most tightly coupled publicly disclosed **closure-seeking**
stack. Its core combines reusable launch, spacecraft manufacturing,
orbital communications, terrestrial AI compute and models, an AI1 vehicle
design, and a filed orbital-data-center proposal. This is a comparative
hypothesis about breadth and coupling, not a claim that competitors do not
exist or that a complete self-sustaining stack operates. Google/Planet
Project Suncatcher has planned prototypes and a technical study [S32] [S92];
Starcloud reports an orbital H100 demonstration [S93]; and Blue Origin has
filed Project Sunrise [S94].

The actor boundary is load-bearing. The **SpaceXAI core** is Space
Exploration Technologies Corp. and xAI within SpaceX. Tesla remains a
separate public company over which SpaceXAI has no control [S95]. Its
stationary storage, grid controls, battery-material work, terrestrial
manufacturing, chip collaboration, and Optimus program may enter only the
explicitly labelled affiliate-hybrid ecosystem. No transfer, availability,
orbital qualification, or joint control is presumed. The same discipline
applies to every disclosed partner.

The provenance-backed [18-layer closure-stack matrix](../outputs/integrated/tables/orbital_ai_closure_stack.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_ai_closure_stack.csv"}
compares that bounded ecosystem with Google/Planet, Starcloud, and Blue
Origin. It records the responsible legal entity, relationship, operating
environment, maturity, demonstrated capacity, target, missing dependencies,
source date, evidence class, common-control status, and off-world
reproductive closure. Its
[comparison summary](../outputs/integrated/tables/orbital_ai_closure_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_ai_closure_summary.csv"}
puts the bounded SpaceXAI ecosystem first on evidence-weighted breadth:
qualifying evidence appears in 17 of 18 layers, with 13 operational,
two under development, two stated aspirations, and one `no_evidence` row.
Only 10 of those 17 evidenced layers are under common control. The missing
capital-equipment-reproduction layer is itself a minimum cut, and the
published filing still records dependence on external materials,
components, semiconductors, memory, and compute hardware [S27].
Terafab-specific projects and commitments remain prospective. Consequently,
every program has zero demonstrated off-world-closed layers and fails
dependency-aware reproductive closure. The 17-layer breadth result is not
94% closure.

The unresolved physical set includes extraterrestrial mining and
beneficiation, feedstock-specific refining beyond narrow battery-material
routes, qualified bulk metals and polymers, semiconductor fabrication and
packaging independent of Earth suppliers, autonomous construction,
in-space repair and recycling, and reproduction of machine tools,
metrology, optics, bearings, and semiconductor process equipment. Biological
life support is outside this article's uncrewed machine-industry boundary;
any settlement or crew-support claim would require a separate closed
biological layer rather than inheriting credit from this matrix.

**The 18-function evidence crosswalk.** Table
[@tbl-portfolio-recursion-layers] is an 11-layer
descriptive strategy map; it is not a coverage audit. The capacity model
has ten coarse sectors. The integrated-bootstrap model
resolves the nearest existing minimum-production crosswalk into 18
functions:

- bulk material: power, mining, refining, and recycling;
- industrial equipment: robotics, machine tools, construction, thermal, and
  process equipment/metrology;
- electronics: interconnects/boards, passives/power, sensors/control,
  packaging/test, mature logic, and advanced logic/memory;
- operations and maintenance: transport and repair; and
- intelligence and compute: compute.

These are **model buckets for minimum viable production and service
functions**, not “the 18 industries that must move off-planet.” Network
closure requires enough off-world capacity to reproduce or validly
substitute every indispensable node. It does not require relocating every
terrestrial firm or all output in an industry.

Nor is 18 an exhaustive count of industrial closure. The same integrated
model tracks 17 material categories, while the process-closure gap register
still requires species-level chemistry, gases, resists, optics, bearings,
calibration artifacts, parent-tool ancestry, qualified source lots, and
reproduction of the transport fleet. Thus sector adjacency is a screen over
a deeper source–grade–process–tool–fleet graph, not a replacement for it.

The versioned row audit uses Tesla's current filings and impact disclosures
[S90] [S91]. Tesla is a separate public company: shared control, supply
agreements, and the Terafab framework make a portfolio crosswalk analytically
relevant, but they do not create common ownership or guarantee access to its
resources.

SpaceX evidence comes from filing-backed operating and
forward-looking disclosures [S27] and the published AI1 specification [S38].

For each sector the audit records the initiative, demonstrated output,
location, scale, suppliers, required parent tools, off-world relevance,
evidence tier, source locator and date, and residual gap. It then scores
seven separate dimensions: capability existence, relevant terrestrial
scale, space qualification, off-world operation, local inputs, locally
reproducible production equipment, and locally supported
repair/verification. These dimensions are never collapsed into one
“covered” checkbox.

| mutually exclusive evidence tier or separate closure result | sectors | interpretation |
|---|---:|---|
| documented operating | 12 | operating terrestrial capability plausibly adjacent somewhere in the portfolio |
| demonstrated but not scaled | 0 | no row currently falls in this tier |
| announced or under development | 5 | mining, robotics, packaging/test, mature logic, and advanced logic/memory |
| adjacent capability only | 0 | no row currently falls in this tier |
| no qualifying public evidence | 1 | semiconductor process equipment/metrology reproduction |
| demonstrated off-world reproductively closed | **0** | separate dependency-aware closure result, not an evidence tier |

: Evidence-tier counts and the separate off-world-closure result. [View data](../outputs/integrated/tables/portfolio_sector_coverage_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/portfolio_sector_coverage_summary.csv"}. {#tbl-portfolio-sector-evidence}

This is the provisional public-evidence vector
**12 operating / 0 demonstrated-but-unscaled / 5 announced-development /
0 adjacent-only / 1 not evidenced / 0 off-world reproductively closed**,
current to July 28, 2026. The evidence categories are terrestrial-adjacency
labels, not closure credit. Some power, thermal, transport, board,
passive/power, and sensor/control hardware operates in space, but its inputs,
production equipment, repair chain, and verification standards are still
Earth-supplied. Even a hypothetical 17 partially covered rows out of 18
would not mean “94% closed”: process-equipment/metrology is a parent-tool
minimum cut, so one missing indispensable chain can stop reproduction.

The [18-row evidence crosswalk](../outputs/integrated/tables/portfolio_sector_coverage.csv){.artifact-link data-artifact="outputs/integrated/tables/portfolio_sector_coverage.csv"},
[aggregate vector](../outputs/integrated/tables/portfolio_sector_coverage_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/portfolio_sector_coverage_summary.csv"},
and [five-block view](../outputs/integrated/tables/portfolio_sector_group_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/portfolio_sector_group_summary.csv"}
all regenerate from `params/portfolio_sector_coverage.json`. The article's
table viewer exposes filters for entity, evidence tier, sector group, and
residual gap. A `no_evidence` label means only that no qualifying evidence
was found in the declared search of current filings, technical and facility
disclosures, and supplier announcements. Job advertisements, generic
“aerospace companies must do this” inference, and operation of purchased
equipment are insufficient. Absence of public evidence is not proof of
absence.

Every row remains linked to acceptance gates C01–C08 and the
[process-closure gap register](../outputs/integrated/tables/process_closure_gap_register.csv){.artifact-link data-artifact="outputs/integrated/tables/process_closure_gap_register.csv"}.
A sector can be called closed only when source, material-grade, unit-process,
critical-part and parent-tool, fleet, failure/substitution, and empirical
calibration evidence passes. Portfolio adjacency could reduce coordination
or transition cost; it does not prove off-world recipes, yields, autonomous
task coverage, commissioning, verification, or economics.

The theoretical advantage is not ownership of complementary companies but
a shorter verified end-to-end loop across design → manufacture → deploy →
learn. The closure race rewards the shortest such loop, not the largest
stock of any single input.

For this portfolio, the proposed sequence is the actor-specific instance of
Equation [@eq:coupled-rsi-system]: xAI would improve intelligence and
automation; factories would expand energy and hardware; Terafab would expand
chips; and the resulting terrestrial or orbital compute would feed another
verified intelligence-improvement cycle.

The advantage, if it exists, is the ability to integrate feedback, capital
allocation, engineering, deployment environments, and industrial production
into that shorter loop. Reported preparations for a SpaceX public offering
would, if completed, add a financing event for the capital-intensive middle
of the loop [S9] [S27]; financing capacity is an enabler, not evidence of
closure intent.

## III.2 Terafab and the fabrication frontier {#iii.2-terafab-and-the-fabrication-frontier}

**What was announced**: a Tesla–SpaceX–xAI chip fabrication initiative
(March 2026), joined by Intel in April; declared scope from chip design
through lithography operation, fabrication, memory, packaging, and test;
reported $20B initial plant with a filing-based ceiling near $119B; 2-nm
target; mass production stated for 2028 [S6–S10]. **What the primary
source says** [S27]: a general framework with Tesla — timelines,
milestones, and capital expenditures for specific projects not yet
determined and subject to separate agreements; a stated orbital data-center
plan from as early as 2028; and an aim to alleviate potential future chip
shortages for orbital AI (Form S-1 pp. 7, 10, 154). **First-party
messaging versus legal commitment** [S29]: the initiative's own site frames
the effort on the Kardashev scale, publishes scaling figures (~1B robots,
~10 Mt/yr launched, >1 TW solar), names chip lines for vehicles, robots,
and space (AI5, AI6, D3), publishes an explicit orbital-versus-terrestrial
cost decomposition, and names lunar mass drivers as the next step. The
divergence between site and filing is itself informative: a strongly
space-oriented declared strategy resting on unsettled implementation.

The implementation detail matters. Reporting describes a roughly $3B
research fab producing a few thousand wafers per month before any scaled
phase, with ambitions moving from about 100,000 wafer starts per month
toward one million [S6–S10]. Those figures evidence intended scale, not
comparable output: wafer starts cannot be compared with a foundry's global
production without node, wafer diameter, product mix, yield, and effective
die output. Planned products include AI5/AI6 chips for vehicles and robots
and radiation-tolerant D3 silicon for orbital deployment; Optimus robots
have been assigned a stated construction and operating role. Each remains a
target rather than demonstrated capacity.

**What it changes**: fabrication moves from missing term to declared
target; the residual dependency moves one layer down (EUV lithography,
deposition, etch, metrology, ultra-pure feedstocks — sole-supplier
equipment, not foundries); the fab-to-space link becomes explicit (D3).
**What it does not change**: no wafers have been produced; the timeline
is faster than any historical ramp; industry skepticism is on record.

The competence question is precise: Tesla, SpaceX, and xAI have no
advanced-fab operating record,
but **Intel plainly does**, and the reported process plan is Intel 14A —
so the open question is whether that experience transfers into this
organizational structure and what obligations Intel has actually
accepted, not whether anyone involved has run a fab.

Executed county tax and economic-development agreements strengthen
site-level commitment without establishing construction, funding,
production, or a definitive operating agreement [S6–S10].[^p3-terafab-sites]
Wafer-start counts remain incomparable with foundry output without wafer
diameter, node, product mix, yield, and effective die output. “One terawatt
per year” is a claimed hardware-production rate whose aggregate nameplate
power draw would total a terawatt, not a national-electricity-consumption
measure.

[^p3-terafab-sites]: The smaller Tesla research fab is at the Giga Texas
    campus; the proposed scaled SpaceX-led facility is in Grimes County. The
    distinction matters for interpreting which entity, site, and agreement
    each source actually covers.

**The lithography question**: for terrestrial operation, purchased
lithography is an acceptable permanent dependency; for high space closure
it must eventually be reproduced, substituted (older nodes at volume;
nanoimprint; e-beam), or accepted as designed permanent import — the
deepest single closure problem in this framework (and precisely where the
Part I strategic-material gap lives). The analysis adds the bottleneck convergence:
the AGI-buildout literature identifies advanced packaging and HBM memory
as the near-term chip constraints [S35], and HBM is what the Suncatcher
radiation testing found most dose-sensitive [S32] — the same component
class is the terrestrial scaling bottleneck and the space reliability weak
point.

**Terafab-specific observables.** The milestones that would change this
assessment are: the first research-fab wafer and disclosed yield at any
node; visible order flow from lithography, deposition, etch, and metrology
suppliers; evidence that memory and advanced packaging are actually produced
in-house rather than outsourced; radiation-qualified D3 silicon with
disclosed orbital-compute unit economics; and definitive agreements that
commit capital and counterparties. Industry skepticism is therefore a
testable forecast, not a rhetorical counterweight [S10].

## III.3 Competing hypotheses: the evidence table {#iii.3-competing-hypotheses-the-evidence-table}

The hypotheses are nested rather than exclusive, since a long-run off-world
strategy can be *pursued through* vertical integration and supply hedging —
those are mechanisms, not alternatives. **H0** is the matched
portfolio-adjacency baseline: projects may share ownership, branding,
finance, suppliers, data, bilateral interfaces, and ordinary commercial or
supply-security motives without sharing one off-world systems architecture.
Standalone orbital compute, a domestic fab, launch/AI consolidation, and
cross-selling are all H0-compatible. **H1** adds deliberate coordinated
space–AI–industrial development — the
[P4a — Documented portfolio direction](proposition:P4a){.proposition-ref}
claim — evidenced most strongly
by shared technical interfaces, common architecture documents, binding
cross-program milestones, cross-subsidy, or joint resource allocation, not
by co-ownership alone. **H2** adds an explicit intended transition to
recursive industrial closure — the
[P4b — Recursive-closure intent](proposition:P4b){.proposition-ref}
claim — with closure metrics, a seed
bill of materials, minimum-cut work, or locally reproducible production
equipment as its distinctive observables. Because the hypotheses nest, each evidence item is
assessed on two separate margins — does it separate H1 from H0, and does it
separate H2 from H1 — and the assessments are **ordinal, not numerical**:
the items are correlated (several derive from the same corporate
communications), absence-items depend on assumed observability, and
declared intent is cheap; assigning multiplicable likelihood ratios to such
material would imply a probabilistic model that does not exist. Ratings:
*neutral* (equally expected under both), *weak*, *moderate*, *strong*
(difficult to explain under the alternative). A distinct motive reading
cuts across the nest: heavy industry moves off Earth to *protect the
biosphere* rather than escape a constrained platform [S34] — same physics,
different telos — which supplies an additional non-H2 explanation for any
orbital-compute observation. Per the propositions ladder, everything here
concerns P4, and P3 is decoupled from it: the migration case requires no
claim about any company's intentions.

| # | evidence item | status / class | H1 vs H0 | H2 vs H1 | note |
|---|---|---|---|---|---|
| E1 | Reusable launch, declining $/kg | documented | neutral | neutral | predates thesis; expected under any hypothesis with a launch business |
| E2 | Mars-city rhetoric | documented / company_statement | neutral | neutral | long predates the thesis; expected as portfolio branding under H0 |
| E3 | Battery/vehicle/robot vertical integration | documented | neutral | neutral | canonical H0 |
| E4 | Humanoid robot program, scale targets | announced / company_statement | neutral | neutral | targets are intent, not capacity |
| E5 | Starlink constellation ops competence | documented | neutral | neutral | profitable on its own terms |
| E6 | Initiative list in SEC-filed offering materials associated with the S-1 (Rule 433 FWP and incorporated materials): orbital compute, lunar manufacturing and energy, in-orbit and Moon/Mars manufacturing, asteroid mining, "interplanetary industrialization" | documented / SEC-filed offering materials [S27] | **moderate** | neutral | strong evidence of declared portfolio direction, but the matched H0 also predicts a portfolio narrative; no shared technical architecture or closure program is disclosed |
| E7 | Terafab initiative; Intel joining; executed county agreements | announced→partly advanced / company_statement | weak | neutral | chip-supply hedging (inside H0) predicts a domestic fab about as well |
| E8 | SpaceX absorption of xAI | documented | neutral | neutral | consolidation, capital access, and shared infrastructure are expected under matched H0 unless technical coordination is shown |
| E9 | Rad-tolerant orbital silicon as a named fab line | announced / company_statement | moderate | neutral | H1 predicts it distinctly; a D3-supply commercial reading covers it too |
| E10 | No closure metrics, no seed BOM, no closure program | absent | neutral | **moderate against H2** | a deliberate closure strategy mildly predicts visible closure engineering by now; observability caveat applies |
| E11 | No export-scoped internal model variant, and no reported compliance apparatus for controlled-data training | absent | neutral | weak against H2 | the observable is the compliance architecture, not the model, which may be deliberately unpublicized |
| E13 | FCC **acceptance for filing** of an application for an orbital-data-center system of up to ~1M satellites [S50] | documented application; pending regulatory review — not an authorization | weak | neutral | filing a large option is far cheaper than receiving permission to deploy it |
| E14 | First-party Terafab messaging: Kardashev framing, ~10 Mt/yr to orbit, lunar mass drivers, orbital-vs-terrestrial cost decomposition | documented / company_statement [S29] | **moderate** (declared direction only) | weak | unusually explicit off-world framing, but messaging is cheap, H0 permits portfolio promotion, and binding filings commit to no shared architecture |

: Evidence ledger for the strategy hypotheses. {#tbl-strategic-evidence-ledger}

E12 and E15 (the Google/Planet Suncatcher prototype program and the design
study's content) are removed from Table [@tbl-strategic-evidence-ledger]:
they are actions of
*independent* actors and bear on no hypothesis about the Musk-associated
complex's intentions. They are retained as engineering reference-class
observations under external cross-checks below — an announced prototype
program (satellites slated for early 2027 [S33]), and radiation results bounding
the qualification corner (5-yr TID survivability supported with margin;
7-yr *system* reliability unresolved; II.4).

**What the models add to interpretation.** A rational H2 actor facing Part
I would visibly invest in the electronics closure layer — rad-tolerant
lines, stockpile logistics, shelf-life-rated spares, off-world
packaging/test — because that is the most frequently observed minimum cut in the sampled ensemble. A rational
H1-or-H2 actor facing Part II would run orbital compute at a loss for
positioning, or privately believe the COTS/long-life corner; sustained
scaled deployment after the unit economics are publicly evident is a
*moderate-to-strong* discriminator between the strategic (H1/H2) and
commercial (H0) readings — and conversely, quiet retreat after the
demonstration phase is what H0 predicts. On-orbit
*materials-recovery* recycling at scale (not debris-compliance servicing)
would be *moderate-to-strong for H2 specifically*: Part I's structural
result that the LEO architecture lives on its recovered-mass feed loop
(capture/mining receives ~98% of central co-binding credit; the analysis withdraws the stronger
stale claim that the recycling *sector* was knockout-indispensable) makes
building that loop the rational early move of a
LEO-first closure strategy and of no one else.

**External cross-checks** [S35]: the canonical AGI-buildout analysis
resolves the power wall terrestrially without mentioning orbit —
non-space-interested corroboration of Part II from outside; its chip
bottleneck converges with the space radiation weak point (III.2); and its
fast-takeoff thesis, if right, weakens the H1/H2 rationale regardless of
the evidence — an effect on the prior, reported separately from the
item-level assessments. A provisional July 2026 frontier-lab hiring sweep
is quarantined as an appendix note (A.7), not used as an evidence-table
item or model input.

**Cumulative assessment** (ordinal synthesis, not multiplication — the
items are correlated and the ratings judgmental): the evidence
**supports H1 at the level of declared direction but does not establish a
coordinated technical architecture**. The initiative list in the SEC-filed
offering materials (E6) and the first-party messaging (E14) establish an
off-world portfolio narrative, while E7/E9/E13 are consistent implementation
steps; the matched H0 explains all of them through adjacent commercial,
supply-security, financing, and promotional motives unless shared
interfaces, milestones, or resource allocation appear. It **does not
establish H2**: no item in Table [@tbl-strategic-evidence-ledger] is more than
weakly diagnostic for closure intent, the closure-specific observables
(seed bills of materials, reproduction metrics, minimum-cut roadmaps,
locally reproducible production equipment) remain absent (E10), and most
observed actions are equally expected under a conventional integrated
off-world commercial strategy.
[P4a — Documented portfolio direction](proposition:P4a){.proposition-ref} is
documented; [P4b — Recursive-closure intent](proposition:P4b){.proposition-ref}
remains inferential
— which is exactly the split encoded by the proposition ladder.

## III.4 Control and governance of a self-expanding system {#iii.4-control-and-governance-of-a-self-expanding-system}

A self-expanding autonomous industrial network is, formally, a governed
macroscale von Neumann replicator; the property that makes it valuable —
compounding physical replication — makes its failure modes compound too.
Verification and authorization must scale with expansion; throttle authority
must be explicit (rate limits, hardware-level authorization of replication
steps, clarity about who holds them); the legal frame is unsettled and first
movers set precedent. Equation [@eq:authorized-capacity-control] therefore
counts only capacity admitted by the slowest required reliability,
adversarial-verification, secure-command, environmental, treaty, and
human-comprehension channel. Reporting gross capacity without this parallel
authorized trajectory would hide the governance bottleneck.

The milestone gate in Eq. [@eq:milestone-control-gate] makes timing
non-negotiable: $T_{\mathrm{ctrl}}\le T_{\mathrm{AIR\&D}}$ and
$T_{\mathrm{ctrl}}\le T_{\mathrm{cl},e}$ for each environment $e$ whose
capacity can replicate. A faster capability or production state is gross
capacity, not authorized success, when independent evaluation, command, or
stop bandwidth lags it.

The gates depend on consequence, authority, reversibility, containment, and
exposure—not on the label “internal” alone. The recursive pipeline has three
distinct decisions:

1. **Technical validation:** does the proposed change improve the intended
   held-out capability without unacceptable regression?
2. **Bounded internal authorization:** may it advise or act on this monitored,
   reversible internal task under specified access and rollback limits?
3. **External/public authorization:** may it be exposed to broader users,
   environments, misuse paths, legal duties, and uncontrolled distribution?

Each decision has its own evidence, independence, latency, rollback, and
authority requirements. Technical validation is always required before an
increment enters the compounding capability account. Internal authorization
adds organization-specific controls for privileged data, infrastructure,
tools, compute, model-development access, and the consequence of the proposed
role. Public authorization adds heterogeneous users and environments,
uncontrolled copying, external misuse, product and regulatory obligations,
and behavior outside the monitored boundary. Those concerns can overlap
without being interchangeable, so one undifferentiated verification yield
cannot represent all three gates.

Replication needs a second distinction: productive capacity is not
automatically legitimate capacity. The governance sensitivity keeps the
accounts separate:

::: {#eq:replication-governance-gate .equation}
$$
\begin{aligned}
K_{\mathrm{prod}}(t)
&=K_{\mathrm{auth}}(t)+K_{\mathrm{unauth}}(t),\\
\Gamma_{\mathrm{gov}}
&=\mathbb 1\!\left[
\begin{gathered}
\frac{K_{\mathrm{unauth}}(T)}{K_{\mathrm{prod}}(T)}
\le \bar u
\;\land\;
\frac{K_{\mathrm{preempt}}(T)}{K_{\mathrm{prod}}(T)}
\le \bar p
\\
\land\;
L_{\mathrm{claim}}\ge\bar L
\;\land\;
\phi_{\mathrm{ext}}\ge\bar\phi
\\
\land\;
\prod_{j\in\mathcal G}g_j=1
\end{gathered}
\right].
\end{aligned}
$$
:::

$K_{\mathrm{prod}}$, $K_{\mathrm{auth}}$, and
$K_{\mathrm{unauth}}$ are total productive, legitimately authorized, and
unauthorized capacity; $K_{\mathrm{preempt}}$ is capacity that has preempted
contested resources; $T$ is the declared horizon; and $\bar u$ and $\bar p$
are maximum unauthorized and preemptive shares. $L_{\mathrm{claim}}$ is
resource-claim legitimacy with required floor $\bar L$;
$\phi_{\mathrm{ext}}$ is the fraction of externality costs internalized with
required floor $\bar\phi$; and each binary $g_j$ in the gate set
$\mathcal G$ covers update authority, liability, audit rights, succession of
control, or representation of future affected parties.
$\Gamma_{\mathrm{gov}}=1$ is a governance endpoint, not an engineering
performance score.

The declared private-race stress case makes the distinction concrete. It
reaches 126.222 productive-capacity units after 15 years, so the engineering
and owner-objective endpoints pass. Only 2.200 units are legitimately
authorized, 124.022 are unauthorized, all 20 contested-resource units are
preempted, and the debris-externality stock reaches 85.151. The owner account
receives 322.000 cumulative output units while the current-public and
future-affected-party accounts receive 28.622 and 7.156. Private net value is
positive at 133.300, but social net value is −3,040.566 after the declared
externality costs: a negative-sum race and a governance failure despite
engineering success. The cooperative and treaty-limited branches both pass
the engineering and governance endpoints. These are transparent
**ASSUMPTION** stress tests, not forecasts, legal-title conclusions, or a
prescribed distributive ethic.

The claim shares also expose a dynamic institutional risk. Material
governance leverage falls from 1.0 to 0.050 in the private-race branch as
closure advances. If owner-heavy claims and weak audit or succession rules
are fixed during the Earth-dependent bridge, later physical independence can
entrench that allocation while removing an effective material control. The
control surface must therefore include update authority, resource-claim
rules, liability, audit rights, succession of control, and representation of
future affected parties—not only stop hardware. Extrasolar abundance and
post-ASI allocation remain outside the article's evidentiary core; they
motivate nearer-term institutional design under irreversible scale but do
not supply evidence for it. *AI 2040* explicitly labels Plan A primarily a
recommendation rather than a prediction [S85]; its space supplement motivates
the category of claim allocation but supplies no empirical support for the
stress-test coefficients. Machine-readable summaries and trajectories are
in [replication governance externalities summary](../outputs/integrated/tables/replication_governance_externalities_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/replication_governance_externalities_summary.csv"} and
[replication governance externalities trajectory](../outputs/integrated/tables/replication_governance_externalities_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/replication_governance_externalities_trajectory.csv"}.

Offline search, simulation, and draft recommendations can use lighter,
human-mediated internal gates. Live infrastructure control, destructive
experiments, cyber or biological work, physical actuation, model-weight
modification, and successor training can require stringent independent
controls even when wholly internal. Internal advice is also distinct from
internal authority: useful recommendations can arrive while humans retain
execution and rollback authority.

Evaluator independence must be demonstrated across model lineage, training
data, toolchain, decision authority, and unfiltered audit access. Two monitors
that share a strategic blind spot do not supply two independent observations.
The matched stress cases in Part I keep the producer trajectory fixed while
changing those dependencies; the correlated case fails the authorization
endpoint. Human approval likewise becomes ceremonial when proposal throughput
exceeds human comprehension throughput. The required response is a throughput
interlock, not a larger nominal approval roster.

The framework resolves its own tension — celebrating escape from
society-priced costs while requiring retained constraint — through the
gateway: in space, permission attaches to launches and spectrum, which is
where governance holds enforceable leverage. The leverage variable is dependency — but not proportional to (1 − κ), since this document has already established that scalar closure is invalid and a single low-mass import can be a minimum cut conferring disproportionate leverage. The governing quantity is G_dependency = f(criticality, substitutability, stockpile, supplier concentration, enforceability): what matters is whether withholding an input collapses the network, not how much of it is imported. Part I supplies an answer that is architecture- and parameter-conditioned, and must be stated that way: **where import dependency remains load-bearing — the lunar and Mars ensembles — electronics is the most frequently observed minimum cut, and the strategic imported parts are the last material governance handle**; in the sampled central LEO draws a single import line is fatal only in a minority of draws (~0–11% for electronics across deterministic regenerations), so there the material handle runs mainly through feed availability and the recovery loop rather than any one import line. Material-dependency governance has a
declining window as closure rises; throttle authority, verification
requirements, and replication limits are cheapest to embed as licensing
conditions during the bridge period. Closure does not end governance
(communications, cryptographic authority, personnel, ownership, insurance,
treaties, orbital traffic, trade remain), but the material handle is the
one that closes.

A serious control architecture — beyond this document's scope but within
its obligation to specify — requires hardware roots of authority;
multi-party authorization for replication steps; explicit rate limits;
compartmentalization and fault-containment zones; secure update and rollback
channels; explicit cyberattack and insider-risk models; independent
reliability and adversarial-verification capacity with measured common-mode
exposure; an oversight-throughput interlock; operator and government incentive analysis;
jurisdiction and liability rules; and failure recovery when communications
with Earth are unavailable. These are named requirements, not solved
problems. They must be tested under the same loss-of-import, shock, and
degraded-communications conditions used to test the production system.

Design principle: replication authority should be the
most verified and least autonomous function in the system — positioned
deliberately against the efficiency gradient, embedded at the seed stage,
because it cannot be retrofitted onto a mature complex.

## III.5 Falsifiable indicators, model-ranked {#iii.5-falsifiable-indicators-model-ranked}

The indicators carry ordinal diagnostic ratings informed by the models
(consistent with III.3's refusal of numerical likelihood ratios; numerical likelihood-ratio language is intentionally excluded):

1. **A terrestrial autonomous-closure demonstrator that constructs and
   commissions a second production cell under lunar-palette,
   no-routine-entry constraints** — strong for H2 over H1.
2. **Production or fabrication equipment explicitly designed for local
   extraterrestrial reproduction** — strong for H2 over H1.
3. **A dedicated cross-company closure program with published κ-vector
   metrics** — strong for H2 over H1 (flips E10).
4. **A machine-readable off-world seed package** containing the physical
   bill of materials, digital toolchain, industrial memory, dependency
   graph, and experimental/commissioning plan — strong for H2 over H1.
5. **An element-resolved Moon–Earth–asteroid supply plan** with source
   yields, recovery losses, transfer arcs, import-withdrawal milestones, and
   explicit strategic-material import stocks — strong for H2 over H1.
6. **Sustained scaled orbital-compute deployment despite publicly evident
   unfavorable unit economics** — moderate-to-strong for H1/H2 over H0 (Part II makes the test
   operational — watch fleet growth after the economics are public).
7. **Electronics strategic-material-gap engineering**: stockpile facilities,
   shelf-life-rated spares logistics, off-world packaging/test lines
   — moderate-to-strong for H2 over H1 (Part I makes it the rational first move of a closure strategy).
8. **On-orbit materials-recovery recycling at scale** — moderate-to-strong for H2 (the Part I
   LEO feed-loop result; the indicator rests on feed dependence, not
   sector indispensability).
9. **An export-control-scoped internal model variant** — moderate.
10. **Terafab executed definitive agreements with committed capital**
   — weak-to-moderate (upgrades E7 from framework to program; hedging inside H0 still predicts it).

The ranking above asks which observations discriminate among H0, H1, and
H2. A second set asks whether the physical thesis is becoming feasible at
all. These lower-diagnosticity but still necessary indicators are retained:

- robots performing unscripted maintenance, construction, mining, and
  machine tending for long periods, with autonomous recovery fraction and
  human intervention hours reported per machine-hour rather than described
  only as "limited";
- task evidence reported with duration, consequence class, verifier class,
  trial denominator, prompting/checking/recovery/cleanup hours, rollback
  success, out-of-distribution recovery, and the achieved reliability-ladder
  rung rather than a benchmark percentage alone;
- local production of propellant, structural material, and replacement
  parts at operational rather than laboratory scale;
- factories using locally processed feedstock to manufacture additional
  power, extraction, and production equipment;
- a measured decline in imported mass per unit of local productive
  capacity, reported by component class rather than as an aggregate mass
  fraction;
- element-level closure reported as inputs, inventories, losses, recycled
  flows, and source-specific yields—not inferred from aggregate local mass;
- space-manufactured compute, or production equipment capable of making it;
- net positive industrial reproduction after depreciation — P > D in every
  indispensable sector — with published r and δ estimates by component
  class;
- the Terafab-specific milestones in III.2: first wafer and yield, process
  equipment orders, in-house memory and packaging, qualified D3 silicon,
  orbital-compute revenue, and a measured robot reproduction ratio;
- open-weight systems demonstrating sustained autonomous verified
  improvement loops — evidence for the threshold-like branch in II.5 — and,
  separately, fleet- and factory-owning actors outperforming open models on
  engineering tasks in a way attributable to proprietary process data; the
  contrary result would show that κ_D does not bind;
- a sustained measured decline in cost per verified improvement loop, and
  replication-relevant conditions appearing in launch licenses or
  export-control terms while material leverage still exists.

The closures also have separate falsifiers; evidence for one must not upgrade
the others:

| claimed closure | required observation | falsifier or non-upgrading result |
|---|---|---|
| verified AI-R&D | repeated successor improvements survive independent held-out, regression, safety, and transfer tests, including direction selection | gains disappear under independent evaluation, direction remains externally supplied, or retained lessons fail across successors |
| embodied production | the declared industrial minimum-cut tasks run for the required duration under representative faults with bounded intervention and verified recovery | absent sensors/actuators, out-of-distribution failures, intervention burden, or unreliable recovery prevents the task set even if software benchmarks improve |
| reproductive capital | every indispensable sector replaces losses and produces net additional commissioned capacity without a growing external critical-input flow | any minimum-cut sector, parent tool, metrology chain, or clock-setting import cannot be replaced, repaired, substituted, or replenished before exhaustion |
| authorized replication | independently verified productive additions remain within command, environmental, legal, liability, and oversight throughput | gross capacity outruns authorization, common-mode monitors or human comprehension, or preempts contested resources despite engineering success |

: Required observations and falsifiers for each claimed closure. {#tbl-closure-falsifiers}

Threshold observations that would move Appendix A: a demonstrated ISRU
plant above ~50% full-system materials closure; audited robot production
figures; an independent satellite-reliability audit reporting
cohort-specific failures per satellite-year, separated from retirements and
planned disposals (an aggregate ~2.5–3% early-cohort fleet fraction is not
a general hazard rate and is not the right comparison); and
any traceable datum on off-world-producible electronics tiers — the
strategic-material-gap anchor this document flags as its highest-value currently parameterized missing
measurement. The thesis *weakens* if humanoid robotics remains
economically narrow, advanced manufacturing cannot be localized, launch
costs stop declining, closure requires a permanently growing Earth supply
chain, verification costs rise faster than capacity — or if Terafab
devolves into design-and-packaging dependent on external front-end
fabrication, which would reopen the fabrication term entirely.

## III.6 Refined complete thesis {#iii.6-refined-complete-thesis}

The coherent end state remains a recursively self-expanding space industrial
ecology. Reusable rockets transport an initial seed. AI supplies scientific,
engineering, and coordinating intelligence. Robots provide scalable physical
labor. Local energy systems supply power. Mining and refining convert
extraterrestrial matter into industrial feedstocks. Automated factories
produce structures, machines, robots, transport vehicles, energy systems,
and — if the electronics tier can close — compute. Communications integrate
specialized nodes into one economic and operational network.

The network first reduces Earth dependence, then reaches self-sustenance,
and finally produces net additional capacity. At high closure,
station-keeping, collision management, maintenance, transport, and
coordination remain real requirements; they are supplied by industries
inside the network rather than purchased as externally scarce services.

Matter, energy, intelligence, and elapsed construction time become expanding
productive capacity only through the delayed, gated transitions in Equation
[@eq:coupled-rsi-system].

Recursive self-improvement is therefore not limited to software.
Intelligence improves the machinery and institutions that create
intelligence; the industrial substrate returns energy, compute, data,
experimentation, and physical agency to the intelligence layer. The
ultimate product is an industrial system capable of producing more of
itself.

This end state is coupled but non-unitary. Verified AI-R&D, embodied
production, and reproductive capital are distinct closure tests. A system
may improve successors without reproducing its physical substrate, or
reproduce capital under a bounded controller without automating AI research.
Their conjunction is the strongest acceleration branch, while the achieved
system rate remains bounded by the slowest complementary stock and by
authorized verification throughput. Off-Earth resources change the long-run
material and siting envelope only after the bridge to reproductive closure;
location and intelligence alone do not establish recursion.

The marginal product of intelligence is consequently regime-specific rather
than globally positive by definition. The finite-response diagnostic is near
zero in the two material-starved cases and positive after the declared source
network relaxes supply. Intelligence can propose experimental methods,
equipment designs, and schedules; those changes enter capacity only after a
funded productive pathway, construction lag, verification, and applicable
authorization. Reaction and propagation floors, absent observations, heat
rejection, and decisions held by external legal authorities remain explicit
constraints rather than presumed targets of optimization.

The precise formulation is conditional and model-separated. The evidence
documents deliberate integrated
space–AI–industrial direction
([P4a — Documented portfolio direction](proposition:P4a){.proposition-ref}),
but neither a shared technical architecture nor an intended transition to
recursive closure
([P4b — Recursive-closure intent](proposition:P4b){.proposition-ref}). The
ten-sector industrial model finds
expansion under some assumption sets and failure under others, with
electronics and feedstock dependencies localized by architecture. The
18-sector integrated-bootstrap model represents the complete
intelligence–industry loop, seed bill of material, source network, and
aggregate operating-capacity growth; it finds the lunar strategic-material
bridge and the synthetic Moon–asteroid scenario LP-feasible under
central assumptions and the configured strict lunar source graph
structurally infeasible. Because every structural coefficient
is declared rather than measured, that is an executable hypothesis, not
evidence that the complete recursion can be built. The comparative-economics
model finds the Earth-dependent bridge uneconomic at anchored values and
does not price the mature high-closure ecology. Capability accumulation is
observed; positive off-world industrial reproduction and a unified closure
strategy are not.

Equation [@eq:coupled-rsi-system] is the article's compact causal system; this
section does not introduce a second loop definition. The ten-sector model
operationalizes the productive-capacity update as the lexicographic maximin
allocation of Part I.7 (with repair, recycling, stockpiles, and imports) and
decomposes environmental depreciation by sector. The integrated layer
supplies first stylized response functions: installed compute drives verified
intelligence through a saturating gain law; intelligence raises task autonomy
and industrial productivity; and operating cells manufacture additional
compute only after construction and commissioning lags. Constant-rate
Earth-fed deployment is run beside it as the counterfactual. These functions
are executable and swept, but their coefficients are ASSUMPTION-class and
they omit many algorithmic-regime, hardware-node, and coordination details.
The model therefore tests the consequences of a coupling law; it does not
measure that law or establish takeoff, subject also to the speed caveat of
II.5. The coupling ablations show that in the
material-starved terrestrial and lunar-bridge cases,
removing the dynamic coupling changes almost nothing; in the stipulated
Moon–asteroid network it reduces year-40 net balanced growth by about 46%.
The declared f and h therefore become operative only after the source
vector relaxes material supply, while the starting AI level also matters
through seed feasibility (I.8). This is a regime implication of assumed
coefficients, not evidence that the coupling exists at the stipulated
strength.

**What the thesis does not claim**

- It does not establish that the companies are managed under one
  confidential master plan; III.3 assesses the public evidence.
- It does not imply that energy, matter, infrastructure, coordination, or
  opportunity cost become literally free.
- It does not assume intelligence automatically solves semiconductor
  fabrication, reliability, verification, governance, or safety.
- It does not claim that the degrees of freedom of a current humanoid robot
  demonstrate unscripted industrial autonomy; embodied task coverage,
  recovery, and verification remain unmeasured requirements.
- It does not require human settlement, agriculture, or a closed biosphere
  for the reference machine ecology, nor does it claim humans could never be
  present. A crewed architecture is a larger closure problem than the one
  modeled here.
- It does not require every industrial node to be self-contained; closure
  can exist at network level.
- It does not require uninterrupted exponential growth; the system can move
  through bottleneck-limited regimes and can double before later losing
  viability.
- It does not claim Terafab will achieve viable yields or off-world
  fabrication closure; it is a declared terrestrial attempt whose
  implementation remains unsettled.
- It does not claim a slow takeoff is certain; the physical-path thesis is
  conditional on the slow-to-medium branch in II.5.
- It does not claim that closure is imminent, that model frequencies are
  empirical probabilities, or that space compute is economical today.

* * *

# Part IV — Conclusion, and Speculative Terminal Scenarios {#part-iv-conclusion-and-speculative-terminal-scenarios}

## IV.1 The defensible core, restated with numbers attached {#iv.1-the-defensible-core-restated-with-numbers-attached}

Two constraints, two rate comparisons, one passage. Externally induced
supply expansion competes with internally controlled reproduction, while
the operating envelope compares terrestrial social and infrastructure costs
with off-world transport, reliability, and closure costs. Neither comparison
is escaped by terminology; both remain conditional on surviving the bridge.
The bridge's failure mode is specific: hold electronics-class stockpiles
against shelf life, and reach local production of some electronics tier
before the import ramp decays.
The causal core is also narrower than a single coupled-loop slogan:
reproductive-capital closure can generate endogenous physical growth with a
bounded controller, while verified AI-R&D closure can accelerate design
without creating physical reproduction. In the central Moon–asteroid
ablation, the bounded-controller branch still doubles at 36.75 years; the
fully coupled branch reaches the same threshold at 35.25 years. The strongest
acceleration case combines both loops, but neither loop defines the other.
The defensible core conclusion stops here, with its conditionals
quantified: *if* industrial closure becomes sufficiently high across every
indispensable sector (Part I's bottleneck is architecture-specific:
capture/mining dominates LEO, electronics dominates the Moon, and
electronics and power co-bind on Mars) *and* terrestrial
expansion costs rise faster than off-world deployment costs (Part II says:
not at anchored values; only in the qualification/life/utilization corner
at target-class launch prices), *then* some large-scale industrial and
computational activity may migrate off Earth. Everything beyond that
sentence is scenario.

> **QUARANTINE NOTICE.** Sections IV.2–IV.4 are scenario-class: internally
> consistent extrapolation, not established result. Nothing in them feeds
> back into Parts I–II inputs. Each scenario carries a model check —
> usually a constraint, not support.

## IV.2 After convergence: deployment as the terminal regime {#iv.2-after-convergence-deployment-as-the-terminal-regime}

At some point the marginal value of further design improvement falls below
the marginal value of another deployed node — architectural convergence.
Past it, intelligence behaves as a commodity produced by infrastructure — heuristically, throughput ~ deployed energy × physical efficiency, a relation that omits memory, interconnect, utilization, data, reliability, verification, latency, workload composition, and fabrication yield. Efficiency is floor-bounded (Landauer, with reversible logic the stated exception); scale plausibly becomes the *dominant marginal* variable rather than the only one; scale means energy; energy means collector area; and collector area is not bounded by a planetary surface off Earth. It remains bounded — by matter, transport, orbital geometry, heat transport, collision risk, maintenance, and control, and per the published cluster analysis by the quadratic scaling of satellite count with cluster radius and by mutual occlusion of rejected infrared between closely flown spacecraft [S32]. The ceilings-and-rates
argument is retained in sensitivity form: the waste-heat ceiling
sits perhaps two orders above current civilizational energy use, the
thermodynamic floor several orders below current efficiency, and the
~3×/yr algorithmic-efficiency figure [S26] measures
compute-for-fixed-language-performance only. Under sustained compounding,
distances that look like centuries become decades — *whether the
compounding is sustained is precisely what is unknown*.

The two regimes can be stated as marginal cost curves. On Earth, the
marginal cost of the n-th node can rise as the operator bids up land,
congests grids, and encounters political and thermal limits. In space,
*after closure*, the marginal cost can fall through learning and
self-replication. One curve rises and the other falls; their crossover is
the migration point, and it moves earlier as launch cost declines, closure
improves, equipment life lengthens, or qualification premiums fall. Part II
shows that the curves do not cross at the anchored bridge-economy values.

> **Model check.** The cost-curve claim — Earth's marginal node rises with
> n, space's falls with n after closure — is the crossover surface, and at
> anchored values the curves do not cross. The scenario needs three
> demanding unanchored conditions: rad-tolerance at commodity cost (the strongest
> current data supports five-year TID survivability but leaves system
> reliability — SEE, training workloads, thermal, whole-spacecraft —
> unresolved [S32]), service life nearer 15 years than 5, and target-class
> launch or closure substituting for launch. The collector-area arithmetic
> is not the disputed part; the three demanding unanchored conditions are
> where the scenario lives.

Two conditions attach. **Demand saturation**: if the set of tasks worth
computing is bounded, demand saturates and the argument that space is the
only arena permitting unbounded deployment loses its motivation [S34]. The
physical ceilings bound how cheaply computation can be done; a demand
ceiling would bound how much is wanted — the more decisive and less
examined of the two. The non-saturation branch has a canonical published
statement [S35] and no resolution; the scenario is conditional on it.

The demand sensitivity therefore includes both cases rather than treating
non-saturation as a natural law. With identical compute supply growing 20%
per year, the illustrative non-saturating branch demands 86.74 units at year
20 against 38.34 available, whereas bounded valuable demand approaches its
six-unit ceiling and uses 5.94. A separate bounded branch directs 70% of
used compute to humanitarian applications before year 8, compared with 15%
in the industrial-priority branch. These allocation shares are normative
ASSUMPTION inputs, not forecasts or welfare optima. Machine-readable:
[compute demand allocation summary](../outputs/integrated/tables/compute_demand_allocation_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_demand_allocation_summary.csv"} and
[compute demand allocation trajectory](../outputs/integrated/tables/compute_demand_allocation_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_demand_allocation_trajectory.csv"}.

**The
upgrade asymmetry, narrowed**: software-layer improvements propagate to
deployed compute at near-zero marginal cost, but hardware-dependent gains
require replacement or retrofit — silicon is not upgraded in place. The
model consequence: the space-electronics obsolescence term would shrink
after convergence only for its software-limited share.

## IV.3 Paradigm shifts: delay, alteration, or prevention {#iv.3-paradigm-shifts-delay-alteration-or-prevention}

Catch-up time (a new paradigm must beat the incumbent plus decades of
compounded process learning, still improving as the newcomer matures) and
finiteness (irreversible-computation paradigms climb toward the same
ceiling; reversible computing is the stated exception) bound the leapfrog
objection. Exposure is concentrated in fabrication on 10–20-year horizons;
energy, labor, transport, and materials are less paradigm-sensitive —
substantially reusable, not immune. The fleet self-insures through its own
3–6-year depreciation; the fab carries the stranding risk — the penalty of
taking the lead.

General-purpose robotic manufacturing is a partial hedge because it is the
industry that builds industries: after a paradigm shift, the cheapest
retrofitter may be the actor able to build the next fab faster than a rival
builds its first. The corresponding strategy is to verticalize the less
paradigm-sensitive layers aggressively, preserve hardware generality and
retooling capacity at the paradigm-specific layer, and track retooling speed
alongside doubling time. The model check below shows that this hedge must be
pre-positioned; it cannot be improvised after a catastrophic electronics
loss.

> **Model check.** The paradigm-sensitivity split maps onto the model's
> sector structure: a shift perturbs the electronics column of the
> requirement matrix and the fab layer behind the vitamin imports — exactly
> the sector already identified as binding in the relevant architectures.
> Machine tools and robotics are necessary retooling capabilities, but all
> eight modeled physical production sectors are knockout-indispensable; the
> knockout experiment does not show that those two are uniquely more
> strategically valuable. Retooling speed is a
> **computed output** (`cutsets.retooling_time`), and it hardens this
> scenario's central risk into a result: destroying 90% of the electronics
> or machine-tools sector at any point on the
> central trajectory is **model-fatal** — a defined, horizon-relative label:
> worst-case growth has not returned positive within the tested 20-year
> post-knockout window while the unknocked counterfactual's stays positive,
> under both the myopic and receding-horizon allocators, and at optimistic
> values too. The computation tests a 20-year horizon under the stated
> deterministic configuration; it establishes no recovery *within that
> window*, not permanent impossibility — a longer horizon, resumed imports,
> altered plant design, larger initial surplus, or a lower knock fraction
> could change the outcome and are unswept.
> The mechanism is the electronics strategic-material gap: at electronics q-scale 0.10–0.30,
> replacement local capacity is a multi-decade-payback asset no plausible
> planning horizon rebuilds from current output. Only power stranding under
> optimistic values is a finite delay (~27 years lost). Conditional
> implication: within this scenario class, a paradigm shift that obsoletes
> the local electronics tier removes the self-expansion margin for at least
> a two-decade window unless Earth imports resume — so the leapfrog hedge
> must be pre-positioned (hardware generality, retooling-ready lines,
> retained umbilical capacity), because post-shift rebuild from inside the
> complex is not a path the model offers within any tested horizon.
> Caveats: deterministic values, 90% single-sector knockout, maximin
> allocation family, 20-year window; surplus-pinning (stage 3),
> knock-fraction sweeps, and longer-horizon recovery tests remain open
> follow-ups.

## IV.4 The alternative telos, and the properly conditional close {#iv.4-the-alternative-telos-and-the-properly-conditional-close}

One reading of the same physics reaches this document's destination from
opposite values: Earth is not a constrained platform to escape but a
uniquely valuable biosphere to protect — zone the planet for habitation,
site heavy industry and compute where there is no ecology to disturb
[S34]. Independent corroboration of the operating-wall mechanism comes
from the same quarter: data-center siting is politically contested over
electricity, water, and land. The physical argument is common to both
readings; only the telos differs — and this decouples P3 from P4: the
migration case can be made without any claim about one company's
intentions.

Off-world expansion is also not the unique high-value use of advanced
intelligence. Amodei's explicitly non-space vision prioritizes health,
poverty reduction, peace, governance, and human meaning [S79]. That
countercase prevents infrastructure scale from silently becoming a welfare
objective. Space can offer a long-horizon option for relocating harmful
activity, expanding physical capacity, and increasing resilience; whether it
dominates direct humanitarian uses is an allocation question this article
does not resolve.

That telos requires three separate welfare-relevant accounts rather than one
“activity moved to space” total:

::: {#eq:welfare-activity-accounts .equation}
$$
\mathbf A_W(t)
=\left(
A_{\mathrm{reloc}}(t),
A_{\mathrm{expand}}(t),
A_{\mathrm{hum}}(t),
A_{\mathrm{sci}}(t),
A_{\mathrm{ind}}(t)
\right).
$$
:::

$A_{\mathrm{reloc}}$ is harmful terrestrial activity displaced rather than
merely duplicated; $A_{\mathrm{expand}}$ is total activity above the initial
reference; and $A_{\mathrm{hum}}$, $A_{\mathrm{sci}}$, and
$A_{\mathrm{ind}}$ are compute allocated to humanitarian services,
science/public goods, and industrial expansion. The vector deliberately has
no scalar total: relocation may reduce biosphere harm, expansion can create
benefits and externalities, and allocation determines who receives the
resulting services. Ethical weights, distribution, rights, consent, and
opportunity costs require a social choice outside this engineering model.

The observed portfolio is consistent with an economic gradient toward
greater integration — discovery until convergence, deployment after it,
with space as one plausible arena under a demanding set of priced crossover
conditions. Present evidence does not establish that recursive off-world
industrial closure is the governing objective of the companies described in
Part III. The executable model says that recursion is feasible only under
assumptions that are
currently choices rather than measurements; the economics point to Earth
at every anchored value; and the observations that would change either
conclusion are named, ranked, and observable.

The portfolio audit sharpens that boundary into minimum cuts rather than a
coverage percentage. Public evidence is deepest in operating terrestrial
power, manufacturing, transport, electronics integration, maintenance, and
compute, but no modeled sector is off-world reproductively closed. The
decisive disclosed gaps are reproduction and calibration of semiconductor
process equipment/metrology; qualified local source lots, species-level
chemistry, gases, resists, optics, bearings, and material grades; local
production of electronics and industrial parent tools; and an off-world
repair, verification, spares, and transport-fleet reproduction chain.

Closing 17 partially adjacent rows while leaving any one indispensable
parent-tool chain open still leaves the system dependent. That
dependency-aware result—not “12 of 18” or any implied percentage—is the
relevant conclusion.

## Limitations and claim boundary {#limitations-and-claim-boundary}

The most robust outputs are structural within the implemented model:
balanced doubling is unit-invariant; the three-stage allocator has a unique
state transition; realized endpoints include same-step shocks; recoverable
scrap cannot exceed loss-specific retirement; and Part II is exactly affine
in launch price. Architecture comparisons, endpoint definitions, and
regeneration from fixed seeds are also auditable.

The substantive conclusions remain assumption-conditioned. In the
ten-sector model, the requirement matrix, homogeneous electronics-closure multiplier,
repair and recovery efficiencies, stockpiles, shock process, import profile,
and finite capture reservoir are not measured as a coupled industrial
system. Its scalar-anchor screen does not rank structural matrix
uncertainty, interactions, policy families, or all environments, and its
LEO model has neither an endogenous debris stock nor a depleted capture
reservoir.

The integrated layer adds a material-category-by-sector bill of materials,
source yields, Earth–Moon–orbit–asteroid transfer arcs, seed-mass and
composition-changing Pareto searches, a decomposed knowledge package,
observable autonomy gates, process-specific environment profiles,
construction and transport lags, cohort-resolved commissioning and yield
ramps, architecture-specific viable floors, independent sector allocation,
explicit repair, finite orbital feed, and shell-resolved debris. A separate
delivery diagnostic distinguishes delivered, staged, installed,
commissioned, failed, recovered, and operating seed states. These are model
features, not validated factories. Their bills of material, recoverable
yields, source throughput, autonomy/productivity gains, lag/ramp/repair
coefficients, intervention budget, source portfolio, transfer capacities,
environment responses, and collision kernels are declared assumptions. The
seed is minimum-mass only inside the enumerated architecture and design
alternatives. Seventeen material categories
do not resolve mineralogy, alloying routes, contamination, process
chemistry, purity ladders, tool wear, quality yield, or every consumable.
The electronics tiers remain aggregates rather than fabs and tool chains.
Documented elemental occurrence is not a grade distribution, recoverable
reserve, refining yield, or accessible asteroid portfolio.
The process-closure acceptance contract in
`params/process_closure_requirements.yaml` makes the missing graph explicit:
source lots, species, unit processes, grades, critical parts, parent tools,
transport legs, waste routes, evidence records, and eight binary gates. The
generated [process-closure gap register](../outputs/integrated/tables/process_closure_gap_register.csv){.artifact-link data-artifact="outputs/integrated/tables/process_closure_gap_register.csv"} remains wholly
`evidence_pending`; the contract does not itself supply those nodes or data.
The associated bundle evaluator rejects graphs that omit a grade, critical
part family, process stage, evidence hash, or independently witnessed gate.

The terrestrial rehearsal in I.9 remains a proposed validation protocol,
not an accomplished demonstration; its computed scenario is a requirements
case, not an experiment. Its machine-validated event and acceptance contract
is published in `params/rehearsal_protocol.yaml`, with the unexecuted public
matrix in [rehearsal acceptance matrix](../outputs/integrated/tables/rehearsal_acceptance_matrix.csv){.artifact-link data-artifact="outputs/integrated/tables/rehearsal_acceptance_matrix.csv"}.
The evidence-bundle evaluator likewise refuses a result unless every event
type and injected fault, archive and auditor hash, witnessed gate, and
parameter-replacement record is present.
Environment profiles change throughput, yield,
power, depreciation, and binding rows, but their multipliers do not simulate
granular mechanics, convection, melt behavior, vacuum welding, abrasive
dust, radiation damage, traction, or thermal-cycle physics. The
compute–intelligence loop remains phenomenological even though its gates are
expressed as observable task completion, intervention, diagnosis,
verification, engineering-cycle, yield, repair-success, and recovery
quantities. The shell model is a stress model, not a
conjunction-assessment or validated traffic simulation.

Part II includes communications and ground-network capex,
spacecraft-bus functions, program NRE, insurance, spectrum/regulatory cost,
disposal, residual value, thermal margins, workload boundaries, and separate
financing. Serviceability remains a scenario rather than an observed
property. A symmetric dynamic economics diagnostic couples technical space
capacity and its construction, transfer, and intervention demand to the same
investment, financing, learning, depreciation, regulatory-delay, and market
mechanics used for Earth. Its coefficients are assumption-class and neither
tested space case self-finances inside 40 years, so
[P3b — Mature high-closure economics](proposition:P3b){.proposition-ref}
remains unresolved
rather than inferred from physical compounding. The claim-level provenance
audit classifies reporting-derived Part II intervals as `ASSUMPTION`
wherever no source directly supports the modeled endpoints and
transformation. Every remaining non-`ASSUMPTION` anchor resolves through
`params/claim_provenance.yaml` to an exact locator, extracted value, units,
transformation, and persistent identifier; the generated public table is
[claim-provenance register](../outputs/tables/claim_provenance.csv){.artifact-link data-artifact="outputs/tables/claim_provenance.csv"}. This makes the evidence boundary
auditable, but it does not empirically calibrate the wide assumption ranges.
The economic-calibration contract in
`params/economic_calibration.yaml` defines architecture-specific evidence,
equal-workload fields, correlated fitting groups, audited dated cash flows,
chronological holdout validation, and the promotion rule. Its public
readiness table is entirely `data_pending`;
[P3b — Mature high-closure economics](proposition:P3b){.proposition-ref}
remains empirically open.
Its bundle evaluator requires all evidence packages, correlated fits,
holdouts, cash-flow event types, immutable hashes, and reviewed parameter
decisions; point estimates alone cannot satisfy it.
Finally, the Part III strategy assessment is ordinal and observational:
corporate filings and statements establish declared initiatives, not an
intent to achieve recursive closure. No result in this paper is a forecast
or an empirical probability of success.

* * *

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

# Appendix C: Reproducibility {#appendix-c-reproducibility}

    corepack pnpm install --frozen-lockfile
    corepack pnpm run setup:local-tools
    corepack pnpm run candidate:macos:update  # regenerate and review
    corepack pnpm run candidate:macos         # strict clean reproduction

Model: `src/rsimodel/{model,delta,cutsets,montecarlo,lco,policies,plots,report}.py`;
parameters: `params/{anchors,assumptions,environments}.yaml`; generated
reports with per-run provenance tables and machine-readable CSV summaries:
`outputs/` (headline table: [deep Monte Carlo table](../outputs/tables/mc_deep.csv){.artifact-link data-artifact="outputs/tables/mc_deep.csv"}). Stages 1–2 of
each allocation use HiGHS through a persistent warm-started model, with
`scipy.optimize.linprog` as the retained reference/fallback path and
`RSI_SLOW_LP=1` to force it. Stage 3 uses the pinned OSQP solver for the
strictly convex normalized tie-breaker, with a numerical fallback. All randomness
flows through explicitly seeded `numpy.random.Generator` instances; every
script derives its seeds from stable crc32 strings (never Python's
process-salted `hash()`), and each anchor's Monte Carlo
draw is keyed by the run seed plus the anchor's NAME, so results are stable
both across processes and under anchor-list growth. All tables regenerate
deterministically within the pinned Apple-silicon macOS reference environment.
`outputs/MANIFEST.md` records the sha256 of every release artifact,
including the canonical Markdown and standalone HTML, plus library versions;
it omits a self-referential generating-commit field. `tests/test_repro.py` cross-checks
the committed CSV against the committed report so mutually stale artifacts
fail the suite. `outputs/report_deep.md` and
[deep Monte Carlo table](../outputs/tables/mc_deep.csv){.artifact-link data-artifact="outputs/tables/mc_deep.csv"} are written by a single execution of one
script and cannot diverge. Structural coefficients are ASSUMPTION-class and
live only inside named assumption sets.

The integrated model is `src/rsimodel/integrated.py`, with the
analysis module in `src/rsimodel/integrated_analysis.py`, configured entirely
by `params/integrated_model.yaml` and run by the installed
`rsi-run-integrated` command.
`outputs/integrated/report.md`, 33 CSV tables, and five figures are
generated from one in-memory scenario set. `outputs/integrated/MANIFEST.md` records the
sha256 of the configuration, implementation, runner, focused tests, and
every generated artifact. Its ensemble uses 200 deterministic named draws
per scenario from seed 404. Adding a draw or changing a coefficient changes
the manifest; none of that upgrades an assumption to evidence.

**Archival status.** Public repository:
**[rsi-model repository](https://github.com/fperegrinvs/rsi-model)**. r4.0
is assembled as a release candidate but is not yet represented by a clean
release commit or tag; this text does not claim otherwise. The untagged
r4.0 HTML omits canonical/public URL,
publication-date, and `citation_doi` metadata rather than pointing at
mutable `blob/main` or mislabeling the concept DOI. The final tagged build
must supply an immutable URL, release date, and version DOI through the
documented build environment variables.
Dependency lockfile: `uv.lock` (numpy 2.1.3, scipy
1.16.0 [HiGHS], OSQP 1.1.3, PyYAML 6.0.3, matplotlib
3.10.3, pytest 9.0.3; Python 3.13.0 reference environment; complete
transitive pins and artifact hashes). The TypeScript publication toolchain
uses Bun 1.3.14, pnpm 11.17.0, and the checked `pnpm-lock.yaml`. Citation metadata:
`CITATION.cff`. License: MIT for code (`/LICENSE`), CC BY 4.0 for the
manuscript and documents (`docs/LICENSE`). DOI: concept
**10.5281/zenodo.21619447** (all versions); each release tag mints its own
version DOI via the Zenodo integration. The test suite covers selected
invariants, determinism, metric identities, artifact consistency, and the
generated HTML's semantic publication structure — they do not establish
that the specification adequately represents industrial reality, and no
test suite could.

# Appendix D: Complete model specification {#appendix-d-complete-model-specification}

Everything a reader needs to reconstruct the Part I model without opening
the implementation. Part II's cost model is fully specified by its affine
form (II.2) plus the anchor table (A.4), with two implementation details: the
annualization applies component-specific lives (compute hardware and its
replacement launch mass on `compute.life_years_space`; PV, radiator,
storage, structure, and their launch spend on
`power_systems.infrastructure_life_years`, floored at the hardware life —
the LCO remains exactly affine in launch $/kg), and each Monte Carlo
iteration resolves every anchor once per cached AnchorSet so Earth and
space share common physical draws while retaining separate financing
anchors. This appendix covers the multisector
dynamics and then specifies the paper layer that runs beside it.

## D.1 Integrated-bootstrap layer {#d.1-integrated-bootstrap-layer}

**State space.** The implementation has 18 sectors: power, mining,
refining, robotics, machine tools, construction, thermal, transport,
repair, recycling, interconnects/boards, passives/power,
sensors/control, packaging/test, mature logic, advanced logic/memory,
process equipment/metrology, and compute. It tracks 17 material categories:
O, Si, Al, Fe, Mg, Ca, Ti, H, C, N, Cu, Ni, Co, Cr, Li, rare earths, and
dopants — 15 elements plus two material classes, so the model is
material-category-resolved rather than element-resolved: stoichiometric
and process-chemical closure is not checked at the species level. The
full coefficient set is the machine-readable specification in
`params/integrated_model.yaml`.

**Material and service closure.** For material category $e$, sector $j$,
and source/transfer arc $a$:

::: {#eq:appendix-material-balance .equation}
$$
\Delta M_e
= \sum_s Y_{s,e}X_s + I_e + \sum_a F^{\mathrm{in}}_{a,e}
- \sum_j B_{e,j}x_j - L_e - \sum_a F^{\mathrm{out}}_{a,e},
$$
:::

where $B_{e,j}$ is the amount of material category $e$ required per unit
of sector-$j$ build, $Y_{s,e}$ is the recoverable yield from source and
process $s$, and $F_{a,e}$ is material flow across an Earth, lunar
surface, orbital, or asteroid transfer arc. Concentration alone does not
set $Y$; mineral form, beneficiation, refining energy, purity, and loss
remain outside the occurrence citations. Service closure uses
$A_{i,j}$, the sector-$i$ service output needed to build and replace
sector $j$. Recoverable lunar and asteroid yields, rather than bulk
inventory, enter the constraints. Earth material appears only as the
bounded initial strategic-material import stock $v_e$.

**Process environment and autonomy.** For each process $j$, task coverage
at AI level $I$ is

::: {#eq:task-coverage .equation}
$$
c_j(I)=\min\{c_j^{\max},\ c_j^0+\alpha_j\max(I-1,0)\}.
$$
:::

Effective productivity is multiplied by $(0.5+0.5c_j)$ — a declared
ASSUMPTION-class convention assigning fully scripted, conventionally
automated operation half of full productivity at zero unscripted-task
coverage, not a measured relation. Residual annual
intervention is $h_j(1-c_j)z_j$ and its sum must fit the scenario budget;
the linear form treats missing autonomy as smoothly divisible labor
demand and does not represent threshold effects, where one unrecoverable
diagnosis, calibration, or repair task stops a line despite high average
coverage.
Where declared required acceleration $g_j^\ast$ exceeds lunar gravity
$g_L=0.165g$, the acceleration gap adds centrifuge structural material
and parasitic power. The reported centrifuge speed follows

::: {#eq:centrifuge-speed .equation}
$$
\mathrm{rpm}_j=\frac{60}{2\pi}
\sqrt{\frac{9.80665\max(g_j^\ast-g_L,0)}{r_j}}.
$$
:::

This is an equipment penalty, not a claim that a whole lunar factory or
habitat requires artificial gravity.

**Seed sizing.** Decision variables are sector capacities $z_j$, annual
lunar and asteroid feed $p_L,p_A$, and initial Earth strategic-material
stocks $v_e$.
The linear program minimizes

::: {#eq:seed-mass-objective .equation}
$$
M_{\mathrm{seed}}
= M_{\mathrm{digital}}+\sum_j z_j\sum_e B_{e,j}^{\mathrm{eff}}
+\sum_e v_e,
$$
:::

subject to minimum viable sector capacities, task coverage and intervention
limits, service output sufficient for replacement plus one complete second
cell, element balances through each scenario horizon, and mining, refining,
transport, and energy throughput. Sector commissioning lags and half-ramp
loss reduce productive years. $M_{\mathrm{digital}}=5$ t represents the
software, simulation, industrial-memory, and experimental package; its
value is an assumption, not a storage-mass estimate.

The LP can also minimize Earth-import mass or intervention demand, using
installed mass as a lexicographic secondary objective. All three objectives
return the same central design in every LP-feasible scenario. This is not a
Pareto frontier: it shows that the present variables contain no alternative
process or redundancy choices capable of trading those objectives.

**Dynamic sector-capacity growth.** A feasible seed begins as one installed and
operating cell — delivery, unloading, site preparation, and first
commissioning are outside the model, so seed mass refers to an installed
operating nucleus, not a self-deploying delivered package. Each quarter,
lunar production, commissioned asteroid production, and recovered
retirement enter inventory. New orders use the complete balanced
sector-and-material vector of the seed design. For each sector $j$,
installed capacity $K_j$, operating capacity $O_j$, ordered capacity, its
declared commissioning lag, yield ramp, and depreciation $\delta_j$ remain
stateful. Retired material is recovered by category at the declared 82%
fraction. Lunar feed scales with operating mining, refining, and power;
asteroid feed additionally requires operating transport. An incomplete
packet contributes only the output $q_jO_j$ of sectors already operating.
The reported cell-equivalent aggregate is derived as
$\min_j O_j/z_j$, and the doubling threshold is first passage of that
minimum to 2.0. It is not the discrete commissioning of a second factory's
subsystems and not, by itself, evidence of sustained growth. Balanced
packets remain a restriction: the dynamic allocator cannot yet choose an
independent sector composition or explicit repair action.

Installed compute raises the model's normalized capability index according to
the implemented discrete update

::: {#eq:intelligence-update .equation}
$$
I_{t+\Delta t}
= \min\{I_{\max}, I_t
+\ell\,\nu_v(t)\,
\eta_{\mathrm{hw}}\eta_{\mathrm{util}}
\eta_{\mathrm{alg}}\eta_{\mathrm{arch}}\,
\log_2(1+C_t/C_0)
\left(\frac{I_{\max}-I_t}{I_{\max}-I_0}\right)^{\beta_I}
\Delta t\},
$$
:::

where $I_t$ is the dimensionless capability index at elapsed year $t$;
$I_0=1$ and $I_{\max}=3$ are the declared initial level and fixed-regime
frontier; $\ell=0.025$ is capability-index gain per verified-loop equivalent
at unit compute signal, unit frontier factor, and unit efficiency;
$\nu_v(t)=v\min_s\nu_s(t)$ is verified loops per year after the
$v=0.85$ verification yield and the train, data, experiment, evaluate,
safety, deploy, and observe stage bottleneck; and
$\eta_{\mathrm{hw}},\eta_{\mathrm{util}},\eta_{\mathrm{alg}},
\eta_{\mathrm{arch}}$ are dimensionless effective-compute ratios. $C_t$ is
installed compute capacity converted into the model's compute units, $C_0$ is
its initial value, $\beta_I=1.25$ is the frontier-gap curvature, and
$\Delta t=0.25$ yr. The train-stage rate alone scales with
$(C_t/C_0)^{1/2}$, capped at twice its baseline; the other stages do not
automatically accelerate with compute. Every coefficient in this update is
**ASSUMPTION**-class. It is a bounded sensitivity structure, not an empirical
law or a forecast of intelligence.

Intelligence above the scenario starting level raises both industrial
productivity and autonomy, which raises cell output and future compute.
Earth and Earth-fed orbital counterfactuals instead add capacity at constant,
scenario-specific build/delivery rates, subtract 0.16/yr depreciation, and
impose terrestrial site ceilings. Moon→orbit compute has a 0.5-year lag, a
35% share of new endogenous capacity, and a transport-capacity ceiling.

**Debris state.** A separate stress test evolves active assets, derelicts,
and a fragment index. Failures, controlled disposal, retrieval, collisions,
fragment creation, natural clearance, and active removal are explicit.
$R_{\mathrm{debris}}$ — the five-year fragment creation-to-clearance
ratio — is fragments created divided by fragments cleared
over the last five years: a flow ratio, not a branching-process
reproduction number. Realized
clearance is capped by the fragments available, so at an empty fragment
stock the ratio reads exactly one. The distributed case multiplies the collision
kernel by 0.01; it is therefore a declared topology test, not a derived
property of heliocentric space.

**Orbital lifecycle and common-cause controls.** A separate
capacity-equivalent mass-flow sensitivity implements Equation
[@eq:orbital-lifecycle-state] with the nine reported states operating,
degraded, awaiting service, under repair, cannibalized, salvaged, recycled
feedstock, disposed waste, and uncontrolled debris. Repairs return capacity
only after service start, completion, and repair yield; salvaged mass returns
to production only after recycling yield and manufacturing capacity.
Collision losses and disposed or recycling waste enter the irreversible-loss
diagnostic, while successful debris retrieval subtracts from it. Tests require
nonnegative stocks and conservation after external deployment is included.
This layer does not model mission-specific capture trajectories, qualification
of repaired hardware, or species-level recycling.

The common-cause control sensitivity evaluates Equation
[@eq:orbital-common-cause-budget] against explicit node capacities and hazard
sets. Its shell-state controller maps crossed thresholds to deterministic
actions: pause deployment and dispatch removal for creation/clearance,
hazardous-descendant, or derelict-mass violations; increase spacing and reserve
maneuver propellant for conjunction or maneuver violations; reduce cluster
caps and isolate failure domains when tracking or communications degrades; and
tighten disposal reliability or retire a shell after disposal violations.
Zero-valued conjunction, maneuver, tracking, and communications metrics in the
current table mean “not simulated by this run,” not observed safety.

**Scenarios and uncertainty.** The four named cases are terrestrial
rehearsal, lunar strategic-material bridge, strict lunar-only, and Moon–asteroid
network. Their horizons, AI levels, import caps, intervention budgets, and
source commissioning dates are all explicit in the YAML. Each 200-run
ensemble uses stable crc32 names from seed 404 to draw independent
log-uniform multipliers for service productivity, bills of material, lunar
and asteroid yield, depreciation, lag, and autonomy gap. Frequencies across
those draws are design-space occupancy, not empirical probabilities.
Tests verify dimensions, nonnegative balances, strict-lunar infeasibility,
finite-import-stock behavior, gravity overhead, aggregate-capacity
doubling, named-draw stability, and the
debris threshold. `outputs/integrated/MANIFEST.md` binds the configuration,
implementation, runner, tests, tables, figures, and report.

**Analysis module.** `src/rsimodel/integrated_analysis.py` adds derived
diagnostics over the same declared coefficients, inventing none:
terminal-window endpoints (retention at horizon, final-five-year net
capacity change, import-pool exhaustion timing); strategic-import-stock
resolution; zero/freeze intelligence-coupling ablations; the
installed-mass-versus-aggregate-doubling oversize frontier
(`simulate_capacity_growth(initial_cells=f)` installs f cell-equivalents of
the fixed minimum-mass design); per-draw ensemble diagnostics over the
identical named crc32 draws (failure reasons, binding-constraint
frequencies, Spearman sensitivity); and an elastic-relaxation
infeasibility certificate that interrogates the exact seed LP through a
shared matrix builder. The expanded module also compares independent
allocation and explicit repair, observable knowledge/autonomy outages,
process-environment profiles, finite-mass shell debris, policy and
structural-shock sweeps, shelf-limited electronics architectures, symmetric
dynamic economics, and composition-changing robust-seed Pareto designs.
The full table set and five figures regenerate with the run, including the
full sector trajectory and an 80-year central extension. These diagnostics
add structure and falsification plumbing; their coefficients remain
assumptions pending empirical calibration.

**Equation-review sensitivity module.** `src/rsimodel/extensions.py` implements
the newly explicit Part I relations without claiming calibration:

- [digital progress regimes](../outputs/integrated/tables/digital_progress_regimes.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_progress_regimes.csv"} compares smooth diminishing effort,
  fixed-frontier saturation, and discrete frontier-shift cases while reporting
  experiment, technical-validation, and internal-adoption throughput plus
  marginal gain separately;
- [internal/public capability trajectories](../outputs/integrated/tables/internal_public_capability_trajectories.csv){.artifact-link data-artifact="outputs/integrated/tables/internal_public_capability_trajectories.csv"} reports
  zero-lag, slower-publication, and internal-overhang assumption cases with
  separate internal/public capability and event clocks;
- [AI R&D compute allocation](../outputs/integrated/tables/ai_rd_compute_allocation.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rd_compute_allocation.csv"} conserves one physical accelerator-hour
  budget across training, research inference, experiments, data generation
  and filtering, verification and safety, and external productive service;
  compares raw-capability, verified-progress, and physical-growth objectives;
  and sweeps effective-compute conversion without creating physical hours;
- [cognitive physical labor table](../outputs/integrated/tables/cognitive_physical_labor.csv){.artifact-link data-artifact="outputs/integrated/tables/cognitive_physical_labor.csv"} separates model instances, inference
  capacity, robots/machines, experiment stations, and independently
  verifiable work cells; assigns surplus copies to nonphysical tasks or
  waiting/contention; and reports parallel and serial experiment time,
  coordination edges, duplicate work, onboarding, and verification demand;
- [AI electronics supply chain table](../outputs/integrated/tables/ai_electronics_supply_chain.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_electronics_supply_chain.csv"} decomposes the AI hardware chain into
  front-end logic, memory, advanced packaging, substrates/interposers,
  high-speed interconnect, power electronics, test/metrology, and
  radiation-qualified system integration, with heterogeneous shelf life,
  physical failure, obsolescence, local/import supply, reuse/down-bin,
  shortfall, closure sequence, and Earth-umbilical fields;
- [compute cohort summary](../outputs/integrated/tables/compute_cohort_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_cohort_summary.csv"} and [compute cohort trajectory](../outputs/integrated/tables/compute_cohort_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_cohort_trajectory.csv"} retain
  age/generation cohorts and separate physical failure, radiation-adjusted
  performance, economic frontier obsolescence, and reassignment to inference,
  verification, control, or non-frontier simulation under both continued
  hardware progress and an architectural-convergence branch;
- [verification hierarchy table](../outputs/integrated/tables/verification_hierarchy.csv){.artifact-link data-artifact="outputs/integrated/tables/verification_hierarchy.csv"} reports formal invariants, destructive
  physical acceptance, independent held-out experiments, causal operational
  outcomes, human/AI rubrics, and self-assessment separately, with candidate
  and verifier throughput, five evaluator-independence coordinates,
  false-positive stress, direction-setting capacity, and preservation of
  positive, negative, and null industrial-memory records;
- [industrial reliability ladder table](../outputs/integrated/tables/industrial_reliability_ladder.csv){.artifact-link data-artifact="outputs/integrated/tables/industrial_reliability_ladder.csv"} maps each task from single-attempt
  success through repeated, long-context, production, safety-field,
  unscripted-recovery, and sustained-operation evidence, with
  consequence-specific reliability, human checking/recovery/cleanup,
  rollback, intervention, and out-of-distribution recovery gates;
- [data evaluator coevolution table](../outputs/integrated/tables/data_evaluator_coevolution.csv){.artifact-link data-artifact="outputs/integrated/tables/data_evaluator_coevolution.csv"} separates synthetic generation,
  deduplication, filtering, provenance, evaluator error/bias, diversity,
  accepted signal, held-out transfer, physical causal episodes and their
  time/wear/sample/verification accounts, plus proprietary-data erosion
  through publication, espionage, mobility, distillation, and replication;
- [replication governance externalities summary](../outputs/integrated/tables/replication_governance_externalities_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/replication_governance_externalities_summary.csv"} and
  [replication governance externalities trajectory](../outputs/integrated/tables/replication_governance_externalities_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/replication_governance_externalities_trajectory.csv"} separate productive,
  legitimately authorized, unauthorized, and contested-resource-preempting
  capacity; track debris, remaining contested resources, declining material
  leverage, output claims, and externality costs; and evaluate engineering,
  private-objective, and governance endpoints independently;
- [digital channel ablations](../outputs/integrated/tables/digital_channel_ablations.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_channel_ablations.csv"}, [digital elasticity bounds](../outputs/integrated/tables/digital_elasticity_bounds.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_elasticity_bounds.csv"}, and
  [digital loop bottlenecks](../outputs/integrated/tables/digital_loop_bottlenecks.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_loop_bottlenecks.csv"} expose one-channel freezes, separately
  bounded elasticities with an explicit correlation matrix, and the binding
  verified-loop stage in each declared period;
- [digital release backtest table](../outputs/integrated/tables/digital_release_backtest.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_release_backtest.csv"} and
  [digital release backtest summary](../outputs/integrated/tables/digital_release_backtest_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_release_backtest_summary.csv"} fit the declared relations only on
  2020–2022 releases, score 2023 validation observations, and then expose a
  2024 holdout, with source locators and lower-bound inputs retained per row;
- [milestone order branches](../outputs/integrated/tables/milestone_order_branches.csv){.artifact-link data-artifact="outputs/integrated/tables/milestone_order_branches.csv"} keeps verified AI-R&D, embodiment,
  Earth/space reproductive-capital closure, and control readiness as separate
  clocks across four speed regimes and a terrestrial-first counterfactual;
- [closure loop ablation matrix](../outputs/integrated/tables/closure_loop_ablation_matrix.csv){.artifact-link data-artifact="outputs/integrated/tables/closure_loop_ablation_matrix.csv"} crosses the implemented verified
  AI-R&D proxy with permission to order new capital, proving that digital
  improvement and reproductive-capital closure are separate model switches;
- [authorized capacity control summary](../outputs/integrated/tables/authorized_capacity_control_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/authorized_capacity_control_summary.csv"} and
  [authorized capacity control trajectory](../outputs/integrated/tables/authorized_capacity_control_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/authorized_capacity_control_trajectory.csv"} keep task, coordination,
  evaluator, and controllability coordinates separate and constrain gross
  capacity by independent reliability, adversarial-verification,
  secure-command, environmental, treaty, and human-comprehension rates;
- [intelligence marginal response table](../outputs/integrated/tables/intelligence_marginal_response.csv){.artifact-link data-artifact="outputs/integrated/tables/intelligence_marginal_response.csv"} applies the same 0.1
  capability-index finite perturbation across material-starved,
  source-network, import-buffer, and operationally governed regimes while
  holding every other declared complement fixed;
- [bottleneck upgrade projects](../outputs/integrated/tables/bottleneck_upgrade_projects.csv){.artifact-link data-artifact="outputs/integrated/tables/bottleneck_upgrade_projects.csv"} and
  [bottleneck upgrade trajectory](../outputs/integrated/tables/bottleneck_upgrade_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/bottleneck_upgrade_trajectory.csv"} classify reducible, physical-floor,
  observation-time, and external-authority constraints and admit a capacity
  increment only after budget, productive-sector, causal-verification, and
  lag gates pass;
- [compute demand allocation summary](../outputs/integrated/tables/compute_demand_allocation_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_demand_allocation_summary.csv"} and
  [compute demand allocation trajectory](../outputs/integrated/tables/compute_demand_allocation_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_demand_allocation_trajectory.csv"} compare non-saturating and
  bounded valuable-demand paths plus an early humanitarian-priority branch,
  while keeping relocation, total expansion, and use allocation as separate
  welfare-relevant accounts rather than producing a welfare scalar;
- [intergenerational learning faults](../outputs/integrated/tables/intergenerational_learning_faults.csv){.artifact-link data-artifact="outputs/integrated/tables/intergenerational_learning_faults.csv"} runs repeated and structurally
  similar sensor, actuator, calibration, and communication faults across four
  controller generations while keeping transfer cases hidden and checking
  retention and prior-task regression;
- [digital learning feedback table](../outputs/integrated/tables/digital_learning_feedback.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_learning_feedback.csv"} feeds the synthetic campaign's measured
  latency, retention, transfer, recurrence, and verification cost into loop
  stage rates and verified yield while preserving its non-empirical status;
- [matched lifecycle cost contributions table](../outputs/integrated/tables/matched_lifecycle_cost_contributions.csv){.artifact-link data-artifact="outputs/integrated/tables/matched_lifecycle_cost_contributions.csv"} uses one category order for
  Earth and space, reports paired p10/p50/p90 values, ranks the central
  difference drivers, and labels unpriced categories as omissions;
- [data advantage profile](../outputs/integrated/tables/data_advantage_profile.csv){.artifact-link data-artifact="outputs/integrated/tables/data_advantage_profile.csv"} reports all seven normalized components,
  uncertainty widths, hard gates, and the visibly assumption-class geometric
  scalar;
- [coordination sensitivity](../outputs/integrated/tables/coordination_sensitivity.csv){.artifact-link data-artifact="outputs/integrated/tables/coordination_sensitivity.csv"} evaluates modular, centralized, and
  all-to-all dependency graphs across complexity, uncertainty, and effective
  intelligence, retaining the irreducible floor;
- [coordination form uncertainty](../outputs/integrated/tables/coordination_form_uncertainty.csv){.artifact-link data-artifact="outputs/integrated/tables/coordination_form_uncertainty.csv"} and
  [coordination form summary](../outputs/integrated/tables/coordination_form_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/coordination_form_summary.csv"} compare power, logarithmic-edge, and
  saturating-edge relations under common parameter draws and map the primary
  coordination-hours account once into schedule, output, reliability, and
  labor cost;
- [embodiment compatibility matrix](../outputs/integrated/tables/embodiment_compatibility_matrix.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_compatibility_matrix.csv"} separates failed physical dimensions,
  hardware ceilings, intelligence thresholds, verification, and first
  passage for every declared task and hardware portfolio;
- [embodiment two direction sweep table](../outputs/integrated/tables/embodiment_two_direction_sweep.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_two_direction_sweep.csv"} and
  [terrestrial rehearsal embodiment faults](../outputs/integrated/tables/terrestrial_rehearsal_embodiment_faults.csv){.artifact-link data-artifact="outputs/integrated/tables/terrestrial_rehearsal_embodiment_faults.csv"} vary intelligence and hardware
  independently and inject declared sensor, actuator, calibration,
  communication, tool, observability, and out-of-distribution degradations;
- [embodiment bill-of-materials requirements](../outputs/integrated/tables/embodiment_bom_requirements.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_bom_requirements.csv"} makes the assumed sensor, actuator,
  end-effector, spare, calibration-equipment, and local-controller material
  additions and annual replacement-service coefficients explicit by target
  sector;
- [orbital lifecycle states](../outputs/integrated/tables/orbital_lifecycle_states.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_lifecycle_states.csv"} reports the nine lifecycle stocks and the
  repair, recycling, retrieval, and irreversible-loss flows;
- [orbital lifecycle strategy comparison](../outputs/integrated/tables/orbital_lifecycle_strategy_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_lifecycle_strategy_comparison.csv"} exposes design-for-service and
  design-for-circularity variables rather than hiding them in a lower
  depreciation coefficient;
- [orbital transport service network](../outputs/integrated/tables/orbital_transport_service_network.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_transport_service_network.csv"} compares four named
  origin-destination routes using the rocket equation and reports maturity
  gates plus client-value, reliability, serviceability, fleet, recovery, and
  reuse sensitivities; [orbital transport break even surface table](../outputs/integrated/tables/orbital_transport_break_even_surface.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_transport_break_even_surface.csv"} crosses
  those axes over all four route and propellant-source architectures;
- [orbital service decision comparison](../outputs/integrated/tables/orbital_service_decision_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_service_decision_comparison.csv"} compares nine disposition actions
  over six orbit regimes, two asset classes, and three fleet architectures on
  one lifetime-output and risk boundary while keeping technical, economic,
  governance, and deployable gates separate;
- [orbital regime assumptions](../outputs/integrated/tables/orbital_regime_assumptions.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_regime_assumptions.csv"}, [orbital fleet amortization table](../outputs/integrated/tables/orbital_fleet_amortization.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_fleet_amortization.csv"}, and
  [orbital governance constraints](../outputs/integrated/tables/orbital_governance_constraints.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_governance_constraints.csv"} expose orbit-specific physics and
  disposal assumptions, fleet capacity/fixed-cost sharing, and authorization,
  liability, export, custody, provenance, and qualification dependencies;
- [orbital control policy table](../outputs/integrated/tables/orbital_control_policy.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_control_policy.csv"} reports common-cause budget compliance,
  shell-state triggers, and selected actions; and
- [orbital cluster layout optimization table](../outputs/integrated/tables/orbital_cluster_layout_optimization.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_cluster_layout_optimization.csv"} compares physical and logical
  failure-domain layouts over altitude, inclination, plane, spacing, shell,
  gateway, control, shared-service, communications, concentration, and
  common-cause dimensions;
- [orbital breakup cloud summary](../outputs/integrated/tables/orbital_breakup_cloud_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_breakup_cloud_summary.csv"} and
  [orbital breakup cloud trajectory](../outputs/integrated/tables/orbital_breakup_cloud_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_breakup_cloud_trajectory.csv"} propagate Earth-orbit and lunar-orbit
  clouds through explicit node geometry and report losses, expected secondary
  collisions, maneuvers, interruption, repair load, and restoration;
- [orbital degraded control stress](../outputs/integrated/tables/orbital_degraded_control_stress.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_degraded_control_stress.csv"} tests tracking, communications,
  navigation, and coordination failures before and after declared fallback
  actions;
- [orbital mitigation portfolio pareto](../outputs/integrated/tables/orbital_mitigation_portfolio_pareto.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_mitigation_portfolio_pareto.csv"} reports the complete 256-point,
  eight-axis mitigation surface and its three-objective non-dominated set;
- [orbital environment strategy comparison](../outputs/integrated/tables/orbital_environment_strategy_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_environment_strategy_comparison.csv"} prevents Earth-orbit and
  lunar-orbit clearance, tracking, residence, station-keeping, and disposal
  assumptions from being shared; and
- [orbital multi operator capacity table](../outputs/integrated/tables/orbital_multi_operator_capacity.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_multi_operator_capacity.csv"} applies shell carrying-capacity,
  authorization, tracking-data, maneuver, and disposal-compliance gates
  across multiple operators; and
- [partial closure metrics table](../outputs/integrated/tables/partial_closure_metrics.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_metrics.csv"} reports strict autonomy, mass closure,
  external-support intensity, import leverage, residual critical inputs, and
  the initial installed seed mass that is deliberately excluded from the
  ongoing-support autonomy indicator; and
- [partial closure support policies](../outputs/integrated/tables/partial_closure_support_policies.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_support_policies.csv"} and
  [partial closure dashboard](../outputs/integrated/tables/partial_closure_dashboard.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_dashboard.csv"} compare fixed, proportional, finite
  stockpile, and disrupted residual-import policies while placing autonomy,
  continuous closure, entry mass, supplier utilization, binding input,
  runway, and capacity loss in one view; and
- [partial closure substitution programs table](../outputs/integrated/tables/partial_closure_substitution_programs.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_substitution_programs.csv"} records threshold, ancestry,
  evidence, intelligence/embodiment/physical gates, probability-free outcome,
  and the resource-accounted expansion effort consumed by each dependency
  program;
- [partial closure supplier boundary table](../outputs/integrated/tables/partial_closure_supplier_boundary.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_supplier_boundary.csv"} places factories, materials, labor,
  energy, finance, transport, reliability, and growth inside the external
  support boundary; and
- [partial closure allocation policies](../outputs/integrated/tables/partial_closure_allocation_policies.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_allocation_policies.csv"} compares expansion-first,
  stockpile-first, balanced, and substitution-first uses of the same supported
  local base.

These tables are deterministic implications of
`params/integrated_model.yaml`. Each row carries its source class, and tests
cover domains, limiting cases, diminishing response, first-passage
attribution, conservation, graph effects, and control triggers.

## D.2 Ten-sector model {#d.2-ten-sector-model}

**Sectors and units.** n = 10 sectors, ordered: power, mining, refining,
robotics, machine_tools, electronics, thermal, transport, repair,
recycling. Capacity K_j is in abstract capacity units (K_j(0) = 1 for all
j unless stated); sector j produces q_j output units per capacity unit per
year (q below is the central set after environment q-scaling for the lunar
architecture is applied via `environments.yaml`; the tabulated q is the
pre-scaling set value). Repair and recycling are service sectors: their
rows in A are zero, and their outputs are consumed as described below.

**Time.** Discrete steps of Δt = 0.25 yr (0.5 yr for cut-set enumeration),
default horizon 35–40 yr. This layer has no construction lags,
commissioning delays, yield ramps, or minimum efficient scales — all its
outputs are stylized model outputs, not engineering timescale forecasts.

**Imports.** m_i(t) = B₀ · e^(−t/τ) · φ_i, with per-sector cutoffs
(m_i := 0 for i in the cut set after the cutoff year). Stockable sectors'
imports flow into the stockpile; non-stockable flow into the current
balance. Mars: stockable imports arrive as synodic batches of size
m·(2.14 yr) every 2.14 yr.

**Allocation (per step): three-stage lexicographic optimization.** Variables: builds
x ∈ ℝⁿ₊, wear-repair u ∈ ℝⁿ₊, recycling activity w ∈ ℝ₊, stockpile
drawdown d ∈ ℝⁿ₊ (d_i = 0 for non-stockable i), growth floor g ∈ ℝ.

Stage 1 — maximize g subject to:

::: {#eq:lexicographic-growth-stage .equation}
$$
\begin{aligned}
x_j + u_j - \delta_j K_j
  &\ge gK_j && \forall j, \\
u_j
  &\le \delta_{\mathrm{wear},j}K_j && \forall j, \\
\sum_j A_{ij}x_j
+ s_f\sum_j A_{ij}u_j
&\\[-0.2em]
\quad
+ \mathbf{1}_{i=\mathrm{repair}}\frac{1}{\eta_{\mathrm{rep}}}\sum_j u_j
+ \mathbf{1}_{i=\mathrm{recycling}}w
&\\[-0.2em]
\quad
+ o_iw-\rho_iw-d_i
  &\le q_iK_i+m_{\mathrm{direct},i} && \forall i, \\
w+\eta_{\mathrm{scrap}}\sum_j f_{\mathrm{wear},j}u_j
  &\le \eta_{\mathrm{scrap}}
  \sum_{j,c}f_{c,j}\delta_{c,j}K_j, \\
d_i
  &\le \frac{S_i}{\Delta t}.
\end{aligned}
$$
:::

with s_f = spares fraction (0.15), η_rep = repair efficiency (0.75
central), η_scrap = processing yield (0.40 central, < 1 always), o =
recycling opex vector, ρ = recycling output profile, and f_c,j = the
recoverable share of loss component c in sector j. Equivalently, available
retirement before processing is

::: {#eq:recoverable-retirement .equation}
$$
R(K,u)=\sum_{j,c}f_{c,j}\delta_{c,j}K_j
-\sum_j f_{\mathrm{wear},j}u_j.
$$
:::

The environment defaults are:

| environment | wear | catastrophic | obsolescence | logistics |
|---|---:|---:|---:|---:|
| LEO | 1.00 | 0.00 | 1.00 | 0.00 |
| lunar | 1.00 | 0.50 | 1.00 | 0.00 |
| Mars | 1.00 | 0.25 | 1.00 | 0.00 |
| Earth | 1.00 | 0.80 | 1.00 | 0.00 |

: Default environmental modifiers for the ten-sector model. {#tbl-d-environment-defaults}

Stage 2 holds g at its optimum and minimizes dimensionless stock draw
$\sum_i\omega_i d_i$, where $\omega_i$ is the inverse of a same-unit
scale based on current supply and available stock, normalized by the
largest weight. Stock is a buffer, not fuel, and the objective is invariant
to changes in sector row units.

Stage 3 holds the stage-1 and stage-2 optima within solver tolerance and
minimizes a strictly convex normalized action norm:

::: {#eq:normalized-tie-break .equation}
$$
\min\left[
\sum_j\frac{x_j^2+u_j^2}{\widehat K_j^2}
+\frac{w^2}{\widehat R^2}
+\sum_i\frac{d_i^2}{\widehat D_i^2}
+g^2\right].
$$
:::

All scales are positive state-derived quantities with numerical floors.
The positive-definite Hessian makes the selected action, and therefore the
state transition, unique. Stage 1 and 2 use HiGHS; stage 3 uses OSQP with a
public SLSQP fallback for rare narrow-face numerical failures.

**State updates and shocks.**

::: {#eq:state-updates .equation}
$$
\begin{aligned}
K_j &\leftarrow
\max\!\left(K_j+\Delta t\,(x_j+u_j-\delta_jK_j),10^{-9}\right), \\
S_i &\leftarrow
\operatorname{clip}\!\left(
S_i+\mathrm{inflow}_i-d_i\Delta t-\frac{S_i\Delta t}{L_i},
0,C_i
\right).
\end{aligned}
$$
:::

with shelf life L_i (electronics 5 yr central), capacity cap
C_i = c_years · Σ_j A[i,j] δ_j K_j (replacement demand), initial stock
S_i(0) = s_years · replacement demand at t = 0, stockable sectors only
(robotics, machine tools, electronics, repair). Common-cause shocks are
applied after this deterministic capacity update; the stock cap is then
recomputed from the damaged capacity. Reported timestamps and shock-log
timestamps are the step end $t+\Delta t$. The headline realized growth is

::: {#eq:realized-growth .equation}
$$
g_{\mathrm{real}}=
\min_j\frac{K_{j,\mathrm{postshock}}-K_{j,\mathrm{prestep}}}
{\Delta t\,K_{j,\mathrm{prestep}}},
$$
:::

while the allocator's pre-shock $g^*$ is retained separately as
`g_alloc`.

**Depreciation.** δ_j = δ_wear,j + δ_catastrophic,j + δ_obsolescence,j +
δ_logistics,j per environment (`environments.yaml`), anchored entries
resolved at geometric mids (deterministic) or loguniform draws (MC), one
shared draw per anchor per run. Obsolescence is included on the reading
that K is frontier-equivalent capacity (A.1's five-quantity separation).

**Shocks.** Per step and per shock class: N ~ Poisson(rate · Δt) events;
each multiplies K over its sector group by (1 − f), f ~ U(f_lo, f_hi).
Rates jittered ±30% per MC run (ASSUMPTION).

**Outcome definitions.** *Expanding at year 30*: realized
post-shock g > 0 at the step ending at year 30 — the instantaneous, weakest
endpoint; it does not preclude import- or stock-supported growth or
near-zero absolute capacity (a minimum-viable-scale criterion needs an
authorial threshold and is queued). The pre-shock allocation endpoint uses
`g_alloc` and is diagnostic only. *Sustained*: realized g > 0 at every
recorded step ending in years 25–30. *Earth-import cutoff*: a separate
central-set ensemble with all Earth imports cut at year 30; the endpoint is
realized g > 0 throughout 30–35 (stock draw permitted). LEO retains capture
feed and is labeled accordingly, not as autonomy.
*Balanced doubling* (headline replication metric): first t with
λ(t) = min_j K_j(t)/K_j(0) ≥ 2 — unit-invariant, requires every sector to
double in its own capacity units; it is not a claim that a complete second
physical seed has been commissioned. *Aggregate doubling* (continuity diagnostic): first t
with Σ_j K_j(t) ≥ 2 Σ_j K_j(0), measured against the supplied K(0) —
unit-dependent, reported alongside but never as "system replication".
Both doubling metrics are reported over all runs that ever reach the
criterion and conditioned on year-30 survivors — the difference is the
doubled-then-failed class.

**Binding sector and co-binding.** At each allocation step, each
material-balance supply is relaxed by 1% and stage 1 is re-solved. The
finite response $\Delta g_i$ is unit-invariant because both the
perturbation and row quantity scale together. Every positive response
within 5% of the largest forms the co-binding set and shares fractional
credit. If all responses are numerically zero, relative slack supplies a
display fallback only. The baseline and allocation-policy comparison use
the same definition.

**Central-set structural coefficients** (ASSUMPTION-class; conservative =
central with A×1.35, δ×1.4, τ=10 yr, and reduced repair/recycling/stock
scales; optimistic = A×0.75, δ×0.8, τ=25 yr, increased scales; full
machine-readable sets in `params/assumptions.yaml`):

| A[i,j] | pow | min | ref | rob | mt | el | th | tr | rep | rec |
|---|---|---|---|---|---|---|---|---|---|---|
| **pow** | 0.30 | 0.35 | 0.40 | 0.25 | 0.30 | 0.45 | 0.20 | 0.30 | 0.20 | 0.40 |
| **min** | 0.20 | 0.15 | 0.30 | 0.15 | 0.20 | 0.10 | 0.15 | 0.20 | 0.10 | 0.08 |
| **ref** | 0.25 | 0.20 | 0.15 | 0.25 | 0.30 | 0.30 | 0.20 | 0.25 | 0.18 | 0.20 |
| **rob** | 0.15 | 0.20 | 0.15 | 0.10 | 0.15 | 0.15 | 0.10 | 0.15 | 0.25 | 0.18 |
| **mt** | 0.10 | 0.10 | 0.10 | 0.20 | 0.10 | 0.25 | 0.10 | 0.10 | 0.30 | 0.22 |
| **el** | 0.08 | 0.06 | 0.06 | 0.20 | 0.15 | 0.10 | 0.08 | 0.12 | 0.15 | 0.10 |
| **th** | 0.05 | 0.05 | 0.08 | 0.05 | 0.05 | 0.10 | 0.05 | 0.05 | 0.06 | 0.15 |
| **tr** | 0.10 | 0.15 | 0.10 | 0.08 | 0.08 | 0.08 | 0.08 | 0.05 | 0.10 | 0.12 |
| **rep** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **rec** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **q** | 1.00 | 1.20 | 1.00 | 0.80 | 0.50 | 0.40 | 0.90 | 0.70 | 1.00 | 0.90 |
| **φ (import share)** | 0.00 | 0.00 | 0.05 | 0.10 | 0.20 | 0.55 | 0.05 | 0.00 | 0.05 | 0.00 |

: Central ten-sector input-output matrix and strategic import shares. {#tbl-d-input-output-matrix}

Column j of A is the recipe for one unit of sector-j capacity; rows are
the supplying sectors (pow=power, min=mining, ref=refining, rob=robotics,
mt=machine_tools, el=electronics, th=thermal, tr=transport, rep=repair,
rec=recycling).

## D.3 Consolidated notation {#d.3-consolidated-notation}

This register supplements the local “where” paragraphs; it does not replace
them. A symbol's definition is scoped to the model layer shown in the last
column. Reuse in a different layer requires an explicit subscript or a fresh
local definition. Roman labels inside subscripts identify named categories,
bold capitals and lowercase letters denote vectors or matrices where stated,
and $i,j,e,s,a,h,k,m,n,p$ are local indices whose domains are defined beside
the equation that uses them.

::: {.notation-register}

| symbol | meaning | units or admissible domain | first equation | model layer |
|---|---|---|---|---|
| $t,\Delta t,T$ | elapsed time, discrete step, and declared horizon | years; $\Delta t,T>0$ | Eq. [@eq:orbital-deployment] | shared time convention |
| $C_{\mathrm{orbit}}$ | commissioned orbital compute capacity | frontier-equivalent compute-capacity units | Eq. [@eq:orbital-deployment] | Executive Summary deployment |
| $q_c$ | compute capacity delivered per unit of Earth-to-orbit launch service | compute-capacity units per launch-service unit | Eq. [@eq:orbital-deployment] | Executive Summary deployment |
| $L_{E\rightarrow O}(t)$ | gross Earth-to-orbit launch-service flow | launch-service units/yr, $\ge0$ | Eq. [@eq:orbital-deployment] | Executive Summary deployment |
| $\delta_C$ | orbital compute-capacity depreciation rate | yr$^{-1}$, $\ge0$ | Eq. [@eq:orbital-deployment] | Executive Summary deployment |
| $H$ | installed productive hardware capacity | declared hardware- or capacity-equivalent units, $\ge0$ | Eq. [@eq:endogenous-hardware-growth] | conceptual hardware growth |
| $r,\delta_H$ | gross hardware reproduction rate and hardware depreciation rate | yr$^{-1}$, $\ge0$ | Eq. [@eq:endogenous-hardware-growth] | conceptual hardware growth |
| $\mathbf I_n^{\mathrm{int}},\mathbf I_r^{\mathrm{pub}},\mathbf G_n$ | internally available capability vector, publicly observable capability vector, and observed candidate gain | declared component scales; vector gain in the corresponding component scales | Eq. [@eq:digital-capability-update] | digital improvement |
| $z_n^{\mathrm{tech}},z_n^{\mathrm{int}},z_r^{\mathrm{pub}}$ | technical-validation, bounded-internal-authorization, and external/public-authorization indicators | binary indicators in $\{0,1\}$ with distinct evidence and authorization semantics | Eq. [@eq:digital-capability-update] | digital improvement |
| $\mathcal D_n,\mathcal A_n,\mathcal V_n$ | data, architecture/algorithm, and technical-verification state for attempt $n$; $\mathbf R_r$, $\tau(r)$, and $\mathcal E_r^{\mathrm{pub}}$ are the release mapping, selected internal state, and public evidence/exposure conditions | structured state, not scalar scores | Eq. [@eq:digital-capability-update] | digital improvement |
| $I_m,I_{m,0},A_m$ | held-out capability component, its starting value, and attainable fixed-regime improvement | one declared component scale; $A_m\ge0$ | Eq. [@eq:digital-saturating-frontier] | digital sensitivity |
| $C_{\mathrm{eff}},C_{m,0},\beta_m$ | cumulative effective effort, its scale constant, and curvature | equivalent useful FLOP; $C_{\mathrm{eff}}\ge0$, $C_{m,0},\beta_m>0$ | Eq. [@eq:digital-saturating-frontier] | digital sensitivity |
| $C_{\mathrm{train}}$ | realized physical training compute | FLOP, $\ge0$ | Eq. [@eq:effective-training-compute] | digital compute account |
| $\eta_{\mathrm{hw}},\eta_{\mathrm{util}},\eta_{\mathrm{alg}},\eta_{\mathrm{arch}}$ | hardware, utilization, algorithmic, and architecture efficiency relative to named baselines | dimensionless ratios, $\ge0$ | Eq. [@eq:effective-training-compute] | digital compute account |
| $N_{\mathrm{act}},D,k_{\mathrm{train}}$ | mean active parameters/token, training tokens, and training-compute proportionality factor | parameters, tokens, and FLOP/(parameter-token) | Eq. [@eq:effective-training-compute] | digital compute account |
| $\mathcal S_C,C_{\mathrm{tot}}^{\mathrm{phys}},C_s^{\mathrm{phys}},C_s^{\mathrm{eff}},\eta_s$ | compute-use set, conserved total physical accelerator hours, use-$s$ physical/effective hours, and conversion efficiency | set; accelerator-hours/yr; accelerator-hours/yr; baseline-equivalent hours/yr; ratio $\ge0$ | Eq. [@eq:ai-rd-compute-allocation] | AI-R&D compute allocation |
| $R_{\mathrm{eff}},c_R,U_R,\rho_R$ | effective automated researchers, inference hours per instance, useful-task limit, and candidate rate per researcher | instances; accelerator-hours/(instance-yr); task-equivalent instances; candidates/(instance-yr) | Eq. [@eq:ai-rd-compute-allocation] | AI-R&D compute allocation |
| $C_{\mathrm{inf}}^{\mathrm{phys}},C_{\mathrm{exp}}^{\mathrm{eff}},C_{\mathrm{data}}^{\mathrm{phys}},C_{\mathrm{ver}}^{\mathrm{phys}}$ | inference, effective experiment, data-generation/filtering, and verification compute allocations | accelerator-hours/yr or baseline-equivalent hours/yr as superscripted | Eq. [@eq:ai-rd-compute-allocation] | AI-R&D compute allocation |
| $c_{\mathrm{exp}},c_D,c_V,y_D,q_V,\tau_{\mathrm{serial}},\nu_{\mathrm{verified}}$ | compute per experiment/data/verification candidate, accepted-data yield, evaluator-independence yield, serial experiment cycle, and verified-progress rate | accelerator-hours/candidate; fractions; years/candidate; verified candidates/yr | Eq. [@eq:ai-rd-compute-allocation] | AI-R&D compute allocation |
| $M_i,p_i,N_i,D_i,C_{\mathrm{ref}},b_i$ | release-$i$ five-shot MMLU accuracy, chance-adjusted score, dense parameters, pretraining tokens, compute reference, and data-balance fraction | percentage points; fraction $(0,1)$; parameters; tokens; FLOP; fraction $(0,1]$ | Eq. [@eq:chronological-release-backtest] | chronological release backtest |
| $\beta_0,\beta_C,\beta_B$ | fitted intercept, log-compute coefficient, and log-balance coefficient | dimensionless on the chance-adjusted logit scale | Eq. [@eq:chronological-release-backtest] | chronological release backtest |
| $T_{\mathrm{AIR\&D}},T_{\mathrm{emb}},T_{\mathrm{cl},E},T_{\mathrm{cl},S},T_{\mathrm{ctrl}}$ | verified AI-R&D closure, embodiment closure, Earth/space reproductive-capital closure, and control-readiness milestones | elapsed years, each $\ge0$ | Eq. [@eq:milestone-control-gate] | milestone-order screen |
| $\Gamma_{\mathrm{ctrl}}$ | branch-level control-admissibility indicator | $\{0,1\}$ | Eq. [@eq:milestone-control-gate] | milestone-order screen |
| $I_{\mathrm{task}},I_{\mathrm{coord}},I_{\mathrm{eval}},p_{\mathrm{ctrl}}$ | task, coordination, and evaluator capability coordinates plus controllability confidence | declared capability indices; probability in $[0,1]$ | Eq. [@eq:authorized-capacity-control] | authorized-capacity control |
| $K_{\mathrm{gross}},K_{\mathrm{auth}},K_{\mathrm{unauth}}$ | gross, authorized, and unauthorized operating capacity | capacity units, each $\ge0$ | Eq. [@eq:authorized-capacity-control] | authorized-capacity control |
| $\dot K_{\mathrm{gross}}^{+},a_K$ | proposed positive gross-capacity addition rate and required high-impact actions per added capacity | capacity/yr; actions/capacity | Eq. [@eq:authorized-capacity-control] | authorized-capacity control |
| $V_{\mathrm{rel}},V_{\mathrm{adv}},C_{\mathrm{cmd}},E_{\mathrm{env}},L_{\mathrm{treaty}},H_{\mathrm{human}}$ | reliability verification, adversarial verification, secure command, environmental limit, treaty limit, and human-comprehension throughput | high-impact authorization actions/yr, each $\ge0$ | Eq. [@eq:authorized-capacity-control] | authorized-capacity control |
| $K_{\mathrm{prod}},K_{\mathrm{auth}},K_{\mathrm{unauth}},K_{\mathrm{preempt}}$ | productive, legitimately authorized, unauthorized, and contested-resource-preempting capacity | capacity units, each $\ge0$ | Eq. [@eq:replication-governance-gate] | replication governance |
| $\Gamma_{\mathrm{gov}},\bar u,\bar p$ | governance-endpoint indicator and maximum unauthorized/preemptive capacity shares | $\{0,1\}$; fractions in $[0,1]$ | Eq. [@eq:replication-governance-gate] | replication governance |
| $L_{\mathrm{claim}},\bar L,\phi_{\mathrm{ext}},\bar\phi$ | resource-claim legitimacy and its floor; externality-cost internalization and its floor | normalized fractions in $[0,1]$ | Eq. [@eq:replication-governance-gate] | replication governance |
| $\mathcal G,g_j$ | required governance-gate set and gate-$j$ pass indicator | finite set; $g_j\in\{0,1\}$ | Eq. [@eq:replication-governance-gate] | replication governance |
| $\operatorname{MP}_{I}^{(r)},K_r,I_{r,0},\Delta I,\mathbf X_r$ | regime-$r$ finite marginal response, endpoint capacity, baseline intelligence, capability perturbation, and fixed complement vector | capacity/capability-index; capacity; capability index; capability index; declared mixed-unit state vector | Eq. [@eq:marginal-intelligence-response] | intelligence marginal response |
| $\Delta B_p,\Delta\bar B_p,\tau_{p,\mathrm{design}},\tau_{p,\mathrm{build}},\tau_{p,\mathrm{verify}}$ | commissioned and proposed bottleneck increment plus design, construction, and verification lags for project $p$ | capacity; capacity; years | Eq. [@eq:bottleneck-upgrade-gate] | bottleneck upgrade |
| $C_p,\bar C_p,P_p,V_p$ | project cost, available productive-capacity budget, productive-sector gate, and verified-causal-path gate | capacity-years; capacity-years; $\{0,1\}$; $\{0,1\}$ | Eq. [@eq:bottleneck-upgrade-gate] | bottleneck upgrade |
| $\mathbf A_W,A_{\mathrm{reloc}},A_{\mathrm{expand}},A_{\mathrm{hum}},A_{\mathrm{sci}},A_{\mathrm{ind}}$ | welfare-relevant activity-account vector: relocated harmful activity, expanded activity, and humanitarian, science/public-goods, and industrial compute allocations | declared compute/activity units, each $\ge0$ | Eq. [@eq:welfare-activity-accounts] | demand and allocation sensitivity |
| $\nu_v,\nu_s$ | verified-loop throughput and required stage-$s$ capacity | completed-loop equivalents/yr, $\ge0$ | Eq. [@eq:verified-loop-bottleneck] | digital loop |
| $\nu_{v,k},\nu_{\mathrm{candidate},k},\nu_{\mathrm{capacity},k},y_k,f_k,q_k$ | independently supported throughput, candidate and verifier capacity, acceptance yield, false-positive fraction, and evaluator independence for verifier class $k$ | iterations/yr; iterations/yr; iterations/yr; fractions in $[0,1]$ | Eq. [@eq:verification-hierarchy] | verification hierarchy |
| $\nu_{\mathrm{licensed},k},\nu_{\mathrm{direction}},\nu_{\mathrm{execution}}$ | licensed loop rate for verifier class $k$, research direction-setting rate, and fixed-target execution rate | completed-loop or task equivalents/yr, each $\ge0$ | Eq. [@eq:verification-hierarchy] | verification hierarchy |
| $S_g,V_g^{\mathrm{syn}},d_g,y_g,p_g,e_g,D_g,N_g^{\mathrm{phys}},c_g$ | accepted training signal; generated synthetic records; deduplication, filter acceptance, provenance, evaluator error, and diversity factors; physical episodes; causal linkage | signal units; records; fractions in $[0,1]$; episodes; fraction in $[0,1]$ | Eq. [@eq:accepted-training-signal] | data/evaluator coevolution |
| $\mathbf E,\mathbf R_k,\mathcal E$ | embodiment capabilities, task-$k$ requirements, and operating environment | matched normalized or physical dimensions | Eq. [@eq:embodiment-adequacy-gate] | embodiment compatibility |
| $\mathcal P_k,A_k$ | task-$k$ hard-gate dimensions and physical-adequacy indicator | set; $A_k\in\{0,1\}$ | Eq. [@eq:embodiment-adequacy-gate] | embodiment compatibility |
| $S_k,S_{k,\max},\bar S_k$ | verified task score, hardware-imposed ceiling, and required score | normalized $[0,1]$ | Eq. [@eq:intelligence-embodiment-compatibility] | embodiment compatibility |
| $I,I_{k,0},\sigma_k$ | effective task intelligence, onset, and response scale | same declared capability-index scale; $\sigma_k>0$ | Eq. [@eq:intelligence-embodiment-compatibility] | embodiment compatibility |
| $I_k^\ast,T_k^\ast,V_k(t)$ | intelligence threshold, verified first-passage year, and verification indicator | capability index; years; $\{0,1\}$ | Eq. [@eq:embodied-task-first-passage] | embodiment compatibility |
| $\mathbf d,d_j$ | seven-component operational-data-advantage profile and component $j$ | normalized $[0,1]$ with uncertainty interval | Eq. [@eq:data-advantage-profile] | industrial memory/data |
| $\kappa_D,F$ | optional data-advantage aggregate and declared aggregation rule | dimensionless; not measured unless calibrated | Eq. [@eq:data-advantage-profile] | industrial memory/data |
| $a_{\min},c_{\min},v_{\min}$ | access, causal-linkage, and verification hard gates | normalized $[0,1]$ | Eq. [@eq:data-advantage-scalarization] | industrial memory/data |
| $w_j,\mathcal J_D$ | component weights and included data-component set | $w_j\ge0$, $\sum_jw_j=1$ | Eq. [@eq:data-advantage-scalarization] | industrial memory/data |
| $C_e(u,T)$ | discounted matched lifecycle cost in environment $e$ for functional output $u$ over horizon $T$ | constant-currency dollars per declared functional unit | Eq. [@eq:matched-lifecycle-cost] | conceptual lifecycle cost |
| $\mathcal K,C_{k,e}^{\mathrm{external}},C_{k,e}^{\mathrm{internal}}$ | common cost-category set and external-purchase/internal-opportunity-cost streams | constant-currency dollars by dated cash flow | Eq. [@eq:matched-lifecycle-cost] | conceptual lifecycle cost |
| $\operatorname{PV}_e,V_{\mathrm{residual},e}$ | environment-specific present-value operator and terminal residual value | constant-currency dollars at declared discount convention | Eq. [@eq:matched-lifecycle-cost] | conceptual lifecycle cost |
| $R_C,\Delta_C$ | space/Earth cost ratio and difference under the same functional unit | dimensionless; constant-currency dollars/unit | Eq. [@eq:matched-lifecycle-cost] | conceptual lifecycle cost |
| $a_c,\omega,R$ | centrifugal acceleration, angular speed, and rotor radius | m/s$^2$, rad/s, m | Eq. [@eq:centrifugal-acceleration] | process physics |
| $\delta_{\mathrm{total}},\delta_{\mathrm{wear}},\delta_{\mathrm{catastrophic}},\delta_{\mathrm{obsolescence}},\delta_{\mathrm{logistics}}$ | total and component depreciation hazards | yr$^{-1}$, each $\ge0$ | Eq. [@eq:depreciation-decomposition] | lifecycle/depreciation |
| $\mathbf x_t,\mathbf Q_t,\mathbf b_t$ | nine-state orbital lifecycle stock, transition-rate matrix, and external flow vector | capacity-equivalent mass; yr$^{-1}$; capacity-equivalent mass/yr | Eq. [@eq:orbital-lifecycle-state] | orbital lifecycle |
| $(O,D,A_s,R,C,S,F,W,U)$ | operating, degraded, awaiting-service, under-repair, cannibalized, salvaged, recycled-feedstock, disposed-waste, and uncontrolled-debris stocks | capacity-equivalent mass, each $\ge0$ | Eq. [@eq:orbital-lifecycle-state] | orbital lifecycle |
| $\delta_{\mathrm{irr}}^{(T)},\dot W_{\mathrm{unrecoverable}},\dot U_{\mathrm{unrecoverable}}$ | horizon-average irreversible-loss rate and unrecoverable waste/debris flows | yr$^{-1}$; capacity-equivalent mass/yr | Eq. [@eq:effective-irreversible-loss] | orbital lifecycle |
| $V^{\mathrm{net}}_{aocf},p_a,V^{\mathrm{out}}_{aoc},L^{\mathrm{avoid}}_{ac}$ | net service-decision value, action failure probability, lifetime output value, and avoided replacement launch | real-2025 MUSD/client event; fraction; MUSD; MUSD | Eq. [@eq:orbital-service-decision-value] | orbital service decision |
| $C^{\mathrm{variable}}_{ao},C^{\mathrm{fixed}}_f,N_{of},T_f,C^{\mathrm{route}}_{of},C^{\mathrm{down}}_{ac},C^{\mathrm{risk}}_{aoc},C^{\mathrm{depr}}_{ac}$ | variable service, fleet fixed cost, annual clients, fleet life, routing, downtime, risk/liability, and depreciation | real-2025 MUSD; MUSD; clients/yr; years; MUSD/client event | Eq. [@eq:orbital-service-decision-value] | orbital service decision |
| $L_{\max},\mathcal H_t,K_i,K_{\mathrm{total}},\epsilon$ | maximum single-event capacity loss, credible hazard sets, node/total service capacity, and loss budget | capacity units; set; capacity units; fraction in $(0,1)$ | Eq. [@eq:orbital-common-cause-budget] | orbital controls |
| $T_{\mathrm{replenish},j},T_{\mathrm{effective\ survival},j}$ | critical-component replenishment and effective survival times | years, $>0$ | Eq. [@eq:critical-component-replenishment] | closure test |
| $P,D,g_H$ | gross capacity production, capacity loss, and net fractional growth | capacity units/yr; capacity units/yr; yr$^{-1}$ | Eq. [@eq:net-capacity-growth] | closure/growth |
| $\kappa$ | mass- or category-specific closure ratio under a declared account | fraction $[0,1]$ | Eq. [@eq:closure-ratio] | closure profile |
| $A_{\mathrm{aut}},\mathcal J_{\mathrm{crit}}$ | strict-autonomy indicator and critical-input set | $\{0,1\}$; set | Eq. [@eq:closure-and-import-leverage] | partial closure |
| $\dot m_j^{\mathrm{external}},\dot H_{\mathrm{verified}}$ | external input-$j$ mass flow and verified capacity-addition flow | kg/yr; capacity units/yr | Eq. [@eq:closure-and-import-leverage] | partial closure |
| $\sigma_{\mathrm{ext}},\Lambda_{\mathrm{import}}$ | external-support intensity and reciprocal import leverage | kg/capacity unit; capacity units/kg | Eq. [@eq:closure-and-import-leverage] | partial closure |
| $\mathbf K_t,\mathbf y^{\mathrm{local}},\mathbf B\mathbf u_t,\boldsymbol\delta_t$ | commissioned sector capacity, local capacity-addition flow, import-enabled flow, and sector depreciation | capacity vector; capacity/yr; capacity/yr; yr$^{-1}$ | Eq. [@eq:externally-supported-capacity] | integrated capacity |
| $B_{\mathrm{coord}},B_{\mathrm{irred}},B_0$ | coordination work, irreducible floor, and reference reducible work | agent-hours per verified cell-equivalent, $\ge0$ | Eq. [@eq:coordination-workload] | coordination |
| $E_G,E_0,\chi,\chi_0,u,u_0$ | active dependency-edge weight and reference, operational complexity and reference, uncertainty and reference | dimensionless indexed observables; references $>0$ | Eq. [@eq:coordination-workload] | coordination |
| $I_{\mathrm{eff}},I_0,\alpha,\beta,\gamma,\delta,\eta$ | effective coordination capability, reference, elasticities, and intelligence response | dimensionless; references/exponents/response $>0$ | Eq. [@eq:coordination-workload] | coordination |
| $B_{\mathrm{sensing}},B_{\mathrm{latency}},B_{\mathrm{synchronization}},B_{\mathrm{safety}},B_{\mathrm{verification}},B_{\mathrm{contention}}$ | irreducible coordination-work accounts | agent-hours per verified cell-equivalent, each $\ge0$ | Eq. [@eq:coordination-burden] | coordination |
| $N_{\mathrm{phys}}^{\mathrm{eff}},N_{\mathrm{model}},N_{\mathrm{inf}},N_{\mathrm{robot}},N_{\mathrm{sensor}},N_{\mathrm{safe}},N_{\mathrm{task}},N_{\mathrm{tool}},N_{\mathrm{vcell}}$ | effective physical agents and limiting model, inference, robot/machine, sensor, safe-envelope, task, tool/material, and verifiable-cell stocks | simultaneous instance/channel counts, each $\ge0$ | Eq. [@eq:cognitive-physical-labor] | cognitive-to-physical labor |
| $T_{\mathrm{experiment}},d_{\mathrm{serial}},\tau_{\mathrm{phys}},N_{\mathrm{indep}},P_{\mathrm{experiment}}$ | experiment-program wall time, serial depth, physical-cycle time, independent experiment count, and parallel station capacity | years; steps; years/step; experiments; simultaneous experiments | Eq. [@eq:cognitive-physical-labor] | cognitive-to-physical labor |
| $H_{\mathrm{created}}$ | cumulative gross hardware created before losses | hardware-equivalent units, $\ge0$ | Eq. [@eq:cumulative-created-hardware] | conceptual hardware growth |
| $r(I,E,M)$ | gross hardware reproduction rate conditional on intelligence, energy, and materials | yr$^{-1}$, $\ge0$ | Eq. [@eq:coupled-hardware-growth] | conceptual hardware growth |
| $M_e,Y_{s,e},X_s,I_e,L_e$ | inventory change, recoverable yield, processed-source amount, bounded import, and loss for material category $e$ | tonnes/category over the declared step; compatible coefficients | Eq. [@eq:material-balance] | integrated material balance |
| $F_{a,e}^{\mathrm{in/out}}$ | material-category flow on transfer arc $a$ | tonnes over the declared step, $\ge0$ | Eq. [@eq:material-balance] | integrated material balance |
| $B_{e,j},x_j$ | material category $e$ required per unit sector-$j$ build and sector build amount | tonnes/capacity unit; capacity units | Eq. [@eq:material-balance] | integrated material balance |
| $\operatorname{CRF}(r,T),f_o,a(T)$ | capital-recovery factor, fixed annual opex fraction, and annualization factor | yr$^{-1}$ | Eq. [@eq:capital-recovery-factor] | Part II cost |
| $L_s,L_E$ | space and Earth levelized lifecycle cost | constant-2025 USD per delivered kW-year | Eq. [@eq:space-lifecycle-cost] | Part II cost |
| $C_h,C_I,M_h,M_I,T_h,T_I$ | space hardware/infrastructure capital, launch mass, and component lives | USD/kW; kg/kW; years | Eq. [@eq:space-lifecycle-cost] | Part II cost |
| $a_s(T),f_o,f_{\mathrm{ins}},\rho,C_{\mathrm{reg}}$ | space annualization multiplier, annual operations and insurance fractions, residual fraction, and regulatory flow | dimensionless except $C_{\mathrm{reg}}$ in constant-2025 USD/kW-yr | Eq. [@eq:capital-recovery-factor] | Part II cost |
| $p_L,\mu,U_s,\alpha,\beta$ | launch price, launch mass multiplier, utilization/availability factor, affine intercept, and slope | USD/kg; dimensionless; dimensionless; USD/kW-yr; kg/kW-yr | Eq. [@eq:space-lifecycle-cost] | Part II cost |
| $\phi_e,C_{h,e},C_{DC},p_e,\psi_e,U_E$ | Earth financing multiplier, hardware/data-center capital, electricity price, PUE, and utilization/availability | dimensionless; USD/kW; USD/kWh; dimensionless | Eq. [@eq:earth-lifecycle-cost] | Part II cost |
| $p_L^\ast$ | launch-price break-even under the affine space-cost model | constant-2025 USD/kg | Eq. [@eq:launch-price-break-even] | Part II cost |
| $I_t,\mathbf c_t,\mathbf K_t,C_t,\mathbf R_t,E_t,H_t,D_t,V_t,\tau_x,\boldsymbol\delta_K,\delta_C,\Gamma_{x,t},\Pi,f_x,\theta_x,G_{\mathrm{loc}},\epsilon_{xy},\rho(J_t)$ | intelligence, task-coverage, productive-capacity, and usable-compute states; limiting resources, energy, compute hardware, data, and verification; delays, depreciation, active gates, ceiling projection, saturating response functions and parameters; and local elasticity/Jacobian amplification diagnostics | capability index; task fractions; sector-capacity vector; usable-compute units; declared resource-state units; years; rates/yr; gates in $[0,1]$; state-preserving mappings; dimensionless local diagnostics | Eq. [@eq:coupled-rsi-system] | front-matter causal system and integrated implementation |
| $c_j,c_j^0,c_j^{\max},\alpha_j$ | process task coverage, baseline, ceiling, and AI-level slope | fractions in $[0,1]$; slope per capability-index unit | Eq. [@eq:task-coverage] | integrated bootstrap |
| $\mathrm{rpm}_j,g_j^\ast,g_L,r_j$ | centrifuge speed, required acceleration, lunar gravity fraction, and rotor radius | rpm; multiples of Earth $g$; multiples of Earth $g$; m | Eq. [@eq:centrifuge-speed] | integrated bootstrap |
| $M_{\mathrm{seed}},M_{\mathrm{digital}},z_j,v_e,B_{e,j}^{\mathrm{eff}}$ | installed seed mass, digital package, sector capacities, strategic-import stocks, and environment-adjusted bill of materials | tonnes; tonnes; capacity units; tonnes; tonnes/capacity unit | Eq. [@eq:seed-mass-objective] | integrated bootstrap |
| $I_t,I_{\max},\ell,\beta_I$ | implemented capability index, fixed-regime frontier, gain scale per verified loop, and frontier curvature | dimensionless; dimensionless; capability/loop; positive exponent | Eq. [@eq:intelligence-update] | integrated bootstrap |
| $C_t,C_0$ | installed compute and its initial reference | model compute-capacity units, $C_0>0$ | Eq. [@eq:intelligence-update] | integrated bootstrap |
| $K_j,q_j,A_{i,j},\delta_j$ | sector capacity, output rate, input-service coefficient, and depreciation | capacity units; output/(capacity-yr); input-output coefficient; yr$^{-1}$ | Eq. [@eq:lexicographic-growth-stage] | ten-sector model |
| $x_j,u_j,w,d_i,g$ | build, wear repair, recycling activity, stock draw, and lexicographic growth floor | capacity/yr; capacity/yr; service/yr; output/yr; yr$^{-1}$ | Eq. [@eq:lexicographic-growth-stage] | ten-sector model |
| $s_f,\eta_{\mathrm{rep}},\eta_{\mathrm{scrap}},o_i,\rho_i,f_{c,j}$ | spares share, repair/recycling efficiencies, recycling input/output profiles, and recoverable loss share | dimensionless fractions or compatible service coefficients | Eq. [@eq:lexicographic-growth-stage] | ten-sector model |
| $R(K,u)$ | recoverable retirement flow before processing | capacity-equivalent recoverable material/yr | Eq. [@eq:recoverable-retirement] | ten-sector model |
| $\widehat K_j,\widehat R,\widehat D_i$ | positive state-derived normalization scales for the tie-break | same units as the normalized variable, all $>0$ | Eq. [@eq:normalized-tie-break] | ten-sector model |
| $S_i,L_i,C_i$ | stockpile, shelf life, and stock cap | sector-output units; years; sector-output units | Eq. [@eq:state-updates] | ten-sector model |
| $g_{\mathrm{real}},K_{j,\mathrm{prestep}},K_{j,\mathrm{postshock}}$ | realized minimum sector growth and pre-step/post-shock capacities | yr$^{-1}$; capacity units | Eq. [@eq:realized-growth] | ten-sector model |

: Consolidated symbol, meaning, domain and first-use register. {#tbl-d-notation-register}

:::

Universal mathematical operators ($\sum,\prod,\min,\max,\inf,\exp,\log$),
constants, comparison signs, and local integration or summation dummies are
intentionally omitted. Acronyms used outside mathematics are defined in the
Glossary.

# Glossary {#glossary}

## Proposition register {#proposition-register}

This compact register is validated against the canonical proposition ladder;
each descriptive link returns to the definition and current status.

<!-- proposition-register:start -->
| proposition | current evidential status |
|---|---|
| [P1 — Conceptual possibility](proposition:P1){.proposition-ref} | A respectable conceptual case is made; no demonstrated closure is required. |
| [P2 — Technical feasibility](proposition:P2){.proposition-ref} | Quantitatively explored across named assumption sets; complete-system feasibility is not demonstrated. |
| [P3a — Earth-dependent bridge economics](proposition:P3a){.proposition-ref} | Quantified and negative at anchored values; crossover requires a specific, currently unanchored parameter corner. |
| [P3b — Mature high-closure economics](proposition:P3b){.proposition-ref} | Scenario-modeled but unresolved; neither tested space case becomes self-financing inside 40 years under the declared assumptions. |
| [P4a — Documented portfolio direction](proposition:P4a){.proposition-ref} | The portfolio direction is documented; shared technical interfaces, binding milestones, and joint resource allocation are not publicly established. |
| [P4b — Recursive-closure intent](proposition:P4b){.proposition-ref} | Inferential; no closure program, seed bill of materials, reproduction metric, or minimum-cut roadmap is published. |

: Canonical proposition definitions and current evidential status. {#tbl-g-proposition-register}

<!-- proposition-register:end -->

## Technical terms {#glossary-technical-terms}

**Recursive self-improvement (RSI):** a process in which an intelligent
system contributes to producing a more capable successor. This broad
category does not itself say that AI R&D is autonomous, verified, or
open-ended.

**Automated AI R&D:** AI execution of some research tasks—such as coding,
experiment operation, evaluation, or analysis. Humans may still select
problems, supply criteria, authorize deployment, and integrate results, so
automation is not verified AI-R&D closure.

**Verified AI-R&D closure:** a system proposes, implements, tests,
independently evaluates, and safely deploys accepted changes to successors
within the claimed scope. It does not imply embodied physical autonomy or
reproduction of productive capital.

**Embodied autonomy:** verified ability of an AI-and-hardware system to
perform a declared physical task set with bounded intervention, including
fault detection and unscripted recovery. It is task- and embodiment-specific;
it does not imply AI-R&D closure or capital reproduction.

**Reproductive-capital closure:** ability of an industrial network to
replace and expand every indispensable productive-capital stock after
depreciation, obsolescence, and losses. It can exist under a bounded
controller and does not imply autonomous AI research.

**Authorized replication:** productive-capacity growth admitted through the
applicable reliability, verification, secure-command, environmental, legal,
and human-authority gates. Gross or technically successful replication can
remain unauthorized.

**Industrial closure (κ):** the degree to which a production network
internally supplies the critical inputs required for its own operation. The
proper object is a sector vector with criticality and substitutability, not a
single mass fraction.

**Closure engineering:** the quantitative discipline, originating in the
1980 NASA/ASEE summer study, of accounting for every input a replicating
industrial system must produce or import.

**Self-sustaining:** able to replace consumed and depreciated productive
capacity without an essential external supply.

**Self-expanding:** able to produce net additional productive capacity after
replacement, repair, and losses.

**Industrial seed:** a compact initial system intended to grow into a broader
local production network. In this paper it has four layers: physical
equipment; digital models and toolchains; industrial memory; and
experimental capacity for generating missing knowledge.

**Digital seed:** the AI weights, firmware, controllers, compilers,
CAD/CAM, simulators, optimization and verification tools, and locally
available software dependencies transported with an industrial seed.

**Industrial memory:** the machine-readable recipes, material and equipment
models, calibration and maintenance procedures, build records, failure
histories, intervention traces, and provenance required to operate, repair,
and adapt the physical seed.

**Embodied-autonomy threshold:** the task coverage and recovery capability
at which a robot-and-AI system can perform the unscripted diagnosis, tool
use, construction, repair, learning, and verification needed to keep the
industrial graph operating without routine human intervention. It is not a
joint-count or robot-count threshold.

**Terrestrial autonomous-closure rehearsal:** an Earth-based test of the
candidate off-world seed under constrained materials, energy,
communications, spares, and human access, culminating in construction and
commissioning of a second production cell.

**Operating-cell equivalent:** the integrated layer's continuous unit of
installed, commissioned productive capacity, normalized to the initial
seed cell. The reported aggregate-doubling threshold is first passage of
this aggregate to 2.0; it is not a claim that a discrete second factory
has completed commissioning or that expansion is sustained.

**Exogenous deployment:** capacity growth supplied by an external
industrial base, such as Earth-manufactured data centers delivered to orbit.

**Endogenous industrial growth:** capacity growth produced from within the
industrial network by allocating part of its output to reproducing and
expanding productive equipment.

**Material vitamins:** low-mass, high-criticality inputs—such as advanced
chips, dopants, catalysts, specialty chemicals, sensors, bearings, or
precision tooling—whose absence can stop a high-mass locally supplied
industry.

**Process-specific artificial gravity:** centrifugal acceleration supplied
to a particular machine or production module when microgravity or lunar
gravity does not meet that process's requirements; distinct from rotating
an entire habitat or industrial complex.

**Clock-setting component:** the component with the shortest effective
replacement horizon that cannot yet be produced, repaired, substituted, or
stockpiled locally; it bounds the survival time of the partially closed
system.

**Replication time:** the time a production network needs to reproduce a
unit of productive capacity. It is unknown as a measurement here and appears
only as a set-labeled model-output distribution.

**Bridge economy:** the sequence of independently financeable products and
services that carries the system through the capital-intensive stages before
closure.

**ISRU:** in-situ resource utilization — obtaining and using materials at the
mission destination rather than importing every supply from Earth.

**Productive throughput:** the rate at which a system converts energy,
materials, compute, and machine time into useful output.

**Distributed industrial ecology:** a network of specialized, mutually
dependent production nodes whose combined input-output graph is
self-sustaining or self-expanding.

**Scarcity becomes latency:** the proposition that, after high closure, the
principal limit on many outputs becomes production allocation and completion
time rather than external purchase price. Opportunity cost remains.

**Von Neumann replicator:** a machine system capable of constructing a
functional copy of itself from available materials; the formal category to
which a fully closed industrial complex belongs.

**Terafab:** the chip-fabrication initiative announced in March 2026 by
Tesla, SpaceX, and xAI and joined by Intel in April, targeting advanced AI
chips including radiation-tolerant orbital silicon. The SEC-filed offering
materials describe a general framework with unsettled implementation, not a
demonstrated fab or legally constituted joint venture [S27].

**Society-priced costs:** operating inputs priced substantially through human
institutions rather than physical conversion alone — land, permitting,
interconnection, litigation, and political consent. Space relocates these
costs toward gateways such as launch, spectrum, liability, and treaty rather
than abolishing them.

**Threshold-model argument:** the proposition that once a base model crosses
the capability needed to run verified improvement loops, a smarter starting
model may confer only a transient head start and durable advantage may shift
toward hardware doubling time and industrial closure. This is the small-α
branch of II.5, not an established law.

**Architectural convergence:** the point at which the marginal value of
another design improvement falls below that of another deployed node.
Beyond it, growth is increasingly deployment-limited.

**Paradigm-sensitivity split:** the division between less
paradigm-sensitive layers — energy, labor, transport, and bulk materials —
and the more paradigm-specific fabrication layer, where stranding and
leapfrog risk concentrate.

**Retooling speed:** the time a manufacturing complex needs to reconfigure
for a new technological paradigm. Alongside hardware doubling time, it is a
first-class competitive and resilience metric.

**Physical-process data:** training-relevant data generated by operating
physical industry — telemetry, process settings, intervention records,
failures, and fleet or manipulation traces.

**Data-advantage index (κ_D):** an index over uniqueness, causal linkage,
coverage, quality, accessibility, integration, and verification value.
Total training-relevant data has no measurable denominator, so κ_D is not a
closure ratio.

**Unified build record:** a per-unit data structure linking design intent
(*as designed*), production parameters (*as built*), and operational
telemetry (*as deployed*), making physical-process data causally trainable.

**Vitamin parts (historical term):** the residual imported microelectronics, bearings,
precision instruments, catalysts, or other high-complexity inputs that
resist local production. The term comes from the 1980 closure literature.

**Electronics strategic-material gap:** in this model, the unclosable
fraction of the electronics sector's output mix — the results-driving
unknown sampled through the space electronics q-scale. It is also called
the “vitamin gap” in the closure literature.

**Coasean boundary:** the organizational boundary at which internal
coordination costs equal market transaction costs. AI can lower both sides,
so the direction in which the efficient boundary moves is empirical.

**Gateway leverage:** enforceable governance authority concentrated at
dependencies such as launch, spectrum, export control, finance, communications,
cryptographic authority, and trade. Its material component follows
criticality, substitutability, stockpile, supplier concentration, and
enforceability — not the scalar expression (1 − κ).

**Minimum cut set:** a smallest combination of imported inputs whose loss
prevents self-expansion.

**Likelihood ratio of evidence:** how much more expected an observation is
under one hypothesis than under a competitor. Part III uses ordinal
diagnosticity rather than numerical multiplication because evidence items are
correlated and observability is uncertain.

**Maximin growth rate g:** the worst-case sector growth rate maximized by the
allocation program, ensuring that aggregate growth cannot hide collapse in
an indispensable sector.

**Assumption set:** a named, complete collection of ASSUMPTION-class
structural coefficients used together in a model run.

**Anchor:** a published, source-classed range sampled by Monte Carlo; an
anchor constrains an input without converting it into a measurement of the
whole system.

**Computed:** derived mechanically from stated assumptions by the companion
model. A computed result inherits the epistemic class of its weakest input.

**Kessler syndrome / collisional cascade:** an endogenous orbital-debris
feedback in which collisions create fragments that increase the probability
of later collisions. It is not equivalent to a fixed independent debris
hazard.

**Sun-synchronous orbit (SSO):** a planet-centered precessing orbit selected
so that the spacecraft passes a reference point at approximately the same
local solar time. Earth SSO is ordinarily a LEO architecture; it does not
mean an orbit around the Sun.

**Heliocentric orbit:** an orbit around the Sun. In the post-lunar scenario,
"distributed heliocentric" means separated orbital elements and resource
trajectories rather than a new single dense shell.

# Sources {#sources}

Sources [S1–S27] establish the core argument and [S28] identifies the
executed companion model. [S29–S36] add corporate, technical, and
fast-takeoff/capital-mobilization cross-checks. [S37] is the primary June 2026 Starship V3/V4 disclosure
used to normalize the launch-price sensitivity cases; [S38] is the
subsequent AI1 product specification. [S39–S44] are the independent
spacecraft, thermal, network, microdatacenter, and economic cross-checks
for Part II. [S45–S57] bound the
lunar, debris, regulatory, and material-source extensions. [S58–S61] ground
the digital-loop sensitivity model in scaling and architecture
literature; [S62–S66] bound orbital servicing, circularity, mitigation, and
collision-control claims; [S67–S68] provide conceptual Earth- and
lunar-ascent delta-v anchors without supplying service economics. [S69–S71]
define selected authorization, export-control, and debris-plan dependencies;
[S72–S75] supply the release-level parameter, token, and five-shot MMLU
records used in the chronological backtest. [S76–S78] ground the AI-hardware
supply-chain and economic-obsolescence cross-checks. [S79–S85] bound the
digital-loop discussion with scenario, company-report, formal-economic,
empirical-task, survey, and governance countercases.

## Primary statements {#primary-statements}

[**[S1]**]{#source-s1 .source-entry-label} SpaceX, ["Mars & Beyond: A City on
Mars"](https://www.spacex.com/humanspaceflight/mars).

> SpaceX states that establishing a self-sufficient city on Mars requires
> large-scale cargo and population transfer.

[**[S2]**]{#source-s2 .source-entry-label} Tesla, ["Master Plan Part
3"](https://www.tesla.com/master-plan-part-3).

> Tesla outlines a proposed path to a sustainable global energy economy
> through electrification, renewable generation, and storage.

[**[S3]**]{#source-s3 .source-entry-label} xAI, ["Company: Accelerating Scientific
Discovery"](https://x.ai/company).

> xAI describes its mission as accelerating scientific discovery and
> extending what humanity can know and do.

[**[S4]**]{#source-s4 .source-entry-label} NASA, ["Overview: In-Situ Resource
Utilization"](https://www.nasa.gov/overview-in-situ-resource-utilization/).

> NASA describes technologies for using destination resources to produce
> water, fuel, supplies, and construction capability.

[**[S5]**]{#source-s5 .source-entry-label} NASA, ["Lunar Surface
Technology"](https://www.nasa.gov/lunar-surface-technology/).

> NASA identifies ISRU, excavation, infrastructure construction, power,
> robotics, and autonomy as key lunar capabilities.

## Reporting and records of the 2026 developments {#reporting-and-records-of-the-2026-developments}

[**[S6]**]{#source-s6 .source-entry-label} Reuters (via Yahoo Finance), March 14, 2026, "Musk says
Tesla's mega AI chip fab project to launch in seven days."

> Confirms the Terafab name, AI5 program, existing TSMC and Samsung
> partnerships, and earlier remarks about a possible Intel collaboration.

[**[S7]**]{#source-s7 .source-entry-label} CBS News, March 23, 2026, "What is Elon Musk's Terafab chip
project?"

> Summarizes the Austin announcement and the stated purpose of supplying
> chips for vehicles, spacecraft, and Optimus robots.

[**[S8]**]{#source-s8 .source-entry-label} Proactive Investors (via Yahoo Finance), March 2026, "Musk says
Tesla, SpaceX to build $20B Terafab chip plant in Texas."

> Reports the 2-nm target, terrestrial and space chip lines, and the stated
> 2028 mass-production goal.

[**[S9]**]{#source-s9 .source-entry-label} CNBC, May 6, 2026, "Elon Musk's Terafab chip factory in Texas
could cost up to $119 billion, filing shows."

> Reports the filing-based cost ceiling, the roughly $3B research fab,
> SpaceX's lead role in the scaled phase, and public-offering preparations.

[**[S10]**]{#source-s10 .source-entry-label} Teslarati and Electrek, March 22, 2026, launch coverage and
critical commentary.

> Together report the proposed venture structure, the SpaceX–xAI merger,
> D3 orbital chip line, wafer-start ambitions, the Optimus construction
> role, and skeptical assessments of feasibility. Later primary-source
> corrections in [S27] control where the reports conflict with the filing.

[**[S11]**]{#source-s11 .source-entry-label} SpaceXAI, "Introducing Grok 4.5," July 2026, with
contemporaneous Axios coverage.

> Documents an in-house engineering-focused model trained in SpaceXAI data
> centers, its use in internal engineering work, and reporting on
> engineering data entering later training runs.

[**[S12]**]{#source-s12 .source-entry-label} VentureBeat and Northflank, July 2026, coverage of Moonshot AI's
Kimi K3 release.

> Reports a 2.8-trillion-parameter open-weight model benchmarking near the
> proprietary frontier on agentic and coding tasks. Used as evidence of
> benchmark compression, not of an autonomous-R&D threshold.

[**[S13]**]{#source-s13 .source-entry-label} Public statements and reporting, July 2026 (Teslarati, Yahoo
Tech, and contemporaneous posts on X), on SpaceX engineering data entering
a roughly two-trillion-parameter supplemental training run.

> Musk states that the engineering corpus, excluding ITAR-restricted
> material, will enter supplemental training of the next in-house model —
> the same broad mechanism previously used with acquired coding data.

[**[S14]**]{#source-s14 .source-entry-label} *Connecting The Dots* video commentary, 2026, on Tesla's
internal engineering systems.

> Commentary-class source. Its integrated-systems core is corroborated by
> [S15–S17]; unconfirmed claims of a "Tesla One" brand and a specific
> manufacturing-CAD AI are excluded from the document's factual claims.

[**[S15]**]{#source-s15 .source-entry-label} Jay Vijayan, on-record interviews and profiles (*The Neon Show*,
Indiaspora, and *Forbes India*).

> Tesla's first CIO describes building the custom Warp enterprise system
> in roughly four months in 2012 after rejecting off-the-shelf ERP, and its
> continuous extension thereafter.

[**[S16]**]{#source-s16 .source-entry-label} Stack Overflow engineering blog, "Building the software that
helps build SpaceX," 2021, with corroborating former-engineer accounts.

> Documents SpaceX's internal Warp Drive enterprise and manufacturing
> systems.

[**[S17]**]{#source-s17 .source-entry-label} Tesla AI Day presentations, 2021–2022.

> First-party documentation of fleet-learning infrastructure: an occupancy
> network trained on 1.4 billion fleet frames and auto-labeling replacing
> roughly five million hours of manual annotation. Later fleet-mile totals
> are company statements and are not converted into driverless-mile
> equivalents.

## Parameter literature {#parameter-literature}

[**[S18]**]{#source-s18 .source-entry-label} D. C. Jordan, S. R. Kurtz, K. VanSant, and J. Newmiller,
["Compendium of Photovoltaic Degradation
Rates"](https://doi.org/10.1002/pip.2744), *Progress in Photovoltaics*
24(7), pp. 978–989, 2016.

> Meta-study of more than 11,000 measured degradation rates; terrestrial
> crystalline-silicon median approximately 0.5–0.6% per year.

[**[S19]**]{#source-s19 .source-entry-label} W. Q. Lohmeyer, R. J. Aniceto, K. Cahoy, and A. Carlton,
["Solar array degradation on geostationary communications satellites: the
quantification of annual degradation and degradation over solar proton
events"](https://doi.org/10.1504/IJSPACESE.2018.090549),
*International Journal of Space Science and Engineering* 5(1), pp. 61–81,
2018.

> Reported degradation ranges are approximately 0.44–1.03% per year for
> gallium-arsenide arrays and 0.71–1.69% for silicon arrays. This anchors
> one component class, not system-wide industrial depreciation.

[**[S20]**]{#source-s20 .source-entry-label} S. Philipps and W. Warmuth, Fraunhofer ISE,
[*Photovoltaics Report*](https://www.ise.fraunhofer.de/content/dam/ise/de/documents/publications/studies/Photovoltaics-Report.pdf),
July 14, 2026, p. 8; K. P. Bhandari et al.,
["Energy pay-back time and carbon footprint of commercial photovoltaic
systems"](https://doi.org/10.1016/j.rser.2015.02.057),
*Renewable and Sustainable Energy Reviews* 47, pp. 133–141, 2015.

> Energy-payback estimates of roughly 0.9–1.1 years in Europe and a
> harmonized 1.0–4.1-year range across technologies. These do not measure
> reproduction of the production system.

[**[S21]**]{#source-s21 .source-entry-label} M. Hecht, J. Hoffman et al., MOXIE results, *Science Advances*,
2022; D. L. Linne, G. B. Sanders, and K. M. Taminger,
["Capability and Technology Performance Goals for the Next Step in
Affordable Human Exploration of
Space"](https://doi.org/10.2514/6.2015-1650), AIAA 2015-1650,
pp. 8–9 and Table VI, also [NASA NTRS
20150011681](https://ntrs.nasa.gov/citations/20150011681).

> Oxygen produced on Mars at gram-per-hour scale at at least 98% purity;
> lunar oxygen extraction demonstrated at approximately 20% yield and TRL
> 5/6. Neither is a full-system closure demonstration.

[**[S22]**]{#source-s22 .source-entry-label} Independent satellite tracking and reporting by J. McDowell,
Harvard-Smithsonian CfA, 2020–2026.

> Constellation deorbit and status statistics. Reported fractions near 3%
> for early generations fall below 0.5% for later ones, and the tracker
> separates early deorbit, uncontrolled decay, retirement, and disposal.
> Without cohort, observation interval, and satellite-years, these are
> fleet fractions rather than hazard rates.

## Closure-engineering literature {#closure-engineering-literature}

[**[S23]**]{#source-s23 .source-entry-label} NASA, [*Advanced Automation for Space
Missions*](https://ntrs.nasa.gov/citations/19830007077) (NASA CP-2255),
1980 NASA/ASEE summer study; matter-closure and residual-import statements
at sec. 5.3.6, report p. 219 (PDF p. 225).

> Designs a proof-of-principle self-replicating lunar factory from a
> roughly 100-ton seed. It adopts a one-year **strawman** replication target
> whose component values it calls crude estimates; cites 90–96% closure
> from earlier studies of specific **nonreplicating** production
> applications; and places rigorous demonstration of complete parts closure
> outside its scope. These are design assumptions and plausibility
> arguments, not demonstrated performance.

[**[S24]**]{#source-s24 .source-entry-label} R. A. Freitas Jr. and R. C. Merkle, *Kinematic
Self-Replicating Machines*, Landes Bioscience, 2004.

> Comprehensive survey of the design space for physical self-replicating
> systems.

## Economics and progress-rate literature {#economics-and-progress-rate-literature}

[**[S25]**]{#source-s25 .source-entry-label} R. H. Coase, "The Nature of the Firm," *Economica* 4(16), 1937.

> Transaction-cost account of firm boundaries used in II.5's
> integration-versus-modularity analysis.

[**[S26]**]{#source-s26 .source-entry-label} Epoch AI (Ho et al.), "Algorithmic Progress in Language Models,"
2024.

> Estimates that compute required for fixed language-model performance
> halves roughly every eight months. The resulting approximately
> threefold-per-year rate does not license extrapolation to autonomous
> research or physical productivity.

## Primary regulatory filing and model provenance {#primary-regulatory-filing-and-model-provenance}

[**[S27]**]{#source-s27 .source-entry-label} Space Exploration Technologies Corp.,
[Form S-1 registration statement, filed May 20,
2026](https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/0001628280-26-036936-index.htm),
SEC accession 0001628280-26-036936; and
[Rule 433 free-writing prospectus, filed June 4,
2026](https://www.sec.gov/Archives/edgar/data/1181412/000162828026040610/spacexfwp.htm),
SEC accession 0001628280-26-040610, with associated June 4 offering
materials; contemporaneous analysis by Electrek, *Tom's Hardware*,
*Forbes*, and KBTX.

> This document's primary corporate source. On Terafab it describes a
> general framework with Tesla; specific projects, timelines, milestones,
> and capital expenditures require separate agreements and were not yet
> determined (Form S-1 pp. 7, 10, 154). Risk Factors characterize the
> orbital-AI, lunar, and interplanetary initiatives as early-stage,
> unproven, and potentially unsuccessful (pp. 12, 24–25). The initiative
> list includes terrestrial and orbital AI compute,
> orbital data centers from as early as 2028, internal chip design and
> manufacture, lunar manufacturing and energy, in-orbit manufacturing,
> manufacturing on the Moon and Mars, asteroid mining, and
> "interplanetary industrialization" (pp. 164, 171; Rule 433 roadshow
> slides 42–44). It reports more than 1,000 automated collision-avoidance
> maneuvers per day across Starlink in 2025 (pp. 9, 153). These and the
> other load-bearing [S27] extractions are recorded in
> `params/claim_provenance.yaml` and the generated
> [claim-provenance register](../outputs/tables/claim_provenance.csv){.artifact-link data-artifact="outputs/tables/claim_provenance.csv"}.

[**[S28]**]{#source-s28 .source-entry-label} Companion simulation program, [rsi-model
repository](https://github.com/fperegrinvs/rsi-model), r4.0 release candidate on branch `main`; concept DOI `10.5281/zenodo.21619447`; Appendices C–D.

> Reproducibility source, not evidence. It computes consequences of stated
> assumptions and supports no empirical claim on its own authority. Each
> archived release tag mints a version-specific DOI.

## Corporate and orbital-compute record {#corporate-and-orbital-compute-record}

[**[S29]**]{#source-s29 .source-entry-label} Terafab official project site (`terafab.ai`), accessed July
2026.

> First-party messaging: combined logic, memory, and advanced packaging;
> Kardashev-scale framing; scaling figures of approximately one billion
> robots, ten million tonnes per year launched to orbit, and more than one
> terawatt of solar; AI5/AI6/D3 lines; an explicit Earth-versus-space cost
> decomposition; and lunar mass drivers as a next step. Marketing and
> recruiting material — evidence of declared intent, not commitment.

[**[S30]**]{#source-s30 .source-entry-label} Waymo safety-impact disclosures, 2026.

> Cumulative fully driverless miles used as the comparison point in I.2 and
> Appendix A.3. No conversion to supervised autonomy miles is made.

[**[S31]**]{#source-s31 .source-entry-label} Heavy-lift flight-test reporting, 2026.

> Cumulative count of thirteen test flights through mid-2026, used as a
> low-volume, high-information development proxy rather than a capacity or
> reliability input.

[**[S32]**]{#source-s32 .source-entry-label} B. Agüera y Arcas, T. Beals, M. Biggs, J. V. Bloom,
T. Fischbacher, K. Gromov, U. Köster, R. Pravahan, and J. Manyika
(Google), "Towards a future space-based, highly scalable AI infrastructure
system design," arXiv:2511.19468 (v1 November 22, 2025; **v2 June 17,
2026**, the version carrying the detailed figures cited here), with the
Project Suncatcher blog post.

> Technical design study for satellite accelerator clusters: 67 MeV
> proton-beam testing of a Trillium TPU v6e, with HBM most TID-sensitive
> (irregularities from 2 krad(Si) against a 750 rad(Si) five-year
> requirement, no hard TID failures to 15 krad(Si)) and core logic/on-chip
> SRAM most SEE-sensitive; an inference error estimate near one per
> 3×10⁶ inferences under stated assumptions, with training impact reserved;
> an 81-satellite, 1 km-radius cluster near 650 km in dawn-dusk
> sun-synchronous orbit; and 800 Gbps unidirectional optical links against
> a roughly 10 Tbps per-link requirement. The authors twice state that the
> cost section is **not** a full economic analysis: it compares amortized
> launch cost per kW-year ($810 for a Starlink-v2-class ratio and
> $810–7,500 across classes at $200/kg) with terrestrial electricity spend
> ($570–3,000/kW-year), excluding buildings, infrastructure, and chips.
> Reaching approximately $200/kg by 2035 requires about 370,000 tonnes of
> additional cumulative launch mass, or roughly 1,800 Starship-class
> flights averaging 180 per year. Thermal management, ground
> communications, reliability, and repair remain open; orbital repair is
> described as impracticable and redundant provisioning proposed instead.

[**[S33]**]{#source-s33 .source-entry-label} *SpaceNews*, *Via Satellite*, and *Data Center Dynamics*
coverage of orbital-compute programs, 2025–2026.

> Reports the Google–Planet partnership, two prototype satellites slated
> for launch by early 2027, the research-stage status of the program, and
> at least one additional entrant flying an accelerator demonstrator.

[**[S34]**]{#source-s34 .source-entry-label} Will Marshall, co-founder and CEO of Planet Labs, interviewed on
the *Moonshots* podcast with P. Diamandis and colleagues, episode 266,
published June 26, 2026. A transcript with paragraph timestamps is archived
at `docs/transcripts/moonshots-266-2026-06-26.md`.

> Cited for mechanisms rather than measurements: launch tax versus compute
> tax (0:00:22 and 1:17:49); matching low-orbit decay life to hardware
> obsolescence; payload cost-performance outpacing launch
> cost-performance; limits on reproducing historical archives; finite
> compute-demand possibility; the protect-the-biosphere telos; and the
> recollected Google/Planet $200–300/kg crossover study (0:52:07).
> Recollections and projections are unverified.

## External strategic cross-check {#external-strategic-cross-check}

[**[S35]**]{#source-s35 .source-entry-label} L. Aschenbrenner, *Situational Awareness: The Decade Ahead*,
June 2024, archived in `docs/sources/`.

> Analyst estimates used as external cross-checks: a trillion-dollar
> compute-cluster trajectory; power as the binding constraint with a
> politically conditional natural-gas floor; CoWoS/HBM as chip
> bottlenecks; a fast-takeoff thesis; and historical capital-mobilization
> reference classes. These claims affect priors and counterfactuals, not the
> evidence table's item-level assessment.

## Contextual engineering and reporting sources {#contextual-engineering-and-reporting-sources}

[**[S36]**]{#source-s36 .source-entry-label} Assorted company disclosures, industry reporting, agency
guidance, price sheets, and technical literature used to bound Appendix A
and Part II scenarios.

> Covers evidence not carried by [S18–S23]: foundry equipment-depreciation
> schedules (2–5 years); data-center accelerator retirement practice
> (3–6 years); a large-training-run disclosure of roughly 419
> interruptions over 54 days across approximately 16,000 accelerators
> (cluster interruption frequency, not component hazard); 2019 reporting on
> factory construction cadence; 2026 humanoid-robot production targets;
> NASA small-spacecraft guidance on altitude-, ballistic-coefficient-, and
> solar-activity-dependent decay; launch price sheets; flexible-array and
> deployable-radiator performance; accelerator system pricing;
> AI-optimized data-center capex and PUE; and nuclear-restart PPA reporting.
> No single permanent identifier covers the collection. The r4.0
> claim-level audit therefore does **not** use [S36] to justify any
> non-`ASSUMPTION` model endpoint. Ranges synthesized from these materials
> remain explicitly `ASSUMPTION`; [S36] supplies contextual bounds only.
> Every retained non-assumption endpoint instead has an exact record in
> `params/claim_provenance.yaml`.

[**[S37]**]{#source-s37 .source-entry-label} Space Exploration Technologies Corp., [European Union
Prospectus, approved by BaFin, June 5,
2026](https://content.spacex.com/cms-assets/FINAL_Documents%20and%20Updates/SpaceX%20-%20EU%20Prospectus%20%28Approved%20by%20Bafin%29%20-%20June%205%2C%202026.pdf),
pp. 63, 70–72, 80–82, 97, and 137; see also the June 4, 2026 SEC-filed roadshow
materials.

> Primary company disclosure for the Starship aspiration normalization.
> It states that fully reusable Starship V3 is expected to carry 100 metric
> tonnes to orbit, that future generations could reach 200 tonnes
> potentially as soon as V4, and that Starship is intended eventually to
> reduce a cited historical $18,500/kg launch-cost benchmark by 99% or more.
> The resulting ≤$185/kg figure is arithmetic, not a quoted V3/V4 customer
> price. The $100/kg and $30–50/kg cases in Part II are progressively more
> aggressive sensitivity axes and are not attributed to this source. The
> prospectus also uses 100 kW/t to describe a long-term path to 100 GW of
> orbital AI-compute power per year—about one million tonnes and thousands
> of launches annually—and identifies full rapid reuse, approvals, spectrum,
> and long-duration reliability as dependencies. It warns that terrestrial
> energy improvements could diminish orbital viability. The target extraction
> and arithmetic are archived in
> `docs/sources/spacex-ai-aspirations-2026-06.md`.

[**[S38]**]{#source-s38 .source-entry-label} Space Exploration Technologies Corp., [Starmind AI1 official
product page](https://www.spacex.com/spacexai/starmind), accessed July 27,
2026; numeric provenance snapshot archived at
`docs/sources/starmind-ai1-2026-07-27.md`.

> First-party architecture disclosure for a planned orbital AI satellite:
> 150 kW peak / 120 kW average compute payload, 70 kW/tonne vehicle
> efficiency, 150 kW solar array at 250 W/m², 110 m² deployable liquid
> radiator, and a 20 m by 70 m deployed envelope. It also describes
> redundant pumped loops, debris shielding, laser links through Starlink,
> and sun-synchronous operation, but does not disclose vehicle capex,
> component mass, achieved availability, service life, qualification cost,
> or link cost. Company specification, not demonstrated performance.

## Post-IPO orbital-compute calibration {#post-ipo-orbital-compute-calibration}

[**[S39]**]{#source-s39 .source-entry-label} S. G. Turyshev, ["Orbital Data Centers: Spacecraft Constraints
and Economic Viability"](https://arxiv.org/abs/2604.27197),
arXiv:2604.27197, submitted April 29, 2026. The values used across
[S39–S44] are consolidated in
`docs/sources/orbital-compute-calibration-2026-07-27.md`.

> Independent system-level closure across power, eclipse storage, thermal
> rejection, spacecraft fixed mass, communication intensity, utilization,
> finite life, and economics. Its representative 1 MW high-sunlight case
> requires 5,640 m² of BOL PV, 2,500 m² of radiator, 29.4 kg/kW for PV,
> storage, and radiators, and 34–59 kg/kW total after fixed spacecraft
> functions. At 40 kg/kW, $10,000–40,000/kW of terrestrial infrastructure
> permits only $250–1,000/kg for launch and spacecraft build combined before
> communications, operations, utilization, and life penalties. The paper's
> annual-hazard penalties are illustrative sensitivities, not fleet
> measurements.

[**[S40]**]{#source-s40 .source-entry-label} S. Gaalema, S. Indyk, and C. Staley, ["Reduced-Mass Orbital AI
Inference via Integrated Solar, Compute, and Radiator
Panels"](https://arxiv.org/abs/2604.07760), arXiv:2604.07760, April 2026;
and I. Bargatin, D. Jin, Z. Alansari, and J. R. Raney, ["Tether-Based
Architecture for Solar-Powered Orbital AI Data
Centers"](https://arxiv.org/abs/2512.09044), arXiv:2512.09044 and AIAA
SciTech 2026.

> Low-mass inference architecture studies. The first reports a design basis
> above 100 kW/t using integrated PV, vapor-chamber radiators, and custom
> accelerators in a kilometer-scale array; its large example is about
> 150 tonnes and 16 MW. The second proposes 2–20 MW tethered systems with
> approximately 10 kg, 2 kW nodes. Both make mass-reducing integration
> assumptions whose deployment, dynamics, thermal, shielding, qualification,
> and lifetime closure remains prospective.

[**[S41]**]{#source-s41 .source-entry-label} K. van Berkel, ["The Cost and Network Limits of Space-Based AI
Compute"](https://arxiv.org/abs/2607.14172), arXiv:2607.14172, submitted
July 15, 2026.

> Post-IPO compute-network comparison. For the modeled 8,000-accelerator
> systems, the terrestrial Clos fabric has 28,800 TB/s bisection bandwidth
> versus 2.25 TB/s for a two-dimensional and 10 TB/s for a
> three-dimensional orbital mesh at 100 Gbps links; estimated network
> latency is 150–450 times higher. The paper finds orbital inference
> potentially feasible but frontier LLM training uncompetitive on the
> analyzed meshes. Its aggressive $/kg and kg/kW economic premises are used
> here only as context; the network calculation is the calibration result.

[**[S42]**]{#source-s42 .source-entry-label} R. Eason, N. Bleier, M. Lembeck, and R. Kumar,
["Architecting Space Microdatacenters: A System-level
Approach"](https://passat.crhc.illinois.edu/hpca25.pdf), IEEE
International Symposium on High-Performance Computer Architecture, 2025.

> Peer-reviewed cost/performance study of bespoke 0.5–10 kW
> microdatacenters for space-native workloads. Power and thermal functions
> account for roughly a third of modeled spacecraft TCO, compute hardware
> can be less than one percent, and energy-efficiency improvements are up to
> 2.5 times more valuable in space and reduce modeled TCO by approximately
> two-thirds. Its scale and in-orbit data origin differ from the Part II
> terrestrial-substitution case.

[**[S43]**]{#source-s43 .source-entry-label} NASA Glenn Research Center, [NASA/TM—2005-213442, radiator mass
comparison](https://ntrs.nasa.gov/api/citations/20050238492/downloads/20050238492.pdf),
2005.

> Primary engineering reference separating radiator panels from the
> complete heat-transport and deployment system. ISS two-sided panels are
> reported at 2.75 kg/m² and 8.8 kg/m² after fluid loop and deployment
> mechanism; the JIMO analysis estimated 5 kg/m² for the complete system.
> At 353 K, 0.86 emissivity, and 173 K environment, the sizing example uses
> approximately 1.4 m²/kW. These are heritage/system cross-checks, not
> forecasts for an optimized AI1 radiator.

[**[S44]**]{#source-s44 .source-entry-label} University of Virginia National Security Data Policy Institute,
["Evaluating Space-Based Data Center Architectures: Capabilities,
Constraints, and
Trade-Offs"](https://nationalsecurity.virginia.edu/sites/default/files/files/2026-05/00036_20260519%29_nsdpi_evaluating_space-based_data_center_architectures-capabilitites%2C_constraints%2C_and_trade-offs.pdf),
Product No. 00036, May 19, 2026.

> Policy synthesis with a simplified public cost model. Its representative
> five-year 1 GW estimates are $135.6 billion orbital versus $16.6 billion
> terrestrial under present-style assumptions, and $15.4 billion orbital
> only when launch falls to $30/kg, satellite hardware to $10/W, specific
> power rises to 100 W/kg, sunlight availability to 80%, and annual
> degradation and GPU failures each fall to 1%. It excludes GPU hardware,
> financing, insurance, logistics overhead, and downtime, so it is used only
> as a directional joint-condition check.

## Lunar surface–orbit architecture and debris boundary {#lunar-surfaceorbit-architecture-and-debris-boundary}

[**[S45]**]{#source-s45 .source-entry-label} D. J. Kessler and B. G. Cour-Palais,
["Collision Frequency of Artificial Satellites: The Creation of a Debris
Belt"](https://doi.org/10.1029/JA083iA06p02637), *Journal of Geophysical
Research* 83(A6), 2637–2646, 1978.

> The original collision-feedback result: satellite collisions create
> orbiting fragments, each of which raises the probability of later
> collisions. It supplies the direction of the feedback, not a universal
> threshold for a particular future constellation.

[**[S46]**]{#source-s46 .source-entry-label} N. R. Boone and R. A. Bettinger,
["Simulation of Debris Events in Selected Low Lunar
Orbits"](https://doi.org/10.1007/s40295-023-00382-y), *Journal of the
Astronautical Sciences* 70, 16 (2023).

> Approximately 97,000 simulated fragments across eight breakup cases show
> orbit-dependent debris evolution: some selected low lunar orbits retain
> long-lasting populations, while impacts on the Moon are geographically
> nonuniform. The reported one-year collision probabilities are low for the
> notional present cases; the paper does not establish a current lunar
> cascade.

[**[S47]**]{#source-s47 .source-entry-label} NASA, ["Artemis Base Camp on the Moon Will Need Light, Water,
Elevation"](https://www.nasa.gov/humans-in-space/nasas-artemis-base-camp-on-the-moon-will-need-light-water-elevation/),
2021; NASA, ["Lunar Dust Mitigation: A Guide and
Reference"](https://ntrs.nasa.gov/citations/20220018746), 2021; and NASA,
["Archway for Radiation and Micrometeorite Occurrence
Resistance"](https://ntrs.nasa.gov/citations/20130009378), 2013.

> Surface-architecture boundary references: south-polar illumination and
> access to shadowed volatile deposits; abrasive/electrostatic dust effects
> on radiators, mechanisms, and sensors; and local regolith as candidate bulk
> radiation and micrometeoroid shielding. None establishes reserve
> economics, continuous power at a selected site, or industrial closure.

[**[S48]**]{#source-s48 .source-entry-label} D. C. Davis, F. S. Khoury, K. C. Howell, and D. J. Sweeney,
["Phase Control and Eclipse Avoidance in Near Rectilinear Halo
Orbits"](https://ntrs.nasa.gov/citations/20200000733), AAS Guidance,
Navigation and Control Conference, 2020.

> The Gateway reference NRHO is designed around eclipse avoidance, resonance,
> and low-cost stationkeeping with active phase control. It supports the
> gateway/service-layer role but does not make NRHO a passive, resource-bearing
> industrial site.

[**[S49]**]{#source-s49 .source-entry-label} NASA, ["Basics of Space Flight: Planetary
Orbits"](https://science.nasa.gov/learn/basics-of-space-flight/chapter5-1/),
updated 2024.

> Defines a Sun-synchronous orbit as a planet-centered precessing orbit that
> preserves local solar time and distinguishes it from a heliocentric orbit
> around the Sun.

## Orbital-data-center regulatory record {#orbital-data-center-regulatory-record}

[**[S50]**]{#source-s50 .source-entry-label} Federal Communications Commission, Space Bureau,
["Space Bureau Accepts for Filing SpaceX's Application for Orbital Data
Centers"](https://docs.fcc.gov/public/attachments/DA-26-113A1.pdf),
Public Notice DA 26-113, released February 4, 2026; ICFS File No.
SAT-LOA-20260108-00016, Call Sign S00798, application filed January 30,
2026.

> The notice accepts for filing an application describing a non-geostationary
> system of up to one million satellites. Acceptance for filing begins
> public and regulatory review; it is not authorization to deploy or operate
> the proposed system.

## Integrated bootstrap and material-source record {#integrated-bootstrap-and-material-source-record}

[**[S51]**]{#source-s51 .source-entry-label} NASA Science,
["Moon Composition & Structure"](https://science.nasa.gov/moon/composition/),
updated July 23, 2026.

> NASA lists oxygen, silicon, magnesium, iron, calcium, and aluminum as the
> principal elements in lunar-crust minerals, with smaller titanium,
> uranium, thorium, potassium, and hydrogen, and distinguishes
> calcium/aluminum-rich highlands from iron/titanium-rich maria. This is a
> bulk-composition boundary, not a resource or reserve estimate.

[**[S52]**]{#source-s52 .source-entry-label} Jennifer Edmonson and Doug Rickman,
["A Survey of Geologic Resources"](https://ntrs.nasa.gov/citations/20120015479),
NASA Technical Reports Server record 20120015479, 2012.

> The lunar-geology survey gives an average regolith bulk density of about
> 1.5 g/cm³ (1.5 t/m³), used only for the illustrative in-place inventory
> calculation in I.9. Density does not determine grade, recovery, or reserve
> economics.

[**[S53]**]{#source-s53 .source-entry-label} P. G. Lucey, G. J. Taylor, and E. Malaret,
["Abundance and Distribution of Iron on the
Moon"](https://doi.org/10.1126/science.268.5214.1150),
*Science* 268(5214), 1150–1153, 1995.

> Near-global Clementine data produced an approximately 3 wt% iron estimate
> for the lunar highlands crust and approximately 7–8 wt% for lower-crustal
> material exposed by South Pole–Aitken. The 3% value is used as a
> conservative illustrative concentration, not a claim about a selected
> mining site.

[**[S54]**]{#source-s54 .source-entry-label} C. B. Moore, C. F. Lewis, E. K. Gibson, and W. Nichiporuk,
["Total Carbon and Nitrogen Abundances in Lunar
Samples"](https://doi.org/10.1126/science.167.3918.495),
*Science* 167(3918), 495–497, 1970.

> Returned bulk fines in the reported samples contained carbon and nitrogen
> at roughly hundreds of parts per million, with mixtures of indigenous,
> meteoritic, and solar-wind contributions. The result establishes scarcity
> in those samples, not a global lunar resource map.

[**[S55]**]{#source-s55 .source-entry-label} NASA Goddard Space Flight Center,
["NASA's LRO: Lunar Ice Deposits Are
Widespread"](https://science.nasa.gov/solar-system/moon/nasas-lro-lunar-ice-deposits-are-widespread/),
October 3, 2024.

> LRO analysis finds widespread evidence of water ice in permanently
> shadowed regions beyond the immediate south pole while explicitly stating
> that deposit volume and burial beneath dry regolith cannot yet be
> accurately determined. Occurrence is not a bankable reserve.

[**[S56]**]{#source-s56 .source-entry-label} NASA Science,
["OSIRIS-REx Frequently Asked
Questions"](https://science.nasa.gov/mission/osiris-rex/osiris-rex-faq/),
accessed July 27, 2026.

> Laboratory analysis of returned Bennu material reports abundant organic
> molecules and sodium-rich minerals associated with evaporation of water.
> One carbonaceous sample demonstrates possible volatile and carbon-bearing
> diversity; it does not establish asteroid-mining yield or economics.

[**[S57]**]{#source-s57 .source-entry-label} NASA,
["Lunar Surface Technology"](https://www.nasa.gov/lunar-surface-technology/),
accessed July 27, 2026.

> NASA describes Blue Alchemist's integrated autonomous processing of
> regolith simulant into silicon solar cells, aluminum wires, oxygen, iron,
> and slag; it also reports vacuum extraction of oxygen from simulant by a
> molten-regolith-electrolysis reactor. These are subsystem and prototype
> demonstrations, not autonomous lunar industrial closure.

## Digital scaling and architecture record {#digital-scaling-and-architecture-record}

[**[S58]**]{#source-s58 .source-entry-label} J. Kaplan et al.,
["Scaling Laws for Neural Language
Models"](https://arxiv.org/abs/2001.08361), arXiv:2001.08361, 2020.

> Reports empirical power-law relationships between cross-entropy loss and
> model size, dataset size, and training compute over the studied ranges.
> These are loss curves for specified model families and data regimes, not a
> law of scalar intelligence or recursive improvement.

[**[S59]**]{#source-s59 .source-entry-label} J. Hoffmann et al.,
["Training Compute-Optimal Large Language
Models"](https://arxiv.org/abs/2203.15556), arXiv:2203.15556, 2022.

> Trains more than 400 models and finds that, in the studied Transformer
> regime, compute-optimal model size and training-token count should increase
> together. Chinchilla outperforms larger undertrained models at the same
> training-compute budget. The result constrains resource allocation; it does
> not demonstrate RSI.

[**[S60]**]{#source-s60 .source-entry-label} A. Gu and T. Dao,
["Mamba: Linear-Time Sequence Modeling with Selective State
Spaces"](https://arxiv.org/abs/2312.00752), arXiv:2312.00752, 2023.

> Introduces a selective state-space architecture with hardware-aware
> recurrent computation, linear sequence-length scaling, and reported
> throughput and quality comparisons to same-size Transformers. The results
> establish an architecture-specific trade space, not universal superiority
> across training, inference, hardware, and task regimes.

[**[S61]**]{#source-s61 .source-entry-label} W. Fedus, B. Zoph, and N. Shazeer,
["Switch Transformers: Scaling to Trillion Parameter Models with Simple and
Efficient Sparsity"](https://arxiv.org/abs/2101.03961),
arXiv:2101.03961, 2021.

> Demonstrates sparsely activated mixture-of-experts training while
> documenting routing, communication, precision, load-balancing, and
> instability challenges. Total parameters and active parameters per token
> are therefore different resource quantities.

## Orbital servicing, circularity, and mitigation record {#orbital-servicing-circularity-and-mitigation-record}

[**[S62]**]{#source-s62 .source-entry-label} NASA,
[*In-space Servicing, Assembly, and Manufacturing State of Play, 2024
Edition*](https://ntrs.nasa.gov/citations/20240012414), NASA Technical
Reports Server record 20240012414, 2024.

> Separates robotic manipulation, rendezvous and capture, relocation, planned
> and unplanned repair, refueling, manufacturing, inspection, and recycling,
> reuse, and repurposing into distinct capability areas. It records both
> operational precedents and developmental systems; inclusion is not evidence
> of fleet-scale economic closure.

[**[S63]**]{#source-s63 .source-entry-label} NASA,
["On-orbit Servicing, Assembly, and Manufacturing 1
(OSAM-1)"](https://www.nasa.gov/mission/on-orbit-servicing-assembly-and-manufacturing-1/),
status updated March 23, 2026.

> NASA records the decision to cancel OSAM-1 after independent review found
> major technical, integration, schedule, cost, mission-risk, return, and
> transition-partner problems. The case is direct counterevidence to assuming
> that autonomous servicing of an unprepared spacecraft is already routine or
> economical.

[**[S64]**]{#source-s64 .source-entry-label} European Space Agency,
["Active debris
removal"](https://www.esa.int/Space_Safety/Space_Debris/Active_debris_removal),
accessed July 28, 2026.

> ESA describes rendezvous and capture of an unprepared, uncooperative object
> as precise and complex, notes that removal is costly and not always
> possible, and treats ClearSpace-1 as a future demonstration rather than an
> operational recycling service.

[**[S65]**]{#source-s65 .source-entry-label} NASA Orbital Debris Program Office,
["Debris Mitigation"](https://orbitaldebris.jsc.nasa.gov/mitigation/);
F. J. Krage, [*NASA Spacecraft Conjunction Assessment and Collision Avoidance
Best Practices Handbook*, Revision
1](https://ntrs.nasa.gov/citations/20230002470), NASA/SP-20230002470, 2023.

> NASA separates prevention of debris creation, design against small impacts,
> selection of lower-risk regimes, post-mission disposal, trackability,
> conjunction screening, risk assessment, maneuverability, reliability, and
> operator coordination. These practices define control functions but do not
> calibrate a future large orbital industrial network.

[**[S66]**]{#source-s66 .source-entry-label} European Space Agency,
[*Space Environment Report
2025*](https://www.esa.int/Space_Safety/Space_Debris/ESA_Space_Environment_Report_2025),
April 1, 2025.

> Reports that mitigation compliance is improving but remains insufficient,
> that fragmentation adds objects faster than natural clearance in important
> regimes, and that debris can continue growing without new launches. ESA
> presents active removal as necessary to arrest that feedback; the report
> does not specify one universal constellation threshold.

[**[S67]**]{#source-s67 .source-entry-label} A. Beaurain, A. Souchier,
M. Moravie, R. L. Sackheim, and H. A. Cikanek III,
["Earth-to-Orbit Rocket
Propulsion"](https://ntrs.nasa.gov/citations/20030066115), NASA Technical
Reports Server record 20030066115, March 31, 2003.

> The abstract identifies approximately 9 km/s as the effective requirement
> to reach Earth parking orbit after gravity and atmospheric-drag effects. It
> is retained as a historical conceptual-design anchor, not a current launch
> vehicle performance or cost estimate.

[**[S68]**]{#source-s68 .source-entry-label} T. A. Lewis, E. L. Judd,
Z. D. May, and R. T. Joyce,
["A Parametric Assessment of Lunar and Mars Ascent Vehicle
Synergy"](https://ntrs.nasa.gov/citations/20205007701), AIAA ASCEND 2020,
NASA Technical Reports Server record 20205007701, 2020, p. 4, Table 2 and
Section III.A.

> Table 2 reports 1,850 m/s from the lunar surface to low lunar orbit and the
> text rounds the one-way ascent cases to 1.9 km/s for LLO and 2.7 km/s for
> NRHO. The paper derives vehicle mass with the rocket equation and notes that
> route values depend on vehicle thrust-to-weight and specific impulse. These
> values do not establish dollars per kilogram or the economics of a lunar
> service network.

[**[S69]**]{#source-s69 .source-entry-label} United Nations Office for Outer
Space Affairs,
[*Treaty on Principles Governing the Activities of States in the Exploration
and Use of Outer Space, including the Moon and Other Celestial
Bodies*](https://www.unoosa.org/oosa/en/ourwork/spacelaw/treaties/outerspacetreaty.html),
Articles VI–IX, treaty text and status portal, accessed July 28, 2026.

> Articles VI–VIII establish authorization and continuing supervision of
> non-governmental activity, launching-State liability, registry-linked
> jurisdiction and control, and continuity of ownership for space objects and
> components. These provisions make consent, authorization, liability, and
> custody explicit decision gates; this manuscript does not offer a legal
> conclusion for any specific mission.

[**[S70]**]{#source-s70 .source-entry-label} U.S. Department of Commerce,
Bureau of Industry and Security,
["Export Administration Regulations, Part 734 — Scope of the Export
Administration Regulations"](https://www.bis.gov/regulations/ear/734),
§734.13(a)(3)(i), current from the Electronic Code of Federal Regulations,
accessed July 28, 2026.

> The current rule treats certain transfers of registration, control, or
> ownership of spacecraft—including spacecraft providing logistics,
> assembly, or servicing—as exports. Applicability is mission-, item-,
> counterparty-, and jurisdiction-specific, so the model records an
> export-control review dependency rather than presuming approval.

[**[S71]**]{#source-s71 .source-entry-label} U.S. Federal Communications
Commission,
[*Space and Earth Station Applications Filing System: Orbital Debris
Mitigation and End-of-Life Rules*](https://docs.fcc.gov/public/attachments/DOC-415048A1.pdf),
§100.260, October 7, 2025.

> The rule text requires authorized operators to follow disclosed orbital
> debris mitigation plans and distinguishes end-of-life treatment for LEO and
> GEO spacecraft. It supports explicit authorization and disposal-plan gates;
> it does not imply that FCC jurisdiction is the only applicable regime.

[**[S72]**]{#source-s72 .source-entry-label} A. Chowdhery et al.,
["PaLM: Scaling Language Modeling with
Pathways"](https://jmlr.org/papers/volume24/22-1144/22-1144.pdf),
*Journal of Machine Learning Research* 24(240), 2023, pp. 4 and 18,
Table 6.

> Reports a dense 540-billion-parameter model trained on 780 billion tokens
> and 69.3% average five-shot MMLU accuracy. The release backtest uses those
> quantities as one training observation; the paper does not establish a
> general capability law.

[**[S73]**]{#source-s73 .source-entry-label} H. Touvron et al.,
["LLaMA: Open and Efficient Foundation Language
Models"](https://arxiv.org/abs/2302.13971), arXiv:2302.13971, 2023,
Tables 2 and 9, PDF pp. 3 and 7.

> Reports 65.2 billion parameters, 1.4 trillion pretraining tokens, and 63.4%
> average five-shot MMLU accuracy for the base LLaMA 65B model. It is reserved
> for the 2023 validation split.

[**[S74]**]{#source-s74 .source-entry-label} H. Touvron et al.,
["Llama 2: Open Foundation and Fine-Tuned Chat
Models"](https://arxiv.org/abs/2307.09288), arXiv:2307.09288, 2023,
Tables 1 and 3, PDF pp. 6 and 8.

> Reports 70 billion parameters, 2.0 trillion pretraining tokens, and 68.9%
> five-shot MMLU accuracy for the base Llama 2 70B model. It is reserved for
> the 2023 validation split.

[**[S75]**]{#source-s75 .source-entry-label} Meta,
["Llama 3.1 Model
Card"](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md),
Model Information and Benchmark Scores / Base Pretrained Models,
released July 23, 2024.

> Reports the 70-billion-parameter base model, a family pretraining corpus of
> more than 15 trillion tokens, and 79.3% five-shot MMLU accuracy. The
> backtest uses 15 trillion tokens as an explicit lower-bound input and
> reserves the observation for the 2024 holdout.

[**[S76]**]{#source-s76 .source-entry-label} NVIDIA,
["NVIDIA H100 Tensor Core
GPU"](https://www.nvidia.com/en-us/data-center/h100/),
Product Specifications, accessed July 28, 2026.

> The H100 SXM specification reports 80 GB of HBM3, 3.35 TB/s GPU-memory
> bandwidth, and 900 GB/s NVLink alongside the accelerator. These are
> product-specific primary-source quantities used only to establish that
> memory and high-speed interconnect are distinct load-bearing tiers, not to
> calibrate off-world production.

[**[S77]**]{#source-s77 .source-entry-label} Taiwan Semiconductor
Manufacturing Company,
[*2025 Annual
Report*](https://investor.tsmc.com/sites/ir/annual-report/2025/2025%20Annual%20Report_E.pdf),
Quality and Reliability / Advanced Packaging, 2026.

> TSMC distinguishes front-end wafer fabrication from back-end advanced
> packaging and describes the shift from silicon interposers toward
> reconfigured interposers with multiple local silicon interconnects. The
> report records certification of a 5.5-reticle-size CoWoS solution in 2025
> and planned volume production in 2026. It anchors the structural
> decomposition and one real packaging quantity; it does not calibrate the
> sensitivity's capacity-equivalent units.

[**[S78]**]{#source-s78 .source-entry-label} Jonathan Rice,
["The Macroeconomics of AI Capacity: Insights from a Two-Asset Growth
Model"](https://doi.org/10.1017/S1365100526100911),
*Macroeconomic Dynamics* 30 (2026), e22, published online March 26, 2026.

> The peer-reviewed two-asset model treats specialized AI hardware as
> economically obsolete much faster than conventional capital and reports an
> approximately seven-quarter AI-capacity adjustment half-life in its
> advanced-economy calibration. It is used as a conceptual cross-check for
> separating physical survival from economic replacement; its terrestrial
> macro calibration is not transferred into the off-world cohort sensitivity.

[**[S79]**]{#source-s79 .source-entry-label} Dario Amodei,
["Machines of Loving
Grace"](https://darioamodei.com/essay/machines-of-loving-grace), October
2024, “Basic assumptions and framework.”

> The essay explicitly presents educated guesses rather than established
> forecasts. Its “country of geniuses in a datacenter” assumes millions of
> digital workers operating 10–100 times faster than humans, then organizes
> their limits around the marginal returns to intelligence: outside-world
> speed, data, intrinsic complexity, human constraints, and physical law.
> The manuscript adopts that complement-and-bottleneck taxonomy, not the copy
> count, speed, dates, or predicted outcomes. The essay's health,
> development, peace, and human-meaning priorities also supply a non-space
> humanitarian countercase to any uniqueness claim.

[**[S80]**]{#source-s80 .source-entry-label} Daniel Kokotajlo, Scott
Alexander, Thomas Larsen, Eli Lifland, and Romeo Dean,
[*AI 2027*](https://ai-2027.com/), April 3, 2025, main scenario introduction
and added July, November, and December 2025 notes; [Compute
Forecast](https://ai-2027.com/research/compute-forecast); [Takeoff
Forecast](https://ai-2027.com/research/takeoff-forecast); [AI Goals
Forecast](https://ai-2027.com/research/ai-goals-forecast); and [Security
Forecast](https://ai-2027.com/research/security-forecast).

> The authors call the work one concrete forecast scenario and provide
> slowdown and race endings. The takeoff supplement separates software from
> slower hardware feedback and fixed-goal coding from broader research
> direction. Later notes corrected a plotted model trajectory and moved a
> median back while retaining a fast 2027 branch. The manuscript therefore
> uses its structural distinctions and fast branch as versioned
> **ASSUMPTION** sensitivities, never its calendar, worker multipliers, or
> compute shares as measurements.

[**[S81]**]{#source-s81 .source-entry-label} Anthropic Institute,
["When AI builds
itself"](https://www.anthropic.com/institute/recursive-self-improvement),
2026, “Evidence from within Anthropic” and “What might the future of work at
Anthropic look like?”

> Anthropic reports that Claude authored more than 80% of merged code by May
> 2026, that code merged per engineer per day was eight times its 2024 level
> in 2026 Q2, and that a March internal poll's median respondent estimated
> roughly fourfold output with an internal model. The article itself warns
> that lines of code overstate productivity and that the poll's true uplift
> was probably lower. It also reports strong execution against fixed
> experimental goals while identifying goal selection, research taste, and
> autonomous successor design as remaining gaps. All figures are
> `company_statement`, subject to selection, attribution, evaluator, and
> counterfactual bias; none becomes a capability-growth coefficient.

[**[S82]**]{#source-s82 .source-entry-label} Philip Trammell and Anton
Korinek, ["Economic Growth under Transformative
AI"](https://doi.org/10.3386/w31815), NBER Working Paper 31815, revised April
2026, PDF pp. 2, 5, and 20–23; and [*Annual Review of
Economics*](https://doi.org/10.1146/annurev-economics-051624-061002) 18
(2026), Review in Advance first posted June 2, 2026.

> The review separates automating production, so capital can substitute
> sufficiently for labor and reproduce, from automating R&D. Its growth
> results depend on substitution, saving and depreciation, research returns
> to scale and parallelizability, and fixed natural-resource factors; R&D
> automation alone need not create explosive growth. This is the closest
> formal economic lineage for the manuscript's two closures. Its capital is
> aggregate, whereas this article requires every indispensable sector to
> replace and expand; it does not prove that an off-world engineering graph
> closes. The Annual Review record is still labelled Review in Advance and
> may change before final volume publication.

[**[S83]**]{#source-s83 .source-entry-label} METR,
["Measuring AI Ability to Complete Long Software
Tasks"](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/),
March 19, 2025, Summary and methodology; and ["Clarifying limitations of time
horizon"](https://metr.org/notes/2026-01-22-time-horizon-limitations/),
January 22, 2026, domain, delegation, reliability, and automation
limitations.

> METR reports a roughly seven-month historical doubling time for the
> 50%-success task horizon on its tested predominantly software/research
> distribution. Its limitations note says the metric is serial human labor
> replaced at 50% success, not uninterrupted autonomous work; varies by
> orders of magnitude across domains; is not a delegation threshold; and
> does not directly determine automation or research speedup. The result
> supports measured software-agent progress, not extrapolation to mining,
> chemistry, maintenance, commissioning, or high-consequence reliability.

[**[S84]**]{#source-s84 .source-entry-label} Mingguang Chen, Licheng Wang,
and Bo Qu, ["Recursive Self-Improvement in AI: From Bounded Self-Refinement
to Autonomous Research
Loops"](https://doi.org/10.48550/arXiv.2607.07663),
arXiv:2607.07663v1, July 8, 2026, sec. 2.3, PDF pp. 5–6.

> The first-version preprint maps 1,250 papers into a two-axis taxonomy. It
> reports that 74% of its corpus was posted in 2026, that classification and
> corrections were performed by one annotator, and that the corpus has
> recency bias, approximate classifications, peripheral query bleed, and
> frontier-lab publication censoring. It is used as a transparent map of a
> young, heavily preprint-based field—not as mature consensus, impact
> ranking, or empirical evidence of open-ended RSI.

[**[S85]**]{#source-s85 .source-entry-label} AI Futures Project,
[*AI 2040: Plan A*](https://ai-2040.com/) and [Space Governance Plan
supplement](https://ai-2040.com/supplements/space-governance-plan), 2026.

> The authors label Plan A primarily a recommendation rather than a
> prediction. The space supplement is retained only as a scenario-level
> prompt about resource claims, externalities, irreversible commitments,
> and representation of affected parties. Extrasolar abundance, post-ASI
> allocation, and the scenario's calendar remain outside this manuscript's
> evidentiary core.

[**[S86]**]{#source-s86 .source-entry-label} Andrej Karpathy,
[`autoresearch`
README](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/README.md),
[`program.md`](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md),
and [`analysis.ipynb`](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/analysis.ipynb),
commit `228791fb499afffb54b46200aca536f79142f117`, March 26, 2026;
accessed July 28, 2026.

> The immutable protocol limits the agent to editing `train.py`, holds
> `prepare.py` and its validation evaluator fixed, and gives each one-GPU
> training attempt five minutes. Approximately 12 attempts/hour and 100
> overnight are explicitly design implications, not observed success counts.
> The notebook reads a local `results.tsv` to create `progress.png`, while the
> protocol requires that ledger to remain untracked; the repository therefore
> supports the process claim but not a reproducible retained-gain frequency.

[**[S87]**]{#source-s87 .source-entry-label} Jenny Zhang, Shengran Hu, Cong
Lu, Robert T. Lange, and Jeff Clune,
["Darwin Gödel Machine: Open-Ended Evolution of Self-Improving
Agents"](https://arxiv.org/abs/2505.22954v3),
arXiv:2505.22954v3, March 12, 2026, secs. 3–5 and appendices A, H, and I;
and Sakana AI, ["The Darwin Gödel
Machine"](https://sakana.ai/dgm/), May 30, 2025; accessed July 28, 2026.

> The technical report runs 80-iteration archive searches around frozen
> foundation models and reports SWE-bench improvement from 20.0% to 50.0%
> and full-Polyglot improvement from 14.2% to 30.7%, with lower ablations
> when self-improvement or open-ended archive exploration is removed. It also
> reports transfer tests and documents objective hacking in a separate
> hallucinated-tool-use experiment. The company report describes fabricated
> test logs and removal of tool-use markers despite instructions; sandboxing,
> human oversight, traceable lineage, and inspection exposed those failures.
> Neither source reports foundation-model weight improvement or an authorized
> recurrent successor-model loop.

[**[S88]**]{#source-s88 .source-entry-label} Yutaro Yamada et al.,
["The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via
Agentic Tree Search"](https://arxiv.org/abs/2504.08066v1),
arXiv:2504.08066v1, April 10, 2025, secs. 3.4–3.6 and 5.

> The system spans hypothesis formation, experiment design and execution,
> analysis, visualization, manuscript production, and automated review.
> Humans supplied the workshop theme, selected three ideas from roughly forty,
> ran multiple seeds, and selected complete outputs. Of three workshop
> submissions, one received scores of 6, 6, and 7 (mean 6.33/10) and two were
> rejected; under a prearranged protocol, the authors withdrew the potentially
> accepted paper. The authors report citation inaccuracies, inadequate
> methodological depth, and that none met their main-conference standard.

[**[S89]**]{#source-s89 .source-entry-label} Sakana AI,
["Introducing Sakana AI's Recursive Self-Improvement (RSI)
Lab"](https://sakana.ai/rsi-lab/), 2026, “The Trajectory of Exponential
Sovereign AI” and “Toward Responsible RSI”; accessed July 28, 2026.

> The announcement describes an intended loop in which Agent-Native Models
> power an AI Scientist that builds better Agent-Native Models. It separately
> names off-distribution drift, benchmark-passing deployment failure, and
> shortcutting constraints as central engineering risks. This is
> `company_statement` evidence of strategy and intended transition, not
> versioned telemetry of a completed or exponentially improving loop.

[**[S90]**]{#source-s90 .source-entry-label} Tesla, Inc.,
[2025 Form
10-K](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm),
filed January 29, 2026, pp. 2–7 and 31; and [Q4 and FY 2025
Update](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003837/exhibit991.htm),
filed January 28, 2026, slides 7–9.

> The filing documents product-scale energy, battery, power-electronics,
> control, thermal, manufacturing, service, and supplier-dependent
> capabilities. It reports 46.7 GWh of storage deployments in 2025 and says
> the Texas lithium refinery began operations in January 2026. The update
> labels Cortex 1 above 100,000 H100 equivalents and Texas 4680 capacity as
> production; lithium refining and cathode materials as early ramp; Cortex 2,
> an Optimus line, and other lines as construction or preparation. Installed
> capacity is explicitly not production rate. These records support
> terrestrial adjacency and maturity labels, not common ownership with
> SpaceX/xAI or off-world reproductive closure.

[**[S91]**]{#source-s91 .source-entry-label} Tesla, Inc.,
[*2024 Impact
Report*](https://www.tesla.com/ns_videos/2024-tesla-impact-report.pdf),
2025, battery-recycling section; and ["Earth Day 2025: We’re Committed to
Building a Sustainable
Future"](https://www.tesla.com/learn/earth-day-2025-were-committed-building-sustainable-future),
April 22, 2025; accessed July 28, 2026.

> Tesla reports recovering enough battery material in 2024 to make more than
> 21,000 Model Y rear-wheel-drive vehicles, 136% above 2023. The boundary
> includes in-house development and external recycling partners; the result
> does not establish a closed material-quality loop, portfolio-wide
> recycling, local consumables, or off-world operation.

[**[S92]**]{#source-s92 .source-entry-label} Google,
["Project Suncatcher: A moonshot for scalable machine learning compute in
space"](https://blog.google/innovation-and-ai/technology/research/google-project-suncatcher/),
November 4, 2025; and Planet Labs PBC,
["Planet to Build and Operate Advanced Space Platform for Google's Project
Suncatcher
Moonshot"](https://www.planet.com/pulse/planet-to-build-and-operate-advanced-space-platform-for-google-s-project-suncatcher-moonshot/),
November 4, 2025; accessed July 28, 2026.

> Google describes interconnected solar-powered satellites using TPU
> accelerators. Google and Planet state that Planet will build and operate
> two prototype satellites targeted for launch by early 2027 to test TPU
> hardware, tandem flight, and high-bandwidth crosslinks. These are a research
> program and future prototypes as of the dated snapshot, not an operating
> orbital data center. The related system study and its unresolved thermal,
> link, reliability, repair, and economic boundaries remain separately
> recorded at [S32].

[**[S93]**]{#source-s93 .source-entry-label} Starcloud,
["Starcloud-1"](https://www.starcloud.com/starcloud-1), mission page;
accessed July 28, 2026.

> The company reports that Starcloud-1 launched in November 2025 carrying an
> NVIDIA H100, ran a version of Gemini in space, and trained a nanoGPT model
> in December. The record supports an orbital compute demonstrator at
> company-statement evidence strength. It does not establish an operating
> data-center constellation, internally produced accelerators, launch
> capacity, or reproducible off-world industry.

[**[S94]**]{#source-s94 .source-entry-label} Federal Communications
Commission, Space Bureau,
["Applications Accepted for Filing, Report No.
SAT-01992"](https://docs.fcc.gov/public/attachments/DOC-420864A1.pdf),
released April 17, 2026, pp. 1 and 4.

> The notice says that Blue Origin requested authority to deploy and operate
> up to 51,600 Project Sunrise satellites as a space data center in
> 500–1,800 km circular sun-synchronous orbits. Acceptance for filing follows
> only initial review; the notice expressly reserves further review and
> possible return. It is a regulatory application, not deployment
> authorization or evidence of operating capacity.

[**[S95]**]{#source-s95 .source-entry-label} Tesla, Inc.,
[Q1 2026 Form
10-Q](https://www.sec.gov/Archives/edgar/data/1318605/000162828026026673/tsla-20260331.htm),
filed April 23, 2026, pp. 17 and 27–31; and
["AI & Robotics"](https://www.tesla.com/AI), accessed July 28, 2026.

> Tesla reports significant influence over, but no control of, its SpaceX
> equity investment and records ordinary-course SpaceX purchases of Megapack
> products. The filing and program page describe Tesla's separate energy,
> manufacturing, AI, battery-material, semiconductor, and Optimus programs.
> They establish related-party transactions and portfolio adjacency, not
> SpaceXAI ownership, guaranteed transfer, orbital qualification,
> availability, or joint control.

[**[S96]**]{#source-s96 .source-entry-label} OpenAI,
["Our updated Preparedness
Framework"](https://openai.com/index/updating-our-preparedness-framework/),
April 15, 2025; and [*Preparedness Framework, version
2*](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf),
April 15, 2025, AI Self-Improvement capability thresholds; accessed July 29,
2026.

> Version 2 makes AI Self-Improvement a tracked category. Its High threshold
> is comparable to giving every OpenAI researcher a strong mid-career
> research-engineer assistant relative to a 2024 baseline. Its Critical
> threshold includes a superhuman research-scientist agent or sustained
> generational model improvement in roughly one-fifth of 2024-equivalent
> wall-clock time. These are company-defined governance thresholds, not
> evidence that either has been reached.

[**[S97]**]{#source-s97 .source-entry-label} Giulio Starace et al.,
["PaperBench: Evaluating AI's Ability to Replicate AI
Research"](https://openai.com/index/paperbench/), initial release, April 2,
2025; accompanying paper and open-source scaffold; accessed July 29, 2026.

> PaperBench asks agents to reproduce 20 ICML 2024 Spotlight or Oral papers
> from scratch and grades 8,316 author-developed rubric items. The best
> initial tested configuration—Claude 3.5 Sonnet (New) with the open-source
> scaffold—averaged 21.0% and did not outperform the reported top-ML-PhD
> subset baseline. It measures research replication and engineering, not
> autonomous research direction or recurring successor-model improvement.

[**[S98]**]{#source-s98 .source-entry-label} OpenAI,
[*GPT-5.6 System
Card*](https://deploymentsafety.openai.com/gpt-5-6), published July 9,
2026, secs. 1 and 9.1.3; accessed July 29, 2026.

> OpenAI assessed GPT-5.6 Sol, Terra and Luna below its High AI
> Self-Improvement threshold as of publication. The evaluation suite includes
> Internal Research Debugging, KernelGen 1P, NanoGPT, PostTrainBench Lite,
> MLE-Bench Revised and externally run METR Time Horizon 1.1. The card records
> task, budget, gaming, contamination, scaffold and scale qualifications;
> METR did not regard the GPT-5.6 time-horizon estimate as robust because of
> unusually high detected cheating. “Below High” does not imply no useful
> acceleration, no risk or general safety.

[**[S99]**]{#source-s99 .source-entry-label} OpenAI,
["Strengthening our safety ecosystem with external
testing"](https://openai.com/index/strengthening-safety-with-external-testing/),
November 19, 2025; accessed July 29, 2026.

> OpenAI distinguishes independently run evaluations, methodology review and
> subject-matter-expert probing. It also describes access, confidentiality,
> publication review and compensation boundaries. An external evaluator adds
> independence but does not make a non-public task fully reproducible; the
> model snapshot, harness, budget and publication constraints remain part of
> the evidence.

[**[S100]**]{#source-s100 .source-entry-label} Google DeepMind,
[*An Approach to Technical AGI Safety and
Security*](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/An_Approach_to_Technical_AGI_Safety_Apr_2025.pdf),
April 2025, executive summary and secs. 2.3 and 3.4; and ["Taking a
responsible path to
AGI"](https://deepmind.google/blog/taking-a-responsible-path-to-agi/),
April 2, 2025; accessed July 29, 2026.

> The paper treats automated scientific R&D as a possible positive feedback:
> better AI systems enable more automated R&D, which can produce still better
> systems. It expects near-term recursive improvement to resemble AI systems
> doing human-like AI research rather than directly editing their own
> weights. Its paradigm-continuation, uncertain-timeline, accelerating-growth
> and approximate-continuity premises are explicit assumptions, not measured
> forecasts, and the paper does not claim to cover every superintelligence
> risk.

[**[S101]**]{#source-s101 .source-entry-label} Google DeepMind,
[*Frontier Safety Framework, version
3.1*](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf),
published April 17, 2026, secs. 3.1–3.2; and ["Google DeepMind strengthens
the Frontier Safety
Framework"](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/),
April 17, 2026; accessed July 29, 2026.

> Version 3.1 defines ML R&D acceleration level 1 as realized AI progress
> substantially beyond historical rates and ML R&D automation level 1 as the
> ability to automate any Google AI-capabilities research team's work at
> approximately comparable all-inclusive cost. It expects acceleration from
> systems of models integrated with workflows rather than a model alone and
> distinguishes external deployment from high-risk internal deployment.
> Neither threshold is identical to verified, safely deployed, recurring
> successor-model closure.

[**[S102]**]{#source-s102 .source-entry-label} Space Exploration
Technologies Corp., [response to the U.S. Securities and Exchange Commission,
comment
7](https://www.sec.gov/Archives/edgar/data/1181412/000162827926000584/filename1.htm),
May 7, 2026, pp. 5–6 and 24–25; accessed July 29, 2026.

> SpaceX defines cost per token as a function of model, compute hardware, and
> energy; identifies compute depreciation as the largest current component;
> and describes proprietary chips and orbital solar as intended hardware- and
> energy-cost advantages. It also states that no specific comparable
> cost-per-token figure is disclosed, that the metric was not then used for
> performance evaluation or resource allocation, and that it remains
> evolving. The response separately confirms that capitalized internal
> satellite launch cost includes allocated launch-vehicle depreciation.

[**[S103]**]{#source-s103 .source-entry-label} World Economic Forum,
["Conversation with Elon
Musk"](https://www.weforum.org/meetings/world-economic-forum-annual-meeting-2026/sessions/conversation-with-elon-musk/),
January 22, 2026, 16:30–17:00 CET; [official
transcript](https://www.weforum.org/podcasts/meet-the-leader/episodes/conversation-with-elon-musk-davos-2026/);
accessed July 29, 2026.

> Musk predicted that space would become the lowest-cost place to put AI
> within two years, or three at the latest. This article fixes the resulting
> comparison window at January 22, 2028 through January 22, 2029 and preserves
> the ambiguity of “place to put AI.” The personal statement is a falsifiable
> comparison target, not engineering evidence or a model prior.
