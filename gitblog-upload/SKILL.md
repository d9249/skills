---
name: gitblog-upload
description: Turn a paper, GitHub repo, dataset, model page, or product/site URL into a unified Korean AI lab report-style blog post, save it under the user's blog repo, then stage/commit/push the post.
triggers:
  - blog post
  - 블로그 글
  - 링크 정리
  - paper review
  - 논문 리뷰
  - github.com
  - arxiv
  - openreview
  - huggingface.co
  - model page
  - website
  - 사이트
  - repo
  - dataset
argument-hint: "<URL> [category] [series-number]"
---

# Gitblog Upload

## Purpose

Convert one user-provided artifact URL into a polished Korean blog post for the user's site and publish it with a safe git workflow.

Supported inputs:
- Paper URLs: arXiv, OpenReview, conference page, PDF
- Code URLs: GitHub repositories, project pages, docs sites
- Gist / idea-doc URLs: GitHub Gists, manifesto-style markdown idea files, prompt/spec documents
- Model or dataset URLs: Hugging Face model/dataset pages, benchmark pages
- Product/site URLs: model launch pages, research lab writeups, official docs, company product pages
- Independent technical report / synthesis pages: personal research blogs, lab notes, educational AI reports that summarize primary papers or techniques

Primary output path:
- `/Users/mean/Documents/Github/d9249.github.io/content/blog`

This skill is specifically for the user's unified AI lab report/blog workflow, not generic note-taking.

## When to Activate

Use this skill when the user sends a link and wants you to:
- summarize it into a Korean post
- turn it into a blog article
- save it in the blog repo
- write a commit message
- commit and push

Also use it when the user sends only a GitHub repo or website but expects the same polished style previously used for paper reviews.

## Required End-to-End Workflow

1. Identify artifact type
   - Paper
   - Repository / codebase
   - Dataset / benchmark
   - Model page / product page / technical website

2. Gather primary sources first
   - Start from the exact URL the user sent.
   - Prefer official pages, author-maintained repos, linked docs, paper abstracts/PDFs, dataset cards, release notes, and project pages.
   - When the starting URL is an official project/launch page that exposes a bundle like `Paper`, `Model`, `Code`, and `Demo`, treat that bundle as the primary source set rather than relying on the landing page alone. Cross-check architecture/method claims against the paper, packaging/deployment claims against the model or repo, and product-surface claims against the live page/demo.
   - For model launch pages in particular, explicitly pair the marketing/launch page with the linked technical report and the distribution surface (usually Hugging Face). Use the launch page for positioning and curated visuals, the report for architectural/training claims, and the model card/API for packaging facts like active vs total parameters, context length, shard layout, downloads/likes, and deployment commands.
   - If the launch page is built in a JS-heavy site builder (for example Framer) and browser DOM text extraction is sparse or empty, fetch the raw HTML and recover the narrative by parsing the ordered `h*`/`p`/`img` blocks directly. This is often the fastest way to recover official section prose and stable figure URLs without relying on brittle rendered DOM selectors.
   - For GitHub Gists, fetch both the rendered gist page and the raw gist markdown/text. The raw gist is usually the cleanest canonical source for quoting structure, headings, and exact wording.
   - If the gist is a fork, preserve that provenance and distinguish between the current fork author's additions and the upstream original idea.
   - If the starting artifact officially links to related paper/code/dataset pages, follow those links.
   - For official sites protected by Cloudflare, heavy JavaScript, or anti-bot interstitials, try a text mirror such as `https://r.jina.ai/http://<original-host-and-path>` to recover the article text before falling back to secondary sources.
  - If the text mirror is blocked or returns 403 but the live site still renders in the browser, inspect the live page directly and also fetch the raw HTML. Product pages and official blogs often expose high-value structured metadata even when plain-text mirroring fails: `og:title`, `og:description`, `og:image`, canonical URL, article publish date, and `application/ld+json` blocks such as `SoftwareApplication`, `Organization`, or `Article`. Use those fields as grounded evidence for product positioning, feature lists, authorship, and official visuals.
   - When an official docs site is split across a marketing domain and a docs domain, do not assume the marketing-site paths are canonical. First look for an index like `llms.txt` (for example `https://docs.<host>/llms.txt`) or other docs sitemap material, then follow those canonical docs URLs. This avoids wasting time on mirrored 404s from guessed marketing-site paths.
   - For arXiv papers, when the abstract is not enough, also inspect the `/html/` rendering in addition to `/abs` or PDF; the HTML version often exposes figure captions and direct image asset URLs that are easier to embed accurately in the blog post.
