"""
Local dev server that handles Netlify-style _redirects for the REEL website.
Rewrites /article/* -> /article.html so blog slugs work locally.
Run with: python serve.py
Then open: http://localhost:3000
"""
import http.server
import socketserver
import os
import re
from urllib.parse import urlparse

PORT = 3000
WEBROOT = r'c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web'

class REELHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBROOT, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Rewrite /article/* and /article to /article.html
        if re.match(r'^/article(/.*)?$', path):
            self.path = '/article.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        # Try to serve as-is
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        # Clean log output
        print(f"  {self.address_string()} {format % args}")

os.chdir(WEBROOT)
with socketserver.TCPServer(("", PORT), REELHandler) as httpd:
    print(f"\n  REEL Local Server running at http://localhost:{PORT}")
    print(f"  Serving: {WEBROOT}")
    print(f"  /article/* routes -> article.html (slug URLs work!)")
    print(f"\n  Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
