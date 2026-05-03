# logos/

Core logo files. Top-level guide: [`../README.md`](../README.md). Full brand spec: [`../guidelines/BRAND.md`](../guidelines/BRAND.md).

<div align="right">

**[中文](./README.zh-hans.md) | English**

</div><br/>

## Quick reference

| Want | File |
|---|---|
| Dark page · video · OS dark icon | [`master/m-mark-dark.png`](master/m-mark-dark.png) |
| Light page · web hero · light docs | [`master/m-mark-light.png`](master/m-mark-light.png) |
| Round social avatar | [`master/m-mark-light-circle.png`](master/m-mark-light-circle.png) |
| Hard square (print, signage) | [`master/m-mark-light-square.png`](master/m-mark-light-square.png) |
| Browser favicon set | [`favicon/`](favicon/) |
| Mono single-color (embroidery, etching) | [`mono/`](mono/) |
| Wordmark lockup (M + 蒙太奇字幕组 / MontageSubs) | [`lockup/`](lockup/) |
| Hi-res raster exports | [`png/`](png/) |
| Original photo + license | [`source/`](source/) |

## Subdirectory map

### `master/` — locked master logos

The canonical brand logos. Everything downstream derives from these.

- **`m-mark-dark.png`** — source photo at native 2924px resolution, centered on a 2560×2560 deep-ink (`#0E0B07`) canvas, **zero post-processing** ("RAW"). The brand.
- **`m-mark-light.png`** — default light master = M inside a deep rounded-square token, on warm cream (`#FAF7EE`). Same as `m-mark-light-rounded.png`.
- **`m-mark-light-{rounded,circle,square}.png`** — three token shapes for different light contexts.
- **`m-mark-transparent.png`** — M on alpha background (no bg fill); for compositing into custom layouts.
- **`m-geom-base.svg`** — smoothed M geometry (Catmull-Rom path, ~5KB d-string). Used as the source for the mono variants and the animated logo.

Every PNG ships with a same-name `.svg` wrapper that embeds the PNG as base64, so the SVG is self-contained (one file, no external resources).

### `mono/` — single-color vector variants

Ten SVG variants of the M silhouette for contexts where photographic gradient is impossible (embroidery, single-color printing, laser etching, fax, very small UI).

```
m-mono-black.svg            ink (#1A1410) on transparent
m-mono-white.svg            white on transparent
m-mono-yellow.svg           brand yellow (#FBC100) on transparent
m-mono-true-black.svg       true black (#000000) for print/embroidery

m-mono-yellow-on-ink.svg    pre-composed: yellow M on deep-ink tile
m-mono-ink-on-mist.svg      pre-composed: ink M on mist tile
m-mono-white-on-ink.svg     pre-composed: white M on deep-ink tile
m-mono-black-on-mist.svg    pre-composed: true black M on mist tile

m-mono-knockout-yellow.svg  yellow tile with M cut out (transparent M)
m-mono-knockout-ink.svg     ink tile with M cut out
```

### `lockup/` — wordmark lockups

Four lockup combinations: `{horizontal, stacked} × {dark, light}`. Each lockup has three text layers (English / Chinese / tagline). PNGs at print resolution; SVG wrappers self-contained.

### `favicon/` — favicon family

- 11 PNG sizes: 16, 32, 48, 64, 96, 128, 180, 192, 256, 384, 512
- `favicon.ico` (multi-resolution: 16/32/48)
- `apple-touch-icon.png` (180px)
- `manifest.webmanifest` for PWA
- `html-snippet.html` — copy-paste snippet for `<head>`

### `png/` — raster exports at common sizes

Derived from the master files. Use these when you don't need SVG.

```
png/app/    128 / 180 / 192 / 256 / 384 / 512 / 1024 / 2048    (dark master)
png/web/    200 / 400 / 600 / 800 / 1200 / 1600                (dark master)
            + matching logo-light-{size}.png variants            (rounded token)
png/hires/  logo-{black,light,transparent}-2560.png             (master at full size)
            + archived logo-*-2924.png from original source
```

### `source/` — original asset + license

Don't modify these. They are the brand origin:

- `original.jpg` — Zacharie Elbaz's Unsplash photo
- `LICENSE.md` — Unsplash License
- `README.md` / `README.zh-hans.md` — provenance

---

For detailed clearspace, min-size, misuse rules, and color tokens, see [`../guidelines/`](../guidelines/).
