from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Home/', views.data, name='Home'),
    path('Logs/', views.logs, name='Logs'),
    path('Users_History/', views.users_history, name='Users_History'),
]