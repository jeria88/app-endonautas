import datetime
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .models import UserProfile

FRASES = [
    "Tú tienes el poder, no la IA.",
    "El autoconocimiento no es un destino, es una práctica.",
    "Lo que resistes, persiste. Lo que observas, se transforma.",
    "Cada patrón que ves en ti mismo es una puerta.",
    "No hay camino equivocado, hay caminos no explorados.",
    "La presencia es el principio de todo cambio real.",
    "Romper el patrón comienza con nombrarlo.",
    "La incomodidad que sientes es información, no amenaza.",
    "Eres el observador y lo observado.",
    "El inconsciente habla. Aprende su idioma.",
]


def referral_redirect(request, code):
    from tokens.models import ReferralCode
    try:
        ReferralCode.objects.filter(code=code).update(click_count=F('click_count') + 1)
        request.session['ref_code'] = code
    except Exception:
        pass
    return redirect('register')


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


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

        ref_code = request.session.pop('ref_code', None)
        if ref_code:
            from tokens.service import process_referral_signup
            process_referral_signup(ref_code, user)

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('onboarding')
    return render(request, 'accounts/register.html')


@login_required
def dashboard(request):
    from mirror.models import ChatSession, BitacoraEntry
    from psychometrics.models import TestResult
    from tokens.models import TokenBalance, MissionCompletion, Mission

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    frase = random.choice(FRASES)

    ultima_sesion = ChatSession.objects.filter(user=request.user).order_by('-updated_at').first()
    ultimos_resultados = TestResult.objects.filter(user=request.user).select_related('test').order_by('-completed_at')[:3]

    misiones_completadas = set(
        MissionCompletion.objects.filter(user=request.user).values_list('mission__slug', flat=True)
    )
    misiones_pendientes = Mission.objects.filter(active=True).exclude(slug__in=misiones_completadas)[:4]

    ultimas_bitacora = BitacoraEntry.objects.filter(user=request.user).order_by('-created_at')[:3]

    try:
        balance = TokenBalance.objects.get(user=request.user).balance
    except TokenBalance.DoesNotExist:
        balance = 0

    return render(request, 'accounts/dashboard.html', {
        'profile': profile,
        'frase': frase,
        'ultima_sesion': ultima_sesion,
        'ultimos_resultados': ultimos_resultados,
        'misiones_pendientes': misiones_pendientes,
        'ultimas_bitacora': ultimas_bitacora,
        'balance': balance,
    })


@login_required
def perfil(request):
    from tokens.service import get_or_create_referral_code
    from tokens.models import Referral
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.map_aesthetic = request.POST.get('map_aesthetic', profile.map_aesthetic)
        profile.color_palette = request.POST.get('color_palette', profile.color_palette)
        profile.bio = request.POST.get('bio', profile.bio)
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        profile.save()
        if request.POST.get('first_name'):
            request.user.first_name = request.POST['first_name']
            request.user.save(update_fields=['first_name'])
        return redirect('perfil')
    referral_code = get_or_create_referral_code(request.user)
    referrals_made = Referral.objects.filter(referrer=request.user)
    conversions = referrals_made.filter(conversion_rewarded=True).count()
    from payments.constants import PACKS
    return render(request, 'accounts/perfil.html', {
        'profile': profile,
        'referral_code': referral_code,
        'referrals_count': referrals_made.count(),
        'conversions_count': conversions,
        'packs': PACKS,
    })


@login_required
def configuracion(request):
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
    is_own = (target == request.user)
    return render(request, 'accounts/perfil_social.html', {
        'target': target, 'posts': posts, 'is_own': is_own
    })


@login_required
def onboarding(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.onboarding_complete:
        return redirect('dashboard')
    if request.method == 'POST':
        import json as _json
        raw = request.POST.get('priorities', '')
        try:
            priorities = _json.loads(raw) if raw.startswith('[') else [p.strip() for p in raw.split(',') if p.strip()]
        except Exception:
            priorities = []
        profile.onboarding_priorities  = priorities
        profile.onboarding_entry_point = priorities[0] if priorities else ''
        profile.onboarding_complete    = True
        profile.save(update_fields=['onboarding_priorities', 'onboarding_entry_point', 'onboarding_complete'])
        from tokens.service import credit_mission
        credit_mission(request.user, 'onboarding')
        return redirect('dashboard')
    return render(request, 'accounts/onboarding.html')
