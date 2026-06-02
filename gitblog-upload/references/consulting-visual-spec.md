# Consulting Visual Spec Workflow

Use this reference when a blog post would benefit from a text-derived diagram, chart, matrix, or editorial cover. The goal is not to imitate a consulting brand; it is to make the article's argument visible through a grounded, reusable visual specification before drawing anything.

## Core Rule

Do not jump from prose directly to "make a nice image." First classify the article section by communication intent, then write a compact visual spec with the chosen visual type, source evidence, output path, alt text, and QA checks.

For this user's Korean gitblog workflow, every public-facing visual must be Korean-first. Visible text in diagrams, charts, thumbnails, captions, and alt text should be Korean unless it is an official product name, model name, library name, command, URL, benchmark name, or source identifier.

Text fit is a hard acceptance criterion, not polish. A visual is not done until the final rendered image has been inspected and all text stays inside its intended panel, chip, axis label, card, or title area without clipping, overlap, or awkward spillover.

Connector logic is also a hard acceptance criterion. Arrows should encode an explicit direction from the article or visual spec. Do not add decorative arrows just to make a graphic feel dynamic, and do not accept arrows that point into labels, terminate in empty space, cross unrelated content, or use renderer-scaled arrowheads that become visually disproportionate. When the relationship is grouping, co-occurrence, dependency, or "several parts produce one shared result," prefer numbered cards, separators, grouping bands, or a shared result band over arrows.

Visual variety is a functional requirement. Do not let every generated image collapse into the same three-card or card-grid template. The selected layout should make a specific kind of reasoning easier:
- use stack/layer maps for runtime layers, responsibility boundaries, or operating models;
- use before-after boards for measured deltas;
- use matrices for tradeoffs or capability comparison;
- use timelines for release or process phases;
- use issue trees for causes and risks;
- use dashboards only when several independent metrics must be scanned together.
When creating more than one visual for the same post, use distinct layout grammars unless the visuals are intentionally a repeated series.

## Visual Type Catalog

| Article signal | Prefer visual type | Use when | Avoid when |
|---|---|---|---|
| One decisive thesis or headline conclusion | `impact_summary` | The post needs one strong social/hero card | The body has several separate claims |
| 2-4 core takeaways with supporting bullets | `executive_takeaways` | The intro or conclusion has a structured argument | The content is mainly a process or metric set |
| Runtime, architecture, toolchain, workflow | `process_flow` or `architecture_map` | Components pass artifacts, state, requests, or evidence | The relation is merely a list |
| Problem decomposition or root causes | `issue_tree` | The article explains why a system fails or what layers cause risk | The branches are chronological steps |
| Metrics, benchmark deltas, token/cost changes | `metric_dashboard` or `comparison_chart` | The source has grounded numbers readers should compare | Numbers are speculative or unverified |
| Options, capabilities, feature families | `comparison_matrix` | Side-by-side comparison helps scan product/runtime tradeoffs | A simple Markdown table is enough |
| Prioritization, maturity, risk, readiness | `assessment_matrix` or `status_table` | Items need high/medium/low, green/amber/red, or quadrant framing | The source does not support scoring |
| Roadmap, phases, release path | `timeline` or `phase_flow` | The artifact has a clear sequence or delivery plan | There is no real temporal order |

## Visual Spec Schema

Write this as JSON or YAML in the working notes before creating the asset:

```json
{
  "id": "short-visual-id",
  "type": "architecture_map",
  "article_section": "핵심 아이디어 / 구조 / 동작 방식",
  "message": "One sentence explaining the image's point.",
  "source_evidence": [
    "Article sentence, official metric, table row, or source URL grounding the visual"
  ],
  "content": {
    "nodes": [],
    "metrics": [],
    "comparisons": [],
    "steps": []
  },
  "output": {
    "path": "/images/blog/<slug>-<short-name>.svg",
    "alt": "Precise accessible description",
    "caption": "Korean caption that explains why the figure matters"
  },
  "qa": [
    "All local image paths exist",
    "SVG has title/desc or raster has useful alt text",
    "Visible text is Korean-first except proper nouns and commands",
    "Text remains legible at article width",
    "Rendered final image has no clipped, overflowing, or overlapping text",
    "Arrows and connectors match explicit workflow direction and render at sensible size",
    "Layout grammar is chosen for the content and is not a recycled card-grid default",
    "No unsupported numeric claim appears only in the image"
  ]
}
```

## Renderer Selection

Prefer deterministic renderers for technical posts:

- `SVG`: default for architecture maps, process flows, issue trees, static dashboards, and editorial covers.
- `Markdown table`: use when a table is clearer than a figure and does not need visual hierarchy.
- `HTML/CSS screenshot`: use when the site style itself should frame a card or dashboard.
- `PPTX slide renderer`: useful as a template-selection sandbox or when the user explicitly wants a deck-like deliverable; export to image only after visual QA tooling is available.
- Generative image model: use mainly for abstract editorial covers, not for numeric charts or detailed architecture text.

## Public Wording

Use neutral labels such as `consulting-style`, `executive diagram`, `metric dashboard`, or `strategy visual`. Do not publish brand-specific phrasing such as "McKinsey-style" in captions, alt text, filenames, or public article prose.

## QA Checklist

Before committing a post with text-derived visuals:

- The visual spec chooses a type for a stated reason and rejects at least one nearby type when the choice is not obvious.
- The visual spec also chooses a layout grammar and explains why it fits the content better than a generic card grid.
- If the post has multiple visuals, their layout grammars differ unless the spec explicitly says they are a repeated series.
- All visible text is Korean-first except official artifact names, model names, library names, commands, URLs, and source identifiers.
- Long Korean labels are manually wrapped or shortened before rendering; do not rely on the renderer to auto-fit SVG `<text>`.
- Every number in the visual also appears in the article body or a cited source.
- Every generated local asset is referenced by the article or frontmatter.
- For SVG, include `<title>` and `<desc>`, stable dimensions, and readable text at final article width.
- Render the final SVG/HTML/card to the actual output size and inspect the image. Reject it if any text is clipped, overlaps another component, or escapes its panel/card/chip/axis.
- For diagrams, connectors should show direction clearly, should not terminate inside labels or empty space, and should not be used unless the visual spec states the relationship they encode.
- If a human reviewer would ask "why is this arrow here?", remove the arrow and use numbering, spacing, dividers, or grouping instead.
- For SVG markers, use fixed-size arrowheads or manually drawn arrowheads when needed; avoid marker settings that scale arrowheads into oversized triangles.
- If the site supports `image` frontmatter, the image path exists and is queried/rendered by the template; if the template ignores it, note the gap rather than assuming it works.
