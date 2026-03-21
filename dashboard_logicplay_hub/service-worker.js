const CACHE_NAME = 'logicplay-v2';
const OFFLINE_URL = './offline.html';

const urlsToCache = [
  './',
  './landing.html',
  './index.html',
  './manifest.json',
  './offline.html'
];

// Install: pre-cache essential resources including offline page
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache).catch(err => console.log('Partial cache: ' + err));
      })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch: Network-first for navigation, cache-first for assets
self.addEventListener('fetch', event => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  const isNavigation = event.request.mode === 'navigate';

  if (isNavigation) {
    // Network-first for page navigation — show offline.html on failure
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Cache the fresh page response
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
          return response;
        })
        .catch(() => {
          // Network failed — try cache, fallback to offline page
          return caches.match(event.request)
            .then(cached => cached || caches.match(OFFLINE_URL));
        })
    );
  } else {
    // Cache-first for static assets (CSS, JS, images, fonts)
    event.respondWith(
      caches.match(event.request)
        .then(cached => {
          if (cached) return cached;
          return fetch(event.request)
            .then(response => {
              const responseClone = response.clone();
              caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
              return response;
            })
            .catch(() => {
              // For non-navigation failed requests, just return nothing
              return new Response('', { status: 408, statusText: 'Offline' });
            });
        })
    );
  }
});
