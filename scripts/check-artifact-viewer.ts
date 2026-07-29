#!/usr/bin/env bun

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

import { type Browser, chromium, webkit } from "@playwright/test";

import { artifactViewerBudgets } from "./artifacts.ts";
import { root, stem } from "./manuscript-config.ts";

const site = path.join(root, "_site");
const standalone = path.join(root, "docs", `${stem}.html`);
const failures: string[] = [];

function check(condition: boolean, message: string): void {
  if (!condition) failures.push(message);
}

if (!fs.existsSync(site) || !fs.statSync(site).isDirectory()) {
  process.stderr.write("FAIL _site/ does not exist; run pnpm run build:site\n");
  process.exit(1);
}
if (!fs.existsSync(standalone) || !fs.statSync(standalone).isFile()) {
  process.stderr.write("FAIL standalone HTML does not exist; run pnpm run build:manuscript\n");
  process.exit(1);
}

const csvRequests: string[] = [];
const server = Bun.serve({
  hostname: "127.0.0.1",
  port: 0,
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname.endsWith(".csv")) csvRequests.push(url.pathname);
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

const largestKey = "outputs-integrated-tables-sector-capacity-trajectory";
const smallName = "View data: closure loop ablation matrix";
let browser: Browser | undefined;
let webkitBrowser: Browser | undefined;
let stage = "browser startup";
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "rsi-artifact-viewer-"));

