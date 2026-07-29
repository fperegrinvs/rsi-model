import { describe, expect, test } from "bun:test";

import {
  footnoteInventory,
  normalizeRenderedFootnotes,
  readabilityCandidates,
} from "../../scripts/readability.ts";

describe("readability and footnote audit", () => {
  test("finds semantic footnotes without mechanical defects", () => {
    const inventory = footnoteInventory();
    expect(inventory.definitions.size).toBe(6);
    expect(inventory.references).toHaveLength(6);
    expect(inventory.warnings).toEqual([]);
    expect([...inventory.definitions.keys()]).toContain("p2-ai1-radiator-area");
  });

  test("treats prose measurements as review signals", () => {
    const candidates = readabilityCandidates();
    expect(candidates.length).toBeGreaterThan(100);
    expect(candidates.some(({ signals }) => signals.some((signal) => signal.startsWith("long paragraph"))))
      .toBe(true);
    expect(candidates.every(({ opening, section }) => opening.length > 0 && section.length > 0)).toBe(
      true,
    );
  });

  test("adds descriptive names without replacing native footnote links", () => {
    const rendered = normalizeRenderedFootnotes(
      '<a href="#fn1" id="fnref1" role="doc-noteref"><sup>1</sup></a>' +
        '<a href="#fnref1" role="doc-backlink">↩︎</a>',
    );
    expect(rendered).toContain('aria-label="Read footnote 1"');
    expect(rendered).toContain('aria-label="Return to footnote reference 1"');
    expect(rendered).toContain('href="#fn1"');
  });
});
