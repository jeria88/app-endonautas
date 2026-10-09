"""Endpoints que llama el harness de ACME Agents (acciones de soporte y comunidad de endonautas).

Auth: `Authorization: Bearer <HARNESS_API_KEY>` — la misma api_key del tenant endonautas que esta app
ya usa para avisarle al harness; la comparten los dos lados, no hay un secreto nuevo.
  POST /pago/harness/reenviar-acceso/      {email}            → reenvía los links de la última compra del ebook
  POST /pago/harness/comunidad/publicar/   {titulo, contenido} → publica en el feed a nombre de FRANCO_EMAIL
Respuesta de las acciones de soporte: {"resuelto": bool, "detalle"|"motivo": str} (contrato del harness).
"""
import hmac
import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..models import EbookOrder
from .entrega import entregar_ebook


def _autorizado(request) -> bool:
    clave = os.environ.get('HARNESS_API_KEY', '')
    dada = (request.headers.get('Authorization') or '').removeprefix('Bearer ').strip()
    return bool(clave) and hmac.compare_digest(dada, clave)


def _json(request) -> dict:
    try:
        return json.loads(request.body or b'{}')
    except ValueError:
        return {}


@csrf_exempt
@require_POST
def reenviar_acceso(request):
    if not _autorizado(request):
        return JsonResponse({'error': 'no autorizado'}, status=401)
    email = (_json(request).get('email') or '').strip().lower()
    order = (EbookOrder.objects
             .filter(user__email__iexact=email, status__in=[EbookOrder.STATUS_PAID, EbookOrder.STATUS_DELIVERED])
             .exclude(download_token='').order_by('-created_at').first()) if email else None
    if not order:
        return JsonResponse({'resuelto': False, 'motivo': 'sin compra pagada del ebook para ese email'})
    if not entregar_ebook(order, request=None):
        return JsonResponse({'resuelto': False, 'motivo': 'falló el envío del correo de entrega'})
    return JsonResponse({'resuelto': True, 'detalle': 'links de descarga del ebook reenviados (PDF y EPUB)'})


@csrf_exempt
@require_POST
def comunidad_publicar(request):
    if not _autorizado(request):
        return JsonResponse({'error': 'no autorizado'}, status=401)
    from community.models import Post
    d = _json(request)
    titulo, contenido = (d.get('titulo') or '').strip(), (d.get('contenido') or '').strip()
    if not titulo or not contenido:
        return JsonResponse({'error': 'falta título o contenido'}, status=422)
    autor = get_user_model().objects.filter(email__iexact=settings.FRANCO_EMAIL).first()
    if not autor:
        return JsonResponse({'error': f'no existe el usuario {settings.FRANCO_EMAIL} en la app'}, status=422)
    post = Post.objects.create(author=autor, content=f'{titulo}\n\n{contenido}')
    url = f"{settings.APP_BASE_URL.rstrip('/')}{reverse('community_post_detail', args=[post.pk])}"
    return JsonResponse({'post_id': post.pk, 'url': url})
