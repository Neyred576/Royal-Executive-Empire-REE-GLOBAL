let deferredPrompt;

// ── Detect iOS ──
const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
const isInStandaloneMode = ('standalone' in navigator && navigator.standalone);

// ── Register Service Worker ──
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('ServiceWorker registered with scope:', registration.scope);
      })
      .catch(err => {
        console.log('ServiceWorker registration failed:', err);
      });
  });
}

// ── Capture Android install prompt ──
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  // Don't auto-show; will be triggered by cookie consent
});

// ── Inject shared animation styles ──
function ensureAnimStyles() {
  if (document.getElementById('pwa-anim-style')) return;
  const style = document.createElement('style');
  style.id = 'pwa-anim-style';
  style.textContent = `
    @keyframes pwaSlideUp {
      from { opacity: 0; transform: translate(-50%, 30px); }
      to   { opacity: 1; transform: translate(-50%, 0); }
    }
    @keyframes pwaSlideDown {
      from { opacity: 0; transform: translate(-50%, -30px); }
      to   { opacity: 1; transform: translate(-50%, 0); }
    }
    .pwa-toast-base {
      position: fixed;
      left: 50%;
      transform: translateX(-50%);
      width: 92%;
      max-width: 390px;
      background: rgba(12, 12, 12, 0.98);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(212, 175, 55, 0.45);
      border-radius: 18px;
      padding: 14px 16px;
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 99999;
      box-shadow: 0 24px 60px rgba(0,0,0,0.85);
      color: #fff;
      font-family: 'Outfit', sans-serif;
    }
    .pwa-toast-icon {
      width: 42px;
      height: 42px;
      border-radius: 10px;
      background: rgba(212,175,55,0.12);
      border: 1px solid rgba(212,175,55,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .pwa-toast-icon img { width: 28px; height: 28px; object-fit: contain; }
    .pwa-toast-body { flex: 1; min-width: 0; }
    .pwa-toast-title { font-weight: 700; font-size: 0.9rem; color: #D4AF37; line-height: 1.2; margin-bottom: 2px; }
    .pwa-toast-sub   { font-size: 0.72rem; color: rgba(255,255,255,0.7); line-height: 1.3; }
    .pwa-toast-actions { display: flex; gap: 8px; align-items: center; flex-shrink: 0; }
    .pwa-btn-install {
      background: linear-gradient(135deg, #D4AF37, #B8962E);
      color: #000;
      border: none;
      border-radius: 8px;
      padding: 8px 14px;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.5px;
      cursor: pointer;
      white-space: nowrap;
      box-shadow: 0 4px 12px rgba(212,175,55,0.35);
    }
    .pwa-btn-close {
      background: transparent;
      color: rgba(255,255,255,0.4);
      border: none;
      font-size: 1.7rem;
      line-height: 1;
      cursor: pointer;
      padding: 0;
    }
    .pwa-ios-steps {
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px solid rgba(212,175,55,0.15);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .pwa-ios-step {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.72rem;
      color: rgba(255,255,255,0.75);
    }
    .pwa-ios-step-num {
      width: 20px; height: 20px;
      border-radius: 50%;
      background: rgba(212,175,55,0.2);
      color: #D4AF37;
      font-size: 0.65rem;
      font-weight: 800;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
    }
  `;
  document.head.appendChild(style);
}

// ── Main Install Promotion Function (called after cookie accept) ──
function showInstallPromotion() {
  if (document.getElementById('pwa-install-toast')) return;

  ensureAnimStyles();

  if (isIOS) {
    showIOSInstallModal();
  } else {
    showAndroidInstallModal();
  }
}

// ── Android Install Modal ──
function showAndroidInstallModal() {
  const toast = document.createElement('div');
  toast.id = 'pwa-install-toast';
  toast.className = 'pwa-toast-base';
  toast.style.bottom = '90px';
  toast.style.animation = 'pwaSlideUp 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards';

  toast.innerHTML = `
    <div class="pwa-toast-icon">
      <img src="/Images/BG/logo%20bg.png" onerror="this.outerHTML='<span style=\\'font-size:1.4rem\\'>⚜</span>'" alt="REEL">
    </div>
    <div class="pwa-toast-body">
      <div class="pwa-toast-title">Install REEL App</div>
      <div class="pwa-toast-sub">Add to home screen for fast access</div>
    </div>
    <div class="pwa-toast-actions">
      <button class="pwa-btn-install" id="pwa-install-btn">INSTALL</button>
      <button class="pwa-btn-close" id="pwa-install-close">&times;</button>
    </div>
  `;

  document.body.appendChild(toast);

  document.getElementById('pwa-install-btn').addEventListener('click', async () => {
    toast.remove();
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      console.log('Install prompt outcome:', outcome);
      deferredPrompt = null;
    }
  });

  document.getElementById('pwa-install-close').addEventListener('click', () => toast.remove());
}

