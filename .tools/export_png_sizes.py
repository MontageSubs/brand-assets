"""Render PNGs at all standard sizes from new dark + light masters.
Replaces the old logos/png/ contents with files derived from the new locked masters.
"""

from pathlib import Path
from PIL import Image

ROOT = Path("/Users/wesleywu/Desktop/Wesley_personal/鼓捣鼓捣/brand-assets-main")
MASTER = ROOT / "logos/master"
PNG = ROOT / "logos/png"

(PNG / "app").mkdir(parents=True, exist_ok=True)
(PNG / "web").mkdir(parents=True, exist_ok=True)
(PNG / "hires").mkdir(parents=True, exist_ok=True)

dark = Image.open(MASTER / "m-mark-dark.png").convert("RGB")
transp = Image.open(MASTER / "m-mark-transparent.png").convert("RGBA")
light_round = Image.open(MASTER / "m-mark-light-rounded.png").convert("RGB")

# App-icon sizes (used in OS app icon contexts)
app_sizes = [128, 180, 192, 256, 384, 512, 1024, 2048]
for s in app_sizes:
    dark.resize((s, s), Image.LANCZOS).save(PNG / "app" / f"logo-{s}.png", optimize=True)
print(f"app/: {len(app_sizes)} sizes (dark master)")

# Web sizes (used inline on dark websites — keep dark master)
web_sizes = [200, 400, 600, 800, 1200, 1600]
for s in web_sizes:
    dark.resize((s, s), Image.LANCZOS).save(PNG / "web" / f"logo-{s}.png", optimize=True)
print(f"web/: {len(web_sizes)} sizes (dark master)")

# Light versions (separate filenames so they're discoverable)
for s in [200, 400, 600, 800, 1200, 1600]:
    light_round.resize((s, s), Image.LANCZOS).save(PNG / "web" / f"logo-light-{s}.png", optimize=True)
print(f"web/: + 6 light versions (rounded token)")

# Hi-res (keep masters at full 2560)
dark.save(PNG / "hires" / "logo-black-2560.png", optimize=True)
light_round.save(PNG / "hires" / "logo-light-2560.png", optimize=True)
transp.save(PNG / "hires" / "logo-transparent-2560.png", optimize=True)
print(f"hires/: 3 PNGs (2560×2560)")

# Keep old 2924 raw for archival
print(f"keeping logos/png/hires/logo-*-2924.png as archival source files")
