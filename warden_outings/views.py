from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import urllib.parse


@login_required
def warden_outings(request):
    if not request.user.is_staff:
        return redirect('login')

    from outing.models import OutingRequest
    from student_profile.models import StudentProfile

    # Get warden's assigned students
    profiles      = StudentProfile.objects.filter(
        warden=request.user
    ).select_related('user')
    student_users = [p.user for p in profiles]

    # If warden has no assigned students
    # show ALL parent approved requests
    if not student_users:
        pending = OutingRequest.objects.filter(
            status='parent_approved'
        ).order_by('-created_at')

        all_outings = OutingRequest.objects.all().order_by('-created_at')

        checked_out = OutingRequest.objects.filter(
            status='checked_out'
        ).order_by('-created_at')

    else:
        pending = OutingRequest.objects.filter(
            student__in=student_users,
            status='parent_approved'
        ).order_by('-created_at')

        all_outings = OutingRequest.objects.filter(
            student__in=student_users
        ).order_by('-created_at')

        checked_out = OutingRequest.objects.filter(
            student__in=student_users,
            status='checked_out'
        ).order_by('-created_at')

    return render(request, 'warden_outings/outings.html', {
        'pending':       pending,
        'checked_out':   checked_out,
        'all_outings':   all_outings,
        'pending_count': pending.count(),
    })


@login_required
def warden_outing_detail(request, outing_id):
    if not request.user.is_staff:
        return redirect('login')

    from outing.models import OutingRequest
    outing = get_object_or_404(OutingRequest, id=outing_id)

    if request.method == 'POST':
        action  = request.POST.get('action')
        remarks = request.POST.get('remarks', '')

        if action == 'approve':
            outing.status             = 'warden_approved'
            outing.warden             = request.user
            outing.warden_approved_at = timezone.now()
            outing.warden_remarks     = remarks
            outing.qr_generated       = True
            outing.save()

            # Build WhatsApp notify URL for student
            student_whatsapp = None
            try:
                from student_profile.models import StudentProfile
                profile = StudentProfile.objects.get(user=outing.student)
                if profile.phone:
                    qr_link = f"http://127.0.0.1:8000/outing/qr/{outing.id}/"
                    msg = (
                        f"HostelHub - Outing Approved!\n\n"
                        f"Your outing to {outing.destination} "
                        f"has been approved by the warden.\n\n"
                        f"View your QR pass:\n{qr_link}\n\n"
                        f"Show this QR at the gate when leaving."
                    )
                    phone = profile.phone.strip().replace(
                        ' ', '').replace('-', '').replace('+', '')
                    if not phone.startswith('91'):
                        phone = '91' + phone
                    student_whatsapp = (
                        f"https://wa.me/{phone}?text="
                        f"{urllib.parse.quote(msg)}"
                    )
            except Exception:
                pass

            messages.success(request, '✅ Outing approved! QR pass generated.')
            return render(request, 'warden_outings/outing_approved.html', {
                'outing':           outing,
                'student_whatsapp': student_whatsapp,
            })

        else:
            outing.status         = 'warden_rejected'
            outing.warden         = request.user
            outing.warden_remarks = remarks
            outing.save()

            student_whatsapp = None
            try:
                from student_profile.models import StudentProfile
                profile = StudentProfile.objects.get(user=outing.student)
                if profile.phone:
                    msg = (
                        f"HostelHub Alert\n\n"
                        f"Your outing to {outing.destination} "
                        f"has been rejected by the warden.\n\n"
                        f"Remarks: {remarks or 'No remarks'}"
                    )
                    phone = profile.phone.strip().replace(
                        ' ', '').replace('-', '').replace('+', '')
                    if not phone.startswith('91'):
                        phone = '91' + phone
                    student_whatsapp = (
                        f"https://wa.me/{phone}?text="
                        f"{urllib.parse.quote(msg)}"
                    )
            except Exception:
                pass

            messages.info(request, 'Outing request rejected.')
            return render(request, 'warden_outings/outing_approved.html', {
                'outing':           outing,
                'student_whatsapp': student_whatsapp,
                'rejected':         True,
            })

    return render(request, 'warden_outings/outing_detail.html', {
        'outing': outing,
    })