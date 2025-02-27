#Files for MechInit a class that will instaniate all of the mechs needed
#for a game.
#################################80CHAR#########################################
import random
import dreadnought
import playerGrid
import weapons
import enemyai


class MechInit:
	#initializes an object which will hold all of the mech's along
	#with any additional information
	playerMech
	playerPosition
	enemyMech
	enemyPosition
	currentEnemy
	currentStage
	def __init__(self):
		#construct player mech default 2 bolters
		self.playerMech = new Dreadnought(
			"template", 1, new Bolter(), new Bolter()
			)
		self.playerPosition = new playerGrid()
		#construct 9 enemy mech's with a random combo of weapons
		self.enemyMech = []
		self.enemyPosition = []
		for i in range(9):
			self.enemyMech.append(
				new BadMech(10, self.Random_Weapon(), self.Random_Weapon())
				)
			if 0 <= i <= 2:
				self.enemyMech[i].Set_Level(1)
			if 3 <= i <= 5:
				self.enemyMech[i].Set_Level(2)
			if 6 <= i <= 8:
				self.enemyMech[i].Set_Level(3)
			self.enemyPosition.append(new playerGrid())
		#construct variable to keep track of current enemy
		self.currentEnemy = 0
		#construct variable to keep track of current stage
		self.currentStage = 1
	#method used for choosing how to construct the NPC mechs with random
	#weapons
	def Random_Weapon(self):
		choice = random.randint(1, 4)
		if choice == 1:
			return new Bolter()
		elif choice == 2:
			return new MeleeWeapon1()
		elif choice == 3:
			return new AOEWeapon1()
		else:
			return new AssaultCannon()
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
