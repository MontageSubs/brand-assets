"""3-way comparison: RAW / v3a (sat only) / v3b (sat + gentle unsharp).

For each diagnostic region, show three crops side by side. User picks the
column that strikes the right balance, no over-sharpening / no false contrast.
"""

import base64
import io
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
ZOOMS = ROOT / "preview/zooms-v3"


def b64(p: Path, max_dim: int | None = None) -> str:
    img = Image.open(p)
    if max_dim and max(img.size) > max_dim:
        s = max_dim / max(img.size)
        img = img.resize((int(img.size[0] * s), int(img.size[1] * s)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, "PNG", optimize=True)
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")


REGIONS = [
    ("01-left-leg-bottom",  "① 左腿底部端面"),
    ("02-left-leg-top",     "② 左腿顶部"),
    ("03-V-tip",            "③ V 尖中心"),
    ("04-right-leg-top",    "④ 右腿顶部"),
    ("05-right-leg-bottom", "⑤ 右腿底部"),
    ("06-tube-highlight",   "⑥ 灯管高光带"),
]

# Full overview (small)
full_raw = b64(ZOOMS / "_full-raw.png", 1200)
full_v3a = b64(ZOOMS / "_full-v3a.png", 1200)
full_v3b = b64(ZOOMS / "_full-v3b.png", 1200)

zoom_html = []
for slug, title in REGIONS:
    raw = b64(ZOOMS / f"{slug}-raw.png")
    v3a = b64(ZOOMS / f"{slug}-v3a.png")
    v3b = b64(ZOOMS / f"{slug}-v3b.png")
    zoom_html.append(f"""
    <section class="zoom">
      <h3>{title}</h3>
      <div class="triplet">
        <figure><img src="{raw}"><figcaption>RAW · 零增强</figcaption></figure>
        <figure><img src="{v3a}"><figcaption>v3a · 仅 sat +4%</figcaption></figure>
        <figure><img src="{v3b}"><figcaption>v3b · sat +4% + 温和锐化</figcaption></figure>
      </div>
    </section>""")

HTML = f"""<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<title>Dark master v3 · 三档对比</title>
<style>
  body {{ background: #1C1812; color: #FAF7EE; margin: 0; padding: 32px;
          font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }}
  h1 {{ font-size: 14px; letter-spacing: 3px; text-align: center; margin: 0 0 24px; }}
  h2 {{ font-size: 11px; letter-spacing: 2px; color: rgba(250,247,238,0.55);
        text-transform: uppercase; margin: 32px 0 12px; }}
  h3 {{ font-size: 14px; margin: 0 0 12px; color: #FFE872; }}
  .changes {{ background: #0E0B07; border: 1px solid rgba(250,247,238,0.1);
              border-radius: 6px; padding: 16px 20px; font-size: 13px; line-height: 1.7; }}
  .changes b {{ color: #FFE872; }}
  .changes ul {{ margin: 8px 0 0 0; padding-left: 20px; }}
  .triplet, .full-row {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }}
  figure {{ background: #0E0B07; border: 1px solid rgba(250,247,238,0.1);
            border-radius: 6px; padding: 12px; margin: 0; }}
  figure.pick {{ border-color: #FFE872; }}
  figure img {{ display: block; width: 100%; height: auto; }}
  figcaption {{ font-size: 10px; letter-spacing: 1.2px; text-transform: uppercase;
                color: rgba(250,247,238,0.55); text-align: center; margin-top: 8px; }}
  figure.pick figcaption {{ color: #FFE872; }}
  .zoom {{ margin-bottom: 32px; }}
  .grid-zooms {{ display: grid; grid-template-columns: 1fr; gap: 24px; }}
</style>
</head>
<body>

<h1>DARK MASTER · v3 · 三档增强对比</h1>

<div class="changes">
  <b>v2 错在哪</b>: percent=110 锐化 + 对比度 +6% + 亮度 +2% 叠加，造成边缘 halo 光环 + 亮部偏白 = 失真。<br><br>
  <b>v3 三档</b>:
  <ul>
    <li><b>RAW</b> — 零增强，只居中 + 合成深墨底。源图原汁原味（M 在画布里保持源 2924 px 的<b>原生分辨率</b>，0 缩放，0 LANCZOS 软化）</li>
    <li><b>v3a</b> — 仅 saturation +4%（轻微让黄色更饱和，无对比度/亮度推动）</li>
    <li><b>v3b</b> — v3a 基础上再加<b>温和 Unsharp Mask</b> (radius=0.8, percent=40, threshold=6)。threshold=6 意味着只有亮度差 ≥6 步的边缘才被锐化，平面噪点不动，不会出 halo 光环</li>
  </ul>
  默认输出已用 <b>v3b</b>。如果你看完觉得 v3b 还是过头 → 用 v3a；觉得 v3a 还是过头 → 用 RAW。<br>
  也可以告诉我"V 尖那块的锐化合适但端面还是过", 我做局部 mask 处理。
</div>

<h2>① 整体三档</h2>
<div class="full-row">
  <figure><img src="{full_raw}"><figcaption>RAW</figcaption></figure>
  <figure><img src="{full_v3a}"><figcaption>v3a · sat +4%</figcaption></figure>
  <figure class="pick"><img src="{full_v3b}"><figcaption>v3b · sat +4% + 温和锐化 ★ 默认</figcaption></figure>
</div>

<h2>② 关键部位三档对照</h2>
<div class="grid-zooms">
{''.join(zoom_html)}
</div>

<div class="changes" style="margin-top:32px">
  回我 <b>"RAW / v3a / v3b"</b> 三选一，或具体哪几块要走更轻的档。锁定后 dark 收尾，进入 light + 下游变体。
</div>

</body>
</html>
"""

(ROOT / "preview/06-dark-v3-three-way.html").write_text(HTML)
print(f"wrote preview/06-dark-v3-three-way.html ({len(HTML):,} bytes)")
