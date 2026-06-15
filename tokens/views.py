from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def balance(request):
    try:
        tb = request.user.token_balance
    except Exception:
        tb = None
    return render(request, 'tokens/balance.html', {'tb': tb})


@login_required
def historial(request):
    transactions = request.user.token_transactions.all()[:50]
    return render(request, 'tokens/historial.html', {'transactions': transactions})
