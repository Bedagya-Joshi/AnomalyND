from django.contrib import admin
from django.urls import path
from NAD import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('reports/', views.reports_view, name='reports'),
    path('notifications/', views.notifications_view, name='notifications'),
]
