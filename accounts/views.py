from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import UserProfile


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/home.html')


def login_view(request):
    error = None
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        error = 'Credenciales incorrectas'
    return render(request, 'accounts/login.html', {'error': error})


def register_view(request):
    if request.method == 'POST':
        from django.contrib.auth import get_user_model
        User = get_user_model()
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error': 'Email ya registrado'})
        user = User.objects.create_user(email=email, password=password,
                                        first_name=request.POST.get('first_name', ''))
        from tokens.models import TokenBalance
        from django.conf import settings
        balance, created_balance = TokenBalance.objects.get_or_create(user=user)
        if created_balance:
            balance.credit_monthly(settings.PLAN_MONTHLY_TOKENS['free'], reason='signup')

        claimed_code = request.session.pop('claim_code', None)
        if claimed_code:
            from practitioners.models import TemporaryProfile
            try:
                tp = TemporaryProfile.objects.get(access_code=claimed_code, claimed_by=None)
                tp.claimed_by = user
                tp.save()
            except TemporaryProfile.DoesNotExist:
                pass

        login(request, user)
        return redirect('onboarding')
    return render(request, 'accounts/register.html')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required
def perfil(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.map_aesthetic = request.POST.get('map_aesthetic', profile.map_aesthetic)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.save()
        if request.POST.get('first_name'):
            request.user.first_name = request.POST['first_name']
            request.user.save()
        return redirect('perfil')
    return render(request, 'accounts/perfil.html', {'profile': profile})


@login_required
def configuracion(request):
    """Alias de perfil para mantener la URL /configuracion/ del sidebar."""
    return perfil(request)


@login_required
def perfil_social(request, username=None):
    from django.contrib.auth import get_user_model
    from community.models import Post
    User = get_user_model()
    if username:
        target = get_object_or_404(User, email=username)
    else:
        target = request.user
    posts = Post.objects.filter(author=target).order_by('-created_at')[:20]
    return render(request, 'accounts/perfil_social.html', {'target': target, 'posts': posts})


@login_required
def onboarding(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.onboarding_complete:
        return redirect('dashboard')
    if request.method == 'POST':
        step = request.POST.get('step', '1')
        if step == 'final':
            profile.onboarding_entry_point = request.POST.get('entry_point', '')
            profile.onboarding_noise_area = request.POST.get('noise_area', '')
            profile.onboarding_complete = True
            profile.save()
            from tokens.service import credit_mission
            credit_mission(request.user, 'onboarding')
            return redirect('dashboard')
    return render(request, 'accounts/onboarding.html')
