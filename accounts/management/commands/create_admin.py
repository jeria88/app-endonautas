import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or update admin superuser from env vars ADMIN_EMAIL / ADMIN_PASSWORD'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        email = os.getenv('ADMIN_EMAIL', 'admin@endonautas.cl')
        password = os.getenv('ADMIN_PASSWORD', 'endonautas2026')

        user, created = User.objects.get_or_create(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        action = 'Creado' if created else 'Actualizado'
        self.stdout.write(f'{action}: {email}')
