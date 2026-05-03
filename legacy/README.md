# Legacy assets

These directories contain the **pre-redesign** brand assets. They are kept
for reference / git history but **should not be used** in any new context.

| Legacy | What replaces it |
|---|---|
| `svg/logo-detailed-black.svg` (~1MB) and `logo-detailed-transparent.svg` | These were bitmap-traced from the photo, with edge jitter and large file size. Replaced by `logos/master/m-mark-{dark,transparent}.svg` (the photo embedded as base64 inside an SVG wrapper, the canonical way to deliver the photo-based master). |
| `svg/logo-outline-{black,gray,stroke}.svg` | Replaced by `logos/master/m-geom-base.svg` (smoothed Catmull-Rom path, ~5KB d-string) and the `logos/mono/` family. |
| `svg/logo-abstract.svg` | Same path as outline + a radial gradient — superseded by `logos/master/m-mark-dark.svg`. |
| `animated/` (was empty) | Replaced by `applications/animated/`. |
| `usage/` (was empty) | Replaced by `guidelines/`. |
| `favicon/default/` and `favicon/transparent/` (legacy nested layout) | Replaced by the flat `logos/favicon/` directory with a complete size set + `.ico` + `manifest.webmanifest` + HTML snippet. |
| `png-app-compressed/` (extra optimized copies of original png/app sizes) | The new `logos/png/app/` set is already compressed via PIL `optimize=True`. |

**Reason for keeping**: useful as reference if you need to see what the
original repo state looked like before the May 2026 brand asset redesign,
or if any external integration was hard-coded against the old paths.

**Anything you build now**: use the live directories
(`logos/`, `applications/`, `guidelines/`). Never link into `legacy/`.

## master-stale/

Files that lived briefly in `logos/master/` during the iteration where we
were trying to deliver flat / abstract / 10-layer-trace renderings. After
the photo-as-brand decision (see top-level README §"设计哲学"), these
are dead. Kept here in case anyone wants to see the failed attempts.

| File | Why moved |
|---|---|
| `m-mark-flat-*.svg` | Flat geometric M used during the v1 abstract pass — replaced by `logos/mono/`. |
| `m-mark-knockout.svg` | Same era — replaced by `logos/mono/m-mono-knockout-*.svg`. |
| `m-trace-faithful.svg` | The 10-layer poster-art trace (the "粗糙不能更粗糙" version). |
