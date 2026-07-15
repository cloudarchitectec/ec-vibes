#!/usr/bin/env python3
"""
Assemble the publishable fitting-room.html from:
  - data.json                     (source of truth: records, categories, seasons, ui)
  - fitting-room.template.html    (markup + CSS + JS, with __TITLE__ / __DATA_JSON__ / __PHOTOS_JSON__ tokens)
  - photos/<sku>.<ext>             (per-record original images, optional)

Photos are resized (<=360px, jpeg q72) and inlined as base64 data URIs because the
Claude Artifact CSP blocks all remote image requests. Run this after editing
data.json or adding a photo, then (re)publish dist/fitting-room.html as a Claude
Artifact.

Requires Pillow for photo resizing: pip install pillow
(No photos at all? That's fine — skip photos/ entirely and this still works.)

Usage:
  python3 build.py                    # stamps the "updated" date = today
  python3 build.py --date 2026-07-14  # pin the stamp (e.g. a non-data rebuild)
"""
import argparse, base64, datetime, glob, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data.json")
TEMPLATE = os.path.join(ROOT, "fitting-room.template.html")
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(DIST, "fitting-room.html")
PHOTOS_DIR = os.path.join(ROOT, "photos")
ARTIFACT_URL_FILE = os.path.join(ROOT, ".artifact-url")
MAX_PX = 360
JPEG_QUALITY = 72

# Measure labels are normalised here at build time (not in the page JS), so the baked
# data — cards and the size-range strip alike — always carries canonical keys.
# Fix data.json at source when a note below appears; this is a backstop. Add your own
# aliases here if you track measurements this list doesn't cover (e.g. "Neck", "Thigh").
MEASURE_CANON = {
    "bust": "Bust", "chest": "Bust",
    "waist": "Waist", "hip": "Hip",
    "inseam": "Inseam", "inleg": "Inseam",
    "shoulder": "Shoulder", "length": "Length", "sleeve": "Sleeve",
    "under-bust": "Under-bust", "cup": "Cup",
}


def normalise_measures(data):
    # record measures + each category's optional manual "range" (same [[label, value]] shape)
    targets = [(r.get("measures", []), f"SKU {r.get('sku','?')}") for r in data["records"]]
    targets += [(c.get("range", []), f"category {c['key']}") for c in data["categories"]]
    for measures, where in targets:
        for m in measures:
            canon = MEASURE_CANON.get(str(m[0]).strip().lower())
            if canon is None:
                print(f"⚠ unrecognised measure label {m[0]!r} ({where}) — "
                      f"left as-is; fix data.json or extend MEASURE_CANON in build.py")
            elif m[0] != canon:
                print(f"ℹ normalised measure label {m[0]!r} → {canon!r} ({where}) — "
                      f"please also fix data.json at source")
                m[0] = canon


def safe(sku):
    return re.sub(r"[^A-Za-z0-9._-]", "_", sku)


def data_uri(path):
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit(
            "Pillow is required to inline photos. Install it with:\n"
            "    pip install pillow\n"
            "or remove the photos/ folder if you don't want product photos."
        )
    img = Image.open(path)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    img.thumbnail((MAX_PX, MAX_PX))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser(description="Build the self-contained fitting-room artifact.")
    ap.add_argument("--date", metavar="YYYY-MM-DD",
                    help="Pin the 'updated' stamp instead of using today.")
    args = ap.parse_args()
    updated = args.date or datetime.date.today().isoformat()

    data = json.load(open(DATA, encoding="utf-8"))
    data["updated"] = updated                     # build owns the timestamp, not data.json
    data["records"].sort(key=lambda r: r["cat"])   # display order; data.json's own order can stay append-order
    normalise_measures(data)
    template = open(TEMPLATE, encoding="utf-8").read()

    photos, missing = {}, []
    if os.path.isdir(PHOTOS_DIR):
        for r in data["records"]:
            sku = r.get("sku")
            if not sku:
                continue
            hits = sorted(glob.glob(os.path.join(PHOTOS_DIR, safe(sku) + ".*")))
            if hits:
                photos[sku] = data_uri(hits[0])
            else:
                missing.append(sku)

    ui = data.get("ui", {})
    ui_map = {
        "__TITLE__": ui.get("title", ""),
        "__SUBTITLE__": ui.get("subtitle", ""),
        "__UPDATED_LABEL__": ui.get("updatedLabel", ""),
        "__SEARCH_PH__": ui.get("searchPlaceholder", ""),
    }
    html = template
    for token, value in ui_map.items():
        html = html.replace(token, value)
    html = html.replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))
    html = html.replace("__PHOTOS_JSON__", json.dumps(photos, ensure_ascii=False))
    os.makedirs(DIST, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Built dist/fitting-room.html · {len(data['records'])} records · "
          f"{len(photos)} photos · updated {updated} · ~{round(os.path.getsize(OUT)/1024,1)}KB")
    if missing:
        print("⚠ no photo for SKU:", ", ".join(missing))

    if os.path.exists(ARTIFACT_URL_FILE):
        url = open(ARTIFACT_URL_FILE, encoding="utf-8").read().strip()
        print(f"\nRepublish dist/fitting-room.html to the SAME artifact URL:\n  {url}")
    else:
        print(f"\nNo saved artifact URL yet ({os.path.basename(ARTIFACT_URL_FILE)} not found).")
        print("Publish dist/fitting-room.html as a new Claude Artifact, then save the URL it")
        print(f"gives you into {os.path.basename(ARTIFACT_URL_FILE)} so future rebuilds update the same link.")


if __name__ == "__main__":
    main()
