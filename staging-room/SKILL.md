---
name: staging-room
description: Scaffold and maintain "Staging Room" — a private, phone-friendly travel packing checklist published as a Claude Artifact. Use when the user wants to build their own version of this tool ("set up a packing list", "build a travel checklist"), or wants to add/update items in an instance they already built with this skill.
---

# Staging Room

A private **travel-packing master list + toolbox**. It's cumulative packing memory, not a
one-trip checklist: the user builds up every item they own or might need once, tags
trip-specific gear (ski, beach, business…) as "situational modules", and then for each
real trip toggles on the modules that apply and ticks items off as they pack. The result
is a single self-contained HTML file published as a **private Claude Artifact**, bookmarked
on their phone. Master list is read-only in the browser — all item edits happen here in chat.

Sibling skill: `fitting-room` (a clothing size & fit tracker). Same architecture, different data.

## Architecture (why it's built this way)

```
data.json  +  staging-room.template.html  --[build.py]-->  dist/staging-room.html  --[Artifact tool]--> private link
```

- **`data.json`** is the single source of truth (`ui`, `sections`, `modules`, `items`).
- **`staging-room.template.html`** is the only editable HTML — markup, CSS and JS, with
  `__TITLE__` / `__SUBTITLE__` / `__UPDATED_LABEL__` / `__SEARCH_PH__` / `__DATA_JSON__` tokens.
- **`build.py`** validates `data.json` (unknown section/module keys, situational items
  missing a module, duplicate item ids) and assembles `dist/staging-room.html`. No photos
  in this tool — everything is a text row.
- **Packing state is device-local, not in `data.json`.** Which boxes are ticked and which
  situational modules are switched on live in the browser's `localStorage`
  (`sr-checked`, `sr-mods`) — per device, never synced, never written back. That's
  deliberate: the master list is shared/curated content, ticks are ephemeral per-trip state.
- The build never hand-edits the output; `dist/` is regenerable and disposable.

Bundled in `reference/` (copy these into the user's new project folder — don't
regenerate them from scratch, they're already tested):
- `staging-room.template.html`
- `build.py` (no extra dependencies)
- `data.example.json` — a fully worked mock example (generic trip items) so you or the
  user can see the tool working before entering real data.
- `gitignore` — copy as `.gitignore` into the new project if it'll be its own git repo.

## Step 0 — first time, or an existing project?

Check the user's current directory (ask if it's unclear where their project lives) for a
folder containing `data.json` **and** `.artifact-url`. If found → skip straight to
**"Update workflow"** below. If not → this is first-time setup.

## First-time setup

### 1. Where and what to call it
Ask where to create the project (default: `./staging-room/` in the current directory)
and what to call the tool (default title `Staging Room 🧳`).

### 2. Ask a few configuration questions
Use the `AskUserQuestion` tool if you have it; otherwise just ask conversationally.

- **UI language** — English, Traditional Chinese (Taiwan), or a custom mix. Two
  ready-to-paste `ui` blocks are below. This only affects labels baked into the
  artifact — chat with the user in whatever language they prefer.
- **Accent colour** — pick one of the presets below, or give a hex code.
- **Sections** — the default eight (bags & gear / carry-on essentials / fine to check in /
  wearing on travel day / clothes to pack / toiletries / everything else / trip-specific)
  cover most people, but ask if they want to rename, drop or add any. Sections are just
  data — freely edit `data.json` → `sections` any time. **The `situational` section key
  is special** (see Data model below) — keep exactly one section with that key if the
  user wants the module-toggle behaviour at all; it's fine to rename its `label`.
- **Situational modules** — what kinds of trips does the user actually take? Common ones:
  winter, beach, business, road trip, hiking/camping, formal occasion. Only set up
  modules they'll actually reuse — a module with one item in it isn't worth the chip.