- If the paper has an official project page, treat it as a first-class companion source rather than an optional extra. Use the arXiv HTML for method structure, equations, and section flow; use the project page for cleaner benchmark tables, rollout summaries, and stable official visuals.
- For arXiv papers, explicitly check the HTML rendering itself for companion-source links such as a top-of-page `Code:` link. The `/html/` page can expose an official GitHub repo or project page even when the `/abs/` page or abstract snippet did not make that companion source obvious.
- If the paper-linked repo exists, inspect it as a first-class companion source even for paper-centric posts: README benchmark tables, example/config files, asset filenames, and repository metadata can corroborate release maturity and sometimes provide cleaner numbers or more stable official visuals than the paper HTML alone.
- For arXiv training/architecture papers with a freshly created companion repo, explicitly capture repo-age and packaging signals before calling the release mature: creation/push dates, stars/forks, whether `/releases/latest` 404s, whether `/tags` is empty, and whether the README already contains a usable reproduction guide. These details often matter as much as the paper when judging how real the release is.
- If the repo is a derivative framework fork rather than a clean standalone library (for example Megatron-based research code), inspect README + `LICENSE`/`NOTICE` together and look for packaging quirks such as a distinct pip package name but inherited import path. Report that shape explicitly; it materially changes how readers should interpret reviewability, install friction, and release maturity.
- If the paper-linked repo is really a trace-backed research harness rather than a plain code drop, also inspect architecture docs and release-artifact docs (for example `docs/architecture.md`, `docs/task_adapter.md`, `release_artifacts/README.md`). These often ground what the system actually automates, which run records are preserved, and whether the release is better described as an auditable research artifact bundle versus a polished framework. See `references/trace-backed-research-repos.md`.
- If a paper does **not** appear to have an official project page, code repo, or model page after explicit checking, record that absence as a grounded release-maturity signal instead of silently implying a public implementation exists. This is especially important for training-dynamics / empirical-study papers.

- When no companion project/code page exists, arXiv HTML itself can still be a strong official visual source. Check for overview assets such as `/figures/main.png` and the `xNN.png` figure files, then use the most explanatory figures (overview, main result, ablation, generalization) rather than defaulting to text-only coverage.
- If mirrored arXiv HTML text is enough for narrative sections but not for structured numeric results, inspect the live HTML page in the browser and extract `table` contents directly. arXiv HTML tables can preserve benchmark values more reliably than mirrored markdown when you need to build a grounded comparison table in the blog post.
- If browser DOM extraction misses arXiv tables because they are nested inside LaTeXML `figure`/`ltx_table` markup, fall back to fetching the raw `/html/` source and parse the `<figure id="S*.T*"> ... </figure>` blocks directly with a short Python/regex pass. This is often the fastest way to recover benchmark rows and captions without needing extra parsing libraries.
- When extracting benchmark evidence from arXiv HTML, do not stop at the first visible table dump. Filter rows for the focal model and its most relevant baselines (for example the immediate predecessor or ablation variants) so the post reports the comparison pattern, not just a wall of metrics.

  - For paper-linked repos, inspect README release notes / TODO sections for weight availability and packaging caveats. Distinguish clearly between code release, partial checkpoint plans, and full production weight availability; do not let the existence of a public repo imply that the headline paper results are immediately reproducible.
  - When a paper/project ships multiple official Hugging Face checkpoints tied to specific benchmarks, tasks, or subcomponents, do not flatten them into a single generic "model release" claim. Note the packaging shape explicitly — for example benchmark-specific checkpoints, auxiliary decoder checkpoints, or partial component releases — because this materially affects reproducibility and deployment interpretation.

