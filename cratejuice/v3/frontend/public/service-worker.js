const CACHE = "cj-shell-v1";
const SHELL = ["./index.html","./style.css","./app.js","./manifest.webmanifest"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(self.clients.claim()); });
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (url.pathname.includes("/offgrid-crates/") || url.pathname.includes("/content/data/")) {
    e.respondWith(caches.open(CACHE).then(async cache => {
      const match = await cache.match(e.request);
      const net = fetch(e.request).then(res => { cache.put(e.request, res.clone()); return res; });
      return match || net;
    }));
  } else {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
  }
});
