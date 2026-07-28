# r4.0 publication set

The canonical repository manuscript remains the archival monograph:
`docs/Recursive_Industrial_Intelligence_r4.0.md`.

The submission set separates three arguments that must not validate one
another:

| Artifact | Propositions addressed | Propositions not established |
|---|---|---|
| `TECHNICAL_PAPER_r4.0.md` | P1 conceptual possibility; conditional P2 requirements and failure boundaries | real-world industrial closure; corporate intent; economic superiority |
| `ORBITAL_COMPUTE_ECONOMICS_r4.0.md` | P3a bridge-economy orbital-compute boundary; conditions relevant to P3b | physical industrial closure; corporate coordination |
| `STRATEGY_GOVERNANCE_CASE_STUDY_r4.0.md` | P4a declared direction; tests for P4b; governance requirements | technical feasibility; economic competitiveness; validated safety |
| `TECHNICAL_SUPPLEMENT_r4.0.md` | model/release cross-reference, glossary, provenance and extended diagnostics | independent empirical evidence |

The selected routes are:

| Artifact | Target | Fallback |
|---|---|---|
| `TECHNICAL_PAPER_r4.0.md` | Acta Astronautica, Original research paper | New Space, Original Article |
| `ORBITAL_COMPUTE_ECONOMICS_r4.0.md` | Space Policy, full-length paper | New Space, Perspective |
| `STRATEGY_GOVERNANCE_CASE_STUDY_r4.0.md` | Astropolitics, Research Article | Space Policy, case study |
| `TECHNICAL_SUPPLEMENT_r4.0.md` | supplement to the technical paper | repository archive |

The authoritative requirements and current readiness results are
`params/publication_targets.yaml`,
`docs/VENUE_SELECTION_AND_CONFORMANCE.md`, and
`outputs/integrated/tables/publication_readiness.csv`. Venue names are selected;
submission is not authorized. The drafts now contain a checked core citation
set; final source-to-claim and target-style review, live-portal checks,
immutable release coordinates, and
author-controlled identity, contribution, funding, conflict, permission,
acknowledgement, and AI-use statements remain pending.
New Space expansion is a contingency only if a selected target route is
changed to its fallback.

The current external authorization shape is generated and checked with
`scripts/publication_preflight.py`. It binds author approval and packaging
evidence to the exact paper hashes without placing private correspondence or
signature material in the repository.
