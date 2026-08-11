import os

def rewrite_admin_js():
    file_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\admin\js\admin.js"
    
    new_js = """/**
 * REEL - Admin Controller
 * Handles authentication and saving data to FIREBASE FIRESTORE.
 */

const MASTER_PASS = "REEGLOBAL@090021";

document.addEventListener('DOMContentLoaded', () => {
  
  // --- LOGIN LOGIC ---
  const loginForm = document.getElementById('admin-login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const passInput = document.getElementById('admin-pass').value;
      const errorMsg = document.getElementById('login-error');
      
      if (passInput === MASTER_PASS) {
        sessionStorage.setItem('ree_admin_auth', 'true');
        window.location.href = 'index.html';
      } else {
        errorMsg.style.display = 'block';
        const card = document.querySelector('.admin-login-card');
        card.style.transform = 'translateX(-10px)';
        setTimeout(() => card.style.transform = 'translateX(10px)', 100);
        setTimeout(() => card.style.transform = 'translateX(-10px)', 200);
        setTimeout(() => card.style.transform = 'translateX(10px)', 300);
        setTimeout(() => card.style.transform = 'translateX(0)', 400);
      }
    });
  }

  // --- DASHBOARD LOGIC ---
  const dashboard = document.getElementById('admin-dashboard');
  if (dashboard) {
    if (sessionStorage.getItem('ree_admin_auth') !== 'true') {
      window.location.href = 'login.html';
      return;
    }

    document.getElementById('logout-btn').addEventListener('click', (e) => {
      e.preventDefault();
      sessionStorage.removeItem('ree_admin_auth');
      window.location.href = 'login.html';
    });

    const navLinks = document.querySelectorAll('.admin-nav-link');
    const sections = document.querySelectorAll('.admin-section');
    
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        navLinks.forEach(l => l.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active'));
        link.classList.add('active');
        const targetId = link.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');
      });
    });

    // --- FIREBASE INITIALIZATION WAIT ---
    const waitForDb = (callback) => {
      if (window.db) {
        callback();
      } else {
        setTimeout(() => waitForDb(callback), 100);
      }
    };

    waitForDb(() => {
      initAdminPanel();
    });
  }

  // GLOBAL SCHEDULER STATE
  let pendingScheduleTime = null;
  let activeScheduleForm = null;

  window.closeScheduleModal = function() {
    document.getElementById('schedule-modal-overlay').style.display = 'none';
    if(activeScheduleForm) {
      // Revert select back to published if they cancel
      const select = document.getElementById(activeScheduleForm + '-status');
      if(select) select.value = 'published';
    }
  };

  window.confirmScheduleTime = function() {
    const input = document.getElementById('global-schedule-time').value;
    if(!input) {
      alert("Please select a date and time!");
      return;
    }
    pendingScheduleTime = input;
    document.getElementById('schedule-modal-overlay').style.display = 'none';
    showToast("Scheduled", "Time has been set successfully.");
  };

  function initAdminPanel() {
    
    // --- SCHEDULER TOGGLE MODAL LOGIC ---
    const setupScheduleToggle = (selectId, prefix) => {
      const select = document.getElementById(selectId);
      if(select) {
        select.addEventListener('change', (e) => {
          if (e.target.value === 'scheduled') {
            activeScheduleForm = prefix;
            document.getElementById('schedule-modal-overlay').style.display = 'flex';
          }
        });
      }
    };
    setupScheduleToggle('blog-status', 'blog');
    setupScheduleToggle('portfolio-status', 'portfolio');
    setupScheduleToggle('shop-status', 'shop');

    // --- RENDER HELPERS ---
    const renderAdminList = (docs, containerId, type) => {
      const container = document.getElementById(containerId);
      if (!container) return;
      container.innerHTML = '';
      
      if (docs.length === 0) {
        container.innerHTML = `<div class="empty-state">No ${type} items found.</div>`;
        return;
      }
      
      docs.forEach((docSnap) => {
        const item = docSnap.data();
        const id = docSnap.id;
        const div = document.createElement('div');
        div.className = 'admin-list-item';
        div.innerHTML = `
          <div class="item-info">
            <strong>${item.title || item.name} ${item.status === 'scheduled' ? '<span style="color:#D4AF37; font-size:0.7rem;">(Scheduled)</span>' : ''}</strong>
            <span class="item-date">${item.date || item.category || item.price}</span>
          </div>
          <button class="btn-delete" data-id="${id}" data-type="${type}">Delete</button>
        `;
        container.appendChild(div);
      });

      container.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const id = e.target.getAttribute('data-id');
          const t = e.target.getAttribute('data-type');
          if (confirm(`Are you sure you want to delete this item?`)) {
            let collection = t === 'product' ? 'products' : t;
            if(t==='blog') collection = 'blogs';
            window.db.collection(collection).doc(id).delete().then(() => showToast("Deleted", "Item removed successfully.", "delete"));
          }
        });
      });
    };

    const renderSchedulerList = (allScheduled) => {
      const container = document.getElementById('scheduler-list');
      if (!container) return;
      container.innerHTML = '';
      
      if(allScheduled.length === 0) {
        container.innerHTML = `<div class="empty-state">No scheduled content.</div>`;
        return;
      }
      
      allScheduled.sort((a,b) => new Date(a.scheduleTime) - new Date(b.scheduleTime));
      
      allScheduled.forEach(item => {
        const div = document.createElement('div');
        div.className = 'admin-list-item';
        const dateStr = new Date(item.scheduleTime).toLocaleString();
        div.innerHTML = `
          <div class="item-info">
            <span style="font-size:0.65rem; color:var(--gold); text-transform:uppercase;">${item.type}</span>
            <strong>${item.title || item.name}</strong>
            <span class="item-date">Scheduled for: ${dateStr}</span>
          </div>
          <button class="btn-delete" data-id="${item.id}" data-type="${item.type}">Delete</button>
        `;
        container.appendChild(div);
      });
      
      container.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const id = e.target.getAttribute('data-id');
          const t = e.target.getAttribute('data-type');
          if (confirm(`Are you sure you want to delete this scheduled item?`)) {
            let col = t === 'product' ? 'products' : t;
            if(t==='blog') col = 'blogs';
            window.db.collection(col).doc(id).delete().then(()=> showToast("Deleted", "Scheduled item removed."));
          }
        });
      });
    };

    // --- REALTIME LISTENERS ---
    let globalScheduled = [];
    
    window.db.collection('blogs').orderBy('timestamp', 'desc').onSnapshot(snap => {
      renderAdminList(snap.docs, 'blog-list', 'blog');
      globalScheduled = globalScheduled.filter(i => i.type !== 'blog');
      snap.forEach(d => {
        if(d.data().status === 'scheduled') globalScheduled.push({id: d.id, type: 'blog', ...d.data()});
      });
      renderSchedulerList(globalScheduled);
    });

    window.db.collection('portfolio').orderBy('timestamp', 'desc').onSnapshot(snap => {
      renderAdminList(snap.docs, 'portfolio-list', 'portfolio');
      globalScheduled = globalScheduled.filter(i => i.type !== 'portfolio');
      snap.forEach(d => {
        if(d.data().status === 'scheduled') globalScheduled.push({id: d.id, type: 'portfolio', ...d.data()});
      });
      renderSchedulerList(globalScheduled);
    });

    window.db.collection('products').orderBy('timestamp', 'desc').onSnapshot(snap => {
      renderAdminList(snap.docs, 'product-list', 'product');
      globalScheduled = globalScheduled.filter(i => i.type !== 'product');
      snap.forEach(d => {
        if(d.data().status === 'scheduled') globalScheduled.push({id: d.id, type: 'product', ...d.data()});
      });
      renderSchedulerList(globalScheduled);
    });

    // --- FORM SUBMISSIONS (FIREBASE) ---
    
    // Blog
    document.getElementById('form-blog').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = document.getElementById('blog-title').value;
      const category = document.getElementById('blog-cat').value;
      const content = document.getElementById('blog-content').value;
      const status = document.getElementById('blog-status').value;
      const fileInput = document.getElementById('blog-img');
      
      let sTime = status === 'scheduled' ? pendingScheduleTime : null;

      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          window.db.collection('blogs').add({
            title, category, content, status, scheduleTime: sTime,
            image: evt.target.result, 
            date: (status === 'scheduled' && sTime) ? new Date(sTime).toLocaleDateString('en-US', {month: 'short', day: 'numeric', year: 'numeric'}) : new Date().toLocaleDateString('en-US', {month: 'short', day: 'numeric', year: 'numeric'}),
            timestamp: Date.now()
          }).then(() => {
            e.target.reset(); pendingScheduleTime = null;
            showToast('Published', 'Blog post successfully added to Firebase.');
          });
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        alert("Please select an image.");
      }
    });

    // Portfolio
    document.getElementById('form-portfolio').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = document.getElementById('pf-title').value;
      const category = document.getElementById('pf-cat').value;
      const status = document.getElementById('portfolio-status').value;
      const fileInput = document.getElementById('pf-img');
      let sTime = status === 'scheduled' ? pendingScheduleTime : null;
      
      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          window.db.collection('portfolio').add({
            title, category, status, scheduleTime: sTime,
            image: evt.target.result,
            timestamp: Date.now()
          }).then(() => {
            e.target.reset(); pendingScheduleTime = null;
            showToast('Added', 'Portfolio project saved.');
          });
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        alert("Please select an image.");
      }
    });

    // Shop
    document.getElementById('form-shop').addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('shop-name').value;
      const price = document.getElementById('shop-price').value;
      const category = document.getElementById('shop-cat').value;
      const status = document.getElementById('shop-status').value;
      const fileInput = document.getElementById('shop-img');
      let sTime = status === 'scheduled' ? pendingScheduleTime : null;
      
      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          window.db.collection('products').add({
            name, price, category, status, scheduleTime: sTime,
            image: evt.target.result,
            timestamp: Date.now()
          }).then(() => {
            e.target.reset(); pendingScheduleTime = null;
            showToast('Added', 'Product saved to shop.');
          });
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        alert("Please select an image.");
      }
    });

    // --- BROADCAST CENTER LOGIC ---
    const bcInput = document.getElementById('bc-input');
    const bcPreview = document.getElementById('bc-preview');
    const bcCount = document.getElementById('bc-count');
    const bcSendBtn = document.getElementById('bc-send-btn');
    const bcHistoryList = document.getElementById('bc-history-list');

    if(bcInput) {
      bcInput.addEventListener('input', (e) => {
        const val = e.target.value;
        bcCount.textContent = `${val.length}/300`;
        bcPreview.textContent = val.trim() === '' ? 'Your message will appear here...' : val;
      });

      bcSendBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const body = bcInput.value.trim();
        if(!body) return;
        
        // Extract a title dynamically, e.g. first 20 chars
        const title = "New Broadcast from REEL";
        
        bcSendBtn.disabled = true;
        bcSendBtn.innerHTML = "Sending...";
        
        window.db.collection('notifications').add({
          title: title,
          message: body,
          timestamp: Date.now()
        }).then(() => {
          showToast('Broadcast Sent!', 'Notification saved and pushed to users.', 'check');
          bcInput.value = '';
          bcCount.textContent = `0/300`;
          bcPreview.textContent = 'Your message will appear here...';
          bcSendBtn.disabled = false;
          bcSendBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg> Send Broadcast`;
        }).catch(err => {
          console.error(err);
          alert('Failed to send notification: ' + err.message);
          bcSendBtn.disabled = false;
        });
      });

      // Listen to notification history
      window.db.collection('notifications').orderBy('timestamp', 'desc').limit(15).onSnapshot(snap => {
        if(snap.empty) {
          bcHistoryList.innerHTML = `<div class="bc-empty"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="32" height="32"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path></svg>No broadcast history found</div>`;
          return;
        }
        let hHtml = '';
        snap.forEach(doc => {
          const d = doc.data();
          hHtml += `
            <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px; margin-bottom:10px;">
              <div style="font-size:0.75rem; color:#D4AF37; margin-bottom:6px;">${new Date(d.timestamp).toLocaleString()}</div>
              <div style="font-size:0.9rem; color:#fff;">${d.message}</div>
            </div>
          `;
        });
        bcHistoryList.innerHTML = hHtml;
      });
    }
  } // end initAdminPanel

});
"""

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_js)
    print("Updated admin.js")

if __name__ == "__main__":
    rewrite_admin_js()
