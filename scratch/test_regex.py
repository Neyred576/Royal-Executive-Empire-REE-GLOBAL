import os, re

files = ['.\\index.html', '.\\about.html', '.\\reel-tech-hub.html', '.\\reel-auto-center.html', '.\\reel-global-palace.html']
for p in files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    # Match the entire calendar column
    m = re.search(r'<!--\s*(?:Footer\s+)?Calendar\s+Widget\s*-->[\s\S]*?id="fc-days"[^>]*></div>\s*</div>\s*</div>', c, re.IGNORECASE)
    if m:
        print(f"{p}: MATCHED (len {len(m.group(0))})")
    else:
        # Check without HTML comment
        m2 = re.search(r'<div class="[^"]*footer-calendar-col[^"]*"[^>]*>[\s\S]*?id="fc-days"[^>]*></div>\s*</div>\s*</div>', c, re.IGNORECASE)
        print(f"{p}: m2 MATCHED: {bool(m2)}")

