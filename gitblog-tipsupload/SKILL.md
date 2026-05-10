---
name: gitblog-tipsupload
description: Use when the user provides a GitHub repository, app, CLI tool, or useful library URL and wants it added as a Korean tips entry under the d9249.github.io content/tips collection, with repo-focused evidence gathering, practical usage framing, build verification, and safe git commit/push.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tips, github, library, apps, cli, productivity, git]
    related_skills: [gitblog-upload, github-repo-management]
argument-hint: "<URL> [slug] [platforms]"
---

# Gitblog Tips Upload

## Overview

This skill is the tips-focused companion to `gitblog-upload`.

Use it when the user sends a GitHub repository, open-source app, CLI utility, developer library, local productivity tool, or small useful project and wants it added to the user's tips collection rather than written as a full AI lab-style blog article.

Primary output path:

- `/Users/mean/Documents/Github/d9249.github.io/content/tips/<slug>.md`

The current tips section is designed as a curated library/app catalog. Each entry should help a reader quickly answer:

1. What is this tool?
2. What problem does it solve?
3. Which platforms does it apply to?
4. What makes it useful or distinctive?
5. How would I install, try, or evaluate it?
6. What license, maturity, or operational caveats should I know before adopting it?

Do not write a long research-post-style essay unless the source really requires it. Tips entries should be practical, scannable, and opinionated.

## When to Use

Activate this skill when the user says things like:

- `gitblog-tipsupload <URL>`
- "tips에 추가해줘"
- "유용한 라이브러리로 정리해줘"
- "이 GitHub repo를 tips 컬렉션에 넣어줘"
- "앱/CLI/라이브러리 추천 항목으로 만들어줘"
- "content/tips에 글을 추가해줘"

Good input types:

- GitHub repositories for useful developer tools, libraries, desktop apps, menu bar apps, CLIs, local-first tools, automation helpers, plugins, and small utilities
- Official product/documentation pages for installable OSS tools
- Package registry pages when paired with source repo evidence
- App release pages when they are the canonical distribution surface

Do not use this skill for:

- Full paper/model/product launch analysis — use `gitblog-upload`
- YouTube-driven long-form article generation — use `gitblog-mvupload`
- Personal notes not intended for the public tips collection
- Tools with no accessible primary source unless the user explicitly wants a speculative placeholder

## Live Repo Grounding

Current repo path:

- `/Users/mean/Documents/Github/d9249.github.io`

Current tips source path:

- `/Users/mean/Documents/Github/d9249.github.io/content/tips`

Current tips URL shape:

- `/tips/<slug>/`

Current tips renderer facts:

- `gatsby-node.js` marks Markdown files from the `tips` source instance as `contentType: "tip"`.
- `src/templates/tip-post.js` renders `title`, `description`, `repository`, `sourceUrl`, `status`, `license`, `platforms`, and `tags` from frontmatter.
- `src/components/TipsIndex.js` renders `highlights` on cards.
- `tip-post.js` removes a trailing paragraph that starts with `Sources:` from rendered article HTML, so prefer a normal `## 참고한 공개 자료` section for visible sources.
- `src/data/tipCategories.json` currently supports platform slugs:
  - `macos-linux` — label `macOS / Linux`
  - `winos` — label `WinOS`

The existing frontmatter pattern is:

```yaml
---
title: "<Korean title>"
date: "YYYY-MM-DDTHH:mm:ss"
description: "<one-sentence practical summary>"
author: "Sangmin Lee"
repository: "owner/repo"
sourceUrl: "https://github.com/owner/repo"
status: "Open source"
license: "MIT"
platforms:
  - "macos-linux"
  - "winos"
tags:
  - "CLI"
  - "Developer Tools"
highlights:
  - "Index card bullet 1."
  - "Index card bullet 2."
draft: false
---
```

