const CACHE="axinfo-v25";
const ASSETS=["./index.html","./manifest.json","./icon.svg","./bridge.html"];
self.addEventListener("install",e=>e.waitUntil(caches.open(CACHE).then(async c=>{for(const a of ASSETS){try{await c.add(a)}catch(err){}}return self.skipWaiting()})));
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==CACHE).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{if(e.request.method!=="GET")return;e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{if(res&&res.status===200&&new URL(e.request.url).origin===location.origin){const cp=res.clone();caches.open(CACHE).then(c=>c.put(e.request,cp))}return res}).catch(()=>caches.match("./index.html"))))});