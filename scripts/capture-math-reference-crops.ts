#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import { chromium } from "@playwright/test";

import { root } from "./manuscript-config.ts";

const site = path.join(root, "_site");
const output = path.join(root, "tests", "visual", "math");
if (!fs.existsSync(site) || !fs.statSync(site).isDirectory()) {
  throw new Error("_site/ does not exist; run pnpm run build:site");
}
fs.mkdirSync(output, { recursive: true });

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

const cases = [
  {
    name: "desktop-diminishing-frontier.png",
    route: "/part-i/",
    selector: "#eq\\:digital-saturating-frontier",
    width: 1280,
    media: "screen",
  },
  {
    name: "intermediate-data-scalarization.png",
    route: "/part-i/",
    selector: "#eq\\:data-advantage-scalarization",
    width: 800,
    media: "screen",
  },
  {
    name: "mobile-authorized-capacity.png",
    route: "/part-i/",
    selector: "#eq\\:authorized-capacity-control",
    width: 390,
    media: "screen",
  },
  {
    name: "print-lexicographic-growth.png",
    route: "/appendix-d/",
    selector: "#eq\\:lexicographic-growth-stage",
    width: 794,
    media: "print",
  },
] as const;

const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 1123 } });
  for (const example of cases) {
    await page.setViewportSize({ width: example.width, height: 1123 });
    await page.emulateMedia({ media: example.media });
    await page.goto(`http://127.0.0.1:${server.port}${example.route}`, {
      waitUntil: "load",
    });
    await page.evaluate(async () => {
      await document.fonts.load('16px "STIX Two Math"', "∫∑√αβΓ()[]{}");
      await document.fonts.ready;
    });
    const equation = page.locator(example.selector);
    await equation.scrollIntoViewIfNeeded();
    await equation.screenshot({
      path: path.join(output, example.name),
      animations: "disabled",
    });
  }
} finally {
  await browser.close();
  server.stop(true);
}
process.stdout.write(`Math reference crops: ${path.relative(root, output)}/ (${cases.length})\n`);
