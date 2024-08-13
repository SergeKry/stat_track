from django.urls import path
from .views import GetPlayersView, CreatePlayerView, DetailedStatView, PlayerStatView


urlpatterns = [
    path('get_players/', GetPlayersView.as_view(), name='wg_players'),
    path('create_player/', CreatePlayerView.as_view(), name='create_player'),
    path('detailed_stats/<int:player_id>/', DetailedStatView.as_view(), name='detailed_stats'),
    path('player_stats/<int:player_id>/', PlayerStatView.as_view(), name='player_stats'),
]