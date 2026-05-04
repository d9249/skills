---
name: current-diff-commit-ko
description: Write a Korean git commit message from the repository's current modified files only. Use when the user asks for a commit message based on the current code changes, current diff, current working tree, or explicitly says not to rely on previous conversation/history. Inspect git status and current diffs first, base the message only on files currently changed, and avoid mentioning features not present in the live working tree.
---

# Current Diff Commit Ko

## Overview

Inspect the repository's current working tree and draft a Korean commit message that reflects only the files currently modified.
Ignore previous chat context, stale assumptions, and features that are not visible in the live diff.

## Workflow

1. Run `git status --short --untracked-files=all` and `git diff --stat` first.
2. Treat the current working tree as the only source of truth.
3. Separate real code/config/docs changes from generated or runtime artifacts.
4. Read enough of the relevant diff to understand the dominant theme before writing.
5. Choose the commit type from the current diff only.

## Type Selection

- Use `feat` for a new capability, workflow, or user-visible behavior.
- Use `fix` for a bug fix or incorrect behavior correction.
- Use `refactor` for structural cleanup without a new capability.
- Use `chore` for tooling, build, config, generated manifests, or housekeeping.

## Scope Selection

- Pick one dominant area from the changed files, such as `history`, `template`, `layout`, `parser`, `admin`, `research`, `build`, `auth`, or `ui`.
- Keep the scope singular and tied to the main change theme.
- If no clear area dominates, prefer the smallest honest scope instead of inventing a broad one.

## Current-Diff Rules

- Mention only what can be justified by the files currently changed.
- Do not reuse commit themes from earlier chat turns unless the current diff still supports them.
- If the user says "현재 수정된 코드들만", ignore prior assistant summaries completely.
- If generated files and code files are mixed, summarize the code/config/theme first.
- Ignore runtime noise and generated state unless the current diff is actually about those artifacts.

Usually ignore these unless the user explicitly wants them included:

- `data/`, `results/`, `logs/`, `out/`
- `.db`, `.sqlite`, `.enc`, `.sig`, lock files
- temporary directories and runtime state

## Output Format

Use this exact style:

```text
type(scope): 한 줄 요약

- 현재 diff에서 확인되는 핵심 변경 1
- 현재 diff에서 확인되는 핵심 변경 2
- 현재 diff에서 확인되는 핵심 변경 3
```

## Writing Guidelines

- Write the subject and bullets in Korean.
- Keep the subject concrete and short.
- Prefer 3 to 6 bullets.
- Keep each bullet grounded in the current modified files.
- If only one small file changed, keep the message short instead of inflating it.
- If the user asks to rewrite again, re-check the working tree before answering.

## Useful Checks

- `git diff --name-only`
- `git diff --unified=1 -- <relevant files>`
- `git status --short --untracked-files=all`
