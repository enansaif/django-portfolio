"""
Defines all endpoints for authentication.
"""
from django.urls import path
from . import views

app_name = 'authenticator'
urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
