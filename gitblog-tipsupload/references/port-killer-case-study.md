# PortKiller case study — desktop utility with platform-specific builds

Use this reference when `gitblog-tipsupload` handles a desktop utility, menu bar app, tray app, or cross-platform local developer tool.

Input handled:

- `https://github.com/productdevbook/port-killer`

## What made this case useful

PortKiller was not just a README-only GitHub utility. The reliable tips entry required cross-checking several distribution and implementation surfaces:

- GitHub repo metadata: `productdevbook/port-killer`, public, MIT, Swift primary language
- README: value proposition, supported platforms, official screenshots, install notes
- GitHub Releases: latest release `v3.3.1`, macOS DMG, Windows x64/arm64 ZIP assets
- `appcast.xml`: Sparkle/macOS update metadata and macOS minimum version signal
- Homebrew tap cask: official cask command and OS requirement
- `platforms/macos/Package.swift`: SwiftUI menu bar app, macOS 15+, dependencies
- `platforms/windows/README.md`: Windows requirements, admin rights, IPv4 limitation, process kill caveats
- `platforms/windows/PortKiller/PortKiller.csproj`: `.NET` target (`net9.0-windows`)
- `platforms/windows/PortKiller/app.manifest`: elevation/admin intent
- platform source files: how port scan and kill operations are implemented

## Reusable workflow

1. Start with repo metadata, README, latest release, tags, and root contents.
2. If the tool is a desktop app, inspect platform folders such as:
   - `platforms/macos/`
   - `platforms/windows/`
   - `apps/desktop/`
   - `src-tauri/`
   - `electron-builder.*`
3. If README mentions auto-update or native distribution, check update/distribution metadata:
   - `appcast.xml` for Sparkle apps
   - Homebrew formula/cask in the project or linked tap
   - GitHub release asset names and architectures
   - Windows manifests, installers, or `.csproj`/MSIX metadata
4. Download official screenshots from README/docs only when they materially explain the UI. For PortKiller, the useful local images were:
   - `static/images/tips/port-killer-macos.png`
   - `static/images/tips/port-killer-windows.jpeg`
5. Use `vision_analyze` on screenshots to extract visible UI structure before writing.
6. In the article, distinguish blog category slugs from real platform support. `macos-linux` may be the closest available category slug, but the body should say when the real support is macOS-only or macOS+Windows, not Linux.
7. For tools that kill processes, manage ports, require elevated permissions, read local logs, or alter the system, include an explicit safety/caveat section.

## Editorial angle that worked

The final framing was not “a port killer app” only; it was a practical local development network control panel:

- local TCP ports and PID/process names
- macOS menu bar / Windows tray workflows
- Kubernetes port-forward sessions
- Cloudflare Tunnel visibility
- watched/favorite ports
- kill-all/deep-kill safety caveats

## Validation pattern

After writing:

- verify frontmatter, platform slugs, and image existence with the standard Python validation snippet
- run Gatsby build with the safe PATH on this user's machine:
  `PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin npm run build`
- verify `public/tips/<slug>/index.html` includes title, repository, and local image filenames
- stage only the markdown file and intended images
- confirm `origin/main..HEAD` contains only the intended tips commit before push
