# Report Template

Default output language: Korean.

Default output structure:

1. `제목`
2. `TL;DR 3-5줄`
3. `기본 정보 표`
4. `관련 논문/공식 문헌`
5. `핵심 차별점`
6. `성능/벤치마크`
7. `커뮤니티 반응/실사용 코멘트`
8. `아키텍처·학습·서빙 포인트`
9. `리스크/한계`
10. `적합/부적합 용도`
11. `출처`

## Title Pattern

Use one of these patterns:

- Architecture-heavy repo:
  - `# <Model> = <Novelty A> & <Novelty B>`
- Derivative packaging or tuning repo:
  - `# <Model> = <Base Model>의 <Packaging/Tuning/Deployment Focus>`
- Non-generative task model:
  - `# <Model> = <Task> 특화 <Key Property>`

If structural novelty is not publicly documented, do not force a flashy
architecture title. Prefer packaging, tuning, deployment, or task-fit framing.

## Table Template

```md
| 항목 | 값 | 근거 |
| --- | --- | --- |
| Repo | `owner/model` | [공식 자료] HF API |
| 파이프라인 | `text-generation` | [공식 자료] HF API |
| 라이브러리/포맷 | `mlx` | [공식 자료] HF API |
| 라이선스 | `gemma` | [공식 자료] HF API |
| 베이스 모델 | `google/gemma-4-26B-A4B-it` | [공식 자료] HF metadata |
```

## Literature Section Rules

- Add `관련 논문/공식 문헌` immediately after the basic info table.
- Cite the current repo's official paper or technical report when available.
- If the current repo is a derivative package without its own paper, cite the
  base model paper and state that repo-specific changes should be interpreted
  separately.
- If no paper is found, write `[공식 자료] 미확인: ...` and avoid overclaiming
  architecture or training novelty.

## Community Section Rules

- Add `커뮤니티 반응/실사용 코멘트` after `성능/벤치마크`.
- Prefer practitioner discussion threads from GeekNews (`news.hada.io`) and
  Hacker News (`news.ycombinator.com`) when relevant threads exist.
- Use this section for lived experience: deployment friction, surprising failure
  modes, prompt-template gotchas, quality impressions, inference cost concerns,
  and integration headaches.
- If no relevant thread is found, write `[제3자 자료] 미확인: ...`.
- Avoid turning one thread into universal truth; call out when evidence is thin
  or anecdotal.

## Tone Rules

- Keep the top section memo-like and decision-friendly.
- Keep the lower section technical, but concise.
- Prefer statements like `공개 자료 기준`, `현재 확인 가능한 범위에서는`, `직접 비교는 곤란` over vague hedging.
- If evidence is weak, say so early.

## Example Evidence Usage

```md
- [모델 카드 자기주장] Quick bench overall은 `95.8`로 제시되어 있으며, 동일 README에서는 원본 4bit baseline `91.4` 대비 개선이라고 주장한다.
- [공식 자료] 현재 repo가 직접 링크한 논문은 `https://arxiv.org/abs/2501.01234` 이며, 아키텍처 설명은 README 요약보다 이 문헌 표현을 우선 근거로 잡는 편이 안전하다.
- [공식 자료] 베이스 모델 `google/gemma-4-26B-A4B-it` 는 Hugging Face 상에서 `image-text-to-text` 파이프라인과 256K context를 표기한다.
- [제3자 자료] GeekNews/Hacker News 토론에서는 설치 난이도, VRAM 체감, prompt template 호환성처럼 공식 문서에 약하게 드러나는 실사용 이슈가 반복적으로 언급되는지 확인한다.
- [제3자 자료] 독립 재현 벤치는 이번 조사 범위에서 확인하지 못했다.
- [로컬 검증] 미수행: 안전한 로컬 런타임과 사전 캐시를 확인하지 못해 다운로드 없이 검증하기 어려웠다.
- [추정] 공개 정보 기준으로 이 repo의 차별점은 신규 아키텍처보다는 MLX 4-bit 배포 패키징과 후속 튜닝에 가깝다.
```

## Closing Checklist

- Every important number has a source label.
- `관련 논문/공식 문헌` is present, even when the answer is `미확인`.
- `커뮤니티 반응/실사용 코멘트` is present, even when the answer is `미확인`.
- `리스크/한계` is present even when the model looks strong.
- Missing third-party or local evidence is explicit.
- The title does not overclaim architectural novelty.
