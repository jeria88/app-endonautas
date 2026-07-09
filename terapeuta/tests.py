"""
Tests del motor de diferenciación (scoring.py) — deterministas, sin IA.

Verifican que el rediseño resuelve el caso reportado: dermatitis ya NO cae en
"Estancamiento de Qi de Hígado" sino en patrones de piel (Viento-Calor, Calor
en Sangre, etc.), y que los casos que funcionaban siguen funcionando.
"""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from terapeuta.models import Consulta, DiagnosticoPropuesto
from terapeuta.scoring import score_diagnosticos


def _ids(resultado):
    return [c["id"] for c in resultado["candidatos"]]


class TestDermatitisVientoCalor(SimpleTestCase):
    """Dermatitis roja, caliente, picor migratorio, empeora con calor, sed fría."""

    signos = {
        "R03": ["calor"],                 # empeora con el calor
        "G01": "caluroso",                # más calor
        "G03": "sed_fria",                # mucha sed, agua fría
        "O01": "roja_bordes",             # lengua roja en bordes
        "O02": "amarilla",                # saburra amarilla
        "P01": "roja_caliente",           # lesión roja y caliente
        "P02": "migratorio",              # picor que cambia de lugar
        "P03": ["calor"],
        "P05": "brotes",
    }
    sistemas = ["piel"]

    def test_top_incluye_patron_de_piel(self):
        r = score_diagnosticos(self.signos, self.sistemas)
        top3 = _ids(r)[:3]
        self.assertTrue(
            any(pid in top3 for pid in ("M28", "M29", "M30")),
            f"Se esperaba un patrón de piel en el top-3, salió {top3}",
        )

    def test_qi_higado_no_supera_a_piel(self):
        r = score_diagnosticos(self.signos, self.sistemas)
        ids = _ids(r)
        # M01 (Qi Hígado) no está en sistema piel → ni siquiera debe aparecer
        self.assertNotIn("M01", ids, "Qi de Hígado no debería ser candidato en un caso de piel")

    def test_formula_menciona_calor(self):
        r = score_diagnosticos(self.signos, self.sistemas)
        self.assertEqual(r["formula"]["termico"], "Calor")


class TestPielSecaDeficienciaSangre(SimpleTestCase):
    """Piel seca, descamativa, pálida, con fatiga → Deficiencia de Sangre."""

    signos = {
        "G01": "friolento",
        "G08": "agotamiento",
        "O01": "palida",
        "P01": "seca_descama",
        "P02": "nocturno",
        "P06": "seca",
    }
    sistemas = ["piel"]

    def test_deficiencia_sangre_arriba(self):
        r = score_diagnosticos(self.signos, self.sistemas)
        top3 = _ids(r)[:3]
        self.assertIn("M31", top3, f"Se esperaba M31 (Def. Sangre) en top-3, salió {top3}")


class TestDigestivoQiBazo(SimpleTestCase):
    """Regresión: caso digestivo clásico sigue dando Qi de Bazo."""

    signos = {
        "G04": "poco_pesadez",   # poco apetito, pesadez
        "G05": "blandas",        # heces blandas
        "G08": "baja_manana",    # energía baja
        "G09": ["preocupacion"], # preocupación → Bazo
        "O01": "palida",
        "O03": "hinchada",       # lengua hinchada con marcas
    }
    sistemas = ["digestivo"]

    def test_qi_bazo_gana(self):
        r = score_diagnosticos(self.signos, self.sistemas)
        top = _ids(r)
        self.assertTrue(top and top[0] == "M06", f"Se esperaba M06 (Qi Bazo) primero, salió {top}")


class TestContradiccionLengua(SimpleTestCase):
    """Calor Verdadero/Frío Ilusorio (Manual 5.4): la lengua arbitra."""

    signos = {
        "R02": ["calor"],     # se alivia con el calor → parece Frío
        "G01": "friolento",   # se siente friolento → parece Frío
        "O01": "roja",        # pero la lengua es roja → Calor
        "O02": "amarilla",    # saburra amarilla → Calor
    }

    def test_flag_contradiccion(self):
        r = score_diagnosticos(self.signos, [])
        self.assertIsNotNone(r["formula"]["contradiccion"])
        # la lengua arbitra → térmico final Calor
        self.assertEqual(r["formula"]["termico"], "Calor")


class TestWizardE2E(TestCase):
    """Recorre el wizard completo con IA mockeada (fallback determinista)."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_terapeuta")
        User = get_user_model()
        cls.user = User.objects.create_user(email="e2e@test.cl", password="x")
        prof = cls.user.profile
        prof.plan = "navegante"
        prof.save()

    def setUp(self):
        self.client.force_login(self.user)

    @patch("terapeuta.views.call_ai", return_value="")  # sin IA → fallback
    def test_flujo_dermatitis(self, _mock):
        # paso0 crea consulta y redirige a paso1
        r = self.client.get(reverse("terapeuta:paso0"))
        self.assertEqual(r.status_code, 302)
        cid = Consulta.objects.latest("id").id

        # paso1: motivo + triaje piel + roga
        r = self.client.post(reverse("terapeuta:paso1", args=[cid]), {
            "motivo": "dermatitis en los pliegues, pica de noche",
            "sistemas": ["piel"], "intensidad": "6", "duracion": "cronico",
            "signo_R03": ["calor"],
        })
        self.assertEqual(r.status_code, 302)

        # paso2: interrogatorio general
        r = self.client.post(reverse("terapeuta:paso2", args=[cid]), {
            "signo_G01": "caluroso", "signo_G03": "sed_fria",
        })
        self.assertEqual(r.status_code, 302)

        # paso3: observación + módulo piel
        r = self.client.post(reverse("terapeuta:paso3", args=[cid]), {
            "signo_O01": "roja_bordes", "signo_O02": "amarilla",
            "signo_P01": "roja_caliente", "signo_P02": "migratorio",
        })
        self.assertEqual(r.status_code, 302)

        # paso4 GET: genera diagnósticos + fórmula
        r = self.client.get(reverse("terapeuta:paso4", args=[cid]))
        self.assertEqual(r.status_code, 200)
        consulta = Consulta.objects.get(id=cid)
        self.assertTrue(consulta.formula_mtc.get("texto"))
        dxs = list(DiagnosticoPropuesto.objects.filter(consulta=consulta))
        self.assertTrue(dxs, "Debe generar al menos un diagnóstico")
        # ningún Qi de Hígado en caso de piel
        self.assertNotIn("M01", [d.diagnostico_id for d in dxs])

        # paso4 POST: confirmar el primero
        r = self.client.post(reverse("terapeuta:paso4", args=[cid]), {
            "diagnosticos_confirmados": [str(dxs[0].id)],
        })
        self.assertEqual(r.status_code, 302)

        # paso5 GET: propuesta por fallback de bloques
        r = self.client.get(reverse("terapeuta:paso5", args=[cid]))
        self.assertEqual(r.status_code, 200)
        consulta.refresh_from_db()
        self.assertTrue(consulta.propuesta_terapeutica, "Debe generar propuesta (fallback)")
