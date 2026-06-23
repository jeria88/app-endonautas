"""
Ingest el PDF de Endonautica en KnowledgeChunk.

Uso:
    python3 manage.py seed_endonautica_pdf
    python3 manage.py seed_endonautica_pdf --force   # re-crea todos los chunks

El PDF debe estar en la ruta indicada en PDF_PATH. Se divide por párrafos
aproximados de ~700 caracteres para mantener coherencia semántica.
"""
import os
import textwrap

from django.core.management.base import BaseCommand

from mirror.models import KnowledgeChunk

PDF_PATH = '/home/nikka/Proyectos/endonautas/Legacy/assets/pdfs/endonautica-teoria-autoconocimiento.pdf'
AUTHOR = 'Franco Jeria Castro'
SOURCE = 'endonautica-pdf'
CHUNK_SIZE = 700


class Command(BaseCommand):
    help = 'Ingest el PDF de Endonautica en KnowledgeChunk (~700 chars por chunk)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Eliminar chunks existentes de esta fuente y re-crearlos',
        )

    def handle(self, *args, **options):
        try:
            import PyPDF2
        except ImportError:
            self.stderr.write(self.style.ERROR('PyPDF2 no instalado. Ejecuta: pip install PyPDF2'))
            return

        if not os.path.exists(PDF_PATH):
            self.stderr.write(self.style.ERROR(f'PDF no encontrado: {PDF_PATH}'))
            return

        if options['force']:
            deleted, _ = KnowledgeChunk.objects.filter(source=SOURCE).delete()
            self.stdout.write(f'Eliminados {deleted} chunks existentes.')

        # Extraer texto del PDF página a página
        pages_text = []
        with open(PDF_PATH, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)
            self.stdout.write(f'PDF: {total_pages} páginas')
            for i, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ''
                if text.strip():
                    pages_text.append((i, text))

        # Dividir en chunks de ~CHUNK_SIZE caracteres respetando límites de párrafo
        raw_chunks = []
        for page_num, text in pages_text:
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            for para in paragraphs:
                # Partir párrafos muy largos en fragmentos de CHUNK_SIZE
                if len(para) > CHUNK_SIZE * 1.5:
                    for fragment in textwrap.wrap(para, CHUNK_SIZE):
                        raw_chunks.append((page_num, fragment))
                else:
                    raw_chunks.append((page_num, para))

        created = 0
        skipped = 0
        for page_num, content in raw_chunks:
            if len(content) < 60:  # ignorar fragmentos muy cortos (headers, números)
                continue
            title = f'Endonautica — pág {page_num}'
            _, was_created = KnowledgeChunk.objects.get_or_create(
                title=title,
                source=SOURCE,
                defaults={
                    'author': AUTHOR,
                    'content': content,
                    'embedding': [],
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(f'Listo: {created} chunks creados, {skipped} ya existían.')
        )
        self.stdout.write('Próximo paso: python3 manage.py index_knowledge')
