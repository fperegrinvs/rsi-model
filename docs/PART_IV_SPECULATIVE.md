# Part IV — Speculative Terminal Scenarios (Quarantined)

> **QUARANTINE NOTICE.** Everything in this document is scenario-class:
> internally consistent extrapolation, **not** established result (the status
> note inherited from Second Edition §16, final at r2.11; canonical statement
> now Third Edition manuscript r3.3 Part IV). Nothing here feeds back into
> Parts I–II inputs.
> Where a scenario claim touches something the model can actually say, the
> model's answer is quoted in a `Model check` block — usually as a constraint
> on the scenario, not support for it.

The paper's defensible core conclusion, restated with this repo's findings
attached, is: *if industrial closure becomes sufficiently high and terrestrial
expansion costs rise faster than off-world deployment costs, some large-scale
industrial and computational activity may migrate off Earth.* Both conditionals
are now quantified: Part I makes "sufficiently high closure" concrete
(electronics dominates the lunar and Mars binding structure; its import line
alone is fatal in ~9% of otherwise-viable central lunar draws and ~75% on
Mars, while LEO converts the import dependency into an indispensable
recycling sector), and Part II prices the migration condition (unreachable
inside anchored ranges; reachable only in the qualification/life/utilization
corner at target-class launch prices). Everything below extrapolates past
that sentence.

## Scenario 1 — Two walls, two escapes, one passage (§16 core)

The capital wall: market-priced expansion meets scarcity pricing and supply
elasticity limits; the escape is self-replication, re-denominating growth from
dollars into materials, energy, and time. The operating wall: society-priced
costs (land, permits, politics, waste heat) rise with scale; the escape is
space. Both escapes pass through the bridge: the first seed bought at full
market price, operated where depreciation is worst, financed by intermediate
products.

> **Model check (Part I).** The "one passage" framing survives contact with the
> model, with a sharpened failure mode: the passage is not generic burn-rate
> risk but a *specific* dependency structure. Under the conservative assumption
> set the system mostly fails in all three locations regardless of financing
> (10–21% of sampled runs still expand — statistical, not categorical
> failure); under central assumptions survival is a coin-to-strong bet
> (59–90% of sampled runs at 30 yr with shocks, by location; frequencies
> under the stipulated ensemble) and the thing that kills marginal lunar and
> Mars runs is the electronics vitamin line, not aggregate underinvestment. "Surviving the bridge" operationally
> means: hold electronics-class stockpiles against shelf life, and reach local
> production of *some* electronics tier before the import ramp decays.

## Scenario 2 — After convergence: deployment as the terminal regime

§16 posits architectural convergence — the point where discovery stops binding
and deployment becomes the whole game — after which intelligence behaves like a
commodity: throughput = deployed energy × physical efficiency. Efficiency is
floor-bounded (Landauer); scale means energy; energy means collector area;
unbounded collector area exists in one place. The terminal operating-wall
argument: after convergence there is nothing left to compete on except the one
input Earth cannot supply without limit.

> **Model check (Part II).** The scenario's cost-curve claim — Earth's marginal
> node cost rises with n while space's falls with n after closure — is exactly
> the crossover surface, and at anchored values the curves do not cross: the
> space cost is dominated not by launch (which targets can move) but by the
> qualification premium and 3–7-year equipment life, neither of which
> self-replication automatically fixes. For the terminal regime to arrive, the
> scenario needs (a) rad-tolerance at ~commodity cost — plausibly what a
> Terafab rad-tolerant line is *for*, (b) service life closer to GEO's 15 yr
> than LEO's 5, and (c) launch at target-class prices or local manufacture
> replacing launch entirely (the κ axis). The model marks these as three
> demanding unanchored conditions; the scenario stands or falls with them,
> not with collector-area arithmetic, which is not in dispute.

The ceilings-and-rates argument (planetary waste-heat ceiling ~2 orders above
current energy use; Landauer floor several orders below current efficiency;
compounding traversal rates) ports with r2.10's own tightening: the ~3×/yr
algorithmic-efficiency figure measures compute-for-fixed-language-performance
only and licenses no extrapolation to general capability, and the whole
compounding argument is now stated as a *sensitivity result*, not an
expectation. Far in distance, plausibly near in time — and whether the
compounding is sustained is precisely what is unknown. This repo adds nothing
quantitative to it and takes nothing from it.

r2.10 adds a challenge this scenario must now carry: **demand-side
saturation**. The terminal regime assumes appetite for compute is effectively
unbounded; if the set of tasks worth computing is bounded — if understanding
the physical world is a finite computational problem needing some modest
multiple of present capacity — demand saturates, unbounded deployment is never
needed, and the argument that space is the only arena permitting it loses its
motivation entirely. r2.10's own framing: the physical ceilings bound how
cheaply computation can be done; a demand ceiling would bound how much is
*wanted* — "the second is the more decisive and the less examined." Nothing in
Parts I–II bears on which regime obtains; the scenario is conditional on
non-saturation, and that condition is now explicit.

