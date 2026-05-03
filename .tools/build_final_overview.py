"""Final brand asset overview — all deliverables visible in one HTML page."""

import base64
import io
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")


def b64_resized(p: Path, max_dim: int = 600) -> str:
    if not p.exists():
        return ""
    img = Image.open(p)
    if max(img.size) > max_dim:
        s = max_dim / max(img.size)
        img = img.resize((int(img.size[0] * s), int(img.size[1] * s)), Image.LANCZOS)
    buf = io.BytesIO()
    fmt = "PNG" if p.suffix.lower() in (".png", ".svg") else "JPEG"
    if img.mode == "RGBA" and fmt == "JPEG":
        bg = Image.new("RGB", img.size, (250, 247, 238))
        bg.paste(img, mask=img.split()[-1])
        img = bg
    img.save(buf, fmt, optimize=True)
    mime = "image/png" if fmt == "PNG" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def card(title: str, src: str, meta: str = "", lightcard: bool = False) -> str:
    cls = "card lightcard" if lightcard else "card"
    return f'''<div class="{cls}">
      <div class="title"><span>{title}</span><span class="meta">{meta}</span></div>
      <img src="{src}" alt="{title}">
    </div>'''


# Master images (1080 max for the overview)
m_dark = b64_resized(ROOT / "logos/master/m-mark-dark.png", 800)
m_light_round = b64_resized(ROOT / "logos/master/m-mark-light-rounded.png", 800)
m_light_circle = b64_resized(ROOT / "logos/master/m-mark-light-circle.png", 800)
m_light_square = b64_resized(ROOT / "logos/master/m-mark-light-square.png", 800)

# Mono variants (render thumbnails via qlmanage one-off)
import subprocess
mono_dir = ROOT / "logos/mono"
mono_thumbs = ROOT / "preview/thumbs/mono"
mono_thumbs.mkdir(parents=True, exist_ok=True)
for svg in sorted(mono_dir.glob("*.svg")):
    out = mono_thumbs / (svg.stem + ".png")
    if not out.exists():
        subprocess.run(["qlmanage", "-t", "-s", "400", "-o", str(mono_thumbs), str(svg)],
                       capture_output=True)
        # qlmanage outputs name.svg.png, rename to name.png
        intermediate = mono_thumbs / (svg.name + ".png")
        if intermediate.exists():
            intermediate.rename(out)

mono_imgs = {p.stem: b64_resized(p, 400) for p in mono_thumbs.glob("*.png")}

# Lockups
lockup_h_dark = b64_resized(ROOT / "logos/lockup/lockup-horizontal-dark.png", 1200)
lockup_h_light = b64_resized(ROOT / "logos/lockup/lockup-horizontal-light.png", 1200)
lockup_s_dark = b64_resized(ROOT / "logos/lockup/lockup-stacked-dark.png", 600)
lockup_s_light = b64_resized(ROOT / "logos/lockup/lockup-stacked-light.png", 600)

# Favicons (small thumbnails of varied sizes)
fav_thumbs = {}
for s in [16, 32, 48, 64, 128, 256, 512]:
    fav_thumbs[s] = b64_resized(ROOT / f"logos/favicon/favicon-{s}.png", min(s, 400))

# Applications
app_avatar_sq = b64_resized(ROOT / "applications/social/avatar-square-1080.png", 600)
app_avatar_circ = b64_resized(ROOT / "applications/social/avatar-circle-800.png", 600)
app_banner = b64_resized(ROOT / "applications/social/banner-1500x500.png", 1200)
app_banner_yt = b64_resized(ROOT / "applications/social/banner-youtube-2560x1440.png", 1200)
app_ppt_dark = b64_resized(ROOT / "applications/ppt-cover/ppt-cover-dark.png", 1200)
app_ppt_light = b64_resized(ROOT / "applications/ppt-cover/ppt-cover-light.png", 1200)
app_letter_dark = b64_resized(ROOT / "applications/stationery/letterhead-dark.png", 600)
app_letter_light = b64_resized(ROOT / "applications/stationery/letterhead-light.png", 600)
app_card_dark_front = b64_resized(ROOT / "applications/stationery/business-card-dark-front.png", 600)
app_card_dark_back = b64_resized(ROOT / "applications/stationery/business-card-dark-back.png", 600)
app_card_light_front = b64_resized(ROOT / "applications/stationery/business-card-light-front.png", 600)
app_card_light_back = b64_resized(ROOT / "applications/stationery/business-card-light-back.png", 600)

