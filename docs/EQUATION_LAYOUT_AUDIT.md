# Equation layout audit

The publication renders native MathML with the pinned STIX Two Math v2.13
WOFF2. `pnpm run check:math-layout` checks every numbered equation in
Chromium, Firefox, and WebKit at 1280, 800, 520, and 390 px viewports. It
records the real main-content width, not merely the browser width.

The gate requires the local font to load, representative fractions, radicals,
large operators, matrices, scripts, and Greek glyphs to render, each equation
number to remain visible outside its scrolling region, wide mathematics to be
keyboard-scrollable, and the page itself to remain free of horizontal
overflow. It separately checks the embedded standalone font, a failed-font
fallback, site print CSS, and standalone print CSS.

The current audit covers 57 equations. Fifty need local horizontal scrolling
in at least one engine at the narrowest widths; this is intentional and is
contained within the focusable equation region. The largest measured ratio is
2.419× for the authorized-capacity control at a 390 px Firefox viewport with a
339 px content column. All equations fit the declared print width without an
interactive scrollbar.

The seven equations originally observed as wide at an 800 px viewport were
reviewed individually:

| equation | maximum audited ratio at 800 px | treatment |
|---|---:|---|
| `eq:digital-saturating-frontier` | 1.000× | derivative side conditions moved to adjacent prose |
| `eq:verified-loop-bottleneck` | 1.275× | compact minimum retained; local scrolling is clearer than breaking the stage set |
| `eq:intelligence-embodiment-compatibility` | 1.153× | single bounded compatibility relation retained |
| `eq:embodied-task-first-passage` | 1.390× | paired threshold definitions retained together |
| `eq:data-advantage-profile` | 1.582× | seven-component vector retained as one auditable profile |
| `eq:data-advantage-scalarization` | 1.237× | hard gates and geometric aggregate split into semantic lines |
| `eq:matched-lifecycle-cost` | 1.000× | lifecycle account and comparison diagnostics split into semantic lines |

Additional print-only overflows were removed by semantically reflowing the
chronological backtest, central cost substitution, governance gate, and
lexicographic allocator. No equation is scaled below the publication's normal
print math size.

Reference crops live in `tests/visual/math/` for desktop, intermediate,
narrow-mobile, and print layouts. Regenerate them after an intentional
typography change with `pnpm run capture:math-crops`; the automated gate
continues to test structural breakage across all three engines.
