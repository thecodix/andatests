// Service worker de Andatest: cachea el "app shell" (HTML, JS, manifest e
// iconos) para que la app cargue offline tras la primera visita. Las
// llamadas a la API (/api, /auth, /asistente) van siempre a red — nunca se
// cachean, porque son datos dinámicos por usuario (progreso, sesiones,
// asistente IA).
const CACHE_NAME = "andatest-shell-v2";
const APP_SHELL = [
  "/",
  "/support.js",
  "/banco.js",
  "/manifest.json",
  "/icon-192.png",
  "/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function esApi(url) {
  return url.pathname.startsWith("/api/") || url.pathname.startsWith("/auth/") || url.pathname.startsWith("/asistente/");
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin || esApi(url)) return; // deja pasar API y orígenes externos (Google Fonts, etc.)

  if (request.mode === "navigate") {
    // El HTML (la propia SPA) cambia con cada deploy/sesión de desarrollo:
    // red primero, y solo se cae a la copia en caché si no hay conexión.
    // Con stale-while-revalidate aquí, un cambio de frontend tardaba dos
    // recargas en verse (la primera servía la versión vieja cacheada).
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) caches.open(CACHE_NAME).then((cache) => cache.put(request, response.clone()));
          return response;
        })
        .catch(() => caches.open(CACHE_NAME).then((cache) => cache.match(request)))
    );
    return;
  }

  // Resto de assets estáticos (JS, manifest, iconos): stale-while-revalidate,
  // responde con la copia en caché al instante si existe, y en paralelo la
  // refresca en segundo plano para la próxima vez.
  event.respondWith(
    caches.open(CACHE_NAME).then((cache) =>
      cache.match(request).then((cached) => {
        const fetchPromise = fetch(request)
          .then((response) => {
            if (response.ok) cache.put(request, response.clone());
            return response;
          })
          .catch(() => cached);
        return cached || fetchPromise;
      })
    )
  );
});
