with open('admin/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Add uploadOrCompressImage helper after IMGBB_API_KEY
helper_code = '''    const IMGBB_API_KEY = '40fad5b164f7be1f49b470b9563cc0c7';

    // Resilient image uploader: tries ImgBB with timeout; if ImgBB fails/down, gracefully compresses via canvas to lightweight data URL
    async function uploadOrCompressImage(file) {
      if (!file) return '';
      try {
        const getBase64 = (f) => new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(f);
          reader.onload = () => resolve(reader.result.split(',')[1]);
          reader.onerror = reject;
        });
        const base64Image = await getBase64(file);
        const formData = new FormData();
        formData.append('image', base64Image);
        
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 6000);
        const res = await fetch(`https://api.imgbb.com/1/upload?key=${IMGBB_API_KEY}`, {
          method: 'POST',
          body: formData,
          signal: controller.signal
        });
        clearTimeout(timeout);
        const data = await res.json();
        if (data && data.success && data.data && data.data.url) {
          return data.data.url;
        }
      } catch(e) {
        console.warn('ImgBB upload bypassed/failed, falling back to local canvas compression:', e);
      }

      // Safe Fallback: Compress using HTML5 Canvas to lightweight JPEG Data URL
      return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          let w = img.width, h = img.height;
          const maxDim = 1200;
          if (w > maxDim || h > maxDim) {
            if (w > h) { h = Math.round((h * maxDim) / w); w = maxDim; }
            else { w = Math.round((w * maxDim) / h); h = maxDim; }
          }
          canvas.width = w; canvas.height = h;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, w, h);
          resolve(canvas.toDataURL('image/jpeg', 0.82));
        };
        img.onerror = () => {
          const reader = new FileReader();
          reader.onload = () => resolve(reader.result);
          reader.readAsDataURL(file);
        };
        img.src = URL.createObjectURL(file);
      });
    }'''

target1 = "    const IMGBB_API_KEY = '40fad5b164f7be1f49b470b9563cc0c7';"
c = c.replace(target1, helper_code, 1)

# In handleForm: replace lines 2420-2445
target_handleform = '''          if (file) {
            // 1. Convert File to Base64
            const getBase64 = (f) => new Promise((resolve, reject) => {
              const reader = new FileReader();
              reader.readAsDataURL(f);
              reader.onload = () => resolve(reader.result.split(',')[1]);
              reader.onerror = error => reject(error);
            });
            const base64Image = await getBase64(file);

            // 2. Upload to ImgBB
            const formData = new FormData();
            formData.append('image', base64Image);

            const imgbbResponse = await fetch(`https://api.imgbb.com/1/upload?key=${IMGBB_API_KEY}`, {
              method: 'POST',
              body: formData
            });

            const imgbbData = await imgbbResponse.json();
            if (!imgbbData.success) {
              throw new Error('ImgBB Error: ' + (imgbbData.error && imgbbData.error.message ? imgbbData.error.message : 'Upload Failed'));
            }

            imageUrl = imgbbData.data.url; // The live image URL
            btn.innerHTML = 'Saving...';
          }'''

replacement_handleform = '''          if (file) {
            imageUrl = await uploadOrCompressImage(file);
            btn.innerHTML = 'Saving...';
          }'''

c = c.replace(target_handleform, replacement_handleform)

# In blog form
target_blog = '''          if (file) {
            const getBase64 = (f) => new Promise((resolve, reject) => {
              const reader = new FileReader();
              reader.readAsDataURL(f);
              reader.onload = () => resolve(reader.result.split(',')[1]);
              reader.onerror = error => reject(error);
            });
            const base64Image = await getBase64(file);
            const fd = new FormData();
            fd.append('image', base64Image);
            const res = await fetch(`https://api.imgbb.com/1/upload?key=${IMGBB_API_KEY}`, { method: 'POST', body: fd });
            const data = await res.json();
            if (!data.success) throw new Error('ImgBB Error: ' + (data.error?.message || 'Upload Failed'));
            imageUrl = data.data.url;
            btn.innerHTML = 'Saving...';
          }'''

replacement_blog = '''          if (file) {
            imageUrl = await uploadOrCompressImage(file);
            btn.innerHTML = 'Saving...';
          }'''

c = c.replace(target_blog, replacement_blog)

# In properties multiple files
target_prop = '''              for (let file of files) {
                const base64Image = await new Promise((resolve, reject) => {
                  const reader = new FileReader();
                  reader.readAsDataURL(file);
                  reader.onload = () => resolve(reader.result.split(',')[1]);
                  reader.onerror = err => reject(err);
                });
                const formData = new FormData();
                formData.append('image', base64Image);
                const res = await fetch(`https://api.imgbb.com/1/upload?key=${IMGBB_API_KEY}`, { method: 'POST', body: formData });
                const imgData = await res.json();
                if (!imgData.success) throw new Error('ImgBB Error: ' + (imgData.error?.message || 'Upload Failed'));
                imageUrls.push(imgData.data.url);
              }'''

replacement_prop = '''              for (let file of files) {
                const url = await uploadOrCompressImage(file);
                if (url) imageUrls.push(url);
              }'''

c = c.replace(target_prop, replacement_prop)

# In brand form
target_brand = '''          if (file) {
              const getBase64 = (f) => new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(f);
                reader.onload = () => resolve(reader.result.split(',')[1]);
                reader.onerror = err => reject(err);
              });
              const base64Image = await getBase64(file);
              const fd = new FormData();
              fd.append('image', base64Image);
              const res = await fetch(`https://api.imgbb.com/1/upload?key=${IMGBB_API_KEY}`, { method: 'POST', body: fd });
              const data = await res.json();
              if (!data.success) throw new Error('ImgBB Error: ' + (data.error?.message || 'Upload Failed'));
              imageUrl = data.data.url;
          }'''

replacement_brand = '''          if (file) {
              imageUrl = await uploadOrCompressImage(file);
          }'''

c = c.replace(target_brand, replacement_brand)

with open('admin/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Successfully updated admin/index.html')

