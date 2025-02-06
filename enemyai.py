#Files for functions, classes, and methods used by the enemy for
#decision making.
#################################80CHAR#########################################
import random

class DecisionMaker:
	#set up variables
	weapon_main
	weapon_secondary
	defense_ability
	percent_to_move
	percent_to_defend
	def __init__(self):
		#set up constructure for DecisionMaker
		self.weapon_main = [0] * 9
		self.weapon_secondary = [0] * 9
		self.defense_ability = 0
		self.percent_to_move = 33
		self.percent_to_defend = 10
	def Take_Action(self):
		#on random chance will defend
		if random.randint(1, 100) <= 10:
			self._Defense_Action()
			return
		#on random chance will move
		if random.randint(1, 100) <= 33:
			self._Move_Action()
			return
		#if didnt move or defend will choose best weapon to use
		if Main_Is_Best():
			self._Attack_Action(self.weapon_main)
			return
		self._Attack_Action(self.weapon_secondary)
		return
	def _Attack_Action(weapon):
		''' DONT CALL THIS FUNCTION '''
		#attack
	def _Defense_Action():
		''' DONT CALL THIS FUNCTION '''
		#defensive action
	def _Move_Action():
		''' DONT CALL THIS FUNCTION '''
		#move action
	def Main_Is_Best():
		#if main is best return true
	def Create_Enemy(type=None):
