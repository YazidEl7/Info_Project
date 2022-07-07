from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.login, name='Login'),
    path('Home/', views.data, name='Home'),
    path('Logs/', views.logs, name='Logs'),
    path('Users_History/', views.users_history, name='Users_History'),
    path('', include("django.contrib.auth.urls")),
]