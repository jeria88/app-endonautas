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

## Sesión 9 — Documentación inicial (2026-06-18)

**Qué se generó:**
- `README.md` — documentación técnica completa de la app
- `HISTORIAL.md` — este archivo
- Análisis de errores: `ANALISIS_ERRORES.md`

---

## Sesión 10 — Oráculo completo: Tarot, I Ching, Fractal (2026-06-17 a 06-18)

**Qué se construyó:**
- Módulo `oraculo`: Tarot Terapéutico (Jodorowsky, 78 cartas + 6 tiradas nuevas), I Ching (64 hexagramas, líneas móviles), Oráculo Fractal (Arcanos + Sefirot, flip card)
- Interpretación IA por oráculo (`oraculo/interpretations.py`), lectura de integración que sintetiza el arco completo sin repetir por carta
- Rueda zodiacal SVG + Lucide icons en carta astral y Human Design
- Animaciones de revelación: stagger por carta/línea, flip cards, fases de loading

**Problemas resueltos (iterativos, muchos commits de ajuste fino):**
- Datos visuales de cartas cotejados contra el libro Jodorowsky (3 rondas de corrección)
- CSRF en los 3 oráculos, JSON crudo filtrado del panel (think-tags, max_tokens, fallback robusto)
- Fallback estático completo si falla la IA

---

## Sesión 11 — Terapeuta Integral: wizard clínico (2026-06-17)

**Qué se construyó:**
- Módulo `terapeuta`: wizard de 5 pasos (autoconsulta simplificada + fichas clínicas para profesionales)
- Fundamento pedagógico por instrucción terapéutica, propuesta terapéutica vía `openrouter/auto`

**Problemas resueltos:**
- 500 en transición paso2→paso3, doble submit en paso1, diagnósticos regenerados en cada GET del paso4

---

## Sesión 12 — Bitácora + Practitioners (2026-06-17)

**Qué se construyó:**
- Bitácora: CRUD con campos específicos por tipo de entrada, sueños integrados (se elimina Nauminto)
- `practitioners`: dashboard de cliente + agenda mensual, visualizaciones simbólicas por marco terapéutico

---

## Sesión 13 — Regulación: catálogo de 12 momentos (2026-06-19)

**Qué se construyó:**
- Módulo `mirror`/regulación reescrito como catálogo de 12 momentos con flujo instructivo paso a paso
- 26 animaciones premium Canvas 2D (incluye neon light tracing para Respiración Cuadrada) + SVG instructivos para 7 ejercicios kinesiológicos
- `config/ai_client.py` — centraliza todas las llamadas IA de la app (antes dispersas por módulo)
- Onboarding de 3 pantallas con drag-to-rank de prioridades + contexto IA

---

## Sesión 14 — Deploy Oracle/Coolify + Auth Google (2026-06-20 a 06-22)

**Qué se cambió:**
- Migración de infraestructura: Dockerfile + docker-compose para Oracle/Coolify (reemplaza Railway)
- Google OAuth en login y registro (`ACCOUNT_USER_MODEL_USERNAME_FIELD=None` para User email-only)
- Landing (`home.html`) eliminada de la app — migrada a Cloudflare Pages (repo separado)
- Umami analytics, skeleton loaders, caching, optimistic reactions

---

## Sesión 15 — Sistema de pagos v1 + pivot a planes feature-based (2026-06-21 a 06-22)

**Qué se construyó:**
- PayPal + MercadoPago: botones de suscripción, Wallet Brick, packs de fractones
- Página pública `/planes/`, checkout antes/después de onboarding, cancelar suscripción, eliminar cuenta
- **Pivot de modelo económico:** economía de Fractones (tokens por acción) reemplazada por planes feature-based (free/navegante/practicante) — se elimina toda la UI de compra de fractones y tooltips de costo
- Lead magnet: Mapa de Patrones Personales (3 tests gratis + IA)

---

## Sesión 16 — Espejo IA: RAG, Listmonk, memoria entre sesiones (2026-06-23 a 07-06)

**Qué se construyó:**
- RAG completo: `seed_knowledge` (101 chunks marcos teóricos) + `seed_endonautica_md` (38 chunks del libro) + `index_knowledge` (embeddings vía OpenRouter, DeepSeek no tiene API de embeddings)
- Contexto acumulado real: onboarding + tests + bitácora + lectura de nacimiento + sesión anterior
- Multimedia: adjuntos imagen/PDF/doc en el chat
- Auto-suscripción a Listmonk + email de bienvenida al registrarse
- System prompt reestructurado como arquitectura de modos (CRISIS > SÍNTOMA FÍSICO > REVELACIÓN), filtro determinístico anti-voseo, español neutro forzado en toda salida IA
- `_summarize_previous_session()` — memoria entre sesiones vía `conflict_summary` + `return_question`

---

## Sesión 17 — Reports app: KPI semanal automático (2026-06-29)

**Qué se construyó:**
- Comando `weekly_kpi`: KPIs Django ORM + Listmonk + Umami + SerpBear + scraping RRSS (Instagram/Facebook via Meta Graph API, TikTok endpoint público, YouTube API v3, LinkedIn/TikTok via Playwright)
- Top contenido por plataforma, clasificación de escenario (verde/amarillo/rojo), email semanal automático
- Ver detalle completo en `CLAUDE.md`

---

## Sesión 18 — Seguridad, motor de scoring terapeuta, fixes UX (2026-07-03 a 07-12)

**Qué se resolvió:**
- Fix open redirect en login + defaults seguros en settings
- `terapeuta`: catálogo data-driven + motor de scoring determinista (reemplaza heurística ad-hoc)
- Migración Listmonk a URL sslip (dominio propio caído)
- 6 fixes UX/UI: typo onboarding, Espejo unificado, tarot upsell, popstate sin flash

---

## Sesión 19 — Reporte de bugs in-app + PWA (2026-07-14 a 07-16)

**Qué se construyó:**
- Botón "Reportar un problema" (capturas + descripción, admin con thumbnails)
- PWA: manifest + service worker + assetlinks para TWA (Play Store), botón "Instalar app"
- Shell móvil: bottom tab bar, safe areas, modo foco, cosmos aligerado a 18k partículas sin bloom para ≤768px

---

## Sesión 20 — Monetización Taller de Terapeutas (2026-07-18 a 07-20)

**Qué se construyó:**
- Checkout de seña ($5.000) para el taller presencial del 1-ago, guest checkout sin cuenta previa (`payments/views/taller_views.py`, modelo `TallerReserva`)
- Pivot de modelo: la seña baja y el QR mostrado al final del taller activa una suscripción real a Plan Practicante ($39.990/mes) — el taller completo son $44.990 (`payments/views/bono_views.py`)
- Fix (07-20): el cobro post-taller regalaba el primer mes (`free_trial_months=1`) en vez de cobrar los $39.990 — no coincidía con el modelo real. Corregido a cobro inmediato sin trial.
- Onboarding especializado: terapeutas activados vía QR saltan el quiz genérico de autoconocimiento y van directo al Portal Profesional (`onboarding_entry_point='taller_terapeutas'`)
- Detalle completo de arquitectura en `CLAUDE.md` → sección "Taller de Terapeutas"
