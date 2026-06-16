# Frontier — your AI daily, curated from builders not influencers

A magazine-style daily reader for AI news. It follows people who **build** —
researchers, founders, PMs, engineers — and presents their podcasts, posts, and
writing as a clean, image-forward daily you actually want to read (think Wired/NYT,
not a Telegram dump).

**Live:** https://7amberhuang.github.io/frontier/

## Why

Most AI news is influencers regurgitating headlines. Frontier is opinionated:
an **Editor's Choice** every day with a one-line "why this matters," builders
tagged by field so you know who's who, and real cover images — not a wall of text.

## Sources

- **Backbone (auto):** the [follow-builders](https://github.com/zarazhangrui/follow-builders)
  central feed by Zara Zhang — 6 AI podcasts + 26 builders on X + lab blogs.
- **Curated additions:** hand-picked YouTube channels and B站 (Bilibili) AI creators.
  See [`SOURCES.md`](SOURCES.md) for the full, opinionated list.

## How it works

`build.py` reads the feeds, pulls real images (YouTube thumbnails, X avatars),
applies builder field tags + Editor's notes, and writes a self-contained
`index.html`. No build system, no deps — just Python stdlib.

```bash
python3 build.py    # → index.html
```

## Make it yours

Fork it, edit `SOURCES.md` with the builders **you** follow, drop your own
Editor's notes in `build.py`, and `python3 build.py`. Deploy anywhere static
(GitHub Pages, Vercel, Netlify).

## 中文版 / Chinese edition

The page is English by default. A **Chinese edition is on the roadmap** — the
layout and pipeline are language-agnostic, so a localized `index.zh.html` (for a
小红书 / 中文 audience) is a straightforward fork. Want it sooner? Open an issue.

## Credits

Built by [Amber Huang](https://amberhuang.world/) · AI marketing, building in public.
Source philosophy inspired by Zara Zhang's *Follow Builders, Not Influencers*.
