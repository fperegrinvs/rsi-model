# Fourth Edition Release Ledger

**Final manuscript:** `docs/Recursive_Industrial_Intelligence_4th_Ed_r4.0.md`

**Preserved working draft:** `docs/Recursive_Industrial_Intelligence_4th_Edition_DRAFT_r4.0.md`

**Frozen baseline:** `docs/Recursive_Industrial_Intelligence_3rd_Ed_r3.5.md`

**Baseline SHA-256:** `c90341094e5522d72471b77113de98d0250ba16c96d011a5662e79baf620c20c`

**Opened:** 2026-07-27

**Completed:** 2026-07-27

## Editorial contract

- [x] Preserve Third Edition r3.5 unchanged as the release baseline.
- [x] Make the Fourth Edition standalone: it inherits the complete r3.5
      argument, models, results, appendices, and source record.
- [x] Use the separately named r4.0 working draft while the new quantitative
      program is incomplete; preserve it when the final manuscript is cut.
- [x] Do not publish the final Fourth Edition until every release gate below
      is closed or explicitly deferred in the manuscript.
- [x] Do not create a parallel r3.6 unless a factual or integrity correction
      to the frozen Third Edition is independently required.
- [x] Publish r4.0 as canonical Markdown plus standalone HTML only; do not
      generate or commit a Fourth Edition PDF.

## A. Conceptual changes to integrate in r4.0

- [x] **Exogenous versus endogenous compute growth.** Distinguish
      Earth-manufactured orbital deployment from off-world reproduction:
      `dC_orbit/dt = q_c L_E→O - δ_C C_orbit` versus
      `dH/dt = (r - δ_H)H`.
- [x] **Causal correction.** State explicitly that off-Earth location does
      not itself cause acceleration; reproductive closure causes endogenous
      growth, while off-Earth operation relaxes terrestrial land,
      biosphere, siting, and political scaling constraints.
- [x] **Machine-only reference scope.** The reference industrial ecology
      does not require human settlement, agriculture, or biosphere-scale
      life support. Water, carbon, hydrogen, and nitrogen remain industrial
      inputs even in an uncrewed system.
- [x] **Gravity as a process variable.** Distinguish processes that tolerate
      microgravity, benefit from lunar gravity, or require local centrifugal
      acceleration. Do not assume either universal 1g or zero artificial
      gravity for the entire industrial ecology.
- [x] **Embodied-autonomy threshold.** Separate robotic degrees of freedom
      from the intelligence required for unscripted diagnosis, tool use,
      repair, construction, recovery, learning, and verification.
- [x] **Four-layer industrial seed.** Define the physical seed, digital
      seed, industrial memory, and experimental capacity. Replace the
      impossible standard of encoding “all industrial knowledge” with a
      sufficient operating foundation plus the capacity to generate missing
      knowledge experimentally.
- [x] **Terrestrial autonomous-closure rehearsal.** Add Stage 0: use the
      lunar material and energy palette, prohibit routine human entry, log
      interventions, inject faults and communication outages, and require
      the system to construct and commission a second production cell.
- [x] **Moon–Earth–asteroid material architecture.** Treat the Moon as the
      initial bulk-material backbone; Earth as the early supplier of
      low-mass, high-criticality “vitamins”; and asteroids as a later source
      of diversity, volatiles, and supply sovereignty—not as a prerequisite
      for lunar iron.
- [x] **Lunar inventory sanity check.** Include an explicitly illustrative,
      non-reserve calculation using approximately 1.5 t/m³ regolith bulk
      density and approximately 3 wt% highlands iron.
- [x] **Industrial-knowledge stack.** Add software, simulation, toolchains,
      recipes, material models, failure records, and build records to the
      strategy stack.
- [x] **New falsifiable indicators.** Add the terrestrial seed demonstrator,
      autonomous second-cell commissioning, machine-readable seed package,
      unscripted recovery, human-intervention intensity, and element-level
      closure.

## B. Quantitative Fourth Edition work

- [x] **Element-resolved material model.** Add element-by-sector bills of
      material `B[e,j]`, source yields `Y[s,e]`, element-level recovery and
      recycling, and transfer arcs among Earth, lunar surface, orbit, and
      asteroidal sources.
- [x] **Seed-sizing optimization.** Minimize delivered seed mass subject to
      survival, commissioning, second-cell construction, and staged import
      withdrawal.
- [x] **Embodied-autonomy model.** Represent task coverage and autonomous
      recovery as constraints on robotics, repair, machine tools, mining,
      and construction; expose residual human-intervention demand.
- [x] **Process-environment compatibility.** Implement process-specific
      gravity and local-centrifuge mass/power overhead. Vacuum, temperature,
      dust, radiation, granular mechanics, and maintenance-rate coupling are
      explicitly deferred in Limitations because no defensible coefficient
      set was established; r4.0 does not silently treat them as solved.
