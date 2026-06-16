#!/usr/bin/env python3
"""Frontier — build a magazine-style AI news daily from follow-builders feeds.
Pulls real images (YouTube thumbnails + X avatars). No deps, stdlib only.
Run: python3 build.py  → writes index.html
"""
import json, re, html, pathlib

FB = pathlib.Path.home() / ".claude/skills/follow-builders"
OUT = pathlib.Path(__file__).resolve().parent
BYLINE = "curated by Amber Huang · @hiamberhuang"

def yt_id(url):
    for pat in (r"[?&]v=([\w-]{6,})", r"youtu\.be/([\w-]{6,})", r"/live/([\w-]{6,})", r"/embed/([\w-]{6,})"):
        m = re.search(pat, url or "")
        if m:
            return m.group(1)
    return None

def clean(t, n=260):
    if not t:
        return ""
    t = re.sub(r"Speaker\s*\d+\s*\|\s*[\d:]+\s*-\s*[\d:]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return (t[:n].rsplit(" ", 1)[0] + "…") if len(t) > n else t

def esc(s):
    return html.escape(s or "")

pods = json.load(open(FB / "feed-podcasts.json")).get("podcasts", [])
xs = json.load(open(FB / "feed-x.json")).get("x", [])
gen = json.load(open(FB / "feed-podcasts.json")).get("generatedAt", "")[:10]

# ---- podcasts with thumbnails ----
pod_items = []
for p in pods:
    vid = yt_id(p.get("url", ""))
    if not vid:
        continue
    pod_items.append({
        "name": p.get("name", ""), "title": p.get("title", ""),
        "url": p.get("url", ""), "thumb": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg",
        "teaser": clean(p.get("transcript", ""), 300),
    })

# ---- builders with avatars + top tweet ----
x_items = []
for b in xs:
    tw = (b.get("tweets") or [])
    if not tw:
        continue
    h = b.get("handle", "")
    x_items.append({
        "name": b.get("name", ""), "handle": h,
        "avatar": f"https://unavatar.io/x/{h}",
        "tweet": clean(tw[0].get("text", ""), 220),
        "url": f"https://x.com/{h}/status/{tw[0].get('id','')}",
    })

hero = pod_items[0] if pod_items else None
rest_pods = pod_items[1:7]
x_items = x_items[:8]

def pod_card(p):
    return f"""<a class="pod" href="{esc(p['url'])}" target="_blank">
      <img loading="lazy" src="{esc(p['thumb'])}" alt="">
      <div><span class="src">{esc(p['name'])}</span><h3>{esc(p['title'])}</h3></div></a>"""

def x_card(b):
    return f"""<div class="xc">
      <img loading="lazy" class="av" src="{esc(b['avatar'])}" alt="" onerror="this.style.visibility='hidden'">
      <div><div class="xn">{esc(b['name'])} <span>@{esc(b['handle'])}</span></div>
      <p>{esc(b['tweet'])}</p>
      <a href="{esc(b['url'])}" target="_blank">read on X →</a></div></div>"""

hero_html = ""
if hero:
    hero_html = f"""<a class="hero" href="{esc(hero['url'])}" target="_blank">
      <img src="{esc(hero['thumb'])}" alt="">
      <span class="kicker">Today's signal · {esc(hero['name'])}</span>
      <h1>{esc(hero['title'])}</h1>
      <p>{esc(hero['teaser'])}</p></a>"""

page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Frontier · AI daily</title>
<style>
:root{{--ink:#111;--muted:#666;--line:#e4e2dc;--accent:#b8341a;--bg:#faf9f6}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,"Segoe UI",Roboto,"PingFang SC",sans-serif;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:860px;margin:0 auto;padding:0 20px 80px}}
header{{text-align:center;border-bottom:2px solid var(--ink);padding:28px 0 14px;margin-bottom:34px}}
.mast{{font-family:Georgia,"Times New Roman",serif;font-size:64px;font-weight:700;letter-spacing:-1px;line-height:1}}
.tag{{font-size:13px;color:var(--muted);margin-top:8px;letter-spacing:.02em}}
.date{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em;margin-top:6px}}
.hero{{display:block;text-decoration:none;color:inherit;margin-bottom:44px}}
.hero img{{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:6px;background:var(--line)}}
.kicker{{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);margin:16px 0 6px;font-weight:600}}
.hero h1{{font-family:Georgia,serif;font-size:38px;line-height:1.15;margin:0 0 10px;font-weight:700}}
.hero p{{font-size:17px;color:#333;margin:0;max-width:90%}}
.sec{{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);border-bottom:1px solid var(--ink);padding-bottom:6px;margin:0 0 22px;font-weight:600}}
.pods{{display:grid;gap:26px;margin-bottom:48px}}
.pod{{display:grid;grid-template-columns:200px 1fr;gap:18px;text-decoration:none;color:inherit;align-items:start}}
.pod img{{width:200px;aspect-ratio:16/9;object-fit:cover;border-radius:6px;background:var(--line)}}
.pod .src{{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);font-weight:600}}
.pod h3{{font-family:Georgia,serif;font-size:21px;line-height:1.25;margin:5px 0 0;font-weight:700}}
.xs{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.xc{{display:flex;gap:12px}}
.av{{width:46px;height:46px;border-radius:50%;flex-shrink:0;object-fit:cover;background:var(--line)}}
.xn{{font-weight:600;font-size:15px}}.xn span{{color:var(--muted);font-weight:400}}
.xc p{{font-size:14px;line-height:1.55;color:#333;margin:4px 0 4px}}
.xc a{{font-size:12px;color:var(--accent);text-decoration:none}}
footer{{text-align:center;border-top:2px solid var(--ink);margin-top:50px;padding-top:18px;font-size:13px;color:var(--muted)}}
@media(max-width:620px){{.mast{{font-size:44px}}.hero h1{{font-size:28px}}.pod{{grid-template-columns:1fr}}.pod img{{width:100%}}.xs{{grid-template-columns:1fr}}}}
</style></head>
<body><div class="wrap">
<header><div class="mast">Frontier</div>
<div class="tag">AI news, curated from builders — not influencers</div>
<div class="date">{esc(gen)} · {esc(BYLINE)}</div></header>
{hero_html}
<div class="sec">Podcasts</div>
<div class="pods">{''.join(pod_card(p) for p in rest_pods)}</div>
<div class="sec">Builders on X</div>
<div class="xs">{''.join(x_card(b) for b in x_items)}</div>
<footer>Pick your own builders. Read AI like a magazine.<br>fork it · @hiamberhuang</footer>
</div></body></html>"""

(OUT / "index.html").write_text(page, encoding="utf-8")
print(f"✓ built {OUT/'index.html'}  | {len(pod_items)} podcasts, {len(x_items)} builders")
