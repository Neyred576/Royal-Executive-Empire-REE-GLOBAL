import os
import glob
import re

def update_html_files():
    directory = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web"
    
    # We will exclude admin folder for frontend notifications logic because admin has its own logic
    html_files = [f for f in glob.glob(os.path.join(directory, "**", "*.html"), recursive=True) if "admin" not in f]
    
    script_tag = '<script src="/js/notifications.js"></script>\n'
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'src="/js/notifications.js"' not in content:
            # Insert script right before </body>
            content = re.sub(r'(</body>)', lambda m: script_tag + m.group(1), content, flags=re.IGNORECASE)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")

if __name__ == "__main__":
    update_html_files()
