# -*- coding: utf-8 -*-
"""Regenerate ClaudeU/README.md from the content modules that exist."""
import os
import sys
import io

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "content"))

# (semester, content-module, code, title)
PLAN = [
    # Semester 0 is the two program prerequisites, not part of the degree.
    (0, "ucmath600", "UC MATH 600", "Mathematics for Computer Science"),
    (0, "uclina600", "UC LINA 600", "Linear Algebra for Graphics"),
    (1, "csce629", "CSCE 629", "Analysis of Algorithms"),
    (1, "csce641", "CSCE 641", "Computer Graphics"),
    (1, "csce614", "CSCE 614", "Computer Architecture"),
    (2, "csce611", "CSCE 611", "Operating Systems"),
    (2, "csce645", "CSCE 645", "Geometric Modeling"),
    (2, "csce606", "CSCE 606", "Software Engineering"),
    (3, "csce647", "CSCE 647", "Image Synthesis"),
    (3, "csce649", "CSCE 649", "Physically-Based Modeling"),
    (3, "csce608", "CSCE 608", "Database Systems"),
    (4, "csce650", "CSCE 650", "Virtual Reality"),
    (4, "csce748", "CSCE 748", "Computational Photography"),
    (4, "csce735", "CSCE 735", "Parallel Computing"),
    # Semester 5 is a post-degree continuation, not part of the 12-course MS.
    (5, "csce620", "CSCE 620", "Computational Geometry"),
    (5, "csce605", "CSCE 605", "Compiler Design"),
    (5, "csce678", "CSCE 678", "Distributed Systems and Cloud Computing"),
    (6, "csce633", "CSCE 633", "Machine Learning"),
    (6, "csce636", "CSCE 636", "Deep Learning"),
    (6, "csce669", "CSCE 669", "Computational Optimization"),
    (7, "csce753", "CSCE 753", "Computer Vision"),
    (7, "csce625", "CSCE 625", "Artificial Intelligence"),
    (7, "csce642", "CSCE 642", "Deep Reinforcement Learning"),
    (8, "csce627", "CSCE 627", "Theory of Computability"),
    (8, "csce637", "CSCE 637", "Complexity Theory"),
    (8, "csce658", "CSCE 658", "Randomized Algorithms"),
    (9, "csce701", "CSCE 701", "Cybersecurity"),
    (9, "csce711", "CSCE 711", "Applied Cryptography"),
    (9, "csce713", "CSCE 713", "Software Security"),
    (10, "csce638", "CSCE 638", "Natural Language Processing"),
    (10, "csce676", "CSCE 676", "Data Mining"),
    (10, "csce670", "CSCE 670", "Information Retrieval"),
    (11, "csce671", "CSCE 671", "Human-Computer Interaction"),
    (11, "csce679", "CSCE 679", "Data Visualization"),
    (11, "csce632", "CSCE 632", "Accessible Computing"),
    (12, "csce640", "CSCE 640", "Quantum Algorithms"),
    (12, "csce628", "CSCE 628", "Computational Biology"),
    (12, "csce717", "CSCE 717", "Algorithmic Game Theory"),
    # --- Semesters 13-24: the remainder of the catalog ---------------------
    (13, "csce631", "CSCE 631", "Intelligent Agents"),
    (13, "csce635", "CSCE 635", "AI Robotics"),
    (13, "csce752", "CSCE 752", "Robotics and Spatial Intelligence"),
    (14, "csce626", "CSCE 626", "Parallel Algorithm Design and Analysis"),
    (14, "csce654", "CSCE 654", "Supercomputing"),
    (14, "csce653", "CSCE 653", "Computer Methods in Applied Sciences"),
    (15, "csce662", "CSCE 662", "Distributed Processing Systems"),
    (15, "csce668", "CSCE 668", "Distributed Algorithms and Systems"),
    (15, "csce664", "CSCE 664", "Wireless and Mobile Systems"),
    (16, "csce612", "CSCE 612", "Applied Networks and Distributed Processing"),
    (16, "csce765", "CSCE 765", "Network Security"),
    (16, "csce665", "CSCE 665", "Advanced Networking and Security"),
    (17, "csce666", "CSCE 666", "Pattern Analysis"),
    (17, "csce630", "CSCE 630", "Speech Processing"),
    (17, "csce634", "CSCE 634", "Intelligent User Interfaces"),
    (18, "csce727", "CSCE 727", "Algorithmic Foundations of Big Data"),
    (18, "csce726", "CSCE 726", "Large-Scale Optimization for Machine Learning"),
    (18, "csce603", "CSCE 603", "Database Systems and Applications"),
    (19, "csce616", "CSCE 616", "Hardware Design Verification"),
    (19, "csce714", "CSCE 714", "Advanced Functional Verification"),
    (19, "csce680", "CSCE 680", "Testing and Diagnosis of Digital Systems"),
    (20, "csce624", "CSCE 624", "Sketch Recognition"),
    (20, "csce648", "CSCE 648", "Computer Aided Sculpting"),
    (20, "csce743", "CSCE 743", "Digital Fabrication Studio"),
    (21, "csce646", "CSCE 646", "Digital Image"),
    (21, "csce656", "CSCE 656", "Computers and New Media"),
    (21, "csce672", "CSCE 672", "Computer Supported Collaborative Work"),
    (22, "csce749", "CSCE 749", "Cryptographic Engineering"),
    (22, "csce715", "CSCE 715", "Secure Authentication Systems"),
    (22, "csce716", "CSCE 716", "Foundations and Applications of Blockchains"),
    (23, "csce652", "CSCE 652", "Software Reverse Engineering"),
    (23, "csce712", "CSCE 712", "Digital Forensic Engineering"),
    (23, "csce704", "CSCE 704", "Data Analytics for Cybersecurity"),
    (24, "csce702", "CSCE 702", "Law and Policy in Cybersecurity"),
    (24, "csce703", "CSCE 703", "Cybersecurity Risk"),
    (24, "csce655", "CSCE 655", "Human-Centered Computing"),
]


