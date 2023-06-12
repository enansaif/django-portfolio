from django.urls import path
from . import views

app_name = 'portfolio'
urlpatterns = [
    path('', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('resume/', views.resume, name='resume'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
]