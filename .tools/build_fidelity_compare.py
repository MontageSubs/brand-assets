"""Side-by-side fidelity check: original photo vs new faithful trace."""
import base64
from pathlib import Path

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")

def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(p).read_bytes()).decode("ascii")

orig = b64(ROOT / "logos/png/web/logo-600.png", "image/png")
new_dark = b64(ROOT / "logos/master/m-mark-dark.png", "image/png")
new_light = b64(ROOT / "logos/master/m-mark-light.png", "image/png")
old_trace = b64(ROOT / "preview/thumbs/m-trace-faithful.png", "image/png")

HTML = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Fidelity check</title>
<style>
  body {{ background: #1C1812; color: #FAF7EE; font: 14px/1.5 -apple-system, sans-serif;
          margin: 0; padding: 32px; }}
  h1 {{ font-size: 14px; letter-spacing: 3px; text-align: center; margin-bottom: 28px; }}
  .row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 32px; }}
  .row.three {{ grid-template-columns: 1fr 1fr 1fr; }}
  .card {{ background: #0E0B07; border: 1px solid rgba(250,247,238,0.1); border-radius: 6px;
          padding: 18px; }}
  .card.lightcard {{ background: #FAF7EE; }}
  .card .lbl {{ font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase;
                color: rgba(250,247,238,0.55); margin-bottom: 12px; text-align: center; }}
  .card.lightcard .lbl {{ color: rgba(26,20,16,0.55); }}
  .card img {{ display: block; width: 100%; height: auto; }}
  .note {{ margin-top: 24px; font-size: 12px; color: rgba(250,247,238,0.5);
           text-align: center; line-height: 1.6; }}
  h2 {{ font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
        color: rgba(250,247,238,0.55); margin: 28px 0 14px; }}
</style></head><body>
<h1>MONTAGESUBS · FIDELITY CHECK</h1>

<h2>① Original photo &nbsp;vs&nbsp; ② New polished dark master</h2>
<div class="row">
  <div class="card">
    <div class="lbl">① ORIGINAL UNSPLASH PHOTO</div>
    <img src="{orig}">
  </div>
  <div class="card">
    <div class="lbl">② NEW · POLISHED DARK MASTER (the photo, refined)</div>
    <img src="{new_dark}">
  </div>
</div>

<h2>③ Light master (same M, warm cream bg, halo restrained)</h2>
<div class="row">
  <div class="card lightcard">
    <div class="lbl">③ NEW · POLISHED LIGHT MASTER</div>
    <img src="{new_light}">
  </div>
  <div class="card" style="display:flex;align-items:center;justify-content:center;color:rgba(250,247,238,0.6);font-size:13px;line-height:1.7;text-align:left;padding:32px">
    <div>
      <b style="color:#FAF7EE">What changed since v3:</b><br><br>
      ✗ Stopped trying to vectorize the photo (poster-art crudeness).<br>
      ✓ Treat the photo AS the master — refine it, don't replace it.<br>
      ✓ Saturation +12% / contrast +6% / brightness +2%.<br>
      ✓ Tight bbox (no crop on halo).<br>
      ✓ Light master uses the same polished M, halo gamma-curved tighter so it doesn't muddy the cream surface.<br>
      ✓ Vector simplification kept ONLY for: mono single-color, favicon at 16/32px, animation. Those genuinely benefit from vector.
    </div>
  </div>
</div>

<h2>What we are NOT using (kept for the record)</h2>
<div class="row">
  <div class="card">
    <div class="lbl">✗ V2 · POSTERIZED 10-LAYER TRACE</div>
    <img src="{old_trace}">
  </div>
  <div class="card" style="display:flex;align-items:center;justify-content:center;color:rgba(250,247,238,0.5);font-size:13px;line-height:1.7;text-align:left;padding:32px">
    <div>The 10-layer trace produced flat poster-art zones, lost the<br>
    continuous tonal gradient and the diffuse glow that make a real<br>
    neon photo work. Discarded.</div>
  </div>
</div>

</body></html>
"""

(ROOT / "preview/04-fidelity-check.html").write_text(HTML)
print(f"wrote preview/04-fidelity-check.html ({len(HTML):,} bytes)")
