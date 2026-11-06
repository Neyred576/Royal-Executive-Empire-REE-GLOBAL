import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open('admin/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

original_text = text

# ─────────────────────────────────────────────────────────
# PATCH 1: Add global arrays for the 3 new divisions
# after "let brands = [];"
# ─────────────────────────────────────────────────────────
OLD_ARRAYS = "    let brands = [];"
NEW_ARRAYS = """    let brands = [];
    let techProducts = [];
    let palaceServices = [];
    let autoCars = [];"""
text = text.replace(OLD_ARRAYS, NEW_ARRAYS, 1)

# ─────────────────────────────────────────────────────────
# PATCH 2: Extend loadData() — add 3 new Firestore queries
# Replace the Promise.all block to include new collections
# ─────────────────────────────────────────────────────────
OLD_PROMISE = """        const [blogSnap, propSnap, powerSnap, shopSnap, msgSnap, orderSnap, brandSnap] = await Promise.all([
          window.db.collection('blogs').orderBy('timestamp', 'desc').get(),
          window.db.collection('properties').orderBy('timestamp', 'desc').get(),
          window.db.collection('power_products').orderBy('timestamp', 'desc').get(),
          window.db.collection('products').get(),
          window.db.collection('messages').orderBy('timestamp', 'desc').get(),
          window.db.collection('orders').orderBy('timestamp', 'desc').get(),
          window.db.collection('brands').orderBy('timestamp', 'desc').get()
        ]);"""
NEW_PROMISE = """        const [blogSnap, propSnap, powerSnap, shopSnap, msgSnap, orderSnap, brandSnap, techSnap, palaceSnap, autoSnap] = await Promise.all([
          window.db.collection('blogs').orderBy('timestamp', 'desc').get(),
          window.db.collection('properties').orderBy('timestamp', 'desc').get(),
          window.db.collection('power_products').orderBy('timestamp', 'desc').get(),
          window.db.collection('products').get(),
          window.db.collection('messages').orderBy('timestamp', 'desc').get(),
          window.db.collection('orders').orderBy('timestamp', 'desc').get(),
          window.db.collection('brands').orderBy('timestamp', 'desc').get(),
          window.db.collection('tech_products').orderBy('timestamp', 'desc').get(),
          window.db.collection('palace_services').orderBy('timestamp', 'desc').get(),
          window.db.collection('auto_cars').orderBy('timestamp', 'desc').get()
        ]);"""
text = text.replace(OLD_PROMISE, NEW_PROMISE, 1)

# ─────────────────────────────────────────────────────────
# PATCH 3: Populate arrays for new collections and render
# After: brands.length = 0; brands.push(...)
# ─────────────────────────────────────────────────────────
OLD_BRANDS_PUSH = "        brands.length = 0; brands.push(...brandSnap.docs.map(d => ({ id: d.id, ...d.data() })));"
NEW_BRANDS_PUSH = """        brands.length = 0; brands.push(...brandSnap.docs.map(d => ({ id: d.id, ...d.data() })));
        techProducts.length = 0; techProducts.push(...techSnap.docs.map(d => ({ id: d.id, ...d.data() })));
        palaceServices.length = 0; palaceServices.push(...palaceSnap.docs.map(d => ({ id: d.id, ...d.data() })));
        autoCars.length = 0; autoCars.push(...autoSnap.docs.map(d => ({ id: d.id, ...d.data() })));"""
text = text.replace(OLD_BRANDS_PUSH, NEW_BRANDS_PUSH, 1)

# ─────────────────────────────────────────────────────────
# PATCH 4: Add renderList calls for the 3 new divisions
# After: renderList(brands, 'brands-list', 'brand', 'brands');
# ─────────────────────────────────────────────────────────
OLD_RENDER_BRANDS = "        renderList(brands, 'brands-list', 'brand', 'brands');"
NEW_RENDER_BRANDS = """        renderList(brands, 'brands-list', 'brand', 'brands');
        renderList(techProducts, 'tech-products-list', 'tech_product', 'tech_products');
        renderList(palaceServices, 'palace-services-list', 'palace_service', 'palace_services');
        renderList(autoCars, 'auto-cars-list', 'auto_car', 'auto_cars');

        // Update division count badges
        const techCountEl = document.getElementById('tech-catalog-count');
        if (techCountEl) techCountEl.textContent = techProducts.length;
        const palaceCountEl = document.getElementById('palace-services-count');
        if (palaceCountEl) palaceCountEl.textContent = palaceServices.length;
        const autoCountEl = document.getElementById('auto-cars-count');
        if (autoCountEl) autoCountEl.textContent = autoCars.length;"""
text = text.replace(OLD_RENDER_BRANDS, NEW_RENDER_BRANDS, 1)

# ─────────────────────────────────────────────────────────
# PATCH 5: Extend allowedTypes in renderList to include new types
# ─────────────────────────────────────────────────────────
OLD_ALLOWED = "        const allowedTypes = ['blog', 'property', 'power_product', 'product', 'brand'];"
NEW_ALLOWED = "        const allowedTypes = ['blog', 'property', 'power_product', 'product', 'brand', 'tech_product', 'palace_service', 'auto_car'];"
text = text.replace(OLD_ALLOWED, NEW_ALLOWED, 1)

# ─────────────────────────────────────────────────────────
# PATCH 6: Update sub text in renderList to include status badge for new types
# Replace the div.innerHTML template to show status badge when present
# ─────────────────────────────────────────────────────────
OLD_DIV_HTML = """        div.innerHTML = `
          <div class="item-thumb">${imgSrc ? `<img src="${imgSrc}" alt="" decoding="async" loading="lazy">` : '📋'}</div>
          <div class="item-info">
            <strong>${title}</strong>
            <span>${sub}</span>
          </div>
          ${editBtnHtml}
          <button class="btn-delete" data-id="${item.id}" data-idx="${idx}" data-type="${type}" data-col="${collectionName}">"""
NEW_DIV_HTML = """        // Build status badge for divisions
        const statusBadgeMap = {
          'AVAILABLE': 'badge-available',
          'IN STOCK': 'badge-available',
          'UNDER OFFER': 'badge-underoffer',
          'UNDEROFFER': 'badge-underoffer',
          'BOOKED': 'badge-underoffer',
          'SOLD': 'badge-sold',
          'OUT OF STOCK': 'badge-sold'
        };
        const statusVal = item.status ? item.status.toUpperCase() : '';
        const badgeClass = statusBadgeMap[statusVal] || '';
        const statusBadge = badgeClass ? `<span class="badge-status ${badgeClass}">${item.status}</span>` : '';
        div.innerHTML = `
          <div class="item-thumb">${imgSrc ? `<img src="${imgSrc}" alt="" decoding="async" loading="lazy" style="object-fit:${item.imageFit||'cover'};width:100%;height:100%;">` : '📋'}</div>
          <div class="item-info">
            <strong>${title}</strong>
            <span>${item.price ? item.price : sub} ${statusBadge}</span>
          </div>
          ${editBtnHtml}
          <button class="btn-delete" data-id="${item.id}" data-idx="${idx}" data-type="${type}" data-col="${collectionName}">"""
text = text.replace(OLD_DIV_HTML, NEW_DIV_HTML, 1)

# ─────────────────────────────────────────────────────────
# PATCH 7: Add edit handlers for tech_product, palace_service, auto_car
# After the brand edit handler block (after `else if (itemType === 'brand') {`)
# ─────────────────────────────────────────────────────────
OLD_BRAND_EDIT_END = """          else if (itemType === 'brand') {
            switchSection('sec-brands');
            document.getElementById('brand-name').value = itemData.name || '';
            document.getElementById('brand-sector').value = itemData.sector || '';
            document.getElementById('brand-link').value = itemData.link || '';
            const blogLink = document.getElementById('brand-blog-link');
            if (blogLink) blogLink.value = itemData.linkedBlogId || '';
            const statusEl = document.getElementById('brand-status');
            if (statusEl) statusEl.value = itemData.status || 'published';

            const form = document.getElementById('form-brands');
            form.dataset.editId = id;
            form.dataset.editImage = itemData.image || '';
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.innerHTML = 'Update Brand';
          }

          window.scrollTo({ top: 0, behavior: 'smooth' });"""
NEW_BRAND_EDIT_END = """          else if (itemType === 'brand') {
            switchSection('sec-brands');
            document.getElementById('brand-name').value = itemData.name || '';
            document.getElementById('brand-sector').value = itemData.sector || '';
            document.getElementById('brand-link').value = itemData.link || '';
            const blogLink = document.getElementById('brand-blog-link');
            if (blogLink) blogLink.value = itemData.linkedBlogId || '';
            const statusEl = document.getElementById('brand-status');
            if (statusEl) statusEl.value = itemData.status || 'published';

            const form = document.getElementById('form-brands');
            form.dataset.editId = id;
            form.dataset.editImage = itemData.image || '';
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.innerHTML = 'Update Brand';
          }

          // ── REEL TECH HUB Edit ──
          else if (itemType === 'tech_product') {
            switchSection('sec-tech-hub');
            document.getElementById('tech-prod-name').value = itemData.name || itemData.title || '';
            const catEl = document.getElementById('tech-prod-cat');
            if (catEl) catEl.value = itemData.category || itemData.cat || '';
            document.getElementById('tech-prod-price').value = itemData.price || '';
            const origPriceEl = document.getElementById('tech-prod-orig-price');
            if (origPriceEl) origPriceEl.value = itemData.originalPrice || '';
            const statusEl = document.getElementById('tech-prod-status');
            if (statusEl) statusEl.value = itemData.status || 'IN STOCK';
            const specsEl = document.getElementById('tech-prod-specs');
            if (specsEl) specsEl.value = itemData.specs || '';
            const descEl = document.getElementById('tech-prod-desc');
            if (descEl) descEl.value = itemData.description || itemData.desc || '';
            const fitEl = document.getElementById('tech-prod-image-fit');
            if (fitEl) { fitEl.value = itemData.imageFit || 'contain'; fitEl.dispatchEvent(new Event('change')); }
            // Show preview with existing image
            if (itemData.image) {
              const prevImg = document.getElementById('tech-preview-img');
              const prevBox = document.getElementById('tech-preview-box');
              if (prevImg && prevBox) { prevImg.src = itemData.image; prevBox.style.display = 'block'; }
            }
            const imgInput = document.getElementById('tech-prod-img');
            if (imgInput) imgInput.removeAttribute('required');
            const cancelBtn = document.getElementById('btn-cancel-tech');
            if (cancelBtn) cancelBtn.style.display = '';
            const form = document.getElementById('form-tech-product');
            form.dataset.editId = id;
            form.dataset.editImage = itemData.image || '';
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.innerHTML = 'Update Product';
          }

          // ── REEL GLOBAL PALACE Edit ──
          else if (itemType === 'palace_service') {
            switchSection('sec-global-palace');
            document.getElementById('palace-service-name').value = itemData.name || itemData.title || '';
            const catEl = document.getElementById('palace-service-cat');
            if (catEl) catEl.value = itemData.category || itemData.cat || '';
            document.getElementById('palace-service-price').value = itemData.price || '';
            const durEl = document.getElementById('palace-service-duration');
            if (durEl) durEl.value = itemData.duration || '';
            const statusEl = document.getElementById('palace-service-status');
            if (statusEl) statusEl.value = itemData.status || 'AVAILABLE';
            const descEl = document.getElementById('palace-service-desc');
            if (descEl) descEl.value = itemData.description || itemData.desc || '';
            const fitEl = document.getElementById('palace-service-image-fit');
            if (fitEl) { fitEl.value = itemData.imageFit || 'contain'; fitEl.dispatchEvent(new Event('change')); }
            if (itemData.image) {
              const prevImg = document.getElementById('palace-preview-img');
              const prevBox = document.getElementById('palace-preview-box');
              if (prevImg && prevBox) { prevImg.src = itemData.image; prevBox.style.display = 'block'; }
            }
            const imgInput = document.getElementById('palace-service-img');
            if (imgInput) imgInput.removeAttribute('required');
            const cancelBtn = document.getElementById('btn-cancel-palace');
            if (cancelBtn) cancelBtn.style.display = '';
            const form = document.getElementById('form-palace-service');
            form.dataset.editId = id;
            form.dataset.editImage = itemData.image || '';
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.innerHTML = 'Update Service';
          }

          // ── REEL AUTO CENTRE Edit ──
          else if (itemType === 'auto_car') {
            switchSection('sec-auto-centre');
            document.getElementById('auto-car-name').value = itemData.name || itemData.title || '';
            const catEl = document.getElementById('auto-car-cat');
            if (catEl) catEl.value = itemData.category || itemData.cat || '';
            document.getElementById('auto-car-price').value = itemData.price || '';
            const ymEl = document.getElementById('auto-car-year-mileage');
            if (ymEl) ymEl.value = itemData.yearMileage || itemData.year || '';
            const statusEl = document.getElementById('auto-car-status');
            if (statusEl) statusEl.value = itemData.status || 'AVAILABLE';
            const specsEl = document.getElementById('auto-car-specs');
            if (specsEl) specsEl.value = itemData.specs || '';
            const descEl = document.getElementById('auto-car-desc');
            if (descEl) descEl.value = itemData.description || itemData.desc || '';
            const fitEl = document.getElementById('auto-car-image-fit');
            if (fitEl) { fitEl.value = itemData.imageFit || 'contain'; fitEl.dispatchEvent(new Event('change')); }
            if (itemData.image) {
              const prevImg = document.getElementById('auto-preview-img');
              const prevBox = document.getElementById('auto-preview-box');
              if (prevImg && prevBox) { prevImg.src = itemData.image; prevBox.style.display = 'block'; }
            }
            const imgInput = document.getElementById('auto-car-img');
            if (imgInput) imgInput.removeAttribute('required');
            const cancelBtn = document.getElementById('btn-cancel-auto');
            if (cancelBtn) cancelBtn.style.display = '';
            const form = document.getElementById('form-auto-car');
            form.dataset.editId = id;
            form.dataset.editImage = itemData.image || '';
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.innerHTML = 'Update Car';
          }

          window.scrollTo({ top: 0, behavior: 'smooth' });"""
text = text.replace(OLD_BRAND_EDIT_END, NEW_BRAND_EDIT_END, 1)

# ─────────────────────────────────────────────────────────
# PATCH 8: Extend delete handler in renderList
# Replace the broken partial delete handler after the delete comment
# ─────────────────────────────────────────────────────────
OLD_DELETE_HANDLERS = """            if (t === 'blog')       { blogs.splice(i,1); renderList(blogs, 'blog-list', 'blog', col); }
            if (t === 'portfolio') // Using 'portfolio' collection for REEL Properties  { portfolio.splice(i,1); renderL
            if (t === 'product')    { products.splice(i,1); renderList(products, 'product-list', 'product', col); }"""
NEW_DELETE_HANDLERS = """            if (t === 'blog')           { blogs.splice(i,1); renderList(blogs, 'blog-list', 'blog', col); }
            if (t === 'property')       { properties.splice(i,1); renderList(properties, 'prop-list', 'property', col); }
            if (t === 'power_product')  { powerProducts.splice(i,1); renderList(powerProducts, 'power-list', 'power_product', col); }
            if (t === 'product')        { products.splice(i,1); renderList(products, 'product-list', 'product', col); }
            if (t === 'brand')          { brands.splice(i,1); renderList(brands, 'brands-list', 'brand', col); }
            if (t === 'tech_product')   { techProducts.splice(i,1); renderList(techProducts, 'tech-products-list', 'tech_product', col); const el = document.getElementById('tech-catalog-count'); if(el) el.textContent = techProducts.length; }
            if (t === 'palace_service') { palaceServices.splice(i,1); renderList(palaceServices, 'palace-services-list', 'palace_service', col); const el = document.getElementById('palace-services-count'); if(el) el.textContent = palaceServices.length; }
            if (t === 'auto_car')       { autoCars.splice(i,1); renderList(autoCars, 'auto-cars-list', 'auto_car', col); const el = document.getElementById('auto-cars-count'); if(el) el.textContent = autoCars.length; }"""
text = text.replace(OLD_DELETE_HANDLERS, NEW_DELETE_HANDLERS, 1)

# ─────────────────────────────────────────────────────────
# PATCH 9: Fix prop-status values in the edit handler
# Change 'published' default to 'AVAILABLE'
# ─────────────────────────────────────────────────────────
OLD_PROP_STATUS = "            if (statusEl) statusEl.value = itemData.status || 'published';\n            const fitEl = document.getElementById('prop-image-fit');"
NEW_PROP_STATUS = "            if (statusEl) statusEl.value = itemData.status || 'AVAILABLE';\n            const fitEl = document.getElementById('prop-image-fit');"
text = text.replace(OLD_PROP_STATUS, NEW_PROP_STATUS, 1)

# ─────────────────────────────────────────────────────────
# PATCH 10: Fix prop-status validation (remove 'scheduled' check for properties)
# and fix the status values to match AVAILABLE/UNDER OFFER/SOLD
# ─────────────────────────────────────────────────────────
OLD_PROP_SUBMIT_STATUS = """        const statusVal = document.getElementById('prop-status').value;
        if (statusVal === 'scheduled' && !pendingScheduleTime) {
          showToast('Error', 'Please set a schedule date & time before saving.', 'delete');
          return;
        }

        const btn = propForm.querySelector('button[type="submit"]');"""
NEW_PROP_SUBMIT_STATUS = """        const statusVal = document.getElementById('prop-status').value;

        const btn = propForm.querySelector('button[type="submit"]');"""
text = text.replace(OLD_PROP_SUBMIT_STATUS, NEW_PROP_SUBMIT_STATUS, 1)

# ─────────────────────────────────────────────────────────
# PATCH 11: Fix prop payload - remove scheduleTime
# ─────────────────────────────────────────────────────────
OLD_PROP_PAYLOAD = """            imageFit: fitMode,
            status: statusVal,
            scheduleTime: statusVal === 'scheduled' ? pendingScheduleTime : null,
            timestamp: firebase.firestore.FieldValue.serverTimestamp()
          };

          if (editId) {
            await window.db.collection('properties').doc(editId).update(payload);"""
NEW_PROP_PAYLOAD = """            imageFit: fitMode,
            status: statusVal,
            timestamp: firebase.firestore.FieldValue.serverTimestamp()
          };

          if (editId) {
            await window.db.collection('properties').doc(editId).update(payload);"""
text = text.replace(OLD_PROP_PAYLOAD, NEW_PROP_PAYLOAD, 1)

# ─────────────────────────────────────────────────────────
# PATCH 12: Add cancel edit for property
# After: renderList(properties, 'prop-list', 'property', 'properties');  [inside loadData render call]
# ─────────────────────────────────────────────────────────

# Add cancel functions right before the Properties Form Handler section
OLD_CANCEL_MARKER = "    // ── Properties Form Handler (with redirect to REEL Properties page) ──"
NEW_CANCEL_MARKER = """    // ── Cancel Edit Helpers ──
    window.cancelPropEdit = function() {
      const form = document.getElementById('form-properties');
      if (form) { delete form.dataset.editId; delete form.dataset.editImage; delete form.dataset.editImages; form.reset(); }
      const imgInput = document.getElementById('prop-img');
      if (imgInput) imgInput.setAttribute('required', 'required');
      const sb = form && form.querySelector('button[type="submit"]');
      if (sb) sb.innerHTML = 'Add Property';
      const prevBox = document.getElementById('prop-preview-box');
      if (prevBox) prevBox.style.display = 'none';
      const cancelBtn = document.getElementById('btn-cancel-prop');
      if (cancelBtn) cancelBtn.style.display = 'none';
    };
    window.cancelTechEdit = function() {
      const form = document.getElementById('form-tech-product');
      if (form) { delete form.dataset.editId; delete form.dataset.editImage; form.reset(); }
      const imgInput = document.getElementById('tech-prod-img');
      if (imgInput) imgInput.setAttribute('required', 'required');
      const sb = form && form.querySelector('button[type="submit"]');
      if (sb) sb.innerHTML = 'Add Product';
      const prevBox = document.getElementById('tech-preview-box');
      if (prevBox) prevBox.style.display = 'none';
      const cancelBtn = document.getElementById('btn-cancel-tech');
      if (cancelBtn) cancelBtn.style.display = 'none';
    };
    window.cancelPalaceEdit = function() {
      const form = document.getElementById('form-palace-service');
      if (form) { delete form.dataset.editId; delete form.dataset.editImage; form.reset(); }
      const imgInput = document.getElementById('palace-service-img');
      if (imgInput) imgInput.setAttribute('required', 'required');
      const sb = form && form.querySelector('button[type="submit"]');
      if (sb) sb.innerHTML = 'Add Service';
      const prevBox = document.getElementById('palace-preview-box');
      if (prevBox) prevBox.style.display = 'none';
      const cancelBtn = document.getElementById('btn-cancel-palace');
      if (cancelBtn) cancelBtn.style.display = 'none';
    };
    window.cancelAutoEdit = function() {
      const form = document.getElementById('form-auto-car');
      if (form) { delete form.dataset.editId; delete form.dataset.editImage; form.reset(); }
      const imgInput = document.getElementById('auto-car-img');
      if (imgInput) imgInput.setAttribute('required', 'required');
      const sb = form && form.querySelector('button[type="submit"]');
      if (sb) sb.innerHTML = 'Add Car';
      const prevBox = document.getElementById('auto-preview-box');
      if (prevBox) prevBox.style.display = 'none';
      const cancelBtn = document.getElementById('btn-cancel-auto');
      if (cancelBtn) cancelBtn.style.display = 'none';
    };

    // ── Properties Form Handler (with redirect to REEL Properties page) ──"""
text = text.replace(OLD_CANCEL_MARKER, NEW_CANCEL_MARKER, 1)

# ─────────────────────────────────────────────────────────
# PATCH 13: Remove the defaultTech block + renderTechProducts + setTimeout call
# Replace everything from "// 3. Render Tech Hub Default Products" to end of that block
# ─────────────────────────────────────────────────────────
OLD_DEFAULT_TECH = """      // 3. Render Tech Hub Default Products
      window.renderTechProducts = function() {
        const container = document.getElementById('tech-products-list');
        if (!container) return;
        const defaultTech = [
          { name: "Apple iPhone 15 Pro Max (256GB)", cat: "Mobile Phones", price: "₦1,850,000", badge: "Flagship" },
          { name: "Samsung Galaxy S24 Ultra 5G (512GB)", cat: "Mobile Phones", price: "₦1,920,000", badge: "Best Seller" },
          { name: "Google Pixel 8 Pro (256GB)", cat: "Mobile Phones", price: "₦1,250,000", badge: "In Stock" },
          { name: "Dell Latitude 5420 Enterprise Laptop", cat: "Laptops", price: "₦480,000", badge: "Best Seller" },
          { name: "HP EliteBook 840 G8 Executive Laptop", cat: "Laptops", price: "₦560,000", badge: "Corporate Grade" },
          { name: "Lenovo ThinkPad T14 Gen 2", cat: "Laptops", price: "₦520,000", badge: "Workhorse" },
          { name: "Dell Precision 5820 Tower Workstation", cat: "Workstations", price: "₦1,450,000", badge: "Powerhouse" },
          { name: "Dell PowerEdge R640 1U Rack Server", cat: "Servers & Network", price: "₦2,800,000", badge: "Enterprise" },
          { name: "Logitech MX Master 3S Performance Mouse", cat: "Accessories", price: "₦120,000", badge: "Must Have" }
        ];

        container.innerHTML = defaultTech.map((item, idx) => `
          <div style="display:flex; align-items:center; justify-content:space-between; padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex; align-items:center; gap:14px;">
              <span style="font-size:0.75rem; color:var(--w40); width:20px;">0${idx+1}</span>
              <div>
                <div style="font-size:0.9rem; font-weight:600; color:#fff;">${item.name}</div>
                <div style="font-size:0.75rem; color:var(--cyan); margin-top:2px;">${item.cat} &bull; <span style="color:var(--gold);">${item.badge}</span></div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:16px;">
              <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; color:var(--gold); font-size:0.95rem;">${item.price}</span>
              <a href="../reel-tech-hub/shop.html" target="_blank" style="padding:4px 10px; border-radius:6px; background:rgba(0,220,255,0.12); color:var(--cyan); font-size:0.78rem; text-decoration:none;">View</a>
            </div>
          </div>
        `).join('');
      };

      setTimeout(window.renderTechProducts, 600);"""
# Check if this exact string is in the file
if OLD_DEFAULT_TECH in text:
    text = text.replace(OLD_DEFAULT_TECH, "      // Tech Hub products are loaded from Firebase via loadData()", 1)
    print("Removed defaultTech block.")
else:
    # Try approximate match - find the block by anchor
    idx_start = text.find("// 3. Render Tech Hub Default Products")
    idx_end = text.find("setTimeout(window.renderTechProducts, 600);")
    if idx_start != -1 and idx_end != -1:
        old_block = text[idx_start:idx_end + len("setTimeout(window.renderTechProducts, 600);")]
        text = text.replace(old_block, "      // Tech Hub products are loaded from Firebase via loadData()", 1)
        print("Removed defaultTech block (approximate match).")
    else:
        print("WARNING: Could not find defaultTech block to remove.")

# ─────────────────────────────────────────────────────────
# PATCH 14: Inject Tech Hub, Palace, Auto form handlers
# Insert right before Broadcast Center Logic
# ─────────────────────────────────────────────────────────
OLD_BC_MARKER = "    // ── Broadcast Center Logic ──"
NEW_HANDLERS = """    // ── REEL TECH HUB Form Handler ──
    (() => {
      const techForm = document.getElementById('form-tech-product');
      if (!techForm) return;

      // Live fit preview for Tech Hub
      const updateTechPreview = () => {
        const fitSelect = document.getElementById('tech-prod-image-fit');
        const previewImg = document.getElementById('tech-preview-img');
        const previewFrame = document.getElementById('tech-preview-frame');
        const modeTag = document.getElementById('tech-preview-mode-tag');
        if (!fitSelect || !previewImg || !previewFrame) return;
        const val = fitSelect.value || 'contain';
        const label = fitSelect.options[fitSelect.selectedIndex]?.text || '';
        if (modeTag) modeTag.textContent = label.split('\u2014')[0].trim() || val;
        previewFrame.style.aspectRatio = '';
        previewFrame.style.height = '';
        previewImg.style.objectFit = 'contain';
        previewImg.style.height = 'auto';
        if (val === 'contain')       { previewFrame.style.height = '260px'; previewImg.style.objectFit = 'contain'; previewImg.style.maxHeight = '260px'; }
        else if (val === 'cover')    { previewFrame.style.height = '220px'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '16-9')     { previewFrame.style.aspectRatio = '16/9'; previewImg.style.objectFit = 'contain'; }
        else if (val === '16-9-crop'){ previewFrame.style.aspectRatio = '16/9'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '4-3')      { previewFrame.style.aspectRatio = '4/3'; previewImg.style.objectFit = 'contain'; }
        else if (val === '4-3-crop') { previewFrame.style.aspectRatio = '4/3'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '1-1')      { previewFrame.style.aspectRatio = '1/1'; previewImg.style.objectFit = 'contain'; }
        else if (val === '1-1-crop') { previewFrame.style.aspectRatio = '1/1'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
      };
      const techImgInput = document.getElementById('tech-prod-img');
      if (techImgInput) {
        techImgInput.addEventListener('change', (e) => {
          const file = e.target.files && e.target.files[0];
          if (file) {
            const reader = new FileReader();
            reader.onload = (evt) => {
              const prevImg = document.getElementById('tech-preview-img');
              const prevBox = document.getElementById('tech-preview-box');
              if (prevImg && prevBox) { prevImg.src = evt.target.result; prevBox.style.display = 'block'; updateTechPreview(); }
            };
            reader.readAsDataURL(file);
          }
        });
      }
      const techFitSelect = document.getElementById('tech-prod-image-fit');
      if (techFitSelect) techFitSelect.addEventListener('change', updateTechPreview);

      techForm.addEventListener('submit', async e => {
        e.preventDefault();
        const fileInput = document.getElementById('tech-prod-img');
        const files = Array.from(fileInput.files);
        const editId = techForm.dataset.editId;
        if (files.length === 0 && !editId) { showToast('No Image', 'Please select a product image.', 'delete'); return; }
        if (files.length > 5) { showToast('Error', 'Maximum 5 images allowed.', 'delete'); return; }

        const btn = techForm.querySelector('button[type="submit"]');
        const oldText = btn.innerHTML;
        btn.innerHTML = 'Uploading Image...';
        btn.disabled = true;

        try {
          let imageUrls = [];
          if (files.length > 0) {
            for (let file of files) {
              const url = await uploadOrCompressImage(file);
              if (url) imageUrls.push(url);
            }
          } else if (editId && techForm.dataset.editImage) {
            imageUrls.push(techForm.dataset.editImage);
          }

          btn.innerHTML = 'Saving...';
          const fitMode = document.getElementById('tech-prod-image-fit') ? document.getElementById('tech-prod-image-fit').value : 'contain';
          const payload = {
            name: document.getElementById('tech-prod-name').value.trim(),
            category: document.getElementById('tech-prod-cat') ? document.getElementById('tech-prod-cat').value.trim() : '',
            price: document.getElementById('tech-prod-price').value.trim(),
            originalPrice: document.getElementById('tech-prod-orig-price') ? document.getElementById('tech-prod-orig-price').value.trim() : '',
            status: document.getElementById('tech-prod-status').value,
            specs: document.getElementById('tech-prod-specs') ? document.getElementById('tech-prod-specs').value.trim() : '',
            description: document.getElementById('tech-prod-desc') ? document.getElementById('tech-prod-desc').value.trim() : '',
            image: imageUrls[0] || '',
            images: imageUrls,
            imageFit: fitMode,
            timestamp: firebase.firestore.FieldValue.serverTimestamp()
          };

          if (editId) {
            await window.db.collection('tech_products').doc(editId).update(payload);
            const idx = techProducts.findIndex(p => p.id === editId);
            if (idx !== -1) techProducts[idx] = { id: editId, ...payload };
            delete techForm.dataset.editId;
            delete techForm.dataset.editImage;
          } else {
            const docRef = await window.db.collection('tech_products').add(payload);
            techProducts.unshift({ id: docRef.id, ...payload });
          }

          renderList(techProducts, 'tech-products-list', 'tech_product', 'tech_products');
          const countEl = document.getElementById('tech-catalog-count');
          if (countEl) countEl.textContent = techProducts.length;
          showToast('Success!', editId ? 'Product updated!' : 'Product added to REEL TECH HUB!');
          techForm.reset();
          const imgInput = document.getElementById('tech-prod-img');
          if (imgInput) imgInput.setAttribute('required', 'required');
          const submitBtn = techForm.querySelector('button[type="submit"]');
          if (submitBtn) submitBtn.innerHTML = 'Add Product';
          const prevBox = document.getElementById('tech-preview-box');
          if (prevBox) prevBox.style.display = 'none';
          const cancelBtn = document.getElementById('btn-cancel-tech');
          if (cancelBtn) cancelBtn.style.display = 'none';

        } catch (err) {
          console.error(err);
          showToast('Error', err.message || 'Failed to save product.', 'delete');
        } finally {
          btn.innerHTML = oldText;
          btn.disabled = false;
        }
      });
    })();

    // ── REEL GLOBAL PALACE Form Handler ──
    (() => {
      const palaceForm = document.getElementById('form-palace-service');
      if (!palaceForm) return;

      // Live fit preview for Palace
      const updatePalacePreview = () => {
        const fitSelect = document.getElementById('palace-service-image-fit');
        const previewImg = document.getElementById('palace-preview-img');
        const previewFrame = document.getElementById('palace-preview-frame');
        const modeTag = document.getElementById('palace-preview-mode-tag');
        if (!fitSelect || !previewImg || !previewFrame) return;
        const val = fitSelect.value || 'contain';
        const label = fitSelect.options[fitSelect.selectedIndex]?.text || '';
        if (modeTag) modeTag.textContent = label.split('\u2014')[0].trim() || val;
        previewFrame.style.aspectRatio = '';
        previewFrame.style.height = '';
        previewImg.style.objectFit = 'contain';
        previewImg.style.height = 'auto';
        if (val === 'contain')       { previewFrame.style.height = '260px'; previewImg.style.objectFit = 'contain'; previewImg.style.maxHeight = '260px'; }
        else if (val === 'cover')    { previewFrame.style.height = '220px'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '16-9')     { previewFrame.style.aspectRatio = '16/9'; previewImg.style.objectFit = 'contain'; }
        else if (val === '16-9-crop'){ previewFrame.style.aspectRatio = '16/9'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '4-3')      { previewFrame.style.aspectRatio = '4/3'; previewImg.style.objectFit = 'contain'; }
        else if (val === '4-3-crop') { previewFrame.style.aspectRatio = '4/3'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '1-1')      { previewFrame.style.aspectRatio = '1/1'; previewImg.style.objectFit = 'contain'; }
        else if (val === '1-1-crop') { previewFrame.style.aspectRatio = '1/1'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
      };
      const palaceImgInput = document.getElementById('palace-service-img');
      if (palaceImgInput) {
        palaceImgInput.addEventListener('change', (e) => {
          const file = e.target.files && e.target.files[0];
          if (file) {
            const reader = new FileReader();
            reader.onload = (evt) => {
              const prevImg = document.getElementById('palace-preview-img');
              const prevBox = document.getElementById('palace-preview-box');
              if (prevImg && prevBox) { prevImg.src = evt.target.result; prevBox.style.display = 'block'; updatePalacePreview(); }
            };
            reader.readAsDataURL(file);
          }
        });
      }
      const palaceFitSelect = document.getElementById('palace-service-image-fit');
      if (palaceFitSelect) palaceFitSelect.addEventListener('change', updatePalacePreview);

      palaceForm.addEventListener('submit', async e => {
        e.preventDefault();
        const fileInput = document.getElementById('palace-service-img');
        const files = Array.from(fileInput.files);
        const editId = palaceForm.dataset.editId;
        if (files.length === 0 && !editId) { showToast('No Image', 'Please select a service image.', 'delete'); return; }

        const btn = palaceForm.querySelector('button[type="submit"]');
        const oldText = btn.innerHTML;
        btn.innerHTML = 'Uploading Image...';
        btn.disabled = true;

        try {
          let imageUrls = [];
          if (files.length > 0) {
            for (let file of files) {
              const url = await uploadOrCompressImage(file);
              if (url) imageUrls.push(url);
            }
          } else if (editId && palaceForm.dataset.editImage) {
            imageUrls.push(palaceForm.dataset.editImage);
          }

          btn.innerHTML = 'Saving...';
          const fitMode = document.getElementById('palace-service-image-fit') ? document.getElementById('palace-service-image-fit').value : 'contain';
          const payload = {
            name: document.getElementById('palace-service-name').value.trim(),
            category: document.getElementById('palace-service-cat') ? document.getElementById('palace-service-cat').value.trim() : '',
            price: document.getElementById('palace-service-price').value.trim(),
            duration: document.getElementById('palace-service-duration') ? document.getElementById('palace-service-duration').value.trim() : '',
            status: document.getElementById('palace-service-status').value,
            description: document.getElementById('palace-service-desc') ? document.getElementById('palace-service-desc').value.trim() : '',
            image: imageUrls[0] || '',
            images: imageUrls,
            imageFit: fitMode,
            timestamp: firebase.firestore.FieldValue.serverTimestamp()
          };

          if (editId) {
            await window.db.collection('palace_services').doc(editId).update(payload);
            const idx = palaceServices.findIndex(p => p.id === editId);
            if (idx !== -1) palaceServices[idx] = { id: editId, ...payload };
            delete palaceForm.dataset.editId;
            delete palaceForm.dataset.editImage;
          } else {
            const docRef = await window.db.collection('palace_services').add(payload);
            palaceServices.unshift({ id: docRef.id, ...payload });
          }

          renderList(palaceServices, 'palace-services-list', 'palace_service', 'palace_services');
          const countEl = document.getElementById('palace-services-count');
          if (countEl) countEl.textContent = palaceServices.length;
          showToast('Success!', editId ? 'Service updated!' : 'Service added to REEL GLOBAL PALACE!');
          palaceForm.reset();
          const imgInput = document.getElementById('palace-service-img');
          if (imgInput) imgInput.setAttribute('required', 'required');
          const submitBtn = palaceForm.querySelector('button[type="submit"]');
          if (submitBtn) submitBtn.innerHTML = 'Add Service';
          const prevBox = document.getElementById('palace-preview-box');
          if (prevBox) prevBox.style.display = 'none';
          const cancelBtn = document.getElementById('btn-cancel-palace');
          if (cancelBtn) cancelBtn.style.display = 'none';

        } catch (err) {
          console.error(err);
          showToast('Error', err.message || 'Failed to save service.', 'delete');
        } finally {
          btn.innerHTML = oldText;
          btn.disabled = false;
        }
      });
    })();

    // ── REEL AUTO CENTRE Form Handler ──
    (() => {
      const autoForm = document.getElementById('form-auto-car');
      if (!autoForm) return;

      // Live fit preview for Auto
      const updateAutoPreview = () => {
        const fitSelect = document.getElementById('auto-car-image-fit');
        const previewImg = document.getElementById('auto-preview-img');
        const previewFrame = document.getElementById('auto-preview-frame');
        const modeTag = document.getElementById('auto-preview-mode-tag');
        if (!fitSelect || !previewImg || !previewFrame) return;
        const val = fitSelect.value || 'contain';
        const label = fitSelect.options[fitSelect.selectedIndex]?.text || '';
        if (modeTag) modeTag.textContent = label.split('\u2014')[0].trim() || val;
        previewFrame.style.aspectRatio = '';
        previewFrame.style.height = '';
        previewImg.style.objectFit = 'contain';
        previewImg.style.height = 'auto';
        if (val === 'contain')       { previewFrame.style.height = '260px'; previewImg.style.objectFit = 'contain'; previewImg.style.maxHeight = '260px'; }
        else if (val === 'cover')    { previewFrame.style.height = '220px'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '16-9')     { previewFrame.style.aspectRatio = '16/9'; previewImg.style.objectFit = 'contain'; }
        else if (val === '16-9-crop'){ previewFrame.style.aspectRatio = '16/9'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '4-3')      { previewFrame.style.aspectRatio = '4/3'; previewImg.style.objectFit = 'contain'; }
        else if (val === '4-3-crop') { previewFrame.style.aspectRatio = '4/3'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
        else if (val === '1-1')      { previewFrame.style.aspectRatio = '1/1'; previewImg.style.objectFit = 'contain'; }
        else if (val === '1-1-crop') { previewFrame.style.aspectRatio = '1/1'; previewImg.style.objectFit = 'cover'; previewImg.style.height = '100%'; }
      };
      const autoImgInput = document.getElementById('auto-car-img');
      if (autoImgInput) {
        autoImgInput.addEventListener('change', (e) => {
          const file = e.target.files && e.target.files[0];
          if (file) {
            const reader = new FileReader();
            reader.onload = (evt) => {
              const prevImg = document.getElementById('auto-preview-img');
              const prevBox = document.getElementById('auto-preview-box');
              if (prevImg && prevBox) { prevImg.src = evt.target.result; prevBox.style.display = 'block'; updateAutoPreview(); }
            };
            reader.readAsDataURL(file);
          }
        });
      }
      const autoFitSelect = document.getElementById('auto-car-image-fit');
      if (autoFitSelect) autoFitSelect.addEventListener('change', updateAutoPreview);

      autoForm.addEventListener('submit', async e => {
        e.preventDefault();
        const fileInput = document.getElementById('auto-car-img');
        const files = Array.from(fileInput.files);
        const editId = autoForm.dataset.editId;
        if (files.length === 0 && !editId) { showToast('No Image', 'Please select a car image.', 'delete'); return; }

        const btn = autoForm.querySelector('button[type="submit"]');
        const oldText = btn.innerHTML;
        btn.innerHTML = 'Uploading Image...';
        btn.disabled = true;

        try {
          let imageUrls = [];
          if (files.length > 0) {
            for (let file of files) {
              const url = await uploadOrCompressImage(file);
              if (url) imageUrls.push(url);
            }
          } else if (editId && autoForm.dataset.editImage) {
            imageUrls.push(autoForm.dataset.editImage);
          }

          btn.innerHTML = 'Saving...';
          const fitMode = document.getElementById('auto-car-image-fit') ? document.getElementById('auto-car-image-fit').value : 'contain';
          const payload = {
            name: document.getElementById('auto-car-name').value.trim(),
            category: document.getElementById('auto-car-cat') ? document.getElementById('auto-car-cat').value.trim() : '',
            price: document.getElementById('auto-car-price').value.trim(),
            yearMileage: document.getElementById('auto-car-year-mileage') ? document.getElementById('auto-car-year-mileage').value.trim() : '',
            status: document.getElementById('auto-car-status').value,
            specs: document.getElementById('auto-car-specs') ? document.getElementById('auto-car-specs').value.trim() : '',
            description: document.getElementById('auto-car-desc') ? document.getElementById('auto-car-desc').value.trim() : '',
            image: imageUrls[0] || '',
            images: imageUrls,
            imageFit: fitMode,
            timestamp: firebase.firestore.FieldValue.serverTimestamp()
          };

          if (editId) {
            await window.db.collection('auto_cars').doc(editId).update(payload);
            const idx = autoCars.findIndex(p => p.id === editId);
            if (idx !== -1) autoCars[idx] = { id: editId, ...payload };
            delete autoForm.dataset.editId;
            delete autoForm.dataset.editImage;
          } else {
            const docRef = await window.db.collection('auto_cars').add(payload);
            autoCars.unshift({ id: docRef.id, ...payload });
          }

          renderList(autoCars, 'auto-cars-list', 'auto_car', 'auto_cars');
          const countEl = document.getElementById('auto-cars-count');
          if (countEl) countEl.textContent = autoCars.length;
          showToast('Success!', editId ? 'Car listing updated!' : 'Car added to REEL AUTO!');
          autoForm.reset();
          const imgInput = document.getElementById('auto-car-img');
          if (imgInput) imgInput.setAttribute('required', 'required');
          const submitBtn = autoForm.querySelector('button[type="submit"]');
          if (submitBtn) submitBtn.innerHTML = 'Add Car';
          const prevBox = document.getElementById('auto-preview-box');
          if (prevBox) prevBox.style.display = 'none';
          const cancelBtn = document.getElementById('btn-cancel-auto');
          if (cancelBtn) cancelBtn.style.display = 'none';

        } catch (err) {
          console.error(err);
          showToast('Error', err.message || 'Failed to save car listing.', 'delete');
        } finally {
          btn.innerHTML = oldText;
          btn.disabled = false;
        }
      });
    })();

    // ── Broadcast Center Logic ──"""
text = text.replace(OLD_BC_MARKER, NEW_HANDLERS, 1)

# ─────────────────────────────────────────────────────────
# PATCH 15: Add badge CSS if not already present
# Insert before closing </style> in the <head>
# ─────────────────────────────────────────────────────────
BADGE_CSS = """
    /* ── Division Status Badges ── */
    .badge-status {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 20px;
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      margin-left: 6px;
      vertical-align: middle;
    }
    .badge-available {
      background: rgba(74,222,128,0.18);
      color: #4ade80;
      border: 1px solid rgba(74,222,128,0.35);
    }
    .badge-underoffer {
      background: rgba(212,175,55,0.18);
      color: #D4AF37;
      border: 1px solid rgba(212,175,55,0.35);
    }
    .badge-sold {
      background: rgba(255,74,74,0.18);
      color: #ff4a4a;
      border: 1px solid rgba(255,74,74,0.35);
    }
"""
if '.badge-available' not in text:
    # Find last </style> before <body>
    body_pos = text.find('<body')
    style_pos = text.rfind('</style>', 0, body_pos)
    if style_pos != -1:
        text = text[:style_pos] + BADGE_CSS + text[style_pos:]
        print("Badge CSS injected.")
    else:
        print("WARNING: Could not inject badge CSS.")
else:
    print("Badge CSS already present.")

# ─────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────
if text != original_text:
    with open('admin/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("SUCCESS: admin/index.html patched.")
else:
    print("WARNING: No changes were made — check patch targets.")

