#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import { root } from "./manuscript-config.ts";
import { footnoteInventory } from "./readability.ts";

const site = path.join(root, "_site");
const failures: string[] = [];
let footnoteReferenceCount = 0;
let footnoteDefinitionCount = 0;

function count(text: string, pattern: RegExp): number {
  return [...text.matchAll(pattern)].length;
}

function stripTags(text: string): string {
  return text
    .replace(/<script\b[\s\S]*?<\/script>/gi, "")
    .replace(/<style\b[\s\S]*?<\/style>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&(?:nbsp|#160);/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function attribute(attributes: string, name: string): string {
  const match = attributes.match(new RegExp(`\\b${name}="([^"]*)"`, "i"));
  return match?.[1]?.trim() ?? "";
}

function decodeBasicEntities(text: string): string {
  return text
    .replace(/&nbsp;|&#160;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'");
}

function htmlFiles(directory: string): string[] {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) return htmlFiles(target);
    return entry.isFile() && entry.name.endsWith(".html") ? [target] : [];
  });
}

if (!fs.existsSync(site)) {
  process.stderr.write("FAIL _site/ missing; run pnpm run build:site\n");
  process.exit(1);
}

const pages = htmlFiles(site).filter((file) => !file.includes(`${path.sep}download${path.sep}`));
for (const file of pages) {
  const relative = path.relative(site, file).split(path.sep).join("/");
  const html = fs.readFileSync(file, "utf8");
  if (!/<html\b[^>]*\blang="en"/i.test(html)) {
    failures.push(`${relative}: missing English document language`);
  }
  if (relative !== "404.html") {
    if (count(html, /<main\b/gi) !== 1) {
      failures.push(`${relative}: expected exactly one main landmark`);
    }
    if (count(html, /<nav\b/gi) < 2) {
      failures.push(`${relative}: expected persistent navigation landmarks`);
    }
    if (count(html, /<footer\b/gi) !== 1) {
      failures.push(`${relative}: expected exactly one footer landmark`);
    }
    if (!html.includes('class="site-skip-link"')) {
      failures.push(`${relative}: missing keyboard skip link`);
    }
    if (!html.includes('aria-label="Navigation without JavaScript"')) {
      failures.push(`${relative}: missing no-JavaScript navigation`);
    }
  }

  const main = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1] || "";
  const levels = [...main.matchAll(/<h([1-6])\b/gi)].map((match) => Number(match[1]));
  for (let index = 1; index < levels.length; index += 1) {
    const current = levels[index];
    const previous = levels[index - 1];
    if (current === undefined || previous === undefined) continue;
    if (current > previous + 1) {
      failures.push(`${relative}: heading order jumps h${previous} to h${current}`);
    }
  }

  for (const match of html.matchAll(/<img\b([^>]*)>/gi)) {
    const attributes = match[1] ?? "";
    const decorative =
      attribute(attributes, "role") === "presentation" ||
      attribute(attributes, "aria-hidden") === "true";
    if (!decorative && !/\balt="[^"]+"/i.test(attributes)) {
      failures.push(`${relative}: content image lacks nonempty alt text`);
    }
  }

  for (const match of html.matchAll(
    /<figure\b(?<attributes>[^>]*\bid="(?<id>fig-[A-Za-z0-9_-]+)"[^>]*)>(?<body>[\s\S]*?)<\/figure>/gi,
  )) {
    const attributes = match.groups?.attributes ?? "";
    const identifier = match.groups?.id ?? "unknown figure";
    const body = match.groups?.body ?? "";
    const captions = [...body.matchAll(/<figcaption\b[^>]*>([\s\S]*?)<\/figcaption>/gi)];
    const images = [...body.matchAll(/<img\b([^>]*)>/gi)];
    if (captions.length !== 1) {
      failures.push(`${relative}: ${identifier} must have exactly one figcaption`);
      continue;
    }
    if (images.length !== 1) {
      failures.push(`${relative}: ${identifier} must contain exactly one image`);
      continue;
    }
    const alt = decodeBasicEntities(attribute(images[0]?.[1] ?? "", "alt")).replace(/\s+/g, " ");
    const caption = decodeBasicEntities(stripTags(captions[0]?.[1] ?? ""))
      .replace(/^Figure\s+\d+\.\s*/i, "")
      .replace(/\s+/g, " ")
      .trim();
    if (!alt) failures.push(`${relative}: ${identifier} has empty alt text`);
    if (alt.toLocaleLowerCase() === caption.toLocaleLowerCase()) {
      failures.push(`${relative}: ${identifier} repeats its caption as alt text`);
    }
    if (!/\bclass="figure-number"/i.test(body)) {
      failures.push(`${relative}: ${identifier} lacks a linked figure-number label`);
    }
    if (!attribute(attributes, "data-figure-number")) {
      failures.push(`${relative}: ${identifier} lacks a programmatic figure number`);
    }
    if (attribute(attributes, "class").split(/\s+/).includes("figure-wide")) {
      const fullResolutionLink = body.match(
        /<a\b(?<attributes>[^>]*\bclass="figure-full-resolution-link"[^>]*)>\s*<img\b/i,
      );
      if (!fullResolutionLink) {
        failures.push(`${relative}: ${identifier} lacks a full-resolution image link`);
      } else if (
        !/\baria-label="Open Figure \d+ at full resolution"/i.test(
          fullResolutionLink.groups?.attributes ?? "",
        )
      ) {
        failures.push(`${relative}: ${identifier} full-resolution link lacks an accessible name`);
      }
    }
  }

  for (const match of html.matchAll(/<a\b([^>]*)>([\s\S]*?)<\/a>/gi)) {
    const attributes = match[1] ?? "";
    const body = match[2] ?? "";
    const imageAlt = body.match(/<img\b[^>]*\balt="([^"]+)"/i)?.[1] || "";
    const name =
      attribute(attributes, "aria-label") ||
      attribute(attributes, "title") ||
      stripTags(body) ||
      imageAlt;
    if (!name && attribute(attributes, "aria-hidden") !== "true") {
      failures.push(`${relative}: link has no accessible name`);
    }
  }

  for (const match of html.matchAll(/<button\b([^>]*)>([\s\S]*?)<\/button>/gi)) {
    const attributes = match[1] ?? "";
    const body = match[2] ?? "";
    const name =
      attribute(attributes, "aria-label") || attribute(attributes, "title") || stripTags(body);
    if (!name) failures.push(`${relative}: button has no accessible name`);
  }

  const pageIds = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)]
      .map((match) => match[1])
      .filter((identifier): identifier is string => identifier !== undefined),
  );
  for (const match of html.matchAll(/<a\b(?<attributes>[^>]*\brole="doc-noteref"[^>]*)>/gi)) {
    footnoteReferenceCount += 1;
    const attributes = match.groups?.attributes ?? "";
    const target = attribute(attributes, "href").split("#", 2)[1] ?? "";
    if (!target || !pageIds.has(target)) {
      failures.push(`${relative}: footnote reference targets a missing local endnote`);
    }
    if (!/^Read footnote \d+$/.test(attribute(attributes, "aria-label"))) {
      failures.push(`${relative}: footnote reference lacks a descriptive accessible name`);
    }
  }
  for (const match of html.matchAll(
    /<li\b(?<attributes>[^>]*\bid="fn\d+"[^>]*)>(?<body>[\s\S]*?)<\/li>/gi,
  )) {
    footnoteDefinitionCount += 1;
    const attributes = match.groups?.attributes ?? "";
    const body = match.groups?.body ?? "";
    const identifier = attribute(attributes, "id");
    if (!identifier || !pageIds.has(identifier)) {
      failures.push(`${relative}: footnote definition lacks a stable local target`);
    }
    const backlink = body.match(/<a\b(?<attributes>[^>]*\brole="doc-backlink"[^>]*)>/i);
    if (backlink === null) {
      failures.push(`${relative}: ${identifier || "footnote"} lacks a backlink`);
    } else {
      const backlinkAttributes = backlink.groups?.attributes ?? "";
      const target = attribute(backlinkAttributes, "href").split("#", 2)[1] ?? "";
      if (!target || !pageIds.has(target)) {
        failures.push(`${relative}: ${identifier || "footnote"} backlink target is missing`);
      }
      if (!/^Return to footnote reference \d+$/.test(attribute(backlinkAttributes, "aria-label"))) {
        failures.push(`${relative}: ${identifier || "footnote"} backlink name is unclear`);
      }
    }
  }
  for (const match of html.matchAll(
    /<details\b(?<attributes>[^>]*\bclass="equation-explanation"[^>]*)>(?<body>[\s\S]*?)<\/details>/gi,
  )) {
    const attributes = match.groups?.attributes ?? "";
    const body = match.groups?.body ?? "";
    const identifier = attribute(attributes, "id");
    if (!identifier?.startsWith("explain-eq-")) {
      failures.push(`${relative}: equation explanation lacks a stable fragment`);
    }
    if (!attribute(attributes, "data-equation-explanation").startsWith("eq:")) {
      failures.push(`${relative}: ${identifier || "equation explanation"} lacks its equation ID`);
    }
    if (!/<summary>Explain equation \([^)]+\)<\/summary>/i.test(body)) {
      failures.push(`${relative}: ${identifier || "equation explanation"} lacks a named summary`);
    }
    if (
      !html.includes(
        `aria-expanded="false" aria-controls="${identifier}" data-equation-explain="${identifier}"`,
      )
    ) {
      failures.push(`${relative}: ${identifier || "equation explanation"} lacks a matching button`);
    }
  }
  for (const match of html.matchAll(/<button\b([^>]*\bdata-equation-explain="[^"]+"[^>]*)>/gi)) {
    const attributes = match[1] ?? "";
    const controlled = attribute(attributes, "aria-controls");
    if (!controlled || !pageIds.has(controlled)) {
      failures.push(`${relative}: equation explanation button controls a missing target`);
    }
    if (attribute(attributes, "aria-expanded") !== "false") {
      failures.push(`${relative}: equation explanation button lacks collapsed state`);
    }
  }
}

const css = fs.readFileSync(path.join(site, "quarto.css"), "utf8");
if (!/:focus-visible/.test(css) || !/outline\s*:/.test(css)) {
  failures.push("quarto.css: missing visible focus treatment");
}
const expectedFootnotes = footnoteInventory();
if (
  footnoteReferenceCount !== expectedFootnotes.references.length ||
  footnoteDefinitionCount !== expectedFootnotes.definitions.size
) {
  failures.push(
    `footnote semantic count differs: ${footnoteReferenceCount}/${footnoteDefinitionCount}; ` +
      `expected ${expectedFootnotes.references.length}/${expectedFootnotes.definitions.size}`,
  );
}

if (failures.length) {
  for (const failure of failures) process.stderr.write(`FAIL ${failure}\n`);
  process.exit(1);
}
process.stdout.write(
  `PASS accessibility audit: ${pages.length} pages; landmarks, heading order, ` +
    "names, semantic figures, equation disclosures, alt text, focus visibility, " +
    "footnote semantics, and no-JavaScript navigation\n",
);
