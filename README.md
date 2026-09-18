<div align="center">

**English** · [简体中文](README.zh-CN.md)

# Frontier

### An AI daily, curated from builders — not influencers.

[**Live site**](https://hiamberhuang.github.io/frontier/) · [Setup guide](SETUP.md) · [Full source list](SOURCES.md)

</div>

---

Most AI news is influencers recycling headlines. Frontier follows the people who actually
**build** — researchers, founders, PMs, engineers — and lays their podcasts, posts and writing
out as a magazine you'd actually read. One **Editor's Choice** a day with a one-line reason it
matters, builders tagged by field, real cover images. Not a wall of links.

<div align="center">
<img src="docs/screenshot-site.png" width="760" alt="Frontier daily — magazine-style layout with Editor's Choice and Deep dives">
</div>

## Who it follows

**84 sources across four platforms**, picked by hand. The list *is* the opinion — see every name,
with links and a line on why it's there, in **[`SOURCES.md`](SOURCES.md)**.

| Platform | Count | Status | Edit it in |
|---|---|---|---|
| **YouTube** | 20 | ✅ auto-fetched | [`fetch_sources.py`](fetch_sources.py) → `YT_CHANNELS` |
| **X / Twitter** | 36 | ✅ auto-fetched *(TikHub key)* | [`my_builders.txt`](my_builders.txt) |
| **bilibili** | 12 | ⏳ pending (yt-dlp extractor) | [`SOURCES.md`](SOURCES.md) |
| **Xiaohongshu** | 16 | ⏸ watch list only | [`SOURCES.md`](SOURCES.md) |

A few of the 20 YouTube channels: [Sequoia](https://www.youtube.com/@sequoiacapital/videos) ·
[a16z](https://www.youtube.com/@a16z/videos) · [Y Combinator](https://www.youtube.com/@ycombinator/videos) ·
[Anthropic](https://www.youtube.com/@anthropic-ai/videos) · [Karpathy](https://www.youtube.com/@AndrejKarpathy/videos) ·
[Latent Space](https://www.youtube.com/@LatentSpacePod/videos) · [Lenny's](https://www.youtube.com/@LennysPodcast/videos) ·
[No Priors](https://www.youtube.com/@NoPriorsPodcast/videos) — and on X:
[@karpathy](https://x.com/karpathy) · [@swyx](https://x.com/swyx) · [@simonw](https://x.com/simonw) ·
[@levelsio](https://x.com/levelsio) · [@lennysan](https://x.com/lennysan).

## How it works

Three outputs from one daily run. Everything except the core is optional — turn a layer off and
you lose that output, not the daily.

<div align="center">
<img src="docs/pipeline-obsidian.png" width="900" alt="Frontier pipeline: sources to build to three outputs — GitHub Pages, Obsidian vault, Feishu card">
</div>

| Layer | What you get | Needs | Without it |
|---|---|---|---|
| **Core** | YouTube sources → magazine page | Python 3 + yt-dlp | — |
| X feed | Builders on X, freshest posts | TikHub key *or* follow-builders skill | no "Builders on X" block |
| AI curation | Editor's note + long-video previews | `claude` or `codex` CLI | page still builds, no AI summaries |
| Feishu push | A card in your IM every morning | lark-cli + a Feishu app | read it on the web instead |
| Obsidian | Preview notes into your vault | an Obsidian vault | no notes written |

## Quick start

```bash
git clone https://github.com/hiamberhuang/frontier.git && cd frontier
pip3 install -r requirements.txt          # or: brew install yt-dlp
cp config.example.json config.json
python3 fetch_sources.py && python3 build.py
open index.html
```

No API key and no account needed for that. Then:

```bash
bash install_schedule.sh 10 0             # update itself every day at 10:00
```

Everything personal — paths, IDs, which LLM — lives in `config.json`, which is gitignored.
**You never have to edit code to make this yours.** See [`SETUP.md`](SETUP.md) for the full
walkthrough, including the Feishu and Obsidian integrations.

## Make it yours

Swap the roster in `fetch_sources.py` (YouTube) and `my_builders.txt` (X), drop your own
editorial voice into `EDITOR_NOTES` in `build.py`, rebuild. Deploy anywhere static — GitHub
Pages, Vercel, Netlify.

## Requirements

`yt-dlp` is the only hard dependency. `lark-cli`, `claude` / `codex` are optional CLIs, each
gating one optional layer. Missing ones are detected and skipped — they never break the build.

## Credits

Built by [Amber Huang](https://amberhuang.world/) · AI marketing, building in public.
Source philosophy inspired by Zara Zhang's *Follow Builders, Not Influencers*.
