"""Actividad de la comunidad → harness de ACME Agents (evento `actividad_comunidad`).

El harness la usa para saber quién participa (y avisarle al dueño cuándo conviene una invitación
personal). No cuenta lo que publica el propio dueño (FRANCO_EMAIL). No-op sin HARNESS_API_KEY.
"""
from django.conf import settings
from django.db.models.signals import post_save

from payments.services import harness

from .models import Comment, ForumPost, ForumReply, Post

_TIPO = {Post: 'post', Comment: 'comentario', ForumPost: 'foro_post', ForumReply: 'foro_respuesta'}


def _avisar(sender, instance, created, **kwargs):
    if not created:
        return
    autor = getattr(instance, 'author', None)
    email = (getattr(autor, 'email', '') or '').lower()
    if not email or email == (settings.FRANCO_EMAIL or '').lower():
        return
    datos = {'tipo': _TIPO[sender]}
    foro = getattr(instance, 'forum', None) or getattr(getattr(instance, 'post', None), 'forum', None)
    if foro is not None:
        datos['foro'] = foro.slug
    harness.emitir('actividad_comunidad', {'email': email, 'nombre': autor.first_name or None, 'fuente': 'comunidad'},
                   datos=datos, dedupe_key=f'com-{_TIPO[sender]}-{instance.pk}')


for _modelo in _TIPO:
    post_save.connect(_avisar, sender=_modelo, dispatch_uid=f'harness-{_modelo.__name__}')
