#!/usr/bin/env node
"use strict";

/**
 * Build the canonical self-contained long-form HTML manuscript.
 *
 * Requirements:
 *   - Pandoc >= 3 on PATH (or PANDOC_BIN=/path/to/pandoc)
 *
 * In the Codex desktop runtime:
 *   <bundled node> scripts/build_manuscript.cjs
 */

const fs = require("node:fs");
const path = require("node:path");
const {spawnSync} = require("node:child_process");

const root = path.resolve(__dirname, "..");
const stem = "Recursive_Industrial_Intelligence_r4.0";
const releaseTitle = "r4.0";
const versionLabel = "r4.0";
const input = path.join(root, "docs", `${stem}.md`);
const html = path.join(root, "docs", `${stem}.html`);
const css = path.join(root, "docs", "assets", "manuscript.css");
const template = path.join(root, "docs", "assets", "manuscript.html5");
const pandoc = process.env.PANDOC_BIN || "pandoc";

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

for (const file of [input, css, template]) {
  if (!fs.existsSync(file)) fail(`Missing build input: ${file}`);
}

const pandocArgs = [
  input,
  "--from=markdown+smart+tex_math_dollars+pipe_tables+fenced_code_blocks",
  "--to=html5",
  "--standalone",
  "--toc",
  "--toc-depth=3",
  "--section-divs",
  "--mathml",
  "--embed-resources",
  // Figure paths in the Markdown are docs-relative (../outputs/...) so the
  // canonical .md renders on GitHub; resolve them from docs/ here.
  "--resource-path=.:docs",
  `--template=${template}`,
  `--css=${css}`,
  "--metadata=lang:en",
  `--metadata=pagetitle:Recursive Industrial Intelligence — ${releaseTitle}`,
  `--metadata=citationtitle:Recursive Industrial Intelligence — ${releaseTitle}`,
  `--metadata=versionlabel:${versionLabel}`,
  `--metadata=footerlabel:${releaseTitle} · generated from the canonical Markdown source`,
  `--output=${html}`,
];
if (process.env.RELEASE_DATE) {
  pandocArgs.push(`--metadata=releasedate:${process.env.RELEASE_DATE}`);
}
if (process.env.VERSION_DOI) {
  pandocArgs.push(`--metadata=versiondoi:${process.env.VERSION_DOI}`);
}
const built = spawnSync(pandoc, pandocArgs, {
  cwd: root,
  encoding: "utf8",
  stdio: ["ignore", "pipe", "pipe"],
});
if (built.status !== 0) {
  fail(`Pandoc failed:\n${built.stderr || built.stdout}`);
}

const canonicalUrl = process.env.CANONICAL_URL;
let rendered = fs.readFileSync(html, "utf8");
const canonicalMarker = "<!-- CANONICAL_LINK -->";
if (!rendered.includes(canonicalMarker)) {
  fail("Canonical-link marker missing from generated HTML");
}
rendered = rendered.replace(
  canonicalMarker,
  canonicalUrl
    ? `<link rel="canonical" href="${canonicalUrl}">\n` +
      `  <meta name="citation_public_url" content="${canonicalUrl}">`
    : "<!-- Canonical URL omitted until an immutable tagged/archive URL exists. -->",
);
fs.writeFileSync(html, rendered);
const mathCount = (rendered.match(/<math\b/g) || []).length;
const tableCount = (rendered.match(/<table\b/g) || []).length;
if (mathCount < 10) fail(`Expected at least 10 MathML equations; found ${mathCount}`);
if (tableCount < 10) fail(`Expected at least 10 tables; found ${tableCount}`);
if (rendered.includes("$$")) fail("Unconverted TeX delimiter found in generated HTML");

process.stdout.write(
  `HTML: ${path.relative(root, html)} (${mathCount} MathML equations, ${tableCount} tables)\n`,
);
