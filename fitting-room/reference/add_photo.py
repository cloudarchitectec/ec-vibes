#!/usr/bin/env python3
"""
Fetch a product photo and save the ORIGINAL locally under ./photos/<sku>.<ext>.

We keep originals so we never depend on the source URL again (it may 404 later).
The publishable HTML is assembled by build.py, which resizes + base64-embeds
whatever is in ./photos/ (the Claude Artifact CSP blocks remote images, so they
must be inlined). This script does NOT touch the HTML — run build.py after.

Usage:
    python3 add_photo.py "SKU123" "https://example.com/product-page-or-direct-image-url"

- A direct image URL (.jpg/.png/.webp) is used as-is; otherwise the page's
  og:image (falling back to twitter:image) is used.
- The SKU must match the record's `sku` in data.json. Re-running replaces the original.
- Photos are entirely optional — plenty of people run this tool with none at all.
"""
import os, re, subprocess, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PHOTOS_DIR = os.path.join(ROOT, "photos")
UA = "Mozilla/5.0"


def curl(url, out=None):
    cmd = ["curl", "-sL", "--max-time", "25", "-A", UA, url]
    if out:
        cmd += ["-o", out]
        subprocess.run(cmd, check=False)
        return None
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout


def resolve_image_url(url):
    if re.search(r"\.(jpe?g|png|webp)(\?|$)", url, re.I):
        return url
    page = curl(url)
    m = re.search(r'<meta[^>]+property="og:image"[^>]*content="([^"]+)"', page)
    if not m:
        m = re.search(r'<meta[^>]+name="twitter:image"[^>]*content="([^"]+)"', page)
    if m:
        return m.group(1).replace("http://", "https://")
    raise SystemExit(f"Could not find an image on {url} — pass a direct image URL instead.")


def safe(sku):
    return re.sub(r"[^A-Za-z0-9._-]", "_", sku)


def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    sku, url = sys.argv[1], sys.argv[2]
    img_url = resolve_image_url(url)
    os.makedirs(PHOTOS_DIR, exist_ok=True)
    m = re.search(r"\.(jpe?g|png|webp)", img_url, re.I)
    ext = ("." + m.group(1).lower()) if m else ".jpg"
    # remove any existing original for this SKU (extension may differ)
    for old in glob.glob(os.path.join(PHOTOS_DIR, safe(sku) + ".*")):
        os.remove(old)
    dst = os.path.join(PHOTOS_DIR, safe(sku) + ext)
    curl(img_url, dst)
    if not os.path.exists(dst) or os.path.getsize(dst) < 2000:
        raise SystemExit(f"Download failed or too small: {img_url}")
    print(f"Saved {os.path.relpath(dst, ROOT)} ({round(os.path.getsize(dst)/1024)}KB) from {img_url}")
    print("Next: run build.py, then republish fitting-room.html.")


if __name__ == "__main__":
    main()
