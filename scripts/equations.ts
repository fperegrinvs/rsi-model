import fs from "node:fs";
import path from "node:path";

import { fragmentPaths, root } from "./manuscript-config.ts";

export const relationTypes = [
  "definition",
  "accounting identity",
  "constraint",
  "conceptual relation",
  "calibrated relation",
  "numerical substitution",
  "implemented model equation",
] as const;

export type EquationRelationType = (typeof relationTypes)[number];

export const equationLinkKinds = [
  "related equation",
  "source",
  "implementation",
  "test",
  "configuration",
  "result table",
] as const;

export type EquationLinkKind = (typeof equationLinkKinds)[number];

export interface EquationLink {
  kind: EquationLinkKind;
  label: string;
  target: string;
}

export interface NotationTerm {
  firstEquation: string;
  key: string;
  meaning: string;
  modelLayer: string;
  symbol: string;
  unitsOrDomain: string;
}

export interface EquationExplanation {
  assumptions: string[];
  id: string;
  implementationStatus: string;
  indices: string[];
  interpretation: string;
  links: EquationLink[];
  modelLayer: string;
  operators: string[];
  relationType: EquationRelationType;
  termKeys: string[];
  title: string;
}

export interface EquationMetadata {
  equations: EquationExplanation[];
  terms: Map<string, NotationTerm>;
}

