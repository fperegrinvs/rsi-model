#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import { buildArtifactData, readArtifactReferences } from "./artifacts.ts";
import { readEquationMetadata } from "./equations.ts";
import { root, stem } from "./manuscript-config.ts";
import {
  propositionLabel,
  readPropositionReferences,
  readPropositionRegistry,
} from "./propositions.ts";
import { footnoteInventory } from "./readability.ts";

const site = path.join(root, "_site");
const monolithicHtml = path.join(root, "docs", `${stem}.html`);
const viteOutput = path.join(site, "assets", "rsi");
const viteManifest = path.join(viteOutput, "manifest.json");
const expectedPages = [
  "index.html",
  "part-i/index.html",
  "part-i/depreciation-closure.html",
  "part-i/model-results.html",
  "part-ii/index.html",
  "part-iii/index.html",
  "part-iv/index.html",
  "appendices/index.html",
  "appendix-c/index.html",
  "appendix-d/index.html",
  "notation/index.html",
  "glossary/index.html",
  "sources/index.html",
  "data/index.html",
];
const expectedFigureIds = [
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
const approvedFigureClasses = new Set(["figure-compact", "figure-standard", "figure-wide"]);

function fail(messages: string[]): never {
  for (const message of messages) process.stderr.write(`FAIL ${message}\n`);
  process.exit(1);
}

function ids(html: string): string[] {
  return [...html.matchAll(/\sid="([^"]+)"/g)]
    .map((match) => match[1])
    .filter((identifier): identifier is string => identifier !== undefined);
}

function count(html: string, pattern: RegExp): number {
  return [...html.matchAll(pattern)].length;
}

function attribute(attributes: string, name: string): string {
  return attributes.match(new RegExp(`\\b${name}="([^"]*)"`, "i"))?.[1]?.trim() ?? "";
}

function inspectFigures(
  label: string,
  documents: ReadonlyArray<string>,
): Array<{ id: string; number: number }> {
  const found: Array<{ id: string; number: number }> = [];
  for (const html of documents) {
    if (/\{fig-alt=/.test(html)) failures.push(`${label} contains a literal fig-alt attribute`);
    if (/<p\b[^>]*>\s*<img\b/i.test(html)) {
      failures.push(`${label} contains a manuscript image outside a semantic figure`);
    }
    for (const match of html.matchAll(
      /<figure\b(?<attributes>[^>]*\bid="(?<id>fig-[A-Za-z0-9_-]+)"[^>]*)>(?<body>[\s\S]*?)<\/figure>/gi,
    )) {
      const attributes = match.groups?.attributes ?? "";
      const identifier = match.groups?.id ?? "";
      const body = match.groups?.body ?? "";
      const number = Number(attribute(attributes, "data-figure-number"));
      const classes = attribute(attributes, "class").split(/\s+/);
      const presentation = classes.filter((className) => approvedFigureClasses.has(className));
      if (presentation.length !== 1) {
        failures.push(`${label} ${identifier} must have exactly one approved presentation class`);
      }
      if (!classes.includes("numbered-figure")) {
        failures.push(`${label} ${identifier} lacks the numbered-figure class`);
      }
      if (!Number.isInteger(number) || number < 1) {
        failures.push(`${label} ${identifier} has invalid data-figure-number`);
      }
      if (count(body, /<figcaption\b/gi) !== 1) {
        failures.push(`${label} ${identifier} must have exactly one figcaption`);
      }
      const expectedLink = new RegExp(
        `<a href="#${escapePattern(identifier)}" class="figure-number"[^>]*>` +
          `Figure\\s+${number}<\\/a>\\.`,
      );
      if (!expectedLink.test(body)) {
        failures.push(`${label} ${identifier} lacks its linked Figure ${number} caption prefix`);
      }
      found.push({ id: identifier, number });
    }
  }
  const identifiers = found.map(({ id }) => id);
  if (
    identifiers.length !== expectedFigureIds.length ||
    identifiers.some((identifier, index) => identifier !== expectedFigureIds[index])
  ) {
    failures.push(
      `${label} figure order mismatch: expected ${expectedFigureIds.join(", ")}; ` +
        `found ${identifiers.join(", ")}`,
    );
  }
  const numbers = found.map(({ number }) => number);
  if (numbers.some((number, index) => number !== index + 1)) {
    failures.push(`${label} figure sequence is not contiguous: ${numbers.join(", ")}`);
  }
  return found;
}

function inspectFigureReferences(label: string, documents: ReadonlyArray<string>): void {
  const referencedIds = new Set<string>();
  const numberById = new Map<string, number>(
    expectedFigureIds.map((identifier, index) => [identifier, index + 1] as const),
  );
  for (const html of documents) {
    for (const match of html.matchAll(
      /<a href="(?<href>[^"]*#(?<id>fig-[A-Za-z0-9_-]+))"(?<attributes>[^>]*)>(?<body>[^<]+)<\/a>/gi,
    )) {
      const attributes = match.groups?.attributes ?? "";
      if (!/\bclass="figure-reference"/.test(attributes)) continue;
      const identifier = match.groups?.id ?? "";
      const expectedNumber = numberById.get(identifier);
      referencedIds.add(identifier);
      if (expectedNumber === undefined) {
        failures.push(`${label} has a reference to unknown figure ${identifier}`);
        continue;
      }
      if (match.groups?.body?.trim() !== String(expectedNumber)) {
        failures.push(`${label} reference to ${identifier} displays the wrong ordinal`);
      }
      if (!attributes.includes(`aria-label="Go to figure ${expectedNumber}"`)) {
        failures.push(`${label} reference to ${identifier} has the wrong accessible name`);
      }
      if (!attributes.includes(`title="Figure ${expectedNumber}"`)) {
        failures.push(`${label} reference to ${identifier} has the wrong title`);
      }
    }
  }
  for (const identifier of expectedFigureIds) {
    if (!referencedIds.has(identifier)) {
      failures.push(`${label} has no semantic prose reference to ${identifier}`);
    }
  }
}

function escapePattern(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function explanationFragment(identifier: string): string {
  return `explain-${identifier.replace(/^eq:/, "eq-").replace(/[^A-Za-z0-9_-]/g, "-")}`;
}

function inspectEquationExplanations(label: string, documents: readonly string[]): void {
  const metadata = readEquationMetadata();
  const combined = documents.join("\n");
  const explanationIds = [
    ...combined.matchAll(/<details id="([^"]+)" class="equation-explanation"/g),
  ]
    .map((match) => match[1])
    .filter((identifier): identifier is string => identifier !== undefined);
  if (explanationIds.length !== metadata.equations.length) {
    failures.push(
      `${label} has ${explanationIds.length} equation explanations; ` +
        `expected ${metadata.equations.length}`,
    );
  }
  if (new Set(explanationIds).size !== explanationIds.length) {
    failures.push(`${label} has duplicate equation explanation fragments`);
  }
  if (/\b(?:href|src)="(?:equation:|notation:)/.test(combined)) {
    failures.push(`${label} contains an unresolved equation-metadata pseudo-URL`);
  }
  for (const equation of metadata.equations) {
    const fragment = explanationFragment(equation.id);
    const equationOpen = combined.match(
      new RegExp(
        `<div id="${escapePattern(equation.id)}" class="equation numbered-equation" ` +
          `data-equation-number="([^"]+)">`,
      ),
    );
    const number = equationOpen?.[1];
    if (number === undefined) {
      failures.push(`${label} is missing numbered ${equation.id}`);
      continue;
    }
    const control = new RegExp(
      `<button type="button" class="equation-explain-button" ` +
        `aria-expanded="false" aria-controls="${fragment}" ` +
        `data-equation-explain="${fragment}">Explain equation \\(${escapePattern(number)}\\)` +
        "<\\/button>",
    );
    if (!control.test(combined)) {
      failures.push(`${label} ${equation.id} has no separately labelled explanation button`);
    }
    const details = new RegExp(
      `<details id="${fragment}" class="equation-explanation" ` +
        `data-equation-explanation="${escapePattern(equation.id)}">` +
        `<summary>Explain equation \\(${escapePattern(number)}\\)<\\/summary>`,
    );
    if (!details.test(combined)) {
      failures.push(`${label} ${equation.id} has no native-details fallback`);
    }
    if (!combined.includes(`<strong>${escapeHtml(equation.title)}</strong>`)) {
      failures.push(`${label} ${equation.id} is missing its explanation title`);
    }
  }
}

function inspectPropositions(label: string, documents: readonly string[]): void {
  const propositions = readPropositionRegistry();
  const references = readPropositionReferences();
  const combined = documents.join("\n");
  if (/\b(?:href|src)="proposition:/.test(combined)) {
    failures.push(`${label} contains an unresolved proposition pseudo-URL`);
  }
  for (const proposition of propositions) {
    if (count(combined, new RegExp(`\\sid="${escapePattern(proposition.anchor)}"`, "g")) !== 1) {
      failures.push(`${label} must contain exactly one definition for ${proposition.id}`);
    }
    const renderedReferences = [
      ...combined.matchAll(
        new RegExp(`<a\\b(?<attributes>[^>]*\\bdata-proposition="${proposition.id}"[^>]*)>`, "g"),
      ),
    ];
    const expectedReferences = references.filter(({ id }) => id === proposition.id).length;
    if (renderedReferences.length !== expectedReferences) {
      failures.push(
        `${label} has ${renderedReferences.length} ${proposition.id} references; ` +
          `expected ${expectedReferences}`,
      );
    }
    for (const match of renderedReferences) {
      const attributes = match.groups?.attributes ?? "";
      if (!/\bclass="[^"]*\bproposition-ref\b[^"]*"/.test(attributes)) {
        failures.push(`${label} ${proposition.id} reference lacks proposition-ref styling`);
      }
      if (
        attribute(attributes, "aria-label") !== propositionLabel(proposition) ||
        attribute(attributes, "title") !== proposition.currentStatus
      ) {
        failures.push(`${label} ${proposition.id} reference has stale accessible metadata`);
      }
    }
  }
}

function inspectFootnotes(label: string, documents: readonly string[]): void {
  const expected = footnoteInventory();
  const combined = documents.join("\n");
  const references = count(combined, /<a\b[^>]*\brole="doc-noteref"[^>]*>/g);
  const endnotes = count(combined, /<li\b[^>]*\bid="fn\d+"[^>]*>/g);
  const backlinks = count(combined, /<a\b[^>]*\brole="doc-backlink"[^>]*>/g);
  if (
    references !== expected.references.length ||
    endnotes !== expected.definitions.size ||
    backlinks < expected.definitions.size
  ) {
    failures.push(
      `${label} footnote semantics differ: ${references} references, ` +
        `${endnotes} endnotes, ${backlinks} backlinks; expected ` +
        `${expected.references.length}/${expected.definitions.size}/${expected.definitions.size}`,
    );
  }
  if (!/\brole="doc-(?:endnotes|footnote)"/.test(combined)) {
    failures.push(`${label} has no semantic footnote container`);
  }
  for (const match of combined.matchAll(/<a\b(?<attributes>[^>]*\brole="doc-noteref"[^>]*)>/g)) {
    const attributes = match.groups?.attributes ?? "";
    if (!attribute(attributes, "href").includes("#fn")) {
      failures.push(`${label} footnote reference does not target an endnote`);
    }
    if (!/^Read footnote \d+$/.test(attribute(attributes, "aria-label"))) {
      failures.push(`${label} footnote reference lacks a descriptive accessible name`);
    }
  }
  for (const match of combined.matchAll(
    /<li\b(?<attributes>[^>]*\bid="fn\d+"[^>]*)>(?<body>[\s\S]*?)<\/li>/g,
  )) {
    const body = match.groups?.body ?? "";
    if (!/\brole="doc-backlink"/.test(body)) {
      failures.push(`${label} footnote endnote lacks a backlink`);
    } else if (!/\baria-label="Return to footnote reference \d+"/.test(body)) {
      failures.push(`${label} footnote backlink lacks a descriptive accessible name`);
    }
  }
  const footnoteContent =
    combined.match(/<(?:section|aside)\b[^>]*\bclass="footnotes[^"]*"[\s\S]*/)?.[0] ?? "";
  if (!/<math\b/.test(footnoteContent)) {
    failures.push(`${label} does not preserve MathML inside a footnote`);
  }
  if (!/<a\b[^>]*class="source-marker"[^>]*>S43<\/a>/.test(footnoteContent)) {
    failures.push(`${label} does not preserve source-marker links inside a footnote`);
  }
}

function localTarget(sourceRelative: string, url: string): { target: string; fragment: string } {
  const [pathname = "", fragment = ""] = url.split("#", 2);
  const decoded = decodeURIComponent(pathname);
  let target: string;
  if (decoded.startsWith("/rsi-model/")) {
    target = path.join(site, decoded.slice("/rsi-model/".length));
  } else {
    target = path.resolve(
      path.dirname(path.join(site, sourceRelative)),
      decoded || path.basename(sourceRelative),
    );
  }
  if (fs.existsSync(target) && fs.statSync(target).isDirectory()) {
    target = path.join(target, "index.html");
  }
  return { target, fragment: decodeURIComponent(fragment) };
}

if (!fs.existsSync(site) || !fs.statSync(site).isDirectory()) {
  fail(["_site/ does not exist; run pnpm run build:site"]);
}
if (!fs.existsSync(monolithicHtml) || !fs.statSync(monolithicHtml).isFile()) {
  fail(["standalone HTML does not exist; run pnpm run build:manuscript"]);
}

const failures: string[] = [];
const artifacts = buildArtifactData();
const artifactReferences = readArtifactReferences();
const equationArtifactReferences = readEquationMetadata().equations.reduce(
  (total, equation) =>
    total + equation.links.filter(({ target }) => /^outputs\/.+\.csv$/.test(target)).length,
  0,
);
const expectedArtifactReferences = artifactReferences.length + equationArtifactReferences;
if (!fs.existsSync(viteManifest) || !fs.statSync(viteManifest).isFile()) {
  failures.push("missing Vite manifest assets/rsi/manifest.json");
}
const htmlByPage = new Map<string, string>();
for (const relative of [...expectedPages, "404.html"]) {
  const file = path.join(site, relative);
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) {
    failures.push(`missing page ${relative}`);
    continue;
  }
  htmlByPage.set(relative, fs.readFileSync(file, "utf8"));
}

