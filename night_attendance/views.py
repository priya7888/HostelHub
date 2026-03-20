from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import NightAttendance

@login_required
def attendance(request):
    # Get all records first — filter BEFORE slice
    all_records = NightAttendance.objects.filter(
        student=request.user
    ).order_by('-date')

    # Count from full queryset BEFORE slicing
    total   = all_records.count()
    present = all_records.filter(status='present').count()
    absent  = all_records.filter(status='absent').count()
    leave   = all_records.filter(status='on_leave').count()
    pct     = round((present / total * 100), 1) if total > 0 else 0

    # Today's record
    today_record = all_records.filter(
        date=timezone.now().date()
    ).first()

    # Slice AFTER all filtering is done
    records = all_records[:30]

    return render(request, 'night_attendance/attendance.html', {
        'records':      records,
        'total':        total,
        'present':      present,
        'absent':       absent,
        'leave':        leave,
        'percentage':   pct,
        'today_record': today_record,
    })