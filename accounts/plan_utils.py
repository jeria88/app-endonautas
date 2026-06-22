PLAN_ORDER = {'free': 0, 'navegante': 1, 'practicante': 2, 'empresa': 3}

FREE_TEST_SLUGS = {
    'big-five-inventario-de-personalidad',
    'heridas-de-la-infancia-lise-bourbeau',
    'dirty-dozen-triada-oscura',
}

FREE_TAROT_TIRADAS = {'un_arcano'}


def user_plan(user):
    return getattr(getattr(user, 'profile', None), 'plan', 'free')


def plan_at_least(user, min_plan):
    return PLAN_ORDER.get(user_plan(user), 0) >= PLAN_ORDER.get(min_plan, 0)


def upgrade_wall(request, required_plan='navegante', feature='esta función'):
    from django.shortcuts import render
    plan_names = {'navegante': 'Navegante', 'practicante': 'Practicante'}
    return render(request, 'accounts/upgrade_wall.html', {
        'required_plan': required_plan,
        'required_plan_name': plan_names.get(required_plan, required_plan.title()),
        'feature': feature,
    })