Use an ISO-like local timestamp with seconds for tips dates, e.g. `date: "2026-05-10T19:26:19"`. Capture the live local timestamp at drafting time with `date '+%Y-%m-%dT%H:%M:%S'` unless the live repo changes the convention; do not use date-only `YYYY-MM-DD` for new tips entries.

## Source Collection Workflow

Always start from the exact URL the user provided.

For a concrete CLI/developer-tool example with multiple distribution surfaces (GitHub, npm, Homebrew tap, Releases, official images, macOS/GNOME companion apps), see `references/codeburn-case-study.md`. Use it as a pattern when README claims, package metadata, and release tracks need cross-checking.

For AI/dev-observability tools that read local logs, session databases, usage telemetry, or account tokens, see `references/tokscale-case-study.md`. Use it as a pattern for privacy-safe source inspection, avoiding accidental execution against the user's local logs, distinguishing local analysis from public/social upload, and handling GitHub API rate limits by downloading known README asset paths from `raw.githubusercontent.com`.

For a desktop/menu-bar/tray utility example with macOS and Windows builds, official screenshots, Sparkle appcast metadata, Homebrew cask, Windows manifest, and platform-specific implementation folders, see `references/port-killer-case-study.md`.

For a macOS-only document editor or Markdown productivity app, see `references/markedit-case-study.md`. Use it as a pattern for checking official wiki pages, Homebrew cask minimum OS requirements, Xcode project deployment targets, Info.plist document types, entitlements/sandboxing, official screenshots, and macOS system integrations such as Quick Look, Finder extensions, AppleScript, Shortcuts, inline predictions, and Writing Tools.

For macOS menu bar hardware/thermal/sensor utilities, see `references/hot-case-study.md`. Use it as a pattern for checking Xcode project settings, `LSUIElement`, entitlements, Homebrew cask metadata, Release ZIP assets, submodules such as SMC/IOHID/update frameworks, and architecture-specific behavior differences such as Intel CPU speed limit versus Apple Silicon thermal pressure.

For macOS-only clipboard/history utilities, see `references/maccy-case-study.md`. Use it as a pattern for preserving the official Homebrew command even when cask metadata is inspected, extracting useful frames from official demo videos when README screenshots are sparse, checking `LSUIElement`/Sparkle/appcast/minimum macOS evidence, and writing stronger privacy caveats around copied passwords, tokens, pasteboard types, Ignore rules, Accessibility permission, and clear-on-quit behavior.

For old macOS event-tap/menu-bar utilities that modify global mouse or keyboard behavior, see `references/sensible-side-buttons-case-study.md`. Use it as a pattern for checking official websites when README is sparse, collecting website media, verifying `LSUIElement`, `CGEventTapCreate`, `AXIsProcessTrustedWithOptions`, bundle IDs, deployment targets, old DMG-only releases, missing Homebrew casks, and writing careful caveats about Accessibility permissions and modern macOS compatibility.

For mature cross-platform system monitoring tools that expose TUI/Web UI/REST API/Docker/MCP surfaces, see `references/glances-case-study.md`. Use it as a pattern for cross-checking package registries and docs, selecting distinct mode screenshots, and writing security caveats for unauthenticated Web/API exposure, bind addresses, CORS/allowed-hosts, reverse proxies, Docker socket mounts, and recent security release notes.

### 1. Identify the artifact

Extract and verify:

- canonical repo or project name
- owner / organization
- source URL
- official website or docs URL if linked
- package registry URL if applicable
- license from both GitHub API and checked-in `LICENSE` when adoption risk matters
- default branch
- primary language / stack
- release/tag signals
- install commands
- supported platforms
- whether the project is a library, CLI, desktop app, menu bar app, plugin, framework, or app bundle

For GitHub repositories, prefer GitHub REST API and raw files over browser-only extraction:

```bash
curl -s https://api.github.com/repos/<owner>/<repo>
curl -s https://api.github.com/repos/<owner>/<repo>/readme
curl -s https://api.github.com/repos/<owner>/<repo>/releases/latest
curl -s https://api.github.com/repos/<owner>/<repo>/tags?per_page=20
curl -s https://api.github.com/repos/<owner>/<repo>/contents?ref=<default_branch>
```