try {
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    reducedMotion: "reduce",
    viewport: { width: 1280, height: 900 },
  });
  const page = await context.newPage();
  page.on("pageerror", (error) => failures.push(`site JavaScript error: ${error.message}`));
  const base = `http://127.0.0.1:${server.port}`;

  stage = "opening a chapter artifact";
  await page.goto(`${base}/part-i/`, { waitUntil: "networkidle" });
  check(
    (await page.locator("[data-artifact-viewer]").count()) === 1,
    "site chapter must contain one reusable viewer shell",
  );
  const sourceButton = page.getByRole("button", { name: smallName }).first();
  check(
    (await sourceButton.evaluate((element) => element.tagName)) === "BUTTON",
    "View data must be a native button",
  );
  const sourceReference = sourceButton.locator("xpath=..");
  const sourceDownload = sourceReference.getByRole("link", { name: /Download .*CSV/ });
  check(
    (await sourceDownload.getAttribute("download")) !== null,
    "the adjacent CSV action must be a native download link",
  );
  const requestsBefore = csvRequests.length;
  await sourceButton.focus();
  await page.keyboard.press("Enter");
  const dialog = page.getByRole("dialog");
  await dialog.waitFor({ state: "visible" });
  await page.getByText("4 rows loaded.", { exact: true }).waitFor();
  check(
    csvRequests.length === requestsBefore,
    "opening the viewer must not request or navigate to CSV",
  );
  check(
    (await dialog.getByRole("button", { name: "Close data viewer" }).count()) === 1,
    "viewer close control must have an accessible name",
  );
  check(
    (await dialog.locator("caption").textContent())?.trim().length !== 0,
    "viewer table must have a semantic caption",
  );
  check(
    (await dialog.locator('thead th[scope="col"]').count()) > 0,
    "viewer table must use scoped column headers",
  );
  check(
    (await dialog.locator('tbody th[scope="row"]').count()) > 0,
    "a registered identifier must render as scoped row headers",
  );
  const cdp = await context.newCDPSession(page);
  const accessibilityTree = await cdp.send("Accessibility.getFullAXTree");
  const accessibilityRoles = new Set(
    accessibilityTree.nodes
      .map((node) => node.role?.value)
      .filter((value): value is string => typeof value === "string"),
  );
  for (const role of ["dialog", "table", "columnheader", "rowheader", "status"]) {
    check(accessibilityRoles.has(role), `Chromium accessibility tree must expose the ${role} role`);
  }
  check(
    (await dialog.locator("[data-artifact-table-region]").getAttribute("tabindex")) === "0",
    "scrollable table region must be keyboard focusable",
  );
  const firstSort = dialog.locator("thead .artifact-sort").first();
  await firstSort.focus();
  await page.keyboard.press("Space");
  check(
    ["ascending", "descending"].includes(
      (await firstSort.locator("xpath=..").getAttribute("aria-sort")) ?? "",
    ),
    "keyboard sorting must expose aria-sort",
  );
  const search = dialog.getByRole("searchbox", { name: "Search table" });
  await search.fill("no-value-can-match-this-query");
  await dialog.getByText("No matching rows", { exact: true }).waitFor();
  await page.keyboard.press("Escape");
  if (await dialog.isVisible()) await page.keyboard.press("Escape");
  await dialog.waitFor({ state: "hidden" });
  check(
    await sourceButton.evaluate((element) => element === document.activeElement),
    "closing the viewer must return focus to the triggering button",
  );

  stage = "opening the largest site artifact";
  await page.goto(`${base}/data/`, { waitUntil: "networkidle" });
  const largestButton = page.locator(
    `button[data-artifact-view][data-artifact-key="${largestKey}"]`,
  );
  const firstViewStart = performance.now();
  await largestButton.click();
  await page.getByText("8,694 rows loaded.", { exact: true }).waitFor();
  const firstViewMilliseconds = performance.now() - firstViewStart;
  check(
    firstViewMilliseconds <= artifactViewerBudgets.firstViewMilliseconds,
    `site first view ${Math.round(firstViewMilliseconds)} ms exceeds budget`,
  );
  check(
    (await dialog.locator("tbody tr").count()) === 50,
    "largest site table must render only its configured first page",
  );
  check(
    (await dialog.locator("[data-artifact-range]").textContent()) === "Rows 1–50 of 8,694",
    "largest site table must announce its first row range",
  );
  await dialog.getByRole("button", { name: "Next" }).click();
  check(
    (await dialog.locator("[data-artifact-range]").textContent()) === "Rows 51–100 of 8,694",
    "pagination must advance by 50 rows",
  );
  check(
    (
      await dialog.getByRole("link", { name: "Open full data page" }).getAttribute("href")
    )?.endsWith(`${largestKey}.html`) === true,
    "viewer must expose a readable stable HTML data page",
  );
  check(
    await dialog.getByRole("link", { name: /Download .*CSV/ }).isVisible(),
    "viewer must expose an explicitly labeled original CSV download",
  );
  check(
    (await page.evaluate(() => location.hash)) === `#view-${largestKey}`,
    "opening a table must create a stable viewer fragment",
  );
  await page.keyboard.press("Escape");
  await dialog.waitFor({ state: "hidden" });
  await page.waitForTimeout(100);

  stage = "opening a stable full-data page fragment";
  await page.goto(`${base}/data/artifacts/${largestKey}.html#view-${largestKey}`, {
    waitUntil: "networkidle",
  });
  await dialog.waitFor({ state: "visible" });
  await page.getByText("8,694 rows loaded.", { exact: true }).waitFor();
  await page.keyboard.press("Escape");

  stage = "checking mobile, zoom, reduced-motion, and forced-color layouts";
  await page.setViewportSize({ width: 844, height: 390 });
  await page.goto(`${base}/data/`, { waitUntil: "networkidle" });
  await page.locator(`button[data-artifact-view][data-artifact-key="${largestKey}"]`).click();
  await dialog.waitFor({ state: "visible" });
  const mobileBox = await dialog.boundingBox();
  check(
    mobileBox !== null && mobileBox.width <= 844.5 && mobileBox.height <= 390.5,
    "mobile-landscape viewer must fit the viewport",
  );
  const mobileOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  check(!mobileOverflow, "mobile viewer must not create page-level horizontal overflow");
  for (const [zoom, width] of [
    [2, 422],
    [4, 211],
  ] as const) {
    await page.setViewportSize({ width, height: 390 });
    const overlap = await dialog.locator("[data-artifact-table-region]").evaluate((element) => {
      const region = element.getBoundingClientRect();
      return region.left < 0 || region.right > window.innerWidth + 1;
    });
    check(!overlap, `table scroll region must remain contained at ${zoom * 100}% zoom`);
    const headerColors = await dialog
      .locator("thead th")
      .first()
      .evaluate((element) => {
        const header = getComputedStyle(element);
        const sort = element.querySelector<HTMLElement>(".artifact-sort");
        return {
          background: header.backgroundColor,
          foreground: sort === null ? header.color : getComputedStyle(sort).color,
        };
      });
    check(
      headerColors.foreground !== headerColors.background,
      `sticky table header text must remain visible at ${zoom * 100}% zoom`,
    );
  }
  await page.emulateMedia({ forcedColors: "active", reducedMotion: "reduce" });
  check(
    await dialog.locator("[data-artifact-table-region]").isVisible(),
    "viewer table must remain visible in forced-colors mode",
  );
  await page.keyboard.press("Escape");

  stage = "testing site metadata failures";
  const failurePage = await context.newPage();
  failurePage.on("pageerror", (error) =>
    failures.push(`failure-page JavaScript error: ${error.message}`),
  );
  await failurePage.route("**/data/artifacts/*.json", (route) => route.abort());
  await failurePage.goto(`${base}/part-i/`, { waitUntil: "networkidle" });
  await failurePage.getByRole("button", { name: smallName }).first().click();
  const failureDialog = failurePage.getByRole("dialog");
  await failureDialog.getByText(/Table could not be loaded:/).waitFor();
  check(
    await failureDialog.getByRole("link", { name: /Download .*CSV/ }).isVisible(),
    "load failure must preserve an explicitly labeled CSV download",
  );
  await failurePage.close();

  stage = "testing manifest/hash mismatch";
  const mismatchPage = await context.newPage();
  await mismatchPage.goto(`${base}/part-i/`, { waitUntil: "networkidle" });
  const mismatchButton = mismatchPage.getByRole("button", { name: smallName }).first();
  await mismatchButton.evaluate((element) => {
    element.dataset.artifactHash = "0".repeat(64);
  });
  await mismatchButton.click();
  await mismatchPage
    .getByRole("dialog")
    .getByText(/does not match its manifest reference/)
    .waitFor();
  await mismatchPage.close();
  await context.close();

  stage = "opening the standalone viewer from file URL";
  const standaloneContext = await browser.newContext({
    reducedMotion: "reduce",
    viewport: { width: 1280, height: 900 },
  });
  const standalonePage = await standaloneContext.newPage();
  const standaloneRequests: string[] = [];
  standalonePage.on("request", (request) => {
    if (request.url().endsWith(".csv")) standaloneRequests.push(request.url());
  });
  const startupStart = performance.now();
  await standalonePage.goto(pathToFileURL(standalone).href, { waitUntil: "load" });
  await standalonePage.locator("html.rsi-enhanced").waitFor();
  const startupMilliseconds = performance.now() - startupStart;
  check(
    startupMilliseconds <= artifactViewerBudgets.startupMilliseconds,
    `standalone startup ${Math.round(startupMilliseconds)} ms exceeds budget`,
  );
  check(
    (await standalonePage.locator("[data-artifact-viewer]").count()) === 1,
    "standalone must contain the shared viewer shell",
  );
  const standaloneSmall = standalonePage.getByRole("button", { name: smallName }).first();
  await standaloneSmall.click();
  const standaloneDialog = standalonePage.getByRole("dialog");
  await standaloneDialog.getByText("4 rows loaded.", { exact: true }).waitFor();
  check(
    standaloneRequests.length === 0,
    "ordinary standalone viewing must decode embedded data without requesting a CSV",
  );
  await standalonePage.keyboard.press("Escape");
  const standaloneLargest = standalonePage
    .locator(`button[data-artifact-view][data-artifact-key="${largestKey}"]`)
    .first();
  const offlineViewStart = performance.now();
  await standaloneLargest.click();
  await standaloneDialog
    .getByText("50 preview rows loaded from 8,694 total rows.", { exact: true })
    .waitFor();
  const offlineViewMilliseconds = performance.now() - offlineViewStart;
  check(
    offlineViewMilliseconds <= artifactViewerBudgets.firstViewMilliseconds,
    `standalone first view ${Math.round(offlineViewMilliseconds)} ms exceeds budget`,
  );
  check(
    (await standaloneDialog.locator("[data-artifact-preview]").textContent())?.includes(
      "Search, sorting, and page counts cover only this preview.",
    ) === true,
    "standalone preview must disclose omitted rows and operation scope",
  );
  check(
    (await standaloneDialog.locator("tbody tr").count()) === 50,
    "standalone large-table preview must stay within its declared row budget",
  );
  await standalonePage.keyboard.press("Escape");
  await standaloneContext.close();

  stage = "testing no-JavaScript standalone fallback";
  const noScriptContext = await browser.newContext({ javaScriptEnabled: false });
  const noScriptPage = await noScriptContext.newPage();
  await noScriptPage.goto(pathToFileURL(standalone).href, { waitUntil: "load" });
  check(
    !(await noScriptPage.getByRole("button", { name: smallName }).first().isVisible()),
    "no-JavaScript standalone must not promise an inert View data action",
  );
  check(
    await noScriptPage
      .getByRole("link", { name: /Download .*CSV/ })
      .first()
      .isVisible(),
    "no-JavaScript standalone must expose an explicit CSV download",
  );
  await noScriptContext.close();

  stage = "testing corrupt standalone payload and unavailable raw-file fallback";
  const source = fs.readFileSync(standalone, "utf8");
  const corrupt = source.replace(
    /(<script type="application\/octet-stream" data-artifact-payload data-compression="gzip">)[\s\S]*?(<\/script>)/,
    "$1not-a-gzip-payload$2",
  );
  const corruptFile = path.join(temporary, "corrupt.html");
  fs.writeFileSync(corruptFile, corrupt);
  const corruptContext = await browser.newContext();
  const corruptPage = await corruptContext.newPage();
  await corruptPage.goto(pathToFileURL(corruptFile).href, { waitUntil: "load" });
  const corruptButton = corruptPage.getByRole("button", { name: smallName }).first();
  await corruptButton.evaluate((element) => {
    element.dataset.artifactDownload = "./missing.csv";
    element.dataset.artifactDownloadLabel = "Download original CSV (file unavailable)";
  });
  await corruptButton.click();
  const corruptDialog = corruptPage.getByRole("dialog");
  await corruptDialog.getByText(/Table could not be loaded:/).waitFor();
  check(
    (await corruptDialog
      .getByRole("link", { name: /Download original CSV/ })
      .getAttribute("href")) === "./missing.csv",
    "corrupt-payload fallback must remain explicitly labeled even when the raw file is unavailable",
  );
  await corruptContext.close();

  stage = "testing WebKit dialog and table semantics";
  webkitBrowser = await webkit.launch({ headless: true });
  const webkitPage = await webkitBrowser.newPage({
    reducedMotion: "reduce",
    viewport: { width: 390, height: 844 },
  });
  webkitPage.on("pageerror", (error) => failures.push(`WebKit JavaScript error: ${error.message}`));
  await webkitPage.goto(pathToFileURL(standalone).href, { waitUntil: "load" });
  const webkitButton = webkitPage.getByRole("button", { name: smallName }).first();
  await webkitButton.click();
  const webkitDialog = webkitPage.getByRole("dialog");
  await webkitDialog.getByText("4 rows loaded.", { exact: true }).waitFor();
  check(
    (await webkitDialog.locator('thead th[scope="col"]').count()) > 0 &&
      (await webkitDialog.locator('tbody th[scope="row"]').count()) > 0,
    "WebKit must preserve semantic column and row headers",
  );
  await webkitPage.keyboard.press("Escape");
  await webkitDialog.waitFor({ state: "hidden" });
} catch (error) {
  failures.push(
    `artifact viewer audit could not run during ${stage}: ${
      error instanceof Error ? error.message : String(error)
    }`,
  );
} finally {
  await browser?.close();
  await webkitBrowser?.close();
  server.stop(true);
  fs.rmSync(temporary, { recursive: true, force: true });
}

if (failures.length > 0) {
  for (const failure of failures) process.stderr.write(`FAIL ${failure}\n`);
  process.exit(1);
}
process.stdout.write(
  "PASS artifact viewer: site + standalone/file, no-JS, payload/hash failures, keyboard, " +
    "focus, deep links, mobile landscape, zoom, forced colors, Chromium accessibility tree, " +
    "WebKit semantics, search, sorting, and pagination\n",
);
