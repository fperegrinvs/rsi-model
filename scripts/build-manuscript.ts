#!/usr/bin/env bun

/**
 * Build the canonical self-contained long-form HTML manuscript.
 *
 * Requirements:
 *   - Pandoc >= 3 on PATH (or PANDOC_BIN=/path/to/pandoc)
 *
 * In the Codex desktop runtime:
 *   pnpm run build:manuscript
 */

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { brotliCompressSync, gzipSync, constants as zlibConstants } from "node:zlib";
import { artifactViewerShell } from "../web/artifact-viewer-shell.ts";
import {
  artifactViewerBudgets,
  buildArtifactData,
  buildStandaloneArtifactPayload,
  decorateArtifactReferences,
} from "./artifacts.ts";
import { writeEquationExplanationMap } from "./equations.ts";
import { buildInlineViewer } from "./inline-viewer.ts";
import { manuscriptOutput, root, stem, writeMonolithicManuscript } from "./manuscript-config.ts";
import { writePropositionMap } from "./propositions.ts";
import { normalizeRenderedFootnotes } from "./readability.ts";
import { validateTableReferences, writeTableMap } from "./tables.ts";

const releaseTitle = "r4.0";
const versionLabel = "r4.0";
const input = manuscriptOutput;
const html = path.join(root, "docs", `${stem}.html`);
const css = path.join(root, "docs", "assets", "manuscript.css");
const template = path.join(root, "docs", "assets", "manuscript.html5");
const equationFilter = path.join(root, "scripts", "equation_numbering.lua");
const equationExplanationFilter = path.join(root, "scripts", "equation_explanations.lua");
const figureFilter = path.join(root, "scripts", "figure_numbering.lua");
const tableFilter = path.join(root, "scripts", "table_numbering.lua");
const propositionFilter = path.join(root, "scripts", "proposition_links.lua");
const pandoc = process.env.PANDOC_BIN || "pandoc";

function fail(message: string): never {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

for (const file of [
  css,
  template,
  equationFilter,
  equationExplanationFilter,
  figureFilter,
  tableFilter,
  propositionFilter,
]) {
  if (!fs.existsSync(file)) fail(`Missing build input: ${file}`);
}

try {
  writeMonolithicManuscript();
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

const pandocArgs = [
  input,
  "--from=markdown+smart+tex_math_dollars+pipe_tables+fenced_code_blocks",
  "--to=html5",
  "--standalone",
  "--toc",
  "--toc-depth=3",
  "--section-divs",
  "--reference-location=section",
  "--mathml",
  `--lua-filter=${equationFilter}`,
  `--lua-filter=${equationExplanationFilter}`,
  `--lua-filter=${figureFilter}`,
  `--lua-filter=${tableFilter}`,
  `--lua-filter=${propositionFilter}`,
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
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "rsi-pandoc-"));
const explanationMap = writeEquationExplanationMap(temporary);
const propositionMap = writePropositionMap(temporary);
validateTableReferences();
const tableMap = writeTableMap(temporary);
const built = spawnSync(pandoc, pandocArgs, {
  cwd: root,
  encoding: "utf8",
  stdio: ["ignore", "pipe", "pipe"],
  env: {
    ...process.env,
    EQUATION_EXPLANATION_MAP_FILE: explanationMap,
    PROPOSITION_MAP_FILE: propositionMap,
    TABLE_MAP_FILE: tableMap,
  },
});
fs.rmSync(temporary, { recursive: true, force: true });
if (built.status !== 0) {
  fail(`Pandoc failed:\n${built.stderr || built.stdout}`);
}

const canonicalUrl = process.env.CANONICAL_URL;
let rendered = fs.readFileSync(html, "utf8");
rendered = normalizeRenderedFootnotes(rendered);
const artifacts = buildArtifactData();
const payload = buildStandaloneArtifactPayload(artifacts);
const inlineViewer = await buildInlineViewer();
rendered = decorateArtifactReferences(rendered, artifacts, (artifact) => ({
  download: `../${artifact.path}`,
  fullPage: `https://fperegrinvs.github.io/rsi-model/data/artifacts/${artifact.key}.html`,
}));
const viewerAssets = [
  `<style data-rsi-artifact-viewer>${inlineViewer.css.replaceAll("</style>", "<\\/style>")}</style>`,
  artifactViewerShell,
  '<script type="application/octet-stream" data-artifact-payload data-compression="gzip">',
  payload.compressedBase64,
  "</script>",
  `<script data-rsi-artifact-viewer>${inlineViewer.javascript.replaceAll(
    "</script>",
    "<\\/script>",
  )}</script>`,
].join("\n");
const withViewer = rendered.replace(/<\/body>/i, `${viewerAssets}\n</body>`);
if (withViewer === rendered) fail("Could not inject the standalone artifact viewer");
rendered = withViewer;
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
const rawBytes = Buffer.byteLength(rendered);
const gzipBytes = gzipSync(rendered, { level: 9 }).byteLength;
const brotliBytes = brotliCompressSync(rendered, {
  params: {
    [zlibConstants.BROTLI_PARAM_QUALITY]: 11,
  },
}).byteLength;
for (const [label, actual, budget] of [
  ["raw standalone", rawBytes, artifactViewerBudgets.standaloneRawBytes],
  ["gzip standalone", gzipBytes, artifactViewerBudgets.standaloneGzipBytes],
  ["Brotli standalone", brotliBytes, artifactViewerBudgets.standaloneBrotliBytes],
] as const) {
  if (actual > budget) fail(`${label} is ${actual} bytes; budget is ${budget}`);
}
const sizeReport = {
  format: "rsi-artifact-viewer-size-v1",
  baseline: artifactViewerBudgets.baseline,
  budgets: artifactViewerBudgets,
  measured: {
    artifactCount: artifacts.length,
    brotliBytes,
    embeddedArtifactGzipBytes: payload.compressedBytes,
    embeddedArtifactRawBytes: payload.rawBytes,
    fullArtifacts: payload.fullArtifacts,
    gzipBytes,
    previewArtifacts: payload.previewArtifacts,
    referencedCsvBytes: artifacts.reduce((sum, artifact) => sum + artifact.sizeBytes, 0),
    standaloneRawBytes: rawBytes,
  },
  artifacts: payload.artifacts.map((artifact) => ({
    complete: artifact.complete,
    embeddedRows: artifact.rows.length,
    path: artifact.path,
    sourceRows: artifact.rowCount,
  })),
};
const sizeReportFile = path.join(root, "outputs", "quality", "artifact_viewer_size_report.json");
fs.mkdirSync(path.dirname(sizeReportFile), { recursive: true });
fs.writeFileSync(sizeReportFile, `${JSON.stringify(sizeReport, null, 2)}\n`);
const mathCount = (rendered.match(/<math\b/g) || []).length;
const tableCount = (rendered.match(/<table\b/g) || []).length;
if (mathCount < 10) fail(`Expected at least 10 MathML equations; found ${mathCount}`);
if (tableCount < 10) fail(`Expected at least 10 tables; found ${tableCount}`);
if (rendered.includes("$$")) fail("Unconverted TeX delimiter found in generated HTML");

process.stdout.write(
  `HTML: ${path.relative(root, html)} (${mathCount} MathML equations, ${tableCount} tables; ` +
    `${payload.fullArtifacts} full and ${payload.previewArtifacts} preview data payloads)\n`,
);
