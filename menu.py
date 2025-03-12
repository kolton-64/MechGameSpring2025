import sys
import pygame
import pygame_menu
from pygame_menu import themes
from enum import Enum
import time
import unittest

class MenuType(Enum):
	EMPTY = 0
	MAIN = 1
	DIFFICULTY = 2
	IN_GAME = 3

class Difficulty(Enum):
	EASY = (0, "Easy")
	MEDIUM = (1, "Medium")
	HARD = (2, "Hard")

	def __init__(self, int, string):
		self.int = int
		self.string = string

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

		# If theres no menu, set up the correct one
		if self.menu == MenuType.EMPTY and self.gameState.getMenuActive():
			match self.stage:
				case 0:
					self.setMenu(MenuType.MAIN)
				case 1:
					self.setMenu(MenuType.IN_GAME)

		# Only draw the menu if the menu has been properly set
		if self.menu != MenuType.EMPTY:
			self.drawMenu(events)


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
			self.menu.draw(self.screen)


	# Landing page menus

	# Main menu where player can change difficult, enter game, or exit
	def _initMainMenu(self):
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

		print(" - Initialized main menu - ")

	# Start the game
	def _play(self):

		# discard the current menu 
		self.menu = MenuType.EMPTY
		self.currentMenu = MenuType.EMPTY

		# set the menu stage to the in game menu index 1
		self.stage = 1

		# deactivate menu's
		self.gameState.setMenuActive(False)
		self.gameState.setGameActive(True)

		print(" - Beginning game - ")

	def _terminate(self):
		self.pg.quit()
		print("PYGAME TERMINATED")
		sys.exit()

	def _initDifficultyMenu(self):
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
		self.menu.add.button("Easy", self._setDifficulty, Difficulty.EASY.value[0])
		self.menu.add.button("Medium", self._setDifficulty, Difficulty.MEDIUM.value[0])
		self.menu.add.button("Hard", self._setDifficulty, Difficulty.HARD.value[0])
		self.menu.add.button("Back", self._initMainMenu)

		print(" - Initialized difficulty menu - ")
	
	def _setDifficulty(self, difficulty):
		self.gameState.setDifficulty(difficulty)
		print(" - Difficulty set to: ", self.gameState.getDifficulty())
		self._initDifficultyMenu()

	# In game menus
	def _initInGameMenu(self):
		self.menu = pygame_menu.Menu(
			"Game Paused",
			self.width / 2, self.height / 2,
			theme=themes.THEME_DARK
		)

		self.menu.add.button('Resume', self._resume)
		self.menu.add.button('Quit', self._initMainMenu)
		print(" - Initialized in game menu - ")
	
	def _setAudioPreference(self, active: bool, volume: int):
		self.gameState.setMusicActive(active)

	def _fadeMenu(self, timeout):
		self.mainTheme.set_background_color_opacity = 0.5


	
	def _resume(self):
		self._fadeMenu(100)
		# self.menu = MenuType.EMPTY
		# self.gameState.setMenuActive(False)


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
				1) (function) MenuController._play() 
				2) (class) game_state 
	'''
	def test_state_update(self):

		# Starting the program will bring the player straight to the main menu

		# game_state: Game should not be active 
		self.assertFalse(self.GS.getGameActive())

		# game_state: menu should be active 
		self.assertTrue(self.GS.getMenuActive())

		# MenuController._play() will start the game
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