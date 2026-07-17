 ---
name: text-polish
summary: "Rewrite rough notes into polished, professional messages"
description: "Text polish / proofread skill. Use when: text-polish, /proofread, proofread this, polish my message, clean this up, make this professional, rewrite this for an email, tidy up this chat post, write a shout-out, draft a ticket, make this sound professional, fix the tone of this. Rewrites rough notes/keywords into a concise, professional message tailored to a chosen channel (email, meeting invite, announcement, chat message, shout-out, ticket)."
argument-hint: "[type: email | invite | announcement | message | kudos | ticket — e.g. text-polish email or /proofread email]"
---
 
# Text Polish — Professional Tone
 
## What this does
You jot down rough notes, bullet points, or half-formed sentences. This skill rewrites them into a clean, professional message that's ready to copy and paste — matched to where you're sending it (an email, a meeting invite, a chat message, and so on).
 
You don't need to know anything technical. Just tell it the kind of message you want and paste your notes.
 
---
 
## Your Preferences
 
<!-- The skill reads and updates this block. If "Set up" is "no", run First-Run Setup before anything else. -->
 
- **Set up:** no
- **Language:** English
 
---
 
## First-Run Setup
Run this **once**, the first time the skill is used (i.e. when **Set up: no** above), before doing any rewriting.
 
1. Greet the user in one short line and explain you'll set a couple of preferences that take two seconds and can be changed anytime.
2. Ask their language preference:
   ```
   Which English would you like me to write in — UK English or US English?
   ```
   (For now, write in standard English either way; record their choice for future use.)
3. Show the defaults in **one line each** so they can skim, then ask if they're happy or want to tweak anything:
   ```
   Here are the message types I can polish text into. Defaults shown — happy to go with these, or want to change anything? (You can always update later.)
 
   • email        — a full, formal email. Gives you 3 subject-line options + a tidy body.
   • invite       — a meeting invitation. Gives you 3 title options + a short description.
   • announcement — a short, punchy team/channel announcement of a change.
   • message      — a friendly, professional chat/DM message.
   • kudos        — a short, warm public shout-out for a colleague.
   • ticket       — a work ticket: short title + Summary, Pre-Requisites, Testing, Technical Details.
   ```
4. Whatever they choose, record their preferences:
   - **If your agent can edit files:** update the **Your Preferences** block above — set `Set up:` to `yes`, set `Language:` to their choice (`UK English` or `US English`), and add a line for any changed default (e.g. `- **email:** no subject options, single subject line`).
   - **If your agent cannot edit files** (e.g. a chat-only or prompt-library setup): just remember the choices for this conversation, and let the user know they can note them at the top of their saved prompt so they stick next time.
5. Confirm in one short line that setup is done and ask them to paste the notes they'd like polished (and which type).
 
> After setup, never run this section again unless the user asks to "change my preferences" / "reset preferences".
 
---
 
## Core Principles
- **Preserve meaning, never invent.** Don't add facts, names, dates, numbers, or links the user didn't provide. If a detail is expected but missing (e.g. a meeting time), leave a clear `[placeholder]` rather than guessing.
- **Concise over verbose.** Cut filler and repetition. Short sentences, active voice. Professional ≠ wordy.
- **Match the channel's tone** using the type table below — don't make a quick chat message sound like a legal email.
- **Write in the user's chosen language** (see Your Preferences; default standard English).
- **Keep the user's voice and intent** — polish tone and clarity, don't change the substance or add opinions.
- **Ready to paste.** Output only the final message plus the single `Assumptions:` line. No preamble like "Here is your rewritten text".
- **Don't over-format.** Use tables/bullets only where they genuinely help; keep formatting light otherwise.
 
## Type System
 
