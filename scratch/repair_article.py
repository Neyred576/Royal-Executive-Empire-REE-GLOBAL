with open('article.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_snippet = """  function loadArticle() {
    if (!window.db) { setTimeout(loadArticle, 60); return; }

    const urlParams = new URLSearchParams(window.location.search);
    const articleId = urlParams.get('id');
    const main = document.getElementById('article-main');

    if (!articleId) {
      
        if (fit === '16-9-crop') {
          return `width:100%; aspect-ratio:16/9; object-fit:cover; object-position:${pos}; display:block;`;
        }
        if (fit === '4-3' || fit === '4:3') {
          return `width:100%; aspect-ratio:4/3; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
        }
        if (fit === '1-1' || fit === '1:1') {
          return `max-width:550px; width:100%; aspect-ratio:1/1; object-fit:contain; object-position:${pos}; margin:0 auto; display:block;`;
        }
        if (fit === 'cover') {
          return `width:100%; max-height:550px; object-fit:cover; object-position:${pos}; display:block;`;
        }
        return `width:100%; max-height:650px; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
      }

      main.innerHTML = `<div style="text-align:center;padding:200px 20px"><h1 style="color:#fff;font-family:var(--font-display);font-size:3rem">Article Not Found</h1><a href="blog.html" style="color:var(--gold-300);margin-top:20px;display:inline-block">&larr; Return to Blog</a></div>`;
      return;
    }

    // Load the article and all blogs for sidebar
    Promise.all([
      window.db.collection('blogs').doc(articleId).get(),
      window.db.collection('blogs').orderBy('timestamp', 'desc').limit(8).get()
    ]).then(([doc, allSnap]) => {
      if (!doc.exists) {
        
        if (fit === '16-9-crop') {
          return `width:100%; aspect-ratio:16/9; object-fit:cover; object-position:${pos}; display:block;`;
        }
        if (fit === '4-3' || fit === '4:3') {
          return `width:100%; aspect-ratio:4/3; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
        }
        if (fit === '1-1' || fit === '1:1') {
          return `max-width:550px; width:100%; aspect-ratio:1/1; object-fit:contain; object-position:${pos}; margin:0 auto; display:block;`;
        }
        if (fit === 'cover') {
          return `width:100%; max-height:550px; object-fit:cover; object-position:${pos}; display:block;`;
        }
        return `width:100%; max-height:650px; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
      }

      main.innerHTML = `<div style="text-align:center;padding:200px 20px"><h1 style="color:#fff;font-family:var(--font-display);font-size:3rem">Article Not Found</h1><a href="blog.html" style="color:var(--gold-300);margin-top:20px;display:inline-block">&larr; Return to Blog</a></div>`;
        return;
      }

      const b = doc.data();
      const allBlogs = allSnap.docs.map(d => ({ id: d.id, ...d.data() }));
      const pageUrl = encodeURIComponent(window.location.href);
      const pageTitle = encodeURIComponent(b.title || '');

      // Update page title and meta with SEO fields from Firestore
      document.title = (b.seoTitle && b.seoTitle.trim()) ? b.seoTitle : `${b.title} | REEL`;

      // Meta description
      let metaDesc = document.querySelector('meta[name="description"]');
      if (!metaDesc) { metaDesc = document.createElement('meta'); metaDesc.name = 'description'; document.head.appendChild(metaDesc); }
      metaDesc.content = (b.seoDesc && b.seoDesc.trim()) ? b.seoDesc : `Read "${b.title}"  an exclusive insight from Royalty Executive Empire Limited.`;

      // Focus keyword as meta keywords
      if (b.seoKeyword && b.seoKeyword.trim()) {
        let metaKw = document.querySelector('meta[name="keywords"]');
        if (!metaKw) { metaKw = document.createElement('meta'); metaKw.name = 'keywords'; document.head.appendChild(metaKw); }
        metaKw.content = b.seoKeyword;
      }

      // Open Graph tags
      const setOG = (prop, val) => {
        let el = document.querySelector(`meta[property="${prop}"]`);
        if (!el) { el = document.createElement('meta'); el.setAttribute('property', prop); document.head.appendChild(el); }
        el.setAttribute('content', val);
      };
      setOG('og:title',       document.title);
      setOG('og:description', metaDesc.content);
      if (b.image) setOG('og:image', b.image);
      setOG('og:url', window.location.href);

      
        if (fit === '16-9-crop') {
          return `width:100%; aspect-ratio:16/9; object-fit:cover; object-position:${pos}; display:block;`;
        }
        if (fit === '4-3' || fit === '4:3') {
          return `width:100%; aspect-ratio:4/3; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
        }
        if (fit === '1-1' || fit === '1:1') {
          return `max-width:550px; width:100%; aspect-ratio:1/1; object-fit:contain; object-position:${pos}; margin:0 auto; display:block;`;
        }
        if (fit === 'cover') {
          return `width:100%; max-height:550px; object-fit:cover; object-position:${pos}; display:block;`;
        }
        return `width:100%; max-height:650px; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
      }"""

clean_snippet = """  function loadArticle() {
    if (!window.db) { setTimeout(loadArticle, 60); return; }

    const urlParams = new URLSearchParams(window.location.search);
    const articleId = urlParams.get('id');
    const main = document.getElementById('article-main');

    if (!articleId) {
      main.innerHTML = `<div style="text-align:center;padding:200px 20px"><h1 style="color:#fff;font-family:var(--font-display);font-size:3rem">Article Not Found</h1><a href="blog.html" style="color:var(--gold-300);margin-top:20px;display:inline-block">&larr; Return to Blog</a></div>`;
      return;
    }

    // Load the article and all blogs for sidebar
    Promise.all([
      window.db.collection('blogs').doc(articleId).get(),
      window.db.collection('blogs').orderBy('timestamp', 'desc').limit(8).get()
    ]).then(([doc, allSnap]) => {
      if (!doc.exists) {
        main.innerHTML = `<div style="text-align:center;padding:200px 20px"><h1 style="color:#fff;font-family:var(--font-display);font-size:3rem">Article Not Found</h1><a href="blog.html" style="color:var(--gold-300);margin-top:20px;display:inline-block">&larr; Return to Blog</a></div>`;
        return;
      }

      const b = doc.data();
      const allBlogs = allSnap.docs.map(d => ({ id: d.id, ...d.data() }));
      const pageUrl = encodeURIComponent(window.location.href);
      const pageTitle = encodeURIComponent(b.title || '');

      // Update page title and meta with SEO fields from Firestore
      document.title = (b.seoTitle && b.seoTitle.trim()) ? b.seoTitle : `${b.title} | REEL`;

      // Meta description
      let metaDesc = document.querySelector('meta[name="description"]');
      if (!metaDesc) { metaDesc = document.createElement('meta'); metaDesc.name = 'description'; document.head.appendChild(metaDesc); }
      metaDesc.content = (b.seoDesc && b.seoDesc.trim()) ? b.seoDesc : `Read "${b.title}" — an exclusive insight from Royalty Executive Empire Limited.`;

      // Focus keyword as meta keywords
      if (b.seoKeyword && b.seoKeyword.trim()) {
        let metaKw = document.querySelector('meta[name="keywords"]');
        if (!metaKw) { metaKw = document.createElement('meta'); metaKw.name = 'keywords'; document.head.appendChild(metaKw); }
        metaKw.content = b.seoKeyword;
      }

      // Open Graph tags
      const setOG = (prop, val) => {
        let el = document.querySelector(`meta[property="${prop}"]`);
        if (!el) { el = document.createElement('meta'); el.setAttribute('property', prop); document.head.appendChild(el); }
        el.setAttribute('content', val);
      };
      setOG('og:title',       document.title);
      setOG('og:description', metaDesc.content);
      if (b.image) setOG('og:image', b.image);
      setOG('og:url', window.location.href);"""

# Normalize newlines
norm_text = text.replace('\r\n', '\n')
norm_bad = bad_snippet.replace('\r\n', '\n')
norm_clean = clean_snippet.replace('\r\n', '\n')

if norm_bad in norm_text:
    fixed_text = norm_text.replace(norm_bad, norm_clean, 1)
    with open('article.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(fixed_text)
    print("SUCCESS: article.html loadArticle syntax repaired!")
else:
    print("WARNING: Exact match failed. Let's do a substring locate.")
    start = norm_text.find('function loadArticle()')
    end = norm_text.find('main.innerHTML = `\n        <!-- Hero -->')
    print("Found bounds:", start, end)
    if start != -1 and end != -1:
        fixed_text = norm_text[:start] + norm_clean + '\n\n      ' + norm_text[end:]
        with open('article.html', 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(fixed_text)
        print("SUCCESS via bounds replacement!")

