# Roadmap — Evidence and Release Work Still Pending for r4.0

**Audit date:** 2026-07-29

**Scope:** the r4.0 manuscript, model, evidence program, and publication
package.

**Audit method:** each external-review recommendation was checked against the
article, model, generated artifacts, and tests. A checkmark in an older ledger
was not accepted as evidence. This file contains only work that remains both
material and non-obsolete; implemented work is recorded in `CHANGELOG.md`.

The review-response implementation now includes sector-resolved cohort
dynamics, independent allocation and repair, delivered-seed deployment,
observable autonomy regimes, process-environment profiles, finite
shell-resolved mass/debris, structural policy sweeps, shelf-limited
electronics architectures, completed Part II cost/workload boundaries,
symmetric dynamic economics, composition-changing Pareto designs, governance
traceability, a machine claim glossary, claim-level provenance with enforced
source-class demotion where evidence does not support a modeled endpoint, and
three companion-paper drafts. Those structures improve falsifiability. They
do not turn assumption-class coefficients into empirical evidence.

New coefficient-bearing work must use an anchor-grade source or a visibly
named `ASSUMPTION` set with a bounding argument. Model feasibility must never
be restated as demonstrated feasibility.

## Priority 0 — Publish an immutable, independently auditable r4.0

### 1. Exercise the release workflow and publish the immutable archive

**What is already done:** the repository now has a complete hashed dependency
lock, an explicit `osqp` dependency, and a Linux CI workflow that installs
from the locked environments, runs the full test suite, regenerates the
artifact sets and canonical HTML, rejects generated drift, and verifies every
row in both artifact manifests byte-for-byte. The complete local candidate
pipeline passed on 2026-07-29, including model regeneration, provenance,
standalone and Quarto builds, 255 Python tests, 17 Bun tests, coverage,
package isolation, dependency audits, SBOM generation, cross-browser layout,
site/accessibility checks, and 570 manifest records. Candidate and
publication preflight modes also check r4.0 identity, clean-tree state, tag
state, version versus concept DOI, release-date agreement, and immutable HTML
metadata.
Publication mode additionally requires an external authorization record
bound to the exact commit, passing Linux CI run, archive record, release
date, version DOI, canonical URL, responsible person, and attestation. The
record stays outside Git so approving a commit does not change it.

**Why it remains:** the reviewed release candidate is prepared on a dedicated
branch, but the workflow has not yet passed against that exact commit in
GitHub's clean Linux runner or been merged into the remote default branch. No
local immutable `r4.0` tag, archive, canonical release URL, or version DOI
exists. Those publication actions still require a passing remote Linux run,
author or release-manager authorization bound to the exact commit, and an
immutable archive.

**Complete when:**

- the publication workflow passes on the release commit in a clean Linux
  runner;
- any platform-dependent artifact drift is resolved or explicitly removed
  from the cross-platform equality contract;
- the clean commit is tagged `r4.0` and archived immutably;
- the manuscript, `CITATION.cff`, HTML metadata, and release record carry the
  same date, canonical URL, commit, and version DOI;
- the archived artifacts and both manifests verify byte-for-byte.

**Evidence:** manuscript Status and Appendix C; `.github/workflows/publication.yml`;
`pyproject.toml`; `uv.lock`; `rsi-verify-manifests`;
`rsi-release-preflight`; `docs/RELEASE_RUNBOOK.md`; GitHub `origin`
is configured; no r4.0 tag is present locally.

## Priority 1 — Replace the hardest closure assumptions with process evidence

### 2. Build and calibrate a process-feasible industrial-closure graph

**What is already done:** the model distinguishes 17 material categories,
18 sectors, seven electronics tiers, shelf life, obsolescence, alternative
electronics architectures, process-environment response profiles, source
outages, and alternative process/redundancy/source designs. An executable
acceptance contract now defines the required typed process graph, grade
ladder, critical-part and parent-tool ancestry, source/fleet records,
claim-level evidence, and eight binary closure gates; its public gap register
keeps every row `evidence_pending`. A fail-closed bundle evaluator now checks
the complete graph schema, grade and critical-part coverage, process stages,
evidence hashes, and independently witnessed gate results. It now also
requires non-empty source and fleet registers linked from every source-lot
and transport-leg node. A deterministic complete-shape bundle template is
generated from the live contract and is deliberately invalid until real
measurements, hashes, and results replace its placeholders.

