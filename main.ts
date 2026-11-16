// Entrypoint for "I Knitted You an Octopus" (make.fun ai-excited-01).
//
// The graded program is deliberately tiny: generate.py already produced
// the final 1024x1024 image as entry.png, so all this does is copy that
// file byte-for-byte into the output directory the harness asks for.
// No resize, no re-encode, no transformation of any kind — the image the
// judge sees is exactly the image generate.py wrote, and two runs of
// this program therefore write identical bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync("entry.png", join(outDir, "entry.png"));
