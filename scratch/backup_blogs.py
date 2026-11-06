import urllib.request
import json
import os

url = "https://firestore.googleapis.com/v1/projects/royal-executive-empire-ree/databases/(default)/documents/blogs?key=AIzaSyA0CCQzLvA4pZc_fJJSzN6V98IwN9TfofY"
backup_dir = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\MAIN WEBSITE\Test\Backup"
os.makedirs(backup_dir, exist_ok=True)
backup_path = os.path.join(backup_dir, "firestore_blogs_backup_2026-11-04.json")

try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        docs = data.get("documents", [])
        print(f"Successfully fetched {len(docs)} blog documents from Firestore!")
        
        # Also backup all documents across other collections
        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Blogs backup saved to: {backup_path}")
        
        # Display the blog titles backed up
        for i, doc in enumerate(docs):
            fields = doc.get("fields", {})
            title = fields.get("title", {}).get("stringValue", "Untitled")
            print(f"  {i+1}. {title}")

    # Also backup properties, power_products, products, etc.
    collections = ["properties", "power_products", "products", "messages", "brands"]
    for col in collections:
        try:
            col_url = f"https://firestore.googleapis.com/v1/projects/royal-executive-empire-ree/databases/(default)/documents/{col}?key=AIzaSyA0CCQzLvA4pZc_fJJSzN6V98IwN9TfofY"
            with urllib.request.urlopen(urllib.request.Request(col_url)) as col_resp:
                col_data = json.loads(col_resp.read().decode("utf-8"))
                col_backup = os.path.join(backup_dir, f"firestore_{col}_backup_2026-11-04.json")
                with open(col_backup, "w", encoding="utf-8") as cf:
                    json.dump(col_data, cf, indent=2, ensure_ascii=False)
                print(f"Backed up {len(col_data.get('documents', []))} docs from '{col}' to {col_backup}")
        except Exception as ce:
            print(f"Could not backup {col}: {ce}")

except Exception as e:
    print(f"Error fetching blogs: {e}")

