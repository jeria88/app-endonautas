# Análisis de errores — ¿Qué salió mal y cómo hacerlo bien desde el principio?

Este análisis no busca culpables. Busca patrones repetibles para no volver a pagar el mismo costo.

---

## Error 1: Meanings superficiales en primera iteración

### Qué pasó
Se creó `meanings.py` con entradas de 1 oración por cada campo (signos, planetas, tipos HD, etc.). Se integró, se probó, se entregó. El usuario tuvo que pedir explícitamente que se reescribiera todo.

### El error real
No fue un error técnico. Fue una falla de comprensión del dominio. Endonautas es una plataforma de **autoconocimiento profundo**. El usuario lo repitió varias veces en contextos anteriores. Una definición enciclopédica de "Aries" no sirve en un módulo de autoconocimiento — sirve en Wikipedia.

El error fue resolver la tarea técnica (llenar el diccionario) sin entender para qué existe el diccionario.

### Cómo hacerlo bien desde el principio
Antes de escribir el primer meaning, hacer una sola pregunta: ¿Qué quiere sentir el usuario cuando lee esto? En este caso: reconocerse. Eso dictaría inmediatamente el tono: segunda persona, específico, incluye el lado difícil (sombra), orientado a acción o comprensión, no a información.

Regla: **el dominio antecede al código**. Entender para qué sirve algo antes de construirlo ahorra más tiempo que cualquier optimización técnica.

---

## Error 2: HD con campos nombrados pero no descritos

### Qué pasó
Estrategia, No-Yo, Firma, canales y pares Personalidad/Diseño aparecían en el template con sus valores pero sin ninguna descripción. Se entregó el módulo así. El usuario lo señaló explícitamente en una segunda revisión.

### El error real
Se hizo un inventario incompleto de lo que necesitaba descripción. Se asumió que si un campo tiene un nombre (ej. "Generador Manifestante"), ese nombre es suficiente. No lo es — especialmente en HD, donde los conceptos son altamente específicos y no intuitivos para alguien nuevo al sistema.

La raíz: **se completó la checklist técnica sin completar la checklist de experiencia de usuario**. Técnicamente el template funcionaba. Experiencialmente estaba vacío.

### Cómo hacerlo bien desde el principio
Al diseñar un módulo de autoconocimiento, la checklist no es "¿aparece el dato?" sino "¿el usuario sabe qué hacer con este dato?". Si la respuesta es no, falta descripción. Recorrer el template completo desde la perspectiva del usuario antes de declararlo terminado.

---

## Error 3: Inconsistencia visual ignorada hasta que el usuario la señaló

### Qué pasó
Las cards del módulo birth (`.astral-planet`, `.hd-kv`, `.pillar`) se construyeron con estilos inline propios que no coincidían con el design system de la plataforma. El resto de la app usa `.panel` con `var(--surface)` + `backdrop-filter` + `var(--border)` + `var(--radius)`. El módulo birth usaba `rgba(0,0,0,0.88)` + `border-radius:10px` sin border ni blur.

Se vio en todos los templates y no se corrigió hasta que el usuario lo reportó.

### El error real
Se construyó cada template con estilos locales sin verificar el sistema de diseño existente. Hay variables CSS definidas globalmente precisamente para tener consistencia. No usarlas es construir deuda visual activa.

### Cómo hacerlo bien desde el principio
Al crear un nuevo template en Django, el primer paso es revisar `base.html` para identificar las clases y variables ya disponibles. Usar `.panel` para cualquier card que necesite profundidad. Solo crear clases nuevas cuando el componente sea genuinamente diferente.

Regla concreta: **si estoy escribiendo `background:rgba(...)` en un template, algo está mal**. Esa información pertenece a las variables CSS del sistema.

---

## Error 4: Ancho desperdiciado en todas las vistas

### Qué pasó
Todas las vistas del módulo birth (astral, hd, saju) tenían `max-width:700px` en el wrapper exterior. La app usa un layout con sidebar de 280px — en pantallas de 1440px eso dejaba casi 400px de espacio en blanco a la derecha. Los grids de cards usaban `minmax` fijo sin aprovechar el ancho disponible.

### El error real
El `max-width:700px` probablemente se copió de otro módulo o se puso como "seguro". No se pensó en cómo se vería en el contexto real del layout (con sidebar). Se optimizó para mobile-first sin considerar que la app es principalmente de escritorio.

### Cómo hacerlo bien desde el principio
En un layout con sidebar fija, el `main-content` ya tiene `padding:36px 40px` y `flex:1`. No necesita `max-width` adicional en el wrapper — eso rompe el comportamiento responsivo. Los grids con `repeat(auto-fill,minmax(X,1fr))` hacen el trabajo automáticamente.

Regla: **el único lugar donde `max-width` tiene sentido en este layout es en formularios de entrada de datos** (para no estirar inputs a 1200px), no en vistas de lectura.

---

## Error 5: Caché de reportes sin versioning

### Qué pasó
Los `BirthReport` se calculan una vez y se guardan en `raw_data` JSONField. Al añadir meanings, los reportes ya calculados no tenían los nuevos campos. Los templates mostraban nada donde debería aparecer el meaning.

Se descubrió solo cuando se fue a ver el resultado en el browser después de la integración.

### El error real
Se olvidó el problema de backward compatibility. Cualquier cambio en el schema de `raw_data` invalida los reportes existentes. No había ningún mecanismo para detectarlo.

### Cómo hacerlo bien desde el principio
Dos opciones válidas desde el inicio:

**Opción A (la que se implementó)**: sentinel key detection. Añadir un campo como `schema_version: 2` en `raw_data`. Si no existe o es menor al actual, recalcular. Simple, self-healing.

**Opción B**: No cachear `raw_data` como JSONField y recalcular siempre. Más lento pero sin problema de versioning. Válido si el cálculo dura < 2 segundos y hay pocos usuarios concurrentes.

La opción que se eligió (`_needs_recalc` con sentinel key) es correcta pero tardó en llegar. Debería haber sido parte del diseño inicial del modelo.

---

## El patrón de fondo

Revisando todos los errores, hay un denominador común: **se construyó en capas sin revisar la capa anterior**.

1. Se construyó el modelo → sin pensar en caché versioning
2. Se construyeron los meanings → sin pensar en profundidad de dominio
3. Se construyeron los templates → sin revisar el design system
4. Se construyeron las vistas → sin verificar el layout real

Cada error se hubiera evitado con una pregunta antes de empezar cada capa:

- Antes del modelo: ¿Cómo manejo cambios futuros al schema de raw_data?
- Antes de meanings: ¿Qué quiere sentir el usuario al leer esto?
- Antes del template: ¿Qué clases y variables ya existen en la plataforma?
- Antes de las vistas: ¿Cómo se ve esto en el layout real con sidebar?

Ninguna de esas preguntas requería código. Solo requería pausar 30 segundos antes de ejecutar.

---

## Lo que funcionó bien

Para balance, vale registrar lo que no tuvo que rehacerse:

- La arquitectura de `BirthData` / `BirthReport` (modelos limpios, FK correcto, `unique_together`)
- El split en calculadoras independientes (`calculate_astral_chart`, `calculate_hd_chart`, `calculate_saju_chart`)
- `_ensure_timezone(bp)` — detectado y resuelto preventivamente
- La integración de `kerykeion` + `sxtwl` + `timezonefinder` — funcionó en primer intento
- El cálculo de Daewoon con dirección por gender — correcto desde el inicio
- La corrección a Hora Solar Verdadera en Saju
- El sistema de polling / status en BirthReport (pending/processing/done/error)
