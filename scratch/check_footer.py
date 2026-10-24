import glob, os, re

base = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Test\Web'
files = glob.glob(os.path.join(base, '*.html'))

for fpath in sorted(files):
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    m = re.search(r'<p class=["\']footer-brand-desc["\']>(.*?)</p>', content, re.DOTALL)
    if m:
        text = ' '.join(m.group(1).split())
        if 'Building Empires' not in text:
            print(f"{fname:25}: {text}")
    else:
        print(f"{fname:25}: NO footer-brand-desc")
