import { describe, expect, test } from "bun:test";

import {
  propositionLabel,
  readPropositionRegistry,
  renderPropositionRegister,
  validatePropositionSystem,
} from "../../scripts/propositions.ts";

describe("proposition registry", () => {
  test("defines the exact proposition ladder in order", () => {
    const propositions = readPropositionRegistry();
    expect(propositions.map(({ id }) => id)).toEqual(["P1", "P2", "P3a", "P3b", "P4a", "P4b"]);
    expect(new Set(propositions.map(({ anchor }) => anchor)).size).toBe(6);
  });

  test("validates canonical definitions, local register, and semantic references", () => {
    const { propositions, references } = validatePropositionSystem();
    expect(propositions).toHaveLength(6);
    expect(references.length).toBeGreaterThanOrEqual(12);
    for (const reference of references) {
      const proposition = propositions.find(({ id }) => id === reference.id);
      expect(proposition).toBeDefined();
      if (proposition !== undefined) {
        expect(reference.label).toBe(propositionLabel(proposition));
      }
    }
  });

  test("renders the glossary register from canonical statuses", () => {
    const propositions = readPropositionRegistry();
    const register = renderPropositionRegister(propositions);
    expect(register).toContain("proposition:P3b");
    expect(register).toContain(propositions[3]?.currentStatus ?? "missing");
    expect(register).not.toContain("<script");
  });
});
