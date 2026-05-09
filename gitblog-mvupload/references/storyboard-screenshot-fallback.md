# Storyboard Screenshot Fallback for YouTube Posts

Use this when direct video download fails but `yt-dlp --dump-single-json` still returns storyboard formats.

## Why this matters

Some YouTube videos expose metadata and storyboard tiles even when full MP4 download fails with HTTP 403. In that case, storyboard crops are often good enough for contextual in-post screenshots.

## Practical workflow

1. Dump metadata:

```bash
YT_DLP_BIN="$(command -v yt-dlp)"
"$YT_DLP_BIN" --dump-single-json --no-warnings --skip-download "URL" > /tmp/video.json
```

2. Inspect `formats` for storyboard entries such as `sb0`, `sb1`, `sb2`, `sb3`.
   - `sb0` is often the highest-resolution storyboard tile grid.
   - Typical fields: `rows`, `columns`, `width`, `height`, and fragment URLs like `M0.jpg`, `M1.jpg`.

3. Map target timestamps to storyboard cells.
   - Treat each storyboard fragment duration as split evenly across `rows * columns` cells.
   - Choose the cell whose midpoint is closest to the target timestamp.

4. Download the storyboard fragment image and crop the chosen cell.
   - If the grid is `3x3` and each cell is `320x180`, then cell coordinates are easy to derive with row/column math.
   - `ffmpeg` can crop a downloaded storyboard image without extra Python imaging libraries.

## Example crop pattern

If a fragment image is `960x540` and represents a `3x3` grid, crop a single cell like this:

```bash
ffmpeg -y -i /tmp/board-M5.jpg -vf 'crop=320:180:640:360' output.jpg
```

That example selects the bottom-right cell.

## When to use storyboard crops

Good enough for:
- title/context slide
- benchmark/chart slide where the shape is visible
- workflow/tunable-knobs slide
- talk-context visuals in a timeline section

Not ideal for:
- tiny text that readers must inspect closely
- detailed charts where exact axis labels matter
- screenshots meant to serve as primary technical evidence

## Editorial rule

Label these as screenshots from the talk/video context, not as crisp source-of-truth figures. Prefer official companion-source images whenever precise technical readability matters more than video context.