- If the source bundle spans arXiv + GitHub + Hugging Face, cross-check release maturity and licensing across all three surfaces. It is possible for the GitHub repo API to show `license: null`, the repo files to omit a checked-in `LICENSE`, and the Hugging Face card to advertise a license tag such as MIT. Treat that mismatch as reportable evidence rather than silently normalizing it.
- If the paper or repo is specifically about agent skills and links to a marketplace distribution page such as ClawHub, inspect that page as a first-class companion source. Marketplace pages can expose grounded deployment metadata the paper abstract and GitHub API do not: published skill version, install command, security-review banners, scan links, marketplace license string, and positioning copy. Use those signals when writing about release maturity, operational safety, or packaging.

   - For GitHub visuals, if inline `img` discovery is weak or noisy, check `meta[property="og:image"]` as a reliable fallback hero image source.
  - For Hugging Face community model pages, do not stop at the rendered model card. Also inspect the HF API model metadata and list repository siblings/files, then fetch any supporting raw artifacts that materially ground claims, such as `SERVING_NOTES.md`, benchmark JSON files, response samples, chat templates, or release notes.
  - When a Hugging Face model repo ships image assets, do not assume every asset is article-worthy just because it is official. Some repos include generic corporate slides, workflow placeholders, or unrelated sample images. Visually inspect candidate assets and embed only those that materially explain the model, roadmap, workflow, benchmarks, or outputs.
  - For community/forum posts that summarize a project, treat them as secondary context and follow through to the official repo/project page before making stronger technical claims.
  - When the starting point is a secondary/community writeup, use it mainly to understand the narrative angle and discover outbound links, but reconstruct the technical claims from the official repo, paper, docs, or project page before drafting the post.
  - For websites that distribute reusable prompt/design/config assets rather than a single model or app (for example DESIGN.md catalog / marketplace sites), inspect three layers separately: the landing-page thesis, one concrete item/detail page, and any public backing repository. These sites often expose install commands, usage counters, curated-vs-official disclaimers, and structured-data `sameAs` links that materially change the article angle.
  - For catalog-style sites, do not trust headline counts alone. Compare homepage or README badge counts against the actual public repository tree/API enumeration and report meaningful mismatches as evidence that the catalog is actively changing.
  - When a catalog item ships a raw reusable asset file (for example a representative `DESIGN.md`), fetch one sample raw file and inspect its granularity before describing the product. This distinguishes shallow inspiration galleries from real agent-readable specification packs.
  - If the community post points to a technical report PDF plus official distribution pages (for example a Hugging Face collection/model cards, ModelScope collection, or demo Space), prioritize that bundle as the primary source set: use the forum post for convenient structure, then verify headline claims against the PDF first page/abstract and the official model cards or collection pages.
  - If a Hugging Face collection or Space API path is unavailable, gated, or returns legal/auth errors, fall back to public HTML metadata (`og:title`, `og:image`) and any embedded JSON or raw model-card files you can fetch directly. Do not drop the official source just because the nicer API route is blocked.
  - When Hugging Face card metadata and the repository files disagree on licensing or packaging details, report the discrepancy explicitly. In particular, distinguish `cardData` / tag-level license strings from the actual `LICENSE` file contents instead of silently normalizing them.
  - If the community post rehosts images originally coming from the official repo/paper/docs, prefer the official image asset URL when it is easily recoverable and stable enough to embed.
  - Do not invent missing links or unsupported claims.

3. Extract the minimum grounded facts
   - Canonical title / artifact name
   - What problem it addresses
   - What it actually ships or proposes
   - If it is an idea/spec/gist rather than a runnable product, explicitly classify it that way and avoid overstating implementation maturity
   - Core mechanism / architecture / workflow / benchmark design
   - Evidence: metrics, examples, release scope, limitations, license caveats, or deployment constraints
   - Why it matters in practice
   - Whether there is a strong official visual worth embedding
   - Whether there is comparison/workflow/matrix information that should become a table
   - Whether prose-only sections should become a text-derived visual spec; if so, read `references/consulting-visual-spec.md` before creating the image
   - For repositories or docs pages that expose enumerated capability lists, compare the current official list against any existing local post before concluding that no update is needed.
   - When an existing local post already covers the same GitHub repository or artifact, treat the task as an update pass: refresh volatile facts from live official sources before deciding whether the old post is still current. In practice this means re-checking stars/forks, tags/releases, default branch, recent commit/version signals, and any packaging or installation notes that may have drifted.
   - When you update an existing post, audit both narrative paragraphs and any embedded tables so the same volatile facts are not left inconsistent in different sections.
   - When a fast-moving repository shows conflicting counts or summaries across README badges, hero copy, deeper tables, changelog text, or live UI, do not silently pick one number and present it as settled fact. Prefer the most contextual/structured source, and if the discrepancy is itself informative, mention that the catalog is changing quickly and the counts differ by section or update timing.
   - For GitHub repositories, compare API metadata against the actual repository files when licensing or packaging matters. If the GitHub API license field conflicts with the checked-in `LICENSE` file or README claims, report the discrepancy explicitly instead of normalizing it away.

