---
name: library-research-protocol
description: Use when Codex needs to investigate, compare, or document external libraries, OSS projects, SDKs, tools, model/data pipelines, source-intake candidates, capability manifests, backend planner options, duplicate-implementation risk, or ROUTIVA third_party source notes. Trigger for requests like "research this library fully", "compare overlapping capabilities", "write capability manifest", "avoid duplicate implementation", "investigate NeMo Curator/Deepchecks/PyRIT", or Korean equivalents such as "라이브러리 조사", "기능을 온전히 파악", "중복 구현 방지", "Capability Manifest 작성".
---

# Library Research Protocol

## Purpose

Use this skill to turn library research from a marketing summary into source-verified capability intelligence. The output must help a product or engineering planner decide whether to use a library as a dependency, adapter backend, benchmark, feature-harvest reference, or not at all.

## Non-Negotiables

- Treat capabilities as the unit of research, not the library brand.
- Verify current facts from official source surfaces: repository, release/tag, package registry, official docs, source tree, license, and runtime metadata.
- Distinguish `main`/`develop`, latest release, latest package version, docs version, and checked date.
- Distinguish OSS package, hosted/cloud product, enterprise feature, model weights, datasets, and provider/service terms.
- Do not claim "all features" unless the required research surfaces were checked and coverage gaps are stated.
- Do not mark a multi-library batch skim as `capability-family`. Batch research is only `preliminary-overlap-map` until each library has its own source tree / docs / tutorial / release / dependency deep dive.
- Never let external libraries own product decisions. They provide evidence or execution; the host product owns route selection, policy, quality gates, lineage, and final decisions.
- Record license/privacy/runtime constraints alongside capabilities, not as an afterthought.
- Mark the research coverage level: `overview`, `capability-family`, or `implementation-ready`.

## Workflow

1. Define the decision context.
   - Identify the target library, source URL, expected product pipeline/stage, and whether the user needs overview, capability-family, or implementation-ready evidence.
   - If working in ROUTIVA, map to D2D, D2R, R2M, or M2D.

2. Gather source-verified identity.
   - Check repository URL, default branch commit, latest release/tag, package registry version, license file, package metadata, docs URL/version, and current date.
   - Use web for changing/current facts. Prefer official sources. Use source clones for source tree and runtime behavior.

3. Map the source tree.
   - Use `rg --files`, `find`, `rg -n`, package manifests, docs navigation, examples, and tutorials.
   - Group modules/classes/features into feature families. Avoid copying raw file lists into the final note unless useful.

4. Inspect runtime and governance surfaces.
   - Dependencies, optional extras, Python/Node/runtime bounds, GPU/distributed requirements, cloud/provider clients, API keys, telemetry, dotenv behavior, local storage, output logs, data retention, and sensitive artifacts.
   - Check model weights, datasets, hosted service terms, and generated-data ownership separately from code license.

5. Build the Feature Family Inventory.
   - Summarize every material capability family with what it includes and how the host product should interpret it.
   - Mark included, excluded, pending, deprecated, partial, cloud-only, enterprise-only, experimental, or legacy paths.
   - Map install extras/package options to feature families when they change runtime behavior.

6. Build the Capability Manifest.
   - Use capability IDs like `text_deduplication`, `schema_contract_validation`, or `red_team_strategy_executor`.
   - For each capability, include Korean explanation, product pipeline/stage, inputs, outputs/signals, and constraints.

7. Build the Alternatives Matrix.
   - For each important capability, list overlapping libraries and explain when to prefer, avoid, or combine them.
   - Include license/runtime/privacy tradeoffs. This is the duplicate-implementation gate.
   - Ask: is this capability already in the registry; do its inputs/outputs fit the StageContract; can an adapter mapper resolve mismatches; is a safer candidate available; is the planned code external-backend glue or a duplicate implementation?

8. Decide planner role.
   - Classify each library as `GREEN`, `YELLOW`, or `RED`.
   - Classify use mode as `dependency`, `adapter`, `benchmark only`, `feature-harvest`, `fallback`, or `not recommended`.
   - For planner output, separate `single-backend`, `composite-backend`, and `feature-harvest` plans.

