# r4.0 immutable-release runbook

Status: release-candidate checks implemented; publication not authorized or
executed.

The release has two distinct preflight modes:

```bash
python scripts/release_preflight.py --mode candidate
python scripts/release_preflight.py --mode publication \
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
   the author or release manager and attestation, links the passing Linux CI
   run and archive record, and repeats the exact date, version DOI, and
   canonical URL.

Generate the current authorization shape with:

```bash
python scripts/release_preflight.py \
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
2. Create the release commit and let `publication-integrity` pass on Linux.
3. Reserve or create the immutable archive record and obtain its version DOI.
4. Update the manuscript and `CITATION.cff` with the exact date, version DOI,
   and canonical immutable URL.
5. Rebuild with:

   ```bash
   RELEASE_DATE=YYYY-MM-DD \
   VERSION_DOI=10.5281/zenodo.VERSION \
   CANONICAL_URL=https://immutable-version-url \
   npm run build:manuscript
   ```

6. Regenerate both manifests, run the full suite, commit the final metadata,
   and rerun Linux CI.
7. Have the author or release manager complete and attest the external
   authorization record for that exact clean `HEAD` and passing CI run.
8. Tag that exact commit `r4.0`, run publication preflight with the external
   authorization record, push the tag, and attach the verified archive.
9. Verify the archive's hashes against both committed manifests.

Tagging, pushing, creating a GitHub release, or minting a DOI changes external
state. This runbook and its tests do not perform those actions.
