#!/usr/bin/env python3
"""Fetch latest original post from AI product official X accounts via TikHub
(managed scraper — reliable, uses your TikHub credits). → product_feed.json.
Key: put your TikHub token in .tikhub_key (one line) or env TIKHUB_KEY.
Run:  python3 fetch_x_products.py
"""
import urllib.request, urllib.parse, urllib.error, json, pathlib, os, time

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "product_feed.json"
BASE = "https://api.tikhub.io"          # 国内不通就改 https://api.tikhub.dev
EP = "/api/v1/twitter/web/fetch_user_post_tweet"

# 已用 TikHub 实测验证的 handle（✓ = 抓得到）。要加新账号，先确认 @后面那串用户名
ACCOUNTS = [
    ("Anthropic", "AnthropicAI"),   # ✓ 实测
    ("OpenAI", "OpenAI"),           # ✓ 实测
    ("HeyGen", "HeyGen"),           # Amber 提供 x.com/HeyGen
    ("AhaCreator", "_ahacreator"),  # Amber 提供 x.com/_ahacreator
    # Ditto(@ditto_dates）撤掉：最近全是转发、0 赞，没运营。有原创内容了再加回
]

def key():
    f = HERE / ".tikhub_key"
    if f.exists():
        return f.read_text().strip()
    return os.environ.get("TIKHUB_KEY", "").strip()

def get(url, tok):
    """GET with browser UA + retry/backoff (TikHub 400/429s on rapid calls)."""
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {tok}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept": "application/json"})
    last = None
    for attempt in range(3):
        try:
            # strict=False：容忍推文里的换行/控制字符，否则会解析报错
            return json.loads(urllib.request.urlopen(req, timeout=25).read(), strict=False)
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (400, 429, 503) and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise
    raise last

def num(x):
    try:
        return int(str(x).replace(",", ""))
    except Exception:
        return 0

def pick(tws):
    """TikHub returns data.timeline[] (newest-first). Take the most-liked original
    among the latest dozen — skip retweets (RT @…) so we show the account's own voice."""
    pool = [t for t in tws if (t.get("text") or "").strip()
            and not t.get("text", "").lstrip().startswith("RT @")]
    if not pool:
        pool = [t for t in tws if (t.get("text") or "").strip()]   # 实在没原创再退回
    if not pool:
        return None
    recent = pool[:12]
    recent.sort(key=lambda t: -num(t.get("favorites")))
    return recent[0]

def img_of(t):
    m = t.get("media") or []
    if isinstance(m, list) and m and isinstance(m[0], dict):
        return m[0].get("media_url_https") or m[0].get("media_url") or ""
    return ""

def link_of(t):
    urls = ((t.get("entities") or {}).get("urls") or [])
    for u in urls:
        ex = u.get("expanded_url", "")
        if ex and "twitter.com" not in ex and "x.com" not in ex:
            return ex
    return ""

tok = key()
if not tok:
    raise SystemExit("✗ 没找到 TikHub key：把 token 写进 .tikhub_key 文件（一行）或设 TIKHUB_KEY 环境变量")

items = []
for name, handle in ACCOUNTS:
    try:
        url = f"{BASE}{EP}?" + urllib.parse.urlencode({"screen_name": handle})
        data = get(url, tok)
        tws = (data.get("data") or {}).get("timeline") or []
        t = pick(tws)
        if not t:
            print(f"  ✗ {handle}: 没解析到推文（响应里无 timeline）")
            continue
        items.append({
            "name": name, "handle": handle,
            "title": (t.get("text") or "")[:220],
            "img": img_of(t),
            "link": link_of(t),
            "likes": num(t.get("favorites")),
            "views": num(t.get("views")),
            "url": f"https://x.com/{handle}/status/{t.get('tweet_id','')}",
            "time": t.get("created_at", ""),
        })
        print(f"  ✓ {name} (@{handle}): {num(t.get('favorites'))} 赞 · {num(t.get('views'))} 看 · {(t.get('text') or '')[:45]}")
        time.sleep(1.2)          # 给 TikHub 喘口气，避免连发被 400
    except Exception as ex:
        print(f"  ✗ {handle}: {ex}")

# sort by engagement
items.sort(key=lambda x: -(x.get("likes") or 0))
json.dump({"product": items}, open(OUT, "w"), ensure_ascii=False, indent=2)
print(f"✓ {len(items)} 官号 → {OUT}")
