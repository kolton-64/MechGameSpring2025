# rewards.py
"""
Basic start to implementing a 'semi random' reward system for the player
# Rewards are to be possibly granted after a fight is won by the player
# (Will need adaption/integration with UI...)

# Currently, likely does not fully behave properly when called !!!
"""

import random
from weapons import Bolter, MeleeWeapon1, AOEWeapon1, AssaultCannon

class RewardSystem:
	"""
	This class will handle creating/generating the reward/loot options
	for the player after a fight. As well as applying
	the reward/upgrade to the player/game.
	"""

	def __init(self, seed = None):
		# optional seed param for reproducing random states.
		if seed is not None:
			random.seed(seed)

	def generateRewardPool(self, playerDreadnought, rewardFactor):
		"""
		generate 'loot table' options for what rewards are available to choose from
		"""
		rewardOptionCount = random.randint(1, 3) # how many rewards presented?
		rewards = []

		# what type of reward is each reward presented?
		for i in range(rewardOptionCount):
			rewardTypeRoll = random.random()
			if rewardTypeRoll < 0.5 # 50% chance to get new weapon (for now)
				newWpnReward = self._rollNewWeapon_reward(rewardFactor)
				rewards.append(newWpnReward)

			elif rewardTypeRoll < 0.75: # 25% chance to get weapon upgrade (for now)
				wpnUpgradeReward = self._rollWeaponUpgrade_reward(playerDreadnought, rewardFactor)
				rewards.append(wpnUpgradeReward)

			else: # 25% chance to get (dreadnought) stat upgrade (for now)
				statUpgradeReward = self._rollMechStatUpgrade_reward(rewardFactor)
				rewards.append(statUpgradeReward)

		# to-add:
		# rewards.append(self._newAbility_reward)
		# rewards.append(self._abilityUpgrade_reward)
		# etc...

		return rewards

	def applyChosenReward(self, playerDreadnought, chosenReward):
		"""
		apply the reward chosen by the player to the player dreadnought
		"""
		rewardType = reward['type']

		if rewardType == 'new_weapon': # replace one of the players weapons
			newWeaponType = reward['weapon_type']
			# playerDreadnought.leftWeapon = newWeaponType() # pick which weapon to replace

		elif rewardType == 'weapon_upgrade': # upgrade one of the players weapons
			# player selects which weapon to upgrade
			weaponUpgrading = playerDreadnought.leftWeapon # for now!
			# weaponUpgrading = playerDreadnought.rightWeapon
			if weaponUpgrading:
				weaponUpgrading.damage += reward['upgrade_amount'] # upgrade wpn stat

		elif rewardType == 'dreadnought_stat_upgrade': # upgrade the player dreadnought's stats
			playerDreadnought.healthPoints += reward['stat_upgrade_amount'] # just HP, for now!

		# elif reward[''] == '':

		# elif reward[''] == '':

		# etc...

		print(f"Reward applied: {reward['description']}")

	# Helper methods
	def _rollNewWeapon_reward(self, rewardFactor):
		"""
		get random new weapon reward from pool
		"""

		weaponPool = [Bolter, MeleeWeapon1, AOEWeapon1, AssaultCannon] # etc.
		chosenWeaponType = random.choice(weaponPool)

		# reward factor logic?

		return {
			'type': 'new_weapon',
			'description': f"Gained a new weapon: {chosenWeaponType.__name__} !",
			'weapon_type': chosenWeaponType
		}

	def _rollWeaponUpgrade_reward(self, playerDreadnought, rewardFactor):
		"""
		get random weapon upgrade reward from pool
		"""

		wpnUpgradeAmount = random.randint(1, 3) # tester vals
		# scale with rewardFactor?

		# reward factor logic?

		return {
			'type': 'weapon_upgrade',
			'description': f"Gained a weapon upgrade: +{wpnUpgradeAmount} damage!",
			'upgrade_amount': wpnUpgradeAmount
		}

	def _rollMechStatUpgrade_reward(self, rewardFactor):
		"""
		get random dreadnought stat upgrade from pool
		"""

		baseStatUpgrade = random.randint(2, 5)
		# scale with rewardFactor?

		# reward factor logic?

		return {
			'type': 'dreadnought_stat_upgrade',
			'description': f" upgraded HP stat by: +{wpnUpgradeAmount} !",
			'stat_upgrade_amount': baseStatUpgrade
		}