const idsByPage = new Map<string, Set<string>>();
for (const [relative, html] of htmlByPage) {
  const pageIds = ids(html);
  const duplicates = pageIds.filter((identifier, index) => pageIds.indexOf(identifier) !== index);
  if (duplicates.length) {
    failures.push(`${relative} has duplicate IDs: ${[...new Set(duplicates)].join(", ")}`);
  }
  idsByPage.set(relative, new Set(pageIds));
  if (count(html, /<script type="module" [^>]*data-rsi-vite-entry><\/script>/g) !== 1) {
    failures.push(`${relative} must load exactly one Vite entry bundle`);
  }
  if (count(html, /<dialog class="artifact-viewer"/g) !== 1) {
    failures.push(`${relative} must contain exactly one reusable artifact viewer`);
  }
  if (/<!-- (?:SITE_HEAD|SITE_NAV|PAGE_NAV) -->/.test(html)) {
    failures.push(`${relative} contains an unreplaced build marker`);
  }
  if (relative !== "404.html") {
    for (const required of [
      '<nav id="quarto-sidebar"',
      '<nav class="page-navigation"',
      '<main class="content" id="quarto-document-content"',
      'rel="canonical"',
      'property="og:title"',
      'aria-label="Search"',
    ]) {
      if (!html.includes(required)) {
        failures.push(`${relative} is missing ${required}`);
      }
    }
    if (count(html, /sidebar-link active/g) !== 1) {
      failures.push(`${relative} must identify exactly one current chapter`);
    }
  }
}

