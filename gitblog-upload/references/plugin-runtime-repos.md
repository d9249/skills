# Plugin/runtime GitHub repo evidence checklist

Use this when the URL is a GitHub repo for a Claude/Codex/plugin/runtime distribution rather than a plain library.

## Primary evidence surfaces
- GitHub API: `/repos/<owner>/<repo>`, `/readme`, `/releases/latest`, `/tags`, targeted `/contents/<path>`
- Raw manifest files:
  - `.claude-plugin/plugin.json`
  - `.claude-plugin/marketplace.json`
  - `.mcp.json`
  - `settings.json`
  - `agents/*.md`
  - nested host-specific packaging such as `codex/<name>/.codex-plugin/plugin.json`
- Official product site / marketing page
- Release page text for newest version

## What to compare explicitly
- Install path vs actual usage requirements
  - Example: site says "no signup required" while README says login is required on first tool use
- License signals
  - GitHub API `license`
  - checked-in `LICENSE`
  - README claims
  - Terms-of-Service references on official site
- Host coverage
  - Claude plugin only?
  - Codex plugin added recently?
  - Conductor or other wrappers?
- Packaging posture
  - source-first repo vs prebuilt product bundle
  - presence of bundled `node_modules`, giant generated JS, standalone helpers
- Telemetry / hosted coupling
  - analytics env vars in `.mcp.json`
  - hosted account/login flow
  - site tracking stack if relevant to product interpretation

## Strong reportable signals
- `license: null` in API but a restrictive custom `LICENSE` file in repo
- huge prebuilt runtime artifacts (tens of MB JS bundle, bundled dependencies)
- nested alternate-host packaging directory added in latest release before docs fully catch up
- marketing copy and README disagree on signup/login friction
- manifests reveal a more commercial/runtime-oriented positioning than the README alone suggests

## Good article angle
Treat these repos less like ordinary OSS libraries and more like agent runtime products that happen to distribute through GitHub. Focus on:
- runtime replacement layer
- packaging and host integration strategy
- operational reviewability
- licensing/account/telemetry trade-offs
