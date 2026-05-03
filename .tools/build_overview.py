"""
Build a self-contained HTML overview page where every image is embedded as a
base64 data URI. Lets the page render in sandboxed preview panels that block
relative file references.
"""

from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")


def data_uri(path: Path, mime: str) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


THUMBS = ROOT / "preview/thumbs"
ASSETS = {
    "dark":     data_uri(THUMBS / "m-mark-dark.png", "image/png"),
    "light":    data_uri(THUMBS / "m-mark-light.png", "image/png"),
    "yellow":   data_uri(THUMBS / "m-mark-flat-on-ink.png", "image/png"),
    "ink":      data_uri(THUMBS / "m-mark-flat-on-mist.png", "image/png"),
    "knockout": data_uri(THUMBS / "m-mark-knockout.png", "image/png"),
    "geom":     data_uri(THUMBS / "m-geom-base.png", "image/png"),
    "original": data_uri(ROOT / "logos/png/web/logo-600.png", "image/png"),
}

HTML = f"""<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8"/>
<title>MontageSubs · master logos overview</title>
<style>
  :root {{
    --grid-bg: #1C1812;
    --grid-card: #262218;
    --text: #FAF7EE;
    --text-dim: rgba(250, 247, 238, 0.55);
    --rule: rgba(250, 247, 238, 0.10);
    --ink-deep: #0E0B07;
    --mist: #FAF7EE;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: var(--grid-bg); color: var(--text);
    font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }}
  body {{ padding: 40px 48px 80px; }}
  h1 {{ font-size: 14px; letter-spacing: 4px; font-weight: 600; text-align: center; margin-bottom: 32px; }}
  h2 {{ font-size: 12px; letter-spacing: 2px; font-weight: 500; text-transform: uppercase;
        color: var(--text-dim); margin: 32px 0 14px; }}
  .row {{ display: grid; gap: 22px; }}
  .row.masters {{ grid-template-columns: 1fr 1fr; }}
  .row.flats {{ grid-template-columns: repeat(4, 1fr); }}
  .card {{ background: var(--grid-card); border: 1px solid var(--rule);
    border-radius: 6px; overflow: hidden; }}
  .card .title {{ padding: 10px 14px; border-bottom: 1px solid var(--rule);
    font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--text-dim); display: flex; justify-content: space-between; }}
  .card .title .meta {{ color: rgba(250,247,238,0.4); font-size: 10px; }}
  .card img {{ display: block; width: 100%; height: auto; }}
  .swatches {{ display: grid; grid-template-columns: repeat(11, 1fr); gap: 8px; }}
  .sw {{ aspect-ratio: 1 / 1.45; border-radius: 4px; overflow: hidden;
    border: 1px solid var(--rule); display: flex; flex-direction: column; }}
  .sw .chip {{ flex: 1; }}
  .sw .label {{ padding: 6px 4px; background: rgba(0,0,0,0.55);
    font-size: 10px; text-align: center; color: var(--text-dim); }}
  .sw .label b {{ color: var(--text); display: block; font-weight: 500; }}
  .ref {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  .ref .pane {{ background: var(--ink-deep); border-radius: 4px; padding: 18px;
    display: flex; flex-direction: column; align-items: center; gap: 8px; }}
  .ref .pane img {{ max-width: 100%; height: auto; }}
  .ref .pane .cap {{ font-size: 10px; letter-spacing: 1px;
    text-transform: uppercase; color: var(--text-dim); }}
  .footer {{ margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--rule);
    font-size: 11px; color: var(--text-dim); text-align: center; }}
  code {{ font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 11px; }}
</style>
</head>
<body>

<h1>MONTAGESUBS · MASTER LOGOS OVERVIEW</h1>

<section class="row masters">
  <div class="card">
    <div class="title"><span>Dark mode · neon</span><span class="meta">m-mark-dark.svg</span></div>
    <img src="{ASSETS['dark']}" alt="Dark master">
  </div>
  <div class="card">
    <div class="title"><span>Light mode · saturated</span><span class="meta">m-mark-light.svg</span></div>
    <img src="{ASSETS['light']}" alt="Light master">
  </div>
</section>

<h2>Flat mono · variants</h2>
<section class="row flats">
  <div class="card">
    <div class="title"><span>Yellow on ink</span><span class="meta">flat-on-ink</span></div>
    <img src="{ASSETS['yellow']}" alt="">
  </div>
  <div class="card">
    <div class="title"><span>Ink on mist</span><span class="meta">flat-on-mist</span></div>
    <img src="{ASSETS['ink']}" alt="">
  </div>
  <div class="card">
    <div class="title"><span>Yellow tile · M knockout</span><span class="meta">knockout</span></div>
    <img src="{ASSETS['knockout']}" alt="">
  </div>
  <div class="card">
    <div class="title"><span>Geometry base (debug)</span><span class="meta">m-geom-base</span></div>
    <img src="{ASSETS['geom']}" alt="">
  </div>
</section>

<h2>Color tokens</h2>
<div class="swatches">
  <div class="sw"><div class="chip" style="background:#0E0B07"></div><div class="label"><b>ink-deep</b>#0E0B07</div></div>
  <div class="sw"><div class="chip" style="background:#1A1410"></div><div class="label"><b>ink-soft</b>#1A1410</div></div>
  <div class="sw"><div class="chip" style="background:#3D1800"></div><div class="label"><b>amber-bk</b>#3D1800</div></div>
  <div class="sw"><div class="chip" style="background:#7A3D00"></div><div class="label"><b>amber-dk</b>#7A3D00</div></div>
  <div class="sw"><div class="chip" style="background:#A85B00"></div><div class="label"><b>amber-deep</b>#A85B00</div></div>
  <div class="sw"><div class="chip" style="background:#FCAB02"></div><div class="label"><b>amber</b>#FCAB02</div></div>
  <div class="sw"><div class="chip" style="background:#FBC100"></div><div class="label"><b>yellow ★</b>#FBC100</div></div>
  <div class="sw"><div class="chip" style="background:#FDD338"></div><div class="label"><b>yellow-lit</b>#FDD338</div></div>
  <div class="sw"><div class="chip" style="background:#FFE872"></div><div class="label"><b>glow-high</b>#FFE872</div></div>
  <div class="sw"><div class="chip" style="background:#FFFCE0"></div><div class="label"><b>core-white</b>#FFFCE0</div></div>
  <div class="sw"><div class="chip" style="background:#FAF7EE"></div><div class="label"><b>mist</b>#FAF7EE</div></div>
</div>

<h2>Reference · original photo vs new master</h2>
<div class="ref">
  <div class="pane">
    <img src="{ASSETS['original']}" alt="Original photo">
    <div class="cap">ORIGINAL · UNSPLASH PHOTO (Zacharie Elbaz)</div>
  </div>
  <div class="pane">
    <img src="{ASSETS['dark']}" alt="New dark master">
    <div class="cap">NEW · DARK MASTER (vector, neon stack)</div>
  </div>
</div>

<div class="footer">
  ★ = primary brand yellow · use this hex for any flat-color reproduction · all masters live in
  <code>logos/master/</code> · raster thumbs in <code>preview/thumbs/</code>
</div>

</body>
</html>
"""

(ROOT / "preview/03-masters-overview.html").write_text(HTML)
print(f"wrote preview/03-masters-overview.html ({len(HTML):,} bytes, all images inlined)")
