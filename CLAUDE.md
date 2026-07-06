# CLAUDE.md — App Endonautas

> Archivo de contexto técnico para Claude. Leer completo antes de tocar código.

## ⚠️ URLs de herramientas del servidor — ACTUALIZADAS (jun 2026)

Las herramientas de monitoreo/analytics/mail ya NO están en subdominios de `endonautas.cl`.
Fueron migradas a URLs genéricas para uso compartido de todo el servidor Oracle:

| Herramienta | URL anterior (rota) | URL actual |
|---|---|---|
| Umami (analytics) | `analytics.endonautas.cl` | `https://analytics.146.181.39.4.sslip.io` |
| Listmonk (email) | `mail.endonautas.cl` | `https://mail.146.181.39.4.sslip.io` |
| Uptime Kuma (status) | `status.endonautas.cl` | `https://status.146.181.39.4.sslip.io` |
| SerpBear (SEO) | `serpbear.endonautas.cl` | `https://serpbear.146.181.39.4.sslip.io` |

## Comando siempre: `python3 manage.py` (nunca `python`)

## Stack
- Django 6.0.4, SQLite (dev) / PostgreSQL Oracle Cloud (prod)
- Gunicorn 2 workers × 2 threads
- WhiteNoise para static files
- DeepSeek API (key en `.env`) para IA
- kerykeion 5.12.8 (astrología), sxtwl 2.0.7 (Saju/BaZi), timezonefinder (zonas horarias)
- Three.js 0.160 (fondo cosmos), Canvas 2D (fondo mandala/túnel)
- Repo: github.com/jeria88/app-endonautas

## Arrancar el servidor
```bash
python3 manage.py runserver          # SQLite por defecto
python3 manage.py migrate
python3 manage.py seed_tests         # pobla 35 tests psicométricos
python3 manage.py seed_fractal_cards # pobla cartas fractales
```

---

## Estructura de apps

| App | Estado | Descripción |
|-----|--------|-------------|
| `accounts` | ✅ activa | Auth por email, UserProfile, planes, onboarding |
| `birth` | ✅ activa | Lecturas de nacimiento: astral, Human Design, Saju/BaZi |
| `oraculo` | ✅ activa | Tarot Terapéutico (Jodorowsky), I Ching, Oráculo Fractal |
| `psychometrics` | ✅ activa | 35 tests psicométricos con insights IA |
| `tokens` | 🔴 legacy | Fractones desactivados — tablas en BD sin uso activo, views redirigen a /pagos/planes/ |
| `mirror` | ✅ activa | Espejo de Conflictos (RAG + DeepSeek), sueños, regulación |
| `community` | ✅ activa | Feed social, foros, mensajes directos |
| `terapeuta` | ✅ activa | Modo terapeuta: diagnóstico por framework, técnicas somáticas |
| `practitioners` | 🔶 parcial | Directorio de practicantes, TemporaryProfile para clientes |
| `config` | ✅ activa | settings, urls raíz, wsgi |

---

## Modelos clave

### `accounts.UserProfile`
```python
user          OneToOne → User
plan          free / navegante / practicante / empresa
map_aesthetic cosmos / mandala         # controla el fondo visual
color_palette cosmos / aurora / terra / obsidian / sakura  # glow de partículas cosmos
avatar        ImageField(upload_to='avatars/')
bio           TextField
onboarding_complete  BooleanField
hotmart_subscriber_code  CharField
tokens_last_renewed  DateField
```

### `oraculo.CartaFractal`
```python
numero, nombre_arcano, verbo, tipo (arcano/sefirot),
descripcion_breve, descripcion_larga, sefirot_nombre, es_especial
```

### `oraculo.SesionOraculo`
```python
id UUID, usuario FK, tipo_oraculo (tarot/iching/fractal),
pregunta, fecha_creacion, guardada
```
Relaciones OneToOne: `lectura_tarot`, `lectura_iching`, `lectura_fractal`

### `birth.BirthData`
```python
birth_date, birth_time, city, country, latitude, longitude,
timezone_str, gender (M/F — requerido para Daewoon)
# puede ser OneToOne a User o a practitioners.TemporaryProfile
```

