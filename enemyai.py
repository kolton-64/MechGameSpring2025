#Files for functions, classes, and methods used by the enemy for
#decision making.
#################################80CHAR#########################################
import random
import dreadnought
import menu
import playerGrid
import weapons

class BadMech(Dreadnought):
	HealthPoints
	leftWeapon
	rightWeapon
	defend
	def __init__(self, hp, mainhand, offhand):
		self.HealthPoints = hp
		self.leftWeapon = new Weapon(mainhand)
		self.rightWeapon = new Weapon(offhand)
		self.defend = False
	def Level_Up(level):
		self.HealthPoints = self.HealthPoints * level

class StateModel:
	playerMech
	playerPosition
	enemyMech
	enemyPosition
	percent_to_move
	percent_to_defend
	def __init__(self):
		#construct player and 9 enemies
		self.playerMech = new Dreadnought()
		self.playerPosition = new playerGrid()
		self.enemyMech = []
		self.enemyPosition = []
		self.percent_to_move = []
		self.percent_to_defend = []
		for i in range(9):
			self.enemyMech.append(new BadMech(10, sword, bolter))
			if 0 <= i <= 2:
				self.enemyMech[i].Level_Up(1)
			if 3 <= i <= 5:
				self.enemyMech[i].Level_Up(2)
			if 6 <= i <= 8:
				self.enemyMech[i].Level_Up(3)
			self.enemyMech.append(new playerGrid(3))
			self.enemyMech.append(33)
			self.enemyMech.append(10)


class DecisionMaker:
	#declare variables that should be initialized
	public StateModel world_state
	int current_enemy
	def __init__(self, world: StateModel, difficulty: int):
		#construct a world state
		self.world_state = world
	def Take_Action(self):
		defend = self.world_state.percent_to_defend[current_enemy]
		move = self.world_state.percent_to_move[current_enemy]
		#on random chance will defend
		if random.randint(1, 100) <= defend:
			self._Defense_Action()
			return
		#on random chance will move
		if random.randint(1, 100) <= move:
			self._Move_Action()
			return
		#if didnt move or defend will choose best weapon to use
		if _Main_Is_Best():
			self._Attack_Action(self.weapon_main)
			return
		self._Attack_Action(self.weapon_secondary)
		return
	def _Attack_Action(weapon):
		''' DONT CALL THIS FUNCTION '''
		hero = self.world_state.playerMech
		if ((weapon.range & hero.position) && not hero.defend):
			hero.HealthPoints -= weapon.damage
		hero.defend = False
	def _Defense_Action():
		''' DONT CALL THIS FUNCTION '''
		self.world_state.enemyMech[current_enemy].defend = True
	def _Move_Action():
		''' DONT CALL THIS FUNCTION '''
		#do some inferance to figure out where to move
		newPosition = bestmove()
		self.world_state.enemyPosition = newPosition
	def _Main_Is_Best():
		''' DONT CALL THIS FUNCTION '''
		#if main is best return true
		enemy = self.enemyMech
		return enemy.leftWeapon.damage >= enemy.leftWeapon.damage
	def Change_Enemy(round, choice):
		#choice is 1-3 but based on the round will pick enemy 0-8
		if round == 1:
			self.current_enemy = choice - 1
		elif round == 2:
			self.current_enemy = choice + 2
		else:
			self.current_enemy = choice + 5
