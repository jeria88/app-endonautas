"""PWA manifest + service worker + Digital Asset Links.
Servidos en la raíz del dominio (requisito TWA/PWA), no bajo /static/."""
from django.http import HttpResponse, JsonResponse
from django.templatetags.static import static
from django.views.decorators.cache import cache_control

# Fingerprints SHA256 de la app Android. Se completan en Fase C (upload key) y
# Fase D (Play App Signing). Sin ambos, la TWA muestra la barra de URL.
ASSETLINKS_FINGERPRINTS = [
    "REEMPLAZAR_SHA256_UPLOAD_KEY_FASE_C",
    "REEMPLAZAR_SHA256_PLAY_APP_SIGNING_FASE_D",
]
ANDROID_PACKAGE = "cl.endonautas.app"


@cache_control(max_age=3600)
def manifest(request):
    return JsonResponse({
        "name": "Endonautas",
        "short_name": "Endonautas",
        "description": "Tu viaje de autoconocimiento: Espejo IA, tests, oráculo y carta natal.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#03030a",
        "theme_color": "#03030a",
        "lang": "es",
        "icons": [
            {"src": static("img/icon-192.png"), "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": static("img/icon-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": static("img/icon-512-maskable.png"), "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    })


SERVICE_WORKER_JS = """// PWA service worker minimo: habilita instalabilidad (Chrome exige un
// handler de fetch). Passthrough a red; sin cache offline por ahora.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => {});
"""


def service_worker(request):
    resp = HttpResponse(SERVICE_WORKER_JS, content_type="application/javascript")
    resp["Service-Worker-Allowed"] = "/"
    resp["Cache-Control"] = "no-cache"
    return resp


@cache_control(max_age=3600)
def assetlinks(request):
    return JsonResponse([{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": ANDROID_PACKAGE,
            "sha256_cert_fingerprints": ASSETLINKS_FINGERPRINTS,
        },
    }], safe=False)
