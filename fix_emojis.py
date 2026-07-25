import os
import glob

dir_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web"
html_files = glob.glob(os.path.join(dir_path, "*.html"))
js_files = glob.glob(os.path.join(dir_path, "js", "*.js"))
admin_files = glob.glob(os.path.join(dir_path, "admin", "*.html"))

all_files = html_files + js_files + admin_files

replacements = {
    'ðŸ› ï¸ ': '🛍️',
    'ðŸ–¥ï¸ ': '🖥️',
    'ðŸŒ ': '🌍',
    'ðŸ¤ ': '🤝',
    'ðŸ—„ï¸ ': '🗄️',
    'ðŸ ¢': '🏢',
    'ðŸŽ ': '🎁',
    'ðŸ–¨ï¸ ': '🖨️',
    'ðŸ ›ï¸ ': '🖼️',
    'ðŸŽ™ï¸ ': '🎙️',
    'ðŸŽ›ï¸ ': '🎛️',
    'ðŸ   ': '🏠',
    'ðŸ“  ': '📦',
    'ðŸ“‹': '📋',
    'ðŸ‘ ï¸ ': '👁️',
    'ðŸ‡³ðŸ‡¬': '🇳🇬',
    'ðŸ‡¦ðŸ‡ª': '🇦🇪',
    'ðŸ‡¬ðŸ‡§': '🇬🇧',
    'ðŸ‡ºðŸ‡¸': '🇺🇸',
    'ðŸ‡¿ðŸ‡¦': '🇿🇦',
    'ðŸ‡¬ðŸ‡­': '🇬🇭',
    'ðŸ‡°ðŸ‡ª': '🇰🇪',
    'ðŸ‡¸ðŸ‡¬': '🇸🇬',
    'ðŸ‡¨ðŸ‡³': '🇨🇳'
}

for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed remaining emojis in {os.path.basename(filepath)}")

print("Done!")
