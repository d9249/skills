---
name: gitblog-mvupload
description: Use when the user provides a YouTube video URL and wants it turned into a Korean AI lab-style blog post in the blog repo, with transcript analysis, media selection, and safe git commit/push workflow.
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [blog, youtube, video, transcript, git, publishing]
    related_skills: [gitblog-upload, youtube-content]
argument-hint: "<YouTube-URL> [category] [series-number]"
---

# Gitblog MV Upload

## Overview

This skill is the video-first companion to `gitblog-upload`.

Use it when the input artifact is a YouTube video and the expected output is not a casual summary but a publication-ready Korean blog post saved into the user's blog repository, then committed with a safe git workflow.

The core difference from generic link summarization is that a video has four evidence layers that must be handled separately:
1. **Video metadata** — title, channel, publish timing, description, linked resources.
2. **Spoken content** — transcript, chapter flow, claims, demos, benchmarks, opinions.
3. **Timeline structure** — section boundaries, topic transitions, key moments, and timestamp anchors that let the reader jump back into the source.
4. **Visual evidence** — screenshots, diagrams, UI moments, slides, benchmark frames, workflow sequences.

For reusable patterns, see `references/youtube-embed-timeline-screenshots.md`, `references/storyboard-screenshot-fallback.md`, `references/companion-source-contextual-visuals.md`, and `references/video-visual-retrofit-audit.md`.

The final post should read like a polished AI lab report or technical editorial article, not like meeting notes or a transcript cleanup.

Primary output path:
- `/Users/mean/Documents/Github/d9249.github.io/content/blog`

## When to Use

Activate this skill when the user:
- sends a YouTube URL and wants a blog post
- says to turn a video into an article
- wants a Korean writeup of a technical talk, launch video, demo, keynote, tutorial, interview, benchmark walkthrough, or product announcement
- expects the result to be saved in the blog repo with commit/push

Do **not** use this skill for:
- plain one-paragraph video summaries
- downloading/editing the actual video file unless the task explicitly asks for that
- non-YouTube links when `gitblog-upload` already covers the source artifact directly

## Required Source Collection Workflow

Always start from the exact YouTube URL the user sent.

### 1. Identify the video cleanly
Extract and verify:
- canonical video ID
- video title
- channel name
- publish date if available
- description / show notes / outbound links
- whether official chapters exist

Do not trust a single metadata field blindly. When title, description, channel framing, or linked resources appear inconsistent, cross-check the actual session identity using multiple signals:
- YouTube oEmbed title / page title
- spoken self-introduction or host introduction in the transcript
- recurring artifact names mentioned early in the talk
- companion links that actually match the session topic

If the description links to a paper, GitHub repo, product page, docs site, or model card, treat those as **first-class companion sources** rather than optional extras.

If the video page metadata appears to belong to a different talk or was copied from another session, say so explicitly in the article and ground the writeup on the transcript and corroborating companion sources instead of pretending the mismatch does not exist.

### 2. Fetch transcript first
Use the `youtube-content` skill workflow and helper script to retrieve the transcript.

Before fetching, verify the prerequisites actually exist in the active runtime:
- `youtube-transcript-api`
- `yt-dlp`

Important environment pitfall: Hermes terminal sessions may run inside a Python environment that is different from the one used by `pip install --user`. If `python3 -m yt_dlp` fails with `No module named yt_dlp` right after installation, do not keep retrying the same form. Instead, use the actual installed binary path (for example `~/Library/Python/<python-version>/bin/yt-dlp`) or another confirmed executable from `command -v yt-dlp`.

Preferred sequence:
1. Run transcript fetch in plain text with timestamps.
2. If that fails because the dependency is missing, install it and retry immediately.
3. If that fails, retry without language restriction.
4. If no transcript exists, say so explicitly and continue with metadata + visible page evidence only.
5. If the transcript is long, chunk it and summarize per section before synthesizing the final post.

Never pretend to have verified spoken claims if the transcript was unavailable.

### 3. Recover the narrative structure
From chapters, transcript, and description, reconstruct:
- the main thesis of the video
- section/topic transitions
- what is shown vs what is merely stated
- which claims appear grounded by demo, benchmark, slide, or linked source
- which parts are interpretation, speculation, roadmap, or opinion