If `/releases/latest` returns 404, also check tags, README version badges, package manifests, and install instructions before concluding there is no release signal.

### 2. Read the README like a user, not like a reviewer

For tips entries, the README is mainly evidence for:

- the one-line value proposition
- screenshots/GIFs that show the product surface
- install command
- configuration steps
- supported platforms
- core workflow
- known limitations
- license and contribution posture

Do not rewrite the README section-by-section. Compress it into a practical guide.

### 3. Inspect distribution and install surfaces

Depending on project shape, check:

- GitHub Releases and downloadable assets
- Homebrew formula/cask if README mentions it
- npm/PyPI/crates.io package pages if it is a library or CLI
- app bundle notarization/signing notes for macOS apps when visible
- app/update distribution metadata such as Sparkle `appcast.xml`, Homebrew formula/cask files, release asset names, Windows installers/manifests, MSIX metadata, and architecture-specific ZIP/DMG assets
- platform-specific implementation folders such as `platforms/macos`, `platforms/windows`, `src-tauri`, `apps/desktop`, or Electron app directories
- package manifests such as `package.json`, `pyproject.toml`, `Cargo.toml`, `Package.swift`, `.csproj`, `Info.plist`, `tauri.conf.json`, or `electron-builder` config
- native macOS app evidence such as Homebrew cask `depends_on`, Xcode `MACOSX_DEPLOYMENT_TARGET`, `Info.plist` document types / URL schemes / AppleScript support, entitlements/sandboxing, Quick Look or Finder extensions, and official wiki/manual pages
- docs install page when the README points to one

Record install commands exactly when they are official. If install is source-build only, say so.

When an install surface has its own metadata, compare it with the README instead of assuming they match. For example, npm `engines.node`, latest package version, Homebrew formula URL/checksum, and GitHub release assets can reveal version or requirement mismatches. On this user's machine, default `npm` invocations may abort if PATH resolves an old Homebrew Cellar node; use `PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin npm view <package> ...` for npm registry checks when needed.

### 4. Gather visuals only when useful

Tips entries do not need many images. Use visuals when they quickly explain product shape:

- app screenshot
- menu bar / tray UI
- CLI output screenshot
- workflow GIF
- architecture or setup diagram
- official Open Graph image only if no better visual exists

Default for GitHub-only tools:

- Use `https://opengraph.githubassets.com/<stable-token>/<owner>/<repo>` as a contextual repo image only when there is no more informative official screenshot.
- Prefer official screenshots from README/docs when they show the UI or workflow.
- Save local images under `static/images/tips/<slug>-<short-name>.<ext>` only when the source image is stable and materially improves the entry.

Avoid:

- generic full GitHub page screenshots
- decorative images that do not explain usage
- blurry GIF frames
- embedding many screenshots in a short tips entry

### 5. Classify practical adoption status

Use concise `status` labels that match the source evidence. Examples:

- `Open source`
- `Open source beta`
- `Experimental`
- `Archived`
- `Commercial / OSS core`
- `Source available`

Prefer `Open source` only when the repo is public and has an OSI-style license or clear checked-in license.

If the license is missing, use `license: "Unknown"` and say in the body that adoption requires checking licensing.

### 6. Choose platforms

Map the artifact to the existing platform slugs:

- `macos-linux` for tools usable on macOS and/or Linux, including cross-platform CLI libraries and Unix-first developer utilities
- `winos` for Windows support or cross-platform desktop/CLI tools that explicitly include Windows

If a tool is macOS-only, still use `macos-linux` for now because the category label is the closest existing bucket. Say `macOS 중심` or `macOS 전용` in the body/status/highlights.

If a tool is truly web-only and does not fit either category, do not invent a new category without checking `src/data/tipCategories.json` and asking or updating the site intentionally.

