const CACHE_NAME = 'logicplay-v1';
const urlsToCache = [
  './',
  './landing.html',
  './index.html',
  './manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache).catch(err => console.log('Partial cache: '+err));
      })
  );
  self.skipWaiting();
});

self.addEventListener('fetch', event => {
  // Offline support strategy: Cache falling back to network
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
