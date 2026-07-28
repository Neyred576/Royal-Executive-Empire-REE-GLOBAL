import re

files_config = [
    ('blog.html', 'allBlogs'),
    ('shop.html', 'allProducts'),
    ('portfolio.html', 'allProjects'),
]

for fname, varname in files_config:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'scheduleTime' in content and '__autopublish__' not in content:
        # We inject a Firestore-based scheduled items checker that runs every minute
        # When any item's scheduleTime has passed, it updates status to 'published' in Firestore
        # The frontend filter will then show it
        inject = f"""
  // __autopublish__ - Check every 60s if any scheduled items are now due
  setInterval(function() {{
    if (!window.db) return;
    var now = Date.now();
    window.db.collection('{('blogs' if varname=='allBlogs' else 'portfolio' if varname=='allProjects' else 'products')}')
      .where('status', '==', 'scheduled')
      .get()
      .then(function(snap) {{
        snap.forEach(function(doc) {{
          var data = doc.data();
          if (data.scheduleTime && new Date(data.scheduleTime).getTime() <= now) {{
            // Update status to published so it goes live
            doc.ref.update({{ status: 'published' }}).then(function() {{
              console.log('Auto-published: ' + (data.title || data.name));
              // Refresh the page to show the newly published item
              window.location.reload();
            }});
          }}
        }});
      }});
  }}, 30000); // Check every 30 seconds
"""
        # Inject before </script> that closes the main page script block
        # Find the last </script> before </body>
        content = content.replace('</body>', inject + '\n</body>', 1)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {fname}')
    else:
        print(f'Skipped {fname}')
