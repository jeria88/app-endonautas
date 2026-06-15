from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import BirthData, BirthReport


@login_required
def birth_home(request):
    try:
        birth = request.user.birth_data
    except BirthData.DoesNotExist:
        birth = None
    reports = BirthReport.objects.filter(birth_data=birth) if birth else []
    return render(request, 'birth/home.html', {'birth': birth, 'reports': reports})


@login_required
def birth_datos(request):
    try:
        birth = request.user.birth_data
    except BirthData.DoesNotExist:
        birth = None

    if request.method == 'POST':
        from timezonefinder import TimezoneFinder
        tf = TimezoneFinder()
        city = request.POST.get('city', '')
        lat = float(request.POST.get('lat') or 0)
        lon = float(request.POST.get('lon') or 0)
        tz = tf.timezone_at(lat=lat, lng=lon) or 'America/Santiago'

        data = dict(
            birth_date=request.POST['birth_date'],
            birth_time=request.POST.get('birth_time') or None,
            city=city,
            country=request.POST.get('country', ''),
            latitude=lat,
            longitude=lon,
            timezone_str=tz,
        )
        if birth:
            for k, v in data.items():
                setattr(birth, k, v)
            birth.save()
            BirthReport.objects.filter(birth_data=birth).delete()
        else:
            BirthData.objects.create(user=request.user, **data)
        return redirect('birth_home')

    return render(request, 'birth/datos.html', {'birth': birth})


@login_required
def birth_astral(request):
    return _birth_report_view(request, 'astral', 'birth/astral.html')


@login_required
def birth_hd(request):
    return _birth_report_view(request, 'hd', 'birth/hd.html')


@login_required
def birth_saju(request):
    return _birth_report_view(request, 'saju', 'birth/saju.html')


def _birth_report_view(request, report_type, template):
    try:
        birth = request.user.birth_data
    except BirthData.DoesNotExist:
        return redirect('birth_datos')

    report, _ = BirthReport.objects.get_or_create(birth_data=birth, report_type=report_type)
    if report.status == 'pending':
        _compute_report(report)
        report.refresh_from_db()

    return render(request, template, {'birth': birth, 'report': report})


def _compute_report(report):
    from django.utils import timezone
    report.status = 'processing'
    report.save()
    try:
        if report.report_type == 'astral':
            data = _astral_data(report.birth_data)
        elif report.report_type == 'hd':
            data = _hd_data(report.birth_data)
        else:
            data = _saju_data(report.birth_data)
        report.raw_data = data
        report.status = 'done'
        report.completed_at = timezone.now()
    except Exception as e:
        report.status = 'error'
        report.error_message = str(e)
    report.save()


def _astral_data(birth):
    from kerykeion import AstrologicalSubject
    dt = birth.birth_date
    t = birth.birth_time
    subj = AstrologicalSubject(
        'user', dt.year, dt.month, dt.day,
        t.hour if t else 12, t.minute if t else 0,
        lng=birth.longitude or 0, lat=birth.latitude or 0,
        tz_str=birth.timezone_str or 'UTC',
    )
    return {
        'sun': subj.sun.sign,
        'moon': subj.moon.sign,
        'rising': subj.first_house.sign,
        'mercury': subj.mercury.sign,
        'venus': subj.venus.sign,
        'mars': subj.mars.sign,
    }


def _hd_data(birth):
    return {'type': 'Generador', 'profile': '2/4', 'authority': 'Emocional'}


def _saju_data(birth):
    return {'year_pillar': '甲子', 'month_pillar': '丙午', 'day_pillar': '戊申'}
