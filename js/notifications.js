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

/* ============================================================
   MOBILE CALL BUTTON — Intercepts .whatsapp-btn on mobile and
   shows a luxury popup with WhatsApp / Contact Us options.
   Works on EVERY page that loads notifications.js.
   ============================================================ */
(function () {
  function isMobile() { return window.innerWidth <= 768; }

  function injectCallPopup() {
    if (document.getElementById('reel-call-popup')) return; // already injected

    const popup = document.createElement('div');
    popup.id = 'reel-call-popup';
    popup.setAttribute('role', 'dialog');
    popup.setAttribute('aria-modal', 'true');
    popup.setAttribute('aria-label', 'Connect with REEL');
    popup.style.cssText = [
      'display:none',
      'position:fixed',
      'bottom:84px',
      'right:18px',
      'width:272px',
      'background:rgba(10,10,10,0.97)',
      'border:1px solid rgba(212,175,55,0.38)',
      'border-radius:18px',
      'box-shadow:0 20px 48px rgba(0,0,0,0.78),0 0 0 1px rgba(212,175,55,0.08)',
      'backdrop-filter:blur(22px)',
      '-webkit-backdrop-filter:blur(22px)',
      'z-index:9999',
      'overflow:hidden',
      'transform:translateY(10px) scale(0.96)',
      'opacity:0',
      'transition:transform 0.25s cubic-bezier(.34,1.56,.64,1), opacity 0.22s ease',
      'font-family:"Outfit","Cormorant Garamond",sans-serif',
    ].join(';');

    popup.innerHTML = `
      <!-- Header -->
      <div style="padding:14px 16px 12px;border-bottom:1px solid rgba(212,175,55,0.18);display:flex;align-items:center;justify-content:space-between;">
        <span style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;font-weight:600;color:#D4AF37;letter-spacing:.03em;">Connect with REEL</span>
        <button id="reel-call-popup-close" aria-label="Close" style="background:none;border:none;cursor:pointer;padding:4px;line-height:1;color:rgba(255,255,255,0.5);font-size:18px;transition:color .2s;">&#x2715;</button>
      </div>
      <!-- Options -->
      <div style="padding:14px 14px 16px;display:flex;flex-direction:column;gap:11px;">
        <!-- WhatsApp -->
        <a href="https://wa.me/2348067029444" target="_blank" rel="noopener noreferrer" id="reel-popup-wa"
           style="display:flex;align-items:center;gap:14px;padding:13px 14px;border-radius:12px;background:rgba(37,211,102,0.08);border:1px solid rgba(37,211,102,0.25);text-decoration:none;cursor:pointer;transition:background .2s,transform .18s,box-shadow .2s;">
          <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#25D366,#128C7E);display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 4px 12px rgba(37,211,102,0.3);">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
          </div>
          <div style="flex:1;">
            <div style="font-size:.92rem;font-weight:600;color:#25D366;margin-bottom:2px;">WhatsApp</div>
            <div style="font-size:.75rem;color:rgba(255,255,255,0.45);">Chat directly with us</div>
          </div>
          <svg style="opacity:.45;flex-shrink:0;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#25D366" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
        <!-- Contact Us -->
        <a href="contact.html" id="reel-popup-contact"
           style="display:flex;align-items:center;gap:14px;padding:13px 14px;border-radius:12px;background:rgba(212,175,55,0.07);border:1px solid rgba(212,175,55,0.22);text-decoration:none;cursor:pointer;transition:background .2s,transform .18s,box-shadow .2s;">
          <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#D4AF37,#AA771C);display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 4px 12px rgba(212,175,55,0.3);">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.27h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.06 6.06l1.57-1.57a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          </div>
          <div style="flex:1;">
            <div style="font-size:.92rem;font-weight:600;color:#D4AF37;margin-bottom:2px;">Contact Us</div>
            <div style="font-size:.75rem;color:rgba(255,255,255,0.45);">Offices &amp; inquiry form</div>
          </div>
          <svg style="opacity:.45;flex-shrink:0;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
      </div>
    `;

    document.body.appendChild(popup);

    // Close button
    document.getElementById('reel-call-popup-close').addEventListener('click', closePopup);

    // Close on outside tap
    document.addEventListener('touchstart', function outsideTap(e) {
      const btn = document.querySelector('.whatsapp-btn');
      if (!popup.contains(e.target) && (!btn || !btn.contains(e.target))) {
        closePopup();
      }
    }, { passive: true });

    // Close on ESC
    document.addEventListener('keydown', function escKey(e) {
      if (e.key === 'Escape') closePopup();
    });

    // Hover effects
    ['reel-popup-wa', 'reel-popup-contact'].forEach(function(id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.addEventListener('mouseenter', function() {
        el.style.transform = 'translateY(-2px)';
        el.style.boxShadow = '0 8px 20px rgba(0,0,0,0.3)';
      });
      el.addEventListener('mouseleave', function() {
        el.style.transform = '';
        el.style.boxShadow = '';
      });
    });
  }

  function openPopup() {
    var p = document.getElementById('reel-call-popup');
    if (!p) return;
    p.style.display = 'block';
    requestAnimationFrame(function() {
      p.style.opacity = '1';
      p.style.transform = 'translateY(0) scale(1)';
    });
  }

  function closePopup() {
    var p = document.getElementById('reel-call-popup');
    if (!p) return;
    p.style.opacity = '0';
    p.style.transform = 'translateY(10px) scale(0.96)';
    setTimeout(function() { p.style.display = 'none'; }, 250);
  }

  function setupWhatsAppInterceptor() {
    if (!isMobile()) return;

    var btn = document.querySelector('.whatsapp-btn');
    if (!btn || btn.dataset.mobileCall === 'true') return;

    // Mark button as mobile call button (triggers CSS phone icon)
    btn.dataset.mobileCall = 'true';
    btn.setAttribute('aria-label', 'Contact REEL');
    btn.setAttribute('title', 'Contact REEL');
    btn.style.pointerEvents = 'auto';

    // Remove the href navigation — we handle it via JS click
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      var p = document.getElementById('reel-call-popup');
      if (p && p.style.display !== 'none') {
        closePopup();
      } else {
        injectCallPopup();
        openPopup();
      }
    });
  }

  // Run after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupWhatsAppInterceptor);
  } else {
    // DOMContentLoaded already fired, run now (this IIFE runs after the main listener above)
    setTimeout(setupWhatsAppInterceptor, 0);
  }

  // Also re-check on resize in case user rotates device
  window.addEventListener('resize', function() {
    var btn = document.querySelector('.whatsapp-btn');
    if (isMobile() && btn && btn.dataset.mobileCall !== 'true') {
      setupWhatsAppInterceptor();
    } else if (!isMobile()) {
      closePopup();
    }
  });
}());
