---
name: fitting-room
description: Scaffold and maintain "Fitting Room" — a private, phone-friendly clothing size & fit-history tracker published as a Claude Artifact. Use when the user wants to build their own version of this tool ("set up a fitting room", "track my clothing sizes"), or wants to add/update an item in an instance they already built with this skill.
---

# Fitting Room

A private **clothing size & fit-history tracker**. The user hands you a product link, a
receipt, or a size-tag photo; you record brand, size, measurements and a fit verdict
(too small / just right / too big); the result is a single self-contained HTML file
published as a **private Claude Artifact** they bookmark on their phone and check while
shopping. Read-only in the browser — all edits happen here, in chat, on the source files.

Sibling skill: `staging-room` (a travel-packing checklist). Same architecture, different data.

## Architecture (why it's built this way)

```
data.json  +  fitting-room.template.html  --[build.py]-->  dist/fitting-room.html  --[Artifact tool]--> private link
```

- **`data.json`** is the single source of truth (`ui`, `categories`, `seasons`, `records`).
- **`fitting-room.template.html`** is the only editable HTML — markup, CSS and JS, with
  `__TITLE__` / `__SUBTITLE__` / `__UPDATED_LABEL__` / `__SEARCH_PH__` / `__DATA_JSON__` /
  `__PHOTOS_JSON__` tokens.
- **`build.py`** assembles `dist/fitting-room.html`: fills the tokens, sorts records,
  normalises measurement labels, and — if a `photos/` folder exists — resizes each photo
  to ≤360px and inlines it as base64 (a Claude Artifact's CSP blocks remote images, so
  photos *must* be embedded, not linked).
- The build never hand-edits the output; `dist/` is regenerable and disposable.

Bundled in `reference/` (copy these into the user's new project folder — don't
regenerate them from scratch, they're already tested):
- `fitting-room.template.html`
- `build.py` (needs Pillow: `pip install pillow` — only if the user wants photos)
- `add_photo.py` (optional, only needed if the user wants photos)
- `data.example.json` — a fully worked mock example (fake brands, fake sizes) so you or
  the user can see the tool working before entering real data.
- `gitignore` — copy as `.gitignore` into the new project if it'll be its own git repo.

## Step 0 — first time, or an existing project?

Check the user's current directory (ask if it's unclear where their project lives) for a
folder containing `data.json` **and** `.artifact-url`. If found → skip straight to
**"Update workflow"** below. If not → this is first-time setup.

## First-time setup

### 1. Where and what to call it
Ask where to create the project (default: `./fitting-room/` in the current directory)
and what to call the tool (default title `Fitting Room 🧥`).

### 2. Ask a few configuration questions
Use the `AskUserQuestion` tool if you have it; otherwise just ask conversationally. Don't
skip this — it's the whole point of this skill being reusable instead of a one-off script.

- **UI language** — English, Traditional Chinese (Taiwan), or a custom mix. Two
  ready-to-paste `ui` blocks are below; use one as-is or adapt it. This only affects
  labels baked into the artifact — chat with the user in whatever language they prefer.
- **Measurement unit default** — cm (recommended, matches most size charts) or inches.
  Either way both are always available via the in-app toggle; this only sets the default.
- **Accent colour** — pick one of the presets below, or give a hex code.
- **Garment categories** — the default four (tops / bottoms / outerwear / underwear) work
  for most wardrobes, but ask if they want different ones (e.g. add "shoes" or
  "activewear", drop "underwear"). Categories are just data — freely add, rename or
  remove them in `data.json` → `categories` any time.
- **Product photos** — yes (needs Pillow + `photos/`) or no (cleaner, no dependency; the
  card shows a category-label placeholder instead of a thumbnail — this looks fine).

### 3. Scaffold the project
- Create the project folder with a `scripts/` subfolder.
- Copy `reference/fitting-room.template.html` → `<project>/fitting-room.template.html`.
- Copy `reference/build.py` → `<project>/scripts/build.py`.
- If photos were requested, also copy `reference/add_photo.py` → `<project>/scripts/add_photo.py`.
- If the project folder is (or will become) its own git repo, copy `reference/gitignore`
  → `<project>/.gitignore` (it excludes `dist/`, `__pycache__/`, and `.artifact-url`).
