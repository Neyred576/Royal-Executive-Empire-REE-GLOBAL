import os
import re

admin_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\admin\index.html"

with open(admin_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add CSS for division switcher & safety bar
div_switcher_css = """
    /* ═ UNIFIED MULTI-DIVISION SWITCHER ═ */
    .division-hub-bar {
      display: flex;
      gap: 12px;
      overflow-x: auto;
      padding: 6px 4px 18px;
      margin-bottom: 24px;
      scrollbar-width: none;
    }
    .division-hub-bar::-webkit-scrollbar { display: none; }
    .div-hub-btn {
      display: flex;
      align-items: center;
      gap: 10px;
      background: rgba(22, 22, 22, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: var(--radius-lg);
      padding: 12px 20px;
      color: #fff;
      font-family: var(--font-body);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all var(--t) var(--ease);
      backdrop-filter: blur(10px);
    }
    .div-hub-btn:hover {
      background: rgba(30, 30, 30, 0.95);
      border-color: rgba(212, 175, 55, 0.4);
      transform: translateY(-2px);
    }
    .div-hub-btn.active {
      background: linear-gradient(135deg, rgba(212,175,55,0.2) 0%, rgba(20,20,20,0.9) 100%);
      border-color: var(--gold);
      box-shadow: 0 4px 20px rgba(212,175,55,0.2);
    }
    .div-hub-btn .div-icon { font-size: 1.15rem; }
    .div-hub-btn .div-tag {
      font-size: 0.65rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      color: rgba(255,255,255,0.6);
    }
    .div-hub-btn.active .div-tag {
      background: rgba(212,175,55,0.25);
      color: var(--gold-bright);
    }

    /* Safety & Backup Banner */
    .safety-backup-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      border-radius: var(--radius-md);
      padding: 14px 20px;
      margin-bottom: 24px;
    }
    .safety-backup-text {
      display: flex;
      align-items: center;
      gap: 10px;
      color: #34d399;
      font-size: 0.82rem;
      font-weight: 500;
    }
    .safety-backup-actions {
      display: flex;
      gap: 10px;
    }
    .btn-safety-dl {
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #fff;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 999px;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-safety-dl:hover {
      background: rgba(16, 185, 129, 0.35);
      transform: translateY(-1px);
    }
"""

if ".division-hub-bar" not in html:
    html = html.replace(".stats-strip {", div_switcher_css + "\n    .stats-strip {")
    print("Added division switcher CSS!")

# 2. Update the Sidebar Navigation to include all 4 divisions
nav_items_replacement = """    <div class="nav-section-label">Main Empire Holding</div>
    <ul class="admin-nav">
      <li>
        <a href="#" class="admin-nav-link active" data-target="sec-blog">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
            </svg>
          </div>
          <span class="nav-label">Manage Blog (All Sites)</span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-notifications">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </div>
          <span class="nav-label">Push Alerts & Broadcast</span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-scheduler">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <span class="nav-label">Post Scheduler</span>
        </a>
      </li>
    </ul>

    <div class="nav-section-label" style="margin-top:16px;">The 4 Divisions</div>
    <ul class="admin-nav">
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-tech-hub">
          <div class="nav-icon">💻</div>
          <span class="nav-label">REEL Tech Hub</span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-properties">
          <div class="nav-icon">🏡</div>
          <span class="nav-label">REEL Properties</span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-global-palace">
          <div class="nav-icon">✨</div>
          <span class="nav-label">REEL Global Palace</span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-auto-centre">
          <div class="nav-icon">🏎️</div>
          <span class="nav-label">REEL Auto Centre</span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-shop">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
            </svg>
          </div>
          <span class="nav-label">Holding Store Products</span>
        </a>
      </li>
    </ul>"""

pattern_nav = re.compile(r'<div class="nav-section-label">Content Management</div>\s*<ul class="admin-nav">.*?</ul>', re.DOTALL)
if pattern_nav.search(html):
    html = pattern_nav.sub(nav_items_replacement, html, count=1)
    print("Updated Sidebar navigation!")

# 3. Add the Division Hub Switcher Bar and Safety Banner right before stats-strip
switcher_html = """
    <!-- ═ UNIFIED MULTI-DIVISION SELECTOR ═ -->
    <div class="division-hub-bar" id="divHubBar">
      <button class="div-hub-btn active" data-target-sec="sec-blog" data-div="main">
        <span class="div-icon">👑</span>
        <span>Main Empire</span>
        <span class="div-tag">REEL Holding</span>
      </button>
      <button class="div-hub-btn" data-target-sec="sec-tech-hub" data-div="tech">
        <span class="div-icon">💻</span>
        <span>REEL Tech Hub</span>
        <span class="div-tag">Hardware & Phones</span>
      </button>
      <button class="div-hub-btn" data-target-sec="sec-properties" data-div="properties">
        <span class="div-icon">🏡</span>
        <span>REEL Properties</span>
        <span class="div-tag">Real Estate</span>
      </button>
      <button class="div-hub-btn" data-target-sec="sec-global-palace" data-div="palace">
        <span class="div-icon">✨</span>
        <span>REEL Global Palace</span>
        <span class="div-tag">Salon & Lifestyle</span>
      </button>
      <button class="div-hub-btn" data-target-sec="sec-auto-centre" data-div="auto">
        <span class="div-icon">🏎️</span>
        <span>REEL Auto Centre</span>
        <span class="div-tag">Automotive Hub</span>
      </button>
    </div>

    <!-- Safety & Backup Bar -->
    <div class="safety-backup-bar">
      <div class="safety-backup-text">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
        <span>All 25 Blogs & Divisions Data Are Backed Up & Synchronized With Firebase</span>
      </div>
      <div class="safety-backup-actions">
        <button id="btnDownloadBlogBackup" class="btn-safety-dl" title="Download offline JSON file of all blogs">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Download Offline Backup (.JSON)
        </button>
      </div>
    </div>
"""

if "id=\"divHubBar\"" not in html:
    html = html.replace('<div class="stats-strip">', switcher_html + '\n    <div class="stats-strip">')
    print("Added Division Hub Bar and Safety Banner to main area!")

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated admin/index.html successfully!")

