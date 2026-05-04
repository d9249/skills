# Weekly Report Formats

Use this file when `$weekly-report` triggers and you need the exact delivery format.

Default contract:

- produce the stakeholder summary and the repo weekly doc in the same run
- use one shared boundary calculation
- use one shared workstream grouping
- consider the task incomplete if only one output is finished

## 1. Stakeholder Summary Template

```text
YYYYMMDD

기준 범위: <first-date> 첫 커밋 `<first-sha>` ~ <last-date> 최신 커밋 `<last-sha>`
참고: 지난 보고 종료 커밋 `<base-sha>` 이후 총 <count>건 커밋 기준으로 정리했습니다.

금주 진행사항
1. <workstream title> (<owner>)
: <1-3 sentence summary>

2. <workstream title> (<owner>)
: <1-3 sentence summary>

차주 진행사항
1. <next validation or follow-up> (<owner>)
: <1-2 sentence plan>
```

Rules:

- Keep the date line as `YYYYMMDD`.
- Use the first included commit after `base`, not the `base` commit itself, on the left side of `기준 범위`.
- The `참고:` line should mention the previous report end commit and total commit count.
- Group multiple commits into one workstream. Do not create one item per commit.
- Prefer outcome-first titles such as `연구 비교 대시보드`, `템플릿 OCR 보정`, `작업실 UX 재편`.

## 2. Repo Weekly Doc Checklist

When the repo already has weekly docs, mirror the nearest existing file.

For repos like `pp-ocr`, keep this structure:

```text
# 2026-WNN 작업일지

- 기간: YYYY-MM-DD ~ YYYY-MM-DD
- 기준 범위: `base..head`
- 커밋 수: N

## 주간 요약
...

## 핵심 작업
...

## 대표 변경 파일
...

## 비고
...

## 커밋 메모
...
```

Rules:

- Reuse the tone and section order from the nearest existing weekly file.
- If the repo also has weekly indexes, update them in the same change.
- Mention if the report is a mid-week or mid-day snapshot.
- In `비고`, separate actual code or product changes from bulk generated artifacts when the diff is noisy.
- In `커밋 메모`, be detailed enough that a reader can trace what happened during the week without reopening `git log`.

## 3. Combined Completion Checklist

Before finishing, confirm all of the following:

- stakeholder summary text is drafted
- repo weekly doc is created or updated
- any related history index files are synced
- SHAs, dates, and commit counts match the computed boundary
- grouped workstream names are consistent across both outputs

## 4. Workstream Grouping Heuristics

Default grouping order:

1. user-facing feature or workflow change
2. research or benchmark infrastructure
3. backend or runtime change
4. documentation or reporting surface
5. supporting artifacts or snapshots

Good grouping examples:

- `템플릿 OCR 리포트와 이력 요약 추가`
- `Falcon-OCR 비교군과 결과 비교 대시보드 확장`
- `PP-DocLayoutV3 기본 백엔드 정비`
- `초보자/숙련자 시작 화면과 작업실 흐름 재편`

Avoid:

- repeating raw commit subjects verbatim
- listing every file touch as a separate item
- over-weighting line counts when generated data dominates the diff
