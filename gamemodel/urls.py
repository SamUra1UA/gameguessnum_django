from django.urls import path
from .views import start_game, play_game, choose_difficulty

urlpatterns = [
    path('start/<str:difficulty>/', start_game, name='start_game'),
    path('choose_difficulty/', choose_difficulty, name='choose_difficulty'),
    path('play/<int:session_id>/', play_game, name='play_game'),
]
