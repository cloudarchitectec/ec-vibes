# ec-vibes

**🇬🇧 [English](#english)** · **🇹🇼 [繁體中文](#繁體中文)**

---

## English

A small collection of Claude Skills for building your own private, single-page tools
— no coding required. Each skill interviews you for a few preferences, then has Claude
scaffold, build and publish a self-contained tool as a private [Claude
Artifact](https://claude.ai) you can bookmark on your phone.

### Skills in this repo

| Skill | What it builds |
|---|---|
| [`fitting-room/`](fitting-room/) 🧥 | A private clothing size & fit-history tracker — "was I an M or an L in this brand?" |
| [`staging-room/`](staging-room/) 🧳 | A private, reusable travel packing list with trip-type modules (winter/beach/business/…) |

Both follow the same shape: `data.json` (your content) + a template (the look) →
`build.py` (assembles it) → published as a private Claude Artifact. That shared shape is
deliberate — once you understand one, the other (or a new tool you build from the same
pattern) is familiar too.

### Quick start

1. Pick a skill folder above and open its README for the full walkthrough (with a live
   demo link and bilingual instructions).
2. Copy that skill's folder into `~/.claude/skills/<name>/` (or a project's
   `.claude/skills/<name>/`) so Claude Code can find it.
3. Open Claude Code and say what you want, e.g. *"set up a fitting room for my clothes"*.

Custom Skills currently require **Claude Code** (desktop app, VS Code/JetBrains
extension, or terminal) — not the regular claude.ai chat website.

### License

MIT — see [LICENSE](LICENSE).

---

## 繁體中文

ec-vibes 是一組 Claude Skills，讓你不用寫任何程式，也能做出自己專屬的私人小工具──每個工具都是一個獨立網頁，加到手機主畫面就能隨時打開。每個 skill 會先問你幾個偏好問題，接著由 Claude 幫你建好專案、組出工具，發布成只有你能開啟的私人 [Claude Artifact](https://claude.ai)。

### 這個 repo 裡的 Skills

| Skill | 做出來的工具 |
|---|---|
| [`fitting-room/`](fitting-room/) 🧥 | 私人試衣間，記錄你的衣服尺寸──「這個牌子我上次穿 M 還是 L？」再也不用猜 |
| [`staging-room/`](staging-room/) 🧳 | 每趟都能重複使用的旅行打包清單，附情境模組（冬天／海邊／出差……），讓你再也不用每次旅行都重寫一份打包清單 |

兩個 skill 的骨架完全相同：`data.json`（資料）＋ 模板（外觀）→ `build.py`（組裝）→ 發布成私人 Claude Artifact。

### 快速開始

1. 從上面挑一個 skill，打開它的 README 看完整教學（有示範影片，中英文說明都有）。
2. 把該 skill 的資料夾複製到 `~/.claude/skills/<名稱>/`（或某個專案裡的 `.claude/skills/<名稱>/`），讓 Claude Code 讀得到。
3. 打開 Claude Code，直接說出你的需求，例如「幫我建一個記錄衣服尺寸的 fitting room」。

自訂 Skills 目前需要搭配 **Claude Code**（有桌面版 App、VS Code／JetBrains 外掛，也有終端機版本）──一般的 claude.ai 聊天網站還不支援。

### 授權

MIT──詳見 [LICENSE](LICENSE)。
