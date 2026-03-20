from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def warden_notices(request):
    if not request.user.is_staff:
        return redirect('login')

    from notice_board.models import Notice

    notices = Notice.objects.filter(
        posted_by=request.user
    ).order_by('-posted_at')

    urgent_count    = notices.filter(priority='urgent').count()
    important_count = notices.filter(priority='important').count()
    normal_count    = notices.filter(priority='normal').count()

    return render(request, 'warden_notices/notices.html', {
        'notices':         notices,
        'urgent_count':    urgent_count,
        'important_count': important_count,
        'normal_count':    normal_count,
    })


@login_required
def warden_add_notice(request):
    if not request.user.is_staff:
        return redirect('login')

    from notice_board.models import Notice

    if request.method == 'POST':
        title      = request.POST.get('title')
        content    = request.POST.get('content')
        priority   = request.POST.get('priority', 'normal')
        expires_at = request.POST.get('expires_at') or None

        Notice.objects.create(
            title      = title,
            content    = content,
            priority   = priority,
            posted_by  = request.user,
            expires_at = expires_at,
            is_active  = True,
        )
        messages.success(request, f'Notice "{title}" posted successfully!')
        return redirect('warden_notices')

    return render(request, 'warden_notices/add_notice.html')


@login_required
def warden_delete_notice(request, notice_id):
    if not request.user.is_staff:
        return redirect('login')

    from notice_board.models import Notice
    notice = get_object_or_404(Notice, id=notice_id, posted_by=request.user)
    title  = notice.title
    notice.delete()
    messages.success(request, f'Notice "{title}" deleted.')
    return redirect('warden_notices')