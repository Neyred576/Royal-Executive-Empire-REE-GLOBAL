const CACHE_NAME = 'reel-cache-v2';
const urlsToCache = [
  '/',
  '/index.html',
  '/about.html',
  '/shop.html',
  '/contact.html',
  '/css/styles.css', 
  '/js/main.js',
  '/manifest.json',
  '/Images/BG/logo%20bg.png',
  'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700&family=Outfit:wght@300;400;500;600;700;800&display=swap'
];

// Install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        // We use catch to not fail the whole install if one file is missing
        return Promise.all(
          urlsToCache.map(url => {
            return cache.add(url).catch(error => {
              console.error('Failed to cache:', url, error);
            });
          })
        );
      })
  );
});

// Fetch event
self.addEventListener('fetch', event => {
  // We don't cache API calls or Firestore requests
  if (event.request.url.includes('firestore') || event.request.url.includes('firebase')) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        // Clone the request
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(
          response => {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                if(event.request.method === 'GET') {
                   cache.put(event.request, responseToCache);
                }
              });

            return response;
          }
        );
      })
  );
});

// Activate event
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
