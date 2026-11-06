import os

targets = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
                if 'fetchpriority="high"' in c and 'onerror=' in c:
                    targets.append(p)

print("Files with broken onerror:", targets)

