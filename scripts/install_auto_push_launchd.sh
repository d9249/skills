#!/bin/sh
set -eu

repo_dir="${SKILLS_REPO_DIR:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}"
label="${SKILLS_AUTO_PUSH_LABEL:-com.d9249.skills.autopush}"
interval="${SKILLS_AUTO_PUSH_INTERVAL:-300}"
launch_agents="$HOME/Library/LaunchAgents"
log_dir="$HOME/Library/Logs"
plist="$launch_agents/$label.plist"
uid="$(id -u)"
fallback="$repo_dir/scripts/start_auto_push_loop.sh"

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
if launchctl bootstrap "gui/$uid" "$plist"; then
  launchctl enable "gui/$uid/$label"
  launchctl kickstart -k "gui/$uid/$label"
  sleep 2
  if launchctl print "gui/$uid/$label" 2>/dev/null | grep -q 'last exit code = 126'; then
    launchctl bootout "gui/$uid" "$plist" >/dev/null 2>&1 || true
    echo "launchd cannot access the repo; falling back to a user-started loop"
    SKILLS_REPO_DIR="$repo_dir" SKILLS_AUTO_PUSH_INTERVAL="$interval" "$fallback"
    exit 0
  fi
else
  echo "launchd bootstrap failed; falling back to a user-started loop"
  SKILLS_REPO_DIR="$repo_dir" SKILLS_AUTO_PUSH_INTERVAL="$interval" "$fallback"
  exit 0
fi

echo "installed $label"
echo "$plist"
