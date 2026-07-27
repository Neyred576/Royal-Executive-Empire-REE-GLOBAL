
    // ── Security check ──
    if (sessionStorage.getItem('ree_admin_auth') !== 'true') {
      window.location.href = 'login.html';
    }

    // ── Toast ──
    function showToast(title, msg, icon = 'check') {
      const svgs = {
        check: '<circle cx="12" cy="12" r="10"/><polyline points="9 12 12 15 16 9"/>',
        delete: '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>'
      };
      const t = document.createElement('div');
      t.className = 'toast';
      t.innerHTML = `
        <div class="toast-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">${svgs[icon]}</svg></div>
        <div class="toast-text"><strong>${title}</strong><span>${msg}</span></div>
      `;
      document.body.appendChild(t);
      setTimeout(() => { t.classList.add('out'); setTimeout(() => t.remove(), 400); }, 3000);
    }

    // ── Timezone-aware live clock ──
    const tzFlags = {
      'Africa/Lagos': '🇳🇬',
      'Asia/Dubai': '🇦🇪',
      'Europe/London': '🇬🇧',
      'America/New_York': '🇺🇸',
      'America/Chicago': '🇺🇸',
      'America/Los_Angeles': '🇺🇸',
      'Africa/Johannesburg': '🇿🇦',
      'Africa/Accra': '🇬🇭',
      'Africa/Nairobi': '🇰🇪',
      'Asia/Singapore': '🇸🇬',
      'Asia/Shanghai': '🇨🇳',
    };

    const tzSelect = document.getElementById('tz-select');
    // Restore last selected timezone
    const savedTz = localStorage.getItem('ree_admin_tz') || 'Africa/Lagos';
    tzSelect.value = savedTz;

    const updateTime = () => {
      const tz = tzSelect.value;
      const now = new Date();
      const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', timeZone: tz });
      const dateStr = now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', timeZone: tz });
      const timeEl = document.getElementById('topbar-time');
      const dateEl = document.getElementById('topbar-date-str');
      const flagEl = document.getElementById('tz-flag');
      if (timeEl) timeEl.textContent = timeStr;
      if (dateEl) dateEl.textContent = dateStr;
      if (flagEl) flagEl.textContent = tzFlags[tz] || '🌍';
    };

    // Save and update when timezone changes
    tzSelect.addEventListener('change', () => {
      localStorage.setItem('ree_admin_tz', tzSelect.value);
      updateTime();
      showToast('Timezone Updated', `Switched to ${tzSelect.options[tzSelect.selectedIndex].text}`);
    });

    updateTime();
    setInterval(updateTime, 1000);

    // ── Data ──
    let blogs = [];
    let portfolio = [];
    let products = [];

    // ── Load Data from Firebase ──
    // Wait until window.db is ready (Firebase may take a moment to init)
    function waitForDbThenLoad(retries) {
      if (window.db) {
        loadData();
      } else if (retries > 0) {
        setTimeout(function() { waitForDbThenLoad(retries - 1); }, 300);
      } else {
        showToast('Connection Error', 'Could not connect to database. Please refresh.', 'delete');
      }
    }

    const loadData = async () => {
      if (!window.db) { waitForDbThenLoad(10); return; }
      
      try {
        const [blogSnap, pfSnap, shopSnap, msgSnap, orderSnap] = await Promise.all([
          window.db.collection('blogs').orderBy('timestamp', 'desc').get(),
          window.db.collection('portfolio').get(),
          window.db.collection('products').get(),
          window.db.collection('messages').orderBy('timestamp', 'desc').get(),
          window.db.collection('orders').orderBy('timestamp', 'desc').get()
        ]);
        
        blogs.length = 0; blogs.push(...blogSnap.docs.map(d => ({ id: d.id, ...d.data() })));
        portfolio.length = 0; portfolio.push(...pfSnap.docs.map(d => ({ id: d.id, ...d.data() })));
        products.length = 0; products.push(...shopSnap.docs.map(d => ({ id: d.id, ...d.data() })));
        const messages = msgSnap.docs.map(d => ({ id: d.id, ...d.data() }));
        const orders = orderSnap.docs.map(d => ({ id: d.id, ...d.data() }));
        
        renderList(blogs, 'blog-list', 'blog', 'blogs');
        renderList(portfolio, 'portfolio-list', 'portfolio', 'portfolio');
        renderList(products,  'product-list',   'product', 'products');
        
        // Render Messages
        const msgList = document.getElementById('messages-list');
        if (msgList) {
          if (messages.length === 0) {
            msgList.innerHTML = `<div class="empty-state"><p>No messages yet.</p></div>`;
          } else {
            msgList.innerHTML = messages.map(m => `
              <div class="admin-list-item" style="flex-direction:column; align-items:flex-start;">
                <div style="display:flex; justify-content:space-between; width:100%; margin-bottom:8px;">
                  <strong style="color:var(--gold-300);">${m.name}</strong>
                  <span style="font-size:0.75rem; color:var(--w50);">${m.date || ''}</span>
                </div>
                <div style="font-size:0.85rem; color:var(--w70); margin-bottom:4px;"><strong>Email:</strong> ${m.email} | <strong>Phone:</strong> ${m.phone || 'N/A'}</div>
                <div style="font-size:0.85rem; color:var(--w70); margin-bottom:8px;"><strong>Subject:</strong> ${m.subject || 'General'}</div>
                <div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:6px; font-size:0.85rem; width:100%; color:var(--w90); border-left:2px solid var(--gold);">${m.message}</div>
              </div>
            `).join('');
          }
          const mb = document.getElementById('msgs-badge');
          if (mb) mb.textContent = messages.length;
        }

        // Render Orders
        const orderList = document.getElementById('orders-list');
        if (orderList) {
          if (orders.length === 0) {
            orderList.innerHTML = `<div class="empty-state"><p>No orders yet.</p></div>`;
          } else {
            orderList.innerHTML = orders.map(o => `
              <div class="admin-list-item" style="flex-direction:column; align-items:flex-start;">
                <div style="display:flex; justify-content:space-between; width:100%; margin-bottom:8px;">
                  <strong style="color:var(--gold-300);">Order ID: ${o.id.substring(0,8).toUpperCase()}</strong>
                  <span style="font-size:0.75rem; color:var(--w50);">${o.date || ''}</span>
                </div>
                <div style="font-size:0.85rem; color:var(--w70); margin-bottom:12px;"><strong>Total:</strong> AED ${(o.total||0).toFixed(2)}</div>
                <div style="width:100%;">
                  ${(o.items||[]).map(i => `
                    <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:4px; padding-bottom:4px; border-bottom:1px solid rgba(255,255,255,0.05);">
                      <span>${i.qty}x ${i.name}</span>
                      <span>AED ${(i.price * i.qty).toFixed(2)}</span>
                    </div>
                  `).join('')}
                </div>
              </div>
            `).join('');
          }
          const ob = document.getElementById('orders-badge');
          if (ob) ob.textContent = orders.length;
        }

        updateStats();
      } catch(e) {
        console.error("Error loading data:", e);
        showToast('Error', 'Failed to load from database.', 'delete');
      }
    };

    // ── Update stats ──
    const updateStats = () => {
      ['blog','pf','shop'].forEach(k => {
        const arr = k === 'blog' ? blogs : k === 'pf' ? portfolio : products;
        ['stat-','sb-count-'].forEach(p => {
          const el = document.getElementById(p + k);
          if (el) el.textContent = arr.length;
        });
      });
    };

    // ── Render list ──
    const renderList = (arr, containerId, type, collectionName) => {
      const c = document.getElementById(containerId);
      if (!c) return;
      if (arr.length === 0) {
        c.innerHTML = `<div class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
          <p>No ${type} items yet. Add your first one!</p>
        </div>`;
        return;
      }
      c.innerHTML = '';
      arr.forEach((item, idx) => {
        const div = document.createElement('div');
        div.className = 'admin-list-item';
        const imgSrc = item.image || '';
        const title = item.title || item.name;
        const sub = item.date || item.category || `$${item.price}`;
        div.innerHTML = `
          <div class="item-thumb">${imgSrc ? `<img src="${imgSrc}" alt="">` : '📋'}</div>
          <div class="item-info">
            <strong>${title}</strong>
            <span>${sub}</span>
          </div>
          <button class="btn-delete" data-id="${item.id}" data-idx="${idx}" data-type="${type}" data-col="${collectionName}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>
            Delete
          </button>
        `;
        c.appendChild(div);
      });
      c.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', async () => {
          const id = btn.dataset.id;
          const t = btn.dataset.type;
          const col = btn.dataset.col;
          const i = +btn.dataset.idx;
          
          if (!confirm('Delete this item permanently?')) return;
          
          btn.innerHTML = '...';
          try {
            await window.db.collection(col).doc(id).delete();
            
            if (t === 'blog')       { blogs.splice(i,1); renderList(blogs, 'blog-list', 'blog', col); }
            if (t === 'portfolio')  { portfolio.splice(i,1); renderList(portfolio, 'portfolio-list', 'portfolio', col); }
            if (t === 'product')    { products.splice(i,1); renderList(products, 'product-list', 'product', col); }
            
            updateStats();
            showToast('Deleted', 'Item removed successfully.', 'delete');
          } catch(err) {
            console.error("Delete error", err);
            showToast('Error', 'Failed to delete item.', 'delete');
            renderList(arr, containerId, type, col); // re-render to fix button
          }
        });
      });
    };

    // ── Tab switching ──
    document.querySelectorAll('.admin-nav-link').forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        document.querySelectorAll('.admin-nav-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
        link.classList.add('active');
        const sec = document.getElementById(link.dataset.target);
        if (sec) { sec.classList.add('active'); }
      });
    });

    // ── Forms (Uploads file to ImgBB via API, then saves URL to Firestore) ──
    const IMGBB_API_KEY = '40fad5b164f7be1f49b470b9563cc0c7';

    const handleForm = (formId, fileInputId, builder, collectionName, arr, listId, type) => {
      document.getElementById(formId).addEventListener('submit', async e => {
        e.preventDefault();
        
        const fileInput = document.getElementById(fileInputId);
        const file = fileInput.files[0];
        
        if (!file) { showToast('No Image', 'Please select an image file.', 'delete'); return; }
        
        const btn = e.target.querySelector('button[type="submit"]');
        const oldText = btn.innerHTML;
        btn.innerHTML = 'Uploading Image...';
        btn.disabled = true;

        try {
          // 1. Convert File to Base64
          const getBase64 = (f) => new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(f);
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = error => reject(error);
          });
          const base64Image = await getBase64(file);

          // 2. Upload to ImgBB
          const formData = new FormData();
          formData.append('image', base64Image);

          const imgbbResponse = await fetch(`https://api.imgbb.com/1/upload?key=${IMGBB_API_KEY}`, {
            method: 'POST',
            body: formData
          });

          const imgbbData = await imgbbResponse.json();
          if (!imgbbData.success) {
            console.error('ImgBB API Response:', imgbbData);
            throw new Error('ImgBB Error: ' + (imgbbData.error && imgbbData.error.message ? imgbbData.error.message : 'Upload Failed'));
          }

          const imageUrl = imgbbData.data.url; // The live image URL

          btn.innerHTML = 'Saving...';

          // 3. Save directly to Firestore with the new URL
          const docData = builder(imageUrl);
          const docRef = await window.db.collection(collectionName).add(docData);
          
          // Add locally and render
          arr.unshift({ id: docRef.id, ...docData });
          renderList(arr, listId, type, collectionName);
          updateStats();
          e.target.reset();
          showToast('Success!', `${type.charAt(0).toUpperCase() + type.slice(1)} published successfully.`);
        } catch(err) {
          console.error(err);
          showToast('Error', err.message || 'Failed to publish. Check your connection.', 'delete');
        } finally {
          btn.innerHTML = oldText;
          btn.disabled = false;
          pendingScheduleTime = null;
        }
      });
    };

    // ── Blog Word Limit Logic ──
    const blogContent = document.getElementById('blog-content');
    const wordCountDisplay = document.getElementById('word-count-display');
    const wordLimitToggle = document.getElementById('word-limit-toggle');
    const toggleTrack = document.getElementById('toggle-track');
    const toggleThumb = document.getElementById('toggle-thumb');
    const WORD_LIMIT = 1000;

    const countWords = (text) => text.trim().split(/\s+/).filter(w => w.length > 0).length;

    const updateWordCount = () => {
      let words = countWords(blogContent.value);
      
      // Update UI toggle
      if (wordLimitToggle.checked) {
        toggleTrack.style.background = 'rgba(212,175,55,0.7)';
        toggleThumb.style.transform = 'translateX(18px)';
        wordCountDisplay.textContent = `${words} / ${WORD_LIMIT} words`;
        
        // Enforce limit
        if (words > WORD_LIMIT) {
          blogContent.style.borderColor = '#e74c3c';
          wordCountDisplay.style.color = '#e74c3c';
        } else {
          blogContent.style.borderColor = '';
          wordCountDisplay.style.color = 'var(--w40)';
        }
      } else {
        toggleTrack.style.background = 'rgba(255,255,255,0.1)';
        toggleThumb.style.transform = 'translateX(0)';
        wordCountDisplay.textContent = `${words} words (No limit)`;
        blogContent.style.borderColor = '';
        wordCountDisplay.style.color = 'var(--w40)';
      }
    };

    if (blogContent && wordLimitToggle) {
      blogContent.addEventListener('input', updateWordCount);
      wordLimitToggle.addEventListener('change', updateWordCount);
      updateWordCount();
      
      // Prevent form submission if limit is exceeded and enforced
      document.getElementById('form-blog').addEventListener('submit', (e) => {
        if (wordLimitToggle.checked && countWords(blogContent.value) > WORD_LIMIT) {
          e.preventDefault();
          e.stopImmediatePropagation();
          showToast('Limit Exceeded', `Blog content cannot exceed ${WORD_LIMIT} words.`, 'delete');
        }
      });
    }

    // ── Scheduler Modal Logic ──
    let pendingScheduleTime = null;
    let activeScheduleSelect = null;

    window.closeScheduleModal = function() {
      document.getElementById('schedule-modal-overlay').style.display = 'none';
      if (activeScheduleSelect) { activeScheduleSelect.value = 'published'; }
      activeScheduleSelect = null;
    };

    window.confirmScheduleTime = function() {
      const val = document.getElementById('global-schedule-time').value;
      if (!val) { showToast('No Time', 'Please pick a date and time.', 'delete'); return; }
      pendingScheduleTime = val;
      document.getElementById('schedule-modal-overlay').style.display = 'none';
      showToast('Scheduled', 'Post will go live at: ' + new Date(val).toLocaleString());
      // Auto-navigate to Scheduler tab
      document.querySelectorAll('.admin-nav-link').forEach(l => l.classList.remove('active'));
      document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
      const schLink = document.querySelector('[data-target="sec-scheduler"]');
      if (schLink) schLink.classList.add('active');
      const schSec = document.getElementById('sec-scheduler');
      if (schSec) schSec.classList.add('active');
    };

    ['blog-status','portfolio-status','shop-status'].forEach(id => {
      const sel = document.getElementById(id);
      if (!sel) return;
      sel.addEventListener('change', () => {
        if (sel.value === 'scheduled') {
          activeScheduleSelect = sel;
          document.getElementById('global-schedule-time').value = '';
          document.getElementById('schedule-modal-overlay').style.display = 'flex';
        }
      });
    });

    // ── Scheduler List Renderer ──
    function renderSchedulerList(items) {
      const container = document.getElementById('scheduler-list');
      if (!container) return;
      if (!items || items.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No scheduled content yet. Use the Blog, Portfolio, or Shop forms and select "Schedule for Later".</p></div>';
        return;
      }
      items.sort((a,b) => new Date(a.scheduleTime) - new Date(b.scheduleTime));
      container.innerHTML = items.map(item => `
        <div class="admin-list-item" style="flex-direction:column; align-items:flex-start; gap:12px;" id="sched-${item.id}">
          <div style="display:flex; align-items:center; gap:12px; width:100%;">
            ${item.image ? `<div class="item-thumb"><img src="${item.image}" alt="" style="width:50px;height:50px;object-fit:cover;border-radius:8px;"></div>` : ''}
            <div style="flex:1;">
              <span style="font-size:0.65rem; color:#D4AF37; text-transform:uppercase; letter-spacing:1px;">${item._type}</span>
              <strong style="display:block;">${item.title || item.name}</strong>
              <span style="font-size:0.8rem; color:rgba(255,255,255,0.5);">🕐 ${new Date(item.scheduleTime).toLocaleString()}</span>
            </div>
            <button class="btn-delete sched-delete" data-id="${item.id}" data-col="${item._col}" style="flex-shrink:0;">Delete</button>
          </div>
          <div style="width:100%; display:flex; gap:10px; flex-wrap:wrap;">
            <input type="datetime-local" class="sched-time-edit" data-id="${item.id}" data-col="${item._col}" value="${item.scheduleTime || ''}" style="flex:1; min-width:200px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15); border-radius:8px; padding:8px; color:#fff;" />
            <button class="sched-save-btn" data-id="${item.id}" data-col="${item._col}" style="background:#D4AF37; color:#000; border:none; padding:8px 16px; border-radius:8px; cursor:pointer; font-weight:bold;">Save Time</button>
          </div>
        </div>
      `).join('');

      // Delete
      container.querySelectorAll('.sched-delete').forEach(btn => {
        btn.addEventListener('click', async () => {
          if (!confirm('Delete this scheduled item?')) return;
          await window.db.collection(btn.dataset.col).doc(btn.dataset.id).delete();
          showToast('Deleted', 'Scheduled item removed.', 'delete');
        });
      });
      // Save new time
      container.querySelectorAll('.sched-save-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
          const input = container.querySelector(`.sched-time-edit[data-id="${btn.dataset.id}"]`);
          if (!input || !input.value) { showToast('No Time', 'Pick a time first.', 'delete'); return; }
          await window.db.collection(btn.dataset.col).doc(btn.dataset.id).update({ scheduleTime: input.value });
          showToast('Updated', 'Schedule time saved!');
        });
      });
    }

    // ── Real-time Scheduler Listeners ──
    function attachSchedulerListeners() {
      let allScheduled = [];
      const colMap = { blogs: 'Blog', portfolio: 'Portfolio', products: 'Product' };

      Object.entries(colMap).forEach(([col, type]) => {
        window.db.collection(col).where('status', '==', 'scheduled').onSnapshot(snap => {
          // Remove old entries for this collection, add fresh ones
          allScheduled = allScheduled.filter(i => i._col !== col);
          snap.forEach(d => allScheduled.push({ id: d.id, _col: col, _type: type, ...d.data() }));
          renderSchedulerList(allScheduled);
        });
      });
    }
    // Wait for db before attaching scheduler listeners
    function waitForDbThenScheduler(retries) {
      if (window.db) {
        attachSchedulerListeners();
      } else if (retries > 0) {
        setTimeout(function() { waitForDbThenScheduler(retries - 1); }, 300);
      }
    }
    waitForDbThenScheduler(15);

    handleForm('form-blog', 'blog-img',
      img => ({
        title: document.getElementById('blog-title').value,
        category: document.getElementById('blog-cat').value,
        content: document.getElementById('blog-content').value,
        image: img,
        imagePos: document.getElementById('blog-img-pos').value,
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        status: document.getElementById('blog-status').value,
        scheduleTime: document.getElementById('blog-status').value === 'scheduled' ? pendingScheduleTime : null,
        timestamp: firebase.firestore.FieldValue.serverTimestamp()
      }),
      'blogs', blogs, 'blog-list', 'blog'
    );

    handleForm('form-portfolio', 'pf-img',
      img => ({
        title: document.getElementById('pf-title').value,
        category: document.getElementById('pf-cat').value,
        image: img,
        imagePos: document.getElementById('pf-img-pos').value,
        status: document.getElementById('portfolio-status').value,
        scheduleTime: document.getElementById('portfolio-status').value === 'scheduled' ? pendingScheduleTime : null,
        timestamp: firebase.firestore.FieldValue.serverTimestamp()
      }),
      'portfolio', portfolio, 'portfolio-list', 'portfolio'
    );

    handleForm('form-shop', 'shop-img',
      img => ({
        name: document.getElementById('shop-name').value,
        price: document.getElementById('shop-price').value,
        category: document.getElementById('shop-cat').value,
        image: img,
        imagePos: document.getElementById('shop-img-pos').value,
        status: document.getElementById('shop-status').value,
        scheduleTime: document.getElementById('shop-status').value === 'scheduled' ? pendingScheduleTime : null,
        timestamp: firebase.firestore.FieldValue.serverTimestamp()
      }),
      'products', products, 'product-list', 'product'
    );

    // Cleaned up form submit listener

    // ── Broadcast Center Logic ──
    const bcInput = document.getElementById('bc-input');
    const bcPreview = document.getElementById('bc-preview');
    const bcCount = document.getElementById('bc-count');
    const bcSendBtn = document.getElementById('bc-send-btn');
    const bcHistoryList = document.getElementById('bc-history-list');

    if (bcInput) {
      bcInput.addEventListener('input', () => {
        const val = bcInput.value;
        bcCount.textContent = `${val.length}/300`;
        bcPreview.textContent = val.trim() ? val : 'Your message will appear here...';
      });

      bcSendBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        const body = bcInput.value.trim();
        if (!body) { showToast('Empty', 'Please write a message first.', 'delete'); return; }

        bcSendBtn.disabled = true;
        bcSendBtn.textContent = 'Sending...';

        try {
          await window.db.collection('notifications').add({
            title: 'New from REEL',
            message: body,
            timestamp: Date.now()
          });
          showToast('Broadcast Sent!', 'Notification pushed to all active users.', 'check');
          bcInput.value = ''; bcCount.textContent = '0/300'; bcPreview.textContent = 'Your message will appear here...';
        } catch(err) {
          showToast('Error', 'Failed: ' + err.message, 'delete');
        } finally {
          bcSendBtn.disabled = false;
          bcSendBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg> Send Broadcast';
        }
      });

      // Live history listener with delete buttons
      window.db.collection('notifications').orderBy('timestamp','desc').limit(15).onSnapshot(snap => {
        if (!bcHistoryList) return;
        if (snap.empty) {
          bcHistoryList.innerHTML = '<div class="bc-empty"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="32" height="32"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path></svg>No broadcast history found</div>';
          return;
        }
        bcHistoryList.innerHTML = snap.docs.map(doc => {
          const d = doc.data();
          return `<div style="background:rgba(255,255,255,0.05);padding:12px;border-radius:8px;margin-bottom:10px;position:relative;">
            <button onclick="deleteNotification('${doc.id}')" style="position:absolute;top:8px;right:8px;background:rgba(255,74,74,0.15);border:1px solid rgba(255,74,74,0.4);color:#ff4a4a;border-radius:6px;padding:3px 8px;cursor:pointer;font-size:11px;">Delete</button>
            <div style="font-size:0.75rem;color:#D4AF37;margin-bottom:4px;">${new Date(d.timestamp).toLocaleString()}</div>
            <div style="font-size:0.9rem;color:#fff;padding-right:60px;">${d.message}</div>
          </div>`;
        }).join('');
      });

      window.deleteNotification = async function(id) {
        if (!confirm('Delete this notification from history?')) return;
        try {
          await window.db.collection('notifications').doc(id).delete();
          showToast('Deleted', 'Notification removed from history.', 'delete');
        } catch(e) {
          showToast('Error', 'Could not delete: ' + e.message, 'delete');
        }
      };
    }

    waitForDbThenLoad(15);



    // ── Logout ──
    document.getElementById('logout-btn').addEventListener('click', e => {
      e.preventDefault();
      sessionStorage.removeItem('ree_admin_auth');
      window.location.href = 'login.html';
    });

    // ── Mobile Sidebar Toggle ──
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.querySelector('.admin-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (mobileBtn && sidebar && overlay) {
      const toggleMenu = () => {
        sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
      };
      mobileBtn.addEventListener('click', toggleMenu);
      overlay.addEventListener('click', toggleMenu);
      
      // Close menu when clicking a nav link on mobile
      document.querySelectorAll('.admin-nav-link').forEach(link => {
        link.addEventListener('click', () => {
          if (window.innerWidth <= 992) toggleMenu();
        });
      });
    }
  