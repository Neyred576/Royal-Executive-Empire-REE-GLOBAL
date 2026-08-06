document.addEventListener('DOMContentLoaded', () => {
  // 1. Inject Notification Bell into Header
  const navActions = document.querySelector('.nav-actions');
  if (navActions) {
    const bellHtml = `
      <div class="nav-icon" id="notif-btn" style="cursor:pointer;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="width:18px;height:18px;">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
        <span id="notif-badge" style="display:none; position:absolute; top:-6px; right:-6px; background:#D4AF37; color:#000; font-size:10px; font-weight:bold; padding:2px 6px; border-radius:10px;">0</span>
        
        <!-- Dropdown Panel -->
        <div id="notif-panel" style="display:none; position:absolute; top:45px; right:-10px; width:300px; max-width:none; min-width:300px; white-space:normal; text-align:left; background:rgba(10,10,10,0.95); backdrop-filter:blur(10px); border:1px solid rgba(212,175,55,0.3); border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.5); z-index:100; overflow:hidden;">
          <div style="padding:15px; border-bottom:1px solid rgba(255,255,255,0.1); display:flex; justify-content:space-between; align-items:center;">
            <h4 style="margin:0; font-family:'Cormorant Garamond', serif; color:#D4AF37;">Notifications</h4>
            <button id="notif-enable-btn" style="background:transparent; border:1px solid #D4AF37; color:#D4AF37; padding:4px 8px; border-radius:4px; font-size:10px; cursor:pointer;">Enable Alerts</button>
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

          <div id="notif-list" style="max-height:250px; overflow-y:auto; padding:10px;">
            <div style="text-align:center; padding:20px; color:rgba(255,255,255,0.5); font-size:12px;">Loading...</div>
          </div>
        </div>
      </div>
    `;
    navActions.insertAdjacentHTML('afterbegin', bellHtml);
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

  if (notifBtn) {
    notifBtn.addEventListener('click', (e) => {
      // Prevent bubbling to document so it doesn't close immediately
      e.stopPropagation();
      const isVisible = notifPanel.style.display === 'block';
      notifPanel.style.display = isVisible ? 'none' : 'block';
      
      if (!isVisible) {
        unreadCount = 0;
        notifBadge.style.display = 'none';
        notifBadge.textContent = '0';
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
