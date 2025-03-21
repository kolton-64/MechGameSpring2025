#Files for functions, classes, and methods used to allow for expanded
#enemy mech features and provide decision making to the enemy mech.
#################################80CHAR#########################################
import random
import math
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
        self.healthPoints = self.healthPoints * level
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
        self.healthPoints = self.healthPoints * level
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
            self.healthPoints -= (2*dmg)
        elif self.mechStatus == "protected":
            self.healthPoints -= (.5*dmg)
        else:
            self.healthPoints -= dmg
    def Heal(self, life):
        if self.mechStatus == "repairing":
            self.healthPoints += (2*life)
        else:
            self.healthPoints += life
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
        self.current_enemy = 0
        self.best_move = GridCounter()
        self.current_mech = self.world_state.enemyMech[self.current_enemy]
    def Take_Action(self):
        self.current_enemy = self.world_state.Get_Current_Enemy()
        self.current_position = self.world_state.enemyMech[self.current_enemy]
        defend = 25
        move = 33
        #on random chance will defend
        if random.randint(1, 100) <= defend:
            self._Defense_Action()
            return 1
        #on random chance will move
        if random.randint(1, 100) <= move:
            self._Move_Action()
            return 2
        #if didnt move or defend will choose best weapon to use
        if self._Main_Is_Best():
            self._Attack_Action(self.world_state.enemyMech[self.current_enemy].leftWeapon)
            return 3
        self._Attack_Action(self.world_state.enemyMech[self.current_enemy].rightWeapon)
        return 3
    def _Attack_Action(self, weapon):
        ''' DONT CALL THIS FUNCTION '''
        self.world_state.enemyMech[self.current_enemy].Change_Status("normal")
        hero = self.world_state.playerMech
        hero_position = self.world_state.playerPosition.get_player_position()
        hero.healthPoints -= weapon.damage
        if hero.healthPoints < 0:
            hero.healthPoints = 0
    def _Defense_Action(self):
        ''' DONT CALL THIS FUNCTION '''
        self.world_state.enemyMech[self.current_enemy].Change_Status("protected")
    def _Move_Action(self):
        ''' DONT CALL THIS FUNCTION '''
        self.world_state.enemyMech[self.current_enemy].Change_Status("normal")
        #do some inferance to figure out where to move
        move = self.best_move.Best_Move(self.world_state.Get_Enemy_Position())
        self.world_state.Set_Enemy_Position(move)
    def _Main_Is_Best(self):
        ''' DONT CALL THIS FUNCTION '''
        #if main is best return true
        enemy = self.world_state.enemyMech[self.current_enemy]
        return enemy.leftWeapon.damage >= enemy.leftWeapon.damage

class GridCounter:
    def __init__(self):
        self.space_count = [0, 0, 0,
                            0, 1, 0,
                            0, 0, 0]
        self.move_num = 1
    def Update_Count(self, move):
        spot = move[0]*3 + move[1]*1
        move = [0] * 9
        move[spot] = 1
        if (isinstance(move, list) and spot > 8):
            return -1, """error: expected argument of type list with lenth of 
            9. did not recieve that"""
        move[spot] = 1
        self.space_count[spot] += 1
        self.move_num += 1
    def Percent_Matrix(self):
        alpha = 0.001
        total = 0
        percent_array = []
        for spot in self.space_count:
            percent_array.append((self.move_num+alpha)/(spot+(9*alpha)))
            total += (self.move_num+alpha)/(spot+(9*alpha))
        for spot in range(9):
            percent_array[spot] = (percent_array[spot]) / total
        return percent_array
    def Best_Move(self, position):
        spot = position[0]*3 + position[1]*1
        posible_moves = {
        0:[0,1,3,4],
        1:[0,1,2,3,4,5],
        2:[0,1,4,5],
        3:[0,1,3,4,6,7],
        4:[0,1,2,3,4,5,6,7,8],
        5:[1,2,4,5,7,8],
        6:[3,4,6,7],
        7:[3,4,5,6,7,8],
        8:[4,5,7,8],
        }
        info = self.Percent_Matrix()
        move = posible_moves[spot]
        chance = 0
        bestmove = 4
        for space in move:
            if info[space] > chance:
                chance = info[space]
                bestmove = space
            elif math.isclose(info[space], chance):
                if random.randint(0, 1):
                    chance = info[space]
                    bestmove = space
        new_move = (math.floor(bestmove/3),bestmove%3)
        self.Update_Count(new_move)
        return new_move
