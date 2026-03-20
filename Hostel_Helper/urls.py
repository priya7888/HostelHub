"""
URL configuration for Hostel_Helper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('student/', include('student_dashboard.urls')),
    path('dashboard/', include('dashboard1.urls')),
    path('mess/', include('mess.urls')),
    path('complaints/', include('complaint.urls')),
    path('lost-found/', include('lost_and_found.urls')),
    path('notices/', include('notice_board.urls')),
    path('attendance/', include('night_attendance.urls')),
    path('sos/', include('emergency_sos.urls')),
    path('outing/', include('outing.urls')),
     path('warden/',         include('warden_home.urls')),
    path('warden/dash/',    include('warden_dash.urls')),
    path('warden/mess/',    include('warden_mess.urls')),
    path('warden/complaints/', include('warden_complaints.urls')),
    path('warden/lost-found/', include('warden_lost_found.urls')),
    path('warden/notices/', include('warden_notices.urls')),
    path('warden/attendance/', include('warden_attendance.urls')),
    path('warden/outings/', include('warden_outings.urls')),
    path('warden/sos/',     include('warden_sos.urls')),
]