The non-saturation branch has a canonical published statement: *Situational
Awareness* (Aschenbrenner, June 2024, ch. IIIa; `docs/sources/`) — ~$1T/yr of
AI investment by 2027, ~$8T by 2030, individual clusters at >20% of US
electricity, with returns compounding through AGI. Its historical reference
classes calibrate what "unprecedented" means for the capital wall: Manhattan
and Apollo peaked at ~0.4% of GDP, British railway investment ran ~40% of GDP
over a decade, wartime borrowing exceeded 60–100% of GDP — so trillion-scale
buildout is extreme but inside the historical envelope, which is the strongest
available argument that the capital wall yields to expected returns. Note the
same document also supplies this scenario's sharpest *terrestrial* rebuttal:
it meets the operating wall with natural gas and deregulation, never with
orbit (see Part III, external cross-checks).

The upgrade asymmetry is narrower than earlier revisions claimed, per r2.10:
it applies to the **software layer only** — algorithmic gains raise the value
of deployed compute at low marginal cost, but hardware-dependent architectural
gains (new processor architectures, memory hierarchies, photonic/analog
devices, new nodes) require physical replacement or retrofit. Silicon is not
upgraded in place. The model consequence is correspondingly narrower: Part I's
space-electronics obsolescence component (ASSUMPTION 0.06/yr) would shrink
after convergence only for its software-limited share — a scenario-conditional
parameter change, flagged here and nowhere else.

One concession runs the *other* way and touches Part II directly — stated in
its r2.11-narrowed form, since the r2.10 version overclaimed: for some
compute-payload classes in *very low* orbit, aligning useful life with
accelerator-obsolescence cycles reduces the economic value of repair, and
part of δ_logistics + δ_catastrophic folds into a δ_obsolescence Earth pays
regardless. The qualifications are substantial: five-year natural decay is
typical near 400 km but not assured beyond 500 km (altitude-, ballistic-, and
solar-activity-dependent); the leading published orbital-compute architecture
sits near 650 km, chosen for illumination, so the concession does not
describe that design; and disposal is not free — station-keeping, collision
avoidance (on the order of a thousand automated maneuvers per day across the
largest constellation), replacement launch, and spares all remain. This is
the "strap space to Moore's law" argument of the Moonshots transcript in its
defensible form. It is bounded: mines, refineries, machine tools, and robots
must last decades to close a loop, so Part I's industrial δ decomposition
stands unchanged — the narrowed concession applies to some compute payloads
of Part II, not the industrial complex of Part I.

## Scenario 3 — Paradigm shifts: delay, alteration, or prevention

§16's bounding of the leapfrog objection: (1) catch-up time — a new computing
paradigm must beat the incumbent *plus* decades of compounding process
learning, still improving when the newcomer matures; (2) finiteness —
irreversible-computation paradigms all climb toward the same thermodynamic
ceiling, so resets shrink (reversible computing being the stated exception).
Exposure is concentrated in fabrication on 10–20-year horizons; energy, labor,
transport, and materials are *less paradigm-sensitive* (r2.10's softened
wording — substantially reusable across a shift, not immune: a new paradigm
can still alter materials, power quality, cooling, tolerances, and factory
architecture); the chip fleet self-insures via its own 3–6-year depreciation.

> **Model check (Parts I–II).** The paradigm-sensitivity split maps cleanly
> onto the model's sector structure: a paradigm shift changes the electronics
> *column* of the A matrix and the fab layer behind the vitamin imports, while
> leaving power/mining/refining/robotics/thermal/transport recipes largely
> (not perfectly) intact —
> i.e., it perturbs exactly the sector the model already identifies as binding.
> Two consequences. First, the "deepest moat is building the next fab faster
> than a rival builds its first" claim translates to: the machine_tools and
> robotics sectors are the moat, and in the model they are indispensable in
> every location (knockout-unrecoverable) — consistent. Second, retooling
> speed is now a **computed output** (`cutsets.retooling_time`), and the
> result is harsher than the prose: destroying 90% of the electronics or
> machine-tools sector at any point on the central trajectory (≈9% of total
> capacity) is **fatal, not a delay** — the system's worst-case growth goes
> permanently negative relative to its counterfactual, under both the myopic
> and the receding-horizon allocator, and at optimistic values too. The
> mechanism is the vitamin gap itself: with electronics q-scaled to
> 0.10–0.30, replacement local capacity is a multi-decade-payback asset that
> no plausible planning horizon rebuilds out of current output, and the
> import ramp has decayed. Only power stranding under optimistic values is a
> finite delay (~27 years lost per 9% of capacity). Scenario-class
> implication, stated conditionally: within this scenario class a
> compute-paradigm shift that obsoletes the local electronics tier does not
> merely strand capital — it removes the self-expansion margin permanently
> unless Earth imports resume. The hedge must therefore be held *before* the
> shift (hardware generality, retooling-ready lines, retained umbilical
> capacity); post-shift rebuild from inside the complex is not a path this
> model offers. Caveats: deterministic central values, 90% single-sector
> knockout, and the maximin allocation family — a stage-3 surplus-pinning
> refinement and alternative knock fractions are Fourth Edition work.

## What would move any of this out of quarantine

In rising order of demandingness: a demonstrated ISRU plant above ~50%
full-system materials closure (the manuscript §III.5 threshold); an audited off-world
electronics production line at any node size; a measured decline in imported
mass per unit of local productive capacity; and P > D published per component
class. Until then, Part IV remains scenarios — consistent, priced, and
unproven.
