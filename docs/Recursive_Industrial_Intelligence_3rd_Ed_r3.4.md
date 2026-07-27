# Recursive Industrial Intelligence

## Third Edition, revision 3.4 · July 2026

*A self-sustaining, self-expanding space industrial system is coherent as an argument; whether it is feasible or economical is a question for models. This edition contains the argument and the executed models in one document.*

>> **Status.** Third Edition r3.4, assembled 2026-07-27. **Standalone:** this document carries the full argument and requires no prior edition; where earlier editions are mentioned, it is as intellectual history, not as a dependency. It incorporates the Second Edition's final correction pass (r2.11) in full. Every computed claim regenerates from the companion model repository [S28] via `scripts/run_baseline.py`, `run_part2.py`, and `run_deep.py` (35 tests); see Appendix C. Revision history in Appendix B.

## Scope and Status

This is a strategic hypothesis and research program with, now, its first
quantitative core — not a techno-economic demonstration. It identifies
necessary conditions, bottlenecks, and discriminating tests for a
self-expanding industrial system, computes what its own assumptions imply,
and states throughout which of its six propositions each conclusion rests on.

Six distinct propositions run through this document and carry different evidence: **(P1)** a recursively expanding industrial system is conceptually
possible — a respectable case is made; **(P2)** such a system might
eventually be technically feasible — quantitatively explored *for the
industrial substrate only* (Part I): outcomes span near-certain failure to
near-certain expansion across named assumption sets, with the feasibility
margin localized to one sector; feasibility of the complete coupled
intelligence–industry recursion remains unquantified, because the
intelligence and compute-production functions are still unspecified
(III.6); **(P3a)** orbital and lunar *compute during the Earth-dependent
bridge* would be economically competitive — now quantified (Part II) and,
at anchored values, *negative*, with crossover requiring a specific,
currently unanchored corner of parameter space; **(P3b)** a *mature,
high-closure* space-industrial ecology would eventually obtain a structural
economic advantage over terrestrial expansion — **unquantified**: Part II
prices the bridge architectures, not an ecology that manufactures its own
power systems, radiators, structures, and replacement hardware off Earth,
so nothing in this document establishes or refutes P3b (quantifying it
requires coupling the Part I production model into the Part II cost model —
the Fourth Edition's stated frontier); **(P4a)** the companies are deliberately integrating launch, communications, AI, terrestrial and orbital compute, chip design and manufacture, and prospective off-world energy and manufacturing — substantially documented, since the S-1 itself names orbital compute, lunar manufacturing and energy, in-orbit manufacturing, manufacturing on the Moon and Mars, asteroid mining, and "interplanetary industrialization" among its initiatives [S27]; and **(P4b)** that this integration is intended to produce recursive industrial closure — inferential, with no closure program, seed bill of materials, reproduction metric, or minimum-cut roadmap published, and assessed against competing explanations (Part III). The split matters: the two halves carry materially different evidential status, and earlier editions conflated them. Conclusions are licensed by the strongest proposition they rest on, not by the conjunction of all six.

**Evidential classes.** Documented statements; announced initiatives;
technically grounded pathways; inferred strategy; speculative closure — as
in the Second Edition — plus one new rung: **computed**, meaning derived
mechanically from stated assumptions by the companion model (public release pending, Appendix C). A computed result
inherits the epistemic class of its weakest input; structural coefficients
are ASSUMPTION-class throughout, so no computed result is a measurement.
Every computed number below carries its assumption-set label
(conservative / central / optimistic); a result quoted without its set
label is a misquotation.

## Executive Summary

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

This edition prices the passage. Three headline results:

1. **Electronics dominates the lunar and Mars architectures; LEO is
   primarily feedstock- and recovery-constrained** (computed;
   ASSUMPTION-class structure). Pooling allocation steps across sampled
   runs, the worst-case-sector constraint binds on electronics in 80–98%
   of steps on the lunar surface and Mars, while in LEO — which has no ore
   body — mining binds in ~60–70% of steps with electronics second.
   Under the assumed electronics-closure range, electronics is also the
   principal *import cut* where imports bind at all: cutting that line
   alone is fatal in roughly 9% of otherwise-viable central-assumption
   lunar runs and roughly 75% of Mars runs, while in LEO no single import
   line was fatal in any sampled draw — recovered mass substitutes for
   lost feed there, at the price of making the recycling *sector* itself
   indispensable. The clock-setting logic of the depreciation analysis is
   exhibited, not just asserted — and the model names the binding
   dependency per architecture.   The two dominant unanchored numbers in this document are the fraction of electronics output producible off-world (the vitamin gap, sampled 0.10–0.30) and the space logistics penalty — the displayed sensitivity ranking (I.8) supports exactly that pair, within its stated scope — and the reader should hold the circularity in view: that the binding sector is electronics is substantially *entailed* by sampling that gap low, so the finding's force lies in the conditional structure it exposes (which sector, which cut, which location ranks) rather than in the identity of the sector, which follows from an assumption.
2. **System replication time is an output, and it is set-dependent**
   (computed; all shares are frequencies across the stipulated assumption
   ensemble and shock process, not empirical probabilities; denominators
   stated per I.8). Under central assumptions on the lunar surface,
   survivor-conditioned doubling is ~4.5 years — but only 59% of sampled
   runs are still expanding at year 30, and **39% doubled and then lost
   viability**: early growth rides an import ramp that decays faster than
   the electronics tier closes, so transient doubling is cheap and durable
   expansion is the contested outcome. Conservative-set runs mostly fail —
   roughly 11%, 9%, and 24% of sampled runs expanding at year 30 in LEO,
   lunar, and Mars (in two of those cells without ever doubling). Among
   optimistic-set runs, survivor-conditioned doubling is approximately
   three years on the Moon, five on Mars, and six in LEO. No single
   replication time survives the sweep or its denominators — the Second
   Edition's refusal to quote one is vindicated twice over.
3. **The space-compute crossover is not a launch-price story** (computed;
   anchored ranges; P3a only). At published launch prices, orbital compute
   costs 5–9× a terrestrial alternative that responds (lunar surface
   ~300×), and **0 of 2,000 sampled runs favored space** in any reference
   case (95% upper bound ≈ 0.15% under this ensemble — not literal zero).
   Break-even launch prices are frequently *negative*: the
   space-qualification premium, equipment life, and utilization dominate,
   not launch. Published claims of a $200–300/kg crossover reproduce
   inside this model only under COTS qualification, ~7-year life, and
   ~0.95 utilization simultaneously — so the public disagreement is three
   numbers. The strongest current radiation data supports five-year TID
   survivability for the tested accelerator with margin; what it does not
   establish is seven-year *system* reliability (single-event effects,
   training workloads, thermal, whole-spacecraft), which is where the
   long-life corner remains open.

The strategic assessment (Part III): the evidence **substantially
establishes deliberate integrated space–AI–industrial development (P4a)**
at the level of declared direction and early implementation — the S-1's
own initiative list and the first-party messaging are difficult to explain
under a purely terrestrial reading. It **does not establish recursive
closure as the objective (P4b)**: the closure-specific observables — seed
bills of materials, reproduction metrics, minimum-cut roadmaps, locally
reproducible production equipment — remain absent. What has changed is
that the discriminating indicators are now *model-ranked*: the rational
next moves of a closure-seeking actor — electronics-closure engineering,
loss-tolerant orbital-compute persistence, materials-recovery recycling —
are exactly the observations the models identify as informative.

---

# Part I — Technical Feasibility

## I.1 Recursive self-improvement: the digital loop

Recursive self-improvement (RSI) occurs when an intelligent system
contributes to the process that produces a more capable successor. The
useful unit is not a public model release but a verified improvement loop:
identify a weakness, propose a change, run an experiment, evaluate, deploy,
and use the improved system to accelerate the next cycle.

    I(t+1) = I(t) + ΔI(t),        ΔI = L × G

I is effective intelligence; L is the number of useful loops completed; G
is the average gain per successful loop. The loop rate is constrained by
the least scalable part of the development system:

    L = min{ L_C(C), L_D(D), L_X(X), L_V(V), L_R(R) }

— each conversion function turning its resource (compute, data,
experimental throughput, verification capacity, deployment reliability)
into verified loops per unit time. Efficiency is partly a function of
intelligence, E(t) = f(I(t)), and the form of f — logarithmic, linear,
superlinear, saturating — is unknown; a rigorous analysis identifies which
regime observed loop completion supports rather than assuming takeoff.
Public releases are lagging indicators; the strategically relevant measure
is verified improvement loops per calendar time. The verification term V
recurs in a second role as the governing safety constraint (Part III.4).

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

The loops couple through a second channel: **data as the exhaust of the
physical loop**. Operating physical industry generates data that exists
nowhere else — test telemetry, process parameters, failure archives, fleet traces. It commoditises less readily than public text, for four reasons: negative
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

## I.3 Why space changes the cost structure

On Earth, useful locations compete with communities, ecosystems,
jurisdictions, and alternative uses. Off Earth, the monetary price of
unused area approaches zero — but infrastructure does not become free; the
cost *changes kind*, from purchasing scarce terrestrial sites and
coordinating human institutions toward transporting, converting, and
maintaining matter through an automated production network:

    Earth: land + permits + construction + energy + materials + labor + coordination
    Space: transport + energy + extraction + refining + manufacturing + maintenance + coordination

The standard external objections — station-keeping, collision management,
imported mass, maintenance, coordination — become *internal product
categories* once the complex can manufacture the required systems:
propellant lines, tracking and maneuver capability, local extraction and
recycling, inspection robots and modular spares, compute and communications.
The crucial question is never whether these requirements exist but whether
the complex can reproduce the industries that satisfy them faster than the
system depreciates.

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

    dH/dt = [r − δ] H

Every claim ultimately reduces to whether gross replication r exceeds
depreciation δ. Terrestrial industry operates inside an ambient repair economy; space assets have none of it. Published measurements constrain a few component classes without bounding the depreciation of an autonomous industrial ecology. GEO solar arrays degrade 0.4–1.7%/yr [S19], overlapping a terrestrial PV median of 0.5–0.6%/yr at the low end and reaching several times it at the high end [S18] — one component class, silent about bearings, seals, lubricated mechanisms, batteries, machine tools, robots, radiators, dust-exposed joints, and optical metrology. Constellation figures are cohort-dependent: reported early-generation failure fractions near 3% fall below 0.5% for later generations, the underlying tracker separates early deorbit, uncontrolled decay, retirement, and disposal, and a fleet fraction without a cohort definition, observation interval, and satellite-years is not a hazard rate [S22]. Large-training-run figures near one interruption per two thousand accelerator-days mix permanent component failures with recoverable host, network, and software events, most automatically recovered: a **cluster interruption frequency**, not a component hazard rate. The space penalty is not faster wear — it is the five-to-fifteen-year
no-repair design envelope, the internality of every repair chain, and
discrete loss without salvage. Meanwhile the most advanced terrestrial capital — fab tools on 2–5-year schedules, accelerators retired within 3–6 years — is written off faster than a space solar array physically degrades, because obsolescence sets the terrestrial clock. Five quantities must be kept apart, since compressing them was an internal inconsistency of earlier revisions: **physical degradation**, **functional failure**, **accounting depreciation**, **economic obsolescence**, and **frontier-equivalent capacity loss**. The last two are not physical — an accelerator does not vanish because a better one exists — so obsolescence enters a growth equation only where H is measured in quality-adjusted or frontier-equivalent capacity, which is why the terrestrial paradox above is a statement about accounting and frontier equivalence rather than about matter. The corrected form, decomposed per environment,

    δ_total = δ_wear + δ_catastrophic + δ_obsolescence + δ_logistics

is what the model implements per sector and per location: space raises the
catastrophic and logistics terms, Earth raises the obsolescence term, wear
differs modestly. The environment drives δ upward through radiation,
thermal cycling, micrometeoroids and debris, vacuum effects, regolith dust,
and the absence of an ambient repair economy.

One environment-specific case partly cuts the other way, and it is narrower than earlier drafts of this argument claimed. For **short-lived compute payloads in very low orbit**, aligning useful life with accelerator-obsolescence cycles reduces the economic value of repair: hardware retired within a few years regardless costs less to be unable to fix. The qualifications are substantial. Natural decay depends on altitude, ballistic coefficient, and solar activity — small spacecraft near 400 km can decay within five years, but beyond 500 km five-year decay is not assured and some objects persist for decades. The leading published orbital-compute architecture in fact places its cluster near **650 km** in dawn-dusk sun-synchronous orbit, chosen for illumination rather than disposal [S32], so the concession does not describe that design. Nor is disposal free: station-keeping, collision avoidance (large-constellation operators report on the order of a thousand automated avoidance manoeuvres per day [S27]), replacement launch, network spares, and residual capital loss all remain — and the same source that calls orbital repair impracticable proposes redundant provisioning instead, which is a cost, not its absence [S32]. The concession therefore covers some payload classes in very low orbit and does not generalize: mines, refineries, machine tools, and robots must last decades to close a loop. In this edition's models it lands in Part II (compute payloads), while Part I's industrial δ decomposition stands.

**The clock-setting component.** In any partially closed system, the
component with the shortest replacement horizon that cannot yet be produced
or stockpiled locally sets a hard clock on the entire complex. Closure
priority follows failure rate × non-replaceability, not mass fraction.    Viability: T_replenish,j < T_effective-survival,j for every critical component class j

Effective survival includes installed redundancy, spare inventory, repair probability, and substitution — not time to first failure; the naive form ignored inventories, cannibalisation, and stockpiling, all of which the model carries explicitly. Part I.7 enforces the condition by construction, and Part I.8 identifies the clock-setting sector by computation.

## I.5 Industrial closure: the decisive threshold

Self-sustaining (P ≥ D: replacing what is consumed and lost) and
self-expanding (P > D: net additional capacity) are different milestones.
Industrial closure measures how much of the critical input set is produced
inside the network:

    κ = critical inputs produced internally / total critical inputs required

The scalar form is vocabulary, not measure: a system supplying 99.9% of its
mass locally has effectively zero autonomous closure if the residual 0.1%
contains irreplaceable electronics. The proper object is a vector —
κ = (κ_power, κ_mining, κ_refining, κ_robotics, κ_machine-tools,
κ_electronics, κ_thermal, κ_transport) — with minimum cut sets: the
smallest combinations of imported inputs whose loss collapses the network.
The clock-setting component is the scalar shadow of this vector structure.
The hardest closure problem is the deep technological stack — precision
metrology, advanced electronics, semiconductor fabrication, and the
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
infrastructure and transports a compact industrial seed — power,
extraction, refining, manufacturing, robots, compute, repair capability,
and initial spares — viable only if it grows its productive base before
critical imported components fail. A credible design requires redundancy,
recycling, buffers, and an explicit path for every nonlocal dependency.
That sentence, made operational, is the model of I.7: the spares are a
shelf-life-limited stockpile state; the nonlocal dependencies are import
lines that can be cut; the "explicit path" is the requirement matrix.

## I.6 Intelligence, coordination, and time

A sufficiently capable AI converts much of organizational coordination from
human management into a computational service — scheduling, allocation,
routing, diagnosis, redesign, bottleneck selection. Coordination cannot
reach zero: sensing, propagation latency, verification, and contention set
a physical information floor. After high closure the central allocation
question changes from "can the system obtain land, permits, workers,
components?" to "how much productive throughput should be assigned, and
when will output be complete?" — scarcity becomes latency, and the
accounting unit shifts toward joules, kilograms, machine-hours, and
completion time. In the mature regime, growth is bottleneck-limited:

    dH/dt = [r(I, E, M) − δ] H

with intelligence accelerating growth by detecting and expanding the active
bottleneck. The model below implements exactly this: the allocation LP *is*
the coordination service, and the binding sector it reports each step *is*
the active bottleneck.

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
  ASSUMPTION entries elsewhere, each resolved value carrying a provenance
  record into the generated reports.
- **The allocation step**: a lexicographic linear program maximizing the
  worst-case sector growth rate g over builds, wear-repair, recycling
  activity, and stockpile drawdown — the self-expansion criterion
  implemented exactly — then, holding g at its optimum, minimizing
  drawdown: stock is a buffer, not fuel.
- **Vitamin-part stockpiles** with shelf life (electronics-class parts
  decay in storage), per-sector import cutoffs, Mars synodic pulse
  deliveries, and Poisson common-cause shocks hitting correlated sector
  groups (dust storms, solar storms, common design faults).
- **Three reference architectures**: LEO (no ore body — feed imported or
  recycled from on-orbit mass), lunar surface (regolith feed, abrasive
  dust, no magnetosphere), Mars (deepest logistics penalty, ~26-month
  synodic resupply pulses, dust storms).

**The vitamin gap.** One structural parameter dominates all results: the
fraction of the electronics sector's output mix producible off-world
(sampled 0.10–0.30; ASSUMPTION with a documented bounding argument —
advanced-node logic and memory are not locally closable in this scenario
class; boards, passives, and power electronics plausibly are). No published
measurement exists. Anchoring it is the highest-value observation this
program could acquire.

## I.8 Results

Monte Carlo over anchored ranges with common-cause shocks (n = 400 sampled
runs per cell; one shared draw per anchor per run, correlating parameter
uncertainty across sectors; doubling time is an output). Two definitions,
because the columns use different denominators: the *expanding* column is
the share of **runs** with positive worst-case growth at year 30, reported
with its count and 95% Wilson interval; the *binds most* column is the
share of **allocation steps, pooled across all runs**, at which each
sector's material balance was the binding constraint. The doubling columns
use two denominators, stated explicitly because they answer different
questions: *ever doubled* is the first-passage time to 2x total capacity
among all runs that ever reach it within 35 yr (transient growth
capacity); *survivor-conditioned* restricts to runs also expanding at year
30 (durable replication performance). The difference between the two
counts is a distinct outcome class — runs that doubled early and then lost
viability — reported per cell. All shares are frequencies across this
stipulated assumption ensemble and shock process — not empirical
probabilities of real-world success (machine-readable table:
`outputs/tables/mc_deep.csv`):

| set | env | expanding runs (share, 95% CI) | ever doubled: n, median (IQR) | survivor-doubled: n, median (IQR) | doubled-then-failed | binds most |
|---|---|---|---|---|---|---|
| conservative | LEO | 44/400 (0.11, 0.08–0.14) | 0 | 0 | 0 | mining 71%, electronics 29% |
| conservative | lunar | 34/400 (0.09, 0.06–0.12) | 81, 9.2 (7.8–10.8) | 34, 7.8 (7.2–8.7) | 47 | electronics 81% |
| conservative | Mars | 95/400 (0.24, 0.20–0.28) | 0 | 0 | 0 | electronics 86% |
| central | LEO | 360/400 (0.90, 0.87–0.93) | 367, 16.2 (14.8–17.8) | 358, 16.2 (14.8–17.8) | 9 | mining 64%, electronics 36% |
| central | lunar | 234/400 (0.59, 0.54–0.63) | 389, 5.0 (4.2–6.0) | 234, 4.5 (4.0–5.0) | **155** | electronics 97% |
| central | Mars | 260/400 (0.65, 0.60–0.70) | 122, 9.2 (7.3–11.2) | 98, 9.1 (7.1–11.0) | 24 | electronics 89% |
| optimistic | LEO | 400/400 (1.00, 0.99–1.00) | 400, 6.2 (6.0–6.5) | 400, 6.2 (6.0–6.5) | 0 | mining 61%, electronics 39% |
| optimistic | lunar | 395/400 (0.99, 0.97–0.99) | 400, 3.0 (2.8–3.2) | 395, 3.0 (2.8–3.2) | 5 | electronics 98% |
| optimistic | Mars | 360/400 (0.90, 0.87–0.93) | 380, 5.1 (4.8–6.8) | 347, 5.0 (4.8–6.8) | 33 | electronics 91% |

Reading: conservative-set runs mostly fail — nine to twenty-four percent
of sampled runs still expand, so the failure is statistical, not
categorical (and in conservative LEO and Mars, expansion happens without
ever doubling: a slow crawl above zero); the central set is genuinely
marginal, with survival declining steadily as shocks and import decay
accumulate; the optimistic set expands in nearly all sampled runs (a
400/400 cell carries a Wilson lower bound of 0.99, not certainty). The
doubled-then-failed column is a result in its own right: **39% of central
lunar runs (155/400) doubled — median 5 years — and then lost viability**,
the import-ramp trap in which early growth rides Earth supply that decays
faster than the electronics tier closes. Transient doubling is cheap;
durable expansion is the contested outcome, which is why no doubling time
is quoted without its denominator. The central ensemble is architecture-dependent — high-frequency but slow expansion in LEO, materially more marginal survival on the Moon and Mars — and one pairing looks inverted and is not: central LEO expands more often than central lunar (0.90 vs 0.59) yet doubles three times slower (16.2 vs 4.5 yr survivor-conditioned median). The two architectures fail differently. LEO has no ore body, so growth is throttled by recovered-mass feed — slow but robust, and the binding constraint is split between mining and electronics. A mass-accounting caveat governs every LEO result: recycling yields are below unity (recovery 0.40 of retiring capacity), so recycling alone cannot fund net expansion; the balance comes from imports and from a capture feed (mining at 5% productivity) drawing on a finite orbital-matter reservoir the model does not deplete. The LEO architecture as modeled is therefore an *import-supported orbital recycling network*, and its expansion results are conditional on continued feed availability; an explicit embodied-mass conservation state is Fourth Edition work. The lunar surface has regolith feed and can grow fast when electronics permits, but almost everything binds on electronics (97%), so its survival is hostage to a single cut. Robustness and speed are governed by different sectors; conflating them is what produces the apparent paradox. The
spread *is* the result: feasibility is not closed by current evidence, and
the model shows which numbers close it.

**Cut sets and the ensemble-frequent minimum cut.** At central anchor values no
import cut set is fatal by year 30 anywhere — imports accelerate but are
not load-bearing *at central values*. That statement misleads alone,
because cuts appear near the feasibility margin. Over sampled anchors
(n = 40 draws per cell), conditional on an otherwise-expanding draw: the
electronics import line alone is fatal in roughly 9% of central lunar
draws — and cutting *all* import lines is no worse, i.e. electronics *is*
the minimum cut there — and in **75%** of central Mars draws, where the
synodic pulse and the deepest vitamin gap compound. In central LEO no
single import cut was fatal in any sampled draw: the recycling loop
substitutes for lost feed, which converts the import dependency into a
capacity dependency (below). Under the optimistic set the lunar figure
falls to ~5%. These are small-count frequencies (a 9% cell is three of
thirty-four viable draws) and carry wide intervals. Capacity knockouts:
every physical sector is indispensable in every location (knockout
unrecoverable); repair is dispensable where an import line backs it;
**recycling is indispensable in LEO and only in LEO** — the no-ore-body
architecture lives on recovered mass, which is exactly why its import
lines are individually expendable.

**The clock-setting curve.** Expansion frequency against the e-folding
time of Earth-supply withdrawal (n = 60 per grid point): on the lunar
surface under central assumptions, ~0.83 at a 25-year ramp-down falling to
~0.4–0.6 below ten years (the non-monotonic wobble at intermediate ramps
is within binomial noise at this n). The penalty for withdrawing the
umbilical faster than the closure ramp is real and quantifiable, and its
steepness is set by the electronics stockpile shelf life — not by any
aggregate quantity.

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
— 22/30 vs 22/30 sampled runs expanding on the lunar surface, 28/30 vs
28/30 in LEO, with matching limiting-sector shares — because the maximin
criterion already directs each step's investment at the worst-off sector,
which is the future bottleneck. A third policy, maximizing aggregate
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

**Global sensitivity, displayed — with its scope stated.** The claim that
the vitamin gap and logistics penalty dominate is a computation, not an
assertion, and it is a *scoped* one — central assumptions, lunar
architecture, shocks off, scalar anchors only; it does not rank structural
requirement-matrix uncertainty, policy choices, shock distributions, or
interaction effects, and repeating it across environments and sets with
interaction-capable methods is Fourth Edition work:
Spearman rank correlation between each anchor's shared draw and the
worst-case growth rate at year 30 across the ensemble (n = 300, central/
lunar, shocks off; anchors are drawn independently, so per-anchor rank
correlation needs no independence corrections beyond the null band of
roughly ±0.11, wider under multiplicity). Two parameters tower above the
band: the space-electronics closure fraction (ρ ≈ +0.78) and the space
logistics penalty (ρ ≈ −0.57) — both ASSUMPTION-class, which is the
epistemic point: the model's outcome uncertainty is dominated by exactly
the two numbers no one has measured. Every other anchor sits at or near
the null band. (`montecarlo.sensitivity`; ranked table in
`outputs/report_deep.md`.)

**What Part I establishes and does not.** It establishes structure: which
sector binds, what the minimum cut is, how locations rank (lunar most
robust per unit of assumption-optimism; LEO feed-constrained but
recycling-viable; Mars most path-dependent and import-fragile), and where
the feasibility margin lies — structure that survives the allocation-policy
variation above. It does not establish point feasibility: the requirement
matrix, vitamin gap, repair efficiencies, stockpile sizes, and shock rates
are ASSUMPTION-class, and solar-array or satellite data do not establish
the depreciation behavior of mines, bearings, machine tools, or
dust-exposed radiators.

## I.9 Development path, annotated

Stage 1 Earth-dependent operations → Stage 2 local resource
supplementation → Stage 3 heavy-industry closure → Stage 4 advanced
manufacturing closure → Stage 5 self-sustenance → Stage 6 self-expansion →
Stage 7 intelligence-industry recursion. Terafab is best read as a
terrestrial rehearsal of Stage 4 (Part III.2). The model adds stage
warnings: the Stage 4→5 transition is where the vitamin gap binds — no
amount of Stage 3 bulk closure substitutes for an electronics tier — and
Stage 5 is location-dependent: LEO cannot pass it without
materials-recovery recycling; Mars cannot pass it without either
electronics stockpiles engineered to synodic shelf-life or a local
electronics tier; the lunar surface has the widest viable corridor.

## I.10 Binding bottlenecks and failure modes

With model annotations: **lithography and fabrication equipment** (the named residual chokepoint one layer below
foundries — and the deepest single closure problem in this framework);
**reliability and repair** (the model makes mean-time-to-repair and spares
closure first-class: repair is an explicit sector with an efficiency and a
spares bill); **thermal management** (radiators are launched mass — Part
II's radiator axis); **energy storage and continuity** (the lunar night
storage mass term; Mars dust-storm shocks); **resource quality** (LEO has
none — hence recycling's indispensability there); **verification and
control** (Part III.4); **political and legal environment**; **economic
survival of the transition** (Part II.1); **concentrated coordination**
(single points of failure a distributed competitor lacks);
**paradigm-shift stranding** (Part IV.3 — exposure concentrated in the
fabrication layer; the fleet self-insures through its own 3–6-year
depreciation).

---

# Part II — Comparative Economics

## II.1 The bridge economy

Each stage of the recursion must be independently profitable or deliberately
financed: a staircase of self-supporting steps, not a single leap to
closure. The plausible treads, in order: terrestrial products of the same
machinery (vehicles, storage, robots — the ground floor pays rent); launch
and connectivity (Starlink revenue and launch services fund transport);
orbital compute services — a candidate tread, *now priced rather than
merely doubted* (II.2–II.4); and in-space industrial services at higher
closure. The test of the staircase: at every stage, revenue plus strategic
financing must exceed the burn required to reach the next stage before the
clock-setting components of Part I.4 expire — and Part I.8 makes the clock
concrete: the electronics stockpile shelf life against the import ramp.

## II.2 The crossover model

Unit: **dollars per frontier-equivalent kilowatt-year of delivered IT
load** — defined as one kilowatt-year of IT electrical load powering
accelerators of frontier-generation efficiency, delivered at the case's
utilization; older-node capacity is converted by its J/FLOP penalty, so a
frontier-equivalent kilowatt-year buys the same computational output
regardless of which hardware generation supplies it.
Three reference cases: a LEO inference service; high-orbit/cislunar batch
compute; lunar-surface compute on locally manufactured power. Mass and
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

The terrestrial counterfactual **responds** — the epistemic requirement
earlier editions missed. Three scenarios: *tight* prices scarcity (the
politics-binds branch: permitting and climate commitments hold); *base*
takes the anchors; *responsive* prices induced supply at the cheapest
permitted firm-power floor — nuclear PPA, or the politically conditional
natural-gas floor at $0.04–0.06/kWh (CCGT under $1,000/kW, ~2-year builds
[S35]) — with an older-node hardware option taken when it wins on
compute-normalized cost. Aspirational launch targets are sweep axes only,
never inputs. Two financing caveats are deliberate modeling choices,
stated openly: a single WACC range (8–15%) applies to *both* sides —
equalized financing is an assumption in favor of space, since an
unprecedented orbital constellation would not price like a mature
terrestrial data center — and the qualification multiplier, service life,
and utilization are sampled independently, although the favorable corner
(cheap qualification, long life, high utilization) likely involves
correlated engineering assumptions; both refinements are queued (ROADMAP).
Calibration: the Earth base case works out to ≈$1.7/kW-hr, matching
published accelerator rental rates.

**Cost accounting — included and excluded.** Included: IT hardware with
qualification premium; PV, radiators, storage, structure and their launched
mass (with cislunar/lunar delivery multipliers); capital recovery at WACC
over service life (which amortizes replacement); an operations fraction
(2–6% of capex/yr) standing in for ground segment, downlink, and
station-keeping; utilization derating; Earth-side DC capex, PUE, and
firm-power floors. Excluded: development and non-recurring engineering,
launch failure and insurance, redundant provisioning beyond the life
derating, collision-avoidance operations beyond the ops fraction, spectrum
and regulatory costs, deorbit/disposal, residual value, and tax treatment —
all of which burden the space side more than the Earth side, so the
exclusions make the reported negative result *conservative in space's
favor*, not against it.

## II.3 Results

Central anchor values ($ per kW-yr, rounded to three significant figures —
these are assumption-conditioned outputs, not measurements; exact
machine-readable values regenerate in `outputs/`):

| case | LCO | launched mass | vs Earth base (≈14,700) |
|---|---|---|---|
| LEO inference | ≈72,000 | ≈46 kg/kW | 4.9× |
| cislunar batch | ≈128,000 | ≈46 kg/kW | 8.7× |
| lunar surface | ≈5.1 million | ≈450 kg/kW | ≈345× |
| Earth tight | ≈16,000 | — | — |
| Earth responsive | ≈12,800 | — | — |

Monte Carlo over anchored ranges, shared draws both sides (n = 2,000
sampled runs per row; frequencies under this ensemble, not empirical
probabilities):

| case | vs Earth | ratio p10/p50/p90 | space-cheaper runs | break-even $/kg p50 (p90) |
|---|---|---|---|---|
| LEO inference | base | 3.2 / 5.3 / 8.5 | 0 / 2,000 | −628 (−74) |
| LEO inference | responsive | 3.8 / 6.4 / 10.6 | 0 / 2,000 | −746 (−224) |
| cislunar batch | base | 5.4 / 9.4 / 16.4 | 0 / 2,000 | −167 (27) |
| cislunar batch | responsive | 6.4 / 11.2 / 19.6 | 0 / 2,000 | −221 (−37) |
| lunar surface | base | 140.6 / 347.5 / 833.9 | 0 / 2,000 | −11 (−5) |
| lunar surface | responsive | 184.6 / 433.8 / 1051.3 | 0 / 2,000 | −13 (−5) |

Zero observed successes in 2,000 draws bounds the ensemble frequency below
≈0.15% (95%) — a statement about this assumption ensemble, not about the
world.

A negative break-even means fixed, non-launch costs alone exceed the Earth
cost: at those draws no launch price, even zero, closes the gap. The
structural finding: **the crossover is gated by the space-qualification
premium, equipment life, and utilization — not launch price.** The
crossover surface (launch $/kg × life × qualification × radiator × closure
× chip efficiency) shows no ratio-below-1 region at published prices on
any axis, and near-parity only at target-class prices combined with
favorable values on at least two other axes. Lunar closure is the weakest
lever: chips are never closed, so even 95% closure of non-chip mass leaves
the lunar case two orders of magnitude from parity at published prices.

The mass-multiplier refinement: at anchored values a 2× FLOPS/W advantage
buys only ~two-thirds of the benefit of halving launch price (ratio 4.7 vs
3.8 at $3,000/kg), because the hardware term — untouched by efficiency —
dominates both mass and capex. "The compute tax outweighs the launch tax"
[S34] becomes true only after the qualification premium and hardware $/kW
fall; near-term, both taxes are subordinate to qualification and life.

## II.4 External claim checks

Two public claims of an orbital-compute crossover are checked here. Both are recorded as comparison targets (never inputs), and both *reproduce inside the model* under identifiable conditions — which converts a public disagreement into a localized, testable one. One preliminary correction of the record, because this document earlier mis-stated it: the Suncatcher design study does **not** claim system-level parity. Its cost section states twice that it is not a full economic analysis and not a comprehensive economic feasibility study, and its comparison sets the **amortised launch component alone** (≈$810/kW-yr for a Starlink-v2-class mass-to-power ratio at $200/kg; $810–7,500 across satellite classes) beside terrestrial data-centre **electricity spend** (≈$570–3,000/kW-yr), explicitly excluding infrastructure, building, and chip costs [S32]. That is a launch-cost feasibility marker — the finding that launch need not remain independently prohibitive — not a parity claim, and it is consistent with this model, which reproduces launch as a minor term. The crossover claim this model contradicts is the stronger reading in circulation [S34], not the study's own.

- **The Google/Planet study** (reported: crossover at $200–300/kg [S34]).
  At $250/kg with central anchors: space/Earth = 2.16 — no crossover.
  Under the favorable corner *within anchored ranges* (qualification ×1.2,
  7-year life, 0.95 utilization, 3 kg/kW radiators): **0.93** — the claim
  exactly. The dispute is three numbers, none of them launch price.
- **The Suncatcher design study** [S32]: an 81-satellite dawn-dusk sun-synchronous cluster near 650 km, terabit-class optical links (an 800 Gbps unidirectional bench demonstration against a stated ~10 Tbps per-link requirement), and a learning-curve projection of ≲$200/kg by the mid-2030s — itself conditional on roughly 370,000 tonnes of additional cumulative mass launched, on the order of 1,800 Starship-class flights averaging ~180 per year, which the authors call ambitious. Its engineering results should be read precisely (arXiv v2, 17 June 2026): HBM was the most **TID**-sensitive subsystem (irregularities from ~2 krad(Si) against a ~750 rad(Si) shielded five-year requirement, no hard total-dose failures to 15 krad(Si)), while core logic and on-chip SRAM were the most **SEE**-sensitive; the reported inference error probability is roughly one per three million inferences under the stated assumptions, with the effect on **training** explicitly reserved. At ~150 rad(Si)/yr, a seven-year dose (~1.05 krad) sits below the ~2 krad irregularity onset — so the radiation results support five-year TID survivability with margin and *do not obviously contradict seven-year TID survival*. What they do not establish is seven-year **system** reliability: SEE-induced corruption, host interruptions, training sensitivity, thermal management, and whole-spacecraft failure remain unresolved, with orbital repair called impracticable and redundant provisioning proposed instead — a cost, not an absence of one. The COTS practice supporting a low qualification premium (unmodified accelerators flying on imaging satellites [S34]) demonstrates cheapness, not five-year reliability.

Consequence for the staircase, stated within the model's service
definition: **the modeled orbital architectures are not cost-competitive as
substitutes for terrestrial frontier compute at the stated assumptions.**
This does not price differentiated orbital products (in-orbit sensor
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
depreciation runs at its worst (II.3's 5–9×) — so the declining-cost
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
| Intelligence | xAI (within SpaceX) | AI research, large-scale compute | design, coordination, recursive digital improvement |
| Energy | Tesla Energy | generation, storage, power electronics | power for compute, factories, robots |
| Robotic labor | Optimus | manipulation, maintenance; stated Terafab construction role | manufactured labor capacity |
| Manufacturing | Tesla | high-volume factories, batteries, motors | factory design, machine production at scale |
| Fabrication | Terafab (Tesla, SpaceX, xAI; Intel from Apr 2026) | declared: chip design, lithography operation, fabrication, memory, packaging [S6–S10, S27, S29] | declared compute-substrate layer; framework stage |
| Transport | SpaceX / Starship | reusable heavy lift | seed deployment, materials movement |
| Communications | Starlink | distributed connectivity | coordination across remote nodes |
| Compute deployment | planned D3 constellation | radiation-tolerant silicon | space-based compute as stated product |
| Data | fleet, factories, test programs | telemetry, process parameters, failure archives | the physical loop's exhaust (I.2) |
| Settlement | Mars objective | self-sufficient city as stated goal | demand center; survival independent of Earth |

The theoretical advantage is not ownership of complementary companies but
a shorter verified end-to-end loop across design → manufacture → deploy →
learn. The closure race rewards the shortest such loop, not the largest
stock of any single input.

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

**What it changes**: fabrication moves from missing term to declared
target; the residual dependency moves one layer down (EUV lithography,
deposition, etch, metrology, ultra-pure feedstocks — sole-supplier
equipment, not foundries); the fab-to-space link becomes explicit (D3).
**What it does not change**: no wafers have been produced; the timeline is faster than any historical ramp; industry skepticism is on record. The competence question needs stating precisely, since earlier drafts got it wrong: Tesla, SpaceX, and xAI have no advanced-fab operating record, but **Intel plainly does**, and the reported process plan is Intel 14A — so the open question is whether that experience transfers into this organisational structure and what obligations Intel has actually accepted, not whether anyone involved has run a fab. Two further corrections: the sites are distinct — a smaller Tesla research fab at the Giga Texas campus and a proposed SpaceX-led scaled facility in Grimes County, whose county tax and economic-development agreements are now recorded as fully executed, strengthening site-level commitment without constituting a definitive construction, funding, or operating agreement [S6–S10] — and scale comparisons used in earlier drafts are withdrawn: wafer-start counts cannot be set against a foundry's global output without controlling for wafer diameter, node, product mix, yield, and effective die output, and "one terawatt per year" is a claimed annual production rate of hardware whose aggregate nameplate power draw would total a terawatt, a manufacturing-throughput figure not commensurable with national electricity consumption. **The lithography question**: for terrestrial operation, purchased
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
| E6 | S-1 initiative list: orbital compute, lunar manufacturing and energy, in-orbit and Moon/Mars manufacturing, asteroid mining, "interplanetary industrialization" | documented / regulatory filing [S27] | **strong** | neutral | the P4a backbone: a filing enumerating off-world industrial markets is hard to explain under H0 — and says nothing about closure |
| E7 | Terafab initiative; Intel joining; executed county agreements | announced→partly advanced / company_statement | weak | neutral | chip-supply hedging (inside H0) predicts a domestic fab about as well |
| E8 | SpaceX absorption of xAI | documented | weak | neutral | consolidation under overlapping control is expected under H0′; integration of the intelligence layer is also H1 |
| E9 | Rad-tolerant orbital silicon as a named fab line | announced / company_statement | moderate | neutral | H1 predicts it distinctly; a D3-supply commercial reading covers it too |
| E10 | No closure metrics, no seed BOM, no closure program | absent | neutral | **moderate against H2** | a deliberate closure strategy mildly predicts visible closure engineering by now; observability caveat applies |
| E11 | No export-scoped internal model variant, and no reported compliance apparatus for controlled-data training | absent | neutral | weak against H2 | the observable is the compliance architecture, not the model, which may be deliberately unpublicized |
| E13 | FCC **acceptance for filing** of an application for an orbital-data-center system of up to ~1M satellites | documented application; pending regulatory review — not an authorization | weak | neutral | filing a large option is far cheaper than receiving permission to deploy it |
| E14 | First-party Terafab messaging: Kardashev framing, ~10 Mt/yr to orbit, lunar mass drivers, orbital-vs-terrestrial cost decomposition | documented / company_statement [S29] | **strong** (declared intent only) | weak | supply-security strategy does not publish Kardashev framing or mass drivers; but messaging is cheap and the binding filings commit to none of it |

E12 and E15 (the Google/Planet Suncatcher prototype program and the design
study's content) are removed from this table in r3.4: they are actions of
*independent* actors and bear on no hypothesis about the Musk-associated
complex's intentions. They are retained as engineering reference-class
observations under external cross-checks below — an announced prototype
program (satellites slated for early 2027), and radiation results bounding
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
would be *moderate-to-strong for H2 specifically*: the Part I result that
recycling is indispensable in LEO makes it the rational early move of a
LEO-first closure strategy and of no one else.

**External cross-checks** [S35]: the canonical AGI-buildout analysis
resolves the power wall terrestrially without mentioning orbit —
non-space-interested corroboration of Part II from outside; its chip
bottleneck converges with the space radiation weak point (III.2); and its
fast-takeoff thesis, if right, weakens the H1/H2 rationale regardless of
the evidence — an effect on the prior, reported separately from the
item-level assessments. A second, **provisional** cross-check from the frontier-lab side (July
2026 hiring sweep archived at
`docs/transcripts/lab-job-listings-2026-07-26.md`; source-list candidate
for the Fourth Edition, pending a public dated snapshot with per-lab
counts, deduplication rules, and search vocabulary): a search across the
1,170 open OpenAI and Anthropic postings found *multiple roles explicitly
targeting* software-RSI preparation and measurement — RSI early-warning
metrics, "preparations for recursive self-improvement," chip-design RL,
long-horizon training environments — corroborating the fast-takeoff prior
effect from the institutions best placed to judge; and the same search
found *no* roles in fabrication, packaging/test, materials, or
production-equipment reproduction, so on the labs' declared hiring scope
the software loop leaves Part I's electronics import line untouched. A
negative search claim is only as strong as its documentation, hence the
provisional flag. Declared intent, not capability.

**Cumulative assessment** (ordinal synthesis, not multiplication — the
items are correlated and the ratings judgmental): the evidence
**substantially establishes H1 at the level of declared direction and
early implementation** — the S-1's own initiative list (E6) and the
first-party messaging (E14) are difficult to explain under a purely
terrestrial reading, and E7/E9/E12/E13 are consistent implementation
steps. It **does not establish H2**: no item in the table is more than
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
where governance holds enforceable leverage. The leverage variable is dependency — but not proportional to (1 − κ), since this document has already established that scalar closure is invalid and a single low-mass import can be a minimum cut conferring disproportionate leverage. The governing quantity is G_dependency = f(criticality, substitutability, stockpile, supplier concentration, enforceability): what matters is whether withholding an input collapses the network, not how much of it is imported. Part I supplies an answer that is architecture- and parameter-conditioned, and must be stated that way: **where import dependency remains load-bearing — the lunar and Mars ensembles — electronics is the most frequently observed minimum cut, and the vitamin parts are the last governance handle**; in the sampled central LEO draws no single import line was fatal, so there the material handle runs through feed availability and the recycling sector rather than any one import line. Material-dependency governance has a
declining window as closure rises; throttle authority, verification
requirements, and replication limits are cheapest to embed as licensing
conditions during the bridge period. Closure does not end governance
(communications, cryptographic authority, personnel, ownership, insurance,
treaties, orbital traffic, trade remain), but the material handle is the
one that closes. Design principle: replication authority should be the
most verified and least autonomous function in the system — positioned
deliberately against the efficiency gradient, embedded at the seed stage,
because it cannot be retrofitted onto a mature complex.

## III.5 Falsifiable indicators, model-ranked

The indicators now carry expected likelihood ratios informed by the models:

1. **Production or fabrication equipment explicitly designed for local
   extraterrestrial reproduction** — strong for H2 over H1.
2. **A dedicated cross-company closure program with published κ-vector
   metrics** — strong for H2 over H1 (flips E10).
3. **A published bill of materials for an off-world industrial seed**
   — strong for H2 over H1.
4. **Sustained scaled orbital-compute deployment despite publicly evident
   unfavorable unit economics** — moderate-to-strong for H1/H2 over H0 (Part II makes the test
   operational — watch fleet growth after the economics are public).
5. **Electronics vitamin-gap engineering**: stockpile facilities,
   shelf-life-rated spares logistics, off-world packaging/test lines
   — moderate-to-strong for H2 over H1 (Part I makes it the rational first move of a closure strategy).
6. **On-orbit materials-recovery recycling at scale** — moderate-to-strong for H2 (the Part I
   LEO indispensability result).
7. **An export-control-scoped internal model variant** — moderate.
8. **Terafab executed definitive agreements with committed capital**
   — weak-to-moderate (upgrades E7 from framework to program; hedging inside H0 still predicts it).

Threshold observations that would move Appendix A: a demonstrated ISRU
plant above ~50% full-system materials closure; audited robot production
figures; an independent satellite-failure audit diverging from ~2.5–3%; and
any traceable datum on off-world-producible electronics tiers — the
vitamin-gap anchor this document flags as its single most valuable missing
measurement. The thesis *weakens* if humanoid robotics remains
economically narrow, advanced manufacturing cannot be localized, launch
costs stop declining, closure requires a permanently growing Earth supply
chain, verification costs rise faster than capacity — or if Terafab
devolves into design-and-packaging dependent on external front-end
fabrication, which would reopen the fabrication term entirely.

## III.6 Refined complete thesis

    I(t+1) = I(t) + f(C, D, V, H)
    H(t+1) = H(t) + g(I, E, M, R) − δ_env · H(t)
    C(t+1) = C(t) + h(H, E, fab)

In earlier editions f, g, and h were unspecified placeholders and this compact model was a causal diagram. Here g and δ_env have operational form: g is the lexicographic maximin allocation of Part I.7
(with repair, recycling, stockpiles, and imports), and δ_env is the
per-sector, per-environment decomposition of Part I.4 — both executable,
both swept. The system becomes recursively self-expanding when
improvements in I reliably increase H and C, and the resulting increases
reliably increase future I faster than depreciation and failure reduce the
system; Part I computes when that condition holds *for the industrial
half*, as a function of assumptions that are now named, bounded, and
priced. The f and h functions — the intelligence and compute terms — remain
unspecified; making them operational is the Fourth Edition's frontier,
subject to the takeoff-speed caveat of II.5. What the thesis does not
claim is unchanged: no assertion that the companies are managed as one
program (III.3's evidence table is the assessment), no assertion that
closure is imminent (I.8's distributions are the assessment), and no
assertion that space is currently economical (II.3 is the assessment).

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
quantified: *if* industrial closure becomes sufficiently high (Part I says:
in every sector, with electronics the binding one) *and* terrestrial
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

> **Model check.** The cost-curve claim — Earth's marginal node rises with
> n, space's falls with n after closure — is the crossover surface, and at
> anchored values the curves do not cross. The scenario needs three
> demanding unanchored conditions: rad-tolerance at commodity cost (the strongest
> current data supports five-year TID survivability but leaves system
> reliability — SEE, training workloads, thermal, whole-spacecraft —
> unresolved [S32]), service life nearer 15 years than
> 5, and target-class launch or closure substituting for launch. The
> collector-area arithmetic, which is not in dispute; the three conditions are where the
> scenario lives.

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

> **Model check.** The paradigm-sensitivity split maps onto the model's
> sector structure: a shift perturbs the electronics column of the
> requirement matrix and the fab layer behind the vitamin imports — exactly
> the sector already identified as binding. The "deepest moat is building
> the next fab faster than a rival builds its first" claim translates to:
> machine tools and robotics are the moat, and both are
> knockout-indispensable in every location. Retooling speed is now a
> **computed output** (`cutsets.retooling_time`), and it hardens this
> scenario's central risk into a result: destroying 90% of the electronics
> or machine-tools sector (≈9% of total capacity) at any point on the
> central trajectory is **fatal, not a delay** — worst-case growth goes
> permanently negative relative to the unknocked counterfactual, under both
> the myopic and receding-horizon allocators, and at optimistic values too.
> The mechanism is the vitamin gap: at electronics q-scale 0.10–0.30,
> replacement local capacity is a multi-decade-payback asset no plausible
> planning horizon rebuilds from current output. Only power stranding under
> optimistic values is a finite delay (~27 years lost). Conditional
> implication: within this scenario class, a paradigm shift that obsoletes
> the local electronics tier removes the self-expansion margin permanently
> unless Earth imports resume — so the leapfrog hedge must be
> pre-positioned (hardware generality, retooling-ready lines, retained
> umbilical capacity), because post-shift rebuild from inside the complex
> is not a path the model offers. Caveats: deterministic values, 90%
> single-sector knockout, maximin allocation family; surplus-pinning
> (stage 3) and knock-fraction sweeps are Fourth Edition work.

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

---

# Appendix A: Parameter Anchors

The authoritative, machine-readable anchor set is `params/anchors.yaml`
[S28]; every generated report carries a per-run provenance table. Ranges
reflect genuine disagreement across sources; values are anchors, not
precision claims. The Second Edition's discipline — quantities normalized
by type, rate quantities never averaged into one "r" — is implemented in
code (`delta.py`) rather than prose.

## A.1 Capacity-loss quantities (δ), by type

| quantity | range | class [ref] | type |
|---|---|---|---|
| Solar-array degradation, GEO | 0.4–1.7 %/yr | peer_reviewed [S19] | continuous degradation |
| Terrestrial PV degradation | 0.5–0.6 %/yr median | peer_reviewed [S18] | continuous degradation |
| LEO constellation failure | ~3 % early generations; <0.5 % later | reporting [S22] | cohort-dependent; mixes failure, retirement, disposal; not a hazard rate |
| Satellite design life | ~15 yr GEO; ~5 yr LEO | industry standard [S22] | engineering envelope, not a hazard rate |
| Fab-tool depreciation | 2–5 yr | foundry reports | accounting schedule |
| Accelerator retirement | 3–6 yr | operator practice | technological retirement |
| Cluster interruption frequency | ~1 / 2,000 accelerator-days | training-run disclosure | mixes component, host, network, software events, mostly auto-recovered — NOT a component hazard rate |
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
| Strawman replication design target | ~1 yr (assumed) | technical_report [S23] | an estimate or measurement of anything — it is a proof-of-principle design assumption |
| Construction-execution cadence | ~10 months | reporting | recursive reproduction; used a mature host economy |
| Humanoid robot production | 50–100k targeted | company_statement | feasibility — targets evidence intent |

System replication time is unknown as a measurement. In this edition it
exists only as a computed output distribution (Part I.8), set-labeled.

## A.3 Closure and data quantities

| quantity | range | class [ref] | note |
|---|---|---|---|
| Closure reported in cited nonreplicating applications | 90–96 % | technical_report [S23] | not a demonstrated result for the proposed factory; complete parts closure was outside its scope |
| Demonstrated ISRU O₂, Mars | 6–12 g/hr | mission results [S21] | single output, small scale |
| Demonstrated lunar O₂ yield | ~20 %, TRL 5/6 | technical_report [S21] | full-system closure undemonstrated |
| Vitamin import fraction | 4–10 % | technical_report [S23] | CP-2255 residual |
| **Space electronics q-scale** | **0.10–0.30** | **ASSUMPTION** | **the vitamin gap — the results-driving unanchored number** |

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
| Equipment life, space / Earth | 3–7 / 3–6 yr | reporting [S36: LEO design lives; accelerator refresh cycles per A.1] |
| Utilization LEO / cislunar / lunar | 0.65–0.95 / 0.90–0.99 / 0.45–0.85 | ASSUMPTION ([S32] dawn-dusk cluster design supports the LEO high end) |
| DC capex | $11–20k /kW IT | reporting [S36: AI-optimized facility costs 2025–26, $11–20M/MW] |
| PUE | 1.10–1.40 | reporting [S36: hyperscale AI facilities] |
| Firm-power floors: nuclear PPA / gas | $0.09–0.13 / $0.04–0.06 per kWh | reporting [S36: restart PPAs ~$100–115/MWh; gas floor politically conditional, CCGT <$1,000/kW per S35] |
| WACC | 8–15 % | ASSUMPTION |

## A.5 External claims — comparison targets, never inputs

| claim | value | class [ref] |
|---|---|---|
| Google/Planet crossover threshold | $200–300 /kg | company_statement [S34] |
| Suncatcher launch-cost feasibility marker (not a parity claim) | ≲$200 /kg by mid-2030s; launch-only vs electricity-only | technical_report [S32] |

# Appendix B: Revision History and Provenance

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

**3.4 (this document)** — model-integrity and audit pass against a second
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
counts, and register fixes throughout.
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
document's single most valuable missing measurement; external claim checks
localizing the public crossover disagreement to three parameters;
r3.1: rewritten standalone.

# Appendix C: Reproducibility

    pip install -r requirements.txt
    python scripts/run_baseline.py   # Part I sweep + figures (~2 min)
    python scripts/run_part2.py      # Part II LCO + crossover (~1 min)
    python scripts/run_deep.py       # large-n MC, cut probabilities, policy
                                     # robustness, sensitivity (~1-2 h at n=400)
    pytest tests/ -q                 # 35 tests

Model: `src/rsimodel/{model,delta,cutsets,montecarlo,lco,policies,plots,report}.py`;
parameters: `params/{anchors,assumptions,environments}.yaml`; generated
reports with per-run provenance tables and machine-readable CSV summaries:
`outputs/` (headline table: `outputs/tables/mc_deep.csv`). All linear
programs are solved with SciPy's `linprog` (HiGHS backend); all randomness
flows through explicitly seeded `numpy.random.Generator` instances, and
every script fixes its seeds, so all tables regenerate deterministically
within a pinned reference environment. Structural coefficients are ASSUMPTION-class and
live only inside named assumption sets.

**Archival status (pre-publication requirement, not yet satisfied).** The
repository accompanying this draft is local. Before circulation as a
citable artifact, [S28] must acquire: a permanent public repository URL
with a tagged release and commit hash; an archived snapshot with DOI
(Zenodo/OSF); a dependency lockfile recording exact NumPy/SciPy versions;
a license; and a statement of the runtime environment. Until then, "open
model" is a statement of intent, and the 35 tests establish only that the
implementation matches its specification — not that the specification
adequately represents industrial reality.


# Appendix D: Complete model specification

Everything a reader needs to reconstruct the Part I model without opening
the implementation. Part II's cost model is fully specified by its affine
form (II.2) plus the anchor table (A.4); this appendix covers the
multisector dynamics.

**Sectors and units.** n = 10 sectors, ordered: power, mining, refining,
robotics, machine_tools, electronics, thermal, transport, repair,
recycling. Capacity K_j is in abstract capacity units (K_j(0) = 1 for all
j unless stated); sector j produces q_j output units per capacity unit per
year (q below is the central set after environment q-scaling for the lunar
architecture is applied via `environments.yaml`; the tabulated q is the
pre-scaling set value). Repair and recycling are service sectors: their
rows in A are zero, and their outputs are consumed as described below.

**Time.** Discrete steps of Δt = 0.25 yr (0.5 yr for cut-set enumeration),
default horizon 35–40 yr. No construction lags, commissioning delays,
yield ramps, or minimum efficient scales are modeled — all outputs are
stylized model outputs, not engineering timescale forecasts.

**Imports.** m_i(t) = B₀ · e^(−t/τ) · φ_i, with per-sector cutoffs
(m_i := 0 for i in the cut set after the cutoff year). Stockable sectors'
imports flow into the stockpile; non-stockable flow into the current
balance. Mars: stockable imports arrive as synodic batches of size
m·(2.14 yr) every 2.14 yr.

**Allocation (per step): lexicographic maximin LP.** Variables: builds
x ∈ ℝⁿ₊, wear-repair u ∈ ℝⁿ₊, recycling activity w ∈ ℝ₊, stockpile
drawdown d ∈ ℝⁿ₊ (d_i = 0 for non-stockable i), growth floor g ∈ ℝ.

Stage 1 — maximize g subject to:

    x_j + u_j − δ_j K_j ≥ g K_j                                (all j)
    u_j ≤ δ_wear,j K_j                                          (all j)
    Σ_j A[i,j] x_j + s_f Σ_j A[i,j] u_j
        + 1[i=repair] · (1/η_rep) Σ_j u_j
        + 1[i=recycling] · w
        + o_i w − ρ_i w − d_i  ≤  q_i K_i + m_direct,i          (all i)
    w + η_scrap Σ_j u_j ≤ η_scrap Σ_j δ_j K_j
    d_i ≤ S_i / Δt

with s_f = spares fraction (0.15), η_rep = repair efficiency (0.75
central), η_scrap = scrap recovery (0.40 central, < 1 always: recycling
yield is below unity), o = recycling opex vector, ρ = recycling output
profile (secondary mining/refining feed). Stage 2 — holding g at its
stage-1 optimum (tolerance 10⁻⁹), minimize Σ_i d_i: stock is a buffer,
spent only when it buys worst-case growth. The LP objective pins g and d
uniquely; surplus builds above the growth floor are vertex-dependent
(stage-3 pinning queued in ROADMAP), which is why capacity *totals* are
treated cautiously (Part IV retooling metric is defined on g-trajectories).

**State updates.**

    K_j ← max(K_j + Δt (x_j + u_j − δ_j K_j), 10⁻⁹)
    S_i ← clip(S_i + inflow_i − d_i Δt − S_i Δt / L_i, 0, C_i)

with shelf life L_i (electronics 5 yr central), capacity cap
C_i = c_years · Σ_j A[i,j] δ_j K_j (replacement demand), initial stock
S_i(0) = s_years · replacement demand at t = 0, stockable sectors only
(robotics, machine tools, electronics, repair).

**Depreciation.** δ_j = δ_wear,j + δ_catastrophic,j + δ_obsolescence,j +
δ_logistics,j per environment (`environments.yaml`), anchored entries
resolved at geometric mids (deterministic) or loguniform draws (MC), one
shared draw per anchor per run. Obsolescence is included on the reading
that K is frontier-equivalent capacity (A.1's five-quantity separation).

**Shocks.** Per step and per shock class: N ~ Poisson(rate · Δt) events;
each multiplies K over its sector group by (1 − f), f ~ U(f_lo, f_hi).
Rates jittered ±30% per MC run (ASSUMPTION).

**Outcome definitions.** "Expanding at year 30": maximin g > 0 at the step
containing year 30 (this does not by itself preclude near-zero absolute
capacity; a minimum-viable-scale criterion is queued). "Doubling": first t
with Σ_j K_j(t) ≥ 2 Σ_j K_j(0); reported both over all runs that ever
double and conditioned on year-30 survivors — the difference is the
doubled-then-failed class.

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

**Recursive self-improvement (RSI)**: a process in which an intelligent
system contributes to producing a more capable successor. **Industrial
closure (κ)**: the degree to which a production network internally supplies
the critical inputs required for its own operation — a vector, not a
scalar. **Closure engineering**: the quantitative discipline, from the 1980
summer study, of accounting for every input a replicating system must
produce or import. **Self-sustaining / self-expanding**: replacing consumed
capacity / producing net additional capacity. **Industrial seed**: a
compact initial system intended to grow into a local production network.
**Clock-setting component**: the component with the shortest replacement
horizon that cannot yet be produced or stockpiled locally. **Vitamin gap**:
the unclosable fraction of electronics output — this document's binding
unknown. **Maximin growth rate g**: the worst-case sector growth rate the
allocation program maximizes. **Minimum cut set**: a minimal set of
imported inputs whose loss prevents self-expansion. **Assumption set**: a
named, complete collection of ASSUMPTION-class structural coefficients.
**Anchor**: a published, source-classed range sampled by Monte Carlo.
**Computed**: derived mechanically from stated assumptions by the open
model; inherits the class of its weakest input.

# Sources

Second Edition numbering retained; [S35] is new in this edition.

**Primary statements.** [S1] SpaceX, "Mars & Beyond." [S2] Tesla, "Master
Plan Part 3." [S3] xAI, company mission. [S4–S5] NASA, ISRU and lunar
surface technology overviews.

**2026 developments.** [S6] Reuters (Mar 14, 2026): Terafab launch, AI5,
fab partnerships. [S7] CBS News (Mar 23, 2026): the Austin announcement.
[S8] Proactive Investors (Mar 2026): 2-nm target, dual terrestrial/space
lines, 2028 goal. [S9] CNBC (May 6, 2026): filing-based cost ceiling
(~$119B), research fab, SpaceX lead role. [S10] Teslarati/Electrek
(Mar 2026): venture structure, SpaceX–xAI merger, D3 line, skepticism.
[S11] SpaceXAI, "Introducing Grok 4.5" (Jul 2026) with Axios coverage:
in-house engineering model. [S12] VentureBeat/Northflank (Jul 2026): Kimi
K3, 2.8T-parameter open weights near the frontier. [S13] Public statements
(Jul 2026): SpaceX engineering corpus (ex-ITAR) entering supplemental
training. [S14] Connecting The Dots (commentary; corroborated core only).
[S15] Jay Vijayan interviews: Tesla's Warp ERP. [S16] Stack Overflow
engineering blog (2021): SpaceX's Warp Drive. [S17] Tesla AI Day
(2021–22): occupancy network, 1.4B frames, auto-labeling.

**Parameter literature.** [S18] Jordan et al., Progress in Photovoltaics
24(7), 2016. [S19] GEO telemetry study, Int. J. Space Science and
Engineering, 2018. [S20] Fraunhofer ISE PV Report (2026); Bhandari et al.,
RSER 47, 2015. [S21] MOXIE results, Science Advances 2022; NASA carbothermal
reports 2024–25. [S22] Independent satellite tracking (J. McDowell), 2020–2026: constellation deorbit and status statistics; cohort-dependent, separating early deorbit, uncontrolled decay, retirement, and disposal — fleet fractions, not hazard rates.

**Closure engineering.** [S23] NASA CP-2255, *Advanced Automation for Space Missions*, 1980: a proof-of-principle self-replicating lunar factory from a ~100-ton seed; a one-year **strawman** replication target with component values described as crude estimates; 90–96% closure cited from earlier studies of specific **nonreplicating** production applications; rigorous demonstration of complete parts closure explicitly outside scope. [S24] Freitas & Merkle, *Kinematic Self-Replicating
Machines*, 2004.

**Economics and progress rates.** [S25] Coase, "The Nature of the Firm,"
1937. [S26] Epoch AI (Ho et al.), "Algorithmic Progress in Language
Models," 2024.

**Corporate and orbital-compute record.** [S27] SpaceX Form S-1 (filed May
20, 2026) and related offering material, including the Rule 433
free-writing prospectus, SEC accession 0001628280-26-040610 (the source of
the initiative-list quotations in E6; page-level cites to be pinned at
archival): Terafab as unsettled framework; orbital data-center plans; chip
shortfall; ~1,000 automated collision-avoidance maneuvers/day. [S28] Companion simulation program — this edition's model repository (Appendix C). Listed for reproducibility, not as evidence: it computes the consequences of stated assumptions and supports no claim on its own authority. [S29] Terafab official site (accessed Jul 2026):
Kardashev framing, scaling figures, AI5/AI6/D3, Earth-vs-space cost
decomposition, lunar mass drivers — declared intent, not commitment.
[S30] Waymo safety disclosures, 2026. [S31] Heavy-lift flight-test
reporting, 2026. [S32] B. Agüera y Arcas, T. Beals, M. Biggs, J. V. Bloom, T. Fischbacher, K. Gromov, U. Köster, R. Pravahan, J. Manyika (Google), "Towards a future space-based, highly scalable AI infrastructure system design," arXiv:2511.19468 (v1 22 Nov 2025; **v2 17 Jun 2026**, the version carrying the detailed figures cited here), with the accompanying Project Suncatcher blog post: 67 MeV proton-beam testing of a Trillium TPU v6e (**HBM most TID-sensitive**, irregularities from 2 krad(Si) against a 750 rad(Si) five-year requirement, no hard TID failures to 15 krad(Si); **core logic and on-chip SRAM most SEE-sensitive**; inference error probability ~1 per 3×10⁶ inferences under stated assumptions; training impact reserved); an 81-satellite, 1 km-radius cluster at ~650 km in dawn-dusk sun-synchronous orbit; free-space optical links demonstrated at 800 Gbps unidirectional against a ~10 Tbps per-link requirement; and a launch-cost analysis the authors twice state is **not** a full economic analysis, comparing amortised launch cost per kW-yr ($810 Starlink-v2-class, $810–7,500 across classes at $200/kg) with terrestrial **electricity spend** ($570–3,000/kW-yr), excluding infrastructure, building, and chip costs. Reaching ≲$200/kg by ~2035 requires ~370,000 t additional cumulative mass (~1,800 Starship-class flights, ~180/yr). Thermal management, ground communications, and on-orbit reliability and repair named unsolved; orbital repair called impracticable, redundant provisioning proposed. [S33] SpaceNews / Via
Satellite / DCD orbital-compute coverage, 2025–26: Google–Planet
partnership, two prototype satellites by early 2027. [S34] Will Marshall
(co-founder and CEO, Planet Labs), interviewed on the Moonshots podcast
with P. Diamandis and colleagues, episode #266, published 2026-06-26; full
transcript with per-paragraph timestamps archived at
`docs/transcripts/moonshots-266-2026-06-26.md` (launch-tax-vs-compute-tax
at 0:00:22 and 1:17:49; the Google/Planet "$200–300/kg" study recollection
at 0:52:07): launch tax vs compute
tax; decay-life-matches-obsolescence; payload cost-performance; archive
irreproducibility; finite-demand possibility; biosphere telos; the
$200–300/kg study recollection. Recollections and projections unverified.
[S35] L. Aschenbrenner, *Situational Awareness: The Decade Ahead*, June
2024 (archived at `docs/sources/`): trillion-dollar-cluster trajectory;
power as binding constraint resolved via natural gas ($0.04–0.06/kWh floor,
politically conditional); CoWoS/HBM as chip bottlenecks; fast-takeoff
thesis; capital-mobilization reference classes. Analyst estimates.
[S36] Assorted company disclosures, industry reporting, and technical
literature used in Appendix A.4 and `params/anchors.yaml`, cited
collectively because no single permanent identifier applies: launch price
sheets (2024–26); flexible-array and deployable-radiator performance
literature; accelerator system pricing and refresh-cycle reporting;
AI-optimized data-center capex and PUE reporting (2025–26); nuclear
restart PPA reporting (2024). Each `anchors.yaml` entry names its own
class and note; rows are auditable against the archived sources in
`docs/sources/` and `docs/transcripts/` where applicable.