const firstPage = htmlByPage.get("index.html") || "";
const lastPage = htmlByPage.get("data/index.html") || "";
const openingOrder = [
  'id="abstract"',
  'id="executive-summary"',
  'id="scope-claims-and-evidence"',
  'id="proposition-ladder"',
  'id="how-to-read-this-document"',
].map((marker) => firstPage.indexOf(marker));
if (
  openingOrder.some((position) => position < 0) ||
  openingOrder.some((position, index) => index > 0 && position <= (openingOrder[index - 1] ?? -1))
) {
  failures.push("index.html does not preserve the abstract → summary → scope opening order");
}
const renderedOpening = firstPage.slice(0, Math.max(0, openingOrder[0] ?? -1));
if (/(?:release candidate|dirty worktree|Linux CI|TODO)/i.test(renderedOpening)) {
  failures.push("index.html exposes operational release narration before the abstract");
}
if (!/<div class="nav-page nav-page-previous">\s*<\/div>/.test(firstPage)) {
  failures.push("index.html must have an empty previous-page slot");
}
if (!/<div class="nav-page nav-page-next">\s*<a [^>]*class="pagination-link"/.test(firstPage)) {
  failures.push("index.html must retain its next-page link");
}
if (!/<div class="nav-page nav-page-next">\s*<\/div>/.test(lastPage)) {
  failures.push("data/index.html must have an empty next-page slot");
}
if (!/<div class="nav-page nav-page-previous">\s*<a [^>]*class="pagination-link"/.test(lastPage)) {
  failures.push("data/index.html must retain its previous-page link");
}
const siteCss = fs.readFileSync(path.join(site, "quarto.css"), "utf8");
if (
  !/\.page-navigation \.nav-page:not\(:has\(\.pagination-link\)\)\s*\{[^}]*display:\s*none/s.test(
    siteCss,
  )
) {
  failures.push("quarto.css must hide empty page-navigation slots");
}
if (
  !/figure img\s*\{[^}]*display:\s*block[^}]*width:\s*auto[^}]*max-width:\s*100%[^}]*height:\s*auto/s.test(
    siteCss,
  )
) {
  failures.push("quarto.css must keep figure images responsive without forced upscaling");
}
if (
  [...siteCss.matchAll(/figure img\s*\{([^}]*)\}/g)].some((match) =>
    /(?:^|[;\s])width:\s*100%/.test(match[1] ?? ""),
  )
) {
  failures.push("quarto.css must not force every figure image to full column width");
}
for (const className of approvedFigureClasses) {
  if (!siteCss.includes(`.${className}`)) {
    failures.push(`quarto.css is missing .${className}`);
  }
}
if (!siteCss.includes(".proposition-ref") || !siteCss.includes(".proposition-definition:target")) {
  failures.push("quarto.css is missing proposition reference/target styling");
}
if (
  !siteCss.includes('a[role="doc-noteref"]') ||
  !siteCss.includes('.footnotes li[id^="fn"]:target') ||
  !siteCss.includes('a[role="doc-backlink"]')
) {
  failures.push("quarto.css is missing footnote reference/endnote/backlink styling");
}

