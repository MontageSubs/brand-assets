# Logos

Brand assets and logo resources for MontageSubs.

<div align="right">

**[中文](./README.zh-hans.md) | English**

</div><br/>

<div align="center">

<img src="./flat/png/app/rounded/logo-128.png" alt="MontageSubs flat logo" width="128" height="128">&nbsp;&nbsp;&nbsp;<img src="./photo/png/app/rounded/compressed/logo-128.png" alt="MontageSubs photo logo" width="128" height="128">

Flat · Photo

</div><br/>

This directory contains the organizational logo of MontageSubs in two visual styles and multiple formats, available for use by community members, contributors, and external partners.

## Two Styles

| | **Flat** | **Photo** |
|---|---|---|
| Look | Flat, two-colour M in ink `#0E0B07` and yellow `#FBC100`, with no gradients or texture | The original neon street photograph, with glow, texture and depth |
| Best for | Favicons, app icons, small sizes, interfaces, anything that must stay crisp | Large displays, hero images, posters, print |
| Vector | One clean path of about 50 nodes, about 2 KB per file | A posterised trace of the photograph, about 140 KB |
| Folder | [flat/](./flat) | [photo/](./photo) |

Both styles use the same layout, so switching style only means changing one folder name in a path.

## Quick Reference

| Purpose | Recommended | Size Range | Location |
|---------|-------------|-----------|----------|
| Website favicon | Flat, ICO, PNG or SVG | 16–256 px | [flat/favicon/](./flat/favicon) or [flat/svg/favicon.svg](./flat/svg/favicon.svg) |
| App icon (iOS, Android, desktop) | Flat, PNG | 128–2048 px | [flat/png/app/](./flat/png/app) |
| Installable web app (maskable) | Flat, PNG | 192, 512 px | [flat/png/app/maskable/](./flat/png/app/maskable) |
| Social media & web | PNG or SVG | 200–1200 px | [flat/png/web/](./flat/png/web) or [svg/](./flat/svg) |
| High-quality print & large displays | Photo, high-resolution PNG | 2924 px | [photo/png/hires/](./photo/png/hires) |
| Unlimited scalability | SVG | Any | [flat/svg/](./flat/svg) or [photo/svg/](./photo/svg) |

## Selection Guide

**Choose the style first.** Use **flat** wherever the logo is small or has to be recognised at a glance. Use **photo** where there is room for its glow and texture.

**Then choose the format.** **PNG** delivers high-fidelity quality and is ideal for fixed-size applications. **SVG** supports unlimited lossless scaling and is perfect for responsive design and flexible layouts. For the photo style, the SVG files are simplified vector approximations, so prefer the PNG files when fidelity matters most.

## The Story Behind Our Logo

