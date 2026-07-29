#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import { type Browser, chromium } from "@playwright/test";

import { root } from "./manuscript-config.ts";

const site = path.join(root, "_site");
const targets = new Map<string, readonly string[]>([
  [
    "/part-i/model-results.html",
    [
      "fig-survival-central",
      "fig-import-decay-sweep",
      "fig-seed-mass-ensemble",
      "fig-operating-capacity",
      "fig-oversize-frontier",
      "fig-compute-growth-regimes",
      "fig-debris-regimes",
    ],
  ],
  [
    "/part-ii/index.html",
    ["fig-spacexai-threshold-tornado", "fig-lco-ratio-monte-carlo", "fig-crossover-surface"],
  ],
]);
const viewportWidths = [320, 768, 1280, 1440] as const;

function fail(messages: readonly string[]): never {
  for (const message of messages) process.stderr.write(`FAIL ${message}\n`);
  process.exit(1);
}

if (!fs.existsSync(site) || !fs.statSync(site).isDirectory()) {
  fail(["_site/ does not exist; run pnpm run build:site"]);
}

const server = Bun.serve({
  hostname: "127.0.0.1",
  port: 0,
  async fetch(request) {
    const url = new URL(request.url);
    let pathname = decodeURIComponent(url.pathname);
    if (pathname.endsWith("/")) pathname += "index.html";
    const target = path.normalize(path.join(site, pathname));
    if (!target.startsWith(`${site}${path.sep}`)) {
      return new Response("Forbidden", { status: 403 });
    }
    const file = Bun.file(target);
    if (!(await file.exists())) return new Response("Not found", { status: 404 });
    return new Response(file);
  },
});

const failures: string[] = [];
let browser: Browser | undefined;
try {
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  for (const [route, expectedIds] of targets) {
    for (const width of viewportWidths) {
      await page.setViewportSize({ width, height: 1000 });
      const response = await page.goto(`http://127.0.0.1:${server.port}${route}`, {
        waitUntil: "networkidle",
      });
      if (!response?.ok()) {
        failures.push(`${route} at ${width}px returned ${response?.status() ?? "no response"}`);
        continue;
      }
      const result = await page.evaluate(() => {
        const figures = [...document.querySelectorAll<HTMLElement>("figure[id^='fig-']")].map(
          (figure) => {
            const image = figure.querySelector<HTMLImageElement>("img");
            const caption = figure.querySelector<HTMLElement>("figcaption");
            if (image === null || caption === null) {
              return { id: figure.id, structuralFailure: true } as const;
            }
            const figureRect = figure.getBoundingClientRect();
            const imageRect = image.getBoundingClientRect();
            const captionRect = caption.getBoundingClientRect();
            const naturalRatio =
              image.naturalHeight > 0 ? image.naturalWidth / image.naturalHeight : 0;
            const renderedRatio = imageRect.height > 0 ? imageRect.width / imageRect.height : 0;
            return {
              id: figure.id,
              structuralFailure: false,
              imageWidth: imageRect.width,
              imageHeight: imageRect.height,
              figureWidth: figureRect.width,
              captionWidth: captionRect.width,
              aspectError: Math.abs(renderedRatio - naturalRatio),
              imageContained:
                imageRect.left >= figureRect.left - 0.5 &&
                imageRect.right <= figureRect.right + 0.5,
              captionContained:
                captionRect.left >= figureRect.left - 0.5 &&
                captionRect.right <= figureRect.right + 0.5,
              wideLink:
                !figure.classList.contains("figure-wide") ||
                figure.querySelector("a.figure-full-resolution-link > img") !== null,
            } as const;
          },
        );
        return {
          viewportWidth: window.innerWidth,
          clientWidth: document.documentElement.clientWidth,
          scrollWidth: document.documentElement.scrollWidth,
          figures,
        };
      });
      const label = `${route} at ${width}px`;
      if (result.viewportWidth !== width) {
        failures.push(`${label} rendered at ${result.viewportWidth}px`);
      }
      if (result.scrollWidth > result.clientWidth + 1) {
        failures.push(
          `${label} has horizontal overflow (${result.scrollWidth}px > ${result.clientWidth}px)`,
        );
      }
      const actualIds = result.figures.map(({ id }) => id);
      if (
        actualIds.length !== expectedIds.length ||
        actualIds.some((identifier, index) => identifier !== expectedIds[index])
      ) {
        failures.push(`${label} figure order mismatch: ${actualIds.join(", ")}`);
      }
      for (const figure of result.figures) {
        if (figure.structuralFailure) {
          failures.push(`${label} ${figure.id} lacks its image or caption`);
          continue;
        }
        if (figure.imageWidth <= 0 || figure.imageHeight <= 0) {
          failures.push(`${label} ${figure.id} has no rendered image area`);
        }
        if (!figure.imageContained || figure.imageWidth > figure.figureWidth + 0.5) {
          failures.push(`${label} ${figure.id} image escapes its figure`);
        }
        if (!figure.captionContained || figure.captionWidth > figure.figureWidth + 0.5) {
          failures.push(`${label} ${figure.id} caption escapes its figure`);
        }
        if (figure.aspectError > 0.02) {
          failures.push(`${label} ${figure.id} distorts its raster aspect ratio`);
        }
        if (!figure.wideLink) {
          failures.push(`${label} ${figure.id} lacks its full-resolution link`);
        }
      }
    }
  }
} catch (error) {
  failures.push(
    `browser layout audit could not run: ${error instanceof Error ? error.message : String(error)}`,
  );
} finally {
  await browser?.close();
  server.stop(true);
}

if (failures.length > 0) fail(failures);
process.stdout.write(
  `PASS figure layout: ${targets.size} pages × ${viewportWidths.length} viewports; ` +
    "no overflow, clipping, distortion, or missing full-resolution links\n",
);
