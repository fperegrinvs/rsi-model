import { describe, expect, test } from "bun:test";

import { validateScenarioPolicy } from "../../scripts/check-scenario-policy.ts";

describe("orbital-AI scenario policy", () => {
  test("validates registry, generated views, actor boundaries, and prose", () => {
    expect(validateScenarioPolicy()).toEqual({
      inputs: 18,
      capabilities: 33,
      simulationOutputRows: 54,
      closureRows: 72,
      resultRows: 17,
      manuscriptFiles: 7,
    });
  });
});
