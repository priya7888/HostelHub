from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.warden_outings,       name='warden_outings'),
    path('<int:outing_id>/',         views.warden_outing_detail, name='warden_outing_detail'),
]