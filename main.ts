// news-image-20261119 final entry (Node 22, standard library only).
//
// The image is entry.png in this repository, composed by
// compose_final.py from illustration assets in assets/ plus text
// rendered from verified news strings (see STORIES.md). This program
// writes that image to the grader's output directory (/output, or
// MAKEFUN_OUTPUT_DIR locally). It runs twice in grading; both runs
// write the same bytes because the source file never changes.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, "entry.png"));
writeFileSync(join(outDir, "entry.png"), bytes);
