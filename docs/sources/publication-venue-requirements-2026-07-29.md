# Publication-venue requirements snapshot — 2026-07-29

This note records the first-party requirements used by
`params/publication_targets.yaml`. It is a dated conformance snapshot, not a
substitute for the upload form shown to the corresponding author at
submission. Publisher pages can change without versioned URLs.

## Acta Astronautica

- Publisher: Elsevier.
- Selected route: Original research paper.
- Official guide:
  <https://www.sciencedirect.com/journal/acta-astronautica/publish/guide-for-authors>
- Checked: 2026-07-29.
- Review model: single anonymized.
- Abstract: required and standalone; the current guide does not state a
  numeric word ceiling.
- Keywords: at most six.
- Highlights: mandatory separate editable file with three to five bullets,
  each no longer than 85 characters including spaces.
- Structure and references: numbered sections and numbered square-bracket
  citations in order of appearance.
- Files and declarations: editable source, corresponding-author contact
  details, contribution, funding, competing-interest, permission, and
  generative-AI declarations are required where applicable.

The absence of a numeric abstract ceiling is encoded as “no published numeric
ceiling,” not as an unresolved portal field. A non-empty abstract remains a
hard content check.

## Space Policy

- Publisher: Elsevier.
- Selected route: full-length paper.
- Official guide:
  <https://www.sciencedirect.com/journal/space-policy/publish/guide-for-authors>
- Checked: 2026-07-29.
- Review model: double anonymized.
- Packaging: identifying title page and anonymized manuscript are separate.
- Abstract: at most 250 words.
- Keywords: one to seven.
- Structure: numbered sections.
- Files: editable Word or LaTeX source; PDF alone is not an acceptable source.
- Highlights: encouraged rather than mandatory.
- References: the initial submission may use a consistent style; web
  references need a URL and access date.

## Astropolitics

- Publisher: Taylor & Francis.
- Selected route: Article.
- Public author-instructions page:
  <https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=fast20>
- Journal information and peer-review page:
  <https://www.tandfonline.com/journals/fast20/about-this-journal>
- Checked: 2026-07-29. The author-instructions page reported that it was
  updated on 2026-06-22.
- Article length: 5,000–10,000 words, inclusive of abstract, references, and
  notes.
- Abstract: unstructured and at most 200 words.
- Keywords: three to five.
- References: Taylor & Francis US Chicago author–date style.
- Files: Word or LaTeX accepted; a LaTeX submission includes a PDF plus a
  source archive. Figures are separate files.
- Required order: title page, abstract, keywords, main text,
  acknowledgements, declarations, references, appendices, tables, figures,
  and a figure-caption list.
- Declarations include a data-availability statement and applicable funding,
  competing-interest, permission, and AI-use disclosures.

### First-party peer-review conflict

The two live first-party pages disagree. The author-instructions page says
single-anonymous review, while the journal information page says Research
Articles receive double-anonymous review by two independent referees. Neither
statement is silently preferred. The route therefore conservatively requires
an anonymized review file and leaves `peer_review_anonymization` and
`title_page_packaging` as explicit upload-portal confirmations. The numeric
length, abstract, keyword, source-format, and reference-style fields are no
longer represented as unknown.

## Evidence boundary

This snapshot proves that the public publisher guidance was checked on the
date above. It does not prove that an authenticated submission form presents
the same fields, that an editor will classify the manuscript under the
selected article type, or that author-supplied declarations and approvals
exist. Those remain external submission gates.
