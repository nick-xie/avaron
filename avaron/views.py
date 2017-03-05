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
	else: #send user to bad join screen
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
		if not gamelist: #game doesn't exist, stop joining
			data={'gameNumber':-1} #gameNumber = -1 indicates game doesn't exist
			return HttpResponse(json.dumps(data),content_type='application/json')
		g=get_object_or_404(gamelist) #isolates the already existing game
		if int(g.game_started)==0: #game hasn't started
			seed=randint(1,90001) #seed will be used for randomization
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
	if (request.method=='POST' and request.is_ajax()):
		form = PlayerForm(request.POST)
		#gets the name submitted in the template
		player_name=request.POST.get('pname')
		gamelist = Game.objects.all() #gets all existing games
		roomnums=[]
		for game in gamelist:
			roomnums.append(int(game.room_num)) #create an array of all existing game_num's
		new_num=1+max(roomnums) #simply add 1 to largest current game_num and this is our new game_num
		visibilityR=[
		[[-1,-1,0,0,0],[-1,-1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]],
		[[-1,-1,0,0,0,0],[-1,-1,0,0,0,0],[0,-1,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]],
		[[-1,-1,-1,0,0,0,0],[-1,-1,-1,0,0,0,0],[-1,-1,-1,0,0,0,0],[0,-1,-1,1,0,0,0],[0,0,-1,-1,1,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]],
		[[-1,-1,-1,0,0,0,0,0],[-1,-1,-1,0,0,0,0,0],[-1,-1,-1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]],
		[[-1,-1,-1,0,0,0,0,0,0],[-1,-1,-1,0,0,0,0,0,0],[-1,-1,-1,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]]
		]
		RoleNames=[
		["Bad Guy1","Bad Guy2","Good Guy 3","Good Guy 4","Good Guy 5"],
		["Known bad guy - you are hidden so far from good guys","Bad Guy - one good guy sees you","Smart Good guy - You see one bad","Good Guy 1","Good Guy 2","Good Guy 3"],
		["Mordrid","Assassin","Morgana","Merlin","Percival","Dumb Blue 1","Dumb Blue 2"],
		["Bad Guy","Bad Guy","Bad Guy","Good Guy","Good Guy","Good Guy","Good Guy","Good Guy"],
		["Bad Guy","Bad Guy","Bad Guy","Good Guy","Good Guy","Good Guy","Good Guy","Good Guy","Good Guy"]
		]
		g=Game.objects.create(room_num=new_num,pub_date=timezone.now(),
			game_started=0,rules_v=visibilityR,rules_t=RoleNames)
		g.save() #creates game
		seed=randint(1,90001)
		p=Player.objects.create(game=g,name=player_name,role=0,seed=seed)
		p.save() #creates player
		request.session['id']=seed #to identify player
		request.session['gameEntry']=int(new_num)
		data={'gameNumber':new_num}
	else:
		print("ohno")
		form = PlayerForm()
	return HttpResponse(json.dumps(data),content_type='application/json')
	#return HttpResponseRedirect('/avaron/%s' % new_num) #Redirects to game room
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
#send a list of numbers of all open games as a json to js file
def send_games(request):
	if (request.method=='POST' and request.is_ajax()):
		g=Game.objects.filter(game_started=0) #all open games
		glist=[]
		for game in g:
			glist.append(game.room_num)
		data={'games':glist}
		return HttpResponse(json.dumps(data),content_type='application/json')
#in game
def start_game(request, game_num, round_num):
	g=Game.objects.filter(room_num=game_num).first()
	players = Player.objects.filter(game=g).order_by('seed') #players in game, sorted
	if int(g.game_started)==0: #first person to press start game
	# ------ ASSIGN ROLES ---------
		visibR=eval(str(g.rules_v)) #come back to this one day
		NameR=eval(str(g.rules_t))
		for i in range(0,len(visibR)): #choose appropriate game rules based off player count
			if(players.count()==len(visibR[i])):
				visibR=visibR[i]
				NameRules=NameR[i]
				break
		i=0
		for player in players: #assign roles(num) and team to players
			player.role=i #player is number i
			player.team=visibR[i][i]
			player.visible=visibR[i]
			player.save()
			i=i+1
		for player in players: # Write player msg to display to the user.
			VisibNames=[]
			for j in range(0,len(player.visible)):
				#find the name
				if player.visible[j]==-1 and j!=player.role:
					namedP = Player.objects.filter(role=j,game=g)
					VisibNames.append(namedP.first().name)
			random.shuffle(VisibNames)
			player.msg=VisibNames
			player.save()
		g.game_started=1
		g.rules_t=NameRules
		g.save()
	# ------------------------------
	our_seed = request.session['id']
	your_guy=Player.objects.filter(seed=our_seed).first()
	NameR=eval(str(g.rules_t))
	YourRole = NameR[your_guy.role]
	formatVis=""
	for i in eval(str(your_guy.msg)):
		formatVis=formatVis+str(i)+"\n"
	template = loader.get_template('avaron/ingame.html')
	context = {
		'players': players,
		'your_guy': your_guy,
		'game': game_num,
		'round_num': round_num,
		'visible': formatVis,
		'role_name': YourRole,
	}
	return HttpResponse(template.render(context,request))
