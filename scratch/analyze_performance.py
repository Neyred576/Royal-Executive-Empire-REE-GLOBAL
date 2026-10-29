import os
import glob
import re

html_files = glob.glob("*.html")
print(f"Total HTML files: {len(html_files)}")

# Check background images in style.css or html
with open("css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

bg_images = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', css)
print(f"CSS Background images count: {len(bg_images)}")
for bg in bg_images:
    clean_bg = bg.replace('../', '').replace('/', os.sep)
    if os.path.exists(clean_bg):
        sz = os.path.getsize(clean_bg)
        if sz > 500 * 1024:
            print(f"  HEAVY CSS BG: {sz/(1024*1024):.2f} MB -> {clean_bg}")

print("\n--- HTML Image Payload ---")
for h in sorted(html_files):
    with open(h, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()
    srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', c, re.IGNORECASE)
    total_sz = 0
    heavy_imgs = []
    for s in srcs:
        if s.startswith("http") or s.startswith("data:"):
            continue
        clean_s = s.replace("/", os.sep)
        if os.path.exists(clean_s):
            sz = os.path.getsize(clean_s)
            total_sz += sz
            if sz > 1 * 1024 * 1024: # > 1MB
                heavy_imgs.append((sz, clean_s))
    if total_sz > 5 * 1024 * 1024 or len(heavy_imgs) > 0:
        print(f"{h:25} Total: {total_sz/(1024*1024):.2f} MB | {len(heavy_imgs)} heavy images (>1MB)")
        for sz, path in heavy_imgs[:3]:
            print(f"    - {sz/(1024*1024):.2f} MB : {path}")
