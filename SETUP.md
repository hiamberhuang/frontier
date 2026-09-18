# Frontier 部署指南

从 fork 到「每天早上自己更新的 AI 日报」。**最小可用 5 分钟**，全套（AI 预习 + 飞书推送 + Obsidian）大概 30 分钟。

Frontier 是**分层**的：核心那层零配置就能跑，上面每一层都可选，缺了只是少一个板块，不会让整个日报崩掉。

| 层 | 给你什么 | 需要 | 不装的后果 |
|---|---|---|---|
| **核心** | YouTube 信源 → 杂志风网页 | Python 3 + yt-dlp | — |
| X 板块 | Builders on X 最新推 | TikHub key（付费）或 follow-builders skill | 少「Builders on X」一块 |
| AI 策展 | 头条编辑理由 + 长视频预习 | claude 或 codex CLI | 页面照常，但没有 AI 总结 |
| 飞书推送 | 每天一张卡片推到 IM | lark-cli + 飞书自建应用 | 只能自己去看网页 |
| Obsidian | 预习笔记落进你的库 | 一个 Obsidian vault | 不写笔记 |

---

## 1. 最小可用（5 分钟）

```bash
git clone https://github.com/YOURNAME/frontier.git && cd frontier
pip3 install -r requirements.txt          # 或 brew install yt-dlp
cp config.example.json config.json
python3 fetch_sources.py && python3 build.py
open index.html
```

能看到页面就成了。**这一步不需要任何 API key、不需要任何账号。**

### 换成你自己的信源

编辑 `fetch_sources.py` 里的 `YT_CHANNELS`，把 YouTube 频道 handle 换成你关注的：

```python
YT_CHANNELS = [
    ("Lenny's Podcast", "https://www.youtube.com/@LennysPodcast/videos"),
    ("你关注的频道",     "https://www.youtube.com/@THEIR_HANDLE/videos"),
]
```

handle 就是频道页 URL 里 `@` 后面那串。改完重跑上面两条命令。
X 的名单在 `my_builders.txt`，一行一个 `显示名|handle`。
完整信源清单看 [`SOURCES.md`](SOURCES.md)。

### 发布到 GitHub Pages

仓库 **Settings → Pages → Source 选 `Deploy from a branch`**，branch 选 `main`、目录选 `/ (root)`，Save。
等一两分钟，站点在 `https://YOURNAME.github.io/frontier/`。
然后把这个地址填进 `config.json` 的 `site.url`。

> ⚠️ 这一步必须手动点，脚本代劳不了。不开的话 push 上去也是 404。

---

## 2. 每天自动更新

```bash
bash install_schedule.sh 10 0      # 每天 10:00；不传参数默认也是 10:00
```

macOS 装 launchd，Linux 装 crontab，脚本自己判断。日志在 `.daily.log`。

```bash
bash frontier_daily.sh                    # 手动跑一次，验证
bash install_schedule.sh --uninstall      # 不想要了
```

> 💡 定时任务拿到的 PATH 极简，`frontier_daily.sh` 会自己把 homebrew / `~/.local/bin` / fnm / nvm 的目录补回去，所以不用担心「手动能跑、定时跑不了」这个经典坑。

---

## 3. AI 策展（claude 或 codex，二选一）

这层负责两件事：给头条写一句「为什么值得看」，以及把当天的长视频抓字幕、AI 读完、写成预习。

编辑 `config.json`：

```jsonc
{ "llm": { "provider": "claude", "model": "claude-sonnet-4-6" } }
```

**用 Codex 的话**：

```jsonc
{ "llm": { "provider": "codex", "model": "gpt-5-codex" } }
```

> ⚠️ **codex 预设未经实测。** 写这份配置的机器上没装 codex CLI，所以 `codex exec --model X "prompt"` 这个调用形式是照官方文档写的，没跑通过。如果报错，不用改代码 —— 用下面的 custom 模式把 argv 写死成你那版 CLI 实际能用的样子。

**任何其他 CLI**（Gemini CLI、ollama、自己包的脚本都行）：

```jsonc
{ "llm": { "provider": "custom", "command": ["ollama", "run", "llama3"] } }
```

规则很简单：`command` 数组就是 argv，**prompt 会作为最后一个参数追加上去**。上面这条等于执行 `ollama run llama3 "<prompt>"`。

**完全不想要 AI**：`"provider": "none"`。日报照常出，只是没有编辑理由和预习。

---

## 4. 飞书每日推送（lark-cli）

跑通之后，每天早上飞书里会收到一张卡片：封面图 + 今日头条 + 每条视频的 AI 一句话 + 「看完整日报 / 看预习笔记」按钮。

### 4.1 装 lark-cli 并登录

```bash
npm i -g @larksuite/lark-cli
lark-cli auth login
```

会弹浏览器让你扫码授权（device flow）。完事后验证：

```bash
lark-cli auth status
```

### 4.2 拿到你的接收 ID

推送要知道发给谁。两种：

- **发给自己** → 需要你的 `open_id`（`ou_` 开头）
- **发到群里** → 需要群的 `chat_id`（`oc_` 开头）

