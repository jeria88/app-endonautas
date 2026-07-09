"""
Valida la integridad del catálogo clínico del módulo terapeuta:
  - cada eje referenciado en firmas y opciones existe en ejes.TODOS_LOS_EJES
  - cada dx referenciado en anamnesis existe en catalogo_otros
  - cada firma tiene ≥3 ejes
  - cada técnica de patrón existe en FRAMEWORKS_AND_TECHNIQUES

Uso: python3 manage.py validar_catalogo
"""
from django.core.management.base import BaseCommand

from terapeuta.data import DIAGNOSIS_OTROS, PATRONES_MTC, get_all_tecnicas
from terapeuta.data.anamnesis import (
    MODULO_EMOCIONAL,
    MODULO_GENERAL,
    MODULOS_ESPECIFICOS,
    OBSERVACION,
    ROGA_PARIKSHA,
)
from terapeuta.data.ejes import TODOS_LOS_EJES


class Command(BaseCommand):
    help = "Valida integridad del catálogo de patrones y anamnesis del módulo terapeuta."

    def handle(self, *args, **options):
        errores = []
        warnings = []
        tecnicas_validas = set(get_all_tecnicas().keys())
        dx_validos = {d["id"] for d in DIAGNOSIS_OTROS}

        # Firmas MTC
        for p in PATRONES_MTC:
            firma = p.get("firma", {})
            if len(firma) < 3:
                warnings.append(f"{p['id']} ({p['titulo']}): firma con solo {len(firma)} ejes (<3).")
            for ax in firma:
                if ax not in TODOS_LOS_EJES:
                    errores.append(f"{p['id']}: eje desconocido '{ax}' en firma.")
            if p.get("tecnica") not in tecnicas_validas:
                errores.append(f"{p['id']}: técnica '{p.get('tecnica')}' no existe en FRAMEWORKS.")
            for campo in ("titulo", "descripcion", "patron_diagnostico", "protocolo_indicado"):
                if not p.get(campo):
                    warnings.append(f"{p['id']}: campo '{campo}' vacío.")

        # Opciones de anamnesis
        grupos = [("ROGA", ROGA_PARIKSHA), ("GENERAL", MODULO_GENERAL),
                  ("OBSERVACION", OBSERVACION), ("EMOCIONAL", MODULO_EMOCIONAL)]
        for sid, preguntas in MODULOS_ESPECIFICOS.items():
            grupos.append((f"ESPECIFICO:{sid}", preguntas))

        for nombre, preguntas in grupos:
            for q in preguntas:
                for opt in q["opciones"]:
                    for ax in opt.get("ejes", {}):
                        if ax not in TODOS_LOS_EJES:
                            errores.append(f"{nombre}/{q['id']}/{opt['valor']}: eje desconocido '{ax}'.")
                    for did in opt.get("dx", {}):
                        if did not in dx_validos:
                            errores.append(f"{nombre}/{q['id']}/{opt['valor']}: dx '{did}' no existe en catalogo_otros.")

        # Discriminantes: debe existir al menos un peso negativo en el conjunto de opciones
        neg = 0
        for _nombre, preguntas in grupos:
            for q in preguntas:
                for opt in q["opciones"]:
                    if any(w < 0 for w in opt.get("ejes", {}).values()):
                        neg += 1
        if neg == 0:
            warnings.append("No hay ningún peso de eje negativo (discriminante) en toda la anamnesis.")

        for w in warnings:
            self.stdout.write(self.style.WARNING(f"⚠ {w}"))
        for e in errores:
            self.stdout.write(self.style.ERROR(f"✗ {e}"))

        if errores:
            self.stdout.write(self.style.ERROR(f"\n{len(errores)} error(es), {len(warnings)} advertencia(s)."))
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS(
            f"\nCatálogo OK: {len(PATRONES_MTC)} patrones MTC, {len(dx_validos)} dx otros, "
            f"{neg} opciones con discriminante. {len(warnings)} advertencia(s)."
        ))