### `birth.BirthReport`
```python
birth_data FK, report_type (astral/hd/saju),
status (pending/processing/done/error),
raw_data JSONField, ai_reading TextField, completed_at
# unique_together: (birth_data, report_type)
```

### `mirror.ChatSession` / `mirror.ChatMessage`
- RAG sobre `KnowledgeChunk` (embeddings en JSONField)
- `conflict_summary`, `return_question` — memoria versionada

### `mirror.DreamEntry`
```python
user FK, title, content, tags, dream_date, is_lucid, reality_check
```

---

## Sistema visual — Dos fondos

### Arquitectura general
`<body data-aesthetic="{{ map_aesthetic }}">` — JS y CSS leen esto.

```
html[data-aesthetic="cosmos"]  → Three.js activo, mandala oculto
html[data-aesthetic="mandala"] → Túnel Canvas activo, Three.js suspendido
```

El context processor `accounts/context_processors.py` inyecta `map_aesthetic` en todos los templates. Registrado en `settings.TEMPLATES`.

### Fondo Cosmos (Three.js 0.160)
- `UnrealBloomPass` + `EffectComposer` con WebGLRenderer
- **Performance:** `renderer.setPixelRatio(1.0)`, bloom a 50% resolución, N=75k partículas
- Agujero negro kepleriano, presets por sección (cambia camZ, density, bloom, etc.)
- Lazy init: si aesthetic≠cosmos, `window.__initCosmos` se llama solo al previsualizar
- `window.__cosmosCanvas` guarda el canvas para show/hide

### Fondo Mandala (Canvas 2D)
- Canvas `#tunnel-bg` al 50% de resolución, estirado con CSS `width:100%;height:100%`
- **30fps cap:** `if (ts - _lastFrame < 34) return;`
- 4 escenas, mapeadas a secciones:
  - 0 → `landing/general/onboarding` (Corriente Acuática — grid líquido)
  - 1 → `espejo/perfil/terapeuta` (Obsidiana — geometría angular)
  - 2 → `tests/comunidad/practicantes` (Hexagonal — hex grid)
  - 3 → `nacimiento/oraculo/suenos` (Fibonacci — espiral áurea)
- Transición portal: círculo negro expansivo 2200ms
- Overlay oscuro: `#mandala-overlay` (`rgba(3,3,6,0.44)`, z-index:1) para legibilidad

### SPA Navigation
`spaGo()` en base.html: fetch + swap `#page-content`.
Al navegar:
1. Swapea `<style data-page-style>` de la nueva página
2. Llama `window.presetForPath(path)` → devuelve preset según URL
3. `window.updateCosmosPreset(preset)` si está activo
4. `document.dispatchEvent(new CustomEvent('bg:preset', {detail: preset}))` — el túnel escucha este evento

### Live preview en perfil
```javascript
window.__switchAesthetic = function(name) {
  // Cambia data-aesthetic en body y html
  // Muestra/oculta tunnel canvas o cosmos container
  // Lazy init cosmos si se activa por primera vez
};
```
Las cards de aesthetic en `perfil.html` llaman `__switchAesthetic` en onclick.

### CSS tokens globales
```css
--surface: rgba(12,10,20,0.76)
--surface2: rgba(20,17,35,0.85)
--border: rgba(255,255,255,0.08)
--border-active: rgba(126,204,205,0.3)
--radius: 16px
--calipso: #7ECCCD          /* acento primario */
--violet: #9b8ec4
--rose: #c97b84
--amber: #d4a056
--sidebar-w: 280px
```
Clase `.panel`: glassmorphism oscuro con `backdrop-filter:blur(14px)`.

---

## Sistema de Planes

