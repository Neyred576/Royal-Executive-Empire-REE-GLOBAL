import re

def update_admin():
    file_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\admin\index.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sidebar_link = """      <li>
        <a href="#" class="admin-nav-link" data-target="sec-notifications">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </div>
          <span class="nav-label">Push Alerts</span>
        </a>
      </li>
    </ul>"""

    if 'data-target="sec-notifications"' not in content:
        content = content.replace('</ul>\n\n    <div class="nav-section-label" style="margin-top:16px;">Inbox</div>', sidebar_link + '\n\n    <div class="nav-section-label" style="margin-top:16px;">Inbox</div>')

    section_html = """
    <!-- ── PUSH NOTIFICATIONS ── -->
    <section id="sec-notifications" class="admin-section">
      <div class="section-header">
        <div class="section-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
        </div>
        <div>
          <h1>Push Notifications</h1>
          <p>Send instant alerts to all active users on the website.</p>
        </div>
      </div>
      <div class="admin-grid" style="grid-template-columns: 1fr;">
        <div class="admin-card">
          <div class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
            Send New Broadcast
          </div>
          <form id="form-notification">
            <div class="form-group">
              <label>Notification Title</label>
              <input type="text" id="notif-title" placeholder="e.g. New Collection Dropped!" required />
            </div>
            <div class="form-group">
              <label>Message Content</label>
              <textarea id="notif-body" placeholder="Write your alert message..." required style="min-height:100px;"></textarea>
            </div>
            <button type="submit" class="btn-submit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
              Send Notification Now
            </button>
          </form>
        </div>
      </div>
    </section>
  </main>"""

    if 'sec-notifications' not in content:
        # We replace the closing main tag
        content = content.replace("</main>", section_html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_admin()
