# -*- coding: utf-8 -*-
"""
Generic course builder.

Takes a course content module (content/<pkg>.py exposing COURSE, MODULES)
and emits:
    Syllabus.pdf
    Resource-Map.pdf
    Slides/M<nn>-<slug>.pptx      (one per module)
    Notes/M<nn>-<slug>.pdf        (one per module)
"""
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "content"))

from uc import Deck, Doc, link

ROOT = r"C:\Users\csant\ClaudeU\Courses"


def slug(s):
    s = re.sub(r"[^A-Za-z0-9 ]+", "", s).strip()
    return re.sub(r"\s+", "-", s)[:46]


# --------------------------------------------------------------- slides
def build_deck(course, m, path):
    d = Deck(course["code"], course["title"],
             f"Module {m['n']:02d}", m["title"])
    d.title_slide(subtitle=m.get("subtitle"),
                  meta=f"{course['code']} \u00b7 Module {m['n']:02d} of "
                       f"{course['n_modules']} \u00b7 original material, "
                       f"share freely")

    # outcomes slide
    d.bullets("What you will be able to do",
              m["outcomes"], kicker="Module outcomes",
              note="State the outcomes before the content. Every slide that "
                   "follows exists to serve one of these.")

    for sl in m["slides"]:
        t = sl["t"]
        if t == "section":
            d.section(sl["label"], sl["title"], sl.get("blurb"))
        elif t == "bullets":
            d.bullets(sl["title"], sl["items"], kicker=sl.get("kicker"),
                      note=sl.get("note"), footnote=sl.get("footnote"))
        elif t == "two":
            d.two_col(sl["title"], sl["lh"], sl["l"], sl["rh"], sl["r"],
                      kicker=sl.get("kicker"), note=sl.get("note"))
        elif t == "code":
            d.code(sl["title"], sl["code"], lang=sl.get("lang"),
                   caption=sl.get("caption"), kicker=sl.get("kicker"),
                   note=sl.get("note"))
        elif t == "eq":
            d.equations(sl["title"], sl["eqs"], caption=sl.get("caption"),
                        kicker=sl.get("kicker"), note=sl.get("note"))
        elif t == "table":
            d.table(sl["title"], sl["header"], sl["rows"],
                    kicker=sl.get("kicker"), note=sl.get("note"),
                    widths=sl.get("widths"))
        elif t == "callout":
            d.callout(sl["title"], sl["body"], kind=sl.get("kind", "Key idea"),
                      kicker=sl.get("kicker"), note=sl.get("note"))
        else:
            raise ValueError(f"unknown slide type {t}")

    d.takeaways(m["takeaways"])
    return d.save(path)


# ---------------------------------------------------------------- notes
def build_notes(course, m, path):
    d = Doc(m["title"],
            m.get("subtitle"),
            course=f"{course['code']} \u00b7 Module {m['n']:02d}",
            kicker=f"{course['code']} {course['title'].upper()} \u00b7 "
                   f"MODULE {m['n']:02d} \u00b7 LECTURE NOTES")

    d.callout("Module outcomes", m["outcomes"])

    for b in m["notes"]:
        t = b[0]
        if t == "h1":
            d.h1(b[1])
        elif t == "h2":
            d.h2(b[1])
        elif t == "h3":
            d.h3(b[1])
        elif t == "p":
            d.p(b[1])
        elif t == "ul":
            d.bullets(b[1])
        elif t == "ol":
            d.bullets(b[1], numbered=True)
        elif t == "code":
            d.code(b[1], b[2] if len(b) > 2 else None)
        elif t == "eq":
            d.eq(b[1])
        elif t == "cap":
            d.cap(b[1])
        elif t == "callout":
            d.callout(b[1], b[2])
        elif t == "table":
            d.table(b[1], b[2], widths=b[3] if len(b) > 3 else None,
                    caption=b[4] if len(b) > 4 else None)
        elif t == "break":
            d.pagebreak()
        else:
            raise ValueError(f"unknown note block {t}")

    if m.get("resources"):
        d.h1("Where to see this taught differently")
        d.p("Original material only goes so far \u2014 hearing the same idea "
            "in another voice is how it sticks. These are free, and they "
            "cover this module specifically.")
        d.table(["Resource", "What it covers for this module"],
                [[link(u, lbl), what] for lbl, u, what in m["resources"]],
                widths=[0.37, 0.63])

    if m.get("exercises"):
        d.h1("Exercises")
        d.p("Do these in code, not on paper, unless the exercise says "
            "otherwise. The module is not finished until they run.")
        d.bullets(m["exercises"], numbered=True)

    if m.get("selfcheck"):
        d.h1("Self-check")
        d.p("Answer these in writing, from memory, without looking back at "
            "the notes. If you cannot, you have read this module but not yet "
            "learned it \u2014 that is useful information, not a failure.")
        d.bullets(m["selfcheck"], numbered=True)

    return d.save(path)