### Acceso por feature
| Feature | Free | Navegante ($10/mes) | Practicante ($39/mes) |
|---------|------|--------------------|-----------------------|
| Comunidad, Bitácora, Regulación | ✓ | ✓ | ✓ |
| Espejo IA (1 sesión/día · máx 45 min) | ✓ | — | — |
| Espejo IA ilimitado | — | ✓ | ✓ |
| Carta Astral | ✓ | ✓ | ✓ |
| Mapa de Patrones (3 tests gratuitos + IA) | ✓ — patrones visibles | ✓ — completo | ✓ — completo |
| Tests: Big Five, Heridas Infancia, Dirty Dozen | ✓ | ✓ | ✓ |
| I Ching, Tarot 1 carta | ✓ | ✓ | ✓ |
| Todos los tests (35+) | — | ✓ | ✓ |
| AI Insights en tests | — | ✓ | ✓ |
| Diseño Humano, Saju/BaZi | — | ✓ | ✓ |
| Tarot todas las tiradas, Oráculo Fractal | — | ✓ | ✓ |
| Módulo Terapeuta | — | ✓ | ✓ |
| Portal Profesional (practitioners) | — | — | ✓ |

### Gating (`accounts/plan_utils.py`)
```python
from accounts.plan_utils import plan_at_least, upgrade_wall, FREE_TEST_SLUGS, FREE_TAROT_TIRADAS

plan_at_least(user, 'navegante')   # True si plan >= navegante
upgrade_wall(request, 'navegante', 'Nombre del feature')  # devuelve HttpResponse con muro
```

### Página /planes/ — pública desde 2026-07-06
- Sin `login_required`: anónimos ven precios con CTA "Crear cuenta y comenzar" → `/registro/?plan=X` (el flujo post-registro con `?plan=` ya existía en `accounts/views.py`)
- Forms de pago MP y SDK PayPal se renderizan solo autenticados
- El cuerpo real vive en `templates/payments/_planes_body.html`, incluido en los blocks `content` (app) y `public_content` (anónimo) de `planes.html`
- Al activar un plan (MP/PayPal, retorno y webhook) se llama `update_subscriber_lists()` de Listmonk — segmentación de email se actualiza sola
- ⚠️ Discrepancia pendiente: la tabla comparativa dice "Espejo IA ilimitado" en Free, pero el gating real es 1 sesión/día 45 min — decidir cuál es la verdad y alinear

### Sistema de tokens (desactivado)
- `tokens/signals.py`: vaciado — no genera fractones
- `tokens/views.py`: redirige a /pagos/planes/
- Tablas en BD (TokenBalance, Mission, TokenTransaction) sin uso activo — no tocar

---

## Módulo Oráculo — detalles técnicos

### Tarot Terapéutico (Jodorowsky)
- 78 cartas cargadas en DB vía seed
- Tiradas: 1, 3, 5 cartas
- Imágenes en `static/img/tarot/` (nombradas por número)
- Reverso: `static/img/tarot/cardback.jpg` (imagen real del mazo)
- Interpretación vía DeepSeek (`oraculo/interpretations.py`)
- **Animaciones:** stagger 120ms por carta + interpPanel diferido

### I Ching
- 64 hexagramas con líneas móviles
- Tirada de 3 monedas × 6 líneas
- Líneas dibujadas como divs HTML (no SVG) → permite stagger CSS
- Revelación: bottom-to-top, 160ms por línea
- Animación: pulso Yang/Yin para líneas móviles
- Hexagrama secundario (si hay líneas móviles): sigue usando SVG

### Oráculo Fractal
- Cartas: Arcanos Mayores + Sefirot
- Mecánica: flip (reverso → frente)
- `static/img/tarot/cardback.jpg` como reverso
- Interpretación oculta hasta 700ms después del flip

---

## Módulo Birth — estructura de cálculo

### `birth/calculators.py`
- `calculate_astral_chart(bp)` — kerykeion, tropical Placidus, 10 planetas + Nodo + Quirón
- `calculate_hd_chart(bp)` — Tipo/Autoridad/Perfil/Centros/Canales/Cruz de Encarnación
  - `HD_WHEEL_START = 302.0` — inicio zodíaco HD para puertas
  - Diseño = 88° antes del Sol natal
- `calculate_saju_chart(bp)` — 4 Pilares con Daewoon (requiere gender)
  - Hora Solar Verdadera corregida por longitud

