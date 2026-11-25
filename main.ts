// news-image-20261125 — "The World Today": one image summing up
// Wednesday 25 November 2026 — 47 real stories from 7 regions, drawn
// as a newspaper front page.
//
// The image (entry.png, 1024x1024, 47 stories) is drawn in this repo by
// render.py (Python + Pillow + DejaVu, deterministic — running it twice
// writes byte-identical bytes). This program only copies that one file to
// the output directory and writes nothing else. After the copy it checks
// the output file exists, so a silent failure cannot pass as a success.
// Node 22, standard library only, no network, no randomness, no
// timestamps. It never deletes the output directory: the grader mounts
// /output, so removing it would fail the run.
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");
copyFileSync(join(repoDir, "entry.png"), outPath);
const size = statSync(outPath).size;
console.log(`wrote ${outPath} (${size} bytes)`);
