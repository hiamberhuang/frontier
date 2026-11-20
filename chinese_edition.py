#!/usr/bin/env python3
"""Render a Chinese Frontier edition and its Feishu card from one ranked list."""
import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

TITLE = "📰 Frontier · 今日 AI 日报"
SHORT_LIMIT = 3
FULL_LIMIT = 10


def https_url(value):
    if not isinstance(value, str) or re.search(r'[\s<>()]', value):
        return False
    parts = urlsplit(value)
    return parts.scheme == "https" and bool(parts.hostname) and not parts.username


def load_edition(path):
    edition = json.loads(Path(path).read_text(encoding="utf-8"))
    edition["date"] = date.fromisoformat(edition["date"]).isoformat()
    for key in ("coverage", "selection"):
        if not isinstance(edition[key], str) or not edition[key].strip():
            raise ValueError(f"{key} is required")
    stories = edition["stories"]
    if not 1 <= len(stories) <= FULL_LIMIT:
        raise ValueError("An edition needs 1–10 verified stories")
    seen_posts = set()
    for story in stories:
        for key in ("title", "summary", "insight"):
            if not isinstance(story[key], str) or not story[key].strip():
                raise ValueError(f"Each story needs a {key}")
        post_url = story["post_url"]
        if (not https_url(post_url) or urlsplit(post_url).hostname not in ("x.com", "twitter.com")
                or not re.fullmatch(r"/[^/]+/status/\d+", urlsplit(post_url).path)):
            raise ValueError("Each story needs an X post URL")
        post_id = urlsplit(post_url).path.rsplit("/", 1)[1]
        if post_id in seen_posts:
            raise ValueError("X posts must be unique in an edition")
        seen_posts.add(post_id)
        if story.get("source_url") and not https_url(story["source_url"]):
            raise ValueError("Official source URLs must use HTTPS")
    videos = edition["videos"]
    if len(videos) > 3:
        raise ValueError("The card supports up to three YouTube videos")
    for video in videos:
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video["id"]):
            raise ValueError("Invalid YouTube video ID")
        for key in ("title", "channel", "note"):
            if not isinstance(video[key], str) or not video[key].strip():
                raise ValueError(f"Each video needs a {key}")
    return edition


def watch_url(video):
    return f"https://www.youtube.com/watch?v={video['id']}"


def md_text(value):
    # Treat source-derived text as plain text inside Feishu's markdown fields.
    return re.sub(r"([\\\[\]_*~`<>])", r"\\\1", " ".join(value.split()))


def card_payload(edition, full_url, upload_thumb, *, preview_url=None):
    if not https_url(full_url):
        raise ValueError("Use a live HTTPS URL for the full edition")
    if preview_url and not https_url(preview_url):
        raise ValueError("Use an HTTPS URL for the preview notes")

    def markdown(content):
        return {"tag": "div", "text": {"tag": "lark_md", "content": content}}

    top = edition["stories"][:SHORT_LIMIT]
    elements = [
        markdown(f"<font color='grey'>{edition['date']}　·　{md_text(edition['coverage'])}</font>"),
        markdown(f"**北美 X 热点 · Top {len(top)}**"),
    ]
    for rank, story in enumerate(top, 1):
        title = md_text(story.get("card_title") or story["title"])
        summary = md_text(story.get("card_summary") or story["summary"])
        elements.append({
            "tag": "column_set",
            "flex_mode": "none",
            "background_style": "grey",
            "columns": [
                {"tag": "column", "width": "auto", "vertical_align": "top",
                 "elements": [markdown(f"<font color='red'>**{rank:02d}**</font>")]},
                {"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "top",
                 "elements": [markdown(f"**{title}**\n<font color='grey'>{summary}</font>")]},
                {"tag": "column", "width": "auto", "vertical_align": "top",
                 "elements": [markdown(f"[原帖 ↗]({story['post_url']})")]},
            ],
        })
    columns = []
    for video in edition["videos"]:
        image_key = upload_thumb(video["id"])
        parts = [{"tag": "img", "img_key": image_key, "mode": "fit_horizontal",
                  "alt": {"tag": "plain_text", "content": video["title"]}}] if image_key else []
        parts.extend([
            markdown(f"**{md_text(video['title'])}**\n{md_text(video['channel'])}"),
            markdown(f"[▶ 看视频]({watch_url(video)})"),
        ])
        columns.append({"tag": "column", "width": "weighted", "weight": 1,
                        "vertical_align": "top", "elements": parts})
    if columns:
        elements.extend([{"tag": "hr"}, markdown("**YouTube 推荐**"),
                         {"tag": "column_set", "flex_mode": "stretch", "columns": columns}])
    actions = [{"tag": "button", "type": "primary", "url": full_url,
                "text": {"tag": "plain_text", "content": f"看完整日报 · Top {len(edition['stories'])}"}}]
    if columns and preview_url:
        actions.append({"tag": "button", "type": "default", "url": preview_url,
                        "text": {"tag": "plain_text", "content": "看预习笔记"}})
    elements.extend([{"tag": "hr"}, {"tag": "action", "actions": actions}])
    return {"config": {"wide_screen_mode": True},
            "header": {"template": "red", "title": {"tag": "plain_text", "content": TITLE}},
            "elements": elements}


