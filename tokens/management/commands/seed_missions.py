from django.core.management.base import BaseCommand

from tokens.models import Mission

MISSIONS = [
    {'slug': 'onboarding', 'name': 'Bienvenido al viaje', 'fracton_reward': 60, 'order': 1,
     'description': 'Completa el onboarding inicial'},
    {'slug': 'first_test', 'name': 'Primer test completado', 'fracton_reward': 20, 'order': 2,
     'description': 'Responde tu primer test psicométrico'},
    {'slug': 'first_espejo', 'name': 'Primera conversación con el Espejo', 'fracton_reward': 40, 'order': 3,
     'description': 'Inicia tu primera sesión en el Espejo de Conflictos'},
    {'slug': 'first_dimension', 'name': 'Dimensión completada', 'fracton_reward': 50, 'order': 4,
     'description': 'Completa todos los tests de una dimensión'},
]


class Command(BaseCommand):
    help = 'Crea o actualiza las misiones de fractones'

    def handle(self, *args, **options):
        for data in MISSIONS:
            obj, created = Mission.objects.update_or_create(slug=data['slug'], defaults=data)
            status = 'creada' if created else 'actualizada'
            self.stdout.write(f'  {obj.name} — {status}')
        self.stdout.write(self.style.SUCCESS(f'Misiones: {len(MISSIONS)} procesadas'))
