# MontageSubs · 品牌手册

蒙太奇字幕组 · 用爱发电 ❤️ Powered by Love

---

## 1. 品牌身份

| | |
|---|---|
| 中文名 | 蒙太奇字幕组 |
| 英文名 | MontageSubs |
| 成立时间 | 2025 年 8 月 |
| 性质 | 非营利在线字幕社区 |
| Tagline | 用爱发电 · Powered by Love |
| Logomark 来源 | 巴黎地铁入口 M 标志（RATP 1970s 启用，公共领域） |
| Logomark 摄影 | [Zacharie Elbaz](https://unsplash.com/@zachlba)，2024-10-22 巴黎，[Unsplash](https://unsplash.com/photos/the-letter-m-is-lit-up-in-the-dark-GejUCxKwAUw) |
| 设计核心 | 黑夜里点亮的黄色霓虹 M——光与影的"蒙太奇" |

### 1.1 Logo 背景故事

蒙太奇字幕组是一个非营利性的在线字幕社区，成立于 2025 年 8 月，致力于连接影视创作者、字幕创作者与全球观众。

本 Logo 最初源于**巴黎地铁入口标志**——黄色 M 灯箱由 RATP（巴黎大众运输公司）于 1970 年代采用 [[1]](https://www.ratp.fr/en/discover/coulisses/daily-life/do-you-know-how-paris-metro-signposts-have-evolved)。由于不满足版权保护所需的原创性阈值，该标志属于**公有领域** [[2]](https://en.wikipedia.org/wiki/Threshold_of_originality)。

摄影师 Zacharie Elbaz 于 2024 年 10 月 22 日在巴黎街头拍摄了这张作品，发布在 Unsplash，采用 Unsplash License。原始作品保存在 [`../logos/source/`](../logos/source/) 目录。创始人**小 p** 于 2025 年 9 月下旬将该作品裁剪后用作社群头像，并于 **2026 年 5 月 3 日**进行了完整优化处理，包括精细裁剪、降噪修复、细节提升、背景处理、矢量化和多色版本等工作。

这张街头摄影作品完美诠释了蒙太奇字幕组的品牌定位：

- **M** 代表 Montage（蒙太奇）的首字母，隐含 Movie（电影）的含义
- **黄色霓虹** 象征光影在黑暗中的绽放，寓意字幕的价值与意义
- **黑色背景** 具有电影感与专业氛围，体现影视制作的专业性
- **霓虹美学** 呈现独特的艺术张力，赋予组织强烈的视觉个性

---

## 2. Logo 系统

### 2.1 Master logos（核心）

| 文件 | 用途 |
|---|---|
| [`logos/master/m-mark-dark.png`](../logos/master/m-mark-dark.png) | **Dark master**——锁定的源照片在 2560×2560 画布、深墨 `#0E0B07` 底，原生 2924px 分辨率，0 处理。任何深色页面 / 视频 / app 直接使用 |
| [`logos/master/m-mark-light.png`](../logos/master/m-mark-light.png) | **Light master**（默认 = rounded token）——M 嵌在深色圆角 token 里，浮在米白 `#FAF7EE` 页面上 |
| [`logos/master/m-mark-light-rounded.png`](../logos/master/m-mark-light-rounded.png) | 圆角方 token——网站、社媒、app 图标首选 |
| [`logos/master/m-mark-light-circle.png`](../logos/master/m-mark-light-circle.png) | 圆形 token——头像 / profile picture |
| [`logos/master/m-mark-light-square.png`](../logos/master/m-mark-light-square.png) | 直角方 token——印刷、招牌、海报 |
| [`logos/master/m-mark-transparent.png`](../logos/master/m-mark-transparent.png) | 透明底版本——给后续合成用 |

每个 PNG 都配有同名 `.svg`（PNG 以 base64 内联，自包含）。

### 2.2 设计哲学：M 永远住在它的"夜"里

霓虹只有在黑暗里才"亮"——把 dark master 的照片直接放在白底，halo 和案体阴影会糊成一片黄雾，霓虹味立刻消失。所以**我们不重新着色 M**，而是给浅色场景配一个深色 token 作为它的"夜"。

| 场景 | 用什么 |
|---|---|
| 深色页面 / 视频 / 黑底海报 | `m-mark-dark.png`（M + 黑底） |
| 浅色页面 / 网站 hero / 浅底文档 | `m-mark-light-rounded.png`（深 token + M） |
| 圆形社媒头像 | `m-mark-light-circle.png` |
| 印刷直角场景 | `m-mark-light-square.png` |
| 单色印刷 / 绣花 / 激光雕刻 | `logos/mono/m-mono-*.svg`（矢量单色） |
| favicon 16/32px | `logos/favicon/favicon-*.png` |
| 动效（霓虹通电） | `applications/animated/animated-neon-on.svg` |

### 2.3 Mono 单色矢量

[`logos/mono/`](../logos/mono/) 共 10 个变体：

- 透明底：`m-mono-{black,white,yellow,true-black}.svg`
- 已合成：`m-mono-{yellow-on-ink,ink-on-mist,white-on-ink,black-on-mist}.svg`
- Knockout（M 透出）：`m-mono-knockout-{yellow,ink}.svg`

用于不能渲染照片质感的所有场景（绣花、激光雕刻、单色印刷、传真）。

### 2.4 Lockup 字标

[`logos/lockup/`](../logos/lockup/)：

- `lockup-horizontal-{dark,light}.{png,svg}` — M 左 + 文字右，header 用
- `lockup-stacked-{dark,light}.{png,svg}` — M 上 + 文字下，海报 / 封面用

每个 lockup 含三层文字：
1. `MontageSubs`（Helvetica Bold）
2. `蒙太奇字幕组`（PingFang SC Medium）
3. `用爱发电 · POWERED BY LOVE`（PingFang SC Regular，60% 不透明度）

---

## 3. 配色规范

完整规范图：[`colors.svg`](./colors.svg)

### 3.1 11 色 brand tokens

| Token | HEX | RGB | 用途 |
|---|---|---|---|
| `ink-deep` | `#0E0B07` | 14, 11, 7 | Dark mode 主背景 |
| `ink-soft` | `#1A1410` | 26, 20, 16 | 浅底上的单色 M 填充 |
| `amber-bk` | `#3D1800` | 61, 24, 0 | 案体最深处阴影 |
| `amber-dk` | `#7A3D00` | 122, 61, 0 | 案体中段 |
| `amber-deep` | `#A85B00` | 168, 91, 0 | 案体亮边 |
| `amber` | `#FCAB02` | 252, 171, 2 | 中段琥珀 |
| **`yellow ★`** | **`#FBC100`** | **251, 193, 0** | **★ 主品牌黄——单色复刻必用** |
| `yellow-lit` | `#FDD338` | 253, 211, 56 | 灯管亮面 |
| `glow-high` | `#FFE872` | 255, 232, 114 | 外发光带 |
| `core-white` | `#FFFCE0` | 255, 252, 224 | 灯管核心 |
| `mist` | `#FAF7EE` | 250, 247, 238 | Light mode 主背景（暖米白） |

### 3.2 配色使用建议

- **任何"单色复刻"必用 `#FBC100`**（金箔印刷、绣花、激光、车贴、街头招牌）
- **Dark mode 主底必用 `#0E0B07`**——不要用纯黑 `#000000`，会让 M 的霓虹显得发灰
- **Light mode 主底必用 `#FAF7EE`**——不要用纯白 `#FFFFFF`，黄霓虹在纯白底会发灰
- 文字在深底 = `#FAF7EE`，在浅底 = `#1A1410`（不用纯黑）

---

## 4. 字体规范

| | 主字体（Canonical） | Fallback Stack |
|---|---|---|
| 中文 | **思源黑体 / Source Han Sans / Noto Sans CJK SC** | `"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui` |
| 英文 | **Inter** 或 **Helvetica** | `"Helvetica Neue", "Helvetica", system-ui, -apple-system, sans-serif` |

字号建议：

| 用途 | EN 字号 | CN 字号 |
|---|---|---|
| Logotype | 88-130 px Bold | 60-88 px Medium |
| 副标题 | 36-44 px Regular | 36-44 px Regular |
| Tagline | 22-28 px Regular | 22-28 px Regular |
| 正文 | 14-16 px Regular | 14-16 px Regular |

CSS 推荐：

```css
/* English */
font-family: "Inter", "Helvetica Neue", "Helvetica", system-ui, -apple-system, sans-serif;
font-feature-settings: "ss01" on, "cv11" on; /* Inter 推荐 */

/* Chinese */
font-family: "Noto Sans CJK SC", "Source Han Sans CN", "PingFang SC",
             "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif;
```

---

## 5. 安全间距 · 最小尺寸 · 错误用法

| 规范 | 文件 |
|---|---|
| 安全间距（X = M 高 ÷ 4） | [`clearspace.svg`](./clearspace.svg) |
| 最小尺寸（按用途） | [`minsize.svg`](./minsize.svg) |
| 错误用法（6 种禁止） | [`misuse.svg`](./misuse.svg) |

### 6 种错误用法（关键）

1. ✗ 拉伸 / 压扁——M 必须保持原始比例
2. ✗ 自由旋转——M 的左倾角度是设计的一部分，不要再旋转
3. ✗ 改色——主品牌黄 `#FBC100` 不能换成其他颜色
4. ✗ 加效果——drop shadow / outline / glow 不要叠加（master 已经包含）
5. ✗ 改成线框——M 是实心填充
6. ✗ 嘈杂背景——M 周围至少留 X 安全间距，不能压在花纹 / 渐变 / 照片上

### 最小尺寸

| 用途 | 最小尺寸 |
|---|---|
| 网站 header / 导航 | ≥ 64 px |
| 社媒头像 | ≥ 256 px |
| 视频台标 / 字幕水印 | ≥ 80 px @ 1080p |
| PPT / 演示封面 | ≥ 200 px |
| 名片 / 信纸 | ≥ 18 mm |
| 绣花 / 单色印刷 | ≥ 25 mm（用 mono 矢量） |
| 浏览器 favicon | 16-32 px（用 favicon set） |

---

## 6. 应用模板

### 6.1 社媒 [`applications/social/`](../applications/social/)

- `avatar-square-{1080,1500}.png`——通用方形头像
- `avatar-circle-{400,800,1080}.png`——圆形头像
- `banner-1500x500.png`——X / Twitter / Discord 横幅
- `banner-x-twitter.png`——同上
- `banner-youtube-2560x1440.png`——YouTube 频道头图（含安全区域居中）

### 6.2 视频台标 [`applications/video-bug/`](../applications/video-bug/)

- `video-bug-yellow.svg`——黄 M + 投影，用于浅底视频
- `video-bug-white.svg`——白 M + 投影，用于杂色背景
- `video-bug-wordmark.svg`——M + MontageSubs + 蒙太奇字幕组，bottom-corner 长版

放置建议：右下角，距边缘 5%；@ 1080p 视频用 80-120px；@ 4K 视频用 160-240px。

### 6.3 PPT [`applications/ppt-cover/`](../applications/ppt-cover/)

- `ppt-cover-dark.png`（1920×1080）——深底封面
- `ppt-cover-light.png`（1920×1080）——浅底封面

PowerPoint / Keynote 直接拖入封面 slide 当背景。文字层（标题、作者、日期）在 PowerPoint 里用 PingFang SC Medium / Helvetica Bold 自行覆盖。

### 6.4 信纸 + 名片 [`applications/stationery/`](../applications/stationery/)

- `letterhead-{dark,light}.png`（A4 portrait, 2480×3508 @ 300dpi）
- `business-card-{dark,light}-front.png`（90×54mm @ 300dpi → 1080×648）
- `business-card-{dark,light}-back.png`——含联系信息

打印输出：CMYK 模式，300 dpi，无出血。

### 6.5 动效 [`applications/animated/`](../applications/animated/)

**做法**：用 dark master 真实照片做帧动画，按真实霓虹通电的 flicker 模式（off → 微闪 → 稳定）调整逐帧亮度。**M 永远是品牌那张照片，不用矢量替代**。

5 种格式覆盖所有用法：

| 格式 | 大小 | 用途 |
|---|---|---|
| `animated-neon-on.html` | ~1.7 MB | 浏览器播放（CSS filter on `<img>`），含 ▶ Replay 按钮 |
| `animated-neon-on.webp` | ~370 KB | ★ 推荐 —— 现代浏览器、GitHub README、Notion 首选 |
| `animated-neon-on.gif` | ~3.8 MB | 老 markdown / 不支持 WebP 的 viewer |
| `animated-neon-on.apng` | ~5.9 MB | 无损动画（高质量保留） |
| `animated-neon-on.svg` | ~1.7 MB | SVG SMIL（嵌入照片 + opacity 动画） |

参数：720×720, 24 fps, 2.5 s, 60 帧 + 12 帧静止保留。

**Markdown 嵌入**：
```markdown
![MontageSubs neon on](applications/animated/animated-neon-on.webp)
```

**视频片头制作**：
1. 浏览器打开 `animated-neon-on.html`
2. QuickTime / OBS / ffmpeg 屏幕录制 2.5 s
3. 输出 ProRes / H.264，导入 NLE

---

## 7. 文件索引（一图全 view）

```
brand-assets-main/
├── BRAND.md ← 你正在看
├── README.md
├── logos/
│   ├── master/
│   │   ├── m-mark-dark.{png,svg}                  ← Dark master 锁定
│   │   ├── m-mark-light.{png,svg}                 ← Light master 默认
│   │   ├── m-mark-light-{rounded,circle,square}.{png,svg}
│   │   ├── m-mark-transparent.{png,svg}
│   │   └── m-geom-base.svg                        ← 矢量轮廓基底
│   ├── mono/
│   │   └── m-mono-*.svg                           ← 10 个单色变体
│   ├── lockup/
│   │   └── lockup-{horizontal,stacked}-{dark,light}.{png,svg}
│   └── favicon/
│       ├── favicon-{16,32,48,64,96,128,180,192,256,384,512}.png
│       ├── favicon.ico
│       ├── apple-touch-icon.png
│       ├── manifest.webmanifest
│       └── html-snippet.html
├── applications/
│   ├── social/                                    ← 社媒 8 个文件
│   ├── video-bug/                                 ← 视频台标 3 个 SVG
│   ├── ppt-cover/                                 ← PPT 封面 dark + light
│   ├── stationery/                                ← 信纸 + 名片 dark + light
│   └── animated/                                  ← 霓虹通电动效
└── guidelines/
    ├── BRAND.md
    ├── clearspace.svg
    ├── minsize.svg
    ├── misuse.svg
    └── colors.svg
```

---

## 8. 许可

logo 源自 [Zacharie Elbaz @ Unsplash](https://unsplash.com/photos/the-letter-m-is-lit-up-in-the-dark-GejUCxKwAUw)，遵循 Unsplash License（商用 / 非商用自由使用，无需署名）。

整套 brand asset 在该 logo 基础上由蒙太奇字幕组重制，沿用相同 Unsplash License。

---

**蒙太奇字幕组 · 用爱发电 ❤️ Powered by Love**
