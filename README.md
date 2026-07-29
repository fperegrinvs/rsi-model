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

The canonical artifact-generation environment is Apple-silicon macOS with
Python 3.13.0, uv 0.9.18, Bun 1.3.14, pnpm 11.17.0, Pandoc 3.10.1, and
Quarto 1.9.38. Bun runs the TypeScript publication tools, pnpm installs their
locked dependencies, Pandoc creates the archival self-contained HTML, and
Quarto creates the multi-page GitHub Pages edition from the same ordered
fragments. The setup command downloads the pinned Quarto archive, verifies its
sha256, and installs it under the ignored `.tools/` directory.

```sh
corepack pnpm install --frozen-lockfile
corepack pnpm run setup:local-tools
corepack pnpm run candidate:macos:update
# Review and commit the regenerated files, then prove clean reproduction:
corepack pnpm run candidate:macos
```

The candidate command regenerates every model artifact, provenance record,
manifest, standalone document, and reader page; runs all Python and TypeScript
tests, package and dependency audits, and three-browser publication checks;
and rejects tracked drift in strict mode. It records the exact commit,
toolchain, platform, duration, and result in the ignored
`outputs/quality/candidate-audit.json`. `pnpm run check:package` also imports
the built wheel and exercises every installed maintenance command from an
isolated temporary environment outside the checkout.

Generated reports, tables, and figures live under `outputs/`. The canonical
`outputs/MANIFEST.md` binds the manuscript, HTML, release inputs, and
generated artifacts. `outputs/integrated/MANIFEST.md` provides an additional
content-addressed record for the integrated-model run.
The local Apple-silicon macOS candidate command is the sole canonical
artifact-generation workflow. GitHub Actions runs only when manually
dispatched: it verifies the committed artifacts and can deploy the reader
site, but it never regenerates or redefines the numerical outputs.

The fragments are the only hand-edited manuscript source. The monolithic
Markdown, standalone HTML, and `_site/` tree are deterministic products; do
not edit them directly. The local candidate workflow crawls every Quarto page,
checks internal assets and fragments, and compares
equation/table/figure/source counts against the standalone HTML. A successful
manual workflow dispatch from `main` can deploy `_site/` to GitHub Pages. The
configured project URL is
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
