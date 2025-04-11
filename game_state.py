from enum import Enum
import unittest

# World state keeps track of global game state
class GameState: 
	def __init__(self):
		self.difficulty: Difficulty = Difficulty.EASY
		self.musicActive: bool = True
		self.gameActive: bool = False

		# Menu active is set to true by default because game currently loads to menu
		self.menuActive: bool = True	

		self.gameOver: bool = False
	
	# Getters
	def getDifficulty(self):
		return self.difficulty.value[0]

	def getDifficultyName(self):
		return self.difficulty.value[1]
	

	def getMusicActive(self):
		return self.musicActive


	def getGameActive(self):
		return self.gameActive

	def getMenuActive(self):
		return self.menuActive

	# Setters
	def setDifficulty(self, diff):
		if(type(diff) == Difficulty):
			self.difficulty = diff
	
	def setMusicActive(self, active: bool):
		self.musicActive = active
	
	def setGameActive(self, active: bool):
		self.gameActive = active

	def setMenuActive(self, state: bool):
		self.menuActive = state

	def setGameOver(self, state: bool):
		self.gameOver = state




	def currentState(self):
		state = None
		if(self.menuActive and not self.gameActive):
			state = State.MAIN_MENU
		elif(not self.menuActive and self.gameActive and not self.gameOver):
			state = State.IN_GAME
		elif(self.menuActive and self.gameActive and not self.gameOver):
			state = State.PAUSED
		elif(self.menuActive and self.gameOver):
			state = State.GAME_OVER
		return state



class GameStateTest(unittest.TestCase):
	def setUp(self):
		self.GS = GameState()

	'''
		White-box unit test
		- Unit: currentState() function
		   - branch coverage is achieved as each branch condition is tested
		   - statement coverage is achieved as each statement is tested
		   - condition coverage is achieved as each condition is tested
	'''
	def test_currentState(self):
		# if the menu is active and game is not active state should return MAIN_MENU
		self.GS.setMenuActive(True)
		self.GS.setGameActive(False)
		state = self.GS.currentState()

		self.assertEqual(state, State.MAIN_MENU)

		# if the menu is not active and game is active state should return IN_GAME
		self.GS.setMenuActive(False)
		self.GS.setGameActive(True)
		state = self.GS.currentState()

		self.assertEqual(state, State.IN_GAME)

		# if both are true, state should return PAUSED
		self.GS.setMenuActive(True)
		self.GS.setGameActive(True)
		state = self.GS.currentState()

		self.assertEqual(state, State.PAUSED)


	    # inside of currentState, the only time state remains as None is when both menu and game are equal to False
		self.GS.setMenuActive(False)
		self.GS.setGameActive(False)
		state = self.GS.currentState()

		self.assertEqual(state, None)

		



class Difficulty(Enum):
	EASY = (0, "Easy")
	MEDIUM = (1, "Medium")
	HARD = (2, "Hard")

	def __init__(self, int, string):
		self.int = int
		self.string = string

class State(Enum):
	MAIN_MENU = 0
	IN_GAME = 1
	PAUSED = 2 
	GAME_OVER = 3