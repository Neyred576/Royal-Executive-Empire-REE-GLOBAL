import glob, os, re

base = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Test\Web'
files = [os.path.join(base, 'ceo-profile.html'), os.path.join(base, 'gm-profile.html')]

old_desc = 'Royalty Executive Empire Limited &mdash; Building Wealth, Creating Opportunities, and Creating Global Impact across Africa and the world.'
new_desc = 'Royalty Executive Empire Limited &mdash; Building Empires, Shaping Futures, Leading Innovation across Africa and beyond.'

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_desc in content:
        content = content.replace(old_desc, new_desc)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(fpath)}")
