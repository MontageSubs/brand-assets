"""
Build wordmark lockups: M mark + 蒙太奇字幕组 / MontageSubs.

Variants:
  · horizontal-dark   M (photo) + text on the right, deep ink bg
  · horizontal-light  M (in dark token) + text on the right, cream bg
  · stacked-dark      M (photo) + text below, deep ink bg
  · stacked-light     M (in dark token) + text below, cream bg

Typography:
  · CN: PingFang SC Medium (canonical, fallback: Noto Sans CJK SC, Hiragino, Microsoft YaHei)
  · EN: Helvetica Bold (canonical, fallback: SF Pro Display, Inter, system-ui)

Output: PNG @ high res + SVG wrapper (PNG embedded as base64).
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
OUT = ROOT / "logos/lockup"
OUT.mkdir(parents=True, exist_ok=True)

# ---- Fonts ----
PINGFANG = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc"
HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
PINGFANG_SC_MEDIUM = (PINGFANG, 7)
PINGFANG_SC_REGULAR = (PINGFANG, 3)
HELVETICA_BOLD = (HELVETICA, 1)

# ---- Colors ----
INK_DEEP = (14, 11, 7)
MIST = (250, 247, 238)
TEXT_ON_DARK = (250, 247, 238)
TEXT_ON_LIGHT = (26, 20, 16)
TEXT_DIM_ON_DARK = (250, 247, 238, 160)   # subtitle/tagline alpha
TEXT_DIM_ON_LIGHT = (26, 20, 16, 160)


def font(spec: tuple[str, int], size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(spec[0], size, index=spec[1])


def text_size(draw: ImageDraw.ImageDraw, txt: str, fnt) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), txt, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def load_m_for_dark() -> Image.Image:
    """Photo M with full halo, ready to drop on dark bg."""
    return Image.open(ROOT / "logos/master/m-mark-transparent.png").convert("RGBA")


def load_m_for_light() -> Image.Image:
    """M in dark rounded token, ready to drop on light bg."""
    return Image.open(ROOT / "logos/master/m-mark-light-rounded.png").convert("RGBA")


def composite_image_at(canvas: Image.Image, img: Image.Image, x: int, y: int):
    """Alpha-compose a transparent or pre-baked image onto canvas at (x, y)."""
    canvas.paste(img, (x, y), img if img.mode == "RGBA" else None)


def build_horizontal(mode: str, m_img: Image.Image, bg: tuple[int, int, int],
                     text_color: tuple[int, int, int]) -> Image.Image:
    """Horizontal lockup. Canvas 2400×800. M on left (square), text on right (left-aligned)."""
    W, H = 2400, 800
    canvas = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(canvas)

    # M occupies left ~750 px, vertically centered
    m_size = 700
    m_resized = m_img.resize((m_size, m_size), Image.LANCZOS)
    m_x = 60
    m_y = (H - m_size) // 2
    composite_image_at(canvas, m_resized, m_x, m_y)

    # Text block on the right
    text_x = m_x + m_size + 80
    f_en = font(HELVETICA_BOLD, 116)
    f_cn = font(PINGFANG_SC_MEDIUM, 80)
    f_tag = font(PINGFANG_SC_REGULAR, 38)

    # Lines:
    en = "MontageSubs"
    cn = "蒙太奇字幕组"
    tag = "用爱发电 · POWERED BY LOVE"

    en_w, en_h = text_size(draw, en, f_en)
    cn_w, cn_h = text_size(draw, cn, f_cn)
    tag_w, tag_h = text_size(draw, tag, f_tag)

    line_gap_main = 28
    line_gap_tag = 38
    block_h = en_h + line_gap_main + cn_h + line_gap_tag + tag_h
    text_y = (H - block_h) // 2 - 20

    draw.text((text_x, text_y), en, font=f_en, fill=text_color)
    draw.text((text_x, text_y + en_h + line_gap_main), cn, font=f_cn, fill=text_color)

    # Tagline at slightly dim opacity
    tag_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tag_draw = ImageDraw.Draw(tag_layer)
    tag_draw.text((text_x, text_y + en_h + line_gap_main + cn_h + line_gap_tag),
                  tag, font=f_tag,
                  fill=(*text_color, 160))
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), tag_layer).convert("RGB"))

    return canvas


def build_stacked(mode: str, m_img: Image.Image, bg: tuple[int, int, int],
                  text_color: tuple[int, int, int]) -> Image.Image:
    """Stacked lockup. Canvas 1600×2000. M on top, centered text below."""
    W, H = 1600, 2000
    canvas = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(canvas)

    # M at top, centered, ~1100 px
    m_size = 1100
    m_resized = m_img.resize((m_size, m_size), Image.LANCZOS)
    m_x = (W - m_size) // 2
    m_y = 100
    composite_image_at(canvas, m_resized, m_x, m_y)

    # Text below
    f_en = font(HELVETICA_BOLD, 130)
    f_cn = font(PINGFANG_SC_MEDIUM, 88)
    f_tag = font(PINGFANG_SC_REGULAR, 42)

    en = "MontageSubs"
    cn = "蒙太奇字幕组"
    tag = "用爱发电 · POWERED BY LOVE"

    en_w, en_h = text_size(draw, en, f_en)
    cn_w, cn_h = text_size(draw, cn, f_cn)
    tag_w, tag_h = text_size(draw, tag, f_tag)

    text_y_start = m_y + m_size + 60
    draw.text(((W - en_w) // 2, text_y_start), en, font=f_en, fill=text_color)
    draw.text(((W - cn_w) // 2, text_y_start + en_h + 30), cn, font=f_cn, fill=text_color)

    tag_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tag_draw = ImageDraw.Draw(tag_layer)
    tag_draw.text(((W - tag_w) // 2, text_y_start + en_h + 30 + cn_h + 50),
                  tag, font=f_tag,
                  fill=(*text_color, 160))
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), tag_layer).convert("RGB"))

    return canvas


def write_svg_wrapper(png_path: Path, svg_path: Path, label: str, w: int, h: int):
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MontageSubs · lockup · {label} -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="MontageSubs lockup, {label}">
  <title>MontageSubs · lockup · {label}</title>
  <image x="0" y="0" width="{w}" height="{h}" href="data:image/png;base64,{b64}"/>
</svg>
'''
    svg_path.write_text(svg)


def main():
    print("loading M images…")
    m_for_dark = load_m_for_dark()
    m_for_light = load_m_for_light()

    print("building lockups…")

    h_dark = build_horizontal("dark", m_for_dark, INK_DEEP, TEXT_ON_DARK)
    h_dark.save(OUT / "lockup-horizontal-dark.png", optimize=True)
    write_svg_wrapper(OUT / "lockup-horizontal-dark.png", OUT / "lockup-horizontal-dark.svg",
                      "horizontal · dark", 2400, 800)

    h_light = build_horizontal("light", m_for_light, MIST, TEXT_ON_LIGHT)
    h_light.save(OUT / "lockup-horizontal-light.png", optimize=True)
    write_svg_wrapper(OUT / "lockup-horizontal-light.png", OUT / "lockup-horizontal-light.svg",
                      "horizontal · light", 2400, 800)

    s_dark = build_stacked("dark", m_for_dark, INK_DEEP, TEXT_ON_DARK)
    s_dark.save(OUT / "lockup-stacked-dark.png", optimize=True)
    write_svg_wrapper(OUT / "lockup-stacked-dark.png", OUT / "lockup-stacked-dark.svg",
                      "stacked · dark", 1600, 2000)

    s_light = build_stacked("light", m_for_light, MIST, TEXT_ON_LIGHT)
    s_light.save(OUT / "lockup-stacked-light.png", optimize=True)
    write_svg_wrapper(OUT / "lockup-stacked-light.png", OUT / "lockup-stacked-light.svg",
                      "stacked · light", 1600, 2000)

    for name in ["lockup-horizontal-dark", "lockup-horizontal-light", "lockup-stacked-dark", "lockup-stacked-light"]:
        sz = (OUT / f"{name}.png").stat().st_size
        print(f"  {name}.png: {sz/1024:.1f} KB")
    print("done.")


if __name__ == "__main__":
    main()
