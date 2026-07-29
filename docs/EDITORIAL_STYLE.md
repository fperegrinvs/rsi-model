# Manuscript editorial rules

Each rule binds human and agent editing alike and is re-validated on every
new version: a named automated gate covers the mechanical subset where one
exists, and an LLM-assisted or human review executes the full rule using
the protocol given with it.

## Rule 1 — Standalone prose

The article must read as a self-contained argument, not as a conversation
with its drafting history.

Every sentence in `docs/manuscript/` must do at least one of the following:

- advance the argument;
- provide evidence or a source boundary;
- define a term, equation, method, or result;
- state a limitation, uncertainty, or falsification condition; or
- help the reader navigate the current article.

Remove process narration, self-reference, and statements whose only content
is that an earlier draft, relation, model, or review was different. Put that
history in `CHANGELOG.md` or version control instead.

The automated `pnpm run check:prose` gate detects common residue such as
“earlier drafts,” “previous version,” “is now,” “was replaced,” “retired,”
model-lineage labels, and version-tagged analysis narration. It is
intentionally narrower than the editorial rule: an LLM-assisted or human
review must still evaluate whether each sentence earns its place in context.
Current release metadata, dated evidence about the subject, and reproducible
artifact filenames are not drafting-history narration.

The reader-facing opening proceeds from title, compact edition/byline metadata,
and deck directly to the abstract and executive summary. It must not contain a
release-candidate callout, dirty-worktree or CI narration, TODO text, or
regeneration instructions. Detailed claim scope follows the summary under
“Scope, Claims, and Evidence”; reproducibility mechanics remain in Appendix C
and repository documentation. The project deliberately does not publish a
separate status page: build state belongs in CI and release records, while
empirical claim status belongs beside the relevant claim. Source and rendered
opening-order checks enforce the mechanical part of this rule.

## Rule 2 — Section conclusions

Every argumentative section must end by telling the reader what it
established. A section that stops at its last subtopic is incomplete even
when every sentence in it passes Rule 1.

**Scope.** Every `##`-level section in the Part I–IV fragments
(`docs/manuscript/10-*.md` through `40-*.md`). Front matter (`00-*`),
appendices and registers (`50-*` through `53-*`), the glossary (`60-*`),
and sources (`70-*`) are exempt. The exemption list is declared here; a
validator must not infer additional exemptions.

**Requirement.** The final paragraph of each in-scope section is a
conclusion. A paragraph qualifies only if all four criteria hold:

1. **Synthesis, not continuation.** It states what the section as a whole
   established — its structural claim or central result — rather than
   continuing the final subtopic. Test: the paragraph remains a correct
   summary of the section if the section's last subtopic is deleted.
2. **Specificity.** It names at least one equation, quantity, artifact, or
   term introduced in the section. Test: appended to a different section,
   the paragraph would be visibly wrong.
3. **Epistemic status.** When the section reports numbers, the conclusion
   restates their class consistently with the epistemic rules —
   implication of a declared design space, scenario mechanics, or
   measurement — and, when the section's claim is falsifiable, names what
   evidence would change it.
4. **No new material.** It introduces no topic, source, number, or
   definition absent from the body of its own section. Pointers to where
   the article uses or defends the result elsewhere are encouraged and do
   not violate this criterion.

A section whose final block is an equation, table, figure, list, or a
caution scoped to a single subtopic fails.

**Validation protocol (LLM-executed on every new version).** The final
paragraph is the last prose block of the section: skip trailing thematic
breaks (`* * *`), HTML comments, and whitespace when locating it; a
trailing blockquote or bold-labeled paragraph is judged like any other
paragraph. For each in-scope section, read the full section, then judge
its final paragraph against the four criteria. Emit one verdict row per section:

| section id | verdict | final paragraph opens with | reason |
|---|---|---|---|
| `#i.1-…` | PASS or FAIL | verbatim opening words | criterion number and a one-sentence reason |

Quote evidence verbatim; do not paraphrase. The check fails when any
in-scope section fails or when a section cannot be classified using the
declared scope. Record the verdict table in the release review notes.

