import pygame
import pygame_menu
from pygame_menu import themes
from enum import Enum

class MenuType(Enum):
	EMPTY = 0
	MAIN = 1
	DIFFICULTY = 2


class MenuController: 
	def __init__(self, screen):
		self.screen = screen
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.stage = 0
		self.menu = MenuType.EMPTY
		self.active = False

	
	'''
		Menu Loop
			
			** handles logic for drawing the menus
			- Gets called on each frame if a menu is active
			- Stage represents which menu state is active
				- set the correct menu for the corresponding stage
			
	'''
	def menuLoop(self, events):
		if self.menu == MenuType.EMPTY:
			match self.stage:
				case 0:
					self.setMenu(MenuType.MAIN)
				case 1:
					self.setMenu(MenuType.DIFFICULTY)

		if self.menu != MenuType.EMPTY:
			self.drawMenu(events)

	def setMenu(self, menuType):
		print("Set menu")
		match menuType:
			case MenuType.MAIN:
				self._initMainMenu()
			case MenuType.DIFFICULTY:
				self._initDifficultyMenu()

	def drawMenu(self, events):
		self.menu.update(events)
		self.menu.draw(self.screen)


	def _initMainMenu(self):
		print("Init main menu")
		self.menu = pygame_menu.Menu(
			"Welcome, Pilot!",
			self.width, self.height,
			theme=themes.THEME_BLUE
		)
		self.menu.add.button("Change Difficulty", self._select_difficulty)
		self.menu.add.button('Play', self._play)
	
	def _initDifficultyMenu(self):
		self.menu = pygame_menu.Menu(
			"Select Difficulty",
			self.width, self.height,
			theme=themes.THEME_BLUE
		)
		self.menu.add.button("Easy", self._play)
		self.menu.add.button("Medium", self._play)
		self.menu.add.button("Hard", self._play)
		print("Init difficulty menu")
	
	

	def _select_difficulty(self):
		print("Select difficulty")

	def _play(self):
		print("Play")