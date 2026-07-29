import fs from "node:fs";
import path from "node:path";

import { fragmentPaths, fragments } from "./manuscript-config.ts";

export interface TableRecord {
  identifier: string;
  caption: string;
  number: string;
  output: string;
  fragment: string;
  line: number;
}

const fragmentOutputs = new Map<string, string>([
  ["00-front-matter.md", "index.html"],
  ["10-part-i-foundations.md", "part-i/index.html"],
  ["11-part-i-depreciation-closure.md", "part-i/depreciation-closure.html"],
  ["12-part-i-model-results.md", "part-i/model-results.html"],
  ["20-part-ii-comparative-economics.md", "part-ii/index.html"],
  ["30-part-iii-strategy-governance.md", "part-iii/index.html"],
  ["40-part-iv-conclusion-limitations.md", "part-iv/index.html"],
  ["50-appendices-a-b.md", "appendices/index.html"],
  ["51-appendix-c-reproducibility.md", "appendix-c/index.html"],
  ["52-appendix-d-model-specification.md", "appendix-d/index.html"],
  ["53-notation-register.md", "notation/index.html"],
  ["60-glossary.md", "glossary/index.html"],
  ["70-sources.md", "sources/index.html"],
]);
const forcedSeries = new Map<string, string>([["60-glossary.md", "G"]]);
const tableSeparator = /^\|(?:\s*:?-+:?\s*\|)+\s*$/;
const tableCaption = /^: (.+\S) \{#(tbl-[A-Za-z0-9_-]+)\}$/;

function fail(message: string): never {
  throw new Error(message);
}

export function tableOutputForFragment(fragment: string): string {
  const output = fragmentOutputs.get(fragment);
  if (output === undefined) fail(`No site output configured for ${fragment}`);
  return output;
}

export function tableRecords(): TableRecord[] {
  const records: TableRecord[] = [];
  const seen = new Set<string>();
  const seriesCounts = new Map<string, number>();
  let mainCount = 0;
  let appendixSeries: string | null = null;

  for (const [fragmentIndex, file] of fragmentPaths().entries()) {
    const fragment = fragments[fragmentIndex];
    if (fragment === undefined) fail(`Missing fragment at position ${fragmentIndex}`);
    const output = tableOutputForFragment(fragment);
    appendixSeries = forcedSeries.get(fragment) ?? appendixSeries;
    const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
    for (let index = 0; index < lines.length; index += 1) {
      const line = lines[index] ?? "";
      const appendixMatch = line.match(/^# Appendix ([A-Z]):/);
      if (appendixMatch?.[1] !== undefined) appendixSeries = appendixMatch[1];
      if (!tableSeparator.test(line)) continue;
      const header = lines[index - 1] ?? "";
      if (!header.startsWith("|")) {
        fail(`${fragment}:${index + 1}: table separator has no pipe-table header`);
      }
      let end = index + 1;
      while ((lines[end] ?? "").startsWith("|")) end += 1;
      const tableEnd = end;
      while ((lines[end] ?? "").trim() === "") end += 1;
      if (end - tableEnd > 1) {
        fail(`${fragment}:${tableEnd + 1}: table caption must remain adjacent`);
      }
      const captionLine = lines[end] ?? "";
      const captionMatch = captionLine.match(tableCaption);
      if (captionMatch?.[1] === undefined || captionMatch[2] === undefined) {
        fail(`${fragment}:${end + 1}: substantive table requires ': Caption. {#tbl-id}'`);
      }
      const caption = captionMatch[1];
      const identifier = captionMatch[2];
      if (seen.has(identifier)) fail(`${fragment}:${end + 1}: duplicate table ID ${identifier}`);
      seen.add(identifier);
      let number: string;
      if (appendixSeries === null) {
        mainCount += 1;
        number = String(mainCount);
      } else {
        const count = (seriesCounts.get(appendixSeries) ?? 0) + 1;
        seriesCounts.set(appendixSeries, count);
        number = `${appendixSeries}.${count}`;
      }
      records.push({
        identifier,
        caption,
        number,
        output,
        fragment,
        line: end + 1,
      });
      index = end;
    }
  }
  if (records.length === 0) fail("No substantive manuscript tables found");
  return records;
}

export function writeTableMap(directory: string): string {
  const output = path.join(directory, "tables.tsv");
  const rows = tableRecords().map(
    ({ identifier, number, output: page }) => `${identifier}\t${number}\t${page}`,
  );
  fs.writeFileSync(output, `${rows.join("\n")}\n`);
  return output;
}

export function validateTableReferences(): void {
  const records = tableRecords();
  const ids = new Set(records.map(({ identifier }) => identifier));
  const manuscript = fragmentPaths()
    .map((file) => fs.readFileSync(file, "utf8"))
    .join("\n");
  const references = [...manuscript.matchAll(/\[@(tbl-[A-Za-z0-9_-]+)\]/g)].map(
    (match) => match[1] ?? "",
  );
  const unresolved = [...new Set(references)].filter((identifier) => !ids.has(identifier));
  if (unresolved.length > 0) fail(`Unresolved table references: ${unresolved.join(", ")}`);
  const ambiguous = manuscript.match(
    /\btable (?:below|above)\b|\bthe (?:following|preceding|visible) table\b/gi,
  );
  if (ambiguous !== null) {
    fail(`Ambiguous positional table reference(s): ${[...new Set(ambiguous)].join(", ")}`);
  }
}

export function tableSummary(): string {
  const records = tableRecords();
  const main = records.filter(({ number }) => /^\d+$/.test(number)).length;
  const appendix = records.length - main;
  return `${records.length} tables (${main} main, ${appendix} appendix/glossary)`;
}

if (import.meta.main) {
  try {
    validateTableReferences();
    process.stdout.write(`PASS table source audit: ${tableSummary()}\n`);
  } catch (error) {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exit(1);
  }
}
