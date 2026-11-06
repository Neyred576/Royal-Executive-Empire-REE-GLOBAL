import re

path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Web\contact.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

map_section = """
<!-- ============================================================ -->
<!-- INTERACTIVE MAP & CONCIERGE LOCATION (From REEL Global)      -->
<!-- ============================================================ -->
<section class="section" style="padding: 20px 0 90px; background: #070707; border-top: 1px solid rgba(212,175,55,0.15);">
  <div class="container">
    <div style="text-align: center; max-width: 680px; margin: 0 auto 40px;">
      <div class="hero-eyebrow" style="justify-content: center; margin-bottom: 10px;">
        <span class="eyebrow-line"></span><span>Headquarters & Concierge</span><span class="eyebrow-line"></span>
      </div>
      <h2 class="section-heading" style="font-size: clamp(1.8rem, 3.5vw, 2.8rem); margin-bottom: 12px;">
        Visit Our <span class="gold-text">Empire Headquarters</span>
      </h2>
      <p style="color: var(--w60); font-size: 0.95rem; line-height: 1.7;">
        Located along the rapidly expanding executive corridor of Lekki-Epe. Step in for executive consultations, property viewings, or connect with our concierge desk.
      </p>
    </div>

    <!-- Embedded Luxury Map Card -->
    <div style="position: relative; border-radius: 24px; overflow: hidden; border: 1px solid rgba(212,175,55,0.35); box-shadow: 0 25px 60px rgba(0,0,0,0.85); height: 480px; background: #000;">
      <iframe
        title="REEL Corporate Headquarters Location"
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126860.55288289063!2d3.6074!3d6.4716!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x103bf7e2bf579b9b%3A0x7d6c5478479e0a0!2sIbeju%20Lekki%2C%20Lagos!5e0!3m2!1sen!2sng!4v1700000000000"
        width="100%"
        height="100%"
        style="border:0; width:100%; height:100%; min-height:480px; filter: invert(90%) hue-rotate(180deg) brightness(85%) contrast(120%);"
        allowfullscreen=""
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade">
      </iframe>

      <!-- Floating Map Info Badge -->
      <div style="position: absolute; bottom: 20px; left: 20px; right: 20px; max-width: 540px; background: rgba(8, 8, 8, 0.92); backdrop-filter: blur(16px); border: 1px solid rgba(212,175,55,0.35); border-radius: 18px; padding: 18px 24px; display: flex; align-items: center; justify-content: space-between; gap: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">
        <div>
          <div style="font-family: var(--font-display); font-size: 1.15rem; color: #fff; font-weight: 700; letter-spacing: 0.5px;">
            Plaza 30, Alatishe Corridor
          </div>
          <div style="font-size: 0.8rem; color: var(--gold-300); margin-top: 2px;">
            Along Lekki–Epe Expressway, Ibeju-Lekki, Lagos State, Nigeria
          </div>
        </div>
        <a href="https://maps.google.com/?q=Plaza+30+Alatishe+Lekki-Epe+Expressway+Ibeju-Lekki+Lagos" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #D4AF37 0%, #b89125 100%); color: #000; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; padding: 10px 18px; border-radius: 999px; text-decoration: none; white-space: nowrap; transition: all 0.25s; box-shadow: 0 4px 15px rgba(212,175,55,0.3);">
          Get Directions &rarr;
        </a>
      </div>
    </div>
  </div>
</section>
"""

target = "<!-- ============================================================ -->\n<!-- FOOTER"
target_crlf = "<!-- ============================================================ -->\r\n<!-- FOOTER"

if target_crlf in content:
    content = content.replace(target_crlf, map_section + "\r\n" + target_crlf)
    print("Replaced with CRLF!")
elif target in content:
    content = content.replace(target, map_section + "\n" + target)
    print("Replaced with LF!")
else:
    print("Target not found!")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done writing contact.html!")