// ── iOS Install Modal (manual instructions since Safari blocks auto-prompt) ──
function showIOSInstallModal() {
  const toast = document.createElement('div');
  toast.id = 'pwa-install-toast';
  toast.className = 'pwa-toast-base';
  toast.style.bottom = '90px';
  toast.style.animation = 'pwaSlideUp 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards';
  toast.style.flexDirection = 'column';
  toast.style.alignItems = 'stretch';
  toast.style.gap = '0';

  toast.innerHTML = `
    <div style="display:flex; align-items:center; gap:10px;">
      <div class="pwa-toast-icon">
        <img src="/Images/BG/logo%20bg.png" onerror="this.outerHTML='<span style=\\'font-size:1.4rem\\'>⚜</span>'" alt="REEL">
      </div>
      <div class="pwa-toast-body">
        <div class="pwa-toast-title">Add REEL to Home Screen</div>
        <div class="pwa-toast-sub">Follow 3 quick steps below</div>
      </div>
      <div class="pwa-toast-actions">
        <button class="pwa-btn-close" id="pwa-install-close">&times;</button>
      </div>
    </div>
    <div class="pwa-ios-steps">
      <div class="pwa-ios-step">
        <div class="pwa-ios-step-num">1</div>
        <span>Tap the <strong style="color:#D4AF37;">Share</strong> button&nbsp;
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="2.5" style="vertical-align:middle;">
            <path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/>
            <polyline points="16 6 12 2 8 6"/>
            <line x1="12" y1="2" x2="12" y2="15"/>
          </svg>
          at the bottom of Safari
        </span>
      </div>
      <div class="pwa-ios-step">
        <div class="pwa-ios-step-num">2</div>
        <span>Scroll down and tap <strong style="color:#D4AF37;">"Add to Home Screen"</strong></span>
      </div>
      <div class="pwa-ios-step">
        <div class="pwa-ios-step-num">3</div>
        <span>Tap <strong style="color:#D4AF37;">Add</strong> in the top-right corner</span>
      </div>
    </div>
  `;

  document.body.appendChild(toast);
  document.getElementById('pwa-install-close').addEventListener('click', () => toast.remove());
}

// ── Hide install toast once app is installed ──
window.addEventListener('appinstalled', () => {
  console.log('PWA was installed');
  const toast = document.getElementById('pwa-install-toast');
  if (toast) toast.remove();
});

// ── Notifications Modal (shown 5s after page load, once per session) ──
function showNotificationPromotion() {
  if (document.getElementById('pwa-notification-toast')) return;
  if (!('Notification' in window)) return;
  if (Notification.permission !== 'default') return;
  if (sessionStorage.getItem('ree_notif_prompted')) return;

  ensureAnimStyles();

  const toast = document.createElement('div');
  toast.id = 'pwa-notification-toast';
  toast.className = 'pwa-toast-base';
  toast.style.top = '15px';
  toast.style.animation = 'pwaSlideDown 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards';

  toast.innerHTML = `
    <div class="pwa-toast-icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="2">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
      </svg>
    </div>
    <div class="pwa-toast-body">
      <div class="pwa-toast-title">Enable Push Alerts</div>
      <div class="pwa-toast-sub">Stay updated on exclusive deals &amp; news</div>
    </div>
    <div class="pwa-toast-actions">
      <button class="pwa-btn-install" id="pwa-notif-allow-btn">ENABLE</button>
      <button class="pwa-btn-close" id="pwa-notif-close-btn">&times;</button>
    </div>
  `;

  document.body.appendChild(toast);

  document.getElementById('pwa-notif-allow-btn').addEventListener('click', async () => {
    toast.remove();
    sessionStorage.setItem('ree_notif_prompted', 'true');
    const permission = await Notification.requestPermission();
    console.log('Notification permission:', permission);
  });

  document.getElementById('pwa-notif-close-btn').addEventListener('click', () => {
    toast.remove();
    sessionStorage.setItem('ree_notif_prompted', 'true');
  });
}

// Show notification prompt after 5 seconds
setTimeout(showNotificationPromotion, 5000);
