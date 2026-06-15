from django.conf import settings

from .models import Mission, MissionCompletion, TokenBalance


def _get_balance(user):
    balance, _ = TokenBalance.objects.get_or_create(user=user)
    return balance


def has_balance(user, cost_key):
    cost = settings.TOKEN_COSTS.get(cost_key, 0)
    return _get_balance(user).balance >= cost


def spend(user, cost_key):
    cost = settings.TOKEN_COSTS.get(cost_key, 0)
    if cost == 0:
        return True
    return _get_balance(user).spend(cost, reason=cost_key)


def credit_permanent(user, amount, reason=''):
    _get_balance(user).credit_permanent(amount, reason)


def credit_mission(user, mission_slug):
    try:
        mission = Mission.objects.get(slug=mission_slug, active=True)
    except Mission.DoesNotExist:
        return False
    _, created = MissionCompletion.objects.get_or_create(user=user, mission=mission)
    if created:
        _get_balance(user).credit_permanent(mission.fracton_reward, reason=f'mission:{mission_slug}')
    return created


def renew_monthly(user):
    from django.utils import timezone
    plan = getattr(getattr(user, 'profile', None), 'plan', 'free')
    amount = settings.PLAN_MONTHLY_TOKENS.get(plan, 100)
    balance = _get_balance(user)
    balance.monthly = amount
    balance.monthly_last_renewed = timezone.now().date()
    balance.save()
