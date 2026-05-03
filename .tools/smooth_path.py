"""
Smooth the trace-artifacted outline-black M path.

Strategy:
  1. Sample the existing cubic-bezier path into a dense polygon.
  2. Apply Gaussian smoothing along the polygon boundary (preserves overall shape,
     removes high-frequency trace jitter).
  3. Apply Ramer-Douglas-Peucker simplification at a low tolerance to remove
     redundant points.
  4. Re-emit as a clean cubic-bezier path with Catmull-Rom-derived control points
     (smooth first-derivative continuity).

Output is written to logos/master/m-geom-base.svg with viewBox 0 0 1024 1024.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np


SRC = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main/legacy/svg/logo-outline-black.svg")
DST = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main/logos/master/m-geom-base.svg")
DEBUG_DST = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main/preview/02-smoothed.svg")


def parse_path(d: str) -> list[tuple[float, float]]:
    """Parse SVG path 'd' that uses M/L/C (and lowercase) and return densely
    sampled (x, y) points."""
    tokens = re.findall(r"[MLCmlcZz]|-?\d+\.?\d*(?:[eE][-+]?\d+)?", d)
    pts: list[tuple[float, float]] = []
    cur = (0.0, 0.0)
    start = (0.0, 0.0)
    i = 0
    cmd = None
    while i < len(tokens):
        t = tokens[i]
        if t in "MLCmlcZz":
            cmd = t
            i += 1
            if t in "Zz":
                cur = start
                continue
        if cmd in ("M", "m"):
            x = float(tokens[i]); y = float(tokens[i+1]); i += 2
            if cmd == "m" and pts:
                x += cur[0]; y += cur[1]
            cur = (x, y); start = cur
            pts.append(cur)
            cmd = "L" if cmd == "M" else "l"
        elif cmd in ("L", "l"):
            x = float(tokens[i]); y = float(tokens[i+1]); i += 2
            if cmd == "l":
                x += cur[0]; y += cur[1]
            pts.append((x, y))
            cur = (x, y)
        elif cmd in ("C", "c"):
            x1 = float(tokens[i]); y1 = float(tokens[i+1])
            x2 = float(tokens[i+2]); y2 = float(tokens[i+3])
            x = float(tokens[i+4]); y = float(tokens[i+5])
            i += 6
            if cmd == "c":
                x1 += cur[0]; y1 += cur[1]
                x2 += cur[0]; y2 += cur[1]
                x  += cur[0]; y  += cur[1]
            # sample bezier at 8 steps
            p0 = cur
            for s in range(1, 9):
                u = s / 8.0
                bx = (1-u)**3*p0[0] + 3*(1-u)**2*u*x1 + 3*(1-u)*u*u*x2 + u*u*u*x
                by = (1-u)**3*p0[1] + 3*(1-u)**2*u*y1 + 3*(1-u)*u*u*y2 + u*u*u*y
                pts.append((bx, by))
            cur = (x, y)
        else:
            i += 1
    return pts


def apply_transform(pts: list[tuple[float, float]]) -> np.ndarray:
    """outline-black uses transform='translate(0,2924) scale(0.1,-0.1)'.
    Bake that in so coordinates land in viewBox space (501..2457, 490..2446)."""
    arr = np.array(pts, dtype=float)
    arr[:, 0] = arr[:, 0] * 0.1
    arr[:, 1] = 2924.0 + arr[:, 1] * -0.1
    return arr


def normalize_to_1024(arr: np.ndarray) -> np.ndarray:
    """Re-frame so the M sits centered in a 1024x1024 viewBox with ~10% padding."""
    minx, miny = arr.min(axis=0)
    maxx, maxy = arr.max(axis=0)
    w = maxx - minx
    h = maxy - miny
    pad = 96.0  # ~9.4% padding in 1024
    target = 1024.0 - 2 * pad
    scale = target / max(w, h)
    out = arr.copy()
    out[:, 0] = (arr[:, 0] - minx) * scale + (1024.0 - w * scale) / 2
    out[:, 1] = (arr[:, 1] - miny) * scale + (1024.0 - h * scale) / 2
    return out


def gaussian_smooth_closed(arr: np.ndarray, sigma: float) -> np.ndarray:
    """Smooth a closed polygon with a Gaussian kernel along arc length."""
    n = len(arr)
    radius = int(math.ceil(3 * sigma))
    if radius < 1:
        return arr
    kernel = np.exp(-(np.arange(-radius, radius + 1) ** 2) / (2 * sigma * sigma))
    kernel /= kernel.sum()
    pad = radius
    padded = np.concatenate([arr[-pad:], arr, arr[:pad]], axis=0)
    sx = np.convolve(padded[:, 0], kernel, mode="valid")
    sy = np.convolve(padded[:, 1], kernel, mode="valid")
    return np.column_stack([sx, sy])


def rdp(arr: np.ndarray, eps: float) -> np.ndarray:
    """Iterative Ramer-Douglas-Peucker for a closed polyline."""
    n = len(arr)
    keep = np.zeros(n, dtype=bool)
    keep[0] = True
    keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        seg = arr[i:j + 1]
        a = arr[i]; b = arr[j]
        ab = b - a
        L = np.hypot(*ab)
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


def emit_smooth_path(arr: np.ndarray, tension: float = 0.5) -> str:
    """Emit a cubic-bezier path through the points using Catmull-Rom -> Bezier.
    `tension` ~0.5 produces gentle curvature continuity at every node;
    use 0 for straight lines (would skip beziers)."""
    n = len(arr)
    parts = [f"M{arr[0,0]:.2f},{arr[0,1]:.2f}"]
    for i in range(n):
        p0 = arr[(i - 1) % n]
        p1 = arr[i % n]
        p2 = arr[(i + 1) % n]
        p3 = arr[(i + 2) % n]
        c1x = p1[0] + (p2[0] - p0[0]) * tension / 3.0
        c1y = p1[1] + (p2[1] - p0[1]) * tension / 3.0
        c2x = p2[0] - (p3[0] - p1[0]) * tension / 3.0
        c2y = p2[1] - (p3[1] - p1[1]) * tension / 3.0
        parts.append(f"C{c1x:.2f},{c1y:.2f} {c2x:.2f},{c2y:.2f} {p2[0]:.2f},{p2[1]:.2f}")
    parts.append("Z")
    return " ".join(parts)


def main():
    txt = SRC.read_text()
    m = re.search(r'<path[^>]*\bd="([^"]+)"', txt, re.DOTALL)
    d = m.group(1)
    raw = parse_path(d)
    arr = apply_transform(raw)
    arr = normalize_to_1024(arr)

    # Two-stage smooth: small sigma first (kill jitter), then RDP, then re-smooth lightly.
    s1 = gaussian_smooth_closed(arr, sigma=4.0)
    s2 = rdp(s1, eps=0.6)
    s3 = gaussian_smooth_closed(s2, sigma=1.2)

    print(f"raw points: {len(arr)}  after smooth+rdp: {len(s2)}  final: {len(s3)}")

    path_d = emit_smooth_path(s3, tension=0.42)
    print(f"path d length: {len(path_d)} chars")

    geom_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · M geometry base
  Smoothed from logos/svg/logo-outline-black.svg.
  Trace artifacts removed via Gaussian + RDP + Catmull-Rom rebuild.
  Preserves DNA: tilt, perspective, asymmetric stroke widths, beveled terminals.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="MontageSubs M">
  <title>MontageSubs M geometry</title>
  <path d="{path_d}" fill="#1A1410" fill-rule="evenodd"/>
</svg>
'''
    DST.write_text(geom_svg)
    print(f"wrote {DST}")

    # Also write a side-by-side preview SVG: original (dim red) + smoothed (black)
    # to verify DNA is preserved.
    raw_arr = apply_transform(parse_path(d))
    raw_norm = normalize_to_1024(raw_arr)
    raw_d = "M" + " L".join(f"{p[0]:.1f},{p[1]:.1f}" for p in raw_norm) + " Z"

    side = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2080 1080" role="img">
  <title>Trace vs Smoothed comparison</title>
  <rect width="2080" height="1080" fill="#FAF7EE"/>
  <g transform="translate(20,28)">
    <text x="512" y="0" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="22" fill="#1A1410">Original (trace, jagged edges)</text>
    <g transform="translate(0,40) scale(1.0)">
      <path d="{raw_d}" fill="#1A1410"/>
    </g>
  </g>
  <g transform="translate(1040,28)">
    <text x="512" y="0" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="22" fill="#1A1410">Smoothed ({len(s3)} nodes, clean bezier)</text>
    <g transform="translate(0,40) scale(1.0)">
      <path d="{path_d}" fill="#1A1410"/>
    </g>
  </g>
</svg>
'''
    DEBUG_DST.write_text(side)
    print(f"wrote {DEBUG_DST}")


if __name__ == "__main__":
    main()
