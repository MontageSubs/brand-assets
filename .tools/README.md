# Build scripts

Run order to reproduce all brand assets from scratch (assuming
`logos/source/original.jpg` and `logos/png/hires/logo-transparent-2924.png`
are present):

```bash
# 1. Geometry base — smoothed M outline (input for mono / animated)
python3 .tools/smooth_path.py

# 2. Master logos
python3 .tools/finalize_dark_raw.py     # Dark master (RAW photo, locked)
python3 .tools/polish_light_token.py    # Light master (dark token approach)

# 3. Mono single-color variants
python3 .tools/build_mono.py

# 4. Wordmark lockups
python3 .tools/build_lockup.py

# 5. Favicons (uses light-rounded as source)
python3 .tools/build_favicon.py

# 6. Application templates (social / video bug / PPT / stationery)
python3 .tools/build_applications.py

# 7. Animated logo
python3 .tools/build_animated_v2.py

# 8. Guidelines spec sheets
python3 .tools/build_guidelines.py

# 9. Raster exports at standard sizes
python3 .tools/export_png_sizes.py

# 10. Final overview HTML (depends on everything above)
python3 .tools/build_final_overview.py
```

## Active vs deprecated

**Active** (used in the live build pipeline above):

```
smooth_path.py
finalize_dark_raw.py
polish_light_token.py
build_mono.py
build_lockup.py
build_favicon.py
build_applications.py
build_animated_v2.py
build_guidelines.py
export_png_sizes.py
build_final_overview.py
```

**Deprecated** (kept for reference / git history of decisions):

```
build_masters.py        — early v1 abstract masters (replaced by finalize_dark_raw + polish_light_token)
build_animated.py       — v1 vector-based animation (replaced by v2 photo-based)
build_overview.py       — v1 overview (replaced by build_final_overview.py)
build_zoom_compare.py   — v2 sharpening QA (one-off, not part of pipeline)
build_zoom_compare_v3.py — v3 sharpening QA (one-off)
build_fidelity_compare.py — fidelity check between iterations (one-off)
photo_trace.py          — failed 10-layer poster trace (the "粗糙不能更粗糙" version)
polish_photo.py         — v1 photo polish (replaced by finalize_dark_raw)
polish_dark_v2.py       — v2 sharpening pass (rejected: 过度锐化 + 强行对比度)
polish_dark_v3.py       — v3 three-way comparison (RAW chosen)
polish_light_off.py     — 关灯版 light master (rejected by user, scheme ① picked)
```

## Dependencies

```
python3 -m pip install --user pillow numpy scipy scikit-image
brew install librsvg            # for batch SVG→PNG conversion
```

(macOS `qlmanage` is also used for one-off SVG previews.)
