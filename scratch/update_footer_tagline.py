import glob, os, re

base = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Test\Web'
files = glob.glob(os.path.join(base, '*.html'))

old_desc_pattern = re.compile(r'<p class=["\']footer-brand-desc["\']>Royalty Executive Empire Limited &mdash; Building Wealth, Creating Opportunities, and\s*Creating Global Impact across Africa and the world since our founding\.</p>', re.DOTALL)
new_desc = '<p class="footer-brand-desc">Royalty Executive Empire Limited &mdash; Building Empires, Shaping Futures, Leading Innovation across Africa and beyond.</p>'

updated_files = []
for fpath in sorted(files):
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if old_desc_pattern.search(content):
        new_content = old_desc_pattern.sub(new_desc, content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_files.append(fname)

print(f"Updated {len(updated_files)} files:")
for f in updated_files:
    print("  -", f)
