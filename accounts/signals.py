from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_balance(sender, instance, created, **kwargs):
    if not created:
        return
    from accounts.models import UserProfile
    from tokens.models import TokenBalance

    UserProfile.objects.get_or_create(user=instance)
    TokenBalance.objects.get_or_create(user=instance)
