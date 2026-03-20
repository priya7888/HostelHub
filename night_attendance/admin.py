from django.contrib import admin
from django.contrib import admin
from .models import NightAttendance

@admin.register(NightAttendance)
class NightAttendanceAdmin(admin.ModelAdmin):
    list_display   = ['student','date','status','remarks']
    list_filter    = ['status','date']
    list_editable  = ['status']
    search_fields  = ['student__username']
    date_hierarchy = 'date'
# Register your models here.
