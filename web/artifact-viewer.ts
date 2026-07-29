import { artifactViewerShell } from "./artifact-viewer-shell.ts";

export interface ArtifactColumn {
  description?: string;
  key: boolean;
  label: string;
  name: string;
  units?: string;
}

export interface ArtifactData {
  columns: ArtifactColumn[];
  complete: boolean;
  defaultSort?: { column: string; direction: "asc" | "desc" };
  description: string;
  freshness: string;
  hash: string;
  key: string;
  path: string;
  rowCount: number;
  rows: string[][];
  sizeBytes: number;
  sourceClass: string;
  sourceManifest: string;
  title: string;
}

interface EmbeddedPayload {
  artifacts: ArtifactData[];
  format: "rsi-artifact-viewer-v1";
}

type SortState = { column: number; direction: "asc" | "desc" } | null;
type ArtifactTrigger = HTMLButtonElement;

function required<T extends Element>(root: ParentNode, selector: string): T {
  const element = root.querySelector<T>(selector);
  if (element === null) throw new Error(`Missing viewer element: ${selector}`);
  return element;
}

function comparable(value: string): number | string {
  const stripped = value.trim();
  if (/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?$/.test(stripped)) {
    return Number(stripped);
  }
  return stripped.toLocaleLowerCase();
}

function copyText(value: string): Promise<void> {
  if (navigator.clipboard?.writeText !== undefined) return navigator.clipboard.writeText(value);
  const textarea = document.createElement("textarea");
  textarea.value = value;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.append(textarea);
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
  return Promise.resolve();
}

function decodeBase64(value: string): Uint8Array {
  const binary = atob(value.replace(/\s+/g, ""));
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }
  return bytes;
}

async function decodeEmbeddedPayload(): Promise<Map<string, ArtifactData>> {
  const element = document.querySelector<HTMLScriptElement>(
    'script[data-artifact-payload][data-compression="gzip"]',
  );
  if (element === null) throw new Error("embedded table payload is unavailable");
  if (typeof DecompressionStream === "undefined") {
    throw new Error("this browser cannot decompress the offline table preview");
  }
  const bytes = decodeBase64(element.textContent ?? "");
  const buffer = new ArrayBuffer(bytes.byteLength);
  new Uint8Array(buffer).set(bytes);
  const stream = new Blob([buffer]).stream().pipeThrough(new DecompressionStream("gzip"));
  const parsed = (await new Response(stream).json()) as EmbeddedPayload;
  if (
    parsed.format !== "rsi-artifact-viewer-v1" ||
    !Array.isArray(parsed.artifacts) ||
    parsed.artifacts.some(
      (artifact) =>
        typeof artifact !== "object" ||
        artifact === null ||
        typeof artifact.key !== "string" ||
        typeof artifact.hash !== "string" ||
        !Array.isArray(artifact.rows) ||
        !Array.isArray(artifact.columns),
    )
  ) {
    throw new Error("embedded table payload has an invalid structure");
  }
  return new Map(parsed.artifacts.map((artifact) => [artifact.key, artifact]));
}

function isNumericColumn(rows: readonly string[][], column: number): boolean {
  const observed = rows
    .map((row) => row[column]?.trim() ?? "")
    .filter((value) => value !== "")
    .slice(0, 200);
  return (
    observed.length > 0 &&
    observed.every((value) => /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?$/.test(value))
  );
}

function ensureViewerShell(): HTMLDialogElement | null {
  const existing = document.querySelector<HTMLDialogElement>("[data-artifact-viewer]");
  if (existing !== null) return existing;
  if (document.querySelector("[data-artifact-view]") === null) return null;
  document.body.insertAdjacentHTML("beforeend", artifactViewerShell);
  return document.querySelector<HTMLDialogElement>("[data-artifact-viewer]");
}

