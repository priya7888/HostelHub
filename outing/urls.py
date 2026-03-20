from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.outing_list,       name='outing_list'),
    path('new/',                      views.new_outing,        name='new_outing'),
    path('parent/<uuid:token>/',      views.parent_approve,    name='parent_approve'),
    path('warden/',                   views.warden_outing_list,name='warden_outing_list'),
    path('warden/<int:outing_id>/',   views.warden_approve,    name='warden_approve'),
    path('qr/<int:outing_id>/',       views.view_qr,           name='view_qr'),
    path('scan/<uuid:token>/',        views.scan_qr,           name='scan_qr'),
]