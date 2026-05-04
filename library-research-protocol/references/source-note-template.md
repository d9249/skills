# Source Note Template

Read this reference when writing a durable library source note, registry row, or capability matrix entry.

## Required Source Note Shape

```markdown
# Library Name

## 기본 정보

- Source:
- Docs:
- Package registry:
- Version / Commit:
- License:
- Runtime:
- Registry:
- ROUTIVA 위치:
- Primary pipelines:
- Support pipelines:
- Not primary:
- Coverage level:

## 공식 Positioning / 한 줄 판단

State what the library is and what it is not. Separate OSS, hosted/cloud, enterprise, model, dataset, and service boundaries.

## Feature Family Inventory

| Feature family | 포함 기능 | ROUTIVA/제품 해석 |
|---|---|---|
|  |  |  |

## Capability Manifest

| Capability | 한국어 설명 | Pipeline / stage | 입력 | 출력 / signal | 제약 |
|---|---|---|---|---|---|
| `capability_id` |  |  |  |  |  |

## Output / Artifact Shape

| Artifact | Shape | Product mapping |
|---|---|---|
|  |  |  |

## Alternatives Matrix

| Capability | Candidate libraries | Overlap | Preferred when | Avoid / defer when | Product decision |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Workflow Fit

```text
Workflow:
Required capabilities:
  -
Backend plan:
  -
Product-owned:
  -
```

## BackendPlanner 규칙

- `condition=true`이면 후보로 둔다.
- `license_policy=...`이면 제외하거나 benchmark-only로 둔다.
- `privacy_or_egress_blocked=true`이면 fallback을 사용한다.

## Product-Owned Boundaries

- route decision
- WorkflowDraft/state transition
- quality gate and promotion
- lineage and artifact mapper
- user review/approval
- final decision report

## Runtime / License / Privacy 제약

- license and NOTICE duties
- provider/API key egress
- telemetry and analytics
- local/cloud storage
- sensitive logs/reports/artifacts
- model/data/hosted terms

## Adapter Readiness Checklist

- [ ] version is pinned
- [ ] minimal smoke test plan exists
- [ ] public API/config is identified
- [ ] input/output mapper is known
- [ ] secrets/egress policy is defined
- [ ] artifact redaction/retention is defined
- [ ] alternatives were checked

## Research Coverage

- Coverage level:
- Confidence:
- Decision readiness:
- Implementation-ready capabilities:
- Pending deep-dive capabilities:
- Duplicate-implementation check:

## 조사 출처

- official repository, checked YYYY-MM-DD
- official docs, checked YYYY-MM-DD
- package registry, checked YYYY-MM-DD
- release/tag metadata, checked YYYY-MM-DD
```

## Registry Row Pattern

```markdown
| Name | Source | Version / Commit | License | Class | Intake mode | Product location | Notes |
```

Class guidance:

- `GREEN`: permissive and acceptable by default, still subject to provider/model/data terms.
- `YELLOW`: permissive or usable but distribution, egress, privacy, runtime, hosted, enterprise, or dependency blast-radius review is needed.
- `RED`: do not import into core/dependency/runtime; benchmark or reference only.

## Matrix Row Pattern

```markdown
| Capability cluster | Candidate libraries | Primary fit | Decision rule |
```

The matrix should reveal overlap and stop duplicate implementation. It should not repeat the full source note.
