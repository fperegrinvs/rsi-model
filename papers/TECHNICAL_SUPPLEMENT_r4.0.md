# r4.0 technical supplement and repository map

This supplement keeps material that conventional venue limits would remove
from the three submission papers. The canonical archival object remains
`docs/Recursive_Industrial_Intelligence_r4.0.md`.

## Reproducibility

```bash
uv sync --locked --all-groups
pnpm install --frozen-lockfile
pnpm run generate:baseline
pnpm run generate:part2
pnpm run generate:deep
pnpm run generate:integrated
uv run --locked rsi-write-provenance --project-root .
pnpm run build:manuscript
pnpm run build:site
uv run --locked rsi-write-manifest --project-root .
uv run --locked rsi-verify-manifests --project-root .
pnpm run test:coverage
pnpm run test:typescript
```

Generated artifacts are hash-listed in `outputs/MANIFEST.md` and
`outputs/integrated/MANIFEST.md`. Exact solver values remain in CSV; narrative
papers round assumption-conditioned outputs.

## Model specification

- ten-sector baseline: `src/rsimodel/model.py` and
  `params/environments.yaml`;
- Part II cost model: `src/rsimodel/lco.py` and `params/anchors.yaml`;
- Integrated bootstrap: `src/rsimodel/integrated.py` and
  `params/integrated_model.yaml`;
- Integrated diagnostics: `src/rsimodel/integrated_analysis.py`;
- governance traceability: `params/governance_controls.yaml`;
- process-closure acceptance: `params/process_closure_requirements.yaml`;
- Stage-0 execution contract: `params/rehearsal_protocol.yaml`;
- economic-calibration contract: `params/economic_calibration.yaml`; and
- claim-level provenance: `params/claim_provenance.yaml`.
- venue and submission conformance: `params/publication_targets.yaml`.

The complete matrices, sector definitions, source yields, scenario
coefficients, uncertainty ranges, and tests are machine-readable at those
paths. The repository implementation controls where prose and code differ.

## Extended diagnostics

The supplement retains:

- seed-sector and material-flow tables;
- commissioning and sector trajectories;
- import-stock composition and shelf-life results;
- ablation and operational-regime tables;
- allocation, repair, shock, and policy sweeps;
- environment-response profiles;
- shell-resolved debris and finite mass accounting;
- symmetric dynamic economics;
- dominated and non-dominated robust-seed designs;
- full ensemble diagnostics and sensitivity screens;
- strict-lunar elastic infeasibility cuts.
- pending-only registers for process closure, the physical rehearsal, and
  economic calibration.
- venue-specific publication readiness and author-confirmation gates.

## Provenance boundary

Claim status and input source class are distinct. A model output is
`computed`; its coefficient may still be `ASSUMPTION`. The current source
register gives every retained non-`ASSUMPTION` anchor exact
author/organization, title, date, locator, persistent identifier, extracted
value, units, and transformation. Reporting-derived Part II ranges whose
endpoints were not directly supported were demoted to `ASSUMPTION`; their
contextual sources do not promote them back to empirical inputs.

## Glossary

- **Aggregate operating-capacity doubling:** every indispensable sector
  reaches two seed-normalized operating equivalents.
- **Delivered seed:** installed-seed mass plus deployment packaging,
  equipment, calibration, spares, and startup-energy storage.
- **Internal-consistency certificate:** a feasible solution inside a
  stipulated matrix; not proof that coefficients are achievable.
- **Strategic-material bridge:** substantial finite imported feedstock,
  distinct from trace parts or catalysts.
- **Terminal-window expanding:** positive capacity change over the declared
  final window; not an indefinite durability claim.
- **Design-space occupancy:** count under the declared sampling measure; not a
  success probability.
- **Source class:** provenance category of an input.
- **Claim status:** documented, announced, technically grounded, computed,
  inferred, or speculative status of a statement.

## Auxiliary material

Provisional hiring and observability material remains repository context
rather than evidence. Extended debris and governance discussions remain here
and in their machine-readable artifacts.
