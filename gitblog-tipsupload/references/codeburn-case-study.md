# CodeBurn Tips Case Study

Session input:

- `gitblog-tipsupload https://github.com/getagentseal/codeburn`

Why this is a useful pattern:

- CodeBurn is a fast-moving developer CLI with multiple distribution surfaces: GitHub repo, npm package, Homebrew tap, GitHub Releases, macOS menubar app, and GNOME extension.
- Good tips entries for this class should verify both source-repo facts and package/distribution facts instead of relying only on README prose.

Reusable checks performed:

```bash
# GitHub repo metadata / README / releases / tags / contents
curl -s https://api.github.com/repos/getagentseal/codeburn
curl -s https://api.github.com/repos/getagentseal/codeburn/readme
curl -s https://api.github.com/repos/getagentseal/codeburn/releases/latest
curl -s https://api.github.com/repos/getagentseal/codeburn/releases?per_page=10
curl -s https://api.github.com/repos/getagentseal/codeburn/tags?per_page=20
curl -s https://api.github.com/repos/getagentseal/codeburn/contents

# npm registry metadata — use the safe PATH on this machine when npm aborts via old Homebrew Cellar node
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin npm view codeburn version description license engines repository dist-tags --json

# Homebrew tap formula when README mentions brew tap
curl -s https://raw.githubusercontent.com/getagentseal/homebrew-codeburn/main/Formula/codeburn.rb
```

Important observations from this case:

- README said Node.js 20+, but npm package metadata for `codeburn@0.9.7` reported `engines.node >=22`; the tips entry explicitly called out this mismatch.
- GitHub latest release endpoint returned the macOS menubar release (`mac-v0.9.7`), while CLI release `v0.9.7` also existed. For projects with multiple release tracks, inspect `/releases?per_page=10`, not only `/releases/latest`.
- Official README images were more useful than GitHub Open Graph:
  - `assets/dashboard.jpg` for the TUI dashboard
  - `assets/menubar-0.8.0.png` for the macOS menubar
- For tools that read local logs, mention privacy/export caveats: local session logs can include project paths, commands, conversation/work traces, and cost data.
- For fast-moving 0.x tools, use `Open source beta` and avoid implying accounting-grade precision when providers may estimate token counts.

Validation pattern:

- Save useful official images under `static/images/tips/<slug>-*.{jpg,png}`.
- Verify frontmatter fields, valid `platforms`, and all `/images/tips/...` paths.
- Build with the safe Homebrew PATH if normal `npm` or `npm run build` aborts.
- Confirm `/public/tips/<slug>/index.html` contains title, repository, and image filenames.

Committed result in the blog repo:

- `75ab304 tips: add codeburn`
