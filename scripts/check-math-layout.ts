#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import {
  type Browser,
  type BrowserType,
  chromium,
  firefox,
  type Page,
  webkit,
} from "@playwright/test";

import { readEquationMetadata } from "./equations.ts";
import { root, stem } from "./manuscript-config.ts";

const site = path.join(root, "_site");
const standalone = path.join(root, "docs", `${stem}.html`);
const routes = [
  "/",
  "/part-i/",
  "/part-i/depreciation-closure.html",
  "/part-i/model-results.html",
  "/part-ii/",
  "/part-iii/",
  "/part-iv/",
  "/appendix-d/",
] as const;
const widths = [1280, 800, 520, 390] as const;
const engines: ReadonlyArray<readonly [string, BrowserType]> = [
  ["chromium", chromium],
  ["firefox", firefox],
  ["webkit", webkit],
];
const expectedEquationIds = new Set(
  readEquationMetadata().equations.map(({ id }) => id.replace(":", "-")),
);
const firstPageWideTargets = [
  "eq-digital-saturating-frontier",
  "eq-verified-loop-bottleneck",
  "eq-intelligence-embodiment-compatibility",
  "eq-embodied-task-first-passage",
  "eq-data-advantage-profile",
  "eq-data-advantage-scalarization",
  "eq-matched-lifecycle-cost",
] as const;
const failures: string[] = [];

interface WidthRecord {
  clientWidth: number;
  contentWidth: number;
  engine: string;
  id: string;
  overflowRatio: number;
  route: string;
  scrollWidth: number;
  viewportWidth: number;
}

function check(condition: boolean, message: string): void {
  if (!condition) failures.push(message);
}

async function boundedTeardown(action: () => Promise<void>): Promise<void> {
  let timeout: ReturnType<typeof setTimeout> | undefined;
  await Promise.race([
    action(),
    new Promise<void>((resolve) => {
      timeout = setTimeout(resolve, 10_000);
    }),
  ]);
  if (timeout !== undefined) clearTimeout(timeout);
}

async function closePage(page: Page, owner: Browser): Promise<void> {
  if (page.isClosed() || !owner.isConnected()) return;
  await boundedTeardown(() => page.close());
}

async function closeBrowser(owner: Browser | undefined): Promise<void> {
  if (owner === undefined || !owner.isConnected()) return;
  await boundedTeardown(() => owner.close());
}

