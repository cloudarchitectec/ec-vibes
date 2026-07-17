# ec-vibes

**🇬🇧 [English](#english)** · **🇹🇼 [繁體中文](#繁體中文)**

---

## English

A small collection of Claude Skills — no coding required. You say what you want in plain language and Claude does the rest.

### Skills in this repo

**3 skills** so far:

| Skill | Type | What it does |
|---|---|---|
| [fitting-room/](fitting-room/) 🧥 | Claude Artifact | A private clothing size & fit-history tracker — "was I an M or an L in this brand?" |
| [staging-room/](staging-room/) 🧳 | Claude Artifact | A private, reusable travel packing list with trip-type modules (winter/beach/business/…) |
| [text-polish/](text-polish/) ✨ | Plain skill | Turns your rough notes into a polished, ready-to-send message — email, invite, announcement, chat, kudos or ticket |

### Skill types

- **Plain skill** — a single `SKILL.md`, nothing to build and nothing to publish. It changes how your assistant writes: you jot down the keywords, it hands back a finished message. Because there's no build step, it's portable — Claude Code, GitHub Copilot, Codex/ChatGPT, Gemini or the claude.ai app; each skill's README shows the setup that fits your assistant.

- **Claude Artifact** (see more detailed instructions below) — the skill builds you a private, single-page tool and publishes it as a private [Claude Artifact](https://claude.ai) you can bookmark on your phone. These all follow the same shape: `data.json` (your content) + a template (the look) → `build.py` (assembles it) → a private webpage only you can open. That shared shape is deliberate — once you understand one, the others (or a new tool you build from the same pattern) are familiar too. Building and publishing needs **Claude Code** (desktop app, VS Code/JetBrains extension, or terminal) — not the regular claude.ai chat website.

   ##### Use it like an app on your phone

   No App Store, nothing to install. Open the link on your phone, tap **Add to Home Screen**, and it sits next to your real apps — one tap away:

   <img src="homescreen.svg" alt="Illustration: two ec-vibes tools saved as icons on a phone home screen" width="450" />

### Quick start

1. Pick a skill folder above and open its README for the full walkthrough (with a live demo link and bilingual instructions).
2. Copy that skill's folder into `~/.claude/skills/<name>/` (or a project's `.claude/skills/<name>/`) so Claude Code can find it.
3. Open Claude Code and say what you want, e.g. *"set up a fitting room for my clothes"*.

### License

MIT — see [LICENSE](LICENSE).

---

## 繁體中文

ec-vibes 是一組 Claude Skills，讓你不用寫任何程式──用日常語言說出需求，其餘交給 Claude。

### 這個 repo 裡的 Skills

目前共有 **3 個 skills**：

| Skill | 類型 | 它能做什麼 |
|---|---|---|
| [fitting-room/](fitting-room/) 🧥 | Claude Artifact | 私人試衣間，記錄你的衣服尺寸──「這個牌子我上次穿 M 還是 L？」再也不用猜 |
| [staging-room/](staging-room/) 🧳 | Claude Artifact | 每趟都能重複使用的旅行打包清單，附情境模組（冬天／海邊／出差……），讓你再也不用每次旅行都重寫一份打包清單 |
| [text-polish/](text-polish/) ✨ | 純 Skill | 把你隨手記下的重點，潤飾成可以直接送出的英文訊息──郵件、會議邀請、公告、聊天訊息、讚美或工作單 |

### Skill 類型

- **純 Skill** ── 就只是一個 `SKILL.md`，不用建置、也不用發布，用來改變 AI 幫你寫字的方式──你列出關鍵字，它給你完成品。因為沒有建置步驟，所以到處都能用：Claude Code、GitHub Copilot、Codex／ChatGPT、Gemini、claude.ai App──設定方式請見各 skill 的 README。

- **Claude Artifact**（詳細說明見下方）── skill 會幫你建置一個私人單頁小工具，發布成只有你能開啟的私人 [Claude Artifact](https://claude.ai)，可以加到手機主畫面。這類 skill 的骨架完全相同：`data.json`（資料）＋ 模板（外觀）→ `build.py`（組裝）→ 私人網頁。骨架刻意共用──學會一個，其他的（或你照同樣模式做的新工具）也就都熟了。建置與發布需要 **Claude Code**（桌面版 App、VS Code／JetBrains 外掛或終端機）──一般的 claude.ai 聊天網站還不支援。

   ##### 像 App 一樣加到手機主畫面

   不用上架 App Store、也不用安裝任何東西。在手機上打開連結、選「**加入主畫面**」，它就會像一般 App 一樣出現在桌面上，一鍵打開：

   <img src="homescreen.svg" alt="示意圖：兩個 ec-vibes 工具以圖示形式放在手機主畫面上" width="450" />

### 快速開始

1. 從上面挑一個 skill，打開它的 README 看完整教學（有示範影片，中英文說明都有）。
2. 把該 skill 的資料夾複製到 `~/.claude/skills/<名稱>/`（或某個專案裡的 `.claude/skills/<名稱>/`），讓 Claude Code 讀得到。
3. 打開 Claude Code，直接說出你的需求，例如「幫我建一個記錄衣服尺寸的 fitting room」。

### 授權

MIT──詳見 [LICENSE](LICENSE)。
