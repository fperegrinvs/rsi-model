#!/usr/bin/env bun

import fs from "node:fs";
import path from "node:path";

import { type Browser, chromium } from "@playwright/test";

import { root } from "./manuscript-config.ts";
import { tableRecords } from "./tables.ts";

const site = path.join(root, "_site");
const viewportWidths = [320, 768, 1280] as const;
const tablesByPage = new Map<string, string[]>();
for (const record of tableRecords()) {
  const ids = tablesByPage.get(record.output) ?? [];
  ids.push(record.identifier);
  tablesByPage.set(record.output, ids);
}

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
  for (const [output, expectedIds] of tablesByPage) {
    const route = `/${output}`;
    for (const width of viewportWidths) {
      await page.emulateMedia({ media: "screen" });
      await page.setViewportSize({ width, height: 1000 });
      const response = await page.goto(`http://127.0.0.1:${server.port}${route}`, {
        waitUntil: "networkidle",
      });
      if (!response?.ok()) {
        failures.push(`${route} at ${width}px returned ${response?.status() ?? "no response"}`);
        continue;
      }
      const screen = await page.evaluate(() => {
        const tables = [
          ...document.querySelectorAll<HTMLElement>(".numbered-table[id^='tbl-']"),
        ].map((wrapper) => {
          const caption = wrapper.querySelector<HTMLElement>("figcaption");
          const table = wrapper.querySelector<HTMLTableElement>("table");
          const scroller = table?.parentElement;
          if (caption === null || table === null || scroller == null) {
            return { id: wrapper.id, structuralFailure: true } as const;
          }
          const wrapperRect = wrapper.getBoundingClientRect();
          const captionRect = caption.getBoundingClientRect();
          const tableRect = table.getBoundingClientRect();
          const overflow = getComputedStyle(scroller).overflowX;
          return {
            id: wrapper.id,
            structuralFailure: false,
            captionAboveTable: captionRect.bottom <= tableRect.top + 1,
            captionContained:
              captionRect.left >= wrapperRect.left - 1 &&
              captionRect.right <= wrapperRect.right + 1,
            tableContainedOrScrollable:
              tableRect.right <= wrapperRect.right + 1 || ["auto", "scroll"].includes(overflow),
            horizontalScroller:
              scroller.scrollWidth <= scroller.clientWidth + 1 ||
              ["auto", "scroll"].includes(overflow),
          } as const;
        });
        return {
          clientWidth: document.documentElement.clientWidth,
          scrollWidth: document.documentElement.scrollWidth,
          tables,
        };
      });
      const label = `${route} at ${width}px`;
      if (screen.scrollWidth > screen.clientWidth + 1) {
        failures.push(`${label} has document-level horizontal overflow`);
      }
      const actualIds = screen.tables.map(({ id }) => id);
      if (
        actualIds.length !== expectedIds.length ||
        actualIds.some((identifier, index) => identifier !== expectedIds[index])
      ) {
        failures.push(`${label} table order mismatch: ${actualIds.join(", ")}`);
      }
      for (const table of screen.tables) {
        if (table.structuralFailure) {
          failures.push(`${label} ${table.id} lacks its caption, table, or scroll container`);
          continue;
        }
        if (!table.captionAboveTable || !table.captionContained) {
          failures.push(`${label} ${table.id} caption is misplaced or clipped`);
        }
        if (!table.tableContainedOrScrollable || !table.horizontalScroller) {
          failures.push(`${label} ${table.id} is neither contained nor horizontally scrollable`);
        }
      }
    }

    await page.emulateMedia({ media: "print" });
    await page.setViewportSize({ width: 794, height: 1123 });
    await page.goto(`http://127.0.0.1:${server.port}${route}`, {
      waitUntil: "networkidle",
    });
    const print = await page.evaluate(() =>
      [...document.querySelectorAll<HTMLElement>(".numbered-table[id^='tbl-']")].map((wrapper) => {
        const caption = wrapper.querySelector<HTMLElement>("figcaption");
        const table = wrapper.querySelector<HTMLTableElement>("table");
        const head = table?.querySelector<HTMLTableSectionElement>("thead");
        const rows = table === null ? [] : [...table.querySelectorAll<HTMLTableRowElement>("tr")];
        return {
          id: wrapper.id,
          structuralFailure: caption === null || table === null || head == null,
          captionBreak: caption === null ? "" : getComputedStyle(caption).breakAfter,
          headerDisplay: head == null ? "" : getComputedStyle(head).display,
          rowBreaks: rows.map((row) => getComputedStyle(row).breakInside),
          tableWidth: table?.getBoundingClientRect().width ?? 0,
          contentWidth:
            document.querySelector<HTMLElement>("main.content")?.getBoundingClientRect().width ?? 0,
        };
      }),
    );
    for (const table of print) {
      if (table.structuralFailure) {
        failures.push(`${route} print ${table.id} lacks caption, table, or repeated header`);
        continue;
      }
      if (!["avoid", "avoid-page"].includes(table.captionBreak)) {
        failures.push(`${route} print ${table.id} caption can separate from its table`);
      }
      if (table.headerDisplay !== "table-header-group") {
        failures.push(`${route} print ${table.id} header will not repeat`);
      }
      if (table.rowBreaks.some((value) => !["avoid", "avoid-page"].includes(value))) {
        failures.push(`${route} print ${table.id} permits a split row`);
      }
      if (table.tableWidth > table.contentWidth + 1) {
        failures.push(`${route} print ${table.id} exceeds the printable content width`);
      }
    }
  }
} catch (error) {
  failures.push(
    `browser table-layout audit could not run: ${error instanceof Error ? error.message : String(error)}`,
  );
} finally {
  await browser?.close();
  server.stop(true);
}

if (failures.length > 0) fail(failures);
process.stdout.write(
  `PASS table layout: ${tablesByPage.size} pages × ${viewportWidths.length} screen widths ` +
    "plus print; captions, scrolling, repeated headers, and unsplit rows verified\n",
);
