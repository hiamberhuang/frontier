#!/usr/bin/env python3
"""Fetch the latest post from AI product official blogs (RSS, stable + legal).
title + link + og:image → product_feed.json. No login, stdlib only.
Run:  python3 fetch_products.py   (needs proxy for foreign sites)
"""
import urllib.request, json, re, pathlib
from xml.etree import ElementTree as ET

OUT = pathlib.Path(__file__).resolve().parent / "product_feed.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) Frontier/1.0"}

# name → RSS/Atom feed (verified set; edit freely)
SOURCES = [
    ("Anthropic",     "https://www.anthropic.com/rss.xml"),
    ("OpenAI",        "https://openai.com/news/rss.xml"),
    ("Google AI",     "https://blog.google/technology/ai/rss/"),
    ("Hugging Face",  "https://huggingface.co/blog/feed.xml"),
    ("HeyGen",        "https://www.heygen.com/blog/rss.xml"),
]

def get(url, t=15):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t).read()

def og_image(url):
    try:
        h = get(url, 12).decode("utf-8", "ignore")
        for pat in (r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image'):
            m = re.search(pat, h)
            if m:
                return m.group(1)
    except Exception:
        pass
    return ""

items = []
for name, feed in SOURCES:
    try:
        x = ET.fromstring(get(feed))
        it = x.find(".//item")
        if it is not None:                       # RSS
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
        else:                                    # Atom
            ns = {"a": "http://www.w3.org/2005/Atom"}
            e = x.find(".//a:entry", ns)
            title = (e.findtext("a:title", default="", namespaces=ns) or "").strip()
            ln = e.find("a:link", ns)
            link = ln.get("href") if ln is not None else ""
        items.append({"name": name, "title": title[:140], "url": link, "img": og_image(link)})
        print(f"  ✓ {name}: {title[:55]}")
    except Exception as ex:
        print(f"  ✗ {name}: {ex}")

json.dump({"product": items}, open(OUT, "w"), ensure_ascii=False, indent=2)
print(f"✓ {len(items)} product blogs → {OUT}")
