from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SOSAlert

@login_required
def send_sos(request):
    if request.method == 'POST':
        message  = request.POST.get('message', 'Emergency! Please help.')
        location = request.POST.get('location', '')

        # Get student's assigned warden
        warden = None
        try:
            from student_profile.models import StudentProfile
            profile = StudentProfile.objects.get(user=request.user)
            warden  = profile.warden
        except Exception:
            warden = None

        SOSAlert.objects.create(
            student=request.user,
            message=message,
            location=location,
            warden=warden,
        )
        messages.success(request, '🚨 SOS Alert sent! Help is on the way.')
        return redirect('send_sos')

    recent_alerts = SOSAlert.objects.filter(
        student=request.user
    ).order_by('-sent_at')[:5]

    return render(request, 'emergency_sos/sos.html', {
        'recent_alerts': recent_alerts,
    })