| Type (aliases) | Formality | Purpose | Length & format |
|----------------|-----------|---------|-----------------|
| **email** (`email`, `mail`, `formal`) | Formal | Full written communication | Longer text allowed. Always produce **3 subject-line options** to choose from, then the body. Bullet lists and simple tables permitted where they aid clarity. Greeting + sign-off placeholder (`Hi [name],` / `Kind regards,`). |
| **invite** (`invite`, `meeting`, `meeting-invite`, `calendar`) | Semi-formal | Meeting invitation | Short. Produce **3 subject-line options** (meeting titles) to choose from, then **one** 1–3 sentence description giving enough context (purpose, what's needed from attendees). Tables permitted where they genuinely aid clarity. |
| **announcement** (`announcement`, `announce`, `post`) | Semi-formal | Team/channel announcement of a change | Short, crisp, punchy. Lead with the change, then impact/action. Tables permitted where they aid scanning. Emoji optional and sparing. Scannable. |
| **message** (`message`, `msg`, `chat`, `dm`) | Formal-casual | Direct/channel chat message | Short, friendly, professional but relaxed. Conversational, easy to read; contractions fine. Tables permitted where they aid clarity. No subject line. |
| **kudos** (`kudos`, `shoutout`, `praise`, `recognition`, `thanks`) | Warm-professional | Short public recognition of a colleague | Very short (1–3 sentences). Warm, specific, genuine. Name the person and the specific thing they did well and its impact. Plain text, upbeat but not gushing. No subject line. Preserve any recognition tokens the user includes. |
| **ticket** (`ticket`, `jira`, `story`, `task`, `issue`) | Formal | Work ticket for a task | Produce a short, meaningful `Title:` line, then sections: **Summary** (1–2 sentence what/why, plus any tooling note), **Pre-Requisites** (bullets), **Testing Details / Approach** (bullets), **Technical Details** (bullets). Keep bullets concise; use `[placeholder]` for missing-but-expected detail. |
 
If the type is missing or unrecognised, ask which type using the six options above — do not assume one.
 
## How to invoke (any agent)
This works with any AI assistant — GitHub Copilot, Claude, Codex/ChatGPT, or a saved prompt library. Trigger it by either:
- a short command like `text-polish email` or `/proofread email`, **or**
- plain language, e.g. "polish this as an email", "tidy this into a Teams message", "write a kudos from these notes".
 
If your assistant supports skills/instruction files, place this `SKILL.md` where it loads them. If not, paste the contents of this `SKILL.md` into your assistant's system prompt / custom instructions / saved prompt, then use the triggers above.
 
## Configuration
- **Rewrite model**: the user's current/default model. (No specific model is required.)
- **Output**: chat only (the user copies from the reply). Do not write files, other than optionally updating the **Your Preferences** block in this skill when the agent supports file edits.
- **Language**: as recorded in Your Preferences (default standard English).
 
---
 
## Procedure
 
### Step 0 — Check preferences
Look at the **Your Preferences** block. If **Set up: no**, run **First-Run Setup** first. Otherwise continue.
 
### Step 1 — Resolve the type
Read the `{type}` argument after `/proofread` (or the user's request) and map it via the aliases in the Type System table.
 
If no type was given, or it doesn't map to a known type, ask:
```
Which format should I polish this into — email, invite, announcement, message, kudos, or ticket?
```
Stop until answered.
 
---
 
### Step 2 — Gather the source text
The source text is whatever the user wants polished — either typed inline with the request, or the message(s) immediately before it in the conversation.
 
If there is no source text to work with, ask:
```
Paste the notes/keywords you'd like me to polish as a {type}.
```
Stop until provided.
 
---
 
### Step 3 — Do the rewrite
Rewrite the source text yourself (using the current model) into the chosen type. Build the rewrite around ALL of the following:
 
1. The role: "You are a professional copy-editor. Rewrite the source text into a polished, concise, professional message in the user's chosen language."
2. The **Core Principles** above (preserve meaning / never invent, concise, keep voice, ready to paste).
3. The specific **row for `{type}`** from the Type System table (formality, purpose, length & format rules), plus any per-type override recorded in Your Preferences.
4. Make reasonable choices rather than asking follow-up questions; record any such choices on the `Assumptions:` line.
5. Return ONLY the final message. Then on a new final line starting with `Assumptions:` give a single short line noting any placeholders used or notable tone/scope choices (or `Assumptions: none`).
 
> If you'd rather keep the rewrite consistent regardless of the running model, you may delegate it to a sub-agent — but this is optional and not required.
 
---
 
### Step 4 — Present the result
Show the user, in chat, exactly:
1. The polished message.
   - For `email`: list the **3 subject-line options** first, then the body.
   - For `invite`: list the **3 subject-line options** first, then the single description body.
   - For `ticket`: keep the `Title:` line first, then the sectioned body.
2. The single `Assumptions:` line beneath it.
 
Do not add commentary before or after. If the user says the tone/length is off, redo Step 3 with their adjustment folded in.
 
---
 
## Tips
- If the source text mixes two intents (e.g. an announcement *and* a follow-up question), polish the primary one and flag the split on the `Assumptions:` line rather than merging them.
- Placeholders (`[name]`, `[date/time]`, `[link]`) are expected for `email`, `invite`, and `ticket` — never fabricate real values to fill them.
- `announcement` and `message` may include tables where they aid scanning; keep formatting otherwise light.
- For `email` and `invite`, always return exactly 3 distinct subject-line options; `invite` returns only one description body.
- For `ticket`, always lead with a short, meaningful `Title:` and mirror the section headings (Summary / Pre-Requisites / Testing Details / Approach / Technical Details).
- This skill only rewrites tone and clarity in the same language. It does **not** translate between languages, fact-check claims, or send/post the message anywhere — that's on the user.
- To change your settings at any time, just say "change my text-polish preferences".