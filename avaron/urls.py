from django.conf.urls import url

from . import views
from .models import Game

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<game_room_num>[0-9]+)/$', views.game_room), #Actual game room, directed from game being made
    url(r'^game/(?P<game_num>[0-9]+)/$', views.make_game), #Makes game, directed from make_player
    url(r'^(?P<player_name>[\w\-]+)/(?P<game_num>[0-9]+)/$', views.make_player), #Makes player, directs to make_game
]