### Patterns importantes
- `_ensure_timezone(bp)` — re-deriva timezone de lat/lng (corrige registros con 'UTC')
- `_needs_recalc(report)` — fuerza recálculo si faltan campos de meanings

---

## Deploy (Oracle Cloud + Coolify)

**Infraestructura:** Oracle Cloud Free Tier ARM64 · IP `146.181.39.4` · Coolify v4.1.2 · Traefik
**Dominio:** `app.endonautas.cl`
**SSH:** `ssh -i '/home/nikka/DevTools/oracle-free/ssh/ssh-key-2026-06-14.key' ubuntu@146.181.39.4`

Start command configurado en Coolify:
```
python manage.py fix_db_state && python manage.py migrate --noinput && python manage.py create_admin && python manage.py seed_tests && python manage.py seed_regulacion && python manage.py seed_momentos && python manage.py seed_foros && python manage.py seed_fractal && python manage.py seed_terapeuta && python manage.py seed_missions && python manage.py seed_knowledge && gunicorn config.wsgi --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:8000
```
**Nota:** `seed_endonautica_md` y `index_knowledge` se ejecutan manualmente, no en Coolify. Para re-seedear el libro:
```bash
scp -i 'ssh-key.pem' endonautica.md ubuntu@146.181.39.4:/tmp/
sudo docker cp /tmp/endonautica.md <container>:/tmp/endonautica.md
sudo docker exec <container> python manage.py seed_endonautica_md --path /tmp/endonautica.md
sudo docker exec <container> python manage.py index_knowledge
```

Variables de entorno requeridas: `SECRET_KEY`, `DATABASE_URL`, `DEEPSEEK_API_KEY`  
Variables opcionales: `DEBUG`, `ALLOWED_HOSTS`, `OPENROUTER_API_KEY`, `AI_MODEL`  
Pagos: `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_MODE`, `PAYPAL_WEBHOOK_ID`, `MERCADOPAGO_ACCESS_TOKEN`, `MERCADOPAGO_WEBHOOK_SECRET`

**Coolify API** (acceso desde el servidor vía SSH, base: `http://localhost:8000/api/v1/`):
- App UUID: `psaza8rlhc5vk7gsmu4xc8l8`
- PATCH no funciona para env vars — usar DELETE + POST

---

## Regla de cambios: un cambio no es solo un cambio

Cuando se modifica cualquier feature (costo, nombre, comportamiento, flujo), hay que revisar y actualizar **todos** los puntos donde esa feature tiene representación:

| Touchpoint | Qué revisar |
|------------|-------------|
| `templates/payments/planes.html` | Precios, fractones incluidos, descripción de features por plan |
| `templates/accounts/perfil.html` | Sección de suscripciones, packs, beneficios |
| `templates/accounts/dashboard.html` | Shortcuts, misiones visibles |
| `templates/tokens/balance.html` | Tabla de costos, descripción de cada feature |
| `data-ft-tip` / `data-tip` en templates | Tooltips deben reflejar el costo real actualizado |
| `tokens/service.py` → `TOKEN_COSTS` | Costo real en código |
| `settings.py` → `TOKEN_COSTS` | Costo en settings si está ahí |
| `templates/terminos.astro` (landing) | Si el cambio afecta condiciones de uso |
| `templates/professionals/` | Si el cambio afecta a practicantes |
| Este CLAUDE.md | Actualizar la sección de pendientes y costos |

**Regla práctica:** antes de cerrar cualquier tarea que toque economía, UI o flujo de usuario, preguntar "¿hay algún tooltip, texto de planes, o referencia en otra página que describe esto?" Si la respuesta es sí, actualizar también.

---

## Modelo Espejo — restricciones por plan

| Plan | Sesiones | Duración |
|------|----------|----------|
| Free | 1 por día (reutiliza la existente si ya hay una de hoy) | 45 min máx por sesión |
| Navegante | Ilimitadas | Sin límite |
| Practicante | Ilimitadas | Sin límite |

**Implementación:** `mirror/views.py` → `chat_new` controla creación, `chat_message` controla tiempo con `datetime.timedelta(minutes=45)`.