const equationPattern = /^::: \{#(eq:[A-Za-z0-9_.:-]+) \.equation[^}]*\}$/gm;
const notationFile = path.join(root, "params", "notation_registry.json");
const explanationFile = path.join(root, "params", "equation_explanations.json");

function object(value: unknown, label: string): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be an object`);
  }
  return value as Record<string, unknown>;
}

function string(value: unknown, label: string): string {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`${label} must be a non-empty string`);
  }
  return value;
}

function strings(value: unknown, label: string): string[] {
  if (!Array.isArray(value) || value.some((item) => typeof item !== "string")) {
    throw new Error(`${label} must be an array of strings`);
  }
  if (value.some((item) => item.trim() === "")) {
    throw new Error(`${label} must not contain empty strings`);
  }
  return value;
}

function array(value: unknown, label: string): unknown[] {
  if (!Array.isArray(value)) throw new Error(`${label} must be an array`);
  return value;
}

function schemaVersion(value: unknown, label: string): void {
  if (value !== 1) throw new Error(`${label} schemaVersion must be 1`);
}

export function readEquationInventory(): string[] {
  const identifiers: string[] = [];
  for (const file of fragmentPaths()) {
    const markdown = fs.readFileSync(file, "utf8");
    for (const match of markdown.matchAll(equationPattern)) {
      const identifier = match[1];
      if (identifier === undefined) {
        throw new Error(`malformed equation declaration in ${path.relative(root, file)}`);
      }
      identifiers.push(identifier);
    }
  }
  const duplicates = identifiers.filter(
    (identifier, index) => identifiers.indexOf(identifier) !== index,
  );
  if (duplicates.length > 0) {
    throw new Error(`duplicate equation IDs: ${[...new Set(duplicates)].join(", ")}`);
  }
  return identifiers;
}

function readNotationTerms(equationIds: ReadonlySet<string>): Map<string, NotationTerm> {
  const document = object(JSON.parse(fs.readFileSync(notationFile, "utf8")), "notation registry");
  schemaVersion(document.schemaVersion, "notation registry");
  const terms = new Map<string, NotationTerm>();
  for (const [index, raw] of array(document.terms, "notation registry terms").entries()) {
    const record = object(raw, `notation term ${index + 1}`);
    const term: NotationTerm = {
      key: string(record.key, `notation term ${index + 1} key`),
      symbol: string(record.symbol, `notation term ${index + 1} symbol`),
      meaning: string(record.meaning, `notation term ${index + 1} meaning`),
      unitsOrDomain: string(record.unitsOrDomain, `notation term ${index + 1} unitsOrDomain`),
      firstEquation: string(record.firstEquation, `notation term ${index + 1} firstEquation`),
      modelLayer: string(record.modelLayer, `notation term ${index + 1} modelLayer`),
    };
    if (terms.has(term.key)) throw new Error(`duplicate notation term key: ${term.key}`);
    if (!equationIds.has(term.firstEquation)) {
      throw new Error(`${term.key} references unknown first equation ${term.firstEquation}`);
    }
    terms.set(term.key, term);
  }
  if (terms.size === 0) throw new Error("notation registry has no terms");
  return terms;
}

function readLinks(
  value: unknown,
  label: string,
  equationIds: ReadonlySet<string>,
): EquationLink[] {
  if (value === undefined) return [];
  const knownKinds = new Set<string>(equationLinkKinds);
  return array(value, label).map((raw, index) => {
    const record = object(raw, `${label} ${index + 1}`);
    const kind = string(record.kind, `${label} ${index + 1} kind`);
    const target = string(record.target, `${label} ${index + 1} target`);
    if (!knownKinds.has(kind)) throw new Error(`${label} ${index + 1} has unknown kind ${kind}`);
    if (kind === "related equation") {
      if (!equationIds.has(target)) {
        throw new Error(`${label} ${index + 1} references unknown equation ${target}`);
      }
    } else if (/^https:\/\//.test(target)) {
      new URL(target);
    } else {
      const resolved = path.resolve(root, target);
      if (!resolved.startsWith(`${root}${path.sep}`) || !fs.existsSync(resolved)) {
        throw new Error(`${label} ${index + 1} has unsafe or missing target ${target}`);
      }
      if (!fs.statSync(resolved).isFile() || !fs.realpathSync(resolved).startsWith(root)) {
        throw new Error(`${label} ${index + 1} target is not a contained file ${target}`);
      }
    }
    return {
      kind: kind as EquationLinkKind,
      label: string(record.label, `${label} ${index + 1} label`),
      target,
    };
  });
}

function readExplanations(inventory: readonly string[]): EquationExplanation[] {
  const document = object(
    JSON.parse(fs.readFileSync(explanationFile, "utf8")),
    "equation explanation registry",
  );
  schemaVersion(document.schemaVersion, "equation explanation registry");
  const equations: EquationExplanation[] = [];
  const knownTypes = new Set<string>(relationTypes);
  const equationIds = new Set(inventory);
  for (const [index, raw] of array(document.equations, "equation explanations").entries()) {
    const record = object(raw, `equation explanation ${index + 1}`);
    const relationType = string(
      record.relationType,
      `equation explanation ${index + 1} relationType`,
    );
    if (!knownTypes.has(relationType)) {
      throw new Error(
        `unknown relation type for equation explanation ${index + 1}: ${relationType}`,
      );
    }
    equations.push({
      id: string(record.id, `equation explanation ${index + 1} id`),
      title: string(record.title, `equation explanation ${index + 1} title`),
      interpretation: string(
        record.interpretation,
        `equation explanation ${index + 1} interpretation`,
      ),
      links: readLinks(record.links, `equation explanation ${index + 1} links`, equationIds),
      termKeys: strings(record.termKeys, `equation explanation ${index + 1} termKeys`),
      indices: strings(record.indices, `equation explanation ${index + 1} indices`),
      operators: strings(record.operators, `equation explanation ${index + 1} operators`),
      assumptions: strings(record.assumptions, `equation explanation ${index + 1} assumptions`),
      relationType: relationType as EquationRelationType,
      modelLayer: string(record.modelLayer, `equation explanation ${index + 1} modelLayer`),
      implementationStatus: string(
        record.implementationStatus,
        `equation explanation ${index + 1} implementationStatus`,
      ),
    });
  }
  const explanationIds = equations.map(({ id }) => id);
  const duplicates = explanationIds.filter(
    (identifier, index) => explanationIds.indexOf(identifier) !== index,
  );
  if (duplicates.length > 0) {
    throw new Error(`duplicate equation explanations: ${[...new Set(duplicates)].join(", ")}`);
  }
  const missing = inventory.filter((identifier) => !explanationIds.includes(identifier));
  const stale = explanationIds.filter((identifier) => !inventory.includes(identifier));
  if (missing.length > 0 || stale.length > 0) {
    throw new Error(
      [
        missing.length > 0 ? `missing explanations: ${missing.join(", ")}` : "",
        stale.length > 0 ? `stale explanations: ${stale.join(", ")}` : "",
      ]
        .filter(Boolean)
        .join("; "),
    );
  }
  if (inventory.some((identifier, index) => explanationIds[index] !== identifier)) {
    throw new Error("equation explanation order must match the manuscript equation order");
  }
  return equations;
}

export function readEquationMetadata(): EquationMetadata {
  const inventory = readEquationInventory();
  const equationIds = new Set(inventory);
  const terms = readNotationTerms(equationIds);
  const equations = readExplanations(inventory);
  for (const equation of equations) {
    if (equation.termKeys.length === 0) {
      throw new Error(`${equation.id} must declare at least one notation term`);
    }
    const duplicateTerms = equation.termKeys.filter(
      (key, index) => equation.termKeys.indexOf(key) !== index,
    );
    if (duplicateTerms.length > 0) {
      throw new Error(
        `${equation.id} repeats term keys: ${[...new Set(duplicateTerms)].join(", ")}`,
      );
    }
    const unknownTerms = equation.termKeys.filter((key) => !terms.has(key));
    if (unknownTerms.length > 0) {
      throw new Error(`${equation.id} has unknown term keys: ${unknownTerms.join(", ")}`);
    }
  }
  return { equations, terms };
}

function markdownList(items: readonly string[]): string {
  return items.length > 0 ? items.map((item) => `- ${item}`).join("\n") : "- None.";
}

function markdownLink(link: EquationLink): string {
  const target = link.kind === "related equation" ? `equation:${link.target}` : link.target;
  const href = /^https:\/\//.test(target)
    ? target
    : target.startsWith("equation:")
      ? target
      : `https://github.com/fperegrinvs/rsi-model/blob/main/${target}`;
  return `- **${link.kind}:** [${link.label}](${href})`;
}

