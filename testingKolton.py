import unittest
from playerGrid import PlayerGrid
from playerMovement import PlayerMovement

#black box unit test 
#placing the player and checking they are actually moved and updates happen
class TestPlayerGrid(unittest.TestCase):
    def test_place_player_valid(self):
        grid = PlayerGrid()  
        grid.place_player((2, 1))
        self.assertEqual(grid.get_player_position(), (2, 1))
        self.assertEqual(grid.grid[2][1], 1)
        self.assertEqual(grid.grid[1][1], 0)
        total_ones = sum(sum(1 for cell in row if cell == 1) for row in grid.grid) #should only be one 1 on the  board
        self.assertEqual(total_ones, 1)


#white box test
#my code to test
# def move_player(self, direction):
#     row, col = self.player_grid.get_player_position()
#     if direction == "up" and row > 0:
#         row -= 1
#     elif direction == "down" and row < 2:
#         row += 1
#     elif direction == "left" and col > 0:
#         col -= 1
#     elif direction == "right" and col < 2:
#         col += 1
#     self.player_grid.place_player((row, col))

# tests if the player provides input to move outside the grid that they don't actually move.
# starts with the player in the top left corner then tests moving up and down. Then it tests if moving right
#works correctly. Then test to make sure the grid is updated to be emtpy where the player moves from
class TestPlayerMovement(unittest.TestCase):
    def test_move_player_edge(self):
        grid = PlayerGrid()
        movement = PlayerMovement(grid)
        grid.place_player((0, 0))
        movement.move_player("up") 
        self.assertEqual(grid.get_player_position(), (0, 0))
        movement.move_player("left")
        self.assertEqual(grid.get_player_position(), (0, 0))
        movement.move_player("right")
        self.assertEqual(grid.get_player_position(), (0, 1))
        self.assertEqual(grid.grid[0][1], 1)
        self.assertEqual(grid.grid[0][0], 0)

#integrations tests
#tests updating the player grid and the click logic for tracking clicking movement
class TestIntegration(unittest.TestCase):
    def test_click_to_move(self):
        GRID_X_OFFSET = 100
        GRID_Y_OFFSET = 100
        CELL_WIDTH = 50
        CELL_HEIGHT = 50

        grid = PlayerGrid()
        grid.place_player((1, 1))

        mouse_x = GRID_X_OFFSET + 2 * CELL_WIDTH + (CELL_WIDTH // 2)
        mouse_y = GRID_Y_OFFSET + 1 * CELL_HEIGHT + (CELL_HEIGHT // 2)

        clicked_col = int((mouse_x - GRID_X_OFFSET) // CELL_WIDTH)
        clicked_row = int((mouse_y - GRID_Y_OFFSET) // CELL_HEIGHT)

        self.assertEqual(clicked_row, 1)
        self.assertEqual(clicked_col, 2)

        current_row, current_col = grid.get_player_position()
        if (abs(clicked_row - current_row) <= 1 and 
            abs(clicked_col - current_col) <= 1 and 
            not (clicked_row == current_row and clicked_col == current_col)):
            grid.place_player((clicked_row, clicked_col))
        
        self.assertEqual(grid.get_player_position(), (1, 2))
        self.assertEqual(len(grid.grid), 3)
        self.assertEqual(len(grid.grid[0]), 3)

if __name__ == '__main__':
    unittest.main()
