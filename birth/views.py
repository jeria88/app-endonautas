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
            gender=request.POST.get('gender', ''),
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
    from .calculators import calculate_astral_chart, calculate_hd_chart, calculate_saju_chart

    report.status = 'processing'
    report.save()
    try:
        bp = report.birth_data
        if report.report_type == 'astral':
            data = calculate_astral_chart(bp)
        elif report.report_type == 'hd':
            data = calculate_hd_chart(bp)
        else:
            data = calculate_saju_chart(bp)
        report.raw_data = data
        report.status = 'done'
        report.completed_at = timezone.now()
    except Exception as e:
        report.status = 'error'
        report.error_message = str(e)
    report.save()
