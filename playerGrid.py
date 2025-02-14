class PlayerGrid:
    def __init__(self):
        #Initialize a 3x3 grid with the player in the center
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.player_position = (1, 1)  # Default to center
        self.grid[1][1] = 1  # Mark player location

    def get_player_position(self):
        #Returns the current player position as (row, col)
        return self.player_position
