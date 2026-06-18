# App Endonautas

Aplicación web de autoconocimiento construida con Django 6. Integra astrología occidental, Human Design, cosmología china (Saju/BaZi), tests psicométricos, espejo de conflictos con RAG y comunidad nativa.

## Stack

| Capa | Tecnología |
|------|-----------|
| Framework | Django 6.0.4 |
| Servidor | Gunicorn (2 workers, 2 threads) |
| Base de datos | PostgreSQL (Railway prod) / SQLite (dev) |
| Archivos estáticos | WhiteNoise |
| Deploy | Railway (nixpacks) |
| IA | DeepSeek-chat via API compatible OpenAI / OpenRouter |
| Astrología | kerykeion 5.12.8 |
| Zona horaria | timezonefinder 8.2.4 + pytz |
| Cosmología china | sxtwl 2.0.7 |

---

## Arquitectura de apps

```
config/           — settings, urls raíz, wsgi
accounts/         — auth (email-based), UserProfile, planes
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
/tokens/            — balance y misiones de Fractones
/practicantes/      — directorio de practicantes
/admin/             — panel de administración Django
```

---

## Módulo: accounts

**Modelo User** — hereda `AbstractUser`, usa `email` como `USERNAME_FIELD` (sin username).

**Modelo UserProfile** (OneToOne a User):
- `plan`: free / navegante / practicante / empresa
- `map_aesthetic`: cosmos / mandala / archipielago / arbol
- `onboarding_completed`, `onboarding_step`
- Campos Hotmart: `hotmart_purchase_id`, `hotmart_product_id`, `plan_expires_at`

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
- `conflict_summary` y `return_question` — memoria versionada de la sesión
- **DreamEntry** — diario de sueños con tags, fecha, is_lucid, reality_check
- **Regulación** — técnicas somáticas (view independiente)
- IA: DeepSeek vía `settings.DEEPSEEK_API_KEY`

---

## Módulo: psychometrics (Tests)

- **Test** — nombre, dimensión (12 dimensiones del mapa), tipo de instrumento, costo en tokens
- **Question** + **Choice** — preguntas con opciones y pesos
- **TestResult** — respuestas JSON + score + insight generado por IA
- Seeds vía `python manage.py seed_tests` (comando de management)

Dimensiones: identidad, emociones, cuerpo, vínculos, sombra, espiritualidad, sueños, propósito, comunidad, abundancia, creatividad, mente

---

## Módulo: tokens (Fractones)

- **TokenBalance** (OneToOne a User): `permanent` + `monthly` (se renuevan)
- `spend()` consume mensual primero, luego permanente
- **TokenTransaction** — log de cada movimiento con razón
- Misiones: acciones que otorgan tokens

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

## Variables de entorno

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `SECRET_KEY` | Sí | Django secret key |
| `DEBUG` | No | `True` en dev, `False` en prod |
| `DATABASE_URL` | Prod | URL PostgreSQL (Railway la inyecta) |
| `ALLOWED_HOSTS` | No | Hosts permitidos (Railway inyecta `RAILWAY_PUBLIC_DOMAIN`) |
| `DEEPSEEK_API_KEY` | Para IA | Clave API DeepSeek o OpenRouter |
| `OPENROUTER_API_KEY` | Para IA | Alternativa a DeepSeek |
| `AI_MODEL` | No | Modelo a usar (default: `deepseek-chat`) |
| `DEFAULT_FROM_EMAIL` | No | Email remitente (default: `hola@endonautas.cl`) |

---

## Deploy (Railway)

```toml
# railway.toml
[build]
builder = "nixpacks"
buildCommand = "pip install -r requirements.txt && python manage.py collectstatic --noinput"

[deploy]
startCommand = "python manage.py fix_db_state && python manage.py migrate --noinput && python manage.py create_admin && python manage.py seed_tests && gunicorn config.wsgi --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:$PORT"
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
```

Comandos de management propios:
- `fix_db_state` — repara inconsistencias de BD antes de migrar
- `create_admin` — crea superusuario desde env si no existe
- `seed_tests` — pobla tests psicométricos iniciales

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

Para Railway, push al repositorio activa deploy automático.
