import fs from "node:fs";
import path from "node:path";

import { parseCsvText } from "./artifacts.ts";
import { root } from "./manuscript-config.ts";

const registryPath = path.join(root, "params", "orbital_ai_scenario_registry.json");
const sourcePath = path.join(root, "docs", "manuscript", "70-sources.md");

const scenarioOrder = [
  "generic_reference",
  "independent_reference",
  "spacexai_disclosed_design",
  "spacexai_stated_aspiration",
  "spacexai_affiliate_hybrid",
] as const;
const programOrder = [
  "spacexai_bounded_ecosystem",
  "google_planet_suncatcher",
  "starcloud",
  "blue_origin_sunrise",
] as const;
const layerOrder = [
  "launch_transport",
  "spacecraft_manufacturing",
  "power_generation",
  "storage_grid_control",
  "communications",
  "ai_compute",
  "models_data",
  "chip_design",
  "chip_fabrication_packaging",
  "robotics",
  "construction",
  "mining",
  "beneficiation",
  "refining",
  "bulk_material_production",
  "maintenance_repair",
  "recycling",
  "capital_equipment_reproduction",
] as const;
const simulationOrder = [
  "orbital_compute_lifecycle_cost",
  "launch_mass_cadence",
  "vehicle_power_thermal",
  "hardware_life_qualification",
  "communications",
  "deployment_growth",
  "constellation_topology",
  "debris_exposure",
  "repair_replacement",
  "physical_closure_supply",
] as const;
const allowedStatuses = new Set([
  "included",
  "axis_marker",
  "hybrid_completion",
  "not_parameterizable",
]);

interface RegistryScenario {
  actorBoundary: string;
  boundary: string;
  evidenceClass: string;
  maturityState: string;
  parameterCompleteness: number;
  scenarioId: string;
  sourceSnapshot: string;
}

interface RegistryInput {
  anchorKey: string;
  denominator: string;
  evidenceClass: string;
  high: number | null;
  low: number | null;
  maturityState: string;
  scenarioId: string;
  sourceDate: string;
  sourceSnapshot: string;
  unit: string;
  value: number | null;
}

interface RegistryProgram {
  boundary: string;
  programId: string;
}

interface RegistrySimulation {
  aspirationBoundary: string;
  aspirationStatus: string;
  disclosedBoundary: string;
  disclosedStatus: string;
  genericBoundary: string;
  genericStatus: string;
  hybridBoundary: string;
  hybridStatus: string;
  independentBoundary: string;
  independentStatus: string;
  outputPaths: string[];
  simulationId: string;
}

interface RegistryLayer {
  layerId: string;
}

interface RegistryCapability {
  layerId: string;
  maturityLevel: string;
  offWorldReproductivelyClosed: boolean;
  programId: string;
  responsibleLegalEntity: string;
  underCommonControl: boolean;
}

interface Registry {
  asOf: string;
  capabilities: RegistryCapability[];
  closureLayers: RegistryLayer[];
  comparisonClass: string;
  inputs: RegistryInput[];
  landscapeSnapshot: string;
  programs: RegistryProgram[];
  registryVersion: string;
  releaseRefreshProtocol: string;
  scenarioOrder: string[];
  scenarios: RegistryScenario[];
  simulationCoverage: RegistrySimulation[];
}

export interface ScenarioPolicyStats {
  capabilities: number;
  closureRows: number;
  inputs: number;
  manuscriptFiles: number;
  resultRows: number;
  simulationOutputRows: number;
}

