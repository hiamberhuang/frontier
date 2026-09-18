#!/usr/bin/env python3
"""Fetch latest videos from Amber's curated YouTube channels via yt-dlp.
Writes custom_feed.json (cached) so build.py stays fast. Run before build.py.
Roster is the authoritative one in SOURCES.md — keep the two in sync.
B站 pending: yt-dlp bilibili extractor currently broken (NoneType) — TODO.
"""
import json, subprocess, pathlib, time

OUT = pathlib.Path(__file__).resolve().parent / "custom_feed.json"

# Amber's curated YouTube roster (name -> channel handle URL).
# Mirrors SOURCES.md § YouTube. All handles verified resolving 2026-09-18.
YT_CHANNELS = [
    # ── 投资机构 · VC ──
    ("Sequoia Capital",  "https://www.youtube.com/@sequoiacapital/videos"),
    ("a16z",             "https://www.youtube.com/@a16z/videos"),
    ("Y Combinator",     "https://www.youtube.com/@ycombinator/videos"),
    ("Redpoint AI",      "https://www.youtube.com/@redpointai/videos"),
    # ── 前沿 AI 公司 · 官方 ──
    ("OpenAI",           "https://www.youtube.com/@OpenAI/videos"),
    ("Anthropic",        "https://www.youtube.com/@anthropic-ai/videos"),
    ("Google DeepMind",  "https://www.youtube.com/@googledeepmind/videos"),
    ("HeyGen",           "https://www.youtube.com/@HeyGen_Official/videos"),
    ("Notion",           "https://www.youtube.com/@Notion/videos"),
    # ── 一线 researcher · 长访谈 ──
    ("Andrej Karpathy",  "https://www.youtube.com/@AndrejKarpathy/videos"),
    ("Lex Fridman",      "https://www.youtube.com/@lexfridman/videos"),
    # ── 播客 · 工程 / 产品 ──
    ("Latent Space",     "https://www.youtube.com/@LatentSpacePod/videos"),
    ("Lenny's Podcast",  "https://www.youtube.com/@LennysPodcast/videos"),
    ("No Priors",        "https://www.youtube.com/@NoPriorsPodcast/videos"),
    ("Uncapped",         "https://www.youtube.com/@uncappedpod/videos"),
    # ── 科普 / 评测(广度) ──
    ("Two Minute Papers","https://www.youtube.com/@TwoMinutePapers/videos"),
    ("AI Explained",     "https://www.youtube.com/@aiexplained-official/videos"),
    ("Matthew Berman",   "https://www.youtube.com/@matthew_berman/videos"),
    ("AI Jason",         "https://www.youtube.com/@AIJasonZ/videos"),
    ("bycloud",          "https://www.youtube.com/@bycloudAI/videos"),
]
PER_CHANNEL = 2
PAUSE = 1.5          # 20 个频道连抓容易被 YouTube 限流，隔一下

def fetch(url, n):
    try:
        r = subprocess.run(
            ["yt-dlp", "--no-update", "--flat-playlist", "--playlist-end", str(n), "-J", url],
            capture_output=True, text=True, timeout=90)
        d = json.loads(r.stdout or "{}")
        return d.get("entries", []) or []
    except Exception as e:
        print(f"  ✗ {url}: {e}")
        return []

items, missed = [], []
for name, url in YT_CHANNELS:
    ents = fetch(url, PER_CHANNEL)
    got = 0
    for e in ents:
        vid = e.get("id")
        if not vid:
            continue
        items.append({
            "name": name, "title": e.get("title", ""),
            "vid": vid, "url": f"https://www.youtube.com/watch?v={vid}",
        })
        got += 1
    print(f"  {name}: {got} 条")
    if got == 0:
        missed.append(name)
    time.sleep(PAUSE)

if missed:
    print(f"⚠ 空手而归 {len(missed)}/{len(YT_CHANNELS)}: {', '.join(missed)}")

if items:                                # yt-dlp 偶发被 YouTube 限流返回 0 → 别用空覆盖上次的好数据
    json.dump({"youtube": items}, open(OUT, "w"), ensure_ascii=False, indent=2)
    print(f"✓ wrote {OUT} — {len(items)} custom videos from {len(YT_CHANNELS)-len(missed)} channels")
else:
    print("⚠ 0 videos（yt-dlp 被限流？）→ 保留上次 custom_feed.json，不覆盖")
