# -*- coding: utf-8 -*-
"""Polite Wayback Machine lookups.

archive.org rate-limits hard and answers 429 for a while once you trip it,
so this is deliberately slow: one request at a time, a pause between them,
and exponential backoff when throttled. Looking up a few hundred URLs takes
minutes, not seconds, and that is the correct speed.

    python wayback.py dead     # only the dead/error URLs in linkcheck.json
    python wayback.py all      # every URL that has no snapshot recorded yet
"""
import io, os, sys, json, ssl, time, random
import urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
LC = os.path.join(HERE, "linkcheck.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

GAP = 2.5          # seconds between requests, minimum
_last = [0.0]


def _wait():
    d = GAP - (time.time() - _last[0])
    if d > 0:
        time.sleep(d)
    _last[0] = time.time()


def lookup(url, tries=5):
    """Newest usable snapshot URL, or None. Backs off on 429."""
    api = ("https://archive.org/wayback/available?url="
           + urllib.parse.quote(url, safe=""))
    delay = 8.0
    for attempt in range(tries):
        _wait()
        try:
            r = urllib.request.Request(api, headers={"User-Agent": UA})
            d = json.load(urllib.request.urlopen(r, timeout=30, context=CTX))
            snap = d.get("archived_snapshots", {}).get("closest")
            if snap and snap.get("available"):
                return snap["url"].replace("http://web.archive.org",
                                           "https://web.archive.org")
            return None                      # genuinely not archived
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(delay + random.uniform(0, 3))
                delay = min(delay * 2, 120)
                continue
            return None
        except Exception:
            time.sleep(delay)
            delay = min(delay * 2, 60)
    return None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "dead"
    res = json.load(io.open(LC, encoding="utf-8"))

    if mode == "dead":
        todo = [u for u, v in res.items()
                if v["status"] in ("dead", "error") and not v.get("wayback")]
    else:
        todo = [u for u, v in res.items() if not v.get("wayback")]

    print("%d URLs to look up, ~%.0f min at %.1fs each"
          % (len(todo), len(todo) * GAP / 60, GAP), flush=True)
    found = 0
    for i, u in enumerate(todo, 1):
        w = lookup(u)
        res[u]["wayback"] = w
        found += bool(w)
        if w:
            print("  [%d/%d] OK   %s" % (i, len(todo), u[:84]), flush=True)
        else:
            print("  [%d/%d] none %s" % (i, len(todo), u[:84]), flush=True)
        if i % 20 == 0:
            json.dump(res, io.open(LC, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)

    json.dump(res, io.open(LC, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\nsnapshots found for %d of %d" % (found, len(todo)))


if __name__ == "__main__":
    main()
