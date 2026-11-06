import sys

with open('admin/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add <meta name="color-scheme" content="dark" /> in <head>
meta_target = '<meta name="viewport" content="width=device-width, initial-scale=1.0" />'
meta_replace = '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <meta name="color-scheme" content="dark" />'

# 2. Add color-scheme: dark to :root and html, body
root_target = """:root {
      --gold: #D4AF37;"""
root_replace = """:root {
      color-scheme: dark;
      --gold: #D4AF37;"""

html_body_target = "html, body { height: 100%; }"
html_body_replace = "html, body { height: 100%; color-scheme: dark; }"

# 3. Add comprehensive dark styling for all select dropdowns and options
form_select_target = """    .form-group input,
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
    }"""

form_select_replace = """    .form-group input,
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
      color-scheme: dark;
    }
    .form-group select {
      background-color: #121212;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='rgba(212,175,55,0.7)' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 14px center;
      background-size: 16px;
      padding-right: 42px;
      cursor: pointer;
    }
    /* Universal Select Dropdown & Options Dark Theme */
    select,
    input,
    textarea {
      color-scheme: dark;
    }
    select {
      background-color: #121212;
      color: #ffffff;
    }
    select option,
    select optgroup,
    .form-group select option,
    .form-group select optgroup {
      background: #161616 !important;
      background-color: #161616 !important;
      color: #ffffff !important;
      color-scheme: dark;
      padding: 12px 16px;
      font-size: 0.9rem;
      font-family: var(--font-body);
    }
    select option:checked,
    .form-group select option:checked {
      background: #282210 !important;
      background-color: #282210 !important;
      color: var(--gold) !important;
      font-weight: 600;
    }
    select option:hover,
    select option:focus,
    .form-group select option:hover,
    .form-group select option:focus {
      background: #332b14 !important;
      background-color: #332b14 !important;
      color: var(--gold-bright) !important;
    }
    select optgroup,
    .form-group select optgroup {
      background: #0d0d0d !important;
      background-color: #0d0d0d !important;
      color: var(--gold) !important;
      font-weight: 700;
      padding: 8px 12px;
    }"""

replacements = [
    (meta_target, meta_replace, "meta color-scheme"),
    (root_target, root_replace, "root color-scheme"),
    (html_body_target, html_body_replace, "html_body color-scheme"),
    (form_select_target, form_select_replace, "select & option dark styling")
]

success = 0
for old, new, label in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f"[OK] Replaced: {label}")
        success += 1
    else:
        print(f"[FAIL] Could not find: {label}")

if success == len(replacements):
    with open('admin/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(content)
    print("\nAll dropdown dark styles applied and saved successfully!")
else:
    print(f"\nAborting: only {success}/{len(replacements)} applied.")
    sys.exit(1)

