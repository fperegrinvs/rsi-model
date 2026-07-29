import { describe, expect, test } from "bun:test";

import {
  artifactKey,
  artifactViewerBudgets,
  assertArtifactPath,
  buildArtifactData,
  buildStandaloneArtifactPayload,
  parseCsvText,
  readArtifactReferences,
} from "../../scripts/artifacts.ts";

describe("artifact registry", () => {
  test("parses quoted CSV without altering values", () => {
    const csv =
      'name,note,value,formula\n"alpha, beta","line one\nline ""two""",,=SUM(A1:A2)\n' +
      "λ,Unicode stays Unicode,0,+CMD\n";
    const parsed = parseCsvText(csv, "fixture.csv");
    expect(parsed.headers).toEqual(["name", "note", "value", "formula"]);
    expect(parsed.rows).toEqual([
      ["alpha, beta", 'line one\nline "two"', "", "=SUM(A1:A2)"],
      ["λ", "Unicode stays Unicode", "0", "+CMD"],
    ]);
  });

  test("rejects duplicate headers and inconsistent rows", () => {
    expect(() => parseCsvText("a,a\n1,2\n", "duplicate.csv")).toThrow("duplicate headers");
    expect(() => parseCsvText("a,b\n1\n", "short.csv")).toThrow();
  });

  test("contains paths and creates stable keys", () => {
    expect(() => assertArtifactPath("../outside.csv")).toThrow("unsafe artifact path");
    expect(() => assertArtifactPath("outputs/../outside.csv")).toThrow("unsafe artifact path");
    expect(artifactKey("outputs/integrated/tables/example.csv")).toBe(
      "outputs-integrated-tables-example",
    );
  });

  test("resolves every authored reference explicitly", () => {
    const references = readArtifactReferences();
    expect(references.length).toBeGreaterThan(100);
    expect(new Set(references.map(({ path }) => path)).size).toBe(90);
  });

  test("validates manifests and preserves the largest table lazily", () => {
    const artifacts = buildArtifactData();
    const largest = artifacts.toSorted((left, right) => right.rows.length - left.rows.length)[0];
    expect(artifacts).toHaveLength(90);
    expect(largest?.path).toBe("outputs/integrated/tables/sector_capacity_trajectory.csv");
    expect(largest?.rows.length).toBeGreaterThan(8_000);
  });

  test("builds one bounded compressed standalone payload with explicit previews", () => {
    const artifacts = buildArtifactData();
    const payload = buildStandaloneArtifactPayload(artifacts);
    expect(payload.rawBytes).toBeLessThanOrEqual(
      artifactViewerBudgets.embeddedArtifactRawBytes,
    );
    expect(payload.compressedBytes).toBeLessThanOrEqual(
      artifactViewerBudgets.embeddedArtifactGzipBytes,
    );
    expect(payload.fullArtifacts + payload.previewArtifacts).toBe(artifacts.length);
    const largest = payload.artifacts.find(
      ({ path }) => path === "outputs/integrated/tables/sector_capacity_trajectory.csv",
    );
    expect(largest?.complete).toBe(false);
    expect(largest?.rows).toHaveLength(artifactViewerBudgets.previewRows);
    expect(largest?.rowCount).toBeGreaterThan(largest?.rows.length ?? Number.POSITIVE_INFINITY);
  });

  test("rejects an oversized mandatory preview payload", () => {
    const source = buildArtifactData()[0];
    if (source === undefined) throw new Error("artifact fixture is unavailable");
    const oversized = {
      ...source,
      rows: Array.from({ length: artifactViewerBudgets.previewRows }, () => [
        "x".repeat(50_000),
      ]),
      rowCount: artifactViewerBudgets.previewRows,
    };
    expect(() => buildStandaloneArtifactPayload([oversized])).toThrow(
      "standalone artifact payload",
    );
  });
});