MontageSubs is a **non-profit online subtitle community** founded in August 2025, dedicated to connecting filmmakers, subtitle creators, and audiences worldwide. Our logo draws inspiration from the iconic Paris Metro entrance signage. The distinctive yellow M letterbox was adopted by RATP (Régie Autonome des Transports Parisiens) in the 1970s [[1]](https://www.ratp.fr/en/discover/coulisses/daily-life/do-you-know-how-paris-metro-signposts-have-evolved); according to Wikimedia Commons, the underlying symbol does not meet the threshold of originality required for copyright protection [[2]](https://commons.wikimedia.org/wiki/File:Metro-M.svg).

Photographer [Zacharie Elbaz](https://unsplash.com/@zachlba) captured this image on the streets of Paris on October 22, 2024, and shared it on [Unsplash](https://unsplash.com/photos/the-letter-m-is-lit-up-in-the-dark-GejUCxKwAUw) under the [Unsplash License](./source/LICENSE.md). The original work is preserved in the [source directory](./source). Founder Meow P adapted this image as the community avatar in late September 2025, and completed comprehensive optimization on May 3, 2026, including precise cropping, noise reduction, detail enhancement, background refinement, vectorization, and multi-color variants.

This street photography perfectly embodies MontageSubs' brand identity:

- **M** represents the first letter of Montage, with implicit reference to Movie
- **Golden luminescence** symbolizes light and brilliance emerging from darkness, embodying the value and significance of subtitles
- **Black background** evokes the cinematic aesthetic and professional atmosphere of film and television production
- **Neon aesthetics** convey distinctive artistic tension, endowing the community with strong visual character

The **flat** style keeps the same slanted, hand-drawn M and reduces it to its essence: one shape, two colours. It is built to stay legible at 16 pixels and to sit comfortably in any interface, while the **photo** style carries the atmosphere of the original image.

## Directory Guide

```
logos/
├── flat/
│   ├── favicon/   opaque · rounded · transparent   (ico, png)
│   ├── png/       app (rounded, square, maskable) · hires · web · watermark
│   └── svg/
├── photo/
│   ├── favicon/   opaque · transparent             (ico, png)
│   ├── png/       app (rounded, square, each with compressed/) · hires · web
│   └── svg/
└── source/
```

### flat/

- **favicon/** — Browser favicons, 16–256 px, in ICO and PNG. `opaque/` has a solid ink background with square corners, `rounded/` has a rounded tile with transparent corners, and `transparent/` has only the yellow M. Each ICO folder also contains `favicon.ico`, a multi-size file (16, 32 and 48 px) for the classic `/favicon.ico` location.
- **png/app/** — App icons, 128–2048 px. `rounded/` has transparent corners, `square/` is full-bleed for platforms that apply their own mask, and `maskable/` (192 and 512 px) keeps the M inside the safe zone for adaptive icons.
- **png/hires/** — Highest resolution (2924 px) in three variants: `logo-black-2924.png`, `logo-white-2924.png` and `logo-transparent-2924.png`.
- **png/web/** — Web-optimised versions, 200–1200 px.
- **png/watermark/** — The yellow M with a subtle drop shadow on a transparent background (256, 512 and 1024 px), for use as an on-screen video watermark.
- **svg/** — Vector files:
  - `logo-yellow-on-ink.svg` — The master: yellow M on a square ink background.
  - `logo-yellow.svg` — Yellow M on a transparent background.
  - `logo-ink.svg` — Ink M on a transparent background, for light surfaces.
  - `logo-yellow-shadow.svg` — Yellow M with a subtle drop shadow, for use as a video watermark (also known as a video bug).
  - `favicon.svg` — Rounded tile cropped for tab-sized display.

### photo/

- **favicon/** — Browser favicons, 16–256 px, in ICO and PNG. `opaque/` has a solid black background, and `transparent/` has a transparent background.
- **png/app/** — App icons, 128–2048 px, in `rounded/` and `square/` variants, each with a `compressed/` folder of palette-optimised files.
- **png/hires/** — Highest resolution (2924 px) in black, white and transparent variants.
- **png/web/** — Web-optimised versions, 200–1200 px.
- **svg/** — Vector files:
  - `logo-gradient.svg` — Gradient vector variant that preserves the core shape and colour of the photograph.
  - `logo-detailed-black.svg` — Posterised vector trace of `png/hires/logo-black-2924.png`, about 23 colours.
  - `logo-detailed-transparent.svg` — The same trace on a transparent background, from `png/hires/logo-transparent-2924.png`.
  - `logo-outline-black.svg` — Black outline variant containing only the M shape.
  - `logo-outline-gray.svg` — Gray outline variant for light background themes.
  - `logo-outline-stroke.svg` — Stroke-only, hollow variant.

### source/

Original assets and license documentation, including photographer Zacharie Elbaz's original work (original.jpg), source file notes, and license information.

## Design Notes

Favicons in both styles use two crops so they read well at every size. At 16 and 32 px the M fills about 88% of the tile height, because small sizes need every pixel. From 48 px upward, and in app icons and web logos, it fills about 75%, which keeps the whole M inside the circular and rounded masks used by search engines and mobile launchers. Maskable icons in the flat style keep the M inside the central circle that adaptive icon masks guarantee.

Every SVG carries a title, a description and Creative Commons licence metadata, so it identifies itself when opened in an editor or read by assistive technology. The flat favicon is kept lean and carries only a title and description.

| Colour | Hex |
|--------|-----|
| Ink | `#0E0B07` |
| Yellow | `#FBC100` |

## What Moved

Earlier versions kept a single style at the top level. If you linked to files by path, use this table to find them.

| Previous path | Current path |
|---------------|--------------|
| `favicon/default/` | `photo/favicon/opaque/` |
| `favicon/transparent/` | `photo/favicon/transparent/` |
| `png/` | `photo/png/` |
| `svg/logo-abstract.svg` | `photo/svg/logo-gradient.svg` |
| `svg/logo-detailed-*.svg`, `svg/logo-outline-*.svg` | `photo/svg/` |
| `svg/m-mark-flat-on-ink.svg` | `flat/svg/logo-yellow-on-ink.svg` |
| `svg/video-bug-yellow.svg` | `flat/svg/logo-yellow-shadow.svg` |

The file formerly called `logo-abstract.svg` is a gradient vector of the photograph, so it is now `logo-gradient.svg`. Photo-style favicons and app icons were re-cropped so the M is larger and easier to read at small sizes.

## License

Content in the **`source/` directory** is licensed under the [Unsplash License](./source/LICENSE.md).

All files in this directory **except those in `source/`** are licensed under [**CC BY-NC-SA 4.0**](./LICENSE). You are free to share and adapt these works provided you give attribution, use them non-commercially, and apply the same license to derivative works. See the [LICENSE file](./LICENSE) for full details.


---

<div align="center">

**MontageSubs**  
Powered by Love ❤

</div>
