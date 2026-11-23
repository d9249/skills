# arXiv HTML Figure Asset Verification

Use this note when turning an arXiv paper with useful official figures into a blog post.

## Recommended workflow

1. Resolve the exact input to its canonical paper and check submission history. Use versioned `html` and `pdf` URLs for the same revision; an unversioned PDF can advance while pinned HTML stays unchanged.
2. Parse the arXiv HTML for figures/captions, but treat image `src` values as candidates rather than truth.
3. Resolve and HTTP-check each candidate image URL. If a candidate 404s, try the canonical arXiv HTML asset base for the paper/version rather than repeatedly downloading broken guessed paths.
4. Check the article/figure license and any separate credit line before copying. For a permitted reuse, save useful figures under `static/images/blog/` as optimized WebP, name the original authors and figure, link the paper and license as required, and disclose changes such as cropping or recomposing a legend. Do not apply the site's code license to the paper or assume third-party artwork inherits the paper license.
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
- If the arXiv HTML image is low-resolution, inspect the paper PDF's embedded images before attempting source-tarball downloads or upscaling. With `pypdf.PdfReader`, enumerate `page.images`, inspect each image's native dimensions via Pillow, and extract `image.data`; PDFs can contain 2–3× larger originals than their HTML counterparts. Match the extracted figure visually against the HTML version, preserve white matte, and optimize that native original rather than enlarging a small bitmap.
- Reject a local asset when labels, axes, legends, or caption-bearing text are unreadable even if the file downloads and dimensions look sane.
- If an explicit Python interpreter imports Pillow from another Python-version environment and fails to load `_imaging`, inspect interpreter/module paths before reinstalling packages. Remove inherited `PYTHONPATH` for a verified interpreter (`env -u PYTHONPATH <python> ...`), or use an already-installed `cwebp` for RGB source figures; do not mutate Hermes or system packages merely to repair image conversion.
- Treat `dark_dominant_wide_figure` as a conversion or extraction warning for chart-like figures. If the official figure is readable but the local optimized copy is dark or matte-inverted, regenerate from the official HTML image or arXiv source bundle.
- When converting transparent PNGs/SVG renders to PNG/JPEG/WebP, flatten onto a white matte unless the source figure is explicitly designed for a dark background. On macOS, `sips` can rasterize an SVG but may leave transparency that becomes black in a WebP conversion. Composite the PNG onto a white background (for example with Pillow) before `cwebp`; remember that `sips -z` takes `height width`, not `width height`.
- Inspect `<figure><object data="…svg" type="image/svg+xml">` as well as `<img>` when the raster-only contact helper finds few figures. That helper intentionally ignores SVG objects; a small contact-sheet count does not mean the paper lacks diagrams. Resolve the actual `data` URL, retain the original SVG, and rasterize a separate copy. For high-resolution macOS rendering, retain the original `viewBox`, set only the root SVG width to the desired pixel width and height to its proportional value, then use `sips -s format png <copy.svg> --out <render.png>`. Check actual PNG dimensions and visually inspect labels before white-matte WebP conversion; measure the final WebP files separately.
- If an SVG loses artwork, the HTML raster is too small, or PDF object extraction returns only an image layer without overlaid labels, render and crop the composed figure from the pinned PDF rather than upscaling or publishing an incomplete panel. Render the single page with an installed Ghostscript: `gs -q -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -r480 -dFirstPage=<page> -dLastPage=<page> -sOutputFile=page.png paper.pdf`. Locate the diagram on a scaled preview, map the crop bounds back to native pixels, then crop and encode to WebP. Compare against the full PDF page to check that all paths and panels survived and adjacent prose was not copied. Record figure number, PDF page and crop bounds.
- A composite figure may put its legend in a separate sibling SVG. Preserve that legend when composing a local copy and check its color/series mapping against the paper.
- Use stdlib `xml.etree.ElementTree` for SVG metadata when an XML backend is not installed. `BeautifulSoup(..., 'xml')` requires an additional backend and may fail despite ordinary HTML parsing working; do not install packages just to read SVG dimensions. Outlined vector text can also have neither `<text>` nodes nor readable label comments, so verify those chart labels visually or against PDF text rather than treating an empty text extraction as missing figure content.
