import sys
import re

with open('admin/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Status Badge CSS
badge_css = """
    /* Status Badges */
    .badge-status {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      margin-left: 6px;
    }
    .badge-available, .badge-in-stock {
      background: rgba(37,211,102,0.15);
      color: #25D366;
      border: 1px solid rgba(37,211,102,0.3);
    }
    .badge-underoffer, .badge-pre-order, .badge-booked {
      background: rgba(212,175,55,0.18);
      color: var(--gold);
      border: 1px solid rgba(212,175,55,0.35);
    }
    .badge-sold, .badge-out-of-stock {
      background: rgba(255,74,74,0.15);
      color: #ff5757;
      border: 1px solid rgba(255,74,74,0.3);
    }
"""

if ".badge-status {" not in content:
    content = content.replace("/* Native select popup dark styling */", badge_css + "\n    /* Native select popup dark styling */")

# 2. Update sec-properties HTML form (Status: AVAILABLE, UNDER OFFER, SOLD + Cancel Edit button)
old_prop_sec_target = """            <div class="form-group" style="padding:15px; background:rgba(212,175,55,0.03); border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                Publishing Schedule
              </label>
              <select id="prop-status" style="margin-bottom:12px;">
                <option value="published">Publish Immediately</option>
                <option value="scheduled">Schedule for Later</option>
                <option value="archived">Archived (Hide from Public)</option>
              </select>
              <div id="prop-schedule-wrap" style="display:none;">
                <label style="font-size:0.65rem;">Schedule Date & Time</label>
                <input type="datetime-local" id="prop-schedule-time" style="margin-bottom:5px;" />
                <span style="font-size:0.7rem; color:var(--w40);">Property will be hidden until this date/time passes.</span>
              </div>
            </div>
            <button type="submit" class="btn-submit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              Add Property
            </button>"""

new_prop_sec_replace = """            <div class="form-group" style="padding:15px; background:rgba(212,175,55,0.03); border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                Property Listing Status *
              </label>
              <select id="prop-status" style="margin-bottom:12px;" required>
                <option value="AVAILABLE">AVAILABLE (Active Listing)</option>
                <option value="UNDER OFFER">UNDER OFFER (Pending Agreement)</option>
                <option value="SOLD">SOLD (Closed Deal)</option>
              </select>
            </div>
            <div style="display:flex; gap:12px; align-items:center;">
              <button type="submit" id="btn-save-prop" class="btn-submit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                Add Property
              </button>
              <button type="button" id="btn-cancel-prop" class="btn-ghost" style="display:none; padding:12px 18px; border-radius:var(--radius-md);" onclick="window.cancelPropEdit()">
                Cancel Edit
              </button>
            </div>"""

if old_prop_sec_target in content:
    content = content.replace(old_prop_sec_target, new_prop_sec_replace, 1)
    print("[OK] Updated Property form status & cancel button")
else:
    print("[WARN] Could not find exact old_prop_sec_target")

# 3. Replace sec-tech-hub, sec-global-palace, and sec-auto-centre HTML
divisions_html_target_start = '<!-- ════════════════════════════════════════════════════════════════════ -->\n    <!-- 💻 REEL TECH HUB DIVISION MANAGEMENT'
divisions_html_target_end = '</section>\n\n  </main>'

new_divisions_html = """<!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- 💻 REEL TECH HUB DIVISION MANAGEMENT                                -->
    <!-- ════════════════════════════════════════════════════════════════════ -->
    <section id="sec-tech-hub" class="admin-section">
      <div class="section-header">
        <div class="section-icon">💻</div>
        <div>
          <h1>REEL Tech Hub Manager</h1>
          <p>Upload hardware, business laptops, smartphones, workstations, and manage stock status.</p>
        </div>
      </div>

      <div class="admin-grid">
        <div class="admin-card">
          <div class="card-title" id="tech-card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
            Add New Tech Hub Product
          </div>
          <form id="form-tech-product">
            <div class="form-group">
              <label>Product Name *</label>
              <input type="text" id="tech-prod-name" placeholder="e.g. Apple iPhone 15 Pro Max (256GB) / Dell Latitude 5420" required />
            </div>
            <div class="form-group">
              <label>Category *</label>
              <select id="tech-prod-cat" required>
                <option value="Mobile Phones">📱 Mobile Phones</option>
                <option value="Laptops">💻 Business &amp; Executive Laptops</option>
                <option value="Workstations">🖥️ Tower &amp; Mobile Workstations</option>
                <option value="Servers & Network">🖧 Enterprise Servers &amp; Network</option>
                <option value="Monitors & Smart Office">📺 Monitors &amp; Smart Office</option>
                <option value="Accessories">🎧 Executive Accessories</option>
              </select>
            </div>
            <div class="form-row" style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
              <div class="form-group">
                <label>Price (₦) *</label>
                <input type="text" id="tech-prod-price" placeholder="e.g. ₦1,850,000" required />
              </div>
              <div class="form-group">
                <label>Original / Strike Price (₦)</label>
                <input type="text" id="tech-prod-orig-price" placeholder="e.g. ₦1,980,000" />
              </div>
            </div>
            <div class="form-group">
              <label>Stock / Inventory Status *</label>
              <select id="tech-prod-status" required>
                <option value="IN STOCK">IN STOCK (Ready to Ship)</option>
                <option value="SOLD">SOLD (Out of Stock)</option>
                <option value="PRE-ORDER">PRE-ORDER</option>
              </select>
            </div>
            <div class="form-group">
              <label>Key Specifications (Highlights) *</label>
              <input type="text" id="tech-prod-specs" placeholder="e.g. A17 Pro Bionic • 256GB • 6.7 OLED • Grade A+ Titanium" required />
            </div>
            <div class="form-group">
              <label>Product Image File (Manual Upload) *</label>
              <input type="file" id="tech-prod-img" accept="image/*" class="file-drop" required />
            </div>
            <div class="form-group" style="padding:14px; background:rgba(0,217,255,0.03); border-radius:8px; border:1px solid rgba(0,217,255,0.2);">
              <label style="color:var(--cyan); display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
                Image Display Mode (Aspect Ratio & Fit)
              </label>
              <select id="tech-prod-image-fit" style="margin-bottom:6px;">
                <option value="16-9">&#9635; 16:9 Widescreen (Fit) — landscape ratio, no crop</option>
                <option value="16-9-crop">&#9635; 16:9 Widescreen (Fill / Crop) — widescreen banner</option>
                <option value="4-3">&#9635; 4:3 Standard (Fit) — classic photo, no crop</option>
                <option value="4-3-crop">&#9635; 4:3 Standard (Fill / Crop) — classic photo cropped</option>
                <option value="1-1">&#9635; 1:1 Square (Fit) — square product flyer</option>
                <option value="1-1-crop">&#9635; 1:1 Square (Fill / Crop) — square card cropped</option>
                <option value="contain">&#10003; Fit in Frame (Contain) — 100% visible, no crop</option>
                <option value="cover">&#9724; Fill Frame (Cover) — classic card fill</option>
              </select>
              <div id="tech-preview-box" style="display:none; background:#080808; border:1px dashed rgba(0,217,255,0.35); border-radius:8px; padding:12px; margin-top:8px;">
                <div style="font-size:0.75rem; color:var(--cyan); font-weight:700; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                  <span>Live Product Preview</span>
                  <span id="tech-preview-mode-tag" style="background:rgba(0,217,255,0.18); color:var(--cyan); padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:600;">16:9 Fit</span>
                </div>
                <div id="tech-preview-frame" style="width:100%; max-width:340px; margin:0 auto; background:#000; border-radius:6px; overflow:hidden; border:1px solid rgba(0,217,255,0.2); display:flex; align-items:center; justify-content:center;">
                  <img id="tech-preview-img" src="" alt="Preview" style="display:block; width:100%; max-height:260px; object-fit:contain;" decoding="async" loading="lazy">
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Product Description</label>
              <textarea id="tech-prod-desc" rows="3" placeholder="Detailed corporate hardware notes, warranty terms, and fleet provisioning details..."></textarea>
            </div>
            <div style="display:flex; gap:12px; align-items:center;">
              <button type="submit" id="btn-save-tech-prod" class="btn-submit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                Publish to Tech Hub Catalog
              </button>
              <button type="button" id="btn-cancel-tech" class="btn-ghost" style="display:none; padding:12px 18px; border-radius:var(--radius-md);" onclick="window.cancelTechEdit()">
                Cancel Edit
              </button>
            </div>
          </form>
        </div>
        <div class="admin-card">
          <div class="card-title" style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:8px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              Live Tech Hub Catalog
            </div>
            <span id="tech-catalog-count" style="font-size:0.72rem; color:var(--cyan); background:rgba(0,217,255,0.12); padding:2px 8px; border-radius:999px;">0 Items</span>
          </div>
          <div id="tech-products-list" class="admin-list"></div>
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- ✨ REEL GLOBAL PALACE DIVISION MANAGEMENT                          -->
    <!-- ════════════════════════════════════════════════════════════════════ -->
    <section id="sec-global-palace" class="admin-section">
      <div class="section-header">
        <div class="section-icon">✨</div>
        <div>
          <h1>REEL Global Palace Services</h1>
          <p>Upload luxury salon services, executive barbing, grooming treatments, and manage bookings.</p>
        </div>
      </div>

      <div class="admin-grid">
        <div class="admin-card">
          <div class="card-title" id="palace-card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
            Add New Palace Service
          </div>
          <form id="form-palace-service">
            <div class="form-group">
              <label>Service Name *</label>
              <input type="text" id="palace-service-name" placeholder="e.g. Executive Royal Haircut & Beard Sculpt" required />
            </div>
            <div class="form-group">
              <label>Category *</label>
              <select id="palace-service-cat" required>
                <option value="Executive Barbing">✂️ Executive Barbing &amp; Grooming</option>
                <option value="Luxury Salon & Styling">💇 Luxury Hair Styling &amp; Treatment</option>
                <option value="Organic Spa & Care">🧴 Organic Spa &amp; Scalp Care</option>
                <option value="VIP Suite Experience">👑 VIP Suite Full Experience</option>
                <option value="Curated Retail Offerings">🛍️ Curated Organic Retail</option>
              </select>
            </div>
            <div class="form-row" style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
              <div class="form-group">
                <label>Rate / Price (₦) *</label>
                <input type="text" id="palace-service-price" placeholder="e.g. ₦15,000 or $35" required />
              </div>
              <div class="form-group">
                <label>Estimated Duration</label>
                <input type="text" id="palace-service-duration" placeholder="e.g. 45 Mins / 1 Hour" value="45 Mins" />
              </div>
            </div>
            <div class="form-group">
              <label>Booking Availability *</label>
              <select id="palace-service-status" required>
                <option value="AVAILABLE">AVAILABLE (Accepting Appointments)</option>
                <option value="BOOKED">BOOKED (Schedule Full)</option>
                <option value="COMING SOON">COMING SOON</option>
              </select>
            </div>
            <div class="form-group">
              <label>Service Image File (Manual Upload) *</label>
              <input type="file" id="palace-service-img" accept="image/*" class="file-drop" required />
            </div>
            <div class="form-group" style="padding:14px; background:rgba(212,175,55,0.04); border-radius:8px; border:1px solid rgba(212,175,55,0.2);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
                Image Display Mode (Aspect Ratio & Fit)
              </label>
              <select id="palace-service-image-fit" style="margin-bottom:6px;">
                <option value="16-9">&#9635; 16:9 Widescreen (Fit) — landscape ratio, no crop</option>
                <option value="16-9-crop">&#9635; 16:9 Widescreen (Fill / Crop) — widescreen banner</option>
                <option value="4-3">&#9635; 4:3 Standard (Fit) — classic photo, no crop</option>
                <option value="4-3-crop">&#9635; 4:3 Standard (Fill / Crop) — classic photo cropped</option>
                <option value="1-1">&#9635; 1:1 Square (Fit) — square flyer</option>
                <option value="1-1-crop">&#9635; 1:1 Square (Fill / Crop) — square card cropped</option>
                <option value="contain">&#10003; Fit in Frame (Contain) — 100% visible, no crop</option>
                <option value="cover">&#9724; Fill Frame (Cover) — classic card fill</option>
              </select>
              <div id="palace-preview-box" style="display:none; background:#080808; border:1px dashed rgba(212,175,55,0.35); border-radius:8px; padding:12px; margin-top:8px;">
                <div style="font-size:0.75rem; color:var(--gold); font-weight:700; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                  <span>Live Service Preview</span>
                  <span id="palace-preview-mode-tag" style="background:rgba(212,175,55,0.18); color:var(--gold); padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:600;">16:9 Fit</span>
                </div>
                <div id="palace-preview-frame" style="width:100%; max-width:340px; margin:0 auto; background:#000; border-radius:6px; overflow:hidden; border:1px solid rgba(212,175,55,0.2); display:flex; align-items:center; justify-content:center;">
                  <img id="palace-preview-img" src="" alt="Preview" style="display:block; width:100%; max-height:260px; object-fit:contain;" decoding="async" loading="lazy">
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Service Description & Details</label>
              <textarea id="palace-service-desc" rows="3" placeholder="Description of grooming treatment, products used, amenities included..."></textarea>
            </div>
            <div style="display:flex; gap:12px; align-items:center;">
              <button type="submit" id="btn-save-palace" class="btn-submit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                Add Palace Service
              </button>
              <button type="button" id="btn-cancel-palace" class="btn-ghost" style="display:none; padding:12px 18px; border-radius:var(--radius-md);" onclick="window.cancelPalaceEdit()">
                Cancel Edit
              </button>
            </div>
          </form>
        </div>
        <div class="admin-card">
          <div class="card-title" style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:8px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              Live Palace Services
            </div>
            <span id="palace-services-count" style="font-size:0.72rem; color:var(--gold); background:rgba(212,175,55,0.12); padding:2px 8px; border-radius:999px;">0 Services</span>
          </div>
          <div id="palace-services-list" class="admin-list"></div>
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- 🏎️ REEL AUTO CENTRE DIVISION MANAGEMENT                             -->
    <!-- ════════════════════════════════════════════════════════════════════ -->
    <section id="sec-auto-centre" class="admin-section">
      <div class="section-header">
        <div class="section-icon">🏎️</div>
        <div>
          <h1>REEL Auto Centre Fleet</h1>
          <p>Upload luxury vehicles, manage pricing, specs, and status (AVAILABLE, UNDER OFFER, SOLD).</p>
        </div>
      </div>

      <div class="admin-grid">
        <div class="admin-card">
          <div class="card-title" id="auto-card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
            Add New Vehicle to Fleet
          </div>
          <form id="form-auto-car">
            <div class="form-group">
              <label>Vehicle Model / Title *</label>
              <input type="text" id="auto-car-name" placeholder="e.g. 2024 Mercedes-Benz G63 AMG / Range Rover Autobiography" required />
            </div>
            <div class="form-group">
              <label>Vehicle Category *</label>
              <select id="auto-car-cat" required>
                <option value="Luxury SUV">🚙 Luxury SUV</option>
                <option value="Executive Sedan">🚗 Executive Sedan</option>
                <option value="Sports Car">🏎️ Sports &amp; Exotic Car</option>
                <option value="Armored & Tactical">🛡️ Armored &amp; Tactical Vehicle</option>
                <option value="Detailing & Fleet Package">🔧 Detailing &amp; Maintenance Package</option>
              </select>
            </div>
            <div class="form-row" style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
              <div class="form-group">
                <label>Price *</label>
                <input type="text" id="auto-car-price" placeholder="e.g. ₦185,000,000 or $220,000 / POA" required />
              </div>
              <div class="form-group">
                <label>Year &amp; Mileage</label>
                <input type="text" id="auto-car-year-mileage" placeholder="e.g. 2024 • 5,000 km" />
              </div>
            </div>
            <div class="form-group">
              <label>Inventory / Availability Status *</label>
              <select id="auto-car-status" required>
                <option value="AVAILABLE">AVAILABLE (In Showroom)</option>
                <option value="UNDER OFFER">UNDER OFFER (Pending Purchase)</option>
                <option value="SOLD">SOLD (Delivered)</option>
              </select>
            </div>
            <div class="form-group">
              <label>Key Specifications *</label>
              <input type="text" id="auto-car-specs" placeholder="e.g. 4.0L V8 Bi-Turbo • 577 HP • AWD • Full Option Interior" required />
            </div>
            <div class="form-group">
              <label>Vehicle Image File (Manual Upload) *</label>
              <input type="file" id="auto-car-img" accept="image/*" class="file-drop" required />
            </div>
            <div class="form-group" style="padding:14px; background:rgba(212,175,55,0.04); border-radius:8px; border:1px solid rgba(212,175,55,0.2);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
                Image Display Mode (Aspect Ratio & Fit)
              </label>
              <select id="auto-car-image-fit" style="margin-bottom:6px;">
                <option value="16-9">&#9635; 16:9 Widescreen (Fit) — landscape ratio, no crop</option>
                <option value="16-9-crop">&#9635; 16:9 Widescreen (Fill / Crop) — widescreen banner</option>
                <option value="4-3">&#9635; 4:3 Standard (Fit) — classic photo, no crop</option>
                <option value="4-3-crop">&#9635; 4:3 Standard (Fill / Crop) — classic photo cropped</option>
                <option value="1-1">&#9635; 1:1 Square (Fit) — square flyer</option>
                <option value="1-1-crop">&#9635; 1:1 Square (Fill / Crop) — square card cropped</option>
                <option value="contain">&#10003; Fit in Frame (Contain) — 100% visible, no crop</option>
                <option value="cover">&#9724; Fill Frame (Cover) — classic card fill</option>
              </select>
              <div id="auto-preview-box" style="display:none; background:#080808; border:1px dashed rgba(212,175,55,0.35); border-radius:8px; padding:12px; margin-top:8px;">
                <div style="font-size:0.75rem; color:var(--gold); font-weight:700; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                  <span>Live Vehicle Preview</span>
                  <span id="auto-preview-mode-tag" style="background:rgba(212,175,55,0.18); color:var(--gold); padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:600;">16:9 Fit</span>
                </div>
                <div id="auto-preview-frame" style="width:100%; max-width:340px; margin:0 auto; background:#000; border-radius:6px; overflow:hidden; border:1px solid rgba(212,175,55,0.2); display:flex; align-items:center; justify-content:center;">
                  <img id="auto-preview-img" src="" alt="Preview" style="display:block; width:100%; max-height:260px; object-fit:contain;" decoding="async" loading="lazy">
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Vehicle Details & Provenance</label>
              <textarea id="auto-car-desc" rows="3" placeholder="Condition details, service history, custom options, warranty and import status..."></textarea>
            </div>
            <div style="display:flex; gap:12px; align-items:center;">
              <button type="submit" id="btn-save-auto" class="btn-submit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                Add Vehicle to Auto Fleet
              </button>
              <button type="button" id="btn-cancel-auto" class="btn-ghost" style="display:none; padding:12px 18px; border-radius:var(--radius-md);" onclick="window.cancelAutoEdit()">
                Cancel Edit
              </button>
            </div>
          </form>
        </div>
        <div class="admin-card">
          <div class="card-title" style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:8px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              Live Auto Fleet &amp; Inventory
            </div>
            <span id="auto-cars-count" style="font-size:0.72rem; color:var(--gold); background:rgba(212,175,55,0.12); padding:2px 8px; border-radius:999px;">0 Vehicles</span>
          </div>
          <div id="auto-cars-list" class="admin-list"></div>
        </div>
      </div>
    </section>
"""

start_idx = content.find(divisions_html_target_start)
end_idx = content.find(divisions_html_target_end, start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_divisions_html + '\n  </main>' + content[end_idx + len(divisions_html_target_end):]
    print("[OK] Replaced 3 division sections HTML with new responsive forms & lists")
else:
    print(f"[FAIL] Could not find division sections boundary: start={start_idx}, end={end_idx}")
    sys.exit(1)

with open('admin/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content)
print("Saved HTML structural updates successfully!")

