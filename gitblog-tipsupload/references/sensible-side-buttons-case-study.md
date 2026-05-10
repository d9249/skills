# SensibleSideButtons case study: old macOS event-tap/menu-bar utilities

Use this as a pattern when adding small macOS-only mouse/keyboard/menu-bar utilities whose README is sparse but an official website has deeper behavior notes.

## Source URL

- User input: `https://github.com/archagon/sensible-side-buttons`
- Output slug: `sensible-side-buttons`
- Output file: `content/tips/sensible-side-buttons.md`

## What to verify

1. **Duplicate search**
   - Search for repo, title, slug, and source URL in `content/tips`.

2. **Repo metadata**
   - GitHub API showed:
     - full name: `archagon/sensible-side-buttons`
     - description: macOS menu bar app for system-wide navigation side buttons on third-party mice
     - default branch: `master`
     - language: C / Objective-C project
     - license: `GPL-2.0`
     - latest release: `1.0.6` from 2018 with DMG asset
   - Tags: `1.0.6`, `1.0.5`, `1.0`.

3. **Official website is essential**
   - README is short and points to `http://sensible-side-buttons.archagon.net`.
   - Fetch the official site HTML and media manually; it contains the useful explanation and images:
     - `app.jpg` / `app.mp4` — behavior demo
     - `bar.png` — menu-bar icon/state
     - `settings.png` — macOS Trackpad “Swipe between pages” context
   - Do not rely on a nonexistent README `screenshot.png`; raw URL may return 404 text/HTML.

4. **Install/distribution**
   - Official install path is GitHub Releases DMG, not Homebrew.
   - Homebrew formula/cask checks returned 404 for `sensible-side-buttons`.
   - State that the latest packaged release is old and that modern macOS should be tested directly.

5. **Native app evidence**
   - `SideButtonFixer/Info.plist`:
     - `LSUIElement=true` menu-bar/background style app
     - `CFBundleShortVersionString=1.0.6`
   - Xcode project:
     - `MACOSX_DEPLOYMENT_TARGET=10.10` for app target
     - `PRODUCT_BUNDLE_IDENTIFIER=net.archagon.sensible-side-buttons`
   - Entitlements are effectively empty.

6. **Behavior/source evidence**
   - `AppDelegate.m` registers defaults:
     - `SBFWasEnabled`, `SBFMouseDown`, `SBFDonated`, `SBFSwapButtons`.
   - Menu items include:
     - `Enabled`
     - `Trigger on Mouse Down`
     - `Swap Buttons`
     - `Hide Menu Bar Icon`
     - `Open Accessibility Whitelist`
     - `Quit`
   - Event handling:
     - `CGEventTapCreate(kCGHIDEventTap, ..., kCGEventOtherMouseUp|kCGEventOtherMouseDown, ...)`
     - Checks `kCGMouseEventButtonNumber` for M4/M5.
     - Returns `NULL` to swallow original M4/M5 event.
     - Posts fake left/right swipe events via `tl_CGEventCreateFromGesture` and `CGEventPost`.
   - Accessibility:
     - Uses `AXIsProcessTrustedWithOptions` and prompts/blocks menu controls when not trusted.

## Writing stance

- Because site platform buckets only include `macos-linux` and `winos`, use `macos-linux` for macOS-only utilities and explicitly say the tool is macOS-only in the body/highlights.
- For old macOS event-tap utilities, do **not** imply current macOS compatibility from old deployment target alone.
- Mention Accessibility/Input Monitoring style permission implications when global mouse/keyboard events are intercepted.
- License/adoption caveat: GPL-2.0 matters if modifying or redistributing internally.

## Images used

Save official media as local tips assets:

- `/static/images/tips/sensible-side-buttons-app.jpg`
- `/static/images/tips/sensible-side-buttons-menubar.png`
- `/static/images/tips/sensible-side-buttons-trackpad-settings.png`

## Validation/build notes

- Frontmatter platforms: `['macos-linux']` only.
- Build command should use safe PATH:
  `PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin npm run build`
- Gatsby may print the known `punycode` deprecation warning under `ERROR UNKNOWN`; if exit code is 0 and page exists, treat it as non-blocking.