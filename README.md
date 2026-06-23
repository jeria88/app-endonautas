# App Endonautas

Aplicación web de autoconocimiento construida con Django 6. Integra astrología occidental, Human Design, cosmología china (Saju/BaZi), tests psicométricos, espejo de conflictos con RAG y comunidad nativa.

## Stack

| Capa | Tecnología |
|------|-----------|
| Framework | Django 6.0.4 |
| Servidor | Gunicorn (2 workers, 2 threads) |
| Base de datos | PostgreSQL 16 (Oracle Cloud prod) / SQLite (dev) |
| Archivos estáticos | WhiteNoise |
| Deploy | Coolify v4.1.2 en Oracle Cloud ARM64 |
| IA | DeepSeek-chat via API compatible OpenAI / OpenRouter |
| Auth social | Google OAuth 2.0 (allauth) |
| Astrología | kerykeion 5.12.8 |
| Zona horaria | timezonefinder 8.2.4 + pytz |
| Cosmología china | sxtwl 2.0.7 |

---

## Infraestructura de producción

### Servidor
- **Oracle Cloud ARM64** — IP: `146.181.39.4`
- **Coolify v4.1.2** (PaaS self-hosted) en puerto 8000 internamente; expuesto vía Traefik v3.6
- **Traefik v3.6** como reverse proxy / TLS terminator (Let's Encrypt automático)

### Proyectos Coolify

| Proyecto | UUID | Apps |
|----------|------|------|
| Endonautas | `bmyudzu3wkclojezggc5tfd1` | app Django + PostgreSQL |
| Agency | `qf3aoateif565dzl1i8bd55k` | n8n + Flowise + Redis |
| Herramientas | `k1ui2bvkptqneglns34gj422` | Umami + Uptime Kuma + Listmonk + Serpbear |

### App Endonautas en Coolify

| Campo | Valor |
|-------|-------|
| App UUID | `psaza8rlhc5vk7gsmu4xc8l8` |
| DB UUID | `ox72b94tsgzuhcf0768xipf1` |
| Repo | `github.com/jeria88/app-endonautas` |
| Branch | `master` |
| Auto-deploy | Sí — push a master activa deploy en Coolify |
| URL | `https://app.endonautas.cl` |

---

## Stack de herramientas (proyecto Herramientas)

| Servicio | URL | Función |
|---------|-----|---------|
| Umami | `https://analytics.endonautas.cl` | Analytics web (open source) |
| Uptime Kuma | `https://status.endonautas.cl` | Monitoreo de uptime |
| Listmonk | `https://mail.endonautas.cl` | Email marketing |
| Serpbear | `https://seo.endonautas.cl` | Seguimiento de keywords SEO |

### Credenciales de acceso

> Guardar en gestor de contraseñas. No compartir.

| Servicio | Usuario | Contraseña |
|---------|---------|-----------|
| Umami | admin | `Endo44e4e1af3cfda5e8!` |
| Uptime Kuma | admin | `Endo2026Status!` |
| Listmonk | admin | `Endo2026Mail!` |
| Serpbear | admin (UI) | configurar en primer acceso |

### Umami — sitios trackeados

| Sitio | Website ID |
|-------|-----------|
| Landing (astro-endonautas) | `e03fa69e-9931-411c-9838-7f6ffea90426` |
| App Django | `9aa0968f-0cd2-4c77-9c70-fbb745d31754` |

Script de tracking (ya integrado en ambos frontends):
```html
<script defer data-website-id="<SITE_ID>" src="https://analytics.endonautas.cl/script.js"></script>
```

### Uptime Kuma — monitores configurados

6 monitores activos (vía inserción directa en SQLite `/app/data/kuma.db`):
1. App Endonautas — `https://app.endonautas.cl`
2. Landing — `https://endonautas.cl`
3. Umami Analytics — `https://analytics.endonautas.cl`
4. Listmonk Mail — `https://mail.endonautas.cl`
5. Serpbear SEO — `https://seo.endonautas.cl`
6. Coolify Panel — `http://146.181.39.4:8000`

### Listmonk — configurado

SMTP configurado con Brevo SMTP relay:
- Host: `smtp-relay.brevo.com` · Puerto: `587` · Auth: STARTTLS / login
- Login SMTP: `aaccf1001@smtp-brevo.com`
- From: `hola@endonautas.cl`

| Lista | ID | Descripción |
|-------|----|-------------|
| Endonautas — Usuarios App | 1 | Registrados en app.endonautas.cl |
| Endonautas — Interesados | 2 | Leads de la landing page |
| Endonautas — Newsletter | 3 | Suscriptores al blog/contenido |

**API programática:** usuario `api_claude` tipo `api` — autenticación con token en campo `password` (plain text en basic auth: `api_claude:<token>`).

**Templates TX disponibles:** ID 3 (Sample transactional) — usar para emails automáticos vía `/api/tx`.

### SerpBear — configurado

Dominio `endonautas.cl` agregado vía SQLite directo (la UI requiere JWT con env var `SECRET` que no coincide con `SECRETKEY` en el contenedor — workaround confirmado).

Keywords configuradas basadas en estrategia SEO de 3 capas:
- Capa 1 (autoconocimiento): términos base
- Capa 2 (viaje interior): términos de proceso
- Capa 3 (nivel de conciencia): términos de profundidad

Para agregar keywords nuevas: `docker exec -it <serpbear_container> sh`, modificar SQLite en `/app/data/database.sqlite`.

---

## Deploy (Coolify — producción actual)

### Proceso automático

```
git push origin master
    → Coolify detecta el push vía webhook de GitHub
    → Build Docker con el Dockerfile del repo
    → Corre el startCommand en el nuevo contenedor
    → Traefik actualiza el routing automáticamente
```

### startCommand

```bash
python manage.py fix_db_state && \
python manage.py migrate --noinput && \
python manage.py create_admin && \
python manage.py seed_tests && \
python manage.py seed_regulacion && \
python manage.py seed_momentos && \
python manage.py seed_foros && \
python manage.py seed_fractal && \
python manage.py seed_terapeuta && \
python manage.py seed_missions && \
gunicorn config.wsgi --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:8000
```

### API Coolify (para administración)

```
Base URL: http://localhost:8000/api/v1/  (desde el servidor)
Bearer token: 2|I36Uuw6S5funJQG3zcgY7vTBitE5kOE8PwIkQd1Bc3831ca2

# Deploy manual de la app
curl -X POST "http://localhost:8000/api/v1/deploy?uuid=psaza8rlhc5vk7gsmu4xc8l8" \
  -H "Authorization: Bearer <token>"
```

### Comandos de management propios

| Comando | Función |
|---------|---------|
| `fix_db_state` | Repara inconsistencias de migraciones antes de `migrate` |
| `create_admin` | Crea superusuario desde env vars si no existe |
| `seed_tests` | Pobla 35 tests psicométricos iniciales |
| `seed_fractal_cards` | Pobla cartas del Oráculo Fractal |

---

## Variables de entorno (producción)

Configuradas en Coolify UI — Environment Variables del proyecto Endonautas.

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `SECRET_KEY` | Sí | Django secret key |
| `DEBUG` | No | `False` en prod |
| `DATABASE_URL` | Sí | `postgres://endonautas:<pass>@db:5432/endonautas` |
| `ALLOWED_HOSTS` | Sí | `app.endonautas.cl,localhost` |
| `DEEPSEEK_API_KEY` | Para IA | Clave API DeepSeek |
| `OPENROUTER_API_KEY` | Para IA | Alternativa a DeepSeek |
| `GOOGLE_CLIENT_ID` | OAuth | ID de Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | OAuth | Secret de Google Cloud Console |
| `DEFAULT_FROM_EMAIL` | No | `hola@endonautas.cl` |

---

## Arquitectura de apps

```
config/           — settings, urls raíz, wsgi
accounts/         — auth (email-based + Google OAuth), UserProfile, planes
birth/            — lecturas de nacimiento (astral, HD, saju)
oraculo/          — Tarot Terapéutico, I Ching, Oráculo Fractal
mirror/           — espejo de conflictos (RAG + DeepSeek), sueños, regulación
psychometrics/    — tests psicométricos con insights de IA
tokens/           — sistema de Fractones (balance, transacciones, misiones)
community/        — feed social, foros, mensajes directos
terapeuta/        — modo terapeuta: diagnóstico por framework, técnicas somáticas
practitioners/    — directorio de practicantes, perfiles temporales
```

### Rutas principales

```
/                   — home / dashboard
/registro/          — registro por email
/login/             — login
/perfil/            — perfil del usuario
/nacimiento/        — hub de lecturas de nacimiento
/nacimiento/astral/ — carta astral
/nacimiento/hd/     — Human Design
/nacimiento/saju/   — Saju / BaZi
/oraculo/           — hub de oráculos
/oraculo/tarot/     — Tarot Terapéutico
/oraculo/iching/    — I Ching
/oraculo/fractal/   — Oráculo Fractal
/tests/             — tests psicométricos
/espejo/            — espejo de conflictos
/suenos/            — diario de sueños
/regulacion/        — técnicas somáticas / regulación
/terapeuta/         — modo terapeuta
/comunidad/         — feed social (posts, reacciones, comentarios)
/foros/             — foros por tema
/mensajes/          — mensajes directos
/tests/mapa-patrones/          — lead magnet: Mapa de Patrones Personales
/tests/mapa-patrones/resultado/ — resultado del mapa con análisis IA cruzado
/practicantes/      — directorio de practicantes
/admin/             — panel de administración Django
```

---

## Mapa del código (codegraph)

Análisis estático al 2026-06-20 — `codegraph init`:

| Métrica | Valor |
|---------|-------|
| Archivos Python | 138 |
| Nodos totales | 1.054 |
| Dependencias (edges) | 1.431 |
| DB codegraph | 1.94 MB |

**Nodos por tipo:**

| Tipo | Cantidad |
|------|----------|
| import | 251 |
| function | 186 |
| variable | 160 |
| class | 141 |
| file | 138 |
| route | 90 |
| method | 88 |

**Archivos más densos (símbolos):**

| Archivo | Símbolos | Nota |
|---------|----------|------|
| `psychometrics/evaluator.py` | 40 | lógica de evaluación + dispatcher |
| `terapeuta/views.py` | 37 | el view más complejo de la app |
| `birth/calculators.py` | 34 | 3 calculadoras + helpers |
| `oraculo/services/tarot_service.py` | 35 | tiradas + interpretación |
| `config/settings.py` | 58 | configuración completa |

---

## Módulo: accounts

**Modelo User** — hereda `AbstractUser`, usa `email` como `USERNAME_FIELD` (sin username).

**Modelo UserProfile** (OneToOne a User):
- `plan`: free / navegante / practicante / empresa
- `map_aesthetic`: cosmos / mandala / archipielago / arbol
- `onboarding_completed`, `onboarding_step`
- Campos Hotmart: `hotmart_purchase_id`, `hotmart_product_id`, `plan_expires_at`

### Registro y onboarding (señales)

`accounts/signals.py` — `post_save` en User: al crear usuario (cualquier path, email o Google OAuth):
1. Crea `UserProfile`
2. Crea `TokenBalance` y acredita `PLAN_MONTHLY_TOKENS['free']` fractones con reason `'signup'`
3. Crea `ReferralCode`

---

## Módulo: birth (núcleo técnico)

El módulo más complejo de la app. Genera tres tipos de lecturas a partir de fecha, hora y lugar de nacimiento.

### Modelos

**BirthData** (OneToOne a User o TemporaryProfile):
```
birth_date      DateField
birth_time      TimeField (opcional)
city            CharField(150)
country         CharField(100)
latitude        FloatField
longitude       FloatField
timezone_str    CharField(60)   — derivado de lat/lng vía timezonefinder
gender          CharField(1)    — M / F, requerido para Daewoon (Saju)
```

**BirthReport** (FK a BirthData):
```
report_type     astral | hd | saju
status          pending | processing | done | error
raw_data        JSONField — todos los datos calculados
ai_reading      TextField — lectura narrativa (opcional, futura integración)
error_message   TextField
completed_at    DateTimeField
```

Constraint: `unique_together = ('birth_data', 'report_type')` — un reporte por tipo por persona.

### Calculadoras (`birth/calculators.py`)

**`calculate_astral_chart(bp)`**
- Usa `kerykeion` (tropical, Placidus)
- Extrae: 10 planetas + Nodo Norte + Quirón (sign, house, degree, retrograde)
- Ascendente y Medio Cielo con grado
- Enriquece cada campo con `planet_meaning`, `sign_meaning`, `meaning` (ASC/MC) desde `meanings.py`

**`calculate_hd_chart(bp)`**
- Usa `kerykeion` para posición solar natal (Personalidad)
- Calcula fecha de Diseño: 88° antes del Sol natal (aritmética de arco solar con `pytz` para UTC)
- Extrae: Tipo, Estrategia, Autoridad, Perfil (líneas Sol P/D), Definición, No-Yo, Firma
- Centros definidos vía activación de canales (64 hexagramas I Ching)
- Cruz de Encarnación (4 puertas: Sol P, Tierra P, Sol D, Tierra D)
- `HD_WHEEL_START = 302.0` — constante de inicio del zodíaco HD para cálculo de puertas
- Enriquece todo desde `meanings.py`

**`calculate_saju_chart(bp)`**
- Usa `sxtwl` para los 4 Pilares (Año, Mes, Día, Hora)
- Corrección a Hora Solar Verdadera via offset de longitud
- Extrae: Tallo Celestial + Rama Terrestre por pilar, elemento, animal
- Balance elemental (Madera, Fuego, Tierra, Metal, Agua)
- Señor del Día, Elemento Dominante, Animal del año lunar
- **Daewoon** (Grandes Ciclos de 10 años): requiere gender para dirección (M avanza, F retrocede por ciclo); calcula edad de inicio y año de inicio/fin de cada ciclo

**`_ensure_timezone(bp)`** — re-deriva timezone desde lat/lng antes de cada cálculo (fix para registros con `timezone_str = 'UTC'` por defecto).

**`_needs_recalc(report)`** — detecta reportes en caché que no tienen campos de meanings (sentinel: `planet_meaning`, `type_meaning`, `day_master_meaning`) y fuerza recálculo en el siguiente acceso.

### Meanings (`birth/meanings.py`)

Diccionarios de significados en español, profundidad real de autoconocimiento (no enciclopédico). Formato: 3-6 oraciones, segunda persona, incluye don y sombra/reto.

```python
PLANET_MEANINGS        # 10 planetas + Nodo + Quirón
SIGN_MEANINGS          # 12 signos × planeta
ASC_MEANINGS           # 12 signos como Ascendente
MC_MEANINGS            # 12 signos como Medio Cielo
HD_TYPE_MEANINGS       # 5 tipos HD
HD_PROFILE_MEANINGS    # 12 perfiles (todas las combinaciones 1-6)
HD_AUTHORITY_MEANINGS  # 7 autoridades
HD_NOT_SELF_MEANINGS   # 5 temas del No-Yo
HD_SIGNATURE_MEANINGS  # 5 firmas
HD_DEFINITION_MEANINGS # 5 definiciones
HD_CENTER_MEANINGS     # 9 centros
HD_CHANNEL_MEANINGS    # 33 canales definidos
HD_PLANET_MEANINGS     # 13 planetas en contexto HD (distinción P vs D)
HD_PERSONALITY_DESIGN_INTRO  # párrafo introductorio para la sección
SAJU_PILLAR_MEANINGS   # 4 pilares (año/mes/día/hora)
SAJU_ELEMENT_MEANINGS  # 5 elementos
SAJU_DAYMASTER_MEANINGS # 10 Señores del Día (10 Tallos)
SAJU_ANIMAL_MEANINGS   # 12 animales
SAJU_STEM_SHORT        # 10 Tallos — descripciones breves para Daewoon
```

### Flow de cálculo

```
Usuario accede a /nacimiento/astral/ (o hd/ o saju/)
    → view busca BirthReport existente
    → si no existe: crea con status='pending', redirige (polling o recarga)
    → si status='done' y _needs_recalc(): recalcula y guarda
    → si status='done': renderiza template con raw_data
    → si status='error': muestra mensaje de error
    → si status='pending'/'processing': muestra "Calculando…"
```

---

## Módulo: oraculo

Tres sistemas de oráculo terapéutico con interpretación IA y animaciones de revelación.

### Modelos
- **CartaFractal** — Arcanos Mayores + Sefirot (número, verbo, descripción breve/larga)
- **SesionOraculo** — UUID PK, usuario, tipo (`tarot`/`iching`/`fractal`), pregunta, guardada
- **LecturaTarot** — tipo de tirada, cartas (JSONField), interpretación
- **LecturaIChing** — líneas (JSONField), hexagrama primario + secundario (número + nombre), interpretación
- **LecturaFractal** — FK CartaFractal, invertida, interpretación

### Tarot Terapéutico (Jodorowsky)
- 78 cartas; tiradas de 1, 3 o 5 cartas
- Imágenes en `static/img/tarot/` nombradas por número
- Reverso: `static/img/tarot/cardback.jpg`
- Interpretación: DeepSeek via `oraculo/interpretations.py`
- **Revelación animada:** `@keyframes card-in` con stagger de 120ms por carta; `#interpPanel` aparece 770ms después de la última carta

### I Ching
- Tirada de 3 monedas × 6 líneas, 64 hexagramas con líneas móviles
- Líneas del hexagrama primario: divs HTML con clases `.hex-line.yang/.yin[.movil]` → stagger bottom-to-top cada 160ms
- Líneas móviles: pulso CSS `@keyframes movil-pulse`
- Hexagrama secundario (cuando hay líneas móviles): SVG via `renderHexLines()`
- Cadena de timing total: ~3800ms hasta interpretación

### Oráculo Fractal
- Cartas Arcanos Mayores + Sefirot con mecánica de flip (reverso → frente)
- `#interpPanel` oculto hasta 700ms después del flip (`@keyframes carta-in` con spring)
- `#flipHint` se desvanece al hacer flip

---

## Módulo: terapeuta

Modo terapeuta para sesiones de orientación integrativa.

- **DIAGNOSIS_CATALOG** — catálogo de diagnósticos por área con keywords
- **FRAMEWORKS_AND_TECHNIQUES** — técnicas somáticas / frameworks terapéuticos
- **KEYWORD_TO_FRAMEWORKS** — mapa de palabras clave a frameworks recomendados
- **QUESTIONS_BANK** — banco de preguntas por framework
- Visualizaciones simbólicas por marco terapéutico
- IA: DeepSeek para fundamentación pedagógica por instrucción

---

## Módulo: mirror (Espejo de Conflictos)

- **RAG** sobre base de conocimiento (`KnowledgeChunk` con embeddings en JSONField)
- **ChatSession** / **ChatMessage** — historial de conversación por usuario
- `conflict_summary` y `return_question` — campos de memoria versionada (guardados, pendiente inyectarlos al prompt)
- **DreamEntry** — diario de sueños con tags, fecha, is_lucid, reality_check
- **Regulación** — técnicas somáticas (view independiente)
- IA: DeepSeek vía `settings.DEEPSEEK_API_KEY`

### Restricciones por plan
| Plan | Sesiones | Duración |
|------|----------|----------|
| Free | 1/día (reutiliza sesión existente) | 45 min máx |
| Navegante+ | Ilimitadas | Sin límite |

### System prompt
`mirror/prompts/espejo_system.txt` — actualmente optimizado para sostén/presencia. Pendiente: modo revelación de patrones con contexto psicométrico del usuario.

---

## Módulo: psychometrics (Tests)

- **Test** — nombre, dimensión (12 dimensiones del mapa), tipo de instrumento
- **Question** + **Choice** — preguntas con opciones y pesos
- **TestResult** — respuestas JSON + score + insight generado por IA
- Seeds vía `python manage.py seed_tests` (comando de management)

Dimensiones: identidad, emociones, cuerpo, vínculos, sombra, espiritualidad, sueños, propósito, comunidad, abundancia, creatividad, mente

### Mapa de Patrones Personales (lead magnet)

Feature de conversión principal. Tres tests gratuitos secuenciados que la IA cruza para identificar patrones.

| Test | Slug | Dimensión |
|------|------|-----------|
| Big Five | `big-five-inventario-de-personalidad` | Personalidad |
| Heridas de la Infancia | `heridas-de-la-infancia-lise-bourbeau` | Origen |
| Dirty Dozen | `dirty-dozen-triada-oscura` | Sombra |

- `/tests/mapa-patrones/` — intro con progreso
- `/tests/mapa-patrones/resultado/` — 3 patrones IA + upgrade trigger
- Free: ve patrones, locked el reflejo integrador y siguiente paso con Espejo
- Navegante+: acceso completo

Tests gratuitos (sin plan requerido): definidos en `accounts/plan_utils.py → FREE_TEST_SLUGS`

---

## Módulo: tokens (legacy — desactivado)

Sistema de Fractones desactivado. Las tablas (`TokenBalance`, `TokenTransaction`, `Mission`) siguen en la BD pero no se usan. `tokens/views.py` redirige a `/pagos/planes/`. No agregar lógica de tokens en features nuevas.

---

## Módulo: community

- **Post** — foto + texto + `somatic_tag` + score (algoritmo HN)
- **Reaction** — resonar / gracias / fuerza (unique_together post+user)
- **Comment** — comentarios en posts
- **Forum** + **ForumPost** + **ForumReply** — foros por tema
- **DirectMessage** — mensajes entre usuarios

---

## Módulo: practitioners

- Directorio de practicantes de salud integrativa
- **TemporaryProfile** — permite calcular carta natal para un cliente sin cuenta

---

## Sistema visual — Fondos animados

La app tiene dos fondos intercambiables controlados por `UserProfile.map_aesthetic`.

`<body data-aesthetic="{{ map_aesthetic }}">` — JS y CSS leen este atributo.

### Fondo Cosmos (aesthetic = `cosmos`)
- Three.js 0.160 con `UnrealBloomPass` + `EffectComposer`
- Agujero negro kepleriano con 75k partículas en espiral
- **Performance:** `pixelRatio=1.0`, bloom a 50% resolución, 75k partículas
- Presets por sección: cambia densidad, camZ, tamaño de partículas según URL
- Lazy init: en modo mandala, `window.__initCosmos` guarda la función pero no la ejecuta hasta que se pida previsualización

### Fondo Mandala (aesthetic = `mandala`)
- Canvas 2D `#tunnel-bg` al 50% de resolución nativa
- **30fps cap** para no competir con el hilo principal
- 4 escenas / secciones: Corriente Acuática (0), Obsidiana (1), Hexagonal (2), Fibonacci (3)
- Transición portal entre escenas: círculo negro expansivo de 2200ms
- Overlay de contraste: `#mandala-overlay` con `rgba(3,3,6,0.44)` z-index:1

### Event system para SPA
```javascript
// Al navegar (spaGo), se dispara:
document.dispatchEvent(new CustomEvent('bg:preset', { detail: preset }))
// Cosmos escucha vía window.updateCosmosPreset(preset)
// Túnel escucha vía document.addEventListener('bg:preset', ...)
```

### Preview en perfil
`window.__switchAesthetic(name)` — cambia el fondo en tiempo real al hacer click en las cards de aesthetic en `/perfil/`, sin recargar.

---

## Sistema de diseño (CSS tokens)

La app usa variables CSS globales definidas en `base.html`:

```css
--surface: rgba(12,10,20,0.76)      /* cards principales */
--surface2: rgba(20,17,35,0.85)     /* cards secundarias */
--border: rgba(255,255,255,0.08)    /* bordes sutiles */
--border-active: rgba(126,204,205,0.3)
--radius: 16px
--calipso: #7ECCCD                  /* acento primario */
--violet: #9b8ec4                   /* acento secundario */
--rose: #c97b84
--amber: #d4a056
--sidebar-w: 280px
```

Clase `.panel`: `background:var(--surface); backdrop-filter:blur(14px); border:1px solid var(--border); border-radius:var(--radius); padding:24px`

Navegación SPA: `spaGo(event, el)` — intercepta clicks de `<a>` y carga contenido vía fetch sin recargar la página.

---

## Desarrollo local

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # editar variables
python manage.py migrate
python manage.py seed_tests
python manage.py runserver
```

### Análisis de código (codegraph)

```bash
codegraph init          # primera vez — indexa los 138 archivos
codegraph sync          # actualizar tras cambios
codegraph status        # estadísticas del índice
codegraph query <símbolo>           # buscar por nombre
codegraph callers <función>         # quién llama a esta función
codegraph callees <función>         # qué llama esta función
codegraph impact <función>          # qué se rompe si cambia
```

---

## GitHub

| Repo | Branch | URL |
|------|--------|-----|
| App Django | `master` | `github.com/jeria88/app-endonautas` |
| Landing Astro | `main` | `github.com/jeria88/astro-endonautas` |
| Blog/CRM | `main` | `github.com/jeria88/blog-endonautas` |

Push a `master` en `app-endonautas` activa el auto-deploy en Coolify automáticamente.
