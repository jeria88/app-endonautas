"""
python manage.py weekly_kpi
python manage.py weekly_kpi --week 2026-W27
python manage.py weekly_kpi --week 2026-W27 --dry-run
"""
import os
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError

from reports.services import kpi_calculator, listmonk_metrics, umami_metrics
from reports.services.markdown_renderer import render, render_email_html
from reports.services.scenario_classifier import classify


class Command(BaseCommand):
    help = 'Calcula KPIs semanales y guarda KPISnapshot'

    def add_arguments(self, parser):
        parser.add_argument(
            '--week',
            help='Semana ISO a calcular, ej: 2026-W27. Default: semana actual.',
            default=None,
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra resultados sin guardar en BD ni enviar email.',
        )

    def handle(self, *args, **options):
        week_start, week_number, year = _parse_week(options['week'])
        dry_run = options['dry_run']

        self.stdout.write(f"Calculando KPIs para {year}-W{week_number:02d} (inicio: {week_start})...")

        # 1. KPIs Django ORM
        django_kpis = kpi_calculator.calculate_week(week_start)
        self.stdout.write(f"  Django ORM: {django_kpis}")

        # 2. Listmonk
        lm_kpis = listmonk_metrics.fetch_week_stats(week_start)
        self.stdout.write(f"  Listmonk: {lm_kpis}")

        # 3. Umami
        umami_kpis = umami_metrics.fetch_week_stats(week_start)
        self.stdout.write(f"  Umami: {umami_kpis}")

        # 4. Merge
        all_kpis = {**django_kpis, **lm_kpis, **umami_kpis}

        # 5. Clasificar
        escenario, alertas, decision = classify(all_kpis, month=week_start.month)
        self.stdout.write(f"  Escenario: {escenario} | Alertas: {alertas}")

        # 6. MD
        md = render(all_kpis, escenario, alertas, decision, week_start, week_number)

        if dry_run:
            self.stdout.write(self.style.WARNING("\n--- DRY RUN — no se guarda nada ---\n"))
            self.stdout.write(md)
            return

        # 7. Guardar KPISnapshot
        from reports.models import KPISnapshot
        snap, created = KPISnapshot.objects.update_or_create(
            week_start=week_start,
            defaults={
                'week_number': week_number,
                'year': year,
                **all_kpis,
                'escenario': escenario,
                'alertas': alertas,
                'decision_sugerida': decision,
                'md_snapshot': md,
            },
        )
        action = 'Creado' if created else 'Actualizado'
        self.stdout.write(self.style.SUCCESS(f"  {action} KPISnapshot #{snap.pk}"))

        # 8. Guardar MD en archivo
        _write_md_file(md, year, week_number)

        # 9. Enviar email TX a Franco
        _send_email(all_kpis, escenario, week_number, decision)

        self.stdout.write(self.style.SUCCESS(f"Weekly KPI completado — {escenario.upper()}"))


def _parse_week(week_str):
    if week_str:
        try:
            year_str, w_str = week_str.split('-W')
            year = int(year_str)
            week_num = int(w_str)
            # Calcular lunes de esa semana ISO
            jan4 = date(year, 1, 4)
            start = jan4 + timedelta(weeks=week_num - 1, days=-jan4.weekday())
            return start, week_num, year
        except Exception:
            raise CommandError(f"Formato de semana inválido: {week_str}. Usar formato 2026-W27")

    today = date.today()
    iso = today.isocalendar()
    year, week_num = iso[0], iso[1]
    week_start = today - timedelta(days=today.weekday())
    return week_start, week_num, year


def _write_md_file(md, year, week_number):
    try:
        import os
        snap_dir = os.path.join(os.path.dirname(__file__), '../../../../reports/snapshots')
        os.makedirs(snap_dir, exist_ok=True)
        path = os.path.join(snap_dir, f'{year}-W{week_number:02d}.md')
        with open(path, 'w') as f:
            f.write(md)
    except Exception:
        pass


def _send_email(kpis, escenario, week_number, decision):
    try:
        import requests, base64, os

        base = 'https://mail.146.181.39.4.sslip.io'
        user = 'api_claude'
        token = 'lm_api_2b99334cb53a67a428a364049b45b986533908952a897102'
        creds = base64.b64encode(f'{user}:{token}'.encode()).decode()
        headers = {'Authorization': f'Basic {creds}', 'Content-Type': 'application/json'}

        template_id = int(os.getenv('LISTMONK_TX_KPI_TEMPLATE_ID', '0'))
        franco_email = os.getenv('FRANCO_EMAIL', 'fjeriacastro@gmail.com')
        if not template_id:
            return

        color = {'verde': '#2d6a4f', 'amarillo': '#b5770d', 'rojo': '#9b2226'}.get(escenario, '#333')
        label = {'verde': '🟢 VERDE', 'amarillo': '🟡 AMARILLO', 'rojo': '🔴 ROJO'}.get(escenario, escenario)

        requests.post(
            f'{base}/api/tx',
            json={
                'subscriber_email': franco_email,
                'template_id': template_id,
                'data': {
                    'week_number': week_number,
                    'escenario_label': label,
                    'color': color,
                    'registros_nuevos': kpis.get('registros_nuevos', 0),
                    'activacion_pct': kpis.get('activacion_pct', 0),
                    'retencion_d7_pct': kpis.get('retencion_d7_pct', 0),
                    'retencion_d30_pct': kpis.get('retencion_d30_pct', 0),
                    'sesiones_espejo_avg': kpis.get('sesiones_espejo_avg', 0),
                    'navegantes_total': kpis.get('navegantes_total', 0),
                    'mrr_estimado_usd': kpis.get('mrr_estimado_usd', 0),
                    'email_open_rate_pct': kpis.get('email_open_rate_pct', 0),
                    'email_ctr_pct': kpis.get('email_ctr_pct', 0),
                    'suscriptores_total': kpis.get('suscriptores_total', 0),
                    'visitas_landing': kpis.get('visitas_landing', 0),
                    'decision': decision,
                },
            },
            headers=headers,
            timeout=8,
        )
    except Exception:
        pass
