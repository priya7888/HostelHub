from django.urls import path
from . import views

urlpatterns = [
    path('', views.warden_lost_found, name='warden_lost_found'),
]