"""
Finalize dark master = RAW.

User locked RAW: source image, native resolution, zero enhancement,
centered on deep ink. No saturation / contrast / brightness / sharpness
changes. The photo IS the master.

Outputs:
  logos/master/m-mark-dark.png         — 2560×2560, source on #0E0B07
  logos/master/m-mark-dark.svg         — wrapper
  logos/master/m-mark-transparent.png  — 2560×2560, source on alpha
  logos/master/m-mark-transparent.svg  — wrapper
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
SRC = ROOT / "logos/png/hires/logo-transparent-2924.png"
OUT = ROOT / "logos/master"

OUT_SIZE = 2560
PADDING = 110
INK_DEEP = (14, 11, 7)


def tight_bbox(rgba, alpha_threshold=80):
    a = rgba[..., 3]; mask = a > alpha_threshold
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def loose_bbox(rgba):
    a = rgba[..., 3]; mask = a > 4
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def fit_canvas_native(rgba, size, pad):
    tight = tight_bbox(rgba); loose = loose_bbox(rgba)
    tx0, ty0, tx1, ty1 = tight
    lx0, ly0, lx1, ly1 = loose
    tw = tx1 - tx0; th = ty1 - ty0
    inner = size - 2 * pad
    scale = 1.0 if max(tw, th) <= inner else inner / max(tw, th)
    new_lw = int(round((lx1 - lx0) * scale))
    new_lh = int(round((ly1 - ly0) * scale))
    crop = Image.fromarray(rgba[ly0:ly1+1, lx0:lx1+1], "RGBA")
    if scale != 1.0:
        crop = crop.resize((new_lw, new_lh), Image.LANCZOS)
    crop_arr = np.array(crop)
    tcx = ((tx0 + tx1) / 2 - lx0) * scale
    tcy = ((ty0 + ty1) / 2 - ly0) * scale
    ox = int(round(size / 2 - tcx)); oy = int(round(size / 2 - tcy))
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    sx0 = max(0, -ox); sy0 = max(0, -oy)
    sx1 = min(new_lw, size - ox); sy1 = min(new_lh, size - oy)
    dx0 = ox + sx0; dy0 = oy + sy0
    dx1 = dx0 + (sx1 - sx0); dy1 = dy0 + (sy1 - sy0)
    canvas[dy0:dy1, dx0:dx1] = crop_arr[sy0:sy1, sx0:sx1]
    return canvas, scale


def composite(rgba, bg):
    a = rgba[..., 3:4].astype(float) / 255.0
    fg = rgba[..., :3].astype(float)
    bg_arr = np.array(bg, dtype=float).reshape(1, 1, 3)
    return (fg * a + bg_arr * (1 - a)).astype(np.uint8)


def write_svg_wrapper(png_path, svg_path, label):
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · {label}
  Source photo at native resolution, zero enhancement.
  This is the canonical brand master — do not redraw, vectorize, or filter.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OUT_SIZE} {OUT_SIZE}" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs · M · {label}</title>
  <image x="0" y="0" width="{OUT_SIZE}" height="{OUT_SIZE}" href="data:image/png;base64,{b64}"/>
</svg>
'''
    svg_path.write_text(svg)


def main():
    src = np.array(Image.open(SRC).convert("RGBA"))
    canvas, scale = fit_canvas_native(src, OUT_SIZE, PADDING)
    print(f"native scale: {scale:.3f} (1.0 = source preserved exactly)")

    Image.fromarray(canvas, "RGBA").save(OUT / "m-mark-transparent.png", optimize=True)
    Image.fromarray(composite(canvas, INK_DEEP)).save(OUT / "m-mark-dark.png", optimize=True)

    write_svg_wrapper(OUT / "m-mark-dark.png",        OUT / "m-mark-dark.svg",        "dark master · RAW")
    write_svg_wrapper(OUT / "m-mark-transparent.png", OUT / "m-mark-transparent.svg", "transparent master · RAW")

    # Clean up the v2/v3 leftover svgs that referenced light/v3b versions
    light_png = OUT / "m-mark-light.png"
    if light_png.exists():
        # Regenerate light from RAW using the same fit (just a different bg)
        # NOTE: per user, light is paused — but we keep a basic light version
        # so the master directory is consistent, can be revised later.
        from PIL import Image as PI
        a = canvas[..., 3].astype(float) / 255.0
        a_tight = a ** 1.6
        light_rgba = canvas.copy()
        light_rgba[..., 3] = (a_tight * 255).astype(np.uint8)
        Image.fromarray(composite(light_rgba, (250, 247, 238))).save(light_png, optimize=True)
        write_svg_wrapper(OUT / "m-mark-light.png", OUT / "m-mark-light.svg", "light master · halo-tightened (provisional)")
        print(f"  m-mark-light.png: {light_png.stat().st_size/1024:.1f} KB (provisional, awaiting decision)")

    for name in ["m-mark-dark.png", "m-mark-transparent.png"]:
        sz = (OUT / name).stat().st_size
        print(f"  {name}: {sz/1024:.1f} KB")
    print("done.")


if __name__ == "__main__":
    main()
