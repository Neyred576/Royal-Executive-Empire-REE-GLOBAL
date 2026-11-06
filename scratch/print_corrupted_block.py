with open('article.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_start = text.find('function getArticleImgStyle')
pos_end = text.find('main.innerHTML = `\n        <!-- Hero -->')
print(text[pos_start:pos_end])

