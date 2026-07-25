import os
import re

dir_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web"

new_nav_links_template = """        <li><a href="index.html" class="nav-link">Home</a></li>
        <li><a href="reel-power.html" class="nav-link">REEL Power</a></li>
        <li><a href="reel-branding.html" class="nav-link">REEL Branding</a></li>
        <li><a href="reel-smart.html" class="nav-link">REEL Smart</a></li>
        <li><a href="reel-business.html" class="nav-link">Business Solutions</a></li>
        <li><a href="blog.html" class="nav-link">Blog</a></li>
        <li><a href="shop.html" class="nav-link">Shop</a></li>"""

for filename in os.listdir(dir_path):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find the content between <ul class="nav-links" id="nav-links" role="list"> and </ul>
    pattern = re.compile(r'(<ul class="nav-links" id="nav-links" role="list">)(.*?)(</ul>)', re.DOTALL)
    
    match = pattern.search(content)
    if match:
        new_nav = new_nav_links_template
        # Add active class for the current file
        # We find the a tag with href="filename" and add active class
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
            
        new_nav_block = f"{match.group(1)}\n{new_nav}\n      {match.group(3)}"
        content = content[:match.start()] + new_nav_block + content[match.end():]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated nav links in {filename}")

# Now update the sections in index.html
index_path = os.path.join(dir_path, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find SECTION 2 (Founder)
# Find SECTION 4 (Business Divisions)
# We will extract SECTION 4 and insert it before SECTION 2

sec2_pattern = re.compile(r'(\s*<!-- =+ -->\s*<!-- SECTION 2[^>]*?-->.*?)(?=\s*<!-- =+ -->\s*<!-- SECTION 3)', re.DOTALL)
sec4_pattern = re.compile(r'(\s*<!-- =+ -->\s*<!-- SECTION 4[^>]*?-->.*?)(?=\s*<!-- =+ -->\s*<!-- SECTION 5)', re.DOTALL)

sec2_match = sec2_pattern.search(index_content)
sec4_match = sec4_pattern.search(index_content)

if sec2_match and sec4_match:
    sec4_text = sec4_match.group(1)
    
    # Remove sec4_text from its original place
    new_content = index_content[:sec4_match.start()] + index_content[sec4_match.end():]
    
    # Find new start of sec2 since length changed
    sec2_match_new = sec2_pattern.search(new_content)
    
    if sec2_match_new:
        final_content = new_content[:sec2_match_new.start()] + sec4_text + new_content[sec2_match_new.start():]
        
        # fix the section numbers in comments just to be clean
        # But maybe it's not strictly necessary, I can just leave it as is or do a simple replace
        # "SECTION 2" -> "SECTION temp"
        # "SECTION 4" -> "SECTION 2"
        # "SECTION 3" -> "SECTION 4"
        # "SECTION temp" -> "SECTION 3"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print("Reordered sections in index.html")
    else:
        print("Failed to find sec2 in new_content")
else:
    print("Failed to find sec2 or sec4")
