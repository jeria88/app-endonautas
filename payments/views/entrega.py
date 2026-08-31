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

# El PDF va primero en todos lados: mucha gente no tiene lector de EPUB, y un
# libro que no se puede abrir es un reembolso. Se generan los dos con
# `ebook-venta/generar.sh`.
FORMATOS = {
    'pdf':  ('endonautica.pdf',  'Endonautica.pdf',  'application/pdf'),
    'epub': ('endonautica.epub', 'Endonautica.epub', 'application/epub+zip'),
}


def _avisar_fallo(lead, motivo):
    """Un lead que no recibe su PDF queda en 'nuevo' y hay que descubrirlo mirando
    el admin. Avisar es la diferencia entre reenviarlo a mano hoy o perderlo."""
    try:
        from django.core.mail import mail_admins, send_mail
        destino = getattr(settings, 'FRANCO_EMAIL', '')
        cuerpo = (
            f'No se pudo entregar el PDF de la herida.\n\n'
            f'Lead: {lead.pk} — {lead.email}\nHerida: {lead.herida}\n'
            f'Origen: {lead.canal_origen}\nMotivo: {motivo}\n\n'
            f'Reenviar a mano desde el admin.'
        )
        if destino:
            send_mail('[Endonautas] Lead sin PDF', cuerpo,
                      settings.DEFAULT_FROM_EMAIL, [destino], fail_silently=True)
        else:
            mail_admins('[Endonautas] Lead sin PDF', cuerpo, fail_silently=True)
    except Exception:
        pass


def entregar_pdf_herida(lead):
    """Envía por email el PDF 'mapa de tu herida' generado por
    `manage.py generar_pdfs_heridas` desde heridas.ts. Nunca lanza — si falla,
    el lead queda en 'nuevo' y es visible en el admin para reenviar a mano."""
    if not lead.email:
        return False

    pdf_path = os.path.join(EBOOK_FILES_DIR, f'mapa-herida-{lead.herida}.pdf')
    if not os.path.exists(pdf_path):
        logger.error(f'entregar_pdf_herida: no existe {pdf_path} (lead={lead.pk})')
        _avisar_fallo(lead, f'no existe el PDF {pdf_path}')
        return False

    try:
        sitio = settings.PUBLIC_SITE_URL.rstrip('/')
        subject = 'El mapa completo de tu herida'
        body_text = (
            'Aquí va, en PDF adjunto: el mapa completo de tu herida principal — cómo se '
            'formó, la máscara que armaste encima y qué la sostiene hoy.\n\n'
            'Es un fragmento de La Endonáutica. El libro entero trae esta herida y las '
            'otras cuatro, más el marco completo del viaje interior: 205 páginas, mi '
            'sistema para leerte con precisión.\n\n'
            'Si quieres dejar de operar desde esta herida, el resto del mapa está aquí '
            f'(con la página adaptada a tu perfil):\n{sitio}/?herida={lead.herida}\n\n'
            '— Franco'
        )
        msg = EmailMultiAlternatives(subject, body_text, to=[lead.email])
        with open(pdf_path, 'rb') as f:
            msg.attach(f'mapa-herida-{lead.herida}.pdf', f.read(), 'application/pdf')
        msg.send(fail_silently=False)
    except Exception as e:
        logger.error(f'entregar_pdf_herida error (lead={lead.pk}): {e}')
        _avisar_fallo(lead, str(e))
        return False

    lead.status = EbookLead.STATUS_PDF_ENTREGADO
    lead.save(update_fields=['status', 'updated_at'])
    return True


def entregar_ebook(order, request=None):
    """Envía el email con el link de descarga tokenizado. Nunca lanza — si falla,
    la orden queda 'paid' igual y el fallback es entrega manual por WhatsApp
    (el registro queda visible en el admin para hacerlo a mano)."""
    try:
        def url(formato):
            path = reverse('descargar_ebook_formato', args=[order.download_token, formato])
            # El webhook de MP entrega sin request: ahí el link tiene que salir
            # absoluto igual, o el comprador recibe un href que no lleva a ningún lado.
            return (request.build_absolute_uri(path) if request
                    else f'{settings.APP_BASE_URL.rstrip("/")}{path}')

        url_pdf, url_epub = url('pdf'), url('epub')
        download_url = url_pdf
        nombre = (order.user.first_name or '').strip()
        saludo = f'Hola {nombre}.' if nombre else 'Hola.'
        subject = 'Tu mapa llegó. Ahora empieza el viaje.'
        body_text = (
            f'{saludo}\n\n'
            f'Aquí está tu libro, en los dos formatos:\n\n'
            f'  PDF ilustrado — con las láminas de cada capítulo, ideal para pantallas '
            f'grandes o para imprimir: {url_pdf}\n'
            f'  EPUB — para Kindle, Apple Books o el lector de tu teléfono: {url_epub}\n\n'
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
            f'<p>Aquí está tu libro, en los dos formatos:</p>'
            f'<p><a href="{url_pdf}"><strong>Descargar el PDF ilustrado</strong></a>'
            f' — con las láminas de cada capítulo, ideal para pantallas grandes o para imprimir.<br>'
            f'<a href="{url_epub}">Descargar en EPUB</a>'
            f' — para Kindle, Apple Books o el lector de tu teléfono.</p>'
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


def descargar_ebook(request, token, formato='epub'):
    """`formato` por defecto es epub para no romper los links ya enviados por
    email antes de que existiera el PDF."""
    order = EbookOrder.objects.filter(
        download_token=token,
        status__in=[EbookOrder.STATUS_PAID, EbookOrder.STATUS_DELIVERED],
    ).first()
    if not order:
        raise Http404('Link inválido o vencido.')

    archivo, nombre, tipo = FORMATOS.get(formato, FORMATOS['epub'])
    ruta = os.path.join(EBOOK_FILES_DIR, archivo)
    if not os.path.exists(ruta):
        logger.error(f'descargar_ebook: falta {ruta} (order={order.pk})')
        raise Http404('Archivo no disponible — escríbenos por WhatsApp.')
    return FileResponse(
        open(ruta, 'rb'), as_attachment=True, filename=nombre, content_type=tipo,
    )
