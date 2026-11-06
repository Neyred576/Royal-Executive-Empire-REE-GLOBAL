import sys
sys.stdout.reconfigure(encoding='utf-8')

for p in ['.\\index.html', '.\\about.html', '.\\admin\\login.html', '.\\admin\\index.html']:
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
    print(f'=== {p} ===')
    for i, l in enumerate(lines):
        if 'fetchpriority="high"' in l and 'onerror' in l:
            print(f'Line {i+1}: {repr(l)}')