if (!fs.existsSync(site) || !fs.statSync(site).isDirectory()) {
  process.stderr.write("FAIL _site/ does not exist; run pnpm run build:site\n");
  process.exit(1);
}
if (!fs.existsSync(standalone) || !fs.statSync(standalone).isFile()) {
  process.stderr.write("FAIL standalone HTML does not exist; run pnpm run build:manuscript\n");
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

const records: WidthRecord[] = [];
const overflowIds = new Set<string>();
let browser: Browser | undefined;
let stage = "browser startup";
try {
  for (const [engineName, engine] of engines) {
    process.stdout.write(`Math layout: checking ${engineName}…\n`);
    stage = `${engineName} startup`;
    browser = await engine.launch({ headless: true, timeout: 30_000 });
    const page = await browser.newPage();
    page.on("pageerror", (error) =>
      failures.push(`${engineName} page JavaScript error: ${error.message}`),
    );
    const seen = new Set<string>();
    const constructsSeen = new Set<string>();
    page.setDefaultNavigationTimeout(15_000);
    page.setDefaultTimeout(15_000);
    for (const route of routes) {
      await page.setViewportSize({ width: widths[0], height: 1000 });
      const response = await page.goto(`http://127.0.0.1:${server.port}${route}`, {
        waitUntil: "load",
      });
      check(response?.ok() === true, `${engineName} ${route} did not return a successful response`);
      for (const width of widths) {
        await page.setViewportSize({ width, height: 1000 });
        await page.evaluate(
          () =>
            new Promise<void>((resolve) =>
              requestAnimationFrame(() => requestAnimationFrame(() => resolve())),
            ),
        );
        stage = `${engineName} ${route} at ${width}px`;
        const result = await page.evaluate(async () => {
          await Promise.race([
            document.fonts
              .load('16px "STIX Two Math"', "∫∑√αβΓ()[]{}")
              .then(() => document.fonts.ready),
            new Promise((resolve) => setTimeout(resolve, 5_000)),
          ]);
          const main = document.querySelector<HTMLElement>("main.content");
          const equations = [...document.querySelectorAll<HTMLElement>(".numbered-equation")].map(
            (equation) => {
              const wrapper = equation.querySelector<HTMLElement>(".equation-math-scroll");
              const math = wrapper?.querySelector<MathMLElement>("math[display='block']");
              const label = equation.querySelector<HTMLElement>(".equation-label-container");
              const cue = equation.querySelector<HTMLElement>(".equation-scroll-cue");
              if (
                wrapper === null ||
                wrapper === undefined ||
                math === null ||
                math === undefined ||
                label === null ||
                cue === null
              ) {
                return { id: equation.id.replace(":", "-"), structuralFailure: true } as const;
              }
              const equationBox = equation.getBoundingClientRect();
              const wrapperBox = wrapper.getBoundingClientRect();
              const labelBox = label.getBoundingClientRect();
              return {
                id: equation.id.replace(":", "-"),
                structuralFailure: false,
                clientWidth: wrapper.clientWidth,
                scrollWidth: wrapper.scrollWidth,
                tabIndex: wrapper.tabIndex,
                fontFamily: getComputedStyle(math).fontFamily,
                mathWidth: math.getBoundingClientRect().width,
                wrapperContained:
                  wrapperBox.left >= equationBox.left - 1 &&
                  wrapperBox.right <= equationBox.right + 1,
                labelContained:
                  labelBox.left >= equationBox.left - 1 && labelBox.right <= equationBox.right + 1,
                labelVisible: labelBox.width > 0 && labelBox.height > 0,
                cueVisible: getComputedStyle(cue).display !== "none",
              } as const;
            },
          );
          return {
            contentWidth: main?.clientWidth ?? 0,
            fontLoaded: document.fonts.check('16px "STIX Two Math"', "∫∑√αβΓ()[]{}"),
            pageOverflow:
              document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
            constructCounts: {
              fraction: document.querySelectorAll("math mfrac").length,
              radical: document.querySelectorAll("math msqrt, math mroot").length,
              largeOperator: document.querySelectorAll("math munderover, math munder").length,
              matrix: document.querySelectorAll("math mtable").length,
              script: document.querySelectorAll("math msub, math msup, math msubsup").length,
              greek: [...document.querySelectorAll("math mi")].filter((item) =>
                /[α-ωΑ-Ω]/u.test(item.textContent ?? ""),
              ).length,
            },
            equations,
          };
        });
        check(result.fontLoaded, `${stage} did not load STIX Two Math`);
        check(!result.pageOverflow, `${stage} created page-level horizontal overflow`);
        for (const [construct, count] of Object.entries(result.constructCounts)) {
          if (count > 0) constructsSeen.add(construct);
        }
        for (const equation of result.equations) {
          seen.add(equation.id);
          if (equation.structuralFailure) {
            failures.push(`${stage} ${equation.id} lacks its math wrapper, MathML, or label`);
            continue;
          }
          check(
            equation.fontFamily.startsWith('"STIX Two Math"') ||
              equation.fontFamily.startsWith("STIX Two Math"),
            `${stage} ${equation.id} has unexpected font ${equation.fontFamily}`,
          );
          check(equation.tabIndex === 0, `${stage} ${equation.id} is not keyboard-scrollable`);
          check(equation.wrapperContained, `${stage} ${equation.id} scroll area escapes its grid`);
          check(equation.labelContained, `${stage} ${equation.id} label escapes its grid`);
          check(equation.labelVisible, `${stage} ${equation.id} label is not visible`);
          check(equation.mathWidth > 0, `${stage} ${equation.id} has zero-width mathematics`);
          const ratio = equation.scrollWidth / Math.max(1, equation.clientWidth);
          records.push({
            engine: engineName,
            route,
            viewportWidth: width,
            contentWidth: result.contentWidth,
            id: equation.id,
            clientWidth: equation.clientWidth,
            scrollWidth: equation.scrollWidth,
            overflowRatio: Number(ratio.toFixed(3)),
          });
          if (equation.scrollWidth > equation.clientWidth + 1) {
            overflowIds.add(equation.id);
            check(ratio <= 4, `${stage} ${equation.id} overflows by ${ratio.toFixed(2)}×`);
            check(equation.cueVisible, `${stage} ${equation.id} lacks its visible scroll cue`);
          } else {
            check(!equation.cueVisible, `${stage} ${equation.id} shows a misleading scroll cue`);
          }
        }
      }
    }
    const missing = [...expectedEquationIds].filter((identifier) => !seen.has(identifier));
    check(missing.length === 0, `${engineName} did not render equations: ${missing.join(", ")}`);
    for (const construct of ["fraction", "radical", "largeOperator", "matrix", "script", "greek"]) {
      check(constructsSeen.has(construct), `${engineName} rendered no ${construct} fixture`);
    }
    await closePage(page, browser);
    await closeBrowser(browser);
    browser = undefined;
    process.stdout.write(`Math layout: ${engineName} complete\n`);
  }

  stage = "keyboard horizontal scrolling";
  browser = await chromium.launch({ headless: true });
  const keyboardPage = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await keyboardPage.goto(`http://127.0.0.1:${server.port}/appendix-d/`, {
    waitUntil: "load",
  });
  const scrollable = keyboardPage.locator(".equation-math-scroll:has(math)");
  let testedKeyboardScroll = false;
  for (let index = 0; index < (await scrollable.count()); index += 1) {
    const candidate = scrollable.nth(index);
    const dimensions = await candidate.evaluate((element) => ({
      client: element.clientWidth,
      scroll: element.scrollWidth,
    }));
    if (dimensions.scroll <= dimensions.client + 1) continue;
    await candidate.focus();
    await keyboardPage.keyboard.press("ArrowRight");
    await keyboardPage.waitForTimeout(100);
    check(
      (await candidate.evaluate((element) => element.scrollLeft)) > 0,
      "focused wide equation must scroll with the keyboard",
    );
    testedKeyboardScroll = true;
    break;
  }
  check(testedKeyboardScroll, "no wide Appendix D equation was available for keyboard testing");

  stage = "standalone offline font";
  const standalonePage = await browser.newPage();
  await standalonePage.goto(`file://${standalone}`, { waitUntil: "load" });
  const standaloneFont = await standalonePage.evaluate(async () => {
    await document.fonts.load('16px "STIX Two Math"', "∫∑√αβΓ()[]{}");
    await document.fonts.ready;
    return {
      loaded: document.fonts.check('16px "STIX Two Math"', "∫∑√αβΓ()[]{}"),
      source: [...document.styleSheets].some((sheet) =>
        [...sheet.cssRules].some(
          (rule) =>
            rule instanceof CSSFontFaceRule &&
            rule.style.getPropertyValue("font-family").includes("STIX Two Math") &&
            rule.style.getPropertyValue("src").includes("data:font/woff2;base64"),
        ),
      ),
    };
  });
  check(standaloneFont.loaded, "standalone HTML did not load its embedded math font");
  check(standaloneFont.source, "standalone HTML math font is not embedded as a WOFF2 data URL");
  await closePage(standalonePage, browser);

  stage = "font-load failure fallback";
  const fallbackPage = await browser.newPage({ viewport: { width: 800, height: 900 } });
  await fallbackPage.route("**/STIXTwoMath-Regular.woff2", (route) => route.abort());
  await fallbackPage.goto(`http://127.0.0.1:${server.port}/`, { waitUntil: "load" });
  const fallback = await fallbackPage.locator("math[display='block']").first().boundingBox();
  check(
    fallback !== null && fallback.width > 0 && fallback.height > 0,
    "failed font load must retain readable fallback mathematics",
  );
  await closePage(fallbackPage, browser);

  stage = "site print layout";
  const printPage = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await printPage.emulateMedia({ media: "print" });
  for (const route of routes) {
    await printPage.goto(`http://127.0.0.1:${server.port}${route}`, { waitUntil: "load" });
    const printEquations = await printPage
      .locator(".equation-math-scroll")
      .evaluateAll((elements) =>
        elements.map((element) => ({
          id: element.parentElement?.id ?? "unknown",
          clientWidth: element.clientWidth,
          scrollWidth: element.scrollWidth,
          overflow: getComputedStyle(element).overflowX,
        })),
      );
    for (const equation of printEquations) {
      check(
        equation.overflow === "visible",
        `print ${equation.id} retains an interactive scroller`,
      );
      check(
        equation.scrollWidth <= equation.clientWidth + 1,
        `print ${equation.id} exceeds its printable width ` +
          `(${equation.scrollWidth}px > ${equation.clientWidth}px)`,
      );
    }
  }
  await closePage(printPage, browser);

  stage = "standalone print layout";
  const standalonePrintPage = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await standalonePrintPage.emulateMedia({ media: "print" });
  await standalonePrintPage.goto(`file://${standalone}`, { waitUntil: "load" });
  const standalonePrintOverflow = await standalonePrintPage
    .locator(".equation-math-scroll")
    .evaluateAll((elements) =>
      elements
        .filter((element) => element.scrollWidth > element.clientWidth + 1)
        .map((element) => element.parentElement?.id ?? "unknown"),
    );
  check(
    standalonePrintOverflow.length === 0,
    `standalone print equations exceed the printable width: ${standalonePrintOverflow.join(", ")}`,
  );
  await closePage(standalonePrintPage, browser);
} catch (error) {
  failures.push(
    `math layout audit could not run during ${stage}: ${
      error instanceof Error ? error.message : String(error)
    }`,
  );
} finally {
  await closeBrowser(browser);
  server.stop(true);
}

const firstPageAudit = firstPageWideTargets.map((identifier) => {
  const candidates = records.filter(
    (record) => record.id === identifier && record.viewportWidth === 800,
  );
  check(candidates.length > 0, `${identifier} has no 800px audit record`);
  const maximum =
    candidates.length > 0
      ? Math.max(...candidates.map(({ overflowRatio }) => overflowRatio))
      : Number.NaN;
  return `${identifier.replace("eq-", "")}=${maximum.toFixed(3)}×`;
});
const reflowed = records.filter(
  (record) =>
    record.id === "eq-digital-saturating-frontier" &&
    record.viewportWidth === 800 &&
    record.overflowRatio > 1.01,
);
check(
  reflowed.length === 0,
  "digital-saturating-frontier still overflows after its semantic reflow",
);

if (failures.length > 0) {
  for (const failure of failures) process.stderr.write(`FAIL ${failure}\n`);
  process.exit(1);
}
const maxOverflow = records.toSorted((left, right) => right.overflowRatio - left.overflowRatio)[0];
process.stdout.write(
  `PASS math layout: ${engines.length} engines × ${widths.length} widths; ` +
    `${expectedEquationIds.size} equations, ${overflowIds.size} intentionally scrollable; ` +
    `maximum ${maxOverflow?.overflowRatio.toFixed(3) ?? "1.000"}× ` +
    `(${maxOverflow?.id ?? "none"}, ${maxOverflow?.engine ?? "none"}, ` +
    `${maxOverflow?.viewportWidth ?? 0}px viewport / ${maxOverflow?.contentWidth ?? 0}px content); ` +
    `reviewed 800px targets: ${firstPageAudit.join(", ")}\n`,
);
