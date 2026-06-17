#!/usr/bin/env python3
"""Frontier — magazine-style AI news daily from follow-builders feeds.
Real images (YouTube maxres thumbnails + X avatars), builder field tags,
Editor's Choice notes. No deps, stdlib only.  Run: python3 build.py
"""
import json, re, html, pathlib

FB = pathlib.Path.home() / ".claude/skills/follow-builders"
OUT = pathlib.Path(__file__).resolve().parent
PORTFOLIO = "https://amberhuang.world/"
TWITTER = "https://x.com/amber168196"   # TODO: swap to @hiamberhuang after rename

# Builder field tags — so readers know who's who (handle -> "field · who")
BUILDER_FIELDS = {
    "karpathy": "AI research & education · ex-OpenAI/Tesla",
    "swyx": "AI engineering · Latent Space",
    "joshwoodward": "Google Labs / Gemini",
    "bcherny": "Claude Code · Anthropic",
    "thsottiaux": "Anthropic",
    "petergyang": "product & AI content",
    "thenanyu": "builder",
    "realmadhuguru": "builder",
    "AmandaAskell": "AI alignment · Anthropic",
    "_catwu": "Claude Code · Anthropic",
    "trq212": "agents · Anthropic",
    "GoogleLabs": "Google Labs · official",
    "amasad": "Replit · CEO",
    "rauchg": "Vercel · CEO",
    "alexalbert__": "developer relations · Anthropic",
    "levie": "Box · CEO",
    "ryolu_": "design · Cursor",
    "garrytan": "Y Combinator · president",
    "mattturck": "VC · FirstMark (MAD landscape)",
    "zarazhangrui": "builder & writer · ex-a16z",
    "nikunj": "operator & investor",
    "steipete": "indie dev · ex-PSPDFKit",
    "danshipper": "Every · CEO (AI workflows)",
    "adityaag": "investor · ex-Dropbox",
    "sama": "OpenAI · CEO",
    "claudeai": "Anthropic · official",
}

# Editor's notes for hero picks (keyed by substring of title). Human-curated = the POV.
EDITOR_NOTES = {
    "Jensen Huang": {
        "note": "Jensen with Sequoia on AI factories and compute as the new industrial base. If you want to grasp why this cycle is 'the largest infrastructure buildout in history' — and where the money flows — start here.",
        "tags": ["Sequoia", "AI infrastructure", "Investing", "Jensen Huang"],
    },
}

