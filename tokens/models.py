import uuid

from django.conf import settings
from django.db import models


class TokenBalance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='token_balance')
    permanent = models.IntegerField(default=0)
    monthly = models.IntegerField(default=0)
    monthly_last_renewed = models.DateField(null=True, blank=True)

    @property
    def balance(self):
        return self.permanent + self.monthly

    def spend(self, amount, reason=''):
        if self.balance < amount:
            return False
        if self.monthly >= amount:
            self.monthly -= amount
        else:
            remaining = amount - self.monthly
            self.monthly = 0
            self.permanent -= remaining
        self.save()
        TokenTransaction.objects.create(user=self.user, amount=-amount, reason=reason)
        return True

    def credit_permanent(self, amount, reason=''):
        self.permanent += amount
        self.save()
        TokenTransaction.objects.create(user=self.user, amount=amount, reason=reason)

    def credit_monthly(self, amount, reason=''):
        self.monthly += amount
        self.save()
        TokenTransaction.objects.create(user=self.user, amount=amount, reason=f'[monthly] {reason}')

    def __str__(self):
        return f'{self.user.email}: {self.balance} ({self.permanent}p + {self.monthly}m)'


class TokenTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='token_transactions')
    amount = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        sign = '+' if self.amount > 0 else ''
        return f'{self.user.email} {sign}{self.amount} — {self.reason}'


class Mission(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    fracton_reward = models.IntegerField()
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} (+{self.fracton_reward})'


class MissionCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mission_completions')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'mission')

    def __str__(self):
        return f'{self.user.email} — {self.mission.slug}'


class ReferralCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(max_length=12, unique=True)
    click_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.email} → {self.code}'


class Referral(models.Model):
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referral_origin')
    created_at = models.DateTimeField(auto_now_add=True)
    signup_rewarded = models.BooleanField(default=False)
    conversion_rewarded = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.referrer.email} → {self.referred.email}'
