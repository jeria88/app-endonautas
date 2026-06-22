from django.core.management.base import BaseCommand
from community.models import Forum

FOROS = [
    {
        'title': 'Errores & Soporte',
        'slug': 'errores-soporte',
        'description': 'Reporta bugs en fractones, pagos y módulos. El equipo revisa cada hilo.',
        'instructions': (
            'Para que podamos resolver tu caso rápido, incluí:\n'
            '1. Tipo de error (fractones, pago, módulo)\n'
            '2. Qué hiciste antes de que ocurriera\n'
            '3. Qué esperabas que pasara\n'
            '4. Qué pasó realmente\n'
            '5. Captura de pantalla si podés'
        ),
        'icon': '🛠',
        'color': 'rgba(220,80,60,0.15)',
        'is_bug_forum': True,
        'order': 1,
    },
    {
        'title': 'Soñadores Lúcidos',
        'slug': 'sonadores-lucidos',
        'description': 'Técnicas de inducción, símbolos oníricos y patrones del inconsciente.',
        'instructions': '',
        'icon': '🌙',
        'color': 'rgba(155,142,196,0.15)',
        'is_bug_forum': False,
        'order': 2,
    },
    {
        'title': 'Emprendedores',
        'slug': 'emprendedores',
        'description': 'Propósito, proyectos, bloqueos creativos y camino profesional con perspectiva interior.',
        'instructions': '',
        'icon': '🌱',
        'color': 'rgba(212,160,86,0.15)',
        'is_bug_forum': False,
        'order': 3,
    },
    {
        'title': 'Padres',
        'slug': 'padres',
        'description': 'Crianza consciente, vínculos, patrones familiares y el viaje de acompañar a otro.',
        'instructions': '',
        'icon': '🫶',
        'color': 'rgba(201,123,132,0.15)',
        'is_bug_forum': False,
        'order': 4,
    },
]


class Command(BaseCommand):
    help = 'Crea los foros iniciales de la comunidad'

    def handle(self, *args, **options):
        creados = 0
        actualizados = 0
        for data in FOROS:
            forum, created = Forum.objects.update_or_create(
                slug=data['slug'],
                defaults={k: v for k, v in data.items() if k != 'slug'},
            )
            if created:
                creados += 1
            else:
                actualizados += 1
        self.stdout.write(f'Foros: {creados} creados, {actualizados} actualizados')
