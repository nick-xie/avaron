from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Game, Player
from django.utils import timezone
from django.urls import reverse

from .forms import NameForm

def index(request):
    latest_game_list = Game.objects.order_by('-pub_date')[:5]
    template = loader.get_template('avaron/index.html')
    context = {
        'latest_game_list': latest_game_list,
    }
    return HttpResponse(template.render(context, request))

def game_room(request, game_room_num):
	return HttpResponse("You're in the room for game %s" % game_room_num)

# def make_player(request, name):
# 	g=Game.objects.create(room_num=3,pub_date=timezone.now())
# 	new_player=Player.objects.create(name="Tim",game=g,role=1)
# 	new_player.save()
# 	return HttpResponse("hi")