### 4. Build a timestamped working timeline
Create a compact internal timeline before drafting the article.

Minimum fields:
- start timestamp
- end timestamp when inferable
- segment label
- what is visually shown
- what is verbally claimed
- companion source to verify against, if any
- whether the segment deserves an embedded screenshot in the article

Prefer official YouTube chapters when available.
If chapters do not exist, infer boundaries from transcript topic shifts and visible demo/slide changes.

This timeline is not necessarily pasted verbatim into the article, but it should drive:
- the section order of the post
- any `## 타임라인으로 보는 핵심 구간` section
- screenshot selection
- timestamp mentions inside captions or prose

### 5. Inspect companion sources
If the video references official resources, inspect them as part of the evidence base:
- GitHub repo / docs / release notes
- paper / arXiv / project page
- product page / launch page / model card
- benchmark page / dataset page
- slide deck / speaker notes if publicly linked

Use the companion sources to verify exact names, metrics, release scope, packaging details, and terminology.

For workshop, tutorial, or explainer videos, also check whether a linked GitHub repo, docs page, or project site is the clearest companion artifact. In these cases, the companion source is often better than raw frame grabs for both factual grounding and high-resolution contextual visuals.

### 6. Gather visual evidence deliberately
For video-driven posts, visuals matter more than usual.

Prefer extracting or embedding visuals only when they materially help understanding, such as:
- title slide or framing slide
- architecture or workflow diagrams
- benchmark charts
- UI demo states
- before/after result frames
- qualitative examples
- code/demo pipeline screenshots

Avoid decorative thumbnails that add no information.

If stable official images already exist in linked companion sources, use them as supplements or fallbacks — not as an automatic replacement for video-native evidence.

Default rule: when the source is a YouTube video, the final article should usually contain at least one genuinely video-native visual (slide, demo frame, chart, UI moment, architecture frame, or workflow frame) if such a frame can be extracted at acceptable quality.

A particularly strong pattern for educational or workshop-style videos is to combine:
1. one or more video-native frames that show what the speaker actually presented on screen, and
2. optional companion-source visuals that add higher-resolution context such as repo structure, docs framing, benchmark tables, or setup instructions.

Use companion-source visuals as the primary images only when video-native candidates fail the usefulness bar — for example when extracted frames are blurry, redundant, visually empty, or materially less informative than the linked official artifact.

If storyboard- or video-derived screenshots are too blurry to read at article width, do not force them into the post just because they came from the source video. First try better extraction, better timestamps, or a higher-resolution source. Only after that should you switch to companion-source visuals, including official docs pages, repo pages, product pages, or other context-setting assets that better explain the artifact.

If the video itself is the best visual source, use selective screenshots representing distinct information, not five nearly identical frames.

### 7. Embed the source video and prepare screenshot candidates
Default behavior for blog posts made with this skill:
- embed the YouTube video in the article unless the user explicitly does not want embeds
- place the embed near the top of the article, usually after the intro or after `## 무엇을 다루는 영상인가`
- use the canonical embed URL form: `https://www.youtube.com/embed/<VIDEO_ID>`
- use HTML embed markup rather than a bare watch URL when the repo supports raw HTML in article bodies

Current repo grounding: the user's Gatsby blog renders article HTML via `dangerouslySetInnerHTML` in `src/templates/blog-post.js`, and `src/styles/global.css` already styles `.article-body iframe` to width 100%, so iframe-based YouTube embeds are a valid default in this repo.

For screenshots:
- choose 2-5 key moments when they add distinct explanatory value
- prefer moments that align with the working timeline
- record the timestamp for each screenshot you keep
- mention the timestamp in nearby prose or caption when it helps traceability
- prefer the highest-resolution available source for each image, not the fastest low-detail grab
- default to keeping at least one useful video-native frame in the final article when technically possible and article-legible
- reject frames that are readable only as thumbnails; if slide text, UI labels, charts, or qualitative outputs are not legible at article width, re-extract from a higher-resolution source or pick a different moment

