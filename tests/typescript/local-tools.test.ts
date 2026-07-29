import { describe, expect, test } from "bun:test";

import { quartoRelease } from "../../scripts/local-tools.ts";

describe("canonical local toolchain", () => {
  test("pins a checksum-verified macOS Quarto archive", () => {
    expect(quartoRelease.version).toBe("1.9.38");
    expect(quartoRelease.archive).toBe(`quarto-${quartoRelease.version}-macos.tar.gz`);
    expect(quartoRelease.url).toEndWith(`/v${quartoRelease.version}/${quartoRelease.archive}`);
    expect(quartoRelease.sha256).toMatch(/^[a-f0-9]{64}$/);
  });
});
