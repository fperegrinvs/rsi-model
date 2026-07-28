# rsi-model

Companion repository for *Recursive Industrial Intelligence* r4.0.

- Canonical source: `docs/Recursive_Industrial_Intelligence_r4.0.md`
- Standalone HTML: `docs/Recursive_Industrial_Intelligence_r4.0.html`
- Pending-only roadmap: `ROADMAP.md`
- License: MIT for code and CC BY 4.0 for documents
- Concept DOI: [10.5281/zenodo.21619447](https://doi.org/10.5281/zenodo.21619447)

The repository combines a multisector industrial-closure model, an
Earth–space compute-cost comparison, and an 18-sector/17-material
integrated-bootstrap model. Structural coefficients remain
`ASSUMPTION`-class unless a source is explicitly recorded; generated results
are scenario implications, not measurements, probabilities, engineering
estimates, or forecasts.

## Reproduce the release candidate

Python 3.13, Node.js 22, and Pandoc 3 or newer are required.

```sh
python -m venv .venv
.venv/bin/pip install --require-hashes -r requirements.lock
.venv/bin/python scripts/run_baseline.py
.venv/bin/python scripts/run_part2.py
.venv/bin/python scripts/run_deep.py
.venv/bin/python scripts/run_integrated.py
.venv/bin/python scripts/write_claim_provenance.py
npm run build:manuscript
.venv/bin/python scripts/write_manifest.py
.venv/bin/python scripts/verify_manifests.py
.venv/bin/python scripts/release_preflight.py --mode candidate
.venv/bin/pytest tests/ -q
```

Generated reports, tables, and figures live under `outputs/`. The canonical
`outputs/MANIFEST.md` binds the manuscript, HTML, release inputs, and
generated artifacts. `outputs/integrated/MANIFEST.md` provides an additional
content-addressed record for the integrated-model run.

The untagged HTML intentionally omits a publication date, version DOI, and
canonical public URL. For immutable publication, regenerate it with:

```sh
RELEASE_DATE=YYYY-MM-DD \
VERSION_DOI=10.5281/zenodo.VERSION \
CANONICAL_URL=https://zenodo.org/records/VERSION \
npm run build:manuscript
```

Release and paper submission authorization records stay outside Git. The
templates are deliberately non-passing:

```sh
.venv/bin/python scripts/release_preflight.py \
  --write-authorization-template /secure/path/r4.0-release-authorization.json
.venv/bin/python scripts/publication_preflight.py \
  --write-authorization-template /secure/path/r4.0-paper-authorization.json
```

Evidence-bundle evaluation also requires the local archive that backs every
declared digest:

```sh
.venv/bin/python scripts/evaluate_evidence_bundle.py process_closure \
  /secure/path/process-closure-bundle.json \
  --archive-root /secure/path/process-closure-archive
```
