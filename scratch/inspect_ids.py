import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# The broken img tag - find it exactly and replace with clean version
# The issue: onerror contains unescaped fetchpriority="high" which breaks the HTML attribute

OLD_IMG = '<div class="sb-ring-core">\n          <img src="../Images/BG/reel_logo.png" alt="REEL" onerror="this.outerHTML=\'<span style=\\\'font-size:1.4rem\\\' fetchpriority=\"high\">⚜</span>\'" />\n        </div>'

NEW_IMG = '<div class="sb-ring-core">\n          <img src="../Images/BG/reel_logo.png" alt="REEL" fetchpriority="high" onerror="this.style.display=\'none\'" />\n        </div>'

if OLD_IMG in text:
    text = text.replace(OLD_IMG, NEW_IMG, 1)
    with open('admin/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("FIXED: Logo img tag cleaned up.")
else:
    print("Exact match not found. Trying line-based fix...")
    # Line based fix
    lines = text.splitlines(keepends=True)
    for i, l in enumerate(lines):
        if 'sb-ring-core' in l and '<div' in l:
            print(f"Found at line {i+1}")
            # Check next line for the broken img
            if i+1 < len(lines) and 'reel_logo.png' in lines[i+1]:
                print(f"Broken img line {i+2}:")
                print(repr(lines[i+1]))
                lines[i+1] = '          <img src="../Images/BG/reel_logo.png" alt="REEL" fetchpriority="high" onerror="this.style.display=\'none\'" />\n'
                text = ''.join(lines)
                with open('admin/index.html', 'w', encoding='utf-8', newline='') as f:
                    f.write(text)
                print("FIXED via line-based approach.")
                break
