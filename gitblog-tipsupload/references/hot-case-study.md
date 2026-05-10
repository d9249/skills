# Hot Case Study — macOS Menu Bar Thermal/Sensor Utility

Use this reference when adding macOS menu bar utilities that read hardware/thermal/sensor state.

Representative input:

- `https://github.com/macmade/Hot`

## What to verify

- GitHub repo metadata: description, default branch, license, primary language, archived status.
- README value proposition and screenshots.
- GitHub Releases asset names and latest release notes.
- Homebrew cask metadata if available: version, URL, `auto_updates`, app artifact, zap paths.
- Xcode project settings:
  - `MACOSX_DEPLOYMENT_TARGET`
  - `PRODUCT_BUNDLE_IDENTIFIER`
  - `CODE_SIGN_ENTITLEMENTS`
  - hardened runtime / sandbox indicators
- `Info.plist` evidence for menu bar app behavior:
  - `LSUIElement` for agent/menu-bar style app
  - bundle identifier
- Entitlements file, especially sandbox/app group/network permissions.
- Submodules/dependencies that reveal implementation approach, e.g. SMC, IOHID, update frameworks.
- Source files that ground sensor/thermal claims rather than relying only on screenshots.

## Useful commands/patterns

```bash
# GitHub metadata via gh to avoid unauthenticated REST rate limits.
gh api repos/macmade/Hot > /tmp/hot-api/repos_macmade_Hot.json
gh api repos/macmade/Hot/releases/latest > /tmp/hot-api/repos_macmade_Hot_releases_latest.json
curl -L -o /tmp/hot-README.md https://raw.githubusercontent.com/macmade/Hot/main/README.md
curl -L -o /tmp/hot-Hot_Info.plist https://raw.githubusercontent.com/macmade/Hot/main/Hot/Info.plist
curl -L -o /tmp/hot-Hot_Hot.entitlements https://raw.githubusercontent.com/macmade/Hot/main/Hot/Hot.entitlements
curl -L -o /tmp/hot-Hot.xcodeproj_project.pbxproj https://raw.githubusercontent.com/macmade/Hot/main/Hot.xcodeproj/project.pbxproj
curl -L -o /tmp/hot-.gitmodules https://raw.githubusercontent.com/macmade/Hot/main/.gitmodules
curl -L -o /tmp/hot-dist-hot.json https://formulae.brew.sh/api/cask/hot.json
```

README images can be better than GitHub Open Graph for small UI utilities. For Hot, save distinct official screenshots:

- Intel menu view: shows CPU speed limit, scheduler limit, available CPUs, CPU temperature.
- Apple Silicon menu view: shows CPU temperature and thermal pressure.
- Sensors graph view: shows sensor cards, search/filter, temperature/voltage/current filters.

## Editorial framing

For macOS hardware monitor/menu-bar utilities, explain real OS support explicitly. The site may use `macos-linux` as the closest bucket, but the body/highlights should say `macOS 전용` if the app is macOS-only.

Separate architecture-specific behavior:

- Intel Mac: CPU speed limit, scheduler limit, available CPUs, CPU temperature.
- Apple Silicon: CPU temperature and macOS thermal pressure; do not imply Intel-style CPU speed limit is available.

Position the tool as a quick status indicator unless it truly provides long-term logging/remote monitoring. Avoid overstating sensor accuracy across every Mac model; sensor names and availability differ by hardware and macOS version.

## Safe git lesson from the session

During the Hot run, unrelated local modifications briefly appeared in status (`gatsby-node.js`, tips index/pagination components). The correct response was:

1. Do not stage them.
2. Inspect `git status --short --branch` and focused diffs to understand scope.
3. Continue validating/building only if the intended content is safe.
4. Before commit, verify status again and stage only the intended post/images.
5. Confirm `origin/main..HEAD` had no unrelated ahead commits before creating/pushing the tips commit.

This reinforces the general rule: tips upload commits must include only the intended Markdown and images, even when the working tree contains unrelated edits.