## Minimum Grounded Facts

Before drafting, verify as many as possible:

- repository full name
- source URL
- description / project thesis
- license
- primary language and stack
- latest release or tag, or absence of releases
- star/fork counts only if they matter editorially
- install method
- supported OS/platforms
- core usage flow
- dependency requirements
- whether it is actively maintained enough to recommend trying
- limitations, security caveats, account/token requirements, or missing packaging
- official screenshots or images worth embedding

For fast-moving repos, do not overstate maturity from star count alone. A small tool can be useful but still early.

## Tips Entry Shape

Keep the body practical and scannable. Default structure:

```markdown
<2-5 short opening paragraphs that explain what the tool is and why it is useful.>

![<Tool> repository](https://opengraph.githubassets.com/<token>/<owner>/<repo>)

## <Tool> 개요

<What it does, who it is for, how it fits into a workflow.>

## 왜 유용한가

<Practical differentiators. Prefer bullets when helpful.>

## 설치와 첫 사용법

<Official install commands and minimal first-run flow.>

```bash
<official command>
```

## 활용 포인트

<Concrete workflows, examples, when to use it.>

## 주의할 점

<License, maturity, platform, account/token, security, update caveats.>

## 내 판단

<Opinionated recommendation: who should try it, who can skip it.>

## 참고한 공개 자료

- [owner/repo GitHub repository](https://github.com/owner/repo)
- [Official docs](...)
```

Adjust headings to fit the artifact. For example:

- menu bar app: `## 메뉴바에서 무엇을 보여주는가`, `## GitHub 토큰과 알림 범위`
- CLI: `## 명령어 흐름`, `## 스크립트/CI에 넣을 때`
- library: `## API 표면`, `## 기존 대안과의 차이`
- desktop app: `## 앱 구조와 데이터 저장 방식`, `## 설치와 업데이트`

## Writing Style

Write in Korean.

Tips entries should be:

- shorter than full blog articles
- practical rather than academic
- clear about install/use cases
- honest about maturity and caveats
- useful as a curated personal library catalog

Avoid:

- overlong research-report framing
- marketing copy pasted from README
- raw bullet dumps with no synthesis
- unsupported benchmark/performance claims
- saying the user sent the link or asked for the entry

A strong tips entry should feel like: “I checked this tool enough to know where it fits, how to try it, and what to watch out for.”

## Duplicate and Update Rules

Before creating a file:

1. Search `content/tips` for the repository name, source URL, slug candidate, and project title.
2. If an existing tips entry covers the same artifact, update it instead of creating a duplicate.
3. If the existing entry is stale, refresh live facts: release/tag, install command, license, supported platforms, and major README changes.
4. If creating a new file, use short kebab-case ASCII slug: `<project-name>.md` unless collision requires a more specific slug.

Commit message:

- New tip: `tips: add <slug>`
- Update tip: `tips: update <slug>`

## Safe Git Workflow

1. Run `git status --short --branch` in `/Users/mean/Documents/Github/d9249.github.io`.
2. Do not disturb unrelated local changes.
3. Write only the intended tips file and intentional images under `static/images/tips/`.
4. Validate frontmatter fields used by the tip templates:
   - `title`
   - `date`
   - `description`
   - `author`
   - `repository`
   - `sourceUrl`
   - `status`
   - `license`
   - `platforms`
   - `tags`
   - `highlights`
   - `draft`
5. Verify every platform slug exists in `src/data/tipCategories.json`.
6. Verify local image paths exist if used.
7. Run `npm run build` unless the user explicitly says not to. If Node crashes before Gatsby starts with a Homebrew `libllhttp` dylib error, see `references/d9249-build-node-path.md` and retry with `PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin npm run build`.
8. Stage only intended files.
9. Commit with `tips: add <slug>` or `tips: update <slug>`.
10. Before pushing, confirm `origin/<branch>..HEAD` contains only the intended tips commit. If unrelated local commits are ahead, do not push automatically.
11. Push when safe and report the commit hash.