**Authoring guidance (for agents).** Write the conclusion last and derive
it from the section's own content, in this order: (a) the structural claim
the section established; (b) what binds, or the key quantitative
implication, within the declared design space; (c) the epistemic class of
those results and the evidence that would move them; (d) where the article
uses the result next. Do not add a “Conclusion” subheading; the conclusion
is the final paragraph of the section body.

## Rule 3 — Semantic figures

Every authored manuscript image is a numbered semantic figure. Use one
attached attribute block containing a stable `fig-` identifier, exactly one
presentation class, and visual-description text:

`![Interpretive caption.](path){#fig-example .figure-standard fig-alt="What the visual contains."}`

Captions state the interpretation and evidence class. `fig-alt` describes the
visual without repeating the caption. Refer to the figure as
`Figure [@fig-example]`; never type an ordinal into prose or a caption.
The build assigns one global sequence shared by the chapter site, standalone
HTML, print, and future PDF output. The generated label and every prose
reference link to the stable figure anchor without JavaScript.

Choose the smallest of three presentation classes that remains legible:

- `.figure-compact` for a simple single-panel chart;
- `.figure-standard` for an information-dense single panel; and
- `.figure-wide` for a genuine multi-panel comparison.

Images keep their full raster resolution but render with `width: auto`,
`max-width: 100%`, and `height: auto`. Wide figures receive an ordinary
full-resolution image link as a progressive aid; the inline figure, caption,
and semantic link remain complete without it. Do not repair a dense,
ultra-wide panel with CSS shrinkage alone—regenerate it as a reader-sized
grid.

Run `pnpm run check:figures`, `pnpm run check:site`, and
`pnpm run check:accessibility` after every figure change. Release review also
samples every figure at 320, 768, 1,280, and 1,440 CSS pixels, confirming no
page or figure overflow, contained captions and images, undistorted aspect
ratios, readable labels, keyboard-visible links, and acceptable print sizing.

## Rule 4 — Semantic tables

Every substantive reader-facing table has a descriptive caption and stable
`tbl-` identifier authored immediately after the pipe table:

`: Descriptive caption. {#tbl-example}`

The build assigns one shared sequence across editions: `Table 1`, `Table 2`,
and so on in the main article, with lettered appendix/register series such as
`Table A.1`, `Table D.1`, and `Table G.1`. Refer to it as
`Table [@tbl-example]`; never type an ordinal or use “the table above/below.”
Generated labels and references are ordinary deep links and remain usable
without JavaScript.

Captions identify what the table contains and its evidence or scenario
boundary when that is not obvious. When a table summarizes a generated CSV,
its caption includes an unobtrusive `View data` artifact action; the separate
download action retains the exact source CSV. Captions are programmatically
associated with tables, header cells remain semantic, and wide tables scroll
inside a local container rather than widening the page.

Run `pnpm run check:tables`, `pnpm run check:table-rendering`, and
`pnpm run check:table-layout` after every table change. The rendered audit
requires a unique visible number, stable anchor and caption association in
both editions. The layout audit samples 320, 768, and 1,280 CSS pixels plus
print, checking local horizontal scrolling, caption placement, repeating
headers, unsplit rows, and printable width.

## Rule 5 — Publication data artifacts

Reader prose names a table by meaning, not by its raw filename. Author every
CSV reference as an ordinary Markdown link with one explicit repository path:

`[digital-elasticity bounds](../outputs/integrated/tables/digital_elasticity_bounds.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_elasticity_bounds.csv"}`

The `href` and `data-artifact` path must identify the same file under
`outputs/`. Basename lookup, parent traversal, directories, missing files,
escaping symlinks, and artifacts absent from the applicable manifest are
invalid. Exact filenames remain visible in the catalog and viewer rather than
interrupting argumentative prose.

The build replaces that authoring link with two controls whose purposes do not
overlap. **View data: _title_** is a native button, shown only after the shared
viewer initializes. **Download original CSV** is an ordinary anchor with the
`download` attribute, file size, and a descriptive accessible name containing
both “Download” and “CSV.” Never hand-author a button or reuse one ambiguous
anchor for both actions. With JavaScript disabled, the hidden View button
cannot make a false promise and the explicit download remains available.

