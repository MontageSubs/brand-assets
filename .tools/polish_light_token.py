"""
Light master · 「黑夜永驻」(dark-token approach).

Concept: the M never changes — it always lives in its dark context. On a
light page, we put the M inside a DARK TOKEN (rounded square / circle /
hard square) which becomes the M's habitat. The token is the night,
floating on the day-page.

This produces three canonical token shapes for different uses:
  · token-rounded   (default app/web/social — Spotify/Threads style)
  · token-circle    (avatar / profile picture)
  · token-square    (hard square — print, signage)

Each token has:
  · deep ink fill (#0E0B07)
  · 1px hairline rim at 8% white (subtle "card" definition on cream)
  · soft warm drop shadow underneath

The dark master M is centered inside, scaled to ~64% of token width so
the M has natural air around it.

Outputs:
  logos/master/m-mark-light.png            (= rounded token, the default)
  logos/master/m-mark-light-rounded.png
  logos/master/m-mark-light-circle.png
  logos/master/m-mark-light-square.png
  + matching .svg wrappers
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
DARK_PNG = ROOT / "logos/master/m-mark-dark.png"      # the locked RAW master
TRANSP_PNG = ROOT / "logos/master/m-mark-transparent.png"
OUT = ROOT / "logos/master"

OUT_SIZE = 2560

# Layout
TOKEN_INSET = 220        # token sits inside this padding from canvas edge
M_SCALE = 0.78           # M occupies this ratio of token width
TOKEN_RADIUS_ROUND = 380 # corner radius for rounded square token
RIM_OPACITY = 0.10       # subtle rim highlight strength

# Colors
INK_DEEP = (14, 11, 7)        # token fill
MIST = (250, 247, 238)        # page bg
RIM = (255, 240, 200)         # rim highlight (warm cream)
SHADOW = (110, 74, 32)        # warm shadow color


def make_token_mask(shape: str, w: int, h: int, radius: int = 0) -> np.ndarray:
    """Build a token alpha mask of the given shape (255 = inside token)."""
    img = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(img)
    if shape == "rounded":
        draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    elif shape == "circle":
        draw.ellipse((0, 0, w, h), fill=255)
    elif shape == "square":
        draw.rectangle((0, 0, w, h), fill=255)
    else:
        raise ValueError(shape)
    return np.array(img)


def render_token(shape: str, m_dark_rgba: np.ndarray, m_dark_dark_rgb: np.ndarray) -> np.ndarray:
    """Render an OUT_SIZE×OUT_SIZE canvas with the token + M centered + drop shadow on cream."""
    H = W = OUT_SIZE
    inner = W - 2 * TOKEN_INSET
    radius = TOKEN_RADIUS_ROUND if shape == "rounded" else 0

    # Token alpha
    tok_mask = make_token_mask(shape, inner, inner, radius)

    # ---- Drop shadow (under token) ----
    # Place token mask in shadow position
    sh_mask = np.zeros((H, W), dtype=np.float32)
    sh_mask[TOKEN_INSET:TOKEN_INSET + inner, TOKEN_INSET:TOKEN_INSET + inner] = tok_mask.astype(np.float32) / 255.0
    sh_mask = np.roll(sh_mask, 28, axis=0)  # shift down
    sh_mask = gaussian_filter(sh_mask, sigma=42)
    sh_mask = (sh_mask * 0.30).clip(0, 1)

    # ---- Token fill ----
    tok_layer_a = np.zeros((H, W), dtype=np.float32)
    tok_layer_a[TOKEN_INSET:TOKEN_INSET + inner, TOKEN_INSET:TOKEN_INSET + inner] = tok_mask.astype(np.float32) / 255.0

    # ---- Compose page = bg + shadow + token + rim ----
    page = np.ones((H, W, 3), dtype=np.float32) * np.array(MIST, dtype=np.float32)
    sh_arr = np.array(SHADOW, dtype=np.float32)
    page = page * (1 - sh_mask[..., None]) + sh_arr[None, None, :] * sh_mask[..., None]

    ink_arr = np.array(INK_DEEP, dtype=np.float32)
    page = page * (1 - tok_layer_a[..., None]) + ink_arr[None, None, :] * tok_layer_a[..., None]

    # Rim highlight: thin ring on the inside top edge of the token
    # Compute the "top edge" by eroding the mask and subtracting
    rim_inner = np.zeros((H, W), dtype=np.float32)
    rim_inner[TOKEN_INSET:TOKEN_INSET + inner, TOKEN_INSET:TOKEN_INSET + inner] = tok_mask.astype(np.float32) / 255.0
    # Erode by gaussian + threshold
    rim_blur = gaussian_filter(rim_inner, sigma=2.5)
    rim_band = (rim_inner - rim_blur).clip(0, 1) * RIM_OPACITY
    # Only show on top half (lit edge)
    yy = np.linspace(0, 1, H)[:, None]
    rim_band = rim_band * np.maximum(0, 1 - 1.6 * yy)
    rim_arr = np.array(RIM, dtype=np.float32)
    page = page * (1 - rim_band[..., None]) + rim_arr[None, None, :] * rim_band[..., None]

    # ---- Place M centered in token ----
    # M is in m_dark_rgba (RGBA), 2560×2560, M occupies the central area.
    # We need to scale it to M_SCALE × inner.
    target_m = int(round(M_SCALE * inner))
    m_pil = Image.fromarray(m_dark_rgba, "RGBA").resize((target_m, target_m), Image.LANCZOS)
    m_arr = np.array(m_pil).astype(np.float32) / 255.0
    m_a = m_arr[..., 3:4]
    m_rgb = m_arr[..., :3] * 255.0

    cx = W // 2; cy = H // 2
    mx0 = cx - target_m // 2; my0 = cy - target_m // 2
    # Composite M onto page (only where token covers, but the M's natural alpha
    # already fades into transparent at edges = M's halo)
    region = page[my0:my0 + target_m, mx0:mx0 + target_m].astype(np.float32)
    composite = region * (1 - m_a) + m_rgb * m_a
    page[my0:my0 + target_m, mx0:mx0 + target_m] = composite

    return page.clip(0, 255).astype(np.uint8)


def write_svg_wrapper(png_path, svg_path, label):
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · {label}
  Light-mode rendering: dark token (the M's natural night habitat) sits
  on a cream page. The M itself is the locked dark master — never altered.
  Use this anywhere the surrounding context is light.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OUT_SIZE} {OUT_SIZE}" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs · M · {label}</title>
  <image x="0" y="0" width="{OUT_SIZE}" height="{OUT_SIZE}" href="data:image/png;base64,{b64}"/>
</svg>
'''
    svg_path.write_text(svg)


def main():
    print("loading dark master + transparent…")
    transp_full = np.array(Image.open(TRANSP_PNG).convert("RGBA"))
    print(f"transparent master: {transp_full.shape}")

    # We need a "tight" version of the M (the M itself, not the 2560 canvas).
    # Crop to the M's tight bbox so we can scale into the token cleanly.
    a = transp_full[..., 3]
    mask = a > 4
    ys, xs = np.where(mask)
    x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
    m_crop = transp_full[y0:y1+1, x0:x1+1]
    # Pad to square so M scales without distortion
    h, w = m_crop.shape[:2]
    side = max(h, w)
    sq = np.zeros((side, side, 4), dtype=np.uint8)
    oy = (side - h) // 2; ox = (side - w) // 2
    sq[oy:oy+h, ox:ox+w] = m_crop
    print(f"M tight square: {sq.shape}")

    # The dark composite isn't actually used — we use the transparent M and let
    # the token color show through.
    for shape in ["rounded", "circle", "square"]:
        print(f"render token: {shape}…")
        canvas = render_token(shape, sq, None)
        Image.fromarray(canvas).save(OUT / f"m-mark-light-{shape}.png", optimize=True)
        write_svg_wrapper(
            OUT / f"m-mark-light-{shape}.png",
            OUT / f"m-mark-light-{shape}.svg",
            f"light master · dark {shape} token",
        )

    # Default light master = rounded
    Image.open(OUT / "m-mark-light-rounded.png").save(OUT / "m-mark-light.png", optimize=True)
    write_svg_wrapper(OUT / "m-mark-light.png", OUT / "m-mark-light.svg",
                      "light master · default (dark rounded token)")

    for name in ["m-mark-light.png", "m-mark-light-rounded.png", "m-mark-light-circle.png", "m-mark-light-square.png"]:
        sz = (OUT / name).stat().st_size
        print(f"  {name}: {sz/1024:.1f} KB")
    print("done.")


if __name__ == "__main__":
    main()
