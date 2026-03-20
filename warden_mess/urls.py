from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.warden_mess,       name='warden_mess'),
    path('delete/<int:item_id>/',views.delete_food_item, name='warden_delete_food'),
]