from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'room_number', 'course', 'year', 'phone', 'parent_phone', 'warden']
    search_fields = ['user__username', 'room_number', 'course']
    list_filter   = ['year', 'course']