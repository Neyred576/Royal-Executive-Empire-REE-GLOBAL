import os, re

instagram_column_html = """          <!-- Footer Instagram Feed -->
          <div class="footer-col footer-insta-col">
            <h3 class="footer-heading">Instagram</h3>
            <div class="footer-insta-card" aria-label="Official Instagram feed">
              <div class="insta-header">
                <div class="insta-user-info">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" class="insta-icon">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                  </svg>
                  <span class="insta-handle">@reelholding</span>
                </div>
                <span class="insta-badge">Official</span>
              </div>
              <div class="insta-grid">
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="REEL Properties on Instagram">
                  <img src="Images/real_estate_hero.png" alt="REEL Luxury Properties" loading="lazy" />
                  <div class="insta-overlay">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069z"/></svg>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="REEL Auto Centre on Instagram">
                  <img src="Images/efuas_auto_center_hero.jpg" alt="REEL Auto Centre" loading="lazy" />
                  <div class="insta-overlay">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069z"/></svg>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="REEL Tech Hub on Instagram">
                  <img src="Images/vannys_tech_hub_hero.jpg" alt="REEL Tech Hub" loading="lazy" />
                  <div class="insta-overlay">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069z"/></svg>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="REEL Global Palace on Instagram">
                  <img src="Images/glorious_global_palace_hero.jpg" alt="REEL Global Palace" loading="lazy" />
                  <div class="insta-overlay">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069z"/></svg>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="REEL Branding on Instagram">
                  <img src="Images/reel_branding_hero.png" alt="REEL Branding" loading="lazy" />
                  <div class="insta-overlay">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069z"/></svg>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="REEL Power on Instagram">
                  <img src="Images/reel_power_hero.png" alt="REEL Power Infrastructure" loading="lazy" />
                  <div class="insta-overlay">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069z"/></svg>
                  </div>
                </a>
              </div>
              <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-follow-btn">
                <span>Follow on Instagram</span>
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </a>
            </div>
          </div>"""

# CSS to inject into css/style.css
insta_css = """
/* ── Footer Instagram Feed Widget (Replaces Calendar) ── */
.footer-insta-col { min-width: 0; }
.footer-insta-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 14px;
  padding: 14px;
  backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
.footer-insta-card:hover {
  border-color: rgba(212, 175, 55, 0.45);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(212, 175, 55, 0.08);
}
.insta-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.insta-user-info {
  display: flex;
  align-items: center;
  gap: 6px;
}
.insta-icon {
  color: var(--gold-300, #D4AF37);
}
.insta-handle {
  font-size: 0.82rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.02em;
}
.insta-badge {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(212, 175, 55, 0.15);
  color: var(--gold-300, #D4AF37);
  border: 1px solid rgba(212, 175, 55, 0.3);
}
.insta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}
.insta-tile {
  position: relative;
  aspect-ratio: 1 / 1;
  border-radius: 8px;
  overflow: hidden;
  background: #111;
  display: block;
}
.insta-tile img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}
.insta-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-300, #D4AF37);
  opacity: 0;
  transition: opacity 0.25s ease;
}
.insta-tile:hover img {
  transform: scale(1.1);
}
.insta-tile:hover .insta-overlay {
  opacity: 1;
}
.insta-follow-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.16), rgba(212, 175, 55, 0.04));
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: var(--gold-300, #D4AF37);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-decoration: none;
  transition: all 0.2s ease;
}
.insta-follow-btn:hover {
  background: var(--gold-gradient, linear-gradient(135deg, #D4AF37, #8B6914));
  color: #000;
  border-color: transparent;
}
"""

# Append CSS to css/style.css
with open('css/style.css', 'r', encoding='utf-8', errors='ignore') as f:
    css_content = f.read()

if '.footer-insta-card' not in css_content:
    with open('css/style.css', 'a', encoding='utf-8') as f:
        f.write('\n' + insta_css + '\n')
    print("Added Instagram CSS to css/style.css")

# Update all 25 HTML files containing the calendar
updated_count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
            
            # Pattern matching the calendar widget column
            pattern = re.compile(r'<!--\s*(?:Footer\s+)?Calendar\s+Widget\s*-->[\s\S]*?id="fc-days"[^>]*></div>\s*</div>\s*</div>', re.IGNORECASE)
            if pattern.search(content):
                new_c = pattern.sub(instagram_column_html, content, count=1)
                with open(p, 'w', encoding='utf-8', newline='\r\n') as fp:
                    fp.write(new_c)
                updated_count += 1
                print(f"Updated: {p}")
            else:
                # Fallback pattern without comment
                pattern2 = re.compile(r'<div class="[^"]*footer-calendar-col[^"]*"[^>]*>[\s\S]*?id="fc-days"[^>]*></div>\s*</div>\s*</div>', re.IGNORECASE)
                if pattern2.search(content):
                    new_c = pattern2.sub(instagram_column_html, content, count=1)
                    with open(p, 'w', encoding='utf-8', newline='\r\n') as fp:
                        fp.write(new_c)
                    updated_count += 1
                    print(f"Updated (fallback): {p}")

print(f"\nDone! Updated {updated_count} HTML files.")

