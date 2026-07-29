import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const expectedBun = fs.readFileSync(path.join(root, ".bun-version"), "utf8").trim();
if (process.versions.bun !== expectedBun) {
  throw new Error(
    `Bun ${expectedBun} required; found ${process.versions.bun ?? "non-Bun runtime"}`,
  );
}
export const stem = "Recursive_Industrial_Intelligence_r4.0";
export const fragmentDirectory = path.join(root, "docs", "manuscript");
export const manuscriptOutput = path.join(root, "docs", `${stem}.md`);

export const fragments = Object.freeze([
  "00-front-matter.md",
  "10-part-i-foundations.md",
  "11-part-i-depreciation-closure.md",
  "12-part-i-model-results.md",
  "20-part-ii-comparative-economics.md",
  "30-part-iii-strategy-governance.md",
  "40-part-iv-conclusion-limitations.md",
  "50-appendices-a-b.md",
  "51-appendix-c-reproducibility.md",
  "52-appendix-d-model-specification.md",
  "53-notation-register.md",
  "60-glossary.md",
  "70-sources.md",
]);

export function fragmentPaths(): string[] {
  return fragments.map((name) => path.join(fragmentDirectory, name));
}

export function validateFragmentSet(): void {
  if (!fs.existsSync(fragmentDirectory)) {
    throw new Error(`Missing manuscript fragment directory: ${fragmentDirectory}`);
  }
  const expected = new Set(fragments);
  const actual = fs
    .readdirSync(fragmentDirectory)
    .filter((name) => name.endsWith(".md"))
    .sort();
  const missing = fragments.filter((name) => !actual.includes(name));
  const unexpected = actual.filter((name) => !expected.has(name));
  if (missing.length || unexpected.length) {
    const details = [];
    if (missing.length) details.push(`missing: ${missing.join(", ")}`);
    if (unexpected.length) details.push(`unexpected: ${unexpected.join(", ")}`);
    throw new Error(`Invalid manuscript fragment set (${details.join("; ")})`);
  }
}

export function readManuscript(): string {
  validateFragmentSet();
  return fragmentPaths()
    .map((file) => fs.readFileSync(file, "utf8"))
    .join("\n");
}

export function writeMonolithicManuscript(): string {
  const assembled = readManuscript();
  const current = fs.existsSync(manuscriptOutput)
    ? fs.readFileSync(manuscriptOutput, "utf8")
    : null;
  if (current !== assembled) {
    fs.writeFileSync(manuscriptOutput, assembled);
  }
  return assembled;
}
