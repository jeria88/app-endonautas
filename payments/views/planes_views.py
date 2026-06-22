from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..services.paypal import PLAN_IDS as PAYPAL_PLAN_IDS


@login_required
def planes(request):
    plan_actual = request.user.profile.plan
    return render(request, 'payments/planes.html', {
        'plan_actual': plan_actual,
        'paypal_client_id': getattr(settings, 'PAYPAL_CLIENT_ID', ''),
        'paypal_plan_ids': PAYPAL_PLAN_IDS,
        'mp_public_key': getattr(settings, 'MERCADOPAGO_PUBLIC_KEY', ''),
    })
