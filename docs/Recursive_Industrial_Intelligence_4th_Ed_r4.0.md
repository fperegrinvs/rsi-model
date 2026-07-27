# Recursive Industrial Intelligence

## Fourth Edition, revision 4.0 · July 2026

**Leonardo Stern · Independent researcher**

*A self-sustaining, self-expanding space industrial system is coherent as an argument; whether it is feasible or economical is a question for models. This standalone edition preserves the executed Third Edition models and adds an explicit autonomous seed, its knowledge package, its material flows, and the dynamics by which it attempts to reproduce.*

> **Status.** Fourth Edition r4.0 release candidate, completed 2026-07-27 from the frozen Third Edition r3.5 baseline and not yet represented as an immutable tag or version DOI. The complete implementation and artifacts are published on the repository's `main` branch; the final tagged build must add the immutable URL, release date, and version DOI. **Standalone:** this document carries the full argument and requires no prior edition; earlier editions are intellectual history, not dependencies. The inherited r3.5 results regenerate via `scripts/run_baseline.py`, `run_part2.py`, and `run_deep.py` and are checksummed in `outputs/MANIFEST.md`. The new integrated-bootstrap results regenerate via `scripts/run_fourth.py` and are checksummed separately in `outputs/fourth/MANIFEST.md`. They reserve explicit terms for material flows, seed sizing, embodied autonomy, process-specific gravity, construction and commissioning, source transfers, a rate-limited Earth counterfactual, the intelligence–compute coupling, and debris state dynamics — and test their consequences through declared, stylized proxies rather than resolving the underlying engineering. Every structural coefficient in the new layer is ASSUMPTION-class; its outputs are scenario implications, not measurements, probabilities, engineering estimates, or forecasts. The completed change ledger is `docs/FOURTH_EDITION_PLAN.md`; see Appendices B–D.

## Abstract

This paper develops and tests a conditional thesis: advanced AI, reusable
launch, robotics, energy systems, and automated manufacturing could be
combined into an industrial system beyond Earth that maintains and expands
its own productive capacity. This Fourth Edition retains the complete
Third Edition quantitative baseline and expands the object of analysis from
an abstract industrial substrate to a reproducible autonomous seed:
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
The inherited model begins with positive capacity in all ten sectors and
omits construction lags, commissioning, yield ramps, and minimum efficient
scales; its doubling times are stylized capacity-model first passages, not
factory-construction or seed-commissioning forecasts. Part II
builds an affine levelized-cost model for terrestrial and space compute,
separating integrated disposable satellites from serviceable/reusable
platforms. At central inputs, generic LEO compute costs 3.97 times Earth on
the serviceable-platform architecture and 4.90 times Earth if integrated
and disposable; the disclosed Starmind AI1 mass case remains 2.56 and 2.90
times Earth, respectively. The analysis therefore supports neither a point
forecast of autonomous industry nor present orbital-compute parity. It
identifies the architecture-dependent measurements and demonstrations that
would most change those conclusions. A new 18-sector, 17-material-group
integrated-bootstrap model then represents an installed operating seed —
physical equipment with stylized autonomy, intervention, construction, and
commissioning constraints — and asks how much installed mass is
sufficient, whether its material graph can close first on the Moon and
later across asteroidal sources, and whether it can reach a second
operating production cell without routine human intervention. Under the
declared central assumptions, the minimum-mass lunar design retaining an
Earth-supplied vitamin stock is 216.7 t installed — 58.1 t (27%) of it
that stock — and first reaches two operating-cell equivalents at
11.2 years, holding 2.29 equivalents at year 40; the configured strict
lunar-only source graph is structurally infeasible; and a synthetic
composite Moon–asteroid portfolio satisfies the same constraints at
185.5 t, reaches two cell-equivalents at 22.8 years, and reaches 12.55 at
year 40. These are deterministic consequences of a stipulated
architecture and assumption ensemble (Part I.8), not seed designs,
engineering estimates, or forecasts. Ablation of the declared
intelligence coupling leaves every central trajectory unchanged — growth
is material-limited at every step, so the coupling's dynamic
coefficients never bind — and reproduction is durable only in the
Moon–asteroid case. The model operationalizes the
coupled loop and sharpens its material and autonomy conditions; it does
not demonstrate that the assumed processes, source portfolio, AI gains,
or industrial closure exist.

**Keywords:** recursive industrial improvement; space manufacturing;
industrial closure; orbital compute; lunar industry; multisector capacity;
autonomous industrial seed; embodied autonomy; lunar materials;
techno-economics; Monte Carlo.

## Scope and Status

This is a strategic hypothesis and research program with, now, its first
quantitative core — not a techno-economic demonstration. It identifies
necessary conditions, bottlenecks, and discriminating tests for a
self-expanding industrial system, computes what its own assumptions imply,
and states throughout which of its six propositions each conclusion rests on.

The reference system in this edition is **machine-only**: no resident human
population, agriculture, or biosphere-scale life-support loop is required
for industrial reproduction. Human settlement can create demand and impose
additional requirements, but it is not a prerequisite of the thesis. Water,
hydrogen, carbon, nitrogen, and oxygen remain important as propellants,
reductants, coolants, lubricants, polymers, process gases, and chemical
feedstocks; removing agriculture narrows the closure problem but does not
remove volatile chemistry from it.

Six distinct propositions run through this document and carry different
evidence:

- **(P1)** A recursively expanding industrial system is conceptually
  possible — a respectable case is made.
- **(P2)** Such a system might eventually be technically feasible —
  quantitatively explored for both the inherited industrial substrate and
  a first explicit integrated bootstrap (Part I): outcomes span failure to
  sustained expansion across named assumption sets, with the feasibility
  margin localized to architecture-specific bottlenecks. The coupled
  intelligence–industry functions now have an operational stylized form,
  but their coefficients remain assumptions rather than evidence of
  complete-system feasibility (III.6).
- **(P3a)** Orbital and lunar *compute during the Earth-dependent bridge*
  would be economically competitive — now quantified (Part II) and, at
  anchored values, *negative*, with crossover requiring a specific,
  currently unanchored corner of parameter space.
