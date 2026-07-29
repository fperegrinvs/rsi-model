import path from "node:path";

import { type Rollup, build as viteBuild } from "vite";

import { root } from "./manuscript-config.ts";

export interface InlineViewerBundle {
  css: string;
  javascript: string;
}

export async function buildInlineViewer(): Promise<InlineViewerBundle> {
  const result = await viteBuild({
    configFile: false,
    logLevel: "silent",
    publicDir: false,
    root,
    build: {
      cssCodeSplit: false,
      emptyOutDir: false,
      minify: true,
      rollupOptions: {
        input: path.join(root, "web", "standalone.ts"),
        output: {
          format: "iife",
        },
      },
      target: "es2022",
      write: false,
    },
  });
  const builds = Array.isArray(result) ? result : [result];
  const outputs: Array<Rollup.OutputChunk | Rollup.OutputAsset> = [];
  for (const build of builds) {
    if (!("output" in build)) throw new Error("Vite unexpectedly entered watch mode");
    outputs.push(...build.output);
  }
  const chunk = outputs.find(
    (item): item is Rollup.OutputChunk => item.type === "chunk" && item.isEntry,
  );
  const style = outputs.find(
    (item): item is Rollup.OutputAsset =>
      item.type === "asset" && item.fileName.toLocaleLowerCase().endsWith(".css"),
  );
  if (chunk === undefined || style === undefined) {
    throw new Error("Vite did not produce the standalone viewer JavaScript and CSS");
  }
  return {
    javascript: chunk.code,
    css: typeof style.source === "string" ? style.source : new TextDecoder().decode(style.source),
  };
}
