#!/bin/sh
set -eu

repo_dir="${SKILLS_REPO_DIR:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}"
cd "$repo_dir"

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

lock_dir=".git/skills-auto-push.lock"
if ! mkdir "$lock_dir" 2>/dev/null; then
  log "skip: another auto-push run is active"
  exit 0
fi
trap 'rmdir "$lock_dir"' EXIT INT TERM

if [ -e ".git/index.lock" ] || [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
  log "skip: git operation already in progress"
  exit 0
fi

branch="$(git branch --show-current)"
if [ -z "$branch" ]; then
  log "skip: detached HEAD"
  exit 0
fi

ahead=0
behind=0
upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
if [ -n "$upstream" ]; then
  counts="$(git rev-list --left-right --count "HEAD...$upstream" 2>/dev/null || printf '0 0')"
  set -- $counts
  ahead="${1:-0}"
  behind="${2:-0}"
  if [ "$behind" != "0" ]; then
    log "skip: $branch is behind $upstream by $behind commit(s)"
    exit 0
  fi
fi

if git diff --quiet --ignore-submodules -- && git diff --cached --quiet --ignore-submodules -- && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  if [ "$ahead" != "0" ] && [ "${SKILLS_AUTO_PUSH_NO_PUSH:-0}" != "1" ]; then
    git push
    log "pushed $branch"
    exit 0
  fi
  log "clean: no skill changes"
  exit 0
fi

git add -A
if git diff --cached --quiet --ignore-submodules --; then
  log "clean: no stageable skill changes"
  exit 0
fi

commit_subject="${SKILLS_AUTO_COMMIT_SUBJECT:-chore(skills): sync Hermes skill updates}"
commit_body="Automated sync from Hermes-linked skill directories.

Source: $repo_dir
Timestamp: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"

git commit -m "$commit_subject" -m "$commit_body"

if [ "${SKILLS_AUTO_PUSH_NO_PUSH:-0}" = "1" ]; then
  log "committed only: SKILLS_AUTO_PUSH_NO_PUSH=1"
  exit 0
fi

git push
log "pushed $branch"
