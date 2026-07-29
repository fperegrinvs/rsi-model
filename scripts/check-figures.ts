#!/usr/bin/env bun

import fs from "node:fs";

import { fragmentPaths } from "./manuscript-config.ts";

const expectedIds = [
  "fig-survival-central",
  "fig-import-decay-sweep",
  "fig-seed-mass-ensemble",
  "fig-operating-capacity",
  "fig-oversize-frontier",
  "fig-compute-growth-regimes",
  "fig-debris-regimes",
  "fig-spacexai-threshold-tornado",
  "fig-lco-ratio-monte-carlo",
  "fig-crossover-surface",
] as const;
const approvedClasses = new Set(["figure-compact", "figure-standard", "figure-wide"]);
const failures: string[] = [];
const figures: Array<{ id: string; file: string; attributes: string }> = [];

for (const file of fragmentPaths()) {
  const markdown = fs.readFileSync(file, "utf8");
  const relative = file.split("/docs/manuscript/").at(-1) ?? file;
  const matches = [
    ...markdown.matchAll(
      /!\[(?<caption>[\s\S]*?)\]\((?<target>[^)]+)\)\{#(?<id>fig-[A-Za-z0-9_-]+)(?<attributes>[^}]*)\}/g,
    ),
  ];
  const imageCount = [...markdown.matchAll(/!\[/g)].length;
  if (matches.length !== imageCount) {
    failures.push(
      `${relative}: ${imageCount - matches.length} image(s) lack a complete semantic figure block`,
    );
  }
  if (/^\s*\{fig-alt=/m.test(markdown)) {
    failures.push(`${relative}: detached fig-alt attribute block`);
  }
  if (/\bFigure\s+\d+\b/.test(markdown)) {
    failures.push(`${relative}: manually typed figure ordinal`);
  }
  for (const match of matches) {
    const { caption, target, id, attributes } = match.groups ?? {};
    if (!caption?.trim()) failures.push(`${relative}: ${id ?? "figure"} has no caption`);
    if (!target?.startsWith("../outputs/") || !target.endsWith(".png")) {
      failures.push(`${relative}: ${id ?? "figure"} has unsafe or non-output target ${target}`);
    }
    if (id === undefined || attributes === undefined) {
      failures.push(`${relative}: malformed figure declaration`);
      continue;
    }
    const classes = [...attributes.matchAll(/(?:^|\s)\.(figure-[A-Za-z0-9_-]+)/g)].map(
      (candidate) => candidate[1],
    );
    if (classes.length !== 1 || classes[0] === undefined || !approvedClasses.has(classes[0])) {
      failures.push(`${relative}: ${id} must have exactly one approved presentation class`);
    }
    const alt = attributes.match(/\bfig-alt="([^"]+)"/)?.[1]?.trim();
    if (!alt) failures.push(`${relative}: ${id} has no nonempty fig-alt`);
    if (alt && caption && alt.replace(/\s+/g, " ") === caption.replace(/\s+/g, " ").trim()) {
      failures.push(`${relative}: ${id} caption and alt text are duplicates`);
    }
    figures.push({ id, file: relative, attributes });
  }
}

const actualIds = figures.map(({ id }) => id);
if (
  actualIds.length !== expectedIds.length ||
  actualIds.some((identifier, index) => identifier !== expectedIds[index])
) {
  failures.push(
    `figure order mismatch: expected ${expectedIds.join(", ")}; found ${actualIds.join(", ")}`,
  );
}
const duplicates = actualIds.filter((identifier, index) => actualIds.indexOf(identifier) !== index);
if (duplicates.length > 0) {
  failures.push(`duplicate figure IDs: ${[...new Set(duplicates)].join(", ")}`);
}

const allMarkdown = fragmentPaths()
  .map((file) => fs.readFileSync(file, "utf8"))
  .join("\n");
const referencedIds = new Set<string>();
for (const match of allMarkdown.matchAll(/@(?<id>fig-[A-Za-z0-9_-]+)/g)) {
  const identifier = match.groups?.id;
  if (identifier !== undefined && !actualIds.includes(identifier)) {
    failures.push(`unresolved figure reference: ${identifier}`);
  }
  if (identifier !== undefined) referencedIds.add(identifier);
}
for (const identifier of expectedIds) {
  if (!referencedIds.has(identifier)) {
    failures.push(`figure has no semantic prose reference: ${identifier}`);
  }
}

if (failures.length > 0) {
  for (const failure of failures) process.stderr.write(`FAIL ${failure}\n`);
  process.exit(1);
}
process.stdout.write(
  `PASS figure source audit: ${figures.length} semantic figures in global order\n`,
);
