class PlayerGrid:
    def __init__(self):
        #Initialize a 3x3 grid with the player in the center
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.player_position = (1, 1)  # Default to center
        self.grid[1][1] = 1  # Mark player location

    def get_player_position(self):
        #Returns the current player position as (row, col)
        return self.player_position
    def place_player(self, new_position):
        """Updates the grid with the new player position."""
        old_row, old_col = self.player_position
        self.grid[old_row][old_col] = 0  # Clear old position

        new_row, new_col = new_position
        self.grid[new_row][new_col] = 1  # Set new position
        self.player_position = new_position
