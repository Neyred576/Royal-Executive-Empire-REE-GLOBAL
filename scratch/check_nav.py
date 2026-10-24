import glob, os, re

base = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Test\Web'
files = glob.glob(os.path.join(base, '*.html'))

print(f"{'Page':25} | {'Nav Class':20} | {'Divisions':10} | {'Dropdown':10}")
print("-" * 75)

for fpath in sorted(files):
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    nav_match = re.search(r'<nav[^>]*id=["\']main-nav["\'][^>]*>', content)
    nav_tag = nav_match.group(0) if nav_match else 'NO NAV'
    
    cls_match = re.search(r'class=["\']([^"\']*)["\']', nav_tag)
    cls = cls_match.group(1) if cls_match else ''
    
    has_divisions = 'our-divisions-dropdown' in content
    has_dropdown = 'nav-dropdown' in content
    
    # Check what divisions links exist
    old_links = []
    for old_brand in ['reel-power.html', 'reel-branding.html', 'reel-smart.html', 'music-store.html', 'portfolio.html']:
        if old_brand in content:
            old_links.append(old_brand)

    print(f"{fname:25} | {cls:20} | {str(has_divisions):10} | {str(has_dropdown):10} | Old links: {len(old_links)}")
