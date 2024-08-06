from django.urls import path
from .views import GetPlayersView, CreatePlayerView


urlpatterns = [
    path('get_players/', GetPlayersView.as_view(), name='wg_players'),
    path('create_player/', CreatePlayerView.as_view(), name='create_player'),
]