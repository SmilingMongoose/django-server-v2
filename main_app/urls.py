
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view_data/', views.view_data, name='view_data'),
    path('health/', views.health_check, name='health_check'),
]
