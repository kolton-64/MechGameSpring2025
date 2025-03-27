import sys
import pygame
import pygame_menu
from pygame_menu import themes
from enum import Enum
import time
import unittest
from game_state import Difficulty

class MenuType(Enum):
	EMPTY = 0
	MAIN = 1
	DIFFICULTY = 2
	IN_GAME = 3



'''
	Menu Controller

		- creates game menus using pygame_menu library 
			- link: https://pygame-menu.readthedocs.io/en/3.5.2/index.html
		- keeps track of current menu
		- only draws menu when a menu is supposed to be active
'''

class MenuController: 
	def __init__(self, gameState, pg, screen):
		self.gameState = gameState
		self.pg = pg
		self.screen = screen
		self.width = screen.get_width()
		self.height = screen.get_height()

		# stage determines if player is on main menu or in-game menu
		self.stage: int = 0

		self.menu = MenuType.EMPTY
		self.currentMenu = MenuType.EMPTY
		self.mainTheme = themes.THEME_BLUE

		self.j = 0


		# This is just a placeholder variable
		# difficulty will be tracked in a state machine
		# default to easy
		self.difficulty = Difficulty.EASY
		print(self.difficulty.value)

	
	'''
		Menu Loop
			
			** handles logic for drawing the menus
			- Gets called on each frame if a menu is active
			- Stage represents which menu state is active
				- set the correct menu for the corresponding stage
			
	'''
	def menuLoop(self, events):


		print("Menu Loop")

		print("TESTING")
		print(self.gameState.currentState())

		if self.menu == MenuType.EMPTY and self.gameState.getMenuActive():
			match self.stage:
				case 0:
					self.setMenu(MenuType.MAIN)
				case 1:
					self.setMenu(MenuType.IN_GAME)
		
		if self.gameState.currentState().value == 1 and self.gameState.getMenuActive():
			if(self.gameState.getMenuActive()): #james smells like cheese -Oscar
				self.setMenu(MenuType.IN_GAME)
			self._initInGameMenu()


	def setMenu(self, menuType):
		print("Set menu")
		match menuType:
			case MenuType.MAIN:
				self.currentMenu = MenuType.MAIN
				self._initMainMenu()
			case MenuType.IN_GAME:
				self.currentMenu = MenuType.IN_GAME
				self._initInGameMenu()

	def drawMenu(self, events):
		self.menu.update(events)
		if(type(self.menu) == pygame_menu.menu.Menu):
			self.menu.mainloop(self.screen)


	# Landing page menus

	# Main menu where player can change difficult, enter game, or exit
	def _initMainMenu(self):
		if(self.menu != MenuType.EMPTY):
			self.menu.disable()
		# indicate main menu stage
		self.stage = 0  

		# define pygame menu
		self.menu = pygame_menu.Menu(
			"Rogue Dreadnaught",
			self.width, self.height,
			theme=self.mainTheme
		)

		# define buttons and onclick functions
		self.menu.add.button('Play', self._play)
		self.menu.add.button("Change Difficulty", self._initDifficultyMenu)
		self.menu.add.button("Exit", self._terminate)

		self.menu.mainloop(self.screen)

		print(" - Initialized main menu - ")

	# Start the game
	def _play(self):
		self.menu.disable()

		# discard the current menu 
		self.menu = MenuType.EMPTY
		self.currentMenu = MenuType.EMPTY

		# set the menu stage to the in game menu index 1
		self.stage = 1

		# deactivate menu's
		self.gameState.setMenuActive(False)
		self.gameState.setGameActive(True)


		print(self.gameState.currentState())

		print(" - Beginning game - ")
		pygame_menu.events.EXIT

	def _terminate(self):
		self.pg.quit()
		print("PYGAME TERMINATED")
		sys.exit()

	def _initDifficultyMenu(self):
		if(self.menu != MenuType.EMPTY):
			self.menu.disable()
		self.menu = pygame_menu.Menu(
			"Select Difficulty",
			self.width, self.height,
			theme=themes.THEME_BLUE
		)

		match self.gameState.getDifficulty():
			case 0:
				message = "Difficulty: Easy"
			case 1:
				message = "Difficulty: Medium"
			case 2:
				message = "Difficulty: Hard"
			case _:
				print(self.gameState.getDifficulty())
				message = "Difficulty: Unknown"
		# message = f"Difficulty: {Difficulty(self.worldState.getDifficulty())}"

		self.menu.add.label(message)

		# needed to declare individual functions to avoid immediate callback
		self.menu.add.button("Easy", self._setDifficulty, Difficulty.EASY)
		self.menu.add.button("Medium", self._setDifficulty, Difficulty.MEDIUM)
		self.menu.add.button("Hard", self._setDifficulty, Difficulty.HARD)
		self.menu.add.button("Back", self._initMainMenu)

		self.menu.mainloop(self.screen)
		print(" - Initialized difficulty menu - ")
	
	def _setDifficulty(self, difficulty: Difficulty):
		self.gameState.setDifficulty(difficulty)
		print(" - Difficulty set to: ", self.gameState.getDifficulty())
		self._initDifficultyMenu()

	# In game menus
	def _initInGameMenu(self):
		print(" - Initializing in game menu - ")
		if(self.menu != MenuType.EMPTY):
			self.menu.disable()
		self.menu = pygame_menu.Menu(
			"Game Paused",
			self.width / 2, self.height / 2,
			theme=themes.THEME_DARK
		)

		self.menu.add.button('Resume', self._resume)
		self.menu.add.button('Quit', self._initMainMenu)
		self.menu.mainloop(self.screen)
		print(" - Initialized in game menu - ")
	
	def _setAudioPreference(self, active: bool, volume: int):
		self.gameState.setMusicActive(active)



	
	def _resume(self):
		self.menu.disable()
		self.menu = MenuType.EMPTY
		self.gameState.setMenuActive(False)


