from django.core.management.base import BaseCommand
from mirror.models import CategoriaNecesidad, EjercicioRegulacion, MomentoEjercicio, MomentoRegulacion


CATEGORIAS = [
    {'slug': 'para-mi-dia',         'nombre': 'Para mi día a día',       'tipo': 'cotidiano', 'orden': 0},
    {'slug': 'enfoque-claridad',    'nombre': 'Enfoque y claridad',       'tipo': 'cotidiano', 'orden': 1},
    {'slug': 'descanso-sueno',      'nombre': 'Descanso y sueño',         'tipo': 'cotidiano', 'orden': 2},
    {'slug': 'ansiedad-panico',     'nombre': 'Ansiedad y pánico',        'tipo': 'crisis',    'orden': 3},
    {'slug': 'cuando-me-desborde',  'nombre': 'Cuando me desbordé',       'tipo': 'crisis',    'orden': 4},
    {'slug': 'bloqueo-disociacion', 'nombre': 'Bloqueo y disociación',    'tipo': 'crisis',    'orden': 5},
]

MOMENTOS = [
    # ── COTIDIANOS ─────────────────────────────────────────────────────────────
    {
        'nombre': 'Ancla de mañana',
        'slug': 'ancla-manana',
        'tagline': 'Tres minutos para centrar el sistema nervioso antes de empezar el día.',
        'image_key': 'ancla-manana',
        'duracion_min': 6,
        'tipo': 'cotidiano',
        'orden': 0,
        'categorias': ['para-mi-dia'],
        'ejercicios': ['Botones del Cerebro', 'Respiración Cuadrada', 'Declaración de Coherencia'],
    },
    {
        'nombre': 'Activación suave al despertar',
        'slug': 'activacion-despertar',
        'tagline': 'Mueve el cuerpo y la mente antes de que el día tome control.',
        'image_key': 'activacion-despertar',
        'duracion_min': 5,
        'tipo': 'cotidiano',
        'orden': 1,
        'categorias': ['para-mi-dia', 'enfoque-claridad'],
        'ejercicios': ['Marcha Cruzada', '8 Perezoso', 'Respiración de Fuego'],
    },
    {
        'nombre': 'Reseteo antes de una reunión',
        'slug': 'reseteo-reunion',
        'tagline': 'Llega presente, no arrastrado. Cuatro minutos que cambian cómo entras.',
        'image_key': 'reseteo-reunion',
        'duracion_min': 4,
        'tipo': 'cotidiano',
        'orden': 2,
        'categorias': ['enfoque-claridad'],
        'ejercicios': ['Respiración Cuadrada', 'Puntos Neurovasculares'],
    },
    {
        'nombre': 'Micro-pausa de mediodía',
        'slug': 'micro-pausa-mediodia',
        'tagline': 'Un corte consciente para no llegar al final del día agotado.',
        'image_key': 'micro-pausa',
        'duracion_min': 4,
        'tipo': 'cotidiano',
        'orden': 3,
        'categorias': ['para-mi-dia'],
        'ejercicios': ['Suspiro de Purificación', 'Tarareo', 'Flujo Central'],
    },
    {
        'nombre': 'Integración al final del día',
        'slug': 'integracion-fin-dia',
        'tagline': 'Suelta lo que acumulaste y regresa a ti antes de cerrar el día.',
        'image_key': 'integracion-dia',
        'duracion_min': 10,
        'tipo': 'cotidiano',
        'orden': 4,
        'categorias': ['para-mi-dia', 'descanso-sueno'],
        'ejercicios': ['Seis Sonidos Curativos', 'Armonización por Dedos', 'Metáfora Sensorial'],
    },
    {
        'nombre': 'Preparación para dormir',
        'slug': 'preparacion-dormir',
        'tagline': 'Lleva el sistema nervioso a modo reposo. El cuerpo que descansa sana.',
        'image_key': 'preparacion-dormir',
        'duracion_min': 9,
        'tipo': 'cotidiano',
        'orden': 5,
        'categorias': ['descanso-sueno'],
        'ejercicios': ['Parasimpático 4 · 8', 'Cuna Occipital', 'Niño Interior'],
    },
    # ── CRISIS ─────────────────────────────────────────────────────────────────
    {
        'nombre': 'Ansiedad aguda ahora mismo',
        'slug': 'ansiedad-aguda',
        'tagline': 'Para cuando el pecho aprieta y la mente no para. Cinco minutos, paso a paso.',
        'image_key': 'ansiedad-aguda',
        'duracion_min': 5,
        'tipo': 'crisis',
        'orden': 6,
        'categorias': ['ansiedad-panico'],
        'ejercicios': ['Parasimpático 4 · 8', 'Tensión y Liberación', 'Equilibrio del Ombligo'],
    },
    {
        'nombre': 'El cuerpo no para de activarse',
        'slug': 'cuerpo-activado',
        'tagline': 'Cuando la adrenalina no baja aunque el peligro ya pasó.',
        'image_key': 'cuerpo-activado',
        'duracion_min': 7,
        'tipo': 'crisis',
        'orden': 7,
        'categorias': ['ansiedad-panico'],
        'ejercicios': ['Tensión y Liberación', 'Rotación de Ojos', 'Respiración Cuadrada'],
    },
    {
        'nombre': 'Explotaste y lo sabes',
        'slug': 'explotaste',
        'tagline': 'Sin juicio. Descarga, regula, y cierra el ciclo de activación.',
        'image_key': 'explotaste',
        'duracion_min': 8,
        'tipo': 'crisis',
        'orden': 8,
        'categorias': ['cuando-me-desborde'],
        'ejercicios': ['Suspiro de Purificación', 'Seis Sonidos Curativos', 'Corte de Lazos'],
    },
    {
        'nombre': 'Después de una discusión fuerte',
        'slug': 'post-discusion',
        'tagline': 'Para bajar del conflicto y volver a tu centro, sin tragarte nada.',
        'image_key': 'post-discusion',
        'duracion_min': 10,
        'tipo': 'crisis',
        'orden': 9,
        'categorias': ['cuando-me-desborde', 'ansiedad-panico'],
        'ejercicios': ['Suspiro de Purificación', 'Armonización por Dedos', 'Declaración de Coherencia'],
    },
    {
        'nombre': 'Mente en blanco / disociación',
        'slug': 'disociacion',
        'tagline': 'Cuando no estás del todo presente. Ejercicios de anclaje cruzado para volver.',
        'image_key': 'disociacion',
        'duracion_min': 6,
        'tipo': 'crisis',
        'orden': 10,
        'categorias': ['bloqueo-disociacion'],
        'ejercicios': ['Botones del Cerebro', 'Marcha Cruzada', 'Respiración Conectada'],
    },
    {
        'nombre': 'Cuando no puedes dejar de llorar',
        'slug': 'no-para-de-llorar',
        'tagline': 'No para detenerlo — para acompañarlo y darle un cauce seguro.',
        'image_key': 'no-para-de-llorar',
        'duracion_min': 9,
        'tipo': 'crisis',
        'orden': 11,
        'categorias': ['cuando-me-desborde', 'bloqueo-disociacion'],
        'ejercicios': ['Tarareo', 'Cuna Occipital', 'Entonación de Vocales', 'Niño Interior'],
    },
]


