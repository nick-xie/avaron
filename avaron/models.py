from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Game(models.Model):
	room_num = models.IntegerField()
	pub_date = models.DateTimeField('date created')
	def __str__(self):
		return "Room num: " + str(self.room_num)
class Player(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	name = models.CharField(max_length=20)
	role = models.BooleanField()
	seed = models.BigIntegerField(default = 0)
	def __str__(self):
		return "Name: " + self.name +" Game: " + str(self.game.room_num) + "Seed: " + str(self.seed)