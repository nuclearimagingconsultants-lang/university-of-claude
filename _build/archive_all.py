# -*- coding: utf-8 -*-
"""Record an archive snapshot for every external URL, not just the dead ones.

Link rot is continuous: a link that works today is the one that breaks next
year. This fills in the "wayback" field for every entry in linkcheck.json,
so that when a URL does die the replacement is already known and the fix is
mechanical rather than a research task.

    python archive_all.py           # fill in whatever is missing
    python archive_all.py --report  # just summarise coverage
"""
import io, os, sys, json, ssl, time, collections
import urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
LC = os.path.join(HERE, "linkcheck.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def wayback(url):
    api = ("https://archive.org/wayback/available?url="
           + urllib.parse.quote(url, safe=""))
    for attempt in range(2):
        try:
            r = urllib.request.Request(api, headers={"User-Agent": UA})
            d = json.load(urllib.request.urlopen(r, timeout=25, context=CTX))
            snap = d.get("archived_snapshots", {}).get("closest")
            if snap and snap.get("available"):
                return snap["url"].replace("http://web.archive.org",
                                           "https://web.archive.org")
            return None
        except Exception:
            time.sleep(1.5)
    return None


def main():
    res = json.load(io.open(LC, encoding="utf-8"))

    if "--report" in sys.argv:
        have = sum(1 for v in res.values() if v.get("wayback"))
        by = collections.Counter(
            (v["status"], bool(v.get("wayback"))) for v in res.values())
        print("URLs: %d   with archive snapshot: %d (%.0f%%)"
              % (len(res), have, 100 * have / max(1, len(res))))
        for (st, w), n in sorted(by.items()):
            print("   %-9s archived=%-5s %d" % (st, w, n))
        return

    todo = [u for u, v in res.items() if not v.get("wayback")]
    print("looking up %d snapshots (%d already known) ..."
          % (len(todo), len(res) - len(todo)), flush=True)
    t0, done = time.time(), 0
    with ThreadPoolExecutor(max_workers=5) as ex:
        for u, w in zip(todo, ex.map(wayback, todo)):
            res[u]["wayback"] = w
            done += 1
            if done % 100 == 0:
                print("   %d/%d  %.0fs" % (done, len(todo), time.time() - t0),
                      flush=True)
                json.dump(res, io.open(LC, "w", encoding="utf-8"),
                          ensure_ascii=False, indent=1)

    json.dump(res, io.open(LC, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    have = sum(1 for v in res.values() if v.get("wayback"))
    print("\n%d of %d URLs now have a recorded snapshot (%.0f%%)"
          % (have, len(res), 100 * have / max(1, len(res))))


if __name__ == "__main__":
    main()
