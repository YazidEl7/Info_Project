from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.m, name='m'),
    path('Home/', views.data, name='Home'),
    path('Logs/', views.logs, name='Logs'),
    path('Users_History/', views.users_history, name='Users_History'),
    path('U_H/<str:user>/', views.u_h, name='U_H'),
    path('C_H/<str:comp>/', views.c_h, name='C_H'),
    path('between/', views.between, name='between'),
    path('', include("django.contrib.auth.urls")),
]