# Animation: embed WebP directly as base64 (preserves animation)
_webp_path = ROOT / "applications/animated/animated-neon-on.webp"
animated_webp = "data:image/webp;base64," + base64.b64encode(_webp_path.read_bytes()).decode("ascii")
animated_frames_sample = b64_resized(ROOT / "preview/animated-frames-sample.png", 1500)

# Video bug — render one to preview
vbug_yellow_thumb = ROOT / "preview/thumbs/video-bug-yellow.png"
if not vbug_yellow_thumb.exists():
    subprocess.run(["qlmanage", "-t", "-s", "400", "-o", str(ROOT / "preview/thumbs/"),
                    str(ROOT / "applications/video-bug/video-bug-yellow.svg")],
                   capture_output=True)
    intermediate = ROOT / "preview/thumbs/video-bug-yellow.svg.png"
    if intermediate.exists():
        intermediate.rename(vbug_yellow_thumb)
vbug_yellow = b64_resized(vbug_yellow_thumb, 400)

# Guidelines previews
clearspace_thumb = ROOT / "preview/thumbs/clearspace.png"
minsize_thumb = ROOT / "preview/thumbs/minsize.png"
misuse_thumb = ROOT / "preview/thumbs/misuse.png"
colors_thumb = ROOT / "preview/thumbs/colors.png"
for src_name, thumb in [
    ("clearspace.svg", clearspace_thumb),
    ("minsize.svg", minsize_thumb),
    ("misuse.svg", misuse_thumb),
    ("colors.svg", colors_thumb),
]:
    if not thumb.exists():
        subprocess.run(["qlmanage", "-t", "-s", "1500", "-o", str(ROOT / "preview/thumbs/"),
                        str(ROOT / "guidelines" / src_name)], capture_output=True)
        intermediate = ROOT / "preview/thumbs" / (src_name + ".png")
        if intermediate.exists():
            intermediate.rename(thumb)

clearspace = b64_resized(clearspace_thumb, 1200)
minsize = b64_resized(minsize_thumb, 1200)
misuse = b64_resized(misuse_thumb, 1200)
colors = b64_resized(colors_thumb, 1200)


