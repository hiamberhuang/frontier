#!/usr/bin/env python3
"""Frontier daily as a RICH multi-column Feishu card — like a magazine spread:
each Deep-dive video is a column (cover thumbnail + title + source + AI one-line preview
+ 看视频 button), then bottom buttons (看完整日报 / 看预习笔记).
Run after digest_videos.py + build.py.
"""
import json, re, subprocess, datetime, urllib.request, pathlib, math

HERE = pathlib.Path(__file__).resolve().parent
OID = "ou_e71b8550edc0acc975ef9682aa3a0bc6"
LARK = str(pathlib.Path.home() / ".local/share/fnm/node-versions/v24.15.0/installation/bin/lark-cli")
NOTE = (pathlib.Path.home() / "Documents/Brain/wiki/行业通用/每日预习"
        / f"{datetime.date.today().isoformat()}.md")
SITE = "https://hiamberhuang.github.io/frontier/"
today = datetime.date.today().isoformat()


def blocks():
    """逐节解析预习笔记 → [(title, src, one)]，避免跨节误匹配。"""
    if not NOTE.exists():
        return []
    t = NOTE.read_text(encoding="utf-8")
    out = []
    for sec in re.split(r"(?=^## )", t, flags=re.M):
        if not sec.startswith("## "):
            continue
        title = sec.splitlines()[0][3:].split("|")[0].strip()
        ms = re.search(r"^\*(.+?)\*\s*·", sec, re.M)
        src = ms.group(1).strip() if ms else ""
        m = (re.search(r"🎯\s*\*\*一句话\*\*[：:]\s*(\S.*)", sec)
             or re.search(r"🎯\s*\*\*一句话\*\*[：:]?\s*\n+\s*(\S.*)", sec))
        out.append((title, src, m.group(1).strip() if m else ""))
    return out


def _dw(s):
    """显示宽度：CJK/全角 ≈ 2，拉丁/数字 ≈ 1。"""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def trim_w(s, max_units=34):
    """按显示宽度截断（≈2 行），尽量在标点/空格断 + …。"""
    s = (s or "").strip()
    if _dw(s) <= max_units:
        return s
    out, w = "", 0
    for c in s:
        cw = 2 if ord(c) > 0x2E80 else 1
        if w + cw > max_units - 1:          # 留位给 …
            break
        out += c; w += cw
    for p in ("。", "——", "，", "、", " "):
        i = out.rfind(p)
        if i >= len(out) * 0.5:
            out = out[:i]; break
    return out.rstrip("，、—— ") + "…"


CAP = 18            # 3 列宽屏卡片：每列每行大致容纳的显示宽度（经验值）
ZWS = "​"      # 零宽空格，用来垫“看不见但不会被折叠”的空行


def _nlines(s):
    return max(1, math.ceil(_dw(s) / CAP))


def upload_thumb(vid):
    """下载 YouTube 缩略图 → 上传飞书拿 image_key（失败返回 ''，卡片自动退化为纯文字列）。"""
    p = HERE / f"_t_{vid}.jpg"
    try:
        for q in ("maxresdefault", "mqdefault"):   # 都是 16:9，避免 4:3 的 hqdefault 撑高某列
            try:
                urllib.request.urlretrieve(f"https://img.youtube.com/vi/{vid}/{q}.jpg", p)
                if p.stat().st_size > 3000:
                    break
            except Exception:
                continue
        r = subprocess.run([LARK, "im", "images", "create", "--file", f"image={p.name}",
                            "--data", '{"image_type":"message"}', "--as", "bot"],
                           cwd=HERE, capture_output=True, text=True, timeout=40)
        return (json.loads(r.stdout).get("data") or {}).get("image_key", "")
    except Exception:
        return ""
    finally:
        p.unlink(missing_ok=True)


bs = blocks()
preview_by_title = {t: one for t, s, one in bs}

