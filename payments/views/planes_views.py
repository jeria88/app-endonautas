from django.conf import settings
from django.shortcuts import render

from ..services.paypal import PLAN_IDS as PAYPAL_PLAN_IDS


def planes(request):
    plan_actual = request.user.profile.plan if request.user.is_authenticated else ''
    return render(request, 'payments/planes.html', {
        'plan_actual': plan_actual,
        'paypal_client_id': getattr(settings, 'PAYPAL_CLIENT_ID', ''),
        'paypal_plan_ids': PAYPAL_PLAN_IDS,
        'mp_public_key': getattr(settings, 'MERCADOPAGO_PUBLIC_KEY', ''),
    })
