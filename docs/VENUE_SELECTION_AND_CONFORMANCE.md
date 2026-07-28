# r4.0 venue selection and submission conformance

Status: venues selected; conformance and author confirmation pending.

Requirements were checked on 2026-07-28 against the publishers' current
instructions. They must be rechecked in the live submission portal because
publisher rules can change.

## Selected routes

| Paper | Target | Fallback | Reason |
|---|---|---|---|
| Technical closure model | Acta Astronautica, Original research paper | New Space, Original Article | Acta directly covers engineering analysis of space-borne and Earth-based systems; New Space is suitable after a much larger commercial-space framing. |
| Orbital-compute economics | Space Policy, full-length paper | New Space, Perspective | Space Policy explicitly covers economic and industrial contexts; New Space provides a 1,500–3,000-word perspective route. |
| Strategy/governance | Astropolitics, Research Article | Space Policy, case study | Astropolitics directly covers civil and commercial space politics and policy; Space Policy explicitly accepts case studies. |
| Technical supplement | Supplement to the technical paper | Repository archive linked from either fallback | It is shared methods and provenance, not independent validation or a fourth paper. |

The authoritative machine-readable decision is
`params/publication_targets.yaml`.

## Publisher requirements encoded

The [Acta Astronautica guide](https://www.sciencedirect.com/journal/acta-astronautica/publish/guide-for-authors)
requires original research papers to use numbered sections, no more than six
keywords, editable source, numbered square-bracket references, and a separate
highlights file containing three to five bullets of at most 85 characters.
Its review is single anonymized.

The [Space Policy guide](https://www.sciencedirect.com/journal/space-policy/publish/guide-for-authors)
uses double-anonymized review, requires a separate identifying title page, a
standalone abstract of at most 250 words, one to seven keywords, and editable
source. It covers economic, industrial, political, legal, and social analysis
and accepts full papers and case studies.

The [Astropolitics journal page](https://www.tandfonline.com/journals/fast20/about-this-journal)
states that Research Articles receive double-anonymous review and that the
journal covers civil and commercial space policy. The accessible page does
not expose a stable complete word/abstract/reference specification, so those
fields remain a mandatory live-portal check rather than an invented limit.

The [New Space instructions](https://journals.sagepub.com/author-instructions/NSP)
specify 6,000–8,000 words for Original Articles, 1,500–3,000 words for
Perspectives, a 350-word unstructured abstract, at least four keywords,
editable manuscript files, separate figures, and supplemental-material
support.

## Current disposition

The target and fallback choices are explicit, and `target` is the selected
route for all three papers, but none of the drafts is
submission-ready. Each draft now has in-text citations and a core reference
set that meets its encoded minimum-source floor. A final source-to-claim and
target-style audit, submission metadata, declarations, and author
confirmation remain. The technical and economics drafts would need
substantial expansion only if their unselected New Space fallbacks are
activated. Astropolitics'
portal-only fields must be confirmed immediately before packaging.

The generated
`outputs/integrated/tables/publication_readiness.csv` reports measured abstract
and manuscript word counts plus every machine, author-controlled, and
packaging-action gate. Unknown publisher requirements stay
`portal_recheck_pending`; author
identity, contribution, funding, conflict, acknowledgement, permission, and
AI-use statements stay `author_confirmation_pending`; anonymization, title
page, editable export, figure upload, supplement attachment, and live portal
work stay `submission_action_pending`.
Unselected fallback checks stay visible as `contingency_not_selected` and do
not inflate the active pending-work count.

No submission, journal account action, or claim of author approval is made by
this document.

## External author authorization

Generate a privacy-preserving authorization record outside the repository:

    scripts/publication_preflight.py \
      --write-authorization-template /secure/path/r4.0-paper-authorization.json

The generated record binds each selected route to the exact manuscript and
supplement hashes and enumerates every author confirmation and packaging
action. It is deliberately non-passing until the author supplies confirmations,
portal evidence, action records, final approval, and an attestation. Validate
the completed external record with:

    scripts/publication_preflight.py \
      --authorization-record /secure/path/r4.0-paper-authorization.json

Private correspondence, addresses, email, and signature material should not
be committed to Git. The record can attest that those details are present in
the journal title page or submission system.
