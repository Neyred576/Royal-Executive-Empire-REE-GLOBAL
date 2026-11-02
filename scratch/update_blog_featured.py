with open('blog.html', 'r', encoding='utf-8') as f:
    c = f.read()

old = '<img src="${blog.image}" alt="${blog.title}" class="blog-featured-img" style="${getBlogFitStyle(blog.imageFit, blog.imagePos)}" decoding="async" loading="lazy">'
new = '<img src="${blog.image}" alt="${blog.title}" class="blog-featured-img" style="${getBlogFitStyle(blog.imageFit, blog.imagePos)}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\'; this.style.padding=\'40px\';">'

if old in c:
    c = c.replace(old, new)
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Updated blog-featured-img in blog.html')
else:
    print('Not found')

