import re
import os

def update_filters():
    files = {
        'blog.html': ('allBlogs', 'allBlogs = snap.docs.map(d => ({ id: d.id, ...d.data() }));'),
        'shop.html': ('allProducts', 'allProducts = snap.docs.map(d => ({ id: d.id, ...d.data() }));'),
        'portfolio.html': ('allPortfolio', 'allPortfolio = snap.docs.map(d => ({ id: d.id, ...d.data() }));')
    }
    
    directory = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web"
    
    for filename, (var_name, target_line) in files.items():
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        replacement = f"""let _fetched = snap.docs.map(d => ({{ id: d.id, ...d.data() }}));
      const _now = new Date();
      {var_name} = _fetched.filter(item => {{
        if(item.status === 'scheduled' && item.scheduleTime) {{
          return new Date(item.scheduleTime) <= _now;
        }}
        if(item.status === 'draft') return false;
        return true;
      }});"""
      
        if target_line in content:
            content = content.replace(target_line, replacement)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")
        else:
            print(f"Target line not found in {filename}")

if __name__ == "__main__":
    update_filters()
