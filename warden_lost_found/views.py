from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def warden_lost_found(request):
    if not request.user.is_staff:
        return redirect('login')

    from lost_and_found.models import LostFoundItem

    # Handle resolve
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item    = get_object_or_404(LostFoundItem, id=item_id)
        item.is_resolved = True
        item.save()
        messages.success(request, f'"{item.title}" marked as resolved.')
        return redirect('warden_lost_found')

    # Filter
    filter_type = request.GET.get('type', 'all')
    items = LostFoundItem.objects.filter(
        is_resolved=False
    ).order_by('-posted_at')

    if filter_type in ('lost', 'found'):
        items = items.filter(item_type=filter_type)

    # Resolved items
    resolved = LostFoundItem.objects.filter(
        is_resolved=True
    ).order_by('-posted_at')[:10]

    lost_count  = LostFoundItem.objects.filter(
        is_resolved=False, item_type='lost').count()
    found_count = LostFoundItem.objects.filter(
        is_resolved=False, item_type='found').count()

    return render(request, 'warden_lost_found/lost_found.html', {
        'items':       items,
        'resolved':    resolved,
        'filter_type': filter_type,
        'lost_count':  lost_count,
        'found_count': found_count,
    })
# Create your views here.
