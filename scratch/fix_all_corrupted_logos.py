import os, re

corrupted_pattern = re.compile(r'onerror="this\.outerHTML=\'<span style=\\\'font-size:[^\']*\\\'\s*fetchpriority="high">[^<]*</span>\'"')

fixed_files = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
            if 'fetchpriority="high">' in c and 'onerror=' in c:
                # check if it matches the broken outerHTML
                new_c = re.sub(
                    r'onerror="this\.outerHTML=\'<span style=\\\'[^\\\']*\\\'\s*fetchpriority="high">[^<]*</span>\'"',
                    'fetchpriority="high" onerror="this.style.display=\'none\'"',
                    c
                )
                if new_c != c:
                    with open(p, 'w', encoding='utf-8', newline='\r\n') as fp:
                        fp.write(new_c)
                    fixed_files.append(p)

print("Fixed files:", fixed_files)