- [x] **Coupled intelligence–industry loop.** Operationalize stylized `f`
      and `h` functions and couple operating cells into local compute and
      Moon→orbit deployment. Dynamic coupling into Part II's monetary cost
      model is explicitly deferred, so P3b remains unpriced.
- [x] **Terrestrial build-rate counterfactual.** Model Earth deployment as a
      rate-limited process, not only a price scenario.
- [x] **Dynamics omitted by r3.5.** Add construction and transport lags,
      commissioning delays, yield ramps, minimum viable scale, and explicit
      production-cell reproduction.
- [x] **Electronics decomposition.** Split the homogeneous electronics
      sector into non-substitutable tiers and connect each tier to
      element/process requirements.
- [x] **Coupled lunar surface–orbit architecture.** Replace isolated
      locations with a production graph and explicit transfer arcs.
- [x] **Asteroid follow-on cases.** Test when additional source diversity
      becomes operationally load-bearing. Complete economics are explicitly
      deferred with P3b.
- [x] **Endogenous orbital-debris dynamics.** Condition orbital scale on a
      subcritical debris regime rather than a fixed exogenous event rate.

## C. Claim and source discipline

- [x] Preserve all r3.5 computed values as inherited Third Edition results
      until regenerated by a changed model.
- [x] Label every new materials quantity as inventory, concentration,
      occurrence, resource, reserve, or modeled flow; never substitute one
      category for another.
- [x] Cite lunar bulk composition, regolith density, highlands iron,
      volatile uncertainty, and asteroid sample composition from primary or
      authoritative sources.
- [x] State that current lunar ISRU demonstrations are prototype/subsystem
      demonstrations and do not establish autonomous industrial closure.
- [x] State that the inherited ten-sector model cannot determine lunar
      elemental sufficiency or the date at which asteroid supply is needed.
- [x] Keep claimed current robot capability separate from assumed future
      AI-enabled capability; do not use a named robot platform as evidence
      that unscripted industrial autonomy has been demonstrated.

## D. Release gates

- [x] Fourth title, abstract, scope, limitations, revision history, glossary,
      and source record identify the document consistently as r4.0.
- [x] No stale statement says that the Fourth Edition is merely future work.
- [x] All internal stage, proposition, appendix, and source references pass.
- [x] Baseline r3.5 SHA-256 still matches the value recorded above.
- [x] Final Markdown publication build succeeds without modifying r3.5 artifacts.
- [x] Publication policy is encoded in `package.json`, README, Appendix C,
      and this ledger: `npm run build:fourth` is HTML-only.
- [x] New model artifacts regenerate deterministically
      and receive their own checksummed manifest.
- [x] Final editorial audit maps every checked item in this ledger to a
      manuscript section, model artifact, or explicit deferral.

## E. r3.5 release-integrity review applied to r4.0

- [x] **Inline mathematics and Pandoc citation corruption.** Converted all
      72 inherited `\(...\)` pairs to Pandoc-supported dollar delimiters;
      removed the `@35` table token; regenerated 103 MathML expressions;
      added regression checks for the reported malformed patterns, duplicate
      IDs, and unresolved internal targets.
- [x] **Stale inherited conclusions.** Replaced LEO recycling-sector
      indispensability with capture-and-recovery feed-loop dependence;
      replaced universal-electronics language with architecture-specific
      bottlenecks; qualified lunar speed versus LEO durability; removed the
      invalid “9% of total capacity” aggregation and unique-moat inference.
- [x] **Inherited-model boundary.** Elevated the complete abstract seed,
      continuous fractional capacity, and omitted lag/commissioning/ramp/
      minimum-scale boundary to the Abstract and immediately before the
      inherited result table; recast the allocator as an idealized,
      perfectly informed coordination benchmark.
- [x] **AI1 reconstructibility.** Documented the exact aggregate-mass rule:
      scale the generic engineering budget proportionally, use its resulting
      hardware/infrastructure shares for lifecycle accounting, retain
      generic component capex, and label both the split and serviceability
      `ASSUMPTION`.
- [x] **S27 filing metadata.** Separated the May 20 S-1
      (0001628280-26-036936) from the June 4 Rule 433 FWP
      (0001628280-26-040610) and linked both SEC records.
- [x] **S36 bibliographic criticism disposition.** Added a prominent
      calibration-provenance boundary in Limitations, Appendix A, and S36.
      The claim-level source register is **explicitly deferred** rather than
      misrepresented as complete: several inherited interval endpoints still
      need exact title/date/location/permanent-link/extraction records before
      an independently source-audited academic quantitative release.
- [x] **Noisy clock curve.** Softened the $n=60$ sweep to suggestive and
      expressly withdrew any stable steepness estimate.
