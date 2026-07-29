# r4.0 immutable-release runbook

Status: release-candidate checks implemented; publication not authorized or
executed.

## Reader-site operations

- Live URL: <https://fperegrinvs.github.io/rsi-model/>.
- Local preview: run `pnpm run build:site`, then
  `uv run --locked python -m http.server 8000 --directory _site` and open
  <http://localhost:8000/>.
- Deployment trigger: manually dispatch `.github/workflows/publication.yml`
  from `main` with `deploy_pages=true`. It verifies committed manifests,
  builds and checks the reader edition, and deploys `_site/`; model
  regeneration remains local.
- URL policy: the Pages root is the mutable latest-reviewed reader edition.
  Immutable r4.0 identity belongs to the Git tag and versioned archive/DOI,
  not to the mutable root. No `/r4.0/` Pages permanence is claimed until
  versioned-tree retention is implemented.
- External links: `pnpm run check:external-links` reports third-party
  availability in a non-gating workflow step. Internal links, assets, and
  fragments remain hard deployment gates.
- Rollback: revert the offending source commit on `main`, run the local macOS
  candidate workflow, commit its verified artifacts, and manually deploy the
  restored source state. Do not edit `_site/` or a deployed artifact by hand.
  For an emergency, disable the Pages environment deployment until the
  verified revert succeeds.

The release has two distinct preflight modes:

```bash
uv run --locked rsi-release-preflight --project-root . --mode candidate
uv run --locked rsi-release-preflight --project-root . --mode publication \
  --authorization-record /secure/path/r4.0-release-authorization.json
```

Candidate mode requires a clean worktree, no local `r4.0` tag, matching r4.0
identity, candidate wording, intentionally absent version-publication
metadata, and byte-valid manifests. During development only,
`--allow-dirty` permits the worktree gate to remain pending while every other
gate is evaluated.

Publication mode fails unless all of the following are already true:

1. The author has approved the final source and release metadata.
2. `RELEASE_DATE`, `VERSION_DOI`, and `CANONICAL_URL` are supplied.
3. `VERSION_DOI` is a version DOI and is not the all-versions concept DOI.
4. `CITATION.cff` carries the same release date and version DOI.
5. The manuscript no longer calls itself a release candidate.
6. The HTML was built with the same date, DOI, and immutable canonical URL.
7. The worktree is clean and both manifests verify byte-for-byte.
8. Local tag `r4.0` exists and resolves to `HEAD`.
9. An external authorization record approves that exact `HEAD`, identifies
   the author or release manager and attestation, binds a checksum-verified
   strict local macOS candidate audit and archive record, and repeats the exact
   date, version DOI, and canonical URL.

Generate the current authorization shape with:

```bash
uv run --locked rsi-release-preflight --project-root . \
  --write-authorization-template /secure/path/r4.0-release-authorization.json
```

The generated record is deliberately non-passing. It stays outside the
repository so approving a commit does not change the commit being approved.
Do not put private signature material in the worktree.

## Publication sequence

Do not create the tag until the version DOI and immutable archive coordinates
are known. The intended sequence is:

1. Obtain author approval in principle for the complete diff and proposed
   paper/release metadata.
2. On Apple-silicon macOS, run `corepack pnpm run candidate:macos:update`,
   review and commit the regenerated files, then run the strict
   `corepack pnpm run candidate:macos` command on that clean commit.
3. Reserve or create the immutable archive record and obtain its version DOI.
4. Update the manuscript and `CITATION.cff` with the exact date, version DOI,
   and canonical immutable URL.
5. Rebuild with:

   ```bash
   RELEASE_DATE=YYYY-MM-DD \
   VERSION_DOI=10.5281/zenodo.VERSION \
   CANONICAL_URL=https://immutable-version-url \
   pnpm run build:manuscript
   ```

6. Run `pnpm run check:notation`, `pnpm run check:prose`,
   `pnpm run check:scenario-policy`,
   `pnpm run check:propositions`, `pnpm run check:readability`,
   `pnpm run build:site`, `pnpm run check:site`,
   `pnpm run check:accessibility`, and `pnpm run check:footnotes`.
   Quarto 1.9.38
   writes the reader edition to untracked `_site/`; Pandoc remains responsible
   for the self-contained archival HTML. Separately, execute the LLM-assisted
   editorial review in `docs/EDITORIAL_STYLE.md` — the Rule 1 sentence-level
   review, Rule 2 section-conclusion validation, and Rule 6 contextual
   readability review — and record the verdict tables in the release review
   notes.
7. Run `pnpm run quality:python`, `pnpm run test:coverage`,
   `pnpm run check:package`, `pnpm audit --audit-level high`,
   `pnpm run audit`, and `pnpm run sbom`. The package gate builds both
   distributions and tests the installed wheel outside the checkout.
8. Regenerate both manifests, run the full suite, commit the final metadata,
   and rerun the strict local macOS candidate command.
9. Have the author or release manager complete and attest the external
   authorization record for that exact clean `HEAD` and the checksum-verified
   strict local audit.
10. Tag that exact commit `r4.0`, run publication preflight with the external
   authorization record, push the tag, and attach the verified archive.
11. Verify the archive's hashes against both committed manifests. If desired,
    manually dispatch the workflow from `main` with `deploy_pages=true` to
    deploy the configured GitHub Pages project URL.

Tagging, pushing, creating a GitHub release, or minting a DOI changes external
state. This runbook and its tests do not perform those actions.