9. Write artifacts.
   - For a source note or registry update, read `references/source-note-template.md`.
   - In ROUTIVA, update `third_party/sources/<library>.md`, `third_party/registry.md`, and `third_party/source-capability-matrix.md` when the user requests durable research.

10. Verify before finalizing.
   - Run markdown/diff checks where applicable, usually `git diff --check`.
   - Use `rg` to confirm key markers, capability IDs, registry rows, and matrix rows exist.
   - Report what was verified and what remains uncertain.

## Coverage Levels

| Level | Meaning | Minimum evidence |
|---|---|---|
| `overview` | Basic purpose and fit | README/docs overview, license, source identity |
| `capability-family` | Decision-grade feature map | README, docs, examples/tutorials, source tree, release/package, deps, license, runtime/privacy, alternatives matrix |
| `implementation-ready` | Adapter-ready for selected capabilities | Public API/config, input/output schema, error modes, smoke test, pinned version, artifact mapper plan, license/provider terms |

Use `capability-family` as the default for planning. Use `implementation-ready` only for capabilities the user intends to implement now.

## Required Research Surfaces

Check these surfaces before declaring `capability-family`:

| Surface | What to verify |
|---|---|
| README / overview | official positioning, quickstart, representative workflow |
| Official docs | feature guide, concepts, API reference, runtime/deployment guide |
| Tutorials / examples | hidden workflow families, actual input/output patterns |
| Source tree map | package/module/stage/class/function families |
| Install extras / dependencies | optional extras, GPU/CUDA/Ray/service/OS/container conditions |
| Release notes / tags | recent architecture changes, deprecations, known issues |
| License / model / data terms | code license, model weights, datasets, hosted terms |
| Runtime behavior | local/hosted, batch/distributed jobs, secrets, telemetry, storage |
| Output artifacts | reports, metrics, datasets, embeddings, model artifacts, external links |

## Duplicate-Implementation Gate

Before proposing ROUTIVA-owned code or a new adapter, answer:

1. Does a registry library already provide this capability?
2. If yes, do its inputs, outputs, artifacts, and quality signals fit the host StageContract?
3. If not, can an Adapter or ArtifactMapper resolve the mismatch?
4. Is there a safer alternative by license, privacy, runtime, egress, or maintenance status?
5. Is the proposed code product-owned contract glue, or is it reimplementing an external backend?

If these answers are missing, do not start implementation. Continue research or mark the capability as pending.

## Confidence Labels

| Label | Meaning |
|---|---|
| `high` | official docs/source/tutorials were checked and alternatives were compared |
| `medium` | official evidence supports the capability, but API/runtime deep dive remains |
| `low` | README or secondary evidence dominates; source/API confirmation is insufficient |

## Subagents

Use subagents only when the user explicitly asks for multi-agent/subagent work or the active workspace instructions authorize it. Good splits are:

- one library per subagent,
- docs/release/runtime vs source-tree/license surfaces,
- independent alternatives for the same capability.

Ask subagents for evidence and uncertainty, not polished conclusions. Cross-check their findings against official sources before writing durable artifacts.

## Output Rules

- Lead with the decision-relevant distinction, not a generic description.
- Keep library capabilities decomposed. Avoid "Library adapter" as the only unit.
- Use Korean explanations for capability rows when the target artifact is Korean or ROUTIVA-facing.
- Include source links in the artifact. Keep quotes short and paraphrase long source material.
- Call out uncertainty plainly: package metadata mismatch, stale docs, release-vs-main divergence, cloud-only features, telemetry not found, unsupported bridges, or license ambiguity.

## Verification Checklist

Before claiming completion, confirm:

- source identity and version pins are recorded,
- feature families are broader than README bullets,
- capability manifest exists,
- alternatives matrix exists,
- license/runtime/privacy constraints are recorded,
- planner role and route ownership are separated,
- coverage level and pending gaps are stated,
- durable registry/matrix rows are updated when relevant,
- verification commands passed or known gaps are reported.
