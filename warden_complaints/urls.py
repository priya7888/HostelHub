from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.warden_complaints,      name='warden_complaints'),
    path('<int:complaint_id>/',            views.warden_complaint_reply, name='warden_complaint_reply'),
]