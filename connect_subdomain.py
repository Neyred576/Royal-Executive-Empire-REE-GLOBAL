import os
import glob
import re

SUBDOMAIN_URL = "https://reelglobal.reelholding.com.ng"

files = [f for f in glob.glob("*.html") if f != "REEL_MultiSite_Strategy_Plan.html"]
updated_count = 0

for file in files:
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content

    # 1. Mega-menu card link:
    # <a href="reel-global-palace/" class="mega-div-card" aria-label="REEL Global Palace">
    content = re.sub(
        r'<a\s+href=["\'](?:/)?reel-global-palace/?["\']\s+class=["\']mega-div-card["\']',
        f'<a href="{SUBDOMAIN_URL}" target="_blank" rel="noopener noreferrer" class="mega-div-card"',
        content
    )

    # 2. Dropdown link:
    # <li><a href="reel-global-palace/">REEL Global Palace</a></li>
    content = re.sub(
        r'<li><a\s+href=["\'](?:/)?reel-global-palace/?["\']>REEL Global Palace</a></li>',
        f'<li><a href="{SUBDOMAIN_URL}" target="_blank" rel="noopener noreferrer">REEL Global Palace</a></li>',
        content
    )

    # 3. Footer link:
    # <li><a href="reel-global-palace/">REEL Global Palace</a></li>
    # (Covered by above)

    # 4. Explore button in division card:
    # <a href="reel-global-palace/" class="div-cta-link" aria-label="Explore REEL Global Palace">
    content = re.sub(
        r'<a\s+href=["\'](?:/)?reel-global-palace/?["\']\s+class=["\']div-cta-link["\']',
        f'<a href="{SUBDOMAIN_URL}" target="_blank" rel="noopener noreferrer" class="div-cta-link"',
        content
    )

    # 5. Inline gold-link:
    # <a href="reel-global-palace/" class="gold-link">REEL Global Palace</a>
    content = re.sub(
        r'<a\s+href=["\'](?:/)?reel-global-palace/?["\']\s+class=["\']gold-link["\']>REEL Global Palace</a>',
        f'<a href="{SUBDOMAIN_URL}" target="_blank" rel="noopener noreferrer" class="gold-link">REEL Global Palace</a>',
        content
    )

    # 6. Any remaining href="reel-global-palace/" (e.g. quick links in 404, etc.)
    content = re.sub(
        r'href=["\'](?:/)?reel-global-palace/?["\']',
        f'href="{SUBDOMAIN_URL}" target="_blank" rel="noopener noreferrer"',
        content
    )

    if content != original:
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        updated_count += 1
        print(f"Updated {file}")

print(f"\nDone: Updated {updated_count} HTML files to point to {SUBDOMAIN_URL}")

