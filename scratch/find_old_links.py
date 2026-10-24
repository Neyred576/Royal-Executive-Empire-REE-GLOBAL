import glob, os, re

base = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Test\Web'
files = glob.glob(os.path.join(base, '*.html'))

old_pages = ['reel-power.html', 'reel-branding.html', 'reel-smart.html', 'music-store.html', 'portfolio.html']

for op in old_pages:
    print(f"=== References to {op} ===")
    for fpath in sorted(files):
        fname = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            if op in line:
                print(f"  {fname}:{idx} -> {line.strip()[:100]}")
    print()
