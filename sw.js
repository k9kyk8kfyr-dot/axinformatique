const CACHE = "axinfo-v17-2";
const ASSETS = [
  "./AXinfo_Ultimate_v17_iPhone.html",
  "./manifest.json",
  "./sw.js",
  "./icon.svg"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE).then(cache =>
      Promise.all(ASSETS.map(url => cache.add(url).catch(() => null)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    caches.match(event.request).then(cached =>
      cached || fetch(event.request).catch(() =>
        caches.match("./AXinfo_Ultimate_v17_iPhone.html")
      )
    )
  );
});
