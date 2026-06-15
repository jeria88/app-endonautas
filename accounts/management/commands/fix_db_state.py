from django.core.management.base import BaseCommand
from django.db import connection, OperationalError


class Command(BaseCommand):
    help = 'Fix migration state mismatch: clears recorded migrations for apps whose tables are missing'

    APPS_TO_CHECK = [
        ('birth', 'birth_birthdata'),
        ('community', 'community_post'),
        ('mirror', 'mirror_mirrorentry'),
        ('practitioners', 'practitioners_temporaryprofile'),
        ('psychometrics', 'psychometrics_test'),
        ('tokens', 'tokens_tokenbalance'),
    ]

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                for app, table in self.APPS_TO_CHECK:
                    cursor.execute(
                        "SELECT EXISTS(SELECT 1 FROM information_schema.tables "
                        "WHERE table_schema='public' AND table_name=%s)",
                        [table],
                    )
                    table_exists = cursor.fetchone()[0]
                    if not table_exists:
                        cursor.execute(
                            "DELETE FROM django_migrations WHERE app=%s", [app]
                        )
                        self.stdout.write(f'Cleared migration state for {app} (table {table} missing)')
        except OperationalError:
            self.stdout.write('django_migrations not found — fresh database, skipping fix')
