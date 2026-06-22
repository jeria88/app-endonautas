def user_context(request):
    if not request.user.is_authenticated:
        return {'map_aesthetic': 'cosmos', 'user_plan': 'free'}
    try:
        profile = request.user.profile
        aesthetic = profile.map_aesthetic
        plan = profile.plan
    except Exception:
        aesthetic = 'cosmos'
        plan = 'free'
    return {
        'map_aesthetic': aesthetic,
        'user_plan': plan,
    }
