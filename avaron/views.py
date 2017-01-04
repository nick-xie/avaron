from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Game, Player
from django.utils import timezone
from django.urls import reverse
from .forms import PlayerForm


def index(request):
    latest_game_list = Game.objects.order_by('-pub_date')[:5]
    template = loader.get_template('avaron/index.html')
    context = {
        'latest_game_list': latest_game_list,
    }
    return HttpResponse(template.render(context, request))

def game_room(request, game_room_num):
	return HttpResponse("You're in the room for game %s" % game_room_num)

def make_player(request, player_name, game_num):
	if request.method=='POST':
		form = PlayerForm(request.POST)
		if form.is_valid():
			p=Game.objects.create(game=game_num,name=player_name,role=0)
			p.save()
	else:
		form = PlayerForm()
	return HttpResponseRedirect('/avaron/game/%s' % game_num) #Redirects to make game
def make_game(request, game_num):
	g=Game.objects.create(room_num=int(game_num),pub_date=timezone.now())
	g.save()
	return HttpResponseRedirect('/avaron/%s/' % game_num) #Redirects to game room

# def make_player(request, name):
# 	g=Game.objects.create(room_num=3,pub_date=timezone.now())
# 	new_player=Player.objects.create(name="Tim",game=g,role=1)
# 	new_player.save()
# 	return HttpResponse("hi")