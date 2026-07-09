# skills

이 저장소는 반복적으로 재사용하는 Codex/Hermes 스타일 스킬들을 모아두는 개인 스킬 라이브러리다.

각 스킬은 보통 다음 형태를 따른다.

- `SKILL.md`: 스킬 본문과 트리거 조건
- `references/`: 필요할 때만 읽는 보조 문서
- `templates/`: 산출물 템플릿
- `scripts/`: 반복 작업 자동화를 위한 도우미 스크립트
- `assets/`: 출력물에 쓰는 정적 리소스

## 새로 반영한 블로그 스킬

### `gitblog-upload`
링크 하나를 한국어 AI 랩 리포트 스타일 블로그 글로 바꾸는 스킬이다.

주요 대상:
- 논문
- GitHub 저장소
- 데이터셋
- Hugging Face 모델/데이터셋 페이지
- 기술 제품/공식 웹사이트

핵심 기능:
- 1차 공식 소스 우선 수집
- 기존 블로그 글 중복 여부 확인 후 업데이트/신규 생성 판단
- 카테고리/슬러그/프론트매터 자동 정리
- 고해상도 이미지 우선 사용
- 읽기 쉬운 짧은 문단과 필요한 표 중심의 글 구성
- 안전한 git add / commit / push 흐름

포함 리소스:
- `references/design-md-catalog-sites.md`
- `references/plugin-runtime-repos.md`
- `references/trace-backed-research-repos.md`
- `templates/blog-post-template.md`

### `gitblog-mvupload`
YouTube 영상을 분석해서 한국어 AI 랩 스타일 블로그 글로 발행하는 영상 전용 스킬이다.

핵심 기능:
- YouTube 메타데이터, transcript, timeline, visual evidence를 분리해서 수집
- 영상 embed 기본 포함
- 타임라인 기반 핵심 구간 정리
- video-native visual 우선 원칙 적용
- storyboard fallback 기반 스크린샷 후보 추출 흐름 지원
- companion-source visual은 보조/fallback으로만 사용
- 고해상도, 기사 폭에서 읽히는 이미지 우선
- 가독성 높은 문단 분리와 안전한 git 반영

포함 리소스:
- `references/youtube-embed-timeline-screenshots.md`
- `references/storyboard-screenshot-fallback.md`
- `references/companion-source-contextual-visuals.md`
- `references/video-visual-retrofit-audit.md`

### `gitblog-tipsupload`
GitHub 저장소, 앱, CLI, 유용한 라이브러리 링크를 `content/tips` 컬렉션용 한국어 tips 글로 정리하는 스킬이다.

핵심 기능:
- 기존 tips 중복 여부 확인 후 업데이트/신규 생성 판단
- 라이브러리·앱·CLI의 실제 사용 가치, 설치 경로, 권한/라이선스 주의점을 중심으로 정리
- tips 템플릿에 필요한 frontmatter, `platforms`, `highlights` 필드 검증
- GitHub repo 메타데이터, README, release, license, 공식 스크린샷 우선 조사
- 짧고 실용적인 큐레이션 글 작성과 안전한 git 반영

## 전체 스킬 목록

### 블로그 / 문서화

#### `gitblog-upload`
논문, 저장소, 모델 페이지, 기술 웹사이트 링크를 한국어 AI 블로그 글로 정리하고 블로그 저장소까지 반영한다.

#### `gitblog-mvupload`
YouTube 영상을 transcript·timeline·시각 자료까지 분석해 블로그 글로 발행한다.

#### `gitblog-tipsupload`
GitHub 저장소, 앱, CLI, 유용한 라이브러리를 `content/tips`용 실용 큐레이션 글로 정리하고 블로그 저장소까지 반영한다.

#### `paper-review`
AI 논문, 코드 저장소, 데이터셋 링크를 한국어 paper review 스타일 문서로 요약한다.

#### `weekly-report`
현재 저장소의 git history를 바탕으로 주간 보고서를 작성하고 관련 문서를 업데이트한다.

### 리서치 / 분석

#### `hf-research`
Hugging Face 모델을 조사해 모델카드 주장, 공식 근거, 논문 근거, 커뮤니티 반응, 추론을 분리한 내부 브리핑 형태로 정리한다.

