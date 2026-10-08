# -*- coding: utf-8 -*-
"""Scan every content module for unbalanced inline markup.

An unclosed <b> reaches reportlab as a parse error only if that string
happens to be rendered through a paragraph style that parses markup --
otherwise it prints literally or is silently dropped. Checking the source
catches it everywhere, including in slide text where the Deck parser is
lenient.
"""
import glob
import os
import re
import sys

TAG = re.compile(r"</?(b|i|em|strong|code|tt|sub|super|sup)>", re.I)
PAIRED = {"b", "i", "em", "strong", "code", "tt", "sub", "super", "sup"}


def unbalanced(text):
    """Return a list of complaints about tag nesting in one string."""
    stack, bad = [], []
    for m in TAG.finditer(text):
        tag = m.group(1).lower()
        if tag not in PAIRED:
            continue
        if m.group(0).startswith("</"):
            if not stack:
                bad.append("closing </%s> with nothing open" % tag)
            elif stack[-1] != tag:
                bad.append("</%s> closes <%s>" % (tag, stack[-1]))
                stack.pop()
            else:
                stack.pop()
        else:
            stack.append(tag)
    if stack:
        bad.append("never closed: " + ", ".join("<%s>" % t for t in stack))
    return bad


def walk(obj, path, out):
    """Recurse through the COURSE/MODULES structures checking every string."""
    if isinstance(obj, str):
        for complaint in unbalanced(obj):
            out.append((path, complaint, obj[:70]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, "%s.%s" % (path, k), out)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            walk(v, "%s[%d]" % (path, i), out)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "content"))
    bad = []
    for f in sorted(glob.glob(os.path.join(here, "content", "csce*.py"))):
        pkg = os.path.splitext(os.path.basename(f))[0]
        m = __import__(pkg)
        walk(m.COURSE, pkg + ".COURSE", bad)
        for mod in m.MODULES:
            walk(mod, "%s.M%02d" % (pkg, mod["n"]), bad)
    for path, complaint, snippet in bad:
        print("%s\n    %s\n    %r\n" % (path, complaint, snippet))
    print("%d unbalanced markup sites" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
