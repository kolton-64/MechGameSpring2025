#Files for functions, classes, and methods used by the enemy for
#decision making.
#################################80CHAR#########################################
import random
import dreadnought
import menu
import playerGrid
import weapons

class BadMech(Dreadnought):
	mechStatus
	availableStatus
	mechLevel
	def __init__(self, name, weapOne, weapTwo):
                super().__init__(
                	weapOne.name + " & " + weapTwo.name + " Mech",
                	1000,
                	weapOne,
                	weapTwo,
                	)
                mechStatus = "normal"
                availableStatus = [
                	"vulnerable",
                	"protected",
                	"strong",
                	"weak",
                	"repairing",
                ]
                mechLevel = 1
	def Level_Up(self, level):
		if level in range(1,3):
			self.HealthPoints = self.HealthPoints * level
			self.mechLevel = level
		else:
			level = (self.mechLevel)+1
			self.HealthPoints = self.HealthPoints * level
			self.mechLevel = level
	def Weapon_Change(self, hand):
		if hand:
			self.leftWeapon = new Random_Weapon()
		else:
			self.rightWeapon = new Random_Weapon()
	def Take_Damage(self, dmg):
		if self.mechStatus == "vulnerable":
			self.HealthPoints -= (2*dmg)
		elif self.mechStatus == "protected":
			self.HealthPoints -= (.5*dmg)
		else:
			self.HealthPoints -= dmg
	def Heal(self, life):
		if self.mechStatus == "repairing":
			self.HealthPoints += (2*life)
		else:
			self.HealthPoints += life
	def Change_Status(self, status):
		if status.lower() in self.availableStatus:
			self.mechStatus = status
		else:
			self.mechStatus = "normal"


def Random_Weapon():
	choice = random.randint(1, 4)
	if choice == 1:
		return new Bolter()
	elif choice == 2:
		return new MeleeWeapon1()
	elif choice == 3:
		return new AOEWeapon1()
	else:
		return new AssaultCannon()

class StateModel:
	playerMech
	playerPosition
	enemyMech
	enemyPosition
	percent_to_move
	percent_to_defend
	def __init__(self):
		#construct player and 9 enemies
		self.playerMech = new Dreadnought(
			"template", 1, new Bolter(), new Bolter()
			)
		self.playerPosition = new playerGrid()
		self.enemyMech = []
		self.enemyPosition = []
		self.percent_to_move = []
		self.percent_to_defend = []
		for i in range(9):
			self.enemyMech.append(
				new BadMech(10, Random_Weapon(), Random_Weapon())
				)
			if 0 <= i <= 2:
				self.enemyMech[i].Level_Up(1)
			if 3 <= i <= 5:
				self.enemyMech[i].Level_Up(2)
			if 6 <= i <= 8:
				self.enemyMech[i].Level_Up(3)
			self.enemyPosition.append(new playerGrid())
			self.percent_to_move.append(33)
			self.percent_to_defend.append(10)

class DecisionMaker:
	#declare variables that should be initialized
	world_state
	current_enemy
	game_difficulty
	def __init__(self, world, difficulty):
		#construct a world state
		self.world_state = world
		self.game_difficulty = difficulty
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
	def _Attack_Action(self, weapon):
		''' DONT CALL THIS FUNCTION '''
		hero = self.world_state.playerMech
		if ((weapon.range & hero.position) && not hero.defend):
			hero.HealthPoints -= weapon.damage
		hero.defend = False
	def _Defense_Action(self):
		''' DONT CALL THIS FUNCTION '''
		self.world_state.enemyMech[current_enemy].defend = True
	def _Move_Action(self):
		''' DONT CALL THIS FUNCTION '''
		#do some inferance to figure out where to move
		newPosition = bestmove()
		self.world_state.enemyPosition = newPosition
	def _Main_Is_Best(self):
		''' DONT CALL THIS FUNCTION '''
		#if main is best return true
		enemy = self.enemyMech
		return enemy.leftWeapon.damage >= enemy.leftWeapon.damage
	def Change_Enemy(self, round, choice):
		#choice is 1-3 but based on the round will pick enemy 0-8
		if round == 1:
			self.current_enemy = choice - 1
		elif round == 2:
			self.current_enemy = choice + 2
		else:
			self.current_enemy = choice + 5
