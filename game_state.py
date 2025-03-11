import enum

# World state keeps track of global game state
class GameState: 
	def __init__(self):
		self.difficulty: int = 0
		self.musicActive: bool = True
		self.gameActive: bool = False

		# Menu active is set to true by default because game currently loads to menu
		self.menuActive: bool = True	
	
	# Getters
	def getDifficulty(self):
		return self.difficulty

	def getMusicActive(self):
		return self.musicActive


	def getGameActive(self):
		return self.gameActive

	def getMenuActive(self):
		return self.menuActive

	# Setters
	def setDifficulty(self, diff: int):
		self.difficulty = diff
	
	def setMusicActive(self, active: bool):
		self.musicActive = active
	
	def setGameActive(self, active: bool):
		self.gameActive = active

	def setMenuActive(self, state: bool):
		self.menuActive = state




	def currentState(self):
		state = None
		if(self.menuActive and self.gameActive == False):
			state = GameState.MAIN_MENU
		elif(self.menuActive == False and self.gameActive):
			state = GameState.IN_GAME
		else:
			state = GameState.PAUSED



class GameState(Enum):
	MAIN_MENU = 0
	IN_GAME = 1
	PAUSED = 2 