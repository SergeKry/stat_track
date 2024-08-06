from django.urls import path
from .views import GetPlayersView


urlpatterns = [
    path('get_players/', GetPlayersView.as_view(), name='wg_players'),
]