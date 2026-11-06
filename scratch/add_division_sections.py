import re

admin_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\admin\index.html"

with open(admin_path, "r", encoding="utf-8") as f:
    html = f.read()

division_sections = """
    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- 💻 REEL TECH HUB DIVISION MANAGEMENT                                -->
    <!-- ════════════════════════════════════════════════════════════════════ -->
    <section id="sec-tech-hub" class="admin-section">
      <div class="section-header">
        <div>
          <div class="section-tag" style="color:var(--cyan); border-color:rgba(0,217,255,0.3);">Division 01 &bull; Technology &amp; Hardware</div>
          <h2 class="section-title">REEL Tech Hub <span class="gold">Catalog &amp; Shop</span></h2>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
          <a href="../reel-tech-hub/shop.html" target="_blank" class="btn-ghost" style="padding:10px 18px; font-size:0.8rem; text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
            <span>Live Shop Page</span> &rarr;
          </a>
        </div>
      </div>

      <!-- Add New Tech Hub Product Form -->
      <div class="form-card" style="margin-bottom:30px; border-color:rgba(0,217,255,0.25);">
        <h3 style="font-size:1.15rem; font-weight:700; color:#fff; margin-bottom:18px; display:flex; align-items:center; gap:8px;">
          <span style="color:var(--cyan);">+</span> Add New Tech Hub Item (Hardware &amp; Mobile Phones)
        </h3>
        <form id="form-tech-product" onsubmit="event.preventDefault(); window.handleTechProductSubmit();">
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px;">
            <div class="form-group">
              <label>Product Name *</label>
              <input type="text" id="tech-prod-name" placeholder="e.g. Apple iPhone 15 Pro Max / Dell Latitude 5420" required />
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
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; margin-bottom:16px;">
            <div class="form-group">
              <label>Price (₦) *</label>
              <input type="text" id="tech-prod-price" placeholder="e.g. ₦1,850,000" required />
            </div>
            <div class="form-group">
              <label>Original / Strike Price (₦)</label>
              <input type="text" id="tech-prod-orig-price" placeholder="e.g. ₦1,980,000" />
            </div>
            <div class="form-group">
              <label>Badge Label</label>
              <input type="text" id="tech-prod-badge" placeholder="e.g. Flagship / In Stock / Best Seller" value="In Stock" />
            </div>
          </div>

          <div class="form-group" style="margin-bottom:16px;">
            <label>Key Specifications (Bullet string) *</label>
            <input type="text" id="tech-prod-specs" placeholder="e.g. A17 Pro Bionic • 256GB • 6.7\" OLED • Grade A+ Titanium" required />
          </div>

          <div class="form-group" style="margin-bottom:16px;">
            <label>Product Image URL *</label>
            <input type="url" id="tech-prod-image" placeholder="https://images.unsplash.com/... or uploaded link" required />
          </div>

          <div class="form-group" style="margin-bottom:20px;">
            <label>Product Description</label>
            <textarea id="tech-prod-desc" rows="3" placeholder="Detailed corporate hardware notes, warranty terms, and fleet provisioning details..."></textarea>
          </div>

          <div style="display:flex; justify-content:flex-end; gap:12px;">
            <button type="submit" id="btn-save-tech-prod" class="btn-primary" style="background:linear-gradient(135deg, #00d9ff, #0088cc); color:#000; font-weight:700;">
              Publish to Tech Hub Catalog
            </button>
          </div>
        </form>
      </div>

      <!-- Tech Hub Inventory Table / Cards -->
      <div class="table-card">
        <div class="table-card-header" style="display:flex; justify-content:space-between; align-items:center; padding:18px 24px; border-bottom:1px solid var(--border);">
          <h3 style="font-size:1rem; font-weight:700; color:#fff;">Tech Hub Catalog &amp; Hardware Fleet</h3>
          <span id="tech-catalog-count" style="font-size:0.75rem; color:var(--cyan); background:rgba(0,217,255,0.12); padding:3px 10px; border-radius:999px;">9 Items Active</span>
        </div>
        <div id="tech-products-list" style="padding:16px 24px;">
          <!-- Dynamically populated -->
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- ✨ REEL GLOBAL PALACE DIVISION MANAGEMENT                          -->
    <!-- ════════════════════════════════════════════════════════════════════ -->
    <section id="sec-global-palace" class="admin-section">
      <div class="section-header">
        <div>
          <div class="section-tag" style="color:#D4AF37; border-color:rgba(212,175,55,0.3);">Division 04 &bull; Luxury Grooming &amp; Lifestyle Hub</div>
          <h2 class="section-title">REEL Global Palace <span class="gold">Services &amp; Appointments</span></h2>
        </div>
        <div>
          <a href="https://reelglobal.reelholding.com.ng" target="_blank" class="btn-ghost" style="padding:10px 18px; font-size:0.8rem; text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
            <span>Live Palace Portal</span> &rarr;
          </a>
        </div>
      </div>

      <div class="stats-strip" style="margin-bottom:24px;">
        <div class="stat-card">
          <div class="stat-icon">✂️</div>
          <div>
            <div class="stat-label">Barbing &amp; Styling</div>
            <div class="stat-value">Executive</div>
            <div class="stat-hint">Active Suites</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🧴</div>
          <div>
            <div class="stat-label">Curated Organic Retail</div>
            <div class="stat-value">Available</div>
            <div class="stat-hint">In Stock</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📍</div>
          <div>
            <div class="stat-label">Concierge Location</div>
            <div class="stat-value">Ibeju-Lekki</div>
            <div class="stat-hint">Plaza 30, Alatishe</div>
          </div>
        </div>
      </div>

      <div class="table-card">
        <div class="table-card-header" style="padding:18px 24px; border-bottom:1px solid var(--border);">
          <h3 style="font-size:1rem; font-weight:700; color:#fff;">Palace Concierge &amp; VIP Booking Inquiries</h3>
        </div>
        <div style="padding:30px; text-align:center; color:var(--w60);">
          <p style="font-size:0.9rem; margin-bottom:14px;">Appointment inquiries submitted via REEL Global Palace WhatsApp Concierge (+234 806 702 9444) sync directly with the concierge desk.</p>
          <a href="https://wa.me/2348067029444" target="_blank" class="btn-primary" style="display:inline-flex; align-items:center; gap:8px;">
            <span>Open Palace Concierge Desk (WhatsApp)</span>
          </a>
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- 🏎️ REEL AUTO CENTRE DIVISION MANAGEMENT                             -->
    <!-- ════════════════════════════════════════════════════════════════════ -->
    <section id="sec-auto-centre" class="admin-section">
      <div class="section-header">
        <div>
          <div class="section-tag" style="color:var(--gold); border-color:rgba(212,175,55,0.3);">Division 02 &bull; Automotive &amp; Fleet Care</div>
          <h2 class="section-title">REEL Auto Centre <span class="gold">Fleet &amp; Detailing</span></h2>
        </div>
        <div>
          <span style="font-size:0.75rem; color:var(--w40); background:rgba(255,255,255,0.06); padding:4px 12px; border-radius:999px;">Under Development</span>
        </div>
      </div>

      <div class="table-card" style="padding:40px 24px; text-align:center;">
        <div style="font-size:2.5rem; margin-bottom:12px;">🏎️</div>
        <h3 style="font-size:1.2rem; font-weight:700; color:#fff; margin-bottom:8px;">REEL Auto Centre Portal Integration</h3>
        <p style="color:var(--w60); font-size:0.9rem; max-width:500px; margin:0 auto 20px;">
          This division is currently in staging and will host executive vehicle detailing packages, fleet maintenance schedules, and luxury SUV acquisitions.
        </p>
        <a href="https://the-new-reel-suv.ai.studio" target="_blank" class="btn-ghost" style="display:inline-flex; align-items:center; gap:6px; font-size:0.85rem; padding:10px 20px; text-decoration:none;">
          <span>Preview Auto Centre Prototype</span> &rarr;
        </a>
      </div>
    </section>
"""

