from django.urls import path
from . import views

app_name = 'leetquizzer'
urlpatterns = [
    path('', views.MainMenu.as_view(), name='main_menu'),
    path('create/', views.AddProblem.as_view(), name='create')
]