import urllib.request, re

req = urllib.request.Request(
    'https://www.instagram.com/reelholding/',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Status 200, length:", len(html))
        og_images = re.findall(r'property="og:image"\s+content="([^"]+)"', html)
        print("og:image:", og_images)
        desc = re.findall(r'property="og:description"\s+content="([^"]+)"', html)
        print("og:description:", desc)
        title = re.findall(r'<title>([^<]+)</title>', html)
        print("title:", title)
except Exception as e:
    print("Fetch error:", e)

