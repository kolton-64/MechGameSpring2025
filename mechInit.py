#Files for MechInit a class that will instaniate all of the mechs needed
#for a game.
#################################80CHAR#########################################
import random
from dreadnought import Dreadnought
from playerGrid import PlayerGrid
from weapons import Weapon
from weapons import Bolter
from weapons import MeleeWeapon1
from weapons import AOEWeapon1
from weapons import AssaultCannon
from enemyai import BadMech
from enemyai import DecisionMaker


class MechInit:
	def __init__(self):
		#construct player mech default 2 bolters
		self.playerMech = Dreadnought("template", 50, Bolter(), Bolter())
		self.playerPosition = PlayerGrid()
		#construct 9 enemy mech's with a random combo of weapons
		self.enemyMech = []
		self.enemyPosition = []
		for i in range(9):
			self.enemyMech.append(
				BadMech(self.Random_Weapon(), self.Random_Weapon())
				)
			if 0 <= i <= 2:
				self.enemyMech[i].Set_Level(1)
			if 3 <= i <= 5:
				self.enemyMech[i].Set_Level(2)
			if 6 <= i <= 8:
				self.enemyMech[i].Set_Level(3)
			self.enemyPosition.append(PlayerGrid())
		#construct variable to keep track of current enemy
		self.currentEnemy = 0
		#construct variable to keep track of current stage
		self.currentStage = 1
	#method used for choosing how to construct the NPC mechs with random
	#weapons
	def Random_Weapon(self):
		choice = random.randint(1, 4)
		if choice == 1:
			return Bolter()
		elif choice == 2:
			return MeleeWeapon1()
		elif choice == 3:
			return AOEWeapon1()
		else:
			return AssaultCannon()
	def Set_Difficulty(self, difficulty):
		for i in range(9):
			if 0 <= i <= 2:
				self.enemyMech[i].Set_Level(1*difficulty)
			if 3 <= i <= 5:
				self.enemyMech[i].Set_Level(2*difficulty)
			if 6 <= i <= 8:
				self.enemyMech[i].Set_Level(3*difficulty)
	def Set_Enemy(self, round, choice):
		#choice is 1-3 but based on the round will pick enemy 0-8
		if round == 1:
			self.currentStage = 1
			self.current_enemy = choice - 1
		elif round == 2:
			self.currentStage = 2
			self.current_enemy = choice + 2
		else:
			self.currentStage = 3
			self.current_enemy = choice + 5
	def Get_Enemy_Position(self):
		return self.enemyPosition[self.currentEnemy].player_position
	def Set_Enemy_Position(self, spot):
		self.enemyPosition[self.currentEnemy].player_position = spot
	def Get_Current_Enemy(self):
		return self.currentEnemy
	def Get_Level(self):
		return self.enemyMech[self.currentEnemy].mechLevel
