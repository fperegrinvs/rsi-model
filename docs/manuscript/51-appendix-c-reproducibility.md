# Appendix C: Reproducibility {#appendix-c-reproducibility}

    corepack pnpm install --frozen-lockfile
    corepack pnpm run setup:local-tools
    corepack pnpm run candidate:macos:update  # regenerate and review
    corepack pnpm run candidate:macos         # strict clean reproduction

Model: `src/rsimodel/{model,delta,cutsets,montecarlo,lco,policies,plots,report}.py`;
parameters: `params/{anchors,assumptions,environments}.yaml`; generated
reports with per-run provenance tables and machine-readable CSV summaries:
`outputs/` (headline table: [deep Monte Carlo table](../outputs/tables/mc_deep.csv){.artifact-link data-artifact="outputs/tables/mc_deep.csv"}). Stages 1–2 of
each allocation use HiGHS through a persistent warm-started model, with
`scipy.optimize.linprog` as the retained reference/fallback path and
`RSI_SLOW_LP=1` to force it. Stage 3 uses the pinned OSQP solver for the
strictly convex normalized tie-breaker, with a numerical fallback. All randomness
flows through explicitly seeded `numpy.random.Generator` instances; every
script derives its seeds from stable crc32 strings (never Python's
process-salted `hash()`), and each anchor's Monte Carlo
draw is keyed by the run seed plus the anchor's NAME, so results are stable
both across processes and under anchor-list growth. All tables regenerate
deterministically within the pinned Apple-silicon macOS reference environment.
`outputs/MANIFEST.md` records the sha256 of every release artifact,
including the canonical Markdown and standalone HTML, plus library versions;
it omits a self-referential generating-commit field. `tests/test_repro.py` cross-checks
the committed CSV against the committed report so mutually stale artifacts
fail the suite. `outputs/report_deep.md` and
[deep Monte Carlo table](../outputs/tables/mc_deep.csv){.artifact-link data-artifact="outputs/tables/mc_deep.csv"} are written by a single execution of one
script and cannot diverge. Structural coefficients are ASSUMPTION-class and
live only inside named assumption sets.

The integrated model is `src/rsimodel/integrated.py`, with the
analysis module in `src/rsimodel/integrated_analysis.py`, configured entirely
by `params/integrated_model.yaml` and run by the installed
`rsi-run-integrated` command.
`outputs/integrated/report.md`, 33 CSV tables, and five figures are
generated from one in-memory scenario set. `outputs/integrated/MANIFEST.md` records the
sha256 of the configuration, implementation, runner, focused tests, and
every generated artifact. Its ensemble uses 200 deterministic named draws
per scenario from seed 404. Adding a draw or changing a coefficient changes
the manifest; none of that upgrades an assumption to evidence.

**Archival status.** Public repository:
**[rsi-model repository](https://github.com/fperegrinvs/rsi-model)**. r4.0
is assembled as a release candidate but is not yet represented by a clean
release commit or tag; this text does not claim otherwise. The untagged
r4.0 HTML omits canonical/public URL,
publication-date, and `citation_doi` metadata rather than pointing at
mutable `blob/main` or mislabeling the concept DOI. The final tagged build
must supply an immutable URL, release date, and version DOI through the
documented build environment variables.
Dependency lockfile: `uv.lock` (numpy 2.1.3, scipy
1.16.0 [HiGHS], OSQP 1.1.3, PyYAML 6.0.3, matplotlib
3.10.3, pytest 9.0.3; Python 3.13.0 reference environment; complete
transitive pins and artifact hashes). The TypeScript publication toolchain
uses Bun 1.3.14, pnpm 11.17.0, and the checked `pnpm-lock.yaml`. Citation metadata:
`CITATION.cff`. License: MIT for code (`/LICENSE`), CC BY 4.0 for the
manuscript and documents (`docs/LICENSE`). DOI: concept
**10.5281/zenodo.21619447** (all versions); each release tag mints its own
version DOI via the Zenodo integration. The test suite covers selected
invariants, determinism, metric identities, artifact consistency, and the
generated HTML's semantic publication structure — they do not establish
that the specification adequately represents industrial reality, and no
test suite could.
