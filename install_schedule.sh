#!/usr/bin/env bash
# 把 Frontier 装成每天自动跑的定时任务。
#   macOS  -> launchd  (~/Library/LaunchAgents)
#   Linux  -> crontab
# 用法：  bash install_schedule.sh [HH] [MM]      默认 10:00
#         bash install_schedule.sh --uninstall
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABEL="com.frontier.daily"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

if [ "${1:-}" = "--uninstall" ]; then
  if [ "$(uname)" = "Darwin" ]; then
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || launchctl unload "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"; echo "✓ 已卸载 launchd 任务"
  else
    crontab -l 2>/dev/null | grep -v "frontier_daily.sh" | crontab - || true
    echo "✓ 已从 crontab 移除"
  fi
  exit 0
fi

HH="${1:-10}"; MM="${2:-0}"
chmod +x "$HERE/frontier_daily.sh"

if [ "$(uname)" = "Darwin" ]; then
  mkdir -p "$HOME/Library/LaunchAgents"
  cat > "$PLIST" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$HERE/frontier_daily.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>$HH</integer>
        <key>Minute</key><integer>$MM</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$HERE/.daily.log</string>
    <key>StandardErrorPath</key>
    <string>$HERE/.daily.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
PLISTEOF
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST" 2>/dev/null || launchctl load "$PLIST"
  printf '✓ launchd 已装好：每天 %02d:%02d 自动更新\n  日志：%s/.daily.log\n  手动跑一次：bash %s/frontier_daily.sh\n  卸载：bash %s/install_schedule.sh --uninstall\n' \
    "$HH" "$MM" "$HERE" "$HERE" "$HERE"
else
  LINE="$MM $HH * * * /bin/bash $HERE/frontier_daily.sh"
  ( crontab -l 2>/dev/null | grep -v "frontier_daily.sh"; echo "$LINE" ) | crontab -
  printf '✓ crontab 已装好：每天 %02d:%02d 自动更新\n  日志：%s/.daily.log\n' "$HH" "$MM" "$HERE"
fi
