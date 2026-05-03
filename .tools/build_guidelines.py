"""Build clearspace, min-size, and misuse spec sheets."""

import base64
import re
from pathlib import Path

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
OUT = ROOT / "guidelines"
OUT.mkdir(parents=True, exist_ok=True)


def get_path() -> str:
    txt = (ROOT / "logos/master/m-geom-base.svg").read_text()
    return re.search(r'<path\s+d="([^"]+)"', txt).group(1)


def b64_png(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")


D = get_path()
DARK_M = b64_png(ROOT / "logos/master/m-mark-dark.png")
ROUND_M = b64_png(ROOT / "logos/master/m-mark-light-rounded.png")


# --- Clearspace ---
CLEARSPACE = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  MontageSubs · clearspace specification
  Minimum padding around the M = X (where X = 1/4 the M's bounding box height).
  No other element may enter this zone.
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1200" font-family="Helvetica, Arial, sans-serif">
  <rect width="1800" height="1200" fill="#FAF7EE"/>

  <!-- Title -->
  <text x="900" y="80" text-anchor="middle" font-size="22" font-weight="600" letter-spacing="3" fill="#1A1410">CLEARSPACE · 安全间距</text>
  <text x="900" y="110" text-anchor="middle" font-size="13" fill="#1A1410" opacity="0.6">Minimum padding around the M is X (¼ of the M box height). No element enters this zone.</text>

  <!-- Diagram -->
  <g transform="translate(400, 200)">
    <!-- The M -->
    <image x="0" y="0" width="600" height="600" href="{DARK_M}"/>

    <!-- Clearspace zone (dashed) -->
    <rect x="-150" y="-150" width="900" height="900" fill="none"
          stroke="#FBC100" stroke-width="2" stroke-dasharray="10,8"/>

    <!-- X measurement labels -->
    <line x1="-150" y1="-30" x2="0" y2="-30" stroke="#1A1410" stroke-width="1.5"/>
    <line x1="-150" y1="-20" x2="-150" y2="-40" stroke="#1A1410" stroke-width="1.5"/>
    <line x1="0" y1="-20" x2="0" y2="-40" stroke="#1A1410" stroke-width="1.5"/>
    <text x="-75" y="-50" text-anchor="middle" font-size="20" font-weight="600" fill="#1A1410">X</text>

    <line x1="-30" y1="-150" x2="-30" y2="0" stroke="#1A1410" stroke-width="1.5"/>
    <line x1="-20" y1="-150" x2="-40" y2="-150" stroke="#1A1410" stroke-width="1.5"/>
    <line x1="-20" y1="0" x2="-40" y2="0" stroke="#1A1410" stroke-width="1.5"/>
    <text x="-50" y="-72" text-anchor="middle" font-size="20" font-weight="600" fill="#1A1410">X</text>

    <line x1="600" y1="-30" x2="750" y2="-30" stroke="#1A1410" stroke-width="1.5"/>
    <line x1="600" y1="-20" x2="600" y2="-40" stroke="#1A1410" stroke-width="1.5"/>
    <line x1="750" y1="-20" x2="750" y2="-40" stroke="#1A1410" stroke-width="1.5"/>
    <text x="675" y="-50" text-anchor="middle" font-size="20" font-weight="600" fill="#1A1410">X</text>

    <!-- "M box" notation -->
    <line x1="0" y1="-80" x2="0" y2="-100" stroke="#1A1410" stroke-width="1" opacity="0.4"/>
    <line x1="600" y1="-80" x2="600" y2="-100" stroke="#1A1410" stroke-width="1" opacity="0.4"/>
    <line x1="0" y1="-90" x2="600" y2="-90" stroke="#1A1410" stroke-width="1" opacity="0.4"/>
    <text x="300" y="-100" text-anchor="middle" font-size="14" fill="#1A1410" opacity="0.6">M bounding box (height = H)</text>
  </g>

  <!-- Legend -->
  <g transform="translate(150, 1000)">
    <text x="0" y="0" font-size="14" font-weight="600" fill="#1A1410">FORMULA</text>
    <text x="0" y="30" font-size="14" fill="#1A1410">X = H ÷ 4</text>
    <text x="0" y="55" font-size="13" fill="#1A1410" opacity="0.7">where H = the M's vertical bounding box height</text>
  </g>

  <g transform="translate(700, 1000)">
    <text x="0" y="0" font-size="14" font-weight="600" fill="#1A1410">DO</text>
    <text x="0" y="30" font-size="13" fill="#1A1410">· Keep this padding around the M in all uses</text>
    <text x="0" y="55" font-size="13" fill="#1A1410">· If using a token (rounded/circle), token's edge counts as M's edge</text>
  </g>

  <g transform="translate(1300, 1000)">
    <text x="0" y="0" font-size="14" font-weight="600" fill="#1A1410">DON'T</text>
    <text x="0" y="30" font-size="13" fill="#1A1410">· Place text/icons inside the dashed zone</text>
    <text x="0" y="55" font-size="13" fill="#1A1410">· Crop the M tighter than this padding</text>
  </g>
</svg>
'''
(OUT / "clearspace.svg").write_text(CLEARSPACE)


# --- Min size ---
MIN_SIZE = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1200" font-family="Helvetica, Arial, sans-serif">
  <rect width="1800" height="1200" fill="#FAF7EE"/>

  <text x="900" y="80" text-anchor="middle" font-size="22" font-weight="600" letter-spacing="3" fill="#1A1410">MIN SIZE · 最小尺寸</text>
  <text x="900" y="110" text-anchor="middle" font-size="13" fill="#1A1410" opacity="0.6">Below these sizes the M's tube structure becomes illegible — fall back to the favicon set instead.</text>

  <!-- Three reference sizes -->
  <g transform="translate(150, 250)">
    <text x="0" y="-30" font-size="12" letter-spacing="2" font-weight="600" fill="#1A1410">SCREEN · 32 px ≈ FAVICON FALLBACK</text>
    <image x="0" y="0" width="32" height="32" href="{ROUND_M}"/>
    <text x="0" y="80" font-size="12" fill="#1A1410" opacity="0.7">Use logos/favicon/favicon-32.png</text>
  </g>
  <g transform="translate(150, 470)">
    <text x="0" y="-30" font-size="12" letter-spacing="2" font-weight="600" fill="#1A1410">SCREEN · 64 px ≈ MIN FOR PHOTO M</text>
    <image x="0" y="0" width="64" height="64" href="{DARK_M}"/>
    <text x="0" y="100" font-size="12" fill="#1A1410" opacity="0.7">Anything smaller, use the rounded token favicon.</text>
  </g>
  <g transform="translate(150, 720)">
    <text x="0" y="-30" font-size="12" letter-spacing="2" font-weight="600" fill="#1A1410">PRINT · 12 mm ≈ MIN FOR PHOTO M</text>
    <image x="0" y="0" width="170" height="170" href="{DARK_M}"/>
    <text x="0" y="200" font-size="12" fill="#1A1410" opacity="0.7">12 mm at 300 dpi = 142 px square. Below this, use the mono silhouette.</text>
  </g>

  <!-- Recommended sizes -->
  <g transform="translate(900, 250)">
    <text x="0" y="-30" font-size="12" letter-spacing="2" font-weight="600" fill="#1A1410">RECOMMENDED MINIMUMS</text>
    <text x="0" y="20" font-size="14" fill="#1A1410">Web header / nav</text>
    <text x="280" y="20" font-size="14" fill="#1A1410" font-weight="600">≥ 64 px</text>
    <text x="0" y="60" font-size="14" fill="#1A1410">Social avatar</text>
    <text x="280" y="60" font-size="14" fill="#1A1410" font-weight="600">≥ 256 px</text>
    <text x="0" y="100" font-size="14" fill="#1A1410">Video bug / 台标</text>
    <text x="280" y="100" font-size="14" fill="#1A1410" font-weight="600">≥ 80 px @ 1080p (~7% of width)</text>
    <text x="0" y="140" font-size="14" fill="#1A1410">PPT / presentation hero</text>
    <text x="280" y="140" font-size="14" fill="#1A1410" font-weight="600">≥ 200 px</text>
    <text x="0" y="180" font-size="14" fill="#1A1410">Business card / stationery</text>
    <text x="280" y="180" font-size="14" fill="#1A1410" font-weight="600">≥ 18 mm</text>
    <text x="0" y="220" font-size="14" fill="#1A1410">Embroidery / single-color print</text>
    <text x="280" y="220" font-size="14" fill="#1A1410" font-weight="600">≥ 25 mm (use mono silhouette)</text>
  </g>
</svg>
'''
(OUT / "minsize.svg").write_text(MIN_SIZE)


# --- Misuse ---
MISUSE = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1200" font-family="Helvetica, Arial, sans-serif">
  <rect width="1800" height="1200" fill="#FAF7EE"/>

  <text x="900" y="80" text-anchor="middle" font-size="22" font-weight="600" letter-spacing="3" fill="#1A1410">MISUSE · 错误用法</text>
  <text x="900" y="110" text-anchor="middle" font-size="13" fill="#1A1410" opacity="0.6">六种禁止——保持品牌一致性。Six don'ts to keep the brand consistent.</text>

  <!-- 6 misuse cells: 3×2 -->
  <g font-size="13">
    <!-- Cell 1: stretched -->
    <g transform="translate(120, 200)">
      <rect width="380" height="380" fill="#0E0B07" rx="8"/>
      <image x="40" y="80" width="300" height="220" preserveAspectRatio="none" href="{DARK_M}"/>
      <text x="190" y="350" text-anchor="middle" fill="#F26F52" font-weight="600">✗ 拉伸 / 压扁 STRETCH</text>
    </g>
    <!-- Cell 2: rotated -->
    <g transform="translate(560, 200)">
      <rect width="380" height="380" fill="#0E0B07" rx="8"/>
      <g transform="translate(190, 190) rotate(28) translate(-150, -150)">
        <image x="0" y="0" width="300" height="300" href="{DARK_M}"/>
      </g>
      <text x="190" y="350" text-anchor="middle" fill="#F26F52" font-weight="600">✗ 自由旋转 ROTATE</text>
    </g>
    <!-- Cell 3: recoloured -->
    <g transform="translate(1000, 200)">
      <rect width="380" height="380" fill="#0E0B07" rx="8"/>
      <g transform="translate(40, 40)">
        <path d="{D}" fill="#22A0FF" fill-rule="evenodd" transform="scale(0.293)"/>
      </g>
      <text x="190" y="350" text-anchor="middle" fill="#F26F52" font-weight="600">✗ 改色 RECOLOUR</text>
    </g>

    <!-- Cell 4: drop shadow -->
    <g transform="translate(120, 640)">
      <rect width="380" height="380" fill="#0E0B07" rx="8"/>
      <g transform="translate(40, 40)">
        <path d="{D}" fill="#FBC100" fill-rule="evenodd" transform="scale(0.293)" filter="drop-shadow(8px 12px 0 #00FF88)"/>
      </g>
      <text x="190" y="350" text-anchor="middle" fill="#F26F52" font-weight="600">✗ 加效果 EFFECTS</text>
    </g>
    <!-- Cell 5: outlined -->
    <g transform="translate(560, 640)">
      <rect width="380" height="380" fill="#0E0B07" rx="8"/>
      <g transform="translate(40, 40)">
        <path d="{D}" fill="none" stroke="#FBC100" stroke-width="20" fill-rule="evenodd" transform="scale(0.293)"/>
      </g>
      <text x="190" y="350" text-anchor="middle" fill="#F26F52" font-weight="600">✗ 改成线框 OUTLINE</text>
    </g>
    <!-- Cell 6: cluttered bg -->
    <g transform="translate(1000, 640)">
      <rect width="380" height="380" fill="#0E0B07" rx="8"/>
      <g>
        <rect x="20" y="20" width="340" height="340" fill="url(#chaosGrad)" opacity="0.5"/>
      </g>
      <image x="40" y="40" width="300" height="300" href="{DARK_M}"/>
      <text x="190" y="350" text-anchor="middle" fill="#F26F52" font-weight="600">✗ 嘈杂背景 BUSY BG</text>
    </g>
  </g>

  <defs>
    <linearGradient id="chaosGrad">
      <stop offset="0%" stop-color="#22A0FF"/>
      <stop offset="50%" stop-color="#F26F52"/>
      <stop offset="100%" stop-color="#22FF88"/>
    </linearGradient>
  </defs>
</svg>
'''
(OUT / "misuse.svg").write_text(MISUSE)


# --- Color tokens ---
COLORS = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 800" font-family="Helvetica, Arial, sans-serif">
  <rect width="1800" height="800" fill="#FAF7EE"/>
  <text x="900" y="80" text-anchor="middle" font-size="22" font-weight="600" letter-spacing="3" fill="#1A1410">COLOR TOKENS · 配色规范</text>
  <text x="900" y="110" text-anchor="middle" font-size="13" fill="#1A1410" opacity="0.6">11 named tokens · brand yellow #FBC100 is canonical for any flat-color reproduction.</text>

  <!-- 11 color swatches in a row -->
  <g transform="translate(80, 200)">
'''

tokens = [
    ("ink-deep",   "#0E0B07", "dark mode bg"),
    ("ink-soft",   "#1A1410", "mono ink fill"),
    ("amber-bk",   "#3D1800", "case shadow"),
    ("amber-dk",   "#7A3D00", "case mid"),
    ("amber-deep", "#A85B00", "case lit edge"),
    ("amber",      "#FCAB02", "amber tone"),
    ("yellow ★",   "#FBC100", "PRIMARY"),
    ("yellow-lit", "#FDD338", "lit body"),
    ("glow-high",  "#FFE872", "glow halo"),
    ("core-white", "#FFFCE0", "tube core"),
    ("mist",       "#FAF7EE", "light mode bg"),
]

W = 140
for i, (name, hex_, desc) in enumerate(tokens):
    x = i * (W + 10)
    is_primary = "★" in name
    text_color = "#FAF7EE" if hex_ in ["#0E0B07", "#1A1410", "#3D1800", "#7A3D00", "#A85B00"] else "#1A1410"
    border = ' stroke="#1A1410" stroke-width="1"' if hex_ == "#FAF7EE" else ''
    star = '<text x="70" y="60" text-anchor="middle" font-size="20" fill="#1A1410">★</text>' if is_primary else ''
    COLORS += f'''
    <g transform="translate({x}, 0)">
      <rect width="{W}" height="200" fill="{hex_}" rx="6"{border}/>
      {star}
      <text x="70" y="240" text-anchor="middle" font-size="14" font-weight="600" fill="#1A1410">{name}</text>
      <text x="70" y="266" text-anchor="middle" font-size="12" fill="#1A1410" opacity="0.7" font-family="ui-monospace, Menlo, monospace">{hex_}</text>
      <text x="70" y="290" text-anchor="middle" font-size="11" fill="#1A1410" opacity="0.55">{desc}</text>
    </g>'''

COLORS += '''
  </g>
</svg>
'''
(OUT / "colors.svg").write_text(COLORS)


print(f"wrote guidelines/")
print(f"  clearspace.svg")
print(f"  minsize.svg")
print(f"  misuse.svg")
print(f"  colors.svg")
