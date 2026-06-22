from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..constants import PACKS, PLANS


@login_required
def planes(request):
    plan_actual = request.user.profile.plan
    tokens_mes = settings.PLAN_MONTHLY_TOKENS
    return render(request, 'payments/planes.html', {
        'plan_actual': plan_actual,
        'planes': PLANS,
        'packs': PACKS,
        'tokens_mes': tokens_mes,
    })
