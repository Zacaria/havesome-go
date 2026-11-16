import { defineConfig } from "vite-plus";
import tailwindcss from "@tailwindcss/vite";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

export default defineConfig({
  plugins: [
    tailwindcss(),
    {
      name: "copy-playground-and-licenses",
      generateBundle() {
        for (const file of [
          "worker.js",
          "wasm_exec.js",
          "engine.wasm",
          "licenses/GO-LICENSE.txt",
          "licenses/YAEGI-LICENSE.txt",
        ]) {
          this.emitFile({ type: "asset", fileName: file, source: readFileSync(resolve(file)) });
        }
      },
    },
  ],
  build: {
    rollupOptions: { input: { index: resolve("index.html"), fiche: resolve("fiche.html") } },
  },
});
