import os
import re

div_domains = [
    "reeltech.reelholding.com.ng",
    "the-new-reel-suv.ai.studio",
    "reelproperties.reelholding.com.ng",
    "reelglobal.reelholding.com.ng"
]

web_dir = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web"
files_modified = 0

for root, dirs, files in os.walk(web_dir):
    if any(x in root for x in ["Backup", "node_modules", ".git", "scratch"]):
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            orig = content
            for dom in div_domains:
                # 1. target="_blank" after href
                pattern1 = re.compile(rf"""(<a\s+[^>]*href=["\']https?://{re.escape(dom)}[^"\']*["\'][^>]*)target=["\']_blank["\']\s*""", re.IGNORECASE)
                content = pattern1.sub(r"\1", content)
                # 2. target="_blank" before href
                pattern2 = re.compile(rf"""(<a\s+[^>]*)target=["\']_blank["\']\s*([^>]*href=["\']https?://{re.escape(dom)}[^"\']*["\'][^>]*)""", re.IGNORECASE)
                content = pattern2.sub(r"\1\2", content)
                # 3. rel="noopener noreferrer" after href
                pattern3 = re.compile(rf"""(<a\s+[^>]*href=["\']https?://{re.escape(dom)}[^"\']*["\'][^>]*)rel=["\'](?:noopener\s+noreferrer|noopener|noreferrer)["\']\s*""", re.IGNORECASE)
                content = pattern3.sub(r"\1", content)
                # 4. rel="noopener noreferrer" before href
                pattern4 = re.compile(rf"""(<a\s+[^>]*)rel=["\'](?:noopener\s+noreferrer|noopener|noreferrer)["\']\s*([^>]*href=["\']https?://{re.escape(dom)}[^"\']*["\'][^>]*)""", re.IGNORECASE)
                content = pattern4.sub(r"\1\2", content)

            if content != orig:
                files_modified += 1
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated: {os.path.relpath(path, web_dir)}")

print(f"Total files updated: {files_modified}")

