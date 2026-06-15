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
    results = client.test_results.select_related('test').all()
    return render(request, 'practitioners/client_detail.html', {
        'client': client, 'notes': notes, 'sessions': sessions, 'results': results,
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
    sessions = TherapySession.objects.filter(practitioner=request.user).order_by('datetime')
    return render(request, 'practitioners/agenda.html', {'sessions': sessions})


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
    return render(request, 'practitioners/session_form.html', {'clients': clients})


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


def claim_profile(request, code):
    tp = get_object_or_404(TemporaryProfile, access_code=code)
    if request.user.is_authenticated:
        if tp.claimed_by is None:
            tp.claimed_by = request.user
            tp.save()
        return redirect('dashboard')
    request.session['claim_code'] = str(code)
    return redirect(f'/registro/?next=/practicantes/invitar/{code}/')
