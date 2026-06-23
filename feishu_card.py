#!/usr/bin/env python3
"""Build + send today's Frontier digest as a Feishu interactive card
(header bar + per-video preview + buttons). Reads the daily 预习 note.
Run by frontier_daily.sh after digest_videos.py.
"""
import json, re, subprocess, datetime, urllib.parse, pathlib

OID = "ou_e71b8550edc0acc975ef9682aa3a0bc6"
LARK = str(pathlib.Path.home() / ".local/share/fnm/node-versions/v24.15.0/installation/bin/lark-cli")
NOTE = (pathlib.Path.home() / "Documents/Brain/wiki/行业通用/每日预习"
        / f"{datetime.date.today().isoformat()}.md")
SITE = "https://hiamberhuang.github.io/frontier/"

def blocks():
    """逐节解析预习笔记，避免跨节误匹配；「一句话」文字在冒号后或下一行都能抓。"""
    if not NOTE.exists():
        return []
    t = NOTE.read_text(encoding="utf-8")
    out = []
    for sec in re.split(r"(?=^## )", t, flags=re.M):
        if not sec.startswith("## "):
            continue
        title = sec.splitlines()[0][3:].split("|")[0].strip()
        ms = re.search(r"^\*(.+?)\*\s*·", sec, re.M)          # *来源* · [看视频]
        src = ms.group(1).strip() if ms else ""
        m = (re.search(r"🎯\s*\*\*一句话\*\*[：:]\s*(\S.*)", sec)        # 冒号后同行
             or re.search(r"🎯\s*\*\*一句话\*\*[：:]?\s*\n+\s*(\S.*)", sec))  # 或下一行
        one = m.group(1).strip() if m else ""
        if title:
            out.append((title, src, one))
    return out

bs = blocks()
today = datetime.date.today().isoformat()
ob = "obsidian://open?vault=Brain&file=" + urllib.parse.quote(f"wiki/行业通用/每日预习/{today}")
# 「看预习笔记」优先指向 digest 生成的飞书文档（订阅者不用装 Obsidian 也能看）；没有再退回 Obsidian
_pdu = pathlib.Path(__file__).resolve().parent / ".preview_doc_url"
preview_url = _pdu.read_text(encoding="utf-8").strip() if _pdu.exists() else ob

# card body —— 永远有内容：列今日深度视频（custom_feed 每频道一条），有预习就带一句话
preview_by_title = {t: one for t, s, one in bs}
vids, seen = [], set()
_cf = pathlib.Path(__file__).resolve().parent / "custom_feed.json"
if _cf.exists():
    for v in json.load(open(_cf)).get("youtube", []):
        if v.get("name") in seen:
            continue
        seen.add(v["name"]); vids.append(v)
    vids = vids[:4]

head = (f"**{today}** · AI 已替你读完 **{len(bs)}** 条长视频，先看预习再决定深看 👇"
        if bs else f"**{today}** · 今日 AI 日报已更新，下面是今日深度 👇")
lines = [head]
for v in vids:
    ttl = v.get("title", "").split("|")[0].strip()
    one = preview_by_title.get(ttl) or next(
        (preview_by_title[t] for t in preview_by_title if ttl[:16] in t or t[:16] in ttl), "")
    blk = f"\n**{ttl}**  ·  _{v.get('name','')}_"
    if one:
        blk += f"\n{one}"
    lines.append(blk)
md = "\n".join(lines) if vids else f"**{today}** · 今日 AI 日报已更新 → 点下方看完整日报。"

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "template": "red",
        "title": {"tag": "plain_text", "content": "📰 Frontier · 今日 AI 日报"},
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": md}},
        {"tag": "hr"},
        {"tag": "action", "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": "📖 看完整日报"},
             "type": "primary", "url": SITE},
            {"tag": "button", "text": {"tag": "plain_text", "content": "🧠 看预习笔记"},
             "type": "primary", "url": preview_url},
        ]},
    ],
}

content = json.dumps(card, ensure_ascii=False)
# 收件人：.subscribers（每行一个 ou_（用户）或 oc_（群）；# 注释）；默认只发给 Amber 自己
subs = pathlib.Path(__file__).resolve().parent / ".subscribers"
recips = ([l.strip() for l in subs.read_text(encoding="utf-8").splitlines()
           if l.strip() and not l.startswith("#")] if subs.exists() else [OID])
for rid in recips:
    flag = "--chat-id" if rid.startswith("oc_") else "--user-id"
    r = subprocess.run([LARK, "im", "+messages-send", flag, rid,
                        "--msg-type", "interactive", "--content", content, "--as", "bot"],
                       capture_output=True, text=True)
    ok = '"message_id"' in r.stdout
    print(f"  {'✓' if ok else '✗'} {rid}: {(r.stdout or r.stderr).strip()[:140]}")
