from django.urls import path
from . import views

app_name = 'leetquizzer'
urlpatterns = [
    path('', views.MainMenu.as_view(), name='main_menu'),
    path('create/', views.AddProblem.as_view(), name='create'),
    path('add_topic/', views.AddTopic.as_view(), name='add_topic'),
    path('add_difficulty/', views.AddDifficulty.as_view(), name='add_difficulty'),
    path('<str:problem_id>/problem/', views.ProblemMenu.as_view(), name='problem_menu'),
]