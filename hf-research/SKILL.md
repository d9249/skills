---
name: hf-research
description: "Research Hugging Face models from a model URL or `org/model` repo id and draft a Korean internal briefing that separates model-card claims, official upstream information, official paper/technical-report evidence, third-party evidence, community discussion evidence from GeekNews/Hacker News, local smoke-test results, and explicit inferences. Use when Codex needs to explain performance, differentiators, base-model deltas, deployment traits, risks, paper-backed architecture claims, real-user pain points, and best-fit use cases for internal sharing."
---

# HF Research

## Overview

Use this skill to turn a Hugging Face model link into a Korean internal research briefing.
The default deliverable is a mixed-format Markdown memo: a short decision memo first,
then a technical narrative.
When public literature exists, the briefing should explicitly reference the actual
paper or technical report rather than relying only on the model card summary.

## Quick Start

1. Normalize the input to a Hugging Face model repo id.
2. Run:

```bash
python ~/.codex/skills/hf-research/scripts/collect_hf_model_snapshot.py \
  <hf-url-or-repo-id>
```

Add `--with-third-party` when you want external review and community discussion
candidates, and add `--with-local-smoke` when it is worth attempting a safe
local smoke test.

3. Read:
   - `references/source-policy.md`
   - `references/model-family-rubric.md`
   - `references/report-template.md`
4. Identify the official paper or technical report for the current repo. If the
   repo is mainly a derivative, quantization, or tuning package and does not
   link its own paper, trace the `base_model` paper or upstream technical report
   instead. If a Hugging Face paper page or arXiv link is present, use the
   `hugging-face:huggingface-papers` skill or the linked official page to read
   the primary source.
5. Compare the current repo with `base_model` when present. If there is no
   `base_model`, say so explicitly.
6. Draft the briefing in Korean and label every non-trivial claim with one of
   the required evidence classes.
7. If paper evidence, external evidence, or local execution is unavailable,
   keep the section and write `미확인` or `미수행` plus the reason.

## Workflow

### 1. Ground the repo and literature

- Prefer HF public metadata, raw README, file tree, linked paper/technical
  report URLs, structured benchmark files, and serving notes before broader web
  search.
- Capture repo id, pipeline tag, library, license, base model, creation/update
  dates, tags, notable files, linked references, paper candidates, and
  discussion candidates from `news.hada.io` and `news.ycombinator.com` when
  available.
- Treat benchmark JSON/CSV/JSONL shipped in the repo as model-publisher evidence,
  not independent validation.
- For architecture, training recipe, modality, or algorithmic novelty claims,
  prefer the actual paper or technical report wording over README marketing
  phrasing.
- Treat GeekNews/Hacker News discussion threads as high-signal field reports for
  usability, hidden gotchas, deployment friction, and community reception, not
  as standalone proof of benchmark superiority.

### 2. Decide the briefing angle

- Use the family-specific checklist in `references/model-family-rubric.md`.
- If the repo is mainly a format, quantization, or tuning package, center the
  report on packaging, tuning, deployment, and benchmark deltas instead of
  inventing architecture novelty.
- If the current repo has no paper but the base model does, treat the base model
  paper as the upstream source for architecture/training context and keep repo-
  specific packaging or tuning claims separate.
- If the repo documents real architecture or training changes with official
  sources, explain them in the lower narrative section.

### 3. Separate evidence classes

Use exactly these labels:

- `[모델 카드 자기주장]`
- `[공식 자료]`
- `[제3자 자료]`
- `[로컬 검증]`
- `[추정]`

Rules:

- Do not merge evidence classes in one bullet unless you explicitly contrast them.
- Official papers and technical reports belong under `[공식 자료]`.
- GeekNews/Hacker News threads belong under `[제3자 자료]`.
- If speed numbers come from different hardware, prompts, serving stacks, or token
  budgets, do not present them as directly comparable.
- If a structured benchmark file is published by the repo author, keep it under
  `[모델 카드 자기주장]` unless an independent evaluator reproduced it.

### 4. Write the report

- Follow `references/report-template.md`.
- Keep the top `TL;DR` to 3-5 bullets.
- Keep a `기본 정보 표` with evidence in the rightmost column.
- Always include `관련 논문/공식 문헌`. If no paper or technical report is
  found, write `[공식 자료] 미확인: ...` with the reason.
- Include `커뮤니티 반응/실사용 코멘트` when relevant. Prefer threads from
  `news.hada.io` and `news.ycombinator.com`, and write `[제3자 자료] 미확인: ...`
  when no relevant discussion is found.
- Always include `리스크/한계` and `적합/부적합 용도`, even when evidence is sparse.
- Quote numbers sparingly and tie each number to a source.
- Use short, scan-friendly Korean prose.

## Completion Checks

- Paper or technical report found, or explicit `미확인` note present
- Community discussion captured or explicit `미확인` note present
- Architecture/training claims are tied to paper/official documentation or marked uncertain
- Base model compared or explicitly absent
- Report structure matches the template
- All benchmark and differentiator claims have evidence labels
- Missing third-party or local validation is called out, not silently omitted

## Resources

- `scripts/collect_hf_model_snapshot.py`
  - collects HF metadata, README sections, related files, base-model context,
    related variants, paper candidates, community discussion candidates,
    optional third-party candidates, and optional safe local smoke status
- `references/source-policy.md`
  - evidence labeling and interpretation rules
- `references/model-family-rubric.md`
  - required comparison axes by model family
- `references/report-template.md`
  - default Korean briefing template and wording rules
