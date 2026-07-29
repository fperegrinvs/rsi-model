#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import { type Browser, chromium } from "@playwright/test";

import { root } from "./manuscript-config.ts";
import { footnoteInventory } from "./readability.ts";

const site = path.join(root, "_site");
const failures: string[] = [];
const expected = footnoteInventory();

function check(condition: boolean, message: string): void {
  if (!condition) failures.push(message);
}

if (!fs.existsSync(site) || !fs.statSync(site).isDirectory()) {
  process.stderr.write("FAIL _site/ does not exist; run pnpm run build:site\n");
  process.exit(1);
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

let browser: Browser | undefined;
let stage = "browser startup";
try {
  browser = await chromium.launch({ headless: true, timeout: 30_000 });

  const desktop = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await desktop.newPage();
  stage = "desktop hover/focus";
  await page.goto(`http://127.0.0.1:${server.port}/part-ii/`, { waitUntil: "load" });
  const reference = page.locator('a[role="doc-noteref"]').first();
  check((await page.locator('a[role="doc-noteref"]').count()) >= 1, "Part II has no footnotes");
  await reference.hover();
  await page.waitForTimeout(250);
  check((await page.locator(".tippy-box:visible").count()) === 1, "hover preview did not appear");
  await page.keyboard.press("Escape");
  await page.waitForTimeout(400);
  check((await page.locator(".tippy-box:visible").count()) === 0, "Escape did not close preview");
  await reference.focus();
  await page.waitForTimeout(250);
  check((await page.locator(".tippy-box:visible").count()) === 1, "focus preview did not appear");
  const targetSize = await reference.evaluate((element) => {
    const box = element.getBoundingClientRect();
    return { width: box.width, height: box.height };
  });
  check(
    targetSize.width >= 20 && targetSize.height >= 20,
    `footnote touch target is only ${targetSize.width.toFixed(1)}×${targetSize.height.toFixed(1)}`,
  );
  await desktop.close();

  const touch = await browser.newContext({
    viewport: { width: 390, height: 844 },
    hasTouch: true,
    isMobile: true,
  });
  const touchPage = await touch.newPage();
  stage = "touch fallback";
  await touchPage.goto(`http://127.0.0.1:${server.port}/part-ii/`, { waitUntil: "load" });
  const touchReference = touchPage.locator('a[role="doc-noteref"]').first();
  const touchHref = (await touchReference.getAttribute("href")) ?? "";
  const touchFragment = new URL(touchHref, touchPage.url()).hash;
  await touchReference.click();
  await touchPage.waitForTimeout(150);
  check(
    new URL(touchPage.url()).hash === touchFragment,
    "ordinary touch did not retain native endnote navigation",
  );
  check(
    await touchPage.locator(touchFragment).isVisible(),
    "touch target endnote is not visible after navigation",
  );
  check(
    (await touchPage.locator("dialog:visible").count()) === 0,
    "short footnote unexpectedly opens a modal",
  );
  await touch.close();

  const noScript = await browser.newContext({
    javaScriptEnabled: false,
    viewport: { width: 390, height: 844 },
  });
  const noScriptPage = await noScript.newPage();
  stage = "no-JavaScript navigation";
  await noScriptPage.goto(`http://127.0.0.1:${server.port}/part-ii/`, {
    waitUntil: "load",
  });
  const noScriptReference = noScriptPage.locator('a[role="doc-noteref"]').first();
  const noScriptHref = (await noScriptReference.getAttribute("href")) ?? "";
  const noScriptFragment = new URL(noScriptHref, noScriptPage.url()).hash;
  await noScriptReference.click();
  check(
    new URL(noScriptPage.url()).hash === noScriptFragment,
    "no-JavaScript reference did not navigate to its endnote",
  );
  const backlink = noScriptPage.locator(`${noScriptFragment} a[role="doc-backlink"]`).first();
  const backlinkHref = (await backlink.getAttribute("href")) ?? "";
  const backlinkFragment = new URL(backlinkHref, noScriptPage.url()).hash;
  await backlink.focus();
  await noScriptPage.keyboard.press("Enter");
  await noScriptPage.waitForTimeout(100);
  check(
    new URL(noScriptPage.url()).hash === backlinkFragment,
    "no-JavaScript backlink did not return to its reference",
  );
  await noScriptPage.goBack();
  check(
    new URL(noScriptPage.url()).hash === noScriptFragment,
    "browser Back did not restore the deep-linked endnote",
  );
  await noScript.close();

  const sampling = await browser.newPage({ viewport: { width: 390, height: 900 } });
  for (const route of ["/", "/part-i/model-results.html", "/part-ii/", "/part-iii/"]) {
    stage = `rendered-width sample ${route}`;
    await sampling.goto(`http://127.0.0.1:${server.port}${route}`, {
      waitUntil: "load",
    });
    const overflow = await sampling.evaluate(
      () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    );
    check(!overflow, `${route} overflows at the mobile review width`);
  }
  await sampling.close();
} catch (error) {
  failures.push(`${stage}: ${error instanceof Error ? error.message : String(error)}`);
} finally {
  await browser?.close();
  server.stop(true);
}

if (failures.length > 0) {
  for (const failure of failures) process.stderr.write(`FAIL ${failure}\n`);
  process.exit(1);
}
process.stdout.write(
  `PASS footnote interactions: ${expected.references.length} source references; ` +
    "hover, focus, Escape, touch, deep links, Back, and no-JavaScript fallback\n",
);
