# 分鏡 spec.json 格式

整支動畫就是一個 JSON。頁面、編輯器、MP4 匯出都讀同一份，所以「用講的改」和「在頁面上改」改的是同一個東西。

座標單位是畫面像素，以 `meta.width` × `meta.height` 為準（16:9 是 1280×720）。匯出時再用 `--scale` 放大，例如 1.5 倍就是 1920×1080。

## 最外層

```json
{
  "meta": {"title": "影片名稱", "width": 1280, "height": 720, "fps": 30, "background": "bg"},
  "palette": {"bg": "#0e2a2f", "fg": "#f1f5f2", "accent": "#f2b134", "muted": "#8fa9a6"},
  "scenes": [ ... ]
}
```

1. `meta.background`：預設背景，可以寫色票名稱或色碼。
2. `palette`：色票。元素的顏色欄位寫色票名稱（`"accent"`），改色票就整支一起換色。也可以直接寫色碼。
3. 畫面比例預設四種：16:9 = 1280×720、9:16 = 720×1280、1:1 = 1080×1080、4:5 = 1080×1350。

## 幕（scene）

```json
{"name": "差在哪", "duration": 4.5, "background": "panel",
 "transition": {"type": "fade", "dur": 0.4},
 "elements": [ ... ]}
```

1. `duration`：秒，最少 0.5。
2. `transition.type`：從上一幕進來的方式。
	1. `cut` 直接切換
	2. `fade` 淡入
	3. `slide` 推入
	4. `zoom` 縮放
	5. `wipe` 揭開
3. `elements` 由下往上疊，陣列後面的在上層。

## 元素共通欄位

```json
{"type": "text", "name": "可省略", "x": 120, "y": 90, "w": 1040, "h": 80, "rotate": 0,
 "props": { ... },
 "in":  {"effect": "slideUp", "start": 0.3, "dur": 0.6, "ease": "outCubic"},
 "out": {"effect": "fade", "start": 3.8, "dur": 0.4}}
```

1. `in.start`、`out.start` 是從這一幕開始算的秒數。
2. 沒有 `out` 就留到這一幕結束。
3. `ease`：`outCubic`（預設）、`inOutCubic`、`outBack`（回彈）、`outExpo`、`linear`、`inCubic`。

### 進場效果 `in.effect`

| 效果 | 用途 |
|---|---|
| `none` | 一開始就在 |
| `fade` | 淡入 |
| `slideUp` / `slideDown` / `slideLeft` / `slideRight` | 滑入 |
| `scale` | 放大出現 |
| `pop` | 彈出 |
| `wipe` | 由左揭開 |
| `blur` | 模糊轉清楚 |
| `typewriter` | 逐字打出（文字） |
| `count` | 數字跳動（數字、長條圖） |
| `grow` | 長出來（長條圖、方塊） |
| `draw` | 畫出來（線條、箭頭、折線圖） |

### 退場效果 `out.effect`

`none`、`fade`、`slideUp`、`slideDown`、`slideLeft`、`slideRight`、`scale`、`wipe`、`blur`。

## 各類型的 props

### text 文字

`text`（可換行 `\n`）、`size`、`weight`（400/500/700/900）、`color`、`align`（left/center/right）、`valign`（top/middle/bottom）、`lineHeight`、`letterSpacing`（em）、`bg`（底色，有底色時可加 `pad`、`radius`）。

### counter 數字

`from`、`to`、`decimals`、`prefix`、`suffix`、`size`、`weight`、`color`、`align`。

進場用 `count` 才會跳動；用其他效果就直接顯示 `to`。

### shape 圖形

1. `shape`：`rect`、`circle`、`line`、`arrow`。
2. 方塊、圓形：`fill`（`"none"` 為透明）、`stroke`、`strokeWidth`、`radius`、`growFrom`（left/right/bottom/top，搭配 `grow`）。
3. 線條、箭頭：`dir`（right/left/down/up/diag）、`stroke`、`strokeWidth`、`dashed`。

### image 圖片

`src`（data URI）、`fit`（cover/contain）、`radius`。沒有 `src` 時顯示虛線框，提醒放圖。

### bars 長條圖

1. `data`：`[{"label": "外銷", "value": 9.4, "color": "accent"}]`，`color` 可省略。
2. `orientation`：vertical / horizontal。
3. 其他：`barColor`、`labelColor`、`valueColor`、`unit`、`prefix`、`decimals`、`max`、`showValues`、`labelSize`、`valueSize`、`labelWidth`（橫條標籤寬）、`stagger`（每根間隔秒數，預設 0.12）、`gap`、`radius`。

### line 折線圖

1. `data` 同長條圖（不用 color）。
2. 其他：`color`、`strokeWidth`、`area`（線下面積，預設開）、`areaOpacity`、`dots`、`dotColor`、`showValues`、`showLabels`、`min`、`max`、`unit`、`decimals`、`labelSize`、`valueSize`、`labelColor`、`valueColor`、`axisColor`。

### list 清單

`items`（字串陣列）、`bullet`（dot/number/check/none）、`size`、`weight`、`color`、`accent`（符號色）、`gap`、`stagger`（每項間隔秒數，預設 0.3）。

清單不管選哪種進場效果，都是逐項滑上來；選 `none` 才會全部直接出現。