# Deep-dive 视频（custom_feed 每频道一条，前 3 列）
vids, seen = [], set()
cf = HERE / "custom_feed.json"
if cf.exists():
    for v in json.load(open(cf)).get("youtube", []):
        if v.get("name") in seen:
            continue
        seen.add(v["name"]); vids.append(v)
    vids = vids[:3]

# 第一遍：抓数据 + 按显示宽度截断 + 估算每列内容行数
rows = []
for v in vids:
    ttl = v.get("title", "").split("|")[0].strip()
    one = preview_by_title.get(ttl) or next(
        (preview_by_title[t] for t in preview_by_title if ttl[:16] in t or t[:16] in ttl), "")
    ik = upload_thumb(v["vid"])
    yurl = f"https://www.youtube.com/watch?v={v['vid']}"
    ttl_t = trim_w(ttl, 34)                          # 标题 ≤ 2 行
    desc_str = trim_w(one, 52) if one else ZWS       # 预习 ≤ 3 行；无预习占 1 行（垫平逻辑负责对齐，可放宽保留内容）
    content_lines = _nlines(ttl_t) + 1 + _nlines(desc_str)   # 标题 + 来源(1) + 预习
    rows.append((ttl_t, v.get("name", ""), desc_str, yurl, ik, content_lines))

# 第二遍：垫平到最高列 → 三个「看视频」落同一行
M = max((r[5] for r in rows), default=0)
cols = []
for ttl_t, name, desc_str, yurl, ik, cl in rows:
    elems = []
    if ik:
        elems.append({"tag": "img", "img_key": ik, "alt": {"tag": "plain_text", "content": ""},
                      "mode": "fit_horizontal"})
    body = f"[**{ttl_t}**]({yurl})\n_{name}_\n\n{desc_str}"
    body += ("\n" + ZWS) * (M - cl)                  # 补隐形空行，垫平高度
    body += f"\n\n[▶ 看视频]({yurl})"
    elems.append({"tag": "div", "text": {"tag": "lark_md", "content": body}})
    cols.append({"tag": "column", "width": "weighted", "weight": 1,
                 "vertical_align": "top", "elements": elems})

_pdu = HERE / ".preview_doc_url"
preview_url = _pdu.read_text(encoding="utf-8").strip() if _pdu.exists() else SITE
_WD = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.date.today().weekday()]
func = f"**{today} · {_WD}**"
q = {}
_qf = HERE / ".quote.json"
if _qf.exists():
    try:
        q = json.load(open(_qf))
    except Exception:
        q = {}
# 顶部「今日金句」= 真·当日最火 builder 推文：金句→点进推文，作者→点进主页关注
if q.get("quote"):
    h, tid = q.get("handle", ""), q.get("tweet_id", "")
    qtxt = f"[“{q['quote']}”](https://x.com/{h}/status/{tid})" if (h and tid) else f"“{q['quote']}”"
    auth = f"[{q['author']}](https://x.com/{h})" if h else q['author']
    intro = f"💬 *{qtxt}* —— **{auth}**\n\n{func}"
else:
    intro = func

card = {
    "config": {"wide_screen_mode": True},
    "header": {"template": "red",
               "title": {"tag": "plain_text", "content": "📰 Frontier · 今日 AI 日报"}},
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": intro}},
    ] + ([{"tag": "column_set", "flex_mode": "stretch", "columns": cols}] if cols else []) + [
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
subs = HERE / ".subscribers"
recips = ([l.strip() for l in subs.read_text(encoding="utf-8").splitlines()
           if l.strip() and not l.startswith("#")] if subs.exists() else [OID])
for rid in recips:
    flag = "--chat-id" if rid.startswith("oc_") else "--user-id"
    r = subprocess.run([LARK, "im", "+messages-send", flag, rid,
                        "--msg-type", "interactive", "--content", content, "--as", "bot"],
                       capture_output=True, text=True)
    ok = '"message_id"' in r.stdout
    print(f"  {'✓' if ok else '✗'} {rid}: {(r.stdout or r.stderr).strip()[:120]}")
