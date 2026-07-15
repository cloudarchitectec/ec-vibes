#!/usr/bin/env python3
"""
Assemble the publishable staging-room.html from:
  - data.json                     (source of truth: sections, modules, items, ui)
  - staging-room.template.html    (markup + CSS + JS, with __TITLE__ / __DATA_JSON__ etc.)

No photos in this tool — items are text rows. Output goes to dist/ (gitignored,
regenerable); the only editable HTML in the tree is the template. Run this after
editing data.json, then (re)publish dist/staging-room.html as a Claude Artifact.

Usage:
  python3 build.py                    # stamps the "updated" date = today
  python3 build.py --date 2026-07-15  # pin the stamp (e.g. a non-data rebuild)
"""
import argparse, datetime, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data.json")
TEMPLATE = os.path.join(ROOT, "staging-room.template.html")
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(DIST, "staging-room.html")
ARTIFACT_URL_FILE = os.path.join(ROOT, ".artifact-url")


def validate(data):
    """Referential integrity + id stability. Checked state in the browser is keyed by
    sec|group-or-module|name, so a rename resets that item's tick — fine, but
    duplicates would make two rows share one checkbox."""
    problems = []
    secs = {s["key"] for s in data["sections"]}
    mods = {m["key"] for m in data.get("modules", [])}
    seen = set()
    for it in data["items"]:
        where = f"item {it.get('name')!r}"
        if it["sec"] not in secs:
            problems.append(f"{where}: unknown sec {it['sec']!r}")
        if it.get("module") and it["module"] not in mods:
            problems.append(f"{where}: unknown module {it['module']!r}")
        if it["sec"] == "situational" and not it.get("module"):
            problems.append(f"{where}: situational item needs a module")
        if it["sec"] != "situational" and not it.get("module") and not it.get("group"):
            problems.append(f"{where}: needs a group")
        iid = it["sec"] + "|" + ("m:" + it["module"] if it.get("module") else it.get("group", "")) + "|" + it["name"]
        if iid in seen:
            problems.append(f"duplicate item id {iid!r} — rename one of them")
        seen.add(iid)
    if problems:
        raise SystemExit("data.json problems:\n  " + "\n  ".join(problems))


def main():
    ap = argparse.ArgumentParser(description="Build the self-contained staging-room artifact.")
    ap.add_argument("--date", metavar="YYYY-MM-DD",
                    help="Pin the 'updated' stamp instead of using today.")
    args = ap.parse_args()
    updated = args.date or datetime.date.today().isoformat()

    data = json.load(open(DATA, encoding="utf-8"))
    validate(data)
    data["updated"] = updated  # build owns the timestamp, not data.json

    ui = data.get("ui", {})
    html = open(TEMPLATE, encoding="utf-8").read()
    for token, value in {
        "__TITLE__": ui.get("title", ""),
        "__SUBTITLE__": ui.get("subtitle", ""),
        "__UPDATED_LABEL__": ui.get("updatedLabel", ""),
        "__SEARCH_PH__": ui.get("searchPlaceholder", ""),
    }.items():
        html = html.replace(token, value)
    html = html.replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))

    os.makedirs(DIST, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    n_core = sum(1 for it in data["items"] if not it.get("module"))
    n_mod = len(data["items"]) - n_core
    print(f"Built dist/staging-room.html · {n_core} core + {n_mod} situational items · "
          f"updated {updated} · ~{round(os.path.getsize(OUT)/1024,1)}KB")

    if os.path.exists(ARTIFACT_URL_FILE):
        url = open(ARTIFACT_URL_FILE, encoding="utf-8").read().strip()
        print(f"\nRepublish dist/staging-room.html to the SAME artifact URL:\n  {url}")
    else:
        print(f"\nNo saved artifact URL yet ({os.path.basename(ARTIFACT_URL_FILE)} not found).")
        print("Publish dist/staging-room.html as a new Claude Artifact, then save the URL it")
        print(f"gives you into {os.path.basename(ARTIFACT_URL_FILE)} so future rebuilds update the same link.")


if __name__ == "__main__":
    main()
