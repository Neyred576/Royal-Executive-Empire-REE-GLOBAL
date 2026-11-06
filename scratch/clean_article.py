import re

path = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\article.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if 'function getArticleImgStyle(' in line:
        skip = True
        continue
    if skip:
        if 'return `width:100%; max-height:650px' in line or 'return \'width:100%; max-height:650px' in line:
            continue
        if line.strip() == '}':
            skip = False
            continue
        continue
    out.append(line)

content = ''.join(out)

fn = '''
  function getArticleImgStyle(imageFit, imagePos) {
    const pos = imagePos || 'center center';
    const fit = imageFit || 'contain';
    if (fit === '16-9' || fit === '16:9') {
      return `width:100%; aspect-ratio:16/9; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
    }
    if (fit === '16-9-crop') {
      return `width:100%; aspect-ratio:16/9; object-fit:cover; object-position:${pos}; display:block;`;
    }
    if (fit === '4-3' || fit === '4:3') {
      return `width:100%; aspect-ratio:4/3; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
    }
    if (fit === '1-1' || fit === '1:1') {
      return `max-width:550px; width:100%; aspect-ratio:1/1; object-fit:contain; object-position:${pos}; margin:0 auto; display:block;`;
    }
    if (fit === 'cover') {
      return `width:100%; max-height:550px; object-fit:cover; object-position:${pos}; display:block;`;
    }
    return `width:100%; max-height:650px; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
  }
'''

content = content.replace('  function loadArticle() {', fn + '\n  function loadArticle() {', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Success. Count:', content.count('function getArticleImgStyle'))