The site copies each referenced CSV byte-for-byte, validates UTF-8 and CSV
structure once with the pinned parser, checks its manifest SHA-256, and writes
one payload plus one readable `/data/artifacts/<stable-key>.html` page per
artifact. A site page lazy-loads only the payload a reader opens and caches it
for that page session. Modified/new-tab navigation uses the readable HTML data
page; raw CSV navigation is never the View action.

The self-contained standalone edition embeds one gzip-compressed payload,
decoded only when a table is opened. Complete data are embedded only while the
serialized artifact and total payload remain within the registered budgets.
Larger tables expose exactly the first 50 of the declared total rows and state
that search, sorting, and pagination cover only that preview; their full HTML
page and original CSV remain separate actions. The build records raw,
gzip/Brotli, payload, and per-table measurements in
`outputs/quality/artifact_viewer_size_report.json` and fails over budget.
Do not add a second viewer implementation or expanded JSON/table duplicates.

Both editions use the same TypeScript behavior, dialog shell, and CSS. The
viewer is searchable, sortable, paginated, and text-only at the cell boundary:
cell content is assigned through `textContent`, so CSV values are neither HTML
nor executable formulas. It exposes a semantic caption, scoped column headers,
registered row headers, declared labels/descriptions/units, missing-value
names, provenance class, freshness, source path and hash. The first registered
key column freezes during horizontal scrolling; charts remain absent unless
the registry explicitly declares axes, units, and series.

`params/artifact_registry.json` may define `title`, `description`, `class`,
`keyColumns`, `defaultSort`, and per-column `label`, `description`, and
`units`. Register only genuine row identifiers as key columns and never infer
units or display precision from a header. CSV bytes remain authoritative.

Run `pnpm run test:typescript`, `pnpm run check:site`, and
`pnpm run check:artifact-viewer` after changing artifact syntax, metadata, the
viewer, or a referenced CSV. The browser gate covers the hosted and local
`file://` editions, JavaScript-disabled and corrupt-payload fallbacks,
manifest mismatches, keyboard/focus/history behavior, mobile landscape,
200%/400% reflow proxies, reduced motion, forced colors, search, sorting,
pagination, and the startup/first-view latency budgets.

## Rule 6 — Equation explanations and deterministic mathematics

Every numbered equation has one record in `params/equation_explanations.json`
and resolves its named terms through stable keys in
`params/notation_registry.json`. Explanations state the relation class, model
layer, implementation status, assumptions, indices, and non-obvious operators;
they supplement rather than replace the nearby prose and local “where”
paragraph. Optional resource links may point to related equations, sources,
implementation, tests, configuration, or result tables.

The rendered number remains a selectable, deep-linkable anchor. A separate
button enhances a native `<details>` disclosure, while the disclosure remains
usable without JavaScript and provides a stable `explain-eq-*` fragment.
Notation-register rows link directly to both the equation and its explanation.
Print output includes opened explanations and always exposes the canonical
notation-register link.

Native MathML uses the pinned, self-hosted STIX Two Math WOFF2 asset and the
generic `math` family only as fallback. Wide mathematics may scroll within a
focusable local region on screens, with its number fixed outside and a visible
overflow cue; print must fit without interactive scrolling.

Run `pnpm run test:typescript`, `pnpm run check:equation-explanations`,
`pnpm run check:notation`, `pnpm run check:math-layout`, and
`pnpm run check:font` after changing equations, notation, explanations, or
math styling.

## Rule 7 — Selective detail and semantic footnotes

Classify detail by argumentative function, not length. Keep the proposition
needed for the next inference, central mechanisms and results, equation terms
and units, evidence classes, material assumptions, countercases, falsifiers,
safety boundaries, and conclusion-changing limitations in the main reading
path. Move only compact provenance detail, secondary arithmetic, narrow
implementation mechanics, or a nonessential example to a footnote. Put a
multi-paragraph method or table in an appendix instead. Removing repeated
material is preferable to hiding a duplicate in a note.