def story_html(story, rank, full):
    title = story["title"] if full else story.get("card_title") or story["title"]
    summary = story["summary"] if full else story.get("card_summary") or story["summary"]
    extra = ""
    if full:
        extra += f'<p class="insight"><strong>为什么值得看</strong> {escape(story["insight"])}</p>'
    link_label = "看 X 原帖 ↗" if full else "原帖 ↗"
    links = f'<a href="{escape(story["post_url"])}">{link_label}</a>'
    if full and story.get("source_url"):
        links += f'<a href="{escape(story["source_url"])}">看官方资料 ↗</a>'
    details = f'<h3>{escape(title)}</h3><p>{escape(summary)}</p>{extra}'
    source_links = f'<div class="links">{links}</div>'
    content = f'<div>{details}{source_links}</div>' if full else f'<div>{details}</div>{source_links}'
    return (f'<li id="story-{rank}"><span class="rank" aria-hidden="true">{rank:02}</span>'
            f'{content}</li>')


def videos_html(videos, full):
    cards = []
    for video in videos:
        vid = video["id"]
        note = f'<p>{escape(video["note"])}</p>' if full else ""
        cards.append(
            f'<article class="video"><a href="{watch_url(video)}" aria-label="{escape(video["title"])}">'
            f'<img src="https://i.ytimg.com/vi/{vid}/mqdefault.jpg" width="320" height="180" alt=""></a>'
            f'<div><h3>{escape(video["title"])}</h3><span>{escape(video["channel"])}</span>{note}'
            f'<a href="{watch_url(video)}">▶ 看视频</a></div></article>'
        )
    return ('<section id="videos"><h2>YouTube 推荐</h2><div class="videos">'
            + "".join(cards) + '</div></section>') if cards else ""


def render(edition, css, full, article_name):
    stories = edition["stories"] if full else edition["stories"][:SHORT_LIMIT]
    body = "".join(story_html(story, rank, full) for rank, story in enumerate(stories, 1))
    notes = f'<p class="selection">{escape(edition["selection"])}</p>' if full else ""
    footer = ""
    if not full:
        link = escape(article_name)
        actions = f'<a class="primary" href="{link}">📖 看完整日报 · Top {len(edition["stories"])}</a>'
        if edition["videos"]:
            actions += f'<a href="{link}#videos">🧠 看预习笔记</a>'
        footer = f'<footer>{actions}</footer>'
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE} · {edition['date']}</title><style>{css}</style></head>
<body class="{'full' if full else 'preview'}"><main>
<header><h1>{TITLE}</h1></header>
<div class="content">
<p class="date"><time datetime="{edition['date']}">{edition['date']}</time><span>{escape(edition['coverage'])}</span></p>
<section aria-labelledby="hotspots"><h2 id="hotspots">X（Twitter）热点 <small>TOP {len(stories)}</small></h2>
{notes}<ol class="stories">{body}</ol></section>
{videos_html(edition['videos'], full)}
{footer}</div></main></body></html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edition", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    edition = load_edition(args.edition)
    css = Path(__file__).with_suffix(".css").read_text(encoding="utf-8")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    article_name = edition["date"] + ".html"
    for full, filename in ((True, article_name), (False, "group-card.html")):
        path = args.output_dir / filename
        path.write_text(render(edition, css, full, article_name), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