Preferred extraction order:
1. confirm a working `yt-dlp` binary path
2. inspect available formats/storyboards and note the best reachable video or storyboard resolution before extracting anything
3. download the video locally at the highest practical quality when feasible
4. use `ffmpeg` with explicit timestamps to extract stills from that higher-quality local source
5. if direct download fails but `yt-dlp --dump-single-json` exposes storyboard formats (`sb0`/`sb1`/etc.), prefer the highest-resolution storyboard variant available and crop timestamp-nearest cells as fallback screenshots
6. visually inspect candidates and keep only distinct, legible, publication-grade frames
7. if the kept video-native frames are still not article-legible, fall back to higher-resolution companion-source visuals rather than publishing blurry screenshots

If direct video download or frame extraction fails, do not give up on video-native visuals immediately. Try the storyboard fallback first, then use companion-source images, and only then fall back to thumbnail/header usage. Do not block the article on perfect screenshot extraction.

## Minimum Grounded Facts to Extract

Before drafting, verify as many of these as available:
- canonical video title
- channel / speaker / organization
- core topic or product/research artifact
- what problem the video is trying to address
- what is actually demonstrated or explained
- what is merely claimed verbally
- the major timeline segments and their timestamp anchors
- any screenshot-worthy moments that materially clarify the post
- any linked official artifacts
- benchmark numbers, feature lists, architecture claims, or workflow steps that can be grounded
- limitations, caveats, release constraints, or missing pieces
- whether the best framing is tutorial, launch analysis, research walkthrough, product teardown, or ecosystem commentary

For interview/opinion videos, be careful not to overstate offhand verbal remarks as verified technical facts.

## Blog Repo Inspection Workflow

Before writing:
1. Confirm repo exists at `/Users/mean/Documents/Github/d9249.github.io`
2. Inspect existing categories under `content/blog/`
3. Search for an existing post on the same video/topic/channel/artifact
4. If a matching post exists, update it instead of creating a duplicate
5. Read at least 1-2 representative posts in the target category to match frontmatter and tone
6. If the task is a retrofit of older YouTube-derived posts rather than a brand-new post, audit all affected posts for whether companion-source visuals accidentally replaced video-native evidence; use `references/video-visual-retrofit-audit.md` as the repair workflow

Prefer updating an existing post when:
- the same video was already covered
- the video is really the narrative wrapper around an artifact already posted on the blog
- the new work is an expansion/refresh rather than a totally new topic

## Writing Strategy

Write in Korean and keep the tone analytical, polished, and publication-ready.

Paragraph readability is a first-class requirement, not a cosmetic afterthought:
- default to 1-3 sentences per paragraph unless a tighter grouping is clearly better
- split long explanations into multiple short paragraphs at idea transitions
- leave explicit blank lines between paragraphs in the saved markdown so the article is easy to read on desktop and mobile
- when a section mixes explanation, evidence, and interpretation, separate them into adjacent paragraphs instead of one dense block

The post should not read like:
- transcript bullets
- chapter dump
- "이 영상에서는..." repeated every paragraph
- AI-generated meeting notes

Instead, convert the material into a coherent article with editorial judgment.

### Default article shape

1. **Intro**
   - explain why this video matters now
   - frame the technical or market context
   - identify whether the video is revealing a product, explaining a method, or synthesizing a trend

2. `## 무엇을 다루는 영상인가`
   - summarize the subject, speaker, and scope
   - clarify whether it is a launch video, tutorial, keynote, demo, panel, or review
   - embed the YouTube video here by default when it helps the article package

3. `## 핵심 아이디어 / 구조 / 시연 흐름`
   - reconstruct the video's main mechanism or narrative arc
   - separate visible demo flow from conceptual explanation

4. Optional but strongly recommended: `## 타임라인으로 보는 핵심 구간`
   - condense the working timeline into reader-facing checkpoints
   - use a table or bullet structure when that is clearer
   - include timestamps only when they help the reader jump back to the source

5. `## 영상과 연결 자료에서 확인되는 점`
   - verified claims, numbers, releases, feature scope, benchmark evidence, docs, repos, model cards
   - clearly separate observed facts from interpretation

6. `## 실무 관점에서의 해석`
   - why this matters
   - where the real value is
   - what remains unclear or unproven
   - what teams could learn or adopt from it

