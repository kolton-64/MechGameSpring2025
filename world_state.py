
# World state keeps track of global game state
class WorldState: 
	def __init__(self):
		self.difficulty: int = 0
		self.gameActive: bool = False

		# Menu active is set to true by default because game currently loads to menu
		self.menuActive: bool = True	
	
	# Getters
	def getDifficulty(self):
		return self.difficulty

	def getGameActive(self):
		return self.gameActive

	def getMenuActive(self):
		return self.menuActive

	# Setters
	def setDifficulty(self, diff: int):
		self.difficulty = diff
	
	def setGameActive(self, active: bool):
		self.gameActive = active

	def setMenuActive(self, state: bool):
		self.menuActive = state

	