class TestMenuController(unittest.TestCase):
	import game_state
	def setUp(self):
		self.GS = self.game_state.GameState()
		self.pg = pygame
		self.screen = pygame.display.set_mode((1280,720), pygame.NOFRAME)
		self.MC = MenuController(self.GS, self.pg, self.screen)
	
	'''
		Integration test

			- 2 units: 
				1) (class) MenuController 
				2) (class) game_state 
	'''
	def test_integration_game_state_menu(self):
		self.pg.init()

		# game_state: Game should not be active 
		self.assertFalse(self.GS.getGameActive())

		# game_state: menu should be active 
		self.assertTrue(self.GS.getMenuActive())

		# Setting difficulty in Menu Controller should update game state
		# game_state: should only accept Difficulty enum types but can return the int value or the string value of the difficulty
		self.MC._setDifficulty(-1)
		self.assertEqual(self.GS.getDifficulty(), 0)

		self.MC._setDifficulty(Difficulty.EASY)
		self.assertEqual(self.GS.getDifficulty(), 0)
		self.assertEqual(self.GS.getDifficultyName(), "Easy")

		self.MC._setDifficulty(Difficulty.MEDIUM)
		self.assertEqual(self.GS.getDifficulty(), 1)
		self.assertEqual(self.GS.getDifficultyName(), "Medium")

		self.MC._setDifficulty(Difficulty.HARD)
		self.assertEqual(self.GS.getDifficulty(), 2)
		self.assertEqual(self.GS.getDifficultyName(), "Hard")

		self.MC._setDifficulty(3)

		# game_state: difficulty should not change from last value as 3 is out of range
		self.assertEqual(self.GS.getDifficulty(), 2)

		self.MC._setDifficulty("HARD")

		# getDifficulty should still return 2 for hard as it has still not been mutated.
		# setDifficulty only accepts Difficulty enum types
		self.assertEqual(self.GS.getDifficulty(), 2)



		# Now start the game from menu controller
		self.MC._play()

		# game_state: game should now be active
		self.assertTrue(self.GS.getGameActive())

		# game_state: menus should be inactive
		self.assertFalse(self.GS.getMenuActive())
	

	'''
		Black box test.  Testing Functional Requirement #34
		     - for this requirement I need a function that determines how much
			 the HUD will scale by, depending on the amount of damage taken
			 
			 1) 1 - 5 damage, HUD will scale by .1
			 2) 6 - 10 damage, HUD will scale by .2
			 3) 11+ damage, HUD will scale by .3

			unit will be a function called hud_scale(damage: int)
			I will use the test to write the function.
	'''
	def test_hud_scale(self):
		scaleFactor = hud_scale(-1)
		self.assertEqual(scaleFactor, 0)

		scaleFactor = hud_scale(0)
		self.assertEqual(scaleFactor, 0)

		scaleFactor = hud_scale(1)
		self.assertEqual(scaleFactor, .1)

		scaleFactor = hud_scale(5)
		self.assertEqual(scaleFactor, .1)

		scaleFactor = hud_scale(6)
		self.assertEqual(scaleFactor, .2)

		scaleFactor = hud_scale(10)
		self.assertEqual(scaleFactor, .2)
		
		scaleFactor = hud_scale(11)
		self.assertEqual(scaleFactor, .3)


def hud_scale(damage: int):
	scale: float = 0 
	if(damage > 0 and damage <= 5):
		scale = .1
	if(damage >= 6 and damage <= 10):
		scale = .2
	if(damage > 10):
		scale = .3
	return scale