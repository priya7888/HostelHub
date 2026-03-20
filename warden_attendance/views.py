from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User


@login_required
def warden_attendance(request):
    if not request.user.is_staff:
        return redirect('login')

    from student_profile.models import StudentProfile
    from night_attendance.models import NightAttendance

    profiles = StudentProfile.objects.filter(
        warden=request.user
    ).select_related('user').order_by('room_number')

    today = timezone.now().date()

    # Build attendance data for each student
    attendance_data = []
    for sp in profiles:
        record = NightAttendance.objects.filter(
            student=sp.user, date=today
        ).first()
        attendance_data.append({
            'profile': sp,
            'record':  record,
        })

    # Students on leave today
    on_leave = NightAttendance.objects.filter(
        student__in=[sp.user for sp in profiles],
        status='on_leave',
        date=today,
    ).select_related('student')

    # Summary counts
    present_count  = sum(1 for d in attendance_data if d['record'] and d['record'].status == 'present')
    absent_count   = sum(1 for d in attendance_data if d['record'] and d['record'].status == 'absent')
    leave_count    = sum(1 for d in attendance_data if d['record'] and d['record'].status == 'on_leave')
    unmarked_count = sum(1 for d in attendance_data if not d['record'])

    return render(request, 'warden_attendance/attendance.html', {
        'attendance_data': attendance_data,
        'on_leave':        on_leave,
        'today':           today,
        'present_count':   present_count,
        'absent_count':    absent_count,
        'leave_count':     leave_count,
        'unmarked_count':  unmarked_count,
        'total':           len(attendance_data),
    })


@login_required
def mark_attendance(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        from night_attendance.models import NightAttendance
        from datetime import date as dt

        student_id = request.POST.get('student_id')
        status     = request.POST.get('status')
        remarks    = request.POST.get('remarks', '')
        date_str   = request.POST.get('date')

        try:
            date = dt.fromisoformat(date_str) if date_str else timezone.now().date()
        except Exception:
            date = timezone.now().date()

        student = get_object_or_404(User, id=student_id)

        NightAttendance.objects.update_or_create(
            student=student,
            date=date,
            defaults={
                'status':  status,
                'remarks': remarks,
            }
        )
        messages.success(request,
            f'✅ Attendance marked for '
            f'{student.first_name or student.username}.')

    return redirect('warden_attendance')


@login_required
def mark_all_attendance(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        from night_attendance.models import NightAttendance
        from student_profile.models import StudentProfile

        status  = request.POST.get('status', 'present')
        remarks = request.POST.get('remarks', '')
        today   = timezone.now().date()

        profiles = StudentProfile.objects.filter(warden=request.user)
        count    = 0
        for sp in profiles:
            NightAttendance.objects.update_or_create(
                student=sp.user,
                date=today,
                defaults={
                    'status':  status,
                    'remarks': remarks,
                }
            )
            count += 1

        messages.success(request,
            f'✅ Attendance marked for all {count} students as {status}.')

    return redirect('warden_attendance')
# Create your views here.
