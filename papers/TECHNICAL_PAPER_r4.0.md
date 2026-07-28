# Conditional closure of an autonomous off-world industrial bootstrap

r4.0 technical-paper draft

## Abstract

We ask a conditional engineering question: what material, service, autonomy,
commissioning, and source constraints must a machine-only industrial seed
satisfy before aggregate operating capacity can expand without routine Earth
resupply? An 18-sector, 17-material linear seed model is coupled to
sector-resolved construction, commissioning cohorts, depreciation, recycling,
finite strategic-material inventory, lunar and synthetic asteroid feed,
observable autonomy gates, repair queues, source outages, and minimum viable
sector floors. The central terrestrial rehearsal and lunar
strategic-material bridge contract to 0.47 and 0.54 sector-balanced
cell-equivalents at year 40. Strict lunar closure is infeasible. A deliberately
synthetic Moon–asteroid source portfolio reaches 3.61 equivalents and first
crosses two at year 34.75, but this is an internal-consistency result for a
stipulated source vector, not evidence that an accessible portfolio exists.
Independent allocation, repair, environment, shock, and Pareto diagnostics
show that policy and seed composition materially change outcomes. The model
therefore identifies requirements, cuts, and falsification tests; it does not
establish real-world industrial closure or recursive intelligence-driven
growth.

## Keywords

industrial closure; space manufacturing; autonomous systems; lunar industry;
industrial ecology; systems engineering

## Highlights

- Sector-resolved dynamics overturn the former scalar doubling result.
- Strict lunar closure is infeasible in the declared source graph.
- The synthetic Moon–asteroid case doubles only after 34.75 years.
- Every mass and frequency is an assumption-conditioned implication.

## 1. Question and claims

Prior lunar-factory and machine-reproduction studies establish an engineering
design lineage, not an achieved self-reproducing industrial system [1,2].
The paper addresses two propositions only:

- P1: a self-expanding industrial system is conceptually representable as
  coupled material, service, knowledge, repair, and commissioning constraints;
- P2: particular architectures are conditionally feasible if their declared
  coefficients and source vectors hold.

It does not infer P2 from corporate plans, does not price mature economic
superiority, and does not treat a model solution as empirical proof.

The computed object is an internal-consistency certificate for a stipulated
closure matrix. “Aggregate operating-capacity doubling” means that every
indispensable sector has reached two times its seed-normalized operating
capacity. It is not an audited second factory unless every subsystem also
passes the discrete construction, commissioning, yield, and connection gates.

## 2. Model

The seed program contains 18 sectors: power, mining, refining, robotics,
machine tools, construction, thermal control, transport, repair, recycling,
five electronics-production tiers, process equipment/metrology, and compute.
Seventeen material categories flow through sector bills of material. Service
requirements form a sector-by-sector matrix. Lunar and synthetic
Moon–asteroid sources provide recoverable-yield vectors; Earth contributions
are finite initial strategic-material inventories rather than continuing
resupply. NASA capability roadmaps and laboratory or prototype ISRU results
motivate several process categories, but they demonstrate individual
operations rather than the closed production system modeled here [3,4].

The seed LP minimizes installed mass subject to:

1. minimum viable sector capacity;
2. horizon replacement and one additional balanced capacity equivalent;
3. material conservation;
4. mining, refining, transport, and process-energy throughput;
5. task coverage and remote-intervention limits.

All recovery yields, process coefficients, autonomy mappings, and candidate
source portfolios are scenario assumptions unless a source is named.
Occurrence data—including bulk lunar composition—do not establish
recoverable reserves or plant yield [5].

The dynamic model retains every sector as state. Orders enter sector-specific
construction queues and cohort-resolved yield ramps. Depreciation produces
repairable failures and recoverable retirement material. Repair consumes
parts, repair service, intervention hours, and queue time. Aggregate capacity
is derived from the weakest normalized operating sector. A separate
delivered-seed model adds packaging, unloading and site equipment, calibration
references, startup-energy storage, spares, startup failures, and recovery.

Observable autonomy quantities include named-task completion, intervention
hours, fault diagnosis, verification throughput, engineering-cycle time,
process yield, repair success, and mean time to recovery. The scalar
intelligence state is not treated as independent evidence of any capability.

## 3. Central results

The minimum installed seed is approximately 207 t for the terrestrial
rehearsal, 217 t for the lunar strategic-material bridge, and 186 t for the
Moon–asteroid network. The bridge contains approximately 58 t of initial
Earth strategic material—27% of installed mass—so it is not a trace “vitamin”
case. Nickel, copper, and carbon dominate that stock.

With balanced construction and the identity environment profile:

