"""
Defines all endpoints of the portfolio application.
"""
from django.urls import path
from . import views

app_name = 'portfolio'
urlpatterns = [
    path('', views.index, name='base'),
    path('contact/', views.contact, name='contact'),
]
