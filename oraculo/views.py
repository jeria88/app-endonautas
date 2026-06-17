import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction

from .models import SesionOraculo, LecturaTarot, LecturaIChing, LecturaFractal
from .services import TarotService, IChingService, CardService
from .interpretations import (
    generar_interpretacion_tarot,
    generar_interpretacion_iching,
    generar_interpretacion_fractal,
)

logger = logging.getLogger(__name__)

tarot_service = TarotService()
iching_service = IChingService()
card_service = CardService()


def hub(request):
    historial = []
    if request.user.is_authenticated:
        historial = SesionOraculo.objects.filter(
            usuario=request.user, guardada=True
        ).order_by("-fecha_creacion")[:6]
    return render(request, "oraculo/hub.html", {"historial": historial})


def tarot_view(request):
    return render(request, "oraculo/tarot.html")


def iching_view(request):
    return render(request, "oraculo/iching.html")


def fractal_view(request):
    return render(request, "oraculo/fractal.html")


@csrf_exempt
@require_POST
def tarot_api(request):
    try:
        data = json.loads(request.body)
        pregunta = data.get("pregunta", "").strip()
        tipo_tirada = data.get("tipo_tirada", "tres_cartas")

        if not pregunta:
            return JsonResponse({"error": "Escribe una pregunta"}, status=400)

        TIRADAS = {
            "un_arcano": tarot_service.tirar_un_arcano,
            "tres_cartas": tarot_service.tirar_tres_cartas,
            "cruz_normal": tarot_service.tirar_cruz_normal,
            "cruz_celta": tarot_service.tirar_cruz_celta,
            "viaje_heroe": tarot_service.tirar_viaje_heroe,
        }
        tirar = TIRADAS.get(tipo_tirada, tarot_service.tirar_tres_cartas)
        tirada = tirar(pregunta)

        datos_interp = tarot_service.obtener_datos_para_interpretacion(tirada)
        interpretacion = generar_interpretacion_tarot(datos_interp)

        usuario = request.user if request.user.is_authenticated else None
        with transaction.atomic():
            sesion = SesionOraculo.objects.create(
                usuario=usuario, tipo_oraculo="tarot", pregunta=pregunta,
            )
            LecturaTarot.objects.create(
                sesion=sesion, tipo_tirada=tipo_tirada,
                cartas=[c.to_dict() for c in tirada.cartas],
                interpretacion=interpretacion.get("texto_completo", ""),
            )

        return JsonResponse({
            "success": True,
            "sesion_id": str(sesion.id),
            "tirada": tirada.to_dict(),
            "interpretacion": interpretacion,
        })
    except Exception as e:
        logger.error(f"tarot_api error: {e}", exc_info=True)
        return JsonResponse({"error": "Error interno"}, status=500)


@csrf_exempt
@require_POST
def iching_api(request):
    try:
        data = json.loads(request.body)
        pregunta = data.get("pregunta", "").strip()

        if not pregunta:
            return JsonResponse({"error": "Escribe una pregunta"}, status=400)

        resultado = iching_service.generar_hexagrama(pregunta)
        datos_interp = iching_service.obtener_datos_para_interpretacion(resultado)
        interpretacion = generar_interpretacion_iching(datos_interp)

        hp = resultado["hexagrama_primario"]
        hs = resultado.get("hexagrama_secundario")
        usuario = request.user if request.user.is_authenticated else None

        with transaction.atomic():
            sesion = SesionOraculo.objects.create(
                usuario=usuario, tipo_oraculo="iching", pregunta=pregunta,
            )
            LecturaIChing.objects.create(
                sesion=sesion, lineas=hp["lineas"],
                hexagrama_primario_numero=hp["numero"],
                hexagrama_primario_nombre=hp["nombre"],
                hexagrama_secundario_numero=hs["numero"] if hs else None,
                hexagrama_secundario_nombre=hs["nombre"] if hs else "",
                interpretacion=interpretacion.get("texto_completo", ""),
            )

        return JsonResponse({
            "success": True,
            "sesion_id": str(sesion.id),
            "resultado": resultado,
            "interpretacion": interpretacion,
        })
    except Exception as e:
        logger.error(f"iching_api error: {e}", exc_info=True)
        return JsonResponse({"error": "Error interno"}, status=500)


@csrf_exempt
@require_POST
def fractal_api(request):
    try:
        data = json.loads(request.body)
        pregunta = data.get("pregunta", "").strip()

        if not pregunta:
            return JsonResponse({"error": "Escribe una pregunta"}, status=400)

        seleccion = card_service.seleccionar_carta(pregunta)
        carta = seleccion["carta"]
        invertida = seleccion["invertida"]
        carta_dict = card_service.carta_to_dict(carta, invertida)

        interpretacion = generar_interpretacion_fractal({
            "pregunta": pregunta, "carta": carta_dict,
        })

        usuario = request.user if request.user.is_authenticated else None
        with transaction.atomic():
            sesion = SesionOraculo.objects.create(
                usuario=usuario, tipo_oraculo="fractal", pregunta=pregunta,
            )
            LecturaFractal.objects.create(
                sesion=sesion, carta=carta, invertida=invertida,
                interpretacion=interpretacion.get("texto_completo", ""),
            )

        return JsonResponse({
            "success": True,
            "sesion_id": str(sesion.id),
            "carta": carta_dict,
            "interpretacion": interpretacion,
        })
    except Exception as e:
        logger.error(f"fractal_api error: {e}", exc_info=True)
        return JsonResponse({"error": "Error interno"}, status=500)
