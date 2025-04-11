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

def combat_log_text(first_a, second_a, turn_counter):
    #set up variables for crafting combat text
    move = 0
    buff = 0
    attack = 0
    log_text = ""
    if first_a == 1:
        buff += 1
        if second_a == 1:
            buff += 1
            log_text = "Action "+str(turn_counter)+": The enemy defended greatly."
        elif second_a == 2:
            move += 1
            log_text = "Action "+str(turn_counter)+": The enemy defended and moved."
        else:
            attack += 1
            log_text = "Action "+str(turn_counter)+": The enemy defended and attacked."
    elif first_a == 2:
        move += 1
        if second_a == 1:
            buff += 1
            log_text = "Action "+str(turn_counter)+": The enemy moved and defended."
        elif second_a == 2:
            move += 1
            log_text = "Action "+str(turn_counter)+": The enemy moved extra far."
        else:
            attack += 1
            log_text = "Action "+str(turn_counter)+": The enemy moved and attacked."
    else:
        attack += 1
        if second_a == 1:
            buff += 1
            log_text = "Action "+str(turn_counter)+": The enemy attacked and defended"
        elif second_a == 2:
            move += 1
            log_text = "Action "+str(turn_counter)+": The enemy attacked and moved"
        else:
            attack += 1
            log_text = "Action "+str(turn_counter)+": The enemy attacked twice"
    return log_text, [move, buff, attack]

class BadMech(Dreadnought):
    def __init__(self, weapOne, weapTwo):
                super().__init__(
                    "'"+weapOne.name + "&" + weapTwo.name+"'" + " Mech",
                    20,
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
    def Level_Up(self):
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
        self.best_attack = GridCounter()
        self.current_mech = self.world_state.enemyMech[self.current_enemy]
        self.turns_since_move = 0
        self.turns_since_defend = 0
    def Take_Action(self):
        self.current_enemy = self.world_state.Get_Current_Enemy()
        self.current_position = self.world_state.enemyMech[self.current_enemy]
        self.best_attack.Update_Count(self.world_state.playerPosition.get_player_position())
        defend = 50 - (self.game_difficulty*20) + self.turns_since_defend
        move = 50 - (self.game_difficulty*20) + self.turns_since_move
        #on random chance will defend
        if random.randint(1, 100) <= defend:
            self._Defense_Action()
            self.turns_since_defend = 0
            return 1
        #on random chance will move
        if random.randint(1, 100) <= move:
            self._Move_Action()
            self.turns_since_move = 0
            return 2
        #if didnt move or defend will choose best weapon to use
        self.turns_since_move += 0.5
        self.turns_since_defend += 0.5
        if self._Main_Is_Best():
            return self._Attack_Action(self.world_state.enemyMech[self.current_enemy].leftWeapon)
        return self._Attack_Action(self.world_state.enemyMech[self.current_enemy].rightWeapon)
    def _Attack_Action(self, weapon):
        ''' DONT CALL THIS FUNCTION '''
        attack_position = self.best_attack.Best_Attack()
        self.world_state.enemyMech[self.current_enemy].Change_Status("normal")
        hero = self.world_state.playerMech
        hero_position = self.world_state.playerPosition.get_player_position()
        hits, hit_option = self._Does_Weapon_Hit(weapon.getWeaponAttackZoneOptions(), hero_position, attack_position)
        if hits:
            hero.healthPoints -= weapon.damage
        if hero.healthPoints < 0:
            hero.healthPoints = 0
        return hit_option
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
    def Update_Difficulty(self, difficulty):
        self.game_difficulty = difficulty
        for i in range(difficulty):
            for mech in self.world_state.enemyMech:
                mech.Level_Up()
    def _Does_Weapon_Hit(self, weapon_range, hero_pos, attack_pos):
        for option in weapon_range:
            for spot in option:
                if spot == attack_pos:
                    if spot == hero_pos:
                        return 1, option
                    else:
                        return 0, option
        return 0




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
        0:[1,3],
        1:[0,2,4],
        2:[1,5],
        3:[0,4,6],
        4:[1,3,5,7],
        5:[2,4,8],
        6:[3,7],
        7:[4,6,8],
        8:[5,7],
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
    def Best_Attack(self):
        chance = 1
        besthit = 4
        for spot,likely in enumerate(self.Percent_Matrix()):
            if likely < chance:
                chance = likely
                besthit = spot
            elif math.isclose(likely, chance):
               if random.randint(0, 1):
                    chance = likely
                    besthit = spot 
        return (math.floor(besthit/3),besthit % 3)
