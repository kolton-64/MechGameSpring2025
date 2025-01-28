# weapons.py
# module for handling Dreadnought weapon logic
#
# to use, import weapons via weapon class
# ie:
# from weapons import Bolter, MeleeWeapon1, AOEWeapon1
#

class Weapon:
	# weapongRange = attackPattern? rename?
	# add ammoCapacity for weapons requiring ammunition?
	def __init__(self, name, damage, weaponRange):
		self.name = name
		self.damage = damage
		self.weaponRange = weaponRange

	# weapon attack logic? or will that be in combat/player/ect file?

class Bolter(Weapon):
# weapon #1: Bolter: base dmg, Straight line attack on grid, ammo?

	def __init__(self):
		super().__init__(
			name = "Bolter",
			# damage = 1,
			# weaponRange = [],
			)

class MeleeWeapon1(Weapon):
# weapon #2: MeleeWeapon1(placeholder, Powerfist, Chainfist, Chain-axe/sword, etc..): high dmg, Single tile attack?

	def __init__(self):
		super().__init__(
			name = "MeleeWeapon1", #placeholder
			# damage = 3,
			# weaponRange = [], # single?
			)

class AOEWeapon1(Weapon):
# weapon #1: AOEWeapon1(placeholder, Flamer, Assault-Cannon, etc.: , base dmg?, Multi-tile pattern attack(AOE).

	def __init__(self):
		super().__init__(
			name = "AOEWeapon1",
			# damage = 1,
			# weaponRange = [],
			)
