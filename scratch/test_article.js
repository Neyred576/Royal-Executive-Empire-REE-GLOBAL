
  document.getElementById('footer-year').textContent = new Date().getFullYear();

  // Reading progress bar
  window.addEventListener('scroll', () => {
    const doc = document.documentElement;
    const scrolled = doc.scrollTop;
    const total = doc.scrollHeight - doc.clientHeight;
    document.getElementById('reading-progress').style.width = (scrolled / total * 100) + '%';
  });

  function formatContent(raw) {
    if (!raw) return '<p>No content available.</p>';
    // If it already contains HTML from the new Rich Text Editor, return as-is
    if (/<[a-z][\s\S]*>/i.test(raw)) {
      return raw;
    }
    // Fallback for old plain-text blog posts
    return raw.split(/\n\n+/).map(block => {
      block = block.trim();
      if (!block) return '';
      // If looks like a heading
      if (block.startsWith('# ')) return `<h2>${block.slice(2)}</h2>`;
      if (block.startsWith('## ')) return `<h3>${block.slice(3)}</h3>`;
      // Otherwise paragraph (handle single newlines inside)
      return `<p>${block.replace(/\n/g, '<br>')}</p>`;
    }).filter(Boolean).join('');
  }

  function renderRelated(blogs, currentId) {
    const others = blogs.filter(b => b.id !== currentId).slice(0, 4);
    if (!others.length) return '<p style="color:var(--w40);font-size:0.85rem">No other articles yet.</p>';
    return others.map(b => `
      <a href="article.html?id=${b.id}" class="rel-post">
        <div class="rel-thumb">${b.image ? `<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||'center'}" decoding="async" loading="lazy" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='/Images/BG/reel_logo.png'; this.style.objectFit='contain';">` : '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,0.02);color:rgba(212,175,55,0.4);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="24" height="24"><path d="M4 22h14a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v4"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M2 15h10"></path><path d="M2 19h10"></path></svg></div>'}</div>
        <div><div class="rel-title">${b.title}</div><div class="rel-date">${b.date || ''}</div></div>
      </a>
    `).join('');
  }


  function getArticleImgStyle(imageFit, imagePos) {
    const pos = imagePos || 'center center';
    const fit = imageFit || 'contain';
    if (fit === '16-9' || fit === '16:9') {
      return `width:100%; aspect-ratio:16/9; object-fit:contain; object-position:${pos}; background:#050505; display:block;`;
    }
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

  function loadArticle() {
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
      setOG('og:url', window.location.href);

      main.innerHTML = `
        <!-- Hero -->
        <div class="article-hero">
          <div class="article-hero-bg">
            ${b.image ? `<img src="${b.image}" alt="${b.title}" style="object-position:${b.imagePos||'center center'}; filter: blur(24px); opacity: 0.38; transform: scale(1.08);" decoding="async" loading="lazy" referrerpolicy="no-referrer">` : ''}
          </div>
          <div class="article-hero-overlay"></div>
          <div class="article-hero-body">
            <div class="container">
              <div class="article-tag">${b.category || 'Insight'}</div>
              <h1 class="article-hero-title">${b.title}</h1>
              <div class="article-hero-meta">
                <div class="article-meta-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                  ${b.date || 'REEL'}
                </div>
                <div class="article-meta-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  Royalty Executive Empire Limited
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Body -->
        <section class="article-section">
          <div class="container">
            <div class="article-layout">
              <!-- Content -->
              <div>
                <a href="blog.html" class="back-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 5l-7 7 7 7"/></svg>
                  Back to Blog
                </a>
                ${b.image ? `
                <div class="article-featured-image-box" style="margin-bottom:34px; border-radius:18px; overflow:hidden; border:1px solid rgba(212,175,55,0.25); background:#080808; box-shadow:0 12px 40px rgba(0,0,0,0.7); display:flex; align-items:center; justify-content:center;">
                  <img src="${b.image}" alt="${b.title}" style="${getArticleImgStyle(b.imageFit, b.imagePos)}" decoding="async" loading="eager" />
                </div>
                ` : ''}
                <article class="article-content">
                  ${formatContent(b.content)}
                </article>
                <!-- Share -->
                <div class="article-share">
                  <span class="share-label">Share:</span>
                  <a href="https://twitter.com/intent/tweet?text=${pageTitle}&url=${pageUrl}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on X">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.74l7.73-8.835L1.254 2.25H8.08l4.253 5.622zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                  </a>
                  <a href="https://www.facebook.com/sharer/sharer.php?u=${pageUrl}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on Facebook">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
                  </a>
                  <a href="https://wa.me/?text=${pageTitle}%20${pageUrl}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on WhatsApp">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
                  </a>
                </div>
              </div>

              <!-- Sidebar -->
              <aside class="article-sidebar">
                <div class="sidebar-card">
                  <div class="sidebar-card-title">More Articles</div>
                  ${renderRelated(allBlogs, articleId)}
                </div>
                <div class="sidebar-card" style="text-align:center">
                  <div class="sidebar-card-title">Follow REEL</div>
                  <p style="color:var(--w50);font-size:0.85rem;margin-bottom:18px;line-height:1.7">Stay updated with our latest insights, projects and announcements.</p>
                  <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:8px;padding:12px 24px;background:var(--gold-gradient);color:var(--black-900);border-radius:8px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:all 0.3s">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="2" y="2" width="20" height="20" rx="5" ry="5" /><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" /></svg>
                    Follow on Instagram
                  </a>
                </div>
              </aside>
            </div>
          </div>
        </section>
      `;

      // Trigger scroll animations for newly added elements
      setTimeout(() => {
        document.querySelectorAll('.article-content, .article-hero-title, .article-hero-body').forEach(el => el.classList.add('in-view'));
      }, 100);

    }).catch(err => {
      console.error('Article load error:', err);
      document.getElementById('article-main').innerHTML = `<div style="text-align:center;padding:200px 20px"><h1 style="color:#fff;font-family:var(--font-display)">Error Loading Article</h1><p style="color:var(--w50);margin-top:12px">Please check your connection and try again.</p><a href="blog.html" style="color:var(--gold-300);margin-top:20px;display:inline-block">&larr; Return to Blog</a></div>`;
    });
  }

  loadArticle();
</script>

  <script src="/js/pwa.js"></script>
<script src="/js/notifications.js">