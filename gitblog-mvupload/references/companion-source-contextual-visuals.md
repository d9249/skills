# Companion-source contextual visuals

Use this when a YouTube post needs images and the best video-native screenshots are blurry, redundant, or less informative than linked official artifacts. Companion-source visuals should usually supplement video-native evidence, not replace it by default.

## Good candidates
- GitHub repo homepage showing repo name, stars, file tree, README title, and setup framing
- Docs landing page with architecture diagram, workflow, or quickstart
- Official project/product page with clear artifact naming and scope
- Benchmark/result page when the chart is sharper than the video frame

## Strong fit cases
- workshop videos
- tutorial videos
- research explainers with linked code/docs
- launch videos whose real evidence lives in repo/docs/release notes

## What to capture
- visible artifact identity: repo/project/model name
- one layer of credibility/context: stars, version, release label, official branding, section title
- one layer of explanatory value: README overview, diagram, config table, workflow block, benchmark chart

## Why this helps
Companion-source visuals do two jobs at once:
1. they ground the article against the official artifact
2. they stay readable at article width when storyboard or frame-grab images do not

## Minimal workflow
1. inspect outbound links from the YouTube description
2. open the most relevant repo/docs/product page
3. check whether you already have at least one useful video-native visual for the article
4. only prefer the companion page as a primary visual if the video-native options are not article-legible or clearly explain less
5. capture a clean, readable screenshot
5. save it under `static/images/blog/`
6. use a caption that explains why the companion page matters to the article

## Caption pattern
- "이 워크숍의 companion repo는 <what it exposes>를 문서와 코드 구조로 직접 대응시킨다."
- "공식 docs 페이지는 <artifact>의 구조를 영상보다 더 선명하게 보여준다."

## Pitfalls
- do not capture generic homepages that say little beyond branding
- do not use repo screenshots if the README section in view is irrelevant to the article
- do not prefer a companion-source image when a high-resolution chart/slide from the video itself is clearly better
