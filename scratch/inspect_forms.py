with open('admin/index.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

import re

# Find form-blog HTML
idx_blog_form = html.find('id="form-blog"')
print("=== form-blog snippet ===")
print(html[idx_blog_form:idx_blog_form+2500])

# Find form-properties snippet for comparison
idx_prop_form = html.find('id="form-properties"')
print("\n=== form-properties snippet ===")
print(html[idx_prop_form:idx_prop_form+2500])
