# weapons.py
# module for handling Dreadnought weapon logic
#
# to use, import weapons via weapon class
# ie:
# from weapons import Bolter, MeleeWeapon1, AOEWeapon1
# or 
# from weapons import Weapon
#

class Weapon:
	# weaponRange rename?
	# add ammoCapacity for weapons requiring ammunition?
	def __init__(self, name, damage, weaponRange):
		self.name = name
		self.damage = damage
		self.weaponRange = [] # name attackZone?

	def getWeaponRange(self):
		return self.weaponRange

	# weapon attack logic? or will that be in combat/player/ect file?
	def weaponAttack(self, occupantPosition, targetDreadnought):
		# temporary basic weapon attack logic, text (always hits static zone) 
		if occupantPosition in self.weaponRange:
			# Hit = character damage == weaponDamage
			print(f"{self.name} hit at tile: {occupantPosition} for {self.damage} damage.")
		else:
			# Miss = no character damage
			print(f"{self.name} missed at tile: {occupantPosition}.")

	def displayWeaponStats(self):
		# FR#22 When weapon is selected and indicator will present the stats and attack pattern
		# will need to visually indicate, but for now just print
		print(f"Selected Weapon: {self.name}")
		print(f"Weapon Damage: {self.damage}")
		self.displayWeaponAttackGrid # needs integration with pygame / visuals

	def displayWeaponAttackGrid(self):
		# shows grid representation of weapon attack zone(1's = hit zone)
		print(f"{self.name}: Attack Pattern:")
		for row in range(3):
			rowRepr = []
			for col in range(3):
				if (row, col) in self.weaponRange:
					rowRepr.append("1")
				else:
					rowRepr.append("0")
			print(" ".join(rowRepr))
		print()


class Bolter(Weapon):
# weapon #1: Bolter: base dmg, Straight line attack on grid, ammo?

	def __init__(self):
		super().__init__(
			name = "Bolter", #placeholder
			damage = 2, # temp
			weaponRange = [(1, 0), (1, 1), (1, 2)], # middle row for now
			)

class MeleeWeapon1(Weapon):
# weapon #2: MeleeWeapon1(placeholder, Powerfist, Chainfist, Chain-axe/sword, etc..): high dmg, Single tile attack?

	def __init__(self):
		super().__init__(
			name = "MeleeWeapon1", #placeholder
			damage = 3, # temp
			weaponRange = [(0, 0), (1, 0), (2, 0)], # single? (first column for now)
			)

class AOEWeapon1(Weapon):
# weapon #3: AOEWeapon1(placeholder, Flamer, Assault-Cannon, etc.: , base dmg?, Multi-tile pattern attack(AOE).

	def __init__(self):
		super().__init__(
			name = "AOEWeapon1",
			damage = 1, # temp
			weaponRange = [ # back 2 columns for now
				(0, 1), (0, 2),
				(1, 1), (1, 2),
				(2, 1), (2, 2)
			], 
			)

class AssaultCannon(Weapon):
# weapon #4: AOEWeapon2(placeholder, Flamer, Assault-Cannon, etc.: , base dmg?, Multi-tile pattern attack(AOE).

	def __init__(self):
		super().__init__(
			name = "AssaultCannon",
			damage = 2, # temp
			weaponRange = [ # every other tile hit. (scatter)
				(0, 0), (0, 2),
				(1, 1),
				(2, 0), (2, 2)
			], 
			)

