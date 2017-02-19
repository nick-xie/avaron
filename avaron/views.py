from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Game, Player
from django.utils import timezone
from django.urls import reverse
from .forms import PlayerForm
from django.shortcuts import get_object_or_404
from random import randint
import random
import math
import json
#TODO
#start game function, game logic to assign roles
#leave game
#delete game when all leave

def index(request):
    latest_game_list = Game.objects.filter(game_started=0).order_by('-pub_date')
    template = loader.get_template('avaron/index.html')
    context = {
        'latest_game_list': latest_game_list,
    }
    request.session['gameEntry']="na"
    return HttpResponse(template.render(context, request))

def game_closed(request):
    template = loader.get_template('avaron/gameClosed.html')
    context={}
    return HttpResponse(template.render(context, request))

def game_room(request, game_room_num):
	test=request.session['gameEntry']
	if test==int(game_room_num): #properly entered game (not typing in url)
		g=Game.objects.filter(room_num=game_room_num) #Game ID =/= Game room num, find the game that has the same room num
		players = Player.objects.filter(game=g) #Using g, we can find the players in the game properly since game compares id's
		template = loader.get_template('avaron/gameroom.html')
		context = {
			'players': players,
			'game': game_room_num, #'name' is the name of the variable that can be used in the html file through {{ name }}
		}
		return HttpResponse(template.render(context,request))
	else: #send user to badjoing screen
		template = loader.get_template('avaron/badjoin.html')
		context = {}
		return HttpResponse(template.render(context, request))
#join game
def make_player(request):
	if (request.method=='POST' and request.is_ajax()):
		form = PlayerForm(request.POST)
		#gets the values submitted in the template
		player_name=request.POST.get('pname')
		game_num=request.POST.get('num')
		gamelist = Game.objects.filter(room_num=game_num) #for more help, seek Django QuerySet API
		if not gamelist: #game doesn't exist, create it
			g=Game.objects.create(room_num=int(game_num),pub_date=timezone.now(),game_started=0)
			g.save() #creates game from game num
		else:
			g=get_object_or_404(gamelist) #isolates the already existing game
		if int(g.game_started)==0: #game hasn't started
			seed=randint(1,9001) #seed will determine role
			p=Player.objects.create(game=g,name=player_name,role=0,seed=seed)
			p.save() #creates players with game among other things
			request.session['id']=seed #to identify player
			request.session['gameEntry']=int(game_num) #Adds a cookie/session to indicate a legit entry
			data={'gameNumber':game_num}
			return HttpResponse(json.dumps(data),content_type='application/json')
			# return HttpResponseRedirect('/avaron/%s' % game_num) #Redirects to game room
		else: #game has already started, send to sorry page
			data={'gameNumber':0}
			return HttpResponse(json.dumps(data),content_type='application/json')
	else:
		form = PlayerForm()
		return HttpResponseRedirect('/avaron/%s' % game_num) #Redirects to game room

#create game
def make_game(request):
	if request.method=='POST':
		form = PlayerForm(request.POST)
		#gets the name submitted in the template
		player_name=request.POST.get("player_field", None)
		gamelist = Game.objects.all() #gets all existing games
		roomnums=[]
		for game in gamelist:
			roomnums.append(int(game.room_num)) #create an array of all existing game_num's
		new_num=1+max(roomnums) #simply add 1 to largest current game_num and this is our new game_num
		visibilityR=[[[1,2],[2,1],[3,1,2],[4],[5]],[[1,2],[2,1],[3,1],[4],[5],[6]],[[1,2,3],[2,1,3],[3,1,2],[4,2,5],[5,2,3],[6],[7]]]
		teamR=[[[1,2],[3,4,5]],[[1,2],[3,4,5,6]],[[1,2,3],[4,5,6,7]]]
		g=Game.objects.create(room_num=new_num,pub_date=timezone.now(),
			game_started=0,rules_v=visibilityR,rules_t=teamR)
		g.save() #creates game
		seed=randint(1,9001)
		p=Player.objects.create(game=g,name=player_name,role=0,seed=seed)
		p.save() #creates player
		request.session['id']=seed #to identify player
		request.session['gameEntry']=int(new_num)
	else:
		form = PlayerForm()
	return HttpResponseRedirect('/avaron/%s' % new_num) #Redirects to game room
#send a list of players as a json to js file
def send_players(request):
	if (request.method=='POST' and request.is_ajax()):
		game_num=request.POST.get('num')
		g=Game.objects.filter(room_num=int(game_num))
		players = Player.objects.filter(game=g) #players in game
		plist=[]
		for player in players:
			plist.append(player.name)
		data={'players':plist}
		return HttpResponse(json.dumps(data),content_type='application/json')
#in game
def start_game(request, game_num, round_num):
	g=Game.objects.filter(room_num=game_num).first()
	players = Player.objects.filter(game=g).order_by('seed') #players in game, sorted
	if int(g.game_started)==0: #first person to press start game
		visibR=eval(str(g.rules_v)) #come back to this one day
		teamR=eval(str(g.rules_t))
		for i in range(0,len(visibR)): #choose appropriate game based off player count
			if(players.count()==len(visibR[i])):
				visibR=visibR[i]
				teamR=teamR[i]
				break
		i=1#counter
		for player in players: #assign roles(num) and team to players
			player.role=i #player is number i
			for tc in range(0,len(teamR)): #assigns team
				if (i in teamR[tc]):
					player.team=tc
					break
			vc=0
			for vc in range(0, len(visibR)): #give visibility rules to player by vc
				if (visibR[vc][0]==i):
					player.visible=visibR[vc] #convert back to string
			i=i+1
			player.save()
		for player in players: #replace vc with names
			newVisib=[]
			for i in range(0,len(player.visible)):
				#find the name
				namedP = Player.objects.filter(role=player.visible[i],game=g)
				newVisib.append(namedP.first().name)
			random.shuffle(newVisib)
			player.visible=newVisib
			player.save()
		g.game_started=1
		g.save()
	our_seed = request.session['id']
	your_guy=Player.objects.filter(seed=our_seed).first()
	formatVis=""
	for i in eval(str(your_guy.visible)):
		formatVis=formatVis+str(i)+"\n"
	template = loader.get_template('avaron/ingame.html')
	context = {
		'players': players,
		'your_guy': your_guy,
		'game': game_num,
		'round_num': round_num,
		'visible': formatVis,
	}
	return HttpResponse(template.render(context,request))
