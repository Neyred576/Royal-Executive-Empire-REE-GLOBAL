with open('article.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 580 to 690:")
for i in range(580, 690):
    print(f"{i+1}: {lines[i]}", end='')

