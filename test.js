<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Admin Dashboard | REEL</title>
  <link rel="icon" type="image/png" href="/Images/BG/logo%20bg.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --gold: #D4AF37;
      --gold-bright: #F0CC55;
      --gold-dim: rgba(212,175,55,0.12);
      --gold-border: rgba(212,175,55,0.22);
      --gold-glow: 0 0 30px rgba(212,175,55,0.25);
      --black: #080808;
      --surface: rgba(14,14,14,0.9);
      --surface-hover: rgba(22,22,22,0.95);
      --border: rgba(255,255,255,0.06);
      --w40: rgba(255,255,255,0.4);
      --w60: rgba(255,255,255,0.6);
      --font-display: 'Cormorant Garamond', serif;
      --font-body: 'Outfit', sans-serif;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --radius-xl: 24px;
      --sidebar-w: 280px;
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
    }

    /* ═ BACKGROUND ═ */
    .bg-canvas {
      position: fixed; inset: 0; z-index: 0; pointer-events: none;
    }
    .bg-orb {
      position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.18;
    }
    .bg-orb-1 {
      width: 700px; height: 700px;
      background: radial-gradient(circle, rgba(212,175,55,0.6), transparent 70%);
      top: -200px; right: -200px;
      animation: bgDrift1 15s ease-in-out infinite alternate;
    }
    .bg-orb-2 {
      width: 400px; height: 400px;
      background: radial-gradient(circle, rgba(212,175,55,0.4), transparent 70%);
      bottom: -100px; left: 50px;
      animation: bgDrift2 12s ease-in-out infinite alternate-reverse;
    }
    @keyframes bgDrift1 { from { transform: translate(0,0); } to { transform: translate(-30px, 20px); } }
    @keyframes bgDrift2 { from { transform: translate(0,0); } to { transform: translate(20px, -30px); } }
    .grid-bg {
      position: fixed; inset: 0; z-index: 0;
      background: #080808;
    }

    /* ═ SIDEBAR ═ */
    @keyframes sidebarIn {
      from { transform: translateX(-100%); opacity: 0; }
      to   { transform: translateX(0); opacity: 1; }
    }
    .admin-sidebar {
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
    }
    /* Gold shimmer strip on left edge */
    .admin-sidebar::before {
      content: '';
      position: absolute;
      left: 0; top: 0; bottom: 0;
      width: 2px;
      background: linear-gradient(180deg, transparent, var(--gold), rgba(212,175,55,0.4), var(--gold), transparent);
    }

    /* Sidebar header */
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
    }
    @keyframes ringRot { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes ringRotRev { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }
    .sb-ring-outer {
      position: absolute; inset: 0; border-radius: 50%;
      border: 1.5px solid transparent;
      border-top-color: var(--gold);
      border-right-color: rgba(212,175,55,0.2);
      animation: ringRot 3s linear infinite;
    }
    .sb-ring-inner {
      position: absolute; inset: 6px; border-radius: 50%;
      border: 1px solid transparent;
      border-bottom-color: rgba(212,175,55,0.7);
      animation: ringRotRev 2s linear infinite;
    }
    .sb-ring-core {
      position: absolute; inset: 12px;
      border-radius: 50%;
      background: var(--gold-dim);
      display: flex; align-items: center; justify-content: center;
      overflow: hidden;
    }
    .sb-ring-core img { width: 36px; object-fit: contain; }
    .sb-brand { font-family: var(--font-display); font-size: 1.3rem; color: var(--gold); margin-bottom: 3px; }
    .sb-role {
      font-size: 0.68rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 2.5px;
      color: var(--w40);
    }
    /* Live badge */
    .sb-live {
      display: inline-flex; align-items: center; gap: 6px;
      margin-top: 10px;
      padding: 4px 10px;
      background: rgba(37,211,102,0.12);
      border: 1px solid rgba(37,211,102,0.3);
      border-radius: 999px;
      font-size: 0.7rem; font-weight: 600; color: #25D366;
    }
    .sb-live-dot {
      width: 6px; height: 6px;
      border-radius: 50%;
      background: #25D366;
      animation: livePulse 1.5s ease-in-out infinite;
    }
    @keyframes livePulse {
      0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(37,211,102,0.6); }
      50%        { opacity: 0.7; box-shadow: 0 0 0 5px rgba(37,211,102,0); }
    }

    /* Nav */
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
    }
    .admin-nav-link::before {
      content: '';
      position: absolute; inset: 0;
      background: linear-gradient(90deg, var(--gold-dim), transparent);
      opacity: 0;
      transition: opacity var(--t) ease;
    }
    .admin-nav-link:hover::before,
    .admin-nav-link.active::before { opacity: 1; }
    .admin-nav-link:hover,
    .admin-nav-link.active {
      color: var(--gold);
    }
    .admin-nav-link .nav-icon {
      width: 36px; height: 36px; border-radius: 10px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      display: flex; align-items: center; justify-content: center;
      transition: all var(--t) ease; flex-shrink: 0;
    }
    .admin-nav-link:hover .nav-icon,
    .admin-nav-link.active .nav-icon {
      background: var(--gold-dim);
      border-color: var(--gold-border);
      box-shadow: var(--gold-glow);
    }
    .admin-nav-link svg { width: 16px; height: 16px; }
    .nav-label { position: relative; z-index: 1; }
    /* Active indicator bar */
    .admin-nav-link.active::after {
      content: '';
      position: absolute; right: 0; top: 25%; bottom: 25%;
      width: 3px;
      background: var(--gold);
      border-radius: 3px 0 0 3px;
    }

    /* Nav section label */
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
    }
    .logout-btn:hover {
      background: rgba(255,74,74,0.16);
      border-color: rgba(255,74,74,0.4);
      transform: translateY(-1px);
      box-shadow: 0 4px 20px rgba(255,74,74,0.15);
    }
    .logout-btn svg { width: 16px; height: 16px; }

    /* ═ MAIN AREA ═ */
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
    }
    .topbar-greeting { font-size: 0.8rem; color: var(--w40); margin-bottom: 4px; }
    .topbar-title {
      font-family: var(--font-display);
      font-size: 2rem; color: #fff;
    }
    .topbar-title .gold { color: var(--gold); }
    .topbar-date {
      text-align: right;
      font-size: 0.8rem; color: var(--w40);
    }
    .topbar-date strong { display: block; font-size: 1.1rem; color: #fff; margin-top: 2px; letter-spacing: 0.5px; }
    .topbar-date small { display: block; font-size: 0.72rem; color: var(--w40); margin-top: 2px; }

    /* Timezone selector */
    .tz-selector-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 10px;
    }
    .tz-flag { font-size: 1.1rem; }
    #tz-select {
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--gold-border);
      border-radius: 8px;
      color: var(--gold);
      font-family: var(--font-body);
      font-size: 0.78rem;
      font-weight: 600;
      padding: 6px 30px 6px 10px;
      cursor: pointer;
      transition: all 0.3s;
      outline: none;
      -webkit-appearance: none;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='rgba(212,175,55,0.7)' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 8px center;
      background-size: 14px;
    }
    #tz-select:hover, #tz-select:focus {
      border-color: var(--gold);
      background-color: rgba(212,175,55,0.06);
      box-shadow: 0 0 0 3px rgba(212,175,55,0.1);
    }
    #tz-select option { background: #111; color: #fff; }

    /* Stats strip */
    @keyframes statsIn {
      from { opacity: 0; transform: translateY(20px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .stats-strip {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-bottom: 40px;
      animation: statsIn 0.6s 0.1s var(--ease) both;
    }
    .stat-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 24px 28px;
      display: flex; align-items: center; gap: 18px;
      transition: all var(--t) var(--ease);
      position: relative; overflow: hidden;
    }
    .stat-card::after {
      content: '';
      position: absolute; bottom: 0; left: 0; right: 0;
      height: 2px;
      background: var(--gold);
      transform: scaleX(0);
      transition: transform 0.4s ease;
    }
    .stat-card:hover { border-color: var(--gold-border); transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0,0,0,0.5), var(--gold-glow); }
    .stat-card:hover::after { transform: scaleX(1); }
    .stat-icon {
      width: 48px; height: 48px;
      border-radius: var(--radius-sm);
      background: var(--gold-dim);
      border: 1px solid var(--gold-border);
      display: flex; align-items: center; justify-content: center;
      color: var(--gold); flex-shrink: 0;
    }
    .stat-icon svg { width: 22px; height: 22px; }
    .stat-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--w40); margin-bottom: 4px; }
    .stat-value { font-family: var(--font-display); font-size: 2rem; color: #fff; line-height: 1; }
    .stat-hint { font-size: 0.72rem; color: var(--gold); margin-top: 3px; }

    /* ═ SECTIONS ═ */
    @keyframes sectionIn {
      from { opacity: 0; transform: translateY(24px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .admin-section { display: none; }
    .admin-section.active {
      display: block;
      animation: sectionIn 0.55s var(--ease) both;
    }
    .section-header {
      display: flex; align-items: center; gap: 14px;
      margin-bottom: 32px;
    }
    .section-icon {
      width: 44px; height: 44px;
      background: var(--gold-dim);
      border: 1px solid var(--gold-border);
      border-radius: var(--radius-sm);
      display: flex; align-items: center; justify-content: center;
      color: var(--gold);
    }
    .section-icon svg { width: 20px; height: 20px; }
    .section-header h1 {
      font-family: var(--font-display); font-size: 2.2rem;
    }
    .section-header p { color: var(--w40); font-size: 0.88rem; margin-top: 2px; }

    /* Grid layout */
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
    }
    .admin-card::before {
      content: '';
      position: absolute; top: 0; left: 0; right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);
    }
    .admin-card:hover {
      border-color: var(--gold-border);
      box-shadow: 0 24px 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(212,175,55,0.08);
    }
    .card-title {
      display: flex; align-items: center; gap: 10px;
      font-family: var(--font-display); font-size: 1.35rem; color: var(--gold);
      margin-bottom: 24px; padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }
    .card-title svg { width: 18px; height: 18px; }

    /* Form inputs */
    .form-group { margin-bottom: 18px; }
    .form-group label {
      display: block;
      font-size: 0.72rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 1.5px;
      color: var(--w40); margin-bottom: 8px;
    }
    .form-group input,
    .form-group textarea,
    .form-group select {
      width: 100%;
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: var(--radius-md);
      padding: 13px 16px;
      color: #fff;
      font-family: var(--font-body); font-size: 0.9rem;
      transition: all 0.3s ease;
      -webkit-appearance: none;
    }
    .form-group select {
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='rgba(212,175,55,0.7)' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 14px center;
      background-size: 16px;
      padding-right: 42px;
      cursor: pointer;
    }
    .form-group input::placeholder, .form-group textarea::placeholder { color: rgba(255,255,255,0.18); }
    .form-group textarea { min-height: 110px; resize: vertical; }
    .form-group input:focus,
    .form-group textarea:focus,
    .form-group select:focus {
      outline: none;
      border-color: var(--gold);
      background: rgba(212,175,55,0.04);
      box-shadow: 0 0 0 3px rgba(212,175,55,0.1), 0 4px 12px rgba(0,0,0,0.3);
    }
    .file-drop {
      padding: 20px;
      background: rgba(212,175,55,0.04);
      border: 1px dashed var(--gold-border);
      border-radius: var(--radius-md);
      cursor: pointer;
      text-align: center;
      font-size: 0.82rem; color: var(--w40);
      transition: all 0.3s;
    }
    .file-drop:hover { border-color: var(--gold); color: var(--gold); background: rgba(212,175,55,0.07); }

    /* Submit button */
    .btn-submit {
      width: 100%; padding: 15px;
      background: linear-gradient(135deg, #D4AF37 0%, #B8962E 50%, #D4AF37 100%);
      background-size: 200%;
      background-position: 0%;
      border: none; border-radius: var(--radius-md);
      color: #000; font-family: var(--font-body);
      font-size: 0.85rem; font-weight: 800;
      text-transform: uppercase; letter-spacing: 2px;
      cursor: pointer;
      transition: all 0.4s ease;
      box-shadow: 0 6px 20px rgba(212,175,55,0.2);
      display: flex; align-items: center; justify-content: center; gap: 8px;
      position: relative; overflow: hidden;
    }
    .btn-submit::before {
      content: '';
      position: absolute; inset: 0;
      background: linear-gradient(135deg, transparent, rgba(255,255,255,0.18), transparent);
      transform: translateX(-100%);
      transition: transform 0.5s ease;
    }
    .btn-submit:hover::before { transform: translateX(100%); }
    .btn-submit:hover {
      background-position: 100%;
      box-shadow: 0 10px 35px rgba(212,175,55,0.4);
      transform: translateY(-2px);
    }
    .btn-submit svg { width: 16px; height: 16px; }

    /* List */
    .admin-list { display: flex; flex-direction: column; gap: 10px; }
    .admin-list-item {
      display: flex; align-items: center; gap: 14px;
      padding: 14px 18px;
      background: rgba(255,255,255,0.025);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      transition: all 0.3s ease;
      position: relative; overflow: hidden;
      cursor: default;
    }
    .admin-list-item::before {
      content: '';
      position: absolute; left: 0; top: 0; bottom: 0;
      width: 3px;
      background: linear-gradient(180deg, var(--gold), rgba(212,175,55,0.3));
      transform: scaleY(0);
      transform-origin: top;
      transition: transform 0.3s ease;
    }
    .admin-list-item:hover::before { transform: scaleY(1); }
    .admin-list-item:hover {
      background: rgba(212,175,55,0.04);
      border-color: var(--gold-border);
      transform: translateX(4px);
    }
    .item-thumb {
      width: 40px; height: 40px;
      border-radius: 8px;
      background: var(--gold-dim);
      border: 1px solid var(--gold-border);
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0; color: var(--gold); font-size: 1.1rem;
      overflow: hidden;
    }
    .item-thumb img { width: 100%; height: 100%; object-fit: cover; }
    .item-info { flex: 1; min-width: 0; }
    .item-info strong {
      display: block; font-size: 0.88rem;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      color: #fff; transition: color 0.3s;
    }
    .admin-list-item:hover .item-info strong { color: var(--gold); }
    .item-info span { font-size: 0.75rem; color: var(--w40); }
    .btn-delete {
      background: rgba(255,74,74,0.08);
      border: 1px solid rgba(255,74,74,0.15);
      color: #ff5757;
      padding: 7px 13px;
      border-radius: 7px;
      font-size: 0.72rem; font-weight: 700;
      cursor: pointer; text-transform: uppercase; letter-spacing: 1px;
      transition: all 0.3s; flex-shrink: 0;
      display: flex; align-items: center; gap: 5px;
    }
    .btn-delete:hover {
      background: #ff5757; color: #fff;
      border-color: #ff5757;
      box-shadow: 0 4px 16px rgba(255,74,74,0.3);
      transform: translateY(-1px);
    }
    .btn-delete svg { width: 12px; height: 12px; }

    .empty-state {
      text-align: center; padding: 40px 20px;
      color: var(--w40);
      border: 1px dashed rgba(255,255,255,0.08);
      border-radius: var(--radius-lg);
    }
    .empty-state svg { width: 40px; height: 40px; color: rgba(212,175,55,0.3); margin: 0 auto 12px; display: block; }
    .empty-state p { font-size: 0.85rem; }

    /* Toast notification */
    @keyframes toastIn {
      from { opacity: 0; transform: translateX(100%); }
      to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes toastOut {
      from { opacity: 1; transform: translateX(0); }
      to   { opacity: 0; transform: translateX(100%); }
    }
    .toast {
      position: fixed; top: 28px; right: 28px; z-index: 9999;
      padding: 16px 22px;
      background: rgba(10,10,10,0.95);
      backdrop-filter: blur(16px);
      border: 1px solid var(--gold-border);
      border-radius: 14px;
      display: flex; align-items: center; gap: 12px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.7), inset 0 1px 0 rgba(212,175,55,0.1);
      animation: toastIn 0.4s var(--ease) forwards;
    }
    .toast.out { animation: toastOut 0.3s ease forwards; }
    .toast-icon { width: 34px; height: 34px; border-radius: 8px; background: var(--gold-dim); border: 1px solid var(--gold-border); display: flex; align-items: center; justify-content: center; color: var(--gold); flex-shrink: 0; }
    .toast-icon svg { width: 16px; height: 16px; }
    .toast-text { font-size: 0.88rem; }
    .toast-text strong { display: block; color: #fff; margin-bottom: 2px; }
    .toast-text span { color: var(--w40); font-size: 0.78rem; }
    
    /* ═ RESPONSIVE ═ */
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
    }
  
    /* --- NEW BROADCAST CENTER & SCHEDULER MODAL CSS --- */
    .broadcast-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-top: 24px;
    }
    @media (max-width: 992px) {
      .broadcast-container { grid-template-columns: 1fr; }
    }
    .bc-card {
      background: rgba(15, 15, 15, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 16px;
      padding: 24px;
      backdrop-filter: blur(10px);
    }
    .bc-card h3 {
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: rgba(255, 255, 255, 0.6);
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .bc-card h3 svg { width: 16px; height: 16px; }
    
    .bc-input {
      width: 100%;
      background: rgba(0,0,0,0.5);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 12px;
      padding: 16px;
      color: #fff;
      font-family: inherit;
      resize: none;
      min-height: 120px;
      margin-bottom: 8px;
    }
    .bc-input:focus {
      outline: none;
      border-color: rgba(212, 175, 55, 0.5);
    }
    .bc-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .bc-char-count {
      color: rgba(255,255,255,0.4);
      font-size: 0.8rem;
    }
    .bc-btn {
      background: rgba(212, 175, 55, 0.15);
      color: #D4AF37;
      border: 1px solid rgba(212, 175, 55, 0.3);
      padding: 10px 24px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 500;
      transition: all 0.3s ease;
    }
    .bc-btn:hover {
      background: rgba(212, 175, 55, 0.3);
    }
    
    .bc-preview-box {
      margin-top: 32px;
    }
    .bc-preview-box h4 {
      font-size: 0.75rem;
      color: rgba(255,255,255,0.4);
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .bc-preview-card {
      background: rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      border: 1px solid rgba(255,255,255,0.05);
    }
    .bc-preview-text {
      color: #fff;
      font-size: 0.95rem;
      font-style: italic;
    }
    
    .bc-history-subtitle {
      color: rgba(255,255,255,0.5);
      font-size: 0.85rem;
      margin-bottom: 24px;
      margin-top: -12px;
    }
    .bc-empty {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 200px;
      color: rgba(255,255,255,0.3);
      font-size: 0.9rem;
      gap: 12px;
    }
    
    /* MODAL CSS */
    .schedule-modal-overlay {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.8);
      backdrop-filter: blur(5px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 9999;
    }
    .schedule-modal {
      background: #111;
      border: 1px solid rgba(212,175,55,0.3);
      border-radius: 16px;
      padding: 32px;
      width: 400px;
      max-width: 90%;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
      text-align: center;
    }
    .schedule-modal h2 {
      color: #D4AF37;
      margin-bottom: 8px;
    }
    .schedule-modal p {
      color: rgba(255,255,255,0.6);
      font-size: 0.85rem;
      margin-bottom: 24px;
    }
    .schedule-modal input[type="datetime-local"] {
      width: 100%;
      padding: 12px;
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 8px;
      color: #fff;
      margin-bottom: 24px;
    }
    .schedule-modal-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
    }
    .schedule-modal-actions button {
      padding: 10px 20px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: bold;
    }
    .btn-cancel {
      background: transparent;
      border: 1px solid rgba(255,255,255,0.2);
      color: #fff;
    }
    .btn-confirm {
      background: #D4AF37;
      color: #000;
      border: none;
    }
    </style>
    

  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#D4AF37" />
  <link rel="apple-touch-icon" href="/Images/icons/icon-192x192.png" />
</head>
<body id="admin-dashboard">

  <div class="bg-canvas">
    <div class="bg-orb bg-orb-1"></div>
    <div class="bg-orb bg-orb-2"></div>
  </div>
  <div class="grid-bg"></div>

  <!-- ═ SIDEBAR ═ -->
  <aside class="admin-sidebar">
    <div class="sb-header">
      <div class="sb-logo-ring">
        <div class="sb-ring-outer"></div>
        <div class="sb-ring-inner"></div>
        <div class="sb-ring-core">
          <img src="../Images/BG/logo%20bg.png" alt="REEL" onerror="this.outerHTML='<span style=\'font-size:1.4rem\'>⚜</span>'" />
        </div>
      </div>
      <div class="sb-brand">REEL</div>
      <div class="sb-role">Admin Portal</div>
      <div class="sb-live">
        <span class="sb-live-dot"></span>
        Live System
      </div>
    </div>

    <div class="nav-section-label">Content Management</div>
    <ul class="admin-nav">
      <li>
        <a href="#" class="admin-nav-link active" data-target="sec-blog">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
            </svg>
          </div>
          <span class="nav-label">Manage Blog</span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-portfolio">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
            </svg>
          </div>
          <span class="nav-label">Portfolio</span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-shop">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
            </svg>
          </div>
          <span class="nav-label">Shop Products</span>
        </a>
      </li>

      <li>
        <a href="#" class="admin-nav-link" data-target="sec-scheduler">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <span class="nav-label">Scheduler</span>
        </a>
      </li>
          <li>
        <a href="#" class="admin-nav-link" data-target="sec-notifications">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </div>
          <span class="nav-label">Push Alerts</span>
        </a>
      </li>
    </ul>

    <div class="nav-section-label" style="margin-top:16px;">Inbox</div>
    <ul class="admin-nav">
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-orders">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          </div>
          <span class="nav-label">Orders <span id="orders-badge" style="background:rgba(212,175,55,0.2);color:var(--gold);padding:1px 7px;border-radius:999px;font-size:0.7rem;margin-left:4px;">0</span></span>
        </a>
      </li>
      <li>
        <a href="#" class="admin-nav-link" data-target="sec-messages">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          </div>
          <span class="nav-label">Messages <span id="msgs-badge" style="background:rgba(212,175,55,0.2);color:var(--gold);padding:1px 7px;border-radius:999px;font-size:0.7rem;margin-left:4px;">0</span></span>
        </a>
      </li>
    </ul>

      <div class="sb-stat">
        <span>Blog Posts</span>
        <span class="sb-stat-val" id="sb-count-blog">0</span>
      </div>
      <div class="sb-stat">
        <span>Portfolio Items</span>
        <span class="sb-stat-val" id="sb-count-pf">0</span>
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
  </aside>

  <!-- ═ MAIN AREA ═ -->
  <main class="admin-main">

    <!-- Top bar -->
    <div class="sidebar-overlay" id="sidebar-overlay"></div>
    <div class="admin-topbar">
      <div style="display:flex; align-items:center;">
        <button class="mobile-menu-btn" id="mobile-menu-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <div>
        <div class="topbar-greeting">Welcome back, CEO</div>
        <div class="topbar-title">Executive <span class="gold">Dashboard</span></div>
      </div>
      </div>
      <div class="topbar-right-panel">
      <div class="topbar-date">
        <strong id="topbar-time">—</strong>
        <small id="topbar-date-str">—</small>
        <div class="tz-selector-wrap">
          <span class="tz-flag" id="tz-flag">🌍</span>
          <select id="tz-select" title="Select Timezone">
            <optgroup label="🇳🇬 Nigeria">
              <option value="Africa/Lagos">Nigeria (WAT, UTC+1)</option>
            </optgroup>
            <optgroup label="🇦🇪 UAE">
              <option value="Asia/Dubai">Dubai (GST, UTC+4)</option>
            </optgroup>
            <optgroup label="🇬🇧 United Kingdom">
              <option value="Europe/London">London (GMT/BST)</option>
            </optgroup>
            <optgroup label="🇺🇸 USA">
              <option value="America/New_York">New York (EST/EDT)</option>
              <option value="America/Chicago">Chicago (CST/CDT)</option>
              <option value="America/Los_Angeles">Los Angeles (PST/PDT)</option>
            </optgroup>
            <optgroup label="🇿🇦 South Africa">
              <option value="Africa/Johannesburg">Johannesburg (SAST)</option>
            </optgroup>
            <optgroup label="🇬🇭 Ghana">
              <option value="Africa/Accra">Accra (GMT)</option>
            </optgroup>
            <optgroup label="🇰🇪 Kenya">
              <option value="Africa/Nairobi">Nairobi (EAT, UTC+3)</option>
            </optgroup>
            <optgroup label="🇸🇬 Singapore">
              <option value="Asia/Singapore">Singapore (SGT, UTC+8)</option>
            </optgroup>
            <optgroup label="🇨🇳 China">
              <option value="Asia/Shanghai">Shanghai (CST, UTC+8)</option>
            </optgroup>
          </select>
        </div>
      </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-strip">
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
          </svg>
        </div>
        <div>
          <div class="stat-label">Blog Posts</div>
          <div class="stat-value" id="stat-blog">0</div>
          <div class="stat-hint">Published</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
          </svg>
        </div>
        <div>
          <div class="stat-label">Portfolio</div>
          <div class="stat-value" id="stat-pf">0</div>
          <div class="stat-hint">Projects</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
        </div>
        <div>
          <div class="stat-label">Products</div>
          <div class="stat-value" id="stat-shop">0</div>
          <div class="stat-hint">In Shop</div>
        </div>
      </div>
    </div>

    <!-- ── BLOG ── -->
    <section id="sec-blog" class="admin-section active">
      <div class="section-header">
        <div class="section-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
          </svg>
        </div>
        <div>
          <h1>Blog Manager</h1>
          <p>Publish and manage news, insights, and stories for your audience.</p>
        </div>
      </div>
      <div class="admin-grid">
        <div class="admin-card">
          <div class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
            New Blog Post
          </div>
          <form id="form-blog">
            <div class="form-group">
              <label>Post Title</label>
              <input type="text" id="blog-title" placeholder="e.g. The Future of Luxury Real Estate" required />
            </div>
            <div class="form-group">
              <label>Category</label>
              <select id="blog-cat" required>
                <option value="Business">Business</option>
                <option value="Technology">Technology</option>
              </select>
            </div>
            <div class="form-group">
              <label>Cover Image File</label>
              <input type="file" id="blog-img" accept="image/*" required class="file-drop" />
            </div>
            <div class="form-group">
              <label>Image Focus (thumbnail position)</label>
              <select id="blog-img-pos">
                <option value="center center">Center (default)</option>
                <option value="top center">Top — show face/head</option>
                <option value="bottom center">Bottom</option>
                <option value="center left">Left side</option>
                <option value="center right">Right side</option>
              </select>
            </div>
            <div class="form-group">
              <label>Content
                <span style="float:right; display:flex; align-items:center; gap:10px;">
                  <span id="word-count-display" style="font-size:0.72rem; color:var(--w40); font-weight:500;">0 / 1000 words</span>
                  <span style="font-size:0.72rem; color:var(--w40); font-weight:700; text-transform:uppercase; letter-spacing:1px;">Limit</span>
                  <label style="position:relative; display:inline-block; width:38px; height:20px; cursor:pointer; margin:0;">
                    <input type="checkbox" id="word-limit-toggle" checked style="opacity:0;width:0;height:0;position:absolute;">
                    <span id="toggle-track" style="position:absolute;inset:0;border-radius:20px;background:rgba(212,175,55,0.7);transition:background 0.3s;"></span>
                    <span id="toggle-thumb" style="position:absolute;top:3px;left:3px;width:14px;height:14px;border-radius:50%;background:#fff;transition:transform 0.3s;"></span>
                  </label>
                </span>
              </label>
              <textarea id="blog-content" placeholder="Write your full blog post here…" required style="min-height:260px;"></textarea>
            </div>
            
            <div class="form-group" style="padding:15px; background:rgba(212,175,55,0.03); border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                Publishing Schedule
              </label>
              <select id="blog-status" style="margin-bottom:12px;">
                <option value="published">Publish Immediately</option>
                <option value="scheduled">Schedule for Later</option>
              </select>
              <div id="blog-schedule-wrap" style="display:none;">
                <label style="font-size:0.65rem;">Schedule Date & Time</label>
                <input type="datetime-local" id="blog-schedule-time" style="margin-bottom:5px;" />
                <span style="font-size:0.7rem; color:var(--w40);">Post will be hidden until this date/time passes.</span>
              </div>
            </div>
            <button type="submit" class="btn-submit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
              Publish Post
            </button>
          </form>
        </div>
        <div class="admin-card">
          <div class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            Published Posts
          </div>
          <div id="blog-list" class="admin-list"></div>
        </div>
      </div>
    </section>

    <!-- ── SCHEDULER ── -->
    <section id="sec-scheduler" class="admin-section">
      <div class="section-header">
        <div class="section-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <div>
          <h1>Content Scheduler</h1>
          <p>View and manage all upcoming scheduled content across the site.</p>
        </div>
      </div>
      <div class="admin-grid" style="grid-template-columns: 1fr;">
        <div class="admin-card">
          <div class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            Upcoming Scheduled Content
          </div>
          <div id="scheduler-list" class="admin-list">
             <!-- Scheduled items injected here -->
          </div>
        </div>
      </div>
    </section>

    <!-- ── PORTFOLIO ── -->
    <section id="sec-portfolio" class="admin-section">
      <div class="section-header">
        <div class="section-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
          </svg>
        </div>
        <div>
          <h1>Portfolio Manager</h1>
          <p>Upload completed projects and executive achievements by division.</p>
        </div>
      </div>
      <div class="admin-grid">
        <div class="admin-card">
          <div class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
            Add New Project
          </div>
          <form id="form-portfolio">
            <div class="form-group">
              <label>Project Title</label>
              <input type="text" id="pf-title" placeholder="e.g. Marina Luxury Villas, Dubai" required />
            </div>
            <div class="form-group">
              <label>Division</label>
              <select id="pf-cat" required>
                <option value="REEL Branding">REEL Branding</option>
                <option value="REEL Power">REEL Power</option>
              </select>
            </div>
            <div class="form-group">
              <label>Project Image File</label>
              <input type="file" id="pf-img" accept="image/*" required class="file-drop" />
            </div>
            <div class="form-group">
              <label>Image Focus (thumbnail position)</label>
              <select id="pf-img-pos">
                <option value="center center">Center (default)</option>
                <option value="top center">Top — show face/head</option>
                <option value="bottom center">Bottom</option>
                <option value="center left">Left side</option>
                <option value="center right">Right side</option>
              </select>
            </div>
            
            <div class="form-group" style="padding:15px; background:rgba(212,175,55,0.03); border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                Publishing Schedule
              </label>
              <select id="portfolio-status" style="margin-bottom:12px;">
                <option value="published">Publish Immediately</option>
                <option value="scheduled">Schedule for Later</option>
              </select>
              <div id="portfolio-schedule-wrap" style="display:none;">
                <label style="font-size:0.65rem;">Schedule Date & Time</label>
                <input type="datetime-local" id="portfolio-schedule-time" style="margin-bottom:5px;" />
                <span style="font-size:0.7rem; color:var(--w40);">Project will be hidden until this date/time passes.</span>
              </div>
            </div>
            <button type="submit" btn-submit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              Add Project
            </button>
          </form>
        </div>
        <div class="admin-card">
          <div class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            Live Portfolio
          </div>
          <div id="portfolio-list" class="admin-list"></div>
        </div>
      </div>
    </section>

    <!-- ── SHOP ── -->
    <section id="sec-shop" class="admin-section">
      <div class="section-header">
        <div class="section-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
        </div>
        <div>
          <h1>Shop Manager</h1>
          <p>Add luxury products, set executive pricing, and manage inventory.</p>
        </div>
      </div>
      <div class="admin-grid">
        <div class="admin-card">
          <div class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
            Add New Product
          </div>
          <form id="form-shop">
            <div class="form-group">
              <label>Product Name</label>
              <input type="text" id="shop-name" placeholder="e.g. Executive Leather Briefcase" required />
            </div>
            <div class="form-group">
              <label>Price (USD $)</label>
              <input type="number" step="0.01" id="shop-price" placeholder="e.g. 299.99" required />
            </div>
            <div class="form-group">
              <label>Category</label>
              <select id="shop-cat" required>
                <option value="Electronics">Electronics</option>
                <option value="Corporate Gifts">Corporate Gifts</option>
                <option value="Apparel">Apparel</option>
                <option value="Accessories">Accessories</option>
              </select>
            </div>
            <div class="form-group">
              <label>Product Image File</label>
              <input type="file" id="shop-img" accept="image/*" required class="file-drop" />
            </div>
            <div class="form-group">
              <label>Image Focus (thumbnail position)</label>
              <select id="shop-img-pos">
                <option value="center center">Center (default)</option>
                <option value="top center">Top — show face/head</option>
                <option value="bottom center">Bottom</option>
                <option value="center left">Left side</option>
                <option value="center right">Right side</option>
              </select>
            </div>
            
            <div class="form-group" style="padding:15px; background:rgba(212,175,55,0.03); border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                Publishing Schedule
              </label>
              <select id="shop-status" style="margin-bottom:12px;">
                <option value="published">Publish Immediately</option>
                <option value="scheduled">Schedule for Later</option>
              </select>
              <div id="shop-schedule-wrap" style="display:none;">
                <label style="font-size:0.65rem;">Schedule Date & Time</label>
                <input type="datetime-local" id="shop-schedule-time" style="margin-bottom:5px;" />
                <span style="font-size:0.7rem; color:var(--w40);">Product will be hidden until this date/time passes.</span>
              </div>
            </div>
            <button type="submit" btn-submit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
              Add to Shop
            </button>
          </form>
        </div>
        <div class="admin-card">
          <div class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            Live Products
          </div>
          <div id="product-list" class="admin-list"></div>
        </div>
      </div>
    </section>



    <!-- ── ORDERS ── -->
    <section id="sec-orders" class="admin-section">
      <div class="section-header">
        <div class="section-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
        </div>
        <div>
          <h1>Order Management</h1>
          <p>Review and process incoming shop orders.</p>
        </div>
      </div>
      <div class="admin-card" style="margin-top:24px;">
        <div class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          Incoming Orders
        </div>
        <div id="orders-list" class="admin-list">
          <div class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <p>Order history will appear here once the WhatsApp checkout logic integrates with Firebase in the future.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── MESSAGES ── -->
    <section id="sec-messages" class="admin-section">
      <div class="section-header">
        <div class="section-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        </div>
        <div>
          <h1>Contact Messages</h1>
          <p>Read messages submitted through the website contact form.</p>
        </div>
      </div>
      <div class="admin-card" style="margin-top:24px;">
        <div class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          Inbox
        </div>
        <div id="messages-list" class="admin-list">
          <div class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <p>Loading messages...</p>
          </div>
        </div>
      </div>
    </section>

  
    <!-- ── PUSH NOTIFICATIONS ── -->
    
    <!-- ── PUSH NOTIFICATIONS ── -->
    <section id="sec-notifications" class="admin-section">
      <div class="section-header">
        <div>
          <h1 style="font-family: 'Cormorant Garamond', serif; font-size:2.5rem;">Broadcast Center</h1>
          <p style="color:rgba(255,255,255,0.5);">Communicate directly with your users in real time</p>
        </div>
      </div>
      
      <div class="broadcast-container">
        <!-- Left Panel: Sender -->
        <div class="bc-card">
          <h3>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
            SEND A NEW MESSAGE
          </h3>
          <textarea id="bc-input" class="bc-input" placeholder="Write your message here... e.g. '🎉 New arrivals just dropped! Shop now for exclusive deals.'"></textarea>
          <div class="bc-footer">
            <span class="bc-char-count" id="bc-count">0/300</span>
            <button class="bc-btn" id="bc-send-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
              Send Broadcast
            </button>
          </div>
          
          <div class="bc-preview-box">
            <h4>PREVIEW</h4>
            <div class="bc-preview-card">
              <svg viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="2" width="20" height="20"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path></svg>
              <span class="bc-preview-text" id="bc-preview">Your message will appear here...</span>
            </div>
          </div>
        </div>
        
        <!-- Right Panel: History -->
        <div class="bc-card" style="display:flex; flex-direction:column;">
          <h3>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
            History & Status
          </h3>
          <p class="bc-history-subtitle">Active notifications appear on customer screens instantly.</p>
          
          <div id="bc-history-list" style="flex:1; overflow-y:auto;">
            <div class="bc-empty">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="32" height="32"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path></svg>
              No broadcast history found
            </div>
          </div>
        </div>
      </div>
    </section>
    
    
  </main>

  <!-- SCHEDULER MODAL -->
  <div class="schedule-modal-overlay" id="schedule-modal-overlay">
    <div class="schedule-modal">
      <h2>📅 Schedule Publish Time</h2>
      <p>Select exactly when you want this post to go live on the website.</p>
      <input type="datetime-local" id="global-schedule-time" />
      <div class="schedule-modal-actions">
        <button class="btn-cancel" onclick="closeScheduleModal()">Cancel</button>
        <button class="btn-confirm" onclick="confirmScheduleTime()">✓ Set Time</button>
      </div>
    </div>
  </div>

  <!-- Firebase Integration -->
  <script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js">