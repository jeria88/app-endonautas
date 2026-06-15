def user_context(request):
    if not request.user.is_authenticated:
        return {'map_aesthetic': 'cosmos', 'user_plan': 'free', 'token_balance': 0}
    try:
        profile = request.user.profile
        aesthetic = profile.map_aesthetic
        plan = profile.plan
    except Exception:
        aesthetic = 'cosmos'
        plan = 'free'
    try:
        balance = request.user.token_balance.balance
    except Exception:
        balance = 0
    return {
        'map_aesthetic': aesthetic,
        'user_plan': plan,
        'token_balance': balance,
    }