**Sistema prompt:** `mirror/prompts/espejo_system.txt` — cargado en cada request vía `_load_system_prompt()`. Contiene: rol de espejo (no terapeuta, no diagnóstico), tono y estilo, protocolos de crisis (ideación suicida 3 niveles, voces psicóticas, pánico agudo, disociación, violencia doméstica, fantasías de daño), y modo "revelación de patrones" (fase 1 sostén → fase 2 nombrar el patrón con referencia al contexto psicométrico).

**Contexto inyectado:** `user_intent_context()` (onboarding_priorities) + `user_history_context()` (tests psicométricos, sesión Espejo anterior, bitácora, lectura de nacimiento) + `_retrieve_context()` (RAG: top-5 chunks de KnowledgeChunk por similitud coseno o keyword). Implementado en `config/ai_client.py` y `mirror/views.py::_get_reply()`. `max_tokens` = 700.

**RAG — KnowledgeChunk:** 139 chunks en producción: 101 marcos teóricos (Jung, Freud, Castaneda, Grinberg, Hawkins, Bourbeau, Ruiz, Campbell, Naranjo, Gendlin, Perls, Tolle, Wilber, Lao Tse...) + 38 chunks conceptuales del libro Endonautica (secciones `##`, primeros 3000 chars c/u — "head approach"). Retrieval: semántico con `get_embedding()` (OpenRouter `openai/text-embedding-3-small`) o keyword fallback. Comandos: `seed_knowledge` (marcos teóricos, en startCommand), `seed_endonautica_md` (libro, manual), `index_knowledge` (embeddings, manual con `OPENROUTER_API_KEY`).

**Nota embeddings:** DeepSeek NO tiene API de embeddings. Siempre usar OpenRouter para `get_embedding()`.

**Multimedia:** `ChatMessage.attachment` (FileField) + `attachment_type` (image/pdf/doc). Vista `chat_message()` procesa adjuntos: imágenes → base64 → visión multimodal, PDFs/docs → extracción de texto → contexto. Requiere PyPDF2, python-docx.

**Multimedia:** `ChatMessage.attachment` (FileField) + `attachment_type` (image/pdf/doc). Vista `chat_message()` procesa adjuntos: imágenes → base64 → visión multimodal, PDFs/docs → extracción de texto → contexto. Requiere PyPDF2, python-docx.

---

## Email marketing (Listmonk — al 2026-06-23)

Listas activas:
| Lista | ID | UUID |
|-------|----|------|
| Usuarios App | 4 | — |
| Practicantes | 5 | `574f7450-0663-4848-95e5-8ebe4765a33a` |
| Leads App | 7 | — |
| Lanzamiento | 8 | `431ebe70-b897-416b-9016-daea6acc030c` |

9 campañas email en draft en Listmonk — activar desde `https://mail.endonautas.cl`.
Secuencias: 3 emails × Lanzamiento (leads sin cuenta), 3 × Leads App (free → Navegante), 3 × Practicantes (terapeutas).

SMTP Brevo: `smtp-relay.brevo.com:587` · login `aaccf1001@smtp-brevo.com` · verificado con smtplib.

### Módulo programático: `accounts/listmonk.py`

Integración API Basic Auth. Todas las funciones fallan silenciosamente.

```python
subscribe_user(email, plan='free', name='')
    # Suscribe a las listas del plan. Mapeo:
    # free        → [4 Usuarios App, 7 Leads App]
    # navegante   → [4 Usuarios App]
    # practicante → [4 Usuarios App, 5 Practicantes]
    # empresa     → [4 Usuarios App, 5 Practicantes]

update_subscriber_lists(email, plan)
    # Busca al suscriptor y agrega las listas del nuevo plan (para upgrades)

send_welcome_email(email, name='')
    # Envía email de bienvenida vía TX endpoint con WELCOME_TEMPLATE_ID = 7
```

**Activación automática:** `accounts/signals.py` llama a `subscribe_user` + `send_welcome_email` en el `post_save` de User cuando `created=True`. Cubre registro por email y Google OAuth.

