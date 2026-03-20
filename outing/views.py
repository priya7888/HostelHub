from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import OutingRequest
import qrcode
import io
import base64
import urllib.parse


def make_whatsapp_url(phone, message):
    """Generate wa.me link — opens WhatsApp directly with message ready"""
    phone = phone.strip().replace(' ', '').replace('-', '').replace('+', '')
    if not phone.startswith('91'):
        phone = '91' + phone  # change 91 to your country code
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded}"


@login_required
def outing_list(request):
    my_requests = OutingRequest.objects.filter(
        student=request.user
    ).order_by('-created_at')
    return render(request, 'outing/outing_list.html', {
        'requests': my_requests
    })


@login_required
def new_outing(request):
    if request.method == 'POST':
        outing = OutingRequest.objects.create(
            student     = request.user,
            reason      = request.POST.get('reason'),
            destination = request.POST.get('destination'),
            out_date    = request.POST.get('out_date'),
            out_time    = request.POST.get('out_time'),
            return_date = request.POST.get('return_date'),
            return_time = request.POST.get('return_time'),
        )

        # Build parent approval link
        parent_link = (
            f"{request.scheme}://{request.get_host()}"
            f"/outing/parent/{outing.parent_token}/"
        )

        # Get parent phone
        parent_phone    = None
        whatsapp_url    = None
        try:
            from student_profile.models import StudentProfile
            profile      = StudentProfile.objects.get(user=request.user)
            parent_phone = profile.parent_phone
        except Exception:
            parent_phone = None

        # Build WhatsApp URL
        if parent_phone:
            msg = (
                f"HostelHub Alert\n\n"
                f"Your child {request.user.first_name or request.user.username} "
                f"has submitted an outing request.\n\n"
                f"Destination: {outing.destination}\n"
                f"Reason: {outing.reason}\n"
                f"Going Out: {outing.out_date} at {outing.out_time}\n"
                f"Returning: {outing.return_date} at {outing.return_time}\n\n"
                f"Click to Approve or Reject:\n{parent_link}"
            )
            whatsapp_url = make_whatsapp_url(parent_phone, msg)

        # Show submitted page with WhatsApp button
        return render(request, 'outing/outing_submitted.html', {
            'outing':       outing,
            'parent_link':  parent_link,
            'whatsapp_url': whatsapp_url,
            'parent_phone': parent_phone,
        })

    return render(request, 'outing/new_outing.html')


# Parent approval — NO login required
def parent_approve(request, token):
    outing = get_object_or_404(OutingRequest, parent_token=token)

    if request.method == 'POST':
        action  = request.POST.get('action')
        remarks = request.POST.get('remarks', '')

        if action == 'approve':
            outing.status             = 'parent_approved'
            outing.parent_approved_at = timezone.now()
            outing.parent_remarks     = remarks
            outing.save()

            # Build warden notification WhatsApp URL
            warden_whatsapp = None
            try:
                from student_profile.models import StudentProfile
                profile = StudentProfile.objects.get(user=outing.student)
                if profile.warden:
                    try:
                        warden_profile = StudentProfile.objects.get(
                            user=profile.warden
                        )
                        if warden_profile.phone:
                            warden_msg = (
                                f"HostelHub - Outing Request\n\n"
                                f"Student {outing.student.first_name or outing.student.username} "
                                f"Room {outing.student.last_name} has parent approval "
                                f"for outing to {outing.destination}.\n\n"
                                f"Please login to approve:\n"
                                f"http://127.0.0.1:8000/outing/warden/"
                            )
                            warden_whatsapp = make_whatsapp_url(
                                warden_profile.phone, warden_msg
                            )
                    except Exception:
                        pass
            except Exception:
                pass

            return render(request, 'outing/parent_response.html', {
                'approved':        True,
                'outing':          outing,
                'warden_whatsapp': warden_whatsapp,
            })

        else:
            outing.status         = 'parent_rejected'
            outing.parent_remarks = remarks
            outing.save()
            return render(request, 'outing/parent_response.html', {
                'approved': False,
                'outing':   outing,
            })

    return render(request, 'outing/parent_approve.html', {'outing': outing})


# Warden approval
@login_required
def warden_approve(request, outing_id):
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

            # Build student notification WhatsApp URL
            student_whatsapp = None
            try:
                from student_profile.models import StudentProfile
                profile = StudentProfile.objects.get(user=outing.student)
                if profile.phone:
                    qr_link     = f"http://127.0.0.1:8000/outing/qr/{outing.id}/"
                    student_msg = (
                        f"HostelHub - Outing Approved!\n\n"
                        f"Your outing to {outing.destination} "
                        f"has been approved by the warden.\n\n"
                        f"View your QR pass:\n{qr_link}\n\n"
                        f"Show this QR at the gate when leaving."
                    )
                    student_whatsapp = make_whatsapp_url(profile.phone, student_msg)
            except Exception:
                pass

            messages.success(request, '✅ Outing approved. QR generated.')
            return render(request, 'outing/warden_approved.html', {
                'outing':           outing,
                'student_whatsapp': student_whatsapp,
            })

        else:
            outing.status         = 'warden_rejected'
            outing.warden_remarks = remarks
            outing.save()

            # Build student rejection WhatsApp URL
            student_whatsapp = None
            try:
                from student_profile.models import StudentProfile
                profile = StudentProfile.objects.get(user=outing.student)
                if profile.phone:
                    reject_msg = (
                        f"HostelHub Alert\n\n"
                        f"Your outing to {outing.destination} "
                        f"has been rejected by the warden.\n\n"
                        f"Remarks: {remarks or 'No remarks'}"
                    )
                    student_whatsapp = make_whatsapp_url(profile.phone, reject_msg)
            except Exception:
                pass

            messages.info(request, 'Outing request rejected.')
            return render(request, 'outing/warden_approved.html', {
                'outing':           outing,
                'student_whatsapp': student_whatsapp,
                'rejected':         True,
            })

    return render(request, 'outing/warden_approve.html', {'outing': outing})


# QR Code view
@login_required
def view_qr(request, outing_id):
    outing = get_object_or_404(
        OutingRequest,
        id=outing_id,
        student=request.user,
        status='warden_approved'
    )
    qr_data = f"http://127.0.0.1:8000/outing/scan/{outing.qr_token}/"
    qr      = qrcode.QRCode(version=1, box_size=8, border=3)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img    = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'outing/view_qr.html', {
        'outing':   outing,
        'qr_image': qr_base64,
    })


# Scan QR — NO login required
def scan_qr(request, token):
    try:
        outing = OutingRequest.objects.get(qr_token=token)
        valid  = outing.status in ('warden_approved', 'checked_out')
        if outing.status == 'warden_approved':
            outing.status         = 'checked_out'
            outing.checked_out_at = timezone.now()
            outing.save()
            action = 'CHECKED OUT'
        elif outing.status == 'checked_out':
            outing.status      = 'returned'
            outing.returned_at = timezone.now()
            outing.save()
            action = 'RETURNED'
        else:
            valid  = False
            action = 'INVALID'
    except OutingRequest.DoesNotExist:
        outing = None
        valid  = False
        action = 'NOT FOUND'

    return render(request, 'outing/scan_result.html', {
        'outing': outing,
        'valid':  valid,
        'action': action,
    })


# Warden list
@login_required
def warden_outing_list(request):
    pending = OutingRequest.objects.filter(
        status='parent_approved'
    ).order_by('-created_at')
    return render(request, 'outing/warden_outing_list.html', {
        'pending': pending
    })