# test file for weapons.py and dreadnought.py

import unittest
from unittest.mock import patch

from dreadnought import Dreadnought
from weapons import Bolter, MeleeWeapon1, AOEWeapon1, AssaultCannon

# BlackBox Unit-Tests:
class TestAssaultCannon(unittest.TestCase):

	def testAssaultCannonAttackAndZone(self):
		testACannon = AssaultCannon()
		# BB testing attackZone
		# AssaultCannon has a 1x2 (rowXcol) attack zone, which means it can have 6 different options for its attack zone.
		possibleAttackZones = testACannon.getWeaponAttackZoneOptions()
		self.assertEqual(len(possibleAttackZones), 6, "The AssaultCannon should have 6 attack zone options to choose from.") # assert #1
		for attackZone in possibleAttackZones:
			self.assertEqual(len(attackZone), 2, f"Each attack zone should consist of 2 tiles, and got {attackZone}") # assert #2

		# BB weaponAttack (against a test/mock dreadnought)
		class MockDreadnought:
			def __init__(self):
				self.hp = 20

			def takeDamage(self, amount):
				self.hp -= amount

		targetDreadnought = MockDreadnought()
		chosenAttackZone = possibleAttackZones[0] # assume first zone as example
		occupantPosition1 = list(chosenAttackZone)[0] # case of assume target is there

		testACannon.weaponAttack(selectedAttackZone = chosenAttackZone, occupantPosition = occupantPosition1, targetDreadnought = targetDreadnought)
		self.assertEqual(targetDreadnought.hp, 18, "Target's HP should be reduced by 2 after being hit by an AssaultCannon") # assert #3 (20HP - AssaultCannonDmg = 18HP)

		occupantPosition2 = (2, 2) # case of assume target is not there
		testACannon.weaponAttack(chosenAttackZone, occupantPosition2, targetDreadnought)
		self.assertEqual(targetDreadnought, 18, "Target's HP should remain the same if it is not in the selected attackZone.") # assert #4 (18HP - 0(MISS) = 18HP)


# WhiteBox Unit-Tests:
class TestDreadnoughtTakeDamage(unittest.TestCase):
	# below is a copy of the functions/methods tested in the WB-UT
	'''
	def isAlive(self):
		return self.healthPoints > 0

	def takeDamage(self, amount: int):
	# when a dreadnought is hit for damage
		self.healthPoints -= amount
		if not self.isAlive(): # check if dead
			print(f"{self.name} has been destroyed!") # temp
			# remove from game, end game etc...
			
	'''

	def testDreadnoughtTakeDamageCases(self):
		# WB testing takeDamage and isAlive from dreadnought.py in different cases. (Both/All branches -> full coverage)
		testDreadnought1 = Dreadnought(name = "WhiteBoxTestDread", healthPoints = 5, leftWeapon = Bolter, rightWeapon = MeleeWeapon1)

		# takes damage but doesnt die
		testDreadnought1.takeDamage(2)
		# takes dmg?
		self.assertEqual(testDreadnought1.healthPoints, 3, "If starting HP=5, taking 2 damage should leave HP=3") # assert #5
		# alive?
		self.assertTrue(testDreadnought1.isAlive(), "Should be left with 3 hp, alive.") # assert #6

		# takes damage and dies
		testDreadnought1.takeDamage(3)
		# takes dmg?
		self.assertEqual(testDreadnought1, 0, "If HP=3, taking 3 damage should leave HP=0") # assert #7
		self.assertFalse(testDreadnought1.isAlive(), "If HP=0, should be dead.") # assert #8

		# takes damage that reduces it below death threshhold (0 hp)
		testDreadnought1.takeDamage(11)
		self.assertEqual(testDreadnought1.healthPoints, -11, "If HP=0, HP can still be damaged, HP=-11") # assert #9
		self.assertFalse(testDreadnought1.isAlive(), "If HP<0, should continue being dead.") # assert #10


# Integration Tests:
class TestWeaponDreadnoughtIntegration(unittest.TestCase):
	# exercises weapons.py and dreadnought.py at once
	# using mock for user input
	@patch('builtins.input', side_effect = ['0']) # first attack zone option will always be chosen

	def testLWeaponDreadnoughtIntegration(self, mock_input):
		lWpn = Bolter()
		rWpn = MeleeWeapon1()
		attackingDreadnought = Dreadnought(name = "AttackingDreadnought", healthPoints = 10, leftWeapon = lWpn, rightWeapon = rWpn) # doing the attacking

		targetedDreadnought = Dreadnought(name = "TargetedDreadnought", healthPoints = 10, leftWeapon = lWpn, rightWeapon = lWpn) # doing the 'getting attacked'

		# test occupant in row0
		occupantPosition = (0, 1)
		# test attack occupant location with left weapon(bolter)
		attackingDreadnought.attackWithLeftWeapon(occupantPosition, targetedDreadnought)
		self.assertEqual(targetedDreadnought.healthPoints, 8, "TargetedDreadnought should take 2HP from a successful hit with a bolter in row0.") # assert #11

		# test attack location other than occupant location with left weapon
		occupantPosition_miss = (2, 2)
		attackingDreadnought.attackWithLeftWeapon(occupantPosition_miss, targetedDreadnought)
		# HP should not change
		self.assertEqual(targetedDreadnought.healthPoints, 8, "TargetedDreadnought should not take damage if it is not within the chosen attackZone.") # assert #12

if __name__ == '__main__':
	unittest.main()