export function renderEquationExplanationMarkdown(
  equation: EquationExplanation,
  terms: ReadonlyMap<string, NotationTerm>,
): string {
  const termDefinitions = equation.termKeys
    .map((key) => {
      const term = terms.get(key);
      if (term === undefined) throw new Error(`${equation.id} references unknown term ${key}`);
      return `${term.symbol}\n: ${term.meaning}. **Units/domain:** ${term.unitsOrDomain}.`;
    })
    .join("\n\n");
  return [
    "::: {.equation-explanation-body}",
    `<p class="equation-explanation-title"><strong>${equation.title}</strong></p>`,
    equation.interpretation,
    "",
    "**Terms**",
    "",
    termDefinitions,
    "",
    "**Indices and local domains**",
    "",
    markdownList(equation.indices),
    "",
    "**Operators**",
    "",
    markdownList(equation.operators),
    "",
    "**Validity and assumptions**",
    "",
    markdownList(equation.assumptions),
    "",
    ...(equation.links.length > 0
      ? ["**Related resources**", "", equation.links.map(markdownLink).join("\n"), ""]
      : []),
    `<p class="equation-explanation-classification"><strong>Relation:</strong> ${equation.relationType}. <strong>Model layer:</strong> ${equation.modelLayer}. <strong>Implementation:</strong> ${equation.implementationStatus}</p>`,
    "",
    "[Canonical definitions and scoped units](notation:register).",
    ":::",
    "",
  ].join("\n");
}

export function writeEquationExplanationMap(directory: string): string {
  const metadata = readEquationMetadata();
  const snippets = path.join(directory, "equation-explanations");
  fs.mkdirSync(snippets, { recursive: true });
  const rows: string[] = [];
  for (const equation of metadata.equations) {
    const slug = equation.id.replace(/^eq:/, "").replace(/[^A-Za-z0-9_-]/g, "-");
    const file = path.join(snippets, `${slug}.md`);
    fs.writeFileSync(file, renderEquationExplanationMarkdown(equation, metadata.terms));
    rows.push([equation.id, file].join("\t"));
  }
  const map = path.join(directory, "equation-explanations.tsv");
  fs.writeFileSync(map, `${rows.join("\n")}\n`);
  return map;
}
