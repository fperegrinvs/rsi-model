import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { gzipSync } from "node:zlib";

import { parse } from "csv-parse/sync";

import { fragmentPaths, root } from "./manuscript-config.ts";

export interface ArtifactRegistryEntry {
  class?: string;
  columns?: Record<string, { description?: string; label?: string; units?: string }>;
  defaultSort?: { column: string; direction: "asc" | "desc" };
  description?: string;
  keyColumns?: string[];
  title?: string;
}

export interface ArtifactReference {
  label: string;
  path: string;
}

export interface ArtifactData {
  columns: Array<{
    description?: string;
    key: boolean;
    label: string;
    name: string;
    units?: string;
  }>;
  complete: boolean;
  defaultSort?: { column: string; direction: "asc" | "desc" };
  description: string;
  freshness: string;
  hash: string;
  key: string;
  path: string;
  rowCount: number;
  rows: string[][];
  sizeBytes: number;
  sourceClass: string;
  sourceManifest: string;
  title: string;
}

export interface ArtifactReferenceUrls {
  download: string;
  fullPage: string;
  metadata?: string;
}

export interface StandaloneArtifactPayload {
  artifacts: ArtifactData[];
  compressedBase64: string;
  compressedBytes: number;
  fullArtifacts: number;
  previewArtifacts: number;
  rawBytes: number;
}

export const artifactViewerBudgets = {
  baseline: {
    description:
      "Measured immediately before the shared viewer; the older TODO estimate was 2.8 MiB HTML and 2.55 MiB of referenced CSVs.",
    referencedCsvBytes: 2_997_241,
    standaloneBytes: 3_141_572,
  },
  embeddedArtifactRawBytes: 1_310_720,
  embeddedArtifactGzipBytes: 262_144,
  fullArtifactRawBytes: 65_536,
  previewRows: 50,
  standaloneBrotliBytes: 2_202_010,
  standaloneGzipBytes: 2_359_296,
  standaloneRawBytes: 4_718_592,
  startupMilliseconds: 2_500,
  firstViewMilliseconds: 2_500,
} as const;

const artifactPattern =
  /\[([^\]\n]+)\]\(\.\.\/(outputs\/[^)\n]+\.csv)\)\{\.artifact-link data-artifact="(outputs\/[^"\n]+\.csv)"\}/g;
const registryFile = path.join(root, "params", "artifact_registry.json");

function readRegistry(): Record<string, ArtifactRegistryEntry> {
  const parsed: unknown = JSON.parse(fs.readFileSync(registryFile, "utf8"));
  if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error("artifact registry must be a JSON object");
  }
  return parsed as Record<string, ArtifactRegistryEntry>;
}

