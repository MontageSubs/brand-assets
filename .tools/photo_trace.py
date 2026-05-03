"""
Photo-faithful vector trace of the original neon M.

Posterizes the source RGBA photo into N tonal layers by luminance threshold,
then traces each layer's mask boundary as a smooth polygon. Stacking the
polygons recreates the photo's depth (case → body → highlight → hot core)
in a fully scalable, ~50-150 KB SVG that no longer exhibits trace jitter.

Layers (lowest brightness first, drawn back to front):
  halo  → case-deep → case → body-shadow → body → body-lit → highlight → core

Each layer's mask is the set of pixels >= that layer's threshold. Drawing
brighter colors on top of dimmer ones produces a natural tonal gradient.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image
from skimage import measure
from scipy.ndimage import gaussian_filter, binary_closing


ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
SRC = ROOT / "logos/png/hires/logo-transparent-2924.png"
GEOM_OUT = ROOT / "logos/master/m-trace-faithful.svg"
PREVIEW_OUT = ROOT / "preview/04-trace-faithful.svg"


# Tonal layers: (luma_threshold, fill_color, label)
# Drawn from back to front; mask = (luma >= threshold) so each subsequent
# layer is a SUBSET of the prior, creating a natural onion-skin glow.
LAYERS = [
    # threshold, color hex, label
    (   8, "#1A0E03", "halo-out"),    # outermost: just barely lit pixels
    (  35, "#3A1B00", "case-deep"),   # outer case shadow
    (  72, "#6E3500", "case"),        # case mid
    ( 105, "#965000", "case-lit"),    # case lit edge
    ( 135, "#C57600", "body-shadow"), # tube body shadow side
    ( 168, "#F09800", "body"),        # tube body main amber
    ( 198, "#FBC100", "body-lit"),    # tube body lit side (★ brand yellow)
    ( 220, "#FDD846", "highlight"),   # tube highlight stripe
    ( 238, "#FFEC8E", "core"),        # hot core
    ( 248, "#FFFCE0", "spec"),        # specular peak (very small)
]

# Output viewBox: 1024x1024, M centered with ~10% padding
TARGET = 1024
PAD = 96


def find_bbox(alpha: np.ndarray) -> tuple[int, int, int, int]:
    """Tight bbox of non-transparent pixels."""
    on = alpha > 8
    ys, xs = np.where(on)
    return xs.min(), ys.min(), xs.max(), ys.max()


def normalize_contour(contour: np.ndarray, src_bbox: tuple[int, int, int, int]) -> np.ndarray:
    """Map raw image-space (row, col) to SVG-space (x, y) at 1024×1024 with PAD."""
    x0, y0, x1, y1 = src_bbox
    w = x1 - x0
    h = y1 - y0
    target_inner = TARGET - 2 * PAD
    scale = target_inner / max(w, h)
    cx_off = (TARGET - w * scale) / 2
    cy_off = (TARGET - h * scale) / 2
    out = np.zeros_like(contour, dtype=float)
    out[:, 0] = (contour[:, 1] - x0) * scale + cx_off  # col → x
    out[:, 1] = (contour[:, 0] - y0) * scale + cy_off  # row → y
    return out


def rdp(arr: np.ndarray, eps: float) -> np.ndarray:
    """Iterative Ramer-Douglas-Peucker for one polyline."""
    n = len(arr)
    if n < 3:
        return arr
    keep = np.zeros(n, dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        a, b = arr[i], arr[j]
        ab = b - a
        L = np.hypot(*ab)
        seg = arr[i:j+1]
        if L < 1e-9:
            d = np.hypot(seg[:, 0] - a[0], seg[:, 1] - a[1])
        else:
            d = np.abs(ab[0] * (a[1] - seg[:, 1]) - (a[0] - seg[:, 0]) * ab[1]) / L
        k = int(np.argmax(d))
        if d[k] > eps:
            keep[i + k] = True
            stack.append((i, i + k))
            stack.append((i + k, j))
    return arr[keep]


def emit_smooth_path(arr: np.ndarray, tension: float = 0.42) -> str:
    """Catmull-Rom → cubic bezier path."""
    n = len(arr)
    parts = [f"M{arr[0,0]:.1f},{arr[0,1]:.1f}"]
    for i in range(n):
        p0 = arr[(i - 1) % n]
        p1 = arr[i % n]
        p2 = arr[(i + 1) % n]
        p3 = arr[(i + 2) % n]
        c1x = p1[0] + (p2[0] - p0[0]) * tension / 3.0
        c1y = p1[1] + (p2[1] - p0[1]) * tension / 3.0
        c2x = p2[0] - (p3[0] - p1[0]) * tension / 3.0
        c2y = p2[1] - (p3[1] - p1[1]) * tension / 3.0
        parts.append(f"C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    parts.append("Z")
    return "".join(parts)


def trace_layer(luma: np.ndarray, alpha_mask: np.ndarray, threshold: int,
                src_bbox: tuple[int, int, int, int],
                blur_sigma: float = 1.5,
                close_size: int = 3,
                rdp_eps: float = 0.55,
                min_area: int = 80) -> list[str]:
    """Return list of path-d strings for the contours of (luma >= threshold)."""
    blurred = gaussian_filter(luma * alpha_mask, sigma=blur_sigma)
    mask = blurred >= threshold
    if close_size > 0:
        mask = binary_closing(mask, iterations=close_size)
    if not mask.any():
        return []

    # find_contours returns sub-pixel boundaries (using marching squares).
    contours = measure.find_contours(mask.astype(float), 0.5)
    paths = []
    for c in contours:
        if len(c) < 6:
            continue
        # filter tiny noise blobs
        # crude area via shoelace
        x = c[:, 1]; y = c[:, 0]
        area = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
        if area < min_area:
            continue
        # normalize to viewBox
        norm = normalize_contour(c, src_bbox)
        # simplify
        simp = rdp(norm, eps=rdp_eps)
        if len(simp) < 4:
            continue
        paths.append(emit_smooth_path(simp))
    return paths


def main():
    img = Image.open(SRC).convert("RGBA")
    arr = np.array(img)
    rgb = arr[..., :3].astype(float)
    alpha = arr[..., 3]

    # Luma in non-transparent area
    luma = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    alpha_mask = (alpha > 8).astype(float)
    bbox = find_bbox(alpha)

    # Crop to bbox + small margin to speed up processing
    margin = 30
    x0 = max(0, bbox[0] - margin); y0 = max(0, bbox[1] - margin)
    x1 = min(arr.shape[1], bbox[2] + margin); y1 = min(arr.shape[0], bbox[3] + margin)
    luma_c = luma[y0:y1, x0:x1]
    alpha_c = alpha_mask[y0:y1, x0:x1]
    new_bbox = (bbox[0] - x0, bbox[1] - y0, bbox[2] - x0, bbox[3] - y0)

    # Build layers
    layer_svg = []
    total_paths = 0
    for thr, col, label in LAYERS:
        paths = trace_layer(luma_c, alpha_c, threshold=thr, src_bbox=new_bbox,
                            blur_sigma=1.8, close_size=2, rdp_eps=0.45, min_area=60)
        total_paths += len(paths)
        if not paths:
            continue
        # Combine all sub-contours into one path (using fill-rule="evenodd"
        # so any holes naturally cancel out).
        combined = " ".join(paths)
        layer_svg.append(
            f'  <!-- L:{label} threshold={thr} ({len(paths)} contours) -->\n'
            f'  <path d="{combined}" fill="{col}" fill-rule="evenodd"/>'
        )
    print(f"layers emitted: {len(layer_svg)} / {len(LAYERS)} · total contours: {total_paths}")

    body = "\n".join(layer_svg)

    # Self-contained SVG
    geom = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · M · photo-faithful vector trace.
  Multi-layer reconstruction of the original Unsplash photo:
  posterized into {len(LAYERS)} tonal levels, each level traced as a smooth
  polygon via marching squares + RDP simplification + Catmull-Rom bezier.
  Stacking layers reproduces the case → body → highlight → core depth.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TARGET} {TARGET}" role="img" aria-label="MontageSubs M, photo-faithful trace">
  <title>MontageSubs · M · faithful</title>
{body}
</svg>
'''
    GEOM_OUT.write_text(geom)
    print(f"wrote {GEOM_OUT.relative_to(ROOT)} ({len(geom):,} bytes)")

    # Preview: place trace next to original photo for fidelity check
    # (use same bbox normalization; original at half scale + label)
    side = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2080 1120" role="img">
  <rect width="2080" height="1120" fill="#0E0B07"/>
  <text x="512" y="40" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="20" fill="#FAF7EE" opacity="0.7">ORIGINAL · UNSPLASH PHOTO</text>
  <text x="1568" y="40" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="20" fill="#FAF7EE" opacity="0.7">NEW · PHOTO-FAITHFUL TRACE</text>
  <image x="0"    y="56" width="1024" height="1024" href="../logos/png/hires/logo-transparent-2924.png" preserveAspectRatio="xMidYMid meet"/>
  <g transform="translate(1056,56)">
{body}
  </g>
</svg>
'''
    PREVIEW_OUT.write_text(side)
    print(f"wrote {PREVIEW_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
