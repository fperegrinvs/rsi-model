import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";

import { root } from "./manuscript-config.ts";

export const quartoRelease = {
  version: "1.9.38",
  archive: "quarto-1.9.38-macos.tar.gz",
  sha256: "47089a5020cfb41981ba0d4b46e110edfa608722aea45ef248e14efba6d6b18a",
  url: "https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.38/quarto-1.9.38-macos.tar.gz",
} as const;

const toolsDirectory = path.join(root, ".tools");
const installationDirectory = path.join(toolsDirectory, `quarto-${quartoRelease.version}`);
const quartoBinary = path.join(installationDirectory, "bin", "quarto");

function fail(message: string): never {
  throw new Error(message);
}

function run(command: string, args: string[]): string {
  const result = spawnSync(command, args, {
    cwd: root,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
  if (result.error !== undefined) {
    fail(`${command} could not start: ${result.error.message}`);
  }
  if (result.status !== 0) {
    fail(result.stderr.trim() || result.stdout.trim() || `${command} failed`);
  }
  return result.stdout.trim();
}

async function sha256(file: string): Promise<string> {
  const digest = createHash("sha256");
  for await (const chunk of fs.createReadStream(file)) digest.update(chunk);
  return digest.digest("hex");
}

function validateQuarto(binary: string): void {
  const actual = run(binary, ["--version"]);
  if (actual !== quartoRelease.version) {
    fail(`Expected Quarto ${quartoRelease.version}, found ${actual || "unknown"}`);
  }
}

export async function ensureLocalQuarto(): Promise<string> {
  if (process.platform !== "darwin") {
    fail("The canonical local publication pipeline is configured for macOS");
  }
  if (fs.existsSync(quartoBinary)) {
    validateQuarto(quartoBinary);
    return quartoBinary;
  }

  fs.mkdirSync(toolsDirectory, { recursive: true });
  const archive = path.join(toolsDirectory, quartoRelease.archive);
  if (fs.existsSync(archive) && (await sha256(archive)) !== quartoRelease.sha256) {
    fs.unlinkSync(archive);
  }
  if (!fs.existsSync(archive)) {
    const partial = `${archive}.part-${process.pid}`;
    try {
      run("curl", ["--fail", "--location", "--retry", "3", "--output", partial, quartoRelease.url]);
      const actual = await sha256(partial);
      if (actual !== quartoRelease.sha256) {
        fail(`Quarto archive checksum mismatch: expected ${quartoRelease.sha256}, found ${actual}`);
      }
      fs.renameSync(partial, archive);
    } finally {
      if (fs.existsSync(partial)) fs.unlinkSync(partial);
    }
  }

  const extractionRoot = fs.mkdtempSync(path.join(toolsDirectory, ".quarto-extract-"));
  try {
    run("tar", ["-xzf", archive, "-C", extractionRoot]);
    if (!fs.existsSync(path.join(extractionRoot, "bin", "quarto"))) {
      fail("Quarto archive did not contain bin/quarto");
    }
    if (fs.existsSync(installationDirectory)) {
      fail(`Incomplete Quarto installation already exists: ${installationDirectory}`);
    }
    fs.renameSync(extractionRoot, installationDirectory);
  } finally {
    fs.rmSync(extractionRoot, { recursive: true, force: true });
  }

  validateQuarto(quartoBinary);
  return quartoBinary;
}
