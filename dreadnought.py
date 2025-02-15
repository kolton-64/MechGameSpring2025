# dreadnought(player) file
# will handle basic logic and functionality for the dreadnought(player)
# will rely on other classes/files: (weapon.py)
#
from weapons import Weapon

class Dreadnought:
	#
	#
	def __init__(self, name, HealthPoints, leftWeapon, rightWeapon):
		self.name = name
		self.HealthPoints = HealthPoints
		self.leftWeapon = leftWeapon
		self.rightWeapon = rightWeapon

	def attackWithLeftWeapon(self):
		# temp dreadnought weapon attack(LEFT ARM) (will require user confirmation to confirm attack)
		print(f"{self.name} performs an attack with it's (LEFT) ({self.leftWeapon.name})!")
		self.leftWeapon.weaponAttack(occupantPosition, target)

	def attackWithRightWeapon(self):
		# temp dreadnought weapon attack (RIGHT ARM) (will require user confirmation to confirm attack)
		print(f"{self.name} performs an attack with it's (RIGHT) ({self.rightWeapon.name})!")
		self.rightWeapon.weaponAttack(occupantPosition, target)

	def isAlive(self):
		return self.HealthPoints > 0

	def takeDamage(amount: int): # when a dreadnought is hit for damage
		self.HealthPoints -= amount
		if not self.isAlive(): # check if dead
			printf("{self.name} has been destroyed!") # temp
			# remove from game, end game etc...
			
