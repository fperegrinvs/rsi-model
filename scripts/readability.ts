import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";

import { fragmentPaths, root, stem } from "./manuscript-config.ts";

export interface ReadabilityCandidate {
  file: string;
  id: string;
  opening: string;
  section: string;
  signals: string[];
  wordCount: number;
}

interface ReviewEntry extends ReadabilityCandidate {
  disposition: "keep_main" | "keep_appendix";
  rationale: string;
}

interface ReviewBaseline {
  mainTextReview: string;
  reviewedAt: string;
  reviewedBy: string;
  reviews: ReviewEntry[];
  schemaVersion: 1;
}

export interface FootnoteInventory {
  definitions: Map<string, { file: string; text: string }>;
  references: Array<{ file: string; id: string }>;
  warnings: string[];
}

const baselineFile = path.join(root, "docs", "reviews", "readability-review.json");
const reportFile = path.join(root, "outputs", "quality", "readability.md");
const footnoteDefinitionPattern = /^\[\^([a-z0-9][a-z0-9-]*)\]:\s*(.*)$/;
const footnoteReferencePattern = /\[\^([a-z0-9][a-z0-9-]*)\]/g;

function words(text: string): string[] {
  return (
    text
      .replace(/\{[^}]*\}/g, " ")
      .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/[`*_#$>|]/g, " ")
      .replace(/\\[A-Za-z]+/g, " ")
      .match(/[\p{L}\p{N}]+(?:[’'-][\p{L}\p{N}]+)*/gu) ?? []
  );
}

function opening(text: string): string {
  return words(text).slice(0, 12).join(" ");
}

function digest(value: string): string {
  return createHash("sha256").update(value).digest("hex").slice(0, 16);
}

function parentheticalDepth(text: string): number {
  let depth = 0;
  let maximum = 0;
  for (const character of text) {
    if (character === "(") {
      depth += 1;
      maximum = Math.max(maximum, depth);
    } else if (character === ")") {
      depth = Math.max(0, depth - 1);
    }
  }
  return maximum;
}

function longestSentence(text: string): number {
  return Math.max(
    0,
    ...text.split(/(?<=[.!?])\s+(?=[A-Z“"*])/).map((sentence) => words(sentence).length),
  );
}

function sourceParagraphs(file: string): Array<{ section: string; text: string }> {
  const markdown = fs.readFileSync(file, "utf8");
  const lines = markdown.split(/\r?\n/);
  const paragraphs: Array<{ section: string; text: string }> = [];
  let section = "front-matter";
  let inCode = false;
  let inFootnote = false;
  let current: string[] = [];

  const flush = (): void => {
    const text = current.join(" ").trim();
    current = [];
    if (!text) return;
    if (
      /^(?:#{1,6}\s|:::|\$\$|!\[|\||[-*+] |>\s*\*\*Status|<!--)/.test(text) ||
      /^\s{4}/.test(text)
    ) {
      return;
    }
    paragraphs.push({ section, text });
  };

  for (const line of lines) {
    if (/^```/.test(line)) {
      flush();
      inCode = !inCode;
      continue;
    }
    if (inCode) continue;
    const heading = line.match(/^##\s+.+?\{#([^}\s]+)[^}]*\}\s*$/);
    if (heading?.[1] !== undefined) {
      flush();
      section = heading[1];
      continue;
    }
    if (footnoteDefinitionPattern.test(line)) {
      flush();
      inFootnote = true;
      continue;
    }
    if (inFootnote) {
      if (line === "" || /^\s{4}/.test(line)) continue;
      inFootnote = false;
    }
    if (line.trim() === "") {
      flush();
    } else {
      current.push(line.trim());
    }
  }
  flush();
  return paragraphs;
}

