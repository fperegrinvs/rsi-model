import { describe, expect, test } from "bun:test";

import {
  equationLinkKinds,
  readEquationInventory,
  readEquationMetadata,
  relationTypes,
  renderEquationExplanationMarkdown,
} from "../../scripts/equations.ts";

describe("equation explanation registry", () => {
  test("covers the exact manuscript inventory in deterministic order", () => {
    const inventory = readEquationInventory();
    const metadata = readEquationMetadata();
    expect(inventory).toHaveLength(57);
    expect(metadata.equations.map(({ id }) => id)).toEqual(inventory);
    expect(metadata.terms.size).toBe(98);
  });

  test("resolves explicit canonical term keys without copied definitions", () => {
    const metadata = readEquationMetadata();
    for (const equation of metadata.equations) {
      expect(equation.termKeys.length).toBeGreaterThan(0);
      expect(new Set(equation.termKeys).size).toBe(equation.termKeys.length);
      for (const key of equation.termKeys) expect(metadata.terms.has(key)).toBe(true);
      expect(relationTypes).toContain(equation.relationType);
      for (const link of equation.links) expect(equationLinkKinds).toContain(link.kind);
    }
  });

  test("renders native Pandoc math source and complete editorial fields", () => {
    const metadata = readEquationMetadata();
    const equation = metadata.equations.find(({ id }) => id === "eq:orbital-deployment");
    if (equation === undefined) throw new Error("fixture equation is missing");
    const rendered = renderEquationExplanationMarkdown(equation, metadata.terms);
    expect(rendered).toContain("$q_c$");
    expect(rendered).toContain("**Units/domain:**");
    expect(rendered).toContain("**Indices and local domains**");
    expect(rendered).toContain("**Operators**");
    expect(rendered).toContain("**Validity and assumptions**");
    expect(rendered).toContain("<strong>Relation:</strong>");
    expect(rendered).toContain("notation:register");
    expect(rendered).not.toContain("<script");
  });
});
