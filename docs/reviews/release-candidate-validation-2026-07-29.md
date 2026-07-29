# Release-candidate validation — 2026-07-29

Status: repository-controlled candidate pipeline passes; clean remote release
and publication remain pending.

## Scope

This review distinguishes a complete local candidate build from the
authority-bearing immutable release. It does not treat a dirty development
tree, a local simulation, or a generated authorization template as evidence
of a clean Linux run, author approval, archive publication, or journal
submission.

## Generation and publication builds

The pinned workflow regenerated:

- the baseline multisector model;
- the Part II economic comparison;
- the full 400-run-per-cell deep ensemble;
- the integrated 18-sector/17-material model;
- claim-level provenance;
- the standalone archival HTML; and
- the Quarto reader site.

The integrated run was repeated after release-tool source changes and
reproduced the same central results: 206.9286 t for the terrestrial rehearsal,
217.0229 t for the lunar strategic-material bridge, strict lunar infeasibility,
and 187.9296 t with a 35.25-year aggregate doubling time for the
Moon–asteroid network.

## Passing local gates

The following evidence passed on the current worktree:

- 255 Python tests;
- 17 Bun tests with 467 assertions;
- 85.30% aggregate branch-aware coverage and all 11 critical-module floors;
- Ruff, Python formatting, Pyright, TypeScript, Biome, Markdown, YAML, and
  GitHub Actions lint;
- sdist, wheel, isolated import, and all 17 installed console entry points;
- pnpm and Python dependency audits with no known dependency
  vulnerabilities;
- reproducible CycloneDX SBOM generation;
- notation, prose, propositions, scenario policy, readability, figures,
  tables, footnotes, equation explanations, and pinned math-font checks;
- Chromium, Firefox, and WebKit math layout;
- site crawl, accessibility, artifact-viewer, table, figure, and print-layout
  checks;
- 103 external links checked, with none unavailable and 27
  restricted/transient responses reported separately;
- three AI-R&D sources refreshed without change; and
- 380 top-level plus 190 integrated manifest records verified byte-for-byte.

Candidate preflight passes with `--allow-dirty`, which intentionally evaluates
every candidate gate while reporting the development-tree exception.

## Release-tool failure behavior

Publication mode requires `RELEASE_DATE`, `VERSION_DOI`, and `CANONICAL_URL`.
The CLI now reports their absence as a concise invalid-metadata error with
exit status 2 instead of exposing an unhandled traceback. A regression test
covers this fail-closed behavior.

## Remote and authority audit

Read-only GitHub inspection found:

- local branch `main` at `e15354d6e76b779045ade2e3155b740d547f3de4`;
- remote `main` at `2ac2a15c343cb3097c082f34c5264e3607b6b6ae`;
- the publication workflow absent from the remote default branch;
- no GitHub Actions workflows or runs in the repository; and
- no local `r4.0` tag.

The worktree contains extensive tracked and untracked changes from the
current improvement program. Therefore no current commit can be described as
the reviewed release state, and the strict clean-tree candidate gate remains
correctly non-passing.

The generated release-authorization template also confirms that these
external facts are absent: approved commit, passing Linux run and evidence,
archive record, release date, version DOI, canonical URL, responsible
approver, and attestation.

The generated publication-authorization template correctly binds the three
paper and supplement hashes. It remains non-passing because author
confirmations, packaging actions, immutable coordinates, portal evidence,
final approvals, approvers, timestamps, and attestations have not been
supplied.

## External empirical-evidence audit

Complete-shape templates were regenerated for all three evidence programs and
passed back through their fail-closed evaluators with an empty archive root.
All three were rejected, as required:

- process closure lacks the calibrated typed graph, assays, grade and species
  transitions, process distributions, source/fleet records, immutable
  evidence hashes, and eight witnessed gate results;
- the terrestrial rehearsal lacks signed event telemetry, material and energy
  custody, fault injections, raw archive and auditor hashes, ten witnessed
  gate results, and parameter-replacement decisions; and
- economic calibration lacks six normalized evidence packages, five
  correlation fits and holdouts, dated cash-flow event records, archive
  hashes, and independently reviewed parameter decisions.

These failures are positive evidence that placeholders cannot satisfy the
three empirical TODOs. Completing them requires new measurements,
experiments, commercial/engineering records, immutable archives, and
independent review; it is not a repository implementation task.

## Local Linux limitation

The Docker client is installed, but no Docker daemon or alternative local
Linux runtime is available. More importantly, the current source is not a
reviewed clean commit and the workflow is absent from the remote default
branch. A synthetic local copy would not satisfy the acceptance criterion
requiring the exact release commit and GitHub Linux-run evidence, so no
substitute run is represented as completion.

## Verdict

The repository-controlled full-generation definition-of-done gate is
complete. The remaining release, empirical-calibration, author, portal, tag,
DOI, archive, and submission items require new external evidence or explicit
release authority and are not represented as complete.