export function artifactKey(artifactPath: string): string {
  return artifactPath
    .replace(/\.csv$/i, "")
    .replace(/[^A-Za-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export function assertArtifactPath(artifactPath: string): string {
  if (
    !artifactPath.startsWith("outputs/") ||
    !artifactPath.endsWith(".csv") ||
    artifactPath.includes("\\") ||
    path.posix.normalize(artifactPath) !== artifactPath ||
    artifactPath.split("/").includes("..")
  ) {
    throw new Error(`unsafe artifact path: ${artifactPath}`);
  }
  const outputsRoot = path.join(root, "outputs");
  const source = path.resolve(root, artifactPath);
  if (!source.startsWith(`${outputsRoot}${path.sep}`)) {
    throw new Error(`artifact escapes outputs/: ${artifactPath}`);
  }
  if (!fs.existsSync(source) || !fs.statSync(source).isFile()) {
    throw new Error(`missing artifact: ${artifactPath}`);
  }
  if (fs.lstatSync(source).isSymbolicLink()) {
    throw new Error(`artifact must not be a symbolic link: ${artifactPath}`);
  }
  const real = fs.realpathSync(source);
  const realOutputs = fs.realpathSync(outputsRoot);
  if (!real.startsWith(`${realOutputs}${path.sep}`)) {
    throw new Error(`artifact symlink escapes outputs/: ${artifactPath}`);
  }
  return source;
}

export function parseCsvText(
  text: string,
  artifactPath = "artifact.csv",
): {
  headers: string[];
  rows: string[][];
} {
  const records = parse(text, {
    bom: true,
    columns: false,
    relax_column_count: false,
    skip_empty_lines: false,
  }) as string[][];
  const headers = records[0];
  if (headers === undefined || headers.length === 0 || headers.every((header) => header === "")) {
    throw new Error(`${artifactPath} has no header row`);
  }
  if (headers.some((header) => header.trim() === "")) {
    throw new Error(`${artifactPath} has an empty header`);
  }
  const duplicates = headers.filter((header, index) => headers.indexOf(header) !== index);
  if (duplicates.length > 0) {
    throw new Error(
      `${artifactPath} has duplicate headers: ${[...new Set(duplicates)].join(", ")}`,
    );
  }
  const rows = records.slice(1);
  for (const [index, row] of rows.entries()) {
    if (row.length !== headers.length) {
      throw new Error(
        `${artifactPath} row ${index + 2} has ${row.length} cells; expected ${headers.length}`,
      );
    }
  }
  return { headers, rows };
}

export function readArtifactReferences(): ArtifactReference[] {
  const references: ArtifactReference[] = [];
  for (const file of fragmentPaths()) {
    const markdown = fs.readFileSync(file, "utf8");
    for (const match of markdown.matchAll(artifactPattern)) {
      const label = match[1]?.trim();
      const hrefPath = match[2];
      const metadataPath = match[3];
      if (!label || hrefPath === undefined || metadataPath === undefined) {
        throw new Error(`malformed artifact reference in ${path.relative(root, file)}`);
      }
      if (hrefPath !== metadataPath) {
        throw new Error(`artifact href and metadata path differ in ${path.relative(root, file)}`);
      }
      assertArtifactPath(hrefPath);
      references.push({ label, path: hrefPath });
    }
    const residue = markdown.match(/`(?:outputs\/[^`\n]+\/)?[A-Za-z0-9_.-]+\.csv`/);
    if (residue !== null) {
      throw new Error(
        `${path.relative(root, file)} retains a raw reader-facing CSV reference: ${residue[0]}`,
      );
    }
  }
  return references;
}

function manifestEntries(file: string): Map<string, string> {
  const markdown = fs.readFileSync(file, "utf8");
  return new Map(
    [
      ...markdown.matchAll(/\| `?(?<path>outputs\/[^`|\s]+)`? \| `?(?<hash>[0-9a-f]{64})`? \|/g),
    ].map((match) => [match.groups?.path ?? "", match.groups?.hash ?? ""]),
  );
}

function manifestFreshness(file: string): string {
  const markdown = fs.readFileSync(file, "utf8");
  const generated = markdown.match(/^- generated:\s*(.+)$/m)?.[1]?.trim();
  return generated === undefined
    ? `SHA-256 verified in ${path.relative(root, file)}`
    : `${generated} manifest build`;
}

export function buildArtifactData(): ArtifactData[] {
  const references = readArtifactReferences();
  const registry = readRegistry();
  const releaseManifest = manifestEntries(path.join(root, "outputs", "MANIFEST.md"));
  const integratedManifest = manifestEntries(
    path.join(root, "outputs", "integrated", "MANIFEST.md"),
  );
  const releaseFreshness = manifestFreshness(path.join(root, "outputs", "MANIFEST.md"));
  const integratedFreshness = manifestFreshness(
    path.join(root, "outputs", "integrated", "MANIFEST.md"),
  );
  const labels = new Map<string, string>();
  for (const reference of references) {
    const existing = labels.get(reference.path);
    if (existing === undefined || reference.label.length < existing.length) {
      labels.set(reference.path, reference.label);
    }
  }
  const artifacts: ArtifactData[] = [];
  for (const [artifactPath, sourceLabel] of [...labels].sort(([left], [right]) =>
    left.localeCompare(right),
  )) {
    const source = assertArtifactPath(artifactPath);
    const bytes = fs.readFileSync(source);
    const text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    const { headers, rows } = parseCsvText(text, artifactPath);
    const hash = createHash("sha256").update(bytes).digest("hex");
    const sourceManifest = artifactPath.startsWith("outputs/integrated/")
      ? "outputs/integrated/MANIFEST.md"
      : "outputs/MANIFEST.md";
    const expectedHash = (
      artifactPath.startsWith("outputs/integrated/") ? integratedManifest : releaseManifest
    ).get(artifactPath);
    if (expectedHash === undefined) {
      throw new Error(`${artifactPath} is absent from ${sourceManifest}`);
    }
    if (expectedHash !== hash) {
      throw new Error(`${artifactPath} hash differs from ${sourceManifest}`);
    }
    const configured = registry[artifactPath] ?? {};
    const keyColumns = new Set(configured.keyColumns ?? []);
    const columns = headers.map((name) => ({
      name,
      label: configured.columns?.[name]?.label ?? name.replaceAll("_", " "),
      ...(configured.columns?.[name]?.description === undefined
        ? {}
        : { description: configured.columns[name]?.description }),
      ...(configured.columns?.[name]?.units === undefined
        ? {}
        : { units: configured.columns[name]?.units }),
      key: keyColumns.has(name),
    }));
    artifacts.push({
      key: artifactKey(artifactPath),
      path: artifactPath,
      title: configured.title ?? sourceLabel,
      description: configured.description ?? "Machine-readable output referenced by the article.",
      sourceClass:
        configured.class ??
        (artifactPath.startsWith("outputs/integrated/")
          ? "integrated_model_output"
          : "model_output"),
      hash,
      sizeBytes: bytes.byteLength,
      rowCount: rows.length,
      complete: true,
      columns,
      rows,
      ...(configured.defaultSort === undefined ? {} : { defaultSort: configured.defaultSort }),
      sourceManifest,
      freshness: artifactPath.startsWith("outputs/integrated/")
        ? integratedFreshness
        : releaseFreshness,
    });
  }
  const referenced = new Set(artifacts.map(({ path: artifactPath }) => artifactPath));
  const staleRegistryEntries = Object.keys(registry).filter(
    (artifactPath) => !referenced.has(artifactPath),
  );
  if (staleRegistryEntries.length > 0) {
    throw new Error(`stale artifact registry entries: ${staleRegistryEntries.join(", ")}`);
  }
  return artifacts;
}

function serializedBytes(value: unknown): number {
  return Buffer.byteLength(JSON.stringify(value));
}

export function buildStandaloneArtifactPayload(
  artifacts: readonly ArtifactData[],
): StandaloneArtifactPayload {
  const embedded = artifacts.map((artifact) => ({
    ...artifact,
    complete: artifact.rows.length <= artifactViewerBudgets.previewRows,
    rows: artifact.rows.slice(0, artifactViewerBudgets.previewRows),
  }));
  let rawBytes = serializedBytes({
    format: "rsi-artifact-viewer-v1",
    artifacts: embedded,
  });
  for (const [index, artifact] of artifacts.entries()) {
    if (artifact.rows.length <= artifactViewerBudgets.previewRows) continue;
    const fullCandidate = { ...artifact, complete: true };
    if (serializedBytes(fullCandidate) > artifactViewerBudgets.fullArtifactRawBytes) continue;
    const previous = embedded[index];
    if (previous === undefined) throw new Error(`missing embedded artifact at index ${index}`);
    embedded[index] = fullCandidate;
    const candidateBytes = serializedBytes({
      format: "rsi-artifact-viewer-v1",
      artifacts: embedded,
    });
    if (candidateBytes > artifactViewerBudgets.embeddedArtifactRawBytes) {
      embedded[index] = previous;
      continue;
    }
    rawBytes = candidateBytes;
  }
  const payload = {
    format: "rsi-artifact-viewer-v1" as const,
    artifacts: embedded,
  };
  const json = JSON.stringify(payload);
  rawBytes = Buffer.byteLength(json);
  const compressed = gzipSync(json, { level: 9 });
  if (rawBytes > artifactViewerBudgets.embeddedArtifactRawBytes) {
    throw new Error(
      `standalone artifact payload is ${rawBytes} bytes; budget is ` +
        `${artifactViewerBudgets.embeddedArtifactRawBytes}`,
    );
  }
  if (compressed.byteLength > artifactViewerBudgets.embeddedArtifactGzipBytes) {
    throw new Error(
      `compressed standalone artifact payload is ${compressed.byteLength} bytes; budget is ` +
        `${artifactViewerBudgets.embeddedArtifactGzipBytes}`,
    );
  }
  const fullArtifacts = embedded.filter((artifact) => artifact.complete).length;
  return {
    artifacts: embedded,
    compressedBase64: compressed.toString("base64"),
    compressedBytes: compressed.byteLength,
    fullArtifacts,
    previewArtifacts: embedded.length - fullArtifacts,
    rawBytes,
  };
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  return `${Math.ceil(bytes / 1024).toLocaleString("en-US")} KB`;
}

export function renderArtifactReference(
  artifact: ArtifactData,
  labelHtml: string,
  urls: ArtifactReferenceUrls,
): string {
  const size = formatBytes(artifact.sizeBytes);
  const downloadLabel = `Download ${artifact.title} (CSV, ${size})`;
  const metadata =
    urls.metadata === undefined ? "" : ` data-artifact-json="${escapeHtml(urls.metadata)}"`;
  return (
    `<span class="artifact-reference" data-artifact-reference="${escapeHtml(artifact.path)}">` +
    `<button type="button" class="artifact-view-button" data-artifact-view ` +
    `data-artifact="${escapeHtml(artifact.path)}" data-artifact-key="${artifact.key}" ` +
    `data-artifact-hash="${artifact.hash}" ` +
    `data-artifact-download="${escapeHtml(urls.download)}" ` +
    `data-artifact-download-label="${escapeHtml(downloadLabel)}" ` +
    `data-artifact-full-page="${escapeHtml(urls.fullPage)}"${metadata}>` +
    `View data: ${labelHtml}</button>` +
    `<a href="${escapeHtml(urls.download)}" class="artifact-download-link" download ` +
    `aria-label="${escapeHtml(downloadLabel)}" title="${escapeHtml(downloadLabel)}">` +
    `Download original CSV <span class="artifact-file-size">(${escapeHtml(size)})</span></a>` +
    "</span>"
  );
}

export function decorateArtifactReferences(
  html: string,
  artifacts: readonly ArtifactData[],
  urls: (artifact: ArtifactData, originalHref: string) => ArtifactReferenceUrls,
): string {
  const byPath = new Map(artifacts.map((artifact) => [artifact.path, artifact]));
  const authored = html.replace(
    /<a\b(?<attributes>[^>]*\bdata-artifact="(?<path>outputs\/[^"]+\.csv)"[^>]*)>(?<label>[\s\S]*?)<\/a>/g,
    (
      whole: string,
      _attributes: string,
      _artifactPath: string,
      _label: string,
      _offset: number,
      _input: string,
      groups: { attributes?: string; label?: string; path?: string } | undefined,
    ) => {
      const artifactPath = groups?.path;
      const label = groups?.label;
      if (artifactPath === undefined || label === undefined) return whole;
      const artifact = byPath.get(artifactPath);
      if (artifact === undefined) throw new Error(`unknown rendered artifact ${artifactPath}`);
      const attributes = groups?.attributes ?? "";
      const originalHref = attributes.match(/\bhref="([^"]+)"/)?.[1];
      if (originalHref === undefined) {
        throw new Error(`rendered artifact link has no href: ${artifactPath}`);
      }
      return renderArtifactReference(artifact, label, urls(artifact, originalHref));
    },
  );
  return authored.replace(
    /<a\b[^>]*href="(?<href>https:\/\/github\.com\/fperegrinvs\/rsi-model\/blob\/main\/(?<path>outputs\/[^"]+\.csv))"[^>]*>(?<label>[\s\S]*?)<\/a>/g,
    (
      whole: string,
      _href: string,
      _artifactPath: string,
      _label: string,
      _offset: number,
      _input: string,
      groups: { href?: string; label?: string; path?: string } | undefined,
    ) => {
      const artifactPath = groups?.path;
      const label = groups?.label;
      const originalHref = groups?.href;
      if (artifactPath === undefined || label === undefined || originalHref === undefined) {
        return whole;
      }
      const artifact = byPath.get(artifactPath);
      if (artifact === undefined) throw new Error(`unknown rendered artifact ${artifactPath}`);
      return renderArtifactReference(artifact, label, urls(artifact, originalHref));
    },
  );
}
