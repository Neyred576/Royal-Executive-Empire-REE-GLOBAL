import glob
import os
import re

WEB_DIR = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web"
html_files = glob.glob(os.path.join(WEB_DIR, "*.html"))

SUBDOMAIN = "https://reelproperties.reelholding.com.ng"

print(f"Scanning {len(html_files)} HTML files for real-estate links...")

total_replaced = 0

for filepath in html_files:
    fname = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1. Mega-menu card:
    # <a href="real-estate.html" class="mega-div-card" aria-label="REEL Properties">
    content = re.sub(
        r'<a\s+href=[\'"]/?real-estate\.html[\'"]\s+class="mega-div-card"',
        f'<a href="{SUBDOMAIN}" target="_blank" rel="noopener noreferrer" class="mega-div-card"',
        content
    )

    # 2. Nav links:
    # <li><a href="real-estate.html">REEL Properties</a></li>
    content = re.sub(
        r'<a\s+href=[\'"]/?real-estate\.html[\'"]>REEL Properties</a>',
        f'<a href="{SUBDOMAIN}" target="_blank" rel="noopener noreferrer">REEL Properties</a>',
        content
    )

    # 3. Explore Division card CTA link:
    # <a href="real-estate.html" class="div-cta-link" aria-label="Explore REEL Properties">
    content = re.sub(
        r'<a\s+href=[\'"]/?real-estate\.html[\'"]\s+class="div-cta-link"',
        f'<a href="{SUBDOMAIN}" target="_blank" rel="noopener noreferrer" class="div-cta-link"',
        content
    )

    # 4. Gold links in text:
    # <a href="real-estate.html" class="gold-link">REEL Properties</a>
    content = re.sub(
        r'<a\s+href=[\'"]/?real-estate\.html[\'"]\s+class="gold-link">REEL Properties</a>',
        f'<a href="{SUBDOMAIN}" target="_blank" rel="noopener noreferrer" class="gold-link">REEL Properties</a>',
        content
    )

    # 5. Any remaining <a href="real-estate.html"> or href="/real-estate.html"
    content = re.sub(
        r'<a\s+href=[\'"]/?real-estate\.html[\'"](?![^>]*target=)',
        f'<a href="{SUBDOMAIN}" target="_blank" rel="noopener noreferrer"',
        content
    )

    # 6. Any <a href="real-estate.html" ...> that already has target
    content = re.sub(
        r'href=[\'"]/?real-estate\.html[\'"]',
        f'href="{SUBDOMAIN}"',
        content
    )

    # 7. Any href="/real-estate"
    content = re.sub(
        r'href=[\'"]/?real-estate[\'"]',
        f'href="{SUBDOMAIN}"',
        content
    )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        total_replaced += 1
        print(f"Updated {fname}")

print(f"Total files updated: {total_replaced}")
