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

<details open>
<summary><b>YouTube — all 20 channels</b></summary>

| Category | n | Channels |
|---|---|---|
| **VC firms** | 4 | [Sequoia Capital](https://www.youtube.com/@sequoiacapital/videos) · [a16z](https://www.youtube.com/@a16z/videos) · [Y Combinator](https://www.youtube.com/@ycombinator/videos) · [Redpoint AI](https://www.youtube.com/@redpointai/videos) |
| **AI labs · official** | 5 | [OpenAI](https://www.youtube.com/@OpenAI/videos) · [Anthropic](https://www.youtube.com/@anthropic-ai/videos) · [Google DeepMind](https://www.youtube.com/@googledeepmind/videos) · [HeyGen](https://www.youtube.com/@HeyGen_Official/videos) · [Notion](https://www.youtube.com/@Notion/videos) |
| **Researchers · long-form** | 2 | [Andrej Karpathy](https://www.youtube.com/@AndrejKarpathy/videos) · [Lex Fridman](https://www.youtube.com/@lexfridman/videos) |
| **Podcasts · eng & product** | 4 | [Latent Space](https://www.youtube.com/@LatentSpacePod/videos) · [Lenny's Podcast](https://www.youtube.com/@LennysPodcast/videos) · [No Priors](https://www.youtube.com/@NoPriorsPodcast/videos) · [Uncapped with Jack Altman](https://www.youtube.com/@uncappedpod/videos) |
| **Explainers · breadth** | 5 | [Two Minute Papers](https://www.youtube.com/@TwoMinutePapers/videos) · [AI Explained](https://www.youtube.com/@aiexplained-official/videos) · [Matthew Berman](https://www.youtube.com/@matthew_berman/videos) · [AI Jason](https://www.youtube.com/@AIJasonZ/videos) · [bycloud](https://www.youtube.com/@bycloudAI/videos) |

</details>

<details>
<summary><b>X / Twitter — all 36 builders</b></summary>

| Category | n | Accounts |
|---|---|---|
| **Research / Labs** | 11 | [Andrej Karpathy](https://x.com/karpathy) · [Sam Altman](https://x.com/sama) · [Greg Brockman](https://x.com/gdb) · [Yann LeCun](https://x.com/ylecun) · [Andrew Ng](https://x.com/AndrewYNg) · [Jim Fan](https://x.com/DrJimFan) · [Fei-Fei Li](https://x.com/drfeifei) · [Demis Hassabis](https://x.com/demishassabis) · [Noam Brown](https://x.com/polynoamial) · [Nathan Lambert](https://x.com/natolambert) · [Ethan Mollick](https://x.com/emollick) |
| **Model companies** | 2 | [DeepSeek](https://x.com/deepseek_ai) · [MiniMax](https://x.com/MiniMax__AI) |
| **Founders / product CEOs** | 9 | [Aravind Srinivas](https://x.com/AravSrinivas) · [Amjad Masad](https://x.com/amasad) · [Alexandr Wang](https://x.com/alexandr_wang) · [Clement Delangue](https://x.com/ClementDelangue) · [Harrison Chase](https://x.com/hwchase17) · [Michael Truell](https://x.com/mntruell) · [Guillermo Rauch](https://x.com/rauchg) · [Bret Taylor](https://x.com/btaylor) · [Mira Murati](https://x.com/miramurati) |
| **GTM / growth** | 4 | [Lenny Rachitsky](https://x.com/lennysan) · [Greg Isenberg](https://x.com/gregisenberg) · [Peter Yang](https://x.com/petergyang) · [Pieter Levels](https://x.com/levelsio) |
| **Prolific builders** | 4 | [AK](https://x.com/_akhaliq) · [Mckay Wrigley](https://x.com/mckaywrigley) · [Bilawal Sidhu](https://x.com/bilawalsidhu) · [Riley Brown](https://x.com/rileybrown_ai) |
| **Engineering / writing** | 2 | [swyx](https://x.com/swyx) · [Simon Willison](https://x.com/simonw) |
| **Investors & operators** | 3 | [Garry Tan](https://x.com/garrytan) · [Sarah Guo](https://x.com/saranormous) · [Martin Casado](https://x.com/martin_casado) |
| **Benchmark influencer** | 1 | [Zara Zhang 张咋啦](https://x.com/zarazhangrui) |

</details>

> bilibili (12) and Xiaohongshu (16) are listed in [`SOURCES.md`](SOURCES.md) — neither is auto-fetched yet.

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
