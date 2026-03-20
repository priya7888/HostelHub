from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def warden_complaints(request):
    if not request.user.is_staff:
        return redirect('login')

    from student_profile.models import StudentProfile
    from complaint.models import Complaint

    profiles      = StudentProfile.objects.filter(
        warden=request.user
    ).select_related('user')
    student_users = [p.user for p in profiles]

    # Filter by status
    status_filter = request.GET.get('status', 'all')
    complaints    = Complaint.objects.filter(
        student__in=student_users
    ).order_by('-created_at')

    if status_filter in ('pending', 'ongoing', 'completed'):
        complaints = complaints.filter(status=status_filter)

    pending_count   = Complaint.objects.filter(
        student__in=student_users, status='pending').count()
    ongoing_count   = Complaint.objects.filter(
        student__in=student_users, status='ongoing').count()
    completed_count = Complaint.objects.filter(
        student__in=student_users, status='completed').count()

    return render(request, 'warden_complaints/complaints.html', {
        'complaints':      complaints,
        'status_filter':   status_filter,
        'pending_count':   pending_count,
        'ongoing_count':   ongoing_count,
        'completed_count': completed_count,
    })


@login_required
def warden_complaint_reply(request, complaint_id):
    if not request.user.is_staff:
        return redirect('login')

    from complaint.models import Complaint
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        complaint.status      = request.POST.get('status')
        complaint.admin_reply = request.POST.get('admin_reply', '')
        complaint.save()
        messages.success(request, 'Complaint updated successfully.')
        return redirect('warden_complaints')

    return render(request, 'warden_complaints/complaint_reply.html', {
        'complaint': complaint,
    })