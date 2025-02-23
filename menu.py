import pygame
import pygame_menu
from pygame_menu import themes
from enum import Enum

class MenuType(Enum):
	EMPTY = 0
	MAIN = 1
	DIFFICULTY = 2
	IN_GAME = 3

class Difficulty(Enum):
	EASY = 0
	MEDIUM = 1
	HARD = 2


class MenuController: 
	def __init__(self, screen):
		self.screen = screen
		self.width = screen.get_width()
		self.height = screen.get_height()

		# stage determines if player is on main menu or in-game menu
		self.stage: int = 0

		self.menu = MenuType.EMPTY
		self.active = False


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
		if self.menu == MenuType.EMPTY and self.active:
			match self.stage:
				case 0:
					self.setMenu(MenuType.MAIN)
				case 1:
					self.setMenu(MenuType.IN_GAME)

		# Only draw the menu if the menu has been properly set
		if self.menu != MenuType.EMPTY and type(self.menu) == pygame_menu.menu.Menu:
			self.drawMenu(events)


	def setMenu(self, menuType):
		print("Set menu")
		match menuType:
			case MenuType.MAIN:
				self._initMainMenu()
			case MenuType.IN_GAME:
				self._initInGameMenu()

	def drawMenu(self, events):
		print(type(MenuType))
		self.menu.update(events)
		if(type(self.menu) == pygame_menu.menu.Menu):
			self.menu.draw(self.screen)


	def _initMainMenu(self):
		print("Current Difficulty Level: ", self.difficulty)
		self.menu = pygame_menu.Menu(
			"Welcome, Pilot!",
			self.width, self.height,
			theme=themes.THEME_BLUE
		)
		self.menu.add.button('Play', self._play)
		self.menu.add.button("Change Difficulty", self._initDifficultyMenu)
		self.menu.add.button("Exit", self._terminate)
		print(" - Initialized main menu - ")


	def _initInGameMenu(self):
		self.menu = pygame_menu.Menu(
			"Game Paused",
			self.width / 2, self.height / 2,
			theme=themes.THEME_DARK
		)

		self.menu.add.button('Resume', self._resume)
		self.menu.add.button('Quit', self._initMainMenu)
		print(" - Initialized in game menu - ")
	
	def _resume(self):
		self.menu = MenuType.EMPTY


	def _initDifficultyMenu(self):
		self.menu = pygame_menu.Menu(
			"Select Difficulty",
			self.width, self.height,
			theme=themes.THEME_BLUE
		)
		self.menu.add.button("Easy", self._setDifficultyEasy)
		self.menu.add.button("Medium", self._setDifficultyMedium)
		self.menu.add.button("Hard", self._setDifficultyHard)
		self.menu.add.button("Back", self._initMainMenu)
		print(" - Initialized difficulty menu - ")

	
	def _setDifficultyEasy(self):
		self.difficulty = Difficulty.EASY

	def _setDifficultyMedium(self):
		self.difficulty = Difficulty.MEDIUM

	def _setDifficultyHard(self):
		self.difficulty = Difficulty.HARD



	def _play(self):
		print("Play")
		pygame_menu.events.CLOSE
		self.menu = MenuType.EMPTY
		print(self.menu)
		self.stage = 1
		self.active = False

	def _terminate(self):
		pygame.quit()