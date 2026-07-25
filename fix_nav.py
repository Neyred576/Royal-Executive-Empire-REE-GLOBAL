import os
import re

dir_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web"

new_desktop_menu = """      <!-- Desktop Menu -->
      <ul class="nav-links" id="nav-links" role="list">
        <li><a href="index.html" class="nav-link">Home</a></li>
        <li><a href="reel-power.html" class="nav-link">REEL Power</a></li>
        <li><a href="reel-branding.html" class="nav-link">REEL Branding</a></li>
        <li><a href="reel-smart.html" class="nav-link">REEL Smart</a></li>
        <li><a href="reel-business.html" class="nav-link">Business Solutions</a></li>
        <li><a href="blog.html" class="nav-link">Blog</a></li>
        <li><a href="shop.html" class="nav-link">Shop</a></li>
      </ul>

      <!-- E-Commerce Actions -->"""

for filename in os.listdir(dir_path):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We will replace everything from <!-- Desktop Menu --> to <!-- E-Commerce Actions -->
    pattern = re.compile(r'<!-- Desktop Menu -->.*?<!-- E-Commerce Actions -->', re.DOTALL)
    
    match = pattern.search(content)
    if match:
        new_nav = new_desktop_menu
        if filename == 'index.html':
            new_nav = new_nav.replace('href="index.html" class="nav-link"', 'href="index.html" class="nav-link active"')
        elif filename == 'reel-power.html':
            new_nav = new_nav.replace('href="reel-power.html" class="nav-link"', 'href="reel-power.html" class="nav-link active"')
        elif filename == 'reel-branding.html':
            new_nav = new_nav.replace('href="reel-branding.html" class="nav-link"', 'href="reel-branding.html" class="nav-link active"')
        elif filename == 'reel-smart.html':
            new_nav = new_nav.replace('href="reel-smart.html" class="nav-link"', 'href="reel-smart.html" class="nav-link active"')
        elif filename == 'reel-business.html':
            new_nav = new_nav.replace('href="reel-business.html" class="nav-link"', 'href="reel-business.html" class="nav-link active"')
        elif filename == 'blog.html':
            new_nav = new_nav.replace('href="blog.html" class="nav-link"', 'href="blog.html" class="nav-link active"')
        elif filename == 'shop.html':
            new_nav = new_nav.replace('href="shop.html" class="nav-link"', 'href="shop.html" class="nav-link active"')
            
        content = content[:match.start()] + new_nav + content[match.end():]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed nav links in {filename}")

