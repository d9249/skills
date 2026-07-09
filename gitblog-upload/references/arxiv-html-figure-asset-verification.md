# arXiv HTML Figure Asset Verification

Use this note when turning an arXiv paper with useful official figures into a blog post.

## Recommended workflow

1. Start from the exact arXiv URL the user provided, then collect `abs`, `pdf`, and `html` URLs for the same paper ID.
2. Parse the arXiv HTML for figures/captions, but treat image `src` values as candidates rather than truth.
3. Resolve and HTTP-check each candidate image URL. If a candidate 404s, try the canonical arXiv HTML asset base for the paper/version rather than repeatedly downloading broken guessed paths.
4. Save useful official figures locally under `static/images/blog/` as optimized WebP files with clear slugged names.
5. Validate all three asset layers before publishing:
   - source markdown references every intended `/images/blog/...` path;
   - `static/images/blog/...` files exist and have sane dimensions/sizes;
   - after Gatsby build, `public/images/blog/...` files and the generated post HTML contain the expected markers.
6. After deploy, verify the public article returns HTTP 200 and every referenced local image returns HTTP 200 with the expected content type.

## Legibility and matte gate

Run the helper before choosing or converting arXiv HTML figures:

```bash
python3 scripts/arxiv_html_figure_contact_sheet.py <arxiv-id-or-version> <out-dir>
```

The helper writes `contact.jpg` for visual selection and `figure_quality.json` for per-image dimensions, average luma, dark-pixel ratio, black-pixel ratio, light-pixel ratio, source URL, and warnings.

For charts, timelines, architecture diagrams, and other figures with embedded text:

- Compare the chosen local asset against the official PDF/HTML figure before embedding it.
- Reject a local asset when labels, axes, legends, or caption-bearing text are unreadable even if the file downloads and dimensions look sane.
- Treat `dark_dominant_wide_figure` as a conversion or extraction warning for chart-like figures. If the official figure is readable but the local optimized copy is dark or matte-inverted, regenerate from the official HTML image or arXiv source bundle.
- When converting transparent PNGs/SVG renders to PNG/JPEG/WebP, flatten onto a white matte unless the source figure is explicitly designed for a dark background.