## Validation Commands

Use small checks before committing. Parse frontmatter as YAML and inspect `fm['platforms']` directly; do **not** validate platforms by running a broad regex over all frontmatter list items, because `tags` and `highlights` use the same `- "..."` syntax and will be falsely treated as platform slugs.

```bash
python3 - <<'PY'
from pathlib import Path
import re, yaml
repo = Path('/Users/mean/Documents/Github/d9249.github.io')
post = repo / 'content/tips/<slug>.md'
text = post.read_text()
assert text.startswith('---\n')
front = text.split('---', 2)[1]
fm = yaml.safe_load(front)
required = ['title','date','description','author','repository','sourceUrl','status','license','platforms','tags','highlights','draft']
missing = [k for k in required if k not in fm]
assert not missing, missing
assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', str(fm['date'])), fm['date']
valid = {c['slug'] for c in yaml.safe_load((repo/'src/data/tipCategories.json').read_text())}
unknown = [p for p in fm.get('platforms', []) if p not in valid]
assert not unknown, unknown
for src in re.findall(r'!\[[^\]]*\]\((/images/tips/[^)]+)\)', text):
    assert (repo/'static'/src.lstrip('/')).exists(), src
print('ok')
PY
```

Also verify the generated page after build. On this user's machine, prefer the Homebrew-public-bin PATH form if the default shell resolves an old Cellar-specific Node:

```bash
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin npm run build
python3 - <<'PY'
from pathlib import Path
p = Path('/Users/mean/Documents/Github/d9249.github.io/public/tips/<slug>/index.html')
assert p.exists(), p
html = p.read_text()
assert '<title>' in html
print('built', p)
PY
```

## RepoBar Test Case Pattern

RepoBar (`https://github.com/steipete/RepoBar`) is a good representative test input for this skill because it is a small practical utility rather than a research artifact.

When using RepoBar as the test case, verify:

- exact repository name: `steipete/RepoBar`
- what the app puts in the macOS menu bar
- whether it requires a GitHub token/account
- whether it focuses on pull requests, issues, notifications, or repository status
- whether distribution is via GitHub Releases, source build, Homebrew, or another channel
- license and release/tag state
- primary implementation stack
- whether it is macOS-only or cross-platform
- any official screenshots in README/assets

Then write a tips entry that is more like an adoption note than a full blog post:

- why a developer would keep it running
- what setup friction exists
- what signal/noise problem it solves
- what caveats matter before giving it GitHub access

## Common Pitfalls

1. **Writing a full blog article instead of a tip.** Tips entries should be shorter, practical, and library-catalog oriented.

2. **Forgetting `highlights`.** The tips index card uses `frontmatter.highlights`; without it the card loses much of its scannability.

3. **Using unsupported platform slugs.** Check `src/data/tipCategories.json` before writing `platforms`.

4. **Leaving `Sources:` as a final paragraph.** `tip-post.js` strips a trailing `Sources:` paragraph. Use `## 참고한 공개 자료` if sources should remain visible.

5. **Overstating release maturity.** A repo with a README and stars is not necessarily packaged or production-ready. Check releases, tags, install instructions, and manifests. If a project has multiple release tracks, such as CLI tags plus separate macOS app releases, inspect the full recent releases list instead of relying only on `/releases/latest`.

6. **Ignoring token/security/local-log requirements.** Many useful GitHub tools require PATs or OAuth scopes. AI/dev-observability tools may read local logs containing project paths, shell commands, prompts, or cost data. Mention this clearly, especially before recommending exports or screenshots.

7. **Using a generic GitHub Open Graph image when the README has a better screenshot.** Prefer the visual that explains the tool.

8. **Staging unrelated blog or site changes.** The user's blog repo often has unrelated local edits. Stage only the tips file and intentional tips images. If unrelated modified files appear during validation/build, inspect their focused diff if needed, but do not stage or reset them unless the user explicitly asks. Re-check status immediately before `git add` and use explicit file paths.

