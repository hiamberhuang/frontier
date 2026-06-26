#!/usr/bin/env python3
"""今日金句：先按点赞排出当天最「火」的 builder 推文 top N，再让 claude 在其中挑最有金句感的一条
（只挑选 + 截取原话，绝不改写/编造），并校验金句是真推文子串（防篡改）。
→ .quote.json {quote, author, handle, tweet_id}（卡片用来做"金句→推文""作者→主页"两个链接）。
Run after fetch_x_builders.py.
"""
import json, subprocess, pathlib, re, time

HERE = pathlib.Path(__file__).resolve().parent
CLAUDE = str(pathlib.Path.home() / ".local/bin/claude")
OUT = HERE / ".quote.json"
TOPN = 8                                   # 取点赞最高的 8 条进 claude 评选


def clean(t):
    return re.sub(r"\s+", " ", re.sub(r"https?://\S+", "", t or "")).strip()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


xs = json.load(open(HERE / "builders_feed.json")).get("x", []) if (HERE / "builders_feed.json").exists() else []
cands = []
for b in xs:
    tw = b.get("tweets") or []
    if not tw:
        continue
    t0 = tw[0]
    text = clean(t0.get("text", ""))
    if 40 < len(text) < 380 and not text.lower().startswith("rt @"):
        cands.append({"name": b.get("name", ""), "handle": b.get("handle", ""),
                      "id": t0.get("id", ""), "fav": int(t0.get("favorites") or 0), "text": text})

cands.sort(key=lambda c: -c["fav"])         # 最火优先
top = cands[:TOPN]

quote = {}
if top:
    listing = "\n".join(f"{i}. [{c['name']} · {c['fav']}❤] {c['text']}" for i, c in enumerate(top))
    prompt = ("These are today's most-liked tweets from well-known AI builders. Pick the ONE that works "
              "best as an inspiring 'quote of the day' for an AI daily — sharp, insightful, a little "
              "provocative. Use their EXACT words; you may trim to the punchiest span (<=120 chars) but "
              "DO NOT rephrase, translate, or add words. Reply with ONLY compact JSON: "
              "{\"i\": <index>, \"quote\": \"<exact span>\"}.\n\n" + listing)
    for _ in range(3):
        try:
            r = subprocess.run([CLAUDE, "--model", "claude-sonnet-4-6", "-p", prompt],
                               capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            time.sleep(3); continue
        m = re.search(r"\{.*\}", r.stdout, re.S)
        if not m:
            time.sleep(3); continue
        try:
            d = json.loads(m.group(0))
            i, qq = int(d["i"]), clean(d["quote"])
            if 0 <= i < len(top) and norm(qq) and norm(qq) in norm(top[i]["text"]):  # 防篡改：必须是原话子串
                c = top[i]
                quote = {"quote": qq, "author": c["name"], "handle": c["handle"], "tweet_id": c["id"]}
                break
        except Exception:
            pass
        time.sleep(3)
    if not quote:                           # 兜底：直接用最火那条（截取）
        c = top[0]
        quote = {"quote": c["text"][:120].rstrip() + ("…" if len(c["text"]) > 120 else ""),
                 "author": c["name"], "handle": c["handle"], "tweet_id": c["id"]}

OUT.write_text(json.dumps(quote, ensure_ascii=False), encoding="utf-8")
print(f"今日金句: “{quote.get('quote','')}” —— {quote.get('author','(无)')} "
      f"({quote.get('handle','')}, {next((c['fav'] for c in top if c['handle']==quote.get('handle')), '?')}❤)"
      if quote else "无可用金句")
