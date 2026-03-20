from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def warden_home(request):
    if not request.user.is_staff:
        return redirect('login')

    from student_profile.models import StudentProfile
    from complaint.models import Complaint
    from emergency_sos.models import SOSAlert
    from outing.models import OutingRequest
    from night_attendance.models import NightAttendance

    profiles      = StudentProfile.objects.filter(
        warden=request.user
    ).select_related('user')
    student_users = [p.user for p in profiles]
    today         = timezone.now().date()

    return render(request, 'warden_home/home.html', {
        'total_students':     profiles.count(),
        'pending_complaints': Complaint.objects.filter(
            student__in=student_users, status='pending').count(),
        'pending_sos':        SOSAlert.objects.filter(
            warden=request.user, status='sent').count(),
        'pending_outings':    OutingRequest.objects.filter(
            student__in=student_users, status='parent_approved').count(),
        'present_today':      NightAttendance.objects.filter(
            student__in=student_users,
            date=today, status='present').count(),
        'absent_today':       NightAttendance.objects.filter(
            student__in=student_users,
            date=today, status='absent').count(),
        'on_leave_today':     NightAttendance.objects.filter(
            student__in=student_users,
            date=today, status='on_leave').count(),
    })