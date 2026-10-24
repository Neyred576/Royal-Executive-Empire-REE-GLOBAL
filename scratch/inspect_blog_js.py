with open('admin/index.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

import re

# find submit handler for form-blog
idx_blog_sub = html.find("document.getElementById('form-blog')")
if idx_blog_sub == -1:
    idx_blog_sub = html.find('form-blog')
print("=== form-blog JS snippet ===")
print(html[idx_blog_sub:idx_blog_sub+3000])

# find edit blog function
for m in re.finditer(r'function\s+(?:editBlog|editPost|loadBlog|renderBlog)[^{]*\{', html):
    start = m.start()
    print("\n=== Found function:", m.group(0), "===")
    print(html[start:start+1500])
