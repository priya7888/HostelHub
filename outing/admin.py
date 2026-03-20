from django.contrib import admin
from .models import OutingRequest

@admin.register(OutingRequest)
class OutingRequestAdmin(admin.ModelAdmin):
    list_display  = ['student','destination','out_date','status','created_at']
    list_filter   = ['status','out_date']
    list_editable = ['status']
    search_fields = ['student__username','destination']
    readonly_fields = ['parent_token','qr_token','created_at']