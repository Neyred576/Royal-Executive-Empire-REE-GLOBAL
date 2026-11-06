import sys
sys.stdout.reconfigure(encoding='utf-8')

# ══════════════════════════════════════════════════════════════════════
# FIX 1: real-estate.html — Fix status filter to show AVAILABLE/UNDER OFFER items
# ══════════════════════════════════════════════════════════════════════
with open('real-estate.html', 'r', encoding='utf-8') as f:
    text = f.read()

OLD_FILTER = """        // Show published items; show scheduled items whose time has already passed
        props = props.filter(p => {
          if (!p.status || p.status === 'published') return true;
          if (p.status === 'scheduled' && p.scheduleTime) return new Date() >= new Date(p.scheduleTime);
          return false;
        });"""

NEW_FILTER = """        // Show all available/active properties
        props = props.filter(p => {
          if (!p.status) return true;
          const s = p.status.toUpperCase();
          // Show AVAILABLE and UNDER OFFER; hide SOLD
          if (s === 'AVAILABLE' || s === 'UNDER OFFER' || s === 'UNDEROFFER') return true;
          // Legacy: also show 'published' or scheduled items whose time has passed
          if (s === 'PUBLISHED') return true;
          if (s === 'SCHEDULED' && p.scheduleTime) return new Date() >= new Date(p.scheduleTime);
          return false;
        });"""

