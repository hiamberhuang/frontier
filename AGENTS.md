# AGENTS.md — set up Frontier's daily agent from zero

> **You are an AI coding agent (Claude Code / Codex / Cursor / …).** A user handed you
> this repo and said *"set this up so I get a daily AI-news digest in my Feishu."*
> This file is your runbook. Follow it top to bottom. Everything degrades gracefully:
> the **only hard requirement is Python 3 + yt-dlp + you (an LLM CLI)**. Feishu,
> Obsidian, and the X/Twitter feed are optional add-ons — skip any the user lacks.

## What you're building

A cron job that, once a day:
1. **Fetches** today's AI-builder content (YouTube/podcasts via `yt-dlp`; optionally
   official product accounts on X via TikHub).
2. **Builds** a magazine-style `index.html` (`build.py`, pure stdlib) and pushes it to
   GitHub Pages.
3. **Pre-reads the long videos for the user**: grabs auto-captions and has *you* (the
   LLM) distill each into a "should I spend an hour on this?" preview.
4. **Pushes a digest to Feishu** — summary + a link — so the user reads the preview
   first and only then decides what to watch.

## Prerequisites — check, install what's missing, skip what's optional

| Need | Required? | Check | If missing |
|---|---|---|---|
| Python 3.9+ | ✅ | `python3 --version` | install via the OS package manager |
| yt-dlp | ✅ | `yt-dlp --version` | `pip install -U yt-dlp` (or brew) |
| git + a GitHub repo | ✅ (for the public site) | `git remote -v` | `gh repo create` and enable Pages, OR run site-only locally |
| An LLM CLI you can call headless | ✅ | you are it | the digest step calls `claude -p "<prompt>"`; if the user's CLI differs, edit `digest_videos.py`'s `CLAUDE` + `summarize()` to shell out to their CLI |
| Feishu push (`lark-cli`) | ⬜ optional | `lark-cli --version` | if absent, the digest still prints to stdout/log; wire the user's own notifier |
| TikHub key (X official accounts) | ⬜ optional | `cat .tikhub_key` | skip — `build.py` just omits the "Product posts" row |
| Obsidian vault | ⬜ optional | — | if the user has none, point `digest_videos.py`'s `BRAIN`/`OUTDIR` at any local folder; the preview becomes a plain markdown file |

> ⚠️ **Never commit secrets.** `.tikhub_key`, `.daily.log`, and the `*_feed.json`
> caches are already in `.gitignore`. Keep it that way. Do not paste any key into chat.

## Setup steps (run these, reporting each result to the user)

```bash
# 0. from the repo root
python3 build.py                 # sanity: should write index.html with no deps

# 1. pick the sources the user actually wants
#    edit SOURCES.md + the channel lists in fetch_sources.py (YouTube) and
#    fetch_x_products.py (X handles). Defaults follow Zara Zhang's follow-builders feed.

# 2. (optional) Feishu: install lark-cli, log the user in, get their open_id,
#    then set LARK + --user-id in frontier_daily.sh. Test with one message first.

# 3. (optional) TikHub: user pastes their key once -> echo 'KEY' > .tikhub_key
#    then: python3 fetch_x_products.py   # verifies handles resolve

# 4. dry-run the whole thing ONCE, watching output:
bash frontier_daily.sh           # fetch -> build -> push -> digest -> Feishu

# 5. schedule it daily (macOS launchd example; use cron/systemd elsewhere):
#    a launchd plist running `bash <repo>/frontier_daily.sh` at 10:00 local.
```

## The files

- `fetch_sources.py` — yt-dlp pulls latest from curated YouTube channels → `custom_feed.json`
- `fetch_x_products.py` — TikHub pulls latest post from AI product X accounts → `product_feed.json` *(optional)*
- `build.py` — renders everything into a self-contained `index.html` (stdlib only)
- `digest_videos.py` — captions → LLM distills a **预习/preview** per long video → writes a daily note + prints a Feishu-ready summary
- `frontier_daily.sh` — the orchestrator the cron calls
- `SOURCES.md` — the opinionated source list to edit
- `manual.html` — reader-facing "how to file this in your notes" page

## Graceful-degradation summary (for a Feishu-only user)

- No TikHub key → no X "Product posts" row. Everything else works.
- No Obsidian → previews land in a plain local markdown folder; the Feishu message
  still carries the summary.
- No GitHub Pages → run `build.py` and open `index.html` locally; skip the `git push`
  lines in `frontier_daily.sh`.
- Different LLM CLI → change the one `subprocess.run([CLAUDE, "-p", prompt], …)` call
  in `digest_videos.py` to invoke theirs.

The irreducible core that *always* works: **fetch AI-builder videos → you summarize
them → deliver the summary to the user.** Build out from there.
