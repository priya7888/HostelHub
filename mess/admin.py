from django.contrib import admin
from django.contrib import admin
from .models import FoodItem, FoodVote

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display  = ['name','meal_type','date']
    list_filter   = ['meal_type','date']
    search_fields = ['name']

@admin.register(FoodVote)
class FoodVoteAdmin(admin.ModelAdmin):
    list_display = ['student','food_item','voted_at']
# Register your models here.
