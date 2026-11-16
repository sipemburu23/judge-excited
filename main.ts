// "I Knitted You an Octopus" — entrypoint.
//
// Copies entry.png (which lives next to this file) byte-for-byte to
// $MAKEFUN_OUTPUT_DIR/entry.png (default /output). No resize, no
// re-encode, no network.
//
// THE IMPORTANT BIT: entry.png is resolved from THIS FILE's own
// directory (import.meta.url), never from the current working
// directory. The grader runs `node /bot/main.ts` from some other
// working directory on a read-only filesystem, so a bare relative
// path like "entry.png" would not exist there and the run would
// crash with ENOENT. Resolving from the script location works
// from anywhere.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}`);
