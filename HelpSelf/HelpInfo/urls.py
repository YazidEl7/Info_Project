from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('Home/', views.data, name='Home'),
]