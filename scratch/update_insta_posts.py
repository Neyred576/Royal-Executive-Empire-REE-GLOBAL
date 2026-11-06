import os, re

# The enhanced Instagram widget structure
new_insta_widget = """          <!-- Footer Instagram Feed -->
          <div class="footer-col footer-insta-col">
            <h3 class="footer-heading">Instagram</h3>
            <div class="footer-insta-card" aria-label="Official Instagram feed">
              <div class="insta-header">
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-user-info" style="text-decoration:none;">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" class="insta-icon">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                  </svg>
                  <span class="insta-handle">@reelholding</span>
                </a>
                <span class="insta-badge"><span class="insta-live-dot"></span> Live</span>
              </div>
              <div class="insta-grid">
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="View REEL Properties post on Instagram">
                  <img src="Images/real_estate_hero.png" alt="REEL Luxury Properties" loading="lazy" />
                  <span class="insta-type-icon">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="currentColor"><path d="M4 4h16v16H4z"/></svg>
                  </span>
                  <div class="insta-overlay">
                    <div class="insta-overlay-inner">
                      <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                      <span>View</span>
                    </div>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="View REEL Auto post on Instagram">
                  <img src="Images/efuas_auto_center_hero.jpg" alt="REEL Auto Centre" loading="lazy" />
                  <span class="insta-type-icon">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="currentColor"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
                  </span>
                  <div class="insta-overlay">
                    <div class="insta-overlay-inner">
                      <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                      <span>View</span>
                    </div>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="View REEL Tech Hub post on Instagram">
                  <img src="Images/vannys_tech_hub_hero.jpg" alt="REEL Tech Hub" loading="lazy" />
                  <span class="insta-type-icon">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="currentColor"><path d="M4 4h16v16H4z"/></svg>
                  </span>
                  <div class="insta-overlay">
                    <div class="insta-overlay-inner">
                      <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                      <span>View</span>
                    </div>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="View REEL Global Palace post on Instagram">
                  <img src="Images/glorious_global_palace_hero.jpg" alt="REEL Global Palace" loading="lazy" />
                  <span class="insta-type-icon">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="currentColor"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
                  </span>
                  <div class="insta-overlay">
                    <div class="insta-overlay-inner">
                      <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                      <span>View</span>
                    </div>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="View REEL Leadership post on Instagram">
                  <img src="Images/Prince Ose/About/DSC_4985 copy.jpg" alt="REEL Executive Leadership" loading="lazy" />
                  <span class="insta-type-icon">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="currentColor"><path d="M4 4h16v16H4z"/></svg>
                  </span>
                  <div class="insta-overlay">
                    <div class="insta-overlay-inner">
                      <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                      <span>View</span>
                    </div>
                  </div>
                </a>
                <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-tile" title="View REEL Power & Energy post on Instagram">
                  <img src="Images/reel_power_hero.png" alt="REEL Power Infrastructure" loading="lazy" />
                  <span class="insta-type-icon">
                    <svg viewBox="0 0 24 24" width="11" height="11" fill="currentColor"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
                  </span>
                  <div class="insta-overlay">
                    <div class="insta-overlay-inner">
                      <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                      <span>View</span>
                    </div>
                  </div>
                </a>
              </div>
              <a href="https://www.instagram.com/reelholding/" target="_blank" rel="noopener noreferrer" class="insta-follow-btn">
                <span>View Instagram Posts</span>
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </a>
            </div>
          </div>"""

# Enhanced CSS with live dot animation and Reel/Photo badge indicator
insta_css_enhancements = """
/* ── Enhanced Live Instagram Post Grid Styling ── */
.insta-live-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ff3b5c;
  margin-right: 4px;
  animation: instaPulse 1.6s infinite ease-in-out;
}
@keyframes instaPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.8); }
}
.insta-type-icon {
  position: absolute;
  top: 4px;
  right: 4px;
  z-index: 2;
  background: rgba(0, 0, 0, 0.65);
  color: #fff;
  border-radius: 4px;
  padding: 2px 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  font-size: 0.6rem;
}
.insta-overlay-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  font-size: 0.65rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.insta-overlay-inner svg {
  fill: #ff3b5c;
}
"""

with open('css/style.css', 'r', encoding='utf-8', errors='ignore') as f:
    css = f.read()

if '.insta-live-dot' not in css:
    with open('css/style.css', 'a', encoding='utf-8') as f:
        f.write('\n' + insta_css_enhancements + '\n')
    print("Added enhanced Instagram CSS to css/style.css")

# Update all 25 HTML files with the enhanced interactive grid
target_pattern = re.compile(r'<!-- Footer Instagram Feed -->[\s\S]*?<div class="footer-col footer-insta-col">[\s\S]*?</div>\s*</div>', re.IGNORECASE)

updated = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
            if 'footer-insta-col' in c:
                new_c = target_pattern.sub(new_insta_widget, c, count=1)
                with open(p, 'w', encoding='utf-8', newline='\r\n') as fp:
                    fp.write(new_c)
                updated += 1
                print("Updated:", p)

print(f"\nSuccessfully updated {updated} files with the live Instagram post grid.")

