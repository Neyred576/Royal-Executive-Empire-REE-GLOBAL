import os
import glob
import re

main_dir = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web'
html_files = [f for f in glob.glob(os.path.join(main_dir, '*.html')) if os.path.isfile(f)]

wa_svg = '''<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="color:#25D366;width:18px;height:18px;flex-shrink:0;"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.03-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>'''

phone_call_svg = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.41 2 2 0 0 1 3.6 1.23h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.77a16 16 0 0 0 6 6l.97-.97a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7a2 2 0 0 1 1.72 2z" />
                </svg>'''

count = 0
for fpath in html_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    orig = content

    # 1. Phone number replacement: remove outer brackets, split into 2 lines (Call first, WhatsApp second)
    phone_pattern = re.compile(
        r'<p>\s*(<svg[^>]*>.*?</svg>)\s*<span>.*?806\s*702\s*9444.*?911\s*802\s*4521.*?</span>\s*</p>',
        re.DOTALL
    )
    def repl_phone(m):
        return f'''<p>
                {phone_call_svg}
                <a href="tel:+2348067029444">+234 806 702 9444</a>
              </p>
              <p>
                {wa_svg}
                <a href="https://wa.me/2349118024521" target="_blank" rel="noopener noreferrer">+234 911 802 4521</a>
              </p>'''

    content = phone_pattern.sub(repl_phone, content)

    # Alternate single-span or leadership/ceo pattern
    alt_phone_pattern = re.compile(
        r'<span>\(?<span>\(?<a\s+href="tel:\+2348067029444"[^>]*>\+234\s*806\s*702\s*9444</a>\s*-\s*<a\s+href="tel:\+2349118024521"[^>]*>\+234\s*911\s*802\s*4521</a>\)?</span>\)?</span>',
        re.DOTALL
    )
    def repl_alt_phone(m):
        return f'''<a href="tel:+2348067029444">+234 806 702 9444</a></span>
              </p>
              <p>
                {wa_svg}
                <span><a href="https://wa.me/2349118024521" target="_blank" rel="noopener noreferrer">+234 911 802 4521</a>'''
    content = alt_phone_pattern.sub(repl_alt_phone, content)

    # 2. Instagram widget header:
    # Add ROYALTY EXECUTIVE EMPIRE LIMITED in Capital and Bold above @reelholding
    insta_header_pattern = re.compile(
        r'(<a[^>]*class="insta-user-info"[^>]*>\s*<svg[^>]*class="insta-icon"[^>]*>.*?</svg>)\s*(?:<div[^>]*>)?\s*<span class="insta-handle">@reelholding</span>(?:\s*</div>)?',
        re.DOTALL
    )
    def repl_insta(m):
        svg_part = m.group(1)
        return f'''{svg_part}
                  <div style="display:flex;flex-direction:column;line-height:1.2;">
                    <span style="font-weight:900;text-transform:uppercase;color:#fff;font-size:10px;letter-spacing:0.5px;">ROYALTY EXECUTIVE EMPIRE LIMITED</span>
                    <span class="insta-handle" style="font-size:12px;color:rgba(255,255,255,0.7);">@reelholding</span>
                  </div>'''
    content = insta_header_pattern.sub(repl_insta, content)

    # 3. Target=_blank removal for division links so they open in SAME tab
    div_domains = ['reeltech.reelholding.com.ng', 'reelauto.reelholding.com.ng', 'reelproperties.reelholding.com.ng', 'reelglobal.reelholding.com.ng']
    for dom in div_domains:
        content = re.sub(
            r'(<a\s+[^>]*href=["\']https?://' + re.escape(dom) + r'[^"\']*["\'][^>]*?)\s+target=["\']_blank["\']',
            r'\1 target="_self"',
            content
        )
        content = re.sub(
            r'(<a\s+[^>]*?)target=["\']_blank["\'](\s+[^>]*?href=["\']https?://' + re.escape(dom) + r'[^"\']*["\'])',
            r'\1target="_self"\2',
            content
        )

    # 4. Remove cart button completely from navbar
    content = re.sub(
        r'<a\s+href="cart\.html"\s+class="nav-icon\s+cart-icon"[^>]*>.*?</a>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # 5. Fix bullet points or mojibake in Our Divisions footer list
    content = re.sub(r'>\s*(?:â€¢|•|â€)\s*', '>', content)

    # 6. Navbar updates:
    # For index.html:
    # "Our Divisions" button: no dropdown, scrolls to #divisions
    # Center has ONLY "Our Divisions"
    # "News & Media" placed into .nav-actions (where cart was)
    if fname == 'index.html':
        # Replace dropdown with direct link
        dropdown_regex = re.compile(
            r'<li class="nav-item-dropdown" id="our-divisions-dropdown">.*?</li>\s*<li><a href="blog\.html" class="nav-link">News & Media</a></li>',
            re.DOTALL
        )
        replacement_links = '<li><a href="#divisions" class="nav-link">Our Divisions</a></li>'
        content = dropdown_regex.sub(replacement_links, content)

        # In nav-actions: add News & Media before Contact Us
        if 'class="nav-actions"' in content:
            # check if News & Media is already in nav-actions
            if 'blog.html' not in content[content.find('class="nav-actions"'):content.find('class="nav-actions"')+300]:
                content = content.replace(
                    '<div class="nav-actions">',
                    '<div class="nav-actions">\n        <a href="blog.html" class="nav-link" style="text-decoration:none;margin-right:4px;">News &amp; Media</a>'
                )

    else:
        # For all other pages:
        # If dropdown exists, simplify to link to index.html#divisions
        dropdown_regex = re.compile(
            r'<li class="nav-item-dropdown" id="our-divisions-dropdown">.*?</li>\s*<li><a href="blog\.html" class="nav-link">News & Media</a></li>',
            re.DOTALL
        )
        replacement_links = '<li><a href="index.html#divisions" class="nav-link">Our Divisions</a></li>'
        content = dropdown_regex.sub(replacement_links, content)

        if 'class="nav-actions"' in content:
            if 'blog.html' not in content[content.find('class="nav-actions"'):content.find('class="nav-actions"')+300]:
                content = content.replace(
                    '<div class="nav-actions">',
                    '<div class="nav-actions">\n        <a href="blog.html" class="nav-link" style="text-decoration:none;margin-right:4px;">News &amp; Media</a>'
                )

    if content != orig:
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(content)
        count += 1
        print(f'Updated: {fname}')

print(f'Done! Successfully modified {count} HTML files.')
