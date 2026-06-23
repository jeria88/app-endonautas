from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_balance(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        from accounts.models import UserProfile
        from tokens.models import ReferralCode, TokenBalance
        UserProfile.objects.get_or_create(user=instance)
        balance, balance_created = TokenBalance.objects.get_or_create(user=instance)
        if balance_created:
            balance.credit_monthly(settings.PLAN_MONTHLY_TOKENS['free'], reason='signup')
        ReferralCode.objects.get_or_create(user=instance)
    except Exception:
        pass

    try:
        from accounts.listmonk import subscribe_user, send_welcome_email
        name = f'{instance.first_name} {instance.last_name}'.strip()
        subscribe_user(instance.email, plan='free', name=name)
        send_welcome_email(instance.email, name=name)
    except Exception:
        pass
