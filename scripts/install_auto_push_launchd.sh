#!/bin/sh
set -eu

repo_dir="${SKILLS_REPO_DIR:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}"
label="${SKILLS_AUTO_PUSH_LABEL:-com.d9249.skills.autopush}"
interval="${SKILLS_AUTO_PUSH_INTERVAL:-300}"
launch_agents="$HOME/Library/LaunchAgents"
log_dir="$HOME/Library/Logs"
plist="$launch_agents/$label.plist"
uid="$(id -u)"

mkdir -p "$launch_agents" "$log_dir"

cat > "$plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$label</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/sh</string>
    <string>$repo_dir/scripts/commit_and_push_if_changed.sh</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$repo_dir</string>
  <key>StartInterval</key>
  <integer>$interval</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$log_dir/$label.log</string>
  <key>StandardErrorPath</key>
  <string>$log_dir/$label.err.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin</string>
    <key>SKILLS_REPO_DIR</key>
    <string>$repo_dir</string>
  </dict>
</dict>
</plist>
PLIST

launchctl bootout "gui/$uid" "$plist" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$uid" "$plist"
launchctl enable "gui/$uid/$label"
launchctl kickstart -k "gui/$uid/$label"

echo "installed $label"
echo "$plist"
