# Video visual retrofit audit

Use this when older YouTube-derived posts need to be corrected after the image-selection policy changes.

## What to audit first
- posts containing a YouTube embed or watch URL
- posts whose only inline visuals are repo/docs/product-page screenshots
- posts where companion-source visuals appear before any video-native frame
- posts with exploratory screenshot assets still lying around but not referenced

## Retrofit workflow
1. Search the blog tree for `youtube.com/embed/`, `youtu.be/`, or watch URLs.
2. For each matched post, inspect inline image references.
3. Classify each post:
   - already good: video-native frames present and useful
   - mixed but acceptable: video-native + companion visuals both present
   - needs correction: only companion-source visuals or companion visuals dominate despite usable video frames
4. Reuse existing transcript and metadata artifacts if available before re-fetching.
5. Try direct video download first; if blocked (for example HTTP 403), use storyboard fallback from `yt-dlp --dump-single-json`.
6. Extract several timestamped candidates tied to the article timeline, then keep only the most legible ones.
7. Replace primary companion-source figures with video-native frames when technically possible and still informative.
8. Delete or trash superseded companion-source assets and unused frame candidates before staging.
9. Rebuild and commit only the touched posts and intentional media changes.

## Decision rule
- The goal is not "never use companion visuals."
- The goal is: a YouTube-derived post should usually show at least one or more frames from the source video when those frames are available and useful.
- Companion visuals remain valid as context, but they should not silently become the article's only evidence layer.

## Common failure mode
A workshop/tutorial video often links a clean repo or docs page. Those pages are tempting because they look sharper than storyboard crops. The mistake is to let that convenience erase the fact that the article is supposed to analyze the video itself. Use the repo/docs page as support, not as the unexamined default.