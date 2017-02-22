from django.conf.urls import url

from . import views
from .models import Game
app_name='avaron'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^(?P<game_room_num>[0-9]+)/$', views.game_room, name='game_room'), #Actual game room, directed from make_player
    url(r'^make_game/$', views.make_game, name='make_game'), #make game, generate room_num
    url(r'^make_player/$', views.make_player, name='make_player'), #makes player and game
    url(r'^(?P<game_num>[0-9]+)/(?P<round_num>[0-9]+)/$', views.start_game, name='start_game'),
    url(r'^GameClosed/', views.game_closed, name='game_closed'),
    url(r'^\d+/GetPlayers/', views.send_players, name='send_players'),
    url(r'^GetGames/', views.send_games, name='send_games'),
]
