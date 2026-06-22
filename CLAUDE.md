# CLAUDE.md — App Endonautas

> Archivo de contexto técnico para Claude. Leer completo antes de tocar código.

## Comando siempre: `python3 manage.py` (nunca `python`)

## Stack
- Django 6.0.4, SQLite (dev) / PostgreSQL Railway (prod)
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
| `tokens` | ✅ activa | Fractones: balance, transacciones, misiones, Hotmart |
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

### `tokens.TokenBalance`
```python
permanent     int   # ganados + comprados, no expiran
monthly       int   # recarga del plan, se reemplaza cada ciclo
# .spend(amount, reason) — descuenta monthly primero, luego permanent
# .credit_permanent / .credit_monthly
# balance = permanent + monthly (property)
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

## Sistema de Fractones

### Economía
| Plan | Fractones/mes (expiran) |
|------|------------------------|
| free | 100 |
| navegante ($10) | 600 |
| practicante ($39) | 3.000 |

### Costos (TOKEN_COSTS en settings)
```python
'espejo_exchange': 4    # 1 mensaje + respuesta
'ai_insight':      20
'report':          30
```

### API pública (`tokens/service.py`)
```python
from tokens.service import spend, has_balance, credit_mission, renew_monthly
spend(user, 'espejo_exchange')      # True/False — descuenta y registra
has_balance(user, 'ai_insight')     # True/False — sin descontar
credit_mission(user, 'first_espejo')  # idempotente
```

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
python manage.py fix_db_state && python manage.py migrate --noinput && python manage.py create_admin && python manage.py seed_tests && gunicorn config.wsgi --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:8000
```

Variables de entorno requeridas: `SECRET_KEY`, `DATABASE_URL`, `DEEPSEEK_API_KEY`  
Variables opcionales: `DEBUG`, `ALLOWED_HOSTS`, `OPENROUTER_API_KEY`, `AI_MODEL`  
Pagos: `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_MODE`, `PAYPAL_WEBHOOK_ID`, `MERCADOPAGO_ACCESS_TOKEN`, `MERCADOPAGO_WEBHOOK_SECRET`

**Coolify API** (acceso desde el servidor vía SSH, base: `http://localhost:8000/api/v1/`):
- App UUID: `psaza8rlhc5vk7gsmu4xc8l8`
- PATCH no funciona para env vars — usar DELETE + POST

---

## Pendientes técnicos (al 2026-06-18)

### Alta prioridad
1. **Fractones en features existentes**
   - Espejo: `spend(user, 'espejo_exchange')` antes del API call + `credit_mission(user, 'first_espejo')`
   - AI Insights: `spend(user, 'ai_insight')` antes de llamar DeepSeek en test_result
   - Onboarding: `credit_mission(user, 'onboarding')` al completar el flow

2. **Practitioners views** — gestionar perfiles de clientes, asignar tests, ver resultados

3. **Reportes** (`reports` app vacía) — dashboard agregado con evolución temporal

### Media prioridad
4. **Tests psicométricos a auditar** (implementación incompleta):
   - ECR: necesita ECR-R (36 ítems) o ECR-12 en likert7
   - SOC-29: actualmente 7 ítems, versión validada tiene 29 en bipolar likert7
   - MAIA: actualmente 21 ítems, MAIA-2 tiene 37 en escala 0-5
   - DERS-16: actualmente 8 ítems, versión validada tiene 16 en likert5
   - PSQI: suma simple, scoring real tiene 7 componentes ponderados

5. **Hotmart packs** — crear 3 productos, agregar offer codes a env, testear webhook
   ```python
   HOTMART_PACK_200   = offer_code...
   HOTMART_PACK_600   = offer_code...
   HOTMART_PACK_2000  = offer_code...
   ```

6. **Fondos árbol y archipiélago** — en AESTHETIC_CHOICES pero sin implementación visual

### Baja prioridad
7. Eliminar theme switcher temporal de `base.html` (hardcodear paleta definitiva)
8. OAuth Google (panel admin)

---

## Archivos clave

| Archivo | Contenido |
|---------|-----------|
| `templates/base.html` | CSS global, SPA nav, Three.js cosmos, túnel mandala, `__switchAesthetic` |
| `accounts/context_processors.py` | Inyecta `map_aesthetic` y `color_palette` en todos los templates |
| `accounts/models.py` | User (email-based), UserProfile |
| `accounts/views.py` | Auth, perfil (guarda avatar + aesthetic + palette), onboarding |
| `birth/calculators.py` | Lógica completa de cálculo astral/HD/saju |
| `birth/meanings.py` | Diccionarios de significados en español (grande) |
| `oraculo/interpretations.py` | Llamadas IA para tarot/iching/fractal |
| `tokens/service.py` | API pública spend/credit/missions |
| `tokens/signals.py` | Earn automático al completar tests |
| `tokens/hotmart.py` | Webhook: suscripciones + packs |
| `psychometrics/evaluator.py` | Lógica de evaluación por test, dispatcher, polaridad |
| `psychometrics/management/commands/seed_tests.py` | Seed 35 tests |
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