#### `library-research-protocol`
외부 라이브러리, OSS, SDK, 데이터/모델 파이프라인 후보를 조사하고 capability manifest나 중복 구현 방지용 분석 문서를 만들 때 쓰는 스킬이다.

#### `paper2code`
arXiv 논문을 최소 구현 가능한 Python 코드로 바꾸는 오케스트레이션 스킬이다. 애매한 부분은 숨기지 않고 명시하는 쪽에 초점이 있다.

#### `autoresearch`
장시간 unattended improve-verify loop를 돌리면서 반복적인 조사, 개선, 디버깅, 검증을 자동화하는 장기 실행형 스킬이다.

### Git / 동기화 / 커밋 지원

#### `commit-ko`
현재 워킹트리의 실제 변경 파일만 기준으로 한국어 git commit message를 작성한다.

#### `blog-sync`
`aidt-blog` 저장소의 특정 커밋을 짝이 되는 `blog` 저장소로 미러링하고 결과를 검증한다.

#### `ocr-sync`
`pp-ocr` 저장소의 특정 커밋을 `ocr` 저장소로 미러링하고 결과를 검증한다.

### 프롬프트 / 스킬 관리

#### `prompt-master`
특정 AI 도구용 프롬프트를 새로 쓰거나, 개선하거나, 목적에 맞게 변형하는 프롬프트 엔지니어링 스킬이다.

#### `skill-creator`
새 스킬을 설계하거나 기존 스킬을 업데이트할 때 쓰는 제작 가이드 스킬이다.

#### `skill-installer`
큐레이션된 스킬 목록이나 GitHub 경로로부터 스킬을 설치하는 스킬이다.

## 디렉토리 구조

현재 저장소에 포함된 스킬 디렉토리:

- `autoresearch`
- `blog-sync`
- `commit-ko`
- `gitblog-mvupload`
- `gitblog-tipsupload`
- `gitblog-upload`
- `hf-research`
- `library-research-protocol`
- `ocr-sync`
- `paper-review`
- `paper2code`
- `prompt-master`
- `skill-creator`
- `skill-installer`
- `weekly-report`

## 운영 메모

- 스킬은 단일 `SKILL.md`만으로 끝나지 않고, 필요한 경우 reference/template/script를 같이 가져가야 재사용성이 유지된다.
- 블로그 계열 스킬은 특히 **고해상도 이미지**, **읽기 쉬운 문단 분리**, **표 활용**, **선택적 but 안전한 git workflow**를 기본 품질 기준으로 삼는다.
- 영상 기반 글은 source video 자체의 시각 증거를 우선하며, 외부 repo/docs 이미지는 보조 근거로 취급한다.

## Hermes 연동

이 저장소는 Hermes의 복사본이 아니라 Git으로 추적되는 원본으로 쓴다. Hermes에는 `~/.hermes/skills` 아래 symlink를 만들고, `~/.hermes/config.yaml`의 `skills.external_dirs`에도 이 저장소를 등록한다. 기존 Hermes 복사본은 Hermes 스캐너가 무시하는 `~/.hermes/skills/.archive/repo-link-backups/` 아래로 백업한다.

초기 연결:

```bash
uv run scripts/hermes_link_skills.py --dry-run
uv run scripts/hermes_link_skills.py
```

자동 커밋/푸시:

```bash
sh scripts/install_auto_push_launchd.sh
```

설치 후 launchd가 5분마다 `scripts/commit_and_push_if_changed.sh`를 실행한다. Hermes에서 symlink로 연결된 스킬을 수정하면 이 저장소의 실제 파일이 바뀌고, 변경분이 있으면 `chore(skills): sync Hermes skill updates` 커밋으로 `origin/main`에 push된다.

## 추천 사용 순서

- 링크 기반 글 작성: `gitblog-upload`
- YouTube 영상 기반 글 작성: `gitblog-mvupload`
- 유용한 앱/CLI/라이브러리 tips 작성: `gitblog-tipsupload`
- Hugging Face 모델 조사: `hf-research`
- 논문 구현: `paper2code`
- 주간 업무 보고: `weekly-report`
- 스킬 생성/수정: `skill-creator`
- 프롬프트 최적화: `prompt-master`
- 커밋 메시지 작성: `commit-ko`
