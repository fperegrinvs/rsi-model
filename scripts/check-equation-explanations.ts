#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import { type Browser, chromium } from "@playwright/test";

import { readEquationMetadata } from "./equations.ts";
import { root } from "./manuscript-config.ts";

const site = path.join(root, "_site");
const failures: string[] = [];

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
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    reducedMotion: "reduce",
    viewport: { width: 1280, height: 900 },
  });
  const page = await context.newPage();
  page.on("pageerror", (error) =>
    failures.push(`equation-page JavaScript error: ${error.message}`),
  );
  const base = `http://127.0.0.1:${server.port}`;
  stage = "opening the first equation";
  await page.goto(`${base}/`, { waitUntil: "networkidle" });
  const equation = page.locator("#eq\\:orbital-deployment");
  const button = page.getByRole("button", { name: "Explain equation (1)" });
  const details = page.locator("#explain-eq-orbital-deployment");
  check((await button.count()) === 1, "equation must have one explicitly named explanation button");
  check(
    (await equation.locator("math[display='block']").count()) === 1,
    "equation must retain its native MathML display",
  );
  const equationHref = await equation.locator("a.equation-label").getAttribute("href");
  check(
    equationHref !== null &&
      decodeURIComponent(new URL(equationHref, page.url()).hash) === "#eq:orbital-deployment",
    "equation number must retain its stable anchor",
  );
  check(
    (await equation.locator("math button, a.equation-label button").count()) === 0,
    "mathematics and its number must not become explanation controls",
  );
  await button.focus();
  await page.keyboard.press("Enter");
  await details.waitFor({ state: "visible" });
  check((await button.getAttribute("aria-expanded")) === "true", "button must expose open state");
  check(
    new URL(page.url()).hash === "#explain-eq-orbital-deployment",
    "opening an explanation must create its stable fragment",
  );
  check(
    (await details.locator("math").count()) >= 5,
    "term definitions must use server-rendered MathML",
  );
  check(
    await details.getByText("Earth-fed orbital deployment", { exact: true }).isVisible(),
    "explanation title must be visible",
  );
  await page.keyboard.press("Escape");
  await details.waitFor({ state: "hidden" });
  check(
    await button.evaluate((element) => element === document.activeElement),
    "Escape must return focus to the equation explanation button",
  );
  check(
    (await button.getAttribute("aria-expanded")) === "false",
    "button must expose closed state",
  );

  stage = "testing equation explanation history";
  await button.click();
  await details.waitFor({ state: "visible" });
  await page.goBack();
  await details.waitFor({ state: "hidden" });
  await page.goForward();
  await details.waitFor({ state: "visible" });

  stage = "opening a direct explanation fragment";
  await page.goto(`${base}/#explain-eq-orbital-deployment`, { waitUntil: "networkidle" });
  await details.waitFor({ state: "visible" });
  check(
    (await button.getAttribute("aria-expanded")) === "true",
    "direct fragment must set open state",
  );

  stage = "checking the mobile equation disclosure";
  await page.setViewportSize({ width: 390, height: 844 });
  const mobile = await details.evaluate((element) => {
    const box = element.getBoundingClientRect();
    return {
      right: box.right,
      viewport: document.documentElement.clientWidth,
      pageOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    };
  });
  check(mobile.right <= mobile.viewport + 1, "mobile equation explanation must stay in its column");
  check(!mobile.pageOverflow, "equation explanation must not create page-level mobile overflow");

  stage = "following an explanation link from the notation register";
  await page.setViewportSize({ width: 800, height: 900 });
  await page.goto(`${base}/notation/`, { waitUntil: "networkidle" });
  const notationLinks = page.locator("a.equation-explanation-reference");
  const expectedNotationLinks = readEquationMetadata().terms.size;
  check(
    (await notationLinks.count()) === expectedNotationLinks,
    "notation register must link every canonical term to an equation explanation",
  );
  const firstNotationLink = notationLinks.first();
  check(
    (await firstNotationLink.getAttribute("aria-label")) === "Open explanation for equation 1",
    "notation explanation link must have an equation-specific accessible name",
  );
  await firstNotationLink.focus();
  await page.keyboard.press("Enter");
  await page.locator("#explain-eq-orbital-deployment").waitFor({ state: "visible" });
  check(
    new URL(page.url()).hash === "#explain-eq-orbital-deployment",
    "notation-register link must open the stable explanation fragment",
  );
  await context.close();

  stage = "checking the no-script baseline";
  const noScript = await browser.newContext({
    javaScriptEnabled: false,
    viewport: { width: 800, height: 900 },
  });
  const noScriptPage = await noScript.newPage();
  await noScriptPage.goto(`${base}/`, { waitUntil: "domcontentloaded" });
  const noScriptButton = noScriptPage.getByRole("button", { name: "Explain equation (1)" });
  const noScriptDetails = noScriptPage.locator("#explain-eq-orbital-deployment");
  check(!(await noScriptButton.isVisible()), "no-script baseline must hide the inert button");
  check(
    await noScriptDetails.getByText("Explain equation (1)", { exact: true }).isVisible(),
    "no-script baseline must expose the native details summary",
  );
  await noScriptDetails.locator("summary").click();
  check(
    await noScriptDetails.getByText("Earth-fed orbital deployment", { exact: true }).isVisible(),
    "native details must reveal the explanation without JavaScript",
  );
  await noScript.close();
} catch (error) {
  failures.push(
    `equation explanation audit could not run during ${stage}: ${
      error instanceof Error ? error.message : String(error)
    }`,
  );
} finally {
  await browser?.close();
  server.stop(true);
}

if (failures.length > 0) {
  for (const failure of failures) process.stderr.write(`FAIL ${failure}\n`);
  process.exit(1);
}
process.stdout.write(
  "PASS equation explanations: MathML, keyboard, Escape, focus, history, fragments, mobile, and no-script\n",
);
