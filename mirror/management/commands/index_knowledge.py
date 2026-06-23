from django.core.management.base import BaseCommand

from mirror.models import KnowledgeChunk


class Command(BaseCommand):
    help = 'Genera embeddings para KnowledgeChunks sin embedding via DeepSeek API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerar todos los embeddings aunque ya existan',
        )

    def handle(self, *args, **options):
        from config.ai_client import get_embedding

        qs = KnowledgeChunk.objects.all() if options['force'] else KnowledgeChunk.objects.filter(embedding=[])
        total = qs.count()
        if total == 0:
            self.stdout.write('No hay chunks pendientes de embedding.')
            return

        self.stdout.write(f'Generando embeddings para {total} chunks...')
        ok = 0
        errors = 0
        for chunk in qs.iterator():
            vec = get_embedding(chunk.content[:2000])
            if vec:
                chunk.embedding = vec
                chunk.save(update_fields=['embedding'])
                ok += 1
            else:
                errors += 1
            processed = ok + errors
            if processed % 10 == 0:
                self.stdout.write(f'  {processed}/{total}...')

        self.stdout.write(self.style.SUCCESS(f'Listo: {ok} embeddings generados, {errors} errores.'))
