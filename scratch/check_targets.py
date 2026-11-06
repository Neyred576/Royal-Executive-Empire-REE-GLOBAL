import glob, re

files = glob.glob(r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\*.html')
found = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    matches = re.findall(r'<a\s+[^>]*href=["\'][^"\']*(?:reeltech|reelglobal|reelproperties|the-new-reel-suv)[^"\']*["\'][^>]*target=["\']_blank["\'][^>]*>', c, re.IGNORECASE)
    if matches:
        print(f, matches)
        found += len(matches)

print('Total division links with target=_blank remaining:', found)
