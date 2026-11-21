# claude-skills

**motion-studio** 是一支 Claude skill：把報告、Excel 表格、圖片做成 15–30 秒的短動畫，發佈成可以直接拖拉編輯的頁面，再匯出 MP4 或 GIF。不需要 Team 或 Enterprise 方案。

**motion-studio** is a Claude skill that turns reports, Excel/CSV data and images into 15–30 second animations, publishes them as a page you can edit by dragging, and exports MP4 or GIF. No Team or Enterprise plan needed.

這個 repo 放我自己做、自己在用的 Claude skills。
This repo holds Claude skills I built and use myself.

| Skill | 用途 / What it does |
|---|---|
| [motion-studio](motion-studio/) | 把報告、數據、圖片做成可編輯的短動畫 / Turn reports, data and images into short, editable animations |

ABAP 相關的 skill 在另一個 repo：[abap-claude-skills](https://github.com/hungyichiu/abap-claude-skills)。
ABAP skills live in a separate repo: [abap-claude-skills](https://github.com/hungyichiu/abap-claude-skills).

---

## motion-studio

![四格漫畫：使用者想用 Claude 的 Motion，Claude 說只開放給 Team 和 Enterprise；使用者請 Claude 自己做一個，Claude 答應了 / Four-panel comic: a user asks for Motion in Claude, is told it is Team and Enterprise only, then asks Claude to build one, and Claude agrees](docs/cover.png)

想用 Claude 的 Motion 做動畫，它說只開放給 Team 和 Enterprise（2026-10 的情況）。那就請 Claude 自己做一個。

I wanted to use Motion in Claude. It's only available on Team and Enterprise plans (as of 2026-10). So I asked Claude to build one.

### 能做什麼 / What it does

- 把內容做成 15～30 秒的動畫：文字、數字跳動、長條圖、折線圖、清單、箭頭、圖片的進退場與轉場
- 畫面比例：16:9、9:16、1:1、4:5
- 發佈成可以直接在畫面上編輯的頁面：拖拉位置與大小、在時間軸調秒數和出場時間、換色、改字改數字，改完按儲存
- 在對話裡匯出 MP4 或 GIF

- Short animations (15–30s): text, counting numbers, bar and line charts, lists, arrows, images, with entrances, exits and transitions
- Aspect ratios: 16:9, 9:16, 1:1, 4:5
- Published as a page you edit directly: drag and resize, adjust timing on a timeline, change colors, text and numbers, then save
- Export to MP4 or GIF from the chat

做不到：3D、運鏡、寫實影片、真人、配音和背景音樂。

Not supported: 3D, camera moves, live-action footage, voice-over and music.

### 安裝 / Install

1. 下載 `motion-studio` 資料夾，壓成 zip（zip 裡是 `motion-studio/` 資料夾）。
2. 在 Claude 打開 **Customize › Skills**，按 **+** › **Create skill** › **Upload a skill**，上傳 zip。
3. 在技能清單裡把它打開。

1. Download the `motion-studio` folder and zip it (the zip contains the `motion-studio/` folder).
2. In Claude, open **Customize › Skills**, click **+** › **Create skill** › **Upload a skill**, and upload the zip.
3. Toggle it on in your skills list.

### 怎麼用 / Usage

跟 Claude 說「把這份報告做成 30 秒動畫」或「/motion」，附上報告、數據或截圖。要影片檔就說「匯出 MP4」。

Ask Claude something like "turn this report into a 30-second animation" or "/motion", and attach your report, data or screenshots. Say "export MP4" when you want a video file.

### 範例 / Example

輸入：跟 Claude 說「把第三季營收做成 17 秒動畫：先講成長 18%，再看各季走勢、誰貢獻最多，最後講下一步」，附上各季營收數字（範例數字是虛構的）。

Input: ask Claude "turn Q3 revenue into a 17-second animation: lead with 18% growth, then the quarterly trend, the biggest contributors, and next steps", with the quarterly figures attached (the figures in this example are fictional).

輸出：下面這個 GIF（640×360、12fps、約 230KB），分鏡檔是 [`motion-studio/templates/chart.json`](motion-studio/templates/chart.json)。

Output: the GIF below (640×360, 12 fps, about 230 KB); the spec is [`motion-studio/templates/chart.json`](motion-studio/templates/chart.json).

![動態圖表範例：第三季營收成長 18% 的數字跳動，接著折線圖畫出各季營收走勢 / Animated chart example: an 18% Q3 revenue growth counter, followed by a line chart of quarterly revenue](docs/examples/chart-demo.gif)

### 需求 / Requirements

- 發佈可編輯頁面需要 Claude 的 Artifact 功能。
- 匯出 MP4、GIF 需要 Python 的 `playwright`（含 Chromium）和 `ffmpeg`，skill 會先自己檢查。

- The editable page needs Claude's Artifacts.
- MP4 / GIF export needs Python `playwright` (with Chromium) and `ffmpeg`; the skill checks for them first.

### 檔案 / Files

| 路徑 / Path | 用途 / Purpose |
|---|---|
| `SKILL.md` | 給 Claude 的流程說明 / Instructions for Claude |
| `assets/engine.html` | 播放器＋編輯器 / Player and editor |
| `scripts/build.py` | 分鏡 → 可發佈頁面 / Spec → publishable page |
| `scripts/render.py` | 分鏡 → MP4、GIF、靜態圖 / Spec → MP4, GIF, stills |
| `templates/` | 說明動畫、動態圖表、直式步驟導覽範本 / Explainer, chart, vertical walkthrough |
| `references/spec-format.md` | 分鏡格式 / Spec format |

## 常見問題 / FAQ

**和 Claude 內建的 Motion 有什麼不同？ / How is it different from Motion in Claude?**

做法不同：這是一支上傳就能用的 skill，用 Artifact 發佈可編輯頁面，用 Python 腳本匯出影片。內建 Motion 的功能範圍以 Anthropic 官方說明為準。

It's a skill you upload yourself: it publishes the editable page as an Artifact and exports video with Python scripts. For what the built-in Motion offers, see Anthropic's documentation.

**免費或 Pro 方案能用嗎？ / Does it work on Free or Pro plans?**

只要你的方案能上傳 skill、能用 Artifact 就能用。匯出 MP4、GIF 另外需要能執行 Python 的環境。

Yes, if your plan supports uploading skills and Artifacts. MP4 / GIF export also needs an environment that can run Python.

**Claude Code 能用嗎？ / Does it work in Claude Code?**

能。把 `motion-studio` 資料夾複製到 `~/.claude/skills/`。匯出影片的腳本在本機跑，要先裝 `playwright`（含 Chromium）和 `ffmpeg`。

Yes. Copy the `motion-studio` folder into `~/.claude/skills/`. The export scripts run locally and need `playwright` (with Chromium) and `ffmpeg`.

**能做 3D 或運鏡嗎？ / Can it do 3D or camera moves?**

不能。它做 2D 的文字、數字、圖表、圖片動畫；3D、運鏡、寫實影片、配音和背景音樂都不支援。

No. It animates 2D text, numbers, charts and images; 3D, camera moves, live-action footage, voice-over and music are not supported.

## 作者 / Author

[@hungyichiu](https://github.com/hungyichiu)。最後更新：2026-11。

[@hungyichiu](https://github.com/hungyichiu). Last updated: 2026-11.

## License

[MIT](LICENSE)
