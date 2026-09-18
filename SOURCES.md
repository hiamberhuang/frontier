# Frontier 信源清单

> 策展原则：**builders not influencers**。这份是 Frontier 的**完整信息源**，也是唯一权威版本。
> 名单本身就是观点 —— 人是手挑的，不是算法推的。

**共 84 个** · YouTube 20 · X/Twitter 36 · bilibili 12 · 小红书 16

| 平台 | 数量 | 抓取状态 | 配置在哪 |
|---|---|---|---|
| YouTube | 20 | ✅ 全量自动抓取 | `fetch_sources.py` → `YT_CHANNELS` |
| X / Twitter | 36 | ✅ 自动抓取（需 TikHub key） | `my_builders.txt` |
| bilibili | 12 | ⏳ 待接入（yt-dlp 抽取器待修） | 本文件 |
| 小红书 | 16 | ⏸ 仅作关注 / 选题池 | 本文件 |

> 改名单只要改上面那两个文件，改完重跑 `python3 fetch_sources.py && python3 build.py`。

---

## YouTube（20）

| 频道 | 分类 | 为什么在名单里 |
|---|---|---|
| [Sequoia Capital](https://www.youtube.com/@sequoiacapital/videos) `@sequoiacapital` | 投资机构 · VC | Training Data 播客,顶级 VC 看 AI 大盘 |
| [a16z](https://www.youtube.com/@a16z/videos) `@a16z` | 投资机构 · VC | AI 趋势 + 创始人深访,增长/出海视角 |
| [Y Combinator](https://www.youtube.com/@ycombinator/videos) `@ycombinator` | 投资机构 · VC | Lightcone 播客,创业一线判断 |
| [Redpoint AI](https://www.youtube.com/@redpointai/videos) `@redpointai` | 投资机构 · VC | Unsupervised Learning 播客 |
| [OpenAI](https://www.youtube.com/@OpenAI/videos) `@OpenAI` | 前沿 AI 公司 · 官方 | 发布会 / demo 第一现场 |
| [Anthropic](https://www.youtube.com/@anthropic-ai/videos) `@anthropic-ai` | 前沿 AI 公司 · 官方 | Claude + 安全/可解释研究 |
| [Google DeepMind](https://www.youtube.com/@googledeepmind/videos) `@googledeepmind` | 前沿 AI 公司 · 官方 | 前沿模型研究 |
| [HeyGen](https://www.youtube.com/@HeyGen_Official/videos) `@HeyGen_Official` | 前沿 AI 公司 · 官方 | 产品即内容,出海 GTM 范本 |
| [Notion](https://www.youtube.com/@Notion/videos) `@Notion` | 前沿 AI 公司 · 官方 | AI 产品 + GTM / 模板 |
| [Andrej Karpathy](https://www.youtube.com/@AndrejKarpathy/videos) `@AndrejKarpathy` | 一线 researcher · 长访谈 | 第一性原理教学 |
| [Lex Fridman](https://www.youtube.com/@lexfridman/videos) `@lexfridman` | 一线 researcher · 长访谈 | 和造 AI 的人几小时深聊 |
| [Latent Space](https://www.youtube.com/@LatentSpacePod/videos) `@LatentSpacePod` | 播客 · 工程/产品 | swyx,AI 工程最硬核 |
| [Lenny's Podcast](https://www.youtube.com/@LennysPodcast/videos) `@LennysPodcast` | 播客 · 工程/产品 | 产品/增长,最贴 GTM |
| [No Priors](https://www.youtube.com/@NoPriorsPodcast/videos) `@NoPriorsPodcast` | 播客 · 工程/产品 | 模型公司创始人深访 |
| [Uncapped with Jack Altman](https://www.youtube.com/@uncappedpod/videos) `@uncappedpod` | 播客 · 工程/产品 | 创始人/投资人对谈 |
| [Two Minute Papers](https://www.youtube.com/@TwoMinutePapers/videos) `@TwoMinutePapers` | influencer · 科普/评测(广度) | 最新论文几分钟人话 |
| [AI Explained](https://www.youtube.com/@aiexplained-official/videos) `@aiexplained-official` | influencer · 科普/评测(广度) | 抠模型与 benchmark |
| [Matthew Berman](https://www.youtube.com/@matthew_berman/videos) `@matthew_berman` | influencer · 科普/评测(广度) | 新模型/agent 第一时间 demo |
| [AI Jason](https://www.youtube.com/@AIJasonZ/videos) `@AIJasonZ` | influencer · 科普/评测(广度) | agent/编码实操 demo |
| [bycloud](https://www.youtube.com/@bycloudAI/videos) `@bycloudAI` | influencer · 科普/评测(广度) | 模型研究/新论文,偏技术 |

---

## X / Twitter（36）

同步至 [`my_builders.txt`](my_builders.txt)（脚本读这个文件）。该文件里另有 24 个**注释掉的备选账号**，去掉行首 `#` 即可启用。

| 人 | 分类 |
|---|---|
| [Andrej Karpathy](https://x.com/karpathy) `@karpathy` | 研究 / Labs |
| [Sam Altman](https://x.com/sama) `@sama` | 研究 / Labs |
| [Greg Brockman](https://x.com/gdb) `@gdb` | 研究 / Labs |
| [Yann LeCun](https://x.com/ylecun) `@ylecun` | 研究 / Labs |
| [Andrew Ng](https://x.com/AndrewYNg) `@AndrewYNg` | 研究 / Labs |
| [Jim Fan](https://x.com/DrJimFan) `@DrJimFan` | 研究 / Labs |
| [Fei-Fei Li](https://x.com/drfeifei) `@drfeifei` | 研究 / Labs |
| [Demis Hassabis](https://x.com/demishassabis) `@demishassabis` | 研究 / Labs |
| [Noam Brown](https://x.com/polynoamial) `@polynoamial` | 研究 / Labs |
| [Nathan Lambert](https://x.com/natolambert) `@natolambert` | 研究 / Labs |
| [Ethan Mollick](https://x.com/emollick) `@emollick` | 研究 / Labs |
| [DeepSeek](https://x.com/deepseek_ai) `@deepseek_ai` | 模型公司 · 官方 |
| [MiniMax](https://x.com/MiniMax__AI) `@MiniMax__AI` | 模型公司 · 官方 |
| [Aravind Srinivas](https://x.com/AravSrinivas) `@AravSrinivas` | 创始 / 产品 CEO |
| [Amjad Masad](https://x.com/amasad) `@amasad` | 创始 / 产品 CEO |
| [Alexandr Wang](https://x.com/alexandr_wang) `@alexandr_wang` | 创始 / 产品 CEO |
| [Clement Delangue](https://x.com/ClementDelangue) `@ClementDelangue` | 创始 / 产品 CEO |
| [Harrison Chase](https://x.com/hwchase17) `@hwchase17` | 创始 / 产品 CEO |
| [Michael Truell](https://x.com/mntruell) `@mntruell` | 创始 / 产品 CEO |
| [Guillermo Rauch](https://x.com/rauchg) `@rauchg` | 创始 / 产品 CEO |
| [Bret Taylor](https://x.com/btaylor) `@btaylor` | 创始 / 产品 CEO |
| [Mira Murati](https://x.com/miramurati) `@miramurati` | 创始 / 产品 CEO |
| [Lenny Rachitsky](https://x.com/lennysan) `@lennysan` | GTM / 增长 / 出海 |
| [Greg Isenberg](https://x.com/gregisenberg) `@gregisenberg` | GTM / 增长 / 出海 |
| [Peter Yang](https://x.com/petergyang) `@petergyang` | GTM / 增长 / 出海 |
| [Pieter Levels](https://x.com/levelsio) `@levelsio` | GTM / 增长 / 出海 |
| [AK](https://x.com/_akhaliq) `@_akhaliq` | demo / builder 高产 |
| [Mckay Wrigley](https://x.com/mckaywrigley) `@mckaywrigley` | demo / builder 高产 |
| [Bilawal Sidhu](https://x.com/bilawalsidhu) `@bilawalsidhu` | demo / builder 高产 |
| [Riley Brown](https://x.com/rileybrown_ai) `@rileybrown_ai` | demo / builder 高产 |
| [swyx](https://x.com/swyx) `@swyx` | 工程 / 写作 |
| [Simon Willison](https://x.com/simonw) `@simonw` | 工程 / 写作 |
| [Garry Tan](https://x.com/garrytan) `@garrytan` | 投资 & 操盘 |
| [Sarah Guo](https://x.com/saranormous) `@saranormous` | 投资 & 操盘 |
| [Martin Casado](https://x.com/martin_casado) `@martin_casado` | 投资 & 操盘 |
| [Zara Zhang 张咋啦](https://x.com/zarazhangrui) `@zarazhangrui` | 业内 influencer · 对标 |

---

## bilibili（12）

> yt-dlp 的 bilibili 抽取器当前报 NoneType，抓取待修复。空间链接如下，修好后接进 `build.py`。

| UP 主 | 在做什么 |
|---|---|
| [秋叶aaaki](https://space.bilibili.com/12566101) | AI 绘画头部,SD/ComfyUI 整合包与教学 |
| [林亦LYi](https://space.bilibili.com/4401694) | AI 科普 + 硬核上手实测 |
| [老麦的工具库](https://space.bilibili.com/486989780) | 时效最快的 AI 工具速递盘点 |
| [图灵的猫](https://space.bilibili.com/371846699) | AI 原理通识科普 |
| [GenJi是真想教会你](https://space.bilibili.com/49746395) | 手把手 AI 开发与应用教学 |
| [Jack-Cui](https://space.bilibili.com/331507846) | 算法工程师讲 AI + 编程实战 |
| [git源宝](https://space.bilibili.com/38061207) | AI 挖掘机,工具盘点 + 热点鉴定 |
| [玄离199](https://space.bilibili.com/67079745) | AI 工具与 MCP,让设备更好用 |
| [Unitree 宇树科技](https://space.bilibili.com/521974986) | 国产机器人官号,人形/四足发布 |
| [十字路口 Crossing](https://space.bilibili.com/505301413) | Koji 杨远骋的 AI 一线视频播客 |
| [秋芝2046](https://space.bilibili.com/385670211) | AIGC 影像创作,AI 电影/工作流 |
| [Xuan_酱](https://space.bilibili.com/14848367) | 沉迷 AI,爱折腾各类工具应用 |

---

## 小红书（16）

> 当前管线**不自动抓小红书**，这份是关注 / 选题源。

| 账号 | 方向 |
|---|---|
| [十字路口 Crossing(Koji杨远骋)](https://www.xiaohongshu.com/user/profile/548251dce779893bcf3f77bc) | AI 媒体/播客 |
| [周末Zomo](https://www.xiaohongshu.com/user/profile/5a051c124eacab39ed6500ff) | 设计 / vibecoding |
| [几口酱聊AI](https://www.xiaohongshu.com/user/profile/656daf47000000002002d20f) | AI 广告 / agent |
| [西里森森](https://www.xiaohongshu.com/user/profile/6244a8f7000000001000ada3) | AI 设计 / 网站 |
| [丝诺姐姐](https://www.xiaohongshu.com/user/profile/55f920a9c2bdeb18338ab696) | AI 产品经理 / 公司观察 |
| [数字生命卡兹克](https://www.xiaohongshu.com/user/profile/62c98736000000001501e075) | AIGC 头部 KOL |
| [归藏的AI工具箱(歸藏)](https://www.xiaohongshu.com/user/profile/5c696b98000000001003043b) | AI 设计 / 工具 |
| [Simon_阿文](https://www.xiaohongshu.com/user/profile/5b72992cf7e8b94cea514695) | AI 设计 / 信息图 |
| [海辛Hyacinth](https://www.xiaohongshu.com/user/profile/648a5137000000002a0360e5) | AIGC 视觉创作 |
| [哥飞](https://www.xiaohongshu.com/user/profile/5b683c2cc39aaf0001b06269) | 出海 / 独立开发 |
| [刘小排r](https://www.xiaohongshu.com/user/profile/69afc806000000003202c458) | AI 产品 / 超级个体 |
| [AI产品黄叔](https://www.xiaohongshu.com/user/profile/5bbd6615c91fa10001591b7e) | AI 产品 |
| [漫士沉思录](https://www.xiaohongshu.com/user/profile/64100336000000001002bfc7) | AI 技术科普 |
| [赛博禅心](https://www.xiaohongshu.com/user/profile/5b6bee5a6b58b7037ebad058) | AI 资讯 / 深度 |
| [花叔(AI进化论-花生)](https://www.xiaohongshu.com/user/profile/5abc6f17e8ac2b109179dfdf) | AI 超级个体 / builder |
| [深思圈](https://www.xiaohongshu.com/user/profile/625eb64900000000210210ea) | AI 行业洞察 |

---

## 待办

- [x] YouTube 全量接入 `fetch_sources.py`（2026-09-18 完成，20 个 handle 逐个实测可解析）
- [ ] bilibili yt-dlp 抓取修复 + 把 12 个 UID 接入 `build.py`
- [ ] 小红书是否接入自动抓取（目前仅作 roster）
