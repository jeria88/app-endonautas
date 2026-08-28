import logging
import os

from django.conf import settings
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
        subject = 'El mapa completo de tu herida'
        body_text = (
            'Aquí está el mapa completo de tu herida, en PDF — va adjunto.\n\n'
            'Es un fragmento de Endonautica, el libro completo: 207 páginas con esta '
            'herida y las otras cuatro, más el marco entero del viaje interior.\n\n'
            'Si quieres el resto del mapa: https://endonautas.cl/ebook/?herida='
            f'{lead.herida}\n\n'
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
        # El webhook de MP entrega sin request: ahí el link tiene que salir absoluto
        # igual, o el comprador recibe un href relativo que no lleva a ninguna parte.
        download_url = (
            request.build_absolute_uri(path) if request
            else f'{settings.APP_BASE_URL.rstrip("/")}{path}'
        )
        nombre = (order.user.first_name or '').strip()
        saludo = f'Hola {nombre}.' if nombre else 'Hola.'
        subject = 'Tu mapa llegó. Ahora empieza el viaje.'
        body_text = (
            f'{saludo}\n\n'
            f'Aquí está tu ebook: {download_url}\n\n'
            f'Antes de abrirlo, una advertencia honesta:\n\n'
            f'Este no es un libro para leer una vez y guardar. Es un mapa para volver '
            f'cuando te pierdas — y te vas a perder, porque así funciona el viaje interior.\n\n'
            f'No lo leas como información. Léelo como si fuera un espejo.\n\n'
            f'Cada concepto que te genere resistencia es información. Cada cosa que '
            f'reconozcas en ti, también.\n\n'
            f'Bienvenido al viaje.\n\n'
            f'— Franco\n\n'
            f'Si el link no funciona, responde este correo y lo resolvemos.'
        )
        body_html = (
            f'<p>{saludo}</p>'
            f'<p>Aquí está tu ebook:</p>'
            f'<p><a href="{download_url}">Descargar <strong>Endonautica</strong> (EPUB)</a></p>'
            f'<p>Antes de abrirlo, una advertencia honesta:</p>'
            f'<p>Este no es un libro para leer una vez y guardar. Es un mapa para volver '
            f'cuando te pierdas — y te vas a perder, porque así funciona el viaje interior.</p>'
            f'<p>No lo leas como información. <strong>Léelo como si fuera un espejo.</strong></p>'
            f'<p>Cada concepto que te genere resistencia es información. '
            f'Cada cosa que reconozcas en ti, también.</p>'
            f'<p>Bienvenido al viaje.</p>'
            f'<p>— Franco</p>'
            f'<p style="color:#777;font-size:13px">Si el link no funciona, responde este correo y lo resolvemos.</p>'
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