const attributePattern = /\s(?:href|src)="([^"]+)"/g;
for (const [relative, html] of htmlByPage) {
  for (const match of html.matchAll(attributePattern)) {
    const url = match[1] ?? "";
    if (/^(?:https?:|mailto:|data:|javascript:)/.test(url) || url === "") {
      continue;
    }
    if (url.startsWith("/") && !url.startsWith("/rsi-model/")) {
      failures.push(`${relative} has project-unsafe root URL ${url}`);
      continue;
    }
    const { target, fragment } = localTarget(relative, url);
    if (!target.startsWith(`${site}${path.sep}`) && target !== site) {
      failures.push(`${relative} escapes the site tree via ${url}`);
      continue;
    }
    if (!fs.existsSync(target) || !fs.statSync(target).isFile()) {
      failures.push(`${relative} links to missing file ${url}`);
      continue;
    }
    if (fragment) {
      const targetRelative = path.relative(site, target).split(path.sep).join("/");
      let targetIds = idsByPage.get(targetRelative);
      if (!targetIds) {
        targetIds = new Set(ids(fs.readFileSync(target, "utf8")));
      }
      if (!targetIds.has(fragment)) {
        failures.push(`${relative} links to missing fragment ${url}`);
      }
    }
  }
}

const sourceHtml = htmlByPage.get("sources/index.html") || "";
const sourceDefinitions = new Set(
  [...sourceHtml.matchAll(/\sid="source-s(\d+)"/g)].map((match) => Number(match[1])),
);
if (sourceDefinitions.size === 0) {
  failures.push("sources page has no source-entry anchors");
}
for (const [relative, html] of htmlByPage) {
  for (const match of html.matchAll(/<a href="([^"]*#source-s(\d+))" class="source-marker"/g)) {
    if (!sourceDefinitions.has(Number(match[2]))) {
      failures.push(`${relative} has unresolved source marker ${match[1]}`);
    }
  }
}

