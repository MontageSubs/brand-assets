"""
Dark master · v3 — conservative refinement.

User feedback on v2: "过度锐化 + 强行提升对比度" caused distortion.

v3 philosophy: only do things that strictly preserve the photo's natural
look. No contrast push, no brightness push, no aggressive sharpening.
The two things we DO want are:
  1. Native source resolution preserved (no LANCZOS-induced softness from
     resize). Source M is ~2289 px tall in a 2924 frame; we use that scale
     directly and place on a 2560 canvas.
  2. Very gentle edge clarity — Unsharp Mask with very small radius and
     low percent, plus a threshold so flat areas (where ringing would
     show) are untouched.

Render three variants for your inspection:
  RAW  — zero enhancement, just centered + composited (true to source)
  v3a  — +sat 4%, no sharpening
  v3b  — +sat 4% + gentle unsharp (r=0.8 percent=40 threshold=6)

Outputs:
  logos/master/m-mark-dark.png        (= v3b, the picked master)
  preview/zooms/<region>-rawv3a-v3b.png (paired diagnostic crops)
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
SRC = ROOT / "logos/png/hires/logo-transparent-2924.png"
OUT = ROOT / "logos/master"
ZOOM_DIR = ROOT / "preview/zooms-v3"
ZOOM_DIR.mkdir(parents=True, exist_ok=True)

OUT_SIZE = 2560
PADDING = 110            # ~4.3% inset; the M is ~2289 px tall natively
INK_DEEP = (14, 11, 7)


def tight_bbox(rgba: np.ndarray, alpha_threshold: int = 80):
    a = rgba[..., 3]; mask = a > alpha_threshold
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def loose_bbox(rgba: np.ndarray):
    a = rgba[..., 3]; mask = a > 4
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def fit_canvas_native(rgba: np.ndarray, size: int, pad: int) -> np.ndarray:
    """Fit M to canvas at NATIVE source resolution (no resize) when possible."""
    tight = tight_bbox(rgba); loose = loose_bbox(rgba)
    tx0, ty0, tx1, ty1 = tight
    lx0, ly0, lx1, ly1 = loose
    tw = tx1 - tx0; th = ty1 - ty0
    inner = size - 2 * pad

    # If native fits, scale = 1.0 (no resize at all). Otherwise downscale to fit.
    if max(tw, th) <= inner:
        scale = 1.0
    else:
        scale = inner / max(tw, th)

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


def composite(rgba: np.ndarray, bg) -> np.ndarray:
    a = rgba[..., 3:4].astype(float) / 255.0
    fg = rgba[..., :3].astype(float)
    bg_arr = np.array(bg, dtype=float).reshape(1, 1, 3)
    return (fg * a + bg_arr * (1 - a)).astype(np.uint8)


def sat_only(rgba: np.ndarray, factor: float) -> np.ndarray:
    """Saturation adjustment. Nothing else."""
    a = rgba[..., 3:4]
    rgb = Image.fromarray(rgba[..., :3], "RGB")
    rgb = ImageEnhance.Color(rgb).enhance(factor)
    out = np.zeros_like(rgba)
    out[..., :3] = np.array(rgb); out[..., 3:4] = a
    return out


def gentle_unsharp(rgba: np.ndarray, radius: float, percent: int, threshold: int) -> np.ndarray:
    a = rgba[..., 3:4]
    rgb = Image.fromarray(rgba[..., :3], "RGB")
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))
    out = np.zeros_like(rgba)
    out[..., :3] = np.array(rgb); out[..., 3:4] = a
    return out


def write_svg_wrapper(png_path: Path, svg_path: Path, label: str):
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OUT_SIZE} {OUT_SIZE}" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs · M · {label}</title>
  <image x="0" y="0" width="{OUT_SIZE}" height="{OUT_SIZE}" href="data:image/png;base64,{b64}"/>
</svg>
'''
    svg_path.write_text(svg)


# Diagnostic regions (in 2560 canvas coords)
REGIONS = [
    ("01-left-leg-bottom",   (200, 1700, 720, 2220)),
    ("02-left-leg-top",      (210, 240,  730, 760)),
    ("03-V-tip",             (1000, 1450, 1620, 2070)),
    ("04-right-leg-top",     (1750, 660, 2270, 1180)),
    ("05-right-leg-bottom",  (1830, 1900, 2350, 2420)),
    ("06-tube-highlight",    (920, 920, 1720, 1720)),
]


def make_diagnostic_zooms(canvases: dict[str, np.ndarray]):
    for slug, (x0, y0, x1, y1) in REGIONS:
        x0 = max(0, x0); y0 = max(0, y0)
        for variant, canvas in canvases.items():
            x1c = min(canvas.shape[1], x1); y1c = min(canvas.shape[0], y1)
            Image.fromarray(canvas[y0:y1c, x0:x1c]).convert("RGB").save(
                ZOOM_DIR / f"{slug}-{variant}.png", optimize=True)
    # Full frames at 1280 max for the overview
    for variant, canvas in canvases.items():
        img = Image.fromarray(canvas).convert("RGB")
        if max(img.size) > 1280:
            img = img.resize((1280, 1280), Image.LANCZOS)
        img.save(ZOOM_DIR / f"_full-{variant}.png", optimize=True)


def main():
    print("loading source…")
    src = np.array(Image.open(SRC).convert("RGBA"))

    # Variant RAW: no enhancement at all
    raw_canvas, scale = fit_canvas_native(src, OUT_SIZE, PADDING)
    print(f"native scale: {scale:.3f}  (1.0 = no resize)")

    # Variant v3a: +4% sat only
    v3a_src = sat_only(src, 1.04)
    v3a_canvas, _ = fit_canvas_native(v3a_src, OUT_SIZE, PADDING)

    # Variant v3b: +4% sat + gentle unsharp mask
    v3b_src = sat_only(src, 1.04)
    v3b_src = gentle_unsharp(v3b_src, radius=0.8, percent=40, threshold=6)
    v3b_canvas, _ = fit_canvas_native(v3b_src, OUT_SIZE, PADDING)

    # Composite onto deep ink
    raw_dark = composite(raw_canvas, INK_DEEP)
    v3a_dark = composite(v3a_canvas, INK_DEEP)
    v3b_dark = composite(v3b_canvas, INK_DEEP)

    # Save the picked master (v3b — sat+gentle sharp)
    Image.fromarray(v3b_canvas, "RGBA").save(OUT / "m-mark-transparent.png", optimize=True)
    Image.fromarray(v3b_dark).save(OUT / "m-mark-dark.png", optimize=True)
    write_svg_wrapper(OUT / "m-mark-dark.png",        OUT / "m-mark-dark.svg",        "dark master v3b")
    write_svg_wrapper(OUT / "m-mark-transparent.png", OUT / "m-mark-transparent.svg", "transparent master v3b")

    # Diagnostic zooms
    make_diagnostic_zooms({
        "raw": raw_dark,
        "v3a": v3a_dark,
        "v3b": v3b_dark,
    })

    print(f"  m-mark-dark.png: {(OUT/'m-mark-dark.png').stat().st_size/1024:.1f} KB")
    print(f"  zooms: {len(list(ZOOM_DIR.glob('*.png')))} crops")
    print("done.")


if __name__ == "__main__":
    main()
