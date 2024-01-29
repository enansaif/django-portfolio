from django.urls import path
from . import views

app_name = 'chess_app'
urlpatterns = [
    path('', views.home),
    path('play_step/', views.play_step, name='play_step'),
    path('reset_game/', views.reset_game, name='reset_game'),
]