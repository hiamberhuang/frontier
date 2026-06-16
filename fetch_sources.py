#!/usr/bin/env python3
"""Fetch latest videos from Amber's custom YouTube channels via yt-dlp.
Writes custom_feed.json (cached) so build.py stays fast. Run before build.py.
B站 pending: yt-dlp bilibili extractor currently broken (NoneType) — TODO.
"""
import json, subprocess, pathlib

OUT = pathlib.Path(__file__).resolve().parent / "custom_feed.json"

# Amber's curated YouTube additions (name -> channel handle URL)
YT_CHANNELS = [
    ("Lenny's Podcast", "https://www.youtube.com/@LennysPodcast/videos"),
    ("a16z", "https://www.youtube.com/@a16z/videos"),
    ("Uncapped", "https://www.youtube.com/@uncappedpod/videos"),
]
PER_CHANNEL = 2

def fetch(url, n):
    try:
        r = subprocess.run(
            ["yt-dlp", "--flat-playlist", "--playlist-end", str(n), "-J", url],
            capture_output=True, text=True, timeout=90)
        d = json.loads(r.stdout or "{}")
        return d.get("entries", []) or []
    except Exception as e:
        print(f"  ✗ {url}: {e}")
        return []

items = []
for name, url in YT_CHANNELS:
    ents = fetch(url, PER_CHANNEL)
    for e in ents:
        vid = e.get("id")
        if not vid:
            continue
        items.append({
            "name": name, "title": e.get("title", ""),
            "vid": vid, "url": f"https://www.youtube.com/watch?v={vid}",
        })
    print(f"  {name}: {len([e for e in ents if e.get('id')])} 条")

json.dump({"youtube": items}, open(OUT, "w"), ensure_ascii=False, indent=2)
print(f"✓ wrote {OUT} — {len(items)} custom videos")
