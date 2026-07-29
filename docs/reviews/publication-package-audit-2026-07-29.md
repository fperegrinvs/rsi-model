# Publication-package source and style audit — 2026-07-29

Status: complete for repository-controlled content; author, immutable-release,
and authenticated-upload actions remain external gates.

This audit covers the three selected manuscripts and their shared technical
supplement. It checks the selected target, not an inactive fallback. The
publisher-requirement evidence is frozen in
`docs/sources/publication-venue-requirements-2026-07-29.md`; measured results
are generated in
`outputs/integrated/tables/publication_readiness.csv`.

## Audit method

For each paper:

1. identify every load-bearing empirical or first-party claim;
2. verify that a source is cited at the claim and that the reference resolves;
3. distinguish external evidence from model output and assumption;
4. verify abstract, keyword, length, structure, highlights, and citation style
   against the selected publisher route;
5. search for draft-history language that asks the reader to understand a
   prior version; and
6. leave author identity, declarations, final approval, immutable release
   coordinates, and upload packaging outside the repository-controlled pass.

Model results are not promoted into external evidence. Their support is the
versioned parameter set, deterministic generator, tests, and manifests.

## Technical closure paper

Selected route: Acta Astronautica, Original research paper.

### Source-to-claim trace

| Claim ID | Manuscript claim | Support | Verdict |
|---|---|---|---|
| T-C01 | Lunar-factory and machine-reproduction work supplies a design lineage, not a demonstrated closed system. | References 1–2, cited in section 1. | Supported within the stated historical boundary. |
| T-C02 | NASA roadmaps and ISRU work motivate process categories but do not demonstrate the complete modeled production system. | References 3–4, cited in section 2. | Supported; the non-upgrading qualification is explicit. |
| T-C03 | Bulk lunar occurrence does not by itself establish recoverable reserves or process yield. | Reference 5, cited at the boundary statement in section 2. | Supported as a source/claim distinction; no recovery coefficient is attributed to the source. |
| T-C04 | Dust-related scenario bounds are informed by a NASA surface-effects guide rather than fitted degradation data. | Reference 6, cited in section 4. | Supported; coefficients remain labelled as assumptions. |
| T-M01 | Seed masses, capacity endpoints, doubling time, infeasibility cuts, and stress behavior. | Deterministic repository model and generated tables; not presented as observations. | Correctly classified as computed, assumption-conditioned results. |

All six references are cited, all in-text numeric citations resolve to one
contiguous reference list, and no external source is used to validate the
paper's computed result.

### Target-style verdict

- Abstract: 160 words; required and non-empty. The current guide publishes no
  numeric maximum.
- Keywords: six; passes the maximum of six.
- Highlights: four; each passes the 85-character limit.
- Structure: numbered sections present.
- References: numbered square brackets in order of appearance; resolved.
- Editable source: Markdown is repository source and can be exported to the
  required editable submission form.
- Standalone prose: the release-draft label and the historical “former scalar
  result” wording were removed.

Repository-controlled target conformance passes. Immutable release
coordinates, author declarations, final editable export, and upload actions
remain external.

## Orbital-compute economics paper

Selected route: Space Policy, full-length paper.

### Source-to-claim trace

| Claim ID | Manuscript claim | Support | Verdict |
|---|---|---|---|
| E-C01 | The current literature spans clustered accelerators, system spacecraft constraints, mass-integrated inference concepts, and microdatacenters. | References 1–4, cited in section 1. | Supported as a literature-class statement; architectures are not treated as interchangeable evidence. |
| E-C02 | The compared orbital mesh has lower bisection bandwidth and higher latency than its terrestrial comparison fabric. | Reference 5, cited in section 2. | Supported within the cited comparison; not generalized to every future network. |
| E-C03 | AI1's disclosed peak/average compute, array, vehicle-efficiency, radiator, and envelope values define one conditional architecture. | Reference 6, cited in section 3. | Supported as company specifications; undisclosed lifetime and cost terms remain assumptions. |
| E-C04 | Heritage radiator evidence separates panel areal density from a complete thermal system. | Reference 7, cited in section 3. | Supported and used only as a boundary check. |
| E-C05 | The $185/kg and 100 kW/t values are company projections rather than achieved operating values. | Reference 8, with pages, cited in section 3. | Supported and explicitly quarantined from probabilistic sampling. |
| E-M01 | LCO ratios, incomplete/completed-boundary comparison, and dynamic financing outcomes. | Deterministic repository model and generated cost tables. | Correctly classified as computed outcomes under declared assumptions. |

