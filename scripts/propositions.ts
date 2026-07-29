import fs from "node:fs";
import path from "node:path";

import { fragmentPaths, root } from "./manuscript-config.ts";

export interface Proposition {
  anchor: string;
  canonicalWording: string;
  currentStatus: string;
  id: string;
  shortTitle: string;
}

export interface PropositionReference {
  file: string;
  id: string;
  label: string;
}

const registryFile = path.join(root, "params", "propositions.json");
const definitionFile = path.join(root, "docs", "manuscript", "00-front-matter.md");
const glossaryFile = path.join(root, "docs", "manuscript", "60-glossary.md");
const propositionIdPattern = /^P(?:1|2|3a|3b|4a|4b)$/;
const referencePattern = /\[([^\]]+)\]\(proposition:(P(?:1|2|3a|3b|4a|4b))\)\{([^}]*)\}/g;

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

function array(value: unknown, label: string): unknown[] {
  if (!Array.isArray(value)) throw new Error(`${label} must be an array`);
  return value;
}

export function propositionLabel(proposition: Proposition): string {
  return `${proposition.id} — ${proposition.shortTitle}`;
}

export function propositionReference(proposition: Proposition): string {
  return `[${propositionLabel(proposition)}](proposition:${proposition.id}){.proposition-ref}`;
}

export function readPropositionRegistry(): Proposition[] {
  const document = object(
    JSON.parse(fs.readFileSync(registryFile, "utf8")),
    "proposition registry",
  );
  if (document.schemaVersion !== 1) {
    throw new Error("proposition registry schemaVersion must be 1");
  }
  const propositions = array(document.propositions, "propositions").map((raw, index) => {
    const record = object(raw, `proposition ${index + 1}`);
    const proposition: Proposition = {
      id: string(record.id, `proposition ${index + 1} id`),
      shortTitle: string(record.shortTitle, `proposition ${index + 1} shortTitle`),
      canonicalWording: string(
        record.canonicalWording,
        `proposition ${index + 1} canonicalWording`,
      ),
      currentStatus: string(record.currentStatus, `proposition ${index + 1} currentStatus`),
      anchor: string(record.anchor, `proposition ${index + 1} anchor`),
    };
    if (!propositionIdPattern.test(proposition.id)) {
      throw new Error(`unknown proposition identifier ${proposition.id}`);
    }
    if (proposition.anchor !== `proposition-${proposition.id.toLowerCase()}`) {
      throw new Error(`${proposition.id} has noncanonical anchor ${proposition.anchor}`);
    }
    return proposition;
  });
  const exactIds = ["P1", "P2", "P3a", "P3b", "P4a", "P4b"];
  if (
    propositions.length !== exactIds.length ||
    propositions.some(({ id }, index) => id !== exactIds[index])
  ) {
    throw new Error(`proposition registry must contain ${exactIds.join(", ")} in order`);
  }
  for (const field of ["id", "shortTitle", "anchor"] as const) {
    const values = propositions.map((proposition) => proposition[field]);
    if (new Set(values).size !== values.length) {
      throw new Error(`duplicate proposition ${field}`);
    }
  }
  return propositions;
}

export function renderPropositionRegister(propositions: readonly Proposition[]): string {
  const rows = propositions.map(
    (proposition) => `| ${propositionReference(proposition)} | ${proposition.currentStatus} |`,
  );
  return [
    "<!-- proposition-register:start -->",
    "| proposition | current evidential status |",
    "|---|---|",
    ...rows,
    "",
    ": Canonical proposition definitions and current evidential status. {#tbl-g-proposition-register}",
    "",
    "<!-- proposition-register:end -->",
  ].join("\n");
}

export function readPropositionReferences(): PropositionReference[] {
  const references: PropositionReference[] = [];
  for (const file of fragmentPaths()) {
    const markdown = fs.readFileSync(file, "utf8");
    for (const match of markdown.matchAll(referencePattern)) {
      const label = match[1];
      const id = match[2];
      const attributes = match[3];
      if (label === undefined || id === undefined || attributes === undefined) continue;
      if (!/(?:^|\s)\.proposition-ref(?:\s|$)/.test(attributes)) {
        throw new Error(`${path.relative(root, file)} ${id} reference lacks .proposition-ref`);
      }
      references.push({ file: path.relative(root, file), id, label });
    }
  }
  return references;
}

export function validatePropositionSystem(): {
  propositions: Proposition[];
  references: PropositionReference[];
} {
  const propositions = readPropositionRegistry();
  const byId = new Map(propositions.map((proposition) => [proposition.id, proposition]));
  const definitions = fs.readFileSync(definitionFile, "utf8");
  const ladder = definitions.match(/::: \{\.proposition-ladder\}\n(?<body>[\s\S]*?)\n:::\n/)?.groups
    ?.body;
  if (ladder === undefined) throw new Error("front matter has no proposition ladder block");
  for (const proposition of propositions) {
    const heading =
      `### ${propositionLabel(proposition)} ` + `{#${proposition.anchor} .proposition-definition}`;
    if ([...definitions.matchAll(new RegExp(`^${escapePattern(heading)}$`, "gm"))].length !== 1) {
      throw new Error(`${proposition.id} must have exactly one canonical heading`);
    }
    const canonical = `**Canonical claim:** ${proposition.canonicalWording}`;
    const status = `**Current status:** ${proposition.currentStatus}`;
    if (!ladder.includes(canonical) || !ladder.includes(status)) {
      throw new Error(`${proposition.id} canonical wording or status differs from registry`);
    }
  }
  const glossary = fs.readFileSync(glossaryFile, "utf8");
  const expectedRegister = renderPropositionRegister(propositions);
  if (!glossary.includes(expectedRegister)) {
    throw new Error("glossary proposition register differs from registry");
  }

  const references = readPropositionReferences();
  for (const reference of references) {
    const proposition = byId.get(reference.id);
    if (proposition === undefined) {
      throw new Error(`${reference.file} references undefined proposition ${reference.id}`);
    }
    if (reference.label !== propositionLabel(proposition)) {
      throw new Error(
        `${reference.file} ${reference.id} accessible label must be ` +
          `"${propositionLabel(proposition)}"`,
      );
    }
  }
  const referenceIds = new Set(references.map(({ id }) => id));
  for (const proposition of propositions) {
    if (!referenceIds.has(proposition.id)) {
      throw new Error(`stale proposition ${proposition.id} has no manuscript reference`);
    }
  }

  for (const file of fragmentPaths()) {
    let markdown = fs.readFileSync(file, "utf8");
    markdown = markdown.replace(/::: \{\.proposition-ladder\}\n[\s\S]*?\n:::\n/, "");
    markdown = markdown.replace(referencePattern, "");
    markdown = markdown.replace(/`[^`\n]*`/g, "");
    const bare = [...markdown.matchAll(/\bP(?:1|2|3a|3b|4a|4b)\b/g)];
    if (bare.length > 0) {
      throw new Error(
        `${path.relative(root, file)} contains bare proposition labels: ` +
          `${[...new Set(bare.map((match) => match[0]))].join(", ")}`,
      );
    }
  }
  return { propositions, references };
}

export function writePropositionMap(directory: string): string {
  const { propositions } = validatePropositionSystem();
  const file = path.join(directory, "propositions.tsv");
  fs.writeFileSync(
    file,
    `${propositions
      .map((proposition) =>
        [
          proposition.id,
          proposition.shortTitle,
          proposition.anchor,
          proposition.currentStatus,
          "index.html",
        ].join("\t"),
      )
      .join("\n")}\n`,
  );
  return file;
}

function escapePattern(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
