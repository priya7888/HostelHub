from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import FoodItem, FoodVote

@login_required
def food_voting(request):
    today = timezone.now().date()
    food_items = FoodItem.objects.filter(date=today)
    user_votes = FoodVote.objects.filter(
        student=request.user,
        food_item__date=today
    ).values_list('food_item_id', flat=True)

    for item in food_items:
        item.vote_count = FoodVote.objects.filter(food_item=item).count()
        item.voted = item.id in user_votes

    return render(request, 'mess/food_voting.html', {
        'food_items': food_items,
        'today': today,
    })

@login_required
def vote_food(request, food_id):
    if request.method == 'POST':
        food_item = get_object_or_404(FoodItem, id=food_id)
        vote, created = FoodVote.objects.get_or_create(
            student=request.user,
            food_item=food_item
        )
        if not created:
            vote.delete()
            messages.info(request, f'Vote removed for {food_item.name}')
        else:
            messages.success(request, f'Voted for {food_item.name}!')
    return redirect('food_voting')

# Create your views here.
