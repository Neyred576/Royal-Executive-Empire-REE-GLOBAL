import re

def update_forms():
    file_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\admin\index.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    portfolio_schedule = """
            <div class="form-group" style="padding:15px; background:rgba(212,175,55,0.03); border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                Publishing Schedule
              </label>
              <select id="portfolio-status" style="margin-bottom:12px;">
                <option value="published">Publish Immediately</option>
                <option value="scheduled">Schedule for Later</option>
                <option value="draft">Save as Draft</option>
              </select>
              <div id="portfolio-schedule-wrap" style="display:none;">
                <label style="font-size:0.65rem;">Schedule Date & Time</label>
                <input type="datetime-local" id="portfolio-schedule-time" style="margin-bottom:5px;" />
                <span style="font-size:0.7rem; color:var(--w40);">Project will be hidden until this date/time passes.</span>
              </div>
            </div>
            <button type="submit" """

    shop_schedule = """
            <div class="form-group" style="padding:15px; background:rgba(212,175,55,0.03); border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
              <label style="color:var(--gold); display:flex; align-items:center; gap:8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                Publishing Schedule
              </label>
              <select id="shop-status" style="margin-bottom:12px;">
                <option value="published">Publish Immediately</option>
                <option value="scheduled">Schedule for Later</option>
                <option value="draft">Save as Draft</option>
              </select>
              <div id="shop-schedule-wrap" style="display:none;">
                <label style="font-size:0.65rem;">Schedule Date & Time</label>
                <input type="datetime-local" id="shop-schedule-time" style="margin-bottom:5px;" />
                <span style="font-size:0.7rem; color:var(--w40);">Product will be hidden until this date/time passes.</span>
              </div>
            </div>
            <button type="submit" """

    # Find where <form id="form-portfolio"> ends (the submit button)
    # We will just replace the next <button type="submit" class="btn-submit"> inside that form
    # Or specifically replace `<button type="submit" class="btn-submit">\n              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>\n              Add Project\n            </button>`
    
    # Simple regex to find the button inside the portfolio form
    # We can split the content at form-portfolio and form-shop
    
    parts = content.split('<form id="form-portfolio">')
    if len(parts) == 2:
        pf_parts = parts[1].split('<button type="submit"', 1)
        if len(pf_parts) == 2 and 'id="portfolio-status"' not in pf_parts[0]:
            parts[1] = pf_parts[0] + portfolio_schedule + pf_parts[1].split('"', 1)[1] if pf_parts[1].startswith(' ') else portfolio_schedule + pf_parts[1]
    
    content = '<form id="form-portfolio">'.join(parts)
    
    parts2 = content.split('<form id="form-shop">')
    if len(parts2) == 2:
        sh_parts = parts2[1].split('<button type="submit"', 1)
        if len(sh_parts) == 2 and 'id="shop-status"' not in sh_parts[0]:
            parts2[1] = sh_parts[0] + shop_schedule + sh_parts[1].split('"', 1)[1] if sh_parts[1].startswith(' ') else shop_schedule + sh_parts[1]
    
    content = '<form id="form-shop">'.join(parts2)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Updated forms with scheduler.")

if __name__ == "__main__":
    update_forms()
