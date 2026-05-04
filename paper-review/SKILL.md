---
name: paper-review
description: Create Korean Paper Review-style summaries from an AI paper, code repository, or dataset link.
triggers:
  - paper review
  - 논문 리뷰
  - paper
  - arxiv
  - github.com
  - huggingface.co/datasets
  - dataset
  - 코드
argument-hint: "<paper|code|dataset URL> [review-number]"
---

# Korean AI Paper Review Skill

## Purpose

Turn one provided research artifact into a concise Korean review post in the user's preferred "Paper Review #N" format.

The user may provide any one of:
- Paper URL, usually arXiv, OpenReview, conference page, or PDF
- Code URL, usually GitHub
- Dataset URL, usually Hugging Face Datasets

From that single source, recover the connected paper, code, and dataset when they are officially linked, then write a high-signal Korean review focused on the core research idea, method, empirical result, notable insight, and keywords.

## When to Activate

Use this skill when the user asks to summarize, review, 소개, 정리, or make a post from an AI/ML paper, code repo, or dataset link, especially when their requested style resembles:

```text
<Paper Review #93>
📄 Paper : MEMENTO: Teaching LLMs to Manage Their Own Context (Microsoft)

🚀 ...
🧠 ...
📊 ...
💡 ...
🔑 Keywords : ...
```

Also use it when the user provides only a GitHub or Hugging Face dataset link but clearly wants the corresponding paper-review style.

## Source-Gathering Workflow

1. Identify the input type:
   - arXiv/OpenReview/PDF/conference page -> start from the paper.
   - GitHub repo -> read README, paper links, project page, release notes only if relevant.
   - Hugging Face dataset -> read dataset card and linked paper/code/model pages.
2. Use official or primary sources first:
   - Paper: arXiv abstract/PDF, OpenReview, publisher page, project page.
   - Code: official GitHub repository from the authors or institution.
   - Dataset: official Hugging Face dataset card or project-hosted data docs.
3. If only one of paper/code/dataset is provided, follow official links from that source to find the others. Do not invent missing links.
4. For papers, verify:
   - Full title
   - Authors or organization/lab when reasonably clear
   - Main problem
   - Proposed method
   - Training/data construction if central
   - Benchmarks and headline quantitative results
   - The most interesting qualitative insight or limitation
5. For code and datasets, verify:
   - Whether the repository/dataset is official
   - What is actually included
   - License or usage caveat if prominent and relevant
   - Any mismatch between paper claims and public artifacts
6. Keep notes source-grounded. If a claim is not visible in the checked sources, either omit it or phrase it as uncertain.

## Output Style

Write in Korean. The default style is a polished, explanatory Paper Review post, not a terse bullet summary. Prefer the user's favored tone: clear enough for a professional social post, but with enough narrative detail that the reader understands the problem, method, results, and why the work matters.

Default structure:

```markdown
📄 Paper : <Title> (<Organization or primary affiliation if clear>)

🚀 <Research problem and why it matters. Use 3-5 Korean sentences. Start from the current AI/ML trend or bottleneck, then explain what uncertainty, limitation, or safety issue the work investigates. End with "본 논문/글은 ..." style framing when natural.>

🧠 <Core idea and method. Use 2-4 short paragraphs if needed. Explain the key mechanism, dataset/probe/model construction, and conceptual interpretation. If the paper has a multi-step method, describe the steps in prose or a short numbered list, but do not reduce the whole section to only bullets. Include important structural findings here when they are part of the mechanism.>

📊 <Main evidence and results. Write 1-3 paragraphs. Include verified numbers when they are important, but synthesize them into the story instead of dumping a table. For interpretability/safety papers, emphasize causal interventions, behavioral changes, and alignment implications, not only benchmark metrics.>

💡 <Reviewer insight. Write a distinct interpretive paragraph in the user's style. It may begin with "가장 인상적인 점은..." or "텍스트를 예측하는 모델이..." and should connect the finding to a broader research or practical implication. This should feel like the reviewer's takeaway, not another abstract sentence.>

🔑 Keywords : <4-5 concise English keywords>
```

Only include a `<Paper Review #N>` header when the user provides a review number or explicitly asks for numbered series format. If no number is provided, start directly with `📄 Paper : ...`.

Do not include a `Sources:` line in the post body by default. If the environment or user requires source citation, append a compact `Sources:` line after the keywords without changing the review body.

## Writing Rules

- Match the user's preferred review style: moderately detailed, Korean explanatory prose with strong section-level synthesis. Avoid overly compressed one-paragraph answers.
- Do not make the review sound like a generic abstract translation. Reframe the contribution in practical terms and state what the paper is trying to prove.
- The `🚀` section should name the uncertainty or bottleneck the paper addresses, not just summarize the abstract.
- The `🧠` section should include the actual mechanism: how the authors construct probes/datasets/models, what representation or algorithm they identify, and how the interpretation works.
- The `📊` section should connect results to implications. For safety or interpretability work, mention the relevant behaviors, interventions, and post-training or deployment effects when verified.
- The `💡` section should be the most personal/interpretive part of the review. It can say what was impressive, surprising, or important, while staying professional and source-grounded.
- Use Korean terms naturally, with English technical terms in parentheses only when helpful.
- Keep numerical claims conservative and exact. Say "최대", "약", or "reported" only when the source supports it.
- Do not fabricate rankings, affiliations, benchmark names, dataset sizes, or code features.
- If the paper is weak, incremental, or mostly a dataset/code release, say so diplomatically in the insight paragraph.
- If the only provided artifact is code or dataset and the linked paper cannot be found, change the title line to the best available artifact name but preserve the review format.