- [x] **Displayed denominator and cutoff labels.** Stated that the second
      doubling denominator is machine-readable rather than visible and
      expanded the Earth-import-cut table headings.
- [x] **Scenario prose.** Repaired the collector-area fragment and retained
      “demanding unanchored conditions” rather than polemical language.
- [x] **Runtime and release metadata.** Reconciled the deep-run note at
      706.6 seconds on nine workers on the 2026-07-27 release host, with
      explicit hardware dependence. Untagged HTML now omits a
      mutable canonical URL, publication date, and version DOI; the concept
      DOI is labeled as such. Clean-clone Linux reproduction, immutable tag,
      archive, and version DOI are **external release actions deferred**
      until publication, not simulated in the manuscript.

## Integration map

| change | manuscript location |
|---|---|
| exogenous deployment versus endogenous growth; causal correction | Executive Summary; I.3 |
| machine-only scope and residual volatile chemistry | Scope and Status; I.9; III.6 |
| gravity and local centrifugal acceleration | I.3; I.7–I.8; Limitations; Appendix D.1; `process_profile`; YAML `environment` |
| embodied-autonomy threshold | I.2; I.7–I.8; III.5–III.6; Limitations; Appendix D.1; `process_profile`; seed LP |
| physical, digital, memory, and experimental seed | I.2; I.5; III.1; III.5; Glossary |
| terrestrial autonomous-closure rehearsal and second cell | I.9 Stage 0; II.1; III.5; Limitations; Glossary |
| Moon–Earth–asteroid material sequence | I.7–I.9; Limitations; Appendix D.1; YAML source yields and transfer arcs |
| lunar inventory sanity check | I.9; S51–S55 |
| ISRU demonstration boundary | I.9; S57 |
| element-resolved flows and seed sizing | I.7–I.8; Limitations; Appendix D.1; `src/rsimodel/fourth.py`; `outputs/fourth/tables/` |
| electronics tiers | I.7; Appendix D.1; YAML `sectors`; element-flow tables |
| construction, commissioning, and explicit second cell | I.8–I.9; Appendix D.1; `simulate_reproduction`; cell-reproduction figure |
| coupled intelligence, compute, and rate-limited Earth deployment | Executive Summary; I.8; III.6; Appendix D.1; compute-curves table and figure |
| stateful debris threshold | Executive Summary; I.8; Limitations; Appendix D.1; debris table and figure |
| deferred environment and monetary couplings | Limitations; Scope/P3b; Appendix D.1 |
| new strategy observables | III.1; III.5 |
| standalone/editorial status | title block; Abstract; Appendix B; this ledger |

## Audit record

- r3.5 SHA-256 rechecked: `c90341094e5522d72471b77113de98d0250ba16c96d011a5662e79baf620c20c`.
- Source definitions are contiguous and unique from S1 through S57; each
  new source S51–S57 is cited in the body.
- Focused Fourth Edition suite passed: 8 tests.
- `scripts/run_fourth.py` generated one internally consistent report, six
  CSV tables, four figures, and a sha256 manifest from the same in-memory
  run (200 named deterministic draws per scenario, seed 404).
- Central scenario record: terrestrial rehearsal 206.7 t / second cell 9.2
  yr; lunar vitamin bridge 216.7 t / 11.2 yr; strict lunar infeasible;
  Moon–asteroid network 185.5 t / 22.8 yr. These are scenario implications.
- Final standalone HTML build passed with 103 native MathML expressions, 18
  tables, correct r4.0 title/edition metadata, intentionally absent
  pre-release canonical/version metadata, and no unconverted `$$`
  delimiters. Per project policy, no Fourth Edition PDF was retained.
- Full suite passed: 72 tests in 13.47 seconds.
- All 15 paths in `outputs/fourth/MANIFEST.md` were rehashed and matched.
- Source definitions are contiguous and unique from S1 through S57.
- r3.5 SHA-256 rechecked after the r4.0 build and still matches the frozen
  baseline value above.
- `git diff --check` passed without warnings; generated CSVs use LF line
  endings in both artifact sets.

## Change log

- **2026-07-27:** Ledger opened; r3.5 frozen; standalone r4.0 working draft
  copied from the complete r3.5 source.
- **2026-07-27:** Conceptual integration and source pass completed; all
  quantitative Fourth Edition items remained visibly pending in Section B.
- **2026-07-27:** Implemented and tested the Fourth model; generated its
  separate artifact set and manifest; integrated the computed central and
  ensemble results into the final standalone manuscript with explicit
  assumption and deferral boundaries.
- **2026-07-27:** Registered Markdown + standalone HTML as the publication
  format, completed the 72-test and manifest audit, rechecked the frozen
  r3.5 hash, and closed every release gate.
