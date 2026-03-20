from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.warden_sos,        name='warden_sos'),
    path('ack/<int:alert_id>/',     views.acknowledge_sos,   name='warden_ack_sos'),
]