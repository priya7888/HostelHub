from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notice_list(request):
    from .models import Notice
    from django.utils import timezone

    today   = timezone.now().date()
    notices = Notice.objects.filter(
        is_active=True
    ).order_by('-posted_at')

    active = []
    for n in notices:
        if n.expires_at:
            if n.expires_at >= today:
                active.append(n)
        else:
            active.append(n)

    urgent    = [n for n in active if n.priority == 'urgent']
    important = [n for n in active if n.priority == 'important']
    normal    = [n for n in active if n.priority == 'normal']

    return render(request, 'notice_board/notices.html', {
        'notices':         active,
        'urgent_count':    len(urgent),
        'important_count': len(important),
        'normal_count':    len(normal),
    })