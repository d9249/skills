# YouTube Embed, Timeline, and Screenshot Patterns

## Canonical embed block

Use the embed URL, not the watch URL.

```html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin: 1.5rem 0;">
  <iframe
    src="https://www.youtube.com/embed/VIDEO_ID"
    title="Video: TITLE"
    loading="lazy"
    referrerpolicy="strict-origin-when-cross-origin"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen
    style="position: absolute; inset: 0; width: 100%; height: 100%; border: 0;"
  ></iframe>
</div>
```

## Timeline extraction pattern

Build a compact working table before drafting:

| Start | End | Segment label | What is shown | What is said/claimed | Companion source | Screenshot? |
|---|---|---|---|---|---|---|
| 00:00 | 02:10 | Intro thesis | opening slide | why this matters now | description/project page | no |
| 02:10 | 06:40 | Benchmark section | chart/slide | latency vs accuracy claim | official benchmark page | yes |

If official chapters are absent, infer boundaries from transcript topic shifts and visible scene changes.

## Screenshot selection rules

Pick 2-5 distinct frames max unless the video truly needs more.

Good screenshot targets:
- benchmark chart fully visible
- architecture diagram slide
- UI state before/after an operation
- qualitative result grid
- workflow overview frame

Avoid:
- host talking-head closeups unless the speaker identity itself matters
- decorative title cards that add no technical information
- multiple frames from the same unchanged slide

## Local extraction commands

1. Confirm a working downloader path.

```bash
command -v yt-dlp
```

2. Download a practical MP4 copy when allowed.

```bash
YT_DLP_BIN="$(command -v yt-dlp)"
"$YT_DLP_BIN" -f mp4 -o /tmp/gitblog-mvupload-%(id)s.%(ext)s "https://youtu.be/VIDEO_ID"
```

3. Extract a specific frame.

```bash
ffmpeg -ss 00:06:24 -i /tmp/gitblog-mvupload-VIDEO_ID.mp4 -frames:v 1 -q:v 2 /tmp/gitblog-mvupload-VIDEO_ID-0624.jpg
```

4. Extract several candidate frames in one pass.

```bash
for ts in 00:02:10 00:06:24 00:11:48; do
  clean="${ts//:/-}"
  ffmpeg -ss "$ts" -i /tmp/gitblog-mvupload-VIDEO_ID.mp4 -frames:v 1 -q:v 2 "/tmp/gitblog-mvupload-VIDEO_ID-${clean}.jpg"
done
```

## Fallbacks when download/frame extraction fails

Use this fallback order:
1. official companion-source images
2. browser-visible screenshots if tooling works reliably
3. YouTube thumbnail only as a header/cover signal

Do not claim a screenshot came from the video body if it was really an official project image.
