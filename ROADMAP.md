# Roadmap — Inherited Third Edition and Fourth Edition follow-ups

## Part I: Technical feasibility (this repo, priority order)
- [x] Wire anchors.yaml ranges into Monte Carlo (loguniform, one shared draw per anchor per run)
- [x] Vitamin-part stockpiles: shelf-life state, electronics-class cutoff scenarios
- [x] Decomposed delta per environment (wear/catastrophic/obsolescence/logistics) — `params/environments.yaml`, `delta.py`
- [x] Correlated failures (common-cause Poisson shocks across sector groups)
- [x] Repair & recycling as explicit sectors (9th/10th, service sectors in the LP)
- [x] Minimum-cut-set finder over the A matrix + import profile — `cutsets.py`
- [x] Three location architectures: LEO / lunar surface / Mars (env-specific delta, q_scale, imports; Mars synodic pulses)
- [x] Survival curves + P(expansion) vs import_decay_years sweep
- [x] Report generator: figures + parameter provenance table per run — `report.py` → `outputs/report.md`

### Part I follow-ups (found during implementation)
- [x] Vitamin-gap q_scale is now an explicit ASSUMPTION-class anchored RANGE
      (closure.space_electronics_q_scale, 0.10–0.30, bounding argument in the note),
      sampled by MC with provenance. Still unanchored to any measurement — replacing
      it with a traceable number remains open for a Fourth Edition
- [x] Cut-set fatality over sampled anchors (cutsets.cut_probability): electronics
      import line alone fatal in ~15% of otherwise-viable central LEO/lunar draws
      and ~80% on Mars (n=40 per case, report_deep.md)
- [x] Larger-n MC: scripts/run_deep.py (n=120 ensembles, n=60 sweep) → report_deep.md

## Part II: Comparative economics — COMPLETE (v1)
- [x] lco.py rewritten with sourced mass/power budgets (anchors.yaml launch/
      power_systems/compute/earth sections, each with source_class)
- [x] Three reference cases (LEO inference / cislunar batch / lunar surface) with
      break-even tables — break-even is EXACT (LCO is affine in launch $/kg)
- [x] Dynamic terrestrial counterfactual: tight/base/responsive (nuclear-PPA floor,
      older-node option, compute-normalized by J/FLOP penalty)
- [x] Crossover surface: launch $/kg x {equipment life, space-qual multiplier,
      radiator kg/kW, closure fraction} → outputs/report_part2.md
      Headline: P(space cheaper) = 0/2000 for the three original references;
      Starmind AI1/base = 1/2000. Generic LEO favorable-corner break-even
      ≈$444/kg; AI1 favorable-corner break-even ≈$1,152/kg. Both remain
      conditional on qualification/life/utilization values not disclosed by
      the AI1 page
- [x] Deterministic AI1 aspirational best case: company targets $185/kg and
      100 kW/t plus explicitly non-company favorable bounds (qualification
      1.2x, life 7 yr, utilization .95). Result 0.76x Earth base versus 1.85x
      for the company targets alone; excluded from MC. Feasibility audit:
      100 GW/year implies 1M t/year, 10,000 V3 or 5,000 V4 launches/year.

## Publication pipeline — COMPLETE
- [x] Make standalone HTML the primary reading edition while retaining
      Markdown as the canonical editable source
- [x] Render equations to native MathML and preserve semantic HTML tables
- [x] Add responsive screen/print styles and a table of contents; r4.0
      publication is registered as Markdown + standalone HTML only, with no
      generated or committed PDF
- [x] Add structural regression coverage for the generated HTML

