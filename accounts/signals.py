from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_balance(sender, instance, created, **kwargs):
    if not created:
        return
    from accounts.models import UserProfile
    from tokens.models import TokenBalance

    if not hasattr(instance, 'profile'):
        UserProfile.objects.get_or_create(user=instance)
    try:
        instance.token_balance
    except Exception:
        balance = TokenBalance.objects.create(user=instance)
        balance.credit_monthly(settings.PLAN_MONTHLY_TOKENS['free'], reason='signup')