7. Optional visual sections
   - include multiple images when each one explains a different part of the story
   - use captions or nearby text to explain why each visual matters
   - mix official images and video screenshots only when each serves a distinct purpose

8. Optional structured block
   - use tables when the video includes comparisons, timelines, workflows, or benchmark axes

9. Optional closing paragraph
   - adoption or industry implication takeaway

Paragraph formatting defaults:
- prefer 1-3 sentence paragraphs for analytical prose
- break paragraphs when moving from setup, to evidence, to interpretation
- preserve explicit blank lines between paragraph blocks in the saved markdown
- if a section feels dense on a phone-sized screen, split it before finalizing

## Video-Specific Interpretation Rules

### Distinguish these carefully
- **What is shown on screen** vs **what is only said**
- **What the linked official artifact proves** vs **what the host summarizes**
- **Product marketing framing** vs **technical substance**
- **Current release scope** vs **future roadmap**

### For technical demos
Identify:
- demo inputs
- workflow steps
- output quality signals
- hidden assumptions or setup complexity
- signs of cherry-picking vs robust evidence

### For research explainers
Identify:
- whether the speaker is summarizing a paper or presenting original work
- which claims come from the paper vs the speaker's framing
- whether visuals reflect actual experiment results or conceptual illustrations

### For launch/keynote/product videos
Identify:
- what is really shipping now
- what needs waitlist/API access/private beta
- what appears to be roadmap language
- whether pricing, deployment, latency, model scope, or system boundaries are actually stated anywhere official

## Images and Media Guidelines

The user prefers materially useful images, not a fixed single image.

Use visuals when they improve understanding:
- workflow screenshots
- architecture slides
- benchmark charts
- qualitative demo frames
- UI transitions
- result examples
- embedded video player near the top of the post for direct source access

Do not use images that are:
- purely decorative
- redundant with another image
- too blurry or too low-resolution to explain anything at article size
- likely misleading without context
- only marginally related when a sharper companion-source visual could explain the same point better

When both low- and high-resolution versions are available, default to the high-resolution source unless it introduces visible compression artifacts or incorrect cropping.

If a useful official image exists in companion sources, prefer it.
If not, use carefully chosen video screenshots.
If you create exploratory screenshot candidates that are not used in the final post, delete them before staging so the commit contains only intentional media assets.

If the repo supports image embedding conventions already, follow them.
If the blog repo does not support special thumbnail frontmatter, do not invent it casually.

## Category Guidance

Infer the category from the topic actually covered, not from the fact that the source is a video.

Examples:
- model launch breakdown → `foundation-models`
- benchmark walkthrough → `evaluation-benchmarks`
- agent framework demo → `agent-systems`
- training recipe talk → `model-training`
- product/infrastructure deep dive → the closest existing relevant category

Do not create a category like `videos` unless the live repo already uses source-type categories.

## Frontmatter Pattern

Match the live repo exactly when possible. Default shape:

```yaml
---
title: "<Korean title>"
date: "YYYY-MM-DDTHH:MM:SS"
description: "<one-sentence thesis>"
author: "Sangmin Lee"
category: "<category>"
tags:
  - YouTube
  - <topic tag>
  - <artifact tag>
draft: false
---
```

Tags should describe the topic, not just the medium.
`YouTube` may be included when it helps context, but the post should still be primarily about the subject matter.

## Slug Rules

- Use short kebab-case ASCII slugs
- Prefer the artifact/topic framing over the raw YouTube title when the raw title is verbose
- Avoid meaningless slugs like `youtube-video-summary`
- If the video centers on a named product/model/repo, anchor the slug on that artifact

## Safe Git Workflow

1. Run `git status --short --branch` in `/Users/mean/Documents/Github/d9249.github.io`
2. Determine whether this is an add or update
3. Write only the intended post and any intentionally added media assets
4. Inspect the diff for the touched files
5. Stage only those files
6. Commit with a concise message
7. Before pushing, verify that `origin/<branch>..HEAD` contains only the intended blog commit
8. Push only when that scope is safe

Commit message rules:
- new post: `blog: add <slug> post`
- updated post: `blog: update <slug> post`
- if a more specific artifact-centered message is clearly better, use `blog: add post on <artifact-name>`