查自己的 open_id：

```bash
lark-cli contact +search-user --user-ids me --as user
```

输出里那个 `ou_xxxxxxxx` 就是。

> ⚠️ **open_id 是按应用隔离的。** 同一个人在不同飞书应用下的 open_id **不一样**。上面这条命令返回的是 lark-cli 自己那个应用下的 id；而日报卡片是用 `--as bot` 发的，走的可能是另一个应用。
>
> 所以如果按上面拿到的 id 发送失败，改用输出里的 **`p2p_chat_id`**（`oc_` 开头），它跨应用稳定：把那个 `oc_` 填进 `receiver_id` 即可，脚本会自动识别 `oc_` 走 `--chat-id`。

### 4.3 填进配置

```jsonc
{
  "feishu": {
    "enabled": true,
    "receiver_id": "ou_你的open_id",
    "lark_cli": ""
  }
}
```

`lark_cli` 留空就好 —— 它会自己在 PATH 上找。只有当你的 lark-cli 装在一个很怪的位置、自动找不到时，才需要填绝对路径。

### 4.4 测试

```bash
python3 feishu_card.py
```

看到 `✓ ou_xxx: {"message_id": ...}` 就是发出去了，去飞书看。

> **发给多个人？** 在仓库根建一个 `.subscribers` 文件，一行一个 ID（`ou_` 或 `oc_` 混着放都行，`#` 开头是注释）。有这个文件时 `receiver_id` 会被忽略。

### 常见问题

| 症状 | 原因 | 怎么办 |
|---|---|---|
| `找不到 lark-cli → 跳过` | 没装，或不在 PATH | `npm i -g @larksuite/lark-cli`，或把绝对路径填进 `feishu.lark_cli` |
| 手动能发、定时任务发不出去 | launchd 的 PATH 里没有 node | `frontier_daily.sh` 已经处理了；还不行就填绝对路径 |
| 发送返回权限错误 | 自建应用缺 scope | 飞书开放平台后台给应用加 `im:message` 权限并重新发布版本 |
| 卡片是空的 | `digest_videos.py` 没产出（没配 LLM） | 先把第 3 步跑通 |

---

## 5. Obsidian 接入

目前是**单向**的：Frontier 往你的库里写，不读回来。

```jsonc
{
  "vault": {
    "enabled": true,
    "path": "~/Documents/YourVault",
    "notes_subdir": "wiki/daily-preview",
    "vault_name": "YourVault",
    "git_commit": false
  }
}
```

- `path` —— 你的 vault 在磁盘上的位置
- `vault_name` —— Obsidian 里显示的库名。**必须和 Obsidian 里一致**，否则 `obsidian://` 深链点开会失败
- `notes_subdir` —— 笔记落在 vault 里的哪个子目录，不存在会自动建
- `git_commit` —— 如果你的 vault 本身是个 git 仓库，开了就每天自动 commit 一次

跑完 `python3 digest_videos.py`，`<vault>/<notes_subdir>/YYYY-MM-DD.md` 就出来了，带 frontmatter 和 `[[wikilink]]`。飞书卡片里的「看预习笔记」按钮会优先给飞书文档链接，没有飞书就退回 `obsidian://` 深链。

---

## 6. X / Twitter 板块（可选，要钱）

两条路：

1. **TikHub**（`.tikhub_key` 放一行 key）—— 按量付费，能抓到最新推文和头像
2. **follow-builders skill** —— [Zara Zhang 的开源 feed](https://github.com/zarazhangrui/follow-builders)，免费但刷新慢。装好后把目录填进 `config.json` 的 `sources.follow_builders_dir`

两个都没有也没事，`build.py` 会跳过这个板块，不会崩。

> 🔐 **key 不要提交进 git。** `.gitignore` 已经挡了 `.tikhub_key*` 和 `config.json`，但你自己新建的文件要自己注意。公开仓库里的 key 等于公开的 key。

---

## 全部配置项

| 配置 | 默认 | 说明 |
|---|---|---|
| `llm.provider` | `none` | `claude` / `codex` / `custom` / `none` |
| `llm.command` | `[]` | 仅 `custom`：argv 数组，prompt 追加在最后 |
| `llm.timeout_sec` | `300` | 单次调用超时 |
| `vault.enabled` | `false` | 是否写 Obsidian 笔记 |
| `vault.path` | `~/Documents/YourVault` | vault 磁盘路径 |
| `vault.vault_name` | `YourVault` | Obsidian 里的库名，深链要用 |
| `vault.git_commit` | `false` | vault 是 git 仓库时自动 commit |
| `feishu.enabled` | `false` | 是否推飞书 |
| `feishu.receiver_id` | `""` | `ou_`（个人）或 `oc_`（群） |
| `feishu.lark_cli` | `""` | 留空 = 自动找 |
| `site.url` | `""` | 你的 Pages 地址 |
| `site.author` / `site.twitter` / `site.portfolio` | `""` | 页面署名；留空的链接会自动不显示 |
| `sources.follow_builders_dir` | `~/.claude/skills/follow-builders` | 不存在就跳过，不报错 |