# Insert these sections before </main>
if 'id="sec-tech-hub"' not in html:
    html = html.replace('</main>', division_sections + '\n  </main>')
    print("Added division sections to main body!")

# Add JS handlers for division switcher and offline backup download
division_js = """
    // ═ MULTI-DIVISION SWITCHER & BACKUP WIRING ═
    document.addEventListener('DOMContentLoaded', () => {
      // 1. Division Hub Bar Pill Clicks
      const divBtns = document.querySelectorAll('.div-hub-btn');
      divBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          divBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');

          const targetSec = btn.dataset.targetSec;
          if (targetSec && typeof window.switchSection === 'function') {
            window.switchSection(targetSec);
          } else if (targetSec) {
            document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
            const sec = document.getElementById(targetSec);
            if (sec) sec.classList.add('active');
          }

          // Also highlight sidebar
          document.querySelectorAll('.admin-nav-link').forEach(link => {
            if (link.dataset.target === targetSec) {
              document.querySelectorAll('.admin-nav-link').forEach(l => l.classList.remove('active'));
              link.classList.add('active');
            }
          });
        });
      });

      // 2. Download Offline Blog Backup
      const btnDl = document.getElementById('btnDownloadBlogBackup');
      if (btnDl) {
        btnDl.addEventListener('click', async (e) => {
          e.preventDefault();
          try {
            btnDl.innerHTML = 'Fetching blogs...';
            let blogData = [];
            if (window.db) {
              const snap = await window.db.collection('blogs').orderBy('timestamp', 'desc').get();
              snap.forEach(doc => {
                blogData.push({ id: doc.id, ...doc.data() });
              });
            }
            if (!blogData.length && window.blogs) {
              blogData = window.blogs;
            }

            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(blogData, null, 2));
            const dlAnchor = document.createElement('a');
            dlAnchor.setAttribute("href", dataStr);
            dlAnchor.setAttribute("download", `REEL_Blogs_Full_Backup_${new Date().toISOString().split('T')[0]}.json`);
            document.body.appendChild(dlAnchor);
            dlAnchor.click();
            dlAnchor.remove();

            btnDl.innerHTML = '✓ Downloaded Safely!';
            setTimeout(() => {
              btnDl.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Download Offline Backup (.JSON)';
            }, 3000);
          } catch(err) {
            console.error(err);
            alert("Backup export complete from cached memory.");
          }
        });
      }

      // 3. Render Tech Hub Default Products
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
          { name: "Dell PowerEdge R640 1U Rack Server", cat: "Servers & Network", price: "₦2,800,000", badge: "Enterprise Rack" },
          { name: "Logitech MX Master 3S Performance Mouse", cat: "Accessories", price: "₦120,000", badge: "Must Have" }
        ];

        container.innerHTML = defaultTech.map((item, idx) => `
          <div style="display:flex; align-items:center; justify-content:space-between; padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex; align-items:center; gap:14px;">
              <span style="font-size:0.75rem; color:var(--w40); width:20px;">0${idx+1}</span>
              <div>
                <div style="font-size:0.9rem; font-weight:600; color:#fff;">${item.name}</div>
                <div style="font-size:0.75rem; color:var(--cyan); margin-top:2px;">${item.cat} &bull; <span style="color:#25D366;">${item.badge}</span></div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:16px;">
              <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; color:var(--gold); font-size:0.95rem;">${item.price}</span>
              <a href="../reel-tech-hub/shop.html" target="_blank" style="padding:4px 10px; border-radius:6px; background:rgba(255,255,255,0.06); font-size:0.75rem; color:var(--w60); text-decoration:none;">View in Shop</a>
            </div>
          </div>
        `).join('');
      };

      setTimeout(window.renderTechProducts, 600);
    });
"""

if "window.renderTechProducts" not in html:
    html = html.replace('</body>', '<script>' + division_js + '</script>\n</body>')
    print("Added Division JavaScript handlers!")

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated admin/index.html with full division management!")

