#!/usr/bin/env bun

import { validatePropositionSystem } from "./propositions.ts";

try {
  const { propositions, references } = validatePropositionSystem();
  process.stdout.write(
    `PASS proposition audit: ${propositions.length} canonical definitions, ` +
      `${references.length} semantic references\n`,
  );
} catch (error) {
  process.stderr.write(`FAIL ${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
}
