# ec-vibes

**🇬🇧 [English](#english)** · **🇹🇼 [繁體中文](#繁體中文)**

---

## English

A small collection of Claude Skills — no coding required. Some build you a private,
single-page tool you can bookmark on your phone; some just change how Claude writes for
you. Either way, you say what you want in plain language and Claude does the rest.

### Skills in this repo

| Skill | What it does |
|---|---|
| [`fitting-room/`](fitting-room/) 🧥 | A private clothing size & fit-history tracker — "was I an M or an L in this brand?" |
| [`staging-room/`](staging-room/) 🧳 | A private, reusable travel packing list with trip-type modules (winter/beach/business/…) |
| [`text-polish/`](text-polish/) ✨ | Turns your rough notes into a polished, ready-to-send message — email, invite, announcement, chat, kudos or ticket |

`fitting-room` and `staging-room` follow the same shape: `data.json` (your content) + a
template (the look) → `build.py` (assembles it) → published as a private [Claude
Artifact](https://claude.ai) you can bookmark on your phone. That shared shape is
deliberate — once you understand one, the other (or a new tool you build from the same
pattern) is familiar too.

`text-polish` is a different kind of skill: nothing to build, nothing to publish. It's a
single `SKILL.md` that changes how your assistant writes — you jot down the keywords, it
hands back a finished message. Less typing. Better writing.

### Use it like an app on your phone

No App Store, nothing to install: `fitting-room` and `staging-room` each publish as a
private webpage, so on your phone you just open the link and **Add to Home Screen**. The
bookmark then sits next to your real apps, one tap away:

<img src="homescreen.svg" alt="Illustration: two ec-vibes tools saved as icons on a phone home screen" width="450" />

Both READMEs have step-by-step instructions for iPhone and Android.

### Quick start

1. Pick a skill folder above and open its README for the full walkthrough (with a live
   demo link and bilingual instructions).
2. Copy that skill's folder into `~/.claude/skills/<name>/` (or a project's
   `.claude/skills/<name>/`) so Claude Code can find it.
3. Open Claude Code and say what you want, e.g. *"set up a fitting room for my clothes"*.

`fitting-room` and `staging-room` need **Claude Code** (desktop app, VS Code/JetBrains
extension, or terminal) — not the regular claude.ai chat website, because they build and
publish a tool for you. `text-polish` is more portable: it also works with GitHub
Copilot, Codex/ChatGPT, Gemini and the claude.ai app — see
[its README](text-polish/) for the setup that fits your assistant.

### License

MIT — see [LICENSE](LICENSE).

---

## 繁體中文

ec-vibes 是一組 Claude Skills，讓你不用寫任何程式。有些會幫你做出專屬的私人小工具──獨立網頁，加到手機主畫面就能隨時打開；有些則單純改變 AI 幫你寫字的方式。不管是哪一種，你只要用日常語言說出需求，其餘交給 Claude。

### 這個 repo 裡的 Skills

| Skill | 它能做什麼 |
|---|---|
| [`fitting-room/`](fitting-room/) 🧥 | 私人試衣間，記錄你的衣服尺寸──「這個牌子我上次穿 M 還是 L？」再也不用猜 |
| [`staging-room/`](staging-room/) 🧳 | 每趟都能重複使用的旅行打包清單，附情境模組（冬天／海邊／出差……），讓你再也不用每次旅行都重寫一份打包清單 |
| [`text-polish/`](text-polish/) ✨ | 把你隨手記下的重點，潤飾成可以直接送出的英文訊息──郵件、會議邀請、公告、聊天訊息、讚美或工作單 |

`fitting-room` 和 `staging-room` 的骨架完全相同：`data.json`（資料）＋ 模板（外觀）→ `build.py`（組裝）→ 發布成私人 [Claude Artifact](https://claude.ai)，可以加到手機主畫面。

`text-polish` 則是另一種 skill：不用建置、也不用發布，就只是一個 `SKILL.md`，用來改變 AI 幫你寫字的方式──你列出關鍵字，它給你完成品。寫得更少，說得更好。

### 像 App 一樣加到手機主畫面

不用上架 App Store、也不用安裝任何東西：`fitting-room` 和 `staging-room` 發布出來就是一個私人網頁，在手機上打開連結、選「**加入主畫面**」，它就會像一般 App 一樣出現在桌面上，一鍵打開：

<img src="homescreen.svg" alt="示意圖：兩個 ec-vibes 工具以圖示形式放在手機主畫面上" width="450" />

iPhone 和 Android 的詳細步驟，請見這兩個 skill 的 README。

### 快速開始

1. 從上面挑一個 skill，打開它的 README 看完整教學（有示範影片，中英文說明都有）。
2. 把該 skill 的資料夾複製到 `~/.claude/skills/<名稱>/`（或某個專案裡的 `.claude/skills/<名稱>/`），讓 Claude Code 讀得到。
3. 打開 Claude Code，直接說出你的需求，例如「幫我建一個記錄衣服尺寸的 fitting room」。

`fitting-room` 和 `staging-room` 需要搭配 **Claude Code**（有桌面版 App、VS Code／JetBrains 外掛，也有終端機版本）──一般的 claude.ai 聊天網站還不支援，因為它們要幫你建置並發布工具。`text-polish` 則彈性得多：GitHub Copilot、Codex／ChatGPT、Gemini、claude.ai App 都能用──設定方式請見 [它的 README](text-polish/)。

### 授權

MIT──詳見 [LICENSE](LICENSE)。
