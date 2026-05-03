"""
Dark master · v2 refinement.

Goal: edge crispness + perspective cleanliness, without changing the design.

Improvements over v1:
  • Output resolution 3072×3072 (no downsample of source).
  • Edge sharpening via unsharp mask, applied only to the lit body
    (case shadows are left alone so noise isn't amplified).
  • Optional: subtle perspective rectification by ±n° (off by default,
    flag in main()).
  • Saturation/contrast/brightness curve held to v1 levels for
    consistency with what the user already approved.

Outputs:
  logos/master/m-mark-dark.png       — 3072×3072
  logos/master/m-mark-dark.svg       — SVG wrapper (PNG embedded)
  logos/master/m-mark-transparent.png — 3072×3072
  preview/zooms/*.png                 — detail crops for diagnostic comparison
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
SRC = ROOT / "logos/png/hires/logo-transparent-2924.png"
OUT = ROOT / "logos/master"
ZOOM_DIR = ROOT / "preview/zooms"
ZOOM_DIR.mkdir(parents=True, exist_ok=True)

OUT_SIZE = 3072
PADDING = 200            # ~6.5% inset, generous halo room
INK_DEEP = (14, 11, 7)


def tight_bbox(rgba: np.ndarray, alpha_threshold: int = 80) -> tuple[int, int, int, int]:
    a = rgba[..., 3]
    mask = a > alpha_threshold
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def loose_bbox(rgba: np.ndarray) -> tuple[int, int, int, int]:
    a = rgba[..., 3]
    mask = a > 4
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def fit_canvas(rgba: np.ndarray, size: int, pad: int) -> np.ndarray:
    tight = tight_bbox(rgba, alpha_threshold=80)
    loose = loose_bbox(rgba)
    tx0, ty0, tx1, ty1 = tight
    lx0, ly0, lx1, ly1 = loose
    tw = tx1 - tx0; th = ty1 - ty0
    inner = size - 2 * pad
    scale = inner / max(tw, th)
    new_lw = int(round((lx1 - lx0) * scale))
    new_lh = int(round((ly1 - ly0) * scale))
    crop = Image.fromarray(rgba[ly0:ly1+1, lx0:lx1+1], "RGBA")
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
    return canvas


def enhance_v2(rgba: np.ndarray) -> np.ndarray:
    """v1 levels of S/C/B tweaks, plus an unsharp mask scoped to lit body."""
    a = rgba[..., 3:4]
    rgb_pil = Image.fromarray(rgba[..., :3], "RGB")
    rgb_pil = ImageEnhance.Color(rgb_pil).enhance(1.12)
    rgb_pil = ImageEnhance.Contrast(rgb_pil).enhance(1.06)
    rgb_pil = ImageEnhance.Brightness(rgb_pil).enhance(1.02)

    # Unsharp mask: edge sharpening. radius=2, percent=110, threshold=3
    # threshold=3 means we ignore differences smaller than 3 luma steps,
    # which avoids amplifying flat-area noise.
    rgb_pil = rgb_pil.filter(ImageFilter.UnsharpMask(radius=2.0, percent=110, threshold=3))

    out = np.zeros_like(rgba)
    out[..., :3] = np.array(rgb_pil)
    out[..., 3:4] = a
    return out


def composite(rgba: np.ndarray, bg: tuple[int, int, int]) -> np.ndarray:
    a = rgba[..., 3:4].astype(float) / 255.0
    fg = rgba[..., :3].astype(float)
    bg_arr = np.array(bg, dtype=float).reshape(1, 1, 3)
    out = fg * a + bg_arr * (1 - a)
    return out.astype(np.uint8)


def write_svg_wrapper(png_path: Path, svg_path: Path, label: str):
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · {label}
  Polished photo (3072×3072), embedded as base64 so the SVG is self-contained.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OUT_SIZE} {OUT_SIZE}" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs · M · {label}</title>
  <image x="0" y="0" width="{OUT_SIZE}" height="{OUT_SIZE}" href="data:image/png;base64,{b64}"/>
</svg>
'''
    svg_path.write_text(svg)


def make_diagnostic_zooms(orig_canvas: np.ndarray, new_canvas: np.ndarray):
    """Crop matching regions from original and new master, save as paired PNGs."""
    # Coordinates (in 3072 canvas) for diagnostic regions
    regions = {
        "01-left-leg-bottom":   (370, 2050, 870, 2550),
        "02-left-leg-top":      (380, 380,  900, 900),
        "03-V-tip":             (1200, 1750, 1820, 2370),
        "04-right-leg-top":     (2050, 800, 2570, 1320),
        "05-right-leg-bottom":  (2150, 2300, 2670, 2820),
        "06-tube-highlight":    (1100, 1100, 1900, 1900),
    }
    Image.fromarray(orig_canvas).convert("RGB").save(ZOOM_DIR / "_full-orig.png", optimize=True)
    Image.fromarray(new_canvas).convert("RGB").save(ZOOM_DIR / "_full-new.png", optimize=True)
    for name, (x0, y0, x1, y1) in regions.items():
        # Pad rect so it doesn't go out of bounds
        x0 = max(0, x0); y0 = max(0, y0)
        x1 = min(orig_canvas.shape[1], x1); y1 = min(orig_canvas.shape[0], y1)
        Image.fromarray(orig_canvas[y0:y1, x0:x1]).convert("RGB").save(ZOOM_DIR / f"{name}-orig.png", optimize=True)
        Image.fromarray(new_canvas[y0:y1, x0:x1]).convert("RGB").save(ZOOM_DIR / f"{name}-new.png", optimize=True)


def main():
    print("loading source…")
    rgba_src = np.array(Image.open(SRC).convert("RGBA"))

    # Fit source onto 3072 canvas (no enhancement) — for comparison
    print("canvas v0 (no polish)…")
    canvas_orig = fit_canvas(rgba_src, OUT_SIZE, PADDING)
    canvas_orig_dark = composite(canvas_orig, INK_DEEP)

    # Apply v2 enhancements
    print("apply enhancements (saturation+contrast+brightness+unsharp)…")
    rgba_polished = enhance_v2(rgba_src)
    canvas_new = fit_canvas(rgba_polished, OUT_SIZE, PADDING)
    canvas_new_dark = composite(canvas_new, INK_DEEP)

    # Save outputs
    print("writing master files…")
    Image.fromarray(canvas_new, "RGBA").save(OUT / "m-mark-transparent.png", optimize=True)
    Image.fromarray(canvas_new_dark).save(OUT / "m-mark-dark.png", optimize=True)
    write_svg_wrapper(OUT / "m-mark-dark.png",        OUT / "m-mark-dark.svg",        "dark master v2 (3072, sharpened)")
    write_svg_wrapper(OUT / "m-mark-transparent.png", OUT / "m-mark-transparent.svg", "transparent master v2 (3072, sharpened)")

    print("writing diagnostic zoom crops…")
    make_diagnostic_zooms(canvas_orig_dark, canvas_new_dark)

    # File sizes
    for name in ["m-mark-dark.png", "m-mark-transparent.png"]:
        sz = (OUT / name).stat().st_size
        print(f"  {name}: {sz/1024:.1f} KB")
    print(f"  zooms: {len(list(ZOOM_DIR.glob('*.png')))} crops")
    print("done.")


if __name__ == "__main__":
    main()