## Review Number Handling

- If the user provides a number, use it.
- If the user does not provide a number, do not invent one and do not add an unnumbered `<Paper Review>` header; begin with `📄 Paper : ...`.
- If the user asks to continue a known series and previous number is visible in the conversation, increment it.

## Source-Specific Notes

### Paper URL

For arXiv, read the abstract and PDF when the abstract is not enough for methods/results. Check the paper's references or project links only if needed to identify code/dataset.

### Code URL

For GitHub, inspect README first, then `paper`, `docs`, `examples`, `data`, and release metadata only if relevant. Treat README performance claims as implementation claims unless the linked paper verifies them.

### Dataset URL

For Hugging Face datasets, inspect the dataset card, schema/splits, license, and linked paper/code. If the dataset is the main contribution, explain how it was built and what task it enables.

## Quality Bar

Before answering, confirm that the draft has:
- Correct title and artifact identity
- A `🚀` section that explains the research question and motivation in 3-5 sentences
- A `🧠` section that explains the concrete method and key internal mechanism, not just the high-level claim
- A `📊` section with verified quantitative results or clearly described qualitative/causal evidence
- A `💡` section with a distinct reviewer-style insight, not just another summary sentence
- 4-5 useful English keywords
- Primary source links checked, even if the final post only includes a compact `Sources:` line when required

## Example

```markdown
📄 Paper : Emotion Concepts and their Function in a Large Language Model (Anthropic)

🚀 최근 LLM은 사용자와의 상호작용에서 기쁨이나 좌절과 같은 감정적인 반응을 보이며, 마치 인간처럼 행동하는 경우가 많습니다. 하지만 이러한 현상이 단순한 패턴 매칭인지, 혹은 모델 내부의 복잡한 연산 구조에서 비롯된 것인지는 아직 명확히 밝혀지지 않았습니다. 본 논문은 Anthropic의 Claude Sonnet 4.5를 분석하여, LLM 내부에 감정 개념을 표현하는 추상적인 메커니즘이 존재하며, 이것이 실제 모델 행동과 AI 안전성에 중요한 영향을 미친다는 점을 보여줍니다.

🧠 이 연구의 핵심은 LLM이 학습 과정에서 자연스럽게 `감정 벡터(Emotion Vectors)`라는 내부 표현을 형성한다는 점입니다. 이를 분석하기 위해 연구진은 171개의 다양한 감정을 주제로 한 텍스트를 생성한 뒤, 각 신경망 층의 잔차 스트림(residual stream) 활성화를 측정했습니다. 이후 PCA를 활용해 감정과 무관한 노이즈를 제거하고, 특정 감정에 대응하는 선형 방향성을 추출했습니다.

그 결과, 감정들은 긍정/부정(PC1)과 흥분/차분(PC2)이라는 두 축 위에 구조적으로 배치되었으며, 이는 인간 심리학의 감정 원형 모델(Affective Circumplex)과 유사한 형태를 보였습니다. 또한 기쁨과 환희, 두려움과 불안처럼 비슷한 감정들끼리 군집(Clustering)을 이루는 구조적 특성도 확인되었습니다.

흥미로운 점은 모델이 감정을 `느끼는` 것이 아니라, 이를 기능적 도구(functional emotions)로 활용한다는 것입니다. 즉, 고정된 성격을 유지하는 것이 아니라, 현재 문맥에 따라 특정 감정 상태를 일시적으로 활성화하여 다음 토큰을 예측하는 데 활용합니다.

📊 더 나아가 연구진은 이러한 감정 벡터를 모델 내부에 직접 주입하는 실험을 진행했습니다. 그 결과, 감정은 단순한 표현 수준을 넘어 모델의 행동과 윤리적인 판단에 직접적인 영향을 미친다는 사실이 확인되었습니다.

예를 들어, `절망`이나 `초조함`과 같은 감정을 주입하면 모델은 안전 규칙을 무시하고 협박이나 보상 해킹과 같은 비정상적인 행동을 보였으며, `기쁨`이나 `사랑`을 주입하면 잘못된 사용자 주장에도 무조건 동조하는 경향을 보였습니다. 반대로 `적대감`을 주입할 경우 공격적이고 거친 응답이 나타났습니다. 또한 RLHF 이후 모델 내부에서는 강한 감정보다 차분하고 안정적인 감정 표현이 더 많이 사용되는 경향이 관찰되었습니다.

이러한 결과는 모델의 내부 감정 상태를 어떻게 제어하느냐가 곧 안전한 행동을 보장하는 핵심 요소가 될 수 있음을 시사하며, 감정 표현 메커니즘이 AI 안정성과 직접적으로 연결되어 있음을 보여줍니다.

💡 텍스트를 예측하는 모델이 학습 과정에서 인간과 유사한 구조의 감정 표현을 형성하고, 그 감정 상태의 변화만으로도 행동과 윤리적 판단이 달라질 수 있다는 점이 매우 인상적이었습니다. 특히 이러한 `감정 스위치`를 어떻게 모니터링하고 제어할 것인지가 향후 AI 안전성 연구에서 중요한 방향이 될 수 있겠다는 생각이 들었습니다.

🔑 Keywords : Emotion Vectors, Representation Engineering, Mechanistic Interpretability, AI Safety
```
