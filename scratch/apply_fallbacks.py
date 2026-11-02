import os

def update_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
            print(f"Replaced in {filepath}")
        else:
            print(f"NOT FOUND in {filepath}: {old[:50]}...")
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully saved {filepath}\n")

# 1. shop.html
shop_replacements = [
    (
        '<img src="${p.image}" alt="${p.name || \'Product\'}" class="product-img" style="object-position:${p.imagePos||\'center center\'}" decoding="async" loading="lazy">',
        '<img src="${p.image}" alt="${p.name || \'Product\'}" class="product-img" style="object-position:${p.imagePos||\'center center\'}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\'; this.style.padding=\'30px\';">'
    ),
    (
        'imgCol.innerHTML = `<img src="${product.image}" alt="${product.name || \'Product\'}" style="width:100%;height:100%;object-fit:cover;object-position:${product.imagePos || \'center center\'};" decoding="async" loading="lazy"><div class="shop-modal-badge">New</div>`;',
        'imgCol.innerHTML = `<img src="${product.image}" alt="${product.name || \'Product\'}" style="width:100%;height:100%;object-fit:cover;object-position:${product.imagePos || \'center center\'};" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\'; this.style.padding=\'40px\';"><div class="shop-modal-badge">New</div>`;'
    )
]
update_file('shop.html', shop_replacements)

# 2. blog.html
blog_replacements = [
    (
        '<img src="${blog.image}" alt="${blog.title}" style="${getBlogFitStyle(blog.imageFit, blog.imagePos)}" decoding="async" loading="lazy">',
        '<img src="${blog.image}" alt="${blog.title}" style="${getBlogFitStyle(blog.imageFit, blog.imagePos)}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\'; this.style.padding=\'30px\';">'
    ),
    (
        '<img src="${b.image}" alt="${b.title}" style="${getBlogFitStyle(b.imageFit, b.imagePos)}" decoding="async" loading="lazy">',
        '<img src="${b.image}" alt="${b.title}" style="${getBlogFitStyle(b.imageFit, b.imagePos)}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\'; this.style.padding=\'20px\';">'
    ),
    (
        '<img src="${b.image}" alt="${b.title}" style="object-fit:cover;object-position:${b.imagePos||\'center\'};width:100%;height:100%;" decoding="async" loading="lazy">',
        '<img src="${b.image}" alt="${b.title}" style="object-fit:cover;object-position:${b.imagePos||\'center\'};width:100%;height:100%;" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\';">'
    )
]
update_file('blog.html', blog_replacements)

# 3. article.html
article_replacements = [
    (
        '<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||\'center\'}" decoding="async" loading="lazy">',
        '<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||\'center\'}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\';">'
    ),
    (
        '<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||\'center center\'}" decoding="async" loading="lazy">',
        '<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||\'center center\'}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=\'/Images/BG/reel_logo.png\'; this.style.objectFit=\'contain\';">'
    )
]
update_file('article.html', article_replacements)

