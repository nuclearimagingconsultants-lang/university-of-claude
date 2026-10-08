# -*- coding: utf-8 -*-
"""Verify every cross-reference points at something that exists.

The program's claim is that it builds in sequence and that modules refer to
each other accurately. 763 references of the form "CSCE 641 Module 03 §2"
assert that a course, a module and a section all exist. Nothing checked them
until now; a renumbered module or a dropped section breaks them silently.

    python check_xrefs.py
"""
import io, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "content"))
from make_readme import PLAN, load

REF = re.compile(
    r"(CSCE|UC\s+MATH|UC\s+LINA)\s*(\d{3})\s+Module\s+(\d{1,2})"
    r"(?:\s*&sect;+\s*(\d+)|\s*§+\s*(\d+))?")


def main():
    # What actually exists: course code -> {module n -> number of sections}
    world, planned = {}, {}
    for sem, pkg, code, title in PLAN:
        planned[code] = sem
        m = load(pkg)
        if m is None:
            continue
        world[code] = {
            mod["n"]: sum(1 for s in mod["slides"] if s.get("t") == "section")
            for mod in m.MODULES}

    problems = collections.Counter()
    detail = []
    total = 0
    for sem, pkg, code, title in PLAN:
        m = load(pkg)
        if m is None:
            continue
        for mod in m.MODULES:
            blob = repr(mod["slides"]) + repr(mod.get("notes") or []) + \
                   repr(mod.get("exercises") or [])
            here = "%s M%02d" % (code, mod["n"])
            for fam, num, mn, s1, s2 in REF.findall(blob):
                total += 1
                tgt = ("%s %s" % (re.sub(r"\s+", " ", fam), num)).strip()
                mn = int(mn)
                sec = int(s1 or s2) if (s1 or s2) else None
                if tgt not in planned:
                    problems["course not in the plan"] += 1
                    detail.append((here, tgt, mn, sec, "no such course"))
                elif tgt not in world:
                    problems["course planned but not built"] += 1
                    detail.append((here, tgt, mn, sec, "course not built"))
                elif mn not in world[tgt]:
                    problems["module does not exist"] += 1
                    detail.append((here, tgt, mn, sec, "no Module %02d" % mn))
                elif sec is not None and sec > world[tgt][mn]:
                    problems["section does not exist"] += 1
                    detail.append((here, tgt, mn, sec,
                                   "only %d sections" % world[tgt][mn]))
                elif tgt == code and mn == mod["n"]:
                    problems["module cites itself"] += 1
                    detail.append((here, tgt, mn, sec, "self-reference"))

    print("%d cross-references checked" % total)
    if not problems:
        print("all resolve")
        return 0
    for k, v in problems.most_common():
        print("  %-32s %d" % (k, v))
    print()
    for here, tgt, mn, sec, why in detail[:40]:
        print("  %-14s -> %s Module %02d%s   %s"
              % (here, tgt, mn, (" §%d" % sec) if sec else "", why))
    if len(detail) > 40:
        print("  ... and %d more" % (len(detail) - 40))
    return 1


if __name__ == "__main__":
    sys.exit(main())
