with open(r"C:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\admin\index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Look for badge rendering in lists
matches = re.finditer(r'item\.status|data\.status', text)
for m in matches:
    pos = m.start()
    print(text[max(0, pos-150):min(len(text), pos+250)])
    print("=" * 40)