All eight references are cited and resolve. Claims about present proposals are
dated and architecture-specific. The paper does not use a company forecast as
an empirical probability distribution.

### Target-style verdict

- Abstract: 149 words; passes the 250-word maximum.
- Keywords: six; passes the one-to-seven range.
- Structure: numbered sections present.
- References: one consistent numeric style with URLs and dates where
  applicable; acceptable under the current initial-submission guidance.
- Double-anonymous packaging: identifying title page and anonymous manuscript
  are registered as separate submission actions.
- Standalone prose: the release-draft label and historical “former
  incomplete-cost result” wording were removed.

Repository-controlled target conformance passes. Immutable release
coordinates, author declarations, anonymized export, title page, and upload
actions remain external.

## Strategy and governance paper

Selected route: Astropolitics, Article.

### Source-to-claim trace

| Claim ID | Manuscript claim | Support | Verdict |
|---|---|---|---|
| S-C01 | Formal offering materials document a broad declared off-world industrial direction. | Space Exploration Technologies Corp. 2026a and 2026b, cited with page/slide locators in sections 2 and 4. | Supported for declared direction, not execution. |
| S-C02 | The searched public record does not establish a portfolio-wide common architecture, closure metric, seed bill of materials, or reproduction plan. | The same two filings, under the dated negative-evidence method in section 2. | Supported only as bounded public negative evidence; private absence is not claimed. |
| S-C03 | General AI risk-management and cyber-resilience principles motivate governance functions. | Tabassi 2023 and Ross et al. 2021, cited in sections 6 and 9. | Supported as framework adaptation, not validation of the proposed controls. |
| S-M01 | The matched H0/H1/H2 test, threat register, authority states, dependency transition, and physical traceability. | Analytical construction tied to repository state variables. | Correctly labelled as method and requirements, not empirical validation. |

All four references are cited and resolve under author–date parsing. The paper
does not infer technical feasibility from corporate statements or describe
the control architecture as demonstrated.

### Target-style verdict

- Total counted length: 5,007 words, including abstract and references; passes
  the 5,000–10,000-word range.
- Abstract: 152 words; passes the 200-word maximum.
- Keywords: five; passes the three-to-five range.
- References: Chicago author–date form; all four references resolve.
- Article elements: title, abstract, keywords, main text, data statement, and
  references are present.
- Figures: none in the article, so separate figure files and caption list are
  not currently applicable to content; the packaging action remains explicit
  in case figures are added.
- Peer-review packaging: the publisher's single-versus-double-anonymous
  conflict remains a live upload-portal confirmation. The repository
  conservatively requires an anonymized review file.

Repository-controlled target conformance passes. Immutable release
coordinates, author declarations, final title-page/anonymization choice, and
upload actions remain external.

## Shared technical supplement

The supplement's reproducibility commands use the current `uv`, pnpm, Bun,
and installed CLI workflow. References to removed wrapper scripts and missing
implementation files were eliminated. The supplement identifies itself as a
repository map and does not ask a paper reader to reconstruct prior article
states.

## Final repository-controlled verdict

The source-to-claim and selected-target style audit is complete. Automated
readiness checks reject any selected-route content defect, including
reference-style drift. The only selected-route non-passes allowed after this
audit are:

- `release_pending` for immutable release coordinates; and
- `portal_recheck_pending` for Astropolitics'
  peer-review/anonymization and title-page conflict.

Author-supplied identity and declarations, final approval, authenticated
submission-form evidence, exports, uploads, and the immutable archive are not
represented as completed by this audit.
