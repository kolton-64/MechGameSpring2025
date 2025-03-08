#Files for functions, classes, and methods used to allow for expanded
#enemy mech features and provide decision making to the enemy mech.
#################################80CHAR#########################################
import random
from dreadnought import Dreadnought
from playerGrid import PlayerGrid
from weapons import Weapon
from weapons import Bolter
from weapons import MeleeWeapon1
from weapons import AOEWeapon1
from weapons import AssaultCannon

class BadMech(Dreadnought):
    def __init__(self, name, weapOne, weapTwo):
                super().__init__(
                    weapOne.name + " & " + weapTwo.name + " Mech",
                    1000,
                    weapOne,
                    weapTwo,
                    )
                self.mechStatus = "normal"
                self.availableStatus = [
                    "vulnerable",
                    "protected",
                    "strong",
                    "weak",
                    "repairing",
                ]
                self.mechLevel = 1
    def _Level_Up(self):
        level = self.mechLevel+1
        self.HealthPoints = self.HealthPoints * level
        self.mechLevel = level
        return 0, ""
    def Set_Level(self, level):
        if not isinstance(level, int):
            errStr = """error: expected argument of type int.
             did not recieve argument of type int"""
            return -1, errStr
        assert isinstance(level, int)
        if level < 0:
            return -1, "error: level arguments can only be positive"
        self.HealthPoints = self.HealthPoints * level
        self.mechLevel = level
        return 0, ""
    def Weapon_Change(self, hand):
        if not isinstance(level, int):
            errStr = """error: expected argument of type int.
             did not recieve argument of type int"""
            return -1, errStr
        assert isinstance(level, int) 
        if hand:
            self.leftWeapon = Random_Weapon()
        else:
            self.rightWeapon = Random_Weapon()
        return 0, ""
    def Take_Damage(self, dmg):
        if self.mechStatus == "vulnerable":
            self.HealthPoints -= (2*dmg)
        elif self.mechStatus == "protected":
            self.HealthPoints -= (.5*dmg)
        else:
            self.HealthPoints -= dmg
    def Heal(self, life):
        if self.mechStatus == "repairing":
            self.HealthPoints += (2*life)
        else:
            self.HealthPoints += life
    def Change_Status(self, status):
        if status.lower() in self.availableStatus:
            self.mechStatus = status
        else:
            self.mechStatus = "normal"

class DecisionMaker:
    def __init__(self, world, difficulty):
        #construct a world state
        self.world_state = world
        self.game_difficulty = difficulty
    def Take_Action(self):
        defend = 33
        move = 10
        #on random chance will defend
        if random.randint(1, 100) <= defend:
            self._Defense_Action()
            return 1
        #on random chance will move
        if random.randint(1, 100) <= move:
            self._Move_Action()
            return 2
        #if didnt move or defend will choose best weapon to use
        if _Main_Is_Best():
            self._Attack_Action(self.weapon_main)
            return 3
        self._Attack_Action(self.weapon_secondary)
        return 3
    def _Attack_Action(self, weapon):
        ''' DONT CALL THIS FUNCTION '''
        hero = self.world_state.playerMech
        if ((weapon.range & hero.position) and not hero.defend):
            hero.HealthPoints -= weapon.damage
        hero.defend = False
    def _Defense_Action(self):
        ''' DONT CALL THIS FUNCTION '''
        self.world_state.enemyMech[current_enemy].defend = True
    def _Move_Action(self):
        ''' DONT CALL THIS FUNCTION '''
        #do some inferance to figure out where to move
        newPosition = bestmove()
        self.world_state.enemyPosition = newPosition
    def _Main_Is_Best(self):
        ''' DONT CALL THIS FUNCTION '''
        #if main is best return true
        enemy = self.enemyMech
        return enemy.leftWeapon.damage >= enemy.leftWeapon.damage

class GridCounter:
    def __init__(self):
        self.space_count = [0, 0, 0,
                            0, 1, 0,
                            0, 0, 0]
        self.move_num = 1
    def Update_Count(self, move):
        if (isinstance(move, list) and len(move) != 9):
            return -1, """error: expected argument of type list with lenth of 
            9. did not recieve that"""
        assert isinstance(move, list)
        for i in range(9):
            self.space_count[i] += move[i]
        self.move_num += 1
    def Percent_Matrix(self):
        alpha = 1
        percent_array = []
        for spot in self.space_count:
            percent_array.append((self.move_num+alpha)/(spot+(9*alpha)))
        return percent_array
