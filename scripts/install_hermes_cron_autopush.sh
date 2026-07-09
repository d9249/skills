#!/bin/sh
set -eu

repo_dir="${SKILLS_REPO_DIR:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}"
job_name="${SKILLS_AUTO_PUSH_CRON_NAME:-skills-repo-auto-push}"
schedule="${SKILLS_AUTO_PUSH_CRON_SCHEDULE:-*/5 * * * *}"
hermes_scripts="$HOME/.hermes/scripts"
wrapper="$hermes_scripts/skills_auto_push.sh"
jobs_file="$HOME/.hermes/cron/jobs.json"

mkdir -p "$hermes_scripts"

cat > "$wrapper" <<SH
#!/bin/sh
set -eu
SKILLS_REPO_DIR="$repo_dir" /bin/sh "$repo_dir/scripts/commit_and_push_if_changed.sh"
SH
chmod +x "$wrapper"

if [ -f "$jobs_file" ] && grep -q "\"name\": \"$job_name\"" "$jobs_file"; then
  hermes cron resume "$job_name" >/dev/null 2>&1 || true
  echo "cron job already exists: $job_name"
  echo "$wrapper"
  exit 0
fi

hermes cron create "$schedule" "Commit and push Hermes-linked skills repo changes." \
  --name "$job_name" \
  --deliver local \
  --script "$(basename "$wrapper")" \
  --no-agent \
  --workdir "$repo_dir"

echo "$wrapper"