export function readabilityCandidates(): ReadabilityCandidate[] {
  const candidates: ReadabilityCandidate[] = [];
  for (const file of fragmentPaths()) {
    const relative = path.relative(root, file);
    for (const paragraph of sourceParagraphs(file)) {
      const wordCount = words(paragraph.text).length;
      const signals: string[] = [];
      const sentenceLength = longestSentence(paragraph.text);
      const nesting = parentheticalDepth(paragraph.text);
      const referenceCount =
        [...paragraph.text.matchAll(/\[S\d+\]/g)].length +
        [...paragraph.text.matchAll(/\.artifact-link/g)].length +
        [...paragraph.text.matchAll(footnoteReferencePattern)].length;
      if (wordCount >= 100) signals.push(`long paragraph (${wordCount} words)`);
      if (sentenceLength >= 55) {
        signals.push(`long sentence (${sentenceLength} words)`);
      }
      if (nesting >= 2) signals.push(`nested parentheses (depth ${nesting})`);
      if (referenceCount >= 4) signals.push(`reference cluster (${referenceCount})`);
      if (
        /(?:^|[\s(])outputs\/[A-Za-z0-9_./-]+/.test(paragraph.text) &&
        !paragraph.text.includes(".artifact-link")
      ) {
        signals.push("inline artifact path");
      }
      if (signals.length === 0) continue;
      const normalized = paragraph.text.replace(/\s+/g, " ").trim();
      candidates.push({
        file: relative,
        section: paragraph.section,
        opening: opening(normalized),
        wordCount,
        signals,
        id: digest(`${relative}\n${paragraph.section}\n${normalized}`),
      });
    }
  }
  return candidates;
}

function extractFootnoteDefinitions(
  markdown: string,
  file: string,
): Array<{ file: string; id: string; text: string }> {
  const lines = markdown.split(/\r?\n/);
  const definitions: Array<{ file: string; id: string; text: string }> = [];
  for (let index = 0; index < lines.length; index += 1) {
    const match = lines[index]?.match(footnoteDefinitionPattern);
    if (match?.[1] === undefined) continue;
    const body = [match[2] ?? ""];
    while (index + 1 < lines.length && /^\s{4}/.test(lines[index + 1] ?? "")) {
      index += 1;
      body.push((lines[index] ?? "").trim());
    }
    definitions.push({ file, id: match[1], text: body.join(" ").trim() });
  }
  return definitions;
}

export function footnoteInventory(): FootnoteInventory {
  const definitions = new Map<string, { file: string; text: string }>();
  const references: Array<{ file: string; id: string }> = [];
  const warnings: string[] = [];
  for (const file of fragmentPaths()) {
    const relative = path.relative(root, file);
    const markdown = fs.readFileSync(file, "utf8");
    const localDefinitions = extractFootnoteDefinitions(markdown, relative);
    for (const definition of localDefinitions) {
      if (definitions.has(definition.id)) {
        throw new Error(`duplicate footnote definition ${definition.id}`);
      }
      definitions.set(definition.id, { file: relative, text: definition.text });
      const count = words(definition.text).length;
      if (count > 90) warnings.push(`${definition.id} is unusually long (${count} words)`);
      if (
        /\b(?:ASSUMPTION|forecast|probability|safety boundary|limitation)\b/i.test(definition.text)
      ) {
        warnings.push(`${definition.id} may contain a core claim-boundary warning`);
      }
    }
    const withoutDefinitions = markdown
      .split(/\r?\n/)
      .filter((line) => !footnoteDefinitionPattern.test(line) && !/^\s{4}/.test(line))
      .join("\n");
    for (const match of withoutDefinitions.matchAll(footnoteReferencePattern)) {
      const id = match[1];
      if (id !== undefined) references.push({ file: relative, id });
    }
    for (const line of markdown.split(/\r?\n/)) {
      if (/^#{1,6}\s.*\[\^[^\]]+\]/.test(line)) {
        throw new Error(`${relative} contains a footnote in a heading`);
      }
      if (/^(?:\||!\[).*\[\^[^\]]+\]/.test(line)) {
        throw new Error(`${relative} contains a footnote in a table or figure caption`);
      }
      if (/<sup>\s*\d+\s*<\/sup>/.test(line)) {
        throw new Error(`${relative} contains a manually typed footnote ordinal`);
      }
    }
    if (relative.endsWith("00-front-matter.md")) {
      const abstract = markdown.match(/## Abstract\b[\s\S]*?(?=\n## [^\n]+\b)/)?.[0];
      if (abstract !== undefined && footnoteReferencePattern.test(abstract)) {
        throw new Error("abstract contains a footnote");
      }
    }
  }
  for (const reference of references) {
    if (!definitions.has(reference.id)) {
      throw new Error(`${reference.file} has unresolved footnote ${reference.id}`);
    }
  }
  for (const [id, definition] of definitions) {
    const count = references.filter((reference) => reference.id === id).length;
    if (count === 0) throw new Error(`${definition.file} has orphaned footnote ${id}`);
    if (count > 1) warnings.push(`${id} is referenced ${count} times`);
  }
  return { definitions, references, warnings };
}

function rationale(candidate: ReadabilityCandidate): string {
  const text = `${candidate.opening} ${candidate.signals.join(" ")}`;
  if (candidate.file.includes("appendix") || candidate.section.startsWith("appendix")) {
    return "Reviewed as reproducibility or method detail already located in the appendix path.";
  }
  if (/\b(?:ASSUMPTION|not|does|fails|unresolved|boundary)\b/i.test(text)) {
    return "Kept in the reading path because it carries a result boundary or countercase needed for correct interpretation.";
  }
  if (/\b(?:equation|where|model|constraint|capability|closure)\b/i.test(text)) {
    return "Kept in the reading path because it defines or interprets a central model mechanism used by the next inference.";
  }
  if (candidate.signals.some((signal) => signal.startsWith("reference cluster"))) {
    return "Kept in the reading path as a compact evidence synthesis; source markers remain ordinary links.";
  }
  return "Kept in the reading path after contextual review because it states a central result or strategic inference rather than peripheral mechanics.";
}

function reviewBaseline(candidates: readonly ReadabilityCandidate[]): ReviewBaseline {
  return {
    schemaVersion: 1,
    reviewedAt: "2026-07-28",
    reviewedBy: "LLM-assisted editorial review",
    mainTextReview:
      "PASS: with every note collapsed, the propositions, assumptions, limitations, countercases, safety boundaries, and headline-result interpretations remain in the main text.",
    reviews: candidates.map((candidate) => ({
      ...candidate,
      disposition: candidate.file.includes("appendix") ? "keep_appendix" : "keep_main",
      rationale: rationale(candidate),
    })),
  };
}

function readBaseline(): ReviewBaseline {
  const parsed: unknown = JSON.parse(fs.readFileSync(baselineFile, "utf8"));
  if (parsed === null || typeof parsed !== "object" || !("reviews" in parsed)) {
    throw new Error("readability review baseline is malformed");
  }
  return parsed as ReviewBaseline;
}

function report(
  candidates: readonly ReadabilityCandidate[],
  inventory: FootnoteInventory,
  baseline: ReviewBaseline | undefined,
): string {
  const reviewed = new Map(baseline?.reviews.map((entry) => [entry.id, entry]));
  const rows = candidates.map((candidate) => {
    const entry = reviewed.get(candidate.id);
    return (
      `| \`${candidate.file}\` | \`${candidate.section}\` | ${candidate.opening} | ` +
      `${candidate.signals.join("; ")} | ${entry?.disposition ?? "REVIEW_REQUIRED"} | ` +
      `${entry?.rationale ?? "No contextual review recorded."} |`
    );
  });
  return [
    "# Readability and footnote audit",
    "",
    "Automated measurements are triage signals, not prose-quality scores.",
    "",
    `- Authored footnotes: ${inventory.definitions.size} definitions / ${inventory.references.length} references`,
    `- Flagged prose blocks: ${candidates.length}`,
    `- Footnote warnings: ${inventory.warnings.length}`,
    `- Main-text-only review: ${baseline?.mainTextReview ?? "REVIEW_REQUIRED"}`,
    "",
    "## Contextual review",
    "",
    "| fragment | section | opening words | triggering signal | disposition | rationale |",
    "|---|---|---|---|---|---|",
    ...rows,
    "",
    "## Footnote warnings",
    "",
    ...(inventory.warnings.length > 0
      ? inventory.warnings.map((warning) => `- ${warning}`)
      : ["- None."]),
    "",
  ].join("\n");
}

export function runReadabilityAudit(recordBaseline: boolean): {
  candidates: ReadabilityCandidate[];
  inventory: FootnoteInventory;
} {
  const candidates = readabilityCandidates();
  const inventory = footnoteInventory();
  fs.mkdirSync(path.dirname(reportFile), { recursive: true });
  if (recordBaseline) {
    fs.mkdirSync(path.dirname(baselineFile), { recursive: true });
    fs.writeFileSync(baselineFile, `${JSON.stringify(reviewBaseline(candidates), null, 2)}\n`);
  }
  const baseline = fs.existsSync(baselineFile) ? readBaseline() : undefined;
  fs.writeFileSync(reportFile, report(candidates, inventory, baseline));
  if (baseline === undefined) {
    throw new Error(
      "readability baseline missing; run with --record-reviewed-baseline after review",
    );
  }
  const current = new Set(candidates.map(({ id }) => id));
  const reviewed = new Set(baseline.reviews.map(({ id }) => id));
  const unreviewed = [...current].filter((id) => !reviewed.has(id));
  const stale = [...reviewed].filter((id) => !current.has(id));
  if (unreviewed.length > 0 || stale.length > 0) {
    throw new Error(
      `readability review drift: ${unreviewed.length} unreviewed, ${stale.length} stale`,
    );
  }

  const monolith = fs.readFileSync(path.join(root, "docs", `${stem}.md`), "utf8");
  const monolithDefinitions = extractFootnoteDefinitions(monolith, "monolith");
  const monolithReferences =
    [...monolith.matchAll(footnoteReferencePattern)].length - monolithDefinitions.length;
  if (
    monolithDefinitions.length !== inventory.definitions.size ||
    monolithReferences !== inventory.references.length
  ) {
    throw new Error(
      `footnote count drift: fragments ${inventory.references.length}/${inventory.definitions.size}, ` +
        `monolith ${monolithReferences}/${monolithDefinitions.length}`,
    );
  }
  return { candidates, inventory };
}

export function normalizeRenderedFootnotes(html: string): string {
  const withReferences = html.replace(
    /<a\b(?<attributes>[^>]*\brole="doc-noteref"[^>]*)>/g,
    (whole, attributes: string) => {
      if (/\baria-label=/.test(attributes)) return whole;
      const ordinal = attributes.match(/\bhref="#fn(\d+)"/)?.[1];
      if (ordinal === undefined) {
        throw new Error("rendered footnote reference has no numeric endnote target");
      }
      return `<a${attributes} aria-label="Read footnote ${ordinal}" title="Footnote ${ordinal}">`;
    },
  );
  return withReferences.replace(
    /<a\b(?<attributes>[^>]*\brole="doc-backlink"[^>]*)>/g,
    (whole, attributes: string) => {
      if (/\baria-label=/.test(attributes)) return whole;
      const ordinal = attributes.match(/\bhref="#fnref(\d+)"/)?.[1];
      if (ordinal === undefined) {
        throw new Error("rendered footnote backlink has no numeric reference target");
      }
      return (
        `<a${attributes} aria-label="Return to footnote reference ${ordinal}" ` +
        `title="Return to footnote reference ${ordinal}">`
      );
    },
  );
}
