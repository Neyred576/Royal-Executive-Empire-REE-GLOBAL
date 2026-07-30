import os
import re
import glob

def update_html_files():
    html_files = glob.glob('*.html')
    
    for file in html_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file, 'r', encoding='latin-1') as f:
                content = f.read()

        # 1. Header: Remove Home
        # Regex to match <li><a href="index.html" ...>Home</a></li>
        content = re.sub(r'<li>\s*<a href="index\.html"[^>]*>Home</a>\s*</li>', '', content)
        
        # 2. Header: Add Contact Us next to Shop
        # Check if Contact Us is already next to Shop
        if 'href="contact.html"' not in content[content.find('href="shop.html"'):content.find('href="shop.html"')+200] and re.search(r'<li>\s*<a href="shop\.html"[^>]*>Shop</a>\s*</li>', content):
            # Apply only in the nav-links area
            content = re.sub(r'(<ul[^>]*id="nav-links"[^>]*>.*?)(<li>\s*<a href="shop\.html"[^>]*>Shop</a>\s*</li>)(.*?</ul\s*>)', 
                             lambda m: m.group(1) + m.group(2) + '\n        <li><a href="contact.html" class="nav-link">Contact Us</a></li>' + m.group(3), 
                             content, flags=re.DOTALL)
            
        # 3. Footer: Remove Quick Links completely
        # Matches: <!-- Quick Links --> ... </div> up to the next <!--
        content = re.sub(r'<!--\s*Quick Links\s*-->\s*<div class="footer-col">\s*<h3 class="footer-heading">Quick Links</h3>.*?</div>', '', content, flags=re.DOTALL)
        # Sometime the comment is omitted, let's also remove if just the div exists
        content = re.sub(r'<div class="footer-col">\s*<h3 class="footer-heading">Quick Links</h3>.*?</nav>\s*</div>', '', content, flags=re.DOTALL)
        
        # 4. Footer Our Divisions: Remove Shop and Contact Us
        def filter_divisions(m):
            div_content = m.group(1)
            div_content = re.sub(r'<li>\s*<a href="shop\.html"[^>]*>Shop</a>\s*</li>', '', div_content)
            div_content = re.sub(r'<li>\s*<a href="contact\.html"[^>]*>Contact Us</a>\s*</li>', '', div_content)
            return '<h3 class="footer-heading">Our Divisions</h3>' + div_content

        content = re.sub(r'<h3 class="footer-heading">Our Divisions</h3>(.*?</ul\s*>)', filter_divisions, content, flags=re.DOTALL)
        
        try:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            with open(file, 'w', encoding='latin-1') as f:
                f.write(content)

if __name__ == '__main__':
    update_html_files()
    print("Done")
