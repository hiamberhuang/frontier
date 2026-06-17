#!/usr/bin/env python3
"""Fetch latest original post from AI product official X accounts via TikHub
(managed scraper — reliable, uses your TikHub credits). → product_feed.json.
Key: put your TikHub token in .tikhub_key (one line) or env TIKHUB_KEY.
Run:  python3 fetch_x_products.py
"""
import urllib.request, urllib.parse, json, pathlib, os

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "product_feed.json"
BASE = "https://api.tikhub.io"          # 国内不通就改 https://api.tikhub.dev
EP = "/api/v1/twitter/web/fetch_user_post_tweet"

# ⚠️ 确认官号 handle 对不对（去 X 核一下，错了改这里）
ACCOUNTS = [
    ("Anthropic", "AnthropicAI"),
    ("OpenAI", "OpenAI"),
    ("HeyGen", "HeyGen_Official"),
    ("AhaCreator", "AhaCreator_AI"),
    ("Ditto", "heyditto"),
]

def key():
    f = HERE / ".tikhub_key"
    if f.exists():
        return f.read_text().strip()
    return os.environ.get("TIKHUB_KEY", "").strip()

def get(url, tok):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}",
                                               "User-Agent": "Frontier/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=25).read())

def find_tweets(o, out):
    """Recursively collect tweet 'legacy' objects from TikHub's X timeline JSON."""
    if isinstance(o, dict):
        if "full_text" in o and "favorite_count" in o:
            out.append(o)
        for v in o.values():
            find_tweets(v, out)
    elif isinstance(o, list):
        for v in o:
            find_tweets(v, out)

def pick(tw):
    """Latest original (not retweet/reply) by created order; fall back to most-liked."""
    orig = [t for t in tw if not t.get("retweeted_status_result")
            and not t.get("in_reply_to_status_id_str")]
    pool = orig or tw
    # tweets usually come newest-first; take first, but prefer one with media
    withmedia = [t for t in pool if (t.get("entities", {}) or {}).get("media")]
    return (withmedia or pool)[0] if pool else None

def img_of(t):
    m = (t.get("entities", {}) or {}).get("media") or \
        (t.get("extended_entities", {}) or {}).get("media") or []
    return m[0]["media_url_https"] if m and m[0].get("media_url_https") else ""

tok = key()
if not tok:
    raise SystemExit("✗ 没找到 TikHub key：把 token 写进 .tikhub_key 文件（一行）或设 TIKHUB_KEY 环境变量")

items = []
for name, handle in ACCOUNTS:
    try:
        url = f"{BASE}{EP}?" + urllib.parse.urlencode({"screen_name": handle})
        data = get(url, tok)
        tw = []
        find_tweets(data, tw)
        t = pick(tw)
        if not t:
            print(f"  ✗ {handle}: 没解析到推文（响应结构待看）")
            continue
        items.append({
            "name": name, "handle": handle,
            "title": (t.get("full_text") or "")[:200],
            "img": img_of(t),
            "likes": t.get("favorite_count", 0),
            "url": f"https://x.com/{handle}/status/{t.get('id_str','')}",
        })
        print(f"  ✓ {name} (@{handle}): {t.get('favorite_count')} likes")
    except Exception as ex:
        print(f"  ✗ {handle}: {ex}")

# sort by engagement
items.sort(key=lambda x: -(x.get("likes") or 0))
json.dump({"product": items}, open(OUT, "w"), ensure_ascii=False, indent=2)
print(f"✓ {len(items)} 官号 → {OUT}")
