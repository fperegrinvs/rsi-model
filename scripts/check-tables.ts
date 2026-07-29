#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import { fragmentPaths, fragments, root } from "./manuscript-config.ts";
import { tableOutputForFragment, tableRecords, validateTableReferences } from "./tables.ts";

const standalone = path.join(root, "docs", "Recursive_Industrial_Intelligence_r4.0.html");
const siteRoot = path.join(root, "_site");

function fail(messages: readonly string[]): never {
  process.stderr.write(`${messages.map((message) => `FAIL ${message}`).join("\n")}\n`);
  process.exit(1);
}

function escapePattern(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function relativePage(fromPage: string, toPage: string): string {
  if (fromPage === toPage) return "";
  const from = path.posix.dirname(fromPage).split("/").filter(Boolean);
  const to = toPage.split("/").filter(Boolean);
  let common = 0;
  while (common < from.length && common < to.length - 1 && from[common] === to[common]) {
    common += 1;
  }
  return [...from.slice(common).map(() => ".."), ...to.slice(common)].join("/");
}

function validateRenderedTables(): string[] {
  const failures: string[] = [];
  if (!fs.existsSync(standalone)) return ["standalone HTML is missing"];
  if (!fs.existsSync(siteRoot)) return ["_site is missing"];
  const records = tableRecords();
  const standaloneHtml = fs.readFileSync(standalone, "utf8");
  const standaloneIds = [
    ...standaloneHtml.matchAll(/<table\b[^>]*\bid="(tbl-[A-Za-z0-9_-]+)"/g),
  ].map((match) => match[1] ?? "");
  if (standaloneIds.length !== records.length) {
    failures.push(
      `standalone has ${standaloneIds.length} numbered table IDs; expected ${records.length}`,
    );
  }
  if (new Set(standaloneIds).size !== standaloneIds.length) {
    failures.push("standalone contains duplicate table IDs");
  }

  for (const record of records) {
    const identifier = escapePattern(record.identifier);
    const number = escapePattern(record.number);
    const standaloneTable = new RegExp(
      `<table\\b(?=[^>]*\\bid="${identifier}")` + `(?=[^>]*\\bdata-table-number="${number}")[^>]*>`,
    );
    if (!standaloneTable.test(standaloneHtml)) {
      failures.push(`${record.identifier}: standalone table number/ID is missing`);
    }
    const standaloneCaption = new RegExp(
      `<caption>\\s*<a\\b[^>]*href="#${identifier}"[^>]*` +
        `class="table-number"[^>]*>Table\\s+${number}</a>\\.\\s*`,
    );
    if (!standaloneCaption.test(standaloneHtml)) {
      failures.push(`${record.identifier}: standalone visible caption number is missing`);
    }

    const siteFile = path.join(siteRoot, record.output);
    if (!fs.existsSync(siteFile)) {
      failures.push(`${record.identifier}: site page ${record.output} is missing`);
      continue;
    }
    const siteHtml = fs.readFileSync(siteFile, "utf8");
    const siteWrapper = new RegExp(
      `<div\\b(?=[^>]*\\bid="${identifier}")` +
        `(?=[^>]*\\bclass="[^"]*\\bnumbered-table\\b[^"]*")` +
        `(?=[^>]*\\bdata-table-number="${number}")[^>]*>`,
    );
    if (!siteWrapper.test(siteHtml)) {
      failures.push(`${record.identifier}: site table number/ID is missing`);
    }
    const siteCaption = new RegExp(
      `<figcaption\\b[^>]*>\\s*<a\\b[^>]*href="#${identifier}"[^>]*` +
        `class="table-number"[^>]*>Table\\s+${number}</a>\\.\\s*`,
    );
    if (!siteCaption.test(siteHtml)) {
      failures.push(`${record.identifier}: site visible caption number is missing`);
    }
    const wrapperIndex = siteHtml.indexOf(`id="${record.identifier}"`);
    const captionIndex = siteHtml.indexOf(`title="Table ${record.number}"`, wrapperIndex);
    const tableIndex = siteHtml.indexOf("<table", wrapperIndex);
    if (!(wrapperIndex >= 0 && captionIndex > wrapperIndex && tableIndex > captionIndex)) {
      failures.push(`${record.identifier}: site caption must precede its table`);
    }
    if (!siteHtml.includes(`aria-describedby="${record.identifier}-caption-`)) {
      failures.push(`${record.identifier}: site table lacks caption association`);
    }
  }
  return failures;
}

function validateRenderedReferences(): string[] {
  const failures: string[] = [];
  const byId = new Map(tableRecords().map((record) => [record.identifier, record]));
  for (const [index, file] of fragmentPaths().entries()) {
    const fragment = fragments[index];
    if (fragment === undefined) continue;
    const currentPage = tableOutputForFragment(fragment);
    const markdown = fs.readFileSync(file, "utf8");
    const siteFile = path.join(siteRoot, currentPage);
    if (!fs.existsSync(siteFile)) continue;
    const html = fs.readFileSync(siteFile, "utf8");
    for (const match of markdown.matchAll(/\[@(tbl-[A-Za-z0-9_-]+)\]/g)) {
      const identifier = match[1] ?? "";
      const target = byId.get(identifier);
      if (target === undefined) continue;
      const page = relativePage(currentPage, target.output);
      const href = `${page === "" ? "" : page}#${identifier}`;
      const reference = new RegExp(
        `<a href="${escapePattern(href)}" class="table-reference"[^>]*>` +
          `${escapePattern(target.number)}</a>`,
      );
      if (!reference.test(html)) {
        failures.push(
          `${fragment}: rendered reference to Table ${target.number} has no correct deep link`,
        );
      }
    }
  }
  return failures;
}

try {
  validateTableReferences();
  const failures = [...validateRenderedTables(), ...validateRenderedReferences()];
  if (failures.length > 0) fail(failures);
  process.stdout.write(
    `PASS rendered table audit: ${tableRecords().length} tables in both editions\n`,
  );
} catch (error) {
  fail([error instanceof Error ? error.message : String(error)]);
}
