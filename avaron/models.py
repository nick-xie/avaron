from __future__ import unicode_literals

from django.db import models

class Game(models.Model):
	room_num = models.IntegerField()
	pub_date = models.DateTimeField('date created')
	game_started = models.BooleanField(default=0)
	rules_v = models.CharField(max_length=200, default='[]') #visibility matrix
	rules_t = models.CharField(max_length=200, default='[]') #role mapping index to name
	rules_wl = models.CharField(max_length=200, default='[]') #win lose conditions, i.e. mission details
	def __str__(self):
		return "Room num: " + str(self.room_num)
class Player(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	name = models.CharField(max_length=20)
	role = models.IntegerField()
	seed = models.BigIntegerField(default = 0)
	visible = models.CharField(max_length = 200, default='[]') #the guys this guy can see
	team = models.CharField(max_length=20, default='na') #which team
	msg = models.CharField(max_length=20, default='na') #The message the user sees
	def __str__(self):
		return "Name: " + self.name +" Game: " + str(self.game.room_num) + "Seed: " + str(self.seed)