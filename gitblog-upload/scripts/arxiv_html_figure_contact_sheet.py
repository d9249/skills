#!/usr/bin/env python3
"""Download arXiv HTML figures and build a contact sheet for blog visual selection.

Usage:
  python scripts/arxiv_html_figure_contact_sheet.py 2604.12374 /tmp/arxiv_2604_12374/figures
  python scripts/arxiv_html_figure_contact_sheet.py 2604.12374v1 /tmp/arxiv_2604_12374/figures

The script uses only stdlib + Pillow. It fetches https://arxiv.org/html/<id>/,
resolves image URLs against the versioned HTML URL, downloads unique PNG/JPG/WebP
assets, writes figure_quality.json, and writes contact.jpg with filenames printed
under each thumbnail.
"""
from __future__ import annotations

import html.parser
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SAMPLE_MAX_SIDE = 96
DARK_WIDE_WARNING = "dark_dominant_wide_figure"


class ImgParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag.lower() != "img":
            return
        d = dict(attrs)
        src = d.get("src") or d.get("data-src")
        if src:
            self.srcs.append(src)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Hermes gitblog visual selection"},
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def resolve_img_url(html_url: str, src: str) -> str:
    """Resolve arXiv HTML image paths without duplicating versioned prefixes.

    arXiv HTML commonly emits relative paths like ``2604.27077v2/x1.png``.
    Joining those against ``https://arxiv.org/html/2604.27077v2/`` produces the
    bogus ``.../2604.27077v2/2604.27077v2/x1.png``. When the relative path
    already starts with an arXiv id/version directory, resolve it from the
    ``/html/`` root instead.
    """
    src = src.strip()
    if not src:
        return src
    parsed = urllib.parse.urlparse(src)
    if parsed.scheme or src.startswith("//"):
        return urllib.parse.urljoin(html_url, src)
    clean = src.lstrip("./")
    first = clean.split("/", 1)[0]
    if re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", first):
        return urllib.parse.urljoin("https://arxiv.org/html/", clean)
    return urllib.parse.urljoin(html_url, src)


def flatten_on_white(image: Image.Image) -> Image.Image:
    has_alpha = image.mode in ("RGBA", "LA")
    has_palette_alpha = image.mode == "P" and "transparency" in image.info
    if has_alpha or has_palette_alpha:
        rgba = image.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        background.alpha_composite(rgba)
        return background.convert("RGB")
    return image.convert("RGB")


def measure_image(path: Path) -> dict[str, object]:
    with Image.open(path) as image:
        width, height = image.size
        rgb = flatten_on_white(image)

    scale = min(1, SAMPLE_MAX_SIDE / max(width, height))
    sample_width = max(1, round(width * scale))
    sample_height = max(1, round(height * scale))
    sample = rgb.resize((sample_width, sample_height), Image.Resampling.BOX)

    total = 0
    dark_pixels = 0
    black_pixels = 0
    light_pixels = 0
    luma_sum = 0.0

    for red, green, blue in sample.getdata():
        luma = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        total += 1
        luma_sum += luma
        if luma < 45:
            dark_pixels += 1
        if luma < 22:
            black_pixels += 1
        if luma > 210:
            light_pixels += 1

    average_luma = luma_sum / total if total else 0
    dark_ratio = dark_pixels / total if total else 0
    black_ratio = black_pixels / total if total else 0
    light_ratio = light_pixels / total if total else 0
    aspect_ratio = width / height if height else 0

    warnings: list[str] = []
    if (
        aspect_ratio >= 2.0
        and average_luma < 80
        and dark_ratio > 0.65
        and black_ratio > 0.45
        and light_ratio < 0.15
    ):
        warnings.append(DARK_WIDE_WARNING)

    return {
        "filename": path.name,
        "width": width,
        "height": height,
        "aspect_ratio": round(aspect_ratio, 3),
        "average_luma": round(average_luma, 2),
        "dark_ratio": round(dark_ratio, 3),
        "black_ratio": round(black_ratio, 3),
        "light_ratio": round(light_ratio, 3),
        "warnings": warnings,
    }


def quality_summary(quality: dict[str, object]) -> str:
    return (
        f"size={quality['width']}x{quality['height']} "
        f"avg_luma={quality['average_luma']} "
        f"dark={quality['dark_ratio']} "
        f"black={quality['black_ratio']} "
        f"light={quality['light_ratio']}"
    )


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "Usage: arxiv_html_figure_contact_sheet.py <arxiv-id-or-version> <out-dir>",
            file=sys.stderr,
        )
        return 2
    arxiv_id = sys.argv[1]
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    html_url = f"https://arxiv.org/html/{arxiv_id}/"
    body = fetch(html_url).decode("utf-8", "replace")
    parser = ImgParser()
    parser.feed(body)

    urls: list[str] = []
    for src in parser.srcs:
        url = resolve_img_url(html_url, src)
        path = urllib.parse.urlparse(url).path.lower()
        if not path.endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue
        if url not in urls:
            urls.append(url)

    downloaded: list[Path] = []
    qualities: list[dict[str, object]] = []
    for index, url in enumerate(urls, 1):
        name = urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name)
        path = out_dir / f"{index:02d}-{name}"
        try:
            path.write_bytes(fetch(url))
            Image.open(path).verify()
            quality = measure_image(path)
            quality["url"] = url
            quality["bytes"] = path.stat().st_size
            qualities.append(quality)
            downloaded.append(path)
            warning_text = ",".join(quality["warnings"])
            warning_suffix = f" WARN={warning_text}" if warning_text else ""
            print(
                f"OK {path.name} {path.stat().st_size} {url} "
                f"{quality_summary(quality)}{warning_suffix}",
            )
        except Exception as error:
            print(f"SKIP {url}: {error}", file=sys.stderr)
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    if qualities:
        quality_report = out_dir / "figure_quality.json"
        quality_report.write_text(
            json.dumps(qualities, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        warning_count = sum(1 for quality in qualities if quality["warnings"])
        print(f"QUALITY {quality_report} images={len(qualities)} warnings={warning_count}")

    thumbs: list[Image.Image] = []
    for path in downloaded:
        image = flatten_on_white(Image.open(path))
        image.thumbnail((520, 340), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (560, 410), "white")
        canvas.paste(image, ((560 - image.width) // 2, 20))
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([0, 370, 560, 410], fill=(245, 245, 245))
        draw.text((10, 378), path.name[:72], fill=(0, 0, 0), font=ImageFont.load_default())
        thumbs.append(canvas)

    if thumbs:
        cols = 2
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 560, rows * 410), (230, 230, 230))
        for index, thumb in enumerate(thumbs):
            sheet.paste(thumb, ((index % cols) * 560, (index // cols) * 410))
        contact = out_dir / "contact.jpg"
        sheet.save(contact, quality=90)
        print(f"CONTACT {contact} {sheet.size} images={len(thumbs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
