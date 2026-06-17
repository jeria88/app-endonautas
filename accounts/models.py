from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email requerido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('navegante', 'Navegante'),
        ('practicante', 'Practicante'),
        ('empresa', 'Empresa'),
    ]
    AESTHETIC_CHOICES = [
        ('cosmos', 'Cósmico'),
        ('mandala', 'Mandala'),
        ('archipielago', 'Archipiélago'),
        ('arbol', 'Árbol'),
    ]
    PALETTE_CHOICES = [
        ('cosmos', 'Cosmos (por defecto)'),
        ('aurora', 'Aurora Boreal'),
        ('terra', 'Tierra Viva'),
        ('obsidian', 'Obsidiana'),
        ('sakura', 'Sakura'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    map_aesthetic = models.CharField(max_length=20, choices=AESTHETIC_CHOICES, default='cosmos')
    color_palette = models.CharField(max_length=20, choices=PALETTE_CHOICES, default='cosmos')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    # Onboarding
    onboarding_complete = models.BooleanField(default=False)
    onboarding_entry_point = models.CharField(max_length=100, blank=True)
    onboarding_noise_area = models.CharField(max_length=100, blank=True)
    onboarding_nucleo = models.JSONField(default=dict, blank=True)

    # Hotmart
    hotmart_subscriber_code = models.CharField(max_length=100, blank=True)
    tokens_last_renewed = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_practicante(self):
        return self.plan in ('practicante', 'empresa')

    def __str__(self):
        return f'{self.user.email} ({self.plan})'
