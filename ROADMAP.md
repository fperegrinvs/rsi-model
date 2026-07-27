# Roadmap — Third Edition

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
      Headline: P(space cheaper) ≈ 0 over the anchored ensemble in all cases;
      crossover needs the unanchored qual/life/util corner AND target-class
      launch prices simultaneously

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
- [ ] Anchor the vitamin gap: any traceable datum on off-world-producible
      electronics tiers (the single most results-driving number)
- [x] Retooling-speed metric (`cutsets.retooling_time`, 2026-07-27): 90%
      electronics/machine-tools stranding is FATAL at central and optimistic
      values under both myopic and receding-horizon allocation — the vitamin
      gap makes replacement capacity a multi-decade-payback asset; only
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
