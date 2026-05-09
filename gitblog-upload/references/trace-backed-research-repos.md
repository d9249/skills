# Trace-backed research repos

Use this checklist when a paper links to an official GitHub repo that is not just code, but a released experiment trace / harness artifact.

## When this matters
- The paper's main claim is about closed-loop experimentation, agent orchestration, or automated research/search.
- The companion repo exposes run records, blackboards, lineage snapshots, release artifacts, or architecture/task-adapter docs.
- README headline metrics are plausible, but you want stronger grounding for *what was actually released* and *how auditable it is*.

## What to inspect
1. Repo root README
   - Confirm headline task names, reported improvements, environment assumptions, and required credentials/hardware.
2. Architecture docs
   - Look for files like `docs/architecture.md`, `docs/task_adapter.md`, or similarly named design notes.
   - Use them to distinguish the task-agnostic harness/core from task-specific packages.
3. Release-artifact docs
   - Look for `release_artifacts/README.md` or equivalent.
   - These files often state which run records are frozen, what exact best scores are preserved, and which logs/snapshots were omitted.
4. Artifact tree contents
   - Check whether the repo ships blackboard state, `results.tsv`, `best.json`, snapshots, lineage examples, or only high-level code.
5. Packaging maturity
   - Note whether Releases/Tags exist. Absence of releases/tags with presence of rich artifacts usually means "research artifact bundle" rather than polished framework/toolkit.

## Useful blog angles this enables
- "The real product is the auditable trial trajectory, not just the final model/recipe."
- "This is closer to a research harness / experiment operating system than a generic agent demo."
- "The release posture matters: trace-rich artifact bundle vs production-ready platform."

## Category cue
If the artifact is primarily about specialist-agent orchestration, lineage sharing, supervisor loops, evaluator-owned feedback, or a research harness, prefer `agent-systems` even when the experiments optimize training recipes. Use `model-training` only when the article's center of gravity is the learning dynamics or training method itself.
