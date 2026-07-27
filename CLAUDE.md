# RSI Model — Fourth Edition Simulation

Companion codebase to *Recursive Industrial Intelligence, Fourth Edition*,
current revision **r4.0** (canonical Markdown + standalone HTML in `docs/`;
no PDF release artifact). The complete Third Edition r3.5 model and
manuscript remain frozen as the inherited quantitative baseline; the Second
Edition is frozen at r2.11 for provenance. The paper's [S28] is this repo.

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
  anchored MC with shared draws both sides; current AI1 disclosure case plus a
  deterministic company-aspiration best case excluded from MC; crossover_grid
  over any anchor axis.
- `src/rsimodel/fourth.py` — separate Fourth Edition 18-sector,
  17-material integrated-bootstrap layer: element BOM/source balances,
  seed-sizing LP, task autonomy/intervention, process-specific gravity,
  commissioning and explicit second-cell dynamics, compute/intelligence
  coupling, rate-limited Earth/orbit counterfactuals, and debris stocks.
- `scripts/run_baseline.py` — Part I smoke run + figures (~30 s).
- `scripts/run_deep.py` — large-n Part I MC + cut-set fatality probabilities
  (measured 706.6 s on nine workers on the 2026-07-27 release host;
  hardware-dependent process pool over chunked cells + persistent HiGHS).
- `scripts/run_part2.py` — Part II sweep + report (~10 s).
- `scripts/run_fourth.py` — Fourth Edition central scenarios, named
  200-draw ensembles, tables, figures, report, and separate sha256 manifest.
- `scripts/build_manuscript.cjs` — Markdown → self-contained HTML with MathML;
  `npm run build:fourth` selects r4.0. HTML only; no PDF output path.
- `docs/PART_III_HYPOTHESES.md` — H0–H3 likelihood-ratio assessment (document).
- `docs/PART_IV_SPECULATIVE.md` — quarantined Section 16 scenarios + model checks.
- `docs/transcripts/` — primary-source transcripts with provenance headers
  (external claims land in `anchors.yaml` under `claims:` — comparison targets,
  never baseline inputs).

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
    python scripts/run_baseline.py          # inherited smoke test + figures
    python scripts/run_fourth.py            # integrated-bootstrap artifacts
    pytest tests/ -q
    npm run build:fourth                    # r4.0 standalone HTML only

## Current status

Parts I–IV and the bounded integrated-bootstrap layer are complete for the
**r4.0 release candidate**. Canonical source:
`docs/Recursive_Industrial_Intelligence_4th_Ed_r4.0.md`; primary reading
artifact: the same stem with `.html`. r3.5 is frozen as the inherited
baseline; r3.4 is retained for provenance.

r4.0 adds the explicit physical/digital seed, source network, electronics
tiers, autonomy and gravity constraints, second-cell commissioning,
rate-limited Earth/orbit comparison, stylized intelligence/compute loop,
and aggregate debris threshold. `outputs/fourth/MANIFEST.md` binds its
configuration, implementation, tests, report, six tables, and four figures.
Every new structural coefficient is ASSUMPTION-class. The untagged HTML
omits canonical URL, publication date, and version DOI until immutable
release metadata is supplied.

r4.0 RC correction pass (2026-07-28, against a fourth external review):
seed restated as INSTALLED operating nucleus; reproduction metric renamed
first passage to two operating-cell equivalents with year-40 durability
reading; model relabeled material-category-resolved; strict-lunar 0/200
restated as structural LP infeasibility; R_debris renamed five-year
fragment creation-to-clearance ratio (sub/supercritical language
withdrawn); three stale Third Edition passages removed (I.3/I.4/I.5);
vitamin share (23–27%) reported; import-decay sweep committed
(`outputs/tables/import_decay_deep.csv`, run_deep.py now writes it);
Appendix A reconciled with anchors.yaml (five-class taxonomy, 14 missing
anchors added, context rows marked); "two orders of magnitude" lunar
closure claim corrected to ~15–30×; 8 figures embedded in manuscript and
HTML (build uses --resource-path=.:docs); P1–P6/I.10/I.4/Suncatcher/
Terafab walls restructured; "How to read this document" added; r4.1
model work (durable endpoints, ablations, Pareto, diagnostics,
delivered-seed stage) queued in ROADMAP.

