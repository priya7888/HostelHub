from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint

@login_required
def complaints(request):
    my_complaints = Complaint.objects.filter(
        student=request.user
    ).order_by('-created_at')
    return render(request, 'complaint/complaints.html',
                  {'complaints': my_complaints})

@login_required
def new_complaint(request):
    if request.method == 'POST':
        title       = request.POST.get('title')
        category    = request.POST.get('category')
        description = request.POST.get('description')
        Complaint.objects.create(
            student=request.user,
            title=title,
            category=category,
            description=description
        )
        messages.success(request, 'Complaint submitted successfully!')
        return redirect('complaints')
    return render(request, 'complaint/new_complaint.html')