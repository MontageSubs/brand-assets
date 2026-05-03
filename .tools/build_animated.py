"""
Build animated logo: neon turn-on flicker sequence.

Two artifacts:
  1. animated-neon-on.html — self-contained HTML demo with CSS keyframe
     animation. Renders the smoothed M silhouette in dark room, then
     flickers and stabilizes into full neon brightness over ~2.5s.
  2. animated-neon-on.svg — pure SVG (with SMIL animation) for embedding
     in markdown / GitHub README / etc. Supports the same flicker.

Mechanism:
  · Background: deep ink
  · M silhouette: starts dim (10% brightness), flickers via opacity keyframes,
    settles to full neon (gradient + glow + hot core)
  · Layered halo also fades in
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
OUT = ROOT / "applications/animated"
OUT.mkdir(parents=True, exist_ok=True)


def get_path() -> str:
    txt = (ROOT / "logos/master/m-geom-base.svg").read_text()
    return re.search(r'<path\s+d="([^"]+)"', txt).group(1)


D = get_path()


# Animated SVG (with SMIL animation, plays once on load)
SVG = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · animated logo · neon turn-on (~2.5s loop)
  Plays once: dim → flicker → flicker → stabilize at full neon.
  Embed in markdown / README / web pages directly.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"
     role="img" aria-label="MontageSubs M, neon turning on">
  <title>MontageSubs · animated · neon on</title>
  <defs>
    <linearGradient id="bodyA" x1="0.20" y1="0.12" x2="0.85" y2="0.95">
      <stop offset="0%"  stop-color="#FDD338"/>
      <stop offset="22%" stop-color="#FBC100"/>
      <stop offset="55%" stop-color="#FCAB02"/>
      <stop offset="82%" stop-color="#A85B00"/>
      <stop offset="100%" stop-color="#7A3D00"/>
    </linearGradient>

    <filter id="haloA" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="38" result="far"/>
      <feFlood flood-color="#FCAB02" flood-opacity="0.40"/>
      <feComposite in2="far" operator="in" result="farC"/>
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" result="near"/>
      <feFlood flood-color="#FBC100" flood-opacity="0.55"/>
      <feComposite in2="near" operator="in" result="nearC"/>
      <feMerge><feMergeNode in="farC"/><feMergeNode in="nearC"/></feMerge>
    </filter>

    <filter id="hotcoreA" x="-10%" y="-10%" width="120%" height="120%">
      <feMorphology in="SourceAlpha" radius="36" operator="erode" result="cs"/>
      <feGaussianBlur in="cs" stdDeviation="14" result="cb"/>
      <feFlood flood-color="#FFFCE0" flood-opacity="0.55"/>
      <feComposite in2="cb" operator="in"/>
    </filter>
  </defs>

  <rect width="1024" height="1024" fill="#0E0B07"/>

  <!-- Halo layer (animates in) -->
  <g opacity="0">
    <animate attributeName="opacity"
             values="0;0;0.2;0;0.5;0.1;0.7;0.3;0.9;0.6;1;1"
             keyTimes="0;0.10;0.18;0.22;0.30;0.38;0.46;0.55;0.65;0.78;0.92;1"
             dur="2.5s" fill="freeze"/>
    <path d="{D}" fill="#FBC100" filter="url(#haloA)" fill-rule="evenodd"/>
  </g>

  <!-- Body M -->
  <g>
    <animate attributeName="opacity"
             values="0;0.05;0.05;0.4;0.1;0.6;0.2;0.85;0.5;1;0.7;1"
             keyTimes="0;0.08;0.18;0.25;0.32;0.40;0.50;0.60;0.70;0.82;0.90;1"
             dur="2.5s" fill="freeze"/>
    <path d="{D}" fill="url(#bodyA)" fill-rule="evenodd"/>
  </g>

  <!-- Hot core (animates last) -->
  <g opacity="0">
    <animate attributeName="opacity"
             values="0;0;0;0;0.3;0.1;0.6;0.4;0.9;0.7;1;1"
             keyTimes="0;0.10;0.20;0.30;0.40;0.50;0.60;0.70;0.80;0.88;0.95;1"
             dur="2.5s" fill="freeze"/>
    <path d="{D}" fill="#FFFCE0" filter="url(#hotcoreA)" fill-rule="evenodd"/>
  </g>
</svg>
'''
(OUT / "animated-neon-on.svg").write_text(SVG)


# Self-contained HTML demo
HTML = f'''<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<title>MontageSubs · animated · neon on</title>
<style>
  html, body {{ margin: 0; padding: 0; background: #0E0B07; height: 100%; }}
  body {{ display: grid; place-items: center; }}
  .stage {{ width: min(80vw, 80vh); aspect-ratio: 1; position: relative; }}
  .stage svg {{ width: 100%; height: 100%; }}
  .controls {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
               display: flex; gap: 12px; }}
  .controls button {{ padding: 8px 16px; background: rgba(250,247,238,0.1);
                       color: #FAF7EE; border: 1px solid rgba(250,247,238,0.2);
                       border-radius: 4px; font: 12px sans-serif; cursor: pointer;
                       letter-spacing: 1px; text-transform: uppercase; }}
  .controls button:hover {{ background: rgba(250,247,238,0.18); }}
</style>
</head>
<body>
<div class="stage" id="stage">
  {SVG.replace('<?xml version="1.0" encoding="UTF-8"?>', '')}
</div>
<div class="controls">
  <button onclick="replay()">▶ Replay</button>
</div>
<script>
function replay() {{
  const stage = document.getElementById('stage');
  const svg = stage.querySelector('svg');
  // Re-trigger SMIL animations by replacing the node
  const clone = svg.cloneNode(true);
  svg.parentNode.replaceChild(clone, svg);
}}
</script>
</body>
</html>
'''
(OUT / "animated-neon-on.html").write_text(HTML)


# Markdown embed snippet
md = '''# MontageSubs · animated logo

Embed the neon-turn-on animation in any markdown file:

```markdown
![MontageSubs neon on](applications/animated/animated-neon-on.svg)
```

Or in HTML:

```html
<img src="applications/animated/animated-neon-on.svg" alt="MontageSubs">
```

The SVG plays its 2.5s "neon turn-on" sequence once on each page load.
For a continuous loop, wrap in CSS that periodically reloads or use the
animated GIF version (run `python3 .tools/render_animated_gif.py`).

For video footage (片头/片尾 use), the recommended workflow:
1. Open `animated-neon-on.html` in a browser
2. Use a screen recorder (e.g., Quicktime, OBS, ffmpeg) to capture the 2.5s
3. Encode to ProRes or H.264 with transparent alpha if your editor supports it
'''
(OUT / "README.md").write_text(md)

print(f"wrote applications/animated/")
print(f"  animated-neon-on.svg ({len(SVG):,} bytes)")
print(f"  animated-neon-on.html ({len(HTML):,} bytes)")
print(f"  README.md")