CAT = r'''
<div id="pet">
  <svg width="92" height="92" viewBox="0 0 92 92">
    <path id="tail" d="M70 62 q16 -3 13 -24 q-1 -9 -8 -8" fill="none" stroke="#a9aeb6" stroke-width="7" stroke-linecap="round"/>
    <ellipse cx="46" cy="68" rx="23" ry="17" fill="#b8bcc4"/>
    <ellipse cx="36" cy="84" rx="6" ry="4" fill="#a9aeb6"/>
    <ellipse cx="56" cy="84" rx="6" ry="4" fill="#a9aeb6"/>
    <g id="playpaw"><ellipse cx="65" cy="72" rx="6" ry="5" fill="#c6cad1"/></g>
    <polygon id="earL" points="31,29 27,9 43,23" fill="#b8bcc4"/>
    <polygon id="earR" points="61,29 65,9 49,23" fill="#b8bcc4"/>
    <polygon points="32,26 30,15 40,23" fill="#f0b9c4"/>
    <polygon points="60,26 62,15 52,23" fill="#f0b9c4"/>
    <circle cx="46" cy="42" r="19" fill="#b8bcc4"/>
    <g class="eye"><ellipse cx="39" cy="42" rx="5" ry="6.2" fill="#fff"/><circle id="lpupil" cx="39" cy="42" r="3" fill="#2b2b2b"/></g>
    <g class="eye"><ellipse cx="53" cy="42" rx="5" ry="6.2" fill="#fff"/><circle id="rpupil" cx="53" cy="42" r="3" fill="#2b2b2b"/></g>
    <polygon points="46,47 43,50 49,50" fill="#f0a0b0"/>
    <path id="mouthC" d="M41 52 q5 4 10 0" fill="none" stroke="#8a8f97" stroke-width="1.4"/>
    <ellipse id="mouthO" cx="46" cy="53" rx="4" ry="5.5" fill="#e08494"/>
  </svg>
</div>
<style>
#pet{position:fixed;right:16px;bottom:0;z-index:60;width:92px;height:92px;pointer-events:none;filter:drop-shadow(0 3px 6px rgba(0,0,0,.12))}
#tail{transform-box:fill-box;transform-origin:top center;animation:sway 3.2s ease-in-out infinite}
@keyframes sway{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(11deg)}}
.eye{transform-box:fill-box;transform-origin:center;transition:transform .12s}
#pet.blink .eye,#pet.yawn .eye{transform:scaleY(.12)}
#mouthO{opacity:0}
#pet.yawn #mouthO{opacity:1}
#pet.yawn #mouthC{opacity:0}
#earL,#earR{transition:transform .2s;transform-box:fill-box;transform-origin:bottom center}
#pet.alert #earL{transform:rotate(-7deg)}
#pet.alert #earR{transform:rotate(7deg)}
#playpaw{transform-box:fill-box;transform-origin:bottom right}
#pet.play #playpaw{animation:bat .32s ease-in-out 2}
@keyframes bat{0%,100%{transform:rotate(0)}50%{transform:rotate(-38deg) translateY(-6px)}}
</style>
<script>
(function(){var pet=document.getElementById('pet'),lp=document.getElementById('lpupil'),rp=document.getElementById('rpupil');
setInterval(function(){pet.classList.add('blink');setTimeout(function(){pet.classList.remove('blink')},150)},5200);
var lx=0,ly=0,still,pt;
document.addEventListener('mousemove',function(e){
  var r=pet.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height*0.42;
  var dx=e.clientX-cx,dy=e.clientY-cy,d=Math.hypot(dx,dy),a=Math.atan2(dy,dx);
  var px=Math.cos(a)*2.2,py=Math.sin(a)*2.2;
  lp.setAttribute('transform','translate('+px.toFixed(1)+','+py.toFixed(1)+')');
  rp.setAttribute('transform','translate('+px.toFixed(1)+','+py.toFixed(1)+')');
  var near=d<180;pet.classList.toggle('alert',near);
  var moved=Math.hypot(e.clientX-lx,e.clientY-ly);lx=e.clientX;ly=e.clientY;
  if(near&&moved>4){pet.classList.remove('yawn');pet.classList.add('play');clearTimeout(pt);pt=setTimeout(function(){pet.classList.remove('play')},640);}
  clearTimeout(still);
  if(near){still=setTimeout(function(){pet.classList.add('yawn');setTimeout(function(){pet.classList.remove('yawn')},1500);},2600);}
});})();
</script>
'''

def yt_id(url):
    for pat in (r"[?&]v=([\w-]{6,})", r"youtu\.be/([\w-]{6,})", r"/live/([\w-]{6,})", r"/embed/([\w-]{6,})"):
        m = re.search(pat, url or "")
        if m:
            return m.group(1)
    return None

