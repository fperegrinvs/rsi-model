#!/usr/bin/env bun

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { build as viteBuild } from "vite";
import { artifactViewerShell } from "../web/artifact-viewer-shell.ts";
import {
  type ArtifactData,
  buildArtifactData,
  decorateArtifactReferences,
  renderArtifactReference,
} from "./artifacts.ts";
import { writeEquationExplanationMap } from "./equations.ts";
import {
  fragmentPaths,
  fragments,
  readManuscript,
  root,
  stem,
  writeMonolithicManuscript,
} from "./manuscript-config.ts";
import { writePropositionMap } from "./propositions.ts";
import { normalizeRenderedFootnotes } from "./readability.ts";
import { tableRecords, validateTableReferences, writeTableMap } from "./tables.ts";

const quarto = process.env.QUARTO_BIN || "quarto";
const supportedQuarto = "1.9.38";
const siteProject = path.join(root, "site");
const siteOutput = path.join(root, "_site");
const viteOutput = path.join(siteOutput, "assets", "rsi");
const viteManifest = path.join(viteOutput, "manifest.json");
const fontFiles = [
  "STIXTwoMath-Regular.woff2",
  "STIXTwoMath-OFL.txt",
  "STIXTwoMath-METADATA.json",
] as const;
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

function fail(message: string): never {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function run(command: string, args: string[], options: { env?: NodeJS.ProcessEnv } = {}): string {
  const result = spawnSync(command, args, {
    cwd: root,
    encoding: "utf8",
    ...options,
  });
  if (result.status !== 0) {
    fail(result.stderr || result.stdout || `${command} failed`);
  }
  return result.stdout.trim();
}

function equationRows(): Array<[string, string, string]> {
  const rows: Array<[string, string, string]> = [];
  let main = 0;
  let appendix: string | null = null;
  const appendixCounts = new Map<string, number>();
  for (const [index, file] of fragmentPaths().entries()) {
    const fragment = fragments[index];
    if (fragment === undefined) fail(`Missing fragment at position ${index}`);
    const output = fragmentOutputs.get(fragment);
    if (output === undefined) fail(`No site output configured for ${fragment}`);
    const markdown = fs.readFileSync(file, "utf8");
    for (const line of markdown.split(/\r?\n/)) {
      const appendixMatch = line.match(/^# Appendix ([A-Z]):/);
      if (appendixMatch?.[1] !== undefined) appendix = appendixMatch[1];
      const equationMatch = line.match(/^::: \{#(eq:[A-Za-z0-9_.:-]+) \.equation/);
      if (!equationMatch) continue;
      const equationId = equationMatch[1];
      if (equationId === undefined) fail(`Malformed equation declaration in ${fragment}`);
      let number: string;
      if (appendix === null) {
        main += 1;
        number = String(main);
      } else {
        const count = (appendixCounts.get(appendix) || 0) + 1;
        appendixCounts.set(appendix, count);
        number = `${appendix}.${count}`;
      }
      rows.push([equationId, number, output]);
    }
  }
  return rows;
}

function figureRows(): Array<[string, string, string]> {
  const rows: Array<[string, string, string]> = [];
  for (const [index, file] of fragmentPaths().entries()) {
    const fragment = fragments[index];
    if (fragment === undefined) fail(`Missing fragment at position ${index}`);
    const output = fragmentOutputs.get(fragment);
    if (output === undefined) fail(`No site output configured for ${fragment}`);
    const markdown = fs.readFileSync(file, "utf8");
    for (const match of markdown.matchAll(
      /!\[[\s\S]*?\]\([^)]+\)\{#(fig-[A-Za-z0-9_-]+)[^}]*\}/g,
    )) {
      const figureId = match[1];
      if (figureId === undefined) fail(`Malformed figure declaration in ${fragment}`);
      rows.push([figureId, String(rows.length + 1), output]);
    }
  }
  const actual = rows.map(([identifier]) => identifier);
  if (
    actual.length !== expectedFigureIds.length ||
    actual.some((identifier, index) => identifier !== expectedFigureIds[index])
  ) {
    fail(
      `Figure inventory/order mismatch: expected ${expectedFigureIds.join(", ")}; ` +
        `found ${actual.join(", ")}`,
    );
  }
  return rows;
}

function escapePattern(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function normalizeSiteFigures(rows: ReadonlyArray<readonly [string, string, string]>): void {
  for (const [identifier, number, output] of rows) {
    const file = path.join(siteOutput, output);
    let html = fs.readFileSync(file, "utf8");
    const wrapperPattern = new RegExp(
      `<div id="${escapePattern(identifier)}" class="([^"]*)"([^>]*)>\\s*` +
        '<figure class="([^"]*)">',
    );
    let normalized = false;
    let isWide = false;
    html = html.replace(
      wrapperPattern,
      (_whole, wrapperClasses: string, wrapperAttributes: string, figureClasses: string) => {
        const presentation = wrapperClasses
          .split(/\s+/)
          .find((className) => /^figure-(?:compact|standard|wide)$/.test(className));
        if (presentation === undefined) {
          fail(`${identifier} has no rendered presentation class`);
        }
        isWide = presentation === "figure-wide";
        normalized = true;
        const classes = [
          ...new Set([...figureClasses.split(/\s+/), presentation, "numbered-figure"]),
        ]
          .filter(Boolean)
          .join(" ");
        return (
          `<div class="${wrapperClasses}"${wrapperAttributes}>` +
          `\n<figure id="${identifier}" class="${classes}" data-figure-number="${number}">`
        );
      },
    );
    const captionPattern = /(<figcaption\b[^>]*>\s*)Figure(?:&nbsp;|\s)[^:<]+:\s*/;
    html = html.replace(
      captionPattern,
      `$1<a href="#${identifier}" class="figure-number" ` +
        `aria-label="Figure ${number}" title="Figure ${number}">Figure ${number}</a>. `,
    );
    if (isWide) {
      const imagePattern = new RegExp(
        `(<figure id="${escapePattern(identifier)}"[^>]*>[\\s\\S]*?)` +
          "(<img\\b(?<attributes>[^>]*)>)([\\s\\S]*?</figure>)",
      );
      html = html.replace(
        imagePattern,
        (_whole, before: string, image: string, imageAttributes: string, after: string) => {
          const source = imageAttributes.match(/\bsrc="([^"]+)"/)?.[1];
          if (source === undefined) fail(`${identifier} rendered image has no source`);
          return (
            `${before}<a href="${source}" class="figure-full-resolution-link" ` +
            `aria-label="Open Figure ${number} at full resolution" ` +
            `title="Open full-resolution Figure ${number}">${image}</a>${after}`
          );
        },
      );
    }
    if (!normalized || !html.includes(`data-figure-number="${number}"`)) {
      fail(`Could not normalize ${identifier} in ${output}`);
    }
    fs.writeFileSync(file, html);
  }
}

function normalizeSiteTables(): void {
  for (const { identifier, number, output } of tableRecords()) {
    const file = path.join(siteOutput, output);
    let html = fs.readFileSync(file, "utf8");
    const wrapperPattern = new RegExp(
      `<div id="${escapePattern(identifier)}" class="([^"]*)"([^>]*)>`,
    );
    let normalized = false;
    html = html.replace(wrapperPattern, (_whole, classes: string, attributes: string) => {
      normalized = true;
      const merged = [...new Set([...classes.split(/\s+/), "numbered-table"])]
        .filter(Boolean)
        .join(" ");
      const retained = attributes.replace(/\sdata-table-number="[^"]*"/g, "");
      return (
        `<div id="${identifier}" class="${merged}"${retained} ` + `data-table-number="${number}">`
      );
    });
    const captionPattern = new RegExp(
      `(<figcaption\\b[^>]*\\bid="${escapePattern(identifier)}-caption-[^"]+"[^>]*>\\s*)` +
        "Table(?:&nbsp;|\\s)[^:<]+:\\s*",
    );
    html = html.replace(
      captionPattern,
      `$1<a href="#${identifier}" class="table-number" ` +
        `aria-label="Table ${number}" title="Table ${number}">Table ${number}</a>. `,
    );
    if (
      !normalized ||
      !html.includes(`data-table-number="${number}"`) ||
      !html.includes(`title="Table ${number}">Table ${number}</a>.`)
    ) {
      fail(`Could not normalize ${identifier} in ${output}`);
    }
    fs.writeFileSync(file, html);
  }
}

function copyImages(): void {
  const markdown = readManuscript();
  const imagePattern = /!\[[\s\S]*?\]\(\.\.\/outputs\/([^)]+)\)\{#fig-[^}]+\}/g;
  for (const match of markdown.matchAll(imagePattern)) {
    const relative = match[1];
    if (relative === undefined) fail("Malformed output-image reference in manuscript");
    const source = path.join(root, "outputs", relative);
    const destination = path.join(siteOutput, "outputs", relative);
    if (!fs.existsSync(source) || !fs.statSync(source).isFile()) {
      fail(`Missing manuscript image: ${source}`);
    }
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.copyFileSync(source, destination);
  }
}

function copyFonts(): void {
  const sourceDirectory = path.join(root, "docs", "assets", "fonts");
  const destinationDirectory = path.join(siteOutput, "assets", "fonts");
  fs.mkdirSync(destinationDirectory, { recursive: true });
  for (const name of fontFiles) {
    const source = path.join(sourceDirectory, name);
    if (!fs.existsSync(source) || !fs.statSync(source).isFile()) {
      fail(`Missing publication font asset: ${source}`);
    }
    fs.copyFileSync(source, path.join(destinationDirectory, name));
  }
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function writeArtifactAssets(artifacts: readonly ArtifactData[]): void {
  const artifactDirectory = path.join(siteOutput, "data", "artifacts");
  fs.mkdirSync(artifactDirectory, { recursive: true });
  for (const artifact of artifacts) {
    const source = path.join(root, artifact.path);
    const destination = path.join(siteOutput, artifact.path);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.copyFileSync(source, destination);
    if (!fs.readFileSync(destination).equals(fs.readFileSync(source))) {
      fail(`Deployed artifact differs byte-for-byte: ${artifact.path}`);
    }
    fs.writeFileSync(
      path.join(artifactDirectory, `${artifact.key}.json`),
      `${JSON.stringify(artifact)}\n`,
    );
  }
  const catalog = artifacts.map(({ rows, ...artifact }) => ({
    ...artifact,
    rowCount: rows.length,
  }));
  fs.writeFileSync(path.join(siteOutput, "data", "catalog.json"), `${JSON.stringify(catalog)}\n`);
}

function injectArtifactCatalog(artifacts: readonly ArtifactData[]): void {
  const file = path.join(siteOutput, "data", "index.html");
  let html = fs.readFileSync(file, "utf8");
  const marker = "<!-- ARTIFACT_CATALOG -->";
  if (!html.includes(marker)) fail("Data catalog marker is missing");
  const cards = artifacts
    .map(
      (artifact) =>
        `<article class="artifact-card" id="${escapeHtml(artifact.key)}">` +
        `<h2><a href="artifacts/${artifact.key}.html">${escapeHtml(artifact.title)}</a></h2>` +
        `<p>${escapeHtml(artifact.description)}</p>` +
        `<dl><div><dt>Rows</dt><dd>${artifact.rows.length.toLocaleString("en-US")}</dd></div>` +
        `<div><dt>Columns</dt><dd>${artifact.columns.length.toLocaleString("en-US")}</dd></div>` +
        `<div><dt>Class</dt><dd>${escapeHtml(artifact.sourceClass)}</dd></div>` +
        `<div><dt>SHA-256</dt><dd><code>${artifact.hash}</code></dd></div></dl>` +
        `<p><a href="../${escapeHtml(artifact.path)}" class="artifact-link" ` +
        `data-artifact="${escapeHtml(artifact.path)}">${escapeHtml(artifact.title)}</a></p>` +
        `<p class="artifact-card-path"><code>${escapeHtml(artifact.path)}</code></p>` +
        "</article>",
    )
    .join("\n");
  html = html.replace(marker, `<div class="artifact-catalog">${cards}</div>`);
  fs.writeFileSync(file, html);
}

function writeArtifactHtmlPages(artifacts: readonly ArtifactData[]): void {
  const directory = path.join(siteOutput, "data", "artifacts");
  fs.mkdirSync(directory, { recursive: true });
  for (const artifact of artifacts) {
    const file = path.join(directory, `${artifact.key}.html`);
    const keyColumn = artifact.columns.findIndex((column) => column.key);
    const previewRows = artifact.rows.slice(0, 100);
    const header = artifact.columns
      .map(
        (column) =>
          `<th scope="col">${escapeHtml(
            column.units ? `${column.label} (${column.units})` : column.label,
          )}</th>`,
      )
      .join("");
    const rows = previewRows
      .map(
        (row) =>
          `<tr>${row
            .map((value, index) => {
              const tag = index === keyColumn ? "th" : "td";
              const scope = index === keyColumn ? ' scope="row"' : "";
              return `<${tag}${scope}>${value === "" ? '<span aria-label="Missing value">—</span>' : escapeHtml(value)}</${tag}>`;
            })
            .join("")}</tr>`,
      )
      .join("\n");
    const dataReference = renderArtifactReference(artifact, escapeHtml(artifact.title), {
      download: `../../${artifact.path}`,
      fullPage: `${artifact.key}.html`,
      metadata: `${artifact.key}.json`,
    });
    const disclosure =
      previewRows.length < artifact.rowCount
        ? `<p class="artifact-preview-notice">Preview: first ${previewRows.length.toLocaleString(
            "en-US",
          )} of ${artifact.rowCount.toLocaleString(
            "en-US",
          )} rows. Download the original CSV or use View data for the complete table.</p>`
        : `<p>All ${artifact.rowCount.toLocaleString("en-US")} rows are shown below.</p>`;
    const html = [
      "<!doctype html>",
      '<html lang="en"><head><meta charset="utf-8">',
      '<meta name="viewport" content="width=device-width, initial-scale=1">',
      `<title>${escapeHtml(artifact.title)} · Recursive Industrial Intelligence</title>`,
      '<link rel="stylesheet" href="../../quarto.css">',
      "</head><body>",
      '<a class="site-skip-link" href="#quarto-document-content">Skip to main content</a>',
      '<header class="artifact-site-header"><a href="../../">Recursive Industrial Intelligence</a>',
      '<nav aria-label="Data page"><a href="../">Data catalog</a> · ',
      '<a href="../../sources/">Sources</a> · <a href="../../glossary/">Glossary</a></nav></header>',
      '<noscript><nav class="no-js-navigation" aria-label="Navigation without JavaScript">',
      '<a href="../../">Contents</a> · <a href="../">Data</a> · ',
      '<a href="../../download/Recursive_Industrial_Intelligence_r4.0.html">',
      "Standalone HTML</a></nav></noscript>",
      '<main class="content artifact-data-page" id="quarto-document-content">',
      '<p><a href="../">Back to data catalog</a></p>',
      `<h1>${escapeHtml(artifact.title)}</h1>`,
      `<p>${escapeHtml(artifact.description)}</p>`,
      `<p>${dataReference}</p>`,
      disclosure,
      '<div class="table-wrap artifact-static-preview" tabindex="0" role="region" ',
      `aria-label="${escapeHtml(artifact.title)} static preview">`,
      `<table><caption>${escapeHtml(artifact.title)}</caption><thead><tr>${header}</tr></thead>`,
      `<tbody>${rows}</tbody></table></div>`,
      `<p><strong>Source:</strong> <code>${escapeHtml(artifact.path)}</code><br>`,
      `<strong>SHA-256:</strong> <code>${artifact.hash}</code><br>`,
      `<strong>Freshness:</strong> ${escapeHtml(artifact.freshness)}</p>`,
      "</main>",
      '<footer class="artifact-site-footer"><a href="../">Data catalog</a> · ',
      '<a href="https://github.com/fperegrinvs/rsi-model">Source repository</a></footer>',
      "</body></html>",
    ].join("\n");
    fs.writeFileSync(file, html);
  }
}

function decorateArtifactLinks(artifacts: readonly ArtifactData[]): void {
  for (const file of htmlFiles(siteOutput)) {
    const source = fs.readFileSync(file, "utf8");
    const html = decorateArtifactReferences(source, artifacts, (artifact) => {
      const metadata = path.join(siteOutput, "data", "artifacts", `${artifact.key}.json`);
      const fullPage = path.join(siteOutput, "data", "artifacts", `${artifact.key}.html`);
      const download = path.join(siteOutput, artifact.path);
      return {
        download: relativeHref(file, download),
        fullPage: relativeHref(file, fullPage),
        metadata: relativeHref(file, metadata),
      };
    });
    fs.writeFileSync(file, html);
  }
}

function relativeHref(fromFile: string, toFile: string): string {
  return path.relative(path.dirname(fromFile), toFile).split(path.sep).join("/");
}

function htmlFiles(directory: string): string[] {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) return htmlFiles(target);
    return entry.isFile() && entry.name.endsWith(".html") ? [target] : [];
  });
}

function normalizeSiteFootnotes(): void {
  for (const file of htmlFiles(siteOutput)) {
    const html = fs.readFileSync(file, "utf8");
    fs.writeFileSync(file, normalizeRenderedFootnotes(html));
  }
}

interface ViteManifestEntry {
  css?: string[];
  file: string;
  isEntry?: boolean;
}

function viteEntry(): ViteManifestEntry {
  const parsed: unknown = JSON.parse(fs.readFileSync(viteManifest, "utf8"));
  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    fail("Vite manifest must be a JSON object");
  }
  const entries = Object.values(parsed).filter(
    (candidate): candidate is ViteManifestEntry =>
      typeof candidate === "object" &&
      candidate !== null &&
      "file" in candidate &&
      typeof candidate.file === "string" &&
      (!("css" in candidate) ||
        (Array.isArray(candidate.css) &&
          candidate.css.every((item: unknown) => typeof item === "string"))),
  );
  const entry = entries.find((candidate) => candidate.isEntry === true);
  if (entry === undefined) fail("Vite manifest has no entry bundle");
  return entry;
}

function resolveViteAsset(relative: string): string {
  const asset = path.resolve(viteOutput, relative);
  if (asset !== viteOutput && !asset.startsWith(`${viteOutput}${path.sep}`)) {
    fail(`Vite asset escapes its output directory: ${relative}`);
  }
  if (!fs.existsSync(asset) || !fs.statSync(asset).isFile()) {
    fail(`Vite manifest points to missing asset: ${relative}`);
  }
  return asset;
}

function addViteAssets(): void {
  const entry = viteEntry();
  const script = resolveViteAsset(entry.file);
  const styles = (entry.css ?? []).map(resolveViteAsset);
  for (const file of htmlFiles(siteOutput)) {
    const html = fs.readFileSync(file, "utf8");
    if (html.includes("data-rsi-vite-entry")) {
      fail(`Vite assets were already injected into ${path.relative(siteOutput, file)}`);
    }
    const tags = [
      ...styles.map(
        (style) =>
          `<link rel="stylesheet" href="${relativeHref(file, style)}" data-rsi-vite-style>`,
      ),
      `<script type="module" src="${relativeHref(file, script)}" data-rsi-vite-entry></script>`,
    ].join("\n");
    const rendered = html.replace(/<\/body>/i, `${artifactViewerShell}\n${tags}\n</body>`);
    if (rendered === html) {
      fail(`Could not add Vite assets to ${path.relative(siteOutput, file)}`);
    }
    fs.writeFileSync(file, rendered);
  }
}

function addNonScriptNavigation(): void {
  for (const output of [...fragmentOutputs.values(), "data/index.html"]) {
    const file = path.join(siteOutput, output);
    const html = fs.readFileSync(file, "utf8");
    const routes: ReadonlyArray<readonly [string, string]> = [
      ["Contents", path.join(siteOutput, "index.html")],
      ["Glossary", path.join(siteOutput, "glossary", "index.html")],
      ["Sources", path.join(siteOutput, "sources", "index.html")],
      ["Data", path.join(siteOutput, "data", "index.html")],
      ["Standalone HTML", path.join(siteOutput, "download", `${stem}.html`)],
    ];
    const links = routes
      .map(([label, target]) => `<a href="${relativeHref(file, target)}">${label}</a>`)
      .join(" · ");
    const accessibilityNavigation = [
      '<a class="site-skip-link" href="#quarto-document-content">',
      "Skip to main content</a>",
      '<noscript><nav class="no-js-navigation" ',
      'aria-label="Navigation without JavaScript">',
      links,
      "</nav></noscript>",
    ].join("");
    const rendered = html.replace(/(<body\b[^>]*>)/, `$1\n${accessibilityNavigation}`);
    if (rendered === html) {
      fail(`Could not add accessibility navigation to ${output}`);
    }
    fs.writeFileSync(file, rendered);
  }
}

async function main(): Promise<void> {
  writeMonolithicManuscript();
  run(process.execPath, [path.join(root, "scripts", "build-manuscript.ts")]);
  const version = run(quarto, ["--version"]);
  if (version !== supportedQuarto) {
    fail(`Quarto ${supportedQuarto} required; found ${version || "none"}`);
  }

  fs.rmSync(siteOutput, { recursive: true, force: true });
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "rsi-quarto-"));
  const equationMap = path.join(temporary, "equations.tsv");
  const equationExplanationMap = writeEquationExplanationMap(temporary);
  const propositionMap = writePropositionMap(temporary);
  const figureMap = path.join(temporary, "figures.tsv");
  const figures = figureRows();
  validateTableReferences();
  const tableMap = writeTableMap(temporary);
  const artifacts = buildArtifactData();
  fs.writeFileSync(
    equationMap,
    `${equationRows()
      .map((row) => row.join("\t"))
      .join("\n")}\n`,
  );
  fs.writeFileSync(figureMap, `${figures.map((row) => row.join("\t")).join("\n")}\n`);
  try {
    run(quarto, ["render", siteProject], {
      env: {
        ...process.env,
        EQUATION_MAP_FILE: equationMap,
        EQUATION_EXPLANATION_MAP_FILE: equationExplanationMap,
        PROPOSITION_MAP_FILE: propositionMap,
        FIGURE_MAP_FILE: figureMap,
        TABLE_MAP_FILE: tableMap,
        QUARTO_SITE_MODE: "1",
        SITE_PROJECT_DIR: siteProject,
      },
    });
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }

  normalizeSiteFigures(figures);
  normalizeSiteTables();
  normalizeSiteFootnotes();
  writeArtifactAssets(artifacts);
  injectArtifactCatalog(artifacts);
  writeArtifactHtmlPages(artifacts);
  decorateArtifactLinks(artifacts);
  await viteBuild({
    configFile: path.join(root, "vite.config.ts"),
  });
  addViteAssets();
  copyImages();
  copyFonts();
  const downloadDirectory = path.join(siteOutput, "download");
  fs.mkdirSync(downloadDirectory, { recursive: true });
  fs.copyFileSync(
    path.join(root, "docs", `${stem}.html`),
    path.join(downloadDirectory, `${stem}.html`),
  );
  addNonScriptNavigation();
  process.stdout.write(`Site: ${path.relative(root, siteOutput)}/ (Quarto ${version})\n`);
}

await main();
