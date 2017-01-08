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
    #url(r'^(?P<player_name>[\w\-]+)/(?P<game_num>[0-9]+)/$', views.make_player), #Makes player, directs to make_game
]