const standalone = fs.readFileSync(monolithicHtml, "utf8");
if (!standalone.includes("data:font/woff2;base64")) {
  failures.push("standalone HTML does not embed the pinned math font");
}
for (const name of [
  "STIXTwoMath-Regular.woff2",
  "STIXTwoMath-OFL.txt",
  "STIXTwoMath-METADATA.json",
]) {
  const source = path.join(root, "docs", "assets", "fonts", name);
  const deployed = path.join(site, "assets", "fonts", name);
  if (!fs.existsSync(deployed) || !fs.readFileSync(deployed).equals(fs.readFileSync(source))) {
    failures.push(`site font asset differs from source: ${name}`);
  }
}
if (count(standalone, /\bdata-artifact-reference="/g) !== expectedArtifactReferences) {
  failures.push(
    `standalone artifact references differ: source/generated ${expectedArtifactReferences}, ` +
      `HTML ${count(standalone, /\bdata-artifact-reference="/g)}`,
  );
}
const standaloneWithoutScripts = standalone.replace(/<script\b[\s\S]*?<\/script>/g, "");
if (count(standaloneWithoutScripts, /<dialog class="artifact-viewer"/g) !== 1) {
  failures.push("standalone HTML must contain exactly one shared artifact viewer shell");
}
if (
  count(standalone, /data-artifact-payload data-compression="gzip"/g) !== 1 ||
  count(standalone, /data-rsi-artifact-viewer/g) !== 2
) {
  failures.push("standalone HTML must embed one compressed payload and one inline viewer bundle");
}
const standaloneArticleReferences = count(standalone, /\bdata-artifact-reference="/g);
const siteArticleReferences = [...htmlByPage]
  .filter(([relative]) => relative !== "data/index.html" && relative !== "404.html")
  .reduce((sum, [, pageHtml]) => sum + count(pageHtml, /\bdata-artifact-reference="/g), 0);
if (siteArticleReferences !== standaloneArticleReferences) {
  failures.push(
    `site/standalone artifact-reference parity differs: site ${siteArticleReferences}, ` +
      `standalone ${standaloneArticleReferences}`,
  );
}
const artifactDirectory = path.join(site, "data", "artifacts");
if (
  !fs.existsSync(artifactDirectory) ||
  fs.readdirSync(artifactDirectory).filter((name) => name.endsWith(".json")).length !==
    artifacts.length
) {
  failures.push(`site must contain metadata for exactly ${artifacts.length} artifacts`);
}
const catalogHtml = htmlByPage.get("data/index.html") || "";
for (const artifact of artifacts) {
  const deployed = path.join(site, artifact.path);
  const metadata = path.join(artifactDirectory, `${artifact.key}.json`);
  if (
    !fs.existsSync(deployed) ||
    !fs.readFileSync(deployed).equals(fs.readFileSync(path.join(root, artifact.path)))
  ) {
    failures.push(`${artifact.path} was not deployed byte-for-byte`);
  }
  if (!fs.existsSync(metadata)) {
    failures.push(`${artifact.path} has no viewer metadata`);
  } else {
    const parsed: unknown = JSON.parse(fs.readFileSync(metadata, "utf8"));
    if (
      parsed === null ||
      typeof parsed !== "object" ||
      !("hash" in parsed) ||
      parsed.hash !== artifact.hash ||
      !("rows" in parsed) ||
      !Array.isArray(parsed.rows) ||
      parsed.rows.length !== artifact.rows.length
    ) {
      failures.push(`${artifact.path} viewer metadata differs from the validated CSV`);
    }
  }
  if (
    !catalogHtml.includes(`id="${artifact.key}"`) ||
    !catalogHtml.includes(`data-artifact="${artifact.path}"`)
  ) {
    failures.push(`${artifact.path} is absent from the data catalog`);
  }
  const htmlPage = path.join(artifactDirectory, `${artifact.key}.html`);
  if (!fs.existsSync(htmlPage) || !fs.readFileSync(htmlPage, "utf8").includes("<caption>")) {
    failures.push(`${artifact.path} has no readable static HTML data page`);
  }
}
for (const match of standalone.matchAll(/<a\b(?<attributes>[^>]*href="[^"]+\.csv"[^>]*)>/g)) {
  const attributes = match.groups?.attributes ?? "";
  if (
    !/\bdownload(?:\s|>|=)/.test(attributes) ||
    !/\baria-label="[^"]*Download[^"]*CSV[^"]*"/i.test(attributes)
  ) {
    failures.push("standalone has an ambiguously labeled raw CSV link");
  }
}
for (const [relative, html] of htmlByPage) {
  for (const match of html.matchAll(
    /<button\b[^>]*data-artifact-view[^>]*data-artifact="(?<path>outputs\/[^"]+)"[^>]*>/g,
  )) {
    const artifactPath = match.groups?.path ?? "";
    const artifact = artifacts.find((candidate) => candidate.path === artifactPath);
    if (artifact === undefined) {
      failures.push(`${relative} references unknown artifact ${artifactPath}`);
      continue;
    }
    if (
      !match[0].includes(`data-artifact-key="${artifact.key}"`) ||
      !match[0].includes(`data-artifact-hash="${artifact.hash}"`) ||
      !match[0].includes("data-artifact-json=") ||
      !match[0].includes("data-artifact-download=") ||
      !match[0].includes("data-artifact-full-page=")
    ) {
      failures.push(`${relative} has an incomplete View data control for ${artifactPath}`);
    }
  }
  for (const match of html.matchAll(/<a\b(?<attributes>[^>]*href="[^"]+\.csv"[^>]*)>/g)) {
    const attributes = match.groups?.attributes ?? "";
    if (
      !/\bdownload(?:\s|>|=)/.test(attributes) ||
      !/\baria-label="[^"]*Download[^"]*CSV[^"]*"/i.test(attributes)
    ) {
      failures.push(`${relative} has an ambiguously labeled raw CSV link`);
    }
  }
}
const sitePages = expectedPages
  .filter((name) => name !== "data/index.html")
  .map((name) =>
    (htmlByPage.get(name) || "").replace(/<dialog class="artifact-viewer"[\s\S]*?<\/dialog>/g, ""),
  );
const siteFigures = inspectFigures("site", sitePages);
const standaloneWithoutViewer = standalone.replace(
  /<dialog class="artifact-viewer"[\s\S]*?<\/dialog>/g,
  "",
);
const standaloneFigures = inspectFigures("standalone", [standaloneWithoutViewer]);
inspectFigureReferences("site", sitePages);
inspectFigureReferences("standalone", [standaloneWithoutViewer]);
inspectEquationExplanations("site", sitePages);
inspectEquationExplanations("standalone", [standaloneWithoutViewer]);
inspectPropositions("site", sitePages);
inspectPropositions("standalone", [standaloneWithoutViewer]);
inspectFootnotes("site", sitePages);
inspectFootnotes("standalone", [standaloneWithoutViewer]);
const expectedNotationLinks = readEquationMetadata().terms.size;
const siteNotationLinks = count(
  htmlByPage.get("notation/index.html") || "",
  /class="equation-explanation-reference"/g,
);
const standaloneNotationLinks = count(standalone, /class="equation-explanation-reference"/g);
if (siteNotationLinks !== expectedNotationLinks) {
  failures.push(
    `site notation register has ${siteNotationLinks} explanation links; ` +
      `expected ${expectedNotationLinks}`,
  );
}
if (standaloneNotationLinks !== expectedNotationLinks) {
  failures.push(
    `standalone notation register has ${standaloneNotationLinks} explanation links; ` +
      `expected ${expectedNotationLinks}`,
  );
}
if (
  siteFigures.some(
    (figure, index) =>
      figure.id !== standaloneFigures[index]?.id ||
      figure.number !== standaloneFigures[index]?.number,
  )
) {
  failures.push("site and standalone figure identifiers/numbers differ");
}
const parityChecks: ReadonlyArray<readonly [string, RegExp]> = [
  ["equations", /class="equation numbered-equation"/g],
  ["equation scroll regions", /class="equation-math-scroll"/g],
  ["equation explanations", /class="equation-explanation"/g],
  ["tables", /<table\b/g],
  ["figures", /<figure\b[^>]*\bid="fig-[A-Za-z0-9_-]+"/g],
  ["source definitions", /\sid="source-s\d+"/g],
  ["proposition definitions", /\sid="proposition-p(?:1|2|3a|3b|4a|4b)"/g],
  ["proposition references", /data-proposition="P(?:1|2|3a|3b|4a|4b)"/g],
  ["footnote references", /<a\b[^>]*\brole="doc-noteref"/g],
  ["footnote definitions", /<li\b[^>]*\bid="fn\d+"/g],
];
for (const [label, pattern] of parityChecks) {
  const expected = count(standaloneWithoutViewer, pattern);
  const actual = sitePages.reduce((total, html) => total + count(html, pattern), 0);
  if (actual !== expected) {
    failures.push(`${label} differ: standalone ${expected}, site ${actual}`);
  }
}

const stableIds = [
  ...fs.readFileSync(path.join(root, "docs", `${stem}.md`), "utf8").matchAll(/\{#([^\s}]+)/g),
]
  .map((match) => match[1])
  .filter((identifier): identifier is string => identifier !== undefined);
for (const identifier of stableIds) {
  const occurrences = sitePages.reduce(
    (total, html) => total + Number(ids(html).includes(identifier)),
    0,
  );
  if (occurrences !== 1) {
    failures.push(`stable identifier ${identifier} occurs on ${occurrences} site pages`);
  }
}

const equationNumbers = sitePages.flatMap((html) =>
  [...html.matchAll(/data-equation-number="([^"]+)"/g)]
    .map((match) => match[1])
    .filter((number): number is string => number !== undefined),
);
const mainNumbers = equationNumbers.filter((value) => /^\d+$/.test(value)).map(Number);
if (mainNumbers.some((number, index) => number !== index + 1)) {
  failures.push(`main equation sequence is not contiguous: ${mainNumbers.join(", ")}`);
}

const download = path.join(site, "download", `${stem}.html`);
if (!fs.existsSync(download) || !fs.statSync(download).isFile()) {
  failures.push("standalone download is missing");
} else if (!fs.readFileSync(download).equals(fs.readFileSync(monolithicHtml))) {
  failures.push("standalone download differs from canonical HTML");
}

const propositionSearch = fs.readFileSync(path.join(site, "search.json"), "utf8");
for (const proposition of readPropositionRegistry()) {
  if (
    !propositionSearch.includes(propositionLabel(proposition)) ||
    !propositionSearch.includes(proposition.canonicalWording)
  ) {
    failures.push(`site search index is missing ${proposition.id}`);
  }
}
if (!propositionSearch.includes("positive-stock equilibrium")) {
  failures.push("site search index does not retain local footnote text");
}
if (
  !firstPage.includes('href="#proposition-ladder"') ||
  !firstPage.includes('href="#proposition-p1"')
) {
  failures.push("index.html table of contents does not expose the proposition ladder");
}

if (failures.length) fail(failures);
process.stdout.write(
  `PASS site crawl: ${htmlByPage.size} HTML files, ` +
    `${stableIds.length} stable IDs, ${sourceDefinitions.size} sources, ` +
    `${equationNumbers.length} numbered equations, ${siteFigures.length} numbered figures, ` +
    `${readPropositionReferences().length} proposition references, ` +
    `${artifacts.length} data artifacts\n`,
);
