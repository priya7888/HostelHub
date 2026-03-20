from django.contrib import admin
from django.contrib import admin
from .models import SOSAlert

@admin.register(SOSAlert)
class SOSAlertAdmin(admin.ModelAdmin):
    list_display    = ['student','status','sent_at','location','resolved_at']
    list_filter     = ['status']
    list_editable   = ['status']
    search_fields   = ['student__username']
    readonly_fields = ['sent_at']
# Register your models here.
