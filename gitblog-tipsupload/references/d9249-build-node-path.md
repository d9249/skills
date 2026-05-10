# d9249.github.io Node PATH / Homebrew build note

During a tips upload build, `npm run build` failed before Gatsby started because the shell resolved `node` from an old shadowing path:

- Bad node path: `/opt/homebrew/Cellar/node/25.6.1_1/bin/node`
- Error: `Library not loaded: /opt/homebrew/opt/llhttp/lib/libllhttp.9.3.dylib`
- Installed Homebrew node was newer and valid: `/opt/homebrew/bin/node` -> `/opt/homebrew/Cellar/node/26.0.0/bin/node`

The fix was not a content change. Re-run build with a clean PATH that prefers Homebrew's public bin symlinks:

```bash
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin npm run build
```

Diagnostic commands that identified the issue:

```bash
which -a node npm
node -v || true
npm -v || true
brew info node llhttp
find /opt/homebrew/Cellar/llhttp -maxdepth 3 -type f -name 'libllhttp*.dylib' -print
```

Use this note for future `gitblog-tipsupload` / d9249 Gatsby build failures that mention `libllhttp` or show a Cellar-specific node path ahead of `/opt/homebrew/bin` in PATH.