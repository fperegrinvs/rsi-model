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

The observed portfolio is consistent with a physical-stack seeding strategy:
orbital compute can create anchor demand and operating experience across
launch, spacecraft production, energy, thermal management, communications,
silicon, autonomy, and servicing. If capable AI accelerates improvement
across that stack, more intelligence could create more industrial capacity,
which could support more intelligence.

The economics nevertheless point to
Earth at every anchored value, so the seeding interpretation must earn its
cost gap through measured learning, faster capacity activation,
cross-program reuse, or declining Earth dependence. Present evidence does
not establish that this is management's actual strategy or that recursive
off-world industrial closure is the governing objective of the companies
described in Part III. The executable model finds recursion only under
assumptions that remain choices rather than measurements; the observations
that would change either conclusion are named, ranked, and observable.

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

Section IV.4 therefore yields a conditional option, not a scalar welfare or
strategy verdict. Equation [@eq:welfare-activity-accounts] keeps relocation,
expansion, humanitarian, scientific, and industrial allocations separate;
the anchored economics still favor Earth; and the 17-of-18 portfolio breadth
still contains an open parent-tool minimum cut. The seeding interpretation
would strengthen only with measured shared-stack learning, faster capacity
activation, cross-program reuse, or declining Earth dependence, while a
closure claim would additionally require the missing production,
verification, repair, and source chains to operate beyond Earth.

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
