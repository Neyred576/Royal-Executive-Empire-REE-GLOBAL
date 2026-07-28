import os
import glob
import re

def update_html_files():
    directory = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web"
    
    # Files to ignore (e.g., in admin or specific ones)
    # We should add it to admin as well, so maybe all .html
    html_files = glob.glob(os.path.join(directory, "**", "*.html"), recursive=True)
    
    head_tags = """
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#D4AF37" />
  <link rel="apple-touch-icon" href="/Images/icons/icon-192x192.png" />
"""

    body_tag = """
  <script src="/js/pwa.js"></script>
"""

    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False
        
        if 'rel="manifest"' not in content:
            # Insert head tags right before </head>
            content = re.sub(r'(</head>)', lambda m: head_tags + m.group(1), content, flags=re.IGNORECASE)
            changed = True
            
        if 'src="/js/pwa.js"' not in content:
            # Insert body script right before </body>
            content = re.sub(r'(</body>)', lambda m: body_tag + m.group(1), content, flags=re.IGNORECASE)
            changed = True
            
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")

if __name__ == "__main__":
    update_html_files()
