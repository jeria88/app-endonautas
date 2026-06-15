from django.conf import settings
from django.db import models


class KnowledgeChunk(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=150, blank=True)
    source = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    embedding = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[:60]} ({self.author})'


class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=200, blank=True)
    conflict_summary = models.TextField(blank=True)
    return_question = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.email} — {self.title or self.pk}'


class ChatMessage(models.Model):
    ROLE_CHOICES = [('user', 'Usuario'), ('assistant', 'Espejo')]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[{self.role}] {self.content[:60]}'


class DreamEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dreams')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_lucid = models.BooleanField(default=False)
    dream_date = models.DateField()
    tags = models.CharField(max_length=200, blank=True)
    reality_check = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dream_date', '-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.title or str(self.dream_date)}'