HTML = f"""<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<title>MontageSubs · Brand Asset Final Overview</title>
<style>
  body {{ background: #1C1812; color: #FAF7EE; margin: 0; padding: 32px;
          font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }}
  h1 {{ font-size: 16px; letter-spacing: 4px; text-align: center; margin: 0 0 8px; }}
  .sub {{ font-size: 12px; color: rgba(250,247,238,0.55); text-align: center;
          letter-spacing: 2px; margin-bottom: 36px; }}
  h2 {{ font-size: 12px; letter-spacing: 2px; color: #FFE872; text-transform: uppercase;
        margin: 48px 0 14px; padding-bottom: 6px; border-bottom: 1px solid rgba(255,232,114,0.2); }}
  .row {{ display: grid; gap: 16px; }}
  .row.two {{ grid-template-columns: 1fr 1fr; }}
  .row.three {{ grid-template-columns: 1fr 1fr 1fr; }}
  .row.four {{ grid-template-columns: 1fr 1fr 1fr 1fr; }}
  .row.five {{ grid-template-columns: repeat(5, 1fr); }}
  .card {{ background: #0E0B07; border: 1px solid rgba(250,247,238,0.1);
          border-radius: 6px; overflow: hidden; }}
  .card.lightcard {{ background: #FAF7EE; }}
  .card .title {{ padding: 10px 14px; border-bottom: 1px solid rgba(250,247,238,0.1);
                  font-size: 11px; letter-spacing: 1.2px; text-transform: uppercase;
                  color: rgba(250,247,238,0.55);
                  display: flex; justify-content: space-between; }}
  .card.lightcard .title {{ color: rgba(26,20,16,0.6); border-color: rgba(26,20,16,0.1); }}
  .card .meta {{ font-size: 9px; color: rgba(250,247,238,0.4); }}
  .card img {{ display: block; width: 100%; height: auto; }}
  .stat {{ font-size: 13px; color: rgba(250,247,238,0.7); }}
  .stat b {{ color: #FFE872; }}
  .footer {{ margin-top: 64px; padding-top: 16px; border-top: 1px solid rgba(250,247,238,0.1);
              font-size: 12px; color: rgba(250,247,238,0.55); text-align: center; line-height: 1.7; }}
  .anim {{ background: #0E0B07; border-radius: 8px; padding: 24px; max-width: 600px; margin: 0 auto; }}
  .anim svg {{ display: block; width: 100%; height: auto; }}
  .fav-strip {{ display: flex; align-items: center; gap: 14px; padding: 18px;
                background: #FAF7EE; border-radius: 6px; }}
  .fav-strip img {{ display: block; }}
  .fav-strip .label {{ color: #1A1410; font-size: 11px; }}
  code {{ font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 11px;
          background: rgba(250,247,238,0.08); padding: 1px 6px; border-radius: 3px; }}
</style>
</head>
<body>

<h1>MONTAGESUBS · BRAND ASSET</h1>
<p class="sub">蒙太奇字幕组 · 用爱发电 · POWERED BY LOVE</p>

<h2>① Master logos</h2>
<div class="row four">
  {card("Dark master · 锁定", m_dark, "m-mark-dark.png")}
  {card("Light · rounded ★默认", m_light_round, "m-mark-light.png", lightcard=True)}
  {card("Light · circle 头像", m_light_circle, "m-mark-light-circle.png", lightcard=True)}
  {card("Light · square 印刷", m_light_square, "m-mark-light-square.png", lightcard=True)}
</div>

<h2>② Wordmark lockup ×4</h2>
<div class="row two">
  {card("Horizontal · dark", lockup_h_dark, "header / nav / 视频片头")}
  {card("Horizontal · light", lockup_h_light, "header / nav / 视频片头", lightcard=True)}
</div>
<div class="row two" style="margin-top:16px">
  {card("Stacked · dark", lockup_s_dark, "海报 / 封面 / 中心点")}
  {card("Stacked · light", lockup_s_light, "海报 / 封面 / 中心点", lightcard=True)}
</div>

<h2>③ Mono · 10 个单色矢量变体</h2>
<div class="row five">
"""
for slug in ["m-mono-yellow-on-ink", "m-mono-ink-on-mist", "m-mono-knockout-yellow",
             "m-mono-knockout-ink", "m-mono-white-on-ink"]:
    img = mono_imgs.get(slug, "")
    if img:
        is_light = "mist" in slug
        HTML += card(slug.replace("m-mono-", ""), img, "logos/mono/", lightcard=is_light)
HTML += "</div>"
HTML += '<div class="row five" style="margin-top:16px">'
for slug in ["m-mono-yellow", "m-mono-black", "m-mono-white", "m-mono-true-black", "m-mono-black-on-mist"]:
    img = mono_imgs.get(slug, "")
    if img:
        is_light = "mist" in slug
        HTML += card(slug.replace("m-mono-", ""), img, "logos/mono/", lightcard=is_light)
HTML += "</div>"

