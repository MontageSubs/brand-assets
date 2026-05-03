"""
Generate every master logo SVG from the smoothed M path.

Reads m-geom-base.svg → extracts the smoothed path data → wraps it with
distinct visual treatments (neon dark, neon light, flat black, flat white,
flat yellow, knockout) and writes them to logos/master/.

Run: python3 .tools/build_masters.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
GEOM = ROOT / "logos/master/m-geom-base.svg"
OUT = ROOT / "logos/master"


# ---------- Brand color tokens ----------
TOKENS = {
    # Surfaces
    "ink_deep":     "#0E0B07",   # dark mode background
    "ink_soft":     "#1A1410",   # mono fill on light
    "mist":         "#FAF7EE",   # light mode background (warm off-white)
    "mist_alt":     "#F2EDDC",   # secondary warm tint
    # Brand yellow stack (the "neon")
    "core_white":   "#FFFCE0",   # hot tube core
    "glow_high":    "#FFE872",   # bright outer glow
    "yellow_lit":   "#FDD338",   # lit body
    "yellow":       "#FBC100",   # primary brand yellow
    "amber":        "#FCAB02",   # mid amber
    "amber_deep":   "#A85B00",   # shadow side of tube
    "amber_dark":   "#7A3D00",   # tube case base
    "amber_black":  "#3D1800",   # case shadow
    # Neutrals
    "white":        "#FFFFFF",
    "ink":          "#000000",
}


def read_geom_path() -> str:
    txt = GEOM.read_text()
    m = re.search(r'<path\s+d="([^"]+)"', txt)
    return m.group(1)


D = read_geom_path()


def write(name: str, content: str):
    p = OUT / name
    p.write_text(content)
    print(f"wrote {p.relative_to(ROOT)}")


# ---------- Master: dark mode neon ----------
# Strategy: layered halo (far + near, both restrained) + bright body with
# diagonal lighting gradient + thin top-left specular highlight + subtle
# bottom-right shadow rim suggesting the tube case. Hot core dialed back so
# tube structure remains visible.
DARK = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · master logo · dark mode (neon-tube M on deep ink).
  Self-contained, scales losslessly.
  Multi-layer: halo / body gradient / specular highlight / shadow rim / hot core.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="MontageSubs M, dark mode">
  <title>MontageSubs · M · dark</title>
  <defs>
    <!-- Tube body: rolled-3D shading via diagonal gradient (lit upper-left, shadow lower-right) -->
    <linearGradient id="tubeBody" x1="0.20" y1="0.12" x2="0.85" y2="0.95">
      <stop offset="0%"  stop-color="{TOKENS['yellow_lit']}"/>
      <stop offset="22%" stop-color="{TOKENS['yellow']}"/>
      <stop offset="55%" stop-color="{TOKENS['amber']}"/>
      <stop offset="82%" stop-color="{TOKENS['amber_deep']}"/>
      <stop offset="100%" stop-color="{TOKENS['amber_dark']}"/>
    </linearGradient>

    <!-- Specular sheen along upper-left edge of every stroke -->
    <linearGradient id="sheen" x1="0" y1="0" x2="0.7" y2="0.6">
      <stop offset="0%"   stop-color="{TOKENS['core_white']}" stop-opacity="0.55"/>
      <stop offset="22%"  stop-color="{TOKENS['glow_high']}"  stop-opacity="0.18"/>
      <stop offset="55%"  stop-color="{TOKENS['amber']}"     stop-opacity="0"/>
      <stop offset="100%" stop-color="{TOKENS['amber_black']}" stop-opacity="0"/>
    </linearGradient>

    <!-- Halo: two concentric blurred copies (far + near). Restrained so structure stays. -->
    <filter id="halo" x="-25%" y="-25%" width="150%" height="150%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="38" result="far"/>
      <feFlood flood-color="{TOKENS['amber']}" flood-opacity="0.35"/>
      <feComposite in2="far" operator="in" result="farC"/>

      <feGaussianBlur in="SourceAlpha" stdDeviation="12" result="near"/>
      <feFlood flood-color="{TOKENS['yellow']}" flood-opacity="0.55"/>
      <feComposite in2="near" operator="in" result="nearC"/>

      <feMerge>
        <feMergeNode in="farC"/>
        <feMergeNode in="nearC"/>
      </feMerge>
    </filter>

    <!-- Hot core: very small, very tight. Suggests the lit tube interior, not bloom. -->
    <filter id="hotcore" x="-10%" y="-10%" width="120%" height="120%">
      <feMorphology in="SourceAlpha" radius="36" operator="erode" result="cs"/>
      <feGaussianBlur in="cs" stdDeviation="14" result="cb"/>
      <feFlood flood-color="{TOKENS['core_white']}" flood-opacity="0.55"/>
      <feComposite in2="cb" operator="in"/>
    </filter>

    <!-- Shadow rim along bottom-right edge: gives the case its 3D depth -->
    <filter id="rim" x="-5%" y="-5%" width="115%" height="115%">
      <feMorphology in="SourceAlpha" radius="3" operator="erode" result="er"/>
      <feOffset in="er" dx="6" dy="9" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2" result="offB"/>
      <feFlood flood-color="{TOKENS['amber_black']}" flood-opacity="0.85"/>
      <feComposite in2="offB" operator="in" result="rimC"/>
      <feComposite in="rimC" in2="SourceAlpha" operator="in"/>
    </filter>
  </defs>

  <rect width="1024" height="1024" fill="{TOKENS['ink_deep']}"/>

  <!-- Soft contextual warmth behind the M -->
  <radialGradient id="vignette" cx="0.42" cy="0.42" r="0.7">
    <stop offset="0%"   stop-color="{TOKENS['amber_dark']}" stop-opacity="0.18"/>
    <stop offset="55%"  stop-color="{TOKENS['amber_dark']}" stop-opacity="0.04"/>
    <stop offset="100%" stop-color="{TOKENS['ink_deep']}"   stop-opacity="0"/>
  </radialGradient>
  <rect width="1024" height="1024" fill="url(#vignette)"/>

  <!-- Halo (separate layer, drawn first, blurred wide) -->
  <path d="{D}" fill="{TOKENS['yellow']}" filter="url(#halo)" fill-rule="evenodd"/>

  <!-- Body: gradient fill -->
  <path d="{D}" fill="url(#tubeBody)" fill-rule="evenodd"/>

  <!-- Shadow rim baked inside the M shape (tube case dimension) -->
  <path d="{D}" fill="{TOKENS['amber_black']}" filter="url(#rim)" fill-rule="evenodd" opacity="0.85"/>

  <!-- Specular sheen -->
  <path d="{D}" fill="url(#sheen)" fill-rule="evenodd"/>

  <!-- Hot core highlight (interior glow line) -->
  <path d="{D}" fill="{TOKENS['core_white']}" filter="url(#hotcore)" fill-rule="evenodd"/>
</svg>
'''
write("m-mark-dark.svg", DARK)


# ---------- Master: light mode (saturated body + soft amber drop shadow) ----------
# Strategy: NO neon glow on light bg (it would wash out). Instead express the
# brand DNA via a saturated yellow-amber body with subtle 3D shading and a
# soft warm drop shadow that gives the M weight and "presence" on the warm
# off-white surface. Same geometry, same tilt + perspective, expressed in
# print-poster idiom rather than neon-tube idiom.
LIGHT = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · master logo · light mode (saturated M on warm off-white).
  Print-poster idiom: solid amber body with 3D shading + soft drop shadow.
  No bloom — bright on light needs structure, not glow.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="MontageSubs M, light mode">
  <title>MontageSubs · M · light</title>
  <defs>
    <!-- Body: stays in bright yellow→amber territory, no deep darks -->
    <linearGradient id="bodyL" x1="0.20" y1="0.05" x2="0.85" y2="1.0">
      <stop offset="0%"   stop-color="{TOKENS['glow_high']}"/>
      <stop offset="22%"  stop-color="{TOKENS['yellow_lit']}"/>
      <stop offset="55%"  stop-color="{TOKENS['yellow']}"/>
      <stop offset="100%" stop-color="{TOKENS['amber']}"/>
    </linearGradient>

    <!-- Soft warm drop shadow -->
    <filter id="dropL" x="-10%" y="-10%" width="120%" height="125%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="11" result="b"/>
      <feOffset in="b" dx="0" dy="12" result="o"/>
      <feFlood flood-color="{TOKENS['amber_dark']}" flood-opacity="0.28"/>
      <feComposite in2="o" operator="in"/>
    </filter>
  </defs>

  <rect width="1024" height="1024" fill="{TOKENS['mist']}"/>

  <!-- Drop shadow -->
  <path d="{D}" fill="{TOKENS['amber_dark']}" filter="url(#dropL)" fill-rule="evenodd"/>

  <!-- Body (bright yellow gradient) -->
  <path d="{D}" fill="url(#bodyL)" fill-rule="evenodd"/>

  <!-- Definition stroke: thin darker amber outline so M reads on warm bg -->
  <path d="{D}" fill="none" stroke="{TOKENS['amber_deep']}" stroke-width="3.2" stroke-linejoin="round" fill-rule="evenodd" opacity="0.55"/>
</svg>
'''
write("m-mark-light.svg", LIGHT)


# ---------- Flat mono variants (for favicon, video bug, small sizes) ----------
def flat(name: str, fill: str, bg: str | None = None, label: str = ""):
    bg_rect = f'<rect width="1024" height="1024" fill="{bg}"/>' if bg else ""
    body = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MontageSubs · M · flat mono · {label} -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="MontageSubs M, {label}">
  <title>MontageSubs M, {label}</title>
  {bg_rect}
  <path d="{D}" fill="{fill}" fill-rule="evenodd"/>
</svg>
'''
    write(name, body)


flat("m-mark-flat-black.svg",  TOKENS["ink_soft"], None, "ink on transparent")
flat("m-mark-flat-white.svg",  TOKENS["white"],    None, "white on transparent (knockout)")
flat("m-mark-flat-yellow.svg", TOKENS["yellow"],   None, "brand yellow on transparent")
flat("m-mark-flat-on-ink.svg",   TOKENS["yellow"],   TOKENS["ink_deep"], "brand yellow on ink")
flat("m-mark-flat-on-mist.svg",  TOKENS["ink_soft"], TOKENS["mist"],     "ink on warm mist")


# ---------- Knockout: yellow background, M cut out (white) ----------
KNOCKOUT = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- MontageSubs · M · brand yellow tile with M knockout -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="MontageSubs M knockout tile">
  <title>MontageSubs · M · knockout</title>
  <defs>
    <mask id="cutout">
      <rect width="1024" height="1024" fill="white"/>
      <path d="{D}" fill="black" fill-rule="evenodd"/>
    </mask>
  </defs>
  <rect width="1024" height="1024" fill="{TOKENS['yellow']}" mask="url(#cutout)"/>
</svg>
'''
write("m-mark-knockout.svg", KNOCKOUT)
