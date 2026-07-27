# RSI Model — Third Edition Simulation

Companion codebase to *"Recursive Industrial Intelligence, Second Edition"*, current
revision **r2.10** (docx in `docs/`; r2.8 FINAL kept alongside; the paper's [S28] is
this repo). Goal: replace the paper's decorative equations with an executed model,
producing the Third Edition's Parts I–II quantitative core.

## What this project is

The paper argues about self-sustaining / self-expanding (space) industrial systems. External review
(see `docs/REVIEW_NOTES.md`) established that its scalar quantities are invalid as measurements:

- **Replication time r is UNKNOWN.** PV energy-payback (~1 yr), NASA-1980's ~1 yr design estimate,
  and Gigafactory Shanghai's 10-month buildout measure three different phenomena. Never present a
  single r; compute it as a model *output*.
- **Closure κ must be a VECTOR** (per sector) with minimum-cut-set analysis, not a scalar.
- **δ must be decomposed**: wear + catastrophic + obsolescence + logistics. Space raises
  catastrophic + logistics; Earth raises obsolescence; wear differs only ~2–3×.
- **Self-expansion criterion**: feasible positive net growth in EVERY indispensable sector,
  not aggregate growth.

## Epistemic rules (non-negotiable, inherited from the paper's review cycle)

1. Every parameter carries a `source_class`: `peer_reviewed | technical_report | company_statement |
   reporting | ASSUMPTION`. Anchored values live in `params/anchors.yaml` (traceable to the paper's
   Appendix A). Unanchored coefficients (the requirement matrix A, closure-investment efficiency,
   maintenance shares) are `ASSUMPTION`-class and exist only inside named assumption sets
   (`params/assumptions.yaml`: conservative / central / optimistic). Never silently invent a number.
2. Results are reported as sweeps across assumption sets + Monte Carlo over anchored ranges —
   never a single trajectory presented as "the" answer.
3. Company targets are evidence of intent, not feasibility. Do not use them as capacity inputs.
4. Outputs must state which sector binds (the active minimum cut), not just aggregate growth.

## Architecture

- `src/rsimodel/model.py` — 10-sector capacity dynamics (incl. repair & recycling as
  service sectors). Per timestep, a lexicographic maximin LP (scipy linprog): maximize
  the worst-case sector growth rate g over builds x, wear-repair u, recycling activity w,
  stock drawdown d; then, at fixed g, minimize drawdown (stock is a buffer, not fuel).
  dK_j = x_j + u_j − δ_j·K_j. Per-sector import cutoffs (electronics-class scenarios),
  Mars synodic pulse deliveries, Poisson common-cause shocks (pass an rng to enable).
- `src/rsimodel/delta.py` — δ assembled per environment as wear + catastrophic +
  obsolescence + logistics from `params/environments.yaml`; anchored entries resolve
  to geometric mids (or loguniform draws under MC) with per-value Provenance records.
- `src/rsimodel/cutsets.py` — minimal import cut sets (monotone lattice enumeration
  with superset pruning) + indispensable-sector knockouts.
- `src/rsimodel/montecarlo.py` — samples anchored ranges (one shared draw per anchor
  per run), runs ensembles: P(self-expanding by T), binding-sector histogram,
  survival curves, P(expansion) vs import-decay sweep.
- `src/rsimodel/report.py` — markdown report with full parameter provenance table.
- `src/rsimodel/lco.py` — Part II levelized cost: LEO inference / cislunar batch /
  lunar-surface compute vs. a RESPONDING terrestrial counterfactual (tight/base/
  responsive with nuclear-PPA floor and older-node option, compute-normalized).
  $ per frontier-equivalent kW-yr; affine in launch $/kg so break-evens are exact;
  anchored MC with shared draws both sides; crossover_grid over any anchor axis.
