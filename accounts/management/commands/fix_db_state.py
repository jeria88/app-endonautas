from django.core.management.base import BaseCommand
from django.db import connection, OperationalError


class Command(BaseCommand):
    help = 'Fix migration state mismatch: clears recorded migrations and drops orphaned tables for apps in bad state'

    # Clear app if its anchor table is missing
    APPS_TO_CHECK = [
        ('birth', 'birth_birthdata'),
        ('community', 'community_post'),
        ('mirror', 'mirror_chatsession'),
        ('psychometrics', 'psychometrics_test'),
        ('tokens', 'tokens_tokenbalance'),
    ]

    # (app, migration_name, dependent_apps) — clear app + dependents if migration not recorded
    MIGRATIONS_TO_VERIFY = [
        ('practitioners', '0002_initial', ['psychometrics', 'birth']),
    ]

    def _drop_app_tables_and_migrations(self, cursor, app):
        cursor.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema='public' AND table_name LIKE %s",
            [f'{app}_%'],
        )
        for (table,) in cursor.fetchall():
            cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
            self.stdout.write(f'Dropped orphaned table {table}')
        cursor.execute("DELETE FROM django_migrations WHERE app=%s", [app])

    def _drop_django_builtins(self, cursor):
        # Django built-in apps use non-standard table names (django_*, not app_*)
        for table in ('django_admin_log', 'django_content_type', 'django_session'):
            cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
            self.stdout.write(f'Dropped table {table}')
        # auth_* tables follow the app_ pattern so the generic method works
        self._drop_app_tables_and_migrations(cursor, 'auth')
        for app in ('admin', 'contenttypes', 'sessions'):
            cursor.execute("DELETE FROM django_migrations WHERE app=%s", [app])

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Detect stale accounts_user schema (username NOT NULL from old project)
                cursor.execute(
                    "SELECT EXISTS(SELECT 1 FROM information_schema.columns "
                    "WHERE table_schema='public' AND table_name='accounts_user' "
                    "AND column_name='username' AND is_nullable='NO')"
                )
                if cursor.fetchone()[0]:
                    self._drop_app_tables_and_migrations(cursor, 'accounts')
                    self._drop_django_builtins(cursor)
                    self.stdout.write('Cleared accounts + Django builtins (stale username NOT NULL column detected)')

                # Detect InconsistentMigrationHistory: admin recorded but accounts not
                cursor.execute(
                    "SELECT EXISTS(SELECT 1 FROM django_migrations WHERE app='admin' AND name='0001_initial') "
                    "AND NOT EXISTS(SELECT 1 FROM django_migrations WHERE app='accounts' AND name='0001_initial')"
                )
                if cursor.fetchone()[0]:
                    self._drop_app_tables_and_migrations(cursor, 'accounts')
                    self._drop_django_builtins(cursor)
                    self.stdout.write('Cleared accounts + Django builtins (admin recorded before accounts)')

                for app, anchor_table in self.APPS_TO_CHECK:
                    cursor.execute(
                        "SELECT EXISTS(SELECT 1 FROM information_schema.tables "
                        "WHERE table_schema='public' AND table_name=%s)",
                        [anchor_table],
                    )
                    if cursor.fetchone()[0]:
                        continue
                    self._drop_app_tables_and_migrations(cursor, app)
                    self.stdout.write(f'Cleared migration state for {app} (anchor table {anchor_table} was missing)')

                for app, migration_name, dependents in self.MIGRATIONS_TO_VERIFY:
                    cursor.execute(
                        "SELECT EXISTS(SELECT 1 FROM django_migrations WHERE app=%s AND name=%s)",
                        [app, migration_name],
                    )
                    if cursor.fetchone()[0]:
                        continue
                    self._drop_app_tables_and_migrations(cursor, app)
                    self.stdout.write(f'Cleared migration state for {app} (migration {migration_name} was not recorded)')
                    for dep_app in dependents:
                        self._drop_app_tables_and_migrations(cursor, dep_app)
                        self.stdout.write(f'Cleared migration state for {dep_app} (dependency on {app} was cleared)')
        except OperationalError:
            self.stdout.write('django_migrations not found — fresh database, skipping fix')
