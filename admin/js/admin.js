/**
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

    // --- INITIALIZE QUILL EDITOR ---
    let blogQuill = null;
    if (document.getElementById('blog-quill-editor') && typeof Quill !== 'undefined') {
      blogQuill = new Quill('#blog-quill-editor', {
        theme: 'snow',
        placeholder: 'Write your full executive blog post here…',
        modules: {
          toolbar: [
            [{ 'header': [1, 2, 3, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ 'color': [] }, { 'background': [] }],
            [{ 'list': 'ordered' }, { 'list': 'bullet' }],
            ['link', 'clean']
          ]
        }
      });

      // Real-time word count
      blogQuill.on('text-change', function () {
        const text = blogQuill.getText().trim();
        const words = text.length > 0 ? text.split(/\s+/).length : 0;
        const chars = text.length;

        const qlInfo = document.getElementById('ql-word-info');
        const headerInfo = document.getElementById('word-count-display');

        if (qlInfo) qlInfo.textContent = `${words} words · ${chars} characters`;
        if (headerInfo) headerInfo.textContent = `${words} words`;
      });
    }

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

  window.closeScheduleModal = function () {
    document.getElementById('schedule-modal-overlay').style.display = 'none';
    if (activeScheduleForm) {
      // Revert select back to published if they cancel
      const select = document.getElementById(activeScheduleForm + '-status');
      if (select) select.value = 'published';
    }
  };

  window.confirmScheduleTime = function () {
    const input = document.getElementById('global-schedule-time').value;
    if (!input) {
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
      if (select) {
        select.addEventListener('change', (e) => {
          if (e.target.value === 'scheduled') {
            activeScheduleForm = prefix;
            document.getElementById('schedule-modal-overlay').style.display = 'flex';
          }
        });
      }
    };
    setupScheduleToggle('blog-status', 'blog');
    setupScheduleToggle('prop-status', 'properties');
    setupScheduleToggle('shop-status', 'shop');
    setupScheduleToggle('power-status', 'power');

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
        let editBtn = (type === 'blog' || type === 'power') ? `<button class="btn-edit" data-id="${id}" data-type="${type}" style="margin-right:8px; background:var(--gold); color:#000;">Edit</button>` : '';
        div.innerHTML = `
          <div class="item-info">
            <strong>${item.title || item.name} ${item.status === 'scheduled' ? '<span style="color:#D4AF37; font-size:0.7rem;">(Scheduled)</span>' : ''}</strong>
            <span class="item-date">${item.date || item.category || item.price}</span>
          </div>
          ${editBtn}
          <button class="btn-delete" data-id="${id}" data-type="${type}">Delete</button>
        `;
        container.appendChild(div);
      });

      container.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const id = e.target.getAttribute('data-id');
          const t = e.target.getAttribute('data-type');

          if (t === 'power') {
            window.db.collection('powerProducts').doc(id).get().then(doc => {
              if (doc.exists) {
                const data = doc.data();
                document.getElementById('power-name').value = data.name || '';
                document.getElementById('power-caption').value = data.caption || '';
                document.getElementById('power-price').value = data.price || '';
                document.getElementById('power-details').value = data.details || '';
                document.getElementById('power-video').value = data.video || '';
                document.getElementById('power-status').value = data.status || 'published';
                const featuredCheckbox = document.getElementById('power-featured');
                if (featuredCheckbox) featuredCheckbox.checked = !!data.featured;
                window.editPowerId = id;
                const submitBtn = document.querySelector('#form-power button[type="submit"]');
                if (submitBtn) submitBtn.innerHTML = 'Update Product';
                // Navigate to power section
                document.querySelectorAll('.admin-nav-link').forEach(l => l.classList.remove('active'));
                document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
                document.querySelector('[data-target="sec-power"]').classList.add('active');
                document.getElementById('sec-power').classList.add('active');
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }
            });
          } else {
            window.db.collection('blogs').doc(id).get().then(doc => {
              if (doc.exists) {
                const data = doc.data();
                document.getElementById('blog-title').value = data.title || '';
                document.getElementById('blog-cat').value = data.category || 'Business Strategy';
                document.getElementById('blog-status').value = data.status || 'published';
                if (blogQuill) {
                  blogQuill.root.innerHTML = data.content || '';
                } else {
                  document.getElementById('blog-content').value = data.content || '';
                }
                window.editBlogId = id;
                const submitBtn = document.querySelector('#form-blog button[type="submit"]');
                if (submitBtn) submitBtn.innerHTML = 'Update Blog Post';
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }
            });
          }
        });
      });

      container.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const id = e.target.getAttribute('data-id');
          const t = e.target.getAttribute('data-type');
          if (confirm(`Are you sure you want to delete this item?`)) {
            let collection = t === 'product' ? 'products' : t === 'power' ? 'powerProducts' : t === 'blog' ? 'blogs' : t;
            window.db.collection(collection).doc(id).delete().then(() => showToast("Deleted", "Item removed successfully.", "delete"));
          }
        });
      });
    };

    const renderSchedulerList = (allScheduled) => {
      const container = document.getElementById('scheduler-list');
      if (!container) return;
      container.innerHTML = '';

      if (allScheduled.length === 0) {
        container.innerHTML = `<div class="empty-state">No scheduled content.</div>`;
        return;
      }

      allScheduled.sort((a, b) => new Date(a.scheduleTime) - new Date(b.scheduleTime));

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
            let col = t === 'product' ? 'products' : t === 'power' ? 'powerProducts' : t === 'blog' ? 'blogs' : t;
            window.db.collection(col).doc(id).delete().then(() => showToast("Deleted", "Scheduled item removed."));
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
        if (d.data().status === 'scheduled') globalScheduled.push({ id: d.id, type: 'blog', ...d.data() });
      });
      renderSchedulerList(globalScheduled);
      
      // Update Dashboard Stats
      const sbCountBlog = document.getElementById('sb-count-blog');
      const statBlog = document.getElementById('stat-blog');
      if (sbCountBlog) sbCountBlog.textContent = snap.size;
      if (statBlog) statBlog.textContent = snap.size;
    });

    window.db.collection('properties').orderBy('timestamp', 'desc').onSnapshot(snap => {
      renderAdminList(snap.docs, 'prop-list', 'properties');
      globalScheduled = globalScheduled.filter(i => i.type !== 'properties');
      snap.forEach(d => {
        if (d.data().status === 'scheduled') globalScheduled.push({ id: d.id, type: 'properties', ...d.data() });
      });
      renderSchedulerList(globalScheduled);

      // Update Dashboard Stats
      const sbCountProp = document.getElementById('sb-count-prop');
      const statPf = document.getElementById('stat-pf');
      if (sbCountProp) sbCountProp.textContent = snap.size;
      if (statPf) statPf.textContent = snap.size;
    });

    window.db.collection('products').orderBy('timestamp', 'desc').onSnapshot(snap => {
      renderAdminList(snap.docs, 'product-list', 'product');
      globalScheduled = globalScheduled.filter(i => i.type !== 'product');
      snap.forEach(d => {
        if (d.data().status === 'scheduled') globalScheduled.push({ id: d.id, type: 'product', ...d.data() });
      });
      renderSchedulerList(globalScheduled);

      // Update Dashboard Stats
      const sbCountShop = document.getElementById('sb-count-shop');
      const statShop = document.getElementById('stat-shop');
      if (sbCountShop) sbCountShop.textContent = snap.size;
      if (statShop) statShop.textContent = snap.size;
    });

    // --- POWER PRODUCTS REALTIME LISTENER ---
    window.db.collection('powerProducts').orderBy('timestamp', 'desc').onSnapshot(snap => {
      renderAdminList(snap.docs, 'power-list', 'power');
      globalScheduled = globalScheduled.filter(i => i.type !== 'power');
      snap.forEach(d => {
        if (d.data().status === 'scheduled') globalScheduled.push({ id: d.id, type: 'power', ...d.data() });
      });
      renderSchedulerList(globalScheduled);
    });

    // --- AUTO-PUBLISH ENGINE ---
    // Runs every 60 seconds. Finds any scheduled item whose scheduleTime has passed
    // and upgrades its status to 'published' directly in Firestore.
    const runAutoPublish = async () => {
      const now = Date.now();
      const collections = [
        { name: 'blogs', titleField: 'title' },
        { name: 'properties', titleField: 'title' },
        { name: 'products', titleField: 'name' }
      ];
      for (const col of collections) {
        try {
          const snap = await window.db.collection(col.name)
            .where('status', '==', 'scheduled')
            .get();
          snap.forEach(async (doc) => {
            const data = doc.data();
            if (data.scheduleTime && new Date(data.scheduleTime).getTime() <= now) {
              await window.db.collection(col.name).doc(doc.id).update({
                status: 'published',
                scheduleTime: null
              });
              console.log(`[AutoPublish] ${col.name}/${doc.id} → published`);
            }
          });
        } catch (err) {
          console.warn(`[AutoPublish] Error checking ${col.name}:`, err);
        }
      }
    };
    // Run once immediately on panel load, then every 60 seconds
    runAutoPublish();
    setInterval(runAutoPublish, 60000);

    // --- FORM SUBMISSIONS (FIREBASE) ---

    // Blog
    document.getElementById('form-blog').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = document.getElementById('blog-title').value;
      const category = document.getElementById('blog-cat').value;

      // Get HTML content from Quill editor, fallback to hidden input just in case
      const content = blogQuill ? blogQuill.root.innerHTML : document.getElementById('blog-content').value;

      // Check if editor is practically empty (Quill leaves a <p><br></p> by default)
      if (!content || content === '<p><br></p>') {
        alert("Please enter the blog content.");
        return;
      }
      const status = document.getElementById('blog-status').value;
      const fileInput = document.getElementById('blog-img');

      // Guard: user selected 'scheduled' but never confirmed a time
      if (status === 'scheduled' && !pendingScheduleTime) {
        alert("Please set a schedule date & time before saving.");
        return;
      }

      let sTime = status === 'scheduled' ? pendingScheduleTime : null;
      const submitBtn = document.querySelector('#form-blog button[type="submit"]');

      const saveBlog = (imageData) => {
        const payload = {
          title, category, content, status, scheduleTime: sTime,
          date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
        };
        if (imageData) {
          payload.image = imageData;
        }

        let promise;
        let isEdit = !!window.editBlogId;
        if (isEdit) {
          promise = window.db.collection('blogs').doc(window.editBlogId).update(payload);
        } else {
          payload.timestamp = Date.now();
          promise = window.db.collection('blogs').add(payload);
        }

        promise.then(() => {
          e.target.reset();
          if (blogQuill) blogQuill.root.innerHTML = '';
          pendingScheduleTime = null;
          window.editBlogId = null;
          if (submitBtn) submitBtn.innerHTML = 'Publish Blog Post';
          showToast(isEdit ? 'Updated' : 'Published', isEdit ? 'Blog post successfully updated.' : 'Blog post successfully added to Firebase.');
        });
      };

      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (evt) {
          saveBlog(evt.target.result);
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        if (window.editBlogId) {
          saveBlog(null);
        } else {
          alert("Please select an image.");
        }
      }
    });

    // Properties
    document.getElementById('form-properties').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = document.getElementById('prop-title').value;
      const caption = document.getElementById('prop-caption').value;
      const price = document.getElementById('prop-price').value;
      const status = document.getElementById('prop-status').value;
      const fileInput = document.getElementById('prop-img');

      // Guard: user selected 'scheduled' but never confirmed a time
      if (status === 'scheduled' && !pendingScheduleTime) {
        alert("Please set a schedule date & time before saving.");
        return;
      }

      let sTime = status === 'scheduled' ? pendingScheduleTime : null;

      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (evt) {
          window.db.collection('properties').add({
            title, caption, price, status, scheduleTime: sTime,
            image: evt.target.result,
            timestamp: Date.now()
          }).then(() => {
            e.target.reset(); pendingScheduleTime = null;
            showToast('Added', 'Property saved.');
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

      // Guard: user selected 'scheduled' but never confirmed a time
      if (status === 'scheduled' && !pendingScheduleTime) {
        alert("Please set a schedule date & time before saving.");
        return;
      }

      let sTime = status === 'scheduled' ? pendingScheduleTime : null;

      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (evt) {
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

    // Power Products
    const formPower = document.getElementById('form-power');
    if (formPower) {
      formPower.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('power-name').value;
        const caption = document.getElementById('power-caption').value;
        const price = document.getElementById('power-price').value;
        const details = document.getElementById('power-details').value;
        const video = document.getElementById('power-video').value;
        const status = document.getElementById('power-status').value;
        const fileInput = document.getElementById('power-img');
        const featuredCheckbox = document.getElementById('power-featured');
        const featured = featuredCheckbox ? featuredCheckbox.checked : false;

        if (status === 'scheduled' && !pendingScheduleTime) {
          alert('Please set a schedule date & time before saving.');
          return;
        }

        let sTime = status === 'scheduled' ? pendingScheduleTime : null;
        const submitBtn = document.querySelector('#form-power button[type="submit"]');
        const isEdit = !!window.editPowerId;

        const savePower = (imageData) => {
          const payload = { name, caption, price, details, video, status, scheduleTime: sTime, featured };
          if (imageData) payload.image = imageData;

          let promise;
          if (isEdit) {
            promise = window.db.collection('powerProducts').doc(window.editPowerId).update(payload);
          } else {
            payload.timestamp = Date.now();
            promise = window.db.collection('powerProducts').add(payload);
          }

          promise.then(() => {
            e.target.reset();
            pendingScheduleTime = null;
            window.editPowerId = null;
            if (submitBtn) submitBtn.innerHTML = 'Add Product';
            showToast(isEdit ? 'Updated' : 'Added', isEdit ? 'Product updated successfully.' : 'Power product saved.');
          });
        };

        if (fileInput.files && fileInput.files[0]) {
          const reader = new FileReader();
          reader.onload = (evt) => savePower(evt.target.result);
          reader.readAsDataURL(fileInput.files[0]);
        } else {
          if (isEdit) {
            savePower(null);
          } else {
            alert('Please select a product image.');
          }
        }
      });
    }

    // --- BROADCAST CENTER LOGIC ---
    const bcInput = document.getElementById('bc-input');
    const bcPreview = document.getElementById('bc-preview');
    const bcCount = document.getElementById('bc-count');
    const bcSendBtn = document.getElementById('bc-send-btn');
    const bcHistoryList = document.getElementById('bc-history-list');

    if (bcInput) {
      bcInput.addEventListener('input', (e) => {
        const val = e.target.value;
        bcCount.textContent = `${val.length}/300`;
        bcPreview.textContent = val.trim() === '' ? 'Your message will appear here...' : val;
      });

      bcSendBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const body = bcInput.value.trim();
        if (!body) return;

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
        if (snap.empty) {
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

    // --- ORDERS & MESSAGES STATS ---
    window.db.collection('orders').onSnapshot(snap => {
      const ordersBadge = document.getElementById('orders-badge');
      if (ordersBadge) {
        ordersBadge.textContent = snap.size;
        ordersBadge.style.display = snap.size > 0 ? 'inline-block' : 'none';
      }
    });

    window.db.collection('messages').onSnapshot(snap => {
      const msgsBadge = document.getElementById('msgs-badge');
      if (msgsBadge) {
        msgsBadge.textContent = snap.size;
        msgsBadge.style.display = snap.size > 0 ? 'inline-block' : 'none';
      }
    });

  } // end initAdminPanel

});
