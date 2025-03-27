'''
***************************COLLABORATORS******************************
Korbin, Kyle, Kolton, James

*****************************CITATION*********************************
Game mechanic inspirtation - Slay the Spire
Graphic inspiration - WarHammer
PyGame learning - 
    Video: The ultimate introduction to Pygame, 
    Channel: Clear Code
    Link: https://youtu.be/AY9MnQ4x3zk?si=gvivndXhupNE7cak

'''
import pygame as pg
from loadBackground import load_background_image
from playerGrid import PlayerGrid
from playerMovement import PlayerMovement
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_ROWS, GRID_COLS, RED, WHITE, BLUE, GREEN
import mechInit
import enemyai
import menu
import game_state

def run_grid_game():
    pg.init()
    pg.mixer.init()
    pg.font.init()
    clock = pg.time.Clock()

    # set up the screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Rouge Dreadnaught 2025")

    gameState = game_state.GameState()
    menuController = menu.MenuController(gameState, pg, screen)

    #load music
    # music source - https://downloads.khinsider.com/game-soundtracks/album/warhammer-40k-space-marine-ost/08.%2520The%2520Blood%2520Ravens.mp3
    pg.mixer.music.load("assets/music.mp3") 
    pg.mixer.music.play(-1) 

    background_image = load_background_image('assets/backgroundFight.jpeg', SCREEN_WIDTH, SCREEN_HEIGHT)

    #end game text
    you_died_font = pg.font.SysFont('Comic Sans MS', 80)
    you_died_text = you_died_font.render('', False, (0, 0, 0))

    #enemy combat log for making sure ai is working
    enemy_logging = 1
    turn_counter = 0
    combat_log = [0] * 10
    combat_log_text = [''] * 10
    combat_font = pg.font.SysFont('Comic Sans MS', 10)

    # initialize
    player_grid = PlayerGrid()
    player_movement = PlayerMovement(player_grid)
    games_mechs = mechInit.MechInit()
    enemy_ai = enemyai.DecisionMaker(games_mechs, 1)
    enemies_turn = 0
    damage_timer = 0

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

    # load the mech image
    player_image = pg.image.load('assets/placeholder_mech_image.jpeg')
    player_image = pg.transform.scale(player_image, (int(CELL_WIDTH * 1.5), int(CELL_HEIGHT * 1.5)))

    running = True
    while running:

        # Initially load to the main menu
        if(gameState.currentState() == game_state.State.MAIN_MENU):

            # The following menuLoop will pause the while loop until the menu is exited
            # Exiting to the main menu from in game menu, will bring us back to this code block
            # We can reinitialize the appropriate variables here, so that the game can be restarted

            menuController.menuLoop(pg.event.get())
        else:
            # background
            screen.blit(background_image, (0, 0))

            #enemy combat log
            if enemy_logging:
                for i in range(9):
                    combat_log[i] = combat_font.render(combat_log_text[i], 1, WHITE)
                    screen.blit(combat_log[i], (SCREEN_WIDTH-180,(SCREEN_HEIGHT/2)-11*i))

            #color timer for damage animation
            if damage_timer:
                damage_timer -= 1

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
                        if damage_timer:
                            pg.draw.rect(screen, RED, rect.inflate(-CELL_WIDTH * 0.1, -CELL_HEIGHT * 0.1))
                        else:
                            pg.draw.rect(screen, GREEN, rect.inflate(-CELL_WIDTH * 0.1, -CELL_HEIGHT * 0.1))

            # positioning for the mech image, offset slightly to appear standing on the square
            player_row, player_col = player_grid.get_player_position()
            extra_offset = player_row * (CELL_WIDTH * 0.3)
            cell_x = player_col * CELL_WIDTH + GRID_X_OFFSET - extra_offset
            cell_y = player_row * CELL_HEIGHT + GRID_Y_OFFSET
            img_width, img_height = player_image.get_size()
            image_x = cell_x + (CELL_WIDTH - img_width) // 2
            image_y = cell_y + (CELL_HEIGHT - img_height) // 2 - 50
            screen.blit(player_image, (image_x, image_y))
            

            # grid and highlight for the enemy
            for row in range(GRID_ROWS):
                for col in range(GRID_COLS):
                    # offset for angeled grid
                    extra_offset = row * (CELL_WIDTH * .3)  
                    # shift each row
                    rect = pg.Rect(col * CELL_WIDTH + GRID_X_OFFSET + extra_offset+500,
                                row * CELL_HEIGHT + GRID_Y_OFFSET,
                                CELL_WIDTH, CELL_HEIGHT)
                    pg.draw.rect(screen, WHITE, rect, 1)  # Draw grid outline

                    # highlight player's cell if this is the current position.
                    if games_mechs.Get_Enemy_Position() == (row, col):
                        pg.draw.rect(screen, GREEN, rect.inflate(-CELL_WIDTH * 0.1, -CELL_HEIGHT * 0.1))

            # event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:

                        # On escape, bring up the in game menu

                        gameState.setMenuActive(True)
                        menuController.menuLoop(pg.event.get())

                        # running = False
                    elif event.key in KEY_TO_DIRECTION:
                        direction = KEY_TO_DIRECTION[event.key]
                        player_movement.move_player(direction)
                        #whenever the player takes a turn the enemy can take one only change
                        #enemy_turn to 1 when the enemy gets a turn
                        enemies_turn = 1
                        damage_timer = 0

                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    # check the click is within the grid
                    if (mouse_y >= GRID_Y_OFFSET and 
                        mouse_y < GRID_Y_OFFSET + CELL_HEIGHT * GRID_ROWS):
                        clicked_row = int((mouse_y - GRID_Y_OFFSET) // CELL_HEIGHT)
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
                                #whenever the player takes a turn the enemy can take one only change
                                #enemy_turn to 1 when the enemy gets a turn
                                enemies_turn = 1
                                damage_timer = 0

            #enemyai takes enemies turn
            if enemies_turn:
                action = enemy_ai.Take_Action()
                turn_counter += 1
                for i in range(9):
                    combat_log_text[9-i] = combat_log_text[8-i]
                if action == 1:
                    combat_log_text[0] = "Action "+str(turn_counter)+": The enemy is defending"
                elif action == 2:
                    combat_log_text[0] = "Action "+str(turn_counter)+": The enemy made a move"
                else:
                    combat_log_text[0] = "Action "+str(turn_counter)+": The enemy has attacked"
                    damage_timer = 20
                enemies_turn = 0
                if games_mechs.playerMech.healthPoints <= 0:
                    you_died_text = you_died_font.render('You have died!', 1, RED)
            screen.blit(you_died_text, (370,200))

            pg.display.flip()
            clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    run_grid_game()