export function enhanceArtifactViewer(): void {
  const viewer = ensureViewerShell();
  if (viewer === null) return;
  const dialog = viewer;
  const title = required<HTMLElement>(viewer, "[data-artifact-title]");
  const description = required<HTMLElement>(viewer, "[data-artifact-description]");
  const metadata = required<HTMLDListElement>(viewer, "[data-artifact-metadata]");
  const status = required<HTMLElement>(viewer, "[data-artifact-status]");
  const preview = required<HTMLElement>(viewer, "[data-artifact-preview]");
  const search = required<HTMLInputElement>(viewer, "[data-artifact-search]");
  const pageSize = required<HTMLSelectElement>(viewer, "[data-artifact-page-size]");
  const tableRegion = required<HTMLElement>(viewer, "[data-artifact-table-region]");
  const caption = required<HTMLTableCaptionElement>(viewer, "[data-artifact-caption]");
  const head = required<HTMLTableSectionElement>(viewer, "[data-artifact-head]");
  const body = required<HTMLTableSectionElement>(viewer, "[data-artifact-body]");
  const range = required<HTMLElement>(viewer, "[data-artifact-range]");
  const previous = required<HTMLButtonElement>(viewer, "[data-artifact-previous]");
  const next = required<HTMLButtonElement>(viewer, "[data-artifact-next]");
  const download = required<HTMLAnchorElement>(viewer, "[data-artifact-download]");
  const fullPage = required<HTMLAnchorElement>(viewer, "[data-artifact-full-page]");
  const copy = required<HTMLButtonElement>(viewer, "[data-artifact-copy]");
  const close = required<HTMLButtonElement>(viewer, "[data-artifact-close]");
  const cache = new Map<string, ArtifactData>();
  let embeddedPayload: Promise<Map<string, ArtifactData>> | null = null;
  let active: ArtifactData | null = null;
  let activeTrigger: ArtifactTrigger | null = null;
  let filteredRows: string[][] = [];
  let numericColumns: boolean[] = [];
  let page = 0;
  let sort: SortState = null;
  let suppressHistory = false;
  let shareUrl = "";

  function setLoading(loading: boolean): void {
    search.disabled = loading;
    pageSize.disabled = loading;
    previous.disabled = loading;
    next.disabled = loading;
    copy.disabled = loading;
    dialog.toggleAttribute("aria-busy", loading);
  }

  function renderMetadata(artifact: ArtifactData): void {
    metadata.replaceChildren();
    const declaredUnits = artifact.columns
      .filter((column) => column.units !== undefined)
      .map((column) => `${column.label}: ${column.units}`)
      .join("; ");
    const values: Array<[string, string]> = [
      ["Rows", artifact.rowCount.toLocaleString("en-US")],
      ["Columns", artifact.columns.length.toLocaleString("en-US")],
      ["Units", declaredUnits || "No units declared"],
      ["Evidence / provenance class", artifact.sourceClass],
      ["Freshness", artifact.freshness],
      ["Source path", artifact.path],
      ["Source manifest", artifact.sourceManifest],
      ["SHA-256", artifact.hash],
    ];
    for (const [term, value] of values) {
      const wrapper = document.createElement("div");
      const name = document.createElement("dt");
      const detail = document.createElement("dd");
      name.textContent = term;
      detail.textContent = value;
      wrapper.append(name, detail);
      metadata.append(wrapper);
    }
  }

  function compareRows(left: string[], right: string[], state: NonNullable<SortState>): number {
    const leftValue = left[state.column] ?? "";
    const rightValue = right[state.column] ?? "";
    if (leftValue === "" && rightValue !== "") return 1;
    if (rightValue === "" && leftValue !== "") return -1;
    const leftComparable = comparable(leftValue);
    const rightComparable = comparable(rightValue);
    const comparison =
      typeof leftComparable === "number" && typeof rightComparable === "number"
        ? leftComparable - rightComparable
        : String(leftComparable).localeCompare(String(rightComparable), undefined, {
            numeric: true,
          });
    return state.direction === "asc" ? comparison : -comparison;
  }

  function renderHead(): void {
    head.replaceChildren();
    if (active === null) return;
    const firstKey = active.columns.findIndex((column) => column.key);
    const row = document.createElement("tr");
    for (const [index, column] of active.columns.entries()) {
      const cell = document.createElement("th");
      cell.scope = "col";
      if (index === firstKey) cell.classList.add("artifact-key-column");
      if (numericColumns[index]) cell.classList.add("artifact-numeric");
      const button = document.createElement("button");
      button.type = "button";
      button.className = "artifact-sort";
      button.textContent = column.units ? `${column.label} (${column.units})` : column.label;
      if (column.description) button.title = column.description;
      button.addEventListener("click", () => {
        sort =
          sort?.column === index
            ? { column: index, direction: sort.direction === "asc" ? "desc" : "asc" }
            : { column: index, direction: "asc" };
        page = 0;
        render();
      });
      if (sort?.column === index) {
        cell.setAttribute("aria-sort", sort.direction === "asc" ? "ascending" : "descending");
        button.dataset.direction = sort.direction;
      }
      cell.append(button);
      row.append(cell);
    }
    head.append(row);
  }

  function filterAndSort(): void {
    if (active === null) {
      filteredRows = [];
      return;
    }
    const query = search.value.trim().toLocaleLowerCase();
    filteredRows =
      query === ""
        ? [...active.rows]
        : active.rows.filter((row) =>
            row.some((value) => value.toLocaleLowerCase().includes(query)),
          );
    const sortState = sort;
    if (sortState !== null) {
      filteredRows.sort((left, right) => compareRows(left, right, sortState));
    }
  }

  function render(): void {
    filterAndSort();
    renderHead();
    body.replaceChildren();
    const size = Number(pageSize.value);
    const pageCount = Math.max(1, Math.ceil(filteredRows.length / size));
    page = Math.min(page, pageCount - 1);
    const start = page * size;
    const end = Math.min(start + size, filteredRows.length);
    const firstKey = active?.columns.findIndex((column) => column.key) ?? -1;
    for (const row of filteredRows.slice(start, end)) {
      const tableRow = document.createElement("tr");
      for (const [index, value] of row.entries()) {
        const cell =
          index === firstKey ? document.createElement("th") : document.createElement("td");
        if (cell instanceof HTMLTableCellElement && index === firstKey) {
          cell.scope = "row";
          cell.classList.add("artifact-key-column");
        }
        if (numericColumns[index]) cell.classList.add("artifact-numeric");
        if (value === "") {
          const missing = document.createElement("span");
          missing.className = "artifact-missing";
          missing.setAttribute("aria-label", "Missing value");
          missing.textContent = "—";
          cell.append(missing);
        } else {
          cell.textContent = value;
        }
        tableRow.append(cell);
      }
      body.append(tableRow);
    }
    previous.disabled = page === 0;
    next.disabled = page >= pageCount - 1;
    const qualifier = active?.complete === false ? " preview" : "";
    range.textContent =
      filteredRows.length === 0
        ? `No matching${qualifier} rows`
        : `Rows ${start + 1}–${end} of ${filteredRows.length.toLocaleString("en-US")}${qualifier}`;
    const loaded = active?.rows.length ?? 0;
    const total = active?.rowCount ?? 0;
    const scope = active?.complete
      ? `${total.toLocaleString("en-US")} rows loaded.`
      : `${loaded.toLocaleString("en-US")} preview rows loaded from ${total.toLocaleString(
          "en-US",
        )} total rows.`;
    status.textContent =
      filteredRows.length === loaded
        ? scope
        : `${filteredRows.length.toLocaleString("en-US")} of ${loaded.toLocaleString(
            "en-US",
          )} ${active?.complete ? "rows" : "preview rows"} match.`;
  }

  async function resolveArtifact(trigger: ArtifactTrigger): Promise<ArtifactData> {
    const metadataUrl = trigger.dataset.artifactJson;
    const artifactKey = trigger.dataset.artifactKey;
    const expectedHash = trigger.dataset.artifactHash;
    if (!artifactKey || !expectedHash) throw new Error("table reference is incomplete");
    const cacheKey = metadataUrl ?? `embedded:${artifactKey}`;
    let artifact = cache.get(cacheKey);
    if (artifact === undefined) {
      if (metadataUrl !== undefined) {
        const response = await fetch(metadataUrl);
        if (!response.ok) throw new Error(`table service returned HTTP ${response.status}`);
        artifact = (await response.json()) as ArtifactData;
      } else {
        embeddedPayload ??= decodeEmbeddedPayload();
        artifact = (await embeddedPayload).get(artifactKey);
        if (artifact === undefined) throw new Error("table is absent from the offline payload");
      }
      if (
        artifact.key !== artifactKey ||
        artifact.hash !== expectedHash ||
        artifact.path !== trigger.dataset.artifact
      ) {
        throw new Error("table payload does not match its manifest reference");
      }
      cache.set(cacheKey, artifact);
    }
    return artifact;
  }

  async function load(trigger: ArtifactTrigger, updateHistory = true): Promise<void> {
    const artifactKey = trigger.dataset.artifactKey;
    if (!artifactKey) return;
    activeTrigger = trigger;
    setLoading(true);
    status.textContent = "Loading table…";
    preview.hidden = true;
    if (!dialog.open) dialog.showModal();
    close.focus();
    const downloadUrl = trigger.dataset.artifactDownload ?? "";
    const fullPageUrl = trigger.dataset.artifactFullPage ?? "";
    download.href = downloadUrl;
    download.setAttribute(
      "aria-label",
      trigger.dataset.artifactDownloadLabel ?? "Download original CSV",
    );
    fullPage.href = fullPageUrl;
    shareUrl = new URL(fullPageUrl || `#view-${artifactKey}`, document.baseURI).href;
    try {
      const artifact = await resolveArtifact(trigger);
      active = artifact;
      title.textContent = artifact.title;
      description.textContent = artifact.description;
      caption.textContent = artifact.title;
      tableRegion.setAttribute("aria-label", `${artifact.title}: scrollable data table`);
      renderMetadata(artifact);
      preview.hidden = artifact.complete;
      preview.textContent = artifact.complete
        ? ""
        : `Preview: first ${artifact.rows.length.toLocaleString(
            "en-US",
          )} of ${artifact.rowCount.toLocaleString(
            "en-US",
          )} rows. Search, sorting, and page counts cover only this preview.`;
      search.value = "";
      page = 0;
      numericColumns = artifact.columns.map((_column, index) =>
        isNumericColumn(artifact.rows, index),
      );
      const defaultColumn = artifact.defaultSort
        ? artifact.columns.findIndex(({ name }) => name === artifact.defaultSort?.column)
        : -1;
      sort =
        defaultColumn >= 0 && artifact.defaultSort
          ? { column: defaultColumn, direction: artifact.defaultSort.direction }
          : null;
      render();
      if (updateHistory) {
        history.pushState({ artifact: artifactKey }, "", `#view-${artifactKey}`);
      }
    } catch (error) {
      active = null;
      head.replaceChildren();
      body.replaceChildren();
      range.textContent = "";
      preview.hidden = true;
      status.textContent = `Table could not be loaded: ${
        error instanceof Error ? error.message : String(error)
      }. Use Download original CSV if you need the source data.`;
    } finally {
      setLoading(false);
    }
  }

  for (const trigger of document.querySelectorAll<ArtifactTrigger>("[data-artifact-view]")) {
    trigger.addEventListener("click", () => void load(trigger));
  }
  search.addEventListener("input", () => {
    page = 0;
    render();
  });
  pageSize.addEventListener("change", () => {
    page = 0;
    render();
  });
  previous.addEventListener("click", () => {
    page = Math.max(0, page - 1);
    render();
  });
  next.addEventListener("click", () => {
    page += 1;
    render();
  });
  close.addEventListener("click", () => dialog.close());
  copy.addEventListener("click", async () => {
    try {
      await copyText(shareUrl);
      status.textContent = "Table link copied.";
    } catch {
      status.textContent = `Copy failed. Table link: ${shareUrl}`;
    }
  });
  dialog.addEventListener("close", () => {
    activeTrigger?.focus();
    if (!suppressHistory && history.state?.artifact) history.back();
    suppressHistory = false;
  });

  function openFragment(): boolean {
    const key = decodeURIComponent(location.hash).replace(/^#view-/, "");
    if (!location.hash.startsWith("#view-") || !key) return false;
    const trigger = document.querySelector<ArtifactTrigger>(
      `[data-artifact-view][data-artifact-key="${CSS.escape(key)}"]`,
    );
    if (trigger === null) return false;
    if (!(dialog.open && active?.key === key)) void load(trigger, false);
    return true;
  }

  window.addEventListener("popstate", () => {
    if (openFragment() || !dialog.open) return;
    suppressHistory = true;
    dialog.close();
  });
  window.addEventListener("hashchange", openFragment);
  openFragment();
}