---

## Pendientes técnicos (al 2026-06-23)

### Alta prioridad
1. ~~**Espejo IA — enriquecimiento de contexto**~~ ✅ RESUELTO 2026-06-23
2. ~~**Espejo — prompt revelación de patrones**~~ ✅ RESUELTO 2026-06-23 (`espejo_system.txt`)
3. ~~**Espejo — RAG con marcos teóricos**~~ ✅ RESUELTO 2026-06-23 (`seed_knowledge`, `_retrieve_context`, `get_embedding`)
4. ~~**Espejo — multimedia (foto/doc/voz)**~~ ✅ RESUELTO 2026-06-23 (ChatMessage.attachment, Web Speech API)

5. **Practitioners views** — gestionar perfiles de clientes, asignar tests, ver resultados

6. ~~**Reportes** (`reports` app vacía)~~ ✅ RESUELTO 2026-06-29 — KPI semanal automático, ver sección abajo

### Media prioridad
7. **Tests psicométricos a auditar** (implementación incompleta):
   - ECR: necesita ECR-R (36 ítems) o ECR-12 en likert7
   - SOC-29: actualmente 7 ítems, versión validada tiene 29 en bipolar likert7
   - MAIA: actualmente 21 ítems, MAIA-2 tiene 37 en escala 0-5
   - DERS-16: actualmente 8 ítems, versión validada tiene 16 en likert5
   - PSQI: suma simple, scoring real tiene 7 componentes ponderados

5. **Fondos árbol y archipiélago** — en AESTHETIC_CHOICES pero sin implementación visual

### Baja prioridad
6. Eliminar theme switcher temporal de `base.html` (hardcodear paleta definitiva)
7. OAuth Google (panel admin)

---

---

## App `reports` — KPI semanal automático (2026-06-29)

### Qué hace
Cada lunes 9:07am (cron Oracle) corre `python manage.py weekly_kpi`:
1. Calcula KPIs de Django ORM (registros, retención, MRR)
2. Fetch métricas Listmonk, Umami, SerpBear
3. Scraping RRSS → seguidores por plataforma
4. Top contenido por plataforma (qué video/post tuvo más engagement)
5. Clasifica escenario (verde/amarillo/rojo), guarda `KPISnapshot`, envía email a `fjeriacastro@gmail.com`

### Archivos del módulo

| Archivo | Función |
|---|---|
| `reports/management/commands/weekly_kpi.py` | Comando principal — orquesta todo |
| `reports/services/social_scraper.py` | Seguidores por red: IG (Meta API), TikTok/LinkedIn (Playwright), YouTube (API v3), Facebook (Meta API) |
| `reports/services/content_metrics.py` | Top post/video por plataforma — YouTube (views), IG (likes+reach), Facebook (reach) |
| `reports/services/kpi_calculator.py` | KPIs Django ORM: registros, activación, retención, MRR |
| `reports/services/markdown_renderer.py` | Renderiza el MD del reporte (y HTML para email) |
| `reports/services/scenario_classifier.py` | Clasifica escenario verde/amarillo/rojo |
| `reports/models.py` | `KPISnapshot` — snapshot semanal completo |
| `reports/migrations/` | 0001→0007 — incluye campos RRSS y `top_content` JSONField |

### Integraciones activas y sus credenciales (en Coolify DB)

| Variable | Valor | Para qué |
|---|---|---|
| `META_PAGE_TOKEN` | token largo (no expira) | Instagram + Facebook Graph API |
| `META_IG_ID` | `17841408150037364` | Instagram Business Account ID |
| `META_PAGE_ID` | `112522961877445` | Facebook Page ID (Endonautas) |
| `YOUTUBE_API_KEY` | `AIzaSyB...` | YouTube Data API v3 |
| `YOUTUBE_CHANNEL_ID` | `UC9hqN2eNx1X-U-2ev9GUsCg` | Canal YouTube Endonautas |
| `YOUTUBE_USERNAME` | `endonautas` | Handle YouTube |
| `TIKTOK_USERNAME` | `endonautas` | Handle TikTok (scraping Playwright) |
| `LINKEDIN_COMPANY` | `endonautas` | Slug empresa LinkedIn (scraping Playwright) |

