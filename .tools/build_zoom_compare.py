"""Build a zoom-comparison HTML page: 6 paired detail crops (orig vs new master)
plus the full-frame side-by-side. All embedded as base64 so the preview panel
sandbox can render it without cross-file loads."""

import base64
import io
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
ZOOMS = ROOT / "preview/zooms"


def b64(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")


def b64_resized(p: Path, max_dim: int) -> str:
    img = Image.open(p)
    w, h = img.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


REGIONS = [
    ("01-left-leg-bottom",   "① 左腿底部端面", "灯箱底端切角的清晰度"),
    ("02-left-leg-top",      "② 左腿顶部",     "顶部端面 + 侧面亮带过渡"),
    ("03-V-tip",             "③ V 尖中心",     "中部低点的曲线还原"),
    ("04-right-leg-top",     "④ 右腿顶部",     "右上端面 + 案体边缘"),
    ("05-right-leg-bottom",  "⑤ 右腿底部",     "右下端面 + 投射光"),
    ("06-tube-highlight",    "⑥ 灯管高光带",   "管体内核反光 / 玻璃反射"),
]

full_orig = b64_resized(ZOOMS / "_full-orig.png", 1280)
full_new  = b64_resized(ZOOMS / "_full-new.png", 1280)

cards_html = []
for slug, title, desc in REGIONS:
    o = b64(ZOOMS / f"{slug}-orig.png")
    n = b64(ZOOMS / f"{slug}-new.png")
    cards_html.append(f"""
    <section class="zoom">
      <h3>{title}</h3>
      <p class="hint">{desc}</p>
      <div class="pair">
        <figure><img src="{o}"><figcaption>原图</figcaption></figure>
        <figure><img src="{n}"><figcaption>新 dark master · v2 (锐化)</figcaption></figure>
      </div>
    </section>""")

HTML = f"""<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<title>MontageSubs · dark master v2 · zoom compare</title>
<style>
  body {{ background: #1C1812; color: #FAF7EE; margin: 0; padding: 32px;
         font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }}
  h1 {{ font-size: 14px; letter-spacing: 3px; text-align: center; margin: 0 0 24px; }}
  h2 {{ font-size: 11px; letter-spacing: 2px; color: rgba(250,247,238,0.55);
        text-transform: uppercase; margin: 32px 0 12px; }}
  h3 {{ font-size: 14px; margin: 0 0 4px; color: #FFE872; }}
  .hint {{ font-size: 12px; color: rgba(250,247,238,0.6); margin: 0 0 12px; }}
  .full {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  .full figure {{ background: #0E0B07; border: 1px solid rgba(250,247,238,0.1);
                  border-radius: 6px; padding: 12px; margin: 0; }}
  .full img, .pair img {{ display: block; width: 100%; height: auto; }}
  figcaption {{ font-size: 10px; letter-spacing: 1.2px; text-transform: uppercase;
                color: rgba(250,247,238,0.55); text-align: center; margin-top: 8px; }}
  .pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  .pair figure {{ background: #0E0B07; border: 1px solid rgba(250,247,238,0.1);
                  border-radius: 6px; padding: 12px; margin: 0; }}
  .zoom {{ margin-bottom: 32px; }}
  .grid-zooms {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media (max-width: 1100px) {{ .grid-zooms {{ grid-template-columns: 1fr; }} }}
  .changes {{ background: #0E0B07; border: 1px solid rgba(250,247,238,0.1);
              border-radius: 6px; padding: 16px 20px; font-size: 13px;
              line-height: 1.7; color: rgba(250,247,238,0.85); }}
  .changes b {{ color: #FFE872; }}
</style>
</head>
<body>

<h1>DARK MASTER · v2 · LINE / ANGLE / PERSPECTIVE 还原度核对</h1>

<div class="changes">
  <b>v2 改动</b><br>
  · 输出尺寸 <b>2048 → 3072</b>（不再下采样源 2924px，避免 LANCZOS 软化）<br>
  · 新增 <b>边缘锐化</b>（Unsharp Mask: r=2.0, percent=110, threshold=3，仅放大 ≥3 luma 步的边缘，不放大平面噪点）<br>
  · 饱和 +12% / 对比 +6% / 亮度 +2%（保留 v1 等级，避免和 light master 调性脱钩）<br>
  · 整体设计、几何、透视角度<b>均不改动</b>（你说过整体设计不动）
</div>

<h2>① 整体对照</h2>
<div class="full">
  <figure><img src="{full_orig}"><figcaption>原图（仅做了居中 + 尺寸归一化，未锐化）</figcaption></figure>
  <figure><img src="{full_new}"><figcaption>新 dark master · v2（饱和+对比+亮度+锐化）</figcaption></figure>
</div>

<h2>② 关键部位逐块对照（4× 放大）</h2>
<div class="grid-zooms">
{''.join(cards_html)}
</div>

<div class="changes" style="margin-top:32px">
  你看完每块对照后，告诉我具体哪些位置还差（"① 左腿底部端面要再清楚"、"③ V 尖那道反光要更利"…），
  我对应调参（锐化半径 / 强度 / 阈值，或单独对那块做 mask 处理）。<br>
  也可以告诉我"OK"，我锁定 dark master 进入 light + 下游变体。
</div>

</body>
</html>
"""

(ROOT / "preview/05-dark-zoom-compare.html").write_text(HTML)
print(f"wrote preview/05-dark-zoom-compare.html ({len(HTML):,} bytes, all images inlined)")
