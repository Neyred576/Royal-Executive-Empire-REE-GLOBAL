import sys

with open('admin/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update :root sidebar width and body styling
old_body = """      --sidebar-w: 280px;
      --ease: cubic-bezier(0.16, 1, 0.3, 1);
      --t: 0.35s;
    }
    html, body { height: 100%; }
    body {
      background: var(--black);
      font-family: var(--font-body);
      color: #fff;
      display: flex;
      min-height: 100vh;
      overflow-x: hidden;
    }"""

new_body = """      --sidebar-w: 260px;
      --ease: cubic-bezier(0.16, 1, 0.3, 1);
      --t: 0.35s;
    }
    html, body { height: 100%; }
    body {
      background: var(--black);
      font-family: var(--font-body);
      color: #fff;
      min-height: 100vh;
      width: 100%;
      overflow-x: hidden;
    }"""

# 2. Update .admin-sidebar styling
old_sidebar = """    .admin-sidebar {
      width: var(--sidebar-w);
      background: rgba(7, 7, 7, 0.96);
      backdrop-filter: blur(20px);
      border-right: 1px solid var(--gold-border);
      display: flex;
      flex-direction: column;
      padding: 36px 0 28px;
      position: fixed;
      top: 0; bottom: 0; left: 0;
      z-index: 100;
      animation: sidebarIn 0.7s var(--ease) forwards;
    }"""

new_sidebar = """    .admin-sidebar {
      width: var(--sidebar-w);
      background: rgba(7, 7, 7, 0.96);
      backdrop-filter: blur(20px);
      border-right: 1px solid var(--gold-border);
      display: flex;
      flex-direction: column;
      padding: 24px 0 16px;
      position: fixed;
      top: 0; bottom: 0; left: 0;
      z-index: 100;
      overflow-y: auto;
      overflow-x: hidden;
      scrollbar-width: thin;
      scrollbar-color: rgba(212,175,55,0.3) transparent;
      animation: sidebarIn 0.7s var(--ease) forwards;
    }
    .admin-sidebar::-webkit-scrollbar {
      width: 4px;
    }
    .admin-sidebar::-webkit-scrollbar-track {
      background: transparent;
    }
    .admin-sidebar::-webkit-scrollbar-thumb {
      background: rgba(212,175,55,0.3);
      border-radius: 4px;
    }
    .admin-sidebar::-webkit-scrollbar-thumb:hover {
      background: rgba(212,175,55,0.6);
    }"""

# 3. Update sb-header, logo-ring, nav and footer sizing
old_sb_header = """    /* Sidebar header */
    .sb-header {
      text-align: center;
      padding: 0 24px 32px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 12px;
      position: relative;
    }
    .sb-logo-ring {
      width: 72px; height: 72px;
      margin: 0 auto 16px;
      position: relative;
    }"""

new_sb_header = """    /* Sidebar header */
    .sb-header {
      text-align: center;
      padding: 0 18px 20px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 10px;
      position: relative;
      flex-shrink: 0;
    }
    .sb-logo-ring {
      width: 58px; height: 58px;
      margin: 0 auto 12px;
      position: relative;
    }"""

# 4. Nav link padding
old_nav = """    /* Nav */
    .admin-nav { list-style: none; flex: 1; padding: 0 12px; }
    .admin-nav li { margin-bottom: 4px; }
    .admin-nav-link {
      display: flex; align-items: center; gap: 14px;
      padding: 14px 20px;
      color: var(--w40);
      text-decoration: none;
      font-size: 0.9rem; font-weight: 500;
      border-radius: var(--radius-md);
      transition: all var(--t) var(--ease);
      position: relative; overflow: hidden;
    }"""

new_nav = """    /* Nav */
    .admin-nav { list-style: none; padding: 0 10px; }
    .admin-nav li { margin-bottom: 3px; }
    .admin-nav-link {
      display: flex; align-items: center; gap: 12px;
      padding: 10px 14px;
      color: var(--w40);
      text-decoration: none;
      font-size: 0.85rem; font-weight: 500;
      border-radius: var(--radius-md);
      transition: all var(--t) var(--ease);
      position: relative; overflow: hidden;
    }"""

# 5. Nav icon
old_nav_icon = """    .admin-nav-link .nav-icon {
      width: 36px; height: 36px; border-radius: 10px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      display: flex; align-items: center; justify-content: center;
      transition: all var(--t) ease; flex-shrink: 0;
    }"""

new_nav_icon = """    .admin-nav-link .nav-icon {
      width: 32px; height: 32px; border-radius: 8px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      display: flex; align-items: center; justify-content: center;
      transition: all var(--t) ease; flex-shrink: 0;
      font-size: 0.95rem;
    }"""

# 6. Nav section label & footer
old_nav_sec = """    /* Nav section label */
    .nav-section-label {
      font-size: 0.65rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 2px;
      color: rgba(255,255,255,0.2);
      padding: 16px 20px 8px;
    }

    /* Sidebar footer */
    .sb-footer { padding: 20px 24px 0; border-top: 1px solid var(--border); margin: 0 0; }
    .sb-stat {
      display: flex; align-items: center; justify-content: space-between;
      padding: 8px 0;
      font-size: 0.8rem; color: var(--w40);
    }
    .sb-stat-val { color: var(--gold); font-weight: 600; }
    .admin-logout {
      margin-top: 16px;
    }
    .logout-btn {
      width: 100%;
      display: flex; align-items: center; gap: 10px; justify-content: center;
      padding: 12px;
      background: rgba(255,74,74,0.08);
      border: 1px solid rgba(255,74,74,0.2);
      border-radius: var(--radius-md);
      color: #ff5757;
      text-decoration: none;
      font-size: 0.85rem; font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
    }"""

new_nav_sec = """    /* Nav section label */
    .nav-section-label {
      font-size: 0.62rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 1.8px;
      color: rgba(255,255,255,0.25);
      padding: 12px 14px 6px;
    }

    /* Sidebar footer */
    .sb-footer {
      padding: 14px 16px 0;
      border-top: 1px solid var(--border);
      margin-top: auto;
      flex-shrink: 0;
    }
    .sb-stat {
      display: flex; align-items: center; justify-content: space-between;
      padding: 6px 0;
      font-size: 0.78rem; color: var(--w40);
    }
    .sb-stat-val { color: var(--gold); font-weight: 600; }
    .admin-logout {
      margin-top: 12px;
    }
    .logout-btn {
      width: 100%;
      display: flex; align-items: center; gap: 8px; justify-content: center;
      padding: 10px;
      background: rgba(255,74,74,0.08);
      border: 1px solid rgba(255,74,74,0.2);
      border-radius: var(--radius-md);
      color: #ff5757;
      text-decoration: none;
      font-size: 0.82rem; font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
    }"""

# 7. Main area & Top bar
old_main = """    /* ═ MAIN AREA ═ */
    .admin-main {
      flex: 1;
      margin-left: var(--sidebar-w);
      padding: 48px 56px;
      position: relative;
      z-index: 1;
    }

    /* Top bar */
    @keyframes slideDown { from { opacity:0; transform:translateY(-20px); } to { opacity:1; transform:translateY(0); } }
    .admin-topbar {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 48px;
      animation: slideDown 0.6s var(--ease) forwards;
    }"""

new_main = """    /* ═ MAIN AREA ═ */
    .admin-main {
      margin-left: var(--sidebar-w);
      width: calc(100% - var(--sidebar-w));
      max-width: calc(100% - var(--sidebar-w));
      min-width: 0;
      box-sizing: border-box;
      padding: 32px 36px;
      position: relative;
      z-index: 1;
      transition: margin-left 0.3s var(--ease), width 0.3s var(--ease), padding 0.3s var(--ease);
    }

    /* Top bar */
    @keyframes slideDown { from { opacity:0; transform:translateY(-20px); } to { opacity:1; transform:translateY(0); } }
    .admin-topbar {
      display: flex; align-items: center; justify-content: space-between;
      gap: 20px; flex-wrap: wrap;
      margin-bottom: 32px;
      animation: slideDown 0.6s var(--ease) forwards;
    }
    .topbar-right-panel {
      display: flex; align-items: center; gap: 16px; flex-shrink: 0;
    }"""

# 8. Division hub bar & buttons
old_div_hub = """    /* ═ UNIFIED MULTI-DIVISION SWITCHER ═ */
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
    }"""

new_div_hub = """    /* ═ UNIFIED MULTI-DIVISION SWITCHER ═ */
    .division-hub-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      padding: 4px 0 16px;
      margin-bottom: 24px;
    }
    .div-hub-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(22, 22, 22, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: var(--radius-lg);
      padding: 9px 15px;
      color: #fff;
      font-family: var(--font-body);
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all var(--t) var(--ease);
      backdrop-filter: blur(10px);
      flex-shrink: 0;
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
    .div-hub-btn .div-icon { font-size: 1.1rem; }
    .div-hub-btn .div-tag {
      font-size: 0.62rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 2px 7px;
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      color: rgba(255,255,255,0.6);
    }
    .div-hub-btn.active .div-tag {
      background: rgba(212,175,55,0.25);
      color: var(--gold-bright);
    }"""

# 9. Safety backup bar
old_safety = """    /* Safety & Backup Banner */
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
    }"""

new_safety = """    /* Safety & Backup Banner */
    .safety-backup-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      border-radius: var(--radius-md);
      padding: 12px 18px;
      margin-bottom: 24px;
    }
    .safety-backup-text {
      display: flex;
      align-items: center;
      gap: 10px;
      color: #34d399;
      font-size: 0.82rem;
      font-weight: 500;
      flex: 1;
      min-width: 260px;
    }
    .safety-backup-actions {
      display: flex;
      gap: 10px;
      flex-shrink: 0;
    }"""

# 10. Stats strip
old_stats = """    .stats-strip {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-bottom: 40px;
      animation: statsIn 0.6s 0.1s var(--ease) both;
    }"""

new_stats = """    .stats-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      margin-bottom: 32px;
      animation: statsIn 0.6s 0.1s var(--ease) both;
    }"""

# 11. Admin grid & card
old_grid = """    /* Grid layout */
    .admin-grid {
      display: grid;
      grid-template-columns: 1fr 420px;
      gap: 28px;
    }

    /* Cards */
    .admin-card {
      background: rgba(12,12,12,0.8);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      padding: 32px;
      transition: all var(--t) var(--ease);
      position: relative;
      overflow: hidden;
    }"""

new_grid = """    /* Grid layout */
    .admin-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(320px, 1fr);
      gap: 24px;
      align-items: start;
    }

    /* Cards */
    .admin-card {
      background: rgba(12,12,12,0.8);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      padding: 28px;
      transition: all var(--t) var(--ease);
      position: relative;
      overflow: hidden;
      min-width: 0;
      word-break: break-word;
    }"""

# 12. Responsive media queries
old_resp = """    /* ═ RESPONSIVE ═ */
    .mobile-menu-btn { display: none; background: transparent; border: none; color: #fff; cursor: pointer; padding: 8px; margin-right: 16px; flex-shrink: 0; }
    .mobile-menu-btn svg { width: 28px; height: 28px; }
    @media(max-width: 992px) {
      .admin-sidebar { position: fixed; left: -100%; top: 0; bottom: 0; z-index: 100; transition: left 0.3s var(--ease); box-shadow: 10px 0 30px rgba(0,0,0,0.5); }
      .admin-sidebar.show { left: 0; }
      .admin-main { margin-left: 0; padding: 24px 20px; }
      .mobile-menu-btn { display: block; }
      .admin-topbar { flex-direction: column; align-items: flex-start; gap: 16px; margin-bottom: 32px; }
      .topbar-right-panel { display: flex; align-items: center; width: 100%; justify-content: space-between; }
      .admin-grid { grid-template-columns: 1fr; }
      .form-row { grid-template-columns: 1fr; }
      .sb-live { position: relative; margin-top: 10px; }
      .sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 99; backdrop-filter: blur(4px); opacity: 0; transition: opacity 0.3s; }
      .sidebar-overlay.show { display: block; opacity: 1; }
    }"""

new_resp = """    /* ═ RESPONSIVE ═ */
    .mobile-menu-btn { display: none; background: transparent; border: none; color: #fff; cursor: pointer; padding: 8px; margin-right: 16px; flex-shrink: 0; }
    .mobile-menu-btn svg { width: 28px; height: 28px; }

    @media (max-width: 1200px) {
      .admin-grid {
        grid-template-columns: 1fr;
      }
      .admin-main {
        padding: 28px 24px;
      }
    }

    @media(max-width: 992px) {
      .admin-sidebar {
        position: fixed;
        left: -100%;
        top: 0; bottom: 0;
        z-index: 200;
        width: 270px;
        transition: left 0.3s var(--ease);
        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
      }
      .admin-sidebar.show { left: 0; }
      .admin-main {
        margin-left: 0;
        width: 100%;
        max-width: 100%;
        padding: 20px 16px;
      }
      .mobile-menu-btn { display: block; }
      .admin-topbar { flex-direction: column; align-items: flex-start; gap: 16px; margin-bottom: 24px; }
      .topbar-right-panel { display: flex; align-items: center; width: 100%; justify-content: space-between; }
      .admin-grid { grid-template-columns: 1fr; }
      .form-row { grid-template-columns: 1fr; }
      .sb-live { position: relative; margin-top: 8px; }
      .sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 150; backdrop-filter: blur(4px); opacity: 0; transition: opacity 0.3s; }
      .sidebar-overlay.show { display: block; opacity: 1; }
      .stats-strip { grid-template-columns: 1fr; }
    }"""

# 13. Sidebar HTML footer wrapping
old_footer_html = """    </ul>

      <div class="sb-stat">
        <span>Blog Posts</span>
        <span class="sb-stat-val" id="sb-count-blog">0</span>
      </div>
      <div class="sb-stat">
        <span>Properties</span>
        <span class="sb-stat-val" id="sb-count-prop">0</span>
      </div>
      <div class="sb-stat">
        <span>Shop Products</span>
        <span class="sb-stat-val" id="sb-count-shop">0</span>
      </div>
      <div class="admin-logout" style="margin-top:16px;">
        <a href="#" id="logout-btn" class="logout-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Secure Logout
        </a>
      </div>
    </div>
  </aside>"""

new_footer_html = """    </ul>

    <div class="sb-footer">
      <div class="sb-stat">
        <span>Blog Posts</span>
        <span class="sb-stat-val" id="sb-count-blog">0</span>
      </div>
      <div class="sb-stat">
        <span>Properties</span>
        <span class="sb-stat-val" id="sb-count-prop">0</span>
      </div>
      <div class="sb-stat">
        <span>Shop Products</span>
        <span class="sb-stat-val" id="sb-count-shop">0</span>
      </div>
      <div class="admin-logout">
        <a href="#" id="logout-btn" class="logout-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Secure Logout
        </a>
      </div>
    </div>
  </aside>"""

replacements = [
    (old_body, new_body, "body & :root"),
    (old_sidebar, new_sidebar, "sidebar"),
    (old_sb_header, new_sb_header, "sb-header"),
    (old_nav, new_nav, "nav"),
    (old_nav_icon, new_nav_icon, "nav-icon"),
    (old_nav_sec, new_nav_sec, "nav-sec & sb-footer"),
    (old_main, new_main, "main area & topbar"),
    (old_div_hub, new_div_hub, "division hub"),
    (old_safety, new_safety, "safety backup"),
    (old_stats, new_stats, "stats strip"),
    (old_grid, new_grid, "admin grid"),
    (old_resp, new_resp, "responsive media queries"),
    (old_footer_html, new_footer_html, "sidebar HTML footer")
]

success_count = 0
for old, new, label in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f"[OK] Replaced: {label}")
        success_count += 1
    else:
        print(f"[FAIL] Could not find: {label}")

if success_count == len(replacements):
    with open('admin/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(content)
    print("\nAll replacements applied and saved cleanly with CRLF!")
else:
    print(f"\nAborting save: only {success_count}/{len(replacements)} found.")
    sys.exit(1)
