# Logos

蒙太奇字幕社区（MontageSubs）的标志及各版本资源。

<div align="right">

**中文 | [English](./README.md)**

</div><br/>

<div align="center">

<img src="./flat/png/app/rounded/logo-128.png" alt="MontageSubs 扁平版 Logo" width="128" height="128">&nbsp;&nbsp;&nbsp;<img src="./photo/png/app/rounded/compressed/logo-128.png" alt="MontageSubs 照片版 Logo" width="128" height="128">

扁平版 · 照片版

</div><br/>

本目录存放蒙太奇字幕社区的组织标志，提供两种视觉风格和多种格式，供社区成员、贡献者和外部合作伙伴使用。

## 两种风格

| | **扁平版（flat）** | **照片版（photo）** |
|---|---|---|
| 外观 | 扁平的双色 M，墨黑 `#0E0B07` 与黄色 `#FBC100`，没有渐变和纹理 | 原始霓虹街头摄影，带有光晕、质感与层次 |
| 适合 | 网站图标、应用图标、小尺寸、界面，以及一切需要保持清晰的场景 | 大幅展示、主视觉、海报、印刷 |
| 矢量 | 单一路径，约 50 个节点，每个文件约 2 KB | 对照片的海报化描摹，约 140 KB |
| 目录 | [flat/](./flat) | [photo/](./photo) |

两种风格采用相同的目录结构，切换风格只需替换路径中的一个文件夹名。

## 快速参考

| 用途 | 推荐 | 尺寸范围 | 路径 |
|------|------|---------|------|
| 网站 favicon | 扁平版，ICO、PNG 或 SVG | 16–256 px | [flat/favicon/](./flat/favicon) 或 [flat/svg/favicon.svg](./flat/svg/favicon.svg) |
| 应用图标（iOS、Android、桌面） | 扁平版，PNG | 128–2048 px | [flat/png/app/](./flat/png/app) |
| 可安装网页应用（maskable） | 扁平版，PNG | 192、512 px | [flat/png/app/maskable/](./flat/png/app/maskable) |
| 社交媒体、网页 | PNG 或 SVG | 200–1200 px | [flat/png/web/](./flat/png/web) 或 [svg/](./flat/svg) |
| 高质量印刷或大幅展示 | 照片版，高分辨率 PNG | 2924 px | [photo/png/hires/](./photo/png/hires) |
| 缩放无限制 | SVG | 任意 | [flat/svg/](./flat/svg) 或 [photo/svg/](./photo/svg) |

## 选择建议

**先选风格。** Logo 尺寸较小、需要一眼识别时用**扁平版**；有足够空间展现光晕与质感时用**照片版**。

**再选格式。** **PNG** 提供高保真的视觉效果，适合尺寸已确定的应用场景。**SVG** 支持任意无损缩放，适合响应式设计和需要灵活适配的场景。照片版的 SVG 是简化后的矢量近似，对保真度要求最高时请优先使用 PNG。

## Logo 背景故事

