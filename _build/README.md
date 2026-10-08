# The build toolchain

Everything in `Courses/`, `00_Program/`, `README.md` and `_app/data/` is
generated. Nothing in those directories should be edited by hand — the next
build will overwrite it. The sources are `_build/content/*.py`.

## Writing a course

A course is a Python module exposing `COURSE` (a dict) and `MODULES` (a list
of 13 dicts). Because a single file that size is unwieldy, each course is
split into three:

```
content/csce679.py      COURSE + Module 01, and the import tail
content/c679_b2.py      Modules 02-07
content/c679_b3.py      Modules 08-13
```

The tail at the bottom of the main file stitches them together:

```python
for _b in ("c679_b2", "c679_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
```

Then register it in `make_readme.PLAN` as `(semester, pkg, code, title)`.

## Building

```bash
python make_course.py csce679     # one course: syllabus, resource map, 13 decks, 13 notes
python make_program.py            # handbook + free-resource catalog
python make_continuation.py       # the Semesters 5+ record (counts are computed)
python make_readme.py             # repository README, and checks every local link
python make_index.py              # _app/data/program.json for the study app
```

`make_course.py` prints `[OVERFLOW RISK]` when a code slide is too tall for
its box. **Split the slide; never shrink the font.** Keeping code slides to
22 lines or fewer means it never fires.

## Checking

```bash
python lint_markup.py             # unbalanced <b>/<i> in the sources
python lint_output.py             # leaked HTML entities in decks AND PDFs
python check_links.py             # live-check every external URL -> linkcheck.json
python archive_all.py --report    # archive-snapshot coverage
python apply_linkfix.py           # dry run; --write to rewrite dead URLs
```

`lint_output.py` supersedes `lint_slides.py`, which only ever scanned the
decks — which is how a batch of entity leaks survived in the notes PDFs.

## Things that bite

- **Slides take raw Unicode; notes take HTML entities.** `√` on a slide,
  `&radic;` in the notes. The deck engine decodes a fixed set; reportlab
  decodes the standard set. Mixing them up is what `lint_output.py` catches.
- **A bare `&` in prose is a bug.** Write `&amp;`. reportlab reads `ATT&CK`
  as an entity reference and emits `&CK;`. A bare `&` is safe inside a code
  block and safe when followed by a space.
- **Uppercasing must not touch entities.** Entity names are case-sensitive,
  so `"&times;".upper()` gives `&TIMES;`, which nothing decodes. All
  uppercasing goes through `uc._upper()`.
- **`&langle;`, `&rangle;` and `&#8214;` render as black boxes** in the PDF
  fonts. Use `E[...]` and `||...||`. ASCII `|0>` beats a ket glyph.
- **`eq` slides take `"eqs": [(line, gloss), ...]`**, not `eq` + `where`. In
  notes an equation is the single-string form `("eq", "...")`.
- **`make_readme.slug` must match `make_course.slug` exactly.** They diverged
  once and silently produced 200+ dead links; `make_readme.py` now verifies
  every local link it writes.
- **Counts in generated documents must be computed, not typed.** A hardcoded
  "thirty-six courses" in the continuation record went stale the moment two
  prerequisites were added.

## Link rot

External links are the part of this repository that decays on its own.
`check_links.py` live-checks every URL and records the result, plus the best
archive snapshot, in `linkcheck.json`. `archive_all.py` fills in a snapshot
for the *live* URLs too, so that when one dies later the replacement is
already recorded and `apply_linkfix.py --write` can apply it mechanically.

403 and 429 are recorded as `blocked`, not `dead` — those are bot
protection (Wiley, Intel, Microsoft Research, Scratchapixel all do it) and
the pages are fine in a browser.

Re-run `check_links.py` every few months; expect a few percent attrition
per year.

## The hosted site

`_app/` runs in two modes from the same `app.js`:

| | Local (`python _app/server.py`) | Static (the hosted site) |
|---|---|---|
| index | `/api/program` | `data/program.json` |
| progress | `_app/data/progress.json` | the visitor's `localStorage` |
| opening a deck | `os.startfile()` — real PowerPoint | an ordinary link |
| Reindex button | runs the Python build | hidden |

The switch is `window.UC_STATIC`, injected into `index.html` by the static
build. Nothing else differs, so a change to the app affects both.

```bash
npm run build      # assembles public/ : app + program.json + Courses/
```

`public/` is generated and gitignored; Vercel runs that command on deploy and
serves the result (`vercel.json`). Nothing is *built* there — the Python
toolchain has already produced everything, and `build.mjs` only gathers it and
flips the flag. **Rebuild the index before deploying** or the site ships a
stale `program.json`:

```bash
python _build/make_course.py <pkg>   # if content changed
python _build/make_readme.py
python _build/make_index.py          # <- the site reads this
npm run build
```

Watch the size. Vercel's Hobby tier caps static uploads at **100 MB**; the
build prints the total and warns past 95 MB. It was 40.8 MB at 38 courses,
so roughly 90 courses would reach the cap.

### Things that bite here too

- **`os.startfile()` is desktop-only.** It opens a file on the machine running
  the server. Hosted, it is meaningless — hence the static branch.
- **`progress.json` is never copied into `public/`.** On a static host there is
  no server to write it, and shipping it would publish your reading position
  to every visitor.
- **A free port is not a fixed port.** `server.py` falls back past 8731 when it
  is busy, so a local app left running from an earlier session can answer on
  the port you were about to test the static build on. Check before concluding
  the build is broken.
