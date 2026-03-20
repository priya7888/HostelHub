from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Notice

@login_required
def notices(request):
    today = timezone.now().date()
    all_notices = Notice.objects.filter(
        is_active=True
    ).exclude(
        expires_at__lt=today
    ).order_by('-posted_at')
    return render(request, 'notice_board/notices.html', {
        'notices': all_notices,
    })