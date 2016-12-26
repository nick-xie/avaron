from django.conf.urls import url

from . import views
from .models import Game

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<game_room_num>[0-9]+)/$', views.game_room, name='game_room'),
]