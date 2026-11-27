import glob

for f in sorted(glob.glob('*.html')):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    has_insta_footer = 'footer-insta-col' in text
    has_footer = '<footer' in text
    print(f"{f:30s} | has footer: {has_footer} | has insta footer: {has_insta_footer}")
