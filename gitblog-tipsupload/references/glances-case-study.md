# Glances Case Study — system monitoring CLI/Web/API tools

Use this reference for mature cross-platform system monitoring tools that combine terminal UI, web UI, REST/API surfaces, Docker deployment, package registries, and security-sensitive runtime exposure.

## Source surfaces checked

- GitHub repository: `nicolargo/glances`
- Default branch: `develop`
- README: `README.rst`
- Latest release: `v4.5.4` at session time
- Package metadata: `pyproject.toml`, PyPI `Glances`, Homebrew formula `glances`, Docker Hub `nicolargo/glances`
- Docs: install, quickstart, REST API, MCP API, Docker, command reference
- License: GitHub/API plus checked-in `COPYING`; use `LGPL-3.0-only` when package metadata confirms it

## Evidence-gathering pattern

1. Fetch repo and release metadata with `gh repo view` / GitHub API.
2. Download README and docs from the actual default branch (`develop` for Glances, not `main`).
3. Cross-check install instructions across README, PyPI, Homebrew, and Docker docs.
4. Inspect `pyproject.toml` for Python version and optional extras. For Glances-like tools, extras reveal real feature surfaces: `web`, `containers`, `gpu`, `sensors`, `export`, `snmp`, `mcp`, etc.
5. Read recent release notes when the tool exposes Web/API surfaces. For Glances, recent 4.5.x releases contained several security fixes around CORS, unauthenticated APIs, DNS rebinding, secrets redaction, SSRF, command injection, SQL/CQL injection.
6. Choose screenshots that show distinct modes rather than many decorative images.

## Image choices that worked

Official docs images were materially useful and saved under `static/images/tips/`:

- `glances-tui.png` — terminal/TUI overview; best representative image
- `glances-web.png` — browser Web UI; supports `glances -w` and REST API discussion
- `glances-fetch.png` — `--fetch` one-shot summary mode; useful for quick SSH/status-check framing

Avoid generic GitHub Open Graph images when official TUI/Web screenshots exist.

## Writing points to capture

- Position the tool as a practical system status board, not only a process viewer like `top`/`htop`.
- Cover multiple modes: standalone TUI, client/server, Web server, browser/central view, fetch, stdout/CSV/JSON.
- Include install options only after cross-checking: `pip install glances`, `glances[web]`, `glances[all]`, `uvx glances`, `pipx`, Homebrew, Docker, Windows via Python.
- Explain Docker host monitoring tradeoffs: `--pid host`, `--network host`, Docker socket mounts are powerful and security-sensitive.
- Mention MCP only if docs confirm it; for Glances, `glances -w --enable-mcp` exposes SSE at `/mcp/sse` and inherits web server auth policy.

## Security caveat pattern

For any tool with Web UI, REST API, XML-RPC, MCP, central browser, or remote monitoring:

- Do not just say “run `tool -w`”; state the default bind/auth behavior if docs provide it.
- For Glances docs, default web server behavior was authentication off and bind to `0.0.0.0`; this can expose process command lines and sensitive system info.
- Recommend `--password`, `--bind 127.0.0.1`, reverse proxy with TLS/auth, allowed-host/CORS review, and current version upgrades when relevant.
- Recent security release notes are editorially important evidence, not noise.

## Validation lesson

When validating frontmatter, parse YAML and inspect `fm['platforms']`. Do not use broad regexes like `^\s*- "..."` over the whole frontmatter; they also match `tags` and `highlights`, causing false invalid platform errors.
