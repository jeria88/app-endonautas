from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='psychometrics.TestResult')
def reward_test_completion(sender, instance, created, **kwargs):
    if not created or not instance.user:
        return
    from tokens.service import credit_mission, credit_permanent

    reward = settings.FRACTON_REWARDS.get('test_completed', 8)
    credit_permanent(instance.user, reward, reason='test_completed')

    credit_mission(instance.user, 'first_test')

    _check_dimension_completion(instance)
    _check_weekly_streak(instance.user)


def _check_dimension_completion(result):
    from psychometrics.models import Test, TestResult
    from tokens.service import credit_permanent

    dimension = result.test.dimension
    tests_in_dim = Test.objects.filter(dimension=dimension, active=True)
    completed_slugs = set(
        TestResult.objects.filter(user=result.user, test__dimension=dimension)
        .values_list('test__slug', flat=True)
    )
    if all(t.slug in completed_slugs for t in tests_in_dim):
        reward = settings.FRACTON_REWARDS.get('dimension_completed', 25)
        credit_permanent(result.user, reward, reason=f'dimension_completed:{dimension}')


def _check_weekly_streak(user):
    from django.utils import timezone
    from psychometrics.models import TestResult
    from tokens.service import credit_permanent

    week_ago = timezone.now() - timezone.timedelta(days=7)
    count = TestResult.objects.filter(user=user, completed_at__gte=week_ago).count()
    if count >= 3:
        from tokens.models import TokenTransaction
        already = TokenTransaction.objects.filter(
            user=user, reason='streak_weekly', created_at__gte=week_ago
        ).exists()
        if not already:
            reward = settings.FRACTON_REWARDS.get('streak_weekly', 15)
            credit_permanent(user, reward, reason='streak_weekly')
