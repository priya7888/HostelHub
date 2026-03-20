from django.urls import path
from . import views

urlpatterns = [
    path('',                   views.warden_dash,   name='warden_dash'),
    path('scanner/',           views.qr_scanner,    name='warden_qr_scanner'),
    path('scan/<uuid:token>/', views.scan_process,  name='warden_scan_process'),
]