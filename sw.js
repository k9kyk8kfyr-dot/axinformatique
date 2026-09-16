const CACHE = "axinfo-v20";
const ASSETS = ["./index.html", "./manifest.json", "./sw.js", "./icon.svg"];
self.addEventListener("install", function(event) { event.waitUntil(caches.open(CACHE).then(function(cache){ return Promise.all(ASSETS.map(function(url){ return cache.add(url).catch(function(){ return null; }); })); }).then(function(){ return self.skipWaiting(); })); });
self.addEventListener("activate", function(event) { event.waitUntil(caches.keys().then(function(keys){ return Promise.all(keys.filter(function(k){ return k !== CACHE; }).map(function(k){ return caches.delete(k); })); }).then(function(){ return self.clients.claim(); })); });
self.addEventListener("fetch", function(event) { if(event.request.method !== "GET") return; event.respondWith(caches.match(event.request).then(function(cached){ return cached || fetch(event.request).catch(function(){ return caches.match("./index.html"); }); })); });
