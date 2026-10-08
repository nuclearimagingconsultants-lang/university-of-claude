# -*- coding: utf-8 -*-
"""Generate _app/data/program.json from whatever is currently built.

The study app reads this file and nothing else, so adding a course is
`make_course.py <pkg>` followed by this script -- no app changes.
"""
import io, os, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "content"))

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "_app", "data", "program.json")

from uc import _plain
from make_course import slug
from make_readme import PLAN, load

SEMESTER_LABELS = {
    0: "Prerequisites",
    1: "Foundations",
    2: "Systems and geometry",
    3: "Light and motion",
    4: "Perception and parallelism",
    5: "Engine internals",
    6: "Learning foundations",
    7: "Perception and agents",
    8: "Theory",
    9: "Security",
    10: "Data and language",
    11: "Human-centred computing",
    12: "Frontiers",
    13: "Robotics and embodiment",
    14: "High-performance computing",
    15: "Distributed systems II",
    16: "Networks and network security",
    17: "Recognition and intent",
    18: "Data at scale",
    19: "Hardware verification",
    20: "Form and fabrication",
    21: "Media and collaboration",
    22: "Security engineering",
    23: "Adversarial and forensic",
    24: "Governance and human factors",
}

# Semesters 1-4 are the degree; 0 is its prerequisites; 5+ is continuation.
def phase(sem):
    if sem == 0:
        return "prerequisite"
    if sem <= 4:
        return "degree"
    return "continuation"


def txt(s):
    """Markup-and-entity-free plain text, for display in the app."""
    return _plain(s) if isinstance(s, str) else s


def txts(xs):
    return [txt(x) for x in xs if isinstance(x, str) and x.strip()]


def rel(path):
    """Repository-relative, forward slashes, for use as a URL."""
    return path.replace("\\", "/")


def main():
    courses, n_mod, n_sl, n_ex, n_rs = [], 0, 0, 0, 0

    for sem, pkg, code, title in PLAN:
        m = load(pkg)
        cdir = "Courses/%s-%s" % (code.replace(" ", ""), slug(title))
        built = m is not None and os.path.isdir(os.path.join(ROOT, cdir))
        if not built:
            courses.append({
                "sem": sem, "code": code, "title": title,
                "phase": phase(sem), "built": False, "modules": [],
            })
            continue

        C, MS = m.COURSE, m.MODULES
        mods = []
        for x in MS:
            base = "M%02d-%s" % (x["n"], slug(x["title"]))
            sl = "%s/Slides/%s.pptx" % (cdir, base)
            nt = "%s/Notes/%s.pdf" % (cdir, base)
            mods.append({
                "n": x["n"],
                "title": txt(x["title"]),
                "subtitle": txt(x.get("subtitle", "")),
                "question": txt(x.get("question", "")),
                "outcomes": txts(x.get("outcomes", [])),
                "takeaways": txts(x.get("takeaways", [])),
                "selfcheck": txts(x.get("selfcheck", [])),
                "n_slides": len(x.get("slides", [])) + 3,
                "n_exercises": len(x.get("exercises", [])),
                "n_resources": len(x.get("resources", [])),
                "slides": rel(sl)
                if os.path.isfile(os.path.join(ROOT, sl)) else None,
                "notes": rel(nt)
                if os.path.isfile(os.path.join(ROOT, nt)) else None,
            })

        syl = "%s/Syllabus.pdf" % cdir
        rmap = "%s/Resource-Map.pdf" % cdir
        courses.append({
            "sem": sem, "code": code, "title": title,
            "phase": phase(sem), "built": True,
            "dir": cdir,
            "tagline": txt(C.get("tagline", "")),
            "term": txt(C.get("term", "")),
            "effort": txt(C.get("effort", "")),
            "prereqs": txt(C.get("prereqs", "")),
            "deliverable": txt(C.get("deliverable", "")),
            "outcomes": txts(C.get("outcomes", [])),
            "syllabus": rel(syl)
            if os.path.isfile(os.path.join(ROOT, syl)) else None,
            "resource_map": rel(rmap)
            if os.path.isfile(os.path.join(ROOT, rmap)) else None,
            "modules": mods,
        })
        n_mod += len(mods)
        n_sl += sum(d["n_slides"] for d in mods)
        n_ex += sum(d["n_exercises"] for d in mods)
        n_rs += sum(d["n_resources"] for d in mods)

    sems = []
    for n in sorted({c["sem"] for c in courses}):
        inner = [c for c in courses if c["sem"] == n]
        sems.append({
            "n": n,
            "label": SEMESTER_LABELS.get(n, "Semester %d" % n),
            "phase": phase(n),
            "built": sum(1 for c in inner if c["built"]),
            "total": len(inner),
        })

    doc = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "program": {
            "name": "University of Claude",
            "degree": "MS in Computer Science",
            "track": "Graphics and Game Engines",
            "accredited": False,
        },
        "stats": {
            "courses_built": sum(1 for c in courses if c["built"]),
            "courses_planned": len(courses),
            "modules": n_mod, "slides": n_sl,
            "exercises": n_ex, "resources": n_rs,
        },
        "semesters": sems,
        "courses": courses,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(OUT)
    print("%d of %d courses, %d modules indexed"
          % (doc["stats"]["courses_built"],
             doc["stats"]["courses_planned"], n_mod))
    return doc


if __name__ == "__main__":
    main()
