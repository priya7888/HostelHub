from django.contrib import admin
from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display  = ['title','student','category','status','created_at']
    list_filter   = ['status','category']
    list_editable = ['status']
    search_fields = ['title','student__username']
# Register your models here.
