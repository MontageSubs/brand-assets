"""
Generate favicons at all standard sizes from m-mark-light-rounded.png
(the rounded dark-token, which is the canonical "logo on light page" form
and works equally well as a square app icon at any size).

Sizes:
  16, 32, 48   — browser tab favicons
  180          — apple-touch-icon
  192, 512     — Android / PWA / web manifest
  + favicon.ico (multi-res 16/32/48)
"""

from pathlib import Path
from PIL import Image

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
SRC = ROOT / "logos/master/m-mark-light-rounded.png"
OUT = ROOT / "logos/favicon"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    src = Image.open(SRC).convert("RGBA")
    print(f"source: {src.size}")

    sizes = [16, 32, 48, 64, 96, 128, 180, 192, 256, 384, 512]
    for s in sizes:
        out = src.resize((s, s), Image.LANCZOS)
        out.save(OUT / f"favicon-{s}.png", optimize=True)
        print(f"  favicon-{s}.png")

    # Multi-res .ico
    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    src.save(OUT / "favicon.ico", format="ICO", sizes=ico_sizes)
    print(f"  favicon.ico ({len(ico_sizes)} sizes)")

    # Apple-touch-icon (often references favicon-180)
    Image.open(OUT / "favicon-180.png").save(OUT / "apple-touch-icon.png", optimize=True)
    print(f"  apple-touch-icon.png")

    # Web manifest stub for PWA
    manifest = '''{
  "name": "MontageSubs · 蒙太奇字幕组",
  "short_name": "MontageSubs",
  "description": "用爱发电 · Powered by Love",
  "background_color": "#0E0B07",
  "theme_color": "#0E0B07",
  "display": "standalone",
  "icons": [
    { "src": "favicon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "favicon-256.png", "sizes": "256x256", "type": "image/png" },
    { "src": "favicon-384.png", "sizes": "384x384", "type": "image/png" },
    { "src": "favicon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ]
}
'''
    (OUT / "manifest.webmanifest").write_text(manifest)
    print(f"  manifest.webmanifest")

    # HTML snippet for sites that want to use these
    html_snippet = '''<!-- MontageSubs · favicon stack -->
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#0E0B07">
'''
    (OUT / "html-snippet.html").write_text(html_snippet)
    print(f"  html-snippet.html")

    print(f"done · {len(list(OUT.glob('*')))} files in logos/favicon/")


if __name__ == "__main__":
    main()