# NOTE: must match make_course.slug() exactly, or every generated link 404s.
from make_course import slug


def load(pkg):
    try:
        m = __import__(pkg)
    except ImportError:
        return None
    return m


# Set once the site is deployed; the README then links it. No trailing slash.
SITE = ""


def main():
    built = []
    for sem, pkg, code, title in PLAN:
        m = load(pkg)
        if m is None:
            built.append((sem, pkg, code, title, None))
            continue
        d = "Courses/%s-%s" % (code.replace(" ", ""), slug(title))
        if not os.path.isdir(os.path.join(ROOT, d)):
            built.append((sem, pkg, code, title, None))
            continue
        built.append((sem, pkg, code, title, (m, d)))

    done = [b for b in built if b[4]]
    n_mod = sum(len(b[4][0].MODULES) for b in done)
    n_sl = sum(len(x["slides"]) + 3 for b in done for x in b[4][0].MODULES)
    n_ex = sum(len(x["exercises"]) for b in done for x in b[4][0].MODULES)
    n_rs = sum(len(x["resources"]) for b in done for x in b[4][0].MODULES)

    o = io.StringIO()
    w = o.write

    w("# University of Claude\n\n")
    w("**MS in Computer Science — Graphics & Game Engines track.**\n")
    w("A complete graduate curriculum with original lecture materials, "
      "mapped onto free university courseware.\n\n")
    w("Not an accredited institution. No degree, transcript, or credential "
      "is awarded.\n")
    w("Everything written for this program is original and free to copy, "
      "adapt, and redistribute.\n")
    w("External courses are linked, never reproduced, and remain under "
      "their own licences.\n\n---\n\n")

    w("## Start here\n\n")
    w("1. **[Program Handbook](00_Program/UC-MSCS-Program-Handbook.pdf)** "
      "— the degree: structure, prerequisites, four-semester sequence, "
      "assessment standard.\n")
    w("2. **[Continuation Record](00_Program/UC-Continuation-Record.pdf)** "
      "— Semesters 5–12: the twenty-four post-degree courses, and what "
      "each semester's three courses converge on.\n")
    w("3. **[Free-Resource Catalog](00_Program/Free-Resource-Catalog.pdf)** "
      "— all 84 courses mapped to 268 free resources.\n")
    w("4. **Any completed course below** — start with its syllabus, "
      "then work the modules in order.\n\n")
    w("Or run the study app, which indexes everything built, tracks which "
      "modules you have finished, keeps your notes, and opens the decks "
      "and lecture notes for you:\n\n")
    w("```bash\npython _app/server.py\n```\n\n")
    if SITE:
        w("The same app is hosted at **<%s>** — everything there is "
          "readable and downloadable, and your progress is kept in your "
          "own browser.\n\n" % SITE)
    w("See [_app/README.md](_app/README.md). It reads whatever is built, "
      "so new courses appear without changing the app.\n\n")

    w("## Progress\n\n")
    # The MS is the 12 courses of S1-S4; S5 onward is a continuation, so
    # report the degree separately rather than diluting it into one ratio.
    deg = [b for b in PLAN if 1 <= b[0] <= 4]
    deg_done = [b for b in done if 1 <= b[0] <= 4]
    ext_done = [b for b in done if b[0] > 4]
    pre_done = [b for b in done if b[0] == 0]
    w("**The %d-course MS is complete** (%d of %d). "
      % (len(deg), len(deg_done), len(deg)))
    if pre_done:
        w("%d prerequisite course%s sit%s before Semester 1. "
          % (len(pre_done), "" if len(pre_done) == 1 else "s",
             "s" if len(pre_done) == 1 else ""))
    if ext_done:
        w("Semester %d onward is a post-degree continuation, "
          "with %d course%s built so far."
          % (min(b[0] for b in ext_done), len(ext_done),
             "" if len(ext_done) == 1 else "s"))
    w("\n\nAcross everything: %d modules, %d slides, %d written "
      "exercises, %d linked free resources.\n\n"
      % (n_mod, n_sl, n_ex, n_rs))
    w("| Sem | Course | Status |\n|---|---|---|\n")
    for sem, pkg, code, title, got in built:
        if got:
            m, d = got
            w("| S%d | **[%s %s](%s/)** | ✅ complete — %d modules |\n"
              % (sem, code, title, d, len(m.MODULES)))
        else:
            w("| S%d | %s %s | not yet built |\n" % (sem, code, title))
    # Once every course is built, nothing remains to be "not blocked".
    if len(done) < len(PLAN):
        w("\nThe [Free-Resource Catalog](00_Program/Free-Resource-Catalog.pdf) "
          "already covers every remaining course with free lectures, books, "
          "and problem sets, so none of them are blocked.\n\n")
    else:
        w("\nEvery planned course is built. The degree is Semesters 1–4; "
          "the [Continuation Record](00_Program/UC-Continuation-Record.pdf) "
          "covers Semesters 5–12 and what each semester's three courses "
          "converge on. The "
          "[Free-Resource Catalog](00_Program/Free-Resource-Catalog.pdf) maps "
          "the wider catalog, so any further course can be built the same "
          "way.\n\n")

    w("## What each course contains\n\n")
    w("- `Syllabus.pdf` — outcomes, 13-module schedule, two projects, "
      "assessment standard\n")
    w("- `Resource-Map.pdf` — module-by-module mapping onto free "
      "university courseware\n")
    w("- `Slides/M01…M13.pptx` — one editable deck per module, "
      "with speaker notes\n")
    w("- `Notes/M01…M13.pdf` — dense written treatment: "
      "derivations, code, exercises, self-check\n\n")

    w("## Completed courses\n")
    cur = 0
    for sem, pkg, code, title, got in built:
        if not got:
            continue
        m, d = got
        if sem != cur:
            cur = sem
            w("\n## Semester %d\n" % sem)
        w("\n### %s — %s\n\n" % (code, title))
        w("*%s.*\n\n" % m.COURSE.get("tagline", "").rstrip("."))
        w("[Syllabus](%s/Syllabus.pdf) · [Resource Map](%s/Resource-Map.pdf)\n\n"
          % (d, d))
        w("| # | Module | Slides | Notes |\n|---|---|---|---|\n")
        for x in m.MODULES:
            s = slug(x["title"])
            w("| %02d | %s | [pptx](%s/Slides/M%02d-%s.pptx) | "
              "[pdf](%s/Notes/M%02d-%s.pdf) |\n"
              % (x["n"], x["title"], d, x["n"], s, d, x["n"], s))

    w("\n## Rebuilding\n\n```bash\n")
    w("cd _build\npython make_program.py\n")
    for sem, pkg, code, title, got in built:
        if got:
            w("python make_course.py %s\n" % pkg)
    w("python make_readme.py\n```\n\n")
    w("- `_build/uc.py` — theme and document engine (PPTX + PDF)\n")
    w("- `_build/make_course.py` — generic course builder; takes a "
      "content module name\n")
    w("- `_build/make_readme.py` — regenerates this file from whatever "
      "has been built\n")
    w("- `_build/content/` — course content, one file per course plus "
      "module batches\n")
    w("- `_build/preview.py` — renders any deck or PDF to PNG for "
      "review\n")
    w("- `_build/lint_slides.py` — scans every built deck for HTML entities "
      "the slide renderer cannot decode\n")
    w("- `_build/lint_markup.py` — scans all course content for unbalanced "
      "inline markup, which the renderers catch only by luck\n")

    w("---\n\n## Licence\n\n")
    w("| What | Licence |\n|---|---|\n")
    w("| Course material — `Courses/`, `00_Program/`, "
      "`_build/content/`, this README | [CC BY 4.0](LICENSE-CONTENT) |\n")
    w("| Build toolchain and study app — `_build/*.py`, `_app/` | "
      "[MIT](LICENSE) |\n")
    w("| The external courses, books and papers linked throughout | "
      "**their own authors' licences** |\n\n")
    w("You may copy, adapt and redistribute the material, commercially "
      "too, with credit. That is **not** permission for the third-party "
      "works this program links to: those are only ever linked and "
      "commented on here, never reproduced.\n\n")
    w("This program is not accredited and awards no degree, transcript "
      "or credential. The licence lets you copy the material; it cannot "
      "make it a qualification.\n\n")

    p = os.path.join(ROOT, "README.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(o.getvalue())
    print(p)
    print("%d of %d courses, %d modules, %d slides, %d exercises"
          % (len(done), len(PLAN), n_mod, n_sl, n_ex))

    # Every local link must resolve. A slug mismatch between this file and
    # make_course.py once silently produced 200+ dead links.
    import re
    bad, tot = [], 0
    for m in re.finditer(r"\]\(([^)]+)\)", o.getvalue()):
        target = m.group(1)
        if target.startswith("http"):
            continue
        tot += 1
        if not os.path.exists(os.path.join(ROOT, target.split("#")[0])):
            bad.append(target)
    print("%d local links, %d broken" % (tot, len(bad)))
    for b in bad:
        print("  MISSING:", b)


if __name__ == "__main__":
    main()
