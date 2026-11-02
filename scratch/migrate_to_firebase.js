/**
 * migrate_to_firebase.js
 * ─────────────────────────────────────────────────────────────────────────
 * 1. Uploads every rescued image from Images/uploads/ to Firebase Storage
 * 2. Updates the matching Firestore document's image/images field with the
 *    new Storage URL
 * ─────────────────────────────────────────────────────────────────────────
 * Run:  node scratch/migrate_to_firebase.js
 */

const fs   = require('fs');
const path = require('path');

// ── Firebase Admin SDK (loaded as compat REST calls — no npm install needed)
const PROJECT_ID     = 'royal-executive-empire-ree';
const STORAGE_BUCKET = 'royal-executive-empire-ree.firebasestorage.app';
const API_KEY        = 'AIzaSyA0CCQzLvA4pZc_fJJSzN6V98IwN9TfofY';

const UPLOADS_DIR = path.join(__dirname, '..', 'Images', 'uploads');

// Firestore REST helpers
const FS_BASE = `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents`;

async function firestoreGet(collection, docId) {
  const res = await fetch(`${FS_BASE}/${collection}/${docId}?key=${API_KEY}`);
  return res.json();
}

async function firestorePatch(collection, docId, fields) {
  const mask = Object.keys(fields).map(f => `updateMask.fieldPaths=${encodeURIComponent(f)}`).join('&');
  const body = { fields };
  const res = await fetch(
    `${FS_BASE}/${collection}/${docId}?${mask}&key=${API_KEY}`,
    { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
  );
  return res.json();
}

// Firebase Storage REST upload
async function uploadToStorage(localPath, storagePath) {
  const fileBytes = fs.readFileSync(localPath);
  const ext = path.extname(localPath).slice(1).toLowerCase();
  const mime = ext === 'png' ? 'image/png' : 'image/jpeg';
  const encodedPath = encodeURIComponent(storagePath);

  const res = await fetch(
    `https://storage.googleapis.com/upload/storage/v1/b/${STORAGE_BUCKET}/o?uploadType=media&name=${encodedPath}&key=${API_KEY}`,
    { method: 'POST', headers: { 'Content-Type': mime }, body: fileBytes }
  );
  const data = await res.json();
  if (data.error) throw new Error(`Storage upload failed: ${JSON.stringify(data.error)}`);

  // Make public
  await fetch(
    `https://storage.googleapis.com/storage/v1/b/${STORAGE_BUCKET}/o/${encodedPath}/iam?key=${API_KEY}`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bindings: [{ role: 'roles/storage.objectViewer', members: ['allUsers'] }] }) }
  );

  // Return public download URL
  return `https://storage.googleapis.com/${STORAGE_BUCKET}/${storagePath}`;
}

// Parse filename like: "blogs_abc123.png" or "properties_xyz_images_0.png"
function parseFilename(filename) {
  const base = path.basename(filename, path.extname(filename));
  // properties with array index: e.g. properties_KAz8_images_0
  const arrayMatch = base.match(/^([^_]+)_([^_]+(?:_[^_]+)?)_images_(\d+)$/);
  if (arrayMatch) {
    return { collection: arrayMatch[1], docId: arrayMatch[2], field: 'images', index: parseInt(arrayMatch[3]) };
  }
  // simple: collection_docId
  const parts = base.split('_');
  const collection = parts[0];
  const docId = parts.slice(1).join('_');
  return { collection, docId, field: 'image', index: null };
}

async function run() {
  const files = fs.readdirSync(UPLOADS_DIR);
  console.log(`Found ${files.length} images to migrate...\n`);

  const results = { success: [], failed: [] };

  for (const file of files) {
    const localPath = path.join(UPLOADS_DIR, file);
    const info = parseFilename(file);
    const storagePath = `uploads/${info.collection}/${file}`;

    try {
      console.log(`⬆  Uploading ${file}...`);
      const newUrl = await uploadToStorage(localPath, storagePath);
      console.log(`   ✅ ${newUrl}`);

      // Update Firestore
      if (info.field === 'image') {
        await firestorePatch(info.collection, info.docId, {
          image: { stringValue: newUrl }
        });
        console.log(`   📝 Firestore updated: ${info.collection}/${info.docId}`);
      } else {
        // Array field: fetch doc first, update index
        const doc = await firestoreGet(info.collection, info.docId);
        const existingValues = (doc.fields && doc.fields.images && doc.fields.images.arrayValue && doc.fields.images.arrayValue.values)
          ? doc.fields.images.arrayValue.values
          : [];
        while (existingValues.length <= info.index) existingValues.push({ stringValue: '' });
        existingValues[info.index] = { stringValue: newUrl };
        await firestorePatch(info.collection, info.docId, {
          images: { arrayValue: { values: existingValues } }
        });
        console.log(`   📝 Firestore updated: ${info.collection}/${info.docId} images[${info.index}]`);
      }

      results.success.push({ file, newUrl, collection: info.collection, docId: info.docId });
    } catch (err) {
      console.error(`   ❌ Failed ${file}: ${err.message}`);
      results.failed.push({ file, error: err.message });
    }
  }

  console.log(`\n${'─'.repeat(60)}`);
  console.log(`✅ Migrated: ${results.success.length}`);
  console.log(`❌ Failed:   ${results.failed.length}`);
  if (results.failed.length) {
    console.log('\nFailed files:');
    results.failed.forEach(f => console.log(`  - ${f.file}: ${f.error}`));
  }

  fs.writeFileSync(
    path.join(__dirname, 'migration_results.json'),
    JSON.stringify(results, null, 2)
  );
  console.log('\nResults saved to scratch/migration_results.json');
}

run().catch(console.error);

