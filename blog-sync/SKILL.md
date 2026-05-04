---
name: blog-sync
description: Mirror specific git commits from /Users/mean/Documents/Github/aidt-blog into the paired /Users/mean/Documents/Github/blog repository by calling aidt-blog's repo-local scripts/git/mirror_commit_to_blog.py workflow and verifying the resulting paths. Use when Codex is working with aidt-blog and the user asks to sync, reflect, copy, mirror, or carry over one or more aidt-blog commit SHAs into blog, or asks to diagnose the aidt-blog -> blog commit mirror hook.
---

# Blog Sync

## Overview

Mirror one or more `aidt-blog` commits into the paired `blog` repo with the repo-local mirror script, then verify every path touched by those commits against the target repo.

## Prefer The Helper

Run the bundled helper from anywhere:

```bash
"${CODEX_HOME:-$HOME/.codex}"/skills/blog-sync/scripts/sync_commits.py <sha1> [<sha2> ...]
```

Override locations only when the default repo discovery is wrong:

```bash
"${CODEX_HOME:-$HOME/.codex}"/skills/blog-sync/scripts/sync_commits.py \
  --source-repo /Users/mean/Documents/Github/aidt-blog \
  --target-repo /Users/mean/Documents/Github/blog \
  --target-branch master \
  <sha1> <sha2>
```

## Follow This Workflow

1. Resolve the source repo by finding `scripts/git/mirror_commit_to_blog.py`.
2. Resolve the target repo from `--target-repo`, `AIDT_BLOG_MIRROR_TARGET`, or the sibling `../blog`.
3. Validate that every requested SHA exists in the source repo and preserve the user-provided order.
4. Run the repo-local mirror script once per SHA.
5. Verify the union of changed paths against the last requested SHA, or `--source-ref` when a different comparison point is needed.
6. Report the target repo status, the latest mirrored commits, the source repo `last_success` value, and verification counts.

## Automatic Hook

The source repo should have:

- `.githooks/post-commit`
- `scripts/git/mirror_commit_to_blog.sh`
- `scripts/git/mirror_commit_to_blog.py`
- local config `core.hooksPath=.githooks`

When diagnosing "it did not sync", inspect these first:

```bash
git -C /Users/mean/Documents/Github/aidt-blog config --local core.hooksPath
test -x /Users/mean/Documents/Github/aidt-blog/.githooks/post-commit
git -C /Users/mean/Documents/Github/blog status --short --branch
cat /Users/mean/Documents/Github/aidt-blog/.git/aidt-blog-mirror-last-success
```

## Manual Current-HEAD Mirror

To mirror all source commits after the last successful hook run:

```bash
/Users/mean/Documents/Github/aidt-blog/scripts/git/mirror_commit_to_blog.sh
```

## Rules

- Stop when the target repo is dirty or on the wrong branch. Do not clean it automatically.
- Do not push unless the user explicitly asks.
- Treat merge commits as unsupported for direct mirroring. Mirror the concrete non-merge commits instead.
- Surface `.git/aidt-blog-mirror-failed/<sha>.patch` when the repo-local mirror script writes one.
- Keep the skill scoped to `aidt-blog -> blog`. Do not use it for generic cherry-pick work or the reverse direction.

## Use The Resource

- `scripts/sync_commits.py`
  Run sequential mirroring plus blob-hash verification in one command. Prefer this script over retyping the workflow by hand.
