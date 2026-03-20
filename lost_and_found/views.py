from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LostFoundItem

@login_required
def lost_found(request):
    filter_type = request.GET.get('type', 'all')
    items = LostFoundItem.objects.filter(
        is_resolved=False
    ).order_by('-posted_at')
    if filter_type in ('lost', 'found'):
        items = items.filter(item_type=filter_type)
    return render(request, 'lost_and_found/lost_found.html', {
        'items': items,
        'filter_type': filter_type,
    })

@login_required
def new_item(request):
    if request.method == 'POST':
        item_type   = request.POST.get('item_type')
        title       = request.POST.get('title')
        description = request.POST.get('description')
        location    = request.POST.get('location')
        LostFoundItem.objects.create(
            posted_by=request.user,
            item_type=item_type,
            title=title,
            description=description,
            location=location,
        )
        messages.success(request, 'Item posted successfully!')
        return redirect('lost_found')
    return render(request, 'lost_and_found/new_item.html')