document.addEventListener('DOMContentLoaded', () => {
  const navActions = document.querySelector('.nav-actions');

  // 1. Inject Mobile News & Media Button if not already present
  if (navActions && !document.getElementById('mobile-nav-news-btn')) {
    const isBlog = window.location.pathname.includes('blog.html') || window.location.pathname.includes('article.html');
    const newsBtnHtml = `
      <a href="blog.html" class="nav-icon nav-news-icon-btn ${isBlog ? 'active' : ''}" id="mobile-nav-news-btn" aria-label="News &amp; Media" title="News &amp; Media">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#D4AF37" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 4v16a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7.5L16.5 2H6a2 2 0 0 0-2 2Z"></path>
          <polyline points="16 2 16 8 22 8"></polyline>
          <polygon points="10 12 10 16 14 14" fill="#D4AF37"></polygon>
          <line x1="8" y1="18" x2="16" y2="18"></line>
        </svg>
      </a>
    `;
    navActions.insertAdjacentHTML('beforeend', newsBtnHtml);
  }

  // 2. Inject Notification Bell into Header
  if (navActions && !document.getElementById('notif-btn')) {
    const bellHtml = `
      <div class="nav-icon" id="notif-btn" style="cursor:pointer;" aria-label="Notifications" title="Notifications">
        <svg viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="1.8" style="width:18px;height:18px;">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
        <span id="notif-badge" style="display:none; position:absolute; top:-6px; right:-6px; background:#D4AF37; color:#000; font-size:10px; font-weight:bold; padding:2px 6px; border-radius:10px;">0</span>
      </div>
    `;
    navActions.insertAdjacentHTML('beforeend', bellHtml);
  }

  // 3. Inject Mobile Contact Us (Call) Button if not already present
  if (navActions && !document.getElementById('mobile-nav-contact-btn')) {
    const isContact = window.location.pathname.includes('contact.html');
    const contactBtnHtml = `
      <a href="contact.html" class="nav-icon nav-contact-icon-btn ${isContact ? 'active' : ''}" id="mobile-nav-contact-btn" aria-label="Contact Us" title="Contact Us">
        <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="#D4AF37" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
        </svg>
      </a>
    `;
    navActions.insertAdjacentHTML('beforeend', contactBtnHtml);
  }

  // 4. Dropdown Panel attached directly to document.body (prevents ancestor CSS transforms from crushing it)
  if (!document.getElementById('notif-panel')) {
    const panelHtml = `
      <div id="notif-panel" class="notif-dropdown-panel" style="display:none; white-space:normal; text-align:left; background:rgba(10,10,10,0.96); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); border:1px solid rgba(212,175,55,0.35); border-radius:14px; box-shadow:0 16px 40px rgba(0,0,0,0.85); overflow:hidden;">
        <div style="padding:15px; border-bottom:1px solid rgba(255,255,255,0.1); display:flex; justify-content:space-between; align-items:center;">
          <h4 style="margin:0; font-family:'Cormorant Garamond', serif; font-size:1.15rem; color:#D4AF37;">Notifications</h4>
          <button id="notif-enable-btn" style="background:transparent; border:1px solid #D4AF37; color:#D4AF37; padding:4px 10px; border-radius:4px; font-size:10px; cursor:pointer; font-weight:600;">Enable Alerts</button>
        </div>
        
        <!-- Pinned Install App -->
        <div id="notif-install-app" style="padding:12px 15px; border-bottom:1px solid rgba(255,255,255,0.05); background:rgba(212,175,55,0.05); display:flex; justify-content:space-between; align-items:center; cursor:pointer; transition:background 0.2s;">
          <div>
            <strong style="display:flex; align-items:center; gap:6px; color:#D4AF37; font-size:13px; margin-bottom:2px;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
              Install REEL App
            </strong>
            <div style="color:rgba(255,255,255,0.7); font-size:11px;">Add to home screen for fast access</div>
          </div>
          <div style="background:#D4AF37; color:#000; padding:4px 8px; border-radius:4px; font-size:10px; font-weight:bold;">INSTALL</div>
        </div>

        <div id="notif-list" style="max-height:260px; overflow-y:auto; padding:10px;">
          <div style="text-align:center; padding:20px; color:rgba(255,255,255,0.5); font-size:12px;">Loading...</div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', panelHtml);
  }

  const notifBtn = document.getElementById('notif-btn');
  const notifPanel = document.getElementById('notif-panel');
  const notifList = document.getElementById('notif-list');
  const notifBadge = document.getElementById('notif-badge');
  const enableBtn = document.getElementById('notif-enable-btn');
  const installAppBtn = document.getElementById('notif-install-app');
  
  if (installAppBtn) {
    installAppBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (notifPanel) notifPanel.style.display = 'none'; // Close panel
      if (typeof showInstallPromotion === 'function') {
        showInstallPromotion();
      }
    });
  }
  
  let lastSeenTimestamp = localStorage.getItem('ree_notif_last_seen') || 0;
  let unreadCount = 0;

  if (notifBtn && notifPanel) {
    notifBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isVisible = notifPanel.style.display === 'block';
      if (isVisible) {
        notifPanel.style.display = 'none';
      } else {
        notifPanel.style.display = 'block';
        if (window.innerWidth > 992) {
          const rect = notifBtn.getBoundingClientRect();
          notifPanel.style.top = `${rect.bottom + 12}px`;
          notifPanel.style.right = `${Math.max(16, window.innerWidth - rect.right)}px`;
          notifPanel.style.left = 'auto';
        } else {
          notifPanel.style.top = '72px';
          notifPanel.style.left = '14px';
          notifPanel.style.right = '14px';
        }
        unreadCount = 0;
        if (notifBadge) {
          notifBadge.style.display = 'none';
          notifBadge.textContent = '0';
        }
        localStorage.setItem('ree_notif_last_seen', Date.now().toString());
      }
    });

    // Close panel when clicking outside
    document.addEventListener('click', (e) => {
      if (notifPanel.style.display === 'block' && !notifPanel.contains(e.target) && !notifBtn.contains(e.target)) {
        notifPanel.style.display = 'none';
      }
    });
  }

  
  // Handle Permissions & FCM Token
  if (enableBtn) {
    if (Notification.permission === 'granted') {
      enableBtn.style.display = 'none';
      // If already granted, ensure token is refreshed/saved silently
      if(typeof firebase !== 'undefined' && firebase.messaging) {
        setTimeout(() => {
          try {
            const messaging = firebase.messaging();
            messaging.getToken({ vapidKey: 'BEp5FxDvfKevIU0clBfu5PRO2KfraAcW1q133smI_WDUh0NqzMTMP47Iwl3nKyxO-vJXGnequLXbylrB1qSWvJg' }).then((currentToken) => {
              if (currentToken && window.db) {
                window.db.collection('subscribers').doc(currentToken).set({ token: currentToken, lastActive: Date.now() }, {merge: true});
              }
            }).catch(e => console.log('FCM token error:', e));
          } catch(e) {}
        }, 2000);
      }
    } else if (Notification.permission === 'denied') {
      enableBtn.textContent = 'Blocked';
      enableBtn.style.opacity = '0.5';
      enableBtn.disabled = true;
    }
    
    enableBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      Notification.requestPermission().then(perm => {
        if (perm === 'granted') {
          enableBtn.style.display = 'none';
          
          if(typeof firebase !== 'undefined' && firebase.messaging) {
            const messaging = firebase.messaging();
            messaging.getToken({ vapidKey: 'BEp5FxDvfKevIU0clBfu5PRO2KfraAcW1q133smI_WDUh0NqzMTMP47Iwl3nKyxO-vJXGnequLXbylrB1qSWvJg' }).then((currentToken) => {
              if (currentToken) {
                if (window.db) {
                  window.db.collection('subscribers').doc(currentToken).set({ token: currentToken, timestamp: Date.now() }, {merge: true});
                }
                new Notification("REEL", { body: "Push notifications enabled!", icon: "/Images/icons/icon-192x192.png" });
              }
            }).catch((err) => {
              console.log('An error occurred while retrieving token. ', err);
            });
          } else {
             new Notification("REEL", { body: "Push notifications enabled!", icon: "/Images/icons/icon-192x192.png" });
          }
          
        } else {
          enableBtn.textContent = 'Blocked';
          enableBtn.disabled = true;
        }
      });
    });
  }
  // Fetch from Firestore
  function initNotifications() {
    if (!window.db) {
      setTimeout(initNotifications, 100);
      return;
    }

    // 1. Initial Load of History
    window.db.collection('notifications').orderBy('timestamp', 'desc').limit(20).get()
      .then(snap => {
        if (snap.empty) {
          notifList.innerHTML = `<div style="text-align:center; padding:20px; color:rgba(255,255,255,0.5); font-size:12px;">No notifications yet.</div>`;
          return;
        }
        
        let html = '';
        snap.forEach(doc => {
          const data = doc.data();
          const date = new Date(data.timestamp).toLocaleString();
          html += `
            <div style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.05);">
              <strong style="display:block; color:#fff; font-size:13px; margin-bottom:4px;">${data.title}</strong>
              <div style="color:rgba(255,255,255,0.7); font-size:12px; margin-bottom:4px;">${data.message}</div>
              <div style="color:#D4AF37; font-size:10px;">${date}</div>
            </div>
          `;
        });
        notifList.innerHTML = html;
        
        // Setup listener for NEW notifications ONLY
        const now = Date.now();
        window.db.collection('notifications')
          .where('timestamp', '>', now)
          .onSnapshot(snapshot => {
            snapshot.docChanges().forEach(change => {
              if (change.type === 'added') {
                const data = change.doc.data();
                
                // Show native push notification
                if (Notification.permission === 'granted') {
                  new Notification(data.title, {
                    body: data.message,
                    icon: '/Images/icons/icon-192x192.png'
                  });
                }
                
                // Update Badge
                unreadCount++;
                if(notifBadge) {
                  notifBadge.textContent = unreadCount;
                  notifBadge.style.display = 'block';
                }
                
                // Prepend to list
                const date = new Date(data.timestamp).toLocaleString();
                const newHtml = `
                  <div style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.05); background:rgba(212,175,55,0.05);">
                    <strong style="display:block; color:#fff; font-size:13px; margin-bottom:4px;">${data.title}</strong>
                    <div style="color:rgba(255,255,255,0.7); font-size:12px; margin-bottom:4px;">${data.message}</div>
                    <div style="color:#D4AF37; font-size:10px;">${date}</div>
                  </div>
                `;
                notifList.insertAdjacentHTML('afterbegin', newHtml);
              }
            });
          });
      })
      .catch(err => {
        console.error("Error loading notifications:", err);
        notifList.innerHTML = `<div style="text-align:center; padding:20px; color:rgba(255,74,74,0.8); font-size:12px;">Failed to load.</div>`;
      });
  }

  initNotifications();
});
