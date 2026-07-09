#!/bin/sh
set -eu

repo_dir="${SKILLS_REPO_DIR:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}"
interval="${SKILLS_AUTO_PUSH_INTERVAL:-300}"
state_dir="$HOME/.local/state/d9249-skills-autopush"
log_dir="$HOME/Library/Logs"
pid_file="$state_dir/pid"
log_file="$log_dir/com.d9249.skills.autopush.log"
err_file="$log_dir/com.d9249.skills.autopush.err.log"

mkdir -p "$state_dir" "$log_dir"

if [ -f "$pid_file" ]; then
  old_pid="$(cat "$pid_file")"
  if [ -n "$old_pid" ] && kill -0 "$old_pid" 2>/dev/null; then
    echo "already running pid $old_pid"
    exit 0
  fi
fi

nohup /bin/sh -c '
repo_dir="$1"
interval="$2"
trap "exit 0" INT TERM HUP
while :; do
  SKILLS_REPO_DIR="$repo_dir" /bin/sh "$repo_dir/scripts/commit_and_push_if_changed.sh" || true
  sleep "$interval" || exit 0
done
' sh "$repo_dir" "$interval" >>"$log_file" 2>>"$err_file" &

pid="$!"
printf '%s\n' "$pid" > "$pid_file"
echo "started background auto-push loop pid $pid"
echo "$pid_file"
