---
name: pp-ocr-ocr-sync
description: Mirror specific git commits from the pp-ocr repository into the paired ocr repository by calling pp-ocr's existing scripts/git/mirror_commit_to_ocr.py workflow and verifying the resulting paths. Use when Codex is working in pp-ocr and the user asks to sync, mirror, carry over, or reflect one or more pp-ocr commit SHAs into the sibling ocr repo.
---

# PP-OCR OCR Sync

## Overview

Mirror one or more `pp-ocr` commits into the paired `ocr` repo with the existing repo-local mirror script, then verify that every path touched by those commits matches in the target repo.

## Prefer The Helper

Run the bundled helper from anywhere:

```bash
"${CODEX_HOME:-$HOME/.codex}"/skills/pp-ocr-ocr-sync/scripts/sync_commits.py <sha1> [<sha2> ...]
```

Override locations only when the default repo discovery is wrong:

```bash
"${CODEX_HOME:-$HOME/.codex}"/skills/pp-ocr-ocr-sync/scripts/sync_commits.py \
  --source-repo /Users/mean/Documents/Github/pp-ocr \
  --target-repo /Users/mean/Documents/Github/ocr \
  --target-branch master \
  <sha1> <sha2>
```

## Follow This Workflow

1. Resolve the source repo by finding `scripts/git/mirror_commit_to_ocr.py`.
2. Resolve the target repo from `--target-repo`, `PP_OCR_MIRROR_TARGET`, or the sibling `../ocr`.
3. Validate that every requested SHA exists in the source repo and preserve the user-provided order.
4. Run the repo-local mirror script once per SHA.
5. Verify the union of changed paths against the last requested SHA, or `--source-ref` when you need a different comparison point.
6. Report the target repo status, the latest mirrored commits, the source repo `last_success` value, and the verification counts.

## Respect These Guardrails

- Stop when the target repo is dirty or on the wrong branch. Do not clean it automatically.
- Do not push unless the user explicitly asks.
- Treat merge commits as unsupported for direct mirroring. `mirror_commit_to_ocr.py` computes `git patch-id` and will fail on merge commits. Mirror the concrete non-merge commits instead.
- Surface `.git/pp-ocr-mirror-failed/<sha>.patch` when the repo-local mirror script writes one.
- Keep the skill scoped to `pp-ocr -> ocr`. Do not use it for generic cherry-pick work or the reverse direction.

## Use The Resource

- `scripts/sync_commits.py`
  Run sequential mirroring plus blob-hash verification in one command. Prefer this script over retyping the workflow by hand.
