import unittest
from dreadnought import Dreadnought
from playerGrid import PlayerGrid
from weapons import Weapon
from weapons import Bolter
from weapons import MeleeWeapon1
from weapons import AOEWeapon1
from weapons import AssaultCannon
from enemyai import BadMech
from enemyai import DecisionMaker
from enemyai import GridCounter
from mechInit import MechInit

class TestSuite(unittest.TestCase):
    """integration test
    - testing the full integration of the MechInit class with Dreadnought,
    Weapon, PlayerGrid, and BadMech.
    - MechInit should create 1 player mech 1 player grid 9 enemy mechs
    and 9 enemy grids along with the 2 weapons each mech should have"""
    def test_mech_init(self):
        #create the instance of MechInit
        creationObject = MechInit()
        #these 3 asserts check that a dreadnought was created for playerMech
        #and that the dreadnought has 2 weapons
        self.assertIsInstance(creationObject.playerMech, Dreadnought)
        self.assertIsInstance(creationObject.playerMech.leftWeapon, Weapon)
        self.assertIsInstance(creationObject.playerMech.rightWeapon, Weapon)
        #this assert makes sure the playerPosition has an instance of a grid
        self.assertIsInstance(creationObject.playerPosition, PlayerGrid)
        #this checks that 9 enemy Mechs were created in an array called enemyMech
        self.assertEqual(len(creationObject.enemyMech),9)
        counter = 0
        for mech in creationObject.enemyMech:
            #these assertEquals make sure the first 3 are level one
            #the second 3 are level 2
            #and the last 3 are level 3
            if 0 <= counter <= 2:
                self.assertEqual(mech.mechLevel,1)
            if 3 <= counter <= 5:
                self.assertEqual(mech.mechLevel,2)
            if 6 <= counter <= 8:
                self.assertEqual(mech.mechLevel,3)
            counter +=1
            #this makes sure for each of the mechs in the array
            #the mech is an instance of BadMech and has two weapons
            self.assertIsInstance(mech, BadMech)
            self.assertIsInstance(mech.leftWeapon, Weapon)
            self.assertIsInstance(mech.rightWeapon, Weapon)
        #this makes sure that there was also 9 objects created in enemyPosition
        self.assertEqual(len(creationObject.enemyPosition),9)
        for spot in creationObject.enemyPosition:
            #this makes sure all the objects in the array are instances 
            #of a PLayerGrid
            self.assertIsInstance(spot, PlayerGrid)
        #these next two make sure currentEnemy and currentStage are the correct
        #starting value
        self.assertEqual(creationObject.currentEnemy,0)
        self.assertEqual(creationObject.currentStage,1)

    def test_set_level(self):
        """black box unit test
        - testing the Set_Level method of BadMech the expected functionality
        when Set_Level is called a number should be passed and if that number 
        is less then zero the function will not change the level returning -1
        with an error message. If the number is 0 or positive the method will
        set the level of the mech to that number and change values of health
        returning with a 0 and and empty string
        - if the argument passed is not a number it will not change the level
        instead returning -1 with an error string
        - this black box test will only be testing the return int and not the
        string that is passed along with just that a string is being passed"""
        mech = BadMech(1, Bolter(), Bolter())
        self.assertEqual(mech.mechLevel,1)
        #test if the level is set to 0
        returnVal, returnStr = mech.Set_Level(0)
        self.assertEqual(mech.mechLevel,0)
        self.assertEqual(returnVal,0)
        self.assertIsInstance(returnStr, str)
        #test if the level is set to a number > 0
        returnVal, returnStr = mech.Set_Level(4)
        self.assertEqual(mech.mechLevel,4)
        self.assertEqual(returnVal,0)
        self.assertIsInstance(returnStr, str)
        #test if the level is set to a number < 0
        returnVal, returnStr = mech.Set_Level(-1)
        self.assertEqual(mech.mechLevel,4)
        self.assertEqual(returnVal,-1)
        self.assertIsInstance(returnStr, str)
        #test if the level is set to a non int value
        returnVal, returnStr =mech.Set_Level('hello')
        self.assertEqual(mech.mechLevel,4)
        self.assertEqual(returnVal,-1)
        self.assertIsInstance(returnStr, str)

    def test_grid_counter(self):
        """White box unit test of the GridCounter class
        - 100% coverage of statement type.
        - initializing the class will run all statments in init. 
        - calling Update_Count with a list of 9 numbers will run all
        statements in Update_Count other than the error return. So I will then
        call Update_Count with a list that doesnt have 9 numbers.
        - calling Percent_Matrix will exercise all statments in Percent_Matrix
        which will acomplish 100% coverage of statment type"""
        grid_count = GridCounter()
        self.assertEqual(grid_count.move_num, 1)
        self.assertEqual(grid_count.space_count, [0, 0, 0, 0, 1, 0, 0, 0, 0])
        grid_count.Update_Count([0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(grid_count.move_num, 2)
        self.assertEqual(grid_count.space_count, [0, 0, 0, 1, 1, 0, 0, 0, 0])
        grid_count.Update_Count([0, 0, 0, 0, 0, 1, 0, 0])
        self.assertNotEqual(grid_count.move_num, 3)
        self.assertNotEqual(grid_count.space_count, [0, 0, 0, 1, 1, 1, 0, 0, 0])
        percent_matrix = grid_count.Percent_Matrix()
        self.assertAlmostEqual(percent_matrix[0], 3/9, places=2)
        self.assertAlmostEqual(percent_matrix[1], 3/9, places=2)
        self.assertAlmostEqual(percent_matrix[2], 3/9, places=2)
        self.assertAlmostEqual(percent_matrix[3], 3/10, places=2)
        self.assertAlmostEqual(percent_matrix[4], 3/10, places=2)
        self.assertAlmostEqual(percent_matrix[5], 3/9, places=2)
        self.assertAlmostEqual(percent_matrix[6], 3/9, places=2)
        self.assertAlmostEqual(percent_matrix[7], 3/9, places=2)
        self.assertAlmostEqual(percent_matrix[8], 3/9, places=2)
        """below is the class being tested with slight modification
        due to using multi line string in the code for the return error
        class GridCounter:
            def __init__(self):
                self.space_count = [0, 0, 0,
                                    0, 1, 0,
                                    0, 0, 0]
                self.move_num = 1
            def Update_Count(self, move):
                if (isinstance(move, list) and len(move) != 9):
                    return -1, error: expected argument of type list with lenth of 
                    9. did not recieve that"
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
        """


if __name__ == '__main__':
    unittest.main()