class Command(BaseCommand):
    help = 'Seed categorías de necesidad y momentos de regulación'

    def handle(self, *args, **kwargs):
        # Categorías
        for c in CATEGORIAS:
            obj, created = CategoriaNecesidad.objects.update_or_create(
                slug=c['slug'],
                defaults={'nombre': c['nombre'], 'tipo': c['tipo'], 'orden': c['orden']},
            )
            self.stdout.write(f"  {'✓' if created else '↺'} categoría: {obj.nombre}")

        # Momentos
        for m in MOMENTOS:
            cat_slugs = m.pop('categorias')
            ejercicio_titles = m.pop('ejercicios')

            momento, created = MomentoRegulacion.objects.update_or_create(
                slug=m['slug'],
                defaults=m,
            )

            # Categorías M2M
            cats = CategoriaNecesidad.objects.filter(slug__in=cat_slugs)
            momento.categorias.set(cats)

            # Ejercicios en orden
            MomentoEjercicio.objects.filter(momento=momento).delete()
            for i, title in enumerate(ejercicio_titles):
                try:
                    ej = EjercicioRegulacion.objects.get(title=title, active=True)
                    MomentoEjercicio.objects.create(momento=momento, ejercicio=ej, orden=i)
                except EjercicioRegulacion.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"    ⚠ ejercicio no encontrado: '{title}'"))

            self.stdout.write(f"  {'✓' if created else '↺'} momento: {momento.nombre} ({len(ejercicio_titles)} ejercicios)")

        self.stdout.write(self.style.SUCCESS('\nMomentos de regulación sembrados.'))
