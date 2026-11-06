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

## End-to-end research benchmark audit gates

- Pin numeric results to the exact paper revision and configuration, not the floating leaderboard. Re-fetch the official page before publication: cached extraction or an earlier worker snapshot can show an older cohort. Do not publish a discrepancy that a current direct read no longer reproduces.
- Separate planned evaluation slots, generated rollouts, completely scored outcomes, and resource-limit failures. Parse reported missing-slot rows and compute denominators in code; if totals differ, retain the uncertainty rather than inventing a cause or silently changing the denominator.
- Trace the scoring contract: deterministic tests and all mandatory rubric blockers can gate a non-blocker weighted score. Keep overall pass, pre-gate rubric score, final gated score, Pass@1 and task-level Pass@k distinct. Research-quality rubric success is not verified journal acceptance or novel discovery.
- Keep human-reviewed error cohorts, corrected labels, rerun benchmark results, and second-reviewer experiments separate. Multi-label error counts need not sum to failed outcomes, and not every grading-error tag changes the final verdict. Report reviewer family/self-preference risks without assuming that either reviewer is ground truth.
- Treat author-reference manuscript scores as a selected-criteria sanity check, not judge accuracy, human agreement, or a full end-to-end baseline. Inspect blocker failures even when non-blocker scores are high, and do not automatically label every such failure a proven evaluator error.
- Verify release coverage per surface: a generic SDK, one task's input bundle, and contribution-stage trajectory archive do not establish a public complete benchmark/evaluator/full-run release. Check actual file lists as well as READMEs; dataset metadata and retained upstream data notices have distinct license scopes. A public 404 does not distinguish private, deleted, or moved repositories.

## Category cue
If the artifact is primarily about specialist-agent orchestration, lineage sharing, supervisor loops, evaluator-owned feedback, or a research harness, prefer `agent-systems` even when the experiments optimize training recipes. Use `model-training` only when the article's center of gravity is the learning dynamics or training method itself.
