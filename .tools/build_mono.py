"""Build all mono flat M variants from the smoothed geometry path.

The mono family is for: embroidery, single-color print, laser etching,
small mono UI marks, video corner watermark. Geometry comes from the
smoothed M (m-geom-base.svg, ~4.5KB path); colors and backgrounds vary.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
GEOM = ROOT / "logos/master/m-geom-base.svg"
OUT = ROOT / "logos/mono"
OUT.mkdir(parents=True, exist_ok=True)


# Brand color tokens (canonical)
T = {
    "ink_deep":  "#0E0B07",
    "ink_soft":  "#1A1410",
    "mist":      "#FAF7EE",
    "yellow":    "#FBC100",   # ★ primary brand yellow
    "white":     "#FFFFFF",
    "black":     "#000000",
}


def get_path() -> str:
    txt = GEOM.read_text()
    m = re.search(r'<path\s+d="([^"]+)"', txt)
    return m.group(1)


D = get_path()


def write(name: str, body: str):
    p = OUT / name
    p.write_text(body)
    print(f"  {name}")


def emit(name: str, fill: str, bg: str | None, label: str):
    bg_rect = f'<rect width="1024" height="1024" fill="{bg}"/>\n  ' if bg else ""
    body = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MontageSubs · M · mono · {label} -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs · M · {label}</title>
  {bg_rect}<path d="{D}" fill="{fill}" fill-rule="evenodd"/>
</svg>
'''
    write(name, body)


def emit_knockout(name: str, tile_color: str, label: str):
    """Yellow tile with M cut out as transparent (mask out)."""
    body = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MontageSubs · M · mono knockout · {label} -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs · M · {label}</title>
  <defs>
    <mask id="cut">
      <rect width="1024" height="1024" fill="white"/>
      <path d="{D}" fill="black" fill-rule="evenodd"/>
    </mask>
  </defs>
  <rect width="1024" height="1024" fill="{tile_color}" mask="url(#cut)"/>
</svg>
'''
    write(name, body)


def main():
    print("writing mono variants…")
    # Solid color on transparent (the M itself, ready to drop into any context)
    emit("m-mono-black.svg",     T["ink_soft"],  None,             "ink on transparent")
    emit("m-mono-white.svg",     T["white"],     None,             "white on transparent")
    emit("m-mono-yellow.svg",    T["yellow"],    None,             "brand yellow on transparent")
    emit("m-mono-true-black.svg", T["black"],    None,             "true black on transparent (print/embroidery)")

    # Pre-composed on bg (drop-in tiles)
    emit("m-mono-yellow-on-ink.svg",  T["yellow"],   T["ink_deep"], "brand yellow on deep ink tile")
    emit("m-mono-ink-on-mist.svg",    T["ink_soft"], T["mist"],     "ink on warm mist tile")
    emit("m-mono-white-on-ink.svg",   T["white"],    T["ink_deep"], "white on deep ink tile")
    emit("m-mono-black-on-mist.svg",  T["black"],    T["mist"],     "true black on mist tile")

    # Knockout (yellow tile, M cut out)
    emit_knockout("m-mono-knockout-yellow.svg", T["yellow"], "yellow tile · M knockout")
    emit_knockout("m-mono-knockout-ink.svg",    T["ink_deep"], "ink tile · M knockout")

    print(f"done · {len(list(OUT.glob('*.svg')))} variants in logos/mono/")


if __name__ == "__main__":
    main()