4. Inspect the user's blog repo before writing
   - Confirm repo exists at `/Users/mean/Documents/Github/d9249.github.io`
   - Inspect existing blog posts under `content/blog/`
   - Do not assume previously seen category names or legacy file paths are still valid; search the live `content/blog/` tree first because categories may be reorganized over time.
   - Read at least 1-2 representative posts in the most relevant target category before drafting so the frontmatter, heading structure, paragraph density, and table/image usage match the live site style
   - Reuse the existing frontmatter pattern and writing tone
   - For the `date` frontmatter, include time as well as the calendar date. Prefer an ISO-like local timestamp such as `YYYY-MM-DDTHH:MM:SS`, unless the live repo clearly uses a different datetime convention.
   - Infer a fitting category from existing categories when possible; if none fit, create a new category directory and keep frontmatter `category` equal to the directory name
- For papers centered on training recipes, optimization dynamics, RL behavior, scaling laws, or empirical studies of how models learn — even when the task setting is agentic — prefer `model-training` over `agent-systems` when the main contribution is about training behavior rather than a deployed orchestration stack.
- Conversely, if the artifact's real center of gravity is the agent orchestration itself — specialist-role decomposition, supervisor loops, lineage sharing, evaluator-owned feedback, MCP/tool harnesses, or released experiment traces — prefer `agent-systems` even when the benchmark domain happens to be training-recipe optimization.
- For open-weight/base model launch posts that are primarily about a foundation model release rather than training technique or a narrow application, prefer `foundation-models` when that category exists in the live repo.
- For segmentation, multimodal perception, or vision-heavy model releases that are presented as general-purpose model/system launches rather than narrow training-method papers, prefer `foundation-models` over inventing a new vision-specific category unless the live repo already has a better established bucket.
- For papers whose main contribution is a new benchmark, evaluation surface, or measurement protocol — even if they also introduce a model trained on that benchmark — prefer `evaluation-benchmarks` when the article's center of gravity is the benchmark design, task construction, leaderboard evidence, or evaluation methodology rather than the model family alone.
- For tabular / structured-data papers that pair a benchmark with a specialized embedding model, decide category by asking which artifact would still matter if the model changed next month. If the durable contribution is the benchmark and its evaluation protocol, file under `evaluation-benchmarks`; if the durable contribution is the representation/model architecture itself, consider `foundation-models` or another existing model-centric bucket.

5. Draft the post in unified blog format
   - Write in Korean
   - Public-facing prose, captions, diagrams, charts, thumbnails, SVG labels, and alt text must be Korean by default. Keep English only for proper nouns, model names, library names, commands, URLs, and source identifiers that should not be translated.
   - Keep the tone analytical and polished, like an internal AI lab report adapted into a public blog post
   - Do not use emoji-section social-post formatting unless the user explicitly asks for that style
   - Prefer short paragraphs with clear section headings over giant bullet dumps

6. Save the post
   - Before creating a new file, search the blog repo for an existing post about the same artifact/topic using title keywords, slug candidates, repo/model name, and canonical source URL if available.
   - If a matching post already exists, update that file instead of creating a duplicate. Treat the task as an update workflow and use the commit message form `blog: update <slug> post`.
   - Path format for new posts: `/Users/mean/Documents/Github/d9249.github.io/content/blog/<category>/<slug>.md`
   - Use kebab-case ASCII slug unless the repo clearly uses another convention
   - Match existing frontmatter fields exactly when possible

7. Optional text-derived visual workflow
   - Use this when the article has an important workflow, architecture, metric delta, comparison, issue tree, risk/maturity matrix, or executive takeaway that would be clearer as a figure.
   - Read `references/consulting-visual-spec.md` and write a compact visual spec before drawing or generating the asset.
   - Prefer deterministic SVG/HTML/table renderers for charts, architecture, process, and benchmark visuals. Use generative image models mainly for abstract editorial covers.
   - For Korean blog posts, all visible labels in the visual must be Korean unless the label is an official product/model/library/source name.
   - Before wiring any generated visual into the post, render the final asset at its intended dimensions and visually inspect the rendered image. Do not accept images with clipped text, overflowing labels, overlapped components, cramped chips, or text that extends outside its intended panel.
   - Keep diagram labels short, manually wrap long Korean copy into separate lines, and size boxes around the longest rendered label rather than assuming the text will fit.
   - Arrows and connectors must be semantic, not decorative. Use an arrow only when the relationship has a clear direction in the article/spec, and verify that the rendered arrow starts and ends at sensible components without pointing into labels or empty space. If the relationship is only grouping, dependency, or "these parts share this output," prefer numbering, section dividers, or a shared result band instead of arrows.
   - Do not reuse the same card-grid layout as the default answer for every visual. Choose a layout grammar that matches the content: stack/layer map for operating layers, before-after board for deltas, matrix for tradeoffs, timeline for releases, issue tree for root causes, and dashboard only for genuinely multi-metric scans. If a post includes multiple visuals, they should use distinct layout grammars unless the article explicitly needs a repeated series.
   - Choose the visual type by communication intent, and record the reason when nearby types could also fit.
   - Keep public labels neutral, such as `metric dashboard`, `architecture map`, or `executive diagram`; do not expose brand-specific inspiration names in the article.
   - Save local assets under `static/images/blog/<slug>-<short-name>.<ext>` and wire them into the article only when the asset materially improves comprehension.

