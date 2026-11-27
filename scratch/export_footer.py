with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<footer class="site-footer"')
end = text.find('</footer>') + len('</footer>')
footer_html = text[start:end]

with open('scratch_footer.html', 'w', encoding='utf-8') as f:
    f.write(footer_html)

print("Saved scratch_footer.html, length:", len(footer_html))
