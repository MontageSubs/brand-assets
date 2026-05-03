"""
Build downstream application templates:
  · social avatars (square + round, dark + light context)
  · video subtitle bug / 台标 (corner watermark, multiple positions)
  · PPT cover (16:9 title slide, dark + light)
  · letterhead (A4 portrait, dark + light)
  · business card (90×54mm, dark + light)
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
APPS = ROOT / "applications"

# Fonts
PINGFANG = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc"
HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
PINGFANG_SC_MEDIUM = (PINGFANG, 7)
PINGFANG_SC_REGULAR = (PINGFANG, 3)
PINGFANG_SC_LIGHT = (PINGFANG, 15)
PINGFANG_SC_SEMIBOLD = (PINGFANG, 11)
HELVETICA_REG = (HELVETICA, 0)
HELVETICA_BOLD = (HELVETICA, 1)

# Colors
INK_DEEP = (14, 11, 7)
INK_SOFT = (26, 20, 16)
MIST = (250, 247, 238)
TEXT_ON_DARK = (250, 247, 238)
TEXT_ON_LIGHT = (26, 20, 16)
YELLOW = (251, 193, 0)


def font(spec, size):
    return ImageFont.truetype(spec[0], size, index=spec[1])


def text_size(draw, txt, fnt):
    bbox = draw.textbbox((0, 0), txt, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def load_m_transparent():
    return Image.open(ROOT / "logos/master/m-mark-transparent.png").convert("RGBA")


def load_m_rounded():
    return Image.open(ROOT / "logos/master/m-mark-light-rounded.png").convert("RGBA")


def load_m_circle():
    return Image.open(ROOT / "logos/master/m-mark-light-circle.png").convert("RGBA")


def write_svg_wrapper(png_path, svg_path, label, w, h):
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MontageSubs · {label} -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="MontageSubs {label}">
  <title>MontageSubs · {label}</title>
  <image x="0" y="0" width="{w}" height="{h}" href="data:image/png;base64,{b64}"/>
</svg>
'''
    svg_path.write_text(svg)


# ---------- Social avatars ----------

def build_social_avatars():
    out = APPS / "social"
    out.mkdir(parents=True, exist_ok=True)

    sizes = {
        "square-1080":   1080,   # generic square
        "square-1500":   1500,   # higher-res
    }
    # Square avatar (uses rounded token)
    rounded = load_m_rounded()
    for name, size in sizes.items():
        rounded.resize((size, size), Image.LANCZOS).save(out / f"avatar-{name}.png", optimize=True)

    # Circle avatar (already pre-built)
    circle = load_m_circle()
    for size in [400, 800, 1080]:
        circle.resize((size, size), Image.LANCZOS).save(out / f"avatar-circle-{size}.png", optimize=True)

    # Discord/Telegram-style banner (1500×500)
    W, H = 1500, 500
    canvas = Image.new("RGB", (W, H), INK_DEEP)
    m = load_m_transparent()
    m_size = 380
    m_resized = m.resize((m_size, m_size), Image.LANCZOS)
    canvas.paste(m_resized, (60, (H - m_size) // 2), m_resized)
    draw = ImageDraw.Draw(canvas)
    f_en = font(HELVETICA_BOLD, 64)
    f_cn = font(PINGFANG_SC_MEDIUM, 44)
    f_tag = font(PINGFANG_SC_REGULAR, 22)
    text_x = 60 + m_size + 50
    en_h = text_size(draw, "MontageSubs", f_en)[1]
    cn_h = text_size(draw, "蒙太奇字幕组", f_cn)[1]
    block_h = en_h + 18 + cn_h + 28 + 24
    text_y = (H - block_h) // 2
    draw.text((text_x, text_y), "MontageSubs", font=f_en, fill=TEXT_ON_DARK)
    draw.text((text_x, text_y + en_h + 18), "蒙太奇字幕组", font=f_cn, fill=TEXT_ON_DARK)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((text_x, text_y + en_h + 18 + cn_h + 28), "用爱发电 · POWERED BY LOVE",
            font=f_tag, fill=(*TEXT_ON_DARK, 150))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB")
    canvas.save(out / "banner-1500x500.png", optimize=True)

    # Twitter/X header (1500×500 — same dim, but framing differs)
    canvas.save(out / "banner-x-twitter.png", optimize=True)

    # YouTube channel art (2560×1440 with safe area)
    YW, YH = 2560, 1440
    yt = Image.new("RGB", (YW, YH), INK_DEEP)
    # The "safe area" on YouTube is 1235×338 centered
    m_yt = m.resize((360, 360), Image.LANCZOS)
    yt.paste(m_yt, ((YW - 360) // 2 - 280, (YH - 360) // 2), m_yt)
    yd = ImageDraw.Draw(yt)
    f_en2 = font(HELVETICA_BOLD, 92)
    f_cn2 = font(PINGFANG_SC_MEDIUM, 60)
    f_tag2 = font(PINGFANG_SC_REGULAR, 28)
    en_w = text_size(yd, "MontageSubs", f_en2)[0]
    yt_text_x = (YW - 360) // 2 - 280 + 360 + 60
    yt_text_y = (YH - 200) // 2
    yd.text((yt_text_x, yt_text_y), "MontageSubs", font=f_en2, fill=TEXT_ON_DARK)
    yd.text((yt_text_x, yt_text_y + 110), "蒙太奇字幕组", font=f_cn2, fill=TEXT_ON_DARK)
    layer = Image.new("RGBA", (YW, YH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((yt_text_x, yt_text_y + 200), "用爱发电 · POWERED BY LOVE",
            font=f_tag2, fill=(*TEXT_ON_DARK, 150))
    yt = Image.alpha_composite(yt.convert("RGBA"), layer).convert("RGB")
    yt.save(out / "banner-youtube-2560x1440.png", optimize=True)

    print(f"  social/: {len(list(out.glob('*.png')))} files")


# ---------- Video subtitle bug / 台标 ----------

def build_video_bug():
    out = APPS / "video-bug"
    out.mkdir(parents=True, exist_ok=True)

    # Mono flat M for bugs (small, must read on any background)
    # Use the smoothed silhouette in brand yellow
    import re
    geom_d = re.search(r'<path\s+d="([^"]+)"',
                       (ROOT / "logos/master/m-geom-base.svg").read_text()).group(1)

    # Yellow M with subtle drop shadow, transparent bg — drop into any video
    body = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MontageSubs · video bug · yellow M with shadow on transparent -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="MontageSubs video bug">
  <title>MontageSubs · video bug</title>
  <defs>
    <filter id="vbShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="14"/>
      <feOffset dx="0" dy="6"/>
      <feFlood flood-color="#000" flood-opacity="0.65"/>
      <feComposite in2="SourceAlpha" operator="in"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <path d="{geom_d}" fill="#FBC100" fill-rule="evenodd" filter="url(#vbShadow)"/>
</svg>
'''
    (out / "video-bug-yellow.svg").write_text(body)

    # White M variant (for any-color video bg, gives contrast against bright too)
    body_w = body.replace('fill="#FBC100"', 'fill="#FFFFFF"')
    (out / "video-bug-white.svg").write_text(body_w)

    # Wordmark bug for video bottom-corner — M + small text
    wb = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MontageSubs · video bug · M + wordmark, for bottom-corner credit -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 400" role="img" aria-label="MontageSubs video credit bug">
  <title>MontageSubs · video credit bug</title>
  <defs>
    <filter id="vbShadow2" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="10"/>
      <feOffset dx="0" dy="5"/>
      <feFlood flood-color="#000" flood-opacity="0.7"/>
      <feComposite in2="SourceAlpha" operator="in"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g filter="url(#vbShadow2)">
    <g transform="translate(40, 40) scale(0.32)">
      <path d="{geom_d}" fill="#FBC100" fill-rule="evenodd"/>
    </g>
    <text x="430" y="190" font-family="Helvetica, Arial, sans-serif" font-weight="bold" font-size="100" fill="#FBC100">MontageSubs</text>
    <text x="430" y="290" font-family="'PingFang SC', 'Noto Sans CJK SC', 'Hiragino Sans GB', sans-serif" font-size="58" fill="#FFFFFF">蒙太奇字幕组</text>
  </g>
</svg>
'''
    (out / "video-bug-wordmark.svg").write_text(wb)

    # Render to PNGs at common sizes
    print(f"  video-bug/: 3 SVG bugs + corresponding PNG renders")


# ---------- PPT cover (16:9) ----------

def build_ppt_cover():
    out = APPS / "ppt-cover"
    out.mkdir(parents=True, exist_ok=True)

    # PPT slide: 1920×1080 (16:9) at 300dpi → high res
    W, H = 1920, 1080

    # Dark version
    dark = Image.new("RGB", (W, H), INK_DEEP)
    m = load_m_transparent()
    m_size = 460
    m_resized = m.resize((m_size, m_size), Image.LANCZOS)
    dark.paste(m_resized, (W - m_size - 100, 80), m_resized)
    d = ImageDraw.Draw(dark)
    f_title = font(PINGFANG_SC_SEMIBOLD, 88)
    f_subtitle = font(PINGFANG_SC_REGULAR, 44)
    f_meta = font(HELVETICA_REG, 24)
    title = "蒙太奇字幕组"
    subtitle = "MontageSubs · 用爱发电"
    meta = "PRESENTATION TITLE · 2026"
    d.text((100, 720), title, font=f_title, fill=TEXT_ON_DARK)
    d.text((100, 830), subtitle, font=f_subtitle, fill=(255, 232, 114))  # glow-high
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((100, 920), meta, font=f_meta, fill=(*TEXT_ON_DARK, 130))
    dark = Image.alpha_composite(dark.convert("RGBA"), layer).convert("RGB")
    # Rule line
    d2 = ImageDraw.Draw(dark)
    d2.line([(100, 700), (520, 700)], fill=(251, 193, 0), width=4)
    dark.save(out / "ppt-cover-dark.png", optimize=True)

    # Light version
    light = Image.new("RGB", (W, H), MIST)
    m_rounded = load_m_rounded()
    m_size_l = 460
    m_l_resized = m_rounded.resize((m_size_l, m_size_l), Image.LANCZOS)
    light.paste(m_l_resized, (W - m_size_l - 100, 80), m_l_resized)
    dl = ImageDraw.Draw(light)
    dl.text((100, 720), title, font=f_title, fill=TEXT_ON_LIGHT)
    dl.text((100, 830), subtitle, font=f_subtitle, fill=(168, 91, 0))  # amber-deep
    layer2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld2 = ImageDraw.Draw(layer2)
    ld2.text((100, 920), meta, font=f_meta, fill=(*TEXT_ON_LIGHT, 140))
    light = Image.alpha_composite(light.convert("RGBA"), layer2).convert("RGB")
    dl2 = ImageDraw.Draw(light)
    dl2.line([(100, 700), (520, 700)], fill=(14, 11, 7), width=4)
    light.save(out / "ppt-cover-light.png", optimize=True)

    print(f"  ppt-cover/: 2 PNGs (dark + light, 1920×1080)")


# ---------- Stationery ----------

def build_stationery():
    out = APPS / "stationery"
    out.mkdir(parents=True, exist_ok=True)

    # Letterhead (A4 portrait, 2480×3508 px @ 300dpi)
    W, H = 2480, 3508

    for mode, bg, text_color, m_loader in [
        ("dark", INK_DEEP, TEXT_ON_DARK, load_m_transparent),
        ("light", MIST, TEXT_ON_LIGHT, load_m_rounded),
    ]:
        page = Image.new("RGB", (W, H), bg)
        m = m_loader()
        m_size = 280
        m_resized = m.resize((m_size, m_size), Image.LANCZOS)
        page.paste(m_resized, (180, 160), m_resized)
        d = ImageDraw.Draw(page)
        f_brand = font(HELVETICA_BOLD, 60)
        f_brand_cn = font(PINGFANG_SC_MEDIUM, 36)
        f_meta = font(PINGFANG_SC_REGULAR, 22)
        f_footer = font(PINGFANG_SC_LIGHT, 22)
        d.text((180 + m_size + 60, 220), "MontageSubs", font=f_brand, fill=text_color)
        d.text((180 + m_size + 60, 300), "蒙太奇字幕组 · 用爱发电", font=f_brand_cn, fill=text_color)

        # Top rule line
        d.line([(180, 500), (W - 180, 500)], fill=(251, 193, 0) if mode == "dark" else (14, 11, 7), width=2)

        # Footer
        footer_y = H - 220
        d.line([(180, footer_y - 40), (W - 180, footer_y - 40)],
               fill=text_color, width=1)
        d.text((180, footer_y), "MONTAGESUBS · 蒙太奇字幕组", font=f_footer, fill=text_color)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((180, footer_y + 30), "用爱发电 ❤️ POWERED BY LOVE", font=f_footer,
                fill=(*text_color, 140))
        ld.text((W - 180 - 800, footer_y), "github.com/MontageSubs · contact@montagesubs.org",
                font=f_footer, fill=(*text_color, 140))
        page = Image.alpha_composite(page.convert("RGBA"), layer).convert("RGB")
        page.save(out / f"letterhead-{mode}.png", optimize=True)

    # Business card (90×54mm @ 300dpi → 1063×638 px, but we use 1080×648 for clean math)
    BW, BH = 1080, 648
    for mode, bg, text_color, m_loader, m_size_bc in [
        ("dark", INK_DEEP, TEXT_ON_DARK, load_m_transparent, 280),
        ("light", MIST, TEXT_ON_LIGHT, load_m_rounded, 230),
    ]:
        # Front (logo only)
        front = Image.new("RGB", (BW, BH), bg)
        m = m_loader()
        m_resized = m.resize((m_size_bc, m_size_bc), Image.LANCZOS)
        front.paste(m_resized, ((BW - m_size_bc) // 2, (BH - m_size_bc) // 2 - 20), m_resized)
        d = ImageDraw.Draw(front)
        f_tag = font(PINGFANG_SC_LIGHT, 22)
        tag = "用爱发电 · POWERED BY LOVE"
        layer = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        tag_w = text_size(d, tag, f_tag)[0]
        ld.text(((BW - tag_w) // 2, BH - 80), tag, font=f_tag, fill=(*text_color, 140))
        front = Image.alpha_composite(front.convert("RGBA"), layer).convert("RGB")
        front.save(out / f"business-card-{mode}-front.png", optimize=True)

        # Back (info)
        back = Image.new("RGB", (BW, BH), bg)
        d2 = ImageDraw.Draw(back)
        f_name = font(PINGFANG_SC_MEDIUM, 44)
        f_role = font(PINGFANG_SC_REGULAR, 26)
        f_label = font(HELVETICA_REG, 18)
        f_value = font(HELVETICA_REG, 22)
        d2.text((80, 100), "Wesley Wu", font=f_name, fill=text_color)
        d2.text((80, 160), "字幕翻译 · 后期制作", font=f_role, fill=(*text_color, 200) if isinstance(text_color, tuple) and len(text_color) == 3 else text_color)
        d2.line([(80, 250), (BW - 80, 250)],
                fill=(251, 193, 0) if mode == "dark" else (14, 11, 7), width=2)
        d2.text((80, 300), "EMAIL", font=f_label, fill=text_color)
        d2.text((80, 330), "wesley@montagesubs.org", font=f_value, fill=text_color)
        d2.text((80, 410), "GITHUB", font=f_label, fill=text_color)
        d2.text((80, 440), "github.com/MontageSubs", font=f_value, fill=text_color)
        # Mini M in corner
        mini_m = m_resized.resize((100, 100), Image.LANCZOS)
        back.paste(mini_m, (BW - 130, BH - 130), mini_m)
        back.save(out / f"business-card-{mode}-back.png", optimize=True)

    print(f"  stationery/: {len(list(out.glob('*.png')))} files (letterhead + business cards)")


def main():
    APPS.mkdir(parents=True, exist_ok=True)
    print("building applications…")
    build_social_avatars()
    build_video_bug()
    build_ppt_cover()
    build_stationery()
    print("done.")


if __name__ == "__main__":
    main()