**Why it remains:** these additions are still aggregate assumption structures.
They do not establish mineral recovery, semiconductor or parent-tool
reproduction, or an accessible Moon–asteroid portfolio. This is the review's
central evidentiary criticism and remains the most important technical gap.

**Complete when:**

- source states include mineral form, grade distribution, accessibility,
  recoverable reserve, and uncertainty rather than elemental occurrence
  alone;
- beneficiation, refining, purification, alloying, and waste routes conserve
  chemical species and energy and expose contamination, yield, rework,
  consumables, and tool life;
- material grades distinguish at least bulk, structural alloy, electronic
  grade, semiconductor grade, and ultra-pure process inputs;
- non-substitutable critical part families and production-equipment ancestry
  resolve the gases, chemicals, masks, resists, filters, optics, coatings,
  seals, lubricants, bearings, calibration artifacts, metrology, controls,
  and parent tools that can stop a line despite low mass;
- the minimum external source-vector result is tested against named bodies or
  defensible source classes with composition distributions, delta-v,
  transfer windows, transit time, vehicle cycles, depletion, reserve limits,
  failed sources, and reproducible mining/transport fleets;
- terrestrial process data or experiments calibrate the coefficients and
  uncertainty bounds; until then the output remains an internal-consistency
  certificate for a stipulated closure matrix.

**Evidence:** I.7–I.9; Limitations; Appendix D.1;
`docs/PROCESS_CLOSURE_ACCEPTANCE_CONTRACT.md`;
`process_closure_gap_register.csv`;
`electronics_architecture_comparison.csv`; `environment_process_effects.csv`.

### 3. Execute the terrestrial autonomous-closure and control rehearsal

**What is already done:** the model now specifies delivered-to-operating
states, named autonomy and verification observables, repair and recovery
queues, communication/verification/compute outages, shock policies,
governance authority states, and a threat/control traceability matrix. The
Stage-0 protocol now preregisters a typed raw-event schema, ten binary
acceptance gates, every governance fault plus progressive communication
loss, a 30-day retained second-cell test, and exact model-parameter
replacement mappings. Its checklist contains no unearned pass state.
A fail-closed evaluator now requires every event type, all threat cases,
auditor/archive hashes, witnessed binary results, and complete parameter
replacement records before it can return a campaign result. Its generated
campaign template enumerates every required event, fault, gate, and parameter
record but cannot pass with placeholder data.

**Why it remains:** none of those coefficients or controls has been validated
as an integrated physical system. The article correctly calls Stage 0 a
proposed falsification test, not an accomplished demonstration.

**Complete when:**

- a closed terrestrial site uses the declared lunar material/energy palette
  and prohibits routine human entry;
- every delivered, installed, commissioned, failed, repaired, recovered, and
  operating state has a provenance-preserving build record;
- interventions, task completions, faults, communication loss, verification
  backlog, yields, contamination, consumables, maintenance, calibration,
  repair success, and mean time to recovery are logged;
- the system commissions an auditable second production cell whose
  indispensable subsystems individually pass BOM, construction,
  commissioning, yield, connection, and viable-floor gates;
- injected cyber, insider, authority-loss, common-mode verification, and
  source-integrity faults exercise the proposed rate limits, interlocks,
  safe hold, rollback, compartmentalization, and independent audit;
- measured and failed results replace the corresponding autonomy, deployment,
  repair, environment, electronics, and governance assumptions in the model.

**Evidence:** I.9 Stage 0; Limitations;
`docs/GOVERNANCE_THREAT_MODEL.md`;
`docs/TERRESTRIAL_REHEARSAL_PROTOCOL.md`;
`rehearsal_acceptance_matrix.csv`; knowledge, deployment, repair, and policy
tables.

## Priority 2 — Calibrate the economics rather than adding more mechanics

### 4. Anchor the completed cost boundary and dynamic P3b comparison

**What is already done:** Part II explicitly prices communications, ground
network, spacecraft bus, NRE, insurance, regulation, disposal, residual
value, thermal design, separate financing, and workload-normalized inference
and training. A symmetric dynamic model gives Earth and space the same
investment, learning, depreciation, regulatory-delay, debt, and demand
mechanics. The completed boundary removes the formerly favorable
aspirational crossover, and neither tested space market becomes
self-financing within 40 years. A machine-validated calibration contract now
separates three architecture cases, defines equal-workload evidence, six
engineering/market packages, five correlation groups, an audited cash-flow
event schema, chronological holdout validation, and the rule for promoting
an assumption. Its readiness table is entirely `data_pending`.
A fail-closed evaluator now requires all six evidence packages, all five
correlation fits and holdouts, every cash-flow event type, archive hashes,
and reviewed promotion decisions for every bound parameter.
A generated calibration-release template enumerates every package, fit,
cash-flow event type, and parameter decision while failing closed until
measurements, immutable hashes, holdouts, and independent reviews exist.