if OLD_FILTER in text:
    text = text.replace(OLD_FILTER, NEW_FILTER, 1)
    with open('real-estate.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("FIX 1 OK: real-estate.html status filter updated.")
else:
    print("FIX 1 SKIP: Filter already updated or not found.")

# ══════════════════════════════════════════════════════════════════════
# FIX 2: reel-tech-hub/shop.html — Replace hardcoded cards with Firebase loading
# ══════════════════════════════════════════════════════════════════════
FIREBASE_SCRIPTS = """  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>
  <script src="../js/firebase-init.js"></script>"""

TECH_FIREBASE_LOADER = """
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const grid = document.getElementById('productGrid');
      const catBtns = document.querySelectorAll('.cat-btn');

      function applyFilter() {
        const activeCat = document.querySelector('.cat-btn.active');
        const cat = activeCat ? activeCat.dataset.cat : 'all';
        document.querySelectorAll('.shop-card').forEach(card => {
          card.style.display = (cat === 'all' || card.dataset.category === cat) ? '' : 'none';
        });
      }

      catBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          catBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          applyFilter();
        });
      });

      function loadTechProducts() {
        if (!window.db) { setTimeout(loadTechProducts, 300); return; }
        window.db.collection('tech_products').orderBy('timestamp', 'desc').get().then(snap => {
          if (snap.empty) return; // keep any hardcoded fallback cards
          // Clear hardcoded items and replace with live data
          grid.innerHTML = '';
          snap.docs.forEach(doc => {
            const p = { id: doc.id, ...doc.data() };
            const statusUp = (p.status || 'IN STOCK').toUpperCase();
            const isSold = statusUp === 'SOLD';
            const badgeText = p.status || 'In Stock';
            const badgeColor = isSold ? '#ff4a4a' : '#D4AF37';
            const waText = encodeURIComponent('Hello REEL Tech Hub, I want to inquire about: ' + (p.name || p.title || ''));
            const card = document.createElement('div');
            card.className = 'shop-card';
            card.dataset.category = p.category || 'General';
            card.innerHTML = `
              <div class="shop-card-img-wrap">
                <span class="shop-badge" style="background:${badgeColor};">${badgeText}</span>
                ${p.image ? `<img src="${p.image}" alt="${p.name || ''}" loading="lazy" style="object-fit:${p.imageFit || 'cover'};width:100%;height:100%;">` : '<div style="width:100%;height:220px;background:rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:center;color:#D4AF37;font-size:2rem;">📦</div>'}
              </div>
              <div class="shop-card-body">
                <div class="shop-card-cat">${p.category || 'Product'}</div>
                <h3 class="shop-card-title">${p.name || p.title || 'Untitled'}</h3>
                ${p.specs ? `<p class="shop-card-specs">${p.specs}</p>` : (p.description ? `<p class="shop-card-specs">${p.description}</p>` : '')}
                <div class="shop-card-footer">
                  <div class="shop-price">${p.price || ''}${p.originalPrice ? ` <span>${p.originalPrice}</span>` : ''}</div>
                  ${!isSold ? `<a href="https://wa.me/2348067029444?text=${waText}" target="_blank" rel="noopener" class="btn-buy-wa">
                    <i class="fa-brands fa-whatsapp"></i> Inquire
                  </a>` : `<span style="color:#ff4a4a;font-weight:700;font-size:0.85rem;">SOLD</span>`}
                </div>
              </div>
            `;
            grid.appendChild(card);
          });
          applyFilter();
        }).catch(err => console.error('Tech products load error:', err));
      }
      loadTechProducts();
    });
  </script>"""

with open('reel-tech-hub/shop.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Insert Firebase scripts before the existing </head> or before <script src="js/main.js
if FIREBASE_SCRIPTS not in text:
    # inject before the category filter script
    inject_before = '<script src="js/main.js?v=4">'
    if inject_before in text:
        text = text.replace(inject_before, FIREBASE_SCRIPTS + '\n  ' + inject_before, 1)
        print("FIX 2a OK: Firebase scripts added to shop.html")
    else:
        print("FIX 2a SKIP: Could not find injection point in shop.html")
else:
    print("FIX 2a SKIP: Firebase already in shop.html")

# Inject the Firebase loader script after the existing category filter script's </script>
# Find the last </script> before </body>
body_pos = text.rfind('</body>')
last_script_end = text.rfind('</script>', 0, body_pos)
if last_script_end != -1 and TECH_FIREBASE_LOADER not in text:
    text = text[:last_script_end + 9] + TECH_FIREBASE_LOADER + text[last_script_end + 9:]
    print("FIX 2b OK: Firebase product loader added to shop.html")
elif TECH_FIREBASE_LOADER in text:
    print("FIX 2b SKIP: Loader already in shop.html")
else:
    print("FIX 2b SKIP: Could not inject loader")

with open('reel-tech-hub/shop.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

# ══════════════════════════════════════════════════════════════════════
# FIX 3: reel-auto-center.html — Add car listings section with Firebase loading
# ══════════════════════════════════════════════════════════════════════
AUTO_FIREBASE_SCRIPTS = """  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>
  <script src="js/firebase-init.js"></script>"""

AUTO_SECTION_HTML = """
<!-- ===================== REEL AUTO CAR LISTINGS ===================== -->
<section class="section" id="car-listings" style="padding-top:0; display:none;">
  <div class="container">
    <header class="section-header reveal-up text-center" style="margin-bottom:36px;">
      <div class="section-eyebrow">Available Now</div>
      <h2 class="section-heading">Our <span class="gold-text">Car Listings</span></h2>
      <div class="gold-rule center-rule"></div>
      <p class="section-desc">Browse our current inventory of executive vehicles.</p>
    </header>
    <div id="auto-cars-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:28px;"></div>
  </div>
</section>"""

AUTO_LOADER_SCRIPT = """
  <script>
    (function() {
      function loadAutoCars() {
        if (!window.db) { setTimeout(loadAutoCars, 300); return; }
        window.db.collection('auto_cars').orderBy('timestamp', 'desc').get().then(snap => {
          if (snap.empty) return;
          const section = document.getElementById('car-listings');
          const grid = document.getElementById('auto-cars-grid');
          if (!section || !grid) return;
          section.style.display = '';
          grid.innerHTML = '';
          snap.docs.forEach(doc => {
            const c = { id: doc.id, ...doc.data() };
            const statusUp = (c.status || 'AVAILABLE').toUpperCase();
            const isSold = statusUp === 'SOLD';
            const isUnderOffer = statusUp === 'UNDER OFFER' || statusUp === 'UNDEROFFER';
            const badgeText = c.status || 'Available';
            const badgeColor = isSold ? '#ff4a4a' : (isUnderOffer ? '#D4AF37' : '#4ade80');
            const badgeBg = isSold ? 'rgba(255,74,74,0.15)' : (isUnderOffer ? 'rgba(212,175,55,0.15)' : 'rgba(74,222,128,0.15)');
            const waText = encodeURIComponent('Hello REEL Auto Centre, I want to inquire about: ' + (c.name || c.title || ''));
            const div = document.createElement('div');
            div.style.cssText = 'background:rgba(255,255,255,0.03);border:1px solid rgba(212,175,55,0.15);border-radius:16px;overflow:hidden;transition:border-color .2s,transform .2s;';
            div.onmouseenter = function(){ this.style.borderColor='rgba(212,175,55,0.5)'; this.style.transform='translateY(-4px)'; };
            div.onmouseleave = function(){ this.style.borderColor='rgba(212,175,55,0.15)'; this.style.transform=''; };
            div.innerHTML = `
              <div style="position:relative;overflow:hidden;${c.imageFit === '16-9' || c.imageFit === '16-9-crop' ? 'aspect-ratio:16/9;' : 'height:220px;'}">
                <span style="position:absolute;top:12px;left:12px;z-index:2;padding:4px 12px;border-radius:20px;font-size:0.72rem;font-weight:700;text-transform:uppercase;background:${badgeBg};color:${badgeColor};border:1px solid ${badgeColor};">${badgeText}</span>
                ${c.image ? `<img src="${c.image}" alt="${c.name||''}" loading="lazy" style="width:100%;height:100%;object-fit:${c.imageFit==='contain'?'contain':'cover'};">` : '<div style="width:100%;height:100%;background:rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:center;color:#D4AF37;font-size:3rem;">🚗</div>'}
              </div>
              <div style="padding:20px;">
                <div style="font-size:0.75rem;color:var(--gold,#D4AF37);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">${c.category || 'Vehicle'}</div>
                <h3 style="font-size:1.1rem;font-weight:700;color:#fff;margin:0 0 8px;">${c.name || c.title || 'Vehicle'}</h3>
                ${c.yearMileage ? `<div style="font-size:0.8rem;color:rgba(255,255,255,0.5);margin-bottom:8px;">${c.yearMileage}</div>` : ''}
                ${c.specs ? `<p style="font-size:0.82rem;color:rgba(255,255,255,0.6);line-height:1.6;margin:0 0 16px;">${c.specs}</p>` : ''}
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                  <div style="font-size:1.1rem;font-weight:700;color:var(--gold,#D4AF37);">${c.price || ''}</div>
                  ${!isSold ? `<a href="https://wa.me/2348067029444?text=${waText}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:8px;background:rgba(37,211,102,0.1);border:1px solid rgba(37,211,102,0.4);color:#25D366;font-size:0.82rem;font-weight:600;text-decoration:none;"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.136.564 4.14 1.547 5.874L.057 23.882a.5.5 0 0 0 .613.613l6.008-1.49A11.94 11.94 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.969 0-3.806-.541-5.378-1.479l-.385-.234-3.991.99.99-3.991-.234-.385A9.956 9.956 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg> Inquire on WhatsApp</a>` : `<span style="color:#ff4a4a;font-weight:700;">SOLD</span>`}
                </div>
              </div>`;
            grid.appendChild(div);
          });
        }).catch(err => console.error('Auto cars load error:', err));
      }
      loadAutoCars();
    })();
  </script>"""

with open('reel-auto-center.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add Firebase scripts if not present
if 'firebase-init.js' not in text:
    inject_before_main = '<script src="js/main.js?v=12">'
    if inject_before_main in text:
        text = text.replace(inject_before_main, AUTO_FIREBASE_SCRIPTS + '\n  ' + inject_before_main, 1)
        print("FIX 3a OK: Firebase scripts added to reel-auto-center.html")
    else:
        print("FIX 3a SKIP: main.js injection point not found")
else:
    print("FIX 3a SKIP: Firebase already present")

# Add the car listings section right before the "WHAT WE OFFER" section
inject_before_offers = '<!-- WHAT WE OFFER -->'
if 'car-listings' not in text and inject_before_offers in text:
    text = text.replace(inject_before_offers, AUTO_SECTION_HTML + '\n\n' + inject_before_offers, 1)
    print("FIX 3b OK: Car listings section added to reel-auto-center.html")
elif 'car-listings' in text:
    print("FIX 3b SKIP: Car listings section already in reel-auto-center.html")
else:
    print("FIX 3b SKIP: Injection point not found")

# Add loader script before </body>
if 'loadAutoCars' not in text:
    text = text.replace('</body>', AUTO_LOADER_SCRIPT + '\n</body>', 1)
    print("FIX 3c OK: Auto loader script injected")
else:
    print("FIX 3c SKIP: Auto loader already present")

with open('reel-auto-center.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

# ══════════════════════════════════════════════════════════════════════
# FIX 4: reel-global-palace.html — Add services section with Firebase loading
# ══════════════════════════════════════════════════════════════════════
PALACE_FIREBASE_SCRIPTS = """  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>
  <script src="js/firebase-init.js"></script>"""

PALACE_SECTION_HTML = """
<!-- ===================== REEL GLOBAL PALACE SERVICE LISTINGS ===================== -->
<section class="section" id="palace-listings" style="padding-top:0; display:none;">
  <div class="container">
    <header class="section-header reveal-up text-center" style="margin-bottom:36px;">
      <div class="section-eyebrow">Our Offerings</div>
      <h2 class="section-heading">Premium <span class="gold-text">Services & Products</span></h2>
      <div class="gold-rule center-rule"></div>
      <p class="section-desc">Explore our curated range of luxury lifestyle services and products.</p>
    </header>
    <div id="palace-services-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:28px;"></div>
  </div>
</section>"""

PALACE_LOADER_SCRIPT = """
  <script>
    (function() {
      function loadPalaceServices() {
        if (!window.db) { setTimeout(loadPalaceServices, 300); return; }
        window.db.collection('palace_services').orderBy('timestamp', 'desc').get().then(snap => {
          if (snap.empty) return;
          const section = document.getElementById('palace-listings');
          const grid = document.getElementById('palace-services-grid');
          if (!section || !grid) return;
          section.style.display = '';
          grid.innerHTML = '';
          snap.docs.forEach(doc => {
            const s = { id: doc.id, ...doc.data() };
            const statusUp = (s.status || 'AVAILABLE').toUpperCase();
            const isBooked = statusUp === 'BOOKED';
            const badgeText = s.status || 'Available';
            const badgeColor = isBooked ? '#D4AF37' : '#4ade80';
            const badgeBg = isBooked ? 'rgba(212,175,55,0.15)' : 'rgba(74,222,128,0.15)';
            const waText = encodeURIComponent('Hello REEL Global Palace, I want to inquire about: ' + (s.name || s.title || ''));
            const div = document.createElement('div');
            div.style.cssText = 'background:rgba(255,255,255,0.03);border:1px solid rgba(212,175,55,0.15);border-radius:16px;overflow:hidden;transition:border-color .2s,transform .2s;';
            div.onmouseenter = function(){ this.style.borderColor='rgba(212,175,55,0.5)'; this.style.transform='translateY(-4px)'; };
            div.onmouseleave = function(){ this.style.borderColor='rgba(212,175,55,0.15)'; this.style.transform=''; };
            div.innerHTML = `
              <div style="position:relative;overflow:hidden;${s.imageFit === '16-9' || s.imageFit === '16-9-crop' ? 'aspect-ratio:16/9;' : 'height:200px;'}">
                <span style="position:absolute;top:12px;left:12px;z-index:2;padding:4px 12px;border-radius:20px;font-size:0.72rem;font-weight:700;text-transform:uppercase;background:${badgeBg};color:${badgeColor};border:1px solid ${badgeColor};">${badgeText}</span>
                ${s.image ? `<img src="${s.image}" alt="${s.name||''}" loading="lazy" style="width:100%;height:100%;object-fit:${s.imageFit==='contain'?'contain':'cover'};">` : '<div style="width:100%;height:100%;background:rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:center;color:#D4AF37;font-size:3rem;">✨</div>'}
              </div>
              <div style="padding:20px;">
                <div style="font-size:0.75rem;color:var(--gold,#D4AF37);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">${s.category || 'Service'}</div>
                <h3 style="font-size:1.05rem;font-weight:700;color:#fff;margin:0 0 8px;">${s.name || s.title || 'Service'}</h3>
                ${s.duration ? `<div style="font-size:0.78rem;color:rgba(255,255,255,0.45);margin-bottom:8px;">⏱ ${s.duration}</div>` : ''}
                ${s.description ? `<p style="font-size:0.82rem;color:rgba(255,255,255,0.6);line-height:1.6;margin:0 0 16px;">${s.description}</p>` : ''}
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                  <div style="font-size:1.05rem;font-weight:700;color:var(--gold,#D4AF37);">${s.price || ''}</div>
                  <a href="https://wa.me/2348067029444?text=${waText}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:8px;background:rgba(37,211,102,0.1);border:1px solid rgba(37,211,102,0.4);color:#25D366;font-size:0.82rem;font-weight:600;text-decoration:none;"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.136.564 4.14 1.547 5.874L.057 23.882a.5.5 0 0 0 .613.613l6.008-1.49A11.94 11.94 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.969 0-3.806-.541-5.378-1.479l-.385-.234-3.991.99.99-3.991-.234-.385A9.956 9.956 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg> Book / Inquire</a>
                </div>
              </div>`;
            grid.appendChild(div);
          });
        }).catch(err => console.error('Palace services load error:', err));
      }
      loadPalaceServices();
    })();
  </script>"""

with open('reel-global-palace.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add Firebase scripts if not present
if 'firebase-init.js' not in text:
    inject_before_main = '<script src="js/main.js?v=12">'
    if inject_before_main in text:
        text = text.replace(inject_before_main, PALACE_FIREBASE_SCRIPTS + '\n  ' + inject_before_main, 1)
        print("FIX 4a OK: Firebase scripts added to reel-global-palace.html")
    else:
        print("FIX 4a SKIP: main.js injection point not found")
else:
    print("FIX 4a SKIP: Firebase already present")

# Add listings section right before "WHAT WE OFFER" section
palace_inject_before = '<!-- WHAT WE OFFER -->'
if 'palace-listings' not in text and palace_inject_before in text:
    text = text.replace(palace_inject_before, PALACE_SECTION_HTML + '\n\n' + palace_inject_before, 1)
    print("FIX 4b OK: Palace listings section added")
elif 'palace-listings' in text:
    print("FIX 4b SKIP: Palace listings already present")
else:
    print("FIX 4b SKIP: Injection point not found")

# Add loader script before </body>
if 'loadPalaceServices' not in text:
    text = text.replace('</body>', PALACE_LOADER_SCRIPT + '\n</body>', 1)
    print("FIX 4c OK: Palace loader script injected")
else:
    print("FIX 4c SKIP: Palace loader already present")

with open('reel-global-palace.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("\nAll fixes done.")

