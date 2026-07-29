#!/usr/bin/env bun

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

import { ensureLocalQuarto, quartoRelease } from "./local-tools.ts";
import { root } from "./manuscript-config.ts";

interface Command {
  args: string[];
  command: string;
  label: string;
}

const updateMode = process.argv.includes("--update");
const started = Date.now();

function fail(message: string): never {
  process.stderr.write(`FAIL ${message}\n`);
  process.exit(1);
}

function execute({ command, args, label }: Command, env: NodeJS.ProcessEnv): void {
  process.stdout.write(`\n==> ${label}\n`);
  const result = spawnSync(command, args, {
    cwd: root,
    env,
    stdio: "inherit",
  });
  if (result.error !== undefined) fail(`${label}: ${result.error.message}`);
  if (result.status !== 0) fail(`${label} exited with status ${result.status ?? "unknown"}`);
}

function capture(command: string, args: string[], env: NodeJS.ProcessEnv): string {
  const result = spawnSync(command, args, {
    cwd: root,
    env,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
  if (result.error !== undefined) fail(`${command}: ${result.error.message}`);
  if (result.status !== 0)
    fail(result.stderr.trim() || result.stdout.trim() || `${command} failed`);
  return result.stdout.trim();
}

function pnpm(label: string, ...args: string[]): Command {
  return { command: "corepack", args: ["pnpm", ...args], label };
}

function uv(label: string, ...args: string[]): Command {
  return { command: "uv", args, label };
}

if (process.platform !== "darwin") {
  fail("candidate:macos must run on macOS");
}

const initialStatus = capture("git", ["status", "--porcelain"], process.env);
if (!updateMode && initialStatus !== "") {
  fail(
    "strict candidate run requires a clean worktree; use candidate:macos:update while rebuilding",
  );
}

let quarto: string;
try {
  quarto = await ensureLocalQuarto();
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

const env = {
  ...process.env,
  QUARTO_BIN: quarto,
};
const expectedVersions = new Map<string, string>([
  ["Bun", "1.3.14"],
  ["pnpm", "11.17.0"],
  ["uv", "0.9.18"],
  ["Python", "3.13.0"],
  ["Pandoc", "3.10.1"],
  ["Quarto", quartoRelease.version],
]);
const uvVersion = capture("uv", ["--version"], env).match(/^uv\s+(\S+)/)?.[1] ?? "";
const actualVersions = new Map<string, string>([
  ["Bun", Bun.version],
  ["pnpm", capture("corepack", ["pnpm", "--version"], env)],
  ["uv", uvVersion],
  [
    "Python",
    capture("uv", ["run", "--locked", "python", "--version"], env).replace(/^Python\s+/, ""),
  ],
  [
    "Pandoc",
    capture("pandoc", ["--version"], env)
      .split(/\r?\n/, 1)[0]
      ?.replace(/^pandoc\s+/, "") ?? "",
  ],
  ["Quarto", capture(quarto, ["--version"], env)],
]);
for (const [tool, expected] of expectedVersions) {
  const actual = actualVersions.get(tool);
  if (actual !== expected) fail(`${tool} ${expected} required; found ${actual || "unknown"}`);
}
process.stdout.write(
  `PASS canonical macOS toolchain: ${[...actualVersions].map(([key, value]) => `${key} ${value}`).join(", ")}\n`,
);

const commands: Command[] = [
  uv("Check the Python lock", "lock", "--check"),
  uv("Install the locked Python environment", "sync", "--locked", "--all-groups"),
  pnpm("Install the locked publication environment", "install", "--frozen-lockfile"),
  pnpm("Check dependencies", "run", "check:dependencies"),
  pnpm("Check AI-R&D evidence", "run", "check:ai-rnd-evidence"),
  pnpm("Check notation", "run", "check:notation"),
  pnpm("Check the math font", "run", "check:font"),
  pnpm("Check standalone prose", "run", "check:prose"),
  pnpm("Check propositions", "run", "check:propositions"),
  pnpm("Refresh the standalone manuscript for source checks", "run", "build:manuscript"),
  pnpm("Check readability", "run", "check:readability"),
  pnpm("Check Markdown", "run", "check:markdown"),
  pnpm("Check YAML", "run", "check:yaml"),
  pnpm("Check GitHub workflow syntax", "run", "check:actions"),
  pnpm("Check TypeScript", "run", "check:typescript"),
  pnpm("Test TypeScript tooling", "run", "test:typescript"),
  pnpm("Check Python quality", "run", "quality:python"),
  pnpm("Regenerate baseline artifacts", "run", "generate:baseline"),
  pnpm("Regenerate Part II artifacts", "run", "generate:part2"),
  pnpm("Regenerate integrated artifacts", "run", "generate:integrated"),
  pnpm("Regenerate deep Monte Carlo artifacts", "run", "generate:deep"),
  uv("Regenerate provenance", "run", "--locked", "rsi-write-provenance", "--project-root", "."),
  uv(
    "Refresh manifests for publication builders",
    "run",
    "--locked",
    "rsi-write-manifest",
    "--project-root",
    ".",
  ),
  uv(
    "Verify regenerated manifests",
    "run",
    "--locked",
    "rsi-verify-manifests",
    "--project-root",
    ".",
  ),
  pnpm("Check figure sources", "run", "check:figures"),
  pnpm("Check table sources", "run", "check:tables"),
  pnpm("Check scenario policy", "run", "check:scenario-policy"),
  pnpm(
    "Install publication browsers",
    "exec",
    "playwright",
    "install",
    "chromium",
    "firefox",
    "webkit",
  ),
  pnpm("Build the standalone manuscript", "run", "build:manuscript"),
  pnpm("Build the Quarto reader site", "run", "build:site"),
  pnpm("Crawl the reader site", "run", "check:site"),
  pnpm("Check rendered tables", "run", "check:table-rendering"),
  pnpm("Check table layout", "run", "check:table-layout"),
  pnpm("Check accessibility", "run", "check:accessibility"),
  pnpm("Check figure layout", "run", "check:figure-layout"),
  pnpm("Check the artifact viewer", "run", "check:artifact-viewer"),
  pnpm("Check equation explanations", "run", "check:equation-explanations"),
  pnpm("Check footnotes", "run", "check:footnotes"),
  pnpm("Check math layout", "run", "check:math-layout"),
  pnpm("Run Python tests with branch coverage", "run", "test:coverage"),
  pnpm("Build and test Python distributions", "run", "check:package"),
  pnpm("Audit JavaScript dependencies", "audit", "--audit-level", "high"),
  pnpm("Audit Python dependencies", "run", "audit"),
  pnpm("Generate the release SBOM", "run", "sbom"),
  uv(
    "Write the final release manifest",
    "run",
    "--locked",
    "rsi-write-manifest",
    "--project-root",
    ".",
  ),
  uv("Verify final manifests", "run", "--locked", "rsi-verify-manifests", "--project-root", "."),
  uv(
    "Run candidate release preflight",
    "run",
    "--locked",
    "rsi-release-preflight",
    "--project-root",
    ".",
    "--mode",
    "candidate",
    ...(updateMode ? ["--allow-dirty"] : []),
  ),
];

for (const command of commands) execute(command, env);

if (!updateMode) {
  const finalStatus = capture("git", ["status", "--porcelain"], env);
  if (finalStatus !== "") fail(`strict candidate run produced worktree drift:\n${finalStatus}`);
}

const auditDirectory = path.join(root, "outputs", "quality");
fs.mkdirSync(auditDirectory, { recursive: true });
const audit = {
  schema: "r4.0-local-candidate-audit-v1",
  commit: capture("git", ["rev-parse", "HEAD"], env),
  completed_at: new Date().toISOString(),
  duration_seconds: Math.round((Date.now() - started) / 1000),
  mode: updateMode ? "update" : "strict",
  platform: `${process.platform}-${process.arch}`,
  tools: Object.fromEntries(actualVersions),
  result: "pass",
};
fs.writeFileSync(
  path.join(auditDirectory, "candidate-audit.json"),
  `${JSON.stringify(audit, null, 2)}\n`,
);
process.stdout.write(
  `\nPASS canonical macOS candidate pipeline in ${audit.duration_seconds}s` +
    `${updateMode ? " (generated updates allowed)" : " (clean reproducibility proven)"}\n`,
);
