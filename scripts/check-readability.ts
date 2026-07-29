#!/usr/bin/env bun

import { runReadabilityAudit } from "./readability.ts";

const recordBaseline = process.argv.includes("--record-reviewed-baseline");

try {
  const { candidates, inventory } = runReadabilityAudit(recordBaseline);
  process.stdout.write(
    `PASS readability audit: ${candidates.length} reviewed prose flags, ` +
      `${inventory.references.length} semantic footnotes, ` +
      `${inventory.warnings.length} warnings; report outputs/quality/readability.md\n`,
  );
} catch (error) {
  process.stderr.write(`FAIL ${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
}