# ------------------------------------------------------------- syllabus
def build_syllabus(course, modules, outdir):
    d = Doc(f"{course['code']} \u2014 {course['title']}",
            course.get("tagline"),
            course=f"{course['code']} Syllabus",
            kicker="UNIVERSITY OF CLAUDE \u00b7 COURSE SYLLABUS")

    d.callout("At a glance", [
        f"<b>Credits:</b> 3 credit-equivalents &nbsp;&middot;&nbsp; "
        f"<b>Modules:</b> {len(modules)} &nbsp;&middot;&nbsp; "
        f"<b>Term:</b> {course['term']}",
        f"<b>Prerequisites:</b> {course['prereqs']}",
        f"<b>Effort:</b> {course['effort']}",
        f"<b>Deliverable:</b> {course['deliverable']}",
    ])

    d.h1("Course description")
    for para in course["description"]:
        d.p(para)

    d.h1("Learning outcomes")
    d.p("On finishing this course you should be able to do the following "
        "without reference material.")
    d.bullets(course["outcomes"], numbered=True)

    d.h1("Module schedule")
    d.p("One module per week for thirteen weeks, then two weeks for the "
        "final project. Each module is a slide deck, a set of lecture notes, "
        "mapped external lectures, and exercises that must run.")
    d.table(["Wk", "Module", "Core question it answers"],
            [[str(m["n"]), f"<b>{m['title']}</b>", m.get("question", "")]
             for m in modules],
            widths=[0.06, 0.34, 0.60])

    d.pagebreak()
    d.h1("Projects")
    for i, p in enumerate(course["projects"], 1):
        d.h2(f"Project {i} &mdash; {p['title']} <font color='#798290'>"
             f"(after Module {p['after']})</font>")
        d.p(p["brief"])
        d.h3("Requirements")
        d.bullets(p["reqs"])
        d.h3("Done means")
        d.bullets(p["done"])

    d.h1("Assessment")
    d.p("Nobody grades this. The standard is therefore mechanical, and you "
        "apply it to yourself honestly or the credential is worth nothing.")
    d.table(["Component", "Weight", "Standard"],
            [["Module exercises", "40%",
              "Code runs and produces the specified output. Not 'I understand "
              "how I would do it.'"],
             ["Projects", "45%",
              "In the portfolio repository, with a README showing results and "
              "a written note on what was hard."],
             ["Self-checks", "15%",
              "Answered in writing from memory. Recognition is not knowledge; "
              "writing exposes the difference."]],
            widths=[0.22, 0.12, 0.66])

    d.h1("Required materials")
    d.p("All free. Nothing in this course requires a purchase.")
    d.table(["Resource", "Role"],
            [[link(u, lbl), role] for lbl, u, role in course["materials"]],
            widths=[0.38, 0.62])

    d.h1("Tooling")
    d.bullets(course["tooling"])

    d.h1("Academic honesty, restated for a solo student")
    d.p("There is no one to cheat but yourself, which makes it easier, not "
        "harder. Two rules: copy code only after you have written a worse "
        "version yourself, and never let a working result stand in for an "
        "understood one. When you paste something you do not understand, "
        "write a TODO naming what you do not understand, and go back to it.")
    return d.save(os.path.join(outdir, "Syllabus.pdf"))


# ---------------------------------------------------------- resource map
def build_resource_map(course, modules, outdir):
    d = Doc("Resource Map",
            f"{course['code']} {course['title']} \u2014 module-by-module "
            f"mapping onto free university courseware",
            course=f"{course['code']} Resource Map",
            kicker="UNIVERSITY OF CLAUDE \u00b7 FREE RESOURCE MAP")

    d.callout("How to use this", [
        "This is your lecture hall. For each module: watch or read the mapped "
        "external material first, then work the module slides and notes, "
        "which are written to assume you have seen it.",
        "Where a specific lecture number is given, that is the one that "
        "covers this module. Where a book chapter is given, read that "
        "chapter, not the whole book.",
        "Everything here is free. Resources remain under their own licences "
        "\u2014 link to them, do not redistribute them.",
    ])

    d.h1("Primary sources for the whole course")
    d.table(["Resource", "Role in this course"],
            [[link(u, lbl), role] for lbl, u, role in course["materials"]],
            widths=[0.38, 0.62])

    d.h1("Module-by-module map")
    for m in modules:
        d.h2(f"Module {m['n']:02d} &mdash; {m['title']}")
        if m.get("resources"):
            d.table(["Resource", "What it covers for this module"],
                    [[link(u, lbl), what] for lbl, u, what in m["resources"]],
                    widths=[0.37, 0.63])
        else:
            d.p("<i>Original material only for this module.</i>")
    return d.save(os.path.join(outdir, "Resource-Map.pdf"))


# ---------------------------------------------------------------- driver
def build(pkg, only=None):
    mod = importlib.import_module(pkg)
    course, modules = mod.COURSE, mod.MODULES
    course["n_modules"] = len(modules)
    outdir = os.path.join(ROOT, f"{course['code'].replace(' ', '')}-"
                                f"{slug(course['title'])}")
    os.makedirs(os.path.join(outdir, "Slides"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "Notes"), exist_ok=True)

    made = []
    if only is None:
        made.append(build_syllabus(course, modules, outdir))
        made.append(build_resource_map(course, modules, outdir))
    for m in modules:
        if only and m["n"] not in only:
            continue
        name = f"M{m['n']:02d}-{slug(m['title'])}"
        made.append(build_deck(course, m,
                               os.path.join(outdir, "Slides", name + ".pptx")))
        made.append(build_notes(course, m,
                                os.path.join(outdir, "Notes", name + ".pdf")))
    return made


if __name__ == "__main__":
    pkg = sys.argv[1]
    only = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
    for f in build(pkg, only):
        print(f)
