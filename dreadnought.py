# dreadnought(player) file
# will handle basic logic and functionality for the dreadnought(player)
# # (utlized heavily by enemy ai)
# will rely on other classes/files: (weapon.py)


from weapons import Weapon

class Dreadnought:
	#
	# playerWeaponPairSynergyMap = { # handle with dictionary keyed by pairs of weapon types ?
	# 	frozenset(["ExampleWeapon1", "ExampleWeapon2"]): "ExampleWeaponSynergyAttack1",
	# 	frozenset(["ExampleWeaponA", "ExampleWeaponB"]): "ExampleWeaponSynergyAttack2",
	# }
	#
	
	def __init__(self, name, healthPoints, leftWeapon, rightWeapon): # rename HealthPoints as healthPoints ?
		#NFR #24
		self.name = name
		self.healthPoints = healthPoints
		self.leftWeapon = leftWeapon
		self.rightWeapon = rightWeapon

	def attackWithLeftWeapon(self, occupantPosition, target): # ! occupantPosition, and target not yet defined within attackWithXWeapon
		# temp dreadnought weapon attack(LEFT ARM) (will require user confirmation to confirm attack)
		chosenAttackZone = self._chooseWeaponAttackZone(self.leftWeapon) # utilize pvt helper to select where to attack
		print(f"{self.name} performs an attack with it's (LEFT) ({self.leftWeapon.name})!")
		self.leftWeapon.weaponAttack(occupantPosition, target)

	def attackWithRightWeapon(self, occupantPosition, target):
		# temp dreadnought weapon attack (RIGHT ARM) (will require user confirmation to confirm attack)
		chosenAttackZone = self._chooseWeaponAttackZone(self.rightWeapon) # utilize pvt helper to select where to attack
		print(f"{self.name} performs an attack with it's (RIGHT) ({self.rightWeapon.name})!")
		self.rightWeapon.weaponAttack(occupantPosition, target)

	def _chooseWeaponAttackZone(self, weapon): # pvt helper used to select which attackZone to attack when attacking with a weapon
		attackZoneOptions = weapon.getWeaponAttackZoneOptions()
		print(f"{weapon.name} can attack in one of the following zones:")
		for i, attackZone in enumerate(attackZoneOptions):
			print(f"{i}) {sorted(attackZone)}")

		while True:
			choice = input("Select an attackZone index to attack: ")
			try:
				choiceInt = int(choice)
				chosenAttackZone = attackZoneOptions[choiceInt]
				return chosenAttackZone
			except(ValueError, IndexError):
				print("Error: Invalid attackZone choice.")

	def isAlive(self):
		return self.healthPoints > 0

	def takeDamage(self, amount: int): # self ?, amount: int ? ~~ correct ?
	# when a dreadnought is hit for damage
		self.healthPoints -= amount
		if not self.isAlive(): # check if dead
			print(f"{self.name} has been destroyed!") # temp
			# remove from game, end game etc...
			
