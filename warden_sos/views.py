from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import urllib.parse


@login_required
def warden_sos(request):
    if not request.user.is_staff:
        return redirect('login')

    from emergency_sos.models import SOSAlert

    # Handle resolve
    if request.method == 'POST':
        alert_id = request.POST.get('alert_id')
        alert    = get_object_or_404(SOSAlert, id=alert_id)
        alert.status      = 'resolved'
        alert.resolved_at = timezone.now()
        alert.save()
        messages.success(request, '✅ SOS Alert marked as resolved.')
        return redirect('warden_sos')

    # Get all alerts for this warden
    active_alerts = SOSAlert.objects.filter(
        warden=request.user,
        status='sent'
    ).order_by('-sent_at')

    acknowledged = SOSAlert.objects.filter(
        warden=request.user,
        status='acknowledged'
    ).order_by('-sent_at')

    resolved = SOSAlert.objects.filter(
        warden=request.user,
        status='resolved'
    ).order_by('-sent_at')[:10]

    # Build WhatsApp reply URLs for each active alert
    alerts_with_wa = []
    for alert in active_alerts:
        wa_url = None
        try:
            from student_profile.models import StudentProfile
            profile = StudentProfile.objects.get(user=alert.student)
            if profile.phone:
                msg = (
                    f"HostelHub - SOS Response\n\n"
                    f"I received your emergency alert. "
                    f"I am on my way. Please stay calm.\n\n"
                    f"- Warden {request.user.first_name or request.user.username}"
                )
                phone = profile.phone.strip().replace(
                    ' ', '').replace('-', '').replace('+', '')
                if not phone.startswith('91'):
                    phone = '91' + phone
                wa_url = (
                    f"https://wa.me/{phone}?text="
                    f"{urllib.parse.quote(msg)}"
                )
        except Exception:
            pass
        alerts_with_wa.append({
            'alert': alert,
            'wa_url': wa_url,
        })

    return render(request, 'warden_sos/sos.html', {
        'alerts_with_wa': alerts_with_wa,
        'acknowledged':   acknowledged,
        'resolved':       resolved,
        'active_count':   active_alerts.count(),
    })


@login_required
def acknowledge_sos(request, alert_id):
    if not request.user.is_staff:
        return redirect('login')

    from emergency_sos.models import SOSAlert
    alert = get_object_or_404(SOSAlert, id=alert_id)
    alert.status = 'acknowledged'
    alert.save()
    messages.success(request, '🔔 SOS Alert acknowledged.')
    return redirect('warden_sos')