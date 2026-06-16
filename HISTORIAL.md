# Historial de construcción — App Endonautas

Registro de sesiones de desarrollo. Cada entrada refleja lo que se construyó, los problemas reales encontrados y cómo se resolvieron.

---

## Sesión 1 — Fundación de la app

**Qué se construyó:**
- Estructura Django base: `config/`, `accounts/`, apps vacías
- Auth por email (`AbstractUser` con `email` como `USERNAME_FIELD`)
- `UserProfile` con plan y mapa estético
- `base.html` con sidebar, design tokens CSS, navegación SPA (`spaGo`)
- Deploy inicial en Railway con nixpacks

**Problemas encontrados:**
- Configuración de Railway con `SECRET_KEY` y `ALLOWED_HOSTS` para HTTPS
- WhiteNoise para archivos estáticos sin servidor separado

---

## Sesión 2 — Módulo community + tokens

**Qué se construyó:**
- `Post`, `Reaction`, `Comment` — feed con algoritmo de score HN
- `Forum`, `ForumPost`, `ForumReply` — foros por tema
- `DirectMessage` — mensajes directos
- `TokenBalance`, `TokenTransaction` — sistema de Fractones (permanentes + mensuales)

---

## Sesión 3 — Espejo de conflictos (mirror)

**Qué se construyó:**
- `KnowledgeChunk` con `embedding` JSONField — base RAG
- `ChatSession` / `ChatMessage` — historial por usuario
- `conflict_summary` y `return_question` — memoria versionada del espejo
- `DreamEntry` — diario de sueños
- Integración DeepSeek via `DEEPSEEK_API_KEY` / `OPENROUTER_API_KEY`
- Vistas: espejo, sueños, regulación

---

## Sesión 4 — Psychometrics

**Qué se construyó:**
- `Test`, `Question`, `Choice` — estructura de tests
- 12 dimensiones del mapa de autoconocimiento
- `TestResult` con score + insight IA
- `seed_tests` management command
- Badges de instrumento: clínico / adaptado / endonauta

---

## Sesión 5 — Módulo birth: estructura base

**Qué se construyó:**
- `BirthData` — fecha, hora, ciudad, lat/lng, timezone
- `BirthReport` — reportes por tipo con `raw_data` JSONField
- `birth/calculators.py` — tres calculadoras independientes
  - `calculate_astral_chart`: kerykeion tropical Placidus, 10 planetas + Nodo + Quirón
  - `calculate_hd_chart`: solar-arc para Design date, 64 puertas I Ching, canales, centros, cruz de encarnación
  - `calculate_saju_chart`: sxtwl, 4 pilares, balance elemental, Daewoon
- Templates: `home.html`, `datos.html`, `astral.html`, `hd.html`, `saju.html`
- Geocodificación en frontend con Nominatim (OpenStreetMap)

**Problemas técnicos resueltos:**
- `timezonefinder` para derivar timezone desde lat/lng
- `pytz` necesario para conversión UTC en cálculo HD (fecha de Diseño 88°)
- `_ensure_timezone(bp)`: re-derivar timezone en cada cálculo (fix para registros con `timezone_str='UTC'`)
- `HD_WHEEL_START = 302.0` — constante de inicio del zodíaco HD vs eclíptico estándar
- True Solar Time para Saju: offset via longitud
- Daewoon requiere gender: dirección forward (M) o backward (F) en el I Ching

---

## Sesión 6 — Meanings: primera iteración

**Qué se construyó:**
- `birth/meanings.py` — diccionarios de significados para todos los campos calculados
- Integración en calculadoras: cada campo enriquecido con texto explicativo
- `_needs_recalc(report)` — detección de caché desactualizado por sentinel key
- Auto-recálculo en view al detectar reportes sin meanings

**Problema identificado:**
- Los meanings de primera iteración eran de 1 oración cada uno — demasiado superficiales para un módulo de autoconocimiento real

---

## Sesión 7 — Meanings: reescritura completa

**Qué se reconstruyó:**
- Reescritura total de `meanings.py`: 3-6 oraciones por entrada, segunda persona, incluye don + sombra/reto
- Añadidos meanings que faltaban por completo:
  - `HD_NOT_SELF_MEANINGS` (5 temas del No-Yo)
  - `HD_SIGNATURE_MEANINGS` (5 firmas)
  - `HD_CHANNEL_MEANINGS` (33 canales con descripción funcional)
  - `HD_PLANET_MEANINGS` (13 planetas en contexto HD, distinción Personalidad vs Diseño)
  - `HD_PERSONALITY_DESIGN_INTRO` (párrafo introductorio para la sección)
  - `SAJU_STEM_SHORT` (10 Tallos Celestiales — descripciones para ciclos Daewoon)
- Calculadoras actualizadas para todos los campos nuevos
- Templates actualizados: HD planets_paired muestra meaning por par, Daewoon muestra descripción por ciclo

**Problemas de regresión resueltos:**
- `defined_centers` cambió de lista de strings a lista de dicts → template actualizado de `{{ c }}` a `{{ c.name }}` / `{{ c.meaning }}`

---

## Sesión 8 — Consistencia visual + ancho completo

**Qué se cambió:**
- **Cards de nacimiento** alineadas al design system de la plataforma:
  - Antes: `background:rgba(0,0,0,0.88)`, `border-radius:10px`, sin `backdrop-filter`, sin `--border`
  - Después: `background:var(--surface)`, `backdrop-filter:blur(14px)`, `border:1px solid var(--border)`, `border-radius:var(--radius)`
  - Afectó: `.astral-planet`, `.hd-kv`, `.pillar`, `.dw-cycle`, `.report-card`
- **Ancho completo** en todas las vistas birth:
  - Eliminado `max-width:700px` en astral, hd, saju
  - `datos.html` ampliado a `max-width:640px`
  - Grids cambiados a `repeat(auto-fill,minmax(220px,1fr))` para aprovechar pantalla

---

## Sesión actual — Documentación

**Qué se generó:**
- `README.md` — documentación técnica completa de la app
- `HISTORIAL.md` — este archivo
- Análisis de errores: `ANALISIS_ERRORES.md`
