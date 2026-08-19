import json
import os

from django.core.management.base import BaseCommand

HERIDAS_JSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ebook_files', 'heridas.json'
)
OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ebook_files'
)


class Command(BaseCommand):
    help = (
        'Genera los 5 PDF "Mapa de tu herida" desde ebook_files/heridas.json '
        '(extraído de endonautas-web/src/data/heridas.ts — fuente única, no se '
        'transcribe contenido a mano). Mismo estilo visual que psychometrics/views.py.'
    )

    def handle(self, *args, **options):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

        with open(HERIDAS_JSON, encoding='utf-8') as f:
            heridas = json.load(f)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'HeridaTitle', parent=styles['Title'], fontSize=22, spaceAfter=6,
            textColor=colors.HexColor('#1a1a1a'),
        )
        mask_style = ParagraphStyle(
            'HeridaMask', parent=styles['Normal'], fontSize=14,
            textColor=colors.HexColor('#7ECCCD'), spaceAfter=14,
        )
        frase_style = ParagraphStyle(
            'Frase', parent=styles['Normal'], fontSize=12, leading=18,
            textColor=colors.HexColor('#333333'), spaceAfter=16, spaceBefore=6,
        )
        h2 = ParagraphStyle('H2', parent=styles['Heading2'], spaceBefore=16, spaceAfter=8)
        body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10.5, leading=16, spaceAfter=8)
        bullet = ParagraphStyle('Bullet', parent=body, leftIndent=14, bulletIndent=0)
        quote = ParagraphStyle(
            'Quote', parent=body, leftIndent=14, textColor=colors.HexColor('#555555'),
            fontName='Helvetica-Oblique',
        )
        faq_q = ParagraphStyle('FaqQ', parent=body, fontName='Helvetica-Bold', spaceBefore=8)

        for h in heridas:
            out_path = os.path.join(OUT_DIR, f"mapa-herida-{h['id']}.pdf")
            doc = SimpleDocTemplate(
                out_path, pagesize=A4,
                topMargin=2.4*cm, bottomMargin=2.2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm,
            )
            story = []
            story.append(Paragraph(f"Mapa de tu herida: {h['herida']}", title_style))
            story.append(Paragraph(h['mascara'], mask_style))
            story.append(HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#DDDDDD')))
            story.append(Paragraph(h['frase'], frase_style))

            for p in h['intro']:
                story.append(Paragraph(p, body))

            story.append(Paragraph('De dónde viene', h2))
            story.append(Paragraph(h['origen'], body))

            story.append(Paragraph('En la adultez', h2))
            for t in h['adultez']:
                story.append(Paragraph(f'• {t}', bullet))

            story.append(Paragraph('En la pareja', h2))
            for t in h['pareja']:
                story.append(Paragraph(f'• {t}', bullet))

            story.append(Paragraph('La voz de adentro', h2))
            for b in h['bucles']:
                story.append(Paragraph(b, quote))

            story.append(Paragraph('En el cuerpo', h2))
            story.append(Paragraph(h['corazaLarga'], body))

            story.append(Paragraph('Por dónde empezar', h2))
            for t in h['trabajo']:
                story.append(Paragraph(t['t'], ParagraphStyle('Wt', parent=body, fontName='Helvetica-Bold', spaceAfter=2)))
                story.append(Paragraph(t['d'], body))

            story.append(Paragraph('Preguntas frecuentes', h2))
            for q, a in h['faq']:
                story.append(Paragraph(q, faq_q))
                story.append(Paragraph(a, body))

            story.append(Spacer(1, 0.8*cm))
            story.append(HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#DDDDDD')))
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph(
                'Esto es un fragmento del marco completo de <i>Endonautica</i>, el libro de '
                'Franco Jeria Castro sobre autoconocimiento y viaje interior. '
                'endonautas.cl',
                ParagraphStyle('Foot', parent=body, fontSize=9, textColor=colors.HexColor('#888888')),
            ))

            doc.build(story)
            self.stdout.write(self.style.SUCCESS(f"OK: {out_path}"))
