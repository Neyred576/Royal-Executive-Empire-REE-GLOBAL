with open(r"C:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\admin\index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Look for where prop-status, tech-prod-status, palace-service-status, auto-car-status are used
for field in ['prop-status', 'tech-prod-status', 'palace-service-status', 'auto-car-status']:
    print(f"=== {field} ===")
    matches = [m.start() for m in re.finditer(re.escape(field), text)]
    for pos in matches:
        print(text[max(0, pos-100):min(len(text), pos+200)])
        print("-" * 30)
