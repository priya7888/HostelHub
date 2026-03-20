from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def warden_dash(request):
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

    return render(request, 'warden_dash/dashboard.html', {
        'total_students':     profiles.count(),
        'pending_complaints': Complaint.objects.filter(
            student__in=student_users, status='pending').count(),
        'pending_sos':        SOSAlert.objects.filter(
            warden=request.user, status='sent').count(),
        'pending_outings':    OutingRequest.objects.filter(
            student__in=student_users,
            status='parent_approved').count(),
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


@login_required
def qr_scanner(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'warden_dash/qr_scanner.html')


@login_required
def scan_process(request, token):
    if not request.user.is_staff:
        return redirect('login')

    import urllib.parse
    from outing.models import OutingRequest

    try:
        outing       = OutingRequest.objects.get(qr_token=token)
        student_name = (
            outing.student.first_name or outing.student.username
        )

        # Check student belongs to this warden
        belongs = False
        try:
            from student_profile.models import StudentProfile
            profile = StudentProfile.objects.get(user=outing.student)
            belongs = (profile.warden == request.user)
        except Exception:
            belongs = False

        if not belongs:
            return render(request, 'warden_dash/scan_result.html', {
                'valid':           False,
                'action':          'NOT YOUR STUDENT',
                'outing':          outing,
                'parent_whatsapp': None,
            })

        parent_whatsapp = None
        valid           = outing.status in (
            'warden_approved', 'checked_out'
        )

        # ── CHECKOUT ──────────────────────────────
        if outing.status == 'warden_approved':
            outing.status         = 'checked_out'
            outing.checked_out_at = timezone.now()
            outing.save()
            action = 'CHECKED OUT'

            # Mark attendance ON LEAVE
            try:
                from night_attendance.models import NightAttendance
                NightAttendance.objects.update_or_create(
                    student=outing.student,
                    date=timezone.now().date(),
                    defaults={
                        'status':  'on_leave',
                        'remarks': f'Outing to {outing.destination}',
                    }
                )
            except Exception:
                pass

            # WhatsApp to parent
            try:
                from student_profile.models import StudentProfile
                profile = StudentProfile.objects.get(user=outing.student)
                if profile.parent_phone:
                    msg = (
                        f"HostelHub Alert\n\n"
                        f"Your child {student_name} has left "
                        f"the hostel.\n\n"
                        f"Destination: {outing.destination}\n"
                        f"Time: "
                        f"{timezone.now().strftime('%d %b %Y %H:%M')}\n"
                        f"Expected Return: {outing.return_date} "
                        f"at {outing.return_time}\n\n"
                        f"- HostelHub System"
                    )
                    phone = profile.parent_phone.strip().replace(
                        ' ','').replace('-','').replace('+','')
                    if not phone.startswith('91'):
                        phone = '91' + phone
                    parent_whatsapp = (
                        f"https://wa.me/{phone}?text="
                        f"{urllib.parse.quote(msg)}"
                    )
            except Exception:
                pass

        # ── RETURN ────────────────────────────────
        elif outing.status == 'checked_out':
            outing.status      = 'returned'
            outing.returned_at = timezone.now()
            outing.save()
            action = 'RETURNED'

            # Mark attendance PRESENT
            try:
                from night_attendance.models import NightAttendance
                NightAttendance.objects.update_or_create(
                    student=outing.student,
                    date=timezone.now().date(),
                    defaults={
                        'status':  'present',
                        'remarks': f'Returned from {outing.destination}',
                    }
                )
            except Exception:
                pass

            # WhatsApp to parent
            try:
                from student_profile.models import StudentProfile
                profile = StudentProfile.objects.get(user=outing.student)
                if profile.parent_phone:
                    msg = (
                        f"HostelHub Alert\n\n"
                        f"Your child {student_name} has safely "
                        f"returned to the hostel.\n\n"
                        f"Return Time: "
                        f"{timezone.now().strftime('%d %b %Y %H:%M')}\n\n"
                        f"- HostelHub System"
                    )
                    phone = profile.parent_phone.strip().replace(
                        ' ','').replace('-','').replace('+','')
                    if not phone.startswith('91'):
                        phone = '91' + phone
                    parent_whatsapp = (
                        f"https://wa.me/{phone}?text="
                        f"{urllib.parse.quote(msg)}"
                    )
            except Exception:
                pass

        # ── ALREADY USED ──────────────────────────
        else:
            valid  = False
            action = 'INVALID — QR Already Used'

    except OutingRequest.DoesNotExist:
        outing          = None
        valid           = False
        action          = 'NOT FOUND'
        parent_whatsapp = None

    return render(request, 'warden_dash/scan_result.html', {
        'outing':          outing,
        'valid':           valid,
        'action':          action,
        'parent_whatsapp': parent_whatsapp,
    })