# logos/

核心 logo 文件。顶层导航：[`../README.md`](../README.md)。完整品牌规范：[`../guidelines/BRAND.md`](../guidelines/BRAND.md)。

<div align="right">

**中文 | [English](./README.md)**

</div><br/>

## 快速参考

| 我想要 | 用这个 |
|---|---|
| 深色页面 · 视频 · 深色 app 图标 | [`master/m-mark-dark.png`](master/m-mark-dark.png) |
| 浅色页面 · 网站 hero · 浅色文档 | [`master/m-mark-light.png`](master/m-mark-light.png) |
| 圆形社媒头像 | [`master/m-mark-light-circle.png`](master/m-mark-light-circle.png) |
| 直角方形（印刷、招牌） | [`master/m-mark-light-square.png`](master/m-mark-light-square.png) |
| 浏览器 favicon 全套 | [`favicon/`](favicon/) |
| 单色印刷 / 绣花 / 激光雕刻 | [`mono/`](mono/) |
| 字标（M + 蒙太奇字幕组 / MontageSubs） | [`lockup/`](lockup/) |
| 各尺寸位图导出 | [`png/`](png/) |
| 原始照片 + 许可证 | [`source/`](source/) |

## 子目录说明

### `master/` —— 锁定的 master logos

品牌核心，下游所有变体都从它派生。

- **`m-mark-dark.png`** —— 源照片以原生 2924px 分辨率居中放在 2560×2560 深墨（`#0E0B07`）画布上，**零后处理**（"RAW"）。这就是品牌。
- **`m-mark-light.png`** —— 默认 light master = M 嵌在深色圆角 token 里，浮在暖米白（`#FAF7EE`）页面上。等同于 `m-mark-light-rounded.png`。
- **`m-mark-light-{rounded,circle,square}.png`** —— 三种 token 形态适配不同浅色场景。
- **`m-mark-transparent.png`** —— 透明底版本，用于合成到自定义布局。
- **`m-geom-base.svg`** —— 平滑后的 M 几何（Catmull-Rom 路径，~5KB d-string）。给 mono 变体和动效用。

每个 PNG 都配同名 `.svg` 包装（PNG 以 base64 内联，自包含——一个文件搞定，无外部依赖）。

### `mono/` —— 单色矢量变体

10 个 SVG 变体，用于无法渲染照片质感的场景（绣花、单色印刷、激光雕刻、传真、极小 UI mark）：

```
m-mono-black.svg            ink (#1A1410) 透明底
m-mono-white.svg            白色透明底
m-mono-yellow.svg           品牌黄 (#FBC100) 透明底
m-mono-true-black.svg       纯黑 (#000000) 给印刷/绣花

m-mono-yellow-on-ink.svg    预合成：黄 M 深墨底
m-mono-ink-on-mist.svg      预合成：ink M 米白底
m-mono-white-on-ink.svg     预合成：白 M 深墨底
m-mono-black-on-mist.svg    预合成：纯黑 M 米白底

m-mono-knockout-yellow.svg  黄底，M 透出（透明 M）
m-mono-knockout-ink.svg     深墨底，M 透出
```

### `lockup/` —— 字标 lockup

4 种组合：`{horizontal, stacked} × {dark, light}`。每个 lockup 含三层文字（英文 / 中文 / tagline）。PNG 印刷分辨率，SVG 包装自包含。

### `favicon/` —— favicon 全家桶

- 11 个 PNG 尺寸：16, 32, 48, 64, 96, 128, 180, 192, 256, 384, 512
- `favicon.ico`（多分辨率：16/32/48）
- `apple-touch-icon.png`（180px）
- `manifest.webmanifest` 给 PWA 用
- `html-snippet.html` —— 复制粘贴进 `<head>` 的 snippet

### `png/` —— 各尺寸位图导出

从 master 文件派生。不需要 SVG 时用这些。

```
png/app/    128 / 180 / 192 / 256 / 384 / 512 / 1024 / 2048    (dark master)
png/web/    200 / 400 / 600 / 800 / 1200 / 1600                (dark master)
            + 对应 logo-light-{size}.png 变体                   (rounded token)
png/hires/  logo-{black,light,transparent}-2560.png            (master 全尺寸)
            + 归档保留的 logo-*-2924.png 原始源
```

### `source/` —— 原始资源 + 许可证

不要修改——这是品牌起源：

- `original.jpg` —— Zacharie Elbaz 的 Unsplash 照片
- `LICENSE.md` —— Unsplash License
- `README.md` / `README.zh-hans.md` —— 来源说明

---

完整的安全间距、最小尺寸、错误用法、配色 token 规范，见 [`../guidelines/`](../guidelines/)。
