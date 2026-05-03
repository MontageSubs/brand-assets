"""
Light master · 「关灯版」(lights-off concept).

Concept: same physical M, but the neon is OFF and we see it in daylight.
The glass tube becomes translucent cream; the metal case becomes warm bronze.
The original photo's tonal topology (which way light falls, where shadows
sit, where reflections catch) is PRESERVED — we only re-translate "luma"
into a daytime palette.

Method:
  1. For every pixel, compute its luma (0-255).
  2. Look up a 256-entry LUT: luma → (R, G, B) in the daytime palette.
  3. Preserve the photo's alpha so the M's silhouette and halo stay intact.
  4. Soften the halo with a gamma curve (a daytime M doesn't glow).
  5. Add a soft warm drop shadow underneath, composite on cream #FAF7EE.

This stays faithful to the dark master's geometry, perspective, and
material topology — only the COLOR of each tonal zone changes.
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
SRC = ROOT / "logos/png/hires/logo-transparent-2924.png"
OUT = ROOT / "logos/master"

OUT_SIZE = 2560
PADDING = 110
MIST = (250, 247, 238)        # cream daylight bg


# --- LUT: luma → daytime palette ---
# Reads as "where the photo had X brightness, paint it Y"
# Anchor stops; linearly interpolated between.
LUT_STOPS = [
    (0,   (28, 18, 8)),       # deep case shadow
    (35,  (62, 41, 18)),      # case base shadow
    (75,  (122, 80, 38)),     # case mid
    (115, (170, 116, 60)),    # case lit
    (145, (196, 146, 80)),    # bronze rim → tube transition
    (175, (217, 181, 133)),   # tube glass shadow side
    (200, (237, 220, 190)),   # tube glass body
    (225, (248, 240, 220)),   # tube glass highlight
    (245, (255, 252, 238)),   # specular peak
    (255, (255, 254, 245)),
]


def build_lut() -> np.ndarray:
    """Build a 256×3 LUT from the anchor stops."""
    lut = np.zeros((256, 3), dtype=np.float64)
    stops = LUT_STOPS
    for i in range(len(stops) - 1):
        l0, c0 = stops[i]
        l1, c1 = stops[i + 1]
        for L in range(l0, l1 + 1):
            t = 0 if l1 == l0 else (L - l0) / (l1 - l0)
            for ch in range(3):
                lut[L, ch] = c0[ch] + (c1[ch] - c0[ch]) * t
    return lut.astype(np.uint8)


def remap_to_daylight(rgba: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """Apply LUT to luma channel, keep alpha."""
    rgb = rgba[..., :3].astype(np.float32)
    luma = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]).astype(np.uint8)
    new_rgb = lut[luma]  # (H, W, 3) uint8
    out = np.zeros_like(rgba)
    out[..., :3] = new_rgb
    out[..., 3] = rgba[..., 3]
    return out


def soften_halo(rgba: np.ndarray, gamma: float = 2.4) -> np.ndarray:
    """Daytime M shouldn't glow. Pull halo alpha down sharply with gamma."""
    a = rgba[..., 3].astype(np.float32) / 255.0
    a = np.where(a < 0.94, a ** gamma, a)
    out = rgba.copy()
    out[..., 3] = (a * 255).astype(np.uint8)
    return out


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
    return canvas


def add_drop_shadow(canvas: np.ndarray, bg: tuple[int, int, int],
                    shadow_color: tuple[int, int, int] = (110, 74, 32),
                    sigma: float = 35, dy: int = 22, opacity: float = 0.35) -> np.ndarray:
    """Composite the M onto bg with a soft warm drop shadow underneath."""
    H, W = canvas.shape[:2]
    a = canvas[..., 3].astype(np.float32) / 255.0
    rgb = canvas[..., :3].astype(np.float32)

    # Shadow alpha: blur the M's alpha, offset down by dy
    shadow_a = np.zeros_like(a)
    if dy > 0:
        shadow_a[dy:] = a[:-dy]
    else:
        shadow_a = a.copy()
    shadow_a = gaussian_filter(shadow_a, sigma=sigma)
    shadow_a = (shadow_a * opacity).clip(0, 1)

    # Composite: bg → shadow → M
    bg_arr = np.array(bg, dtype=np.float32).reshape(1, 1, 3)
    sh_arr = np.array(shadow_color, dtype=np.float32).reshape(1, 1, 3)

    # Step 1: shadow over bg
    layer1 = bg_arr * (1 - shadow_a[..., None]) + sh_arr * shadow_a[..., None]
    # Step 2: M over (shadow over bg)
    final = layer1 * (1 - a[..., None]) + rgb * a[..., None]
    return final.astype(np.uint8)


def write_svg_wrapper(png_path, svg_path, label):
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · {label}
  Lights-off rendering: tonal topology of the dark master is preserved,
  but each luma level is remapped to a daytime palette via a 256-entry LUT.
  Glass tube → milky cream; metal case → warm bronze; underneath → soft warm shadow.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OUT_SIZE} {OUT_SIZE}" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs · M · {label}</title>
  <image x="0" y="0" width="{OUT_SIZE}" height="{OUT_SIZE}" href="data:image/png;base64,{b64}"/>
</svg>
'''
    svg_path.write_text(svg)


def main():
    print("loading source…")
    src = np.array(Image.open(SRC).convert("RGBA"))

    print("build LUT…")
    lut = build_lut()

    print("remap luma → daytime palette…")
    daylight = remap_to_daylight(src, lut)

    print("tighten halo (no glow in daylight)…")
    daylight = soften_halo(daylight, gamma=2.4)

    print("fit to canvas…")
    canvas = fit_canvas_native(daylight, OUT_SIZE, PADDING)

    print("composite + drop shadow on cream…")
    light_final = add_drop_shadow(canvas, MIST, shadow_color=(110, 74, 32),
                                   sigma=38, dy=22, opacity=0.32)

    Image.fromarray(canvas, "RGBA").save(OUT / "m-mark-light-transparent.png", optimize=True)
    Image.fromarray(light_final).save(OUT / "m-mark-light.png", optimize=True)
    write_svg_wrapper(OUT / "m-mark-light.png",             OUT / "m-mark-light.svg",             "light master · lights-off")
    write_svg_wrapper(OUT / "m-mark-light-transparent.png", OUT / "m-mark-light-transparent.svg", "light master · lights-off transparent")

    for name in ["m-mark-light.png", "m-mark-light-transparent.png"]:
        sz = (OUT / name).stat().st_size
        print(f"  {name}: {sz/1024:.1f} KB")
    print("done.")


if __name__ == "__main__":
    main()
