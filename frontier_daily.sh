#!/usr/bin/env bash
# Frontier 日更：抓源 → build → push → 通知。由 launchd/cron 每天触发。
# 路径无关：脚本从自身位置推断仓库根，放哪儿都能跑。
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE" || exit 1
LOG="$HERE/.daily.log"

# 把常见的用户级 bin 目录都加进 PATH —— launchd 给的 PATH 极简，
# 不补的话 yt-dlp / claude / lark-cli 全都找不到。
_add_path() { [ -d "$1" ] && case ":$PATH:" in *":$1:"*) ;; *) PATH="$1:$PATH";; esac; }
for d in /opt/homebrew/bin /usr/local/bin "$HOME/.local/bin" "$HOME/bin"; do _add_path "$d"; done
# fnm/nvm 装的 node 工具（lark-cli）：版本号会变，所以用通配而不是写死
for d in "$HOME"/.local/state/fnm_multishells/*/bin "$HOME"/.local/share/fnm/node-versions/*/installation/bin \
         "$HOME"/.nvm/versions/node/*/bin; do _add_path "$d"; done
export PATH

PY="$(command -v python3 || echo python3)"

echo "[$(date '+%F %T')] start" >> "$LOG"
"$PY" fetch_sources.py            >> "$LOG" 2>&1   # YouTube 信源（必需）
"$PY" fetch_x_products.py         >> "$LOG" 2>&1   # TikHub 官号最新推（需 .tikhub_key，可选）
"$PY" fetch_x_builders.py         >> "$LOG" 2>&1   # TikHub builders 最新推（可选）
"$PY" pick_quote.py               >> "$LOG" 2>&1   # 今日金句（可选）
"$PY" digest_videos.py            >> "$LOG" 2>&1   # AI 预习 + 头条 Editor's note（可选，见 config.llm）
echo "[$(date '+%F %T')] preview done" >> "$LOG"
"$PY" build.py                    >> "$LOG" 2>&1   # 生成 index.html（必需）

# 推送前 review 门禁：站点必须有实质内容才推，避免空站/坏站覆盖线上
REVIEW_OK=1
[ -s index.html ] && [ "$(wc -c < index.html)" -gt 4000 ] && grep -q '<h1>' index.html || REVIEW_OK=0
grep -q 'class="xc"' index.html || echo "[$(date '+%F %T')] ⚠ review: Builders on X 空（TikHub？）" >> "$LOG"

git add -A >> "$LOG" 2>&1
git commit -q -m "daily: $(date '+%Y-%m-%d') refresh" >> "$LOG" 2>&1
if [ "$REVIEW_OK" = 1 ]; then
  PUSH="⚠ push failed (本地已更新)"
  for i in 1 2 3; do                              # push 自动重试，扛偶发网络
    if git push -q >> "$LOG" 2>&1; then PUSH="✓ pushed"; break; fi
    sleep $((i * 8))
  done
else
  PUSH="⛔ review 未通过（站点内容异常）→ 跳过 push，保留线上旧版"
fi
echo "[$(date '+%F %T')] $PUSH" >> "$LOG"

# 桌面通知（macOS only，其他系统静默跳过）
command -v osascript >/dev/null && \
  osascript -e 'display notification "今日 AI 日报已更新" with title "Frontier 📰" sound name "Glass"' 2>/dev/null

# 飞书推送（可选，见 config.feishu）
"$PY" feishu_card.py >> "$LOG" 2>&1 || true
