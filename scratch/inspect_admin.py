with open('admin/index.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

import re

# find sections/forms related to blog / posts
print("=== Forms in admin/index.html ===")
for m in re.finditer(r'<form\s+id="([^"]+)"', html):
    print("Form ID:", m.group(1))

# find blog/post fields
print("\n=== Blog / Post IDs in admin/index.html ===")
for m in re.finditer(r'id="(post-[^"]+|blog-[^"]+)"', html):
    print("ID:", m.group(1))
