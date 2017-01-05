from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Game, Player
from django.utils import timezone
from django.urls import reverse
from .forms import PlayerForm
from django.shortcuts import get_object_or_404


def index(request):
    latest_game_list = Game.objects.order_by('-pub_date')
    template = loader.get_template('avaron/index.html')
    context = {
        'latest_game_list': latest_game_list,
    }
    return HttpResponse(template.render(context, request))

def game_room(request, game_room_num):
	g=Game.objects.filter(room_num=game_room_num) #Game ID =/= Game room num, find the game that has the same room num
	players = Player.objects.filter(game=g) #Using g, we can find the players in the game properly since game compares id's
	template = loader.get_template('avaron/gameroom.html')
	context = {
		'players': players,
		'game': game_room_num, #'name' is the name of the variable that can be used in the html file through {{ name }}
	}
	return HttpResponse(template.render(context,request))

def make_player(request):
	if request.method=='POST':
		form = PlayerForm(request.POST)
		#gets the values submitted in the template
		player_name=request.POST.get("player_field", None)
		game_num=request.POST.get("game_field", None)
		gamelist = Game.objects.filter(room_num=game_num) #for more help, seek Django QuerySet API
		if not gamelist: #game doesn't exist, create it
			g=Game.objects.create(room_num=int(game_num),pub_date=timezone.now())
			g.save() #creates game from game num
		else:
			g=get_object_or_404(gamelist) #isolates the already existing game
		p=Player.objects.create(game=g,name=player_name,role=0)
		p.save() #creates players with game among other things
	else:
		form = PlayerForm()
	return HttpResponseRedirect('/avaron/%s' % game_num) #Redirects to make game
#now obselete
def make_game(request, game_num):
	g=Game.objects.create(room_num=int(game_num),pub_date=timezone.now())
	g.save()
	return HttpResponseRedirect('/avaron/%s/' % game_num) #Redirects to game room

# def make_player(request, name):
# 	g=Game.objects.create(room_num=3,pub_date=timezone.now())
# 	new_player=Player.objects.create(name="Tim",game=g,role=1)
# 	new_player.save()
# 	return HttpResponse("hi")