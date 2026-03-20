from django.urls import path
from . import views

urlpatterns = [
    path('', views.lost_found, name='lost_found'),
    path('new/', views.new_item, name='new_item'),
]