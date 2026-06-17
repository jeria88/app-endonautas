from django.core.management.base import BaseCommand
from terapeuta.models import MarcoEvaluacion, TecnicaEvaluacion
from terapeuta.constants import FRAMEWORKS_AND_TECHNIQUES


class Command(BaseCommand):
    help = "Seed MarcoEvaluacion y TecnicaEvaluacion desde FRAMEWORKS_AND_TECHNIQUES"

    def handle(self, *args, **options):
        marcos_created = marcos_updated = tecnicas_created = tecnicas_updated = 0

        for orden_marco, (marco_nombre, marco_info) in enumerate(FRAMEWORKS_AND_TECHNIQUES.items()):
            marco, created = MarcoEvaluacion.objects.update_or_create(
                nombre=marco_nombre,
                defaults={
                    "descripcion": marco_info.get("descripcion", ""),
                    "framework_code": marco_info.get("framework_code", ""),
                    "orden": orden_marco,
                },
            )
            if created:
                marcos_created += 1
            else:
                marcos_updated += 1

            for orden_tec, (tec_code, tec_info) in enumerate(marco_info["tecnicas"].items()):
                _, created = TecnicaEvaluacion.objects.update_or_create(
                    codigo_interno=tec_code,
                    defaults={
                        "nombre": tec_info["nombre"],
                        "descripcion": tec_info.get("descripcion", ""),
                        "marco": marco,
                        "orden": orden_tec,
                    },
                )
                if created:
                    tecnicas_created += 1
                else:
                    tecnicas_updated += 1

        self.stdout.write(
            f"Marcos: {marcos_created} creados, {marcos_updated} actualizados. "
            f"Técnicas: {tecnicas_created} creadas, {tecnicas_updated} actualizadas."
        )
