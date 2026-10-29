"""
Fix performance lagging:
1. Add loading="lazy" to all non-hero images in all HTML files
2. Add decoding="async" to all images
3. Add fetchpriority="high" to hero/above-fold images
"""
import os
import re
import glob

html_files = glob.glob("*.html") + glob.glob("admin/*.html")

# Images that are above the fold / hero — should stay eager + high priority
HERO_PATTERNS = [
    "hero_bg", "hero-bg", "logo", "LOGO",
    "DSC_4948", "DSC_4999", "DSC_4985",  # CEO/GM profile photos
]

def is_hero_image(src):
    for pat in HERO_PATTERNS:
        if pat.lower() in src.lower():
            return True
    return False

total_changed = 0
for filename in sorted(html_files):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    def replace_img(m):
        tag = m.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        src = src_match.group(1) if src_match else ""

        # Skip if already has loading attribute
        if "loading=" in tag:
            return tag

        # Hero images: eager load + high priority
        if is_hero_image(src):
            # Add fetchpriority if missing
            if "fetchpriority=" not in tag:
                tag = tag.rstrip(">").rstrip("/").rstrip() + ' fetchpriority="high">'
            return tag

        # All other images: lazy load + async decode
        if "decoding=" not in tag:
            tag = tag.rstrip(">").rstrip("/").rstrip() + ' decoding="async"'
        tag = tag.rstrip(">").rstrip("/").rstrip() + ' loading="lazy">'
        return tag

    content = re.sub(r'<img\s[^>]+>', replace_img, content, flags=re.IGNORECASE | re.DOTALL)

    if content != original:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        changed = content.count('loading="lazy"') - original.count('loading="lazy"')
        total_changed += changed
        print(f"  Fixed: {filename} (+{changed} lazy images)")

print(f"\nTotal lazy images added: {total_changed}")
