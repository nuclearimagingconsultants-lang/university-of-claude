/* Assemble public/ for a static host (Vercel runs this).

   Nothing is generated here: the decks, notes and program.json are already
   built by the Python toolchain and committed. This only gathers them into
   one directory and flips the app into static mode, so the site is a plain
   copy of the repository's output with no server behind it. */

import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync,
         readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const APP = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(APP, "..");
const OUT = join(REPO, "public");

const need = (p, what) => {
  if (!existsSync(p)) {
    console.error(`\n  missing ${what}: ${p}`);
    console.error("  run the Python build first (see _build/README.md)\n");
    process.exit(1);
  }
  return p;
};

const INDEX = need(join(APP, "data", "program.json"), "program index");
need(join(REPO, "Courses"), "course artifacts");

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

// The app itself.
cpSync(join(APP, "static"), OUT, { recursive: true });

// The index it reads. progress.json is deliberately NOT copied: on a static
// host progress lives in each visitor's own browser.
mkdirSync(join(OUT, "data"), { recursive: true });
cpSync(INDEX, join(OUT, "data", "program.json"));

// The material.
cpSync(join(REPO, "Courses"), join(OUT, "Courses"), { recursive: true });
if (existsSync(join(REPO, "00_Program"))) {
  cpSync(join(REPO, "00_Program"), join(OUT, "00_Program"), { recursive: true });
}
for (const f of ["LICENSE", "LICENSE-CONTENT", "README.md"]) {
  if (existsSync(join(REPO, f))) cpSync(join(REPO, f), join(OUT, f));
}

// Flip the app into static mode. app.js reads window.UC_STATIC and switches
// to data/program.json, localStorage, and plain links.
const page = join(OUT, "index.html");
const html = readFileSync(page, "utf8");
const anchor = '<script src="app.js"></script>';
if (!html.includes(anchor)) {
  console.error(`\n  could not find ${anchor} in index.html\n`);
  process.exit(1);
}
writeFileSync(page, html.replace(
  anchor, '<script>window.UC_STATIC = true;</script>\n' + anchor), "utf8");

// Report, so a failed copy is visible in the build log rather than silent.
let files = 0, bytes = 0;
(function walk(d) {
  for (const e of readdirSync(d, { withFileTypes: true })) {
    const p = join(d, e.name);
    if (e.isDirectory()) walk(p); else { files++; bytes += statSync(p).size; }
  }
})(OUT);
const { stats } = JSON.parse(readFileSync(INDEX, "utf8"));
console.log(`  public/  ${files} files, ${(bytes / 1048576).toFixed(1)} MB`);
console.log(`  index    ${stats.courses_built} courses, ${stats.modules} modules`);
if (bytes > 95 * 1048576) {
  console.warn("  WARNING: over 95 MB, near Vercel Hobby's 100 MB static cap");
}
