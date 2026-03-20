from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.warden_notices,       name='warden_notices'),
    path('add/',                      views.warden_add_notice,    name='warden_add_notice'),
    path('delete/<int:notice_id>/',   views.warden_delete_notice, name='warden_delete_notice'),
]