Use standard named Pandoc footnotes such as
`[^p2-ai1-radiator-area]`. Identifiers are globally unique and semantic;
generated ordinals are never typed in prose or used as cross-references.
Keep each note to one paragraph and normally one to three sentences. The
budget is at most three notes per `##` section and two references per
paragraph. Do not put notes in the abstract, headings, captions, or tables,
chain notes together, or move a claim-boundary warning into a note.
Source markers remain ordinary source links and machine-readable tables
remain friendly artifact links.

The ordinary reference/endnote/backlink structure is authoritative. Quarto's
non-blocking hover and focus preview is progressive enhancement; touch and
no-JavaScript use navigate to the local endnote. Endnotes remain visible for
standalone HTML and print. The site keeps notes on their chapter page, while
the standalone build places them at section scope. The source identifier and
content remain stable even when displayed ordinals differ.

Run `pnpm run check:readability` after every manuscript edit. It fails broken
footnote mechanics and any new or changed prose flag that lacks contextual
review; long paragraphs, long sentences, nested parentheses, and reference
clusters are triage signals rather than scores. Review each flagged passage
as `keep_main`, `keep_appendix`, move to a short note, or remove, recording
the section, opening words, signal, disposition, and rationale in
`docs/reviews/readability-review.json`. A release review samples the abstract
or executive material, one dense quantitative section, one strategy section,
and every newly flagged passage at rendered width, then repeats a main-text-only
read with notes collapsed. Run `pnpm run check:footnotes`,
`pnpm run check:site`, and `pnpm run check:accessibility` after rendering.

## Rule 8 — Dated orbital-AI scenarios and closure claims

Every quantitatively relevant off-planet-AI comparison uses the canonical
scenario order defined in `params/orbital_ai_scenario_registry.json`: neutral
generic reference, commensurable independent reference, SpaceXAI disclosed
design, SpaceXAI stated aspiration, and—only when separately identified
affiliate or analyst inputs are necessary—an explicit hybrid. A relevant
simulation may omit a numerical track only by publishing
`not_parameterizable` and the missing fields. A named company scenario never
replaces the neutral baseline or becomes the central estimate merely because
it is decision-relevant.

Every result identifies its scenario, evidence class, source snapshot,
parameter completeness, and actor boundary. Keep observed operation,
demonstrated hardware, disclosed design, near-term target, long-run
aspiration, regulatory filing, and analyst assumption distinct. Do not mix
peak and average power, power and compute throughput, payload and total
vehicle mass, annual flow and cumulative stock, launched and commissioned
capacity, or serviceable and disposable architectures. Company targets are
deterministic axes, never empirical priors or achieved-performance
distributions. Independent completion of a company case must carry a hybrid
label and remain visually identifiable.

Neutral and independent cases receive equal visual weight and accessible,
non-color-only differentiation. SpaceXAI is retained because it supplies a
specific, falsifiable real-world design and industrial trajectory against
which the general model can be tested. Independent cases keep that test from
becoming a company narrative. No actor receives undisclosed favorable
completion that is unavailable to its comparators.

Claims using _unique_, _integrated_, _full stack_, _self-sustaining_, _closed
loop_, or equivalent language state:

- an “as of” date;
- the comparison class and actor/legal-entity boundary;
- the maturity threshold being compared;
- the unresolved layers or dependencies; and
- whether the claim concerns breadth, operation, or reproductive closure.

Affiliated companies are not one legal entity. Terrestrial capability is not
space-qualified capacity, an application accepted for filing is not
authorization, and broad vertical integration is not physical closure. Tesla
evidence may enter only an explicitly labelled
`spacexai_affiliate_hybrid` case with transfer, qualification, availability,
and control uncertainties preserved.

Run `pnpm run check:scenario-policy`, `pnpm run test`, and
`pnpm run check:external-links` after changing a named scenario, comparative
market-position claim, actor boundary, closure-stack row, or related source.
Every release repeats the competitor search and creates a new dated registry
version when the public record changes; historical results are not silently
rewritten.
