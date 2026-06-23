"""
Ingest el libro Endonautica (markdown) en KnowledgeChunk.
Chunkea por sección ## — produce ~40-50 chunks conceptuales en lugar de
204 chunks por página del PDF, lo que da mejor calidad RAG.

Uso:
    python3 manage.py seed_endonautica_md
    python3 manage.py seed_endonautica_md --force   # re-crea todos los chunks
    python3 manage.py seed_endonautica_md --path /ruta/alternativa.md
"""
import re
import textwrap

from django.core.management.base import BaseCommand

from mirror.models import KnowledgeChunk

DEFAULT_PATH = '/home/nikka/Personal/varios/endonautica.md'
AUTHOR = 'Franco Jeria Castro'
SOURCE = 'endonautica-libro'
MAX_SECTION = 3000  # chars máximos por sección — se toma solo el inicio (definición + concepto clave)
MIN_CONTENT = 200   # descartar secciones demasiado cortas (ej: entradas de TOC)


class Command(BaseCommand):
    help = 'Ingest el libro Endonautica (MD) en KnowledgeChunk por sección ##'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true',
                            help='Eliminar chunks existentes de esta fuente y re-crearlos')
        parser.add_argument('--path', default=DEFAULT_PATH,
                            help='Ruta al archivo .md del libro')

    def handle(self, *args, **options):
        import os
        path = options['path']
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f'Archivo no encontrado: {path}'))
            return

        if options['force']:
            deleted, _ = KnowledgeChunk.objects.filter(source=SOURCE).delete()
            self.stdout.write(f'Eliminados {deleted} chunks existentes.')

        with open(path, encoding='utf-8') as f:
            raw = f.read()

        chunks = self._parse_sections(raw)
        self.stdout.write(f'Secciones extraídas: {len(chunks)}')

        created = 0
        skipped = 0
        for title, content in chunks:
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

        self.stdout.write(self.style.SUCCESS(
            f'Listo: {created} chunks creados, {skipped} ya existían.'
        ))
        self.stdout.write('Próximo paso: python3 manage.py index_knowledge')

    def _parse_sections(self, text):
        """Divide el MD por headings # y ##, retorna lista de (title, content)."""
        text = text.replace('\r\n', '\n')
        heading_re = re.compile(r'^(#{1,2})\s+(.+)$')  # solo # y ## (no ###)
        clean_re = re.compile(r'\{#[^}]+\}|\*+')

        current_title = None
        current_lines = []
        sections = []

        def flush():
            if current_title is None:
                return
            content = '\n'.join(current_lines).strip()
            content = clean_re.sub('', content)
            content = re.sub(r'\n{3,}', '\n\n', content).strip()
            if self._is_toc(content) or len(content) < MIN_CONTENT:
                return
            # Solo el inicio de cada sección (la parte definitoria)
            if len(content) > MAX_SECTION:
                content = self._head_at_paragraph(content, MAX_SECTION)
            sections.append((f'Endonautica — {current_title}', content))

        for line in text.split('\n'):
            m = heading_re.match(line)
            if m:
                flush()
                raw_title = m.group(2)
                current_title = re.sub(r'\{#[^}]+\}|\*+', '', raw_title).strip()
                current_lines = []
            elif current_title is not None:
                current_lines.append(line)

        flush()
        return sections

    def _is_toc(self, content):
        """Detecta si el contenido es solo entradas de índice (links Markdown)."""
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        if not lines:
            return True
        link_lines = sum(1 for l in lines if re.match(r'^\[.+?\]\(.+?\)', l))
        return link_lines / max(len(lines), 1) > 0.6

    def _head_at_paragraph(self, content, limit):
        """Toma hasta `limit` chars del contenido, cortando en límite de párrafo."""
        if len(content) <= limit:
            return content
        # Buscar el último \n\n antes del límite
        cut = content.rfind('\n\n', 0, limit)
        if cut > limit // 2:
            return content[:cut].strip()
        # Si no hay párrafo, cortar en el último punto seguido de espacio
        cut = content.rfind('. ', 0, limit)
        if cut > 0:
            return content[:cut + 1].strip()
        return content[:limit].strip()
