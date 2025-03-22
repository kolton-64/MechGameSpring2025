# weapons.py
# module for handling Dreadnought weapon logic
#
# to use, import weapons via weapon class
# ie:
# from weapons import Bolter, MeleeWeapon1, AOEWeapon1
# or 
# from weapons import Weapon
# (recommitted with PR... WP#7)

class Weapon:
	# add ammoCapacity for weapons requiring ammunition ?
	# add weaponPairSpecialAttack ?

	def __init__(self, name, damage): #weaponRange
		self.name = name # str - weapon's name
		self.damage = damage # int - weapon's damage

	def getWeaponAttackZoneOptions(self): # (subclasses override) ~ for dynamic weaponRange/AttackZone selection
		return []

	def weaponAttack(self, selectedAttackZone, occupantPosition, targetDreadnought):
		# temporary basic weapon attack logic, text
		# attempts hit occupantPosition if it is within the selected attack zone.
		# if so, the weapon deals its damage to the targetDreadnought in the occupantPosition (subtract hp)
		# otherwise, the attack is a miss (print for now)

		if occupantPosition in selectedAttackZone:
			print(f"{self.name} hit at tile: {occupantPosition} for {self.damage} damage.")
			if targetDreadnought: # if dreadnought in attackZone -> Hit -> character damage == weaponDamage
				targetDreadnought.takeDamage(self.damage)
		else: # Miss = no character damage
			print(f"{self.name} missed at tile: {occupantPosition}.")
			
	def displayWeaponStats(self): # for UI
		# will need to visually indicate, but for now just print
		print(f"Selected Weapon: {self.name}")
		print(f"Weapon Damage: {self.damage}")
		self.displayWeaponAttackGrid() # needs integration with pygame / visuals

	def displayWeaponAttackGrid(self): # utlized by displayWeaponStats
		# shows grid representation of weapon attack zone(1's = hit zone)
		print(f"{self.name}: Attack Pattern:")
		for row in range(3): # make dynamic?
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
			)

	def getWeaponAttackZoneOptions(self): # possible attackZones for weapon
		# Bolter has straight line attackPattern (1 row)
		row0 = {(0, 0), (0, 1), (0, 2)}
		row1 = {(1, 0), (1, 1), (1, 2)}
		row2 = {(2, 0), (2, 1), (2, 2)}
		return [row0, row1, row2]

class MeleeWeapon1(Weapon):
# weapon #2: MeleeWeapon1(placeholder, Powerfist, Chainfist, Chain-axe/sword, etc..): high dmg, Single tile attack?

	def __init__(self):
		super().__init__(
			name = "MeleeWeapon1", #placeholder
			damage = 2, # temp
			)

	def getWeaponAttackZoneOptions(self): # possible attackZones for weapon
		# MeleeWeapon1 has straight column attackPattern (1 columnn) (eventually limit to only front column?)
		# - for now can hit any 1 column
		col0 = {(0, 0), (1, 0), (2, 0)}
		col1 = {(0, 1), (1, 1), (2, 1)}
		col2 = {(0, 2), (1, 2), (2, 2)}
		return [col0, col1, col2]

class AOEWeapon1(Weapon): # will rename to either KrakMissileLauncher or FragMissileLauncher, then add the latter.
# weapon#3: name: AOEWeapon1, dmg: temp, attackZone: AOE/Concentrated explosion,

	def __init__(self):
		super().__init__(
			name = "AOEWeapon1",
			damage = 2, # temp
			)

	def getWeaponAttackZoneOptions(self): # possible attackZones for weapon
		# MissileLauncher for now hits a 2x2 'square' selection of tiles on the grid
		topLeftCornerCoordinates = [(0, 0), (0, 1), (1, 0), (1, 1)]
		attackZoneOptions = []
		for (row, column) in topLeftCornerCoordinates:
			attackZone = {
				(row, column), (row, column + 1), (row + 1, column), (row + 1, column + 1)
			}
			attackZoneOptions.append(attackZone)
		return attackZoneOptions

class AssaultCannon(Weapon):
# weapon #4: AOEWeapon2(placeholder, Flamer, Assault-Cannon, etc.: , base dmg?, Multi-tile pattern attack(AOE).

	def __init__(self):
		super().__init__(
			name = "AssaultCannon",
			damage = 2, # temp 
			)

	def getWeaponAttackZoneOptions(self): # possible attackZones for weapon
		# AssaultCannon for now hits any two tiles (adjacent) in the same column. (choosing from pairs of vertically adjacent tiles)
		attackZoneOptions = []
		for col in range(3):
			attackZone1 = {(0, col), (1, col)}
			attackZone2 = {(1, col), (2, col)}
			attackZoneOptions.append(attackZone1)
			attackZoneOptions.append(attackZone2)
		return attackZoneOptions
