#!/usr/bin/env bun

import { ensureLocalQuarto, quartoRelease } from "./local-tools.ts";

try {
  const quarto = await ensureLocalQuarto();
  process.stdout.write(`PASS local tools: Quarto ${quartoRelease.version} at ${quarto}\n`);
} catch (error) {
  process.stderr.write(`FAIL ${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
}
