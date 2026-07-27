# rsi-model

Public repository: https://github.com/fperegrinvs/rsi-model — release `r3.4`.
Canonical manuscript: `docs/Recursive_Industrial_Intelligence_3rd_Ed_r3.4.md`
(Appendix C: reproducibility; Appendix D: full model specification).
License: MIT (code) + CC BY 4.0 (docs). DOI: [10.5281/zenodo.21619447](https://doi.org/10.5281/zenodo.21619447).

Simulation companion to *Recursive Industrial Intelligence* (Second Edition, current rev r2.10 — see `docs/`).
Third Edition Parts I–II: multisector closure feasibility + Earth–space cost crossover.

Start with `CLAUDE.md` (project rules and roadmap), then:

    pip install -r requirements.txt
    python scripts/run_baseline.py    # Part I smoke sweep (~2 min)
    python scripts/run_part2.py       # Part II LCO sweep (~1 min)
    python scripts/run_deep.py        # large-n MC + cut probabilities (~20 min)
    pytest tests/ -q

Reports land in `outputs/`; Parts III–IV are documents in `docs/`.

Key discipline: system replication time is a model **output**, never an input;
structural coefficients are ASSUMPTION-class and live only in named sets.