### r3.5 review follow-ups
Absorbed in r3.5 (2026-07-27): stable crc32 seeds everywhere incl. Part II;
AnchorSet draw caching (shared draws real); λ(t)=min_j K_j/K_j(0) balanced
doubling as headline metric (Σ K relabeled aggregate); endpoint hierarchy
(realized post-shock / pre-shock allocation diagnostic / sustained 25–30 /
Earth-import cutoff, with continued capture feed named in LEO); unit-invariant
finite 1% binding response with co-binding credit unified across baseline
and policy comparison; recoverable retirement by loss type and environment;
strictly convex stage-3 tie-break for a unique state transition;
Part II component-specific lives (infrastructure_life_years ASSUMPTION
anchor) plus explicit serviceable/reusable and integrated-disposable cases;
lunar case relabeled Earth-supplied; single-execution CSV+report
with sha256 MANIFEST and generated-vs-committed consistency tests; deep run
process-parallelized (fixed per-stage seeds → bit-identical); retooling
language horizon-relative; textual pass (E12, LR wording, S-1 → SEC-filed
materials, satellite threshold, lockfile syntax); Starmind AI1 added as a
separate company-statement architecture scenario (direct specifications
preserved, peak/average mass ambiguity explicit, undisclosed costs retained
from the generic anchors); deterministic company-aspiration case added and
quarantined from MC, with non-company favorable inputs and cadence burden
made explicit; performance pass — persistent warm-started
HiGHS model in allocate_step (~10×, ≈1e-15-equivalent to the retained
scipy reference path, RSI_SLOW_LP=1 to force it), chunked MC cells over
the process pool (deep run measured at 706.6 s on nine workers on the
2026-07-27 release host; hardware-dependent), and name-keyed anchor
draws (anchor additions never re-roll existing cells; one-time
re-baseline). Remaining:
- [ ] **Electronics decomposition** (the big one): split the sector into
      non-substitutable tiers — interconnects/boards; passives+power;
      sensors/control; packaging+test; mature-node logic; advanced
      logic+memory; process equipment+metrology — as distinct A-matrix
      columns/minimum-cut nodes rather than one homogeneous q multiplier.
      Requires new ASSUMPTION-class shares with bounding arguments (authorial
      sign-off; do NOT invent silently). Until then the electronics-binds
      result is conditional on the homogeneous-multiplier implementation.
- [ ] Minimum-viable-scale floor for the autonomy endpoint (needs an
      authorial threshold; endpoint 4 currently = sustained g>0 over the
      import-free window with stock drawdown permitted)
- [ ] Part II: communications/downlink cost case and residual-value
      treatment
- [ ] Full pip-compile lockfile with transitive hashes; CI job that
      regenerates artifacts on the release tag and diffs MANIFEST.md
- [ ] S27 page-level pins to the FWP/prospectus sections quoted in E6
- [ ] Longer-horizon retooling recovery tests + knock-fraction sweep
      (removes the 20-yr-window qualifier from the model-fatal label)

### r3.4 review follow-ups (model integrity)
- [ ] LEO embodied-mass conservation: explicit finite orbital-matter reservoir
      state (M += imports + capture − unrecoverable loss; recycled ≤ η·retired,
      η<1 already enforced), kg-per-capacity-unit conversion layer, and
      depletion of the capture feed — until then LEO results are labeled
      import-supported recycling network, conditional on feed availability
- [ ] Minimum viable sector scale / no-failure-path survival criterion
      (g>0 at horizon does not preclude near-zero absolute capacity)
- [ ] Stage-3 lexicographic surplus pinning (removes LP vertex indeterminacy
      in total-capacity trajectories; prerequisite for capacity-based
      retooling metrics)
- [ ] Part II financing separation: distinct Earth vs space WACC distributions
      (currently equalized — a deliberate assumption favoring space)
- [ ] Sensitivity repeated across all environments/sets with
      interaction-capable methods (Shapley/grouped); Part II sensitivity
      ranking displayed
- [ ] Itemized per-anchor citations replacing the S36 collective reference

## Part III: Strategy interpretation (document, not code) — COMPLETE (v1)
- [x] docs/PART_III_HYPOTHESES.md: H0–H3 likelihood-ratio table per evidence item,
      updated with Part I/II results; ranked discriminating indicators

## Part IV: Speculative scenarios (document) — COMPLETE (v1)
- [x] docs/PART_IV_SPECULATIVE.md: Section 16 ported, quarantined, each scenario
      annotated with model checks from Parts I–II

## Fourth Edition candidates (surfaced during this work)

The consolidated editorial, model, source, and release checklist now lives
in `docs/FOURTH_EDITION_PLAN.md`. That ledger is authoritative for the
standalone r4.0 release; the items below retain deeper-fidelity work beyond
the bounded Fourth Edition implementation.

