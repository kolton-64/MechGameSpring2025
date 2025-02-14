from playerGrid import PlayerGrid

class PlayerMovement:
    def __init__(self, player_grid):
        self.player_grid = player_grid

    def move_player(self, direction):
        """Moves player within the 3x3 grid."""
        row, col = self.player_grid.get_player_position()

        if direction == "up" and row > 0:
            row -= 1
        elif direction == "down" and row < 2:
            row += 1
        elif direction == "left" and col > 0:
            col -= 1
        elif direction == "right" and col < 2:
            col += 1

        self.player_grid.place_player((row, col))

'''how to use this
   this seems like a better solution for movement rather than having the play pick a square 
   to move to we can just have them pick a direction to move in
if __name__ == "__main__":
    pg = PlayerGrid()
    movement = PlayerMovement(pg)
    movement.move_player("right")
    print("New position:", pg.get_player_position())
'''