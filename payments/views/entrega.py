import logging
import os

from django.core.mail import EmailMultiAlternatives
from django.http import FileResponse, Http404
from django.urls import reverse

from ..models import EbookLead, EbookOrder

logger = logging.getLogger(__name__)

EBOOK_FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ebook_files')
EPUB_PATH = os.path.join(EBOOK_FILES_DIR, 'endonautica.epub')


def entregar_pdf_herida(lead):
    """Envía por email el PDF 'mapa de tu herida' generado por
    `manage.py generar_pdfs_heridas` desde heridas.ts. Nunca lanza — si falla,
    el lead queda en 'nuevo' y es visible en el admin para reenviar a mano."""
    if not lead.email:
        return False

    pdf_path = os.path.join(EBOOK_FILES_DIR, f'mapa-herida-{lead.herida}.pdf')
    if not os.path.exists(pdf_path):
        logger.error(f'entregar_pdf_herida: no existe {pdf_path} (lead={lead.pk})')
        return False

    try:
        subject = f'El mapa completo de tu herida'
        body_text = (
            'Acá está el mapa completo de tu herida, en PDF — va adjunto.\n\n'
            'Es un fragmento de Endonautica, el libro completo. Si querés el resto '
            'del mapa, respondé este correo o escribinos por WhatsApp.\n\n'
            '— Franco'
        )
        msg = EmailMultiAlternatives(subject, body_text, to=[lead.email])
        with open(pdf_path, 'rb') as f:
            msg.attach(f'mapa-herida-{lead.herida}.pdf', f.read(), 'application/pdf')
        msg.send(fail_silently=False)
    except Exception as e:
        logger.error(f'entregar_pdf_herida error (lead={lead.pk}): {e}')
        return False

    lead.status = EbookLead.STATUS_PDF_ENTREGADO
    lead.save(update_fields=['status', 'updated_at'])
    return True


def entregar_ebook(order, request=None):
    """Envía el email con el link de descarga tokenizado. Nunca lanza — si falla,
    la orden queda 'paid' igual y el fallback es entrega manual por WhatsApp
    (el registro queda visible en el admin para hacerlo a mano)."""
    try:
        path = reverse('descargar_ebook', args=[order.download_token])
        download_url = request.build_absolute_uri(path) if request else path
        subject = 'Tu ejemplar de Endonautica'
        body_text = (
            f'Gracias por tu compra.\n\n'
            f'Acá está tu ejemplar de Endonautica: {download_url}\n\n'
            f'Cualquier problema con la descarga, responde este correo o escríbenos por WhatsApp.\n\n'
            f'— Franco'
        )
        body_html = (
            f'<p>Gracias por tu compra.</p>'
            f'<p>Acá está tu ejemplar de <strong>Endonautica</strong>:</p>'
            f'<p><a href="{download_url}">Descargar el libro (EPUB)</a></p>'
            f'<p>Cualquier problema con la descarga, responde este correo o escríbenos por WhatsApp.</p>'
            f'<p>— Franco</p>'
        )
        msg = EmailMultiAlternatives(subject, body_text, to=[order.user.email])
        msg.attach_alternative(body_html, 'text/html')
        msg.send(fail_silently=False)
    except Exception as e:
        logger.error(f'entregar_ebook error (order={order.pk}): {e}')
        return False

    order.status = EbookOrder.STATUS_DELIVERED
    from django.utils import timezone
    order.delivered_at = timezone.now()
    order.save(update_fields=['status', 'delivered_at', 'updated_at'])
    return True


def descargar_ebook(request, token):
    order = EbookOrder.objects.filter(
        download_token=token,
        status__in=[EbookOrder.STATUS_PAID, EbookOrder.STATUS_DELIVERED],
    ).first()
    if not order:
        raise Http404('Link inválido o vencido.')
    if not os.path.exists(EPUB_PATH):
        raise Http404('Archivo no disponible — escríbenos por WhatsApp.')
    return FileResponse(
        open(EPUB_PATH, 'rb'), as_attachment=True, filename='Endonautica.epub',
    )