r3.5 = reproducibility/model-identity pass against a third external review
(all its factual claims verified against the repo before acting): stable
crc32 seeds everywhere incl. Part II (hash() was process-salted and r3.4's
committed CSV/report were from DIFFERENT runs — rerun_cells.py deleted, one
script now writes both); AnchorSet caches draws (the stated Earth/space
shared-draw correlation is now real); headline replication metric is
BALANCED doubling λ(t)=min_j K_j/K_j(0) ≥ 2 (unit-invariant; Σ K relabeled
"aggregate"); endpoint hierarchy (instantaneous / sustained 25–30 /
import-cutoff autonomy probe) — this exposed central-Mars "expansion" as
substantially a synodic-pulse artifact (273/400 instantaneous vs 62/400
sustained, median λ@30 = 0.54); binding sector = stage-1 LP shadow price,
same definition in baseline and policy comparison (Mars binding split
electronics ~62%/power ~38% under duals); Part II component lives split
(new infrastructure_life_years ASSUMPTION anchor — central LCOs fell:
LEO ≈58k, lunar ≈2.8M $/kW-yr), lunar case relabeled "Earth-supplied",
exclusion bias no longer claimed uniformly pro-space; "recycling
indispensable in LEO" WITHDRAWN (stale r3.3-era output; post-r3.4 capture
feed makes the knockout survivable — feed-loop dependence is the surviving
claim); retooling now "model-fatal within tested 20-yr window".
SPEED (r3.5 final pass): allocate_step uses a persistent warm-started
HiGHS model via scipy's bundled highspy (~10×, verified ≈1e-15 vs the
retained linprog reference path; RSI_SLOW_LP=1 forces the reference);
run_deep.py fans 4×100-run chunks per cell over a process pool → full
deep run measured 706.6 s on nine workers on the 2026-07-27 release host
(hardware-dependent; formerly ~40 min serial); anchor draws keyed by
(run seed, anchor NAME) via delta.anchor_child_rng, so adding anchors to
anchors.yaml NEVER re-rolls existing cells (old sequential stream did —
that plus chunking re-baselined all MC values once, within Wilson).
outputs/MANIFEST.md sha256 manifest;
tests/test_repro.py cross-checks committed CSV vs report. The full r4.0
suite has 72 tests.
Reports: `outputs/report.md`, `outputs/report_deep.md`,
`outputs/report_part2.md`, `docs/PART_III_HYPOTHESES.md`,
`docs/PART_IV_SPECULATIVE.md`.

Headline structure (ASSUMPTION-class inputs — sweep, don't quote):
- **Inherited Part I**: central finite-response co-binding assigns about
  98% to capture/mining in LEO, 96% to electronics on the Moon, and
  62% electronics / 38% power on Mars. Central expanding@30 is 267/400,
  224/400, and 60/400; sustained years 25–30 is 122/400, 20/400, and
  4/400. Quote ensemble counts as stipulated frequencies, never
  probabilities.
- **Part II**: generic space ~4–9× Earth at published prices (Earth-supplied
  lunar ~200×); the separate Starmind AI1 company-statement scenario uses its
  disclosed 150/120 kW, 150 kW array, and 70 kW/t specifications, reducing
  central mass 46→16 kg/kW and cost to 2.56× Earth. P(space cheaper) is
  0/2000 in all sixteen architecture/reference cells (an earlier 1/2000
  note for AI1/base was stale). With qual=1.2, life=7 yr, utilization=.95 AI1 breaks even at
  ~$1,152/kg and is 0.79× at $250/kg. Qualification/life/availability
  remain undisclosed. A separate deterministic best case uses company targets
  $185/kg and 100 kW/t plus those three favorable non-company bounds: 0.76×
  Earth versus 1.85× if the undisclosed inputs stay central. It is excluded
  from MC. Its 100-GW/year scale implies 1M t/year and 10,000 V3 launches/year.
  Earth base ≈$1.67/kW-hr.
- **Part III**: P4a documented, P4b not established; indicators ordinal.
- **Fourth layer**: central terrestrial rehearsal 206.7 t installed /
  first passage to two cell-equivalents 9.25 yr (holds only 1.93 at yr
  40); lunar vitamin bridge 216.7 t (58.1 t = 27% Earth vitamin stock) /
  11.25 yr; strict lunar structurally infeasible (LP infeasible, all 200
  draws); Moon–asteroid network 185.5 t / 22.75 yr. Seeds are INSTALLED
  operating nuclei (no deployment stage); the model is
  material-category-resolved (15 elements + rare-earth/dopant classes);
  R_debris is a five-year fragment creation-to-clearance flow ratio, not
  a criticality measure. These are scenario implications of the declared
  architecture, not engineering estimates.

Next: ROADMAP higher-fidelity block (claim-level anchor bibliography,
vacuum/dust/radiation process coupling, mineralogy and purity ladders,
shell-resolved debris, dynamic monetary coupling, Linux clean-clone
reproduction, tag/archive/version DOI).
