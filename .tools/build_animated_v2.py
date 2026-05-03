"""
Animated logo · v2 — frame-based on the actual photo.

v1 used the simplified vector M (m-geom-base.svg). User: 完全失真.
The M in the animation must be the same photo as everywhere else in
the brand. So we generate the animation by varying the brightness of
the dark master photo across ~36 keyframes, exported as:

  · animated-neon-on.gif   — small, embeddable in markdown / GitHub
  · animated-neon-on.webp  — better quality, smaller than GIF
  · animated-neon-on.apng  — animated PNG, lossless
  · animated-neon-on.html  — CSS keyframes on <img>, plays in any browser
  · animated-neon-on.svg   — SVG with embedded photo + SMIL opacity flicker
                              (renders in browsers that support SMIL)
"""

from __future__ import annotations

import base64
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
SRC = ROOT / "logos/master/m-mark-dark.png"
OUT = ROOT / "applications/animated"
OUT.mkdir(parents=True, exist_ok=True)

INK = (14, 11, 7)


# Flicker keyframe pattern — (time_fraction, brightness_factor)
# Models real cold-cathode tube turning on: dim → quick flickers → settle
KEYFRAMES = [
    (0.00, 0.00),   # off
    (0.06, 0.00),   # delay
    (0.10, 0.04),   # first dim flicker
    (0.13, 0.00),
    (0.18, 0.07),   # second flicker
    (0.20, 0.02),
    (0.26, 0.35),   # bigger flicker
    (0.30, 0.10),
    (0.36, 0.55),
    (0.40, 0.18),
    (0.46, 0.78),
    (0.50, 0.40),
    (0.56, 0.92),
    (0.60, 0.55),
    (0.66, 1.00),   # stabilizing
    (0.70, 0.78),
    (0.76, 1.00),
    (0.80, 0.92),
    (0.86, 1.00),
    (1.00, 1.00),   # held
]


def make_frame(rgb_arr: np.ndarray, brightness: float, bg=INK) -> np.ndarray:
    """Multiply RGB by brightness factor, then blend with bg toward black where dim.
    brightness=0 → solid bg, brightness=1 → full photo."""
    bg_arr = np.array(bg, dtype=np.float32).reshape(1, 1, 3)
    out = bg_arr + (rgb_arr.astype(np.float32) - bg_arr) * brightness
    return out.clip(0, 255).astype(np.uint8)


