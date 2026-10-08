# The study app

A local study interface for the University of Claude curriculum. It lists
every built course, tracks which modules you have finished, keeps your
notes, and opens the slide decks and lecture notes in whatever application
already handles `.pptx` and `.pdf` on this machine.

## Running it

```bash
python _app/server.py
```

Or double-click `_app/start.cmd`. It opens a browser at
<http://127.0.0.1:8731/>.

The server binds to the loopback address only. Nothing is sent anywhere,
and there are no dependencies beyond the Python standard library.

## How it stays current

The app reads one file, `_app/data/program.json`, which is generated from
whatever is actually built:

```bash
python _build/make_index.py
```

So adding a course is the usual two commands plus one:

```bash
python _build/make_course.py csce631     # build the course
python _build/make_readme.py             # refresh the repository index
python _build/make_index.py              # refresh the app index
```

The **Reindex** button in the top right runs that last step for you.
Courses in the plan that have not been built yet appear greyed out in the
sidebar, so the app doubles as a progress view of the program itself.

## What it stores

`_app/data/progress.json`, which looks like this:

```json
{
 "modules": { "CSCE 679/9": "done", "CSCE 679/10": "doing" },
 "notes":   { "CSCE 679/9": "Quantile dotplots - try these on real data." }
}
```

Plain JSON, one entry per module, safe to edit by hand, and safe to delete
if you want to start over. It is the only file the app writes.

## Using it

- **Overview** shows where you are and a **Continue** card pointing at the
  first module you have not finished, in program order.
- **Click a module** to see its outcomes, what to carry forward, and the
  self-check questions — then open the deck and the notes beside them.
- **The status button cycles** none → in progress → done.
- **`/`** focuses the search box; **Escape** clears it. Search covers course
  titles, taglines, module titles, and the module questions.

## What it deliberately does not do

It does not display the course content itself. The slides and the notes are
the material, and they are PDFs and PowerPoint files meant to be read in a
real reader — this is the index, the progress record, and the launcher,
not a replacement for them.