### Meta App
- App ID: `1553716769663324` · Secret: en `/home/nikka/Proyectos/endonautas/tokn-meta.txt`
- Permisos activos: `instagram_basic`, `pages_show_list`, `pages_read_engagement`, `read_insights`
- **Pendiente:** agregar `instagram_manage_insights` → regenerar token en Graph Explorer para activar reach/guardados por post

### Playwright en producción
- Chromium instalado manualmente en el contenedor (`playwright install chromium --with-deps`)
- **⚠️ Se pierde en cada redeploy.** Para que persista: agregar `playwright install chromium --with-deps &&` al inicio del Start Command en Coolify UI

### Métricas actuales (2026-06-29)
| Red | Seguidores |
|---|---|
| Instagram | 959 |
| TikTok | 689 |
| Facebook | 148 |
| YouTube | 25 |
| LinkedIn | 3 |

### Top contenido
- Sección `## Contenido — Top esta semana` aparece en el email solo cuando hay posts con datos
- YouTube ya muestra el video más visto del canal (20 videos, 3.4k views totales)
- Instagram y Facebook aparecerán automáticamente cuando se publique contenido

### Dry-run de prueba
```bash
docker exec <container> python manage.py weekly_kpi --week 2026-W27 --dry-run
```

---

## Archivos clave

| Archivo | Contenido |
|---------|-----------|
| `templates/base.html` | CSS global, SPA nav, Three.js cosmos, túnel mandala, `__switchAesthetic` |
| `accounts/context_processors.py` | Inyecta `map_aesthetic` y `color_palette` en todos los templates |
| `accounts/models.py` | User (email-based), UserProfile |
| `accounts/views.py` | Auth, perfil, onboarding |
| `accounts/plan_utils.py` | `plan_at_least()`, `upgrade_wall()`, `FREE_TEST_SLUGS` |
| `accounts/listmonk.py` | `subscribe_user()`, `update_subscriber_lists()`, `send_welcome_email()` — Listmonk API |
| `mirror/views.py` | Espejo IA — `_get_reply()`, `_load_system_prompt()`, `chat_new()`, `chat_message()` |
| `mirror/prompts/espejo_system.txt` | System prompt del Espejo — editar aquí para cambiar comportamiento |
| `config/ai_client.py` | `call_ai()` + `user_intent_context()` — wrapper IA compartido por toda la app |
| `birth/calculators.py` | Lógica completa de cálculo astral/HD/saju |
| `birth/meanings.py` | Diccionarios de significados en español (grande) |
| `oraculo/interpretations.py` | Llamadas IA para tarot/iching/fractal |
| `psychometrics/views.py` | Tests + `mapa_patrones()` + `mapa_patrones_resultado()` + `_generate_mapa_insight()` |
| `psychometrics/evaluator.py` | Lógica de evaluación por test, dispatcher, polaridad |
| `psychometrics/management/commands/seed_tests.py` | Seed 35 tests |
| `templates/psychometrics/mapa_patrones.html` | Intro lead magnet — 3 tests en secuencia |
| `templates/psychometrics/mapa_patrones_resultado.html` | Resultado del Mapa + upgrade trigger |
| `templates/oraculo/tarot.html` | Tirada + animaciones revelación |
| `templates/oraculo/iching.html` | Tirada + divs animados hex lines |
| `templates/oraculo/fractal.html` | Flip carta + interpPanel diferido |

---

## Notas metodológicas
- Tests `clinical`: ítems exactos de instrumentos validados en español → siempre mostrar disclaimer de solo-lectura
- Tests `adapted`: instrumento como referencia con adaptaciones → **siempre mostrar disclaimer**
- Tests `custom`: herramientas de reflexión endonauta → **no son diagnóstico**
- PHQ-9 en lugar de BDI-II (libre de copyright, Kroenke & Spitzer 2001)
- Dirty Dozen en lugar de SD3 (Jonason & Webster 2010, 12 ítems)
