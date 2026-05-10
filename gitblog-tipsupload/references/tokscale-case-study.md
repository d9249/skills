# Tokscale Case Study — AI coding usage observability tips entry

Use this as a pattern when a tips target is an AI/dev-observability tool that reads local logs, session databases, usage telemetry, or account tokens.

## Source investigated

- Repo: `junhoyeo/tokscale`
- Website: `https://tokscale.ai`
- npm packages: `tokscale`, `@tokscale/cli`
- Latest checked version: `v2.1.1` / npm `2.1.1` on 2026-05-10
- License: MIT
- Stack: Rust workspace + npm alias package + platform-specific native optional dependencies

## Useful workflow lessons

1. **Do not run the target CLI just to test it when it reads private local logs.**
   - Tokscale scans local AI coding assistant logs (`~/.claude`, `~/.codex`, `~/.hermes`, Cursor cache, etc.).
   - For public blog/tips writing, inspect README, package metadata, source manifests, and screenshots instead of executing the tool against the user’s machine.
   - If execution is necessary, first constrain scope with flags like `--client`, `--since`, `--json`, or a sandbox config dir; never submit/upload data.

2. **Separate local analysis from public/social upload.**
   - Local TUI/JSON analysis reads local logs.
   - Commands like `tokscale submit` upload usage data to a social platform / leaderboard.
   - Cursor integration needs a session token; treat it like a password.
   - Tips entries should explicitly warn about this boundary.

3. **Use npm metadata with safe PATH on this blog repo machine.**
   - Use:
     ```bash
     PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin npm view tokscale @tokscale/cli --json
     ```
   - Avoid default PATH if it might resolve stale Homebrew Cellar Node.

4. **When GitHub API rate limits directory/file fetches, raw.githubusercontent.com can still work for known paths.**
   - README often reveals exact asset paths such as `.github/assets/tui-overview.png`.
   - Download with:
     ```bash
     curl -L --fail --silent --show-error \
       https://raw.githubusercontent.com/<owner>/<repo>/<branch>/.github/assets/<file> \
       -o /tmp/<file>
     ```
   - This worked for Tokscale screenshots after API content calls began returning `403 rate limit exceeded`.

5. **Pick visuals that explain the tool, not generic GitHub OpenGraph.**
   - Tokscale used three official images:
     - hero image: quickly frames the product
     - TUI overview: shows token/day chart, model cost list, token breakdown, keyboard shortcuts
     - web contribution graph: shows 2D/3D activity graph, filters, cost cards, daily breakdown

## Editorial framing for this class

For AI token/cost observability tools, cover:

- Which clients are supported and where their data is read from.
- Whether data stays local by default.
- What commands upload or authenticate (`submit`, `login`, account/session tokens).
- Whether cost is estimated from pricing tables or an official invoice.
- How to scope reports by client/date before producing screenshots or exports.
- Why the tool is useful beyond raw token counting: trends, model mix, cache tokens, JSON export, visualizations.

## Suggested caveat wording

> This tool reads local AI coding assistant logs. Local reports are different from public leaderboard submission: before running upload/login commands, check exactly what data will be sent and treat any API/session tokens as credentials.
