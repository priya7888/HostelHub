from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


@login_required
def warden_mess(request):
    if not request.user.is_staff:
        return redirect('login')

    from mess.models import FoodItem
    from django.db.models import Count

    today = timezone.now().date()

    # Handle add food item
    if request.method == 'POST':
        name      = request.POST.get('name')
        meal_type = request.POST.get('meal_type')
        date_str  = request.POST.get('date')
        try:
            from datetime import date as dt
            date = dt.fromisoformat(date_str) if date_str else today
        except Exception:
            date = today
        FoodItem.objects.create(
            name=name, meal_type=meal_type, date=date
        )
        messages.success(request, f'Food item "{name}" added successfully!')
        return redirect('warden_mess')

    # Get food items with vote counts
    food_items = FoodItem.objects.filter(
        date=today
    ).annotate(
        vote_count=Count('foodvote')
    ).order_by('meal_type', '-vote_count')

    # Total votes today
    total_votes = sum(item.vote_count for item in food_items)

    return render(request, 'warden_mess/mess.html', {
        'food_items':  food_items,
        'today':       today,
        'total_votes': total_votes,
    })


@login_required
def delete_food_item(request, item_id):
    if not request.user.is_staff:
        return redirect('login')
    from mess.models import FoodItem
    item = get_object_or_404(FoodItem, id=item_id)
    item.delete()
    messages.success(request, 'Food item deleted.')
    return redirect('warden_mess')