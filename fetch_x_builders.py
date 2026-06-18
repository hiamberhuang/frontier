#!/usr/bin/env python3
"""Fetch each follow-builders X builder's latest substantive tweet via TikHub,
so 'Builders on X' is fresh instead of the stale central feed.
→ builders_feed.json (same shape as follow-builders feed-x.json; build.py prefers it).
Key: .tikhub_key (one line) or env TIKHUB_KEY.   Run: python3 fetch_x_builders.py
"""
import urllib.request, urllib.parse, urllib.error, json, pathlib, os, time, re

HERE = pathlib.Path(__file__).resolve().parent
FB = pathlib.Path.home() / ".claude/skills/follow-builders"
OUT = HERE / "builders_feed.json"
BASE = "https://api.tikhub.io"
EP = "/api/v1/twitter/web/fetch_user_post_tweet"

REACTION = ("great post", "this is the most", "this is the best", "love this", "so true",
            "exactly", "this.", "100%", "agreed", "well said", "congrats", "amazing",
            "incredible", "+1", "yes", "lol", "haha")

def key():
    f = HERE / ".tikhub_key"
    return f.read_text().strip() if f.exists() else os.environ.get("TIKHUB_KEY", "").strip()

def get(url, tok):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {tok}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept": "application/json"})
    last = None
    for a in range(3):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=25).read(), strict=False)
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (400, 429, 503) and a < 2:
                time.sleep(2 * (a + 1)); continue
            raise
    raise last

def num(x):
    try:
        return int(str(x).replace(",", ""))
    except Exception:
        return 0

def substantive(text):
    s = (text or "").strip()
    if s.lower().startswith("rt @"):
        return False
    body = re.sub(r"https?://\S+", "", s).strip()
    if len(body) < 70:
        return False
    return not any(body.lower().startswith(x) for x in REACTION)

def best_tweet(tl):
    """Latest substantive original (no RT / no reply); fall back to latest original."""
    orig = [t for t in tl if (t.get("text") or "").strip()
            and not t.get("text", "").lstrip().startswith("RT @")
            and not t.get("reply_to")]
    pool = orig or [t for t in tl if (t.get("text") or "").strip()]
    subs = [t for t in pool[:15] if substantive(t.get("text", ""))]
    cand = subs or pool
    return cand[0] if cand else None

tok = key()
if not tok:
    raise SystemExit("✗ 没找到 TikHub key：写进 .tikhub_key 或设 TIKHUB_KEY")

builders = json.load(open(FB / "feed-x.json")).get("x", [])
out = []
for b in builders:
    name, h = b.get("name", ""), b.get("handle", "")
    if not h:
        continue
    try:
        data = get(f"{BASE}{EP}?" + urllib.parse.urlencode({"screen_name": h}), tok)
        tl = (data.get("data") or {}).get("timeline") or []
        t = best_tweet(tl)
        if not t:
            print(f"  ✗ @{h}: 没抓到原创推")
            continue
        out.append({"name": name, "handle": h,
                    "tweets": [{"text": t.get("text", ""), "id": t.get("tweet_id", "")}]})
        print(f"  ✓ @{h}: {num(t.get('favorites'))}赞 — {(t.get('text') or '')[:45]}")
        time.sleep(1.1)          # 给 TikHub 喘口气
    except Exception as ex:
        print(f"  ✗ @{h}: {ex}")

json.dump({"x": out}, open(OUT, "w"), ensure_ascii=False, indent=2)
print(f"✓ {len(out)} builders → {OUT}")
