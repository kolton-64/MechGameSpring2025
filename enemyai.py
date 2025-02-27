#Files for functions, classes, and methods used to allow for expanded
#enemy mech features and provide decision making to the enemy mech.
#################################80CHAR#########################################
import random
import dreadnought
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
	def Set_Level(self, level):
		self.HealthPoints = self.HealthPoints * level
		self.mechLevel = level
	def Level_Up(self):
		level = self.mechLevel+1
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
		defend = 33
		move = 10
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