蒙太奇字幕社区是一个**非营利性的在线社区**，成立于 2025 年 8 月，致力于连接影视创作者、字幕创作者与全球观众。本 Logo 最初源于巴黎地铁入口标志系统。黄色 M 灯箱由 RATP（巴黎大众运输公司）于 1970 年代采用 [[1]](https://www.ratp.fr/en/discover/coulisses/daily-life/do-you-know-how-paris-metro-signposts-have-evolved)。根据 Wikimedia Commons 的版权说明，该符号未达到版权保护所要求的原创性阈值 [[2]](https://commons.wikimedia.org/wiki/File:Metro-M.svg)。

摄影师 [Zacharie Elbaz](https://unsplash.com/@zachlba) 于 2024 年 10 月 22 日在巴黎街头拍摄了这张作品，发布在 [Unsplash](https://unsplash.com/photos/the-letter-m-is-lit-up-in-the-dark-GejUCxKwAUw)，采用 [Unsplash License](./source/LICENSE.md)。原始作品保存在 [source 目录](./source)。创始人小 p 于 2025 年 9 月下旬将该作品裁剪后用作社区头像，并于 2026 年 5 月 3 日进行了完整优化处理，包括精细裁剪、降噪修复、细节提升、背景处理、矢量化和多色版本等工作。

这张街头摄影作品完美诠释了蒙太奇字幕社区的品牌定位：

- **M** 代表 Montage（蒙太奇）的首字母，隐含 Movie（电影）的含义
- **黄色霓虹** 象征光影在黑暗中的绽放，寓意字幕的价值与意义
- **黑色背景** 具有电影感与专业氛围，体现影视制作的专业性
- **霓虹美学** 呈现独特的艺术张力，赋予社区强烈的视觉个性

**扁平版**保留了同一个倾斜、手绘感的 M，并把它精简到本质：一个形状，两种颜色。它能在 16 像素下依然清晰，也能自然融入各种界面；**照片版**则承载着原始影像的氛围。

## 目录说明

```
logos/
├── flat/
│   ├── favicon/   opaque · rounded · transparent   (ico, png)
│   ├── png/       app (rounded, square, maskable) · hires · web · watermark
│   └── svg/
├── photo/
│   ├── favicon/   opaque · transparent             (ico, png)
│   ├── png/       app (rounded, square，各含 compressed/) · hires · web
│   └── svg/
└── source/
```

### flat/

- **favicon/**：浏览器标签页图标，16–256 px，提供 ICO 和 PNG。`opaque/` 为纯墨黑背景的直角版本，`rounded/` 为带透明圆角的圆角版本，`transparent/` 仅保留黄色 M。每个 ICO 目录中还有 `favicon.ico`，包含 16、32、48 px 三种尺寸，适用于经典的 `/favicon.ico` 位置。
- **png/app/**：应用图标，128–2048 px。`rounded/` 带透明圆角，`square/` 为满铺版本，适用于由平台自行施加遮罩的场景，`maskable/`（192 与 512 px）把 M 保持在安全区之内，用于自适应图标。
- **png/hires/**：最高分辨率（2924 px），包含 `logo-black-2924.png`、`logo-white-2924.png` 和 `logo-transparent-2924.png` 三个变体。
- **png/web/**：网页用途版本，200–1200 px。
- **png/watermark/**：透明背景上带轻微投影的黄色 M（256、512、1024 px），用作视频画面水印。
- **svg/**：矢量图：
  - `logo-yellow-on-ink.svg`：主稿，黄色 M 置于方形墨黑背景上。
  - `logo-yellow.svg`：透明背景的黄色 M。
  - `logo-ink.svg`：透明背景的墨黑 M，适用于浅色底。
  - `logo-yellow-shadow.svg`：带轻微投影的黄色 M，用作视频水印（即 video bug）。
  - `favicon.svg`：为标签页尺寸裁切的圆角版本。

### photo/

- **favicon/**：浏览器标签页图标，16–256 px，提供 ICO 和 PNG。`opaque/` 为纯黑背景，`transparent/` 为透明背景。
- **png/app/**：应用图标，128–2048 px，包含 `rounded/` 与 `square/` 两个版本，各自带有 `compressed/` 目录，存放调色板优化后的文件。
- **png/hires/**：最高分辨率（2924 px），包含黑色、白色、透明背景三个变体。
- **png/web/**：网页用途版本，200–1200 px。
- **svg/**：矢量图：
  - `logo-gradient.svg`：渐变矢量版本，保留照片的核心形状与色彩。
  - `logo-detailed-black.svg`：由 `png/hires/logo-black-2924.png` 描摹得到的海报化矢量版本，约 23 种颜色。
  - `logo-detailed-transparent.svg`：同一描摹的透明背景版本，来自 `png/hires/logo-transparent-2924.png`。
  - `logo-outline-black.svg`：黑色轮廓版本，仅保留 M 形状。
  - `logo-outline-gray.svg`：灰色轮廓版本，适合浅色背景主题。
  - `logo-outline-stroke.svg`：纯描边的中空版本。

### source/

原始资源和许可证文档。包含摄影师 Zacharie Elbaz 的原始作品（original.jpg）、源文件说明和许可证信息。

## 设计说明

两种风格的 favicon 都使用两种裁切，以便在各种尺寸下都清晰易读。16 和 32 px 时，M 约占画块高度的 88%，因为小尺寸需要用尽每一个像素；从 48 px 起，以及在应用图标和网页 Logo 中，M 约占 75%，使整个 M 都落在搜索引擎和手机启动器使用的圆形与圆角遮罩之内。扁平版的 Maskable 图标则把 M 保持在自适应图标遮罩所保证的中央圆形区域内。

每个 SVG 都带有标题、说明和 Creative Commons 许可证元数据，在编辑器中打开或被辅助技术读取时能够自我说明。扁平版的 favicon 为保持精简，只包含标题和说明。

| 颜色 | 色值 |
|------|------|
| 墨黑 | `#0E0B07` |
| 黄色 | `#FBC100` |

## 目录变更

早期版本只在顶层放置一种风格。如果你曾按路径引用文件，请对照下表查找。

| 原路径 | 现路径 |
|--------|--------|
| `favicon/default/` | `photo/favicon/opaque/` |
| `favicon/transparent/` | `photo/favicon/transparent/` |
| `png/` | `photo/png/` |
| `svg/logo-abstract.svg` | `photo/svg/logo-gradient.svg` |
| `svg/logo-detailed-*.svg`、`svg/logo-outline-*.svg` | `photo/svg/` |
| `svg/m-mark-flat-on-ink.svg` | `flat/svg/logo-yellow-on-ink.svg` |
| `svg/video-bug-yellow.svg` | `flat/svg/logo-yellow-shadow.svg` |

原先的 `logo-abstract.svg` 实际上是照片的渐变矢量版本，因此改名为 `logo-gradient.svg`。照片版的 favicon 和应用图标已重新裁切，M 更大，小尺寸下更易辨认。

## 许可证

**`source/` 目录内容**采用 [Unsplash License](./source/LICENSE.md)。

**本目录下所有文件**（除 `source/` 外的所有文件和资源）采用 [**CC BY-NC-SA 4.0**](./LICENSE) 许可。您可以自由分享和改编这些作品，但需要署名、非商业使用，且衍生作品必须采用相同许可证。详见 [许可证文件](./LICENSE)。

---

<div align="center">

**蒙太奇字幕社区 (MontageSubs)**  
"用爱发电 ❤️ Powered by Love"

</div>