8. Optional thumbnail workflow
   - Prefer a generative thumbnail when it will improve consistency and clickability.
   - Default thumbnail style: clean technical editorial cover for an AI lab/report blog, not flashy YouTube clickbait.
   - Build the thumbnail concept from the actual article angle: artifact name, core mechanism, and one strong visual metaphor.
   - When available, use official source visuals as reference material or compositional inspiration, but do not simply reuse them if a cleaner generated cover is better.
   - Save thumbnail assets inside the blog repo using a stable path convention such as `static/images/blog/<slug>-thumb.png` unless the repo clearly uses another pattern.
   - If the site supports a frontmatter image field, wire the saved thumbnail into frontmatter (for example `thumbnail`, `cover`, or another existing field already used by the repo).
   - If the repo does not yet support per-post thumbnails, inspect the template/components first before introducing new frontmatter fields.
- In the user's current `d9249.github.io` Gatsby blog, verify whether per-post thumbnail wiring actually exists before generating assets. At the time of this session, `src/templates/blog-post.js` renders a generic `hero-image` block from the post description and `src/components/PostCard.js` does not read thumbnail-related frontmatter. In that state, default to skipping thumbnail generation unless the user also wants the site template updated to consume per-post thumbnail metadata.
   - For generation, prefer image models that are strong at editorial/graphic covers, typography-free compositions, or diagram-like technical visuals. If text rendering inside the image would be unreliable, keep the image text-free and let the page title provide the text.
- If external image-generation credentials are unavailable (for example no `FAL_KEY`/`LEGNEXT_KEY`), fall back to a local generated cover concept: create a clean SVG-based editorial thumbnail from the article's core pipeline/mechanism, then render/export it to PNG inside the repo.
- Prefer rendering the SVG through a browser/screenshot path for final export verification, because direct OS thumbnail/export tools can distort the intended aspect ratio or add unexpected padding. Verify the final PNG dimensions before using it.
- For this fallback path, prefer simple high-contrast shapes, pipeline arrows, badges, and short Korean labels derived from the post's central mechanism rather than long prose blocks.
- Keep the fallback composition minimal. Avoid decorative side bars or extra chart glyphs unless they clearly improve readability; they can easily make the layout feel unbalanced at thumbnail size.

9. Git workflow
   - Check `git status --short --branch` first
   - Do not disturb unrelated existing changes
   - Stage only the newly created or intentionally edited blog file and any intentionally added thumbnail asset or template change
   - Write a concise commit message
   - Commit and push the current branch when safe
   - If push fails because of auth/divergence, report the exact failure

## Unified Blog Output Format

Use the existing repo style: YAML frontmatter + Korean prose article.

### Frontmatter

Follow the repo's established pattern:

```yaml
---
title: "<Korean title>"
date: "YYYY-MM-DDTHH:MM:SS"
description: "<one-sentence summary>"
author: "Sangmin Lee"
category: "<category>"
tags:
  - Tag1
  - Tag2
  - Tag3
draft: false
---
```

### Body Structure

Use this article shape by default:

For GitHub repositories in particular, do not rely only on the rendered web page README. GitHub's browser DOM may omit or truncate README text in automated browsing contexts, so prefer the GitHub REST API for grounded extraction when possible: `/repos/<owner>/<repo>`, `/readme`, `/releases/latest`, and targeted `/contents/<path>` requests for docs/changelog files.

If `/releases/latest` returns 404, do not assume the project has no versioning signal. Also check `/tags`, recent commit messages, and any manifest files that expose version metadata.

