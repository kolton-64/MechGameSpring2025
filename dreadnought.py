# dreadnought(player) file
# will handle basic logic and functionality for the dreadnought(player)
# will rely on other classes/files: (weapon.py)
#

class Dreadnought:
	#
	#
	def __init__(self, HealthPoints, leftWeapon, rightWeapon):
		self.HealthPoints = HealthPoints
		self.leftWeapon = leftWeapon
		self.rightWeapon = rightWeapon
