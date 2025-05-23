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
import random
import math
from loadBackground import load_background_image
from playerGrid import PlayerGrid
from playerMovement import PlayerMovement
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_ROWS, GRID_COLS, RED, WHITE, BLUE, GREEN, ORANGE, TOP_BAR_HEIGHT
import mechInit
import enemyai
import menu
import game_state
from weapons import Bolter, MeleeWeapon1, AOEWeapon1, HeavyFlamer, ChainFist, MultiMelta,LasCannon, AssaultCannon, FragMissileLauncher
from attack_zone_dynamic_change import get_adjusted_attack_zone


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
    enemy_attack_pattern = 0
    player_act_seq = [0]*3

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
    enemy_image = pg.image.load('assets/placeholder_mech_image_reverse.jpeg')
    enemy_image = pg.transform.scale(enemy_image, (int(CELL_WIDTH * 1.5), int(CELL_HEIGHT * 1.5)))

    #randomly selected the primary and secondary weapons for the mech player, they will be unique
    available_weapons = [Bolter(), MeleeWeapon1(), AOEWeapon1(),AssaultCannon(),LasCannon(), HeavyFlamer(), MultiMelta(), FragMissileLauncher(),ChainFist()]
    selected_weapons = random.sample(available_weapons, 2)
    primary_weapon = selected_weapons[0]
    secondary_weapon = selected_weapons[1]

    # Two attack buttons for the mech's left and right weapons.
    btn_w, btn_h = 180, 60
    pad = (TOP_BAR_HEIGHT - btn_h) // 2
    PRIMARY_ATTACK_BTN_RECT   = pg.Rect( 350,pad, btn_w, btn_h)
    SECONDARY_ATTACK_BTN_RECT = pg.Rect(550,pad, btn_w, btn_h)
    # Defend button
    DEFEND_BTN_RECT= pg.Rect(750,pad, btn_w, btn_h)
    
    primary_attack_font = pg.font.SysFont('Comic Sans MS', 24)
    secondary_attack_font = pg.font.SysFont('Comic Sans MS', 24)
    defend_font = pg.font.SysFont('Comic Sans MS', 24)

    is_player_turn = True
    action_points = 2

    hover_weapon = None

    running = True
    while running:

        # Initially load to the main menu
        if(gameState.currentState() == game_state.State.MAIN_MENU):
            print("MAIN MENU")

            # The following menuLoop will pause the while loop until the menu is exited
            # Exiting to the main menu from in game menu, will bring us back to this code block
            # We can reinitialize the appropriate variables here, so that the game can be restarted

            menuController.menuLoop(pg.event.get())

            # Must reinitialize game every time we go back to the main menu
            # Reinitialize game elements
            player_grid = PlayerGrid()
            player_movement = PlayerMovement(player_grid)
            games_mechs = mechInit.MechInit()
            enemy_ai = enemyai.DecisionMaker(games_mechs, 1)
            enemies_turn = 0
            damage_timer = 0
            enemy_attack_pattern = 0

            # reset enemy logging 
            enemy_logging = 1
            turn_counter = 0
            combat_log = [0] * 10
            combat_log_text = [''] * 10
            combat_font = pg.font.SysFont('Comic Sans MS', 10)


            #update mechs with current difficulty
            enemy_ai.Update_Difficulty(gameState.getDifficulty())



        elif gameState.currentState() == game_state.State.GAME_OVER:
            print("GAME OVER!!")
            menuController.menuLoop(pg.event.get())

        else:
            # background
            screen.blit(background_image, (0, 0))

            top_bar_rect = pg.Rect(
                0,
                0,
                SCREEN_WIDTH,
                TOP_BAR_HEIGHT
            )
            screen.fill((0, 0, 0), top_bar_rect)


            #enemy combat log
            if enemy_logging:
                for i in range(9):
                    combat_log[i] = combat_font.render(combat_log_text[i], 1, WHITE)
                    screen.blit(combat_log[i], (SCREEN_WIDTH-210,(SCREEN_HEIGHT/3)-11*i))

            #color timer for damage animation
            if damage_timer:
                damage_timer -= 1

            # grid and highlight
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

            #show the damage pattern
            if damage_timer:
                for spot in enemy_attack_pattern:
                    #flash orange for enemy attack pattern
                    for row in range(GRID_ROWS):
                        for col in range(GRID_COLS):
                            extra_offset = row * (CELL_WIDTH * 0.3)  
                            rect = pg.Rect(col * CELL_WIDTH + GRID_X_OFFSET - extra_offset,
                                        row * CELL_HEIGHT + GRID_Y_OFFSET,
                                        CELL_WIDTH, CELL_HEIGHT)
                            if spot == (row, col):
                                pg.draw.rect(screen, ORANGE, rect.inflate(-CELL_WIDTH * 0.1, -CELL_HEIGHT * 0.1))

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

                    # highlight enemies's cell if this is the current position.
                    if games_mechs.Get_Enemy_Position() == (row, col):
                        pg.draw.rect(screen, RED, rect.inflate(-CELL_WIDTH * 0.1, -CELL_HEIGHT * 0.1))

            # positioning for the enemy mech image same as above but reverse
            enemy_row, enemy_col = games_mechs.Get_Enemy_Position()
            extra_offset = enemy_row * (CELL_WIDTH * 0.3) + 500
            cell_x = enemy_col * CELL_WIDTH + GRID_X_OFFSET + extra_offset
            cell_y = enemy_row * CELL_HEIGHT + GRID_Y_OFFSET
            img_width, img_height = enemy_image.get_size()
            image_x = cell_x + (CELL_WIDTH - img_width) // 2
            image_y = cell_y + (CELL_HEIGHT - img_height) // 2 - 50
            screen.blit(enemy_image, (image_x, image_y))


            # draw the attack buttons for left and right 'hand'
            if is_player_turn:
                # Draw Primary Attack button
                pg.draw.rect(screen, BLUE, PRIMARY_ATTACK_BTN_RECT)
                primary_attack_text = primary_attack_font.render("Left Attack", True, WHITE)
                primary_text_rect = primary_attack_text.get_rect(center=PRIMARY_ATTACK_BTN_RECT.center)
                screen.blit(primary_attack_text, primary_text_rect)
                # Draw Secondary Attack button
                pg.draw.rect(screen, BLUE, SECONDARY_ATTACK_BTN_RECT)
                secondary_attack_text = secondary_attack_font.render("Right Attack", True, WHITE)
                secondary_text_rect = secondary_attack_text.get_rect(center=SECONDARY_ATTACK_BTN_RECT.center)
                screen.blit(secondary_attack_text, secondary_text_rect)
                # Draw Defend bytton
                pg.draw.rect(screen, BLUE, DEFEND_BTN_RECT)
                defend_text = defend_font.render("Defend", True, WHITE)
                defend_text_rect = defend_text.get_rect(center=DEFEND_BTN_RECT.center)
                screen.blit(defend_text, defend_text_rect)


            #hovering your mouse over a weapon attack button will now highlight the attack zone of that weapon based off your position
            hover_weapon = None
            mx, my = pg.mouse.get_pos()
            if PRIMARY_ATTACK_BTN_RECT.collidepoint(mx, my):
                hover_weapon = "primary"
            elif SECONDARY_ATTACK_BTN_RECT.collidepoint(mx, my):
                hover_weapon = "secondary"
            else:
                hover_weapon = None
            if hover_weapon is not None:
                if hover_weapon == "primary":
                    base_attack_zone = primary_weapon.getWeaponAttackZoneOptions()[0]
                elif hover_weapon == "secondary":
                    base_attack_zone = secondary_weapon.getWeaponAttackZoneOptions()[0]
                player_pos = player_grid.get_player_position()
                adjusted_attack_zone = get_adjusted_attack_zone(base_attack_zone, player_pos, default_position=(1,1))
                for (r, c) in adjusted_attack_zone:
                    extra_offset = r * (CELL_WIDTH * 0.3)
                    enemy_rect = pg.Rect(c * CELL_WIDTH + GRID_X_OFFSET + extra_offset + 500,
                                         r * CELL_HEIGHT + GRID_Y_OFFSET,
                                         CELL_WIDTH, CELL_HEIGHT)
                    pg.draw.rect(screen, ORANGE, enemy_rect.inflate(-CELL_WIDTH * 0.1, -CELL_HEIGHT * 0.1))
            
            # event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if is_player_turn:
                        if event.key == pg.K_ESCAPE:
                            # Bring up pause menu without exiting
                            gameState.setMenuActive(True)
                            menuController.menuLoop(pg.event.get())
                        elif event.key in KEY_TO_DIRECTION:
                            if action_points > 0:
                                direction = KEY_TO_DIRECTION[event.key]
                                player_movement.move_player(direction)
                                player_act_seq[0] += 1
                                action_points -= 1  # consume 1 action point for movement
                                if action_points == 0:
                                    is_player_turn = False
                                    enemies_turn = 1
                                    damage_timer = 0
                        elif event.key == pg.K_SPACE:
                            # End turn early if Space is pressed
                            is_player_turn = False
                            enemies_turn = 1
                            damage_timer = 0

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if is_player_turn:
                        mouse_x, mouse_y = pg.mouse.get_pos()
                        # attack button clicked
                        if PRIMARY_ATTACK_BTN_RECT.collidepoint(mouse_x, mouse_y):
                            if action_points > 0:
                                print("Left Hand Attack action performed.")
                                action_points -= 1
                                enemy_pos = games_mechs.Get_Enemy_Position()
                                base_attack_zone = primary_weapon.getWeaponAttackZoneOptions()[0]
                                player_pos = player_grid.get_player_position()
                                adjusted_attack_zone = get_adjusted_attack_zone(base_attack_zone, player_pos, default_position=(1,1))
                                if enemy_pos in adjusted_attack_zone:
                                    games_mechs.enemyMech[0].takeDamage(primary_weapon.damage)
                                if action_points == 0:
                                    is_player_turn = False
                                    enemies_turn = 1
                                    damage_timer = 0
                        elif SECONDARY_ATTACK_BTN_RECT.collidepoint(mouse_x, mouse_y):
                            if action_points > 0:
                                print("Right Hand Attack action performed.")
                                action_points -= 1
                                enemy_pos = games_mechs.Get_Enemy_Position()
                                base_attack_zone = secondary_weapon.getWeaponAttackZoneOptions()[0]
                                player_pos = player_grid.get_player_position()
                                adjusted_attack_zone = get_adjusted_attack_zone(base_attack_zone, player_pos, default_position=(1,1))
                                if enemy_pos in adjusted_attack_zone:
                                    games_mechs.enemyMech[0].takeDamage(secondary_weapon.damage)
                                if action_points == 0:
                                    is_player_turn = False
                                    enemies_turn = 1
                                    damage_timer = 0
                        # defend button clicked
                        elif DEFEND_BTN_RECT.collidepoint(mouse_x, mouse_y):
                            if action_points > 0:
                                print("Defend action performed.")
                                player_act_seq[1] += 1
                                action_points -= 1
                                if action_points == 0:
                                    is_player_turn = False
                                    enemies_turn = 1
                                    damage_timer = 0
                        else:
                            # check the click is within the grid
                            if (mouse_y >= GRID_Y_OFFSET and 
                                mouse_y < GRID_Y_OFFSET + CELL_HEIGHT * GRID_ROWS):
                                clicked_row = int((mouse_y - GRID_Y_OFFSET) // CELL_HEIGHT)
                                adjusted_mouse_x = mouse_x - GRID_X_OFFSET + (clicked_row * (CELL_WIDTH * 0.3))
                                if adjusted_mouse_x >= 0 and adjusted_mouse_x < CELL_WIDTH * GRID_COLS:
                                    clicked_col = int(adjusted_mouse_x // CELL_WIDTH)
                                    # get position
                                    current_row, current_col = player_grid.get_player_position()
                                    # allow if adjacent or diagonal
                                    if (abs(clicked_row - current_row) <= 1 and 
                                        abs(clicked_col - current_col) <= 1 and 
                                        not (clicked_row == current_row and clicked_col == current_col)):
                                        if action_points > 0:
                                            player_grid.place_player((clicked_row, clicked_col))
                                            action_points -= 1
                                            if action_points == 0:
                                                is_player_turn = False
                                                enemies_turn = 1
                                                damage_timer = 0


            #enemyai takes enemies turn
            if not is_player_turn and enemies_turn:
                games_mechs.playerPosition.player_position = player_grid.get_player_position()
                first_a = enemy_ai.Take_Action()
                second_a = enemy_ai.Take_Action()
                enemy_attack_pattern = []
                try:
                    for attack in first_a:
                        enemy_attack_pattern.append(attack)
                except:
                    pass
                try:
                    for attack in second_a:
                        enemy_attack_pattern.append(attack)
                except:
                    pass
                turn_counter += 1
                for i in range(9):
                    combat_log_text[9-i] = combat_log_text[8-i]
                combat_log_text[0], enemy_actions = enemyai.combat_log_text(first_a,
                                                             second_a, turn_counter)
                if enemy_actions[2]:
                    damage_timer = 20

                enemies_turn = 0
                c_enemy = games_mechs.enemyMech[games_mechs.Get_Current_Enemy()]
                while player_act_seq[2]:
                    c_enemy.takeDamage(games_mechs.playerMech.leftWeapon.damage)
                    player_act_seq[2] -= 1
                is_player_turn = True #reset players turn
                #refresh players actions
                player_act_seq = [0]*3
                action_points = 2
                if games_mechs.playerMech.healthPoints <= 0:
                    #player has died
                    gameState.setGameOver(True)
                    gameState.setMenuActive(True)
                    menuController.stage = 2

                    # reinitialize game elements
                    player_grid = PlayerGrid()
                    player_movement = PlayerMovement(player_grid)
                    games_mechs = mechInit.MechInit()
                    enemy_ai = enemyai.DecisionMaker(games_mechs, 1)
                    enemies_turn = 0
                    damage_timer = 0
                    enemy_attack_pattern = 0

                    # reset enemy logging 

                    enemy_logging = 1
                    turn_counter = 0
                    combat_log = [0] * 10
                    combat_log_text = [''] * 10
                    combat_font = pg.font.SysFont('Comic Sans MS', 10)

                    # you_died_text = you_died_font.render('You have died!', 1, RED)
            screen.blit(you_died_text, (370,200))

            pg.display.flip()
            clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    run_grid_game()
