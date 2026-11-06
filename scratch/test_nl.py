with open('admin/index.html', 'r', encoding='utf-8', newline='') as f:
    text = f.read()

# Let's verify line endings
print('text has CRLF:', '\r\n' in text)
print('text line count:', len(text.splitlines()))

