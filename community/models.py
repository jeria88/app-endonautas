from django.conf import settings
from django.db import models


class Post(models.Model):
    SOMATIC_TAGS = [
        ('cuerpo', 'Cuerpo'),
        ('mente', 'Mente'),
        ('emociones', 'Emociones'),
        ('vinculos', 'Vínculos'),
        ('proposito', 'Propósito'),
        ('sombra', 'Sombra'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='community/', blank=True, null=True)
    somatic_tag = models.CharField(max_length=20, choices=SOMATIC_TAGS, blank=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f'{self.author.email}: {self.content[:60]}'


class Reaction(models.Model):
    TYPES = [
        ('resonar', 'Resuena'),
        ('gracias', 'Gracias'),
        ('fuerza', 'Fuerza'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=TYPES)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.email} → {self.reaction_type} on {self.post.pk}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.email}: {self.content[:40]}'


class Forum(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ForumPost(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