function object(value: unknown, label: string): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be an object`);
  }
  return value as Record<string, unknown>;
}

function readRegistry(): Registry {
  const parsed: unknown = JSON.parse(fs.readFileSync(registryPath, "utf8"));
  const candidate = object(parsed, "scenario registry");
  for (const field of [
    "scenarios",
    "inputs",
    "programs",
    "simulationCoverage",
    "closureLayers",
    "capabilities",
  ]) {
    if (!Array.isArray(candidate[field])) {
      throw new Error(`scenario registry ${field} must be an array`);
    }
  }
  return candidate as unknown as Registry;
}

function sameOrder(actual: string[], expected: readonly string[], label: string): void {
  if (
    actual.length !== expected.length ||
    actual.some((value, index) => value !== expected[index])
  ) {
    throw new Error(`${label} does not match the canonical order`);
  }
}

function csvRows(relativePath: string): Array<Record<string, string>> {
  const absolute = path.join(root, relativePath);
  if (!fs.existsSync(absolute)) {
    throw new Error(`missing generated scenario-policy artifact: ${relativePath}`);
  }
  const { headers, rows } = parseCsvText(fs.readFileSync(absolute, "utf8"), relativePath);
  return rows.map((row) =>
    Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ""])),
  );
}

function requireColumns(
  rows: Array<Record<string, string>>,
  columns: readonly string[],
  label: string,
): void {
  if (rows.length === 0) {
    throw new Error(`${label} has no data rows`);
  }
  for (const [index, row] of rows.entries()) {
    for (const column of columns) {
      if ((row[column] ?? "") === "") {
        throw new Error(`${label} row ${index + 2} has no ${column}`);
      }
    }
  }
}

function manuscriptFragments(): string[] {
  const directory = path.join(root, "docs", "manuscript");
  return fs
    .readdirSync(directory)
    .filter((name) => /^(?:00|10|11|12|20|30|40)-.*\.md$/.test(name))
    .map((name) => path.join(directory, name))
    .sort();
}

function checkLanguage(files: string[]): void {
  const prohibited = [
    {
      label: "exclusive orbital-AI actor claim",
      pattern:
        /\bonly (?:company|firm|actor|organization)[^.\n]{0,140}(?:off[- ]planet|orbital)[^.\n]{0,80}\bAI\b/giu,
    },
    {
      label: "affiliate ownership conflation",
      pattern:
        /\b(?:Tesla|The Boring Company)[^.\n]{0,100}\b(?:part of|owned by|controlled by)\s+SpaceXAI\b/giu,
    },
    {
      label: "filing treated as authorization",
      pattern: /\b(?:FCC|application|filing)\s+(?:authorized|approved|deployed)\b/giu,
    },
    {
      label: "affiliate capability conflation",
      pattern: /\b(?:Tesla|affiliate) capabilities? (?:are|is) SpaceXAI capabilities?\b/giu,
    },
  ];
  for (const file of files) {
    const text = fs.readFileSync(file, "utf8");
    for (const { label, pattern } of prohibited) {
      const match = pattern.exec(text);
      pattern.lastIndex = 0;
      if (match !== null) {
        const line = text.slice(0, match.index).split("\n").length;
        throw new Error(`${path.relative(root, file)}:${line}: ${label}: ${match[0]}`);
      }
    }
    for (const paragraph of text.split(/\n\s*\n/)) {
      if (
        /\bSpaceXAI\b/u.test(paragraph) &&
        /\b(?:broadest|unique|full stack|self-sustaining|closed loop)\b/iu.test(paragraph)
      ) {
        if (!/\bas of (?:[A-Z][a-z]+ \d{1,2}, \d{4}|\d{4}-\d{2}-\d{2})\b/iu.test(paragraph)) {
          throw new Error(
            `${path.relative(root, file)}: SpaceXAI breadth/closure claim lacks an as-of date`,
          );
        }
        if (!/\bcomparison class\b/iu.test(paragraph)) {
          throw new Error(
            `${path.relative(root, file)}: SpaceXAI breadth/closure claim lacks a comparison class`,
          );
        }
        if (!/\b(?:not a claim|missing|gap|unresolved|zero)\b/iu.test(paragraph)) {
          throw new Error(
            `${path.relative(root, file)}: SpaceXAI breadth/closure claim lacks open dependencies`,
          );
        }
      }
    }
  }
}

export function validateScenarioPolicy(): ScenarioPolicyStats {
  const registry = readRegistry();
  if (registry.registryVersion !== registry.asOf) {
    throw new Error("registry version and as-of date differ");
  }
  if (
    registry.comparisonClass.trim() === "" ||
    !registry.releaseRefreshProtocol.includes("every release")
  ) {
    throw new Error("registry lacks a comparison class or release refresh protocol");
  }
  sameOrder(registry.scenarioOrder, scenarioOrder, "scenarioOrder");
  sameOrder(
    registry.scenarios.map(({ scenarioId }) => scenarioId),
    scenarioOrder,
    "scenarios",
  );
  sameOrder(
    registry.programs.map(({ programId }) => programId),
    programOrder,
    "programs",
  );
  sameOrder(
    registry.closureLayers.map(({ layerId }) => layerId),
    layerOrder,
    "closure layers",
  );
  sameOrder(
    registry.simulationCoverage.map(({ simulationId }) => simulationId),
    simulationOrder,
    "simulation coverage",
  );
  if (registry.inputs.length !== 18) {
    throw new Error("scenario registry must contain 18 named inputs");
  }
  for (const input of registry.inputs) {
    const scalar = input.value !== null;
    const range = input.low !== null && input.high !== null;
    if (
      scalar === range ||
      input.unit === "" ||
      input.denominator === "" ||
      input.sourceDate === ""
    ) {
      throw new Error(`${input.anchorKey}: invalid value/range or provenance fields`);
    }
    if (input.maturityState === "observed_operation") {
      throw new Error(`${input.anchorKey}: design/target input claims observed operation`);
    }
    if (input.maturityState === "hybrid_completion" && input.evidenceClass !== "ASSUMPTION") {
      throw new Error(`${input.anchorKey}: hybrid completion is not labelled ASSUMPTION`);
    }
    if (!fs.existsSync(path.join(root, input.sourceSnapshot))) {
      throw new Error(`${input.anchorKey}: source snapshot is missing`);
    }
  }
  for (const simulation of registry.simulationCoverage) {
    if (simulation.outputPaths.length === 0) {
      throw new Error(`${simulation.simulationId}: no output paths`);
    }
    for (const prefix of ["generic", "independent", "disclosed", "aspiration", "hybrid"] as const) {
      const status = simulation[`${prefix}Status`];
      const boundary = simulation[`${prefix}Boundary`];
      if (!allowedStatuses.has(status) || boundary.trim() === "") {
        throw new Error(`${simulation.simulationId}: invalid ${prefix} status or boundary`);
      }
    }
    for (const outputPath of simulation.outputPaths) {
      if (!outputPath.startsWith("outputs/") || !fs.existsSync(path.join(root, outputPath))) {
        throw new Error(`${simulation.simulationId}: missing declared output ${outputPath}`);
      }
    }
  }
  for (const capability of registry.capabilities) {
    if (capability.offWorldReproductivelyClosed) {
      throw new Error(`${capability.programId}/${capability.layerId}: unsupported closure claim`);
    }
    if (capability.responsibleLegalEntity.includes("Tesla") && capability.underCommonControl) {
      throw new Error(`${capability.programId}/${capability.layerId}: Tesla control conflation`);
    }
  }

  const inputRows = csvRows("outputs/integrated/tables/orbital_ai_scenario_inputs.csv");
  const coverageRows = csvRows("outputs/integrated/tables/simulation_scenario_coverage.csv");
  const closureRows = csvRows("outputs/integrated/tables/orbital_ai_closure_stack.csv");
  const summaryRows = csvRows("outputs/integrated/tables/orbital_ai_closure_summary.csv");
  const resultRows = csvRows("outputs/integrated/tables/orbital_ai_scenario_results.csv");
  if (inputRows.length !== registry.inputs.length) {
    throw new Error("generated scenario input register is stale");
  }
  const expectedCoverageRows = registry.simulationCoverage.reduce(
    (count, simulation) => count + simulation.outputPaths.length,
    0,
  );
  if (coverageRows.length !== expectedCoverageRows) {
    throw new Error("generated simulation coverage register is stale");
  }
  if (closureRows.length !== programOrder.length * layerOrder.length) {
    throw new Error("generated closure stack is not a complete 18-by-program matrix");
  }
  if (
    summaryRows.length !== programOrder.length ||
    summaryRows.some((row) => row.dependency_aware_off_world_closure !== "false")
  ) {
    throw new Error("closure summary count or zero-closure invariant failed");
  }
  requireColumns(
    resultRows,
    [
      "scenario_id",
      "evidence_class",
      "source_snapshot",
      "parameter_completeness",
      "boundary",
      "metric_status",
    ],
    "scenario results",
  );
  const resultOrder = resultRows.map(({ scenario_id }) =>
    scenarioOrder.indexOf(scenario_id as (typeof scenarioOrder)[number]),
  );
  if (
    resultOrder.some((value, index) => {
      const previous = index === 0 ? value : resultOrder[index - 1];
      return value < 0 || previous === undefined || value < previous;
    })
  ) {
    throw new Error("scenario result order is unstable");
  }

  const sourceText = fs.readFileSync(sourcePath, "utf8");
  for (const sourceId of ["S92", "S93", "S94", "S95"]) {
    if (!sourceText.includes(`{#source-${sourceId.toLowerCase()}`)) {
      throw new Error(`missing manuscript source ${sourceId}`);
    }
  }
  const fragments = manuscriptFragments();
  checkLanguage(fragments);
  return {
    inputs: registry.inputs.length,
    capabilities: registry.capabilities.length,
    simulationOutputRows: coverageRows.length,
    closureRows: closureRows.length,
    resultRows: resultRows.length,
    manuscriptFiles: fragments.length,
  };
}

if (import.meta.main) {
  const stats = validateScenarioPolicy();
  console.log(
    `PASS orbital-AI scenario policy: ${stats.inputs} inputs, ` +
      `${stats.simulationOutputRows} simulation/output rows, ` +
      `${stats.closureRows} closure rows, ${stats.resultRows} result rows, ` +
      `${stats.manuscriptFiles} manuscript files`,
  );
}
