from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_voting, name='food_voting'),
    path('vote/<int:food_id>/', views.vote_food, name='vote_food'),
]