# RSI Model

Companion codebase for *Recursive Industrial Intelligence* r4.0. Ordered
Markdown fragments in `docs/manuscript/` are the editable source of truth.
The same source generates the monolithic Markdown and standalone HTML in
`docs/` and the multi-page Quarto site in untracked `_site/`. The project does
not generate a PDF.

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
7. Every `##` section in the Part I–IV manuscript fragments ends with a
   conclusion paragraph stating the section's structural claim, what binds,
   and its epistemic class, per Rule 2 in `docs/EDITORIAL_STYLE.md`. Execute
   that rule's LLM validation protocol on every new version.

## Architecture

- `src/rsimodel/model.py`: ten-sector capacity, repair, recycling, stocks,
  imports, shocks, and allocation.
- `src/rsimodel/lco.py`: workload-normalized Earth–space compute economics.
- `src/rsimodel/integrated.py`: 18-sector, 17-material seed sizing, autonomy,
  source balances, commissioning, and dynamic growth.
- `src/rsimodel/integrated_analysis.py`: terminal diagnostics, ablations,
  policy and architecture sweeps, shell debris, symmetric economics, and
  robust-seed design.
- `src/rsimodel/extensions.py`: diminishing digital progress, data-profile
  scalarization, coordination topology, embodiment compatibility, partial
  closure, orbital lifecycle, and common-cause controls.
- Installed `rsi-run-baseline`, `rsi-run-part2`, `rsi-run-deep`, and
  `rsi-run-integrated` commands: deterministic artifact generators.
- `params/`: anchored inputs, assumption sets, evidence contracts, and
  publication requirements.
- `outputs/`: generated reports, tables, figures, and manifests.
- `docs/manuscript/`: ordered editable manuscript fragments.
- `site/`: Quarto 1.9.38 book configuration and thin fragment wrappers.

## Verification

```sh
uv sync --locked --all-groups
pnpm install --frozen-lockfile
uv run --locked rsi-run-baseline --output-dir outputs
uv run --locked rsi-run-part2 --output-dir outputs
uv run --locked rsi-run-deep --output-dir outputs
uv run --locked rsi-run-integrated
uv run --locked rsi-write-provenance --project-root .
pnpm run check:dependencies
pnpm run check:notation
pnpm run check:prose
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

Do not hand-edit generated artifacts, including the monolithic manuscript,
standalone HTML, or `_site/`. Regenerate them from the corresponding script.
Keep `ROADMAP.md` limited to material work that is both unfinished and
non-obsolete.
