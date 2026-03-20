from django.contrib import admin
from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display  = ['title','priority','posted_by','posted_at','expires_at','is_active']
    list_filter   = ['priority','is_active']
    list_editable = ['priority','is_active']
    search_fields = ['title','content']
# Register your models here.
