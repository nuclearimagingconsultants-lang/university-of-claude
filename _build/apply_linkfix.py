# -*- coding: utf-8 -*-
"""Rewrite dead URLs in content/*.py to their archive snapshots.

Reads _build/linkcheck.json. Only touches URLs whose status is "dead" (or
"error" with a snapshot available) AND that appear verbatim on one line of
a content file -- anything split across lines is reported instead, so a
silent partial edit is impossible.

    python apply_linkfix.py            # report only
    python apply_linkfix.py --write    # actually edit
"""
import io, os, sys, json, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
LC = os.path.join(HERE, "linkcheck.json")
WRITE = "--write" in sys.argv


def main():
    with io.open(LC, encoding="utf-8") as f:
        res = json.load(f)

    todo = {u: v["wayback"] for u, v in res.items()
            if v["status"] in ("dead", "error") and v["wayback"]}
    nofix = [u for u, v in res.items()
             if v["status"] in ("dead", "error") and not v["wayback"]]

    files = sorted(glob.glob(os.path.join(HERE, "content", "*.py")))
    applied = collections.Counter()
    unfound = []

    for u, new in sorted(todo.items()):
        hit = False
        for p in files:
            s = io.open(p, encoding="utf-8").read()
            if u in s:
                hit = True
                if WRITE:
                    io.open(p, "w", encoding="utf-8").write(s.replace(u, new))
                applied[os.path.basename(p)] += s.count(u)
        if not hit:
            unfound.append(u)

    print("%s %d dead URLs with snapshots"
          % ("REWROTE" if WRITE else "WOULD REWRITE", len(todo) - len(unfound)))
    for f_, n in sorted(applied.items()):
        print("   %-22s %d" % (f_, n))
    if unfound:
        print("\nnot found verbatim (likely split across lines) -- fix by hand:")
        for u in unfound:
            print("   %s" % u)
    if nofix:
        print("\ndead with NO archive snapshot (%d) -- need a replacement:"
              % len(nofix))
        for u in nofix:
            print("   %-72s %s" % (u[:72], res[u]["where"][0]))
    if not WRITE:
        print("\n(dry run; pass --write to apply)")


if __name__ == "__main__":
    main()