### 3. Scaffold the project
- Create the project folder with a `scripts/` subfolder.
- Copy `reference/staging-room.template.html` → `<project>/staging-room.template.html`.
- Copy `reference/build.py` → `<project>/scripts/build.py`.
- If the project folder is (or will become) its own git repo, copy `reference/gitignore`
  → `<project>/.gitignore` (it excludes `dist/`, `__pycache__/`, and `.artifact-url`).
- Write `<project>/data.json` using the chosen `ui` block, sections and modules, with
  `"items": []` to start.
- If a different accent colour was chosen, edit `--accent` / `--accent-bg` / `--accent-ink`
  in the template's `:root` block (they move together — see presets below).
- Run `python3 scripts/build.py` once from inside the project folder to confirm it builds
  cleanly (it will show 0 items — that's expected and fine).

### 4. Enter their first items
Mirror the update workflow below: propose placement (section/group or module), qty,
notes; get approval; then write to `data.json` and rebuild. Offer to walk through their
core "always in the bag" gear first (documents, chargers, toiletries basics), then any
situational modules they mentioned.

### 5. Publish
Use the Artifact tool on `dist/staging-room.html`, **no `url` argument** (first publish
mints a new link). Save the URL it returns into `<project>/.artifact-url` (plain text,
just the URL) — `build.py` reads this file to remind you where to republish on every
future build. Tell the user:
- It's **private** by default; they can share it from the artifact page if they ever want to.
- **Walk them through adding it to their phone's home screen** — don't just say "bookmark
  it"; give the actual steps (in whatever language you're chatting in) so it sits next to
  their real apps, one tap away before every trip:
  - **iPhone**: open the link in **Safari** (logged into claude.ai) → **Share** button →
    **Add to Home Screen** → give it a short name (emoji fine) → **Add**.
  - **Android**: open the link in **Chrome** (logged into claude.ai) → **⋮** menu →
    **Add to Home screen** → pick the shortcut option if asked → confirm.
  - Mention: it's a bookmark that looks like an app, not an offline app — it needs
    internet + their claude.ai login; and after every republish the icon automatically
    opens the newest version, no need to re-add.
- Ticks and module choices are per-device and never sync — that's intentional, not a bug.
- All *list* edits happen back here in chat — the app itself is read-only for the list;
  only ticking/unticking and toggling modules happens in-app.

## Update workflow (returning sessions)

The user hands you new items, a per-trip lesson ("forgot X this time" / "brought Y, never
used it"), or gear to log (e.g. a new suitcase with its dimensions). Then:

1. **Draft the change** — propose section/group/module placement, qty, notes (their
   wording, don't rewrite or "fix" it), specs if it's a bag/gear item with dimensions.
   Present a compact table in whichever language the user is chatting in. **Do not edit
   `data.json` yet.**
2. **On approval**: edit `data.json` → `python3 scripts/build.py` → check the console
   output (item counts, any validation warnings).
3. **Preview locally when it's worth a look** — `dist/staging-room.html` is fully
   self-contained, so opening it straight in a browser shows exactly what will be
   published. Skip this for a routine item add; offer it for anything visual — an accent
   change, reorganised sections, new modules, template tweaks. (Ticks made in the local
   preview live in that browser's own `localStorage` — they never affect the published page.)
4. **Republish** `dist/staging-room.html` — pass the saved URL from `.artifact-url` as the
   Artifact tool's `url` argument so it updates the same link instead of minting a new one.
   Rebuilding alone only updates the local file: the published link (and the icon on the
   user's phone) keeps showing the old version until this republish happens. If the user
   wants to hold off publishing, fine — but say explicitly that the live page is still the
   old version so they're not surprised mid-packing.

## Data model (one object per item in `data.json` → `items`)

```json
{ "sec": "carry", "group": "Electronics", "name": "Portable charger", "qty": "x2",
  "notes": "Not allowed in checked luggage.",
  "specs": [["Size", "22 x 7 x 16cm"]],
  "module": "beach" }
```

- `sec` — must match a `key` in `data.json` → `sections`.
- `group` — free-text sub-group within the section (e.g. "Documents", "Electronics").
  Display preserves `data.json` order (first appearance wins). **Situational items use
  `module` instead of `group`.**
- `module` — only for `sec: "situational"`; must match a `key` in `data.json` →
  `modules`. These items appear only when their chip is switched on (or while searching —
  search always bypasses module gating so the whole toolbox is findable).
- `qty` — free text (`"x2"`, `"one pack"`, `"50ml"`, `"x?"` for "not decided yet"). Omit
  or `""` if not applicable.
- `specs` — optional, only for items where dimensions/capacity matter (bags, luggage):
  `[["label","value"]]` pairs, free text. Keep formatting consistent across similar items
  (e.g. always `NN x NN x NNcm` for size, no embedded L/W/H letters).
- `notes` — record the user's wording **verbatim** — don't translate or "fix" their
  phrasing, typos included. When an item has several distinct facts (capacity, style,
  colour, price), join them with ` · ` (space-dot-space).
- **Item identity** (the checkbox key) is `sec|group-or-module|name`. Renaming an item
  resets its tick on the user's phone — harmless, but avoid gratuitous renames.
  `build.py` rejects duplicate ids outright.

## UI language presets — paste into `data.json` → `ui`

**English (default):**
```json
{
  "title": "Staging Room 🧳",
  "subtitle": "Packing list · never forget, just go",
  "updatedLabel": "Updated: ",
  "searchPlaceholder": "Search items, notes, categories…",
  "resetBtnLabel": "↺ Reset checks",
  "resetConfirm": "Clear all checks and start a new trip? (Your module choices are kept.)",
  "modCaption": "🎯 Situational modules — tap to add to this trip",
  "progressAriaLabel": "Packing progress",
  "progressTemplate": "Packed <b class=\"tnum\">{done}</b><span class=\"tnum\">/{total}</span>",
  "progressDoneLabel": "🎉 <b>All packed!</b>",
  "emptyState": "No matching items. Try a different search, or add more later.",
  "selectAllAriaPrefix": "Select all: "
}
```

**繁體中文（台灣）：**
```json
{
  "title": "旅行打包清單 🧳",
  "subtitle": "旅行打包母清單．不怕忘，只管玩",
  "updatedLabel": "更新時間：",
  "searchPlaceholder": "搜尋物品、備註、類別…",
  "resetBtnLabel": "↺ 重置勾選",
  "resetConfirm": "清除所有勾選、開始新的一次打包？（情境模組選擇會保留）",
  "modCaption": "🎯 情境模組 — 點選加入旅程",
  "progressAriaLabel": "打包進度",
  "progressTemplate": "已裝 <b class=\"tnum\">{done}</b><span class=\"tnum\">/{total}</span>",
  "progressDoneLabel": "🎉 <b>全部打包完成</b>",
  "emptyState": "沒有符合的物品。換個關鍵字，或之後再新增。",
  "selectAllAriaPrefix": "整組勾選："
}
```

## Accent colour presets

`--accent`, `--accent-bg` and `--accent-ink` move together (the "packed" colour used for
the progress bar, checkboxes, and quantity chips).

| Preset | `--accent` | `--accent-bg` | `--accent-ink` |
|---|---|---|---|
| Spruce green (default) | `#2e6b4f` | `#e2efe8` | `#f2efe9` |
| Ocean blue | `#2f5f8a` | `#e2eaf4` | `#f2efe9` |
| Terracotta | `#a15b3f` | `#f4e6df` | `#f2efe9` |

## Hard rules

- **Never invent** items, quantities, or notes — they come from the user only.
  Unresolved items the user flagged ("should I bring this?") stay phrased as an open
  question in `notes` until they decide.
- Never run `git add` / `commit` / `push` unless the user explicitly says so.
- Keep the artifact self-contained — no runtime requests to external URLs.
- `dist/` is generated and disposable — never hand-edit it; edit the template or
  `data.json` and rebuild.