If unrelated local commits are already ahead of origin, do not auto-push them. Report the situation clearly.

## Quality Bar Before Finishing

Verify all of the following:
- transcript availability and limitations are stated accurately
- artifact/video identity is correct
- the post reflects both spoken content and linked official evidence when available
- the article is saved under the intended blog path
- frontmatter matches repo conventions
- synthesis is stronger than a timestamped summary
- claims are grounded in transcript, metadata, screenshots, or linked sources
- image choices are actually informative
- tables render correctly if used
- only intended files are staged and committed
- push status is confirmed or exact failure is reported

## Common Pitfalls

1. **Treating the transcript as the whole artifact.**
   A good video post also uses metadata, visuals, and linked sources.

2. **Confusing spoken claims with verified evidence.**
   A presenter can claim benchmark wins without showing or linking enough proof.

3. **Using too many near-duplicate screenshots.**
   Each image should add a distinct explanatory function.

4. **Writing a chapter recap instead of an article.**
   The final output should synthesize, not merely replay the timeline.

5. **Classifying by source type instead of topic.**
   The category should reflect the subject matter, not just that it came from YouTube.

6. **Overstating roadmap demos as shipped features.**
   Launch videos often blend current product and future direction.

7. **Getting stuck on tool-path issues after installing dependencies.**
   `pip install --user` may succeed while the active `python3 -m ...` path still cannot import the package. Confirm the executable path and switch to the installed binary instead of repeating the same failing command.

8. **Ignoring linked official resources.**
   Many of the most important grounding details live outside the video page itself.

9. **Trusting mismatched page metadata without transcript cross-checking.**
   Some uploaded videos carry copied descriptions or stale session text from a different talk. If title, description, and spoken intro do not line up, verify the real session identity from the transcript and say the mismatch out loud in the article.

10. **Treating YouTube thumbnail art as a technical figure.**
   Thumbnails are often useful only as topic-signaling cover art; prefer official charts, dataset overviews, architecture figures, benchmark visuals, or real screenshot moments when explaining substance.

10. **Embedding the wrong URL form.**
   A watch URL is not the same as an embeddable iframe source. Use `youtube.com/embed/<VIDEO_ID>` and keep the embed responsive.

11. **Selecting screenshots without a timeline rationale.**
   Screenshots should correspond to distinct segments or claims, not random visually convenient frames.

12. **Assuming video download failure means no video-native screenshots are available.**
   `yt-dlp` can still expose storyboard grids even when MP4 download fails with HTTP 403. Check storyboard formats in the metadata dump before abandoning video-derived screenshots.

13. **Publishing blurry storyboard crops when better companion-source visuals exist.**
   If frame grabs are not readable at article width, use sharper official docs, repo, or product-page visuals instead of forcing low-value video screenshots into the post.

14. **Leaving unused screenshot candidates in the repo.**
   Video-post workflows often generate exploratory frame crops. Remove discarded candidates before staging so the commit contains only the final chosen media assets.

## Verification Checklist

- [ ] YouTube URL and video identity verified
- [ ] If title/description/transcript framing disagree, the mismatch was resolved explicitly before drafting
- [ ] Transcript fetched or transcript absence explicitly documented
- [ ] Description/chapters/outbound links inspected
- [ ] Working timeline created from chapters or inferred transcript sections
- [ ] Companion sources checked when present
- [ ] YouTube embed added unless intentionally skipped with a reason
- [ ] Best visuals selected intentionally
- [ ] Image assets come from the highest practical resolution source available
- [ ] Key screenshots chosen with timestamp rationale when video frames are used
- [ ] Screenshot text/UI/chart details remain legible at the intended article display width
- [ ] At least one video-native visual is kept when technically possible and substantively useful
- [ ] Companion-source visuals replace video-native screenshots only when the video-native options are not article-legible or add less explanatory value
- [ ] Exploratory screenshot candidates not used in the article were removed before staging
- [ ] Existing blog posts searched before creating a new one
- [ ] Category chosen from live repo structure
- [ ] Frontmatter and body match repo style
- [ ] Paragraph blocks are broken up for readability with explicit blank-line spacing in markdown
- [ ] Commit scope limited to intended files
- [ ] Push is safe or the blocking reason is clearly reported