- Write `<project>/data.json` using the chosen `ui` block, categories and seasons, with
  `"records": []` to start.
- If a different accent colour was chosen, edit the `--accent` (and for consistency the
  three `--fit-*-bg`/`--fit-*` pairs only if the user specifically wants those retinted —
  default is to leave the small/ok/big traffic-light colours alone, see the preset note below).
- Run `python3 scripts/build.py` once from inside the project folder to confirm it builds
  cleanly (it will show 0 records — that's expected and fine).

### 4. Enter their first item(s)
Mirror the update workflow below: gather details, present for review, get approval, then
write to `data.json` and rebuild. Don't rush straight to publishing with zero items unless
the user wants an empty tool to fill in later — offer to walk through 1-2 real items first
so they see it working with their own data.

### 5. Publish
Use the Artifact tool on `dist/fitting-room.html`, **no `url` argument** (first publish
mints a new link). Save the URL it returns into `<project>/.artifact-url` (plain text,
just the URL, no trailing content) — `build.py` reads this file to remind you where to
republish on every future build. Tell the user:
- It's **private** by default; they can share it from the artifact page if they ever want to.
- **Walk them through adding it to their phone's home screen** — don't just say "bookmark
  it"; give the actual steps (in whatever language you're chatting in) so it sits next to
  their real apps, one tap away while shopping:
  - **iPhone**: open the link in **Safari** (logged into claude.ai) → **Share** button →
    **Add to Home Screen** → give it a short name (emoji fine) → **Add**.
  - **Android**: open the link in **Chrome** (logged into claude.ai) → **⋮** menu →
    **Add to Home screen** → pick the shortcut option if asked → confirm.
  - Mention: it's a bookmark that looks like an app, not an offline app — it needs
    internet + their claude.ai login; and after every republish the icon automatically
    opens the newest version, no need to re-add.
- All edits happen back here in chat — the app itself is read-only.

## Update workflow (returning sessions)

The user hands you a product link, an order/receipt, or a label/size-guide photo. Then:

1. **Gather details** from the source — don't invent anything. Aim for: brand, product
   name, colour, size, measurements, material composition, SKU/item number, price,
   product link, and a sensible season. If you can't find official measurements, leave
   `measures: []` and add `"measuresNote": "unable to locate official measurement"` —
   **never guess**.
2. **Present for review** — a compact table, in whichever language the user is chatting
   in. Ask them to confirm the fit verdict and anything you inferred (especially
   `season`). **Do not edit `data.json` yet.**
3. **On approval**:
   - Add/edit the record in `data.json` (append order doesn't matter — build sorts by `cat`).
   - If photos are enabled: `python3 scripts/add_photo.py "<SKU>" "<image-or-product-URL>"`.
   - Rebuild: `python3 scripts/build.py`. Check the console output (record count, any
     "unrecognised measure label" or "no photo for" warnings).
4. **Preview locally when it's worth a look** — `dist/fitting-room.html` is fully
   self-contained (photos are inlined as base64), so opening it straight in a browser
   shows exactly what will be published. Skip this for a routine one-record add; offer it
   for anything visual — an accent change, a new category, first photos, template tweaks.
5. **Republish** `dist/fitting-room.html` — pass the saved URL from `.artifact-url` as the
   Artifact tool's `url` argument so it updates the same link instead of minting a new one.
   Rebuilding alone only updates the local file: the published link (and the icon on the
   user's phone) keeps showing the old version until this republish happens. If the user
   wants to hold off publishing, fine — but say explicitly that the live page is still the
   old version so they're not surprised in the changing room.

## Data model (one object per garment in `data.json` → `records`)

```json
{ "cat": "tops", "brand": "...", "product": "...", "colour": "...", "size": "...",
  "material": "...", "measures": [["Bust","98"], ["Waist","76"]], "fit": "ok",
  "date": "2026-06-28", "notes": "...", "link": "...", "sku": "...",
  "price": "64.99", "season": "mild" }
```

- `cat` — must match a `key` in `data.json` → `categories`.
- `fit` — exactly one of `small | ok | big` (internal keys, decoupled from display
  language — see `ui.fitLabels`). Nuance goes in `notes`, not the verdict.
- **Measurement labels are canonical English keys** regardless of UI language (`Bust`,
  `Waist`, `Hip`, `Inseam`, `Shoulder`, `Length`, `Sleeve`, `Under-bust`, `Cup`). If a
  source uses an alias (`Chest`, `Inleg`), record the canonical label. `build.py`
  normalises known aliases as a backstop and prints a note; unrecognised labels get a ⚠
  warning — extend `MEASURE_CANON` in `build.py` if the user tracks something not on this
  list (e.g. `Neck`, `Thigh`). Values are text so ranges like `82-89` survive — **always
  in cm** (the in-app cm/in toggle converts at display time only; never store inches).
- `season` — optional, must match a `key` in `data.json` → `seasons`. Skip it (`null`)
  for anything season-agnostic (e.g. underwear).
- `price` may be `""` if unknown. Don't invent it.
- **`categories[].range`** is a manual, curator-set "typical size range" strip shown when
  that category's chip is active — same `[[label, value]]` shape as `measures`. **Never
  auto-calculate this from records** — an "ok" size-chart span mixes garment intents
  (a roomy jacket vs. a slim tee vs. a skin-tight baselayer), so a computed span misleads.
  Only set it if the user gives you numbers directly.
- **`categories[].alwaysShow: true`** keeps that category's chip visible even with 0
  matching records (useful for a category the user wants as a standing reminder to fill in).

## UI language presets — paste into `data.json` → `ui`

**English (default):**
```json
{
  "title": "Fitting Room 🧥",
  "subtitle": "Sizes & fit notes, at a glance",
  "updatedLabel": "Updated: ",
  "searchPlaceholder": "Search brand, item, notes…",
  "emptyState": "No matches. Try a different filter, or add more items later.",
  "countTemplate": "{n} items",
  "countTotalTemplate": "({total} total)",
  "rangeLabel": "📏 Size range: ",
  "unitToggleAriaLabel": "Measurement unit",
  "unnamedLabel": "(untitled)",
  "sizeLabel": "Size: ",
  "linkLabel": "Link ↗",
  "fitLabels": { "small": "Too small", "ok": "Just right", "big": "Too big" }
}
```

**繁體中文（台灣）：**
```json
{
  "title": "衣櫥尺碼本 🧥",
  "subtitle": "品牌尺寸．試穿心得",
  "updatedLabel": "更新時間：",
  "searchPlaceholder": "搜尋品牌、商品、備註…",
  "emptyState": "沒有符合的紀錄。換個篩選，或之後再新增。",
  "countTemplate": "{n} 筆",
  "countTotalTemplate": "（共 {total} 筆）",
  "rangeLabel": "📏 尺寸範圍：",
  "unitToggleAriaLabel": "量測單位",
  "unnamedLabel": "（未命名）",
  "sizeLabel": "尺寸：",
  "linkLabel": "連結 ↗",
  "fitLabels": { "small": "太小", "ok": "剛好", "big": "太大" }
}
```

Mixing is fine and common (e.g. English chrome with the user's own Chinese notes in
`records[].notes` — `notes` is always recorded verbatim in whatever language the user gave it).

## Accent colour presets

Only `--accent` in the template's `:root` block needs to change (it colours links, the
active unit-toggle outline, etc.). Leave `--fit-small` / `--fit-ok` / `--fit-big` and
their `-bg` pairs alone — they're a deliberate small/ok/big traffic light, not a theme colour.

| Preset | `--accent` |
|---|---|
| Slate navy (default) | `#3d5a80` |
| Forest | `#3d6b4f` |
| Plum | `#7a4a6b` |

## Hard rules

- **Never fabricate** measurements, prices, or fit verdicts — those come only from the
  user or a source they point you to. When in doubt, leave it blank with a note.
- **Never guess measurements** — use `measuresNote` instead of inventing a number.
- Never run `git add` / `commit` / `push` unless the user explicitly says so.
- Keep the artifact self-contained — no runtime requests to external URLs (this is why
  photos get inlined as base64 instead of linked).
- `dist/` is generated and disposable — never hand-edit it; edit the template or
  `data.json` and rebuild.