| Scenario | LP status | Aggregate operating capacity, year 40 | First doubling | Direction over final five years |
|---|---|---:|---:|---|
| terrestrial rehearsal | feasible | 0.47 | none | contracting |
| lunar strategic-material bridge | feasible | 0.54 | none | contracting |
| strict lunar | infeasible | — | — | — |
| synthetic Moon–asteroid network | feasible | 3.61 | 34.75 yr | expanding |

The strict-lunar elastic relaxation identifies category-specific shortages in
nickel, copper, carbon, cobalt, chromium, rare earths, lithium, hydrogen, and
dopants. These are requirements for substitution, import, or a different
source; they are not proof that lunar closure is impossible.

The positive network case is deliberately synthetic. It supports only this
inference: the configured industrial graph expands if a sufficiently diverse
source vector is simultaneously accessible at the declared throughput,
timing, and recovery yields. Named-body accessibility, delta-v, transfer
windows, reserve depletion, and mining-fleet reproduction remain empirical
gates.

## 4. Structural diagnostics

Balanced copies are not the only construction policy. A live maximin allocator
can direct material and service to deficient sectors. Repair and shock tests
show large differences from the balanced baseline. Because those coefficients
are assumptions, the spread is evidence of policy sensitivity rather than a
new central forecast.

Nominal and adverse lunar profiles alter throughput, yield, power demand, and
depreciation for dust, traction, reduced convection, vacuum behavior,
radiation, thermal cycling, contamination, and calibration drift. The adverse
lunar bridge becomes LP-infeasible. Some feasible penalized cases improve
their later trajectory because the mass-minimizing LP installs a larger seed;
this is an optimization-frontier artifact. The dust penalties are scenario
bounds informed by NASA's surface-effects guide, not fitted degradation
coefficients [6].

Two-year communication, verification, and compute outages create the
corresponding operational regimes. A 90% advanced-logic/memory loss creates a
repair-limited regime. These stress windows demonstrate classification and
falsification plumbing, not event probabilities.

A composition-changing search enumerates process routes, sector redundancy,
and source allocations. It marks dominated and non-dominated designs across
delivered mass, import mass, intervention, doubling time, year-40 capacity,
and capacity after a five-year asteroid-source outage. The minimum-mass robust
point is conditional on this small discrete design space and is not a globally
optimal mission architecture.

## 5. Falsification tests

The next evidence should come from a closed terrestrial rehearsal using the
declared material and energy palette. Required observations are:

- task-level autonomous completion and intervention hours;
- process yield, contamination, consumable use, calibration drift, and tool
  life;
- fault diagnosis, repair success, recovery time, and failed recovery;
- provenance-preserving material flow and sector-level commissioning;
- performance under communication loss and source interruption;
- construction of a second auditable production cell.

Failure to meet any indispensable sector floor, unexplained material
creation, routine human entry, non-recoverable calibration loss, or inability
to commission a second cell weakens the architecture directly.

## 6. Limitations and conclusion

Material categories remain coarser than mineralogy, chemical species, purity
ladders, critical parts, and production-equipment ancestry. Electronics
tiers are not complete fabs. Environmental and autonomy mappings are
assumption bounds. The asteroid portfolio is synthetic. The terrestrial
rehearsal has not been executed.

The strongest result is therefore negative and conditional: material
diversity, advanced process-equipment reproduction, and retained sector
margins dominate the declared bootstrap. A finite Earth strategic-material
stock does not sustain the lunar bridge. The only central expanding case
requires a stipulated diverse external source. The model is useful because
it makes those requirements and failure cuts explicit—not because it proves
that they can be met.

Reproducibility and full specification are in the r4.0 repository monograph
and `papers/TECHNICAL_SUPPLEMENT_r4.0.md`.

## Data and code availability

Source code, parameters, deterministic seeds, tests, generated tables,
figures, and byte-verifiable manifests accompany the r4.0 repository release.
The public release record must identify the immutable tag, archive URL, and
version DOI before submission.

## References

[1] NASA/ASEE, *Advanced Automation for Space Missions*, NASA CP-2255,
1980. https://ntrs.nasa.gov/citations/19830007077.

[2] R. A. Freitas Jr. and R. C. Merkle, *Kinematic Self-Replicating
Machines*, Landes Bioscience, 2004.

[3] D. L. Linne, G. B. Sanders, and K. M. Taminger, “Capability and
Technology Performance Goals for the Next Step in Affordable Human
Exploration of Space,” AIAA 2015-1650, 2015.
https://doi.org/10.2514/6.2015-1650.

[4] NASA, “Lunar Surface Technology,” accessed July 27, 2026.
https://www.nasa.gov/lunar-surface-technology/.

[5] NASA Science, “Moon Composition & Structure,” updated July 23, 2026.
https://science.nasa.gov/moon/composition/.

[6] NASA, *Lunar Dust Mitigation: A Guide and Reference*,
NASA Technical Reports Server record 20220018746, 2021.
https://ntrs.nasa.gov/citations/20220018746.
