from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Availability, SessionNote, TemporaryProfile, TherapySession


@login_required
def dashboard(request):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    clients = TemporaryProfile.objects.filter(practitioner=request.user).select_related('claimed_by')
    upcoming = TherapySession.objects.filter(
        practitioner=request.user, status__in=('pending', 'confirmed')
    ).order_by('datetime')[:5]
    return render(request, 'practitioners/dashboard.html', {'clients': clients, 'upcoming': upcoming})


@login_required
def client_create(request):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    if request.method == 'POST':
        alias = request.POST.get('alias', '').strip()
        if alias:
            tp = TemporaryProfile.objects.create(
                practitioner=request.user,
                alias=alias,
                email=request.POST.get('email', ''),
                notes=request.POST.get('notes', ''),
            )
            if request.POST.get('send_invite') and tp.email:
                _send_invite(request, tp)
            return redirect('practitioners_client_detail', pk=tp.pk)
    return render(request, 'practitioners/client_form.html')


def _send_invite(request, profile):
    from django.conf import settings
    from django.core.mail import send_mail
    invite_url = request.build_absolute_uri(f'/practicantes/invitar/{profile.access_code}/')
    send_mail(
        subject='Tu terapeuta te invita a Endonautas',
        message=f'Accede aquí para ver tus resultados: {invite_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[profile.email],
        fail_silently=True,
    )


@login_required
def client_detail(request, pk):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    client = get_object_or_404(TemporaryProfile, pk=pk, practitioner=request.user)
    notes = client.session_notes.all()
    sessions = client.sessions.all()
    results = client.temp_test_results.select_related('test').all()
    fichas = client.consultas.select_related('usuario').order_by('-fecha_creacion')
    return render(request, 'practitioners/client_detail.html', {
        'client': client, 'notes': notes, 'sessions': sessions,
        'results': results, 'fichas': fichas,
    })


@login_required
def session_note_create(request, pk):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    client = get_object_or_404(TemporaryProfile, pk=pk, practitioner=request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        date = request.POST.get('session_date')
        if content and date:
            SessionNote.objects.create(
                profile=client, practitioner=request.user, content=content, session_date=date
            )
        return redirect('practitioners_client_detail', pk=pk)
    return render(request, 'practitioners/note_form.html', {'client': client})


@login_required
def agenda(request):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    import calendar
    import datetime
    import json
    from django.utils import timezone

    today = timezone.now().date()
    try:
        year  = int(request.GET.get('year',  today.year))
        month = int(request.GET.get('month', today.month))
    except ValueError:
        year, month = today.year, today.month

    if month < 1:
        month, year = 12, year - 1
    elif month > 12:
        month, year = 1, year + 1

    first_day = datetime.date(year, month, 1)
    days_in_month = calendar.monthrange(year, month)[1]
    last_day = datetime.date(year, month, days_in_month)

    month_sessions = TherapySession.objects.filter(
        practitioner=request.user,
        datetime__date__gte=first_day,
        datetime__date__lte=last_day,
    ).select_related('profile').order_by('datetime')

    cal_sessions = [
        {
            'day':    s.datetime.day,
            'time':   s.datetime.strftime('%H:%M'),
            'client': s.profile.alias,
            'email':  s.profile.email,
            'type':   s.get_session_type_display(),
            'status': s.status,
            'pk':     s.pk,
        }
        for s in month_sessions
    ]

    upcoming = TherapySession.objects.filter(
        practitioner=request.user,
        datetime__gte=timezone.now(),
        status__in=('pending', 'confirmed'),
    ).select_related('profile').order_by('datetime')[:10]

    prev_month, prev_year = (12, year - 1) if month == 1 else (month - 1, year)
    next_month, next_year = (1,  year + 1) if month == 12 else (month + 1, year)

    MONTHS_ES = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    return render(request, 'practitioners/agenda.html', {
        'upcoming':       upcoming,
        'cal_data_json':  json.dumps(cal_sessions),
        'year':           year,
        'month':          month,
        'month_name':     MONTHS_ES[month],
        'prev_year':      prev_year,
        'prev_month':     prev_month,
        'next_year':      next_year,
        'next_month':     next_month,
        'today_day':      today.day if (today.year == year and today.month == month) else 0,
        'days_in_month':  days_in_month,
        'first_weekday':  calendar.monthrange(year, month)[0],
    })


@login_required
def session_create(request):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    clients = TemporaryProfile.objects.filter(practitioner=request.user)
    if request.method == 'POST':
        client = get_object_or_404(TemporaryProfile, pk=request.POST['client'], practitioner=request.user)
        TherapySession.objects.create(
            practitioner=request.user,
            profile=client,
            datetime=request.POST['datetime'],
            duration_minutes=int(request.POST.get('duration', 60)),
            session_type=request.POST.get('session_type', 'online'),
            meeting_url=request.POST.get('meeting_url', ''),
            notes=request.POST.get('notes', ''),
        )
        return redirect('practitioners_agenda')
    preselected_pk = request.GET.get('client', '')
    return render(request, 'practitioners/session_form.html', {
        'clients': clients,
        'preselected_pk': preselected_pk,
    })


@login_required
def availability(request):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    slots = Availability.objects.filter(practitioner=request.user)
    if request.method == 'POST':
        Availability.objects.filter(practitioner=request.user).delete()
        days = request.POST.getlist('day_of_week')
        starts = request.POST.getlist('start_time')
        ends = request.POST.getlist('end_time')
        for day, start, end in zip(days, starts, ends):
            if day and start and end:
                Availability.objects.get_or_create(
                    practitioner=request.user, day_of_week=int(day),
                    start_time=start, defaults={'end_time': end}
                )
        return redirect('practitioners_availability')
    return render(request, 'practitioners/availability.html', {'slots': slots})


@login_required
def fichas_list(request):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    from terapeuta.models import Consulta
    fichas = (
        Consulta.objects
        .filter(usuario=request.user, modo='terapeuta')
        .select_related('perfil_cliente')
        .order_by('-fecha_creacion')
    )
    clients = TemporaryProfile.objects.filter(practitioner=request.user)
    return render(request, 'practitioners/fichas_list.html', {'fichas': fichas, 'clients': clients})


@login_required
def ficha_create(request, profile_pk):
    if not request.user.profile.is_practicante:
        return redirect('dashboard')
    from terapeuta.models import Consulta
    client = get_object_or_404(TemporaryProfile, pk=profile_pk, practitioner=request.user)
    consulta = Consulta.objects.create(
        modo='terapeuta',
        usuario=request.user,
        perfil_cliente=client,
        nombre_paciente=client.alias,
        paso_actual=1,
    )
    return redirect('terapeuta:paso1', consulta_id=consulta.id)


def claim_profile(request, code):
    tp = get_object_or_404(TemporaryProfile, access_code=code)
    if request.user.is_authenticated:
        if tp.claimed_by is None:
            tp.claimed_by = request.user
            tp.save()
        return redirect('dashboard')
    request.session['claim_code'] = str(code)
    return redirect(f'/registro/?next=/practicantes/invitar/{code}/')
