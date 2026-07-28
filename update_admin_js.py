import os

def update_admin_js():
    file_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\admin\js\admin.js"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add toggle logic for schedule inputs
    toggle_logic = """
    // --- SCHEDULER TOGGLE LOGIC ---
    const setupScheduleToggle = (selectId, wrapId) => {
      const select = document.getElementById(selectId);
      const wrap = document.getElementById(wrapId);
      if(select && wrap) {
        select.addEventListener('change', (e) => {
          if (e.target.value === 'scheduled') {
            wrap.style.display = 'block';
          } else {
            wrap.style.display = 'none';
          }
        });
      }
    };
    setupScheduleToggle('blog-status', 'blog-schedule-wrap');
    setupScheduleToggle('portfolio-status', 'portfolio-schedule-wrap');
    setupScheduleToggle('shop-status', 'shop-schedule-wrap');

    // Helper for Scheduler List
    const renderSchedulerList = () => {
      const container = document.getElementById('scheduler-list');
      if (!container) return;
      container.innerHTML = '';
      
      const allScheduled = [];
      
      blogs.forEach((b, i) => { if(b.status === 'scheduled') allScheduled.push({...b, type: 'blog', idx: i}) });
      portfolio.forEach((p, i) => { if(p.status === 'scheduled') allScheduled.push({...p, type: 'portfolio', idx: i}) });
      products.forEach((p, i) => { if(p.status === 'scheduled') allScheduled.push({...p, type: 'product', idx: i}) });
      
      if(allScheduled.length === 0) {
        container.innerHTML = `<div class="empty-state">No scheduled content.</div>`;
        return;
      }
      
      allScheduled.sort((a,b) => new Date(a.scheduleTime) - new Date(b.scheduleTime));
      
      allScheduled.forEach(item => {
        const div = document.createElement('div');
        div.className = 'admin-list-item';
        const dateStr = new Date(item.scheduleTime).toLocaleString();
        div.innerHTML = `
          <div class="item-info">
            <span style="font-size:0.65rem; color:var(--gold); text-transform:uppercase;">${item.type}</span>
            <strong>${item.title || item.name}</strong>
            <span class="item-date">Scheduled for: ${dateStr}</span>
          </div>
          <button class="btn-delete" data-index="${item.idx}" data-type="${item.type}">Delete</button>
        `;
        container.appendChild(div);
      });
    };
    """
    
    if "SCHEDULER TOGGLE LOGIC" not in content:
        content = content.replace("// 4. Initialize Data Arrays", toggle_logic + "\n    // 4. Initialize Data Arrays")

    # 2. Update renderAdminList to re-render scheduler and show badge if scheduled
    if "renderSchedulerList();" not in content:
        render_injection = """
        container.appendChild(div);
      });
      renderSchedulerList();
"""
        content = content.replace("container.appendChild(div);\n      });", render_injection)

    # Add schedule mark to admin list
    mark_injection = """
          <div class="item-info">
            <strong>${item.title || item.name} ${item.status === 'scheduled' ? '<span style="color:#D4AF37; font-size:0.7rem;">(Scheduled)</span>' : ''}</strong>
"""
    content = content.replace("""<div class="item-info">
            <strong>${item.title || item.name}</strong>""", mark_injection)


    # 3. Update form submissions
    # Blog
    blog_extract = """const content = document.getElementById('blog-content').value;
      const status = document.getElementById('blog-status').value;
      const scheduleTime = document.getElementById('blog-schedule-time').value;"""
    content = content.replace("const content = document.getElementById('blog-content').value;", blog_extract)

    blog_save = """blogs.unshift({
            title, category, content, status, scheduleTime,
            image: evt.target.result, """
    content = content.replace("""blogs.unshift({
            title, category, content, 
            image: evt.target.result, """, blog_save)

    # Portfolio
    pf_extract = """const category = document.getElementById('pf-cat').value;
      const status = document.getElementById('portfolio-status').value;
      const scheduleTime = document.getElementById('portfolio-schedule-time').value;"""
    content = content.replace("const category = document.getElementById('pf-cat').value;", pf_extract)

    pf_save = """portfolio.unshift({
            title, category, status, scheduleTime,
            image: evt.target.result"""
    content = content.replace("""portfolio.unshift({
            title, category,
            image: evt.target.result""", pf_save)

    # Shop
    shop_extract = """const category = document.getElementById('shop-cat').value;
      const status = document.getElementById('shop-status').value;
      const scheduleTime = document.getElementById('shop-schedule-time').value;"""
    content = content.replace("const category = document.getElementById('shop-cat').value;", shop_extract)

    shop_save = """products.unshift({
            name, price, category, status, scheduleTime,
            image: evt.target.result"""
    content = content.replace("""products.unshift({
            name, price, category,
            image: evt.target.result""", shop_save)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated admin.js")

if __name__ == "__main__":
    update_admin_js()
