# Source Policy

## Evidence Order

Use sources in this order unless a stronger source clearly exists:

1. Hugging Face public metadata and raw repo files
2. Official papers, technical reports, and base-model upstream official materials
3. Third-party reviews and independent benchmarks
4. Community discussions such as GeekNews (`news.hada.io`) and Hacker News (`news.ycombinator.com`)
5. Local smoke-test evidence
6. Explicit inference when the public record is incomplete

## Required Evidence Labels

Use exactly one of these labels on each substantive claim:

- `[모델 카드 자기주장]`
- `[공식 자료]`
- `[제3자 자료]`
- `[로컬 검증]`
- `[추정]`

## Interpretation Rules

- Treat model-card numbers, repo-shipped benchmark files, and README claims as
  publisher claims, not independent validation.
- Treat base-model HF pages, vendor blogs, vendor docs, official GitHub repos,
  and official papers as `[공식 자료]`.
- Treat external benchmarks, community reviews, and independent repos as
  `[제3자 자료]`.
- Treat GeekNews and Hacker News discussion threads as `[제3자 자료]`.
- Treat your own run logs, prompt traces, errors, or local latency numbers as
  `[로컬 검증]`.
- Treat any unconfirmed bridge statement as `[추정]`.

## Literature Rules

- For architecture, training objective, data recipe, modality expansion, or
  algorithmic novelty claims, prefer the actual paper or technical report over a
  README summary when both exist.
- If the current repo is a derivative, quantization, packaging, or tuning layer
  without its own paper, use the base-model paper as the upstream architecture
  source and keep repo-specific deltas under model-card or inference evidence as
  appropriate.
- If no paper or technical report is found for a claim that would normally need
  one, write `[공식 자료] 미확인` and avoid restating README marketing language as
  established fact.

## Community Discussion Rules

- Prefer GeekNews (`news.hada.io`) for Korean practitioner reactions and Hacker
  News (`news.ycombinator.com`) for broader English-language practitioner
  reactions when relevant threads exist.
- Use these threads for deployment quirks, quality complaints, adoption signals,
  undocumented behavior, prompt-format gotchas, and operational tradeoffs that
  official docs often omit.
- Do not use a community thread as the sole basis for architecture, training
  method, benchmark, license, or safety claims.
- If a thread only summarizes an external article, follow the article and/or the
  official source before elevating the claim.
- Quote community consensus carefully: distinguish one loud comment from a
  repeated pattern across multiple commenters or threads.

## Comparison Rules

- Do not compare speed numbers across different hardware, prompt lengths,
  decoding settings, or serving stacks as if they were apples-to-apples.
- Separate format and deployment changes from architecture changes.
  - Quantization, GGUF/MLX/AWQ packaging, chat-template fixes, and runtime tuning
    are not architecture changes by themselves.
- If the current repo is a derivative of a base model, compare:
  - supported modality
  - serving/runtime format
  - context or visible limits
  - benchmark claims
  - risk profile
- If `base_model` is absent, state that upstream lineage is not declared.
- If no paper or technical report is found for either the current repo or the
  base model, say that literature-backed architecture comparison is limited.
- If community discussion is absent, say that practitioner-reported pain points
  or adoption sentiment could be under-observed.

## Missing Information Rules

- Never omit a section because evidence is missing.
- Write `미확인` when a public source should exist but was not found.
- Write `미수행` when local verification was skipped or unsafe.
- Include the reason:
  - no public source
  - runtime unavailable
  - download cost too high
  - gated model
  - ambiguous repo lineage

## Risk Flags To Call Out

- uncensored or abliterated positioning
- unknown training data or unclear post-training recipe
- benchmark methodology not independently reproduced
- no paper or technical report found for architecture/training claims
- practitioner complaints or deployment gotchas surfaced only in community threads
- serving/template fixes presented as capability gains
- derivative licensing constraints from the base model
