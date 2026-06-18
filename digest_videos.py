#!/usr/bin/env python3
"""Pre-read the day's long videos so Amber reads a 预习 before deciding to watch.
For each Deep-dive YouTube video: grab auto-captions (fast, no whisper) →
claude distills a knowledge-ified preview → write one daily note into Brain.
Prints a short Feishu-ready preview to stdout. Run after build.py.
"""
import json, subprocess, pathlib, tempfile, re, datetime, urllib.parse, time

HERE = pathlib.Path(__file__).resolve().parent
BRAIN = pathlib.Path.home() / "Documents/Brain"
OUTDIR = BRAIN / "wiki/行业通用/每日预习"
CLAUDE = str(pathlib.Path.home() / ".local/bin/claude")
MAX = 4
TODAY = datetime.date.today().isoformat()

def captions(vid):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["yt-dlp", "--skip-download", "--write-auto-subs",
                        "--sub-lang", "en.*", "--sub-format", "vtt",
                        "-o", f"{d}/%(id)s.%(ext)s",
                        f"https://www.youtube.com/watch?v={vid}"],
                       capture_output=True, timeout=150)
        vtts = sorted(pathlib.Path(d).glob("*.vtt"), key=lambda p: ("orig" in p.name))
        if not vtts:
            return ""
        return clean_vtt(vtts[0].read_text(encoding="utf-8", errors="ignore"))

def clean_vtt(t):
    out = []
    for ln in t.splitlines():
        if "-->" in ln or ln.strip().isdigit() or ln.startswith(("WEBVTT", "Kind:", "Language:")) or not ln.strip():
            continue
        ln = re.sub(r"<[^>]+>", "", ln).strip()
        if ln and (not out or out[-1] != ln):
            out.append(ln)
    return " ".join(out)

def summarize(name, title, transcript):
    prompt = f"""这是一个 AI 长视频的字幕转写。给 Amber 做"预习总结"——让她不用看完一小时就知道重点，再决定要不要深看。

来源：{name} · {title}

输出（中文，知识化、体系化，像拆解 case 那样，别寒暄）：
🎯 **一句话**：bottom line
📌 **核心观点/框架**（3-5 条，凝练有信息量，能用图标/短语就别长句）
👤 **谁该看 / 重点在哪**
⏱️ **要不要花一小时**：值看 / 选看 / 跳过 + 一句理由

字幕（可能有口语错字，按上下文理解）：
{transcript[:14000]}"""
    for attempt in range(3):              # 重试：claude -p 偶发空/超时，别让视频被静默丢掉
        try:
            r = subprocess.run([CLAUDE, "-p", prompt], capture_output=True, text=True,
                               timeout=300, stdin=subprocess.DEVNULL)
            out = r.stdout.strip()
            if out:
                return out
            print(f"     (claude 空，重试 {attempt+1}/3：{r.stderr.strip()[:120]})")
        except subprocess.TimeoutExpired:
            print(f"     (claude 超时，重试 {attempt+1}/3)")
        time.sleep(3)
    return ""

_all = json.load(open(HERE / "custom_feed.json")).get("youtube", [])
_seen, vids = set(), []
for v in _all:                       # 每频道取一条，去重
    if v["name"] in _seen:
        continue
    _seen.add(v["name"])
    vids.append(v)
vids = vids[:MAX]
OUTDIR.mkdir(parents=True, exist_ok=True)
blocks, feishu = [], []
for v in vids:
    tr = captions(v["vid"])
    if len(tr) < 400:
        print(f"  ✗ {v['name']}: 无字幕/太短，跳过")
        continue
    s = summarize(v["name"], v["title"], tr)
    if not s:
        print(f"  ✗ {v['name']}: 总结失败")
        continue
    url = f"https://www.youtube.com/watch?v={v['vid']}"
    blocks.append(f"## {v['title']}\n*{v['name']}* · [▶ 看视频]({url})\n\n{s}\n")
    bl = next((l for l in s.splitlines() if "一句话" in l or "🎯" in l), s[:80])
    feishu.append(f"· {v['name']}：{re.sub(r'[*🎯]', '', bl).replace('一句话','').strip(': ：')[:60]}")
    print(f"  ✓ {v['name']} 预习完成")

note = OUTDIR / f"{TODAY}.md"
front = f"---\ntitle: 每日预习 {TODAY}\ncategory: synthesis\ntags: [general-ai, ai-workflow]\ndate: {TODAY}\n---\n\n# 📖 每日预习 · {TODAY}\n\n> AI 已帮你读完今天的长视频。先看这个再决定要不要花一小时沉浸看。\n\n"
note.write_text(front + "\n---\n\n".join(blocks) + "\n\n→ 回 [[输入体系]]", encoding="utf-8")
subprocess.run(["git", "-C", str(BRAIN), "add", "-A"], capture_output=True)
subprocess.run(["git", "-C", str(BRAIN), "commit", "-q", "-m", f"每日预习 {TODAY}"], capture_output=True)

# Feishu-ready preview + obsidian deep link
rel = f"wiki/行业通用/每日预习/{TODAY}"
ob = "obsidian://open?vault=Brain&file=" + urllib.parse.quote(rel)
print("---FEISHU---")
print(f"📖 今日预习已写进 Obsidian（{len(blocks)} 条长视频，AI 已读完）：\n" + "\n".join(feishu) + f"\n\n先看预习再决定要不要深看 → {ob}")
