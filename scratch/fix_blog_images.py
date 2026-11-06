import re

# Update blog.html
blog_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\blog.html"
with open(blog_path, "r", encoding="utf-8") as f:
    blog_content = f.read()

new_get_fit = """  // Convert stored imageFit value to inline CSS for blog thumbnails
  function getBlogFitStyle(imageFit, imagePos) {
    const pos = imagePos || 'center center';
    const fit = imageFit || 'cover';
    if (fit === 'contain') {
      return `object-fit:contain !important; object-position:${pos}; width:100%; height:100%; background:rgba(0,0,0,0.85);`;
    }
    if (fit === '16-9' || fit === '16:9') {
      return `object-fit:contain !important; aspect-ratio:16/9; width:100%; height:100%; background:rgba(0,0,0,0.85); object-position:${pos};`;
    }
    if (fit === '16-9-crop') {
      return `object-fit:cover !important; aspect-ratio:16/9; width:100%; height:100%; object-position:${pos};`;
    }
    if (fit === '4-3' || fit === '4:3') {
      return `object-fit:contain !important; aspect-ratio:4/3; width:100%; height:100%; background:rgba(0,0,0,0.85); object-position:${pos};`;
    }
    if (fit === '4-3-crop') {
      return `object-fit:cover !important; aspect-ratio:4/3; width:100%; height:100%; object-position:${pos};`;
    }
    if (fit === '1-1' || fit === '1:1') {
      return `object-fit:contain !important; aspect-ratio:1/1; width:100%; height:100%; background:rgba(0,0,0,0.85); object-position:${pos};`;
    }
    if (fit === '1-1-crop') {
      return `object-fit:cover !important; aspect-ratio:1/1; width:100%; height:100%; object-position:${pos};`;
    }
    return `object-fit:cover !important; object-position:${pos}; width:100%; height:100%;`;
  }"""

pattern = re.compile(r"  // Convert stored imageFit value to inline CSS for blog thumbnails.*?return style;\s*}", re.DOTALL)
if pattern.search(blog_content):
    blog_content = pattern.sub(new_get_fit, blog_content)
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(blog_content)
    print("Updated blog.html getBlogFitStyle successfully!")
else:
    print("Could not find getBlogFitStyle in blog.html")

# Update article.html
article_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\article.html"
with open(article_path, "r", encoding="utf-8") as f:
    art_content = f.read()

# Add getArticleHeroImgStyle helper before main.innerHTML in article.html
helper_code = """
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
"""

if "function getArticleImgStyle" not in art_content:
    art_content = art_content.replace("main.innerHTML = `", helper_code + "\n      main.innerHTML = `")

# Update the hero image in article.html to have a soft ambient blur on the background
old_hero_bg = '<div class="article-hero-bg">\n            ${b.image ? `<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||\'center center\'}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\';">` : \'\'}\n          </div>'
old_hero_bg_crlf = '<div class="article-hero-bg">\r\n            ${b.image ? `<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||\'center center\'}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\';">` : \'\'}\r\n          </div>'

new_hero_bg = '<div class="article-hero-bg">\n            ${b.image ? `<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||\'center center\'}; filter: blur(24px); opacity: 0.38; transform: scale(1.08);" decoding="async" loading="lazy" referrerpolicy="no-referrer">` : \'\'}\n          </div>'

if old_hero_bg in art_content:
    art_content = art_content.replace(old_hero_bg, new_hero_bg)
    print("Replaced hero bg (LF)")
elif old_hero_bg_crlf in art_content:
    art_content = art_content.replace(old_hero_bg_crlf, new_hero_bg)
    print("Replaced hero bg (CRLF)")
else:
    print("Hero bg match not found directly, using regex")
    art_content = re.sub(r'<div class="article-hero-bg">.*?</div>', new_hero_bg, art_content, count=1, flags=re.DOTALL)

# Add clear featured image container right before <article class="article-content">
old_article_tag = '<article class="article-content">'
new_article_tag = """${b.image ? `
                <div class="article-featured-image-box" style="margin-bottom:34px; border-radius:18px; overflow:hidden; border:1px solid rgba(212,175,55,0.25); background:#080808; box-shadow:0 12px 40px rgba(0,0,0,0.7); display:flex; align-items:center; justify-content:center;">
                  <img src="${b.image}" alt="${b.title}" style="${getArticleImgStyle(b.imageFit, b.imagePos)}" decoding="async" loading="eager" />
                </div>
                ` : ''}
                <article class="article-content">"""

if old_article_tag in art_content and "article-featured-image-box" not in art_content:
    art_content = art_content.replace(old_article_tag, new_article_tag, 1)
    print("Added featured image box to article.html!")

with open(article_path, "w", encoding="utf-8") as f:
    f.write(art_content)
print("Updated article.html successfully!")