def clean(t, n=300):
    if not t:
        return ""
    t = re.sub(r"Speaker\s*\d+\s*\|\s*[\d:]+\s*-\s*[\d:]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return (t[:n].rsplit(" ", 1)[0] + "…") if len(t) > n else t

def esc(s):
    return html.escape(s or "")

def editor_note(title):
    for k, v in EDITOR_NOTES.items():
        if k in (title or ""):
            return v
    return {}

pods = json.load(open(FB / "feed-podcasts.json")).get("podcasts", [])
xs = json.load(open(FB / "feed-x.json")).get("x", [])
gen = json.load(open(FB / "feed-podcasts.json")).get("generatedAt", "")[:10]

pod_items = []
for p in pods:
    vid = yt_id(p.get("url", ""))
    if not vid:
        continue
    pod_items.append({
        "name": p.get("name", ""), "title": p.get("title", ""), "url": p.get("url", ""),
        "vid": vid, "teaser": clean(p.get("transcript", ""), 320),
    })

# Merge Amber's custom YouTube sources (from fetch_sources.py → custom_feed.json)
_cf = OUT / "custom_feed.json"
if _cf.exists():
    for c in json.load(open(_cf)).get("youtube", []):
        if c.get("vid"):
            pod_items.append({"name": c["name"], "title": c.get("title", ""),
                              "url": c.get("url", ""), "vid": c["vid"], "teaser": ""})

x_items = []
for b in xs:
    tw = (b.get("tweets") or [])
    if not tw:
        continue
    h = b.get("handle", "")
    x_items.append({
        "name": b.get("name", ""), "handle": h, "field": BUILDER_FIELDS.get(h, ""),
        "avatar": f"https://unavatar.io/x/{h}",
        "tweet": clean(tw[0].get("text", ""), 220),
        "url": f"https://x.com/{h}/status/{tw[0].get('id','')}",
    })

hero = pod_items[0] if pod_items else None

# Deep dives: rank the rest by AI-industry relevance, keep top 3
AI_KW = ["ai", " model", "agent", "foundation", "llm", "venture", "gpt", "openai",
         "anthropic", "compute", "gpu", "intelligence", "robot", "frontier", "scal"]
def ai_score(title):
    t = (title or "").lower()
    return sum(t.count(k) for k in AI_KW)
rest_pods = sorted(pod_items[1:], key=lambda p: -ai_score(p["title"]))[:3]

# Builders on X: keep ORIGINAL TECH/AI takes — drop reposts, reactions, and chit-chat.
REACTION_STARTS = ("great post", "this is the most", "this is the best", "counterpoint",
                   "love this", "so true", "exactly", "this.", "100%", "agreed",
                   "well said", "congrats", "amazing", "incredible", "+1")
TECH_KW = ["ai ", "model", "agent", "llm", "gpt", "claude", "token", "prompt", "coding",
           "code", "repo", "product", "build", "ship", "startup", "founder", "open source",
           "compute", "gpu", "inference", "fine-tun", "rag", "eval", "benchmark", " api",
           "subagent", "context", "reasoning", "robot", "chip", "scal", "venture",
           "enterprise", "saas", "research", "training", "dataset", "intelligence"]
CHATTER = ["flight", "weather", "god bless", "good morning", "gm ", "happy birthday",
           "coffee", "weekend", "tired", "jetlag", "airport", "starlink", "wright brothers",
           "vacation", "dinner", "congrats on"]
def tweet_score(tweet):
    t = re.sub(r"https?://\S+", "", tweet).strip()
    low = t.lower()
    if len(t) < 70:                                   # mostly a link / one-liner
        return -10
    if any(low.startswith(s) for s in REACTION_STARTS):  # reaction/repost
        return -10
    if any(c in low for c in CHATTER):                # personal chit-chat
        return -10
    return sum(1 for k in TECH_KW if k in low)        # tech/AI substance
x_items = sorted([b for b in x_items if tweet_score(b["tweet"]) >= 1],
                 key=lambda b: -tweet_score(b["tweet"]))[:6]

def thumb(vid):  # maxres, fall back to hq on error
    return (f'<img src="https://img.youtube.com/vi/{vid}/maxresdefault.jpg" '
            f'onerror="this.src=\'https://img.youtube.com/vi/{vid}/hqdefault.jpg\'" alt="">')

def pod_card(p):
    return f"""<a class="pod" href="{esc(p['url'])}" target="_blank">
      <div class="thumb sm">{thumb(p['vid'])}</div>
      <div><span class="src">{esc(p['name'])}</span><h3>{esc(p['title'])}</h3></div></a>"""

def x_card(b):
    field = f'<div class="field">{esc(b["field"])}</div>' if b["field"] else ""
    return f"""<div class="xc">
      <img loading="lazy" class="av" src="{esc(b['avatar'])}" alt="" onerror="this.style.visibility='hidden'">
      <div><div class="xn">{esc(b['name'])} <span>@{esc(b['handle'])}</span></div>{field}
      <p>{esc(b['tweet'])}</p><a href="{esc(b['url'])}" target="_blank">read on X →</a></div></div>"""

hero_html = ""
if hero:
    ed = editor_note(hero["title"])
    note_html = ""
    if ed.get("note"):
        tags = "".join(f'<span class="edtag">{esc(t)}</span>' for t in ed.get("tags", []))
        note_html = (f'<div class="ednote"><div class="ednote-h"><i class="star">★</i>'
                     f'Editor\'s choice — why this today</div>{esc(ed["note"])}'
                     f'<div class="edtags">{tags}</div></div>')
    hero_html = f"""<a class="hero" href="{esc(hero['url'])}" target="_blank">
      <div class="thumb">{thumb(hero['vid'])}</div>
      <span class="kicker"><i class="star">★</i> Editor's choice · {esc(hero['name'])}</span>
      <h1>{esc(hero['title'])}</h1></a>{note_html}"""

page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Frontier · AI daily</title>
<style>
:root{{--ink:#111;--muted:#666;--line:#e4e2dc;--accent:#b8341a;--bg:#faf9f6}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:880px;margin:0 auto;padding:0 20px 80px}}
a{{color:inherit}}
header{{text-align:center;border-bottom:2px solid var(--ink);padding:30px 0 16px;margin-bottom:36px}}
.mast{{font-family:Georgia,serif;font-size:66px;font-weight:700;letter-spacing:-1px;line-height:1}}
.tag{{font-size:13px;color:var(--muted);margin-top:8px;font-style:italic}}
.byl{{font-size:12px;color:var(--muted);margin-top:8px}}
.byl a{{color:var(--accent);text-decoration:none}}
.thumb img{{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:8px;background:var(--line);display:block}}
.thumb.sm{{width:210px;flex-shrink:0}}
.hero{{display:block;text-decoration:none;margin-bottom:8px}}
.kicker{{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);margin:16px 0 6px;font-weight:600}}
.hero h1{{font-family:Georgia,serif;font-size:40px;line-height:1.12;margin:0;font-weight:700}}
.ednote{{background:#fff;border:1px solid var(--accent);border-left:4px solid var(--accent);padding:14px 18px;margin:16px 0 44px;font-size:15px;line-height:1.6;color:#222;border-radius:8px}}
.ednote-h{{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);font-weight:600;margin-bottom:8px}}
.star{{color:var(--accent);font-style:normal}}
.edtags{{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px}}
.edtag{{font-size:12px;color:var(--accent);background:#f6e7e3;border:0.5px solid #e3b9ae;padding:2px 10px;border-radius:20px}}
.sec{{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);border-bottom:1px solid var(--ink);padding-bottom:6px;margin:0 0 24px;font-weight:600}}
.pods{{display:grid;gap:26px;margin-bottom:48px}}
.pod{{display:flex;gap:18px;text-decoration:none;align-items:start}}
.pod .src{{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);font-weight:600}}
.pod h3{{font-family:Georgia,serif;font-size:21px;line-height:1.25;margin:5px 0 0;font-weight:700}}
.empty{{font-size:14px;color:var(--muted);font-style:italic;margin-bottom:48px}}
.xs{{display:grid;grid-template-columns:1fr 1fr;gap:26px}}
.xc{{display:flex;gap:12px}}
.av{{width:48px;height:48px;border-radius:50%;flex-shrink:0;object-fit:cover;background:var(--line)}}
.xn{{font-weight:600;font-size:15px}}.xn span{{color:var(--muted);font-weight:400}}
.field{{font-size:11px;color:var(--accent);margin:1px 0 5px}}
.xc p{{font-size:14px;line-height:1.55;color:#333;margin:0 0 4px}}
.xc a{{font-size:12px;color:var(--accent);text-decoration:none}}
footer{{text-align:center;border-top:2px solid var(--ink);margin-top:52px;padding-top:20px;font-size:13px;color:var(--muted)}}
footer a{{color:var(--accent);text-decoration:none}}
@media(max-width:640px){{.mast{{font-size:46px}}.hero h1{{font-size:29px}}.pod{{flex-direction:column}}.thumb.sm{{width:100%}}.xs{{grid-template-columns:1fr}}}}
</style></head>
<body><div class="wrap">
<header><div class="mast">Frontier</div>
<div class="tag">AI news, curated from builders — not influencers</div>
<div class="byl">{esc(gen)} · created by <a href="{PORTFOLIO}" target="_blank">Amber Huang</a> · <a href="{TWITTER}" target="_blank">follow on X</a></div></header>
{hero_html}
<div class="sec">Deep dives</div>
{('<div class="pods">' + ''.join(pod_card(p) for p in rest_pods) + '</div>') if rest_pods else '<div class="empty">Quiet feed today — only the Editor\'s choice above. More as builders publish.</div>'}
<div class="sec">Builders on X</div>
<div class="xs">{''.join(x_card(b) for b in x_items)}</div>
<footer>Pick your own builders. Read AI like a magazine.<br>
<a href="https://github.com/7amberhuang/frontier" target="_blank">fork it on GitHub</a> · <a href="{TWITTER}" target="_blank">@amber</a> · <a href="manual.html">how to file this in Obsidian</a></footer>
</div>{CAT}</body></html>"""

(OUT / "index.html").write_text(page, encoding="utf-8")
print(f"✓ built {OUT/'index.html'}  | {len(pod_items)} podcasts, {len(x_items)} builders ({sum(1 for b in x_items if b['field'])} tagged)")
