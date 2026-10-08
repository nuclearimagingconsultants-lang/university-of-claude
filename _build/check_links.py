# -*- coding: utf-8 -*-
"""Check every external URL in the content, and find archive replacements.

Writes _build/linkcheck.json:
  {url: {"status": "ok"|"dead"|"blocked"|"error", "code": int|null,
         "wayback": url|null, "where": ["CSCE 629 M03 resources", ...]}}

Live-checked with HEAD, falling back to a ranged GET for hosts that refuse
HEAD. 403 and 429 are recorded as "blocked" rather than dead: they are bot
protection, and the page is fine in a browser.
"""
import sys, os, json, ssl, time, collections
import urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "content"))
from make_readme import PLAN, load

OUT = os.path.join(HERE, "linkcheck.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
DEAD_CODES = {404, 410, 451}


def collect():
    seen = collections.OrderedDict()
    for sem, pkg, code, title in PLAN:
        m = load(pkg)
        if m is None:
            continue
        def add(url, where):
            seen.setdefault(url, []).append("%s %s" % (code, where))
        for t in m.COURSE.get("materials", []):
            if len(t) >= 2:
                add(t[1], "materials")
        for t in m.COURSE.get("map", []):
            if len(t) >= 2:
                add(t[1], "map")
        for x in m.MODULES:
            for t in x.get("resources", []):
                if len(t) >= 2:
                    add(t[1], "M%02d" % x["n"])
    return seen


def fetch(url, method="HEAD", timeout=12):
    r = urllib.request.Request(url, method=method, headers={
        "User-Agent": UA, "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.9"})
    if method == "GET":
        r.add_header("Range", "bytes=0-2048")
    return urllib.request.urlopen(r, timeout=timeout, context=CTX).getcode()


def probe(url):
    for method in ("HEAD", "GET"):
        try:
            c = fetch(url, method)
            return ("ok", c)
        except urllib.error.HTTPError as e:
            if e.code in DEAD_CODES:
                return ("dead", e.code)
            if e.code in (403, 429, 401):
                if method == "GET":
                    return ("blocked", e.code)
                continue              # retry once with GET
            if e.code in (405, 501) and method == "HEAD":
                continue              # HEAD not allowed; try GET
            if method == "GET":
                return ("error", e.code)
        except Exception as e:
            if method == "GET":
                msg = str(e).lower()
                if "name or service" in msg or "getaddrinfo" in msg \
                   or "nodename" in msg:
                    return ("dead", None)
                return ("error", None)
    return ("error", None)


def wayback(url):
    """Newest usable snapshot, or None."""
    api = ("https://archive.org/wayback/available?url="
           + urllib.parse.quote(url, safe=""))
    try:
        r = urllib.request.Request(api, headers={"User-Agent": UA})
        d = json.load(urllib.request.urlopen(r, timeout=20, context=CTX))
        snap = d.get("archived_snapshots", {}).get("closest")
        if snap and snap.get("available"):
            return snap["url"].replace("http://web.archive.org",
                                       "https://web.archive.org")
    except Exception:
        pass
    return None


def main():
    seen = collect()
    urls = list(seen)
    print("checking %d distinct URLs ..." % len(urls), flush=True)
    res = {}
    t0 = time.time()

    def work(u):
        s, c = probe(u)
        return u, s, c

    done = 0
    with ThreadPoolExecutor(max_workers=10) as ex:
        for u, s, c in ex.map(work, urls):
            res[u] = {"status": s, "code": c, "wayback": None,
                      "where": seen[u]}
            done += 1
            if done % 100 == 0:
                print("  %d/%d  %.0fs" % (done, len(urls), time.time() - t0),
                      flush=True)

    bad = [u for u, v in res.items() if v["status"] in ("dead", "error")]
    print("looking up %d archive snapshots ..." % len(bad), flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        for u, w in zip(bad, ex.map(wayback, bad)):
            res[u]["wayback"] = w

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)

    tally = collections.Counter(v["status"] for v in res.values())
    print("\n%s" % dict(tally))
    print("archive snapshot found for %d of %d dead/error"
          % (sum(1 for u in bad if res[u]["wayback"]), len(bad)))
    print(OUT)


if __name__ == "__main__":
    main()
