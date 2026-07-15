# ec-vibes

A small collection of Claude Skills for building your own private, single-page tools
— no coding required. Each skill interviews you for a few preferences, then has Claude
scaffold, build and publish a self-contained tool as a private [Claude
Artifact](https://claude.ai) you can bookmark on your phone.

**🇬🇧 English · 🇹🇼 繁體中文** — each skill's own README is bilingual; this page is a short
index in English.

## Skills in this repo

| Skill | What it builds |
|---|---|
| [`fitting-room/`](fitting-room/) 🧥 | A private clothing size & fit-history tracker — "was I an M or an L in this brand?" |
| [`staging-room/`](staging-room/) 🧳 | A private, reusable travel packing list with trip-type modules (winter/beach/business/…) |

Both follow the same shape: `data.json` (your content) + a template (the look) →
`build.py` (assembles it) → published as a private Claude Artifact. That shared shape is
deliberate — once you understand one, the other (or a new tool you build from the same
pattern) is familiar too.

## Quick start

1. Pick a skill folder above and open its README for the full walkthrough (with a live
   demo link and bilingual instructions).
2. Copy that skill's folder into `~/.claude/skills/<name>/` (or a project's
   `.claude/skills/<name>/`) so Claude Code can find it.
3. Open Claude Code and say what you want, e.g. *"set up a fitting room for my clothes"*.

Custom Skills currently require **Claude Code** (desktop app, VS Code/JetBrains
extension, or terminal) — not the regular claude.ai chat website.

## License

MIT — see [LICENSE](LICENSE).
