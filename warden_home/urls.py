from django.urls import path
from . import views

urlpatterns = [
    path('', views.warden_home, name='warden_home'),
]