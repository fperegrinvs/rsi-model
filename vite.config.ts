import path from "node:path";
import { fileURLToPath } from "node:url";

import { defineConfig } from "vite";

const root = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  root,
  publicDir: false,
  build: {
    emptyOutDir: true,
    manifest: "manifest.json",
    outDir: path.join(root, "_site", "assets", "rsi"),
    rollupOptions: {
      input: path.join(root, "web", "site.ts"),
    },
    sourcemap: true,
    target: "es2022",
  },
});
