#!/usr/bin/env python3
"""
REEL Website Terminal Previewer & Dev Server
Royalty Executive Empire Limited (REEL)

Usage:
  python preview.py                (Interactive Menu)
  python preview.py -t [page.html] (Terminal UI text preview)
  python preview.py -s [--open]    (Start local HTTP server)
  python preview.py -l             (List all pages)
"""

import os
import sys
import re
import html
import socket
import argparse
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Configure UTF-8 encoding for Windows terminal stdout/stderr
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Enable ANSI colors on Windows CMD / PowerShell
if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

# Color constants
GOLD = "\033[38;2;212;175;55m"
BRIGHT_GOLD = "\033[38;2;245;215;110m"
CYAN = "\033[38;2;90;200;250m"
GREEN = "\033[38;2;76;217;100m"
DIM = "\033[38;2;140;140;140m"
DARK = "\033[38;2;80;80;80m"
WHITE = "\033[38;2;240;240;240m"
BOLD = "\033[1m"
RESET = "\033[0m"

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def strip_tags(text):
    """Remove HTML tags, strip scripts/styles/svg, and decode HTML entities."""
    if not text:
        return ""
    clean = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<svg.*?</svg>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = html.unescape(clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def get_terminal_width():
    try:
        return min(os.get_terminal_size().columns, 90)
    except Exception:
        return 80

def draw_header(title="ROYALTY EXECUTIVE EMPIRE LIMITED (REEL)"):
    width = get_terminal_width()
    border = "═" * (width - 2)
    print(f"\n{GOLD}╔{border}╗{RESET}")
    print(f"{GOLD}║{BRIGHT_GOLD}{BOLD}{title.center(width - 2)}{RESET}{GOLD}║{RESET}")
    subtitle = "Building Empires • Shaping Futures • Leading Innovation"
    print(f"{GOLD}║{DIM}{subtitle.center(width - 2)}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{border}╝{RESET}\n")

def list_pages():
    """List all available HTML pages in the workspace with metadata."""
    files = [f for f in os.listdir(WORKSPACE_DIR) if f.endswith(".html")]
    files.sort()
    width = get_terminal_width()
    draw_header("AVAILABLE WEBSITE PAGES")
    
    print(f"{BOLD}{'#':<4} {'PAGE FILE':<30} {'SIZE':<10} {'PAGE TITLE'}{RESET}")
    print(f"{DIM}{'─'*width}{RESET}")
    
    for i, file in enumerate(files, 1):
        path = os.path.join(WORKSPACE_DIR, file)
        size_kb = os.path.getsize(path) / 1024
        
        # Read title
        title = "Untitled"
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                head = f.read(4096)
                m = re.search(r'<title>(.*?)</title>', head, re.IGNORECASE | re.DOTALL)
                if m:
                    title = strip_tags(m.group(1))
                    if len(title) > 38:
                        title = title[:36] + "…"
        except Exception:
            pass
        
        color = GOLD if file == "index.html" else WHITE
        print(f"{DIM}{i:<4}{RESET} {color}{BOLD}{file:<30}{RESET} {DIM}{size_kb:>6.1f} KB{RESET}  {DIM}{title}{RESET}")
        
    print(f"{DIM}{'─'*width}{RESET}")
    print(f"{CYAN}Total: {len(files)} HTML pages found in workspace.{RESET}\n")

def preview_page(filename="index.html"):
    """Parse and render a high-fidelity terminal preview of an HTML page."""
    path = os.path.join(WORKSPACE_DIR, filename)
    if not os.path.exists(path):
        matches = [f for f in os.listdir(WORKSPACE_DIR) if f.lower() == filename.lower()]
        if matches:
            path = os.path.join(WORKSPACE_DIR, matches[0])
            filename = matches[0]
        else:
            print(f"{GOLD}[!] File '{filename}' not found in workspace.{RESET}")
            return

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    width = get_terminal_width()

    # Metadata extraction
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = strip_tags(title_match.group(1)) if title_match else "No Title"

    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    desc = strip_tags(desc_match.group(1)) if desc_match else "No description provided."

    theme_match = re.search(r'<meta[^>]*name=["\']theme-color["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
    theme_color = theme_match.group(1) if theme_match else "#D4AF37"

    # Terminal UI Header
    draw_header(f"TERMINAL PREVIEW: {filename.upper()}")

    print(f"{GOLD}╭─ META & SEO ─────────────────────────────────────────────────────────────╮{RESET}")
    print(f"{GOLD}│{RESET} {BOLD}Page Title :{RESET} {WHITE}{title}{RESET}")
    print(f"{GOLD}│{RESET} {BOLD}Theme Color:{RESET} {GOLD}{theme_color}{RESET}")
    print(f"{GOLD}│{RESET} {BOLD}Description:{RESET} {DIM}{desc[:width-16]}...{RESET}" if len(desc) > width-16 else f"{GOLD}│{RESET} {BOLD}Description:{RESET} {DIM}{desc}{RESET}")
    print(f"{GOLD}╰──────────────────────────────────────────────────────────────────────────╯{RESET}\n")

    # Clean Top-level Nav Links extraction
    nav_items = []
    for m in re.finditer(r'<a\s+[^>]*?class=["\'][^"\']*(?:nav-link|nav-btn-contact)[^"\']*["\'][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL):
        tag_text = m.group(0)
        href_match = re.search(r'href=["\']([^"\']*)["\']', tag_text, re.IGNORECASE)
        href = href_match.group(1) if href_match else "#"
        label = strip_tags(m.group(1))
        # Keep only clean navigation labels
        if label and len(label) < 25 and not any(x[0] == label for x in nav_items):
            nav_items.append((label, href))

    if nav_items:
        print(f"{CYAN}┌─ TOP NAVIGATION ────────────────────────────────────────────────────────┐{RESET}")
        nav_line = "  │  ".join([f"{BOLD}{t}{RESET} {DIM}({h}){RESET}" for t, h in nav_items])
        print(f"  {nav_line}")
        print(f"{CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    # Extract Page Hero (h1 and subtitle)
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if h1_match:
        h1_text = strip_tags(h1_match.group(1))
        sub_match = re.search(r'<h1[^>]*>.*?</h1>\s*<(?:p|div)[^>]*class=["\'][^"\']*(?:sub|lead|subtitle)[^"\']*["\'][^>]*>(.*?)</(?:p|div)>', content, re.IGNORECASE | re.DOTALL)
        if not sub_match:
            sub_match = re.search(r'<h1[^>]*>.*?</h1>\s*<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        sub_text = strip_tags(sub_match.group(1)) if sub_match else ""

        print(f"{BRIGHT_GOLD}╔═══════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BRIGHT_GOLD}║                              ★ PAGE HERO ★                               ║{RESET}")
        print(f"{BRIGHT_GOLD}╚═══════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"\n   {BOLD}{WHITE}✦ {h1_text} ✦{RESET}")
        if sub_text:
            print(f"   {GOLD}« {sub_text} »{RESET}\n")

    # If Division Cards present in body
    div_articles = re.findall(
        r'<article[^>]*class=["\'][^"\']*division-card[^"\']*["\'][^>]*>(.*?)</article>',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if div_articles:
        print(f"{GOLD}┌── CORE DIVISIONS ───────────────────────────────────────────────────────┐{RESET}")
        for art in div_articles:
            num_match = re.search(r'<div class=["\']div-label["\']>(.*?)</div>', art, re.I | re.DOTALL)
            h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', art, re.I | re.DOTALL)
            p_match = re.search(r'<p[^>]*>(.*?)</p>', art, re.I | re.DOTALL)
            cta_match = re.search(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*class=["\']div-cta-link["\'][^>]*>(.*?)</a>', art, re.I | re.DOTALL)

            num_str = strip_tags(num_match.group(1)) if num_match else ""
            h3_str = strip_tags(h3_match.group(1)) if h3_match else "Division"
            p_str = strip_tags(p_match.group(1)) if p_match else ""
            link_href = cta_match.group(1) if cta_match else ""

            print(f"  {GOLD}▶ [{num_str}] {BOLD}{h3_str}{RESET} {DIM}({link_href}){RESET}")
            print(f"    {WHITE}{p_str}{RESET}\n")
        print(f"{GOLD}└───" + "─" * (width - 6) + f"┘{RESET}\n")

    # Extract Key Headings (h2) and Context across the page
    h2_matches = list(re.finditer(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL))
    if h2_matches:
        print(f"{WHITE}{BOLD}KEY CONTENT SECTIONS:{RESET}")
        for m in h2_matches[:10]:
            h2_text = strip_tags(m.group(1))
            if not h2_text or h2_text in ["Our Divisions"]:
                continue
            
            pos = m.end()
            p_match = re.search(r'<p[^>]*>(.*?)</p>', content[pos:pos+2500], re.IGNORECASE | re.DOTALL)
            p_text = strip_tags(p_match.group(1)) if p_match else ""
            if len(p_text) > 130:
                p_text = p_text[:127] + "..."

            print(f"  {GOLD}● {BOLD}{h2_text}{RESET}")
            if p_text:
                print(f"    {DIM}↳ {p_text}{RESET}")

    # Extract Products if in Shop
    products = re.findall(r'<h3[^>]*class=["\'][^"\']*(?:product-title|card-title)[^"\']*["\'][^>]*>(.*?)</h3>', content, re.IGNORECASE | re.DOTALL)
    if products:
        print(f"\n{GOLD}┌── FEATURED PRODUCTS ──────────────────────────────────────────────────┐{RESET}")
        for p in products[:6]:
            print(f"  {CYAN}🛍️  {strip_tags(p)}{RESET}")
        print(f"{GOLD}└────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    # Extract Contact Information if found
    phone_m = re.search(r'href=["\']tel:([^"\']*)["\']', content, re.I)
    mail_m = re.search(r'href=["\']mailto:([^"\']*)["\']', content, re.I)
    if phone_m or mail_m:
        print(f"{CYAN}┌── DIRECT CONTACT ───────────────────────────────────────────────────────┐{RESET}")
        if phone_m:
            print(f"  {BOLD}Phone :{RESET} {GREEN}{phone_m.group(1)}{RESET}")
        if mail_m:
            print(f"  {BOLD}Email :{RESET} {WHITE}{mail_m.group(1)}{RESET}")
        print(f"{CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}\n")

    # Stats & Assets Overview
    img_count = len(re.findall(r'<img\s+', content, re.IGNORECASE))
    css_count = len(re.findall(r'<link[^>]*rel=["\']stylesheet["\']', content, re.IGNORECASE))
    js_count = len(re.findall(r'<script\s+src=', content, re.IGNORECASE))
    links_count = len(re.findall(r'<a\s+href=', content, re.IGNORECASE))

    print(f"{DIM}{'─'*width}{RESET}")
    print(f"{BOLD}Page Stats:{RESET} {CYAN}{img_count} Images{RESET} • {GOLD}{css_count} Stylesheets{RESET} • {GREEN}{js_count} Scripts{RESET} • {WHITE}{links_count} Hyperlinks{RESET}")
    print(f"{DIM}{'─'*width}{RESET}\n")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def find_available_port(start_port=8080, max_attempts=50):
    for p in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', p)) != 0:
                return p
    return start_port

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Support SPA fallback for /reel-global-palace/
        path_without_query = self.path.split('?')[0]
        if path_without_query.startswith('/reel-global-palace'):
            local_rel = path_without_query.lstrip('/')
            full_path = os.path.join(WORKSPACE_DIR, local_rel)
            if not os.path.exists(full_path):
                self.path = '/reel-global-palace/index.html'
        return super().do_GET()

    def log_message(self, format, *args):
        code = args[1] if len(args) > 1 else ""
        color = GREEN if code.startswith("2") else (GOLD if code.startswith("3") else DIM)
        sys.stdout.write(f"  {color}[HTTP {code}]{RESET} {args[0]} - {self.address_string()}\n")
        sys.stdout.flush()

def start_server(port=None, auto_open=False):
    """Start local web server for terminal preview."""
    if port is None:
        port = find_available_port(8080)

    os.chdir(WORKSPACE_DIR)
    local_ip = get_local_ip()

    draw_header("LOCAL PREVIEW SERVER STARTED")
    width = get_terminal_width()

    print(f"{GREEN}✓ Web server is live!{RESET}")
    print(f"{BOLD}Local URL   :{RESET} {CYAN}http://localhost:{port}/{RESET}")
    print(f"{BOLD}Network URL :{RESET} {CYAN}http://{local_ip}:{port}/{RESET}")
    print(f"{BOLD}Root Dir    :{RESET} {DIM}{WORKSPACE_DIR}{RESET}\n")

    print(f"{GOLD}Quick Preview Links:{RESET}")
    print(f"  • Home Page           : {WHITE}http://localhost:{port}/index.html{RESET}")
    print(f"  • REEL Global Palace  : {BRIGHT_GOLD}http://localhost:{port}/reel-global-palace/{RESET}")
    print(f"  • Real Estate         : {WHITE}http://localhost:{port}/real-estate.html{RESET}")
    print(f"  • About Page          : {WHITE}http://localhost:{port}/about.html{RESET}")
    print(f"  • Shop                : {WHITE}http://localhost:{port}/shop.html{RESET}")
    print(f"  • Blog                : {WHITE}http://localhost:{port}/blog.html{RESET}")
    print(f"  • Contact Us          : {WHITE}http://localhost:{port}/contact.html{RESET}")
    print(f"  • Admin Portal        : {WHITE}http://localhost:{port}/admin/{RESET}\n")

    print(f"{DIM}Press [Ctrl + C] in this terminal to stop the server.{RESET}")
    print(f"{DIM}{'─'*width}{RESET}\n")

    if auto_open:
        webbrowser.open(f"http://localhost:{port}/")

    try:
        httpd = HTTPServer(('0.0.0.0', port), CustomHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{GOLD}[*] Web server stopped successfully.{RESET}\n")

def interactive_menu():
    while True:
        draw_header("REEL WEBSITE TERMINAL HUB")
        print(f"{BOLD}Choose an action:{RESET}")
        print(f"  {GOLD}[1]{RESET} {BOLD}Preview website in terminal{RESET} (Text/ANSI rendered view of index.html)")
        print(f"  {GOLD}[2]{RESET} {BOLD}Start local preview web server{RESET} (http://localhost:8080)")
        print(f"  {GOLD}[3]{RESET} {BOLD}Start local server & open browser{RESET}")
        print(f"  {GOLD}[4]{RESET} {BOLD}List all website pages{RESET}")
        print(f"  {GOLD}[5]{RESET} {BOLD}Preview specific page in terminal{RESET}")
        print(f"  {DIM}[Q] Quit{RESET}\n")

        try:
            choice = input(f"{CYAN}Enter option (1-5 or Q): {RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if choice in ['1', 't']:
            preview_page("index.html")
            input(f"\n{DIM}Press Enter to return to menu...{RESET}")
        elif choice == '2':
            start_server(auto_open=False)
            break
        elif choice == '3':
            start_server(auto_open=True)
            break
        elif choice in ['4', 'l']:
            list_pages()
            input(f"\n{DIM}Press Enter to return to menu...{RESET}")
        elif choice == '5':
            list_pages()
            p = input(f"{CYAN}Enter HTML filename to preview (e.g. about.html): {RESET}").strip()
            if p:
                if not p.endswith(".html"):
                    p += ".html"
                preview_page(p)
            input(f"\n{DIM}Press Enter to return to menu...{RESET}")
        elif choice in ['q', 'exit']:
            print("Goodbye!")
            break

def main():
    parser = argparse.ArgumentParser(description="REEL Website Terminal Previewer & Dev Server")
    parser.add_argument("-t", "--terminal", nargs="?", const="index.html", help="Render terminal preview of a page (default: index.html)")
    parser.add_argument("-s", "--serve", action="store_true", help="Start local preview HTTP server")
    parser.add_argument("-p", "--port", type=int, default=None, help="Port to run HTTP server on (default: auto)")
    parser.add_argument("-o", "--open", action="store_true", help="Auto-open in browser when starting server")
    parser.add_argument("-l", "--list", action="store_true", help="List all HTML pages in website")

    args = parser.parse_args()

    if args.list:
        list_pages()
    elif args.terminal:
        preview_page(args.terminal)
    elif args.serve:
        start_server(port=args.port, auto_open=args.open)
    else:
        if sys.stdin.isatty():
            interactive_menu()
        else:
            preview_page("index.html")

if __name__ == "__main__":
    main()
