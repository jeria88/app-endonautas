from django.core.management.base import BaseCommand
from django.db import connection, OperationalError


class Command(BaseCommand):
    help = 'Fix migration state mismatch: clears recorded migrations and drops orphaned tables for apps in bad state'

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
                for app, anchor_table in self.APPS_TO_CHECK:
                    cursor.execute(
                        "SELECT EXISTS(SELECT 1 FROM information_schema.tables "
                        "WHERE table_schema='public' AND table_name=%s)",
                        [anchor_table],
                    )
                    if cursor.fetchone()[0]:
                        continue

                    # Anchor table missing — find and drop ALL orphaned tables for this app
                    cursor.execute(
                        "SELECT table_name FROM information_schema.tables "
                        "WHERE table_schema='public' AND table_name LIKE %s",
                        [f'{app}_%'],
                    )
                    orphaned = [row[0] for row in cursor.fetchall()]
                    for orphan in orphaned:
                        cursor.execute(f'DROP TABLE IF EXISTS "{orphan}" CASCADE')
                        self.stdout.write(f'Dropped orphaned table {orphan}')

                    cursor.execute("DELETE FROM django_migrations WHERE app=%s", [app])
                    self.stdout.write(f'Cleared migration state for {app} (anchor table {anchor_table} was missing)')
        except OperationalError:
            self.stdout.write('django_migrations not found — fresh database, skipping fix')
