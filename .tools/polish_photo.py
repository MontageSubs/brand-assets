"""
Polish the original neon-M photograph into clean master PNGs.

The photo IS the brand. Stop trying to vectorize it. This script does
minimal, conservative refinement:
  - Tight bbox of the lit M (ignoring soft halo) for canvas centering
  - Saturation boost +12% so the amber sings
  - Contrast boost +6% so the case shadows separate from the body
  - Composite onto chosen background
  - Preserve the photo's existing alpha halo (don't fabricate new one)

Outputs:
  logos/master/m-mark-transparent.png  — neon M, alpha bg, 2048×2048
  logos/master/m-mark-dark.png         — composited on #0E0B07
  logos/master/m-mark-light.png        — composited on #FAF7EE
  logos/master/m-mark-{dark,light,transparent}.svg  — SVG wrappers
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance


ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
SRC = ROOT / "logos/png/hires/logo-transparent-2924.png"
OUT = ROOT / "logos/master"

OUT_SIZE = 2048
PADDING = 130  # tight inset (~6.3%); the M's natural halo provides air

INK_DEEP = (14, 11, 7)      # #0E0B07
MIST = (250, 247, 238)      # #FAF7EE


def tight_bbox(rgba: np.ndarray, alpha_threshold: int = 60) -> tuple[int, int, int, int]:
    """Bounding box ignoring soft halo (use only highly-opaque pixels for tight crop)."""
    a = rgba[..., 3]
    mask = a > alpha_threshold
    if not mask.any():
        mask = a > 8
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def loose_bbox(rgba: np.ndarray) -> tuple[int, int, int, int]:
    """Bbox including the soft halo (so we don't crop the glow during resize)."""
    a = rgba[..., 3]
    mask = a > 4
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def enhance(rgba: np.ndarray) -> np.ndarray:
    """Saturation + contrast lift on the RGB channels only (alpha untouched)."""
    a = rgba[..., 3:4]
    rgb = Image.fromarray(rgba[..., :3], "RGB")
    rgb = ImageEnhance.Color(rgb).enhance(1.12)       # +12% saturation
    rgb = ImageEnhance.Contrast(rgb).enhance(1.06)    # +6% contrast
    rgb = ImageEnhance.Brightness(rgb).enhance(1.02)  # +2% brightness on lit areas
    out = np.zeros_like(rgba)
    out[..., :3] = np.array(rgb)
    out[..., 3:4] = a
    return out


def fit_canvas(rgba: np.ndarray, size: int, pad: int) -> np.ndarray:
    """Center the M inside a square canvas. Use TIGHT bbox for centering
    (so the visible M sits in the optical center) but include the LOOSE
    bbox in the resampled crop (so the halo isn't cut off)."""
    tight = tight_bbox(rgba, alpha_threshold=60)
    loose = loose_bbox(rgba)
    tx0, ty0, tx1, ty1 = tight
    lx0, ly0, lx1, ly1 = loose
    tw = tx1 - tx0; th = ty1 - ty0

    inner = size - 2 * pad
    scale = inner / max(tw, th)

    # Resample the LOOSE crop at the same scale so halo extends beyond inner area
    new_lw = int(round((lx1 - lx0) * scale))
    new_lh = int(round((ly1 - ly0) * scale))
    crop = Image.fromarray(rgba[ly0:ly1+1, lx0:lx1+1], "RGBA")
    crop = crop.resize((new_lw, new_lh), Image.LANCZOS)
    crop_arr = np.array(crop)

    # Position so the TIGHT bbox center aligns with canvas center
    tight_cx = ((tx0 + tx1) / 2 - lx0) * scale
    tight_cy = ((ty0 + ty1) / 2 - ly0) * scale
    ox = int(round(size / 2 - tight_cx))
    oy = int(round(size / 2 - tight_cy))

    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    # Compute paste region with clipping
    sx0 = max(0, -ox); sy0 = max(0, -oy)
    sx1 = min(new_lw, size - ox); sy1 = min(new_lh, size - oy)
    dx0 = ox + sx0; dy0 = oy + sy0
    dx1 = dx0 + (sx1 - sx0); dy1 = dy0 + (sy1 - sy0)
    canvas[dy0:dy1, dx0:dx1] = crop_arr[sy0:sy1, sx0:sx1]
    return canvas


def composite(rgba: np.ndarray, bg: tuple[int, int, int]) -> np.ndarray:
    a = rgba[..., 3:4].astype(float) / 255.0
    fg = rgba[..., :3].astype(float)
    bg_arr = np.array(bg, dtype=float).reshape(1, 1, 3)
    out = fg * a + bg_arr * (1 - a)
    rgba_out = np.zeros((*rgba.shape[:2], 3), dtype=np.uint8)
    rgba_out[...] = out.astype(np.uint8)
    return rgba_out


def soften_halo(rgba: np.ndarray, gamma: float = 1.7) -> np.ndarray:
    """For light bg: tighten the soft halo (which would muddy the cream surface)."""
    a = rgba[..., 3].astype(float) / 255.0
    halo_zone = a < 0.92
    a = np.where(halo_zone, a ** gamma, a)
    out = rgba.copy()
    out[..., 3] = (a * 255).astype(np.uint8)
    return out


def write_svg_wrapper(png_path: Path, svg_path: Path, label: str):
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    mime = "image/png"
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · {label}
  PNG embedded as base64. The photo is the brand: do NOT replace this
  raster with a vector trace, the trace loses tonal continuity and reads
  as poster art. Use this SVG wherever you want one self-contained file.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OUT_SIZE} {OUT_SIZE}" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs · M · {label}</title>
  <image x="0" y="0" width="{OUT_SIZE}" height="{OUT_SIZE}" href="data:{mime};base64,{b64}"/>
</svg>
'''
    svg_path.write_text(svg)
    print(f"wrote {svg_path.relative_to(ROOT)} ({len(svg):,} bytes)")


def main():
    print("loading source…")
    rgba = np.array(Image.open(SRC).convert("RGBA"))
    print(f"src: {rgba.shape}")

    print("enhance…")
    rgba = enhance(rgba)

    print("fit canvas (transparent master)…")
    transparent = fit_canvas(rgba, OUT_SIZE, PADDING)
    Image.fromarray(transparent, "RGBA").save(OUT / "m-mark-transparent.png", optimize=True)

    print("compose dark master…")
    dark = composite(transparent, INK_DEEP)
    Image.fromarray(dark).save(OUT / "m-mark-dark.png", optimize=True)

    print("compose light master (halo softened for cream bg)…")
    light_rgba = soften_halo(transparent.copy(), gamma=1.6)
    light = composite(light_rgba, MIST)
    Image.fromarray(light).save(OUT / "m-mark-light.png", optimize=True)

    print("svg wrappers…")
    write_svg_wrapper(OUT / "m-mark-dark.png",        OUT / "m-mark-dark.svg",        "dark master (polished photo)")
    write_svg_wrapper(OUT / "m-mark-light.png",       OUT / "m-mark-light.svg",       "light master (cream)")
    write_svg_wrapper(OUT / "m-mark-transparent.png", OUT / "m-mark-transparent.svg", "transparent master")

    # File sizes
    for name in ["m-mark-dark.png", "m-mark-light.png", "m-mark-transparent.png"]:
        sz = (OUT / name).stat().st_size
        print(f"  {name}: {sz/1024:.1f} KB")

    print("done.")


if __name__ == "__main__":
    main()
