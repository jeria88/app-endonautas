import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or update admin superuser. Safe to run on every deploy.'

    def handle(self, *args, **options):
        try:
            from django.contrib.auth import get_user_model
            from accounts.models import UserProfile
            from tokens.models import TokenBalance

            User = get_user_model()
            email = os.getenv('ADMIN_EMAIL', 'admin@endonautas.cl')
            password = os.getenv('ADMIN_PASSWORD', 'endonautas2026')

            user, created = User.objects.get_or_create(email=email)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.is_practicante = True
            profile.save(update_fields=['is_practicante'])
            TokenBalance.objects.get_or_create(user=user)

            action = 'Creado' if created else 'Actualizado'
            self.stdout.write(f'{action}: {email}')
        except Exception as e:
            self.stdout.write(f'create_admin skipped: {e}')
