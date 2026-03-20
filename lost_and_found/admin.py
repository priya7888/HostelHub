from django.contrib import admin
from django.contrib import admin
from .models import LostFoundItem

@admin.register(LostFoundItem)
class LostFoundAdmin(admin.ModelAdmin):
    list_display  = ['title','item_type','posted_by','location','is_resolved','posted_at']
    list_filter   = ['item_type','is_resolved']
    list_editable = ['is_resolved']
    search_fields = ['title','posted_by__username']
# Register your models here.