- **(P3b)** A *mature, high-closure* space-industrial ecology would
  eventually obtain a structural economic advantage over terrestrial
  expansion — **unquantified**: Part II prices the bridge architectures,
  not an ecology that manufactures its own power systems, radiators,
  structures, and replacement hardware off Earth, so nothing in this
  document establishes or refutes P3b (the Fourth Edition couples
  physical and compute quantities, not the mature ecology's full costs).
- **(P4a)** The companies are deliberately integrating launch,
  communications, AI, terrestrial and orbital compute, chip design and
  manufacture, and prospective off-world energy and manufacturing —
  substantially documented, since SEC-filed offering materials associated
  with the S-1 (the Rule 433 free-writing prospectus and incorporated
  materials) name orbital compute, lunar manufacturing and energy,
  in-orbit manufacturing, manufacturing on the Moon and Mars, asteroid
  mining, and "interplanetary industrialization" among the initiatives
  [S27].
- **(P4b)** That this integration is intended to produce recursive
  industrial closure — inferential, with no closure program, seed bill of
  materials, reproduction metric, or minimum-cut roadmap published, and
  assessed against competing explanations (Part III).

The P4 split matters: the two halves carry materially different
evidential status, and earlier editions conflated them. Conclusions are
licensed by the strongest proposition they rest on, not by the
conjunction of all six.

**Evidential classes.** Documented statements; announced initiatives;
technically grounded pathways; inferred strategy; speculative closure — as
in the Second Edition — plus one new rung: **computed**, meaning derived
mechanically from stated assumptions by the companion model (public repository with checksummed output manifest, Appendix C). A computed result
inherits the epistemic class of its weakest input; structural coefficients
are ASSUMPTION-class throughout, so no computed result is a measurement.
Every computed number below carries its assumption-set label
(conservative / central / optimistic); a result quoted without its set
label is a misquotation.

| evidential category | proposition or observation | current status |
|---|---|---|
| Documented | Mars-city objective; integrated energy and manufacturing programs; AI research mission; the SEC-filed off-world initiative list (P4a) | direct statements and regulatory filing |
| Announced / partly advanced | Terafab, Intel participation, executed county agreements, and a named orbital-silicon line | declared initiative with unsettled implementation |
| Technically grounded | ISRU, autonomous excavation, robotic construction, and the self-replicating-factory literature (P1/P2 pathway) [S4, S5, S23, S24] | recognized engineering pathway; system closure undemonstrated |
| Computed | industrial-substrate feasibility, material-category-resolved seed and second-cell scenarios (P2), and bridge-economy compute costs (P3a) | mechanical implications of assumption-class inputs, not measurements or empirical probabilities |
| Inferred | the observed portfolio is intended to progress from integrated off-world industry to recursive closure (P4b) | strategic synthesis; closure-specific observables remain absent |
| Speculative | a mature high-closure ecology obtains a structural economic advantage (P3b) | physical quantities are coupled in r4.0; complete mature-system economics remain unquantified |

## Executive Summary

This document develops a unified hypothesis: the deepest strategic value of
advanced AI, reusable launch, energy systems, robotics, and automated
manufacturing may lie in combining them into a recursively improving
industrial system beyond Earth. The end state is not merely a rocket fleet,
a settlement, a humanoid robot, or a frontier model, but a distributed
industrial ecology able to sustain itself, expand productive capacity, and
progressively reduce Earth dependence.

> **Central proposition.** Once a space-based industrial system can obtain
> local energy and materials, maintain its machinery, manufacture additional
> productive equipment, and coordinate itself through AI, the primary
> constraint shifts from acquiring terrestrial inputs to allocating
> productive throughput over time.

That proposition distinguishes two growth regimes. An orbital data center
whose servers, structures, power systems, and replacements continue to be
made on Earth is **deployed capacity**, not a self-expanding industry:

$$
\frac{\mathrm d C_{\mathrm{orbit}}}{\mathrm d t}
= q_c L_{E\rightarrow O}(t)-\delta_C C_{\mathrm{orbit}}.
$$

At a constant Earth-to-orbit delivery rate $L_{E\rightarrow O}$, capacity
grows approximately linearly while depreciation is small and ultimately
approaches $q_cL_{E\rightarrow O}/\delta_C$. By contrast, a closed
industrial stock that allocates a fraction of its own output to producing
additional productive equipment follows the idealized endogenous law

$$
\frac{\mathrm d H}{\mathrm d t}=(r-\delta_H)H,
$$

and compounds only when $r>\delta_H$. Off-Earth location does not create
that acceleration: **reproductive closure does**. The role of off-Earth
industry is to combine that endogenous growth regime with access to matter,
energy, and usable area outside Earth's biosphere and society-priced siting
constraints. Earth-fed orbital compute can therefore raise intelligence at
a constant deployment rate without crossing the industrial-reproduction
threshold; the two cases must not be conflated.

The framework contains two coupled loops. In the digital loop, AI improves
software, research, engineering, evaluation, and coordination. In the
physical loop, AI and robots improve mining, refining, power, manufacturing,
construction, transport, and the production of additional compute. Each
loop strengthens the other:

    better intelligence → better automation → more productive capacity →
    more compute → better intelligence

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

This edition prices the passage and models the seed. Five headline results:

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
   load-bearing where the sampled vitamin gap is deepest. That identity is
   conditional on a homogeneous electronics-productivity assumption, not a
   measurement of real electronics closure.
2. **Balanced-capacity doubling and durable expansion are different
   outcomes.** The headline replication metric is λ(t) =
   min_j K_j(t)/K_j(0) ≥ 2: every modeled sector has doubled in its own
   capacity units. It is not a claim that a commissioned second physical
   factory exists. The endpoint records realized, post-shock growth; the
   pre-shock allocation endpoint remains a diagnostic. In central
   ensembles, 267/400 LEO, 224/400 lunar, and 60/400 Mars runs are
   expanding at year 30, but only 122, 20, and 4 respectively sustain
   positive realized growth throughout years 25–30. Median balanced
   doubling among runs that reach it is about 26.0 years in LEO, 5.0 on
   the Moon, and 11.0 on Mars. The Earth-import-cut LEO result is expressly
   conditional on continued capture feed and is not an autonomous-ecology
   result.
3. **The space-compute crossover is an architecture story, not a
   launch-price story.** At central inputs, generic LEO compute is 3.97×
   Earth on a serviceable/reusable platform and 4.90× if the satellite is
   integrated and disposable. The Starmind AI1 disclosure scenario is
   2.56× and 2.90×, respectively. None of the 2,000 shared-draw Monte Carlo
   runs in any reported architecture/reference cell favors space. Negative
   median break-even launch prices show why: qualification cost, hardware
   and platform life, and utilization can dominate launch. The
   deterministic aspirational case reaches 0.76× only by combining company
   targets with three favorable, unpublished model bounds and is assigned
   no probability.
4. **The installed seed is a material-and-knowledge graph, not a cargo
   total.** The new 18-sector, 17-material-group layer requires physical
   equipment, digital tools, industrial memory, experiments, task-resolved
   autonomy, gravity-compatible processes, and reproduction to a second
   operating cell. It sizes an already installed, operating seed —
   deployment, unpacking, and first commissioning are not simulated — and
   its reproduction metric is first passage to two operating-cell
   equivalents in a continuous aggregate, not a discretely commissioned
   second factory. Under the declared central assumptions, the
   Earth-vitamin lunar bridge requires 216.7 t installed, of which 58.1 t
   (27%) is Earth-supplied vitamin stock — a substantially
   Earth-provisioned seed, not a nearly closed one — reaching two
   cell-equivalents at 11.2 years and holding 2.29 at year 40. The
   terrestrial rehearsal reaches two at 9.2 years but holds only 1.93 at
   year 40: reproduction occurred once and was not durably retained, the
   same transient-versus-durable distinction Part I's endpoint hierarchy
   enforces. The configured strict lunar-only source graph is structurally
   infeasible — its trace inputs cannot reproduce the assumed electronics
   and process-equipment stack, in the central case and in every draw. A
   deliberately synthetic composite Moon–asteroid portfolio satisfies the
   same constraints at 185.5 t, reaches two cell-equivalents at 22.8
   years, and reaches 12.55 at year 40. Across 200 deterministic
   assumption draws, the lunar-bridge, strict-lunar, and Moon–asteroid
   cases are model-feasible in 126, 0, and 187 draws (the terrestrial
   rehearsal in 83); these frequencies measure the satisfying volume of
   the declared parameter box, not success probabilities.
5. **The declared AI coupling does not drive the Fourth-layer growth.**
   Ablations that zero or freeze the intelligence–industry coupling
   reproduce every central trajectory exactly: realized construction is
   capped by material availability at every step, so the coupling's
   dynamic coefficients never bind — the headline growth is a
   material-throughput result, not an artifact of the assumed AI
   feedback, and symmetrically these trajectories cannot test that
   feedback. The assumed AI level is load-bearing *statically* instead:
   at base autonomy the lunar-bridge and Moon–asteroid seeds fail the
   feasibility threshold outright. Durability splits the cases the same
   way — the lunar bridge retains two cell-equivalents in all 126
   feasible draws yet has negative net reproduction over the final five
   years in every one of them; only the Moon–asteroid network expands
   durably (187/187).

The Fourth layer also makes one architecture boundary stateful:
**industrial closure does not license a dense orbital shell.** Active,
derelict, and fragment stocks feed a **five-year fragment
creation-to-clearance ratio** $R_{\mathrm{debris}}$ — a flow ratio over
the final five years, not a branching-process reproduction number or a
derived criticality threshold. In the declared year-40 scenarios, the
Earth-fed orbital cases clear more fragments than they create
($R_{\mathrm{debris}}=0.61$ with weak mitigation and 0.35 with strong),
while dense endogenous deployment creates roughly 5.5× what it clears
under both mitigation levels ($R=5.53$ weak and 5.58 strong — the ratio
is not monotonic in mitigation strength even as the fragment stock falls
from 16.5 to 12.6, one reason it is a stress-test indicator rather than
a safety measure). A sparse distributed topology sits at the boundary
ratio of 1.00 with an empty fragment stock only because its
collision-kernel multiplier is explicitly set to 0.01. These are
topology stress tests, not orbital traffic forecasts or
cascade-threshold results [S45–S49].

The strategic assessment (Part III): the evidence **substantially
establishes deliberate integrated space–AI–industrial development (P4a)**
at the level of declared direction and early implementation — the
initiative list in the SEC-filed offering materials and the first-party
messaging are difficult to explain
under a purely terrestrial reading. It **does not establish recursive
closure as the objective (P4b)**: the closure-specific observables — seed
bills of materials, reproduction metrics, minimum-cut roadmaps, locally
reproducible production equipment — remain absent. What has changed is
that the discriminating indicators are now *model-ranked*: the rational
next moves of a closure-seeking actor — electronics-closure engineering,
loss-tolerant orbital-compute persistence, materials-recovery recycling —
are exactly the observations the models identify as informative.

## How to read this document

The four parts carry different kinds of claim and can be read
independently:

- **Part I** is model: the inherited ten-sector capacity model and the
  new integrated-bootstrap layer. Its results are computed implications
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
frequency-not-probability convention — are defined in Scope and Status
and apply everywhere. Appendix A carries parameter provenance,
Appendix B the revision history (including what changed under each
external review), Appendix C reproducibility, and Appendix D the
complete model specification.

---

# Part I — Technical Feasibility

## I.1 Recursive self-improvement: the digital loop

Recursive self-improvement (RSI) occurs when an intelligent system
contributes to the process that produces a more capable successor. The
useful unit is not a public model release but a verified improvement loop:
identify a weakness, propose a change, run an experiment, evaluate, deploy,
and use the improved system to accelerate the next cycle.

$$
\begin{aligned}
I(t+1) &= I(t) + \Delta I(t), \\
\Delta I &= L \times G
\end{aligned}
$$

I is effective intelligence; L is the number of useful loops completed; G
is the average gain per successful loop. The loop rate is constrained by
the least scalable part of the development system:

$$
L = \min\!\left\{L_C(C), L_D(D), L_X(X), L_V(V), L_R(R)\right\}
$$

— each conversion function turning its resource (compute, data,
experimental throughput, verification capacity, deployment reliability)
into verified loops per unit time. Efficiency is partly a function of
intelligence, E(t) = f(I(t)): more capable systems may improve coding,
architecture search, synthetic-data generation, hardware design, factory
scheduling, scientific modeling, and evaluation design. The form of f —
logarithmic, linear,
superlinear, saturating — is unknown; a rigorous analysis identifies which
regime observed loop completion supports rather than assuming takeoff.
Public releases are lagging indicators; the strategically relevant measure
is verified improvement loops per calendar time. The verification term V
recurs in a second role as the governing safety constraint (Part III.4).
Time-spaced releases nevertheless remain useful: they generate real-world
feedback, revenue, reliability data, and operational learning. A release is
part of the loop, but it is not the loop.

## I.2 Recursive industrial improvement: the physical loop

Digital intelligence depends on a physical substrate: chips, data centers,
electricity, cooling, networks, factories, labor, materials, logistics,
maintenance — a dependency inventory, not a sum; any term can bind. The
physical recursive loop begins when AI and robotics improve the production
of those inputs: better intelligence designs and operates better machines;
better machines expand energy and manufacturing; expanded industry produces
more compute; more compute supports better intelligence.

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

**The embodied-autonomy threshold.** A mobile manipulator can have enough
joints, reach, payload, sensing, and tool interfaces to span many industrial
tasks without being able to close the labor loop. Kinematic sufficiency is
not cognitive sufficiency. The threshold relevant here is whether the
combined robot-and-AI system can diagnose unfamiliar faults, choose and use
tools, execute long-horizon construction and repair, recover from failed
actions, learn from intervention, and verify that the restored machine is
safe to return to service. Present humanoid programs, including Optimus, are
evidence of an intended general-purpose hardware form, not evidence that
this unscripted industrial task set has been solved. The Fourth Edition
therefore treats embodied autonomy as task coverage and recovery capability,
not as robot count or degrees of freedom.

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

    D_advantage = f(uniqueness, causal linkage, coverage, quality,
                    accessibility, integration, verification value)

Generation is insufficient; the data must be integrated and attributable
enough to train on. Tesla's first CIO has described building the custom Warp
enterprise system in roughly four months in 2012 after the company rejected
off-the-shelf ERP, then extending it continuously so operations could change
without waiting on a vendor [S15]. SpaceX independently built its own internal
manufacturing and enterprise system, Warp Drive [S16]. The convergence on the
same build-don't-buy pattern is evidence that iteration speed, not a common
brand name, drives the architecture.

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
operator [S17, S30]. No valid conversion exists between those regimes, so the
figures are not an advantage multiple. More informative disclosures concern
structure: an occupancy network trained on 1.4 billion fleet video frames and
an auto-labeling system replacing roughly five million hours of manual
annotation [S17]. The aerospace analogue is thirteen heavy-lift flight tests
by mid-2026: few observations, each with high information content [S31].
These quantities demonstrate data generation and integration capacity, not
autonomous industrial closure.

## I.3 Why space changes the cost structure

On Earth, useful locations compete with communities, ecosystems,
jurisdictions, and alternative uses. Off Earth, the monetary price of
unused area approaches zero — but infrastructure does not become free; the
cost *changes kind*, from purchasing scarce terrestrial sites and
coordinating human institutions toward transporting, converting, and
maintaining matter through an automated production network:

    Earth: land + permits + construction + energy + materials + labor + coordination
    Space: transport + energy + extraction + refining + manufacturing + maintenance + coordination

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

$$
a_c=\omega^2R.
$$

One terrestrial $g$ requires about 30 rpm at a one-meter radius or
9.5 rpm at ten meters. An ideal rotor consumes energy to spin up and stores
$E=\tfrac12 I\omega^2$; it does not require continuous power merely to
remain in uniform rotation. The engineering cost lies in structural mass,
containment, bearings or magnetic suspension, balance control, vibration,
rotating power/data interfaces, spin losses, maintenance, and the inability
to share one acceleration geometry across every process. Lunar gravity is
therefore plausibly enough for many bulk operations, while local
centrifugation is the fallback for gravity-sensitive steps. No credible
single dollar estimate exists without a process list, throughput, rotor
radius, and maintenance architecture. The inherited ten-sector model has
none of these variables; the Fourth layer adds declared per-process
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

## I.4 Depreciation: the harsh term

$$
\frac{\mathrm d H}{\mathrm d t} = (r-\delta)H
$$

Every claim ultimately reduces to whether gross replication r exceeds
depreciation δ. Terrestrial industry operates inside an ambient repair
economy; space assets have none of it.

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

Five quantities must be kept apart, since compressing them was an
internal inconsistency of earlier revisions: **physical degradation**,
**functional failure**, **accounting depreciation**, **economic
obsolescence**, and **frontier-equivalent capacity loss**. The last two
are not physical — an accelerator does not vanish because a better one
exists — so obsolescence enters a growth equation only where H is
measured in quality-adjusted or frontier-equivalent capacity, which is
why the terrestrial paradox above is a statement about accounting and
frontier equivalence rather than about matter. The corrected form,
decomposed per environment,

$$
\delta_{\mathrm{total}}
= \delta_{\mathrm{wear}}
+ \delta_{\mathrm{catastrophic}}
+ \delta_{\mathrm{obsolescence}}
+ \delta_{\mathrm{logistics}}
$$

is what the model implements per sector and per location: space raises the
catastrophic and logistics terms, Earth raises the obsolescence term, wear
differs modestly. The environment drives δ upward through radiation,
thermal cycling, micrometeoroids and debris, vacuum effects, regolith dust,
and the absence of an ambient repair economy.

**Collision-cascade boundary.** Kessler risk is not an unusually large
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
assigned a silent proxy value. The Fourth layer supplies a first
aggregate stress test — active assets, intact derelicts, and a fragment
index, reported through a five-year fragment creation-to-clearance ratio
(I.8, D.1); a shell-resolved model tracking trackable and untrackable
fragments, collision-generated yield, and disposal and natural clearance
by orbital region, with expected hazardous descendants per object as the
cascade metric, remains queued (ROADMAP). Lunar orbit does not remove the issue: breakup
simulations find strongly orbit-dependent evolution, including long-lasting
debris in some low lunar orbits and nonuniform lunar impact patterns [S46].

One environment-specific case partly cuts the other way, and it is narrower than earlier drafts of this argument claimed. For **short-lived compute payloads in very low orbit**, aligning useful life with accelerator-obsolescence cycles reduces the economic value of repair: hardware retired within a few years regardless costs less to be unable to fix. The qualifications are substantial. Natural decay depends on altitude, ballistic coefficient, and solar activity — small spacecraft near 400 km can decay within five years, but beyond 500 km five-year decay is not assured and some objects persist for decades. The leading published orbital-compute architecture in fact places its cluster near **650 km** in dawn-dusk sun-synchronous orbit, chosen for illumination rather than disposal [S32], so the concession does not describe that design. Nor is disposal free: station-keeping, collision avoidance (large-constellation operators report on the order of a thousand automated avoidance manoeuvres per day [S27]), replacement launch, network spares, and residual capital loss all remain — and the same source that calls orbital repair impracticable proposes redundant provisioning instead, which is a cost, not its absence [S32]. The concession therefore covers some payload classes in very low orbit and does not generalize: mines, refineries, machine tools, and robots must last decades to close a loop. In this edition's models it lands in Part II (compute payloads), while Part I's industrial δ decomposition stands.

**The clock-setting component.** In any partially closed system, the
component with the shortest replacement horizon that cannot yet be produced
or stockpiled locally sets a hard clock on the entire complex. Closure
priority follows failure rate × non-replaceability, not mass fraction.
Viability requires:

$$
T_{\mathrm{replenish},j} < T_{\mathrm{effective\ survival},j}
\qquad \text{for every critical component class } j
$$

Effective survival includes installed redundancy, spare inventory, repair probability, and substitution — not time to first failure; the naive form ignored inventories, cannibalisation, and stockpiling, all of which the model carries explicitly. Part I.7 enforces the condition by construction, and Part I.8 identifies the clock-setting sector by computation.

## I.5 Industrial closure: the decisive threshold

Self-sustaining (P ≥ D: replacing what is consumed and lost) and
self-expanding (P > D: net additional capacity) are different milestones.

$$
g_H = \frac{P-D}{H}
$$

P is productive capacity manufactured during the period, D is capacity lost
or consumed, and g_H is the net growth rate of productive infrastructure H.
Industrial closure measures how much of the critical input set is produced
inside the network:

$$
\kappa
= \frac{\text{critical inputs produced internally}}
       {\text{total critical inputs required}}
$$

At low closure, nearly all equipment arrives from Earth. At intermediate
closure, local industry supplies propellant, shielding, structural material,
tanks, roads, landing pads, and simple machines. At high closure, the network
also supplies motors, sensors, precision tools, computers, robots, spacecraft,
factory machinery, high-purity chemicals, and semiconductor equipment. The
progression is descriptive, not a scalar score: the identity and
replaceability of the residual imports determine whether the system is
actually autonomous.

The scalar form is vocabulary, not measure: a system supplying 99.9% of its
mass locally has effectively zero autonomous closure if the residual 0.1%
contains irreplaceable electronics. The proper object is a vector —
κ = (κ_power, κ_mining, κ_refining, κ_robotics, κ_machine-tools,
κ_electronics, κ_thermal, κ_transport) — with minimum cut sets: the
smallest combinations of imported inputs whose loss collapses the network.
The clock-setting component is the scalar shadow of this vector structure.
The hardest closure problem is the deep technological stack — precision
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
replication time of a full industrial ecosystem is *unknown* — and in this
edition it appears only as a computed output distribution (Part I.8). For κ, the honest headline is a theory-versus-demonstration gap, stated as its authors did: the 90–96% figure is closure reported in earlier studies of *specific nonreplicating* space-production applications, cited in support of plausibility arguments, and the 1980 study explicitly placed a rigorous demonstration that its factory could produce every required part beyond its own scope [S23]. Against that sit gram-per-hour oxygen and ~20% single-output yields actually demonstrated [S21]; full-system closure has not been demonstrated at any scale. Stating the gap converts the indicators
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
industrial memory. The inherited ten-sector model represents only part of
the physical layer: spares are a shelf-life-limited stockpile state;
nonlocal dependencies are import lines that can be cut; and the "explicit
path" is an abstract sector requirement matrix. The Fourth layer sizes
the seed and adds stylized representations of the remaining layers — a
fixed 5 t digital-seed mass, task-coverage autonomy, intervention
budgets, and commissioning dynamics (I.7, D.1). Those are declared
proxies, not resolved requirements: collapsing storage, compute,
calibration standards, laboratory machinery, consumables, and test
articles into one constant means the model cannot yet determine which
component of knowledge closure binds.

## I.6 Intelligence, coordination, and time

A sufficiently capable AI converts much of organizational coordination from
human management into a computational service: scheduling machines,
allocating energy, routing materials, diagnosing failures, redesigning
components, balancing inventories, planning construction, and selecting the
next bottleneck to expand.

    Coordination burden = f(number of agents, complexity, uncertainty,
                            intelligence)

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

$$
C_{\min}
= C_{\mathrm{sensing}}
+ C_{\mathrm{latency}}
+ C_{\mathrm{verification}}
+ C_{\mathrm{contention}}
$$

The strongest claim is therefore that coordination approaches a physical
information floor, not zero. Intelligence compresses planning and management
overhead until observation, propagation, actuation, and verification dominate.

After high closure the central allocation question changes from "can the
system obtain land, permits, workers, components?" to "how much productive
throughput should be assigned, and when will output be complete?"

$$
H_{\mathrm{created}}(t)
= \int_0^t \operatorname{throughput}(\tau)\,\mathrm d\tau
$$

Scarcity becomes latency: outputs remain scarce because machines, energy,
compute, transport capacity, and time have alternative uses, but the
accounting unit shifts toward joules, kilograms processed, machine-hours,
compute-hours, delta-v, and completion time. In the mature regime, growth is
bottleneck-limited:

$$
\frac{\mathrm d H}{\mathrm d t}
= \bigl(r(I,E,M)-\delta\bigr)H
$$

When r exceeds δ, the idealized solution is exponential growth; real
systems instead move through phases in which extraction, refining, power,
thermal control, transport, precision manufacturing, compute, or maintenance
is slowest. Intelligence accelerates growth by detecting and expanding that
active bottleneck. The model below is an **idealized, perfectly informed
coordination benchmark**, not a demonstration that an AI can observe,
verify, and execute the allocation across a distributed factory. Within
that benchmark, the co-binding set reported each step identifies the
modeled active bottleneck.

## I.7 The multisector model

The model that produces a real number needs, per critical sector, a capacity, a sector-specific depreciation, a requirement matrix, and import terms — with self-expansion defined as feasible positive net growth in *every* indispensable sector. Earlier editions specified it; this one builds and runs it [S28]. Its elements:

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
- **Vitamin-part stockpiles** with shelf life (electronics-class parts
  decay in storage), per-sector import cutoffs, Mars synodic pulse
  deliveries, and Poisson common-cause shocks hitting correlated sector
  groups (dust storms, solar storms, common design faults).
- **Three reference architectures**: LEO (no ore body — feed imported or
  recycled from on-orbit mass), lunar surface (regolith feed, abrasive
  dust, no magnetosphere), Mars (deepest logistics penalty, ~26-month
  synodic resupply pulses, dust storms).

**The vitamin gap.** One structural parameter dominates the scoped
scalar-anchor screen in I.8: the
fraction of the electronics sector's output mix producible off-world
(sampled 0.10–0.30; ASSUMPTION with a documented bounding argument —
advanced-node logic and memory are not locally closable in this scenario
class; boards, passives, and power electronics plausibly are). No published
measurement exists. Among the quantities currently parameterized,
anchoring it is the highest-value observation this program could acquire;
that ranking does not cover omitted structural uncertainties.

**Fourth Edition integrated-bootstrap layer.** The inherited model asks
whether ten abstract capacities can grow together. The new model asks
whether a declared physical seed can supply the material, service,
autonomy, and commissioning requirements of another operating cell. It
expands the graph to 18 sectors — separating interconnects/boards,
passives/power, sensors/control, packaging/test, mature logic, advanced
logic/memory, and process equipment/metrology — and 17 material
categories (15 elements plus rare-earth and dopant classes; the model is
material-category-resolved, not element-resolved — stoichiometric and
process-chemical closure is not checked at the species level). Its
material balance is

$$
\Delta M_e
= \sum_s Y_{s,e}X_s + I_e + \sum_a F^{\mathrm{in}}_{a,e}
- \sum_j B_{e,j}x_j - L_e - \sum_a F^{\mathrm{out}}_{a,e},
$$

with explicit Earth→Moon vitamin, asteroid→Moon feed, and Moon→orbit
finished-compute arcs. The seed optimizer includes task coverage and
residual intervention, construction lags, yield ramps, minimum viable
scale, and process-specific gravity or centrifuge overhead. A dynamic pass
then requires the constructed plant to ramp through commissioning before
it becomes an operating second cell. The equations, scenario definitions,
and reproducibility record are in Appendix D and
`outputs/fourth/MANIFEST.md`.

## I.8 Results

Monte Carlo over anchored ranges with common-cause shocks (n = 400 sampled
runs per cell; one shared draw per anchor per run, correlating parameter
uncertainty across sectors; every replication time is an output). r3.5
replaces the state metrics on external review; the definitions:

- **Balanced doubling (headline replication metric).** λ(t) =
  min_j K_j(t)/K_j(0); balanced doubling occurs when λ ≥ 2 — every modeled
  sector has at least doubled in its own capacity units. This is a
  balanced-capacity event, not a claim that a complete commissioned second
  plant or physical seed exists. λ is invariant to each sector's arbitrary
  capacity unit, which the previous metric was not.
- **Aggregate doubling (continuity only).** First passage of Σ_j K_j to
  2× its initial value. This depends on the arbitrary units the sectors
  are denominated in and can be reached by overbuilding easy sectors while
  a hard sector lags; r3.4's "doubling times" were all of this type and
  are relabeled, not silently redefined.
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
30 (durable replication performance). The visible table below displays the
ever-doubled denominator; survivor-conditioned counts and times remain in
the CSV. The difference is a distinct outcome class — runs that doubled
early and then lost viability. All shares are frequencies across this
stipulated assumption ensemble and shock process — not empirical
probabilities of real-world success (machine-readable table:
`outputs/tables/mc_deep.csv`):

> **Inherited-model boundary.** Every run starts with positive capacity in
> all ten sectors. This layer has no construction lag, commissioning, yield
> ramp, or minimum efficient plant scale, and it permits continuous
> fractional capacity. Its reported years are stylized first-passage times
> inside an already complete abstract seed, not engineering schedules for a
> transported factory. The separate Fourth layer below adds a physical seed
> and commissioning dynamics, but remains assumption-class.

All doubling columns below are **balanced capacity** events (λ ≥ 2: every
modeled sector doubled in its own units);
the aggregate-metric columns live in the CSV. LEO rows describe the
**import/capture-supported orbital recycling network** of I.6, not an
autonomous ecology. (Cell values differ from the prior revision's for two
declared, one-time reasons — a binding-definition change and a
draw-scheme re-key; each cell moved within its Wilson interval, and cells
whose leading binding sector or margin-conditional statistics flipped are
noted where quoted. Appendix B records the details.)

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

Earth-import cutoff (central set, all Earth imports cut at year 30; endpoint
= realized g > 0 at each step ending in the 30–35 window):

| env / qualification | positive realized growth at year 35 after Earth-import cutoff, stock draw permitted (share, 95% CI) | sustained positive realized growth throughout years 30–35 | pre-shock allocation endpoint |
|---|---|---|---|
| LEO — **Earth import cutoff with continued capture feed** | 210/400 (0.53, 0.48–0.57) | 88 | 224 |
| lunar | 170/400 (0.42, 0.38–0.47) | 23 | 187 |
| Mars | 53/400 (0.13, 0.10–0.17) | 2 | 64 |

Reading: the conservative ensemble mostly fails on the realized endpoint:
3% of LEO, 8% of lunar, and 0.5% (2/400) of Mars runs are expanding at
year 30.
Central results are architecture-dependent: the realized endpoint is 67%
in LEO, 56% on the Moon, and 15% on Mars, while only 31%, 5%, and 1% of
all runs, respectively, remain positive throughout years 25–30. The gap
between the pre-shock allocation endpoint and the realized endpoint is the
cost of shocks at the reported step. The Mars synodic pulse can still
flatter a single endpoint; λ = 0.55 and 4/400 sustained central runs show
that contraction is the more informative reading there.

![Survival curves, central assumption set: fraction of runs with positive
realized maximin growth over time, by architecture. Ensemble frequencies
under the stipulated assumption set, not empirical
probabilities.](../outputs/figures/survival_deep_central.png)

Balanced doubling is faster on the Moon but the endpoint is more durable
in LEO: among runs that ever reach λ ≥ 2, the central median is 5.0 years
on the Moon versus 26.0 in LEO. These are balanced-capacity first passages,
not construction records for complete second factories. LEO has no ore
body, so growth is throttled by captured and recovered material. Recycling
yield is below unity and recovery now depends on loss type; recycling alone
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
additionally indispensable on the lunar surface. **A recorded correction
(Appendix B): earlier revisions claimed recycling was
knockout-indispensable in LEO. That claim came from a stale output and
does not reproduce — with LEO's 5% capture feed, a recycling knockout is
survivable at central values.** What survives is the structural point:
the LEO architecture lives on recovered and captured mass (capture/mining
receives 98% of central co-binding credit), so its dependency is the feed loop as a whole
rather than any single import line.

**The clock-setting curve.** Expansion frequency against the e-folding
time of Earth-supply withdrawal (n = 60 per grid point; machine-readable:
`outputs/tables/import_decay_deep.csv`): on the lunar
surface under central assumptions, the realized year-30 endpoint is 0.40,
0.57, 0.43, 0.57, and 0.73 at 4-, 7-, 10-, 15-, and 25-year e-folding
times. The non-monotonic wobble is within binomial noise at this n. The
experiment is suggestive of a penalty for withdrawing the umbilical faster
than the closure ramp, with electronics stockpile shelf life as a plausible
mechanism. At $n=60$ per point it does not estimate a stable response
curve or its steepness.

![Expansion frequency at year 30 versus the e-folding time of
Earth-supply withdrawal, central set, n = 60 per grid point. The wobble is
within binomial noise at this n.](../outputs/figures/import_decay_sweep_deep.png)

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
the vitamin gap and logistics penalty dominate is a computation, not an
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

**Fourth Edition seed and reproduction results.** The new layer is a
second, explicitly assumption-class model, not a relabeling of the
inherited balanced-capacity runs. Structurally it is a two-stage hybrid:
a multisector, multi-material seed-sizing LP, followed by an aggregate
reproduction pass that advances a continuous count of operating
cell-equivalents through construction and commissioning lags — the
18-sector detail constrains seed sizing but does not persist into the
reproduction dynamics (sector-resolved reproduction is queued, ROADMAP).
A scenario is **model-feasible** when the seed LP admits a solution
satisfying every material, service, autonomy, intervention, and
throughput constraint over the scenario horizon. The reproduction metric
is **first passage to two operating-cell equivalents** — a continuous
aggregate crossing, not a discretely commissioned second factory — with
the year-40 column showing whether reproduction was durable. Central
deterministic scenarios and deterministic 200-draw assumption ensembles:

| bootstrap architecture | central minimum-mass installed seed | Earth vitamin stock (share of seed) | first passage to two cell-equivalents | cell-equivalents, year 40 | model-feasible draws | feasible-draw seed p10 / p50 / p90 |
|---|---:|---:|---:|---:|---:|---:|
| terrestrial closure rehearsal | 206.7 t | 48.1 t (23%) | 9.2 yr | 1.93 | 83/200 | 171 / 201 / 228 t |
| lunar vitamin bridge | 216.7 t | 58.1 t (27%) | 11.2 yr | 2.29 | 126/200 | 181 / 212 / 247 t |
| strict lunar-only | infeasible | — | — | — | 0/200 | — |
| Moon–asteroid network | 185.5 t | 0.0 t | 22.8 yr | 12.55 | 187/200 | 155 / 204 / 310 t |

"Minimum-mass installed seed" means minimum *installed operating* mass
inside the declared linear seed architecture: the LP sizes a seed that is
already unloaded, sited, powered, calibrated, and operating — delivery,
unpacking, site preparation, and first commissioning are outside the
model — and it is not a global optimum over unknown processes, designs,
or objectives (a mass-versus-reproduction-time frontier is queued,
ROADMAP). The vitamin share is worth stating plainly: at 27% of installed
mass, the central lunar bridge is a substantially Earth-provisioned seed
whose local loop supplies bulk mass, not a nearly closed system with
trace imports. The year-40 column carries the transient-versus-durable
distinction: the terrestrial rehearsal crosses two cell-equivalents at
9.2 years yet holds only 1.93 at year 40 — reproduction occurred once and
was not durably retained — the lunar bridge barely grows past its first
reproduction (2.29), and only the Moon–asteroid case compounds. The
vitamin stock's composition is resolved in
`outputs/fourth/tables/vitamin_composition.csv`: Ni, Cu, and C dominate
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
timetable, or economical. In its central solution the Moon supplies 366.2
t/yr of feed and the asteroid portfolio 173.8 t/yr. Source occurrence
[S51–S56] bounds plausibility; it does not validate recoverable yield,
reserve, throughput, purity, or transfer cost.

![Installed seed mass across the 200-draw assumption ensembles, by
scenario. Distributions describe the declared parameter box, not
engineering uncertainty.](../outputs/fourth/figures/seed_mass_ensemble.png)

![Operating cell-equivalents over time in the central scenarios:
construction and commissioning lags separate ordering from operating
capacity.](../outputs/fourth/figures/cell_reproduction.png)

**Durability, ablation, and frontier diagnostics (r4.1).** Five analysis
passes interrogate the same declared architecture without introducing any
new coefficient (machine-readable tables in `outputs/fourth/tables/`;
all regenerate with `scripts/run_fourth.py`):

- **Reproduction is mostly transient.** Retention and durability split
  the ensembles sharply: the lunar bridge retains ≥ 2 cell-equivalents
  in all 126 feasible draws yet has *negative* net reproduction over
  years 35–40 in every one of them (central −0.036); the terrestrial
  rehearsal retains in 11 of 83 with none durable; only the
  Moon–asteroid network expands durably (187/187, central +5.17). First
  passage to two cell-equivalents is a reproduction event, not a growth
  regime.
- **The dynamic intelligence coupling is inert at central
  coefficients.** Zero/freeze ablations of the declared coupling — no
  intelligence growth, either channel alone, fully uncoupled —
  reproduce every central trajectory exactly, because realized cell
  orders are capped by material availability below desired orders at
  all 160 steps of all three feasible scenarios. The declared AI level
  is load-bearing *statically* instead: re-sizing the seed at base
  autonomy (AI level 1.0) leaves the terrestrial rehearsal unchanged
  and makes the lunar-bridge and Moon–asteroid scenarios infeasible on
  the autonomy threshold. The headline growth is a material-throughput
  result, not an artifact of the assumed AI feedback — and,
  symmetrically, these trajectories cannot test the coupling's dynamic
  coefficients.
- **Minimum mass is not time-optimal.** Installing f cell-equivalents
  of the minimum-mass design (a sweep axis, not a new assumption) buys
  reproduction time: doubling the lunar-bridge seed (428.5 t) cuts
  first reproduction from 11.25 to 8.0 years, with diminishing returns
  along the axis. Mass-optimal and time-optimal seeds are different
  designs; the declared LP answers only the first question.
- **Failure reasons and binding constraints are per-draw.** Infeasible
  draws split between the autonomy threshold and the material LP
  (terrestrial 77/40, bridge 54/20, strict 33/167); feasible draws bind
  most often on Cu, C, Ni, and Cr (terrestrial and bridge) and on
  dopants plus refining and asteroid-transport throughput (network).
  One sensitivity is a sizing artifact worth naming: the depreciation
  multiplier correlates *positively* (ρ ≈ +0.8 to +0.98) with year-40
  cell-equivalents, because pessimistic depreciation forces the
  minimum-mass LP to oversize service and feed capacity per cell — the
  frontier effect arrived at inadvertently.
- **The strict-lunar cut is quantified.** An elastic relaxation of the
  exact seed LP names the unsatisfiable rows and their minimum
  shortfalls over the horizon: Ni 19.0 t, Cu 18.4 t, C 15.3 t, Co
  3.6 t, Cr 3.1 t, rare earths 2.3 t, Li 2.3 t, H 0.2 t, and dopants
  0.1 t. The infeasibility is a distributed material cut, and the table
  doubles as the engineering target list any lunar-only architecture
  claim would have to defeat.

![Oversize frontier: installed seed mass versus years to one additional
operating cell-equivalent, central
scenarios.](../outputs/fourth/figures/oversize_frontier.png)

The coupled run distinguishes installed compute from the industrial stock
that manufactures it. At year 40, the Moon–asteroid scenario has 12.55
normalized total endogenous compute capacity — numerically identical to
its cell-equivalent count by construction, since endogenous compute is
proportional to operating cells and normalized to the one-cell start —
and exports 1.63 units to orbit. Constant-rate Earth-fed orbital deployment reaches 1.56, 2.81, or
4.99 units under the tight, base, and responsive rate cases. Those curves
show the difference between rate-limited deployment and endogenous
reproduction under the configured coefficients; they do not forecast
datacenter capacity.

![Rate-limited Earth-fed deployment versus endogenous reproduction,
normalized compute capacity under the configured
coefficients.](../outputs/fourth/figures/compute_growth_regimes.png)

The stateful debris stress test reports the **five-year fragment
creation-to-clearance ratio** $R_{\mathrm{debris}}$ — fragments created
divided by fragments cleared over the final five years, a flow ratio
rather than a branching-process reproduction number:

| deployment topology / mitigation | creation-to-clearance ratio, last 5 yr | fragment index, year 40 |
|---|---:|---:|
| Earth-fed orbit / weak | 0.61 | 1.602 |
| Earth-fed orbit / strong | 0.35 | 0.284 |
| dense endogenous / weak | 5.53 | 16.497 |
| dense endogenous / strong | 5.58 | 12.632 |
| distributed endogenous / sparse topology | 1.00 | 0.000 |

A ratio above one means only that more fragments were created than
cleared in the window; it is not a monotonic safety indicator. Strong
mitigation lowers the dense case's fragment stock (16.5 → 12.6) while the
flow ratio stays essentially unchanged, because clearance scales with the
shrinking fragment population. The sparse case reads exactly 1.00 with an
empty stock because realized clearance is capped by the fragments
available — a zero-stock boundary, not a computed equilibrium — and it
reaches that boundary only under an assumed 0.01 collision-kernel
multiplier. The result supports topology as a co-designed industrial
constraint; it does not establish a safe orbit, validate a debris
environment model, or locate a cascade threshold. Complete tables and
figures are generated from the same run in `outputs/fourth/`.

![Fragment-index trajectories by deployment topology and mitigation: the
debris stress test that produces the creation-to-clearance table
above.](../outputs/fourth/figures/debris_regimes.png)

**What Part I establishes and does not.** It establishes structure: which
sector binds, what the minimum cut is, how locations differ qualitatively
(lunar fastest-doubling but hostage to the electronics cut; LEO
feed-constrained but recycling-viable; Mars most path-dependent and
import-fragile — r3.5 drops the earlier "most robust per unit of
assumption-optimism" ranking, which had no defined normalization), and where
the feasibility margin lies — structure that survives the allocation-policy
variation above. The Fourth layer additionally establishes which declared
material, autonomy, gravity, source, and commissioning constraints explain
its own seed scenarios. Neither establishes point feasibility: both
requirement matrices, element recipes and yields, vitamin gap, repair
efficiencies, stockpiles, autonomy coefficients, lags, source portfolio,
and shock/debris rates are ASSUMPTION-class. Solar-array, regolith, sample,
or satellite data do not establish the coupled behavior of mines, bearings,
machine tools, electronics production, or dust-exposed radiators.

## I.9 Development path, annotated

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
   dependency.
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

    I increases → replication efficiency increases → infrastructure
    increases → compute increases → I increases

The bridge economy maps onto the ladder: terrestrial products carry the
early stages; launch and connectivity carry Stages 2–4; orbital compute is a
candidate Stage 4–5 tread; and in-space industrial services carry Stages
5–6. The model adds stage warnings. The Stage 4→5 transition is where the
vitamin gap binds — no amount of Stage 3 bulk closure substitutes for an
electronics tier. Stage 5 is location-dependent: LEO requires a sustained
capture-and-recovery feed loop; under the present 5% capture assumption,
recycling is valuable but not knockout-indispensable at central values.
Mars requires electronics stockpiles engineered to synodic shelf life or a
local electronics tier. The lunar surface has the fastest conditional
balanced-doubling pathway when electronics closes sufficiently; LEO has the
more durable central endpoint under its continuing-capture assumption.

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
estimate [S54, S55]. A robot-only ecology avoids agricultural and
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
bulk matter and shielding. The inherited ten-sector and Part II models
cannot compare that hybrid directly: they isolate lunar-surface capacity,
cislunar compute, and Earth-supplied lunar compute, and they aggregate
elements into industries. The Fourth layer adds material-category bills
of material, source yields, Earth–Moon–orbit–asteroid arcs, and aggregate
endogenous debris states. It therefore computes an explicit hybrid scenario, but its
recipes, yields, transfer capacities, composite asteroid source, and
collision kernels are declared assumptions. It does not establish lunar
material sufficiency, a recoverable reserve, a launch date for asteroid
supply, or an orbital safety case.

## I.10 Binding bottlenecks and failure modes

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

---

# Part II — Comparative Economics

## II.1 The bridge economy

Each stage of the recursion must be independently profitable or deliberately
financed: a staircase of self-supporting steps, not a single leap to
closure. The plausible treads, in order: terrestrial products of the same
machinery (vehicles, storage, robots — the ground floor pays rent **and**
turns the autonomous seed into an audited industrial experiment); launch
and connectivity (Starlink revenue and launch services fund transport);
orbital compute services — a candidate tread, *now priced rather than
merely doubted* (II.2–II.4); and in-space industrial services at higher
closure. The test of the staircase: at every stage, revenue plus strategic
financing must exceed the burn required to reach the next stage before the
clock-setting components of Part I.4 expire — and Part I.8 makes the clock
concrete: the electronics stockpile shelf life against the import ramp.

Stage 0 has a second economic role. Building the candidate lunar industries
first on Earth captures process knowledge, failure data, tool interfaces,
simulation residuals, and commissioning procedures while the repair economy
is still accessible. Selling terrestrial output can finance that learning,
but the decisive deliverable is the measured ability to build and
commission a second cell under lunar-palette and no-routine-entry
constraints. A factory that is profitable yet requires tacit human rescue
has not validated the exported loop.

## II.2 The crossover model

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

For WACC $r$, useful life $T$, and annual operations fraction $f_o$,

$$
\operatorname{CRF}(r,T)=\frac{r}{1-(1+r)^{-T}},
\qquad
a(T)=\operatorname{CRF}(r,T)+f_o.
$$

Let $C_h$ be qualified accelerator capex, $C_I$ the sum of PV,
radiator, and storage capex, $M_h$ accelerator mass, $M_I$ launched
non-hardware mass after local closure, $\mu$ the destination launch
multiplier, $p_L$ the LEO launch price, and $U_s$ delivered
utilization. The complete space expression is

$$
L_s =
\frac{C_h a(T_h)+C_I a(T_I)
+p_L\mu[M_h a(T_h)+M_I a(T_I)]}{U_s}
=\alpha+\beta p_L.
$$

The integrated-disposable case sets $T_I=T_h$. The
serviceable/reusable-platform case sets
$T_I=\max(T_{I,\mathrm{anchor}},T_h)$. For Earth scenario $e$, PUE
$\psi_e$, electricity price $p_e$, data-center shell capex $C_{DC}$,
utilization $U_E$, and frontier-equivalent node penalty $\phi_e$,

$$
L_E =
\frac{\phi_e\left[
C_{h,e}\operatorname{CRF}(r,T_{h,e})
+C_{DC}\operatorname{CRF}(r,15)
+8760p_e\psi_e\right]}{U_E}.
$$

The responsive Earth case evaluates frontier and older-node hardware and
selects the lower $L_E$. Because $L_s$ is affine in launch price, the
exact break-even is

$$
p_L^*=\frac{L_E-\alpha}{\beta};
$$

a negative value means non-launch costs alone exceed the Earth
counterfactual.

For the central LEO serviceable-platform case,
$C_h=\$63{,}640/\mathrm{kW}$, $C_I=\$1{,}697/\mathrm{kW}$,
$M_h=17.3$ and $M_I=28.8\ \mathrm{kg/kW}$,
$p_L=\$2{,}366/\mathrm{kg}$, $a_h=0.3237$, $a_I=0.1704$, and
$U_s=0.786$. Substitution gives

$$
L_s =
\frac{63{,}640(0.3237)+1{,}697(0.1704)
+2{,}366[17.3(0.3237)+28.8(0.1704)]}{0.786}
=\$58{,}264/\mathrm{kW\!-\!yr}.
$$

A fourth, explicitly conditional **Starmind AI1 disclosure scenario** does
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
than a new baseline: **Starmind AI1 aspirational best case**. It uses
SpaceX's formal ≥99% launch-cost-reduction target as **$185/kg** and the
prospectus's long-term **100 kW/t** orbital-compute scaling assumption
(10 kg per average kW) [S37]. Because the company does not publish achieved
AI1 qualification cost, useful life, or compute availability, the case
separately labels as `ASSUMPTION` the favorable existing model bounds:
1.2× qualification, seven-year hardware life, and 0.95 utilization. It is
excluded from Monte Carlo. Treating a target and three selected favorable
bounds as probability distributions would manufacture a spurious
probability of success.

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
average compute is 0.92 m²/kW of quoted area [S38]. If 110 m² is physical
footprint and both faces emit, the mean flux is about 545 W/m²; a simple
Stefan–Boltzmann balance using NASA's emissivity and environmental
temperature gives an ideal radiator surface near 332 K (59 °C). If 110 m²
instead denotes total emitting area, the load is about 1,090 W/m² and the
ideal surface approaches 391 K (118 °C). Both calculations omit solar and
Earth view, degradation, nonuniformity, pumping power, and the
chip-to-coolant-to-radiator temperature drop. The disclosure is therefore
not thermodynamically impossible, but its area convention, coolant
temperature, and full thermal-system mass are crossover-critical
measurements.

The terrestrial counterfactual **responds** — the epistemic requirement
earlier editions missed. Three scenarios: *tight* prices scarcity (the
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
implies **$185/kg**; "or more" implies a lower value. The table converts
that formal aspiration and three more aggressive sensitivity cases into
full-payload flight-cost equivalents:

| LEO sensitivity case | $/kg | V3: 100 t full-load equivalent | V4: 200 t full-load equivalent | status |
|---|---:|---:|---:|---|
| formal corporate aspiration | ≤$185 | ≤$18.5M | ≤$37M | derived from the stated ≥99% reduction; not a price quote |
| aggressive mature-Starship case | $100 | $10M | $20M | scenario axis |
| extreme fuel-like case | $50 | $5M | $10M | scenario axis |
| extreme lower case | $30 | $3M | $6M | scenario axis |

The dollar-per-flight columns are arithmetic (`$/kg × full payload`), not
company forecasts. They rise for V4 in the table because $/kg is being held
constant while payload doubles. Holding flight cost constant gives the
other useful comparison: a $10M flight is $100/kg on a full V3 and $50/kg
on a full V4. Under-filled flights cost more per delivered kilogram;
external customer prices can exceed internal marginal cost; and none of
these figures includes a demonstrated cadence, reuse count, refurbishment
burden, or capital-recovery schedule. This edition therefore uses
**$185/kg as the traceable corporate aspiration, $100/kg as an aggressive
case, and $30–50/kg only as an extreme fuel-like sensitivity band**. All
remain comparison axes; $185/kg also enters the quarantined deterministic
best case, never the Monte Carlo.

Two financing caveats are deliberate modeling choices,
stated openly: a single WACC range (8–15%) applies to *both* sides —
equalized financing is an assumption in favor of space, since an
unprecedented orbital constellation would not price like a mature
terrestrial data center — and the qualification multiplier, service life,
and utilization are sampled independently, although the favorable corner
(cheap qualification, long life, high utilization) likely involves
correlated engineering assumptions; both refinements are queued (ROADMAP).
Calibration: the Earth base case works out to ≈$1.7/kWh, matching
published accelerator rental rates.

**Cost accounting — included and excluded.** Included: IT hardware with
qualification premium; PV, radiators, storage, structure and their launched
mass (with cislunar/lunar delivery multipliers), while structure itself is
only a mass proxy and has no separate construction price; capital recovery
at WACC with component-specific lives — compute hardware and its replacement
launch mass on the refresh cycle, infrastructure and its launch spend on a
separate 10–25-year ASSUMPTION-class range (r3.5); an operations fraction
(2–6% of capex/yr) standing in for ground segment, downlink, and
station-keeping in the serviceable-platform case, or all of those assets on
the compute life in the integrated-disposable case; utilization derating;
Earth-side DC capex, PUE, and
firm-power floors. Excluded: spacecraft-bus, structure, harness, avionics,
integration, and qualification manufacturing cost beyond the component
prices above; complete thermal transport beyond the radiator coefficient;
communications-terminal and ground-network capex; development and
non-recurring engineering; launch-site, landing, turnaround, and fleet
infrastructure beyond whatever is implicit in the $/kg target; launch
failure and insurance; redundant
provisioning beyond the life derating; collision-avoidance operations beyond
the ops fraction; spectrum and regulatory costs; deorbit/disposal; residual
value; and tax treatment. Turyshev's independent inequality is consequently
a stricter comparison than the current launch-only coefficient: at
40 kg/kW, a terrestrial infrastructure allowance of $10,000–40,000/kW
permits only **$250–1,000/kg for launch and spacecraft build combined**
before communications, operations, utilization, and finite-life penalties
[S39].
The net direction of the exclusions is **not** claimed to be uniformly
conservative in space's favor (an r3.4 overstatement corrected on external
review): most excluded items burden space more, but residual value and
reuse of the power/thermal platform across accelerator generations would
favor space, and the zero-closure lunar labeling and equalized financing
are themselves pro-space simplifications. The reported multiples are
therefore stylized-architecture outputs; the robust conclusion is
structural — *which* terms dominate — not the exact ratios.

## II.3 Results

Central reference values plus the deterministic aspiration case ($ per
kW-yr, rounded to three significant figures — these are
assumption-conditioned outputs, not measurements; exact machine-readable
values regenerate in `outputs/`):

| case | architecture | LCO | launched mass | vs Earth base (≈14,700) |
|---|---|---:|---:|---:|
| LEO inference | serviceable/reusable platform | 58,264 | 46 kg/kW | 3.97× |
| LEO inference | integrated disposable satellite | 71,901 | 46 kg/kW | 4.90× |
| cislunar batch | serviceable/reusable platform | 96,726 | 46 kg/kW | 6.59× |
| cislunar batch | integrated disposable satellite | 128,333 | 46 kg/kW | 8.75× |
| lunar surface (Earth-supplied) | serviceable/reusable platform | 2,773,476 | 454 kg/kW | 189× |
| lunar surface (Earth-supplied) | integrated disposable satellite | 5,065,254 | 454 kg/kW | 345× |
| Starmind AI1 disclosure scenario | serviceable/reusable platform | 37,483 | 16 kg/kW | 2.56× |
| Starmind AI1 disclosure scenario | integrated disposable satellite | 42,531 | 16 kg/kW | 2.90× |
| Starmind AI1 aspirational best case | serviceable/reusable platform | 11,156 | 10 kg/kW | 0.76× |
| Earth tight | — | 15,980 | — | — |
| Earth responsive | — | 12,783 | — | — |

(The integrated-disposable rows annualize *all* space capex — PV,
radiators, storage, structure, and the launch spend that emplaced them —
on the short compute-refresh life; the serviceable-platform rows amortize
infrastructure on a separate `infrastructure_life_years` range (10–25 yr,
ASSUMPTION-class with a stated bounding argument), with replacement chips
and their launch mass still recurring on the compute life. Earlier
revisions reported only the disposable reading; Appendix B records the
change. The lunar case is labeled **Earth-supplied** because its central
closure fraction is zero — local manufacture enters only through the
closure sweep axis.)

Monte Carlo over anchored ranges, shared draws both sides (n = 2,000
sampled runs per row; frequencies under this ensemble, not empirical
probabilities). The aspirational best case is excluded because its company
targets and favorable unpublished assumptions are point sensitivities, not
probability distributions:

| case | architecture | vs Earth | ratio p10/p50/p90 | space-cheaper runs | break-even $/kg p50 (p90) |
|---|---|---|---|---|---|
| LEO inference | serviceable/reusable | base | 2.7 / 4.2 / 6.4 | 0 / 2,000 | −844 (−132) |
| LEO inference | serviceable/reusable | responsive | 3.3 / 5.1 / 8.2 | 0 / 2,000 | −1,035 (−339) |
| LEO inference | integrated disposable | base | 3.3 / 5.1 / 8.2 | 0 / 2,000 | −606 (−124) |
| LEO inference | integrated disposable | responsive | 3.9 / 6.3 / 10.4 | 0 / 2,000 | −764 (−239) |
| cislunar batch | serviceable/reusable | base | 4.2 / 6.8 / 11.7 | 0 / 2,000 | −211 (17) |
| cislunar batch | serviceable/reusable | responsive | 5.1 / 8.6 / 14.5 | 0 / 2,000 | −299 (−49) |
| cislunar batch | integrated disposable | base | 5.3 / 9.1 / 15.8 | 0 / 2,000 | −158 (12) |
| cislunar batch | integrated disposable | responsive | 6.4 / 11.5 / 19.8 | 0 / 2,000 | −216 (−41) |
| lunar surface (Earth-supplied) | serviceable/reusable | base | 78.5 / 189.6 / 448.8 | 0 / 2,000 | −19 (−7) |
| lunar surface (Earth-supplied) | serviceable/reusable | responsive | 98.3 / 240.8 / 570.9 | 0 / 2,000 | −21 (−8) |
| lunar surface (Earth-supplied) | integrated disposable | base | 144.4 / 354.2 / 887.2 | 0 / 2,000 | −12 (−5) |
| lunar surface (Earth-supplied) | integrated disposable | responsive | 186.5 / 448.2 / 1,055.0 | 0 / 2,000 | −13 (−6) |
| Starmind AI1 disclosure | serviceable/reusable | base | 1.8 / 2.6 / 3.9 | 0 / 2,000 | −2,555 (−524) |
| Starmind AI1 disclosure | serviceable/reusable | responsive | 2.1 / 3.3 / 5.0 | 0 / 2,000 | −3,215 (−1,040) |
| Starmind AI1 disclosure | integrated disposable | base | 2.0 / 2.9 / 4.4 | 0 / 2,000 | −1,771 (−402) |
| Starmind AI1 disclosure | integrated disposable | responsive | 2.4 / 3.7 / 6.0 | 0 / 2,000 | −2,345 (−839) |

(Earth and space see the same sampled WACC and hardware cost in every
draw — each anchor's draw is cached per iteration — and the script's
seeds are stable, so the tables are deterministic across processes.
Earlier revisions implemented neither property; Appendix B records the
fix.)

All sixteen architecture/reference rows have zero observed successes in
2,000 draws, bounding each ensemble frequency below approximately 0.15%
(95%). These are statements about this assumption ensemble, not empirical
probabilities.

![Distribution of the space/Earth cost ratio over the anchored Monte
Carlo, shared draws both sides. No draw crosses parity in any
architecture/reference cell.](../outputs/figures/lco_ratio_mc.png)

AI1's aggregate mass disclosure is material but not sufficient at the
retained central values: it cuts launched mass from about 46 to 16 kg/kW
and LCO from about $58,300 to $37,500/kW-yr, yet fixed non-launch costs
still exceed Earth base (central break-even −$2,598/kg). With the remaining
anchors simultaneously favorable — qualification ×1.2, seven-year life,
and 0.95 utilization — AI1 is 1.28× Earth at the central published launch
anchor, breaks even at about **$1,152/kg**, and reaches 0.79× at $250/kg.
That moves the favorable-corner crossover close to the bottom of today's
published band, but only conditionally on performance values the AI1 page
does not publish.

The aspirational case makes that conditionality explicit. The two company
numbers alone—$185/kg and 100 kW/t—still produce about **$27,100/kW-yr,
1.85× Earth base** when qualification, life, and utilization remain at
their central values. Selecting the three favorable non-company bounds as
well produces about **$11,200/kW-yr, 0.76× Earth base**. This is the first
modeled orbital-AI case cheaper than central Earth, but it is a boundary,
not a forecast: all five favorable conditions must hold together, and the
model assigns no probability to them.

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
utilization, neither published for AI1. Spectrum and regulatory approvals,
collision avoidance and debris, replenishment, networking, insurance,
program NRE, and landing/turnaround infrastructure remain excluded, while
terrestrial energy, chips, cooling, permitting, and construction can also
improve. The prospectus itself identifies approvals and spectrum as
dependencies and warns that better terrestrial energy could reduce the
orbital advantage [S37].

The post-IPO review sharpens the lifetime interpretation. The model's
10–25-year infrastructure life is defensible only if the power and thermal
platform survives multiple accelerator generations and the compute payload
can actually be exchanged, serviced, or economically separated. For an
integrated, non-serviceable LEO vehicle, the relevant infrastructure life is
instead close to the spacecraft or compute life—typically about five years
in the studies reviewed here [S39–S42]. The serviceable-platform and
integrated-disposable results above now expose both lifecycle readings.
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
architecture's approximately 46 kg/kW, those prices correspond to initial
launch expenditures of about **$8,510, $4,600, $2,300, and $1,380 per
installed IT kW**, respectively, before annualization. They largely remove
the current launch bill, but a negative break-even still means they cannot
overcome the fixed qualification/life/utilization gap on their own. Lunar
closure is the weakest
lever: chips are never closed, so even 95% closure of non-chip mass leaves
the lunar case roughly 15–30× Earth at published prices — still more than
an order of magnitude from parity.

![The generic-LEO crossover surface: space/Earth cost ratio against
launch price with each companion axis varied over its anchored range. No
single-axis path reaches parity at published prices.](../outputs/figures/crossover_surface.png)

The mass-multiplier refinement: at anchored values a 2× FLOPS/W advantage
buys only ~39% of the benefit of halving launch price (ratio 4.0 vs
3.2 at $3,000/kg, both from 4.5), because the hardware term — untouched by
efficiency — dominates both mass and capex. "The compute tax outweighs the
launch tax" [S34] becomes true only after the qualification premium and
hardware $/kW fall; near-term, both taxes are subordinate to qualification
and life.

## II.4 External claim and independent-study checks

The two public crossover claims are recorded as comparison targets (never
inputs), and both *reproduce inside the model* under identifiable conditions
— which converts a public disagreement into a localized, testable one. The
post-IPO review of independent studies below then checks the model rather
than merely restating corporate claims. One preliminary correction of the record,
because this document earlier mis-stated it: the Suncatcher design study
does **not** claim system-level parity. Its cost section states twice that it
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
  At $250/kg with central anchors: space/Earth = 2.04 — no crossover.
  Under the favorable corner *within anchored ranges* (qualification ×1.2,
  7-year life, 0.95 utilization, 3 kg/kW radiators): **0.88** — the claim
  reproduced. The dispute is three numbers, none of them launch price.
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
That conclusion now has a workload boundary: it applies directly to
per-node inference in the cost model, while the new network evidence makes
frontier distributed training less favorable than the scalar model shows.
It does not price differentiated orbital products (in-orbit sensor
processing, sovereign or military demand, resilience niches), which could
be profitable while losing the commodity comparison. What follows for the
staircase is correspondingly bounded: *commodity-scale* deployment ahead of
the enabling corner is strategic positioning or learning investment rather
than substitute-compute profit — an observation Part III converts into a
discriminating test.

## II.5 Competition and the takeoff-speed assumption

**Explicit assumption.** This thesis is decision-relevant chiefly under a
slow-to-medium AI takeoff. Under a fast software takeoff, incumbent compute
and algorithms decide outcomes before any physical loop closes; the space
complex becomes something the resulting intelligence builds afterward, not
the path by which it arises. The prominent published bet on the fast branch
[S35] argues automated AI research compresses AGI-to-superintelligence into
roughly a year; this document's program is the other branch, and the
disagreement operates on priors, not on any evidence item below.

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

**The capital wall.** Expansion purchased through markets pays stacked
scarcity rents; when demand outruns supply, prices are set by scarcity.
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
envelope — the capital wall yields to expected returns; what does not
yield is the dependency structure of Part I.8.

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
parameter in this edition's model, not a mood. And the sequence remains
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

---

# Part III — Strategy Interpretation and Governance

## III.1 A Musk-associated technology stack

The following mapping is an analytical interpretation of how existing
companies could supply layers of the proposed system — not proof that they
are managed as one program, although the 2026 developments (the Terafab
initiative; SpaceX's absorption of xAI) bind the transport, communications,
intelligence, and fabrication layers by overlapping control, strategic
coordination, and contractual collaboration. Tesla remains a separate
public company; a shared controlling figure and a framework agreement are
not common ownership [S27].

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

The theoretical advantage is not ownership of complementary companies but
a shorter verified end-to-end loop across design → manufacture → deploy →
learn. The closure race rewards the shortest such loop, not the largest
stock of any single input.

    xAI improves intelligence → AI improves robots and factories →
    factories expand energy and hardware → Terafab expands chips →
    hardware expands compute on Earth and in orbit → compute improves AI

The advantage, if it exists, is the ability to integrate feedback, capital
allocation, engineering, deployment environments, and industrial production
into that shorter loop. Reported preparations for a SpaceX public offering
would, if completed, add a financing event for the capital-intensive middle
of the loop [S9, S27]; financing capacity is an enabler, not evidence of
closure intent.

## III.2 Terafab and the fabrication frontier

**What was announced**: a Tesla–SpaceX–xAI chip fabrication initiative
(March 2026), joined by Intel in April; declared scope from chip design
through lithography operation, fabrication, memory, packaging, and test;
reported $20B initial plant with a filing-based ceiling near $119B; 2-nm
target; mass production stated for 2028 [S6–S10]. **What the primary
source says** [S27]: a general framework with Tesla — timelines,
milestones, and capital expenditures not yet determined; no binding
obligations; a stated orbital data-center plan from as early as 2028; an
acknowledged present shortfall in chip supply for orbital AI. **First-party
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

The competence question needs stating precisely, since earlier drafts got
it wrong: Tesla, SpaceX, and xAI have no advanced-fab operating record,
but **Intel plainly does**, and the reported process plan is Intel 14A —
so the open question is whether that experience transfers into this
organizational structure and what obligations Intel has actually
accepted, not whether anyone involved has run a fab.

Two further corrections. The sites are distinct: a smaller Tesla research
fab at the Giga Texas campus, and a proposed SpaceX-led scaled facility
in Grimes County whose county tax and economic-development agreements are
now recorded as fully executed — strengthening site-level commitment
without constituting a definitive construction, funding, or operating
agreement [S6–S10]. And scale comparisons used in earlier drafts are
withdrawn: wafer-start counts cannot be set against a foundry's global
output without controlling for wafer diameter, node, product mix, yield,
and effective die output, and "one terawatt per year" is a claimed annual
production rate of hardware whose aggregate nameplate power draw would
total a terawatt — a manufacturing-throughput figure not commensurable
with national electricity consumption.

**The lithography question**: for terrestrial operation, purchased
lithography is an acceptable permanent dependency; for high space closure
it must eventually be reproduced, substituted (older nodes at volume;
nanoimprint; e-beam), or accepted as designed permanent import — the
deepest single closure problem in this framework (and precisely where the
Part I vitamin gap lives). This edition adds the bottleneck convergence:
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

## III.3 Competing hypotheses: the evidence table

The hypotheses are nested rather than exclusive, since a long-run off-world
strategy can be *pursued through* vertical integration and supply hedging —
those are mechanisms, not alternatives. **H0**: no *integrated* off-world strategy — individual terrestrial or
orbital projects arise from ordinary standalone commercial, supply-chain,
or research motives (with **H0′**, partly related businesses under
overlapping control, as its weakest variant). Standalone orbital-compute
ventures are H0-compatible under this definition; what H0 does not predict
is cross-layer integration toward off-world industry.
**H1**: deliberate integrated space–AI–industrial development — the P4a
claim. **H2**: H1 plus an intended transition to recursive industrial
closure — the P4b claim. Because the hypotheses nest, each evidence item is
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
| E2 | Mars-city rhetoric | documented / company_statement | weak | neutral | long predates the thesis; expected as branding under H0′ |
| E3 | Battery/vehicle/robot vertical integration | documented | neutral | neutral | canonical H0 |
| E4 | Humanoid robot program, scale targets | announced / company_statement | neutral | neutral | targets are intent, not capacity |
| E5 | Starlink constellation ops competence | documented | neutral | neutral | profitable on its own terms |
| E6 | Initiative list in SEC-filed offering materials associated with the S-1 (Rule 433 FWP and incorporated materials): orbital compute, lunar manufacturing and energy, in-orbit and Moon/Mars manufacturing, asteroid mining, "interplanetary industrialization" | documented / SEC-filed offering materials [S27] | **strong** | neutral | the P4a backbone: filed offering materials enumerating off-world industrial markets are hard to explain under H0 — repeatedly self-described as early, aspirational, and possibly unsuccessful, and saying nothing about closure |
| E7 | Terafab initiative; Intel joining; executed county agreements | announced→partly advanced / company_statement | weak | neutral | chip-supply hedging (inside H0) predicts a domestic fab about as well |
| E8 | SpaceX absorption of xAI | documented | weak | neutral | consolidation under overlapping control is expected under H0′; integration of the intelligence layer is also H1 |
| E9 | Rad-tolerant orbital silicon as a named fab line | announced / company_statement | moderate | neutral | H1 predicts it distinctly; a D3-supply commercial reading covers it too |
| E10 | No closure metrics, no seed BOM, no closure program | absent | neutral | **moderate against H2** | a deliberate closure strategy mildly predicts visible closure engineering by now; observability caveat applies |
| E11 | No export-scoped internal model variant, and no reported compliance apparatus for controlled-data training | absent | neutral | weak against H2 | the observable is the compliance architecture, not the model, which may be deliberately unpublicized |
| E13 | FCC **acceptance for filing** of an application for an orbital-data-center system of up to ~1M satellites [S50] | documented application; pending regulatory review — not an authorization | weak | neutral | filing a large option is far cheaper than receiving permission to deploy it |
| E14 | First-party Terafab messaging: Kardashev framing, ~10 Mt/yr to orbit, lunar mass drivers, orbital-vs-terrestrial cost decomposition | documented / company_statement [S29] | **strong** (declared intent only) | weak | supply-security strategy does not publish Kardashev framing or mass drivers; but messaging is cheap and the binding filings commit to none of it |

E12 and E15 (the Google/Planet Suncatcher prototype program and the design
study's content) are removed from this table in r3.4: they are actions of
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
demonstration phase is what H0 and H0′ predict. On-orbit
*materials-recovery* recycling at scale (not debris-compliance servicing)
would be *moderate-to-strong for H2 specifically*: Part I's structural
result that the LEO architecture lives on its recovered-mass feed loop
(capture/mining receives ~98% of central co-binding credit; r3.5 withdraws the stronger
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
**substantially establishes H1 at the level of declared direction and
early implementation** — the initiative list in the SEC-filed offering
materials (E6) and the first-party messaging (E14) are difficult to explain
under a purely terrestrial reading, and E7/E9/E13 are consistent
implementation steps (E12 no longer appears in the table — it was moved to
the external cross-checks in r3.4 as an independent actor's program). It **does not establish H2**: no item in the table is more than
weakly diagnostic for closure intent, the closure-specific observables
(seed bills of materials, reproduction metrics, minimum-cut roadmaps,
locally reproducible production equipment) remain absent (E10), and most
observed actions are equally expected under a conventional integrated
off-world commercial strategy. P4a is documented; P4b remains inferential
— which is exactly the split the propositions ladder now encodes.

## III.4 Control and governance of a self-expanding system

A self-expanding autonomous industrial network is, formally, a governed
macroscale von Neumann replicator; the property that makes it valuable —
compounding physical replication — makes its failure modes compound too.
Verification must scale with expansion (V is a safety term); throttle
authority must be explicit (rate limits, hardware-level authorization of
replication steps, clarity about who holds them); the legal frame is
unsettled and first movers set precedent.

The framework resolves its own tension — celebrating escape from
society-priced costs while requiring retained constraint — through the
gateway: in space, permission attaches to launches and spectrum, which is
where governance holds enforceable leverage. The leverage variable is dependency — but not proportional to (1 − κ), since this document has already established that scalar closure is invalid and a single low-mass import can be a minimum cut conferring disproportionate leverage. The governing quantity is G_dependency = f(criticality, substitutability, stockpile, supplier concentration, enforceability): what matters is whether withholding an input collapses the network, not how much of it is imported. Part I supplies an answer that is architecture- and parameter-conditioned, and must be stated that way: **where import dependency remains load-bearing — the lunar and Mars ensembles — electronics is the most frequently observed minimum cut, and the vitamin parts are the last governance handle**; in the sampled central LEO draws a single import line is fatal only in a minority of draws (~0–11% for electronics across r3.5 regenerations), so there the material handle runs mainly through feed availability and the recovery loop rather than any one import line. Material-dependency governance has a
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
verification capacity; operator and government incentive analysis;
jurisdiction and liability rules; and failure recovery when communications
with Earth are unavailable. These are named requirements, not solved
problems. They must be tested under the same loss-of-import, shock, and
degraded-communications conditions used to test the production system.

Design principle: replication authority should be the
most verified and least autonomous function in the system — positioned
deliberately against the efficiency gradient, embedded at the seed stage,
because it cannot be retrofitted onto a mature complex.

## III.5 Falsifiable indicators, model-ranked

The indicators carry ordinal diagnostic ratings informed by the models
(consistent with III.3's refusal of numerical likelihood ratios — the r3.4
"expected likelihood ratios" phrasing was a leftover and is withdrawn):

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
   explicit material-vitamin stocks — strong for H2 over H1.
6. **Sustained scaled orbital-compute deployment despite publicly evident
   unfavorable unit economics** — moderate-to-strong for H1/H2 over H0 (Part II makes the test
   operational — watch fleet growth after the economics are public).
7. **Electronics vitamin-gap engineering**: stockpile facilities,
   shelf-life-rated spares logistics, off-world packaging/test lines
   — moderate-to-strong for H2 over H1 (Part I makes it the rational first move of a closure strategy).
8. **On-orbit materials-recovery recycling at scale** — moderate-to-strong for H2 (the Part I
   LEO feed-loop result; r3.5 note — the earlier sector-indispensability
   framing was a stale-output claim and is withdrawn, the indicator
   survives on the feed-dependence structure).
9. **An export-control-scoped internal model variant** — moderate.
10. **Terafab executed definitive agreements with committed capital**
   — weak-to-moderate (upgrades E7 from framework to program; hedging inside H0 still predicts it).

The ranking above asks which observations discriminate among H0, H1, and
H2. A second set asks whether the physical thesis is becoming feasible at
all. These lower-diagnosticity but still necessary indicators from the
Second Edition are retained:

- robots performing unscripted maintenance, construction, mining, and
  machine tending for long periods, with autonomous recovery fraction and
  human intervention hours reported per machine-hour rather than described
  only as "limited";
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

Threshold observations that would move Appendix A: a demonstrated ISRU
plant above ~50% full-system materials closure; audited robot production
figures; an independent satellite-reliability audit reporting
cohort-specific failures per satellite-year, separated from retirements and
planned disposals (the earlier "~2.5–3%" figure was an early-cohort fleet
fraction, not a general hazard rate, so divergence from it is not the right
test); and
any traceable datum on off-world-producible electronics tiers — the
vitamin-gap anchor this document flags as its highest-value currently parameterized missing
measurement. The thesis *weakens* if humanoid robotics remains
economically narrow, advanced manufacturing cannot be localized, launch
costs stop declining, closure requires a permanently growing Earth supply
chain, verification costs rise faster than capacity — or if Terafab
devolves into design-and-packaging dependent on external front-end
fabrication, which would reopen the fabrication term entirely.

## III.6 Refined complete thesis

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

    matter + energy + intelligence + time → expanding productive capacity

Recursive self-improvement is therefore not limited to software.
Intelligence improves the machinery and institutions that create
intelligence; the industrial substrate returns energy, compute, data,
experimentation, and physical agency to the intelligence layer. The
ultimate product is an industrial system capable of producing more of
itself.

The most precise formulation now available is conditional and
model-separated. Current evidence substantially supports deliberate
integrated space–AI–industrial development (P4a), but not an intended
transition to recursive closure (P4b). The inherited industrial model finds
expansion under some assumption sets and failure under others, with
electronics and feedstock dependencies localized by architecture. The new
integrated-bootstrap model makes a first explicit pass through the complete
intelligence–industry loop, seed bill of material, source network, and
reproduction to a second operating cell; it finds the lunar vitamin
bridge and the synthetic Moon–asteroid scenario model-feasible under
central assumptions and the configured strict lunar source graph
structurally infeasible. Because every new structural coefficient
is declared rather than measured, that is an executable hypothesis, not
evidence that the complete recursion can be built. The comparative-economics
model finds the Earth-dependent bridge uneconomic at anchored values and
does not price the mature high-closure ecology. Capability accumulation is
observed; positive off-world industrial reproduction and a unified closure
strategy are not.

$$
\begin{aligned}
I(t+1) &= I(t) + f(C,D,V,H), \\
H(t+1) &= H(t) + g(I,E,M,R) - \delta_{\mathrm{env}}H(t), \\
C(t+1) &= C(t) + h(H,E,\mathrm{fab})
\end{aligned}
$$

In earlier editions f, g, and h were unspecified placeholders and this
compact model was a causal diagram. The inherited model operationalizes g
as the lexicographic maximin allocation of Part I.7 (with repair,
recycling, stockpiles, and imports) and decomposes δ_env by sector and
environment. The Fourth layer supplies a first stylized f and h: installed
compute drives verified intelligence through a saturating gain law;
intelligence raises task autonomy and industrial productivity; the
resulting operating cells manufacture additional compute after construction
and commissioning lags. Constant-rate Earth-fed deployment is run beside it
as the counterfactual. These functions are executable and swept, but their
coefficients are ASSUMPTION-class and they omit training data, algorithmic
regime changes, verification failures, hardware-node detail, and many
coordination limits. The model therefore tests the consequences of a
coupling law; it does not measure that law or establish takeoff, subject
also to the speed caveat of II.5. The r4.1 ablations sharpen this
further: at central coefficients the dynamic coupling is inert — material
supply caps construction at every step — so the declared f and h
currently matter through seed feasibility (the static autonomy level),
not through the growth trajectories (I.8). A coupling whose removal
changes nothing is not evidence for recursion; it is a declared
mechanism awaiting a regime in which it binds.

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

---

# Part IV — Conclusion, and Speculative Terminal Scenarios

## IV.1 The defensible core, restated with numbers attached

Two walls, two escapes, one passage. The capital wall yields to expected
returns inside the historical envelope; the operating wall binds through
politics rather than physics at current scale; both escapes remain
conditional on surviving the bridge — and the bridge's failure mode is now
specific: hold electronics-class stockpiles against shelf life, and reach
local production of some electronics tier before the import ramp decays.
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

## IV.2 After convergence: deployment as the terminal regime

At some point the marginal value of further design improvement falls below
the marginal value of another deployed node — architectural convergence.
Past it, intelligence behaves as a commodity produced by infrastructure — heuristically, throughput ~ deployed energy × physical efficiency, a relation that omits memory, interconnect, utilization, data, reliability, verification, latency, workload composition, and fabrication yield. Efficiency is floor-bounded (Landauer, with reversible logic the stated exception); scale plausibly becomes the *dominant marginal* variable rather than the only one; scale means energy; energy means collector area; and collector area is not bounded by a planetary surface off Earth. It remains bounded — by matter, transport, orbital geometry, heat transport, collision risk, maintenance, and control, and per the published cluster analysis by the quadratic scaling of satellite count with cluster radius and by mutual occlusion of rejected infrared between closely flown spacecraft [S32]. The ceilings-and-rates
argument is retained in its r2.10 sensitivity form: the waste-heat ceiling
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
statement [S35] and no resolution; the scenario is conditional on it. **The
upgrade asymmetry, narrowed**: software-layer improvements propagate to
deployed compute at near-zero marginal cost, but hardware-dependent gains
require replacement or retrofit — silicon is not upgraded in place. The
model consequence: the space-electronics obsolescence term would shrink
after convergence only for its software-limited share.

## IV.3 Paradigm shifts: delay, alteration, or prevention

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
> values too. (r3.5 correction of r3.4's "fatal, not a delay — permanently
> negative": the computation tests a 20-year horizon under the stated
> deterministic configuration; it establishes no recovery *within that
> window*, not permanent impossibility — a longer horizon, resumed imports,
> altered plant design, larger initial surplus, or a lower knock fraction
> could change the outcome and are unswept.)
> The mechanism is the vitamin gap: at electronics q-scale 0.10–0.30,
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

## IV.4 The alternative telos, and the properly conditional close

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

The observed portfolio is consistent with an economic gradient toward
greater integration — discovery until convergence, deployment after it,
with space as one plausible arena under a demanding set of crossover
conditions that this edition has now priced. Present evidence does not
establish that recursive off-world industrial closure is the governing
objective of the companies described in Part III. Earlier editions ended by saying a model could decide; this one built the model. What the
model says is: the recursion is feasible only under assumptions that are
currently choices rather than measurements; the economics point to Earth
at every anchored value; and the observations that would change either
conclusion are now named, ranked, and waiting.

## Limitations and claim boundary

The most robust outputs are structural within the implemented model:
balanced doubling is unit-invariant; the three-stage allocator has a unique
state transition; realized endpoints include same-step shocks; recoverable
scrap cannot exceed loss-specific retirement; and Part II is exactly affine
in launch price. Architecture comparisons, endpoint definitions, and
regeneration from fixed seeds are also auditable.

The substantive conclusions remain assumption-conditioned. In the inherited
model, the requirement matrix, homogeneous electronics-closure multiplier,
repair and recovery efficiencies, stockpiles, shock process, import profile,
and finite capture reservoir are not measured as a coupled industrial
system. Its scalar-anchor screen does not rank structural matrix
uncertainty, interactions, policy families, or all environments, and its
LEO model has neither an endogenous debris stock nor a depleted capture
reservoir.

The Fourth layer adds a material-category-by-sector bill of materials,
source yields, Earth–Moon–orbit–asteroid transfer arcs, seed-mass
optimization, four knowledge layers, task-resolved autonomy, intervention
demand, process-specific gravity and centrifuge overhead, construction
and transport lags, commissioning, yield ramps, minimum viable scale,
reproduction to a second cell-equivalent, and an
active/derelict/fragment debris state. These are
model features, not validated factories. Its bills of material, recoverable
yields, source throughput, autonomy/productivity gains, lag and ramp
coefficients, intervention budget, asteroid portfolio, transfer capacities,
and collision kernels are declared assumptions. The seed is minimum-mass
only inside its fixed linear architecture, and it is sized as an
installed, operating nucleus: delivery, unloading, site preparation,
initial power deployment, calibration, and first commissioning are not
simulated. The reproduction dynamics advance one continuous aggregate
cell-equivalent — the 18-sector detail constrains seed sizing but does
not persist into reproduction, so sector-specific commissioning order,
partially complete second cells, and mid-construction bottlenecks are
not represented. Seventeen material categories
do not resolve mineralogy, alloying routes, contamination, process
chemistry, purity ladders, tool wear, quality yield, or every consumable.
The electronics tiers remain aggregates rather than fabs and tool chains.
Documented elemental occurrence is not a grade distribution, recoverable
reserve, refining yield, or accessible asteroid portfolio.

The terrestrial rehearsal in I.9 remains a proposed validation protocol,
not an accomplished demonstration; its computed scenario is a requirements
case, not an experiment. Gravity is treated more faithfully than a location
label, but only through declared process compatibility and centrifuge
mass/power penalties; the model does not simulate granular mechanics,
convection, melt behavior, vacuum welding, dust, radiation, traction, or
thermal cycling. The compute–intelligence loop is normalized and
phenomenological. The Earth counterfactual imposes rate and siting ceilings
rather than deriving land, grid, water, permitting, labor, or capital
prices. The debris module is a stress-test stock-flow model, not a
shell-resolved conjunction or traffic simulation.

Part II omits communications
and ground-network capex, program NRE, insurance, spectrum and regulatory
costs, and several spacecraft-bus functions; serviceability is a scenario,
not an observed property. The Part II cost comparison is not dynamically
coupled to the Fourth layer, so P3b remains unpriced even where the
physical-model quantities compound. Several inherited Part II intervals
still resolve through the collective [S36] record rather than a complete
claim-level bibliography. That is sufficient to reproduce the computation,
not to independently audit every range endpoint; Appendix A marks the
affected calibration as provisional.
Finally, the Part III strategy assessment is ordinal and observational:
corporate filings and statements establish declared initiatives, not an
intent to achieve recursive closure. No result in this paper is a forecast
or an empirical probability of success.

---

# Appendix A: Parameter Anchors

The authoritative, machine-readable anchor set is `params/anchors.yaml`
[S28]; every generated report carries a per-run provenance table. Ranges
reflect genuine disagreement across sources; values are anchors, not
precision claims. The Second Edition's discipline — quantities normalized
by type, rate quantities never averaged into one "r" — is implemented in
code (`delta.py`) rather than prose. Rows marked *(context)* are
documentary quantities cited for interpretation only: they are not wired
model inputs and have no YAML entry. Every other row resolves from the
YAML, and source classes use only the five enumerated classes of Scope
and Status.

**Calibration-provenance boundary.** Reproducible anchor resolution is not
the same as a complete scholarly source audit. Later sources provide exact
titles, dates, locations, and permanent links, but several inherited
anchors summarized through [S36] still lack an endpoint-by-endpoint record
of author or organization, title, date, page/table/section, permanent URL or
DOI, extracted value, and transformation. Until that claim-level register
is complete, the affected ranges are provisional calibration inputs and the
Part II multiples should not be described as independently source-audited.

## A.1 Capacity-loss quantities (δ), by type

| quantity | range | class [ref] | type |
|---|---|---|---|
| Solar-array degradation, GEO | 0.4–1.7 %/yr | peer_reviewed [S19] | continuous degradation |
| Terrestrial PV degradation | 0.5–0.6 %/yr median | peer_reviewed [S18] | continuous degradation |
| LEO constellation failure | ~3 % early generations; <0.5 % later | reporting [S22] | cohort-dependent; mixes failure, retirement, disposal; not a hazard rate |
| Satellite design life | ~15 yr GEO; ~5 yr LEO | technical_report (GEO) / reporting (LEO) [S22] | engineering envelope, not a hazard rate |
| Fab-tool depreciation | 2–5 yr | technical_report [S36] | accounting schedule; the wired model input is the advanced-obsolescence rate below |
| Advanced-node obsolescence rate, Earth | 0.15–0.35 /yr | technical_report [S36] | `delta.obsolescence_earth_adv`; frontier-equivalent capacity loss |
| Accelerator retirement | 3–6 yr | technical_report [S36] | technological retirement; `compute.life_years_earth` |
| Cluster interruption frequency | ~1 / 2,000 accelerator-days *(context)* | technical_report [S36] | mixes component, host, network, software events, mostly auto-recovered — NOT a component hazard rate |
| Space logistics penalty | 1–5 %/yr | **ASSUMPTION** | internal repair-chain tax; unanchored |

These are not interchangeable; the model converts each to
capacity-loss-per-year per component class before it enters a growth
equation. Solar-array and satellite data do not establish the depreciation
of mines, bearings, seals, machine tools, batteries, robots, or
dust-exposed thermal equipment — those entries are per-sector ASSUMPTIONS
in `params/environments.yaml`.

## A.2 Rate quantities previously conflated as "r" — separated

| quantity | range | class [ref] | what it does NOT measure |
|---|---|---|---|
| PV energy payback | 0.9–1.1 yr Europe; 1.0–4.1 harmonized | peer_reviewed [S20] | reproduction of mines, refineries, tools, or the panel line |
| Strawman replication design target | ~1 yr (assumed) *(context)* | technical_report [S23] | an estimate or measurement of anything — it is a proof-of-principle design assumption |
| Construction-execution cadence | ~10 months | reporting | recursive reproduction; used a mature host economy |
| Humanoid robot production | 50–100k targeted *(context)* | company_statement | feasibility — targets evidence intent |

System replication time is unknown as a measurement. In this edition it
exists only as a computed output distribution (Part I.8), set-labeled.

## A.3 Closure and data quantities

| quantity | range | class [ref] | note |
|---|---|---|---|
| Closure reported in cited nonreplicating applications | 90–96 % | technical_report [S23] | not a demonstrated result for the proposed factory; complete parts closure was outside its scope |
| Demonstrated ISRU O₂, Mars | 6–12 g/hr *(context)* | peer_reviewed [S21] | single output, small scale |
| Demonstrated lunar O₂ yield | ~20 %, TRL 5/6 | technical_report [S21] | full-system closure undemonstrated |
| Vitamin import fraction | 4–10 % | technical_report [S23] | CP-2255 residual |
| **Space electronics q-scale** | **0.10–0.30** | **ASSUMPTION** | **the vitamin gap — the results-driving unanchored number** |
| Fleet data scale | >10B supervised miles; ~220M fully driverless miles at another operator *(context)* | company_statement [S17, S30] | no conversion between regimes; not an advantage multiple or a model input |
| Heavy-lift flight tests | 13 through mid-2026 *(context)* | reporting [S31] | low-volume, high-information development proxy; not a capacity or reliability input |

## A.4 Comparative-economics budgets (Part II)

Every row resolves from `params/anchors.yaml`, whose per-entry notes carry
the full provenance detail; [S36] is the collective reference for rows
drawn from price sheets, operator disclosures, and industry reporting with
no single permanent identifier.

| quantity | range | class [ref] |
|---|---|---|
| LEO launch, published prices | $1,400–4,000 /kg | company_statement [S36: 2024–26 price sheets; F9 ~$70M/22.8 t, FH ~$97M/~63 t] |
| Cislunar / lunar-surface $/kg multipliers | 2–4× / 4–20× | ASSUMPTION [today's CLPS landed costs are ~100× LEO; range assumes maturing landers] |
| PV specific power | 80–150 W/kg | technical_report [S36: ROSA-class flexible blanket arrays] |
| Radiator specific mass | 3–12 kg/kW | technical_report [S36: deployable radiators at electronics-friendly reject temps; ISS EATCS practice ~6 kg/kW] |
| Accelerator system cost | $25–45k /kW IT | reporting [S36: H100/B200-class system pricing 2024–26] |
| Space qualification multiplier | 1.2–3.0× | ASSUMPTION (low end: COTS practice [S34]; [S32] radiation data supports 5-yr TID at the low end, system reliability open) |
| Equipment life, space / Earth | 3–7 / 3–6 yr | reporting (space) / technical_report (Earth) [S36: LEO design lives; accelerator refresh cycles per A.1] |
| Accelerator mass | 10–30 kg/kW IT | ASSUMPTION |
| Space power overhead | 1.10–1.25× | ASSUMPTION |
| Operations fraction | 2–6 % of capex/yr | ASSUMPTION |
| PV cost | $500–2,000 /kW | reporting [S36] |
| Radiator cost | $200–1,000 /kW | ASSUMPTION |
| Structure overhead fraction | 0.20–0.50 | ASSUMPTION |
| Lunar night storage | 4–10 kg/kWh | technical_report [S36] |
| Serviceable-platform infrastructure life | 10–25 yr | ASSUMPTION; requires power/thermal/structure reuse across compute refreshes |
| Integrated-disposable infrastructure life | equal to space equipment life | architecture definition; all assets retire together |
| Utilization LEO / cislunar / lunar | 0.65–0.95 / 0.90–0.99 / 0.45–0.85 | ASSUMPTION ([S32] dawn-dusk cluster design supports the LEO high end) |
| Starmind AI1 compute / solar / vehicle efficiency | 150 kW peak, 120 kW average / 150 kW / 70 kW·t⁻¹ | company_statement [S38]; conditional scenario |
| Starmind AI1 aggregate mass | 14.3–17.9 kg per average kW | ASSUMPTION derived from [S38]'s unspecified peak-vs-average efficiency denominator |
| Starmind AI1 radiator area / deployed envelope | 110 m² / 20 m × 70 m | company_statement [S38]; context only, no disclosed mass or cost |
| Aspirational AI1 launch cost / efficiency / mass | $185/kg / 100 kW·t⁻¹ / 10 kg per average kW | company targets plus derived arithmetic [S37]; deterministic case only |
| Aspirational AI1 qualification / life / utilization | 1.2× / 7 yr / 0.95 | ASSUMPTION; favorable existing bounds, not SpaceX specifications |
| DC capex | $11–20k /kW IT | reporting [S36: AI-optimized facility costs 2025–26, $11–20M/MW] |
| PUE | 1.10–1.40 | reporting [S36: hyperscale AI facilities] |
| Firm-power floors: nuclear PPA / gas | $0.09–0.13 / $0.04–0.06 per kWh | reporting [S36: restart PPAs ~$100–115/MWh; gas floor politically conditional, CCGT <$1,000/kW per S35] |
| Earth electricity price | $0.05–0.12 /kWh | reporting [S36] |
| Gas power capex | $700–1,200 /kW | reporting [S36] |
| Older-node hardware | $8,000–15,000 /kW | reporting [S36] |
| Older-node energy penalty | 1.5–3.0× | technical_report [S36] |
| Starmind AI1 solar power density | 250 W/m² | company_statement [S38] |
| Orbital-compute scale target | 100 GW/yr | company_statement [S37]; enters II.3's scale audit only |
| WACC | 8–15 % | ASSUMPTION |

## A.5 External claims and quarantined sensitivity targets

| claim | value | class [ref] |
|---|---|---|
| Mature-Starship formal aspiration | ≤$185/kg to orbit, derived from a stated ≥99% reduction from $18,500/kg; V3 100 t and possible V4 200 t | company_statement [S37]; comparison axis and deterministic best-case input, not a quoted price or MC prior |
| Aggressive / extreme Starship sensitivities | $100/kg / $30–50/kg; full-load equivalents: V3 $10M / $3–5M, V4 $20M / $6–10M | derived scenario axes; no demonstrated cost or customer price |
| Google/Planet crossover threshold | $200–300 /kg | company_statement [S34] |
| Suncatcher launch-cost feasibility marker (not a parity claim) | ≲$200 /kg by mid-2030s; launch-only vs electricity-only | technical_report [S32] |

## A.6 Engineering cross-checks added after the IPO — not model inputs

These values test or partition the Part II architecture rather than silently
changing its priors. Where they become model inputs in a later edition,
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

## A.7 Provisional hiring-sweep note — not an evidence-table item

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

# Appendix B: Revision History and Provenance

**4.0 (this edition)** — standalone expansion of the complete, frozen r3.5
manuscript. It distinguishes constant Earth-fed orbital deployment from
endogenous off-world reproduction; defines a machine-only reference
ecology; treats gravity as a process-specific requirement; defines an
embodied-autonomy threshold; expands the industrial seed into physical,
digital, industrial-memory, and experimental layers; adds a terrestrial
autonomous-closure rehearsal culminating in a commissioned second
production cell; and frames the Moon as the initial bulk-material backbone,
Earth as the early material-vitamin supplier, and asteroids as a later
diversity layer.

The new executable layer implements the program: 18 sectors, 17 material
categories, a material-category-resolved bill of material, explicit source
and transfer arcs, minimum-mass seed sizing, autonomy/intervention
constraints, gravity and centrifuge overhead, construction/commissioning
dynamics, rate-limited Earth and Earth-fed orbital counterfactuals,
operational compute–intelligence–productivity coupling, electronics
tiers, and active/derelict/fragment debris dynamics. Central and 200-draw
deterministic assumption-ensemble results are reported in I.8 and
regenerate from `scripts/run_fourth.py`; `outputs/fourth/MANIFEST.md`
checksums their exact inputs and outputs. The completed ledger in
`docs/FOURTH_EDITION_PLAN.md` maps each proposed change to prose, code,
tests, and artifacts. No Fourth Edition output is presented as a
measurement, empirical probability, engineering estimate, or forecast.

A release-candidate correction pass against a fourth external review
then: restated the seed as an installed operating nucleus (delivery,
unpacking, and first commissioning outside the model); renamed the
reproduction metric to first passage to two operating-cell equivalents
and added the transient-versus-durable year-40 reading (the terrestrial
rehearsal reproduces once and holds only 1.93 equivalents at year 40);
relabeled the model material-category-resolved (15 elements plus
rare-earth and dopant classes); restated strict-lunar 0/200 as a
structural LP infeasibility preserved by every draw, and the
Moon–asteroid case as a synthetic composite portfolio; renamed
$R_{\mathrm{debris}}$ the five-year fragment creation-to-clearance ratio
and withdrew subcritical/supercritical language (the ratio is
non-monotonic in mitigation strength); documented the 0.5
autonomy-productivity floor and the fixed 5 t digital-seed aggregation as
declared conventions; removed three stale Third Edition passages (I.3
process-gravity variables, I.4 queued-debris metric, I.5 unsized seed);
reported the vitamin stock's 23–27% share of installed seed mass;
committed the import-decay sweep the manuscript had quoted only from a
figure (`outputs/tables/import_decay_deep.csv`); reconciled Appendix A
with `params/anchors.yaml`; corrected the 95%-lunar-closure distance
(≈15–30×, not two orders of magnitude) and two rounding drifts; embedded
the committed figures into the manuscript; and queued durable-endpoint,
ablation, Pareto-frontier, and diagnostics work as r4.1 scope (ROADMAP).

An r4.1 analysis pass then implemented the computable subset of that
queue as an additive layer (`fourth_analysis.py`; seven tables, one
figure, seven tests; no previously reported quantity changed): durable
reproduction endpoints, vitamin-stock resolution, zero/freeze
intelligence-coupling ablations, the oversize mass-versus-time frontier,
per-draw ensemble diagnostics, and the strict-lunar elastic
infeasibility certificate. Its headline findings: the declared dynamic
intelligence coupling is inert at central coefficients (construction is
material-limited at every step, so ablating the coupling changes
nothing, while the assumed AI level binds statically through seed
feasibility); lunar-bridge reproduction is transient (retained in all
126 feasible draws, durable in none); minimum mass is not time-optimal
(doubling the bridge seed cuts first reproduction from 11.25 to 8.0
years); and the strict-lunar infeasibility resolves to a quantified
Ni/Cu/C/Co/Cr/rare-earth/Li/H/dopant shortfall table. Items needing new
declared coefficients (sector-resolved reproduction, a delivered-seed
deployment stage, shock-recovery endpoints, shell-resolved debris)
remain queued.

**3.5 (frozen Third Edition baseline)** — final integrity and publication pass: the
lexicographic allocator now ends in a normalized strictly convex QP so the
state transition is unique; binding is a unit-invariant finite 1% response
with co-binding credit; realized endpoints are post-shock and timestamped
at step ends; scrap is loss- and environment-specific recoverable
retirement; LEO's import-cut row is qualified as continuing capture feed;
and Part II reports serviceable/reusable and integrated-disposable
architectures separately with complete equations and a worked example.
Author, abstract, keywords, formal limitations, exact FCC filing metadata,
HTML citation metadata, and a standalone changelog were added. This follows
the earlier reproducibility and model-identity pass against a
third external review, which found the r3.4 committed artifacts mutually
inconsistent (the committed deep report predated the committed CSV — the CSV
had been regenerated by a partial rerun script, since deleted) and identified
four implementation defects, all confirmed and fixed: (1) Part II seeds were
process-salted `hash()` values, so the script was nondeterministic across
processes — replaced with stable crc32; (2) the stated shared-draw
correlation between Earth and space was not implemented — `AnchorSet` now
caches each anchor's draw; (3) the system doubling metric was the
unit-dependent Σ K_j — replaced as headline by the unit-invariant balanced
metric λ(t) = min_j K_j(t)/K_j(0) ≥ 2, with Σ K relabeled "aggregate";
(4) the binding-sector statistic changed definition between the baseline
(relative slack) and the policy comparison (realized-growth argmin) — both
now use the finite 1% response definition. Further: endpoint hierarchy
separating realized post-shock g>0, the pre-shock allocation diagnostic,
sustained years 25–30, and an Earth-import cutoff; component-specific Part II lives (infrastructure vs compute
refresh — central space LCOs fell accordingly); the lunar reference case
relabeled Earth-supplied (closure 0); cost-exclusion bias no longer claimed
uniformly pro-space; retooling fatality restated horizon-relative
("model-fatal within the tested 20-year window"); electronics-closure
finding restated as conditional on the homogeneous-multiplier
implementation, with the sub-sector decomposition roadmapped; every
artifact regenerated from one script execution with a checksummed manifest
and generated-vs-committed consistency tests; textual repairs (public
release pending → live repository; E12 residue; likelihood-ratio wording;
satellite-audit threshold; "per unit of assumption-optimism" withdrawn;
S-1 → SEC-filed offering materials; scoped sensitivity claim; valid
lockfile; deep run parallelized with unchanged seeds). A closing
performance-and-stability pass then (a) replaced the per-step
scipy.linprog calls with a persistent warm-started HiGHS model (~10×,
verified equivalent to ~1e-15 against the retained scipy reference path),
(b) split each Monte Carlo cell into independently seeded chunks for pool
load-balancing (full deep run measured 706.6 seconds on nine workers on
the 2026-07-27 release host; runtime is hardware-dependent), and (c)
re-keyed every anchor
draw to (run seed, anchor name) so that adding anchors to `anchors.yaml`
can never again re-roll existing cells — (b) and (c) re-baselined all
Monte Carlo values once, each cell moving within its Wilson interval; the
margin-conditional cut-fatality and paired-policy cells moved most, and
the text now quotes them ordinally with their across-regeneration spread
displayed. The r2.11
carry-forward audit was then ported from r3.4, restoring the physical-data
evidence, coordination architecture, detailed control requirements,
seven-stage roadmap, feasibility indicators, contextual anchors, full
glossary, and annotated source record without reverting any r3.5 model or
reproducibility correction. The Part II launch-price sweep was also
normalized against SpaceX's June 2026 V3/V4 disclosures: the traceable
formal aspiration is now reported as ≤$185/kg, with $100/kg labeled
aggressive and $30–50/kg labeled extreme rather than collectively described
as company targets. A post-IPO orbital-compute calibration pass then added
independent conventional and low-mass architecture envelopes, NASA
full-thermal-system data, an explicit spacecraft-build-cost omission,
platform reuse as the condition supporting long infrastructure lives, and
the inference-versus-training network boundary [S39–S44]. These studies are
reported as cross-checks rather than silently substituted into the r3.5
Monte Carlo priors. The subsequent aspirational-case pass added a
deterministic AI1 boundary using the company-stated $185/kg and 100 kW/t
targets, kept favorable qualification/life/utilization visibly
`ASSUMPTION`-class, excluded the case from Monte Carlo, and reported its
100-GW/year mass, cadence, and cost implications. The publication pass made
standalone HTML the primary reading edition, converted display equations to
native MathML, and added responsive screen and print styling; Markdown
remains the canonical editable source. A subsequent
location-architecture addendum made
the unmodeled Kessler feedback explicit, partitioned a lunar-surface material
backbone from its sparse orbital service layer, and corrected
"Sun-synchronous" versus "heliocentric" in the post-lunar sequence without
adding unsupported numerical priors [S45–S49].

Second Edition history (2.1–2.10) is summarized: 2.1 economics of closure;
2.2 terminal regime; 2.3 paradigm shifts; 2.4 physical-process data;
2.5 unified build record, export-control fence; 2.6 first anchors, measured
correction to the space-depreciation claim; 2.7 Coasean treatment, gateway
governance; 2.8 Terafab against the S-1, propositions ladder, replication
time marked unknown, δ decomposition, vector closure, H0–H3; 2.9 editorial
pass, first-party messaging as evidence, Appendix A restructure;
2.10 orbital compute partially quantified against a published design
study, efficiency as mass multiplier, LEO no-repair concession, temporal
irreproducibility, demand saturation, biosphere telos, payload
cost-performance.

**3.4** — model-integrity and audit pass against a second
external review: LEO relabeled an import-supported orbital recycling
network with an explicit mass-accounting caveat (finite capture reservoir
unmodeled; recycling yield < 1; conservation state queued); doubling-time
denominators split (ever-doubled vs survivor-conditioned, with the
doubled-then-failed class reported); complete model specification added as
Appendix D; cost inclusion/exclusion accounting added to II.2; financing
equalization stated as a deliberate pro-space assumption; policy-robustness
and sensitivity claims scoped to their tested regimes; H0 redefined to
admit standalone orbital projects; independent-actor items (E12/E15) moved
from the strategy table to external cross-checks; III.5 indicators made
ordinal; governance leverage architecture-conditioned; hiring-corpus
cross-check marked provisional; "probabilistic minimum cut" replaced by
ensemble-frequency language; stale r3.2 numbers, cross-references, test
counts, and register fixes throughout. A final carry-forward audit restored
r2.11's physical-data evidence, coordination architecture, detailed control
requirements, seven-stage roadmap, feasibility indicators, contextual
anchors, full glossary, and annotated source record without reverting any
of the Third Edition's model-based corrections.
**3.3** — methods-and-consistency pass against external
review: Executive Summary reconciled with the results tables (per-location
binding statement; conservative sets mostly fail rather than fail
categorically; optimistic doubling stated per location); P3 split into
quantified P3a (bridge-economy compute) and unquantified P3b (mature
high-closure ecology); the P4a/P4b split propagated through the Part III
evidence table with ordinal diagnosticity on two margins replacing
multiplied qualitative likelihood ratios; ensemble-frequency language and
counts with Wilson intervals throughout (n = 400 per Part I cell; 0/2,000
reported as a bounded frequency, not zero); Suncatcher radiation findings
corrected (HBM most TID-sensitive vs logic/SRAM most SEE-sensitive; ~1 per
3M inference errors; five-year TID supported with margin, seven-year
*system* reliability the open question; arXiv v2 cited); FCC item corrected
from approval to acceptance for filing; Suncatcher restated as an announced
prototype program; allocation-policy robustness (receding-horizon and
aggregate policies) and displayed global sensitivity added to Part I;
false precision reduced; reproducibility specification expanded.
**3.2**: the Second Edition's r2.11 correction pass merged in full — the orbital-compute study recharacterised from parity claim to launch-cost feasibility marker against its own text; the 1980 anchor recharacterised as a strawman target with closure drawn from nonreplicating applications; depreciation de-overinterpreted and five capacity-loss quantities separated; the very-low-orbit concession narrowed against the ~650 km published architecture; Terafab sites, executed county agreements, Intel's fab record, and withdrawn scale comparisons; P4 split into documented integration (P4a) and inferred closure (P4b) with nested hypotheses; robot-reproduction, clock-setting, and governance-leverage relations reformulated; the Coasean argument made conditional on relative cost movement; the temporal data moat softened to a lead-time barrier; terminal-scenario absolutes bounded; the LEO/lunar robustness-versus-speed inversion explained; the vitamin-gap circularity stated in the summary; rewritten fully standalone. **3.0–3.1**: the multisector feasibility model and the
Earth–space crossover model built, run, and integrated ([S28]; Parts I–II);
H0–H3 assessed against fifteen items with model-informed discriminators
(Part III); Section 16 scenarios quarantined with model checks (Part IV);
Appendix A regenerated machine-readably; the vitamin gap promoted to the
document's highest-value currently parameterized missing measurement; external claim checks
localizing the public crossover disagreement to three parameters;
r3.1: rewritten standalone.

# Appendix C: Reproducibility

    python -m venv .venv
    .venv/bin/pip install -r requirements.lock
    .venv/bin/python scripts/run_baseline.py  # Part I sweep + figures (~3 min)
    .venv/bin/python scripts/run_part2.py     # Part II (~15 s)
    .venv/bin/python scripts/run_deep.py      # deep run (706.6 s / 9 workers here; hardware-dependent)
    .venv/bin/python scripts/run_fourth.py    # integrated bootstrap
    npm run build:manuscript -- --html-only  # r3.5 standalone HTML
    npm run build:fourth                     # r4.0 standalone HTML only
    .venv/bin/python scripts/write_manifest.py  # run last
    .venv/bin/pytest tests/ -q                # 79 tests

Model: `src/rsimodel/{model,delta,cutsets,montecarlo,lco,policies,plots,report}.py`;
parameters: `params/{anchors,assumptions,environments}.yaml`; generated
reports with per-run provenance tables and machine-readable CSV summaries:
`outputs/` (headline table: `outputs/tables/mc_deep.csv`). Stages 1–2 of
each allocation use HiGHS through a persistent warm-started model, with
`scipy.optimize.linprog` as the retained reference/fallback path and
`RSI_SLOW_LP=1` to force it. Stage 3 uses the pinned OSQP solver for the
strictly convex normalized tie-breaker, with a numerical fallback. All randomness
flows through explicitly seeded `numpy.random.Generator` instances; every
script derives its seeds from stable crc32 strings (never Python's
process-salted `hash()`, an r3.4 defect), and each anchor's Monte Carlo
draw is keyed by the run seed plus the anchor's NAME, so results are stable
both across processes and under anchor-list growth. All tables regenerate
deterministically within a pinned reference environment.
`outputs/MANIFEST.md` records the sha256 of every inherited release artifact,
including the canonical Markdown and standalone HTML, plus library versions;
it omits a self-referential generating-commit field. `tests/test_repro.py` cross-checks
the committed CSV against the committed report so mutually stale artifacts
(the r3.4 failure) fail the suite. `outputs/report_deep.md` and
`outputs/tables/mc_deep.csv` are written by a single execution of one
script and cannot diverge. Structural coefficients are ASSUMPTION-class and
live only inside named assumption sets.

The Fourth model is `src/rsimodel/fourth.py`, with the additive r4.1
analysis layer in `src/rsimodel/fourth_analysis.py`, configured entirely
by `params/fourth_edition.yaml` and run by `scripts/run_fourth.py`.
`outputs/fourth/report.md`, thirteen CSV tables, and five figures are
generated from one in-memory scenario set. `outputs/fourth/MANIFEST.md` records the
sha256 of the configuration, implementation, runner, focused tests, and
every generated artifact. Its ensemble uses 200 deterministic named draws
per scenario from seed 404. Adding a draw or changing a coefficient changes
the manifest; none of that upgrades an assumption to evidence.

**Archival status.** Public repository:
**[rsi-model repository](https://github.com/fperegrinvs/rsi-model)**. r4.0
is the release candidate published on `main`; this text does not claim
that the release tag already exists. The frozen r3.5 Markdown,
HTML, and DOCX remain present as the inherited release baseline.
Accordingly, the untagged r4.0 HTML omits canonical/public URL,
publication-date, and `citation_doi` metadata rather than pointing at
mutable `blob/main` or mislabeling the concept DOI. The final tagged build
must supply an immutable URL, release date, and version DOI through the
documented build environment variables.
Dependency lockfile:
`requirements.lock` (numpy 2.1.3, scipy
1.16.0 [HiGHS], OSQP 1.1.3, PyYAML 6.0.3, matplotlib
3.10.3, pytest 9.0.2; Python 3.12.7, macOS/arm64; direct pins only —
transitive hash-pinning is roadmapped). Citation metadata:
`CITATION.cff`. License: MIT for code (`/LICENSE`), CC BY 4.0 for the
manuscript and documents (`docs/LICENSE`). DOI: concept
**10.5281/zenodo.21619447** (all versions); each release tag mints its own
version DOI via the Zenodo integration. The 79 tests cover selected
invariants, determinism, metric identities, artifact consistency, and the
generated HTML's semantic publication structure — they do not establish
that the specification adequately represents industrial reality, and no
test suite could.


# Appendix D: Complete model specification

Everything a reader needs to reconstruct the Part I model without opening
the implementation. Part II's cost model is fully specified by its affine
form (II.2) plus the anchor table (A.4), with two r3.5 amendments: the
annualization applies component-specific lives (compute hardware and its
replacement launch mass on `compute.life_years_space`; PV, radiator,
storage, structure, and their launch spend on
`power_systems.infrastructure_life_years`, floored at the hardware life —
the LCO remains exactly affine in launch $/kg), and each Monte Carlo
iteration resolves every anchor once per cached AnchorSet so Earth and
space genuinely share draws. This appendix covers the multisector
dynamics and then specifies the Fourth Edition layer that runs beside it.

## D.1 Fourth Edition integrated-bootstrap layer

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
`params/fourth_edition.yaml`.

**Material and service closure.** For material category $e$, sector $j$,
and source/transfer arc $a$:

$$
\Delta M_e
= \sum_s Y_{s,e}X_s + I_e + \sum_a F^{\mathrm{in}}_{a,e}
- \sum_j B_{e,j}x_j - L_e - \sum_a F^{\mathrm{out}}_{a,e},
$$

where $B_{e,j}$ is the amount of material category $e$ required per unit
of sector-$j$ build, $Y_{s,e}$ is the recoverable yield from source and
process $s$, and $F_{a,e}$ is material flow across an Earth, lunar
surface, orbital, or asteroid transfer arc. Concentration alone does not
set $Y$; mineral form, beneficiation, refining energy, purity, and loss
remain outside the occurrence citations. Service closure uses
$A_{i,j}$, the sector-$i$ service output needed to reproduce and replace
sector $j$. Recoverable lunar and asteroid yields, rather than bulk
inventory, enter the constraints. Earth material appears only as the
bounded initial vitamin stock $v_e$.

**Process environment and autonomy.** For each process $j$, task coverage
at AI level $I$ is

$$
c_j(I)=\min\{c_j^{\max},\ c_j^0+\alpha_j\max(I-1,0)\}.
$$

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

$$
\mathrm{rpm}_j=\frac{60}{2\pi}
\sqrt{\frac{9.80665\max(g_j^\ast-g_L,0)}{r_j}}.
$$

This is an equipment penalty, not a claim that a whole lunar factory or
habitat requires artificial gravity.

**Seed sizing.** Decision variables are sector capacities $z_j$, annual
lunar and asteroid feed $p_L,p_A$, and initial Earth vitamins $v_e$.
The linear program minimizes

$$
M_{\mathrm{seed}}
= M_{\mathrm{digital}}+\sum_j z_j\sum_e B_{e,j}^{\mathrm{eff}}
+\sum_e v_e,
$$

subject to minimum viable sector capacities, task coverage and intervention
limits, service output sufficient for replacement plus one complete second
cell, element balances through each scenario horizon, and mining, refining,
transport, and energy throughput. Sector commissioning lags and half-ramp
loss reduce productive years. $M_{\mathrm{digital}}=5$ t represents the
software, simulation, industrial-memory, and experimental package; its
value is an assumption, not a storage-mass estimate.

**Dynamic reproduction.** A feasible seed begins as one installed and
operating cell — delivery, unloading, site preparation, and first
commissioning are outside the model, so seed mass refers to an installed
operating nucleus, not a self-deploying delivered package. Each quarter,
lunar production, commissioned asteroid production, and recovered
retirement enter inventory; the complete
cell-level material vector limits new orders. Orders become installed after
a two-year construction queue and operating through a 1.5-year yield ramp.
Cells depreciate at 0.04/yr and 82% of retired cell material is assumed
recoverable. The state is a continuous aggregate of cell-equivalents; the
reported reproduction event is **first passage of operating
cell-equivalents to 2.0**, not the discrete commissioning of a second
factory's subsystems.

Installed compute $C_t$ raises normalized intelligence according to

$$
I_{t+\Delta t}
= \min\{I_{\max}, I_t
+\ell\,v\log(1+C_t/C_0)\Delta t\},
$$

where $\ell$ is the learning coefficient and $v$ the verification
factor. Intelligence above the scenario starting level raises both
industrial productivity and autonomy, which raises cell output and future
compute. Earth and Earth-fed orbital counterfactuals instead add capacity
at constant, scenario-specific build/delivery rates, subtract 0.16/yr
depreciation, and impose terrestrial site ceilings. Moon→orbit compute has
a 0.5-year lag, a 35% share of new endogenous capacity, and a
transport-capacity ceiling.

**Debris state.** A separate stress test evolves active assets, derelicts,
and a fragment index. Failures, controlled disposal, retrieval, collisions,
fragment creation, natural clearance, and active removal are explicit.
$R_{\mathrm{debris}}$ — the five-year fragment creation-to-clearance
ratio — is fragments created divided by fragments cleared
over the last five years: a flow ratio, not a branching-process
reproduction number, and not monotonic in mitigation strength. Realized
clearance is capped by the fragments available, so at an empty fragment
stock the ratio reads exactly one. The distributed case multiplies the collision
kernel by 0.01; it is therefore a declared topology test, not a derived
property of heliocentric space.

**Scenarios and uncertainty.** The four named cases are terrestrial
rehearsal, lunar vitamin bridge, strict lunar-only, and Moon–asteroid
network. Their horizons, AI levels, import caps, intervention budgets, and
source commissioning dates are all explicit in the YAML. Each 200-run
ensemble uses stable crc32 names from seed 404 to draw independent
log-uniform multipliers for service productivity, bills of material, lunar
and asteroid yield, depreciation, lag, and autonomy gap. Frequencies across
those draws are not empirical probabilities. Tests verify dimensions,
nonnegative balances, strict-lunar infeasibility, finite-vitamin behavior,
gravity overhead, second-cell commissioning, named-draw stability, and the
debris threshold. `outputs/fourth/MANIFEST.md` binds the configuration,
implementation, runner, tests, tables, figures, and report.

**r4.1 analysis layer.** `src/rsimodel/fourth_analysis.py` adds derived
diagnostics over the same declared coefficients, inventing none:
durable-reproduction endpoints (retention at horizon, final-five-year
net reproduction, vitamin-pool exhaustion timing); vitamin-stock
resolution; zero/freeze intelligence-coupling ablations; the
installed-mass-versus-reproduction-time oversize frontier
(`simulate_reproduction(initial_cells=f)` installs f cell-equivalents of
the fixed minimum-mass design); per-draw ensemble diagnostics over the
identical named crc32 draws (failure reasons, binding-constraint
frequencies, Spearman sensitivity); and an elastic-relaxation
infeasibility certificate that interrogates the exact seed LP through a
shared matrix builder. Seven additional tables and one figure regenerate
with the run; no previously reported quantity changes. Ablation variants
requiring new declared magnitudes (delayed gains, degraded
verification), shock-recovery endpoints, and alternative seed objectives
remain queued (ROADMAP).

## D.2 Inherited ten-sector model

**Sectors and units.** n = 10 sectors, ordered: power, mining, refining,
robotics, machine_tools, electronics, thermal, transport, repair,
recycling. Capacity K_j is in abstract capacity units (K_j(0) = 1 for all
j unless stated); sector j produces q_j output units per capacity unit per
year (q below is the central set after environment q-scaling for the lunar
architecture is applied via `environments.yaml`; the tabulated q is the
pre-scaling set value). Repair and recycling are service sectors: their
rows in A are zero, and their outputs are consumed as described below.

**Time.** Discrete steps of Δt = 0.25 yr (0.5 yr for cut-set enumeration),
default horizon 35–40 yr. This inherited layer has no construction lags,
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

$$
\begin{aligned}
x_j + u_j - \delta_j K_j
  &\ge gK_j && \forall j, \\
u_j
  &\le \delta_{\mathrm{wear},j}K_j && \forall j, \\
\sum_j A_{ij}x_j
+ s_f\sum_j A_{ij}u_j
+ \mathbf{1}_{i=\mathrm{repair}}\frac{1}{\eta_{\mathrm{rep}}}\sum_j u_j
+ \mathbf{1}_{i=\mathrm{recycling}}w
+ o_iw-\rho_iw-d_i
  &\le q_iK_i+m_{\mathrm{direct},i} && \forall i, \\
w+\eta_{\mathrm{scrap}}\sum_j f_{\mathrm{wear},j}u_j
  &\le \eta_{\mathrm{scrap}}
  \sum_{j,c}f_{c,j}\delta_{c,j}K_j, \\
d_i
  &\le \frac{S_i}{\Delta t}.
\end{aligned}
$$

with s_f = spares fraction (0.15), η_rep = repair efficiency (0.75
central), η_scrap = processing yield (0.40 central, < 1 always), o =
recycling opex vector, ρ = recycling output profile, and f_c,j = the
recoverable share of loss component c in sector j. Equivalently, available
retirement before processing is

$$
R(K,u)=\sum_{j,c}f_{c,j}\delta_{c,j}K_j
-\sum_j f_{\mathrm{wear},j}u_j.
$$

The environment defaults are:

| environment | wear | catastrophic | obsolescence | logistics |
|---|---:|---:|---:|---:|
| LEO | 1.00 | 0.00 | 1.00 | 0.00 |
| lunar | 1.00 | 0.50 | 1.00 | 0.00 |
| Mars | 1.00 | 0.25 | 1.00 | 0.00 |
| Earth | 1.00 | 0.80 | 1.00 | 0.00 |

Stage 2 holds g at its optimum and minimizes dimensionless stock draw
$\sum_i\omega_i d_i$, where $\omega_i$ is the inverse of a same-unit
scale based on current supply and available stock, normalized by the
largest weight. Stock is a buffer, not fuel, and the objective is invariant
to changes in sector row units.

Stage 3 holds the stage-1 and stage-2 optima within solver tolerance and
minimizes a strictly convex normalized action norm:

$$
\min\left[
\sum_j\frac{x_j^2+u_j^2}{\widehat K_j^2}
+\frac{w^2}{\widehat R^2}
+\sum_i\frac{d_i^2}{\widehat D_i^2}
+g^2\right].
$$

All scales are positive state-derived quantities with numerical floors.
The positive-definite Hessian makes the selected action, and therefore the
state transition, unique. Stage 1 and 2 use HiGHS; stage 3 uses OSQP with a
public SLSQP fallback for rare narrow-face numerical failures.

**State updates and shocks.**

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

with shelf life L_i (electronics 5 yr central), capacity cap
C_i = c_years · Σ_j A[i,j] δ_j K_j (replacement demand), initial stock
S_i(0) = s_years · replacement demand at t = 0, stockable sectors only
(robotics, machine tools, electronics, repair). Common-cause shocks are
applied after this deterministic capacity update; the stock cap is then
recomputed from the damaged capacity. Reported timestamps and shock-log
timestamps are the step end $t+\Delta t$. The headline realized growth is

$$
g_{\mathrm{real}}=
\min_j\frac{K_{j,\mathrm{postshock}}-K_{j,\mathrm{prestep}}}
{\Delta t\,K_{j,\mathrm{prestep}}},
$$

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

**Outcome definitions (r3.5 hierarchy).** *Expanding at year 30*: realized
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
physical seed has been commissioned. *Aggregate doubling* (continuity with earlier revisions): first t
with Σ_j K_j(t) ≥ 2 Σ_j K_j(0), measured against the supplied K(0) —
unit-dependent, reported alongside but never as "system replication".
Both doubling metrics are reported over all runs that ever reach the
criterion and conditioned on year-30 survivors — the difference is the
doubled-then-failed class.

**Binding sector and co-binding (r3.5).** At each allocation step, each
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

Column j of A is the recipe for one unit of sector-j capacity; rows are
the supplying sectors (pow=power, min=mining, ref=refining, rob=robotics,
mt=machine_tools, el=electronics, th=thermal, tr=transport, rep=repair,
rec=recycling).

# Glossary

**Recursive self-improvement (RSI):** a process in which an intelligent
system contributes to producing a more capable successor.

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
local production network. In this edition it has four layers: physical
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

**Operating-cell equivalent:** the Fourth layer's continuous unit of
installed, commissioned productive capacity, normalized to the initial
seed cell. The reported reproduction event is first passage of this
aggregate to 2.0; it is not a claim that a discrete second factory has
completed commissioning.

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

**Vitamin parts:** the residual imported microelectronics, bearings,
precision instruments, catalysts, or other high-complexity inputs that
resist local production. The term comes from the 1980 closure literature.

**Vitamin gap:** in this model, the unclosable fraction of the electronics
sector's output mix — the results-driving unknown sampled through the space
electronics q-scale.

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

# Sources

Second Edition numbering is retained through [S27]. The executed companion
model occupies [S28], so the former [S28–S33] sources appear here as
[S29–S34]; [S35] is the new external fast-takeoff/capital-mobilization
cross-check, and the former collective source [S34] becomes [S36]. The
Second Edition's planned-analysis entry [S35] is superseded by the executed
model at [S28]. [S37] is the primary June 2026 Starship V3/V4 disclosure
used to normalize the launch-price sensitivity cases; [S38] is the
subsequent AI1 product specification. [S39–S44] are the independent
spacecraft, thermal, network, microdatacenter, and economic cross-checks
added to Part II in the post-IPO calibration pass.

## Primary statements

**[S1]** SpaceX, ["Mars & Beyond: A City on
Mars"](https://www.spacex.com/humanspaceflight/mars).

> SpaceX states that establishing a self-sufficient city on Mars requires
> large-scale cargo and population transfer.

**[S2]** Tesla, ["Master Plan Part
3"](https://www.tesla.com/master-plan-part-3).

> Tesla outlines a proposed path to a sustainable global energy economy
> through electrification, renewable generation, and storage.

**[S3]** xAI, ["Company: Accelerating Scientific
Discovery"](https://x.ai/company).

> xAI describes its mission as accelerating scientific discovery and
> extending what humanity can know and do.

**[S4]** NASA, ["Overview: In-Situ Resource
Utilization"](https://www.nasa.gov/overview-in-situ-resource-utilization/).

> NASA describes technologies for using destination resources to produce
> water, fuel, supplies, and construction capability.

**[S5]** NASA, ["Lunar Surface
Technology"](https://www.nasa.gov/lunar-surface-technology/).

> NASA identifies ISRU, excavation, infrastructure construction, power,
> robotics, and autonomy as key lunar capabilities.

## Reporting and records of the 2026 developments

**[S6]** Reuters (via Yahoo Finance), March 14, 2026, "Musk says
Tesla's mega AI chip fab project to launch in seven days."

> Confirms the Terafab name, AI5 program, existing TSMC and Samsung
> partnerships, and earlier remarks about a possible Intel collaboration.

**[S7]** CBS News, March 23, 2026, "What is Elon Musk's Terafab chip
project?"

> Summarizes the Austin announcement and the stated purpose of supplying
> chips for vehicles, spacecraft, and Optimus robots.

**[S8]** Proactive Investors (via Yahoo Finance), March 2026, "Musk says
Tesla, SpaceX to build $20B Terafab chip plant in Texas."

> Reports the 2-nm target, terrestrial and space chip lines, and the stated
> 2028 mass-production goal.

**[S9]** CNBC, May 6, 2026, "Elon Musk's Terafab chip factory in Texas
could cost up to $119 billion, filing shows."

> Reports the filing-based cost ceiling, the roughly $3B research fab,
> SpaceX's lead role in the scaled phase, and public-offering preparations.

**[S10]** Teslarati and Electrek, March 22, 2026, launch coverage and
critical commentary.

> Together report the proposed venture structure, the SpaceX–xAI merger,
> D3 orbital chip line, wafer-start ambitions, the Optimus construction
> role, and skeptical assessments of feasibility. Later primary-source
> corrections in [S27] control where the reports conflict with the filing.

**[S11]** SpaceXAI, "Introducing Grok 4.5," July 2026, with
contemporaneous Axios coverage.

> Documents an in-house engineering-focused model trained in SpaceXAI data
> centers, its use in internal engineering work, and reporting on
> engineering data entering later training runs.

**[S12]** VentureBeat and Northflank, July 2026, coverage of Moonshot AI's
Kimi K3 release.

> Reports a 2.8-trillion-parameter open-weight model benchmarking near the
> proprietary frontier on agentic and coding tasks. Used as evidence of
> benchmark compression, not of an autonomous-R&D threshold.

**[S13]** Public statements and reporting, July 2026 (Teslarati, Yahoo
Tech, and contemporaneous posts on X), on SpaceX engineering data entering
a roughly two-trillion-parameter supplemental training run.

> Musk states that the engineering corpus, excluding ITAR-restricted
> material, will enter supplemental training of the next in-house model —
> the same broad mechanism previously used with acquired coding data.

**[S14]** *Connecting The Dots* video commentary, 2026, on Tesla's
internal engineering systems.

> Commentary-class source. Its integrated-systems core is corroborated by
> [S15–S17]; unconfirmed claims of a "Tesla One" brand and a specific
> manufacturing-CAD AI are excluded from the document's factual claims.

**[S15]** Jay Vijayan, on-record interviews and profiles (*The Neon Show*,
Indiaspora, and *Forbes India*).

> Tesla's first CIO describes building the custom Warp enterprise system
> in roughly four months in 2012 after rejecting off-the-shelf ERP, and its
> continuous extension thereafter.

**[S16]** Stack Overflow engineering blog, "Building the software that
helps build SpaceX," 2021, with corroborating former-engineer accounts.

> Documents SpaceX's internal Warp Drive enterprise and manufacturing
> systems.

**[S17]** Tesla AI Day presentations, 2021–2022.

> First-party documentation of fleet-learning infrastructure: an occupancy
> network trained on 1.4 billion fleet frames and auto-labeling replacing
> roughly five million hours of manual annotation. Later fleet-mile totals
> are company statements and are not converted into driverless-mile
> equivalents.

## Parameter literature

**[S18]** D. Jordan et al., "Compendium of Photovoltaic Degradation
Rates," *Progress in Photovoltaics* 24(7), 2016.

> Meta-study of more than 11,000 measured degradation rates; terrestrial
> crystalline-silicon median approximately 0.5–0.6% per year.

**[S19]** Peer-reviewed telemetry study of solar-array degradation across
eleven GEO satellites, *International Journal of Space Science and
Engineering*, 2018.

> Reported degradation ranges are approximately 0.44–1.03% per year for
> gallium-arsenide arrays and 0.71–1.69% for silicon arrays. This anchors
> one component class, not system-wide industrial depreciation.

**[S20]** Fraunhofer ISE, *Photovoltaics Report* (2026 update); Bhandari
et al., *Renewable and Sustainable Energy Reviews* 47, 2015.

> Energy-payback estimates of roughly 0.9–1.1 years in Europe and a
> harmonized 1.0–4.1-year range across technologies. These do not measure
> reproduction of the production system.

**[S21]** M. Hecht, J. Hoffman et al., MOXIE results, *Science Advances*,
2022; NASA NTRS carbothermal ISRU reports, 2024–2025.

> Oxygen produced on Mars at gram-per-hour scale at at least 98% purity;
> lunar oxygen extraction demonstrated at approximately 20% yield and TRL
> 5/6. Neither is a full-system closure demonstration.

**[S22]** Independent satellite tracking and reporting by J. McDowell,
Harvard-Smithsonian CfA, 2020–2026.

> Constellation deorbit and status statistics. Reported fractions near 3%
> for early generations fall below 0.5% for later ones, and the tracker
> separates early deorbit, uncontrolled decay, retirement, and disposal.
> Without cohort, observation interval, and satellite-years, these are
> fleet fractions rather than hazard rates.

## Closure-engineering literature

**[S23]** NASA, *Advanced Automation for Space Missions* (NASA CP-2255),
1980 NASA/ASEE summer study.

> Designs a proof-of-principle self-replicating lunar factory from a
> roughly 100-ton seed. It adopts a one-year **strawman** replication target
> whose component values it calls crude estimates; cites 90–96% closure
> from earlier studies of specific **nonreplicating** production
> applications; and places rigorous demonstration of complete parts closure
> outside its scope. These are design assumptions and plausibility
> arguments, not demonstrated performance.

**[S24]** R. A. Freitas Jr. and R. C. Merkle, *Kinematic
Self-Replicating Machines*, Landes Bioscience, 2004.

> Comprehensive survey of the design space for physical self-replicating
> systems.

## Economics and progress-rate literature

**[S25]** R. H. Coase, "The Nature of the Firm," *Economica* 4(16), 1937.

> Transaction-cost account of firm boundaries used in II.5's
> integration-versus-modularity analysis.

**[S26]** Epoch AI (Ho et al.), "Algorithmic Progress in Language Models,"
2024.

> Estimates that compute required for fixed language-model performance
> halves roughly every eight months. The resulting approximately
> threefold-per-year rate does not license extrapolation to autonomous
> research or physical productivity.

## Primary regulatory filing and model provenance

**[S27]** Space Exploration Technologies Corp.,
[Form S-1 registration statement, filed May 20,
2026](https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/0001628280-26-036936-index.htm),
SEC accession 0001628280-26-036936; and
[Rule 433 free-writing prospectus, filed June 4,
2026](https://www.sec.gov/Archives/edgar/data/1181412/000162828026040610/spacexfwp.htm),
SEC accession 0001628280-26-040610, with associated June 4 offering
materials; contemporaneous analysis by Electrek, *Tom's Hardware*,
*Forbes*, and KBTX.

> This document's primary corporate source. On Terafab it describes a
> general framework with Tesla; project timelines, milestones, and capital
> expenditures not yet determined; no binding obligation on Tesla or Intel;
> and a general warning that initiatives may not achieve commercial
> viability. It acknowledges a present chip-supply shortfall for orbital AI.
> The initiative list includes terrestrial and orbital AI compute,
> orbital data centers from as early as 2028, internal chip design and
> manufacture, lunar manufacturing and energy, in-orbit manufacturing,
> manufacturing on the Moon and Mars, asteroid mining, and
> "interplanetary industrialization." It also reports on the order of one
> thousand automated collision-avoidance maneuvers per day across the
> constellation in 2025. Page-level quotations remain to be pinned to a
> permanent archival copy.

**[S28]** Companion simulation program, [rsi-model
repository](https://github.com/fperegrinvs/rsi-model), r4.0 release
candidate on branch `main` with r3.5 retained as the frozen inherited
baseline; concept DOI `10.5281/zenodo.21619447`; Appendices C–D.

> Reproducibility source, not evidence. It computes consequences of stated
> assumptions and supports no empirical claim on its own authority. Each
> archived release tag mints a version-specific DOI.

## Corporate and orbital-compute record

**[S29]** Terafab official project site (`terafab.ai`), accessed July
2026.

> First-party messaging: combined logic, memory, and advanced packaging;
> Kardashev-scale framing; scaling figures of approximately one billion
> robots, ten million tonnes per year launched to orbit, and more than one
> terawatt of solar; AI5/AI6/D3 lines; an explicit Earth-versus-space cost
> decomposition; and lunar mass drivers as a next step. Marketing and
> recruiting material — evidence of declared intent, not commitment.

**[S30]** Waymo safety-impact disclosures, 2026.

> Cumulative fully driverless miles used as the comparison point in I.2 and
> Appendix A.3. No conversion to supervised autonomy miles is made.

**[S31]** Heavy-lift flight-test reporting, 2026.

> Cumulative count of thirteen test flights through mid-2026, used as a
> low-volume, high-information development proxy rather than a capacity or
> reliability input.

**[S32]** B. Agüera y Arcas, T. Beals, M. Biggs, J. V. Bloom,
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

**[S33]** *SpaceNews*, *Via Satellite*, and *Data Center Dynamics*
coverage of orbital-compute programs, 2025–2026.

> Reports the Google–Planet partnership, two prototype satellites slated
> for launch by early 2027, the research-stage status of the program, and
> at least one additional entrant flying an accelerator demonstrator.

**[S34]** Will Marshall, co-founder and CEO of Planet Labs, interviewed on
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

## External strategic cross-check

**[S35]** L. Aschenbrenner, *Situational Awareness: The Decade Ahead*,
June 2024, archived in `docs/sources/`.

> Analyst estimates used as external cross-checks: a trillion-dollar
> compute-cluster trajectory; power as the binding constraint with a
> politically conditional natural-gas floor; CoWoS/HBM as chip
> bottlenecks; a fast-takeoff thesis; and historical capital-mobilization
> reference classes. These claims affect priors and counterfactuals, not the
> evidence table's item-level assessment.

## Collective model-input and engineering sources

**[S36]** Assorted company disclosures, industry reporting, agency
guidance, price sheets, and technical literature used in Appendix A,
`params/anchors.yaml`, and the Part II budgets.

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
> No single permanent identifier covers the collection. Each anchor records
> its own source class and note, and auditable material is archived in
> `docs/sources/` or `docs/transcripts/` where available.

> **Bibliographic debt.** This collective entry is not a substitute for the
> claim-level bibliography required for an academic quantitative release.
> r4.0 retains it visibly rather than inventing precision: several endpoints
> still need exact author/organization, title, date, page/table/section,
> permanent URL or DOI, extracted value, and transformation. The code and
> outputs reproduce the chosen ranges; they do not by themselves validate
> those ranges against primary sources.

**[S37]** Space Exploration Technologies Corp., [European Union
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

**[S38]** Space Exploration Technologies Corp., [Starmind AI1 official
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

## Post-IPO orbital-compute calibration

**[S39]** S. G. Turyshev, ["Orbital Data Centers: Spacecraft Constraints
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

**[S40]** S. Gaalema, S. Indyk, and C. Staley, ["Reduced-Mass Orbital AI
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

**[S41]** K. van Berkel, ["The Cost and Network Limits of Space-Based AI
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

**[S42]** R. Eason, N. Bleier, M. Lembeck, and R. Kumar,
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

**[S43]** NASA Glenn Research Center, [NASA/TM—2005-213442, radiator mass
comparison](https://ntrs.nasa.gov/api/citations/20050238492/downloads/20050238492.pdf),
2005.

> Primary engineering reference separating radiator panels from the
> complete heat-transport and deployment system. ISS two-sided panels are
> reported at 2.75 kg/m² and 8.8 kg/m² after fluid loop and deployment
> mechanism; the JIMO analysis estimated 5 kg/m² for the complete system.
> At 353 K, 0.86 emissivity, and 173 K environment, the sizing example uses
> approximately 1.4 m²/kW. These are heritage/system cross-checks, not
> forecasts for an optimized AI1 radiator.

**[S44]** University of Virginia National Security Data Policy Institute,
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

## Lunar surface–orbit architecture and debris boundary

**[S45]** D. J. Kessler and B. G. Cour-Palais,
["Collision Frequency of Artificial Satellites: The Creation of a Debris
Belt"](https://doi.org/10.1029/JA083iA06p02637), *Journal of Geophysical
Research* 83(A6), 2637–2646, 1978.

> The original collision-feedback result: satellite collisions create
> orbiting fragments, each of which raises the probability of later
> collisions. It supplies the direction of the feedback, not a universal
> threshold for a particular future constellation.

**[S46]** N. R. Boone and R. A. Bettinger,
["Simulation of Debris Events in Selected Low Lunar
Orbits"](https://doi.org/10.1007/s40295-023-00382-y), *Journal of the
Astronautical Sciences* 70, 16 (2023).

> Approximately 97,000 simulated fragments across eight breakup cases show
> orbit-dependent debris evolution: some selected low lunar orbits retain
> long-lasting populations, while impacts on the Moon are geographically
> nonuniform. The reported one-year collision probabilities are low for the
> notional present cases; the paper does not establish a current lunar
> cascade.

**[S47]** NASA, ["Artemis Base Camp on the Moon Will Need Light, Water,
Elevation"](https://www.nasa.gov/humans-in-space/nasas-artemis-base-camp-on-the-moon-will-need-light-water-elevation/),
2021; NASA, ["Lunar Dust Mitigation: A Guide and Reference, First
Edition"](https://ntrs.nasa.gov/citations/20220018746), 2021; and NASA,
["Archway for Radiation and Micrometeorite Occurrence
Resistance"](https://ntrs.nasa.gov/citations/20130009378), 2013.

> Surface-architecture boundary references: south-polar illumination and
> access to shadowed volatile deposits; abrasive/electrostatic dust effects
> on radiators, mechanisms, and sensors; and local regolith as candidate bulk
> radiation and micrometeoroid shielding. None establishes reserve
> economics, continuous power at a selected site, or industrial closure.

**[S48]** D. C. Davis, F. S. Khoury, K. C. Howell, and D. J. Sweeney,
["Phase Control and Eclipse Avoidance in Near Rectilinear Halo
Orbits"](https://ntrs.nasa.gov/citations/20200000733), AAS Guidance,
Navigation and Control Conference, 2020.

> The Gateway reference NRHO is designed around eclipse avoidance, resonance,
> and low-cost stationkeeping with active phase control. It supports the
> gateway/service-layer role but does not make NRHO a passive, resource-bearing
> industrial site.

**[S49]** NASA, ["Basics of Space Flight: Planetary
Orbits"](https://science.nasa.gov/learn/basics-of-space-flight/chapter5-1/),
updated 2024.

> Defines a Sun-synchronous orbit as a planet-centered precessing orbit that
> preserves local solar time and distinguishes it from a heliocentric orbit
> around the Sun.

## Orbital-data-center regulatory record

**[S50]** Federal Communications Commission, Space Bureau,
["Space Bureau Accepts for Filing SpaceX's Application for Orbital Data
Centers"](https://docs.fcc.gov/public/attachments/DA-26-113A1.pdf),
Public Notice DA 26-113, released February 4, 2026; ICFS File No.
SAT-LOA-20260108-00016, Call Sign S00798, application filed January 30,
2026.

> The notice accepts for filing an application describing a non-geostationary
> system of up to one million satellites. Acceptance for filing begins
> public and regulatory review; it is not authorization to deploy or operate
> the proposed system.

## Fourth Edition bootstrap and material-source record

**[S51]** NASA Science,
["Moon Composition & Structure"](https://science.nasa.gov/moon/composition/),
updated July 23, 2026.

> NASA lists oxygen, silicon, magnesium, iron, calcium, and aluminum as the
> principal elements in lunar-crust minerals, with smaller titanium,
> uranium, thorium, potassium, and hydrogen, and distinguishes
> calcium/aluminum-rich highlands from iron/titanium-rich maria. This is a
> bulk-composition boundary, not a resource or reserve estimate.

**[S52]** Jennifer Edmonson and Doug Rickman,
["A Survey of Geologic Resources"](https://ntrs.nasa.gov/citations/20120015479),
NASA Technical Reports Server record 20120015479, 2012.

> The lunar-geology survey gives an average regolith bulk density of about
> 1.5 g/cm³ (1.5 t/m³), used only for the illustrative in-place inventory
> calculation in I.9. Density does not determine grade, recovery, or reserve
> economics.

**[S53]** P. G. Lucey, G. J. Taylor, and E. Malaret,
["Abundance and Distribution of Iron on the
Moon"](https://doi.org/10.1126/science.268.5214.1150),
*Science* 268(5214), 1150–1153, 1995.

> Near-global Clementine data produced an approximately 3 wt% iron estimate
> for the lunar highlands crust and approximately 7–8 wt% for lower-crustal
> material exposed by South Pole–Aitken. The 3% value is used as a
> conservative illustrative concentration, not a claim about a selected
> mining site.

**[S54]** C. B. Moore, C. F. Lewis, E. K. Gibson, and W. Nichiporuk,
["Total Carbon and Nitrogen Abundances in Lunar
Samples"](https://doi.org/10.1126/science.167.3918.495),
*Science* 167(3918), 495–497, 1970.

> Returned bulk fines in the reported samples contained carbon and nitrogen
> at roughly hundreds of parts per million, with mixtures of indigenous,
> meteoritic, and solar-wind contributions. The result establishes scarcity
> in those samples, not a global lunar resource map.

**[S55]** NASA Goddard Space Flight Center,
["NASA's LRO: Lunar Ice Deposits Are
Widespread"](https://science.nasa.gov/solar-system/moon/nasas-lro-lunar-ice-deposits-are-widespread/),
October 3, 2024.

> LRO analysis finds widespread evidence of water ice in permanently
> shadowed regions beyond the immediate south pole while explicitly stating
> that deposit volume and burial beneath dry regolith cannot yet be
> accurately determined. Occurrence is not a bankable reserve.

**[S56]** NASA Science,
["OSIRIS-REx Frequently Asked
Questions"](https://science.nasa.gov/mission/osiris-rex/osiris-rex-faq/),
accessed July 27, 2026.

> Laboratory analysis of returned Bennu material reports abundant organic
> molecules and sodium-rich minerals associated with evaporation of water.
> One carbonaceous sample demonstrates possible volatile and carbon-bearing
> diversity; it does not establish asteroid-mining yield or economics.

**[S57]** NASA,
["Lunar Surface Technology"](https://www.nasa.gov/lunar-surface-technology/),
accessed July 27, 2026.

> NASA describes Blue Alchemist's integrated autonomous processing of
> regolith simulant into silicon solar cells, aluminum wires, oxygen, iron,
> and slag; it also reports vacuum extraction of oxygen from simulant by a
> molten-regolith-electrolysis reactor. These are subsystem and prototype
> demonstrations, not autonomous lunar industrial closure.
