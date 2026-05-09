# DESIGN.md catalog / marketplace sites

Use this when the user asks for a blog post about a site like `getdesign.md` that distributes `DESIGN.md` files rather than a single model/repo.

## Evidence checklist

1. Read the landing page metadata (`title`, `description`, `og:image`) and the explainer page (for example `What is DESIGN.md?`) to capture the product thesis in the site's own words.
2. Inspect at least one concrete catalog entry page, not just the homepage.
   - Look for install command patterns such as `npx ... add <slug>`
   - Look for usage counters like installs/bookmarks/saves
   - Look for disclaimers like "not an official design system" vs curated starting point
   - Look for preview surfaces (live preview, light/dark toggle, iframe preview)
3. Check structured data / JSON-LD on the site for `sameAs`, `CreativeWork`, `Organization`, or breadcrumb hints.
   - This can reveal a backing repo or product split not obvious from the visible UI.
4. Follow the backing GitHub repo/API if public.
   - Verify stars/forks/license/default branch
   - Enumerate the actual collection tree with `/contents/...` instead of trusting badge counts only
   - If homepage/README says `71` items but the live tree returns `70`, report the discrepancy as a catalog-drift signal instead of normalizing it away
5. Fetch one representative raw `DESIGN.md` file from the collection.
   - Use it to judge whether the project is shipping shallow theme tokens or a richer rationale + component-spec document
6. Distinguish the open data layer from the closed product layer.
   - Example: a public `awesome-design-md` repo may exist while the web app repo referenced in structured data returns 404/private

## Interpretation angles that worked well

- Treat the site as a **distribution surface for agent-readable design context**, not merely an inspiration gallery
- Emphasize that `DESIGN.md` turns design language into an installable text asset for coding agents
- When entry pages expose usage counters and install commands, interpret the site as a marketplace / package-distribution layer rather than a static docs site
- When a site offers "request private DESIGN.md" or sponsorship inventory, note the lead-gen / commercial layer explicitly

## Pitfalls

- Do not assume all listed counts are perfectly synchronized across homepage, README badges, and GitHub tree
- Do not present curated brand-inspired files as official design systems if the entry page disclaims that
- Do not treat the existence of a public collection repo as proof the whole extraction/generation pipeline is open source