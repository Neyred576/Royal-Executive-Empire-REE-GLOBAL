import re

def update_admin():
    file_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\admin\index.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. NEW CSS FOR BROADCAST CENTER & MODAL
    new_css = """
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
    """
    
    if "NEW BROADCAST CENTER & SCHEDULER MODAL CSS" not in content:
        content = content.replace("</style>", new_css)

    # 2. Add Modal HTML at the bottom before script tags
    modal_html = """
  <!-- SCHEDULER MODAL -->
  <div class="schedule-modal-overlay" id="schedule-modal-overlay">
    <div class="schedule-modal">
      <h2>Schedule Publish Time</h2>
      <p>Select exactly when you want this post to go live.</p>
      <input type="datetime-local" id="global-schedule-time" />
      <div class="schedule-modal-actions">
        <button class="btn-cancel" onclick="closeScheduleModal()">Cancel</button>
        <button class="btn-confirm" onclick="confirmScheduleTime()">Set Time</button>
      </div>
    </div>
  </div>
  """
    if "SCHEDULER MODAL" not in content:
        content = content.replace("<!-- Firebase Integration -->", modal_html + "\n  <!-- Firebase Integration -->")

    # 3. Add Broadcast Center HTML
    broadcast_html = """
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
    """
    
    # Remove old sec-notifications if it exists
    if 'id="sec-notifications"' in content:
        import re as regex
        content = regex.sub(r'<section id="sec-notifications" class="admin-section">.*?</section>', broadcast_html, content, flags=regex.DOTALL)
    else:
        # Append before </main>
        content = content.replace("</main>", broadcast_html + "\n  </main>")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_admin()