For Claude Code / plugin-style repositories, do not stop at the top-level README. Also inspect plugin/package manifests such as `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, package metadata, or other distribution descriptors. These often contain grounded details the README glosses over: exact version, license string, category, keywords, author/distribution identity, and how the project wants to be positioned in a marketplace.

When the repository is really a packaged agent runtime or plugin distribution rather than a normal source repo, also inspect sibling host-specific packaging surfaces (for example `codex/<name>/.codex-plugin/*`, alternate `.mcp.json` files, standalone helpers, or marketplace descriptors under nested directories). Recent releases may add a second host integration there before the README fully explains it.

For plugin/runtime repos that market a hosted product alongside the GitHub repo, pair the repository evidence with the official site. Compare claims across README, manifests, release notes, and the product site for:
- install vs actual login/account requirements
- telemetry or analytics hooks exposed in config/env files
- licensing posture (`license: null`, checked-in `LICENSE`, README wording, Terms-of-Service references)
- whether the repo is primarily source-first or a prebuilt distribution bundle

If the repo ships very large prebuilt runtime artifacts (for example multi-megabyte `servers/*.js`, bundled `node_modules`, or standalone helper binaries/scripts), call that out explicitly in the post's operational interpretation. It is a meaningful signal about reviewability, packaging philosophy, and whether the project behaves more like a distributable product bundle than a traditional OSS library.

See also `references/plugin-runtime-repos.md` for a compact evidence checklist specific to plugin/runtime GitHub repos, and `references/design-md-catalog-sites.md` for design-asset catalog / marketplace sites.

If the repository ships translated READMEs, prefer the language that best matches the target article language for wording checks, but still cross-check technical claims against the canonical top-level README and manifests. Translations are useful for phrasing and section coverage, while the canonical README/manifests remain the source of truth for exact commands and current packaging details.

Do not stop at the README when the repo is fast-moving or methodology-heavy. Also check one or more of:
- latest GitHub release notes
- tags when Releases are absent
- changelog / release notes files
- docs subdirectories that explain architecture or harness-specific behavior
- plugin/package manifest files when the repo is distributed through an agent/plugin ecosystem

For monorepos or product repos with multiple top-level packages/apps, do not assume the root README and root package metadata tell the whole story. Enumerate the top-level tree and inspect the relevant subproject manifests and READMEs as well — for example Python package `pyproject.toml`, backend/service `pyproject.toml`, frontend `package.json`, or package-local `README.md`. Use those files to verify packaging boundaries, deployment surfaces, and version signals. This matters when the root README is high-level, partially stale, or blends multiple components into one marketing narrative.

When the repo markets an official OSS product page or docs portal alongside GitHub, treat that site as a first-class companion source rather than a marketing afterthought. Pair:
- root README for thesis and current positioning,
- subproject/package READMEs for install/runtime reality,
- docs overview/concepts pages for architecture and workflow framing,
- release manifests / package versions for packaging boundaries,
- official OSS product page for curated screenshots and product-surface language.
This combination is especially important for semantic-layer / GenBI / agent-data-infrastructure products where the GitHub repo, docs site, and OSS landing page each expose different parts of the story.

If the repo README or changelog announces a consolidation, rebrand, or migration of older repos/legacy branches, capture that explicitly as a project-direction signal. These repo-shape changes often explain whether the artifact is best interpreted as a product app, a core engine platform, or a newly unified monorepo.

Use these to distinguish the repo's stable core idea from very recent implementation changes, and to ground any claims about project direction, supported environments, or operational philosophy.

If you expect docs like `ARCHITECTURE.md` or `CHANGELOG.md` but direct raw fetches 404, do not conclude the repo lacks deeper documentation. Enumerate `/contents` first and follow the actual tree; many repos move architecture notes under translated READMEs, nested package folders, or docs subdirectories that are not guessable from the root README alone.

Use these to distinguish the repo's stable core idea from very recent implementation changes, and to ground any claims about project direction, supported environments, or operational philosophy.

1. Intro
   - 2-3 paragraphs
   - Explain what the artifact is and why it matters now
   - Frame the current industry or research bottleneck

2. `## 무엇을 해결하려는가`
   - Clarify the problem, market/research context, or operational pain point

3. `## 핵심 아이디어 / 구조 / 동작 방식`
   - For papers: method, mechanism, training/eval design
   - For repos: architecture, pipeline, what is implemented vs promised
   - For datasets: construction, schema, evaluation use case, limitations
   - For websites/model pages: product surface, system design clues, constraints, positioning

4. `## 공개된 근거에서 확인되는 점`
   - Verified metrics, ablations, examples, released components, benchmark claims, pricing/latency/coverage statements, or usage caveats
   - Clearly separate observed facts from your interpretation

5. `## 실무 관점에서의 해석`
   - Your synthesis: why this matters, what is differentiated, what risks or limits remain, what team/product implication follows

6. Optional visual block
   - If the source has strong images, diagrams, workflow figures, architecture figures, screenshots, benchmark charts, or example outputs that materially improve understanding, include as many as are useful.
   - Do not artificially cap the post at one image. Use one image when one is enough, and multiple images when different visuals explain different parts of the story.
- Prefer official images from the source artifact or its linked official pages.
- When multiple versions exist, default to the highest practical resolution that stays clean at article width.
- Each image should earn its place: use it to explain workflow, architecture, UI, benchmark behavior, qualitative output, or before/after differences.
- Reject blurry, tiny, or low-detail assets when a higher-resolution alternative is available.
- Avoid decorative or redundant images that repeat the same point without adding understanding.
- Do not force an image when no useful visual exists.
- If the source lacks good official visuals but the article has a strong workflow, architecture, comparison, or metric story, use `references/consulting-visual-spec.md` to create a grounded text-derived visual instead of a vague decorative thumbnail.

7. Optional structured comparison block
   - When the source includes role comparisons, feature matrices, workflows, benchmark axes, or clearly tabular facts, represent them as a Markdown table or another scannable structured block.
   - Prefer tables when readers benefit from side-by-side comparison.

8. Optional closing paragraph
   - When useful, end with a forward-looking or adoption-oriented takeaway

9. Optional compact source list
   - Add `Sources:` only when it materially helps traceability or the user asks for it

## Writing Rules

- Write in Korean.
- The published post must read as a normal authored article, not as a transcript of the request workflow.
- Do not mention that the user sent the link, requested the summary, asked for the post, or used AI to produce it.
- Avoid provenance-revealing phrasing such as "사용자가 보낸 링크", "요청받은 글", "이 글은 링크를 받아 정리했다", or similar workflow/meta narration inside the article body.
- If source provenance matters editorially, describe the artifact neutrally (for example, "이 비교는 Reddit 커뮤니티에서 확산됐지만 핵심 근거는 공식 포스트에 있다") without referencing the user or the generation workflow.
- If a useful official visual exists, prefer including it rather than leaving the post text-only.
- Favor high-resolution visuals that remain legible in the final article; avoid embedding images that only look acceptable as thumbnails.
- If a generative thumbnail would materially improve the post package, create one in a restrained technical/editorial style.
- Avoid loud marketing-banner aesthetics; prefer minimal, modern, research/product cover art.
- If a side-by-side comparison materially improves readability, use a Markdown table.
- Keep the piece grounded in checked sources.
- Do not make it read like a pasted abstract or README translation.
- For repositories, distinguish clearly between:
  - what the repo demonstrates,
  - what the linked paper claims,
  - what is merely planned or roadmap-level.
- For gists / idea documents, distinguish clearly between:
  - what is a design pattern or conceptual proposal,
  - what concrete tooling/workflow pieces are explicitly suggested,
  - what is not yet a packaged implementation.
- For websites and model pages, focus on:
  - product scope,
  - technical differentiators,
  - workflow/infrastructure implications,
  - evidence actually visible on the page.
- For independently authored technical report or synthesis pages, preserve that framing explicitly:
  - do not present the page as the official origin of the underlying techniques unless it actually is,
  - treat the page itself as the artifact being reviewed,
  - use the linked/cited primary papers when needed to verify terminology or historical attribution,
  - and make the article's value proposition the quality of the synthesis, compression, or comparative framing rather than pretending it is a new research contribution.
- If hard numbers are absent, do not hallucinate them.
- If the artifact is thin, say so diplomatically in the interpretation section.
- Prefer 3-5 meaningful tags, mixing English technical terms and concise category labels when appropriate.
- Titles should be publication-ready, not raw page titles unless the raw title is already strong.
- Descriptions should read like a sharp thesis sentence, similar to existing blog posts in the repo.

## Category and Slug Rules

- First inspect categories already present under `content/blog/`.
- Reuse an existing category when the fit is clear.
- Otherwise create a new category directory with a simple kebab-case name.
- Keep `category` in frontmatter aligned with the directory name.
- Slug should be short, descriptive, and stable.
- Avoid dates in the filename unless the repo already requires them.

Examples:
- `content/blog/ai-systems/context-engineering-stack.md`
- `content/blog/mlops/open-weight-eval-pipeline.md`
- `content/blog/document-ai/layout-reasoning-benchmark.md`

## Commit Message Rules

Default format:

```text
blog: add <slug> post
```

If updating an existing post:

```text
blog: update <slug> post
```

If the article centers on a specific artifact name and a more informative message is clearly better, prefer:

```text
blog: add post on <artifact-name>
```

Keep it short and factual.

## Safe Git Procedure

1. Run `git status --short --branch` in `/Users/mean/Documents/Github/d9249.github.io`
2. Confirm the target article path
3. Write the file
4. Inspect the diff for only that file
5. If the file is brand new and `git diff -- <that-file>` appears empty, confirm creation with `git status --short --branch` before proceeding; untracked files will not always show useful diff output.
6. Run `git add -- <that-file>` only
7. Commit only that staged file
8. Before pushing, check whether `origin/<branch>..HEAD` contains only the new blog commit; if older unrelated local commits are also ahead, do not auto-push them.
9. Push the current branch only when that push scope is intentional and safe

Important:
- If unrelated changes already exist, do not stage them.
- If the new article depends on touching index/config files too, verify that those edits are expected before staging them.
- If the repo is in a risky or conflicted state, explain the situation before pushing.
- If `git status --branch` or `git log origin/<branch>..HEAD` shows the branch is already ahead because of unrelated local commits, do not `git push` automatically. Commit only the blog file, then report that pushing now would also publish pre-existing local commits.
- If the working tree has unrelated modified files, it is still acceptable to create a commit for the blog post as long as only the intended blog file is staged.

## Quality Bar Before Finishing

Before finalizing, verify:
- The artifact identity is correct
- The article is saved under the intended blog path
- Frontmatter matches repo conventions
- YAML indentation is valid in the saved file. In particular, fields such as `draft:` must align with top-level keys and must not accidentally remain indented under `tags:` or another list item.
- The body contains actual synthesis, not only summary bullets
- Claims are source-grounded
- Markdown tables, if used, render correctly — specifically verify there are no accidental malformed rows such as leading double pipes (`|| ...`) from generation or copy/editing
- After writing the file, perform a concrete file-level check for malformed table rows before committing (for example, inspect the saved markdown or search for lines beginning with `||` in the target post) and fix them if present
- If generated Markdown tables contain systematic leading double pipes, normalize the saved file directly with a short Python rewrite before committing rather than repeatedly relying on fuzzy patching.
- If file-reading/search tools appear to show stale or deduplicated content right after an edit, verify the saved markdown with a direct terminal/Python read of the file before committing. Do not rely on a cached read when doing final table-format validation.
- Be careful with numbered file viewers that render lines like `44|...`: a valid Markdown table row `| col | ...` can appear visually as `44|| col | ...`. Do not mistake the viewer's line-number separator for a malformed leading double pipe. For final validation, inspect the raw file text with terminal/Python and specifically test whether the line itself starts with `||`.

- If a thumbnail was appropriate, it was either generated and wired in, or consciously skipped with a reason
- If generation APIs were unavailable, a local SVG-to-PNG fallback was considered before skipping thumbnails entirely
- If a text-derived visual was created, a visual spec exists and each number/node/label is grounded in the article or source evidence
- If the source contained structured comparison/workflow information, the post presents it as a table or another clearly scannable block
- Only intended files are staged/committed
- Push status is confirmed or the failure is clearly reported
- For the user's Gatsby blog, a successful `npm run build` can still print repeated Node deprecation warnings such as `punycode` under noisy `ERROR  UNKNOWN` banners. Treat those as non-blocking only when the command exits 0 and Gatsby reports page generation/build completion; otherwise treat them as real build failures.

## Suggested Working Pattern

When the user sends only a link:
1. Inspect the page and any official linked sources
2. Look for reusable official images, diagrams, screenshots, workflow visuals, benchmark charts, or qualitative examples
3. Decide which of those visuals actually improve comprehension and where each should appear in the article; do not default to a single hero image if multiple visuals explain different sections better
4. If the article's own prose has a workflow, architecture, metric, matrix, or executive-summary story that needs a custom figure, read `references/consulting-visual-spec.md` and draft the visual spec before writing the final image block
5. Decide whether the post should also get a generative thumbnail; if yes, define a thumbnail concept from the article angle before writing
6. Look for comparison points, matrices, workflows, benchmark axes, or other facts that should be rendered as a table
7. Infer title/category/slug
8. Draft the post
9. If appropriate, generate and save the thumbnail or text-derived visual asset, then wire it into frontmatter/template conventions or the article body
10. Save the article into the blog repo
11. Generate commit message
12. Commit and push
13. Return the saved path, visual/thumbnail path if any, commit hash/message, and a short summary of the article angle

## Reference Template

See `templates/blog-post-template.md` for a fill-in structure.