HTML += f"""

<h2>④ Favicon · 11 sizes + .ico + manifest</h2>
<div class="fav-strip">
  <img src="{fav_thumbs[16]}" width="16" alt="16"><span class="label">16</span>
  <img src="{fav_thumbs[32]}" width="32" alt="32"><span class="label">32</span>
  <img src="{fav_thumbs[48]}" width="48" alt="48"><span class="label">48</span>
  <img src="{fav_thumbs[64]}" width="64" alt="64"><span class="label">64</span>
  <img src="{fav_thumbs[128]}" width="100" alt="128"><span class="label">128</span>
  <img src="{fav_thumbs[256]}" width="160" alt="256"><span class="label">256</span>
  <span class="label" style="margin-left:auto;color:#1A1410">+ 96 / 180 / 192 / 384 / 512 + favicon.ico + apple-touch-icon + manifest</span>
</div>

<h2>⑤ Social avatars + banners</h2>
<div class="row two">
  {card("Avatar · square 1080", app_avatar_sq, "social/avatar-square-1080.png")}
  {card("Avatar · circle 800", app_avatar_circ, "social/avatar-circle-800.png")}
</div>
<div class="row two" style="margin-top:16px">
  {card("Banner · 1500×500 (X / Discord)", app_banner, "social/banner-1500x500.png")}
  {card("Banner · YouTube 2560×1440", app_banner_yt, "social/banner-youtube-2560x1440.png")}
</div>

<h2>⑥ PPT cover · 1920×1080</h2>
<div class="row two">
  {card("PPT cover · dark", app_ppt_dark, "ppt-cover/ppt-cover-dark.png")}
  {card("PPT cover · light", app_ppt_light, "ppt-cover/ppt-cover-light.png", lightcard=True)}
</div>

<h2>⑦ Stationery · letterhead + business card</h2>
<div class="row two">
  {card("Letterhead · dark", app_letter_dark, "A4 · 2480×3508 @ 300dpi")}
  {card("Letterhead · light", app_letter_light, "A4 · 2480×3508 @ 300dpi", lightcard=True)}
</div>
<div class="row four" style="margin-top:16px">
  {card("Card · dark · front", app_card_dark_front, "90×54mm")}
  {card("Card · dark · back", app_card_dark_back, "90×54mm")}
  {card("Card · light · front", app_card_light_front, "90×54mm", lightcard=True)}
  {card("Card · light · back", app_card_light_back, "90×54mm", lightcard=True)}
</div>

<h2>⑧ Video subtitle bug · 台标</h2>
<div class="row three">
  {card("Yellow M + shadow", vbug_yellow, "video-bug-yellow.svg")}
  <div class="card" style="display:flex;align-items:center;justify-content:center;padding:24px;color:rgba(250,247,238,0.5);font-size:12px;line-height:1.6">
    <div>
      Bottom-right corner · 5% margin from edge.<br>
      1080p video → 80–120 px.<br>
      4K video → 160–240 px.<br><br>
      White M variant for bright video bg.<br>
      Wordmark variant for credit bug.
    </div>
  </div>
  <div class="card" style="display:flex;align-items:center;justify-content:center;padding:24px;color:rgba(250,247,238,0.5);font-size:12px;line-height:1.6">
    <div>3 SVG variants in<br><code>applications/video-bug/</code></div>
  </div>
</div>

<h2>⑨ Animated logo · neon turn-on (2.5s)</h2>
<div class="row two">
  <div class="anim">
    <img src="{animated_webp}" alt="neon on" style="width:100%;height:auto;display:block">
  </div>
  <div class="card" style="padding:24px;color:rgba(250,247,238,0.7);font-size:13px;line-height:1.7">
    <div>
      <b style="color:#FFE872">v2 · 真照片帧动画</b><br><br>
      用 dark master 真实照片，按霓虹通电的 flicker 模式（dim → 闪烁 → 稳定）调整逐帧亮度。
      M 永远是品牌那张照片，不再用矢量替代。<br><br>
      <b style="color:#FFE872">5 种格式</b>：HTML / WebP / GIF / APNG / SVG-SMIL<br>
      详见 <code>applications/animated/</code>
    </div>
  </div>
</div>
<div class="row" style="margin-top:16px">
  {card("5 个亮度档采样（off → first flicker → mid → near full → stable）", animated_frames_sample, "frame strip")}
</div>

<h2>⑩ Guidelines · clearspace / min-size / misuse / colors</h2>
<div class="row two">
  {card("Clearspace · 安全间距", clearspace, "clearspace.svg", lightcard=True)}
  {card("Min size · 最小尺寸", minsize, "minsize.svg", lightcard=True)}
</div>
<div class="row two" style="margin-top:16px">
  {card("Misuse · 错误用法", misuse, "misuse.svg", lightcard=True)}
  {card("Colors · 配色规范", colors, "colors.svg", lightcard=True)}
</div>

<h2>⑪ Brand guide</h2>
<div class="card" style="padding:24px">
  <p class="stat">完整品牌手册（11 章节）：<code>guidelines/BRAND.md</code></p>
  <p class="stat">章节：身份 · Logo 系统 · 配色 · 字体 · 安全间距 · 最小尺寸 · 错误用法 · 应用模板 · 文件索引 · 许可</p>
</div>

<div class="footer">
  <b style="color:#FAF7EE">交付清单</b><br><br>
  Master ×8 · Mono ×10 · Lockup ×4 · Favicon ×11 + .ico + manifest · Social ×8 · Video bug ×3<br>
  PPT cover ×2 · Stationery ×6 · Animated ×2 · Guidelines ×4 · BRAND.md · README.md<br><br>
  全部文件位置见 <code>README.md</code> · 完整规范见 <code>guidelines/BRAND.md</code><br><br>
  <span style="font-size:11px">蒙太奇字幕组 · MontageSubs · 用爱发电 ❤️ Powered by Love</span>
</div>

</body>
</html>
"""

(ROOT / "preview/00-final-overview.html").write_text(HTML)
print(f"wrote preview/00-final-overview.html ({len(HTML)/1024:.1f} KB)")
