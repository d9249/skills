# MarkEdit Case Study — macOS Document Editor / Markdown App Pattern

Use this reference when a `gitblog-tipsupload` target is a macOS-only document editor, Markdown editor, or native productivity app rather than a CLI/library.

Session input:

- `https://github.com/MarkEdit-app/MarkEdit`
- Output slug: `markedit`
- Final commit: `f8fae8c tips: add markedit`

## What to Verify

For macOS document/editor apps, do not stop at the README. Cross-check these surfaces:

1. **GitHub metadata**
   - `full_name`, description, license, topics, default branch, latest release.
   - If unauthenticated GitHub REST rate limit is hit, retry with `gh api` or direct raw URLs instead of guessing.

2. **README**
   - One-line positioning: MarkEdit is “like TextEdit on Mac but dedicated to Markdown.”
   - Install path: GitHub Releases DMG or Homebrew cask.
   - Real OS support: latest line is macOS 15.0+ even though the site platform bucket is `macos-linux`.
   - Core claims: 4 MB app, 10 MB file handling, privacy-focused, GFM compliance, native integration, CodeMirror 6.

3. **Official wiki/docs**
   - Raw wiki pages can be fetched directly, e.g. `https://raw.githubusercontent.com/wiki/MarkEdit-app/MarkEdit/Manual.md`.
   - Useful MarkEdit wiki pages: `Manual`, `Why-MarkEdit`, `Philosophy`, `Development`.
   - Extract workflow-level details: default app setup, TOC shortcuts, multi-caret editing, code folding, word completion, statistics panel, Quick Look/Finder extensions, Pandoc integration, Shortcuts remapping.

4. **Homebrew cask**
   - Check `https://formulae.brew.sh/api/cask/markedit.json` and Homebrew cask source.
   - Confirm latest version, DMG URL, checksum, minimum macOS requirement, app artifact name.
   - For MarkEdit: cask version `1.32.1`, depends on macOS `>= 15`/Sequoia.

5. **App project files**
   - `MarkEdit.xcodeproj/project.pbxproj` revealed `MACOSX_DEPLOYMENT_TARGET = 15.0`.
   - `MarkEditMac/Info.plist` revealed supported document types (`md`, `markdown`, `textbundle`, plain text, etc.), URL scheme, AppleScript support.
   - `MarkEditMac/Info.entitlements` confirmed sandboxing and user-selected file access.
   - `Build.xcconfig` confirmed marketing version and bundle identifier context.

6. **Releases**
   - Latest release assets showed both universal and Apple Silicon DMG files.
   - Release body clarified latest update context: v1.32.1 bug fixes/performance, following v1.32.0 statistics/tab/selection improvements.

## Visual Selection Pattern

For a polished macOS editor, official screenshots are more useful than GitHub Open Graph images.

MarkEdit official screenshot choices:

- `Screenshots/01.png` → editor UI, light/dark mode, toolbar, table of contents, Writing Tools. Use as representative image.
- `Screenshots/02.png` → selection statistics and word completion. Use for productivity features.
- `Screenshots/04.png` → settings/preferences. Use for configuration section.
- `Screenshots/03.png` was redundant with the editor view and can be skipped.

If PIL is unavailable for resizing/conversion (`No module named 'PIL'`), copying the original PNGs is acceptable when file sizes are reasonable and high-resolution images help understanding.

## Writing Angle

Frame this class of app around workflow fit, not exhaustive feature inventory:

- “TextEdit-like Markdown editor for macOS”
- Source-first Markdown editing: syntax visible rather than hidden WYSIWYG.
- Native macOS integration: Quick Look, Finder extension, AppleScript, Shortcuts, Writing Tools, inline predictions.
- Deliberately limited scope: not a note database, not a second brain, not an all-in-one exporter.
- Installation caveat: latest app may require newer macOS than older users expect.

Useful sections used in the final post:

- `## MarkEdit 개요`
- `## 설치와 요구사항`
- `## 글쓰기 경험: 원문 Markdown을 유지하면서 보기 좋게 편집`
- `## 통계와 완성 기능`
- `## 설정에서 먼저 볼 만한 것`
- `## macOS 통합이 좋은 지점`
- `## 하지 않는 것도 분명하다`
- `## 어떤 사람에게 잘 맞나`
- `## 내 판단`

## Pitfalls

- Do not imply Linux support just because `platforms: ["macos-linux"]` is the closest site category. Explicitly say the app is macOS-only or macOS-centered.
- Do not claim “native text engine” if the app uses CodeMirror/WebKit for editing; explain the hybrid stack accurately.
- Do not assume the app includes full HTML preview/export. MarkEdit delegates preview to `MarkEdit-preview` and export flows to Pandoc.
- For sandboxed macOS apps, default-file-app setup may require Finder `Get Info` → `Open with` → `Change All...`; do not invent an in-app setting.
- Latest README badges and Homebrew cask can change minimum OS requirements; verify both before writing.
