"""The module contains the routing of the requests within the application"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('action', views.action, name="action"),
]
