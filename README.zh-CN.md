<div align="center">

[English](README.md) · **简体中文**

# Frontier

### 一份 AI 日报 —— 只跟造东西的人，不跟蹭热点的人。

[**在线看**](https://hiamberhuang.github.io/frontier/) · [部署指南](SETUP.md) · [完整信源清单](SOURCES.md)

</div>

---

市面上的 AI 资讯，大多是网红在倒腾同一批标题。Frontier 只跟**真在造东西的人** —— 研究员、创始人、
产品、工程师 —— 把他们的播客、推文和长文，排成一份你真会读完的杂志。每天一条 **Editor's Choice**，
配一句「为什么现在值得看」，每个 builder 标注领域，配真封面图。不是一堆链接堆在一起。

<div align="center">
<img src="docs/screenshot-site.png" width="760" alt="Frontier 日报页面 —— 杂志式排版，含 Editor's Choice 与 Deep dives">
</div>

## 跟了谁

**四个平台 84 个信源**，全部手挑。名单本身就是观点 —— 每个名字、链接、以及为什么在名单里，
都在 **[`SOURCES.md`](SOURCES.md)**。

| 平台 | 数量 | 抓取状态 | 改哪个文件 |
|---|---|---|---|
| **YouTube** | 20 | ✅ 全量自动抓取 | [`fetch_sources.py`](fetch_sources.py) → `YT_CHANNELS` |
| **X / Twitter** | 36 | ✅ 自动抓取（需 TikHub key） | [`my_builders.txt`](my_builders.txt) |
| **bilibili** | 12 | ⏳ 待接入（yt-dlp 抽取器待修） | [`SOURCES.md`](SOURCES.md) |
| **小红书** | 16 | ⏸ 仅作关注 / 选题池 | [`SOURCES.md`](SOURCES.md) |

<details open>
<summary><b>YouTube —— 全部 20 个频道</b></summary>

| 分类 | 数量 | 频道 |
|---|---|---|
| **投资机构 · VC** | 4 | [Sequoia Capital](https://www.youtube.com/@sequoiacapital/videos) · [a16z](https://www.youtube.com/@a16z/videos) · [Y Combinator](https://www.youtube.com/@ycombinator/videos) · [Redpoint AI](https://www.youtube.com/@redpointai/videos) |
| **前沿 AI 公司 · 官方** | 5 | [OpenAI](https://www.youtube.com/@OpenAI/videos) · [Anthropic](https://www.youtube.com/@anthropic-ai/videos) · [Google DeepMind](https://www.youtube.com/@googledeepmind/videos) · [HeyGen](https://www.youtube.com/@HeyGen_Official/videos) · [Notion](https://www.youtube.com/@Notion/videos) |
| **一线 researcher · 长访谈** | 2 | [Andrej Karpathy](https://www.youtube.com/@AndrejKarpathy/videos) · [Lex Fridman](https://www.youtube.com/@lexfridman/videos) |
| **播客 · 工程/产品** | 4 | [Latent Space](https://www.youtube.com/@LatentSpacePod/videos) · [Lenny's Podcast](https://www.youtube.com/@LennysPodcast/videos) · [No Priors](https://www.youtube.com/@NoPriorsPodcast/videos) · [Uncapped with Jack Altman](https://www.youtube.com/@uncappedpod/videos) |
| **influencer · 科普/评测(广度)** | 5 | [Two Minute Papers](https://www.youtube.com/@TwoMinutePapers/videos) · [AI Explained](https://www.youtube.com/@aiexplained-official/videos) · [Matthew Berman](https://www.youtube.com/@matthew_berman/videos) · [AI Jason](https://www.youtube.com/@AIJasonZ/videos) · [bycloud](https://www.youtube.com/@bycloudAI/videos) |

</details>

<details>
<summary><b>X / Twitter —— 全部 36 个账号</b></summary>

| 分类 | 数量 | 账号 |
|---|---|---|
| **研究 / Labs** | 11 | [Andrej Karpathy](https://x.com/karpathy) · [Sam Altman](https://x.com/sama) · [Greg Brockman](https://x.com/gdb) · [Yann LeCun](https://x.com/ylecun) · [Andrew Ng](https://x.com/AndrewYNg) · [Jim Fan](https://x.com/DrJimFan) · [Fei-Fei Li](https://x.com/drfeifei) · [Demis Hassabis](https://x.com/demishassabis) · [Noam Brown](https://x.com/polynoamial) · [Nathan Lambert](https://x.com/natolambert) · [Ethan Mollick](https://x.com/emollick) |
| **模型公司 · 官方** | 2 | [DeepSeek](https://x.com/deepseek_ai) · [MiniMax](https://x.com/MiniMax__AI) |
| **创始 / 产品 CEO** | 9 | [Aravind Srinivas](https://x.com/AravSrinivas) · [Amjad Masad](https://x.com/amasad) · [Alexandr Wang](https://x.com/alexandr_wang) · [Clement Delangue](https://x.com/ClementDelangue) · [Harrison Chase](https://x.com/hwchase17) · [Michael Truell](https://x.com/mntruell) · [Guillermo Rauch](https://x.com/rauchg) · [Bret Taylor](https://x.com/btaylor) · [Mira Murati](https://x.com/miramurati) |
| **GTM / 增长 / 出海** | 4 | [Lenny Rachitsky](https://x.com/lennysan) · [Greg Isenberg](https://x.com/gregisenberg) · [Peter Yang](https://x.com/petergyang) · [Pieter Levels](https://x.com/levelsio) |
| **demo / builder 高产** | 4 | [AK](https://x.com/_akhaliq) · [Mckay Wrigley](https://x.com/mckaywrigley) · [Bilawal Sidhu](https://x.com/bilawalsidhu) · [Riley Brown](https://x.com/rileybrown_ai) |
| **工程 / 写作** | 2 | [swyx](https://x.com/swyx) · [Simon Willison](https://x.com/simonw) |
| **投资 & 操盘** | 3 | [Garry Tan](https://x.com/garrytan) · [Sarah Guo](https://x.com/saranormous) · [Martin Casado](https://x.com/martin_casado) |
| **业内 influencer · 对标** | 1 | [Zara Zhang 张咋啦](https://x.com/zarazhangrui) |

</details>

> bilibili（12）和小红书（16）在 [`SOURCES.md`](SOURCES.md) 里，这两个平台目前都还没自动抓取。

## 怎么跑起来的

跑一次，出三个出口。除「核心」外每一层都可以关掉 —— 关掉只是少一个出口，日报照常出。

<div align="center">
<img src="docs/pipeline-obsidian.png" width="900" alt="Frontier 管线：信源 → 构建 → 三个出口（GitHub Pages / Obsidian 库 / 飞书卡片）">
</div>

| 层 | 给你什么 | 需要 | 不装的后果 |
|---|---|---|---|
| **核心** | YouTube 信源 → 杂志风网页 | Python 3 + yt-dlp | — |
| X 板块 | Builders on X 最新推 | TikHub key 或 follow-builders skill | 少「Builders on X」一块 |
| AI 策展 | 头条编辑理由 + 长视频预习 | `claude` 或 `codex` CLI | 页面照常，但没有 AI 总结 |
| 飞书推送 | 每天一张卡片推到 IM | lark-cli + 飞书自建应用 | 只能自己去看网页 |
| Obsidian | 预习笔记落进你的库 | 一个 Obsidian vault | 不写笔记 |

## 五分钟跑起来

```bash
git clone https://github.com/hiamberhuang/frontier.git && cd frontier
pip3 install -r requirements.txt          # 或 brew install yt-dlp
cp config.example.json config.json
python3 fetch_sources.py && python3 build.py
open index.html
```

**这一步不需要任何 API key、不需要任何账号。** 然后：

```bash
bash install_schedule.sh 10 0             # 每天 10:00 自己更新
```

所有跟你个人相关的东西 —— 路径、ID、用哪个 LLM —— 都在 `config.json` 里，这个文件是 gitignore 的。
**你永远不需要改代码来让它变成你的。** 飞书和 Obsidian 的接法看 [`SETUP.md`](SETUP.md)。

## 改成你自己的

YouTube 名单改 `fetch_sources.py`，X 名单改 `my_builders.txt`，编辑口吻改 `build.py` 里的
`EDITOR_NOTES`，改完重新 build。部署到任何静态托管都行 —— GitHub Pages、Vercel、Netlify。

## 依赖

硬依赖只有 `yt-dlp` 一个。`lark-cli`、`claude` / `codex` 都是可选命令行工具，各自对应一层可选功能。
没装会被检测到并跳过，**不会让构建失败**。

## Credits

Built by [Amber Huang](https://amberhuang.world/) · AI marketing, building in public.
策展理念源自 Zara Zhang 的 *Follow Builders, Not Influencers*。
