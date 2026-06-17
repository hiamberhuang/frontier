#!/usr/bin/env bash
# Frontier 日更：抓源 → build → push → 本地通知。launchd 每天 10:00 触发。
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin"
cd "$HOME/Developer/frontier" || exit 1
LOG="$HOME/Developer/frontier/.daily.log"

echo "[$(date '+%F %T')] start" >> "$LOG"
python3 fetch_sources.py          >> "$LOG" 2>&1
python3 fetch_x_products.py       >> "$LOG" 2>&1   # TikHub 官号最新推（需 .tikhub_key）
python3 build.py                  >> "$LOG" 2>&1
git add -A >> "$LOG" 2>&1
git commit -q -m "daily: $(date '+%Y-%m-%d') refresh" >> "$LOG" 2>&1
git push -q >> "$LOG" 2>&1 && PUSH="✓ pushed" || PUSH="⚠ push failed (本地已更新)"
echo "[$(date '+%F %T')] $PUSH" >> "$LOG"

osascript -e 'display notification "今日 AI 日报已更新 · https://7amberhuang.github.io/frontier/" with title "Frontier 📰" sound name "Glass"' 2>/dev/null

# 飞书推送（双保险，跨设备必达）
LARK="/Users/amber/.local/share/fnm/node-versions/v24.15.0/installation/bin/lark-cli"
[ -x "$LARK" ] && "$LARK" im +messages-send --user-id "ou_e71b8550edc0acc975ef9682aa3a0bc6" \
  --text "📰 Frontier 今日 AI 日报已更新
https://7amberhuang.github.io/frontier/
$PUSH" --as user >> "$LOG" 2>&1 || true
