"""
Defines all endpoints for authentication.
"""
from django.urls import path
from . import views

app_name = 'authenticator'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
]
