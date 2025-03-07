
import pygame as pg
from loadBackground import load_background_image
from playerGrid import PlayerGrid
from playerMovement import PlayerMovement
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_ROWS, GRID_COLS, WHITE, BLUE, GREEN

def run_grid_game():
    pg.init()
    pg.mixer.init()
    clock = pg.time.Clock()

    # set up the screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Rouge Dreadnaught 2025")

    #load music
    # music source - https://downloads.khinsider.com/game-soundtracks/album/warhammer-40k-space-marine-ost/08.%2520The%2520Blood%2520Ravens.mp3
    pg.mixer.music.load("assets/music.mp3") 
    pg.mixer.music.play(-1) 

    background_image = load_background_image('assets/backgroundFight.jpeg', SCREEN_WIDTH, SCREEN_HEIGHT)

    # initialize
    player_grid = PlayerGrid()
    player_movement = PlayerMovement(player_grid)

    # cast to int for the click detections
    CELL_WIDTH = int((SCREEN_WIDTH // GRID_COLS) // 3)
    CELL_HEIGHT = int((SCREEN_HEIGHT // GRID_ROWS) // 2.5)

    #offsets that work best for my screen
    GRID_X_OFFSET = 160
    GRID_Y_OFFSET = 385

    # arrow key assigning
    KEY_TO_DIRECTION = {
        pg.K_UP: "up",
        pg.K_DOWN: "down",
        pg.K_LEFT: "left",
        pg.K_RIGHT: "right"
    }

    running = True
    while running:
        # background
        screen.blit(background_image, (0, 0))

        # grid and highlight
        # Inside your main game loop for drawing:
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                # offset for angeled grid
                extra_offset = row * (CELL_WIDTH * 0.3)  
                # shift each row
                rect = pg.Rect(col * CELL_WIDTH + GRID_X_OFFSET - extra_offset,
                               row * CELL_HEIGHT + GRID_Y_OFFSET,
                               CELL_WIDTH, CELL_HEIGHT)
                pg.draw.rect(screen, WHITE, rect, 1)  # Draw grid outline

                # highlight player's cell if this is the current position.
                if player_grid.get_player_position() == (row, col):
                    pg.draw.rect(screen, GREEN, rect.inflate(-CELL_WIDTH * 0.1, -CELL_HEIGHT * 0.1))

        # event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key in KEY_TO_DIRECTION:
                    direction = KEY_TO_DIRECTION[event.key]
                    player_movement.move_player(direction)

            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                # check the click is within the grid
                if (mouse_y >= GRID_Y_OFFSET and 
                    mouse_y < GRID_Y_OFFSET + CELL_HEIGHT * GRID_ROWS):
                    
                    clicked_row = int((mouse_y - GRID_Y_OFFSET) // CELL_HEIGHT)
                    # adjust with offset
                    adjusted_mouse_x = mouse_x - GRID_X_OFFSET + (clicked_row * (CELL_WIDTH * 0.3))
                    
                    if adjusted_mouse_x >= 0 and adjusted_mouse_x < CELL_WIDTH * GRID_COLS:
                        clicked_col = int(adjusted_mouse_x // CELL_WIDTH)
                        
                        # get position
                        player_row, player_col = player_grid.get_player_position()

                        # allow if adjacent or diagonal
                        if (abs(clicked_row - player_row) <= 1 and 
                            abs(clicked_col - player_col) <= 1 and 
                            not (clicked_row == player_row and clicked_col == player_col)):
                            player_grid.place_player((clicked_row, clicked_col))


        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    run_grid_game()