9. **Pushing unrelated ahead commits.** Always inspect `origin/<branch>..HEAD` before pushing. If unrelated local commits are ahead, do not push automatically.

11. **Blurring real OS support with the site's coarse platform buckets.** The tips site currently has only broad platform slugs. If a macOS-only app uses `macos-linux` because it is the closest category, explicitly state the real support in the body/highlights. Do not imply Linux support just because the category label says `macOS / Linux`.

12. **Skipping native-app distribution evidence.** Desktop utilities often hide important facts in appcasts, Homebrew casks, Windows manifests, `.csproj` targets, release asset names, and platform subdirectories. Check those before claiming install methods, minimum OS versions, admin/elevation requirements, or architecture support.

13. **Misdiagnosing Homebrew Node PATH crashes as site build failures.** If `npm run build` aborts with `Library not loaded ... libllhttp...` and the referenced binary is an old `/opt/homebrew/Cellar/node/<version>/bin/node`, first retry with the clean PATH from `references/d9249-build-node-path.md` before editing site content or dependencies.

14. **Under-checking macOS document/editor app evidence.** For macOS-only productivity apps, inspect Homebrew cask requirements, Xcode deployment target, `Info.plist` document types, entitlements/sandboxing, official wiki/manual pages, and official screenshots. If the site category forces `macos-linux`, explicitly state the real app support as macOS-only or macOS-centered.

15. **Assuming built-in preview/export from Markdown-editor branding.** Some editors deliberately avoid full side-by-side HTML preview or PDF/Word export and instead point to extensions or tools such as Pandoc. Verify the product philosophy and docs before listing missing/nonexistent features as built-ins.

16. **Regex-validating YAML list items as platforms.** Frontmatter fields such as `platforms`, `tags`, and `highlights` all use the same YAML list syntax. Validation scripts must parse YAML and check `fm['platforms']` specifically; otherwise tags like `CLI` or highlight sentences will be misreported as invalid platform slugs.

17. **Understating Web/API exposure risk for monitoring tools.** For system monitors and dashboards, check docs and release notes for default bind address, authentication defaults, CORS, allowed hosts, DNS rebinding protections, API token support, and reverse-proxy guidance. If Docker examples mount `/var/run/docker.sock`, use host PID/network, or expose Web/MCP endpoints, state the operational/security caveat clearly.

18. **Under-documenting clipboard-manager privacy risk.** Clipboard/history utilities can store passwords, API keys, customer data, and private snippets even when they advertise secure defaults. Inspect README/settings/source for ignored pasteboard types, app/regexp ignore rules, one-shot ignore modes, clear-on-quit, clear-system-clipboard, storage type toggles, and Accessibility permissions. Mention that confidential pasteboard defaults reduce risk but do not guarantee every secret workflow is excluded.

19. **Overriding official install commands with package-manager internals.** Homebrew may expose a GUI app through cask metadata while the project README says `brew install <app>`. Quote the official README command in the article, and use cask/appcast metadata only to verify version, asset URL, auto-update behavior, and minimum OS requirements.

## Verification Checklist

- [ ] Exact source URL inspected
- [ ] Existing tips duplicates searched
- [ ] Repository metadata and README checked
- [ ] License/status/platforms verified
- [ ] Install or first-use path captured if available
- [ ] Security/token caveats captured when relevant
- [ ] Useful visual chosen or intentionally skipped
- [ ] File saved under `content/tips/<slug>.md`
- [ ] Frontmatter matches tips template needs
- [ ] `highlights` contains 3-6 practical card bullets
- [ ] Platform slugs exist in `src/data/tipCategories.json`
- [ ] Markdown local image paths exist if used
- [ ] `npm run build` succeeds or exact failure is reported
- [ ] Only intended files staged/committed
- [ ] Push scope verified safe
- [ ] Commit hash and path reported
