# Manual accessibility review — 2026-07-29

Status: pass after one corrected data-viewer defect.

## Environment

- macOS 26.2 (25C56)
- Safari 26.2 with VoiceOver
- Google Chrome 150.0.7871.187 with VoiceOver
- Bun 1.3.14
- Quarto 1.9.38
- Local HTTP build of `_site/`

The review used the data-rich
`part-i/model-results.html` route and its AI electronics supply-chain
artifact viewer. VoiceOver was enabled in System Settings for both browser
passes and was returned to its disabled starting state when the review
finished.

## Screen-reader and zoom review

### VoiceOver and Safari at 200%

Safari was reset to Actual Size and zoomed in five steps to the 200% review
condition. The page reflowed to its narrow layout without document-level
horizontal scrolling. VoiceOver exposed and navigated:

- the skip link, persistent navigation, breadcrumbs, and heading hierarchy;
- the article's heading-one and section heading-twos;
- linked source references;
- Equation 39 as a named mathematical-expression region with a horizontal
  scrolling instruction; and
- the artifact-view button and its separately named CSV download.

The reading order followed the visible page order. Enlarged navigation and
article content did not overlap. Safari was returned to Actual Size after the
review.

### VoiceOver and Chrome at 400%

Chrome was reset to 100% and zoomed in eight steps. Chrome's toolbar reported
`Zoom: 400%`. The article reflowed to a single-column presentation without
document-level horizontal overflow.

With VoiceOver enabled, Chrome's accessibility tree exposed the skip link,
landmarks, headings, lists, source links, equation region, artifact trigger,
and download. The open artifact viewer exposed a named dialog, close button,
heading, search field, rows-per-page control, data table, column and row
headers, pagination controls, full-data link, download, and copy-link button.
The scrollable table remained a separately named, focusable region.

Chrome was returned to 100%, the dialog was closed, and VoiceOver was turned
off after the pass.

## Keyboard-only behavior

Native keyboard events in Chromium and WebKit verified:

- focus and Enter activate the native **View data** button;
- the scrollable table region participates in the tab sequence;
- Space activates a sortable column header and updates `aria-sort`;
- Escape closes the modal dialog; and
- focus returns to the invoking button.

The same pass confirmed a contained modal tab sequence, visible focus
indicators, a polite status region, and semantic dialog, table,
column-header, row-header, and status roles.

## Reduced motion, forced colors, and sticky headers

Chromium media emulation verified the viewer under `prefers-reduced-motion:
reduce` and `forced-colors: active`. The table, controls, focus outline, and
boundaries remained visible, and the viewer did not depend on animation to
communicate state.

The initial 400% visual inspection found a genuine defect: Quarto's table
foreground rule made the sticky artifact column labels white on the
viewer's white `Canvas` background. The header reserved space but appeared
blank. `web/artifact-viewer.css` now explicitly applies `CanvasText` to
sticky header cells. A browser regression assertion compares the rendered
header foreground and background at both 200% and 400%.

After rebuilding, the sticky labels (including **tier** and **parent
sector**) remained visible at 400%. The header stayed inside the table
scroller, the first data row began below it, horizontally clipped columns
were reachable through the table's own scrollbar, and no header obscured a
cell or dialog control.

## Automated corroboration

The following checks passed against the rebuilt artifacts:

- `pnpm run check:artifact-viewer`
- `pnpm run check:accessibility`
- `pnpm run check:table-layout`
- `pnpm run test:typescript`

These checks cover 105 HTML pages, three screen widths plus print for the
table-layout routes, Chromium accessibility roles, WebKit table semantics,
keyboard activation and focus restoration, 200% and 400% viewer containment,
reduced motion, forced colors, deep links, no-JavaScript fallbacks, and
standalone-file operation.

## Verdict

The requested manual accessibility matrix passes after the sticky-header
foreground correction. No unresolved accessibility defect was observed in
the reviewed routes or viewer states.
