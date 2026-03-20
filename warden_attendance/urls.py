from django.urls import path
from . import views

urlpatterns = [
    path('',        views.warden_attendance,  name='warden_attendance'),
    path('mark/',   views.mark_attendance,    name='warden_mark_attendance'),
    path('markall/',views.mark_all_attendance,name='warden_mark_all'),
]