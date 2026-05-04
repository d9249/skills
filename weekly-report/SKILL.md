---
name: weekly-report
description: "Assemble weekly reports from git history for the active repository. Use when Codex needs to complete the full weekly-report routine in one pass: compute the reporting boundary from the previous report end commit, draft the stakeholder-style summary with `금주 진행사항` / `차주 진행사항`, create or update the repo's weekly report document, and sync related history index files when the repository already keeps weekly docs such as `docs/history/2026-W*.md`."
---

# Weekly Report

## Overview

Use this skill when the task is not just "summarize recent work" but "finish the whole weekly reporting package."

Default completion contract:

- produce the stakeholder summary
- produce the repo weekly report document
- sync any related weekly-report indexes when the repo already has them
- use one shared git boundary and one shared workstream grouping for both outputs

## Quick Start

1. Resolve the active repo and report boundary.
   - prefer explicit `base` and `head` commits from the user
   - otherwise use the previous report's end commit as `base`
2. Run:

```bash
python ~/.codex/skills/weekly-report/scripts/collect_weekly_report_context.py \
  --repo <repo-root> \
  --base <previous_report_end_sha> \
  --head <target_sha>
```

Add `--json` when you want structured drafting input.

3. Read:
   - `references/report-formats.md`
   - the nearest previous weekly doc in the active repo
4. Group related commits into 4-6 workstreams.
5. Draft both outputs from the same grouping.
6. If the repo keeps weekly docs and index files, update them in the same change.
7. Verify SHAs, dates, commit counts, and run `git diff --check` on touched docs.

## Boundary Rules

- `base` is the previous report's closing commit and is excluded from the current range.
- `head` is the latest commit included in the current report.
- The stakeholder summary should show:
  - first commit after `base`
  - latest commit at `head`
  - total commit count since `base`
- The repo weekly doc should show:
  - human-readable date range from first included commit to last included commit
  - diff range as `base..head`
- If the report is a mid-week or mid-day snapshot, say so explicitly.

## Repo Convention Detection

Prefer existing repo conventions over inventing new ones.

- If the repo contains `docs/history/2026-W*.md`, follow that structure.
- If the repo has weekly indexes such as `README.md`, `monthly-summary.md`, or `feature-axis-index.md` in the same history folder, sync them when the weekly doc changes.
- If no weekly-doc convention exists, still produce the stakeholder summary and draft the repo weekly document in the nearest obvious history/docs area, or in the user-requested path.

## Required Outputs

### 1. Stakeholder Summary

Use the template in `references/report-formats.md`.

Rules:

- start with `YYYYMMDD`
- include `기준 범위:` and `참고:`
- use `금주 진행사항` and `차주 진행사항`
- keep `금주 진행사항` to 4-6 grouped workstreams
- each numbered item should be outcome-first, not commit-first
- format each item as `제목 (담당자)` followed by a `:` explanation block
- derive `차주 진행사항` from unfinished work, validation debt, or the obvious next iteration

### 2. Repo Weekly Doc

Mirror the nearest existing weekly doc in the repository.

For repos like `pp-ocr`, the required sections are:

- 기간
- 기준 범위
- 커밋 수
- 주간 요약
- 핵심 작업
- 대표 변경 파일
- 비고
- 커밋 메모

Completion rule:

- finish only after both outputs are present
- keep workstream names consistent across both outputs
- make `커밋 메모` detailed enough that a reader can reconstruct the week without reopening `git log`

## Writing Rules

- Merge related commits into one theme.
- Name themes by outcome, for example:
  - `연구 비교 대시보드`
  - `템플릿 OCR 리포트`
  - `작업실 UX 재편`
- Use managerial or product wording in stakeholder summaries.
- Use implementation detail only where it changes the meaning of the week.
- Separate:
  - user-facing features
  - backend or runtime changes
  - research infrastructure
  - bulk artifact or documentation additions
- If `data/` or generated results dominate churn, treat them as supporting artifacts unless they are themselves the point of the report.

## Resources

- `scripts/collect_weekly_report_context.py`
  - computes first and last commits, commit count, date range, and top-level diff summary for a report range
- `references/report-formats.md`
  - contains the stakeholder-summary template, repo weekly-doc checklist, and combined completion checklist