**Why it remains:** most newly explicit terms have wide assumption bounds.
Qualification, service life, availability, repairability, insurance,
financing, link performance, and workload throughput are not calibrated as
correlated architecture scenarios. The dynamic comparison is a useful
symmetry test, not evidence for or against mature real-world P3b.

**Complete when:**

- communications and ground costs follow architecture-specific link budgets,
  availability, latency, and regulatory cases;
- qualification, radiation environment, service life, availability,
  repairability, residual value, insurance, and financing are calibrated as
  correlated engineering/market scenarios;
- inference units name a model, precision, batch, memory, latency, accuracy,
  and service level, while training uses a validated topology and
  synchronization/fault model;
- physical construction, replacement, transfer, intervention, and failure
  histories feed audited cash flows;
- Earth resource, grid, water, land, labor, permitting, and geographic
  expansion responses are calibrated symmetrically rather than chosen only
  as scenario coefficients;
- the article reports empirically defensible self-financing boundaries for
  commodity and space-native products, or keeps P3b explicitly unresolved.

**Evidence:** II.2–II.5; Limitations;
`docs/ECONOMIC_CALIBRATION_PROTOCOL.md`;
`economic_calibration_readiness.csv`; `outputs/report_part2.md`;
`symmetric_dynamic_economics.csv`.

## Priority 3 — Finish publication packaging

### 5. Complete and authorize the venue-specific submission packages

**What is already done:** the monograph remains the archival object, and
technical, orbital-compute economics, strategy/governance, and
technical-supplement papers exist. Each selected route has a conformant
abstract, keywords, structure, reference style, resolved core source set, and
explicit proposition boundary. Target/fallback routes are Acta
Astronautica/New Space for the technical paper, Space Policy/New Space for
economics, and Astropolitics/Space Policy for strategy/governance. Publisher
rules are encoded in a machine contract. The final source-to-claim and
target-style audit and the dated public publisher-page recheck were completed
on 2026-07-29. The generated readiness table measures rather than assumes
conformance. An external authorization template binds the selected route,
exact manuscript and supplement hashes, every author confirmation, packaging
action, portal recheck, final approval, and attestation.

**Why it remains:** author identity, correspondence, contribution, funding,
conflict, acknowledgement, permission, AI-use, and final-approval fields
cannot be invented. Immutable release coordinates are absent. The
Astropolitics first-party pages conflict on anonymization, so the
authenticated upload portal must settle that field. Editable exports,
title-page/anonymization packaging, figure and supplement upload, and final
submission actions remain external.

**Complete when:**

- word limits, structure, figures, citation style, anonymization,
  declarations, data/code availability, and supplemental-material rules are
  satisfied;
- proposition boundaries and shared model provenance remain consistent
  across all papers without treating one paper as independent validation of
  another;
- the selected submission packages pass a final source, number, table,
  figure, and artifact cross-check.

**Evidence:** `papers/README.md`; the four r4.0 paper drafts;
`params/publication_targets.yaml`;
`docs/VENUE_SELECTION_AND_CONFORMANCE.md`;
`publication_readiness.csv`.

## Explicitly not pending

The following review recommendations were verified as implemented and are
therefore excluded from this pending-only roadmap: r4.0 identity repair;
strategic-material terminology; aggregate-doubling and terminal-window
vocabulary; design-space rather than probability language; long-horizon
endpoints; sector-resolved dynamics; independent allocation; explicit
repair and cohorts; delivered-seed states; observable autonomy regimes;
environment response profiles; finite mass and shell debris; policy and
shock sweeps; tiered electronics shelf life; completed Part II boundary and
workload units; symmetric dynamic economics; composition-changing Pareto
search; governance threat/control traceability; the machine claim glossary;
claim-level provenance for every retained non-assumption anchor; permanent
SEC page/slide pinning for [S27]; explicit `ASSUMPTION` demotion of ranges
whose exact endpoints and transformations are analyst-constructed; and the
companion-paper split and venue selection. Expansion for the unselected New
Space fallback routes is contingent future work, not an active r4.0 blocker.
