import glob, os, re

base = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Test\Web'
files = glob.glob(os.path.join(base, '*.html'))

keywords = [
    "REEL Power", "REEL Branding", "Vanny", "Efua", "Glorious Global Palace",
    "Building Wealth", "Building Empires", "Ibeju Lekki", "Lagos, Nigeria"
]

results = {k: [] for k in keywords}

for fpath in sorted(files):
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for kw in keywords:
        count = len(re.findall(re.escape(kw), content, re.IGNORECASE))
        if count > 0:
            results[kw].append((fname, count))

for kw, matches in results.items():
    print(f"=== Keyword: '{kw}' ({len(matches)} files) ===")
    for fname, count in matches:
        print(f"   {fname}: {count}")
    print()
