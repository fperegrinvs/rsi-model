# rsi-model

Public repository: https://github.com/fperegrinvs/rsi-model — r4.0 release
candidate (publish the tag only after regeneration and verification).
Canonical source: `docs/Recursive_Industrial_Intelligence_4th_Ed_r4.0.md`.
Primary reading edition: `docs/Recursive_Industrial_Intelligence_4th_Ed_r4.0.html`
(Appendix C: reproducibility; Appendix D: full model specification).
The r4.0 publication target is Markdown plus standalone HTML only; the
project does not generate or commit a Fourth Edition PDF.
License: MIT (code) + CC BY 4.0 (docs). Concept DOI (all versions):
[10.5281/zenodo.21619447](https://doi.org/10.5281/zenodo.21619447).

Companion model to *Recursive Industrial Intelligence, Fourth Edition*
(r4.0, `docs/`; the complete Third Edition r3.5 is frozen and retained as
the inherited quantitative baseline). Executable layers: multisector
closure feasibility, Earth–space compute cost crossover, and the Fourth
Edition's 18-sector/17-material autonomous-bootstrap model. Parts III–IV
are documents in `docs/`.

Start with `CLAUDE.md` (project rules and roadmap), then:

    python -m venv .venv
    .venv/bin/pip install -r requirements.lock
    .venv/bin/python scripts/run_baseline.py
    .venv/bin/python scripts/run_part2.py
    .venv/bin/python scripts/run_deep.py
    .venv/bin/python scripts/run_fourth.py
    npm run build:manuscript -- --html-only
    npm run build:fourth
    .venv/bin/python scripts/write_manifest.py  # run last
    .venv/bin/pytest tests/ -q

Reports land in `outputs/`; `outputs/MANIFEST.md` records the sha256 of every
inherited r3.5 artifact. It deliberately omits an embedded Git commit hash,
which would create a circular release artifact.
`outputs/fourth/MANIFEST.md` independently hashes the Fourth Edition
configuration, implementation, tests, report, six CSV tables, and four
figures. `report_deep.md` and
`tables/mc_deep.csv` are written by a single execution of `run_deep.py` and
cross-checked by `tests/test_repro.py`, so mutually stale artifacts fail CI.

To build the web-first manuscript:

    npm install
    npm run build:manuscript -- --html-only
    npm run build:fourth

Pandoc 3 or newer is also required (`PANDOC_BIN=/path/to/pandoc` may be used
when it is not on `PATH`). Equations are emitted as native MathML, so the HTML
does not depend on a JavaScript formula renderer.

The untagged release-candidate HTML intentionally omits
`citation_publication_date`, `citation_doi`, and canonical/public-URL
metadata. At immutable publication, regenerate it with all three release
values:

    RELEASE_DATE=YYYY-MM-DD VERSION_DOI=10.5281/zenodo.VERSION \
      CANONICAL_URL=https://immutable-version-url npm run build:fourth

Key discipline: system replication time is a model **output**, never an input
(headline metric: balanced-capacity doubling, λ(t) =
min_j K_j(t)/K_j(0) ≥ 2 — unit-invariant and not a commissioned physical
copy); structural coefficients are ASSUMPTION-class and live only in named
sets; all seeds are stable crc32 strings, never process-salted `hash()`.
Fourth Edition optimized masses and ensemble frequencies are implications
of the declared architecture and draws—not engineering estimates,
measurements, success probabilities, or forecasts.