- `scripts/run_baseline.py` — Part I smoke run + figures (~2 min).
- `scripts/run_deep.py` — large-n Part I MC + cut-set fatality probabilities (~20 min).
- `scripts/run_part2.py` — Part II sweep + report (~1 min).
- `docs/PART_III_HYPOTHESES.md` — H0–H3 likelihood-ratio assessment (document).
- `docs/PART_IV_SPECULATIVE.md` — quarantined Section 16 scenarios + model checks.
- `docs/transcripts/` — primary-source transcripts with provenance headers
  (external claims land in `anchors.yaml` under `claims:` — comparison targets,
  never model inputs).

Conventions: numpy-style everything, no classes where a dataclass + functions do, type hints,
figures via `plots.py` only, all randomness through a passed `numpy.random.Generator`.

## Roadmap (Third Edition Parts I–IV) — see ROADMAP.md for task-level detail

- **Part I (this repo, priority):** harden the multisector model — correlated failures,
  vitamin-part stockpiles with shelf life, repair/recycling sectors, three location
  architectures (LEO / lunar surface / Mars), minimum-cut-set finder, Monte Carlo with
  survival curves.
- **Part II:** LCO models with real mass/power budgets; crossover surface over
  (launch $/kg × closure × equipment life × radiator kg/kW); Earth counterfactual that
  *responds* (induced supply, nuclear PPAs, older nodes).
- **Part III (document work, not code):** H0–H3 likelihood-ratio assessment.
- **Part IV (document):** speculative scenarios, quarantined.

## Running

    pip install -r requirements.txt
    python scripts/run_baseline.py          # smoke test + figures
    pytest tests/ -q

## Current status

Parts I–IV complete (v1); Third Edition manuscript at **r3.4**
(`docs/Recursive_Industrial_Intelligence_3rd_Ed_r3.4.md` + .docx) — canonical
(Second Edition frozen at r2.11; earlier revision docx kept for provenance).
r3.4 = model-integrity/audit pass against a second external review: LEO
relabeled an import-supported orbital recycling network (finite capture
reservoir unmodeled — see ROADMAP r3.4 block); doubling denominators split
(headline: 39% of central lunar runs double then lose viability — the
import-ramp trap); Appendix D full model spec incl. central A matrix;
cost inclusion/exclusion accounting; financing equalization declared
pro-space; H0 redefined, independent actors (E12/E15) moved to
cross-checks, III.5 ordinal; retooling metric computed
(`cutsets.retooling_time`: 90% electronics/machine-tools stranding FATAL
under both allocators — vitamin gap makes rebuild a multi-decade-payback
asset); stable crc32 seeds (hash() was process-salted). 35 tests pass. Reports: `outputs/report.md` (Part I
baseline), `outputs/report_deep.md` (large-n MC + cut-set fatality),
`outputs/report_part2.md` (LCO), `docs/PART_III_HYPOTHESES.md`,
`docs/PART_IV_SPECULATIVE.md`.

Headline structure (ASSUMPTION-class inputs — sweep, don't quote):
- **Part I**: electronics binds in ~85–97 % of MC steps in every location;
  conservative fails everywhere, central marginal (P(expanding@30yr) ≈ 0.5–0.8
  with shocks), optimistic expands. Recycling indispensable in LEO only. Over
  sampled anchors the electronics import line ALONE is fatal in ~15 % of
  otherwise-viable central LEO/lunar draws and ~80 % on Mars (pulsed imports +
  deepest vitamin gap) — the probabilistic minimum cut, location-dependent. The
  vitamin gap (closure.space_electronics_q_scale, 0.10–0.30 ASSUMPTION range)
  drives most results.
- **Part II**: at published launch prices space compute is ~5–9× Earth (lunar
  ~300×); P(space cheaper) ≈ 0 over the anchored ensemble even vs the responsive
  Earth. Break-even launch price is often NEGATIVE (qual premium + short life
  dominate, not launch). Crossover needs qual≈1.2 + life≈7yr + high utilization
  + target-class $/kg simultaneously. Earth base LCO ≈ $1.7/kW-hr — matches
  published accelerator rentals (calibration check).
- **Part III**: current evidence does not establish H1 over H0/H2; the model
  makes the discriminating indicators operational (see ranked list).

Next (Fourth Edition candidates): see end of ROADMAP.md.
