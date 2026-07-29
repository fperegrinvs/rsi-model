# rsi-model

Companion repository for *Recursive Industrial Intelligence* r4.0.

- Editable manuscript source: ordered fragments in `docs/manuscript/`
- Generated monolithic Markdown: `docs/Recursive_Industrial_Intelligence_r4.0.md`
- Generated standalone HTML: `docs/Recursive_Industrial_Intelligence_r4.0.html`
- Reader site: Quarto project in `site/`, generated into untracked `_site/`
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

Python 3.13.0, uv 0.9.18, Bun 1.3.14, pnpm 11.17.0, Pandoc 3.10.1, and
Quarto 1.9.38 are the pinned CI toolchain. Bun runs the TypeScript publication
tools, pnpm installs their locked dependencies, Pandoc creates the archival
self-contained HTML, and Quarto creates the multi-page GitHub Pages edition
from the same ordered fragments.

```sh
uv sync --locked --all-groups
pnpm install --frozen-lockfile
pnpm run check:dependencies
uv run --locked rsi-run-baseline --output-dir outputs
uv run --locked rsi-run-part2 --output-dir outputs
uv run --locked rsi-run-deep --output-dir outputs
uv run --locked rsi-run-integrated
uv run --locked rsi-write-provenance --project-root .
pnpm run check:notation
pnpm run check:prose
pnpm run check:scenario-policy
pnpm run check:propositions
pnpm run check:readability
pnpm run build:manuscript
pnpm run build:site
pnpm run check:site
pnpm run check:accessibility
pnpm run check:footnotes
pnpm run quality:python
pnpm run test:coverage
pnpm run check:package
pnpm run audit
pnpm run sbom
uv run --locked rsi-write-manifest --project-root .
uv run --locked rsi-verify-manifests --project-root .
uv run --locked rsi-release-preflight --project-root . --mode candidate
pnpm test
```

`pnpm run check:package` builds both distributions, then imports the wheel and
checks all installed maintenance commands from an isolated temporary
environment outside the checkout. `pnpm run audit` scans the fully resolved
Python environment; `pnpm audit` covers the locked publication toolchain.
`pnpm run sbom` writes the reproducible CycloneDX record to
`outputs/quality/sbom.cdx.json`.

Generated reports, tables, and figures live under `outputs/`. The canonical
`outputs/MANIFEST.md` binds the manuscript, HTML, release inputs, and
generated artifacts. `outputs/integrated/MANIFEST.md` provides an additional
content-addressed record for the integrated-model run.

The fragments are the only hand-edited manuscript source. The monolithic
Markdown, standalone HTML, and `_site/` tree are deterministic products; do
not edit them directly. The publication workflow crawls every Quarto page,
checks internal assets and fragments, compares equation/table/figure/source
counts against the standalone HTML, and deploys `_site/` to GitHub Pages after
a non-pull-request build passes. The configured project URL is
<https://fperegrinvs.github.io/rsi-model/>.

That Pages root is the mutable reader edition for the latest reviewed state
on `main`; it is not the immutable r4.0 archive. The immutable edition is the
tagged release plus its versioned archival record and DOI. The project does
not promise a fixed `/r4.0/` Pages path until the workflow can retain and
verify multiple version trees. External-link availability is reported
separately with `pnpm run check:external-links`; transient third-party failure
does not override a byte-valid local publication build.

The untagged HTML intentionally omits a publication date, version DOI, and
canonical public URL. For immutable publication, regenerate it with:

```sh
RELEASE_DATE=YYYY-MM-DD \
VERSION_DOI=10.5281/zenodo.VERSION \
CANONICAL_URL=https://zenodo.org/records/VERSION \
pnpm run build:manuscript
```

Release and paper submission authorization records stay outside Git. The
templates are deliberately non-passing:

```sh
uv run --locked rsi-release-preflight --project-root . \
  --write-authorization-template /secure/path/r4.0-release-authorization.json
uv run --locked rsi-publication-preflight \
  --write-authorization-template /secure/path/r4.0-paper-authorization.json
```

Evidence-bundle evaluation also requires the local archive that backs every
declared digest:

```sh
uv run --locked rsi-evaluate-evidence process_closure \
  /secure/path/process-closure-bundle.json \
  --archive-root /secure/path/process-closure-archive
```
