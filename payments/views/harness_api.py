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


@csrf_exempt
def ventas(request):
    """GET /pago/harness/ventas/?desde=AAAA-MM-DD&hasta=AAAA-MM-DD — ventas pagadas para conciliar.
    `external_ref` y `pasarela` son los mismos que mandan los avisos al harness (venta), así el
    harness reconoce las que ya tiene y agrega solo las que se perdieron."""
    if not _autorizado(request):
        return JsonResponse({'error': 'no autorizado'}, status=401)
    from datetime import date, timedelta

    from ..constants import PLANS
    from ..models import ConsultoriaReserva, Subscription
    from ..services.harness import a_clp
    try:
        desde = date.fromisoformat(request.GET.get('desde', ''))
        hasta = date.fromisoformat(request.GET.get('hasta', '')) + timedelta(days=1)
    except ValueError:
        return JsonResponse({'error': 'desde/hasta inválidos (AAAA-MM-DD)'}, status=422)
    out = []
    for o in EbookOrder.objects.filter(status__in=[EbookOrder.STATUS_PAID, EbookOrder.STATUS_DELIVERED],
                                       updated_at__date__gte=desde, updated_at__date__lt=hasta).select_related('user'):
        out.append({'pasarela': o.gateway, 'external_ref': o.gateway_payment_id, 'producto': 'endonautica-ebook',
                    'monto_clp': a_clp(o.amount_local, o.currency), 'email': o.user.email,
                    'fecha': o.updated_at.date().isoformat()})
    for r in ConsultoriaReserva.objects.filter(status=ConsultoriaReserva.STATUS_PAID, updated_at__date__gte=desde,
                                               updated_at__date__lt=hasta).select_related('user'):
        out.append({'pasarela': 'mp', 'external_ref': r.gateway_payment_id, 'producto': 'consultoria-60',
                    'monto_clp': int(r.amount_local), 'email': r.user.email, 'fecha': r.updated_at.date().isoformat()})
    for s in Subscription.objects.filter(status=Subscription.STATUS_ACTIVE, updated_at__date__gte=desde,
                                         updated_at__date__lt=hasta).select_related('user'):
        plan = PLANS.get(s.plan, {})
        monto = plan.get('price_clp') if s.gateway == 'mp' else a_clp(plan.get('price_usd', '0'), 'USD')
        out.append({'pasarela': s.gateway, 'external_ref': s.gateway_subscription_id or f'sub-{s.pk}',
                    'producto': f'plan-{s.plan}', 'monto_clp': monto, 'email': s.user.email,
                    'fecha': s.updated_at.date().isoformat()})
    return JsonResponse({'ventas': [v for v in out if v['external_ref']]})
