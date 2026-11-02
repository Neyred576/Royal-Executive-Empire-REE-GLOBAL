/**
 * update_firestore_urls.js
 * Updates all Firestore documents in royal-executive-empire-ree to point to
 * self-hosted Images/uploads/<filename> paths instead of failing imgbb.com URLs.
 */
const fs = require('fs');
const path = require('path');

const PROJECT_ID = 'royal-executive-empire-ree';
const API_KEY = 'AIzaSyA0CCQzLvA4pZc_fJJSzN6V98IwN9TfofY';
const FS_BASE = `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents`;
const UPLOADS_DIR = path.join(__dirname, '..', 'Images', 'uploads');

async function patchDoc(collection, docId, fieldPath, stringValue) {
  const mask = `updateMask.fieldPaths=${encodeURIComponent(fieldPath)}`;
  const url = `${FS_BASE}/${collection}/${docId}?${mask}&key=${API_KEY}`;
  
  // Construct body
  const body = { fields: {} };
  body.fields[fieldPath] = { stringValue: stringValue };

  const res = await fetch(url, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (data.error) {
    throw new Error(`Failed to patch ${collection}/${docId}: ${data.error.message}`);
  }
  return data;
}

async function run() {
  const files = fs.readdirSync(UPLOADS_DIR);
  console.log(`Processing ${files.length} upload files...`);

  let updated = 0;
  for (const file of files) {
    // Examples:
    // products_NmGxEZxsiLwlODTmqIyp.jpg
    // blogs_0JF4o1z9dFj7Q0YhyO9f.png
    // brands_4O8GZLHo3TChh8rVrENa.jpg
    // properties_KAz8F6ZhpvVwEt13AnH1_image.png
    // properties_x9lieAePhnu68y8I7ouR_images_0.png
    
    const ext = path.extname(file);
    const base = path.basename(file, ext);
    const parts = base.split('_');
    const collection = parts[0];
    
    // Check if it's an images array element or single image
    let docId, fieldPath;
    if (parts.length === 2) {
      docId = parts[1];
      fieldPath = 'image';
    } else if (parts.length === 3 && parts[2] === 'image') {
      docId = parts[1];
      fieldPath = 'image';
    } else if (parts.length === 4 && parts[2] === 'images') {
      // array handled separately if needed
      docId = parts[1];
      fieldPath = 'image'; // properties also have 'image' field
    } else {
      docId = parts.slice(1).join('_');
      fieldPath = 'image';
    }

    const localUrl = `Images/uploads/${file}`;

    try {
      await patchDoc(collection, docId, fieldPath, localUrl);
      console.log(`✅ [${collection}] ${docId} -> ${localUrl}`);
      updated++;
    } catch(err) {
      console.error(`❌ [${collection}] ${docId}: ${err.message}`);
    }
  }

  // Also ensure properties have image array updated if needed
  try {
    const prop1 = 'properties_KAz8F6ZhpvVwEt13AnH1_images_0.png';
    const prop2 = 'properties_x9lieAePhnu68y8I7ouR_images_0.png';
    
    await fetch(`${FS_BASE}/properties/KAz8F6ZhpvVwEt13AnH1?updateMask.fieldPaths=images&key=${API_KEY}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        fields: {
          images: { arrayValue: { values: [{ stringValue: `Images/uploads/${prop1}` }] } }
        }
      })
    });

    await fetch(`${FS_BASE}/properties/x9lieAePhnu68y8I7ouR?updateMask.fieldPaths=images&key=${API_KEY}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        fields: {
          images: { arrayValue: { values: [{ stringValue: `Images/uploads/${prop2}` }] } }
        }
      })
    });
    console.log('✅ Updated property image arrays');
  } catch(e) {
    console.error('Property array patch error:', e.message);
  }

  console.log(`\nMigration complete! Total documents updated in Firestore: ${updated}`);
}

run().catch(console.error);

