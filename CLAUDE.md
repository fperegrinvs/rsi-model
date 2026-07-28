# RSI Model

Companion codebase for *Recursive Industrial Intelligence* r4.0. The
canonical manuscript is `docs/Recursive_Industrial_Intelligence_r4.0.md`;
the standalone HTML uses the same stem. The project does not generate a PDF.

## Epistemic rules

1. Every input is classified as `peer_reviewed`, `technical_report`,
   `reporting`, `company_statement`, or `ASSUMPTION`.
2. Unanchored structural coefficients belong only in named assumption sets.
3. Report sweeps and ensemble counts as implications of the declared design
   space, never as real-world probabilities.
4. Company targets establish intent, not feasibility.
5. System replication time is an output. The headline metric is balanced
   doubling, `min_j K_j(t)/K_j(0) >= 2`, not aggregate capacity.
6. Report the active minimum cut and co-binding structure, not only aggregate
   growth.

## Architecture

- `src/rsimodel/model.py`: ten-sector capacity, repair, recycling, stocks,
  imports, shocks, and allocation.
- `src/rsimodel/lco.py`: workload-normalized Earth–space compute economics.
- `src/rsimodel/integrated.py`: 18-sector, 17-material seed sizing, autonomy,
  source balances, commissioning, and dynamic growth.
- `src/rsimodel/integrated_analysis.py`: terminal diagnostics, ablations,
  policy and architecture sweeps, shell debris, symmetric economics, and
  robust-seed design.
- `scripts/run_baseline.py`, `run_part2.py`, `run_deep.py`, and
  `run_integrated.py`: deterministic artifact generators.
- `params/`: anchored inputs, assumption sets, evidence contracts, and
  publication requirements.
- `outputs/`: generated reports, tables, figures, and manifests.

## Verification

```sh
python scripts/run_baseline.py
python scripts/run_part2.py
python scripts/run_deep.py
python scripts/run_integrated.py
python scripts/write_claim_provenance.py
npm run build:manuscript
python scripts/write_manifest.py
python scripts/verify_manifests.py
python scripts/release_preflight.py --mode candidate
pytest tests/ -q
```

Do not hand-edit generated artifacts. Regenerate them from the corresponding
script. Keep `ROADMAP.md` limited to material work that is both unfinished
and non-obsolete.