def main():
    print("loading dark master…")
    img = Image.open(SRC).convert("RGB")
    # Downsize for animation (keep size reasonable for GIF/WebP)
    anim_size = 720
    img_small = img.resize((anim_size, anim_size), Image.LANCZOS)
    rgb = np.array(img_small)
    print(f"animation size: {anim_size}×{anim_size}")

    # Generate frames at fixed FPS
    duration = 2.5
    fps = 24
    n_frames = int(duration * fps)
    print(f"generating {n_frames} frames @ {fps}fps over {duration}s…")

    frames = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        # Interpolate brightness from KEYFRAMES
        b = interp(t, KEYFRAMES)
        frames.append(Image.fromarray(make_frame(rgb, b)))
    # Hold the last frame for 12 frames
    for _ in range(12):
        frames.append(frames[-1].copy())

    # ---- Save as animated GIF ----
    print("writing GIF…")
    frames[0].save(
        OUT / "animated-neon-on.gif",
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),  # ms per frame
        loop=0,                    # forever
        optimize=True,
    )
    print(f"  animated-neon-on.gif: {(OUT/'animated-neon-on.gif').stat().st_size/1024:.1f} KB")

    # ---- Save as animated WebP ----
    print("writing WebP…")
    frames[0].save(
        OUT / "animated-neon-on.webp",
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        quality=85,
        method=6,
    )
    print(f"  animated-neon-on.webp: {(OUT/'animated-neon-on.webp').stat().st_size/1024:.1f} KB")

    # ---- Save as APNG (animated PNG, lossless) ----
    print("writing APNG…")
    frames[0].save(
        OUT / "animated-neon-on.apng",
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
    )
    print(f"  animated-neon-on.apng: {(OUT/'animated-neon-on.apng').stat().st_size/1024:.1f} KB")

    # ---- Save as HTML (CSS keyframes on <img>) ----
    photo_b64 = base64.b64encode((SRC).read_bytes()).decode("ascii")
    # NOTE: CSS @keyframes rules are separated by whitespace, NOT commas.
    # Commas only join multiple selectors that share a rule body.
    keyframes_css = "\n          ".join(
        f"{t*100:.0f}% {{ filter: brightness({b:.3f}); }}" for t, b in KEYFRAMES
    )
    html = f'''<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<title>MontageSubs · animated · neon on</title>
<style>
  html, body {{ margin: 0; padding: 0; background: #0E0B07; height: 100%; }}
  body {{ display: grid; place-items: center; }}
  .stage {{ width: min(80vw, 80vh); aspect-ratio: 1; }}
  .stage img {{ width: 100%; height: 100%; object-fit: contain;
                 filter: brightness(0);
                 animation: neonOn 2.5s cubic-bezier(0.4, 0, 0.6, 1) forwards; }}
  .controls {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
               display: flex; gap: 12px; }}
  .controls button {{ padding: 8px 16px; background: rgba(250,247,238,0.1);
                       color: #FAF7EE; border: 1px solid rgba(250,247,238,0.2);
                       border-radius: 4px; font: 12px sans-serif; cursor: pointer;
                       letter-spacing: 1px; text-transform: uppercase; }}
  .controls button:hover {{ background: rgba(250,247,238,0.18); }}
  @keyframes neonOn {{
    {keyframes_css}
  }}
</style>
</head>
<body>
<div class="stage" id="stage">
  <img id="m" src="data:image/png;base64,{photo_b64}" alt="MontageSubs">
</div>
<div class="controls">
  <button onclick="replay()">▶ Replay</button>
</div>
<script>
function replay() {{
  const img = document.getElementById('m');
  img.style.animation = 'none';
  void img.offsetWidth; // force reflow
  img.style.animation = '';
}}
</script>
</body>
</html>
'''
    (OUT / "animated-neon-on.html").write_text(html)
    print(f"  animated-neon-on.html: {(OUT/'animated-neon-on.html').stat().st_size/1024:.1f} KB")

    # ---- Save as SVG (embedded photo + SMIL animation on opacity of bright copy) ----
    # Two stacked images: bg-color rect + the photo, photo opacity animated.
    # We use opacity (which works in SMIL) instead of brightness (which doesn't).
    # bg shows through when opacity is low — same visual result.
    smil_values = ";".join(f"{b:.2f}" for _, b in KEYFRAMES)
    smil_keytimes = ";".join(f"{t:.2f}" for t, _ in KEYFRAMES)
    svg_b64 = base64.b64encode((SRC).read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · animated logo · neon turn-on (~2.5s)
  Embedded photo + SMIL flicker on opacity. Plays once per page load.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"
     role="img" aria-label="MontageSubs M, neon turning on">
  <title>MontageSubs · animated · neon on</title>
  <rect width="1024" height="1024" fill="#0E0B07"/>
  <image x="0" y="0" width="1024" height="1024"
         href="data:image/png;base64,{svg_b64}"
         opacity="0">
    <animate attributeName="opacity"
             values="{smil_values}"
             keyTimes="{smil_keytimes}"
             dur="2.5s"
             fill="freeze"/>
  </image>
</svg>
'''
    (OUT / "animated-neon-on.svg").write_text(svg)
    print(f"  animated-neon-on.svg: {(OUT/'animated-neon-on.svg').stat().st_size/1024:.1f} KB")

    print("done.")


def interp(t: float, keyframes) -> float:
    """Linearly interpolate brightness given time t in [0,1]."""
    if t <= keyframes[0][0]:
        return keyframes[0][1]
    if t >= keyframes[-1][0]:
        return keyframes[-1][1]
    for i in range(len(keyframes) - 1):
        t0, b0 = keyframes[i]
        t1, b1 = keyframes[i + 1]
        if t0 <= t <= t1:
            u = (t - t0) / (t1 - t0)
            return b0 + (b1 - b0) * u
    return keyframes[-1][1]


if __name__ == "__main__":
    main()
