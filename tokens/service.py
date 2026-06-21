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
    amount = settings.PLAN_MONTHLY_TOKENS.get(plan, 80)
    balance = _get_balance(user)
    balance.monthly = amount
    balance.monthly_last_renewed = timezone.now().date()
    balance.save()


def get_or_create_referral_code(user):
    from .models import ReferralCode
    code, _ = ReferralCode.objects.get_or_create(user=user)
    return code


def process_referral_signup(code_str, new_user):
    from .models import Referral, ReferralCode
    try:
        ref_code = ReferralCode.objects.get(code=code_str)
    except ReferralCode.DoesNotExist:
        return False
    if ref_code.user_id == new_user.pk:
        return False
    referral, created = Referral.objects.get_or_create(
        referred=new_user,
        defaults={'referrer': ref_code.user},
    )
    if created:
        rewards = settings.REFERRAL_REWARDS
        _get_balance(ref_code.user).credit_permanent(rewards['signup_referrer'], reason='referral:signup')
        _get_balance(new_user).credit_permanent(rewards['signup_referred'], reason='referral:welcome')
        referral.signup_rewarded = True
        referral.save(update_fields=['signup_rewarded'])
    return True


def process_referral_conversion(user):
    from .models import Referral
    updated = Referral.objects.filter(referred=user, conversion_rewarded=False).first()
    if not updated:
        return False
    _get_balance(updated.referrer).credit_permanent(
        settings.REFERRAL_REWARDS['conversion_referrer'], reason='referral:conversion'
    )
    updated.conversion_rewarded = True
    updated.save(update_fields=['conversion_rewarded'])
    return True