The r4.0 layer now provides element-resolved seed sizing, electronics tiers,
gravity/centrifuge overhead, construction and commissioning, explicit
Earth–Moon–orbit–asteroid arcs, rate-limited Earth deployment, a stylized
intelligence–compute loop, and aggregate active/derelict/fragment debris
dynamics. The unchecked items below ask for higher-resolution physical,
economic, and orbital-environment models; they are not silent omissions
from r4.0 and are listed in that edition's Limitations.

- [ ] **Endogenous orbital-debris / Kessler model:** replace the fixed-rate
      exogenous `debris_event` as the only cascade proxy with per-shell stocks
      of active assets, intact derelicts, trackable/untrackable fragments,
      density-dependent collision kernels, fragmentation yield, cross-shell
      transport, avoidance-capacity limits, atmospheric/natural clearance,
      controlled disposal, retrieval/recycling, and active removal. Report a
      debris reproduction ratio and condition every LEO scale result on the
      subcritical regime. No new rates are authorized by the current source
      record; see `docs/sources/lunar-surface-orbit-architecture-2026-07-27.md`.
- [ ] **Coupled lunar surface–orbit architecture:** represent the surface as
      the material, shielding, storage, and heavy-industry backbone and a
      sparse LLO/NRHO/DRO layer as communications, navigation, transport,
      assembly, and service nodes. Add explicit transfer arcs and compare the
      hybrid with the current isolated lunar-surface and cislunar cost cases;
      do not infer transfer/productivity coefficients without authorial
      sign-off or anchor-grade sources.
- [ ] **Post-lunar heliocentric architecture:** test a distributed set of
      separated heliocentric orbital elements and resource trajectories after
      lunar export capacity exists, rather than a dense replacement shell.
      Keep terminology exact: Earth Sun-synchronous orbit is still an
      Earth-orbit/LEO architecture, not the post-lunar destination.
- [ ] Anchor the vitamin gap: any traceable datum on off-world-producible
      electronics tiers (the single most results-driving number)
- [x] Retooling-speed metric (`cutsets.retooling_time`, 2026-07-27): 90%
      electronics/machine-tools stranding is MODEL-FATAL (unrecovered within
      the tested 20-yr window while the counterfactual stays positive) at
      central and optimistic values under both myopic and receding-horizon
      allocation — the vitamin gap makes replacement capacity a
      multi-decade-payback asset; only
      power stranding at optimistic values is a finite delay (~27 yr).
      Follow-ups: stage-3 surplus-pinning lexicographic objective (removes
      LP vertex indeterminacy in total-capacity trajectories), knock-fraction
      sweep, MC over the stranding analysis
- [ ] Obsolescence term conditional on architectural convergence (Part IV
      scenario 2's upgrade asymmetry as a parameter regime, not a new default)
- [ ] LCO: radiation-environment-resolved life model (LEO vs cislunar vs lunar
      surface currently share one life anchor)
- [ ] Earth political-constraint scenario, now parameterized: Situational
      Awareness ch. IIIa (docs/sources/) supplies the politics-yields branch
      (CCGT <$1000/kW, ~2yr build, gas floor 0.04-0.06 $/kWh — wired into the
      responsive scenario 2026-07-27) and frames tight-vs-responsive as
      politics-binds vs politics-yields. Remaining work: a buildout-RATE cap
      (GW/yr) rather than a price scenario — the Moonshots #266 siting/water
      argument is about rate, not price level
- [ ] Split space_qual_multiplier by workload class: COTS inference at benign
      LEO (Planet practice, low end ~1.2) vs hardened/training-class (unanchored
      high end) — the single lever the Google/Planet crossover claim turns on.
      r2.10 [S32] proton-beam TPU data (HBM sensitivity beyond shielded 5-yr dose)
      is the first anchor-grade datum for this split
- [ ] Junction temperature as an explicit radiator parameter (r2.10 §16 names
      chip efficiency + junction temp + radiator kg/kW as first-class; we now
      carry the first and third — T^4 radiator sizing vs reliability is missing)
- [ ] r2.10 Appendix A restructure (A.1-A.3 by measured quantity, with
      what-it-does-NOT-measure columns) is the normalization discipline
      delta.py/anchors.yaml already implement; consider adding a quantity_type
      field to anchors so the report can print the A.1-style type column
